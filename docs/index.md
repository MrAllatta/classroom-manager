# Documentation Index

Complete guide to all documentation for the classroom management system with file-based executor pattern.

---

## Quick Navigation

### Just Getting Started?
1. **[EXECUTOR_QUICKSTART.md](../EXECUTOR_QUICKSTART.md)** — Start here! How to use the system (15 min)
2. **[System Architecture](SYSTEM_ARCHITECTURE.md)** — Visual overview of how everything fits together (20 min)
3. **[Roles README](roles/README.md)** — Overview of the 4 agent roles (10 min)

### Understanding the System?
- **[Handoff Workflow](HANDOFF_WORKFLOW.md)** — Complete explanation of task-based coordination
- **[Task Schemas Reference](TASK_SCHEMAS_REFERENCE.md)** — Quick lookup for all task types
- **[Updates Summary](UPDATES_SUMMARY.md)** — What changed and why

### Implementing a Role?
1. Read **[Roles README](roles/README.md)** for the big picture
2. Read your role's specification:
   - **[Curriculum Designer](roles/curriculum_designer.md)**
   - **[Planner](roles/planner.md)**
   - **[Assessor](roles/assessor.md)**
   - **[Communicator](roles/communicator.md)**
3. Focus on the "Handoff Format" section of your role
4. Consult **[Task Schemas Reference](TASK_SCHEMAS_REFERENCE.md)** for task chains

### Setting Up the System?
- **[Executor Quickstart](../EXECUTOR_QUICKSTART.md)** — Installation and first run
- **[Implementation Checklist](IMPLEMENTATION_CHECKLIST.md)** — Track progress
- **[System Architecture](SYSTEM_ARCHITECTURE.md)** — Directory structure and setup

