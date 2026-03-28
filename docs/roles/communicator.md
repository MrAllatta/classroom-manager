# Role: Communicator

## Purpose
Own all communication loops between the classroom and the outside world — parents, students, administration, and school systems — especially where outcomes depend on timely follow-up or documented action.

**Teacher-next:** Drafts and logs state **what the teacher should do after reading** (approve and send, edit then send, call instead, hold, escalate) and by when, when timing matters.

## Responsibilities
- Draft and send routine communications: progress updates, absence follow-ups, assignment reminders, grade notifications
- Maintain contact logs per student, including attempt history and responses
- Escalate non-responsive or high-priority cases to the teacher with full contact history
- Produce call scripts and email templates calibrated to the communication context
- Log all outbound communications and inbound responses with timestamps
- Coordinate with Planner to tie communications to scheduled events (conferences, IEP meetings, deadlines)
- During experimental phase: mock all external sends; produce draft artifacts only

## Inputs
| Source | Artifact |
|---|---|
| Assessor | Grade reports, intervention flags, failing/at-risk student lists |
| Planner | Event dates, conference schedules, deadline reminders |
| Curriculum Designer | Assignment/assessment descriptions for parent-facing summaries |
| Teacher | Escalation decisions, tone/policy constraints, final approval on sensitive communications |
| School system | Compliance communication requirements, official templates |

## Outputs
| Artifact | Consumer |
|---|---|
| Drafted communications (email, text, call script) | Teacher (for approval/send) |
| Sent communication log (timestamped) | Teacher, Admin |
| Contact attempt history per student | Teacher, Assessor |
| Escalation report (non-responsive / urgent cases) | Teacher |
| Compliance communication record | Admin |

## Handoff Format

All tasks follow the schema defined in [`docs/roles/README.md`](README.md). This section documents task types specific to this role.

### Task naming convention

```
COMMS-<FUNCTION>-<QUALIFIER>

Examples:
  COMMS-PROGRESS-UNIT-01
  COMMS-INTERVENTION-1000001
  COMMS-LOG-UNIT-01
  COMMS-ATTEMPT-1000001
  COMMS-ESCALATION-UNIT-01
```

---

### Tasks this role produces

#### `COMMS-PROGRESS-<QUALIFIER>` — Draft progress update communications

Written to `handoffs/` when a scheduled progress update is due (triggered by `PLAN-COMMS-*` schedule). Produces draft emails for teacher approval. Consumed by the Teacher.

**Task JSON:**
```json
{
  "task_id": "COMMS-PROGRESS-UNIT-01",
  "goal": "Draft progress update emails for all Unit 1 Algebra I students following the end-unit assessment.",
  "plan": {
    "upstream_class_report_task": "ASSESS-CLASS-UNIT-01",
    "upstream_comms_schedule_task": "PLAN-COMMS-UNIT-01",
    "class_report_file": "deliverables/class_report_UNIT-01.md",
    "mastery_tracker_file": "deliverables/mastery_tracker_UNIT-01.json",
    "comms_schedule_file": "deliverables/comms_schedule_UNIT-01.json",
    "communication_type": "progress_update"
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "tone": "professional, warm, accessible",
    "no_live_send": true,
    "teacher_approval_required": true,
    "experimental_phase": true
  },
  "deliverables": ["drafts_progress_UNIT-01.md"],
  "timeout_seconds": 600,
  "created_at": "2026-10-03T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "COMMS-PROGRESS-UNIT-01",
  "status": "done",
  "summary": "81 progress update email drafts generated for ALG-01/02/03 Unit 1. Drafts differentiated by mastery level (strong, on-track, at-risk). All marked DRAFT — teacher approval required before send.",
  "deliverables": {
    "drafts_progress_UNIT-01.md": "deliverables/drafts_progress_UNIT-01.md"
  },
  "completed_at": "2026-10-03T08:05:20Z",
  "version": 1
}
```

**Deliverable format:**

`drafts_progress_UNIT-01.md` — Markdown document with one draft per student:
```
---
student_id: 1000001
section: ALG-01
to: guardian@example.com
subject: [DRAFT] Unit 1 Progress Update — Algebra I
status: DRAFT — awaiting teacher approval
---

Dear [Guardian Name],

I'm writing to share [Student Name]'s progress after our first unit in Algebra I, Linear Equations.

[Student Name] demonstrated strong understanding of solving linear equations (standard 8.EE.C.7),
scoring at the 3/4 level. Work on systems of equations (8.EE.C.8) is progressing and will continue
in Unit 2.

Please feel free to reach out with any questions.

[Teacher Name]
---
```

---

#### `COMMS-INTERVENTION-<QUALIFIER>` — Draft intervention notification

Written to `handoffs/` when the Assessor issues an at-risk flag (`ASSESS-FLAGS-*`). Produces a draft intervention notification for teacher approval before send. Qualifier is typically the student ID.

