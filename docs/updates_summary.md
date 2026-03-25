# Documentation Updates Summary

This document summarizes all updates made to the classroom system documentation to integrate the file-based executor pattern and handoff mechanism.

---

## Overview

The classroom team has been updated with a complete **file-based handoff system** using the executor pattern. This replaces ad-hoc coordination with a durable, traceable, deterministic mechanism for role-to-role communication.

All role specifications now include detailed **task schemas** (JSON formats) that define:
- What each role produces (task outputs)
- What each role consumes (task inputs)
- Task naming conventions
- Deliverable formats

---

## Files Updated

### 1. `docs/roles/README.md`

**Changes:**
- Added "File-based handoff mechanism" section explaining directory structure
- Documented task JSON schema (required fields, task lifecycle)
- Documented result JSON schema (status, deliverables, error handling)
- Added "Role execution pattern" explaining the manual workflow during experimental phase
- Added 3 new governing rules (8, 9, 10) about handoffs, atomicity, and traceability

**Purpose:**
- Central reference for understanding the executor system
- Explains the full task lifecycle (queued → running → done/failed)
- Links to detailed role specs for task schemas

---

### 2. `docs/roles/curriculum_designer.md`

**Changes:**
- Added "Handoff Format" section with complete task schemas for:
  - `CURRDES-SCOPE-*` — Generate scope and sequence
  - `CURRDES-ASSESS-*` — Generate assessments and rubrics
  - `CURRDES-LESSONS-*` — Generate lesson plans
  - `ASSESS-REVISION-*` — Consume revision requests from Assessor
- Each task documented with:
  - Task JSON template (inputs, plan, constraints, deliverables)
  - Result JSON template (status, summary, deliverables)
  - Detailed deliverable format examples (markdown, JSON)
- Documented what upstream tasks (Assessor revision, Planner confirmation) are consumed

**Purpose:**
- Curriculum Designer can now read task schemas and understand what to produce
- Other roles can understand what Curriculum Designer outputs look like
- Executor can generate realistic sample content for testing

---

### 3. `docs/roles/planner.md`

**Changes:**
- Added "Handoff Format" section with task schemas for:
  - `PLAN-CALENDAR-*` — Generate master calendar
  - `PLAN-PACING-*` — Generate pacing status report
  - `PLAN-CONFIRM-*` — Confirm time blocks for unit
  - `PLAN-COMMS-*` — Confirm scheduled communication dates
  - `PLAN-ADJUST-*` — Adjust pacing due to conflicts
- Documented upstream consumption of Curriculum Designer scope results
- Each task includes template JSON and deliverable formats

**Purpose:**
- Planner task execution is now fully specified
- Calendar and time block structure is documented
- Downstream roles (Curriculum Designer, Assessor, Communicator) know what to expect

---

### 4. `docs/roles/assessor.md`

**Changes:**
- Added "Handoff Format" section with task schemas for:
  - `ASSESS-INIT-*` — Initialize mastery tracker
  - `ASSESS-SCORE-*` — Score assessment and update mastery
  - `ASSESS-FLAGS-*` — Identify at-risk students
  - `ASSESS-CLASS-*` — Generate class performance report
  - `ASSESS-AUDIT-*` — Audit assessment quality
- Documented mastery tracker JSON structure (per-student, per-standard tracking)
- Documented intervention flag format
- Documented performance report and audit formats

**Purpose:**
- Assessor tasks fully specified
- Mastery tracker schema is now portable (can be consumed by Communicator, Curriculum Designer)
- Intervention flags trigger downstream communication tasks

---

### 5. `docs/roles/communicator.md`

**Changes:**
- Added "Handoff Format" section with task schemas for:
  - `COMMS-PROGRESS-*` — Draft progress update emails
  - `COMMS-INTERVENTION-*` — Draft intervention notifications
  - `COMMS-LOG-*` — Initialize contact log
  - `COMMS-ATTEMPT-*` — Log outbound communication attempt
  - `COMMS-ESCALATION-*` — Generate escalation report
- Documented upstream consumption of Assessor flags and Planner calendar results
- Contact log schema documented for tracking parent communication attempts

**Purpose:**
- Communicator tasks fully specified
- Contact log is now a portable data structure (can be passed back to Assessor)
- Escalation report format supports teacher intervention decisions

---

## New Documentation Files

### 6. `docs/HANDOFF_WORKFLOW.md`

**Content:**
- Complete explanation of the file-based executor pattern
- Directory structure diagram
- Task and result JSON schema reference
- Step-by-step manual execution workflow (for experimental phase)
- Example chains showing role-to-role handoffs:
  - Curriculum → Planner → Assessment chain
  - Assessor → Communicator → Contact log chain
  - Assessor → Communication → Closure chain
  - Assessor → Curriculum revision → Lessons chain
