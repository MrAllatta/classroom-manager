# Classroom Team — Role Overview

## Team structure

| Role | Primary loop owned | File |
|---|---|---|
| **Planner** | Time, calendar, pacing | [planner.md](planner.md) |
| **Communicator** | External communication, contact, follow-up | [communicator.md](communicator.md) |
| **Assessor** | Evidence, grading, reporting, intervention flags | [assessor.md](assessor.md) |
| **Curriculum Designer** | Content, research, materials, rubrics | [curriculum_designer.md](curriculum_designer.md) |
| **Teacher (human)** | Supervision, judgment, approval, student safety | — |

Max 4 agent roles. The teacher supervises; agents execute and hand off.

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

## Governing rules

1. **Every output traces to an input.** No artifact without a named source.
2. **Every role has one owner.** No shared ownership of a function across roles.
3. **Teacher approves; agents draft.** No external communication, grade, or material is issued without teacher sign-off.
4. **Experimental phase safety.** All external actions (sends, submissions, grade reports) are mocked until the teacher explicitly unlocks live deployment.
5. **Escalation path is explicit.** When a role cannot resolve an issue, it escalates to the teacher with full context — not to another agent.
6. **Done criteria are checkable.** Each role's done criteria are binary pass/fail, not subjective.
7. **Minimum viable team.** New roles are not created unless an existing role cannot absorb the function without degrading quality of its primary loop.

---

## Classroom context

- Setting: NYC high school mathematics
- Students: 133
- Deployment target: 2026–27 school year
- Current phase: experimental — dummy data, mocked actions, end-to-end workflow validation

---

## Merge rationale: Researcher + Curriculum → Curriculum Designer

The original five candidate areas included separate Researcher and Curriculum roles. These were merged because:

- In a single-teacher math classroom, curriculum development is never decoupled from research; materials that are not research-grounded are out of spec by definition.
- A handoff between Researcher and Curriculum would require a human to reconcile outputs, increasing coordination burden rather than reducing it.
- A single Curriculum Designer who owns both the knowledge retrieval and the material production closes that loop internally and delivers finished artifacts to the rest of the team.
