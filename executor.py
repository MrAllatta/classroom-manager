#!/usr/bin/env python3
"""
Directory Executor — minimal, robust file-based task executor.

Watches a handoffs/ directory for task JSON files, marks them as running,
executes tasks using LLM API calls with model routing, and writes results 
and deliverables to appropriate folders using atomic writes.

Usage:
    python executor.py [--handoffs-dir DIR] [--results-dir DIR] 
                       [--deliverables-dir DIR] [--tmp-dir DIR]
                       [--poll-interval SECONDS] [--watch | --no-watch]
                       [--log-file FILE]

Environment:
    ANTHROPIC_API_KEY  Required for LLM API calls

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
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import anthropic
except ImportError:
    print("Error: 'anthropic' library not installed. Install with: pip install anthropic")
    sys.exit(1)


# ============================================================================
# Role Specification Loading
# ============================================================================

ROLE_SPECS_DIR = Path(__file__).parent / "docs" / "roles"

# Mapping from task ID prefix to role spec file
ROLE_FILE_MAP = {
    "plan": "planner.md",
    "currdes": "curriculum_designer.md", 
    "assess": "assessor.md",
    "comms": "communicator.md",
}



def get_role_prefix(task_id: str) -> str:
    """Extract role prefix from task_id (e.g., PLAN-CALENDAR -> 'plan')."""
    try:
        return task_id.split("-")[0].lower()
    except (IndexError, AttributeError):
        return ""


def load_role_spec(role_prefix: str) -> Optional[str]:
    """Load role spec markdown. Returns text or None if not found."""
    if not role_prefix:
        return None
    
    # Map role prefix to actual filename
    filename = ROLE_FILE_MAP.get(role_prefix)
    if not filename:
        return None
    
    spec_file = ROLE_SPECS_DIR / filename
    try:
        with open(spec_file, "r") as f:
            return f.read()
    except (FileNotFoundError, IOError):
        return None


# ============================================================================

MODEL_MAP = {
    "CURRDES": "claude-sonnet-4-6",   # complex reasoning, standards knowledge
    "PLAN":    "claude-haiku-4-5-20251001",    # structured calendar math, cheap
    "ASSESS":  "claude-sonnet-4-6",   # data analysis, nuanced judgment
    "COMMS":   "claude-haiku-4-5-20251001",    # templated drafting, cheap
}

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

def get_llm_client() -> anthropic.Anthropic:
    """
    Initialize Anthropic client from environment API key.
    
    Raises ValueError if ANTHROPIC_API_KEY is not set.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable not set. "
            "Please set your API key before running the executor."
        )
    return anthropic.Anthropic(api_key=api_key)


def select_model_for_task(task_id: str) -> str:
    """Select appropriate model based on task type."""
    try:
        role_prefix = task_id.split("-")[0]
        return MODEL_MAP.get(role_prefix, DEFAULT_MODEL)
    except (IndexError, AttributeError):
        return DEFAULT_MODEL


def load_school_context(data_dir: Path = Path("data")) -> Optional[str]:
    """
    Load minimal school/classroom identity context.
    
    Returns a ~200 token header injected into every prompt:
    - School name
    - Student population note  
    - Teacher name
    - Course (if in task)
    
    This is the stable "always on" context that grounds all work.
    """
    school_file = data_dir / "school" / "context.yaml"
    
    if not school_file.exists():
        return None
    
    try:
        with open(school_file, "r") as f:
            lines = []
            for line in f:
                lines.append(line.rstrip())
            
            # Simple YAML extraction (sufficient for school context)
            school_header = "\n".join(lines[:20])  # First ~20 lines
            return school_header
    except IOError:
        return None


