# Agent Architecture

## The problem this document solves

Agent instructions have two distinct kinds of content that must not be conflated:

1. **Platform-specific configuration** — tool permissions, agent metadata, binding syntax. This is specific to the agentic container (Positron, Claude Code, Cursor, a custom harness, etc.) and will need to be rewritten when the platform changes.
2. **Portable behavioral spec** — identity, purpose, operating principles, responsibilities, inputs, outputs, handoffs, done criteria. This is stable across platforms and should never be duplicated in a platform-specific file.

Conflating them creates two problems:
- **Duplication.** The spec gets copied into the platform file and drifts.
- **Coupling.** Changing platforms forces rewriting spec content unnecessarily.

---

## Architecture

```
docs/                          ← portable, platform-independent
  co-teacher.md                  Co-teacher (Inés) full spec
  agent-architecture.md          This document
  roles/
    README.md                    Team structure, handoff map, governing rules
    planner.md                   Planner full spec
    communicator.md              Communicator full spec
    assessor.md                  Assessor full spec
    curriculum_designer.md       Curriculum Designer full spec

.vscode/positron/agents/       ← Positron-specific bindings only
  co-teacher.agent.md            Tool permissions + pointer to docs/co-teacher.md
  planner.agent.md               Tool permissions + pointer to docs/roles/planner.md
  communicator.agent.md          Tool permissions + pointer to docs/roles/communicator.md
  assessor.agent.md              Tool permissions + pointer to docs/roles/assessor.md
  curriculum-designer.agent.md   Tool permissions + pointer to docs/roles/curriculum_designer.md
```

### Rule: agent files are thin bindings

A Positron agent file contains:
1. **Frontmatter** — `description` and `tools` list (Positron-specific)
2. **One paragraph of role identification**
3. **A pointer** to the canonical spec document in `docs/`
4. **A tool scope rationale table** — which tools, and why

Nothing else. If you are tempted to add behavioral instructions to an agent file, put them in the spec instead.

### Rule: spec files are the source of truth

`docs/co-teacher.md` and `docs/roles/*.md` govern agent behavior. They are:
- Read at the start of every session
- Updated when the model changes (new operating guidance, role refinement, handoff changes)
- Never duplicated

---

## Tool scoping

Tools are granted at the minimum needed to perform the role's documented functions.

| Role | Tools | Rationale |
|---|---|---|
| **Co-teacher** | All tools | Builds and repairs the team; needs full access |
| **Planner** | `read`, `search`, `execute`, `projectTree`, `todo` | File-based scheduling workflow; no code execution or external services |
| **Communicator** | `read`, `search`, `execute`, `todo` | Drafting and logging; no code execution, no project tree navigation |
| **Assessor** | `read`, `search`, `execute`, `executeCode`, `inspectVariables`, `getTableSummary`, `getPlot`, `projectTree`, `todo`, Python/R package tools | Needs data analysis for grade computation and mastery tracking |
| **Curriculum Designer** | `read`, `search`, `execute`, `projectTree`, `todo`, `vscode` | Content authoring; file-based workflow with editor navigation |

**To add a tool to a role:** document the use case in the role's spec file first, then update the agent binding. Do not add tools speculatively.

---

## Porting to a new platform

When moving this system to a different agentic container (Claude Code, Cursor, a custom API harness, etc.):

1. **Copy `docs/` unchanged.** The specs are portable.
2. **Create new platform-specific binding files** in whatever format that platform requires.
3. **For each role binding:**
   - Set the equivalent of `description` to match the role's purpose line from its spec
   - Grant the equivalent of the tools in the table above
   - Include the same pointer-to-spec in the body
4. **Do not modify `docs/` to accommodate platform syntax.**

If a platform cannot reference a file by path, paste the spec content into the binding — but note in the spec that it has been duplicated and which platform file is the copy. Treat the `docs/` version as primary.

---

## Updating this system

When Eric provides new operating guidance or philosophy:

1. Update the relevant spec file in `docs/` first.
2. If the change affects tool needs, update the agent binding and this document's tool table.
3. If a new role is needed, define it in `docs/roles/` before creating the agent binding.
4. The co-teacher (Inés) is responsible for keeping this document current.

Last updated: 2026-03-25