**Task JSON:**
```json
{
  "task_id": "COMMS-INTERVENTION-1000001",
  "goal": "Draft intervention notification for student 1000001 following below-mastery result on Unit 1.",
  "plan": {
    "upstream_flags_task": "ASSESS-FLAGS-UNIT-01",
    "flags_file": "deliverables/flags_UNIT-01.json",
    "mastery_tracker_file": "deliverables/mastery_tracker_UNIT-01.json",
    "student_id": "1000001",
    "flag_id": "FLAG-UNIT01-1000001",
    "communication_type": "intervention_notification"
  },
  "constraints": {
    "tone": "direct, supportive, action-oriented",
    "include_next_steps": true,
    "no_live_send": true,
    "teacher_approval_required": true,
    "iep_504_sensitivity": true,
    "experimental_phase": true
  },
  "deliverables": ["draft_intervention_1000001.md"],
  "timeout_seconds": 300,
  "created_at": "2026-10-02T10:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "COMMS-INTERVENTION-1000001",
  "status": "done",
  "summary": "Intervention notification drafted for student 1000001 (ALG-01). IEP flag noted in draft. Marked DRAFT — teacher approval required before send.",
  "deliverables": {
    "draft_intervention_1000001.md": "deliverables/draft_intervention_1000001.md"
  },
  "completed_at": "2026-10-02T10:01:45Z",
  "version": 1
}
```

**Deliverable format:**

`draft_intervention_1000001.md` — Single draft with header metadata:
```
---
student_id: 1000001
section: ALG-01
to: guardian@example.com
subject: [DRAFT] Important: Academic Support Needed — Algebra I Unit 1
flag_id: FLAG-UNIT01-1000001
iep_active: true
status: DRAFT — awaiting teacher approval
---

Dear [Guardian Name],

I want to reach out about [Student Name]'s recent performance on our Unit 1 assessment
in Algebra I. [Student Name] is currently below the mastery threshold on solving linear
equations (8.EE.C.7) and would benefit from additional support.

**Next steps:**
- [Student Name] will receive targeted re-teaching during the next two class sessions.
- I am available for questions during office hours [Day/Time].
- Please contact me at [Email] to discuss further or to schedule a call.

[Teacher Name]
---
```

---

#### `COMMS-LOG-<QUALIFIER>` — Initialize or update contact log

Written to `handoffs/` at the start of a unit (initialize) or after communication events (update). Maintains the per-student contact history. Consumed by the Assessor (closes intervention loop) and the Teacher.

**Task JSON:**
```json
{
  "task_id": "COMMS-LOG-UNIT-01",
  "goal": "Initialize contact log for Unit 1 for all Algebra I students.",
  "plan": {
    "upstream_comms_schedule_task": "PLAN-COMMS-UNIT-01",
    "comms_schedule_file": "deliverables/comms_schedule_UNIT-01.json",
    "student_roster_source": "data/students/",
    "log_action": "initialize"
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"]
  },
  "deliverables": ["contact_log_UNIT-01.json"],
  "timeout_seconds": 300,
  "created_at": "2026-09-06T09:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "COMMS-LOG-UNIT-01",
  "status": "done",
  "summary": "Contact log initialized for 81 students in ALG-01/02/03 for Unit 1. All attempt histories empty. 2 scheduled communications registered.",
  "deliverables": {
    "contact_log_UNIT-01.json": "deliverables/contact_log_UNIT-01.json"
  },
  "completed_at": "2026-09-06T09:01:10Z",
  "version": 1
}
```

**Deliverable format:**

`contact_log_UNIT-01.json` — Per-student contact history:
```json
{
  "unit": "UNIT-01",
  "sections": ["ALG-01", "ALG-02", "ALG-03"],
  "students": [
    {
      "student_id": "1000001",
      "section": "ALG-01",
      "contact_email": "guardian@example.com",
      "contact_phone": "212-555-0100",
      "preferred_language": "en",
      "attempts": [],
      "scheduled_communications": ["COMMS-EVT-UNIT01-01"],
      "intervention_flags_acknowledged": [],
      "escalation_status": null
    }
  ]
}
```

---

#### `COMMS-ATTEMPT-<QUALIFIER>` — Log outbound communication attempt

Written to `handoffs/` after a draft is approved and a send attempt is made (real or mocked). Updates the contact log with attempt outcome. Qualifier is typically the student ID.

**Task JSON:**
```json
{
  "task_id": "COMMS-ATTEMPT-1000001",
  "goal": "Log outbound intervention notification attempt for student 1000001.",
  "plan": {
    "upstream_intervention_task": "COMMS-INTERVENTION-1000001",
    "contact_log_file": "deliverables/contact_log_UNIT-01.json",
    "student_id": "1000001",
    "draft_file": "deliverables/draft_intervention_1000001.md",
    "channel": "email",
    "send_mode": "mock"
  },
  "constraints": {
    "teacher_approval_confirmed": true,
    "experimental_phase": true,
    "no_live_send": true
  },
  "deliverables": ["contact_log_UNIT-01.json"],
  "timeout_seconds": 120,
  "created_at": "2026-10-03T09:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "COMMS-ATTEMPT-1000001",
  "status": "done",
  "summary": "Outbound attempt logged for student 1000001. Channel: email (mocked). Status: sent. Contact log updated.",
  "deliverables": {
    "contact_log_UNIT-01.json": "deliverables/contact_log_UNIT-01.json"
  },
  "completed_at": "2026-10-03T09:00:45Z",
  "version": 2
}
```

