# Classroom Team — Role Overview

## Team structure

| Role | Primary loop owned | File |
|---|---|---|
| **Co-Teacher (Inés Vidal)** | Team coherence, role design, system maintenance | [co-teacher.md](../co-teacher.md) |
| **Planner** | Time, calendar, pacing | [planner.md](planner.md) |
| **Communicator** | External communication, contact, follow-up | [communicator.md](communicator.md) |
| **Assessor** | Evidence, grading, reporting, intervention flags | [assessor.md](assessor.md) |
| **Curriculum Designer** | Content, research, materials, rubrics | [curriculum_designer.md](curriculum_designer.md) |
| **Teacher (Eric)** | Supervision, judgment, approval, student safety | — |

Max 4 agent roles. The co-teacher maintains the system; the teacher supervises; agents execute and hand off.

---

## Handoff map

```
Curriculum Designer
    │  scope/sequence, unit plans ──────────────► Planner
    │  assessments + rubrics ───────────────────► Assessor
    │  lesson plans + materials ────────────────► Teacher
    ▲
    │  mastery data / performance patterns
    │
Assessor
    │  at-risk flags, intervention status ──────► Communicator
    │  grading deadlines ────────────────────────► Planner
    │  compliance reports ───────────────────────► Teacher / Admin
    ▲
    │  assessment windows / schedule changes
    │
Planner
    │  event dates needing comms ───────────────► Communicator
    │  confirmed time blocks ────────────────────► Curriculum Designer
    │  pacing status ────────────────────────────► Teacher
    ▲
    │  scheduled comms confirmed
    │
Communicator
    │  drafted communications ───────────────────► Teacher (approval)
    │  contact logs ─────────────────────────────► Assessor (closes loop)
    │  escalations ──────────────────────────────► Teacher (judgment)
```

---

## File-based handoff mechanism

All role-to-role communication uses a **directory executor** pattern. This ensures durable, traceable, atomic handoffs with no ambiguity about task status or deliverables.

### Directory structure

```
handoffs/              # Tasks handed off between roles
  task-<TASK_ID>.json

results/               # Completion records from executor
  result-<TASK_ID>.json

deliverables/          # Produced outputs (readable by downstream roles)
  *.md, *.json, *.csv, etc.

tmp/                   # Atomic write staging (executor use only)
  task-<TASK_ID>.json.tmp
```

### Task lifecycle

1. **Queued** — Task JSON written to `handoffs/task-<TASK_ID>.json` with `status: "queued"`
2. **Running** — Executor atomically updates status to `"running"` with timestamp
3. **Done** — Executor writes result to `results/result-<TASK_ID>.json` with `status: "done"` and deliverable paths
4. **Failed** — If validation or execution fails, result shows `status: "failed"` with error reason

### Task JSON schema

Each task JSON follows this required structure:

```json
{
  "task_id": "string (unique identifier, e.g., 'PLAN-001')",
  "goal": "string (clear, actionable objective)",
  "plan": "object or string (optional; captures strategy or steps)",
  "constraints": "object (optional; captures boundaries, deadlines, requirements)",
  "deliverables": ["array of filenames expected in deliverables/"],
  "timeout_seconds": "integer (optional; default 600)",
  "version": "integer (optional; for tracking schema changes)",
  "created_at": "string (ISO 8601 timestamp when task was created)",
  "status": "queued | running | done | failed"
}
```

### Result JSON schema

```json
{
  "task_id": "string (matches task_id)",
  "status": "done | failed",
  "summary": "string (what was done or what went wrong)",
  "deliverables": {
    "filename": "path/in/deliverables/"
  },
  "completed_at": "string (ISO 8601 timestamp)",
  "version": "integer",
  "error": "string (present if status is 'failed')"
}
```

### Role execution pattern

When a role executes a task:

