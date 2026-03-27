# Classroom System Architecture

**Canonical narrative (read this first):** [`architecture_and_workflows.md`](architecture_and_workflows.md) — how work moves through the system, simulated-real-world testing, and pointers to the rest of the docs.

This file keeps the extended diagrams and component breakdowns below — visual overview, data flow, and executor path in depth.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CLASSROOM MANAGEMENT SYSTEM                          │
│                                                                         │
│  Roles (Agents)  →  File-Based Handoffs  →  Executor  →  Deliverables │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

```
┌──────────────────────────┐
│   Classroom Roles        │
│  ┌────────────────────┐  │
│  │ Curriculum Designer│◄─┼───┐
│  │  • Scope           │  │   │
│  │  • Assessments     │  │   │
│  │  • Lessons         │  │   │
│  └────────────────────┘  │   │
│                          │   │
│  ┌────────────────────┐  │   │
│  │ Planner            │◄─┼───┼──┐
│  │  • Calendar        │  │   │  │
│  │  • Pacing          │  │   │  │
│  │  • Time blocks     │  │   │  │
│  └────────────────────┘  │   │  │
│                          │   │  │
│  ┌────────────────────┐  │   │  │
│  │ Assessor           │◄─┼───┼──┼──┐
│  │  • Mastery tracker │  │   │  │  │
│  │  • Scoring         │  │   │  │  │
│  │  • Reporting       │  │   │  │  │
│  │  • Flags           │  │   │  │  │
│  └────────────────────┘  │   │  │  │
│                          │   │  │  │
│  ┌────────────────────┐  │   │  │  │
│  │ Communicator       │◄─┼───┼──┼──┼──┐
│  │  • Drafts          │  │   │  │  │  │
│  │  • Contact logs    │  │   │  │  │  │
│  │  • Escalations     │  │   │  │  │  │
│  └────────────────────┘  │   │  │  │  │
│                          │   │  │  │  │
└──────────────────────────┘   │  │  │  │
         │                      │  │  │  │
         │ Produces Task JSONs  │  │  │  │
         │                      ▼  ▼  ▼  ▼
         │              ┌─────────────────────┐
         │              │   handoffs/         │
         │              │  task-*.json        │
         │              │  (queued status)    │
         │              └─────────────────────┘
         │                      │
         │ Executor reads tasks │
         │                      ▼
┌────────┴──────────────────────────────────────┐
│          executor.py                          │
│  ┌─────────────────────────────────────────┐  │
│  │ 1. Read task JSON from handoffs/        │  │
│  │ 2. Validate schema                      │  │
│  │ 3. Mark status: queued → running        │  │
│  │ 4. Generate deliverables                │  │
│  │ 5. Verify all deliverables exist        │  │
│  │ 6. Write result JSON to results/        │  │
│  │ 7. Mark status: running → done/failed   │  │
│  └─────────────────────────────────────────┘  │
└─────────┬─────────────────────────────────────┘
          │
          ▼
    ┌──────────────────┐    ┌─────────────────────┐
    │ results/         │    │ deliverables/       │
    │ result-*.json    │    │ *.md, *.json, etc.  │
    │ (done/failed)    │    │ (consumed by roles) │
    └──────────────────┘    └─────────────────────┘
          │                        ▲
          │                        │
          └────────────────────────┘
               Downstream roles
               read results and
               deliverables to
               create next tasks
```

---

## Task Lifecycle State Machine

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TASK LIFECYCLE                              │
└─────────────────────────────────────────────────────────────────────┘

  Task Created (by upstream role)
           │
           ▼
    ┌─────────────┐
    │   QUEUED    │  ◄─── Task JSON written to handoffs/
    │ task_id set │
    │ status OK   │
    └─────────────┘
           │
           │ Executor reads task
           ▼
    ┌─────────────┐
    │   RUNNING   │  ◄─── Status atomically updated
    │ task_id set │     tmp/ staging + rename pattern
    │ time logged │
    └─────────────┘
           │
      ┌────┴────┐
      │          │
      │          │ Validation fails or execution error
      │          ▼
      │       ┌─────────┐
      │       │ FAILED  │  ◄─── Result JSON written with error field
      │       │ error   │
      │       │ logged  │
      │       └─────────┘
      │
      │ Validation passes, deliverables created successfully
      │
      ▼
    ┌─────────┐
    │  DONE   │  ◄─── Result JSON written with deliverable paths
    │ success │
    │ logged  │
    └─────────┘
           │
           │ Executor skips on future runs
           │ (task already done)
           ▼
    [COMPLETED]  ◄─── Downstream role reads result and
                      consumes deliverables