**Deliverable format:**

Contact log updated — attempt appended to student record:
```json
{
  "attempt_id": "ATT-1000001-01",
  "channel": "email",
  "direction": "outbound",
  "timestamp": "2026-10-03T09:00:45Z",
  "subject": "Important: Academic Support Needed — Algebra I Unit 1",
  "status": "sent_mock",
  "response": null,
  "flag_id": "FLAG-UNIT01-1000001",
  "teacher_approved": true
}
```

---

#### `COMMS-ESCALATION-<QUALIFIER>` — Generate escalation report

Written to `handoffs/` when a student has not responded after the threshold number of outreach attempts, or when a case meets escalation criteria. Consumed by the Teacher for human judgment.

**Task JSON:**
```json
{
  "task_id": "COMMS-ESCALATION-UNIT-01",
  "goal": "Generate escalation report for Unit 1 students with no parent response after 2 outreach attempts.",
  "plan": {
    "contact_log_file": "deliverables/contact_log_UNIT-01.json",
    "flags_file": "deliverables/flags_UNIT-01.json",
    "escalation_criteria": {
      "no_response_after_attempts": 2,
      "open_flag_age_days": 5
    }
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"]
  },
  "deliverables": ["escalation_report_UNIT-01.md"],
  "timeout_seconds": 300,
  "created_at": "2026-10-08T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "COMMS-ESCALATION-UNIT-01",
  "status": "done",
  "summary": "4 students escalated: no parent response after 2 attempts and flag open > 5 days. Escalation report generated. Teacher action required.",
  "deliverables": {
    "escalation_report_UNIT-01.md": "deliverables/escalation_report_UNIT-01.md"
  },
  "completed_at": "2026-10-08T08:02:15Z",
  "version": 1
}
```

**Deliverable format:**

`escalation_report_UNIT-01.md` — Markdown report with one section per escalated student:
- Student ID, section, flag ID, flag age
- Full attempt history (channel, date, outcome)
- Recommended next step (phone call, in-person conference, counselor referral)
- IEP/504 status noted if active

---

### Tasks this role consumes

#### `ASSESS-FLAGS-<QUALIFIER>` result — At-risk flags from Assessor

The Communicator reads intervention flags to trigger `COMMS-INTERVENTION-*` drafts.

**Upstream result JSON (written by Assessor to `results/`):**
```json
{
  "task_id": "ASSESS-FLAGS-UNIT-01",
  "status": "done",
  "summary": "12 students flagged at-risk.",
  "deliverables": {
    "flags_UNIT-01.json": "deliverables/flags_UNIT-01.json"
  },
  "completed_at": "2026-10-01T17:01:45Z",
  "version": 1
}
```

**Action:** Communicator reads `flags_UNIT-01.json` and writes one `COMMS-INTERVENTION-<student_id>` task per flagged student.

#### `PLAN-COMMS-<QUALIFIER>` result — Communication schedule from Planner

The Communicator reads the scheduled communication dates to trigger `COMMS-PROGRESS-*` drafts on schedule.

**Upstream result JSON (written by Planner to `results/`):**
```json
{
  "task_id": "PLAN-COMMS-UNIT-01",
  "status": "done",
  "summary": "Communication schedule confirmed for Unit 1.",
  "deliverables": {
    "comms_schedule_UNIT-01.json": "deliverables/comms_schedule_UNIT-01.json"
  },
  "completed_at": "2026-09-05T09:01:30Z",
  "version": 1
}
```

**Action:** Communicator reads `comms_schedule_UNIT-01.json` and queues `COMMS-PROGRESS-*` tasks on the scheduled send dates.

## Handoffs
- **To Teacher:** all drafted communications requiring approval before send; escalations requiring human judgment
- **To Planner:** confirmation of scheduled communications so calendar hooks are maintained
- **To Assessor:** documentation of parent-acknowledged interventions (closes the intervention loop)

## Done Criteria
- [ ] No open communication task older than 24 hours without a logged status
- [ ] Every drafted communication traces to a triggering input (assessment flag, schedule event, teacher request)
- [ ] Contact log is current for all flagged students
- [ ] During experimental phase: all sends are mocked; no live external communication issued without explicit teacher approval
- [ ] Escalation reports are delivered within 24 hours of a case meeting escalation criteria
- [ ] Draft comms and escalation summaries include an explicit **teacher next step** (approve, revise, send, defer, escalate) per [`architecture_and_workflows.md`](../architecture_and_workflows.md#teacher-next-bar)
