# Executor Quickstart — How to Use

The executor is the orchestration engine for the classroom system. It reads task JSONs from `handoffs/`, executes them, and writes results to `results/` with deliverables in `deliverables/`.

---

## Installation & Setup

The executor requires only Python 3.8+ and the standard library. No external dependencies.

```bash
cd /path/to/classroom-manager
```

Verify the directory structure exists:
```bash
ls -la | grep -E "^d" | awk '{print $NF}'
# Should show: handoffs, results, deliverables, tmp (or create them)

# Create if missing:
mkdir -p handoffs results deliverables tmp
```

---

## Running the Executor

### Run Once (Process All Pending Tasks)

```bash
python executor.py --no-watch
```

This processes all tasks in `handoffs/`, writes results and deliverables, then exits.

**Output:**
```
[2026-03-25 10:00:01] Starting executor (no-watch mode)
[2026-03-25 10:00:02] Found 2 tasks in handoffs/
[2026-03-25 10:00:03] Processing task-CURRDES-SCOPE-UNIT-01
[2026-03-25 10:00:03]   Status: queued → running
[2026-03-25 10:00:05]   Executing: Generate scope_UNIT-01.md
[2026-03-25 10:00:06]   Executing: Generate objectives_UNIT-01.json
[2026-03-25 10:00:08]   Deliverables verified: 2/2 created
[2026-03-25 10:00:09]   Status: running → done
[2026-03-25 10:00:09]   Result written: results/result-CURRDES-SCOPE-UNIT-01.json
[2026-03-25 10:00:11] Completed 2 tasks (0 failed)
[2026-03-25 10:00:11] Exiting
```

### Watch Mode (Continuous Polling)

```bash
python executor.py --watch --poll-interval 5
```

This polls `handoffs/` every 5 seconds and processes any new tasks. Useful for long-running processes; Ctrl+C to stop.

---

## Creating a Task

### Step 1: Write the Task JSON

Create a file `handoffs/task-<YOUR_ID>.json`:

```json
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "goal": "Generate scope and sequence for Unit 1: Linear Equations",
  "plan": {
    "inputs": ["CCSS-M standard 8.EE.B.5", "NYC math framework"],
    "outputs": ["unit outline", "lesson objectives"]
  },
  "constraints": {
    "unit_id": "UNIT-01",
    "course": "ALG-01",
    "standards": ["8.EE.B.5", "8.EE.B.6"],
    "target_hours": 15
  },
  "deliverables": ["scope_UNIT-01.md", "objectives_UNIT-01.json"],
  "timeout_seconds": 600,
  "version": 1,
  "created_at": "2026-03-25T10:00:00Z",
  "status": "queued"
}
```

### Step 2: Run the Executor

```bash
python executor.py --no-watch
```

### Step 3: Check the Result

```bash
cat results/result-CURRDES-SCOPE-UNIT-01.json
```

Expected output:
```json
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "status": "done",
  "summary": "Generated scope and sequence for Unit 1: Linear Equations with 12 lessons across 3 standards.",
  "deliverables": {
    "scope_UNIT-01.md": "deliverables/scope_UNIT-01.md",
    "objectives_UNIT-01.json": "deliverables/objectives_UNIT-01.json"
  },
  "completed_at": "2026-03-25T10:00:15Z",
  "version": 1
}
```

### Step 4: Read the Deliverables

```bash
cat deliverables/scope_UNIT-01.md
cat deliverables/objectives_UNIT-01.json
```

---

## Common Workflow

### Scenario 1: Build a Unit End-to-End

**1. Generate scope (Curriculum Designer)**

Create `handoffs/task-CURRDES-SCOPE-UNIT-01.json`:
```json
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "goal": "Generate scope and sequence for Unit 1: Linear Equations",
  "deliverables": ["scope_UNIT-01.md", "objectives_UNIT-01.json"],
  "status": "queued"
}
```

Run: `python executor.py --no-watch`

**2. Confirm time blocks (Planner)**