```

---

## Handoff Chain Example: Unit Build

```
ROUND 1: Curriculum Designer → Generate Scope
  ┌─────────────────────────────┐
  │ Create task JSON            │
  │ task-CURRDES-SCOPE-UNIT-01  │
  │ status: queued              │
  └────────┬────────────────────┘
           │
           │ python executor.py --no-watch
           ▼
  ┌─────────────────────────────┐
  │ Executor processes task     │
  │ Generates:                  │
  │  • scope_UNIT-01.md         │
  │  • objectives_UNIT-01.json  │
  └────────┬────────────────────┘
           │
           │ Write results/result-CURRDES-SCOPE-UNIT-01.json
           │ status: done
           ▼


ROUND 2: Planner → Confirm Time Blocks
  ┌─────────────────────────────┐
  │ Planner reads result from   │
  │ CURRDES-SCOPE task          │
  │ Checks: status == "done"    │
  │ Reads: deliverables/        │
  │  scope_UNIT-01.md           │
  └────────┬────────────────────┘
           │
           │ Planner creates task
           │ task-PLAN-CONFIRM-UNIT-01
           │ status: queued
           │ inputs: scope_UNIT-01.md
           ▼
  ┌─────────────────────────────┐
  │ Executor processes task     │
  │ Generates:                  │
  │  • time_blocks_UNIT-01.json │
  └────────┬────────────────────┘
           │
           │ Write results/result-PLAN-CONFIRM-UNIT-01.json
           │ status: done
           ▼


ROUND 3: Curriculum Designer → Generate Assessments
  ┌─────────────────────────────┐
  │ Curriculum Designer reads   │
  │ results from PLAN-CONFIRM   │
  │ Checks: status == "done"    │
  │ Reads: deliverables/        │
  │  time_blocks_UNIT-01.json   │
  └────────┬────────────────────┘
           │
           │ Creates task
           │ task-CURRDES-ASSESS-UNIT-01
           │ status: queued
           ▼
  ┌─────────────────────────────┐
  │ Executor processes task     │
  │ Generates:                  │
  │  • assessments_UNIT-01.md   │
  │  • rubrics_UNIT-01.json     │
  └────────┬────────────────────┘
           │
           │ Write result JSON
           │ status: done
           ▼

[Pattern continues for remaining roles...]

END RESULT: Unit 1 fully built with all components
  deliverables/
    ├── scope_UNIT-01.md
    ├── objectives_UNIT-01.json
    ├── time_blocks_UNIT-01.json
    ├── assessments_UNIT-01.md
    ├── rubrics_UNIT-01.json
    ├── mastery_UNIT-01.json
    └── lessons_UNIT-01.md
```

---

## Role Interaction Map

```
┌──────────────────────┐
│ Curriculum Designer  │
│                      │
│ PRODUCES:            │ ─── scope, assessments, lessons
│ CONSUMES:            │ ◄── time blocks, mastery data
│ SENDS TO:            │ ──► Planner, Assessor, Teacher
│ RECEIVES FROM:       │ ◄── Planner, Assessor
└──────────────────────┘


┌──────────────────────┐
│ Planner              │
│                      │
│ PRODUCES:            │ ─── calendar, pacing, time blocks
│ CONSUMES:            │ ◄── scope, communication schedule
│ SENDS TO:            │ ──► Curriculum Designer, Assessor, Communicator, Teacher
│ RECEIVES FROM:       │ ◄── Curriculum Designer, Assessor, Communicator
└──────────────────────┘


┌──────────────────────┐
│ Assessor             │
│                      │
│ PRODUCES:            │ ─── mastery tracker, scores, flags, reports
│ CONSUMES:            │ ◄── assessments, rubrics, calendar windows
│ SENDS TO:            │ ──► Curriculum Designer, Communicator, Planner, Teacher
│ RECEIVES FROM:       │ ◄── Curriculum Designer, Planner
└──────────────────────┘


┌──────────────────────┐
│ Communicator         │
│                      │
│ PRODUCES:            │ ─── drafts, contact logs, escalations
│ CONSUMES:            │ ◄── intervention flags, calendar events
│ SENDS TO:            │ ──► Teacher, Assessor (via contact logs)
│ RECEIVES FROM:       │ ◄── Assessor, Planner
└──────────────────────┘


