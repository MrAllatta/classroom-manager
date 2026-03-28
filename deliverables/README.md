# Deliverables

Exports, snapshots, and human-readable artifacts produced when tasks run. **This directory is not the canonical store.**

## Source of truth: `data/`

Structured, durable classroom metadata lives under **`data/`** (see [`data/README.md`](../data/README.md)):

- School context and academic calendar: `data/school/`
- Course scope and sequence: `data/courses/<course_id>/scope.yaml`
- Sections, students (when used), schemas: `data/sections/`, `data/students/`, `data/schema/`

When a deliverable and `data/` disagree, **trust `data/`** unless you are intentionally reviewing an old export.

## Staleness is expected

Updating canonical YAML or JSON under `data/` **does not require** refreshing every file in `deliverables/`. Snapshots here can legitimately lag until someone:

- Regenerates an export for teacher review, or
- Closes a task whose acceptance criteria name specific `deliverables/` paths

Do **not** treat “keep the repo consistent” as “touch every historical artifact on every change.” Prefer surgical updates to `data/` and regenerate downstream exports only when the workflow calls for it.

Regenerated exports meant for teacher review should still meet the **teacher-next** bar ([`docs/architecture_and_workflows.md`](../docs/architecture_and_workflows.md#teacher-next-bar)): the reader should know **what to do next**, not only what changed.

**Automated assistants (Cursor / agents):** When the user asks only to update canonical course or school data, **skip `deliverables/`** unless they explicitly name files here or ask for a regenerated export. Persistent guidance: [`.cursor/rules/canonical-data-vs-deliverables.mdc`](../.cursor/rules/canonical-data-vs-deliverables.mdc).

## Relationship to other folders

| Location | Role |
|----------|------|
| `data/` | Canonical structured inputs the system is built around |
| `deliverables/` | Optional mirrors, markdown/JSON exports, samples — may be outdated |
| `handoffs/` | Task specs and queue state for agent runs — historical record |
| `results/` | Completion summaries for tasks — historical record |

## Layout

As this folder grows, prefer light structure (subfolders by course, artifact type, or date) rather than one flat list of everything.