### Troubleshooting?
- **[Executor Quickstart - Troubleshooting](../EXECUTOR_QUICKSTART.md#troubleshooting)** — Common issues and solutions
- **[Handoff Workflow - Error Handling](HANDOFF_WORKFLOW.md#error-handling)** — Error scenarios and recovery

---

## All Documentation Files

### Top-Level Documents

| File | Purpose | Audience |
|---|---|---|
| **[EXECUTOR_QUICKSTART.md](../EXECUTOR_QUICKSTART.md)** | How to use the executor; getting started guide | Everyone |
| **[README.md](../README.md)** | Project overview | Everyone |

### Documentation Directory (`docs/`)

#### Reference Documents

| File | Purpose | Length | Audience |
|---|---|---|---|
| **[roles/README.md](roles/README.md)** | Team overview, role definitions, governing rules, handoff map | 5 min | Everyone |
| **[HANDOFF_WORKFLOW.md](HANDOFF_WORKFLOW.md)** | Complete executor pattern explanation with examples | 20 min | Implementers, admins |
| **[TASK_SCHEMAS_REFERENCE.md](TASK_SCHEMAS_REFERENCE.md)** | Quick reference for all task types and schemas | 10 min | Task creators |
| **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** | Visual architecture, data flow, component diagrams | 15 min | Architects, developers |
| **[UPDATES_SUMMARY.md](UPDATES_SUMMARY.md)** | Summary of all documentation updates | 10 min | Leadership, reviewers |
| **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** | Progress tracking for all phases | 5 min | Project managers |

#### Role Specifications

| File | Purpose | Handoff Format? | Audience |
|---|---|---|---|
| **[roles/curriculum_designer.md](roles/curriculum_designer.md)** | Curriculum Designer role definition and responsibilities | ✅ Yes | CD implementation, other roles |
| **[roles/planner.md](roles/planner.md)** | Planner role definition and responsibilities | ✅ Yes | Planner implementation, other roles |
| **[roles/assessor.md](roles/assessor.md)** | Assessor role definition and responsibilities | ✅ Yes | Assessor implementation, other roles |
| **[roles/communicator.md](roles/communicator.md)** | Communicator role definition and responsibilities | ✅ Yes | Communicator implementation, other roles |

#### Context Documents

| File | Purpose | Audience |
|---|---|---|
| **[co-teacher.md](co-teacher.md)** | Co-teacher (Inés Vidal) role specification | Co-teacher, leadership |
| **[agent-architecture.md](agent-architecture.md)** | Agent binding architecture and tool scoping | Developers |

### Synthetic Data

| Location | Contents | Purpose |
|---|---|---|
| **[data/students/](../data/students/)** | 133 student YAML files | Test data for workflows |
| **[data/sections/](../data/sections/)** | Class roster files | Section information |
| **[data/school/](../data/school/)** | School context | School-level configuration |

### Executable Code

| File | Purpose | Language |
|---|---|---|
| **[executor.py](../executor.py)** | File-based task executor | Python 3.8+ |

---

## Reading Paths by Role

### For the Teacher (Eric)

**Goal:** Understand workflow and when to provide input

**Reading Path:**
1. **[EXECUTOR_QUICKSTART.md](../EXECUTOR_QUICKSTART.md)** — Understanding how the system works
2. **[roles/README.md](roles/README.md)** — Understand the roles and handoffs
3. **[roles/communicator.md#done-criteria](roles/communicator.md)** — Understand when you need to approve communications
4. **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** — See the big picture

**Key sections to know:**
- Approval workflow (you review before sending)
- Escalation procedure (how to flag issues)
- Contact points for each role

---

### For Co-Teacher / Admin (Inés)

**Goal:** Maintain system, run executor, track progress

**Reading Path:**
1. **[EXECUTOR_QUICKSTART.md](../EXECUTOR_QUICKSTART.md)** — How to run the executor
2. **[HANDOFF_WORKFLOW.md](HANDOFF_WORKFLOW.md)** — Manual execution workflow
3. **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** — Track progress
4. **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** — Understand the architecture

**Key sections to know:**
- CLI arguments for executor
- How to create tasks
- How to check results
- Troubleshooting procedures

---

### For Curriculum Designer Implementation

**Goal:** Implement curriculum designer role with task handling

**Reading Path:**
1. **[roles/README.md](roles/README.md)** — System overview
2. **[roles/curriculum_designer.md](roles/curriculum_designer.md)** — Full role specification
3. **[TASK_SCHEMAS_REFERENCE.md](TASK_SCHEMAS_REFERENCE.md)** — Your task types
4. **[HANDOFF_WORKFLOW.md](HANDOFF_WORKFLOW.md)** — Example workflows

**Key tasks to implement:**
- `CURRDES-SCOPE-<UNIT_ID>` → Generate scope_<UNIT_ID>.md, objectives_<UNIT_ID>.json
- `CURRDES-ASSESS-<UNIT_ID>` → Generate assessments_<UNIT_ID>.md, rubrics_<UNIT_ID>.json
- `CURRDES-LESSONS-<UNIT_ID>` → Generate lessons_<UNIT_ID>.md
- Consume: ASSESS-REVISION tasks from Assessor, PLAN-CONFIRM results from Planner

---

### For Planner Implementation

**Goal:** Implement planner role with task handling

**Reading Path:**
1. **[roles/README.md](roles/README.md)** — System overview
2. **[roles/planner.md](roles/planner.md)** — Full role specification
3. **[TASK_SCHEMAS_REFERENCE.md](TASK_SCHEMAS_REFERENCE.md)** — Your task types
4. **[HANDOFF_WORKFLOW.md](HANDOFF_WORKFLOW.md)** — Example workflows

**Key tasks to implement:**
- `PLAN-CALENDAR-<TERM>` → Generate calendar_<TERM>.md, calendar_<TERM>.json
- `PLAN-PACING-<TERM>` → Generate pacing_<TERM>.md
- `PLAN-CONFIRM-<UNIT_ID>` → Generate time_blocks_<UNIT_ID>.json
- `PLAN-COMMS-<EVENT>` → Generate confirmed_schedule_<EVENT>.json
- Consume: CURRDES-SCOPE results, ASSESS-CLASS results, COMMS-PROGRESS results

---

### For Assessor Implementation

**Goal:** Implement assessor role with task handling

**Reading Path:**
1. **[roles/README.md](roles/README.md)** — System overview
2. **[roles/assessor.md](roles/assessor.md)** — Full role specification
3. **[TASK_SCHEMAS_REFERENCE.md](TASK_SCHEMAS_REFERENCE.md)** — Your task types
4. **[HANDOFF_WORKFLOW.md](HANDOFF_WORKFLOW.md)** — Example workflows

**Key tasks to implement:**
- `ASSESS-INIT-<UNIT_ID>` → Generate mastery_<UNIT_ID>.json
- `ASSESS-SCORE-<ASSESSMENT_ID>` → Generate score_report_<ASSESSMENT_ID>.md, mastery_<UNIT_ID>_updated.json
- `ASSESS-FLAGS-<TERM>` → Generate intervention_flags_<TERM>.json
- `ASSESS-CLASS-<UNIT_ID>` → Generate class_performance_<UNIT_ID>.md
- `ASSESS-AUDIT-<UNIT_ID>` → Generate audit_<UNIT_ID>.md
- Consume: CURRDES-ASSESS results, PLAN-CALENDAR results

---

### For Communicator Implementation

**Goal:** Implement communicator role with task handling

**Reading Path:**
1. **[roles/README.md](roles/README.md)** — System overview
2. **[roles/communicator.md](roles/communicator.md)** — Full role specification
3. **[TASK_SCHEMAS_REFERENCE.md](TASK_SCHEMAS_REFERENCE.md)** — Your task types
4. **[HANDOFF_WORKFLOW.md](HANDOFF_WORKFLOW.md)** — Example workflows

**Key tasks to implement:**
- `COMMS-PROGRESS-<UNIT_ID>` → Generate progress_<UNIT_ID>.md, progress_<UNIT_ID>_email.txt
- `COMMS-INTERVENTION-<STUDENT_ID>` → Generate intervention_<STUDENT_ID>.md, intervention_<STUDENT_ID>_email.txt
- `COMMS-LOG-<TERM>` → Generate contact_log_<TERM>.json
- `COMMS-ATTEMPT-<STUDENT_ID>` → Generate contact_log_<TERM>_updated.json
- `COMMS-ESCALATION-<TERM>` → Generate escalation_<TERM>.md
- Consume: ASSESS-FLAGS, ASSESS-SCORE results, PLAN-CALENDAR results

---

### For System Architect / Tech Lead

**Goal:** Understand full system design and extension points

**Reading Path:**
1. **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** — Complete architecture overview
2. **[HANDOFF_WORKFLOW.md](HANDOFF_WORKFLOW.md)** — Detailed workflow explanation
3. **[roles/README.md](roles/README.md)** — Role definitions and interactions
4. All role specs with handoff formats
5. **[executor.py](../executor.py)** source code
6. **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** — Project tracking

**Key design decisions:**
- File-based handoff pattern (why, benefits, extensibility)
- Task schema stability (why it matters)
- Single-process executor (why, limits, future)
- Role ownership (no shared functions)

---

## Document Relationships

```
EXECUTOR_QUICKSTART ◄── EVERYONE STARTS HERE
       │
       ├─────► System Architecture (visual overview)
       │
       ├─────► Handoff Workflow (detailed explanation)
       │       │
       │       └─────► Task Schemas Reference (lookup)
       │
       ├─────► Roles README (role overview)
       │       │
       │       └─────► Individual Role Specs (curriculum_designer.md, etc.)
       │               │
       │               └─────► Handoff Format sections
       │
       └─────► Implementation Checklist (progress tracking)
```

---

## Key Concepts by Document

### Executable Patterns
- **Task JSON** (input): `docs/roles/README.md#task-json-schema`
- **Result JSON** (output): `docs/roles/README.md#result-json-schema`
- **Manual execution** (how-to): `EXECUTOR_QUICKSTART.md`
- **Workflows** (examples): `HANDOFF_WORKFLOW.md`

### Design Patterns
- **Atomic writes**: `SYSTEM_ARCHITECTURE.md#component-architecture`
- **Handoff chains**: `TASK_SCHEMAS_REFERENCE.md#handoff-chains`
- **Error handling**: `HANDOFF_WORKFLOW.md#error-handling`
- **Idempotence**: `SYSTEM_ARCHITECTURE.md#key-properties-of-the-architecture`

### Task Types
- All task types: `TASK_SCHEMAS_REFERENCE.md`
- By role: `TASK_SCHEMAS_REFERENCE.md#curriculum-designer-tasks`, etc.
- Full schemas: individual role files (curriculum_designer.md, etc.)
- Examples: `HANDOFF_WORKFLOW.md#example-chains`

### Workflow Examples
- Unit build: `HANDOFF_WORKFLOW.md#example-chain-curriculum-planning-assessment`
- Assessment execution: `SYSTEM_ARCHITECTURE.md#example-full-unit-build-workflow`
- Intervention loop: `SYSTEM_ARCHITECTURE.md#example-score-assessment-parent-notification`
- Full system: `SYSTEM_ARCHITECTURE.md#example-full-system-in-action`

---

## FAQ by Question

**Q: How do I create a task?**
A: `EXECUTOR_QUICKSTART.md#creating-a-task`

**Q: What tasks can I create?**
A: `TASK_SCHEMAS_REFERENCE.md`

**Q: How do I run the executor?**
A: `EXECUTOR_QUICKSTART.md#running-the-executor`

**Q: What's the full workflow?**
A: `HANDOFF_WORKFLOW.md#manual-execution-workflow`

**Q: What happens if a task fails?**
A: `HANDOFF_WORKFLOW.md#error-handling`

**Q: How do roles interact?**
A: `HANDOFF_WORKFLOW.md#example-chains` or `SYSTEM_ARCHITECTURE.md#role-interaction-map`

**Q: Where do I implement my role?**
A: Read your role spec (e.g., `roles/assessor.md`), focus on "Handoff Format" section

**Q: How do I test the system?**
A: `HANDOFF_WORKFLOW.md#testing-the-workflow`

**Q: What goes wrong and how do I fix it?**
A: `EXECUTOR_QUICKSTART.md#troubleshooting`

**Q: What's the system architecture?**
A: `SYSTEM_ARCHITECTURE.md`

---

## Document Maintenance

### When to Add New Documentation
- New task type created → Update `TASK_SCHEMAS_REFERENCE.md` and role spec
- New role added → Create `roles/<newrole>.md` with handoff format
- Workflow changed → Update `HANDOFF_WORKFLOW.md`
- Phase completed → Update `IMPLEMENTATION_CHECKLIST.md`

### When to Update Existing Documentation
- Role responsibilities change → Update role spec
- Task schema changes → Update all references (role spec, reference doc, examples)
- Executor behavior changes → Update `EXECUTOR_QUICKSTART.md` and `HANDOFF_WORKFLOW.md`
- Architecture changes → Update `SYSTEM_ARCHITECTURE.md`

### Version Control
- All documentation is markdown (version-controlled)
- Task schemas are the source of truth
- Examples should match current schemas
- Keep `IMPLEMENTATION_CHECKLIST.md` current during implementation

---

## How to Use This Index

1. **I'm new to the system** → Start with "Quick Navigation - Just Getting Started"
2. **I need to implement something** → Find your role in "Reading Paths by Role"
3. **I need to understand a concept** → Find it in "Key Concepts by Document"
4. **I have a question** → Look it up in "FAQ by Question"
5. **I need specific information** → Use "All Documentation Files" table to find the file

---

## Summary

**26 documents organized into 3 layers:**

**Layer 1: Quickstart**
- EXECUTOR_QUICKSTART.md (everyone starts here)

**Layer 2: Reference**
- TASK_SCHEMAS_REFERENCE.md
- SYSTEM_ARCHITECTURE.md
- HANDOFF_WORKFLOW.md

**Layer 3: Specification**
- roles/README.md
- roles/curriculum_designer.md
- roles/planner.md
- roles/assessor.md
- roles/communicator.md
- IMPLEMENTATION_CHECKLIST.md

**Supporting:**
- co-teacher.md
- agent-architecture.md
- UPDATES_SUMMARY.md
- INDEX.md (this file)

**Total documentation:** ~30,000 words + executable code
**Completeness:** All task schemas documented, all workflows explained, all roles specified
**Readiness:** System ready for Phase 3 implementation