- Idempotence and retry semantics
- Error handling examples (invalid JSON, missing deliverables, timeouts)
- Logging output examples
- Testing instructions (quickstart validation)
- Future extension paths (continuous polling, event triggers)

**Purpose:**
- Primary reference for understanding the executor system
- Shows concrete examples of how roles interact via tasks
- Explains how to test the system manually

---

### 7. `docs/TASK_SCHEMAS_REFERENCE.md`

**Content:**
- Quick reference table of all task types by role
- Task naming convention documented
- All handoff chains visualized (unit build, assessment execution, intervention loop, revision loop)
- Comprehensive list of all deliverables organized by role
- Task status lifecycle documented
- Timeout defaults for each task type
- Validation rules for tasks and results
- Instructions for using the reference (how to create a task, how to consume a result)

**Purpose:**
- Single-page lookup for task schemas
- Helps users find the right task type for their intent
- Shows how task types chain together

---

### 8. `EXECUTOR_QUICKSTART.md` (top-level)

**Content:**
- Installation and setup instructions
- How to run executor (once or watch mode)
- How to create a task (3 steps)
- How to check results
- Common workflows:
  - Scenario 1: Build a unit end-to-end (5 executor runs)
  - Scenario 2: Score assessment and communicate (4 executor runs)
- Complete CLI reference with examples
- Troubleshooting guide (task not processing, failing, executor crashing)
- Next steps for users

**Purpose:**
- First document users read when starting
- Provides step-by-step guidance for common tasks
- Includes troubleshooting so users can resolve issues independently

---

### 9. `docs/UPDATES_SUMMARY.md` (this document)

**Content:**
- Summary of all changes
- File-by-file explanation of what was added
- Rationale for the handoff system
- Key concepts introduced
- Where to start reading

---

## Key Concepts Introduced

### 1. Task JSON (Input)
- Contains: task_id, goal, plan, constraints, deliverables, timeout_seconds, status
- Written by upstream role to `handoffs/task-<ID>.json`
- Status: queued → running → done/failed

### 2. Result JSON (Output)
- Contains: task_id, status, summary, deliverables, completed_at, error
- Written by executor to `results/result-<ID>.json`
- Confirms completion and provides paths to deliverables

### 3. Deliverables
- Actual output files created by executor (markdown, JSON, etc.)
- Placed in `deliverables/` directory
- Consumed by downstream roles as inputs to their tasks

### 4. Handoff Chains
- Series of tasks where output of one becomes input to next
- Fully specified in `TASK_SCHEMAS_REFERENCE.md`
- Deterministic: same inputs always produce same outputs (idempotent)

### 5. Manual Execution
- During experimental phase: humans run `python executor.py --no-watch`
- Processes all queued tasks atomically
- Can be run multiple times safely (idempotent)

---

## Task Naming Convention

All tasks follow this pattern:

```
<ROLE>-<FUNCTION>-<QUALIFIER>

Examples:
  CURRDES-SCOPE-UNIT-01
  PLAN-CONFIRM-UNIT-01
  ASSESS-FLAGS-FALL-2026
  COMMS-INTERVENTION-S-001
  ASSESS-REVISION-UNIT-02
```

This naming scheme ensures:
- Clear ownership (which role produces this task)
- Clear function (what the task does)
- Clear qualifier (what unit, term, or student)

---

## Example: Full Unit Build Workflow

The documentation now enables end-to-end workflows. Example: building Unit 1.

**Step 1: Curriculum Designer generates scope**
```bash
# Create task
cat > handoffs/task-CURRDES-SCOPE-UNIT-01.json << 'EOF'
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "goal": "Generate scope and sequence for Unit 1",
  "deliverables": ["scope_UNIT-01.md", "objectives_UNIT-01.json"],
  "status": "queued"
}
EOF

# Run executor
python executor.py --no-watch

# Result: deliverables/scope_UNIT-01.md and deliverables/objectives_UNIT-01.json
```

**Step 2: Planner confirms time blocks**
```bash
cat > handoffs/task-PLAN-CONFIRM-UNIT-01.json << 'EOF'
{
  "task_id": "PLAN-CONFIRM-UNIT-01",
  "goal": "Confirm time blocks for Unit 1",
  "deliverables": ["time_blocks_UNIT-01.json"],
  "status": "queued"
}
EOF

python executor.py --no-watch

# Result: deliverables/time_blocks_UNIT-01.json
```

