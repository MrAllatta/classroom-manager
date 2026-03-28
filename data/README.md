# Data Directory

This directory holds the structured metadata that runs the classroom system. It is organized in three layers plus **course scope** (shared curriculum files referenced by sections), each with distinct ownership, access rules, and sensitivity levels.

Structured data exists so agents and tools can support **decisions**, not so the teacher digs through fields. Downstream reports and handoffs should still satisfy the **teacher-next** bar: after reading a computed summary, the teacher knows **what to do next**. See [`docs/architecture_and_workflows.md`](../docs/architecture_and_workflows.md#teacher-next-bar).

---

## Three-layer architecture

### Layer 1 — School context (`school/`)
Environmental constants. Set once per school year; updated rarely.

| File | Contents |
|---|---|
| `school/context.yaml` | School name, population characteristics, special education framework, privacy policy, calendar system, teacher identity |
| `school/calendar_<school_year>.yaml` | Academic calendar events (session boundaries, holidays, recesses); referenced from `context.yaml` |

**Sensitivity:** Low. No student data. Safe to read into any agent context.

---

### Layer 2 — Sections (`sections/`)
One file per section. Updated at enrollment changes or staffing changes.

| File | Section |
|---|---|
| `sections/algebra_1.yaml` | Algebra I — Period 1 (ALG-01) |
| `sections/algebra_2.yaml` | Algebra I — Period 2, ICT (ALG-02) |
| `sections/algebra_3.yaml` | Algebra I — Period 4 (ALG-03) |
| `sections/ap_statistics.yaml` | AP Statistics (AP-STAT) |
| `sections/ap_cs_a.yaml` | AP Computer Science A (AP-CSA) |

Each section file contains:
- Course and standards framework
- Staffing (teacher, co-teacher, ICT flag)
- Section-level special education aggregate fields (counts, accommodation cluster)
- Pacing and curriculum references

**Sensitivity:** Low-medium. Aggregate special ed counts are not PII. Safe for agent planning contexts. Do not store individual student names or IDs here.

---

### Layer 3 — Student profiles (`students/`)
One file per student. The living layer — updated continuously by role workflows.

**Sensitivity: HIGH. FERPA-protected.**

In the experimental phase, this directory contains only synthetic/dummy data. In production, real student data must never be passed through an LLM context window. Tools must query this directory locally and return computed results only — not raw records.

See `schema/student_profile.yaml` for the canonical field definitions.

---

## Schema (`schema/`)

Reference documents that define structure. Not student data.

| File | Contents |
|---|---|
| `schema/student_profile.yaml` | Canonical field definitions for a student record |
| `schema/accommodation_types.yaml` | Structured list of accommodation codes with labels, categories, and implementation notes |
| `schema/course_scope.yaml` | Shape of course scope files under `courses/<course_id>/` |
| `schema/school_calendar.yaml` | Shape of academic calendar files under `school/calendar_<school_year>.yaml` |

Schema files are safe to read into any agent context. They contain no student data.

---

## Role access map

| Role | Layer 1 (school) | Layer 2 (sections) | Layer 3 (students) | Schema |
|---|---|---|---|---|
| **Co-Teacher (Inés)** | Read/Write | Read/Write | Write (schema/structure only) | Read/Write |
| **Planner** | Read | Read | Tools only (no raw read) | Read |
| **Curriculum Designer** | Read | Read | Tools only | Read |
| **Assessor** | Read | Read | Tools only — computes grades, flags, mastery | Read |
| **Communicator** | Read | Read | Tools only — reads contact/log fields | Read |
| **Teacher (Eric)** | All | All | All (full access, human judgment) | All |

**"Tools only"** means: a future tool or script queries the student data locally and returns a computed result (e.g., a list of students missing accommodation, a count of IEPs per section). The raw student record does not enter the agent's context window.

---

## Privacy policy

1. **FERPA applies.** All student data is FERPA-protected federal education records.
2. **Experimental phase:** Only synthetic/dummy data is used. No real student data is permitted until the production gate is verified.
3. **Production gate:** See `school/context.yaml` → `privacy.production_gate`. Must be set to `unlocked` (with documented safeguards) before live data may be used.
4. **Sensitive fields:** Fields marked `sensitive: true` in `schema/student_profile.yaml` are FERPA-protected and must be handled by local tools, never passed to an LLM in plain text.
5. **Accommodation codes are not sensitive by themselves.** A code like `TIME_EXTENDED_15` in `accommodation_types.yaml` is reference data. The same code in a specific student's record is sensitive.

---

## SESIS integration roadmap

SESIS is the NYC DOE Special Education Student Information System. It is the source of truth for IEP/504 data in New York City schools.

**Current status:** Not connected. All special education fields in student profiles are populated manually (dummy phase) or will be entered by hand at start of year.

**Planned integration:**
- Export student records from SESIS in the supported format
- Map SESIS fields to the student profile schema (see `schema/student_profile.yaml` — fields marked `sesis_source: true` will be populated from exports)
- Build a local import tool that parses SESIS exports and writes to `data/students/` without exposing raw data to agents
- Validate accommodation codes against `schema/accommodation_types.yaml` on import

**Key SESIS fields to map:**
- OSIS number → `student_id`
- Disability classification → `disability_category`
- Annual review date → `compliance.annual_review_due`
- Triennial evaluation date → `compliance.triennial_evaluation_due`
- Accommodation list → `accommodations[].code` (requires code translation)

**College Board SSD (AP exam accommodations):**
AP exam accommodations are a separate process from classroom IEP/504 accommodations. Students with plans must apply through College Board's Services for Students with Disabilities program. This is flagged in each AP section file. A separate SSD tracking workflow is needed; see section files for deadline notes.

---

## Maintenance

| What changed | Who updates it | Where |
|---|---|---|
| New school year, new school | Teacher (Eric) | `school/context.yaml`, `school/calendar_<school_year>.yaml` |
| Enrollment or staffing changes | Co-teacher or Teacher | `sections/<section>.yaml` |
| Course scope / sequence revision | Curriculum Designer or Teacher | `courses/<course_id>/scope.yaml` |
| New student joins | Assessor or Teacher (via tool) | `students/<id>.yaml` |
| New accommodation type needed | Co-teacher | `schema/accommodation_types.yaml` |
| Schema field added or changed | Co-teacher | `schema/student_profile.yaml` + this README |

Last updated: 2026-03-27
