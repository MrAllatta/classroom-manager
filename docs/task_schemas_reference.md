# Task Schemas Reference — All Roles

This document provides a quick reference of all task types produced by each role, organized by role and task type.

---

## Curriculum Designer Tasks

| Task ID Pattern | Goal | Deliverables | Downstream Consumer |
|---|---|---|---|
| `CURRDES-SCOPE-<UNIT_ID>` | Generate scope and sequence | `scope_<UNIT_ID>.md`, `objectives_<UNIT_ID>.json` | Planner, Assessor, Teacher |
| `CURRDES-ASSESS-<UNIT_ID>` | Generate assessments and rubrics | `assessments_<UNIT_ID>.md`, `rubrics_<UNIT_ID>.json` | Assessor, Teacher |
| `CURRDES-LESSONS-<UNIT_ID>` | Generate lesson plans and materials | `lessons_<UNIT_ID>.md` | Planner, Teacher |

### Consumed by Curriculum Designer

| Source Task Pattern | Consumed From | Purpose |
|---|---|---|
| `result-ASSESS-REVISION-<UNIT_ID>` | Assessor | Mastery data triggers material revision |
| `result-PLAN-CONFIRM-<UNIT_ID>` | Planner | Confirmed time blocks scope lessons |

---

## Planner Tasks

| Task ID Pattern | Goal | Deliverables | Downstream Consumer |
|---|---|---|---|
| `PLAN-CALENDAR-<TERM>` | Generate master calendar for term | `calendar_<TERM>.md`, `calendar_<TERM>.json` | Teacher, all roles |
| `PLAN-PACING-<TERM>` | Generate pacing status report | `pacing_<TERM>.md` | Teacher, Curriculum Designer |
| `PLAN-CONFIRM-<UNIT_ID>` | Confirm time blocks for unit | `time_blocks_<UNIT_ID>.json` | Curriculum Designer, Teacher |
| `PLAN-COMMS-<EVENT>` | Confirm scheduled communication dates | `confirmed_schedule_<EVENT>.json` | Communicator, Calendar |
| `PLAN-ADJUST-<UNIT_ID>` | Adjust pacing due to conflict | `adjusted_schedule_<UNIT_ID>.json` | Calendar, Curriculum Designer |

### Consumed by Planner

| Source Task Pattern | Consumed From | Purpose |
|---|---|---|
| `result-CURRDES-SCOPE-<UNIT_ID>` | Curriculum Designer | Scope and sequence determines time blocks |
| `result-ASSESS-CLASS-<UNIT_ID>` | Assessor | Performance patterns inform pacing adjustments |
| `result-COMMS-PROGRESS-<UNIT_ID>` | Communicator | Scheduled communications affect calendar |

---

## Assessor Tasks

| Task ID Pattern | Goal | Deliverables | Downstream Consumer |
|---|---|---|---|
| `ASSESS-INIT-<UNIT_ID>` | Initialize mastery tracker for unit | `mastery_<UNIT_ID>.json` | Teacher, Curriculum Designer |
| `ASSESS-SCORE-<ASSESSMENT_ID>` | Score assessment and update mastery | `mastery_<UNIT_ID>_updated.json`, `score_report_<ASSESSMENT_ID>.md` | Teacher, Communicator |
| `ASSESS-FLAGS-<TERM>` | Identify at-risk students | `intervention_flags_<TERM>.json` | Communicator, Teacher |
| `ASSESS-CLASS-<UNIT_ID>` | Generate class performance report | `class_performance_<UNIT_ID>.md` | Teacher, Curriculum Designer, Planner |
| `ASSESS-AUDIT-<UNIT_ID>` | Audit assessment quality and alignment | `audit_<UNIT_ID>.md` | Curriculum Designer, Teacher |
| `ASSESS-REVISION-<UNIT_ID>` | Request material revision based on mastery | Task to Curriculum Designer | Curriculum Designer |

### Consumed by Assessor

| Source Task Pattern | Consumed From | Purpose |
|---|---|---|
| `result-CURRDES-ASSESS-<UNIT_ID>` | Curriculum Designer | Assessment instruments and rubrics |
| `result-PLAN-CALENDAR-<TERM>` | Planner | Assessment window dates and deadlines |

---

## Communicator Tasks

| Task ID Pattern | Goal | Deliverables | Downstream Consumer |
|---|---|---|---|
| `COMMS-PROGRESS-<UNIT_ID>` | Draft progress update email | `progress_<UNIT_ID>.md`, `progress_<UNIT_ID>_email.txt` | Teacher (approval), Parents |
| `COMMS-INTERVENTION-<STUDENT_ID>` | Draft intervention notification | `intervention_<STUDENT_ID>.md`, `intervention_<STUDENT_ID>_email.txt` | Teacher (approval), Parents |
| `COMMS-LOG-<TERM>` | Initialize contact log | `contact_log_<TERM>.json` | Teacher, Assessor |
| `COMMS-ATTEMPT-<STUDENT_ID>` | Log outbound communication | `contact_log_<TERM>_updated.json` | Teacher, Assessor |
| `COMMS-ESCALATION-<TERM>` | Generate escalation report | `escalation_<TERM>.md` | Teacher |

