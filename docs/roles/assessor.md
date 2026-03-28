# Role: Assessor

## Purpose
Own the standards-aligned evidence loop. Collect, evaluate, and report on student learning; generate actionable outputs that drive instruction, intervention, and required reporting — all traceable to the standards and rubrics that govern them.

**Grading policy:** [`docs/grading-policy.md`](../grading-policy.md) — proficiency vs task design (including DOK), evidence bundles, and gradebook mapping expectations.

## Responsibilities
- Align assessments to learning objectives and NYS/NYC math standards
- Score or coordinate scoring of assessments; apply rubrics consistently
- Maintain grade books and mastery tracking per student, per standard
- Generate class-level and student-level performance reports
- Flag students at risk of failing, falling behind, or requiring intervention
- Track intervention outcomes: did the corrective action work?
- Produce required compliance reports (progress reports, report cards, SPED documentation)
- Audit assessment quality: are assessments actually measuring what they are intended to measure?
- During experimental phase: use dummy student data; no live grades issued

## Inputs
| Source | Artifact |
|---|---|
| Curriculum Designer | Learning objectives, rubrics, assessment instruments |
| Planner | Assessment windows, grading deadlines |
| Teacher | Scored work, observation notes, override decisions |
| School system | Standards documents, reporting templates, compliance deadlines |

## Outputs
| Artifact | Consumer |
|---|---|
| Mastery tracker (per student, per standard) | Teacher, Curriculum Designer |
| Class performance report | Teacher, Planner |
| At-risk / intervention flag list | Teacher, Communicator |
| Intervention outcome log | Teacher, Communicator |
| Compliance reports (progress reports, report cards) | Teacher, Admin |
| Assessment quality audit | Curriculum Designer, Teacher |

## Handoff Format

All tasks follow the schema defined in [`docs/roles/README.md`](README.md). This section documents task types specific to this role.

### Task naming convention

```
ASSESS-<FUNCTION>-<QUALIFIER>

Examples:
  ASSESS-INIT-UNIT-01
  ASSESS-SCORE-UNIT-01
  ASSESS-FLAGS-UNIT-01
  ASSESS-CLASS-UNIT-01
  ASSESS-AUDIT-UNIT-01
  ASSESS-REVISION-UNIT-01
```

---

### Tasks this role produces

#### `ASSESS-INIT-<QUALIFIER>` — Initialize mastery tracker

Written to `handoffs/` at the start of a unit, after assessment instruments and rubrics are available. Sets up the per-student, per-standard tracking structure that all downstream scoring tasks populate.

**Task JSON:**
```json
{
  "task_id": "ASSESS-INIT-UNIT-01",
  "goal": "Initialize the mastery tracker for Unit 1 across all Algebra I sections.",
  "plan": {
    "upstream_rubrics_task": "CURRDES-ASSESS-UNIT-01",
    "rubrics_file": "deliverables/rubrics_UNIT-01.json",
    "objectives_file": "deliverables/objectives_UNIT-01.json",
    "student_roster_source": "data/students/"
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "rubric_scale": "0-4 per standard",
    "experimental_phase": true
  },
  "deliverables": ["mastery_tracker_UNIT-01.json"],
  "timeout_seconds": 300,
  "created_at": "2026-09-08T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "ASSESS-INIT-UNIT-01",
  "status": "done",
  "summary": "Mastery tracker initialized for Unit 1. 81 students across ALG-01, ALG-02, ALG-03. 2 standards tracked (CCSS.MATH.CONTENT.8.EE.C.7, .C.8). All scores initialized to null.",
  "deliverables": {
    "mastery_tracker_UNIT-01.json": "deliverables/mastery_tracker_UNIT-01.json"
  },
  "completed_at": "2026-09-08T08:02:10Z",
  "version": 1
}
```

**Deliverable format:**

