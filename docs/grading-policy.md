# Grading policy (draft)

**Status:** Draft for teacher review. The teacher of record decides; agents apply rubrics and reporting **consistently** to this text unless Eric revises it.

**Related:** [Assessor role](roles/assessor.md), [Curriculum Designer role](roles/curriculum_designer.md) (assessments + rubrics), unit planning schemas under `data/schema/`.

---

## 1. Purpose

- Make **what is graded** and **what the number means** legible before the year blows the plan up.
- Reduce the moral load of “putting the score down” by requiring **predeclared rubrics**, **traceable evidence**, and **honest labeling** of tasks.
- Keep **Depth of Knowledge (Webb DOK)** where it helps: **task and item design** — not as a substitute for proficiency on standards.
- So that grading outputs answer **what the teacher should do next** (reteach, gather more evidence, confer, report) rather than freezing a number in isolation. See [`architecture_and_workflows.md`](architecture_and_workflows.md#teacher-next-bar).

---

## 2. Two axes (do not collapse them)

| Axis | Describes | Binds to |
|------|-----------|----------|
| **DOK** (or a future parallel taxonomy) | Cognitive **demand of the task** — context, scaffolding, how much independent judgment | Assessment items, key formative anchors, lesson activities (planned together) |
| **Proficiency** | How well the **student** meets the **standard** on evidence | Rubric levels **per standard** (e.g. 0–4) |

Rules of thumb:

- DOK labels **tasks**, not people. No student is “a DOK 2.”
- **Low DOK** can still be **full proficiency** when the standard is recall, fluency, or routine use in scope.
- **High DOK** does not mean automatic “A” work; it means the item is fit to elicit evidence for **standards that require** strategic or extended thinking.

---

## 3. Proficiency scale (0–4 per standard)

Anchor language — **align phrasing to NYS/NYC reporting and course expectations**; adjust in this file when the district changes terms.

| Level | Meaning (evidence-based) |
|-------|---------------------------|
| **4** | Excellent / exceeds: consistent, justified, transferable within the domain for this standard; any gaps are minor and do not undermine the claim. |
| **3** | Proficient / meets: performance matches the rubric’s “meets” descriptor for this standard. |
| **2** | Approaching / partial: recognizable attempt; important elements missing or unstable. |
| **1** | Limited / not yet proficient: minimal or flawed evidence relative to the standard’s minimal bar. |
| **0** | No evidence / not yet assessed. |

**Important:** Proficiency **1** describes **evidence against the standard**, not “DOK 1” and not a moral verdict on the learner. If the gradebook maps levels to percents or letters, that mapping is **school policy**, not mathematics implied by DOK.

---

## 4. School gradebook vs proficiency (the “1 means 65” problem)

When the student information system or report card forces **percent or letter**:

- **Document the conversion explicitly** (e.g. in school context data or the reporting template Eric actually uses). Do not let a rubric level silently equal a percent without review.
- Prefer policies that separate **formative** practice from **summative** grading checkpoints where the school allows it.
- Prefer **reassessment or replacement rules** that are stated up front (what can replace an earlier score, by when, for which standards).

*Eric: fill in concrete rules for your building — mastery-only averages, late policy, retakes, and whether a “1” on a formative is excluded from the average.*

---

## 5. Evidence bundles and fairness

- **Bundle:** Infer proficiency for a standard from **multiple artifacts** when possible (exit ticket, quiz section, project checkpoint, etc.). The unit’s assessor init / mastery structure should name **which artifacts count** for which standards — not invented at report-card time.
- **Backward alignment:** A graded checkpoint should trace to **objectives and practice** named **before** the checkpoint. When the live classroom diverges (normal), **adjust the checkpoint or the weighting** — do not measure a “final task” that was never taught.
- **Override:** The teacher of record may override a suggested score; record a **short reason** so future-you trusts the book.

---

## 6. Roles (how this repo uses the policy)

- **Curriculum Designer:** Builds assessments and **standard-aligned rubrics**; may tag items with **intended DOK** for transparency and audit (“does this item actually elicit the thinking we claim?”).
- **Assessor:** Scores against **rubric ↔ standard**; uses DOK in **quality audits**, not as the proficiency level.
- **Planner:** Schedules windows so evidence exists before hard reporting deadlines.
- **Co-Teacher:** Keeps this document aligned with practice; routes grading-design gaps to the right role.

---

## 7. AI and discernment

Students are expected to **evaluate** tool-generated output (criteria, limits, revision) — especially where standards ask for justification or choice. Grading rewards **grounded judgment**, not mere completion of steps.

---

## 8. Limits

This policy does not override **IEPs**, **504 plans**, **school or district grading regulations**, or **external programs** (e.g. AP) where those rules are stricter or different. Those constraints **win**; this file describes the default classroom philosophy inside those fences.

---

## 9. Next edits (when Eric says go)

- Fill §4 with your building’s real conversion and reassessment rules.
- Optionally add structured fields (e.g. DOK on items, proficiency rules in YAML) in `data/schema/` and wire agents to read them — **one testable chunk at a time.**
