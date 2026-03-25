# File-Based Handoff Workflow — Executor Pattern

## Overview

All role-to-role communication in the classroom system uses a **directory executor** pattern. This ensures durable, traceable, atomic handoffs with no ambiguity about task status or deliverables.

This document describes the manual execution workflow for the experimental phase. Later, this pattern can be extended to continuous polling or event-triggered execution without changing the file structure or task schemas.

---

## Directory Structure

```
handoffs/              # Tasks handed off between roles
  task-PLAN-001.json
  task-CURRDES-001.json
  task-ASSESS-001.json
  task-COMMS-001.json

results/               # Completion records and status
  result-PLAN-001.json
  result-CURRDES-001.json
  result-ASSESS-001.json
  result-COMMS-001.json

deliverables/          # Produced artifacts (readable by downstream roles)
  calendar_FALL_2026.md
  calendar_FALL_2026.json
  scope_UNIT_01.md
  objectives_UNIT_01.json
  assessments_UNIT_01.md
  rubrics_UNIT_01.json
  lessons_UNIT_01.md
  mastery_UNIT_01.json
  score_report_ASSESS_001.md
  intervention_flags_FALL_2026.json
  progress_UNIT_01.md
  progress_UNIT_01_email.txt

tmp/                   # Atomic write staging (executor use only)
  task-PLAN-001.json.tmp
```

---

## Task and Result JSON Schemas

### Task JSON (written to `handoffs/`)

```json
{
  "task_id": "string (unique identifier, e.g., 'PLAN-001')",
  "goal": "string (clear, actionable objective)",
  "plan": "object or string (optional; captures strategy, steps, or key decisions)",
  "constraints": "object (optional; captures boundaries, deadlines, requirements)",
  "deliverables": ["array of filenames expected in deliverables/"],
  "timeout_seconds": "integer (optional; default 600)",
  "version": "integer (optional; for tracking schema changes)",
  "created_at": "string (ISO 8601 timestamp when task was created)",
  "status": "queued | running | done | failed"
}
```

### Result JSON (written to `results/`)

```json
{
  "task_id": "string (matches task_id)",
  "status": "done | failed",
  "summary": "string (what was done or what went wrong)",
  "deliverables": {
    "filename": "path/in/deliverables/",
    "another_file.md": "deliverables/another_file.md"
  },
  "completed_at": "string (ISO 8601 timestamp)",
  "version": "integer",
  "error": "string (present if status is 'failed')"
}
```

---

## Manual Execution Workflow

### Step 1: Upstream Role Prepares Task

A role finishes its work and is ready to hand off to a downstream role. It creates a task JSON describing what the downstream role should do.

**Example:** Planner has confirmed all unit time blocks and is ready to ask Curriculum Designer to generate lesson plans.

```json
// handoffs/task-CURRDES-LESSONS-UNIT-01.json
{
  "task_id": "CURRDES-LESSONS-UNIT-01",
  "goal": "Generate lesson plans and student materials for Unit 1: Linear Equations",
  "plan": {
    "inputs": ["scope_UNIT-01.md", "objectives_UNIT-01.json"],
    "pedagogy": "inquiry-based with formative checkpoints"
  },
  "constraints": {
    "unit_id": "UNIT-01",
    "lesson_count": 12,
    "duration_hours": 18,
    "standards": ["8.EE.B.5", "8.EE.B.6"]
  },
  "deliverables": ["lessons_UNIT-01.md"],
  "timeout_seconds": 1200,
  "version": 1,
  "created_at": "2026-03-25T10:00:00Z",
  "status": "queued"
}
```

---

### Step 2: Run the Executor

When ready to process all pending tasks, the human (or admin) runs:

```bash
cd /path/to/classroom-manager
python executor.py --no-watch
```

**CLI options:**
- `--handoffs-dir` (default: `./handoffs`)
- `--results-dir` (default: `./results`)
- `--deliverables-dir` (default: `./deliverables`)
- `--tmp-dir` (default: `./tmp`)
- `--no-watch` (run once and exit; default is `--watch` with 1-second polling)
- `--log-file` (optional; write logs to file)

---

### Step 3: Executor Processes Tasks

For each task JSON in `handoffs/`:

1. **Validate** — Check required fields (task_id, goal, deliverables)
2. **Mark running** — Atomically update status to "running" with timestamp
3. **Execute** — Read inputs from `results/` and `deliverables/` (from upstream tasks), generate content for deliverables
4. **Write deliverables** — Create all files listed in task.deliverables
5. **Verify** — Confirm all deliverables exist
6. **Write result** — Create `result-<TASK_ID>.json` with status "done" or "failed"