`mastery_tracker_UNIT-01.json` — Per-student, per-standard mastery record:
```json
{
  "unit": "UNIT-01",
  "sections": ["ALG-01", "ALG-02", "ALG-03"],
  "standards": ["CCSS.MATH.CONTENT.8.EE.C.7", "CCSS.MATH.CONTENT.8.EE.C.8"],
  "students": [
    {
      "student_id": "1000001",
      "section": "ALG-01",
      "scores": {
        "CCSS.MATH.CONTENT.8.EE.C.7": {
          "exit_ticket": null,
          "mid_unit_quiz": null,
          "end_unit_test": null,
          "mastery_level": null
        },
        "CCSS.MATH.CONTENT.8.EE.C.8": {
          "exit_ticket": null,
          "mid_unit_quiz": null,
          "end_unit_test": null,
          "mastery_level": null
        }
      },
      "accommodations_applied": ["extended_time"],
      "at_risk": false,
      "intervention_flag": null
    }
  ]
}
```

---

#### `ASSESS-SCORE-<QUALIFIER>` — Score assessment and update mastery tracker

Written to `handoffs/` after an assessment window closes and scored work is available. Updates the mastery tracker with actual scores.

**Task JSON:**
```json
{
  "task_id": "ASSESS-SCORE-UNIT-01",
  "goal": "Score Unit 1 end-unit test results and update mastery tracker for all Algebra I sections.",
  "plan": {
    "upstream_init_task": "ASSESS-INIT-UNIT-01",
    "mastery_tracker_file": "deliverables/mastery_tracker_UNIT-01.json",
    "rubrics_file": "deliverables/rubrics_UNIT-01.json",
    "assessment_type": "end_unit_test",
    "scored_work_source": "teacher_provided"
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "turnaround_hours": 48,
    "experimental_phase": true,
    "note": "In experimental phase, generate synthetic scores consistent with student profiles."
  },
  "deliverables": ["mastery_tracker_UNIT-01.json"],
  "timeout_seconds": 600,
  "created_at": "2026-10-01T16:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "ASSESS-SCORE-UNIT-01",
  "status": "done",
  "summary": "End-unit test scored for 81 students. Mastery tracker updated. Class average: 2.8/4. 12 students below mastery threshold (score < 2) on CCSS.MATH.CONTENT.8.EE.C.7.",
  "deliverables": {
    "mastery_tracker_UNIT-01.json": "deliverables/mastery_tracker_UNIT-01.json"
  },
  "completed_at": "2026-10-01T16:04:55Z",
  "version": 2
}
```

---

#### `ASSESS-FLAGS-<QUALIFIER>` — Identify at-risk students

Written to `handoffs/` after scoring is complete. Applies threshold criteria to mastery data and generates an intervention flag list. Consumed by the Communicator and the Teacher.

**Task JSON:**
```json
{
  "task_id": "ASSESS-FLAGS-UNIT-01",
  "goal": "Identify students at risk of falling below mastery after Unit 1 end-unit test.",
  "plan": {
    "upstream_score_task": "ASSESS-SCORE-UNIT-01",
    "mastery_tracker_file": "deliverables/mastery_tracker_UNIT-01.json",
    "flag_criteria": {
      "mastery_level_below": 2,
      "standards_failing_count_gte": 1
    }
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "flag_within_hours": 24
  },
  "deliverables": ["flags_UNIT-01.json"],
  "timeout_seconds": 300,
  "created_at": "2026-10-01T17:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "ASSESS-FLAGS-UNIT-01",
  "status": "done",
  "summary": "12 students flagged at-risk across ALG-01 (5), ALG-02 (4), ALG-03 (3). Primary standard: CCSS.MATH.CONTENT.8.EE.C.7. Flags written to flags_UNIT-01.json. Communicator should be triggered.",
  "deliverables": {
    "flags_UNIT-01.json": "deliverables/flags_UNIT-01.json"
  },
  "completed_at": "2026-10-01T17:01:45Z",
  "version": 1
}
```

**Deliverable format:**

`flags_UNIT-01.json` — Array of intervention flags:
```json
[
  {
    "flag_id": "FLAG-UNIT01-1000001",
    "student_id": "1000001",
    "section": "ALG-01",
    "trigger": "below_mastery_threshold",
    "standards_failing": ["CCSS.MATH.CONTENT.8.EE.C.7"],
    "mastery_levels": {
      "CCSS.MATH.CONTENT.8.EE.C.7": 1
    },
    "recommended_action": "re_teaching",
    "iep_504_active": true,
    "plan_type": "IEP",
    "flagged_at": "2026-10-01T17:01:45Z",
    "status": "open"
  }
]
```

