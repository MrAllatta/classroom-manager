# Role: Planner

## Purpose
Own calendar-based coordination across the full classroom cycle. Connect objectives, time, people, and required follow-up so nothing falls through scheduling gaps.

## Canonical data vs `deliverables/`

Official calendar boundaries, holidays, and Regents-style windows belong in **`data/school/calendar_<school_year>.yaml`** (and references from `data/school/context.yaml`). Pacing exports under **`deliverables/`** (for example `calendar_*_fullyear.json`) are **snapshots** and may be **out of date** relative to `data/`. When answering “what dates apply this year?”, prefer the calendar files under **`data/`**. Regenerate named deliverables only when a task or review explicitly requires an updated export. **Agent default:** editing `data/school/calendar*.yaml` does not require patching `deliverables/` unless requested. See [`deliverables/README.md`](../../deliverables/README.md) and [`.cursor/rules/canonical-data-vs-deliverables.mdc`](../../.cursor/rules/canonical-data-vs-deliverables.mdc).

## Responsibilities
- Maintain and update the master calendar (unit schedule, assessment windows, school calendar overlays)
- Translate curriculum scope and sequence into time-blocked lesson plans
- Track pacing against the planned sequence; flag drift early
- Schedule recurring events: parent conferences, IEP/504 meetings, make-up windows, department deadlines
- Create and distribute agendas for meetings the teacher owns
- Surface upcoming conflicts and resource constraints before they become problems
- Log completed schedule events with outcomes for continuity

## Inputs
| Source | Artifact |
|---|---|
| Curriculum Designer | Scope and sequence, unit plans, lesson drafts |
| Assessor | Assessment windows, grading turnaround requirements |
| Communicator | Scheduled communications requiring calendar hooks |
| School system | Official calendar, blackout dates, department deadlines |
| Teacher | Priorities, constraints, override decisions |

## Outputs
| Artifact | Consumer |
|---|---|
| Master calendar (week / unit / term views) | Teacher, all roles |
| Time-blocked lesson schedule | Curriculum Designer, Teacher |
| Pacing status report (on-track / at-risk / behind) | Teacher, Curriculum Designer |
| Meeting agendas | Teacher, Communicator |
| Conflict flags | Teacher (for decision) |

## Handoffs
- **To Curriculum Designer:** confirmed time blocks and pacing constraints so materials are scoped to available time
- **To Assessor:** assessment window dates and any schedule changes that compress turnaround
- **To Communicator:** confirmed event dates that require parent/student communication
- **To Teacher:** escalation of conflicts requiring human decision

## Handoff Format

All tasks follow the schema defined in [`docs/roles/README.md`](README.md). This section documents task types specific to this role.

### Task naming convention

```
PLAN-<FUNCTION>-<QUALIFIER>

Examples:
  PLAN-CALENDAR-FALL-2026
  PLAN-PACING-WEEK-03
  PLAN-CONFIRM-UNIT-01
  PLAN-COMMS-UNIT-01
  PLAN-ADJUST-UNIT-02
```

---

### Tasks this role produces

#### `PLAN-CALENDAR-<QUALIFIER>` — Generate master calendar

Written to `handoffs/` at the start of a term or when the school calendar changes. Consumed by all roles and the Teacher.

**Task JSON:**
```json
{
  "task_id": "PLAN-CALENDAR-FALL-2026",
  "goal": "Generate the master calendar for Fall 2026 covering all sections, assessment windows, and school events.",
  "plan": {
    "term_start": "2026-09-08",
    "term_end": "2027-01-23",
    "sections": ["ALG-01", "ALG-02", "ALG-03", "AP-STAT", "AP-CSA"],
    "school_calendar_source": "data/school/context.yaml"
  },
  "constraints": {
    "blackout_dates": ["2026-11-25", "2026-11-26", "2026-12-24", "2026-12-25", "2027-01-01"],
    "no_test_on_monday": true,
    "ap_exam_windows_reserved": true
  },
  "deliverables": ["calendar_FALL-2026.json", "calendar_FALL-2026.md"],
  "timeout_seconds": 600,
  "created_at": "2026-08-25T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "PLAN-CALENDAR-FALL-2026",
  "status": "done",
  "summary": "Master calendar generated for Fall 2026. 18 instructional weeks. 4 blackout dates excluded. Assessment windows reserved for each unit in ALG-01/02/03. AP exam prep windows flagged for AP-STAT and AP-CSA.",
  "deliverables": {
    "calendar_FALL-2026.json": "deliverables/calendar_FALL-2026.json",
    "calendar_FALL-2026.md": "deliverables/calendar_FALL-2026.md"
  },
  "completed_at": "2026-08-25T08:05:14Z",
  "version": 1
}
```

