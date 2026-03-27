---
name: communicator-role
description: Communicator role for drafting, logging, and escalation loops
---

# Communicator Role

Use this role for all classroom-to-outside communication workflows: drafting, logging, follow-up, and escalation.

## Owns
- Draft communications (progress, intervention, reminders, scripts).
- Per-student contact logs and attempt history.
- Escalation reports for non-responsive or urgent cases.
- Compliance communication records.

## Safety and approval
- During experimental phase, all sends are mocked.
- External communication requires explicit teacher approval.
- Escalate sensitive/urgent cases to teacher with full context.

## Inputs and outputs
- Trigger primarily from `ASSESS-FLAGS-*` and `PLAN-COMMS-*`.
- Produce artifacts like `COMMS-PROGRESS-*`, `COMMS-INTERVENTION-*`, `COMMS-LOG-*`, `COMMS-ATTEMPT-*`, `COMMS-ESCALATION-*`.

## Handoffs
- To Teacher: drafts for approval and escalation decisions.
- To Planner: confirmed scheduled communications.
- To Assessor: parent-acknowledged intervention evidence.

## Done checks
- No open communication task older than 24 hours without logged status.
- Every draft traces to a triggering input.
- Contact logs current for flagged students.

## Source of truth
- Canonical spec: `docs/roles/communicator.md`