---

#### `ASSESS-CLASS-<QUALIFIER>` — Generate class performance report

Written to `handoffs/` after scoring is complete. Produces an aggregate performance summary for the Teacher and Planner.

**Task JSON:**
```json
{
  "task_id": "ASSESS-CLASS-UNIT-01",
  "goal": "Generate class-level performance report for Unit 1 across all Algebra I sections.",
  "plan": {
    "upstream_score_task": "ASSESS-SCORE-UNIT-01",
    "mastery_tracker_file": "deliverables/mastery_tracker_UNIT-01.json",
    "report_dimensions": ["by_section", "by_standard", "by_plan_type"]
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "suppress_individual_ids": false,
    "experimental_phase": true
  },
  "deliverables": ["class_report_UNIT-01.md"],
  "timeout_seconds": 300,
  "created_at": "2026-10-02T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "ASSESS-CLASS-UNIT-01",
  "status": "done",
  "summary": "Class performance report generated for Unit 1. Sections ALG-01/02/03. Average mastery 2.8/4. ICT section (ALG-02) average 2.6/4. IEP students average 2.2/4. 12 at-risk flags active.",
  "deliverables": {
    "class_report_UNIT-01.md": "deliverables/class_report_UNIT-01.md"
  },
  "completed_at": "2026-10-02T08:02:30Z",
  "version": 1
}
```

**Deliverable format:**

`class_report_UNIT-01.md` — Markdown report with sections:
- Summary table: Section × Standard × Average mastery score
- Plan-type breakdown: gen ed / IEP / 504 / ELL averages per standard
- At-risk count by section
- Recommended instructional adjustments (re-teaching, extension, pacing)

---

#### `ASSESS-AUDIT-<QUALIFIER>` — Audit assessment quality

Written to `handoffs/` after an assessment has been scored to evaluate whether the instrument measured what it was designed to measure. Consumed by the Curriculum Designer.

**Task JSON:**
```json
{
  "task_id": "ASSESS-AUDIT-UNIT-01",
  "goal": "Audit the Unit 1 end-unit test for alignment, item quality, and scoring consistency.",
  "plan": {
    "upstream_score_task": "ASSESS-SCORE-UNIT-01",
    "assessments_file": "deliverables/assessments_UNIT-01.md",
    "rubrics_file": "deliverables/rubrics_UNIT-01.json",
    "mastery_tracker_file": "deliverables/mastery_tracker_UNIT-01.json",
    "audit_dimensions": ["standard_alignment", "item_discrimination", "rubric_consistency"]
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"]
  },
  "deliverables": ["audit_UNIT-01.md"],
  "timeout_seconds": 300,
  "created_at": "2026-10-03T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "ASSESS-AUDIT-UNIT-01",
  "status": "done",
  "summary": "Assessment audit complete for Unit 1. Item 3 shows low discrimination index (0.12) — may not differentiate mastery levels on CCSS.MATH.CONTENT.8.EE.C.7. Rubric level 3 description ambiguous. Revision recommended.",
  "deliverables": {
    "audit_UNIT-01.md": "deliverables/audit_UNIT-01.md"
  },
  "completed_at": "2026-10-03T08:03:15Z",
  "version": 1
}
```

---

#### `ASSESS-REVISION-<QUALIFIER>` — Request lesson or material revision from Curriculum Designer

Written to `handoffs/` when mastery data indicates a lesson, unit, or assessment instrument needs revision. Consumed by the Curriculum Designer.

