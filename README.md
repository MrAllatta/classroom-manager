# classroom-manager

## Purpose
Build a sustainable, role-based system for running a NYC mathematics high school classroom.
The goal is to reduce single-human overload by distributing recurring work into clear roles with explicit
inputs, outputs, handoffs, and “done” criteria.

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
2. **Top-level role cap:** At most **4 top-level roles** to keep supervision simple.
3. **Tool-aligned role execution:** Roles should generally map to the tools they use (to simplify implementation and testing).
4. **Intent coverage via top-level ownership:** Avoid fragmentation by ensuring at least one role owns the instructional/assessment intent loop.
5. **Helper/subroles are allowed:** Top-level roles may generate/manage smaller helper roles specialized to specific tools.
6. **Every role must define**:
   - Purpose
   - Responsibilities
   - Inputs
   - Outputs
   - Handoffs
   - Done criteria
7. **Experimental safety:** During experimental phase, all data and actions are dummy/mocked.
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