**Example executor output for `task-CURRDES-LESSONS-UNIT-01.json`:**

```json
// results/result-CURRDES-LESSONS-UNIT-01.json
{
  "task_id": "CURRDES-LESSONS-UNIT-01",
  "status": "done",
  "summary": "Generated 12 detailed lesson plans with student materials, including differentiation for IEP/504 students and ELL scaffolds.",
  "deliverables": {
    "lessons_UNIT-01.md": "deliverables/lessons_UNIT-01.md"
  },
  "completed_at": "2026-03-25T10:15:00Z",
  "version": 1
}
```

Deliverable `lessons_UNIT-01.md` is created and ready to use.

---

### Step 4: Downstream Role Consumes Results

The next role reads the result JSON from `results/` to confirm the upstream task is complete, then reads the deliverables from `deliverables/`.

**Example:** Assessor finishes Curriculum Designer task, then reads:
- `results/result-CURRDES-ASSESS-UNIT-01.json` → confirms status is "done"
- `deliverables/assessments_UNIT-01.md` → reads assessment instruments
- `deliverables/rubrics_UNIT-01.json` → reads rubric definitions
- Creates its own task: `task-ASSESS-INIT-UNIT-01.json`

---

### Step 5: Repeat

The downstream role executes its own task (either manually or in another executor run), writes results and deliverables, and hands off to the next role in the chain.

---

## Example Chain: Curriculum → Planning → Assessment

### Round 1: Generate Scope

**Curriculum Designer task:**
```
handoffs/task-CURRDES-SCOPE-UNIT-01.json
Goal: Generate scope and sequence for Unit 1: Linear Equations
Deliverables: [scope_UNIT-01.md, objectives_UNIT-01.json]
```

**Executor runs:**
```
1. Reads task-CURRDES-SCOPE-UNIT-01.json
2. Generates scope_UNIT-01.md and objectives_UNIT-01.json
3. Writes results/result-CURRDES-SCOPE-UNIT-01.json (status: done)
```

---

### Round 2: Confirm Time Blocks

**Planner consumes scope, creates task:**
```
handoffs/task-PLAN-CONFIRM-UNIT-01.json
Goal: Confirm time blocks for Unit 1
Inputs: results/result-CURRDES-SCOPE-UNIT-01.json
Deliverables: [time_blocks_UNIT-01.json]
```

**Executor runs:**
```
1. Reads task-PLAN-CONFIRM-UNIT-01.json
2. Checks results/result-CURRDES-SCOPE-UNIT-01.json (confirmed done)
3. Reads deliverables/scope_UNIT-01.md (lesson count, duration)
4. Generates deliverables/time_blocks_UNIT-01.json
5. Writes results/result-PLAN-CONFIRM-UNIT-01.json (status: done)
```

---

### Round 3: Generate Assessments

**Curriculum Designer consumes time blocks, creates task:**
```
handoffs/task-CURRDES-ASSESS-UNIT-01.json
Goal: Generate assessments and rubrics for Unit 1
Inputs: results/result-PLAN-CONFIRM-UNIT-01.json
Deliverables: [assessments_UNIT-01.md, rubrics_UNIT-01.json]
```

**Executor runs:**
```
1. Reads task-CURRDES-ASSESS-UNIT-01.json
2. Checks results/result-PLAN-CONFIRM-UNIT-01.json (confirmed done)
3. Reads deliverables/time_blocks_UNIT-01.json (duration constraints)
4. Generates assessments_UNIT-01.md and rubrics_UNIT-01.json
5. Writes results/result-CURRDES-ASSESS-UNIT-01.json (status: done)
```

---

### Round 4: Initialize Mastery Tracker

**Assessor consumes assessments, creates task:**
```
handoffs/task-ASSESS-INIT-UNIT-01.json
Goal: Initialize mastery tracker for Unit 1
Inputs: results/result-CURRDES-ASSESS-UNIT-01.json
Deliverables: [mastery_UNIT-01.json]
```

**Executor runs:**
```
1. Reads task-ASSESS-INIT-UNIT-01.json
2. Checks results/result-CURRDES-ASSESS-UNIT-01.json (confirmed done)
3. Reads deliverables/rubrics_UNIT-01.json (standard definitions)
4. Generates mastery_UNIT-01.json with per-student tracking
5. Writes results/result-ASSESS-INIT-UNIT-01.json (status: done)
```

---

## Idempotence and Retries

### Completed Tasks Are Skipped

If a task is already marked as "done" in `results/`, the executor skips it.

**Scenario:** You run the executor twice by mistake.
```
First run:
  task-ASSESS-INIT-UNIT-01 queued → running → done
  result-ASSESS-INIT-UNIT-01.json created with status "done"

Second run:
  Executor checks results/result-ASSESS-INIT-UNIT-01.json
  Sees status "done"
  Skips task (no re-execution)
```