### Consumed by Communicator

| Source Task Pattern | Consumed From | Purpose |
|---|---|---|
| `result-ASSESS-FLAGS-<TERM>` | Assessor | Intervention flags trigger communications |
| `result-ASSESS-SCORE-<ASSESSMENT_ID>` | Assessor | Grade notifications to parents |
| `result-PLAN-CALENDAR-<TERM>` | Planner | Scheduled event dates |
| `result-PLAN-COMMS-<EVENT>` | Planner | Confirmed communication dates |

---

## Task Naming Convention

All task IDs follow the pattern:

```
ROLE-FUNCTION-<QUALIFIER>

Examples:
  CURRDES-SCOPE-UNIT-01       (Curriculum Designer, scope generation, Unit 1)
  PLAN-CONFIRM-UNIT-01        (Planner, confirm, Unit 1)
  ASSESS-FLAGS-FALL-2026      (Assessor, flags, Fall 2026 term)
  COMMS-INTERVENTION-S-001    (Communicator, intervention, Student 001)
  ASSESS-REVISION-UNIT-02     (Assessor, revision request, Unit 2)
```

**Role prefixes:**
- `CURRDES` = Curriculum Designer
- `PLAN` = Planner
- `ASSESS` = Assessor
- `COMMS` = Communicator

**Function examples:**
- SCOPE, ASSESS, LESSONS = Curriculum Designer functions
- CALENDAR, PACING, CONFIRM, COMMS, ADJUST = Planner functions
- INIT, SCORE, FLAGS, CLASS, AUDIT, REVISION = Assessor functions
- PROGRESS, INTERVENTION, LOG, ATTEMPT, ESCALATION = Communicator functions

---

## Handoff Chains

### Chain 1: Build Unit (Curriculum → Planning → Assessment)

```
CURRDES-SCOPE-UNIT-01
  ↓
  Deliverables: scope_UNIT-01.md, objectives_UNIT-01.json
  ↓
PLAN-CONFIRM-UNIT-01
  ↓
  Deliverables: time_blocks_UNIT-01.json
  ↓
CURRDES-ASSESS-UNIT-01
  ↓
  Deliverables: assessments_UNIT-01.md, rubrics_UNIT-01.json
  ↓
ASSESS-INIT-UNIT-01
  ↓
  Deliverables: mastery_UNIT-01.json
  ↓
CURRDES-LESSONS-UNIT-01
  ↓
  Deliverables: lessons_UNIT-01.md
  ↓
Ready for instruction
```

### Chain 2: Execute Assessment (Assessor → Communication → Contact Log)

```
ASSESS-SCORE-<ASSESSMENT_ID>
  ↓
  Deliverables: score_report_<ASSESSMENT_ID>.md, mastery_<UNIT_ID>_updated.json
  ↓
COMMS-PROGRESS-<UNIT_ID>
  ↓
  Deliverables: progress_<UNIT_ID>.md, progress_<UNIT_ID>_email.txt
  ↓
Teacher approves send
  ↓
COMMS-ATTEMPT-<STUDENT_ID>
  ↓
  Deliverables: contact_log_<TERM>_updated.json
  ↓
Contact logged
```

### Chain 3: Intervention Loop (Assessor → Communication → Closure)

```
ASSESS-FLAGS-<TERM>
  ↓
  Deliverables: intervention_flags_<TERM>.json
  ↓
COMMS-INTERVENTION-<STUDENT_ID>
  ↓
  Deliverables: intervention_<STUDENT_ID>.md, intervention_<STUDENT_ID>_email.txt
  ↓
Teacher approves & initiates intervention
  ↓
ASSESS-SCORE-<POST_INTERVENTION_ASSESSMENT>
  ↓
  Deliverables: score_report_<ASSESSMENT_ID>.md
  ↓
Intervention outcome tracked
```

### Chain 4: Revision Loop (Assessor → Curriculum Designer → Lessons)

```
ASSESS-CLASS-<UNIT_ID>
  ↓
  Deliverables: class_performance_<UNIT_ID>.md
  ↓
Curriculum Designer reviews performance data
  ↓
ASSESS-REVISION-<UNIT_ID> (request to revise)
  ↓
CURRDES-LESSONS-UNIT-01 (revised with new pedagogy)
  ↓
  Deliverables: lessons_UNIT-01.md (revised)
  ↓
Ready for re-teaching
```

---

## All Deliverables by Type