def load_curriculum_context(
    task: Dict[str, Any],
    deliverables_dir: Path = Path("deliverables")
) -> Optional[str]:
    """
    Returns None if not applicable (e.g., ASSESS, COMMS tasks).
    """
    # Extract from multiple locations in task structure
    course = task.get("course")  
    if not course:
        course = task.get("constraints", {}).get("course")
    if course == "Algebra I":
        course = "ALG1"
    
    unit = task.get("unit")
    if unit is None:
        unit = task.get("plan", {}).get("unit_number")
    if unit is None:
        unit = task.get("plan", {}).get("context", {}).get("unit_number")
    
    week = task.get("week")
    if week is None:
        week = task.get("plan", {}).get("week_number")
    if week is None:
        week = task.get("constraints", {}).get("week")
    
    # Curriculum context only applies to tasks with course/unit
    if not course:
        return None
    
    # ...existing code...
    
    try:
        with open(scope_file, "r") as f:
            scope = json.load(f)
        with open(calendar_file, "r") as f:
            calendar = json.load(f)
        
        # Find the relevant unit in scope
        units = scope.get("units", [])
        calendar_units = calendar.get("units", [])
        
        # If unit number is specified, use it; otherwise infer from week
        if unit is not None:
            unit_num = unit
        elif week is not None:
            # Infer unit from week number
            unit_num = _infer_unit_from_week(week, calendar_units)
            if unit_num is None:
                return None
        else:
            return None
        
        # Find matching unit in both scope and calendar
        scope_unit = next(
            (u for u in units if u.get("unit") == unit_num),
            None
        )
        calendar_unit = next(
            (u for u in calendar_units if u.get("unit") == unit_num),
            None
        )
        
        if not scope_unit or not calendar_unit:
            return None
        
        # Build context snippet (~200 tokens)
        lines = []
        lines.append(f"# Unit {unit_num}: {scope_unit.get('title', 'Unit ' + str(unit_num))}")
        lines.append("")
        
        # Standards
        standards = scope_unit.get("standards", [])
        if standards:
            lines.append("## Standards")
            for std in standards[:8]:  # Limit to first 8
                lines.append(f"- {std}")
            lines.append("")
        
        # Timeline
        lines.append("## Timeline")
        lines.append(f"Start: {calendar_unit.get('start_date', 'TBD')}")
        lines.append(f"End: {calendar_unit.get('end_date', 'TBD')}")
        lines.append(f"Instructional Days: {calendar_unit.get('instructional_days', '?')}")
        lines.append("")
        
        # Content snapshot
        content = scope_unit.get("content", [])
        if content:
            lines.append("## Key Content")
            for item in content[:5]:  # Limit to first 5 items
                lines.append(f"- {item}")
            lines.append("")
        
        # If week is specified, narrow further
        if week is not None:
            week_context = _get_week_context(unit_num, week, calendar_unit)
            if week_context:
                lines.append("## Week " + str(week) + " Context")
                lines.extend(week_context)
        
        return "\n".join(lines)
    
    except (json.JSONDecodeError, IOError):
        return None


def _infer_unit_from_week(week: int, calendar_units: list) -> Optional[int]:
    """
    Given a week number, infer which unit it falls in.
    Assumes weeks are numbered 1+ and units appear in sequence.
    """
    week_count = 0
    for unit in calendar_units:
        calendar_weeks = unit.get("calendar_weeks", 0)
        if week_count + calendar_weeks >= week:
            return unit.get("unit")
        week_count += calendar_weeks
    return None


def _get_week_context(unit_num: int, week: int, calendar_unit: Dict[str, Any]) -> Optional[list]:
    """
    Extract week-specific context from calendar unit.
    Returns a list of lines describing what week N covers in this unit.
    """
    weeks = calendar_unit.get("weeks", [])
    
    # Try to find week entry in calendar
    for w in weeks:
        if w.get("week") == week:
            lines = []
            if w.get("focus"):
                lines.append(f"Focus: {w.get('focus')}")
            if w.get("topics"):
                for topic in w.get("topics", [])[:3]:
                    lines.append(f"- {topic}")
            if w.get("assessments"):
                lines.append(f"Assessment: {', '.join(w.get('assessments', []))}")
            return lines if lines else None
    
    return None


def load_context(
    task: Dict[str, Any],
    data_dir: Path = Path("data"),
    deliverables_dir: Path = Path("deliverables")
) -> str:
    """
    Load and combine minimal context for the task.
    
    Returns: school_header + curriculum_snippet (if applicable)
    
    This is the core context injection mechanism. For a PLAN-WEEK6-ALG1 task,
    returns ~400-500 tokens total:
    - School identity (stable, always present)
    - Unit 1 scope and calendar snapshot (task-scoped)
    - Week 6 specifics (task-scoped)
    
    For non-curriculum tasks (ASSESS, COMMS), returns school context only.
    """
    context_parts = []
    
    # 1. School context (always)
    school = load_school_context(data_dir)
    if school:
        context_parts.append("## SCHOOL & CLASSROOM CONTEXT")
        context_parts.append(school)
        context_parts.append("")
    
    # 2. Curriculum context (if applicable)
    curriculum = load_curriculum_context(task, deliverables_dir)
    if curriculum:
        context_parts.append("## CURRICULUM CONTEXT")
        context_parts.append(curriculum)
        context_parts.append("")
    
    return "\n".join(context_parts) if context_parts else ""


