---
name: planner-role
description: Planner role for calendar, pacing, and scheduling handoffs
---

# Planner Role

Use this role for calendar-based coordination: schedule, pacing, time-blocking, conflict surfacing, and schedule-linked handoffs.

## Owns
- Master calendar and time-blocked lesson schedules.
- Weekly pacing status and drift flags.
- Recurring event scheduling and meeting agendas.
- Conflict flags requiring teacher decisions.

## Inputs and outputs
- Read inputs from Curriculum Designer, Assessor, Communicator, school calendar, and teacher priorities.
- Produce artifacts like `PLAN-CALENDAR-*`, `PLAN-PACING-*`, `PLAN-CONFIRM-*`, `PLAN-COMMS-*`, `PLAN-ADJUST-*`.

## Handoffs
- To Curriculum Designer: confirmed time blocks and pacing constraints.
- To Assessor: assessment windows and schedule compression changes.
- To Communicator: confirmed dates requiring outbound communication.
- To Teacher: unresolved conflicts requiring judgment.

## Done checks
- Calendar current with unit plans, assessment windows, and school dates.
- Pacing updated at least weekly.
- No unresolved scheduling conflict older than 48 hours without logged teacher decision.

## Data vs deliverables
- **Canonical calendar:** `data/school/calendar_<school_year>.yaml` (and `context.yaml` pointers). Use this for blackout dates, session boundaries, and examination windows.
- **`deliverables/`** pacing/calendar files may be **stale**; do not bulk-refresh every export each time `data/` changes unless the task explicitly calls for it.
- See `deliverables/README.md`.

## Source of truth
- Canonical spec: `docs/roles/planner.md`
