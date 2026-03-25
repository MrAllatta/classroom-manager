#!/usr/bin/env python3
"""
Directory Executor — minimal, robust file-based task executor.

Watches a handoffs/ directory for task JSON files, marks them as running,
executes a lightweight generic operation, and writes results and deliverables
to appropriate folders using atomic writes.

Usage:
    python executor.py [--handoffs-dir DIR] [--results-dir DIR] 
                       [--deliverables-dir DIR] [--tmp-dir DIR]
                       [--poll-interval SECONDS] [--watch | --no-watch]
                       [--log-file FILE]

Directory layout:
    handoffs/         input task files (task-<TASK_ID>.json)
    results/          output result files (result-<TASK_ID>.json)
    deliverables/     produced outputs (e.g., outline.md)
    tmp/              atomic write staging area

Task JSON format (minimal):
    {
      "task_id": "T-0001",
      "goal": "Create outline",
      "deliverables": ["outline.md"],
      "plan": {...},          # optional
      "constraints": {...},   # optional
      "timeout_seconds": 600  # optional, default 600
    }

Status lifecycle: queued → running → done (or failed)
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(log_file: Optional[str] = None) -> logging.Logger:
    """Configure logging to stdout and optionally to a file."""
    logger = logging.getLogger("executor")
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# ============================================================================
# Atomic Write Utilities
# ============================================================================

def atomic_write_json(file_path: Path, data: Dict[str, Any], tmp_dir: Path) -> None:
    """
    Atomically write JSON to file_path using tmp_dir for staging.
    
    Pattern:
    1. Write to tmp/<basename>.tmp
    2. Rename atomically to target file_path
    
    This ensures no partial writes if the process crashes mid-write.
    """
    tmp_file = tmp_dir / f"{file_path.name}.tmp"
    
    # Ensure tmp directory exists
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    # Write to temporary file
    with open(tmp_file, "w") as f:
        json.dump(data, f, indent=2)
    
    # Atomic rename
    tmp_file.replace(file_path)


def read_json(file_path: Path) -> Optional[Dict[str, Any]]:
    """Safely read and parse a JSON file. Return None if invalid."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return None


# ============================================================================
# Task Validation
# ============================================================================

def validate_task(task: Dict[str, Any], task_id: str, logger: logging.Logger) -> Optional[str]:
    """
    Validate task structure. Return error message if invalid; None if valid.
    
    Required fields: task_id, goal, deliverables
    """
    required = ["task_id", "goal", "deliverables"]
    for field in required:
        if field not in task:
            return f"Missing required field: {field}"
    
    if not isinstance(task["deliverables"], list):
        return "deliverables must be a list"
    
    if not task["deliverables"]:
        return "deliverables list cannot be empty"
    
    return None


# ============================================================================
# Task Execution
# ============================================================================

def execute_task(
    task: Dict[str, Any],
    deliverables_dir: Path,
    logger: logging.Logger
) -> tuple[bool, str, Dict[str, str]]:
    """
    Execute a task by creating deliverables.
    
    Returns: (success: bool, summary: str, deliverables_map: dict)
    """
    task_id = task["task_id"]
    goal = task["goal"]
    plan = task.get("plan", {})
    constraints = task.get("constraints", {})
    deliverables_list = task["deliverables"]
    
    # Ensure deliverables directory exists
    deliverables_dir.mkdir(parents=True, exist_ok=True)
    
    deliverables_map = {}
    created_files = []
    
    try:
        for deliverable_name in deliverables_list:
            deliverable_path = deliverables_dir / deliverable_name
            
            # Create parent directories if needed
            deliverable_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate simple content based on file type
            if deliverable_name.endswith(".md"):
                content = _generate_markdown_content(task_id, goal, plan, constraints)
            else:
                content = _generate_generic_content(task_id, goal)
            
            # Write deliverable
            with open(deliverable_path, "w") as f:
                f.write(content)
            
            created_files.append(deliverable_path)
            deliverables_map[deliverable_name] = str(deliverable_path)
            logger.info(f"Created deliverable: {deliverable_path}")
        
        # Validate all deliverables exist
        for deliverable_name in deliverables_list:
            expected_path = deliverables_dir / deliverable_name
            if not expected_path.exists():
                return (
                    False,
                    f"Deliverable {deliverable_name} was not created",
                    {}
                )
        
        summary = f"Successfully generated {len(deliverables_list)} deliverable(s) for task {task_id}"
        logger.info(summary)
        return (True, summary, deliverables_map)
    
    except Exception as e:
        error_msg = f"Error executing task {task_id}: {str(e)}"
        logger.error(error_msg)
        return (False, error_msg, {})


