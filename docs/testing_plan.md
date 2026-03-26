# Testing Plan — Active Phase

**Entered:** 2026-03-26  
**Trigger:** Live LLM calls confirmed working end-to-end.

This document tracks what we are testing, in what order, and what "pass" looks like. It is the working document for this phase — update it as tests run and findings accumulate. When both canonical requests are passing, this phase is done and we prepare for live deployment.

---

## The two canonical requests

Everything here traces back to these:

1. **"I need plans and materials for week X."** → Planner + Curriculum Designer
2. **"I need a report on at-risk students for admin."** → Assessor (+ Communicator)

---

## Phase 1: Output quality — Canonical Request 1

**Status:** In progress

We have a completed run (PLAN-WEEK6-ALG01). The question is whether the output is teacher-reviewable.

### Test 1.1 — Week 6 lesson plans review

**Files to review:**
- `deliverables/week6_ALG01_lesson_plans.md`
- `deliverables/week6_ALG01_materials.md`
- `deliverables/week6_ALG01_assessment.md`

**Pass criteria:**
- [ ] Lesson plans are structured for 45-minute periods (not generic hour-long blocks)
- [ ] Standards cited are NY State (8.EE.C.7 or equivalent), not CCSS generic
- [ ] The model's output reflects that Week 6 is a *review and assessment week*, not new instruction
- [ ] Warm-ups and exit tickets are present and scoped correctly (not full lessons)
- [ ] Assessment is scoped to Unit 1 content only
- [ ] Eric would use these as a starting draft without needing to restructure them

**Failure modes to watch for:**
- Generic lesson templates that ignore the week's position in the unit sequence
- Standards cited that don't exist or don't match grade level
- Materials that ignore the 45-minute constraint
- Assessment that covers content outside Unit 1

**If failing:** Identify whether the problem is in the role spec, the prompt construction, or the task JSON. Update accordingly and rerun.

---

### Test 1.2 — Scope/calendar dependency check

**Question:** Does the executor actually pass scope and calendar data to the model, or does it only pass the task JSON?

**Current behavior:** The task JSON references `deliverables/scope_ALG1_fullyear.json` and `deliverables/calendar_ALG1_fullyear.json` as dependencies, but executor.py does not load and inject them — it only sends the task structure.

**This is a known gap.** The model is generating plans from the goal description alone, not from the actual scope file.

**Test:** Compare a week 6 lesson plan output against the scope file. Does the content match what the scope says should be covered in week 6? Or is it plausible but disconnected?

**Pass criteria:**
- [ ] Content covered matches what the scope file specifies for Week 6
- [ ] OR: gap is documented and a dependency injection mechanism is designed

---

## Phase 2: Role coverage — COMMS and ASSESS

**Status:** Not started. Blocked on Phase 1 completion.

### Test 2.1 — COMMS: Welcome email workflow

**Task:** Submit `COMMS-WELCOME-FALL-2026` (already exists in handoffs).  
**Pass criteria:**
- [ ] Output is a usable draft parent/guardian communication
- [ ] Tone is appropriate for Columbia Secondary context
- [ ] No content that would need to be removed before sending

### Test 2.2 — ASSESS: At-risk student report

**Prerequisite:** Synthetic student data must exist.  
**Task:** Create a task that asks Assessor to identify at-risk students from synthetic section data and produce a formatted report.  
**Pass criteria:**
- [ ] Report format is appropriate for admin submission
- [ ] Criteria applied are explicit and traceable (not opaque)
- [ ] Eric could submit this report after review without restructuring it

---

## Phase 3: Prompt and role spec quality

Tracked separately as findings emerge from Phases 1 and 2.

| Finding | Source | Fix applied | Retest result |
|---|---|---|---|
| (none yet) | | | |

---

## Phase 4: Reliability and edge cases

**Status:** Not started. After Phase 2.

- Multi-task queue: submit 3+ tasks; verify all complete correctly
- Timeout path: submit a task with a 1-second timeout; verify it fails cleanly
- Invalid task: submit malformed JSON; verify executor logs and skips without crashing
- Missing deliverable: verify result shows `failed` if a deliverable file isn't written

---

## What "done" looks like for this phase

This testing phase is complete when:

1. Eric has reviewed at least one Week output and called it usable as a starting draft
2. The scope/calendar dependency gap is either closed or explicitly deferred with a design decision
3. COMMS and ASSESS have each produced one passing output
4. No executor crashes observed across at least 5 task runs

At that point: document the remaining gaps, write the live-deployment readiness checklist, and present to Eric for a go/no-go decision.