### Timeout Detection

If a task is "running" longer than `timeout_seconds`, the executor marks it as failed with a diagnostic reason.

```json
{
  "task_id": "ASSESS-INIT-UNIT-01",
  "status": "failed",
  "summary": "Task timed out after 1200 seconds (20 minutes).",
  "error": "Task exceeded timeout_seconds: 1200. Check logs for cause."
}
```

---

## Error Handling

### Invalid JSON

**Input:** Malformed task JSON in `task-X.json`
**Output:**
```json
{
  "task_id": "X",
  "status": "failed",
  "summary": "Task skipped due to validation error.",
  "error": "Invalid JSON: line 5, col 12 — unterminated string"
}
```

### Missing Required Fields

**Input:** Task missing `goal` or `deliverables`
**Output:**
```json
{
  "task_id": "PLAN-001",
  "status": "failed",
  "summary": "Task validation failed.",
  "error": "Required field missing: 'goal'"
}
```

### Missing Deliverables After Execution

**Input:** Task promises to create `foo.md` and `bar.json`, but only `foo.md` exists
**Output:**
```json
{
  "task_id": "CURRDES-LESSONS-UNIT-01",
  "status": "failed",
  "summary": "Deliverable validation failed.",
  "error": "Expected deliverables missing: ['lessons_UNIT-01.md']. Created: ['objectives_UNIT-01.json']"
}
```

---

## Logging

The executor logs all operations to stdout with timestamps:

```
[2026-03-25 10:00:01] Starting executor (no-watch mode)
[2026-03-25 10:00:02] Found 3 tasks in handoffs/
[2026-03-25 10:00:03] Processing task-CURRDES-SCOPE-UNIT-01
[2026-03-25 10:00:03]   Status: queued → running
[2026-03-25 10:00:05]   Executing: Generate scope_UNIT-01.md
[2026-03-25 10:00:06]   Executing: Generate objectives_UNIT-01.json
[2026-03-25 10:00:08]   Deliverables verified: 2/2 created
[2026-03-25 10:00:09]   Status: running → done
[2026-03-25 10:00:09]   Result written: results/result-CURRDES-SCOPE-UNIT-01.json
[2026-03-25 10:00:10] Processing task-PLAN-CONFIRM-UNIT-01
[2026-03-25 10:00:10]   Status: queued → running
[2026-03-25 10:00:12]   Executing: Confirm time_blocks_UNIT-01.json
[2026-03-25 10:00:15]   Deliverables verified: 1/1 created
[2026-03-25 10:00:15]   Status: running → done
[2026-03-25 10:00:16]   Result written: results/result-PLAN-CONFIRM-UNIT-01.json
[2026-03-25 10:00:17] Completed 2 tasks (0 failed, 1 skipped)
[2026-03-25 10:00:17] Exiting
```

**Optional file logging:** Use `--log-file executor.log` to write logs to a persistent file in addition to stdout.

---

## Testing the Workflow

### Quick Validation

Create a minimal task and run the executor:

```bash
# Create a simple task
cat > handoffs/task-TEST-001.json << 'EOF'
{
  "task_id": "TEST-001",
  "goal": "Create a test outline",
  "deliverables": ["test_outline.md"],
  "timeout_seconds": 600,
  "version": 1,
  "created_at": "2026-03-25T10:00:00Z",
  "status": "queued"
}
EOF

# Run executor
python executor.py --no-watch

# Verify
cat results/result-TEST-001.json
cat deliverables/test_outline.md
```

**Expected output:**
- `results/result-TEST-001.json` with status "done"
- `deliverables/test_outline.md` with sample content
- Executor logs showing all steps

---

## Extending to Continuous Execution

In the future, this pattern can be extended by:

1. Running `executor.py --watch --poll-interval 5` as a background process
2. Replacing the generic executor with role-specific handlers that call the actual agent APIs
3. Adding event triggers (e.g., "start assessor task when curriculum designer result is ready")

**The file structure and task schemas remain unchanged** — making the migration seamless.

---

## Key Design Principles

1. **Durable** — All state is persisted in JSON files; no in-memory state means tasks survive restarts
2. **Atomic** — Writes use tmp/ staging and rename; no partial states
3. **Traceable** — Every task, result, and deliverable is timestamped and versioned
4. **Deterministic** — Single-process, no concurrency; full audit trail is preserved
5. **Idempotent** — Running the executor twice on the same task produces the same result
6. **Extensible** — Task schemas and directory structure are stable; logic can be swapped without changing interfaces
