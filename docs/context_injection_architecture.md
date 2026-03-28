# Context Injection Architecture

## Problem Statement

**Test 1.1 Critical Finding:** The executor was passing task descriptions to the model without curriculum scope and calendar context. The model had to infer unit structure from goal alone, resulting in wrong unit content being generated.

Root cause: `executor.py` called `build_prompt()` with only role spec + task structure, not the actual scope and calendar files the task declared as dependencies.

## Solution: Minimal Stable Core + Task-Scoped Curriculum Context

### Architecture

```
build_prompt(task)
  ↓
load_context(task)  ← NEW: loads + injects context before role spec
  ├─ load_school_context()     [~75 tokens, always]
  └─ load_curriculum_context() [~120 tokens, if course/unit in task]
  ↓
[role spec from load_role_spec()]
  ↓
[task details: goal, plan, constraints]
```

### Token Budget

For a PLAN-WEEK6-ALG01 task:

| Layer | Tokens | Changes | Source |
|-------|--------|---------|--------|
| School context | ~75 | Once per year | `data/school/context.yaml` |
| Unit 1 scope | ~90 | Once per course | `deliverables/scope_ALG1_fullyear.json` |
| Unit 1 calendar | ~35 | Once per year | `deliverables/calendar_ALG1_fullyear.json` |
| **Total context** | **~200** | Rarely | |

**Canonical truth vs injection source:** Scope and calendar **ground truth** for the classroom-manager data layer live under **`data/`** (`data/courses/<course_id>/scope.yaml`, `data/school/calendar_<year>.yaml`). The executor currently loads JSON from **`deliverables/`** for token-efficient prompts; those files can **lag** behind `data/`. Agents answering “what is the current scope/calendar?” should prefer **`data/`**. See [`deliverables/README.md`](../deliverables/README.md). Aligning `executor.py` to read from `data/` where appropriate is a separate, optional hardening step.
| Role spec (planner) | ~1200 | Never | `docs/roles/planner.md` |
| Task details | ~300 | Every call | Task JSON |
| **Total prompt** | **~1700** | | |

### Implementation: Three Functions

#### 1. `load_school_context(data_dir: Path) -> Optional[str]`

Loads the first ~20 lines of `data/school/context.yaml`. This is the stable ground truth for every prompt, regardless of role.

**Returns:** School name, student population note, teacher name, district. ~75 tokens.

#### 2. `load_curriculum_context(task: Dict, deliverables_dir: Path) -> Optional[str]`

Extracts minimal unit context scoped to the task.

**Inputs:** Looks for:
- `task.course` or `task.constraints.course`
- `task.unit` or `task.plan.unit_number` or `task.plan.context.unit_number` ← **nested extraction!**
- `task.week` or `task.plan.week_number` or `task.constraints.week`

**File mapping:** 
- Course "Algebra I" → "ALG1"
- Loads: `deliverables/scope_ALG1_fullyear.json` + `deliverables/calendar_ALG1_fullyear.json`

**Returns:** Unit title, standards (first 8), dates, instructional days. ~120 tokens.

**Returns None if:** no course info, files don't exist, or unit not found in scope/calendar.

#### 3. `load_context(task: Dict, data_dir: Path, deliverables_dir: Path) -> str`

Combines school + curriculum context into a single injection block.

**Returns:** Markdown-formatted context ready to prepend to prompt.

### Extraction Logic (Critical Detail)

The task structure has unit_number in **three possible places**:

```python
unit = task.get("unit")                              # top-level (rare)
if unit is None:
    unit = task.get("plan", {}).get("unit_number")  # plan.unit_number (rare)
if unit is None:
    unit = task.get("plan", {}).get("context", {}).get("unit_number")  # plan.context.unit_number (ACTUAL)
```

The third location is where the handoff system currently puts it. Both earlier checks are for forward-compatibility.

### File Naming Convention

Scope and calendar files use a `_fullyear` suffix:

```
deliverables/scope_ALG1_fullyear.json      (not scope_ALG1.json)
deliverables/calendar_ALG1_fullyear.json   (not calendar_ALG1.json)
```

### Integration with build_prompt()