def _generate_markdown_content(
    task_id: str,
    goal: str,
    plan: Any,
    constraints: Any
) -> str:
    """Generate markdown deliverable content."""
    lines = [
        f"# Task {task_id}",
        "",
        f"## Goal",
        goal,
        "",
    ]
    
    if plan:
        lines.extend([
            "## Plan",
            json.dumps(plan, indent=2) if isinstance(plan, dict) else str(plan),
            "",
        ])
    
    if constraints:
        lines.extend([
            "## Constraints",
            json.dumps(constraints, indent=2) if isinstance(constraints, dict) else str(constraints),
            "",
        ])
    
    lines.extend([
        "---",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        f"Task ID: {task_id}",
    ])
    
    return "\n".join(lines)


def _generate_generic_content(task_id: str, goal: str) -> str:
    """Generate generic text deliverable content."""
    return f"""Task ID: {task_id}
Goal: {goal}
Generated at: {datetime.now(timezone.utc).isoformat()}
"""


# ============================================================================
# Status Management
# ============================================================================

def set_task_status(
    task_file: Path,
    status: str,
    tmp_dir: Path,
    logger: logging.Logger
) -> None:
    """
    Update task status atomically.
    
    Reads current task, updates status and timestamp, writes back atomically.
    """
    task = read_json(task_file)
    if not task:
        logger.error(f"Cannot update status: failed to read {task_file}")
        return
    
    task["status"] = status
    task["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    atomic_write_json(task_file, task, tmp_dir)
    logger.info(f"Task {task.get('task_id')} status: {status}")


def is_task_timed_out(task: Dict[str, Any]) -> bool:
    """Check if a running task has exceeded its timeout."""
    if task.get("status") != "running":
        return False
    
    timeout_seconds = task.get("timeout_seconds", 600)
    
    # Parse the timestamp when task was marked running
    updated_at_str = task.get("updated_at")
    if not updated_at_str:
        return False
    
    try:
        updated_at = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))
        elapsed = (datetime.now(timezone.utc) - updated_at).total_seconds()
        return elapsed > timeout_seconds
    except (ValueError, AttributeError):
        return False


# ============================================================================
# Main Executor Logic
# ============================================================================