Create `handoffs/task-PLAN-CONFIRM-UNIT-01.json`:
```json
{
  "task_id": "PLAN-CONFIRM-UNIT-01",
  "goal": "Confirm time blocks for Unit 1",
  "plan": {
    "inputs": ["scope_UNIT-01.md from Curriculum Designer"],
    "duration": "15 hours available, 12 lessons planned"
  },
  "deliverables": ["time_blocks_UNIT-01.json"],
  "status": "queued"
}
```

Run: `python executor.py --no-watch`

**3. Generate assessments (Curriculum Designer)**

Create `handoffs/task-CURRDES-ASSESS-UNIT-01.json`:
```json
{
  "task_id": "CURRDES-ASSESS-UNIT-01",
  "goal": "Generate assessments and rubrics for Unit 1",
  "plan": {
    "inputs": ["time_blocks_UNIT-01.json from Planner"],
    "formative": ["exit tickets", "practice problems"],
    "summative": ["unit exam"]
  },
  "deliverables": ["assessments_UNIT-01.md", "rubrics_UNIT-01.json"],
  "status": "queued"
}
```

Run: `python executor.py --no-watch`

**4. Initialize mastery tracker (Assessor)**

Create `handoffs/task-ASSESS-INIT-UNIT-01.json`:
```json
{
  "task_id": "ASSESS-INIT-UNIT-01",
  "goal": "Initialize mastery tracker for Unit 1",
  "plan": {
    "inputs": ["rubrics_UNIT-01.json from Curriculum Designer"]
  },
  "deliverables": ["mastery_UNIT-01.json"],
  "status": "queued"
}
```

Run: `python executor.py --no-watch`

**5. Generate lesson plans (Curriculum Designer)**

Create `handoffs/task-CURRDES-LESSONS-UNIT-01.json`:
```json
{
  "task_id": "CURRDES-LESSONS-UNIT-01",
  "goal": "Generate lesson plans for Unit 1",
  "plan": {
    "inputs": ["scope_UNIT-01.md", "objectives_UNIT-01.json"]
  },
  "deliverables": ["lessons_UNIT-01.md"],
  "status": "queued"
}
```

Run: `python executor.py --no-watch`

**Result:** Unit 1 is fully built with scope, lessons, assessments, rubrics, and initialized mastery tracking.

---

### Scenario 2: Score an Assessment and Communicate

**1. Score assessment (Assessor)**

Create `handoffs/task-ASSESS-SCORE-UNIT-01-FORMATIVE-01.json`:
```json
{
  "task_id": "ASSESS-SCORE-UNIT-01-FORMATIVE-01",
  "goal": "Score Unit 1 exit ticket and update mastery",
  "plan": {
    "inputs": ["rubrics_UNIT-01.json"],
    "process": "Apply rubric to each student's exit ticket"
  },
  "deliverables": ["mastery_UNIT-01_updated.json", "score_report_UNIT-01-FORMATIVE-01.md"],
  "status": "queued"
}
```

Run: `python executor.py --no-watch`

Check results: `cat deliverables/score_report_UNIT-01-FORMATIVE-01.md`

**2. Identify flagged students (Assessor)**

Create `handoffs/task-ASSESS-FLAGS-WEEK-2.json`:
```json
{
  "task_id": "ASSESS-FLAGS-WEEK-2",
  "goal": "Identify students needing intervention after Week 2 assessments",
  "plan": {
    "criteria": "mastery_level = 'Not Yet' on 2+ standards"
  },
  "deliverables": ["intervention_flags_WEEK-2.json"],
  "status": "queued"
}
```

Run: `python executor.py --no-watch`

Check results: `cat deliverables/intervention_flags_WEEK-2.json`

**3. Draft progress communication (Communicator)**

Create `handoffs/task-COMMS-PROGRESS-UNIT-01.json`:
```json
{
  "task_id": "COMMS-PROGRESS-UNIT-01",
  "goal": "Draft progress update for parents on Unit 1",
  "plan": {
    "inputs": ["score_report_UNIT-01-FORMATIVE-01.md"],
    "audience": "all parents",
    "tone": "encouraging and informative"
  },
  "deliverables": ["progress_UNIT-01.md", "progress_UNIT-01_email.txt"],
  "status": "queued"
}
```

Run: `python executor.py --no-watch`