**Deliverable formats:**

`calendar_FALL-2026.json` — Structured calendar keyed by week and date:
```json
{
  "term": "Fall 2026",
  "weeks": [
    {
      "week_number": 1,
      "start_date": "2026-09-08",
      "end_date": "2026-09-12",
      "days": [
        {
          "date": "2026-09-08",
          "type": "instructional",
          "sections_meeting": ["ALG-01", "ALG-02", "ALG-03", "AP-STAT", "AP-CSA"],
          "notes": "First day of school."
        }
      ]
    }
  ]
}
```

`calendar_FALL-2026.md` — Human-readable weekly calendar with unit assignments, assessment windows, and flagged events per section.

---

#### `PLAN-PACING-<QUALIFIER>` — Generate pacing status report

Written to `handoffs/` weekly or after a significant schedule change. Consumed by the Teacher and the Curriculum Designer.

**Task JSON:**
```json
{
  "task_id": "PLAN-PACING-WEEK-03",
  "goal": "Generate pacing status report for all sections after week 3.",
  "plan": {
    "upstream_calendar_task": "PLAN-CALENDAR-FALL-2026",
    "upstream_scope_task": "CURRDES-SCOPE-UNIT-01",
    "calendar_file": "deliverables/calendar_FALL-2026.json",
    "scope_file": "deliverables/scope_UNIT-01.md",
    "reporting_week": 3
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03", "AP-STAT", "AP-CSA"],
    "flag_threshold_days_behind": 2
  },
  "deliverables": ["pacing_WEEK-03.md"],
  "timeout_seconds": 300,
  "created_at": "2026-09-26T15:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "PLAN-PACING-WEEK-03",
  "status": "done",
  "summary": "Pacing report generated for week 3. ALG-01 and ALG-03 on track. ALG-02 one lesson behind due to fire drill on 2026-09-22. AP-STAT and AP-CSA on track.",
  "deliverables": {
    "pacing_WEEK-03.md": "deliverables/pacing_WEEK-03.md"
  },
  "completed_at": "2026-09-26T15:02:45Z",
  "version": 1
}
```

**Deliverable format:**

`pacing_WEEK-03.md` — Markdown table per section with columns: Section, Planned Lesson, Actual Lesson, Status (on-track / at-risk / behind), Notes.

---

#### `PLAN-CONFIRM-<QUALIFIER>` — Confirm time blocks for a unit

Written to `handoffs/` after the master calendar exists and a scope is available. Consumed by the Curriculum Designer (triggers lesson plan generation).

**Task JSON:**
```json
{
  "task_id": "PLAN-CONFIRM-UNIT-01",
  "goal": "Confirm and assign time blocks for Unit 1 lessons across all Algebra I sections.",
  "plan": {
    "upstream_calendar_task": "PLAN-CALENDAR-FALL-2026",
    "upstream_scope_task": "CURRDES-SCOPE-UNIT-01",
    "calendar_file": "deliverables/calendar_FALL-2026.json",
    "scope_file": "deliverables/scope_UNIT-01.md"
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "unit_start_date": "2026-09-08",
    "unit_end_date": "2026-10-02",
    "buffer_days": 2
  },
  "deliverables": ["time_blocks_UNIT-01.json"],
  "timeout_seconds": 300,
  "created_at": "2026-09-01T09:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "PLAN-CONFIRM-UNIT-01",
  "status": "done",
  "summary": "Time blocks confirmed for Unit 1 (L01–L12) across ALG-01, ALG-02, ALG-03. Assessment window: 2026-09-29 to 2026-10-01. Two buffer days included.",
  "deliverables": {
    "time_blocks_UNIT-01.json": "deliverables/time_blocks_UNIT-01.json"
  },
  "completed_at": "2026-09-01T09:03:00Z",
  "version": 1
}
```

**Deliverable format:**

`time_blocks_UNIT-01.json` — Array of lesson-to-date assignments:
```json
[
  {
    "lesson_id": "L01",
    "section": "ALG-01",
    "date": "2026-09-08",
    "period": 1,
    "duration_minutes": 45
  },
  {
    "lesson_id": "L01",
    "section": "ALG-02",
    "date": "2026-09-08",
    "period": 2,
    "duration_minutes": 45
  }
]
```

---

#### `PLAN-COMMS-<QUALIFIER>` — Confirm scheduled communication dates

Written to `handoffs/` when calendar events require parent or student communication. Consumed by the Communicator.

