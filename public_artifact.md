# Classroom-Manager: Working Demo Case Study

## What this is

`classroom-manager` is a role-based multi-agent prototype for classroom operations.  
It treats teaching as team-shaped work and tests whether agent handoffs can reduce
teacher glue work across planning, curriculum, assessment, and communication.

This document is the public artifact for the project in its current state. It is
intentionally scoped as a case study, not a product claim.

## Problem and design target

A real secondary teacher is accountable for planning, instruction, assessment,
communication, reporting, and compliance at the same time. Most tools solve one
slice and push integration labor back onto the teacher.

This system tests a different approach:

- Use explicit role ownership instead of one general assistant.
- Use file-based handoffs so each output traces to an input.
- Keep the teacher as approver for sensitive actions.

Two canonical requests define the target behavior:

1. "I need plans and materials for week X."
2. "I need a report on at-risk students for admin."

## System architecture

Top-level roles are bounded and documented:

- `Planner`: calendar, pacing, and time-block coordination.
- `Curriculum Designer`: standards-aligned scope, lessons, and assessments.
- `Assessor`: mastery evidence, flags, and reporting.
- `Communicator`: external communication drafts and logs.
- `Co-Teacher (Ines)`: system architecture, role design, and coherence.

Execution model:

- Tasks are written as JSON in `handoffs/`.
- Executor processes queued tasks and writes outcomes to `results/`.
- Artifacts are saved in `deliverables/`.
- Status lifecycle: `queued -> running -> done` (or `failed`).

Routing and context:

- Role-specific specs are injected into prompts from `docs/roles/*.md`.
- Model routing is role-based for cost/quality balance.
- Current production-safety assumption is experimental mode only.

## Evidence of progress

Confirmed working in repository state dated 2026-03-26:

- End-to-end execution via `make execute` and `make execute-watch`.
- Role-spec prompt injection from canonical docs.
- Atomic task/result file lifecycle with stable naming conventions.
- Completed deliverables for:
  - Full-year Algebra I scope generation
  - Full-year calendar generation
  - Week 6 lesson-plan run

What this proves:

- Multi-agent orchestration with explicit ownership is operational.
- Durable handoffs can be implemented with simple filesystem primitives.
- Classroom-domain constraints can be encoded in role specs and schemas.

## Honest limitations

This is a working demo, not a classroom-ready system.

- Output quality is not yet teacher-trust reliable.
- Assessor and Communicator live loops remain under-tested.
- Failure recovery and multi-task queue behavior need more validation.
- Real-school brittleness (schedule disruptions, transfers, compliance edge cases)
  is not solved by current testing depth.
- The reliability gap from prototype to real weekly use is large.

Hard constraint:

Running frontier models for exploratory development via API is structurally
expensive. Cost controls are required for sustainable iteration.

## Why this artifact matters

As a portfolio signal, this project demonstrates:

- systems architecture and role decomposition
- LLM integration and model routing decisions
- prompt/spec design with durable repository memory
- handoff schema design and operational traceability
- domain fluency in real K-12 classroom operations

The strongest claim is not "product complete."  
The strongest claim is "can design and build coherent, constrained agent systems
for a real domain with hard operational requirements."

## Freeze decision and maintenance posture

Current recommended posture:

- Freeze at working-demo stage.
- Use this case study as the public-facing artifact.
- Avoid scope expansion until funding/time context changes.

Maintenance-only mode:

- Keep canonical docs (`README.md`, `docs/co-teacher.md`, `docs/roles/`) coherent.
- Accept only fixes that improve clarity, traceability, or testability.
- Defer major feature work and new role creation.

## Resume criteria

Resume active product development only when all are true:

1. Sustainable cost model for iterative development exists.
2. Weekly teacher-review loop is available for output quality tuning.
3. Assessor + Communicator workflows are validated end-to-end.
4. Failure handling and multi-task queue behavior pass defined tests.
5. A clear deployment path (or institutional partner) is in scope.

Until then, this project is a strong, honest demonstration artifact.
