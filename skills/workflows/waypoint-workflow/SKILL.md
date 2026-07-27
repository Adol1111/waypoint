---
name: waypoint-workflow
description: Read existing repository artifacts and recommend exactly one next Waypoint atomic skill. Use when the user wants help finding the next durable engineering waypoint among context, roadmap, specification, planning, task state, execution, or optional docs bootstrap; never perform that skill's work.
---

# Waypoint Workflow

Find the next useful atomic waypoint for users who do not want persistent Milestone governance.

## Inspect adaptively

1. Read repository instructions and the current request.
2. Search for relevant artifacts by meaning and local convention. Read only artifacts that exist and bear on the request.
3. Treat absent docs as absence of evidence, not a bootstrap failure.
4. Identify the strongest current need and recommend exactly one atomic skill.
5. Give the evidence, existing artifacts to reuse, and one unresolved choice only when it blocks that skill.

Do not create or update artifacts, specs, plans, roadmap tasks, state, or implementation. Do not invoke the recommended skill in the same coordinator action.

## Recommendation map

- Durable ambiguous term or qualifying architecture decision: `domain-context`
- Goal needs independently verifiable delivery slices: `roadmap-planning`
- Concrete task needs a reviewable behavioral boundary: `task-spec`
- Real sequencing, migration, compatibility, rollout, or coordination risk: `implementation-plan`
- Acceptance, blocker, status, evidence, or isolated-work closing needs visibility: `task-state`
- Scoped task or spec is ready to implement: `task-execution-simple`
- Team explicitly wants a shared local docs convention: `docs-workflow-bootstrap`

Prefer the skill closest to the user's requested outcome. For example, missing docs do not outrank a request to implement a supplied, workable task. When evidence ties, recommend the smallest earlier waypoint that prevents material invention.

## Output

Return:

- `Evidence`: the request and existing artifact signals;
- `Recommended skill`: exactly one skill name;
- `Reuse`: existing artifacts that skill should read or update;
- `Why now`: one concise rationale.

Docs conventions are opt-in and never prerequisites.

This workflow does not create or manage Milestones. When the user wants persistent multi-task delivery governance, use `milestone-workflow` as the chosen workflow rather than layering Milestone state into this router.
