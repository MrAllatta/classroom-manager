# Architecture & Workflows (Canonical)

This document is the **single canonical explanation** of how the system fits together and how work moves through it in the current experimental phase.

If you only read one internal architecture document, read this one.

The **roadmap for testing** interactions under simulated real-world conditions (which canonical request next, what “pass” means) lives in `docs/testing_plan.md` and should stay in sync with this narrative.

---

## System overview

`classroom-manager` is a role-based multi-agent prototype for classroom operations. It treats teaching as team-shaped work and tests whether explicit role ownership + durable handoffs can reduce teacher glue work.

At runtime, the system is deliberately simple:

```
Roles (agents) → file-based task handoffs → executor → results + deliverables
```

---

## Core components

### Roles (agents)

Top-level roles are bounded and documented in `docs/roles/`:

- Planner — calendar, pacing, time blocks
- Curriculum Designer — scope, lessons, assessments
- Assessor — evidence loop, mastery, flags, reports
- Communicator — drafts, logs, escalations
- Co-teacher (Inés) — system coherence and maintenance (not one of the four roles)

### File-based handoffs

Roles do not “message” each other. They write tasks as JSON files into `handoffs/`. The executor reads queued tasks and writes results and artifacts to disk. Downstream roles then read those outputs and generate the next tasks.

### Executor

`executor.py` is the orchestration engine. It:

1. Reads `handoffs/task-*.json`
2. Validates schema
3. Atomically updates task status (`queued → running → done|failed`)
4. Produces the promised deliverables in `deliverables/`
5. Writes `results/result-<TASK_ID>.json`

---

## Directory model (public mental model)

```
handoffs/               # INPUT: queued task JSONs
  task-<TASK_ID>.json

results/                # OUTPUT: durable completion records (done/failed)
  result-<TASK_ID>.json

deliverables/           # OUTPUT: generated artifacts consumed downstream
  *.md
  *.json
  *.txt

tmp/                    # executor-only staging for atomic writes
  *.tmp
```

Operational note: `data/` is the structured metadata layer (school/sections/students/schema). In production, `data/students/` is FERPA-protected and must never be passed into an LLM context window.

---

## Task lifecycle (state machine)

```
Task JSON written (status: queued)
  ↓ (executor processes)
status: running  + tmp/ staging + atomic rename
  ↓
status: done    + result JSON written + deliverables verified
  OR
status: failed  + result JSON written with error
```

Completed tasks are skipped on subsequent executor runs (idempotence).

---

## Task and result contracts (shape, not exhaustive)

### Task JSON (written by roles to `handoffs/`)

Minimum required fields:

```json
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "goal": "Human-readable objective",
  "deliverables": ["some_file.md", "some_file.json"],
  "status": "queued"
}
```

Common optional fields (used heavily in this repo):

- `plan`: structured “how” and input references
- `constraints`: boundaries and invariants
- `timeout_seconds`: execution timeout (defaults exist)
- `version`, `created_at`: durability and traceability

### Result JSON (written by executor to `results/`)

```json
{
  "task_id": "CURRDES-SCOPE-UNIT-01",
  "status": "done",
  "summary": "What happened (or what went wrong).",
  "deliverables": {
    "scope_UNIT-01.md": "deliverables/scope_UNIT-01.md"
  },
  "completed_at": "2026-03-25T10:15:00Z",
  "version": 1
}
```

If failed, `error` is present and `deliverables` may be empty.

For the authoritative catalogue of task types and chains, see `docs/task_schemas_reference.md`.

---

## Manual execution workflow (experimental phase)

### Step 1 — Upstream role queues a task

Write a task JSON into `handoffs/` using the naming convention:

```
<ROLE>-<FUNCTION>-<QUALIFIER>
```

Examples:

- `PLAN-CALENDAR-ALG1-FULLYEAR`
- `CURRDES-SCOPE-ALG1-FULLYEAR`
- `PLAN-WEEK6-ALG01`

### Step 2 — Run executor

Run once (process current queue, then exit):

```bash
make execute
```

Or watch (poll forever):

```bash
make execute-watch
```

### Step 3 — Downstream role consumes outputs

Downstream roles:

1. Confirm completion by reading `results/result-<TASK_ID>.json`
2. Consume referenced artifacts in `deliverables/`
3. Queue the next task(s) into `handoffs/`

---

## Example handoff chains (high-signal only)

### Chain A — Build a unit (content → schedule → assessment → tracking)

```
CURRDES-SCOPE-...
  → scope_*.md + objectives_*.json

PLAN-CONFIRM-...
  → time_blocks_*.json

CURRDES-ASSESS-...
  → assessments_*.md + rubrics_*.json

ASSESS-INIT-...
  → mastery_tracker_*.json

CURRDES-LESSONS-...
  → lessons_*.md
```

### Chain B — Assessment loop (evidence → comms)

```
ASSESS-SCORE-...
  → score_report_*.md + mastery_tracker_*_updated.json

ASSESS-FLAGS-...
  → flags_*.json

COMMS-INTERVENTION-<student>
  → draft_intervention_<student>.md
```

---

## Determinism, idempotence, and retries

This system is designed to be:

- **Durable**: all state is in files
- **Atomic**: executor writes via `tmp/` staging + rename
- **Traceable**: `task_id` + result records are durable
- **Idempotent**: completed tasks are skipped on future runs

If you need to re-run a task intentionally, you must remove/replace the existing result record (or use a new `task_id` / bumped version) so the executor doesn’t treat it as already done.

---

## Failure behavior (what “failed” means)

Common failure modes are deliberately visible:

- invalid JSON
- missing required fields
- timeout (task stuck “running” beyond `timeout_seconds`)
- promised deliverable missing after execution

The executor writes a failed result with a diagnostic error string so the next step is always “inspect the result JSON”.

---

## Context injection (why some tasks need more than the goal)

A critical quality failure mode is “the model generates plausible content from the goal alone” while ignoring the actual curriculum scope/calendar.

This repository addresses that by injecting minimal stable context into prompts (school context; scoped curriculum context) before role specs + task details.

For the design and implementation notes, see `docs/context_injection_architecture.md`.

---

## Where to go next

- **Simulated real-world testing (order of operations, pass criteria):** `docs/testing_plan.md`
- Task types and chains: `docs/task_schemas_reference.md`
- Role specs (the behavioral source of truth): `docs/roles/`
- Running the system: `executor_quickstart.md`
- Portable vs platform bindings: `docs/agent-architecture.md`

