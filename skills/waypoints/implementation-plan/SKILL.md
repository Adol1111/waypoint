---
name: implementation-plan
description: Create or revise a durable implementation plan when the user wants to review execution before coding, work must remain recoverable across multiple meaningful slices or collaborators, or sequencing, migration, compatibility, rollout, rollback, or cross-module coordination creates real risk. Capture strategy, change map, stable slices, constraints, and final verification without prescribing commits.
---

# Implementation Plan

Make one already-bounded Feature or child Task's internal execution strategy reviewable and recoverable when a concise approach preview is not enough.

## Decide whether a plan is warranted

Create or update a plan when at least one material trigger exists:

- the user wants to review execution strategy before coding;
- implementation spans multiple meaningful slices whose stable intermediate states must remain recoverable;
- another session or collaborator needs more durable execution guidance than the task, spec, and design provide;
- modification or deployment order affects correctness;
- data, schema, protocol, or persisted-format migration is involved;
- compatibility must be maintained across versions or modules;
- rollout, feature flags, dual operation, or backout behavior matters;
- ownership spans modules or systems and coordination is non-obvious;
- verification must occur in a particular order to contain risk.

If none applies, return a concise approach preview covering change surface, execution order, material constraints, and verification seam, then stop. Create neither a plan artifact nor a skipped-plan marker, and do not begin implementation unless the user's current request separately assigns that exact Feature or Task.

## Work independently

1. Read repository instructions, the assigned Feature or Task, Feature spec, any relevant technical design, relevant code, and existing plan conventions.
2. Identify which material trigger requires durable planning. Update an existing plan when it fits; otherwise propose the smallest Markdown artifact beside its Feature or Task.
3. Preserve the spec's scope and the technical design's choices; surface contradictions rather than adding requirements or redesigning the solution.
4. Capture the execution strategy, change map, ordered slices, constraints, rollback or containment, and final verification.
5. Make clear why the order matters and what stable state follows each slice.
6. Add a plan Reference to `feature.md` or the owning `task.md` only after the plan artifact exists. Link only the actual repository-native filename and do not create placeholder References.

Do not require a fixed docs tree, branch convention, workflow stage, review pause, or commit sequence. Never prescribe one commit per slice.

Own safe execution order inside one Feature or Task, not Feature decomposition, architecture, or behavior. Use `task-planning` when a Feature must be divided among executors; do not copy its Task graph into this artifact. When a review-critical technical choice is unresolved, leave sequencing undecided and surface the need for technical design.

Use [references/plan-template.md](references/plan-template.md) only when no local format exists. Omit irrelevant headings.

Planning is complete when another session can execute every meaningful slice in order, recognize its stable state, contain or roll back material failure, and verify the integrated result without reconstructing strategy from chat.

Finish after publishing the plan. Approval of an implementation plan authorizes the plan artifact only and never authorizes code changes or invocation of an execution skill.

## Companion skills

Use `research` for unfamiliar migration constraints, `tdd` for test-first execution when useful, `code-review` for an independent risk review, and `handoff` when another collaborator will execute the plan. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`.