┌──────────────────────┐
│ Teacher (Eric)       │
│                      │
│ CONSUMES:            │ ◄── all role outputs for review
│ APPROVES:            │ ─── communications, overrides, decisions
│ PROVIDES:            │ ─── priorities, constraints, final call
└──────────────────────┘
```

---

## Directory Structure

```
classroom-manager/
│
├── handoffs/                    ◄── INPUT: Task JSONs (queued)
│   ├── task-CURRDES-SCOPE-UNIT-01.json
│   ├── task-PLAN-CONFIRM-UNIT-01.json
│   ├── task-CURRDES-ASSESS-UNIT-01.json
│   ├── task-ASSESS-INIT-UNIT-01.json
│   └── ...
│
├── results/                     ◄── OUTPUT: Result JSONs (done/failed)
│   ├── result-CURRDES-SCOPE-UNIT-01.json
│   ├── result-PLAN-CONFIRM-UNIT-01.json
│   ├── result-CURRDES-ASSESS-UNIT-01.json
│   ├── result-ASSESS-INIT-UNIT-01.json
│   └── ...
│
├── deliverables/                ◄── OUTPUT: Produced files
│   ├── scope_UNIT-01.md
│   ├── objectives_UNIT-01.json
│   ├── time_blocks_UNIT-01.json
│   ├── assessments_UNIT-01.md
│   ├── rubrics_UNIT-01.json
│   ├── mastery_UNIT-01.json
│   ├── lessons_UNIT-01.md
│   ├── score_report_ASSESS-001.md
│   ├── intervention_flags_FALL-2026.json
│   ├── progress_UNIT-01.md
│   ├── progress_UNIT-01_email.txt
│   ├── contact_log_FALL-2026.json
│   └── ...
│
├── tmp/                         ◄── TEMP: Atomic write staging
│   ├── task-CURRDES-SCOPE-UNIT-01.json.tmp
│   └── ...
│
├── data/                        ◄── School data (read-only)
│   ├── school/
│   │   └── context.yaml
│   ├── sections/
│   │   ├── algebra_1.yaml
│   │   ├── algebra_1_ict.yaml
│   │   ├── ap_stats.yaml
│   │   └── ap_csa.yaml
│   └── students/
│       ├── S-001.yaml
│       ├── S-002.yaml
│       └── ...
│
├── docs/                        ◄── Documentation
│   ├── co-teacher.md
│   ├── agent-architecture.md
│   ├── HANDOFF_WORKFLOW.md       ◄── NEW
│   ├── TASK_SCHEMAS_REFERENCE.md ◄── NEW
│   ├── UPDATES_SUMMARY.md        ◄── NEW
│   ├── SYSTEM_ARCHITECTURE.md    ◄── NEW
│   └── roles/
│       ├── README.md             ◄── UPDATED
│       ├── curriculum_designer.md ◄── UPDATED
│       ├── planner.md            ◄── UPDATED
│       ├── assessor.md           ◄── UPDATED
│       └── communicator.md       ◄── UPDATED
│
├── executor.py                  ◄── Executor script
├── EXECUTOR_QUICKSTART.md       ◄── NEW: Usage guide
└── README.md                    ◄── Project overview
```

---

## Data Flow Example: Score Assessment → Parent Notification

```
STEP 1: Teacher scores assessment in classroom
  (Manual: teacher provides scores, notes)
           │
           ▼

STEP 2: Assessor creates task
  ┌──────────────────────────────────────┐
  │ task-ASSESS-SCORE-UNIT-01-EXAM-01   │
  │ goal: Score unit exam                │
  │ inputs: [student responses]           │
  │ deliverables:                        │
  │  • score_report_UNIT-01-EXAM-01.md   │
  │  • mastery_UNIT-01_updated.json      │
  └──────────────────────────────────────┘
           │
           ▼

STEP 3: Executor runs
  1. Reads task
  2. Generates score report
  3. Updates mastery tracker
  4. Writes result → done
           │
           ▼

STEP 4: Communicator reads results
  ┌──────────────────────────────────────┐
  │ Check: result-ASSESS-SCORE... done   │
  │ Read: score_report_UNIT-01-EXAM-01   │
  │ Read: mastery_UNIT-01_updated.json   │
  └──────────────────────────────────────┘
           │
           ▼

