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
- **School:** Columbia Secondary School, Manhattan, NYC DOE
- **Population:** Bimodal — gen ed is screened, special ed is unscreened. All sections include students with varied support needs regardless of formal plan status.
- **Sections:** 3 × Algebra I, 1 × AP Statistics, 1 × AP Computer Science A (~133 students total)
- **Special education framework:** NYC DOE / SESIS; IEP and 504 plans; ICT model in one Algebra section
- **Deployment target:** 2026–27 school year
- **Current phase:** Experimental — synthetic data, mocked actions, end-to-end workflow validation

## Data architecture
Structured metadata lives in `data/` — see [`data/README.md`](data/README.md) for the full description.

| Layer | Location | Contents | Sensitivity |
|---|---|---|---|
| School context | `data/school/` | Environmental constants | Low |
| Sections | `data/sections/` | Per-section metadata, staffing, ICT | Low-medium |
| Students | `data/students/` | Individual student records | **FERPA-protected** |
| Schema | `data/schema/` | Field definitions, accommodation codes | Low |

Student data must never pass through an LLM context window in production. Tools query locally; only computed results are surfaced. In the experimental phase, all student data is synthetic.

## Design principles
1. **Minimum viable team first.** Expand only when needed.
2. Target **3–5 top-level roles** plus the human teacher to keep supervision simple.
3. **Tool-aligned role execution.** Top-level roles may spawn or manage helper roles tied to specific tools, APIs, templates, or recurring workflows.
4. **The team reduces coordination burden.** If a proposed change increases glue work for the teacher, push back.
5. **Concrete over abstract.** Every output should be usable immediately.

## Team structure
- **Max 4 top-level agent roles** (supervisable, end-to-end accountable)
- Each top-level role can spawn/manage helper roles tied to specific tools/APIs/templates as needed
- See [`docs/roles/README.md`](docs/roles/README.md) for the full team structure and handoff map

## Co-teacher: Inés Vidal
The co-teacher is the meta-role that builds and maintains the team itself. She is not one of the four agent roles — she is the persistent thought partner to the human teacher, responsible for protecting whole-classroom coherence so the human is never forced to glue partial helpers together. Her full definition lives in [`docs/co-teacher.md`](docs/co-teacher.md).

## Classroom workflow (high-level loop)
1. **Plan:** Choose objectives/content and align to standards
2. **Prepare:** Assemble materials and assessments
3. **Implement:** Run instruction and collect interaction/assessment data
4. **Assess:** Align results to objectives/standards; generate actionable outputs
5. **Correct/Nudge:** Drive targeted interventions and next steps
6. **Document & Track:** Store artifacts and decisions for continuity
7. **Communicate & Admin:** Produce/administer required outputs and communications (mocked in experimental phase)

## Experimental-phase expectations
- Use synthetic context and practice end-to-end workflows
- Validate role handoffs and failure modes before live deployment
- Ensure auditability: outputs trace back to inputs and governing rubrics/standards
- All external actions (communications, grade submissions, compliance reports) are mocked until explicitly unlocked