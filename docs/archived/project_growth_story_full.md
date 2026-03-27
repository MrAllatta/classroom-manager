# Project Growth Story (From Git History)

This artifact is a narrative reconstruction of the project trajectory using `git log`
as the primary source.

## Phase 1: Identity and intent (2026-03-25, early)

The project starts with a basic repository and quickly focuses on purpose:

- Initial commit and first README baseline
- Multiple README rewrites to sharpen philosophy and voice
- Explicit naming and identity choice for the co-teacher role (Ines Vidal)

What changed in this phase:

- The project moved from "new repo" to "mission-driven system"
- Voice and educational philosophy became first-class design constraints

## Phase 2: Role architecture takes shape

After mission clarity, the system was decomposed into explicit ownership:

- Role specs added for Planner, Communicator, Assessor, Curriculum Designer
- Team-level role map added in `docs/roles/README.md`
- Co-teacher moved to canonical docs spec; platform agent files became thin wrappers
- Architecture formalized in `docs/agent-architecture.md`

What changed in this phase:

- Single-assistant idea became a bounded multi-role system
- Spec/source-of-truth discipline appeared (portable specs vs platform bindings)

## Phase 3: Data and schema foundation

The repo then added structure to support realistic classroom workflows:

- Accommodation, student-profile, and school-context schema/data files
- Section placeholders and synthetic student data
- README/data docs expanded for context and constraints

What changed in this phase:

- The project became data-model aware, not prompt-only
- Experimental safety posture emerged: synthetic context first

## Phase 4: Execution engine and workflow contracts

With roles and data in place, the implementation shifted to orchestration:

- Lightweight executor introduced
- Quickstart, workflow, architecture, and task schema references added
- Handoff conventions documented (`handoffs/`, task/result lifecycle)
- Task JSON formats embedded in role docs for executable handoffs

What changed in this phase:

- The system became runnable, not just documented
- Role handoffs became machine-processable contracts

## Phase 5: Live LLM integration and operational controls

The next step connected the executor to real model calls:

- Anthropic API execution path added and updated
- Environment secret hygiene added (`.env` ignored)
- Makefile targets added for repeatable runs
- Role spec injection into prompts added

What changed in this phase:

- Static orchestrator became active agent runtime
- Cost/quality control began through role-based routing and prompt injection

## Phase 6: Consolidation and realism checks (2026-03-26)

The most recent history shows pruning and tighter operating discipline:

- Redundant files removed
- Documentation archived and index updated
- Co-teacher instructions updated for testing-phase realities
- Delegation protocol made explicit (route to owning role first)
- Minimal context injection for planning tasks
- Test payloads and responses added for verification
- Model API names and Make targets updated

What changed in this phase:

- The project shifted from expansion to consolidation
- Architecture maturity increased by reducing documentation sprawl

## Milestone summary

From the commit trail, the project matured along this sequence:

1. **Philosophy**
2. **Roles**
3. **Data model**
4. **Handoff contracts**
5. **Executor runtime**
6. **LLM integration**
7. **Consolidation + testing posture**

That progression is consistent with a serious prototype path: define system intent,
bound responsibilities, make workflows executable, then pressure-test under realistic
constraints.

## Hard truths visible in the history

- Documentation grew fast before implementation stabilized.
- The architecture became stronger once spec canonicalization and pruning started.
- The project is credible as a systems prototype, but commit history alone also shows
  it is still in experimental validation rather than deployment readiness.

## Why this story artifact exists

This file is meant to answer a hiring-manager or collaborator question quickly:
"How did this project grow, and what does that growth prove?"

Answer:
It proves sustained systems thinking, disciplined decomposition, and operational
follow-through from concept to working orchestrated prototype.