def build_prompt(task: Dict[str, Any]) -> str:
    """
    Build a prompt for the LLM from task structure.
    
    Includes:
    1. Minimal school & curriculum context (loaded via load_context())
    2. Role specification if available
    3. Goal, plan, constraints from task
    """
    task_id = task.get("task_id", "UNKNOWN")
    goal = task.get("goal", "")
    plan = task.get("plan")
    constraints = task.get("constraints")
    
    lines = []
    
    # 1. Load and inject minimal context
    context = load_context(task)
    if context:
        lines.append(context)
        lines.append("=" * 80)
        lines.append("")
    
    # 2. Load and inject role specification if available
    role_prefix = get_role_prefix(task_id)
    role_spec = load_role_spec(role_prefix) if role_prefix else None
    
    if role_spec:
        lines.append("## ROLE SPECIFICATION")
        lines.append(role_spec)
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
    
    # 3. Task details
    lines.append("## TASK DETAILS")
    lines.append("")
    lines.append(f"Task ID: {task_id}")
    lines.append(f"Goal: {goal}")
    lines.append("")
    
    if plan:
        lines.append("Plan:")
        if isinstance(plan, dict):
            lines.append(json.dumps(plan, indent=2))
        else:
            lines.append(str(plan))
        lines.append("")
    
    if constraints:
        lines.append("Constraints:")
        if isinstance(constraints, dict):
            lines.append(json.dumps(constraints, indent=2))
        else:
            lines.append(str(constraints))
        lines.append("")
    
    lines.append("Please complete this task and provide your response.")
    
    return "\n".join(lines)


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
    logger: logging.Logger,
    llm_client: anthropic.Anthropic
) -> tuple[bool, str, Dict[str, str]]:
    """
    Execute a task using LLM API calls with model routing.
    
    1. Extract role prefix from task_id to select model
    2. Build prompt from task structure
    3. Call Claude API
    4. Write response to deliverables
    
    Returns: (success: bool, summary: str, deliverables_map: dict)
    """
    task_id = task["task_id"]
    deliverables_list = task["deliverables"]
    
    # Ensure deliverables directory exists
    deliverables_dir.mkdir(parents=True, exist_ok=True)
    
    deliverables_map = {}
    
    try:
        # Select model based on task role
        model = select_model_for_task(task_id)
        logger.info(f"Task {task_id} routed to model: {model}")
        
        # Build prompt from task
        prompt = build_prompt(task)
        
        # Call Claude API
        logger.debug(f"Sending prompt to {model}")
        message = llm_client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract response content
        response_text = message.content[0].text
        logger.info(f"Received response from {model} ({len(response_text)} chars)")
        
        # Write response to deliverables
        for deliverable_name in deliverables_list:
            deliverable_path = deliverables_dir / deliverable_name
            
            # Create parent directories if needed
            deliverable_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write response to file (with metadata for markdown)
            if deliverable_name.endswith(".md"):
                content = _wrap_markdown_response(task_id, model, response_text)
            else:
                content = response_text
            
            with open(deliverable_path, "w") as f:
                f.write(content)
            
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
        
        summary = f"Successfully generated {len(deliverables_list)} deliverable(s) for task {task_id} using {model}"
        logger.info(summary)
        return (True, summary, deliverables_map)
    
    except anthropic.APIError as e:
        error_msg = f"API error executing task {task_id}: {str(e)}"
        logger.error(error_msg)
        return (False, error_msg, {})
    except Exception as e:
        error_msg = f"Error executing task {task_id}: {str(e)}"
        logger.error(error_msg)
        return (False, error_msg, {})


def _wrap_markdown_response(task_id: str, model: str, response_text: str) -> str:
    """Wrap LLM response in markdown with metadata."""
    return f"""# Task {task_id}

## Response (Model: {model})

{response_text}

---
Generated at: {datetime.now(timezone.utc).isoformat()}
Task ID: {task_id}
Model: {model}
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
    logger: logging.Logger,
    llm_client: anthropic.Anthropic
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
        
        # Execute task with LLM
        success, summary, deliverables_map = execute_task(task, deliverables_dir, logger, llm_client)
        
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
    logger: logging.Logger,
    llm_client: anthropic.Anthropic
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
                    process_tasks(handoffs_dir, results_dir, deliverables_dir, tmp_dir, logger, llm_client)
                    time.sleep(poll_interval)
                except KeyboardInterrupt:
                    logger.info("Executor interrupted by user")
                    return 0
        else:
            # Run-once mode
            process_tasks(handoffs_dir, results_dir, deliverables_dir, tmp_dir, logger, llm_client)
            return 0
    
    except Exception as e:
        logger.error(f"Unrecoverable error: {e}", exc_info=True)
        return 1


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Directory Executor — LLM-powered file-based task executor"
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
    
    # Initialize LLM client
    try:
        llm_client = get_llm_client()
        logger.info("LLM client initialized successfully")
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)
    
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
        logger,
        llm_client
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