STEP 5: Communicator creates task
  ┌──────────────────────────────────────┐
  │ task-COMMS-PROGRESS-UNIT-01          │
  │ goal: Draft progress update email    │
  │ inputs: score_report_UNIT-01-EXAM-01 │
  │ deliverables:                        │
  │  • progress_UNIT-01.md               │
  │  • progress_UNIT-01_email.txt        │
  └──────────────────────────────────────┘
           │
           ▼

STEP 6: Executor runs
  1. Reads task
  2. Generates progress email draft
  3. Writes result → done
           │
           ▼

STEP 7: Teacher reviews and approves
  (Manual: teacher reads email draft,
   approves for sending)
           │
           ▼

STEP 8: Communicator logs send
  ┌──────────────────────────────────────┐
  │ task-COMMS-ATTEMPT-<STUDENT_ID>      │
  │ goal: Log communication sent          │
  │ inputs: [email sent timestamp]        │
  │ deliverables:                        │
  │  • contact_log_FALL-2026_updated.json│
  └──────────────────────────────────────┘
           │
           ▼

STEP 9: Executor runs
  1. Reads task
  2. Updates contact log
  3. Writes result → done
           │
           ▼

STEP 10: Contact log available for:
  • Teacher to review all communications
  • Assessor to track intervention outcomes
  • Admin for compliance reporting
```

---

## Key Properties of the Architecture

### 1. Durability
- All state persists in JSON files in `handoffs/`, `results/`, `deliverables/`
- No in-memory state; tasks survive restarts
- Full audit trail from task creation to completion

### 2. Atomicity
- Writes use `tmp/` staging directory
- Atomic rename pattern prevents partial writes
- Task status changes are transactional (queued → running → done, all at once)

### 3. Traceability
- Every task has a unique ID and timestamp
- Every result references the task that created it
- Every deliverable can be traced back to its task via result JSON

### 4. Determinism
- Single-process executor (no concurrency)
- Same task always produces same result (given same inputs)
- No race conditions or timing dependencies

### 5. Idempotence
- Running executor twice on same task = same result
- Completed tasks (status: done) are skipped
- Safe to re-run without side effects

### 6. Extensibility
- Task and result schemas are stable
- Role implementations can be swapped without changing interfaces
- Can extend to continuous polling, event triggers, or role-specific handlers later

---

## Processing Model: Single-Process, Single-Task-At-A-Time

```
EXECUTOR MAIN LOOP:
  while true:
    if watch_mode:
      sleep(poll_interval)
    
    tasks = list_queued_tasks()
    for task in tasks:
      result = process_task(task)
      write_result(result)
    
    if not watch_mode:
      exit()
```

**Why single-process?**
- Deterministic: no race conditions, no complex concurrency
- Debuggable: full execution order is visible in logs
- Testable: same input always produces same output
- Simple: minimal risk of deadlock or resource contention

---

## Example: Full System in Action

```
DAY 1: Build Unit 1

  8:00 AM - Curriculum Designer creates task
            task-CURRDES-SCOPE-UNIT-01.json
  
  8:15 AM - Admin runs: python executor.py --no-watch
            ✓ Generates scope_UNIT-01.md, objectives_UNIT-01.json
  
  8:30 AM - Planner creates task
            task-PLAN-CONFIRM-UNIT-01.json
  
  8:45 AM - Admin runs: python executor.py --no-watch
            ✓ Generates time_blocks_UNIT-01.json
  
  9:00 AM - Curriculum Designer creates task
            task-CURRDES-ASSESS-UNIT-01.json
  
  9:15 AM - Admin runs: python executor.py --no-watch
            ✓ Generates assessments_UNIT-01.md, rubrics_UNIT-01.json
  
  ... (continues for remaining tasks)
  
  12:00 PM - All deliverables ready
             • Unit 1 scope and objectives
             • Time blocks confirmed
             • Assessments and rubrics
             • Mastery tracker initialized
             • Lesson plans generated
             • Teacher ready to teach


