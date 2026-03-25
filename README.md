# classroom-manager

## Purpose
Build a sustainable, role-based system for running a real K-12 classroom.
This project treats the work of a professional teacher as team work, not as a task list that can reasonably be absorbed by one under-resourced human.

A teacher is accountable for student safety and supervision, attendance, planning, instruction, assessment, communication, reporting, documentation, counseling, case-management, collaboration, and intellectual rigor. In practice, that is already a team-shaped job.
## Core philosophy
- The classroom is always trying to accomplish everything at once.
- A system that only solves one slice of the work can make the whole system worse if the human teacher has to glue the helpers together.
- This project is building that glue: shared context, durable handoffs, explicit ownership, and outputs that connect across planning, implementation, assessment, communication, scheduling, and reporting.
- Success means the teacher supervises a coherent system instead of manually reconciling disconnected tools or partial helpers.

## Classroom context
## Classroom context
- Setting: NYC mathematics / high school classroom
- Students: 133
- Experimental phase: build dummy context and practice end-to-end role workflows.
  - Generate practice data
  - Stress-test constructs, teardown, and failure modes
  - Mock external actions (admin/compliance actions and communications) before live data
- Deployment target: 2026–27

## Design principles
1. **Minimum viable team first.** Expand only when needed.
2.Target **3-5 top-level roles** plus the human teacherupervision simple.
3. **Tool-aligned role exespawn or manage **helper roles** tied to specific tools, APIs, templates, or recurring workflows.
- The team should reduce the teacher's coordination burden, not increase it.entation and testing).
## Candidate role areas (draft)
These are draft role areas, not yet final boundaries:

- **Scheduler**  
  Owns calendar-based coordination, creates events, and connects people, time, and required follow-up.
- **Messager**  
  Owns communication loops across email, comments, texts, call scripts, and school systems, especially where action depends on timely follow-up.
- **Assessor**  
  Owns standards-aligned evidence, evaluation, reporting, and flags about student learning.
- **Researcher**  
  Brings in new knowledge and checks alignment to rigorous professional standards and effective practice.
- **Curriculum**  
  Writes and adapts scope and sequence, lessons, and materials in collaboration with established curricula and research.

These may be collapsed, refined, or reorganized as the implementation becomes more concrete.

## Experimental-phase expectations ownership:** Avoid fragmentation by ensuring at least one role owns the instructional/assessment intent loop.
5. **Helper/subroles are allowed:** Top-level roles may generate/manage smaller helper roles specialized to specific tools.
6. **Every role must define**:
   - Purpose
   - Responsibilities
   - Inputs
   - Outputs
   - Handoffs
   - Done criteria
7. **Experimental safety:** During experimental phase, all data and acrubrics, standards, or operating rules.
- Reject partial helpers that create extra reconciliation work for the human teacher.cked.
8. **Tight feedback loops:** assessment → corrective action.

## Classroom workflow (high-level loop)
1. Plan: choose objectives/content and align to standards
2. Prepare: assemble materials and assessments
3. Implement: run instruction and collect interaction/assessment data
4. Assess: align results to objectives/standards; generate actionable outputs
5. Correct/Nudge: drive targeted interventions and next steps
6. Document & Track: store artifacts and decisions for continuity
7. Communicate & Admin: produce/administer required outputs and communications (dummy/mocked in experiments)

## Team structure (initial)
- **Max 4 top-level roles** (supervisable, end-to-end accountable).
- Each top-level role can spawn/manage **helper roles** tied to specific tools/APIs/templates as needed.

## Experimental-phase expectations
- Use dummy context and practice end-to-end workflows.
- Validate role handoffs and failure modes before live deployment.
- Ensure auditability: outputs trace back to inputs and the governing rubrics/standards.