**Task JSON:**
```json
{
  "task_id": "ASSESS-REVISION-UNIT-01",
  "goal": "Request revision of Unit 1 lessons L03–L05 based on below-mastery results on CCSS.MATH.CONTENT.8.EE.C.7.",
  "plan": {
    "upstream_flags_task": "ASSESS-FLAGS-UNIT-01",
    "mastery_tracker_file": "deliverables/mastery_tracker_UNIT-01.json",
    "flags_file": "deliverables/flags_UNIT-01.json",
    "affected_lessons": ["L03", "L04", "L05"],
    "affected_standard": "CCSS.MATH.CONTENT.8.EE.C.7",
    "revision_type": "re_teaching"
  },
  "constraints": {
    "sections": ["ALG-01", "ALG-02", "ALG-03"],
    "revision_due_before_lesson": "L06"
  },
  "deliverables": ["mastery_tracker_UNIT-01.json", "flags_UNIT-01.json"],
  "timeout_seconds": 300,
  "created_at": "2026-10-02T09:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "ASSESS-REVISION-UNIT-01",
  "status": "done",
  "summary": "Revision request written for Unit 1 lessons L03–L05. 12 students below mastery on CCSS.MATH.CONTENT.8.EE.C.7. Mastery tracker and flags handed to Curriculum Designer.",
  "deliverables": {
    "mastery_tracker_UNIT-01.json": "deliverables/mastery_tracker_UNIT-01.json",
    "flags_UNIT-01.json": "deliverables/flags_UNIT-01.json"
  },
  "completed_at": "2026-10-02T09:01:00Z",
  "version": 1
}
```

---

### Tasks this role consumes

#### `CURRDES-ASSESS-<QUALIFIER>` result — Assessment instruments and rubrics from Curriculum Designer

The Assessor reads rubrics and assessment instruments before initializing the mastery tracker.

**Upstream result JSON (written by Curriculum Designer to `results/`):**
```json
{
  "task_id": "CURRDES-ASSESS-UNIT-01",
  "status": "done",
  "summary": "Assessment instruments and rubrics generated for Unit 1.",
  "deliverables": {
    "assessments_UNIT-01.md": "deliverables/assessments_UNIT-01.md",
    "rubrics_UNIT-01.json": "deliverables/rubrics_UNIT-01.json"
  },
  "completed_at": "2026-09-08T08:06:10Z",
  "version": 1
}
```

**Action:** Assessor reads `rubrics_UNIT-01.json` and `assessments_UNIT-01.md`, then writes `ASSESS-INIT-UNIT-01`.

#### `PLAN-CONFIRM-<QUALIFIER>` result — Assessment window dates from Planner

The Assessor reads confirmed time blocks to know when assessment windows open and when scoring turnaround is due.

**Upstream result JSON (written by Planner to `results/`):**
```json
{
  "task_id": "PLAN-CONFIRM-UNIT-01",
  "status": "done",
  "summary": "Time blocks confirmed for Unit 1.",
  "deliverables": {
    "time_blocks_UNIT-01.json": "deliverables/time_blocks_UNIT-01.json"
  },
  "completed_at": "2026-09-01T09:03:00Z",
  "version": 1
}
```

**Action:** Assessor reads `time_blocks_UNIT-01.json` to identify assessment window dates and set scoring deadlines.

#### `COMMS-LOG-<QUALIFIER>` result — Parent-acknowledged interventions from Communicator

The Assessor reads contact logs to close the intervention loop: has the flagged student's parent acknowledged the intervention?

**Upstream result JSON (written by Communicator to `results/`):**
```json
{
  "task_id": "COMMS-LOG-UNIT-01",
  "status": "done",
  "summary": "Contact log updated. 8 of 12 intervention notifications acknowledged by parent.",
  "deliverables": {
    "contact_log_UNIT-01.json": "deliverables/contact_log_UNIT-01.json"
  },
  "completed_at": "2026-10-05T10:00:00Z",
  "version": 2
}
```

**Action:** Assessor reads `contact_log_UNIT-01.json` and updates intervention flag status to `acknowledged` or escalates non-responsive cases.

## Handoffs
- **To Curriculum Designer:** mastery data and performance patterns that inform lesson adjustment or re-teaching
- **To Communicator:** at-risk flags and intervention status that trigger parent/student communication
- **To Planner:** grading timelines and reporting deadlines that affect schedule
- **To Teacher:** escalations requiring professional judgment (anomalous results, SPED considerations, grade disputes)

## Done Criteria
- [ ] Every assessment has a rubric traceable to at least one named standard
- [ ] Mastery tracker is updated within 48 hours of assessment completion
- [ ] At-risk flags are issued within 24 hours of a student meeting threshold criteria
- [ ] Intervention outcomes are logged within one instructional cycle of the intervention
- [ ] All compliance reports are submitted by their deadlines with a logged confirmation
- [ ] During experimental phase: all outputs use dummy data; no live grades or reports issued without explicit teacher sign-off