DAY 2: Teach Unit 1 and Start Grading

  3:30 PM - Teacher finishes first assessment
            Provides scores to Assessor
  
  4:00 PM - Assessor creates task
            task-ASSESS-SCORE-UNIT-01-FORM-01.json
  
  4:15 PM - Admin runs: python executor.py --no-watch
            ✓ Generates score_report_UNIT-01-FORM-01.md
            ✓ Updates mastery_UNIT-01.json
  
  4:30 PM - Communicator creates task
            task-COMMS-PROGRESS-UNIT-01.json
  
  4:45 PM - Admin runs: python executor.py --no-watch
            ✓ Generates progress_UNIT-01_email.txt
  
  5:00 PM - Teacher reviews email draft
            ✓ Approves
  
  5:15 PM - Email sent to parents
            Communicator logs with task-COMMS-ATTEMPT-...
  
  5:30 PM - Admin runs: python executor.py --no-watch
            ✓ Updates contact_log_FALL-2026.json
  
  → Cycle complete: assessment → communication → parent notification


DAY 3: Analysis and Adjustment

  8:00 AM - Assessor creates task
            task-ASSESS-CLASS-UNIT-01.json
  
  8:15 AM - Admin runs: python executor.py --no-watch
            ✓ Generates class_performance_UNIT-01.md
  
  8:30 AM - Teacher reviews: 15% of students not yet on standard 8.EE.B.5
  
  8:45 AM - Assessor creates revision request task
            task-ASSESS-REVISION-UNIT-01.json
  
  9:00 AM - Curriculum Designer creates task
            task-CURRDES-LESSONS-UNIT-01-REVISED.json
  
  9:15 AM - Admin runs: python executor.py --no-watch
            ✓ Generates revised lessons_UNIT-01_v2.md
  
  9:30 AM - Teacher reviews revisions
            ✓ Approves
  
  → Cycle complete: analyze → revise → reteach
```

---

## Comparison: Before and After

### Before (Conceptual)

```
Teacher coordinates manually:
  1. Asks Curriculum Designer for scope
  2. Hands scope to Planner
  3. Planner confirms time blocks (maybe via email)
  4. Curriculum Designer gets time blocks (maybe via Slack)
  5. Designs assessments
  6. Hands to Assessor (maybe verbally)
  7. Assessor sets up grade book
  ... (no clear record of who did what when)
```

**Problems:**
- No durable record of handoffs
- Easy to miss steps or lose information
- Difficult to trace what depends on what
- No clear status (is scope done? still pending?)

### After (File-Based Executor)

```
Clear, traceable workflow:
  1. Curriculum Designer writes task JSON
  2. Admin runs executor
  3. Executor validates, executes, writes result
  4. Planner reads result status (done/failed)
  5. Planner reads deliverables
  6. Planner writes task JSON
  7. Admin runs executor
  ... (full audit trail in files)
```

**Benefits:**
- Durable: all state persists
- Traceable: every step recorded with timestamps
- Clear status: task.status is definitive
- Debuggable: can review what happened at each step
- Extensible: can add continuous polling, agents, triggers later

---

## Next Phase: From Manual to Automated

```
CURRENT (Manual Execution):
  Admin manually runs: python executor.py --no-watch
  
  ↓
  
PHASE 2 (Continuous Polling):
  Executor runs: python executor.py --watch --poll-interval 5
  (background process, polls every 5 seconds)
  
  ↓
  
PHASE 3 (Event Triggers):
  Executor watches for results being written
  Automatically starts downstream tasks
  Example: CURRDES-SCOPE completes → trigger PLAN-CONFIRM
  
  ↓
  
PHASE 4 (Role-Specific Handlers):
  Replace sample content generation with actual role APIs
  Example: CURRDES-SCOPE calls Claude API for real curriculum
  
  ↓
  
PHASE 5 (Live System):
  Full classroom management system operational
  Agents handle all coordination automatically
  Teacher focuses on instruction and decisions only
```

**Key point:** File structure and schemas don't change across phases. Only implementation details.

---

## Summary

The classroom system is built on three pillars:

1. **Clear Role Definitions**
   - Each role has explicit inputs, outputs, responsibilities
   - No overlapping ownership; escalation path is clear

2. **File-Based Handoff Mechanism**
   - Durable, traceable, atomic task and result exchange
   - Full audit trail in persistent JSON files
   - Deterministic, idempotent execution

3. **Extensible Executor Pattern**
   - Generic processing loop reads tasks, runs logic, writes results
   - Can replace logic without changing structure
   - Scales from manual to fully automated

This architecture enables:
- End-to-end workflow testing before live deployment
- Clear debugging (full history of what happened)
- Incremental automation (manual → polling → triggers → agents)
- Easy extension (new roles, new task types)