**Task JSON:**
```json
{
  "task_id": "PLAN-COMMS-UNIT-01",
  "goal": "Confirm scheduled communication dates tied to Unit 1 events (assessment window, progress reports).",
  "plan": {
    "upstream_time_blocks_task": "PLAN-CONFIRM-UNIT-01",
    "time_blocks_file": "deliverables/time_blocks_UNIT-01.json",
    "communication_triggers": ["assessment_window_open", "progress_report_due"]
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "advance_notice_days": 3
  },
  "deliverables": ["comms_schedule_UNIT-01.json"],
  "timeout_seconds": 300,
  "created_at": "2026-09-05T09:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "PLAN-COMMS-UNIT-01",
  "status": "done",
  "summary": "Communication schedule generated for Unit 1. 2 scheduled communications: assessment window notice (2026-09-26) and progress report notice (2026-10-03).",
  "deliverables": {
    "comms_schedule_UNIT-01.json": "deliverables/comms_schedule_UNIT-01.json"
  },
  "completed_at": "2026-09-05T09:01:30Z",
  "version": 1
}
```

**Deliverable format:**

`comms_schedule_UNIT-01.json` — Array of scheduled communications:
```json
[
  {
    "communication_id": "COMMS-EVT-UNIT01-01",
    "trigger": "assessment_window_open",
    "send_date": "2026-09-26",
    "audience": "parents_and_students",
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "context": "Unit 1 end-unit test window opens 2026-09-29."
  }
]
```

---

#### `PLAN-ADJUST-<QUALIFIER>` — Adjust pacing due to conflicts

Written to `handoffs/` when a schedule disruption requires re-allocating time blocks. Consumed by the Curriculum Designer and the Teacher.

**Task JSON:**
```json
{
  "task_id": "PLAN-ADJUST-UNIT-01",
  "goal": "Adjust Unit 1 time blocks for ALG-02 after one instructional period was lost to fire drill on 2026-09-22.",
  "plan": {
    "upstream_time_blocks_task": "PLAN-CONFIRM-UNIT-01",
    "time_blocks_file": "deliverables/time_blocks_UNIT-01.json",
    "disruption": {
      "section": "ALG-02",
      "date_lost": "2026-09-22",
      "lesson_affected": "L08"
    }
  },
  "constraints": {
    "cannot_push_past_date": "2026-10-02",
    "preserve_assessment_window": true
  },
  "deliverables": ["time_blocks_UNIT-01.json"],
  "timeout_seconds": 300,
  "created_at": "2026-09-22T16:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "PLAN-ADJUST-UNIT-01",
  "status": "done",
  "summary": "ALG-02 time blocks adjusted. L08 rescheduled to 2026-09-23 (previously L09 slot). L09 compressed into L10. Assessment window preserved. Teacher approval required before finalizing.",
  "deliverables": {
    "time_blocks_UNIT-01.json": "deliverables/time_blocks_UNIT-01.json"
  },
  "completed_at": "2026-09-22T16:02:10Z",
  "version": 2
}
```

---

### Tasks this role consumes

#### `CURRDES-SCOPE-<QUALIFIER>` result — Scope and sequence from Curriculum Designer

The Planner reads the scope result to assign time blocks and generate the unit calendar.

**Upstream result JSON (written by Curriculum Designer to `results/`):**
```json
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "status": "done",
  "summary": "Scope and sequence generated for Unit 1.",
  "deliverables": {
    "scope_UNIT-01.md": "deliverables/scope_UNIT-01.md",
    "objectives_UNIT-01.json": "deliverables/objectives_UNIT-01.json"
  },
  "completed_at": "2026-09-01T08:04:22Z",
  "version": 1
}
```

**Action:** Planner reads `scope_UNIT-01.md` for estimated lesson count and constraints, then writes `PLAN-CONFIRM-UNIT-01`.

#### `COMMS-LOG-<QUALIFIER>` result — Confirmed communication schedule from Communicator

The Planner reads communication confirmations to keep calendar hooks current.

**Upstream result JSON (written by Communicator to `results/`):**
```json
{
  "task_id": "COMMS-LOG-UNIT-01",
  "status": "done",
  "summary": "Contact log initialized. 2 scheduled communications confirmed for Unit 1.",
  "deliverables": {
    "contact_log_UNIT-01.json": "deliverables/contact_log_UNIT-01.json"
  },
  "completed_at": "2026-09-06T10:00:00Z",
  "version": 1
}
```

**Action:** Planner updates calendar hooks to reflect confirmed send dates.

---

## Done Criteria
- [ ] The master calendar reflects all current unit plans, assessment windows, and school dates
- [ ] Pacing status is current (updated at least weekly)
- [ ] No unresolved scheduling conflicts older than 48 hours without a logged teacher decision
- [ ] All handoff artifacts are versioned and traceable to their source inputs
- [ ] Scheduled events include outcomes logged within 24 hours of occurrence
