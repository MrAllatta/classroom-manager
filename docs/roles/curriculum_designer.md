# Role: Curriculum Designer

## Purpose
Own the full instructional content loop: research what works, build and adapt scope and sequence, write lesson materials and assessments, and revise based on mastery data. This role collapses the Researcher and Curriculum candidate areas into a single owner to prevent a handoff inside the knowledge-to-material pipeline.

## Canonical data vs `deliverables/`

Full-year scope and sequence for a course is canonical in **`data/courses/<course_id>/scope.yaml`** (referenced by section files). JSON or markdown under **`deliverables/`** (for example `scope_*_fullyear.json`) are **exports or snapshots** and may **lag** behind `data/`. Update **`data/`** when the teacher-approved truth changes; refresh **`deliverables/`** only when producing a reviewed artifact or satisfying a task that names those paths. See [`deliverables/README.md`](../../deliverables/README.md).

## Responsibilities
- Maintain and adapt the scope and sequence for each unit and the full term
- Align all materials to NYS/NYC math standards and evidence-based instructional practice
- Research and evaluate external curricula, pedagogical frameworks, and relevant academic literature
- Write or adapt lesson plans, student-facing materials, and formative/summative assessments
- Build and maintain rubrics tied to named standards
- Revise lessons and units in response to Assessor performance data (re-teaching, extension, differentiation)
- Differentiate materials for IEP/504 students and English Language Learners as needed
- Audit material quality: does content reflect rigorous, research-grounded practice?
- During experimental phase: produce materials for dummy units; validate end-to-end flow before live deployment

## Inputs
| Source | Artifact |
|---|---|
| Assessor | Mastery tracker, performance patterns, assessment quality audits |
| Planner | Available time blocks, pacing constraints |
| Teacher | Priority standards, pedagogical preferences, override decisions |
| External | NYS/NYC standards documents, research literature, established curricula (e.g., Illustrative Math, EngageNY) |

## Outputs
| Artifact | Consumer |
|---|---|
| Scope and sequence (unit and term level) | Planner, Teacher |
| Unit plans | Planner, Teacher |
| Lesson plans (time-bound, standard-aligned) | Planner, Teacher |
| Student-facing materials (worksheets, tasks, readings) | Teacher |
| Formative and summative assessment instruments | Assessor, Teacher |
| Rubrics (standard-aligned, scoreable) | Assessor, Teacher |
| Differentiated materials (IEP/504, ELL) | Teacher |
| Research summary / justification for major design decisions | Teacher |

## Handoff Format

All tasks follow the schema defined in [`docs/roles/README.md`](README.md). This section documents task types specific to this role.

### Task naming convention

```
CURRDES-<FUNCTION>-<QUALIFIER>

Examples:
  CURRDES-SCOPE-UNIT-01
  CURRDES-ASSESS-UNIT-01
  CURRDES-LESSONS-UNIT-01
```

---

### Tasks this role produces

#### `CURRDES-SCOPE-<QUALIFIER>` — Generate scope and sequence

Written to `handoffs/` by the Curriculum Designer when a new unit or term scope is needed. Consumed by the Planner (for time block assignment) and the Teacher (for review).

**Task JSON:**
```json
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "goal": "Generate scope and sequence for Unit 1: Linear Equations",
  "plan": {
    "standards": ["CCSS.MATH.CONTENT.8.EE.C.7", "CCSS.MATH.CONTENT.8.EE.C.8"],
    "estimated_lessons": 12,
    "source_curricula": ["Illustrative Math Grade 8", "EngageNY Module 4"]
  },
  "constraints": {
    "section_ids": ["ALG-01", "ALG-02", "ALG-03"],
    "available_weeks": 4,
    "ict_sections": ["ALG-02"]
  },
  "deliverables": ["scope_UNIT-01.md", "objectives_UNIT-01.json"],
  "timeout_seconds": 600,
  "created_at": "2026-09-01T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "status": "done",
  "summary": "Scope and sequence generated for Unit 1: Linear Equations. 12 lessons across 4 weeks. Standards CCSS.MATH.CONTENT.8.EE.C.7 and .C.8 covered. Differentiated objectives included for IEP/ELL students.",
  "deliverables": {
    "scope_UNIT-01.md": "deliverables/scope_UNIT-01.md",
    "objectives_UNIT-01.json": "deliverables/objectives_UNIT-01.json"
  },
  "completed_at": "2026-09-01T08:04:22Z",
  "version": 1
}
```