```python
def build_prompt(task: Dict[str, Any]) -> str:
    lines = []
    
    # 1. Load and inject minimal context ← NEW
    context = load_context(task)
    if context:
        lines.append(context)
        lines.append("=" * 80)
        lines.append("")
    
    # 2. Load and inject role specification (existing)
    role_spec = load_role_spec(get_role_prefix(task_id))
    if role_spec:
        lines.append("## ROLE SPECIFICATION")
        lines.append(role_spec)
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
    
    # 3. Task details (existing)
    lines.append("## TASK DETAILS")
    # ... rest of prompt
    
    return "\n".join(lines)
```

### Scope and Calendar File Structure

**scope_ALG1_fullyear.json:**
```json
{
  "units": [
    {
      "unit_number": 1,
      "title": "Foundations: Numbers, Expressions, and the Language of Algebra",
      "instructional_days": 15,
      "ccss_standards": ["N-RN.1", "N-RN.2", "N-RN.3", "A-SSE.1a", "A-SSE.1b"],
      "essential_questions": [...],
      "content": [...]
    },
    ...
  ]
}
```

**calendar_ALG1_fullyear.json:**
```json
{
  "units": [
    {
      "unit_number": 1,
      "title": "Foundations: Numbers, Expressions, and the Language of Algebra",
      "start_date": "2026-09-09",
      "end_date": "2026-10-01",
      "instructional_days": 15,
      "calendar_weeks": 3,
      "weeks": [...]
    },
    ...
  ]
}
```

Key field names:
- Scope: `unit_number`, `ccss_standards`
- Calendar: `unit_number`, `calendar_weeks`, `start_date`, `end_date`, `instructional_days`

## Testing & Validation

### Test Case: PLAN-WEEK6-ALG01

**Task:** Produce lesson plans for week 6 of Algebra I.

**Context injected:**
```
## SCHOOL & CLASSROOM CONTEXT
# School Context
# ...
school:
  name: Columbia Secondary School
  ...

## CURRICULUM CONTEXT
# Unit 1: Foundations: Numbers, Expressions, and the Language of Algebra

## Standards
- N-RN.1
- N-RN.2
- N-RN.3
- A-SSE.1a
- A-SSE.1b

## Timeline
Start: 2026-09-09
End: 2026-10-01
Instructional Days: 15
```

**Result:** Model now has Unit 1 scope + calendar before generating. Should generate Unit 1 content (numbers, expressions) instead of Unit 2 content (linear equations).

## Future Refinements

### Per-Role Context Variations

ASSESS and COMMS roles don't need curriculum context by default. Could add a role-specific flag:

```python
def load_context(task, role_prefix=None, ...):
    if role_prefix in ("assess", "comms"):
        return load_school_context()  # school only
    else:
        return load_school_context() + load_curriculum_context()
```

### Week-Level Granularity

For more precision, could extract `plan.context.unit_week_range` to indicate "this is week 4-5 of the unit" and narrow further. Currently scoped to unit only.

### Student Context (Future)

ASSESS tasks need student population data. Could extend with `load_student_context()` that extracts from a student registry, scoped by class/section.

### Caching

Could cache loaded scope/calendar files in memory to avoid repeated disk reads. Simple dict keyed by filename.

## Metrics

### Token Efficiency

- School context: **75 tokens** (1 per school year, always used)
- Unit context: **120 tokens** (varies by unit; downloaded once per course)
- **Total overhead: 195 tokens per prompt**

Compare to:
- Role spec: 1200 tokens (large but stable)
- Full task description: 300 tokens

**ROI:** 195 additional tokens gives model ground truth for scope alignment. Very cheap insurance against Test 1.1 failure.

### File I/O

- **Disk reads per prompt:** 2–3 (school context + scope + calendar)
- **Cached:** Could reduce to 0 after first request in a batch
- **Speed impact:** Negligible (~10ms per read on local filesystem)

---

**Status:** ✓ Implemented in executor.py
**Tested:** PLAN-WEEK6-ALG01 context generation working
**Next:** Re-run Test 1.1 with updated executor to verify Unit 1 content generation