def process_tasks(
    handoffs_dir: Path,
    results_dir: Path,
    deliverables_dir: Path,
    tmp_dir: Path,
    logger: logging.Logger
) -> int:
    """
    Discover and process all tasks in handoffs_dir.
    
    Returns: count of tasks processed
    """
    if not handoffs_dir.exists():
        logger.warning(f"Handoffs directory does not exist: {handoffs_dir}")
        return 0
    
    task_files = sorted(handoffs_dir.glob("task-*.json"))
    logger.info(f"Found {len(task_files)} task file(s)")
    
    processed = 0
    
    for task_file in task_files:
        task = read_json(task_file)
        
        if not task:
            logger.error(f"Invalid JSON in {task_file.name}, skipping")
            continue
        
        task_id = task.get("task_id", "UNKNOWN")
        status = task.get("status", "queued")
        
        # Skip completed tasks
        if status == "done":
            logger.debug(f"Task {task_id} already done, skipping")
            continue
        
        # Check for timeout on running tasks
        if status == "running" and is_task_timed_out(task):
            logger.warning(f"Task {task_id} exceeded timeout, marking as failed")
            result = {
                "task_id": task_id,
                "status": "failed",
                "summary": "Task exceeded timeout",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "version": task.get("version", 1),
                "error": "Task did not complete within timeout_seconds"
            }
            results_dir.mkdir(parents=True, exist_ok=True)
            atomic_write_json(results_dir / f"result-{task_id}.json", result, tmp_dir)
            continue
        
        # Validate task
        validation_error = validate_task(task, task_id, logger)
        if validation_error:
            logger.error(f"Task {task_id} validation failed: {validation_error}")
            result = {
                "task_id": task_id,
                "status": "failed",
                "summary": f"Validation failed: {validation_error}",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "version": task.get("version", 1),
                "error": validation_error
            }
            results_dir.mkdir(parents=True, exist_ok=True)
            atomic_write_json(results_dir / f"result-{task_id}.json", result, tmp_dir)
            continue
        
        # Mark as running
        logger.info(f"Processing task {task_id}")
        set_task_status(task_file, "running", tmp_dir, logger)
        
        # Execute task
        success, summary, deliverables_map = execute_task(task, deliverables_dir, logger)
        
        # Write result
        result = {
            "task_id": task_id,
            "status": "done" if success else "failed",
            "summary": summary,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "version": task.get("version", 1)
        }
        
        if success:
            result["deliverables"] = deliverables_map
        else:
            result["error"] = summary
        
        results_dir.mkdir(parents=True, exist_ok=True)
        atomic_write_json(results_dir / f"result-{task_id}.json", result, tmp_dir)
        
        # Mark task as done only on success
        if success:
            set_task_status(task_file, "done", tmp_dir, logger)
        
        processed += 1
    
    return processed


def run_executor(
    handoffs_dir: Path,
    results_dir: Path,
    deliverables_dir: Path,
    tmp_dir: Path,
    poll_interval: float,
    watch: bool,
    logger: logging.Logger
) -> int:
    """
    Main executor loop.
    
    In watch mode: loop indefinitely with poll_interval.
    In run-once mode: process all tasks and exit.
    
    Returns: exit code (0 on success)
    """
    logger.info("Executor starting")
    logger.info(f"Handoffs: {handoffs_dir}")
    logger.info(f"Results: {results_dir}")
    logger.info(f"Deliverables: {deliverables_dir}")
    logger.info(f"Mode: {'watch' if watch else 'run-once'}")
    
    try:
        if watch:
            # Watch mode: loop indefinitely
            while True:
                try:
                    process_tasks(handoffs_dir, results_dir, deliverables_dir, tmp_dir, logger)
                    time.sleep(poll_interval)
                except KeyboardInterrupt:
                    logger.info("Executor interrupted by user")
                    return 0
        else:
            # Run-once mode
            process_tasks(handoffs_dir, results_dir, deliverables_dir, tmp_dir, logger)
            return 0
    
    except Exception as e:
        logger.error(f"Unrecoverable error: {e}", exc_info=True)
        return 1


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Directory Executor — file-based task executor"
    )
    parser.add_argument(
        "--handoffs-dir",
        default="./handoffs",
        help="Directory containing task JSON files (default: ./handoffs)"
    )
    parser.add_argument(
        "--results-dir",
        default="./results",
        help="Directory for result JSON files (default: ./results)"
    )
    parser.add_argument(
        "--deliverables-dir",
        default="./deliverables",
        help="Directory for produced deliverables (default: ./deliverables)"
    )
    parser.add_argument(
        "--tmp-dir",
        default="./tmp",
        help="Directory for atomic write staging (default: ./tmp)"
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=1.0,
        help="Polling interval in seconds (default: 1.0)"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        default=True,
        help="Watch mode: loop indefinitely (default)"
    )
    parser.add_argument(
        "--no-watch",
        dest="watch",
        action="store_false",
        help="Run-once mode: process all tasks and exit"
    )
    parser.add_argument(
        "--log-file",
        help="Optional persistent log file"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.log_file)
    
    # Run executor
    handoffs_dir = Path(args.handoffs_dir)
    results_dir = Path(args.results_dir)
    deliverables_dir = Path(args.deliverables_dir)
    tmp_dir = Path(args.tmp_dir)
    
    exit_code = run_executor(
        handoffs_dir,
        results_dir,
        deliverables_dir,
        tmp_dir,
        args.poll_interval,
        args.watch,
        logger
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