**Step 3: Curriculum Designer generates assessments**
```bash
cat > handoffs/task-CURRDES-ASSESS-UNIT-01.json << 'EOF'
{
  "task_id": "CURRDES-ASSESS-UNIT-01",
  "goal": "Generate assessments for Unit 1",
  "deliverables": ["assessments_UNIT-01.md", "rubrics_UNIT-01.json"],
  "status": "queued"
}
EOF

python executor.py --no-watch

# Result: deliverables/assessments_UNIT-01.md and deliverables/rubrics_UNIT-01.json
```

This pattern continues until the unit is fully built.

---

## Where to Start

**If you're new to the system:**
1. Read `EXECUTOR_QUICKSTART.md` (top-level, 5 min read)
2. Read `docs/HANDOFF_WORKFLOW.md` (15 min read)
3. Pick a role and read its spec in `docs/roles/`
4. Create your first task and run the executor

**If you're implementing a role:**
1. Read `docs/roles/README.md` to understand the overall system
2. Read your role's spec (e.g., `docs/roles/assessor.md`)
3. Read the "Handoff Format" section of your role spec
4. Consult `docs/TASK_SCHEMAS_REFERENCE.md` to see how your tasks chain

**If you're debugging a task:**
1. Check `docs/TASK_SCHEMAS_REFERENCE.md` for task ID pattern and expected structure
2. Validate JSON: `python -m json.tool handoffs/task-<ID>.json`
3. Check result: `cat results/result-<ID>.json`
4. See "Troubleshooting" section in `EXECUTOR_QUICKSTART.md`

**If you're extending the system:**
1. Read `docs/HANDOFF_WORKFLOW.md` section "Extending to Continuous Execution"
2. Understand the task and result schemas are stable — implementation can change
3. Add new task types to existing roles by adding to their "Handoff Format" section
4. Update `docs/TASK_SCHEMAS_REFERENCE.md` when adding new tasks

---

## Key Design Principles Preserved

1. **Every output traces to an input** — Tasks explicitly declare what they consume and produce
2. **Every role has one owner** — No shared task ownership; executor is purely mechanical
3. **Teacher approves; agents draft** — Communication drafts go to teacher before sending
4. **Escalation path is explicit** — Failures and anomalies are captured in result JSONs
5. **Done criteria are checkable** — Status is deterministic (done/failed, not subjective)

**New principles:**
6. **Handoffs are durable** — File-based, not ephemeral; full audit trail
7. **Tasks are atomic** — Either complete fully or fail visibly; no partial states
8. **Results are traceable** — Every result includes task_id, status, summary, error
9. **Execution is deterministic** — Same task always produces same result (given same inputs)
10. **System is extensible** — Schemas are stable; implementation swappable

---

## Integration with executor.py

The documentation is designed to work with `executor.py` (created separately).

The executor:
- Reads task JSONs from `handoffs/`
- Validates against schemas documented here
- Creates sample deliverables (markdown, JSON)
- Writes result JSONs to `results/`
- Atomically updates task status (queued → running → done/failed)

The documentation:
- Specifies what each task should look like
- Shows what each deliverable should contain
- Explains the workflow and chains
- Provides examples and troubleshooting

Together, they enable end-to-end testing and validation of the classroom system without any live external integrations.

---

## Migration Path (Future)

As the system matures:

1. **Replace sample content generation** with actual agent API calls (Anthropic, Posit services, etc.)
2. **Add continuous polling** by running executor as background process instead of manual trigger
3. **Add event triggers** so downstream tasks start automatically when upstream results are written
4. **Add role-specific handlers** that call custom logic for each role (instead of generic content generation)

**None of this requires changing the file structure, task schemas, or documentation.** The schemas are stable; only the implementation details change.

---

## Summary

The classroom system now has:

✅ **Complete task schema documentation** for all 4 roles (Curriculum Designer, Planner, Assessor, Communicator)

✅ **Detailed handoff workflow** explaining how tasks chain together

✅ **Executor quickstart** for getting started with the system

✅ **Task schemas reference** for quick lookup and task creation

✅ **Role specifications** updated with handoff formats

✅ **End-to-end examples** showing complete workflows (unit build, assessment execution, intervention loop)

✅ **Error handling and troubleshooting** guide

The system is now ready for:
- Manual end-to-end testing of the workflow
- Role-by-role implementation (agent APIs can be swapped in for sample content generation)
- Extension to continuous execution when ready
- Training and handoff to the full team

---

## Questions or Next Steps?

Refer back to:
- **How do I use the executor?** → `EXECUTOR_QUICKSTART.md`
- **What tasks can I create?** → `docs/TASK_SCHEMAS_REFERENCE.md`
- **How do roles interact?** → `docs/HANDOFF_WORKFLOW.md`
- **What does my role do?** → `docs/roles/<ROLE>.md`
- **What are the general rules?** → `docs/roles/README.md`