1. **Read the task** from `handoffs/task-<TASK_ID>.json`
2. **Validate inputs** — Ensure all required fields exist and are well-formed
3. **Execute the goal** — Follow the plan, respect the constraints, produce the deliverables
4. **Write results** — Write `result-<TASK_ID>.json` to `results/`; write all deliverables to `deliverables/`
5. **Status is determinate** — Downstream roles can check `results/result-<TASK_ID>.json` to confirm completion

### Manual execution workflow

During the experimental phase, all task execution is manual — no continuous polling or scheduled triggers. The workflow is:

1. **Upstream role** (e.g., Planner) finishes its work
2. **Upstream role writes** a task JSON to `handoffs/` describing what the downstream role (e.g., Assessor) should do
3. **Human or admin** manually runs the executor: `python executor.py --no-watch`
4. **Executor processes** all queued tasks, writes results and deliverables
5. **Downstream role** reads result JSONs and deliverables from `results/` and `deliverables/`
6. **Downstream role executes** its own task (with those inputs)
7. **Downstream role writes** its own task JSON to `handoffs/` for the next role in the chain
8. **Repeat** until all roles have processed their tasks for the cycle

This pattern is fully deterministic, debuggable, and easy to extend to continuous or triggered execution later.

---

## Governing rules

1. **Every output traces to an input.** No artifact without a named source.
2. **Every role has one owner.** No shared ownership of a function across roles.
3. **Teacher approves; agents draft.** No external communication, grade, or material is issued without teacher sign-off.
4. **Experimental phase safety.** All external actions (sends, submissions, grade reports) are mocked until the teacher explicitly unlocks live deployment.
5. **Escalation path is explicit.** When a role cannot resolve an issue, it escalates to the teacher with full context — not to another agent.
6. **Done criteria are checkable.** Each role's done criteria are binary pass/fail, not subjective.
7. **Minimum viable team.** New roles are not created unless an existing role cannot absorb the function without degrading quality of its primary loop.
8. **Handoffs are durable.** All task handoffs use the file-based executor pattern. No ad-hoc file passing or email-based coordination.
9. **Tasks are atomic.** A task either completes fully or fails visibly; partial states are not permitted.
10. **Results are traceable.** Every result JSON includes task_id, status, summary, and error (if applicable) so the full audit trail is preserved.

---

## Classroom context

- **School:** Columbia Secondary School, Manhattan, NYC DOE
- **Population:** Bimodal — gen ed is screened, special ed is unscreened. All sections include students with varied support needs.
- **Teacher:** Eric (5 months to start of year; 5 years since last classroom)
- **Sections (5 total, ~133 students):**

| Section ID | Course | Period | ICT | Notes |
|---|---|---|---|---|
| ALG-01 | Algebra I | 1 | No | No co-teacher |
| ALG-02 | Algebra I | 2 | Yes | Co-teacher TBD |
| ALG-03 | Algebra I | 4 | No | No co-teacher |
| AP-STAT | AP Statistics | 6 | No | College Board SSD process applies |
| AP-CSA | AP Computer Science A | 8 | No | Java; lab room TBD |

- **Standards frameworks:** CCSS-M (Algebra), College Board CED (AP Statistics, AP CS A)
- **Deployment target:** 2026–27 school year
- **Current phase:** Experimental — dummy/synthetic data, mocked actions, end-to-end workflow validation
- **Data layer:** `data/` directory — see `data/README.md` for structure, access rules, and privacy policy

---

## Merge rationale: Researcher + Curriculum → Curriculum Designer

The original five candidate areas included separate Researcher and Curriculum roles. These were merged because:

- In a single-teacher math classroom, curriculum development is never decoupled from research; materials that are not research-grounded are out of spec by definition.
- A handoff between Researcher and Curriculum would require a human to reconcile outputs, increasing coordination burden rather than reducing it.
- A single Curriculum Designer who owns both the knowledge retrieval and the material production closes that loop internally and delivers finished artifacts to the rest of the team.