**Deliverable formats:**

`scope_UNIT-01.md` — Markdown document with:
- Unit title, grade level, course, and section applicability
- Standards addressed (CCSS/College Board identifiers)
- Lesson sequence (numbered, titled, time-estimated)
- Research or curriculum sources for major design decisions
- Differentiation notes for IEP/504 and ELL students

`objectives_UNIT-01.json` — JSON array of learning objectives:
```json
[
  {
    "objective_id": "OBJ-UNIT01-01",
    "standard": "CCSS.MATH.CONTENT.8.EE.C.7",
    "description": "Solve linear equations in one variable with rational number coefficients.",
    "lesson_refs": ["L01", "L02", "L03"],
    "differentiation": {
      "iep_504_note": "Provide equation mats and step-by-step template for students with processing accommodations.",
      "ell_note": "Pre-teach vocabulary: coefficient, variable, solution."
    }
  }
]
```

---

#### `CURRDES-ASSESS-<QUALIFIER>` — Generate assessments and rubrics

Written to `handoffs/` when assessment instruments are needed for an upcoming assessment window. Consumed by the Assessor (for scoring alignment) and the Teacher (for review).

**Task JSON:**
```json
{
  "task_id": "CURRDES-ASSESS-UNIT-01",
  "goal": "Generate formative and summative assessment instruments with rubrics for Unit 1.",
  "plan": {
    "upstream_task": "CURRDES-SCOPE-UNIT-01",
    "objectives_file": "deliverables/objectives_UNIT-01.json",
    "assessment_types": ["exit_ticket", "mid_unit_quiz", "end_unit_test"]
  },
  "constraints": {
    "section_ids": ["ALG-01", "ALG-02", "ALG-03"],
    "extended_time_sections": ["ALG-02"],
    "rubric_scale": "0-4 per standard"
  },
  "deliverables": ["assessments_UNIT-01.md", "rubrics_UNIT-01.json"],
  "timeout_seconds": 600,
  "created_at": "2026-09-08T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "CURRDES-ASSESS-UNIT-01",
  "status": "done",
  "summary": "Generated 3 assessment instruments (exit ticket, mid-unit quiz, end-unit test) and aligned rubrics for Unit 1. All instruments trace to objectives_UNIT-01.json. Rubric scale: 0–4 per standard.",
  "deliverables": {
    "assessments_UNIT-01.md": "deliverables/assessments_UNIT-01.md",
    "rubrics_UNIT-01.json": "deliverables/rubrics_UNIT-01.json"
  },
  "completed_at": "2026-09-08T08:06:10Z",
  "version": 1
}
```

**Deliverable formats:**

`assessments_UNIT-01.md` — Markdown document with each assessment instrument as a section:
- Assessment type and window (date range)
- Items grouped by standard
- Accommodation notes (extended time, reduced items, oral response options)
- Scoring guidance cross-referenced to rubrics

`rubrics_UNIT-01.json` — JSON array of rubric entries:
```json
[
  {
    "rubric_id": "RUB-UNIT01-01",
    "standard": "CCSS.MATH.CONTENT.8.EE.C.7",
    "objective_id": "OBJ-UNIT01-01",
    "scale": {
      "4": "Solves multi-step linear equations independently; explains each step.",
      "3": "Solves linear equations with minor errors; self-corrects.",
      "2": "Solves one-step equations; struggles with multi-step.",
      "1": "Attempts but makes systematic errors; requires significant support.",
      "0": "No evidence of engagement with the standard."
    }
  }
]
```

---

#### `CURRDES-LESSONS-<QUALIFIER>` — Generate lesson plans

Written to `handoffs/` when time-blocked lesson plans are needed. Requires confirmed time blocks from the Planner (`PLAN-CONFIRM-*` result) as upstream input. Consumed by the Teacher.