### Curriculum Designer Outputs

**Scope and Planning:**
- `scope_<UNIT_ID>.md` — Unit overview, standards, objectives, assessment checkpoints
- `objectives_<UNIT_ID>.json` — Lesson-level objectives and standards

**Assessments:**
- `assessments_<UNIT_ID>.md` — Assessment instruments with answer keys
- `rubrics_<UNIT_ID>.json` — Rubric definitions with anchors

**Instruction:**
- `lessons_<UNIT_ID>.md` — Detailed lesson plans with student materials

---

### Planner Outputs

**Calendar:**
- `calendar_<TERM>.md` — Week-by-week calendar view
- `calendar_<TERM>.json` — Structured calendar data

**Pacing:**
- `pacing_<TERM>.md` — Pacing status per unit
- `time_blocks_<UNIT_ID>.json` — Confirmed schedule for unit
- `adjusted_schedule_<UNIT_ID>.json` — Updated schedule after adjustment

**Scheduling:**
- `confirmed_schedule_<EVENT>.json` — Confirmed dates for communication events

---

### Assessor Outputs

**Tracking:**
- `mastery_<UNIT_ID>.json` — Per-student mastery tracking
- `mastery_<UNIT_ID>_updated.json` — Updated mastery after assessment

**Reporting:**
- `score_report_<ASSESSMENT_ID>.md` — Assessment results and class summary
- `class_performance_<UNIT_ID>.md` — Unit-level performance analysis
- `intervention_flags_<TERM>.json` — At-risk student flags

**Quality Assurance:**
- `audit_<UNIT_ID>.md` — Assessment quality audit findings

---

### Communicator Outputs

**Drafts:**
- `progress_<UNIT_ID>.md` — Progress update overview
- `progress_<UNIT_ID>_email.txt` — Parent email template
- `intervention_<STUDENT_ID>.md` — Intervention notification overview
- `intervention_<STUDENT_ID>_email.txt` — Parent email template

**Tracking:**
- `contact_log_<TERM>.json` — Student contact information and attempt history
- `contact_log_<TERM>_updated.json` — Updated contact log after attempt

**Escalation:**
- `escalation_<TERM>.md` — Non-responsive and urgent cases

---

## Task Status Lifecycle

All tasks follow this lifecycle:

```
queued
  ↓ (when executor processes)
running
  ↓ (on success)
done
  ↓ (or on failure)
failed
  ↓
(skipped on future executor runs)
```

Task JSON contains the current status. Result JSON (written by executor) records the final status and outcome.

---

## Key Constraints and Timeouts

| Role | Task Type | Default Timeout | Typical Duration |
|---|---|---|---|
| Curriculum Designer | Scope generation | 600s | 5-10 min |
| Curriculum Designer | Assessment generation | 900s | 5-15 min |
| Curriculum Designer | Lesson planning | 1200s | 10-20 min |
| Planner | Calendar generation | 600s | 5-10 min |
| Planner | Pacing report | 300s | 2-5 min |
| Planner | Time block confirmation | 300s | 2-5 min |
| Assessor | Mastery tracker init | 600s | 5-10 min |
| Assessor | Score assessment | 900s | 5-15 min |
| Assessor | Generate flags | 300s | 2-5 min |
| Assessor | Class report | 600s | 5-10 min |
| Assessor | Assessment audit | 600s | 5-10 min |
| Communicator | Draft communication | 600s | 5-10 min |
| Communicator | Initialize contact log | 300s | 2-5 min |
| Communicator | Log attempt | 200s | 1-2 min |
| Communicator | Generate escalation | 300s | 2-5 min |

---

## Validation Rules

Every task must have:
- `task_id` (non-empty string)
- `goal` (non-empty string describing objective)
- `deliverables` (non-empty array of filenames)
- `status` (one of: queued, running, done, failed)

Every result must have:
- `task_id` (matching the task)
- `status` (done or failed)
- `summary` (non-empty string)
- `deliverables` (object mapping filenames to paths, or empty if failed)
- `completed_at` (ISO 8601 timestamp)
- `error` (optional; present if status is failed)

---

## Using This Reference

When creating a new task:

1. **Find your role** in the section above
2. **Pick the task type** that matches your intent
3. **Copy the task ID pattern** and substitute qualifiers
4. **Check what you need to consume** (look at "Consumed by..." section)
5. **Read the full role spec** (e.g., `docs/roles/assessor.md`) for JSON schema details
6. **Write the task JSON** to `handoffs/task-<YOUR_TASK_ID>.json`
7. **Run the executor** to process

When consuming a result:

1. **Check `results/result-<TASK_ID>.json`** to confirm status is "done"
2. **Read all deliverables** listed in the result's `deliverables` object
3. **Use deliverables as inputs** to your next task
4. **Trace back** to the source task for context and version info