Check draft: `cat deliverables/progress_UNIT-01_email.txt`

**4. Teacher approves and sends (manually)**

Eric reviews the draft email and approves for sending (in experimental phase, mocked; in production, sends via email system).

---

## CLI Reference

```bash
python executor.py [OPTIONS]
```

**Options:**

```
--handoffs-dir PATH       Directory containing task-*.json files
                         (default: ./handoffs)

--results-dir PATH        Directory to write result-*.json files
                         (default: ./results)

--deliverables-dir PATH   Directory to write deliverable files
                         (default: ./deliverables)

--tmp-dir PATH           Temporary directory for atomic writes
                         (default: ./tmp)

--poll-interval SECONDS   Polling interval in watch mode
                         (default: 1)

--watch / --no-watch     Run continuously (--watch) or once (--no-watch)
                         (default: --watch)

--log-file FILE          Optional log file path
                         (default: None; logs to stdout only)
```

**Example:**

```bash
# Run once with custom directories
python executor.py --no-watch \
  --handoffs-dir /data/tasks \
  --results-dir /data/results \
  --deliverables-dir /data/outputs

# Watch with 10-second polling and file logging
python executor.py --watch \
  --poll-interval 10 \
  --log-file logs/executor.log

# Run once with verbose logging to file and stdout
python executor.py --no-watch --log-file logs/executor.log
```

---

## Troubleshooting

### Task not processing?

1. **Check task is in `handoffs/`:**
   ```bash
   ls -la handoffs/
   ```

2. **Verify JSON is valid:**
   ```bash
   python -m json.tool handoffs/task-CURRDES-SCOPE-UNIT-01.json
   # Should print JSON without errors
   ```

3. **Check required fields:**
   ```json
   {
     "task_id": "CURRDES-SCOPE-UNIT-01",      // Required
     "goal": "Generate scope...",              // Required
     "deliverables": ["scope_UNIT-01.md"],    // Required (non-empty array)
     "status": "queued"                        // Required
   }
   ```

4. **Check `results/` for error:**
   ```bash
   cat results/result-CURRDES-SCOPE-UNIT-01.json
   # Look for "error" field
   ```

### Task failing with error?

1. **Read the error message:**
   ```bash
   grep "error" results/result-*.json | tail -1
   ```

2. **Common errors:**
   - Missing deliverable file: Check that all files in `task.deliverables` were created in `deliverables/`
   - Invalid JSON: Ensure no syntax errors in task JSON
   - Timeout: Task took longer than `timeout_seconds`; increase timeout or check for bottlenecks

3. **Rerun on fix:**
   - Fix the task JSON
   - Delete the old result (or it will be skipped)
   - Run executor again

### Executor crashing?

1. **Check Python version:**
   ```bash
   python --version
   # Should be 3.8+
   ```

2. **Check directory permissions:**
   ```bash
   touch handoffs/.test && rm handoffs/.test
   touch results/.test && rm results/.test
   touch deliverables/.test && rm deliverables/.test
   touch tmp/.test && rm tmp/.test
   ```

3. **Review logs:**
   ```bash
   python executor.py --no-watch --log-file executor.log
   cat executor.log
   ```

---

## Next Steps

1. **Read the full documentation:**
   - `docs/HANDOFF_WORKFLOW.md` — Complete workflow explanation
   - `docs/TASK_SCHEMAS_REFERENCE.md` — All task schemas by role
   - `docs/roles/` — Full role specifications

2. **Create your first task:**
   - Pick a role and task type from `TASK_SCHEMAS_REFERENCE.md`
   - Write the task JSON following the schema
   - Run `python executor.py --no-watch`
   - Check results and deliverables

3. **Build a chain:**
   - Create tasks that depend on each other (read results from upstream tasks)
   - Run the executor multiple times to build up a complete workflow
   - Verify the chain by checking final deliverables

---

## Key Principles

- **Durable:** All state in files; survives restarts
- **Atomic:** No partial writes; tmp/ staging + rename pattern
- **Traceable:** Every task and result is timestamped
- **Deterministic:** Single-process; repeatable execution
- **Idempotent:** Running twice on same task = same result
- **Extensible:** Schemas are stable; implementation can change