**Task JSON:**
```json
{
  "task_id": "CURRDES-LESSONS-UNIT-01",
  "goal": "Generate full lesson plans for Unit 1 lessons L01–L12.",
  "plan": {
    "upstream_scope_task": "CURRDES-SCOPE-UNIT-01",
    "upstream_time_blocks_task": "PLAN-CONFIRM-UNIT-01",
    "scope_file": "deliverables/scope_UNIT-01.md",
    "time_blocks_file": "deliverables/time_blocks_UNIT-01.json",
    "lesson_ids": ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12"]
  },
  "constraints": {
    "section_ids": ["ALG-01", "ALG-02", "ALG-03"],
    "period_length_minutes": 45,
    "ict_co_teaching_sections": ["ALG-02"]
  },
  "deliverables": ["lessons_UNIT-01.md"],
  "timeout_seconds": 900,
  "created_at": "2026-09-10T08:00:00Z",
  "status": "queued"
}
```

**Result JSON:**
```json
{
  "task_id": "CURRDES-LESSONS-UNIT-01",
  "status": "done",
  "summary": "Generated 12 lesson plans for Unit 1. Each lesson includes standard, objective, launch, explore, discuss, and close phases. ICT co-teaching notes included for ALG-02.",
  "deliverables": {
    "lessons_UNIT-01.md": "deliverables/lessons_UNIT-01.md"
  },
  "completed_at": "2026-09-10T08:12:44Z",
  "version": 1
}
```

**Deliverable format:**

`lessons_UNIT-01.md` — Markdown document with one section per lesson:
- Lesson ID, title, date (from time blocks), section(s)
- Standard(s) and objective(s) addressed
- Time-phased structure: Launch / Explore / Discuss / Close (minutes per phase)
- Materials and resources needed
- ICT co-teaching notes (for ALG-02 only)
- Differentiation notes (IEP/504 and ELL)
- Formative check (exit ticket or equivalent)

---

### Tasks this role consumes

#### `ASSESS-REVISION-<QUALIFIER>` — Revision request from Assessor

Written by the Assessor when mastery data indicates a lesson or unit requires revision. The Curriculum Designer reads this result and initiates a revision cycle.

**Upstream result JSON (written by Assessor to `results/`):**
```json
{
  "task_id": "ASSESS-REVISION-UNIT-01",
  "status": "done",
  "summary": "Unit 1 end-unit test results indicate 40% of ALG-01 students below mastery on CCSS.MATH.CONTENT.8.EE.C.7. Re-teaching or lesson revision recommended for L03–L05.",
  "deliverables": {
    "mastery_tracker_UNIT-01.json": "deliverables/mastery_tracker_UNIT-01.json",
    "flags_UNIT-01.json": "deliverables/flags_UNIT-01.json"
  },
  "completed_at": "2026-09-25T14:00:00Z",
  "version": 1
}
```

**Action:** The Curriculum Designer reads `mastery_tracker_UNIT-01.json` and `flags_UNIT-01.json`, then writes a new `CURRDES-LESSONS-*` task (revision version, `version: 2`) targeting the flagged lessons.

## Handoffs
- **To Planner:** scope and sequence and unit plans so time blocks can be assigned
- **To Assessor:** assessment instruments and rubrics so scoring is aligned from the start
- **To Teacher:** all student-facing materials and lesson plans; research justifications for significant design choices
- **Internal feedback loop:** receives mastery data from Assessor and closes the loop by revising materials

See [Handoff Format](#handoff-format) above for task schemas and deliverable specifications.

## Done Criteria
- [ ] Every lesson traces to at least one named standard and one research or curriculum source
- [ ] Every assessment instrument has a corresponding rubric in the Assessor's possession before the assessment window opens
- [ ] Scope and sequence is updated within one instructional cycle of a confirmed pacing change
- [ ] Differentiated versions exist for all assessments flagged as requiring them
- [ ] Material revisions triggered by Assessor data are completed within one unit cycle
- [ ] During experimental phase: all materials are dummy/sample; live student-facing deployment requires explicit teacher approval
