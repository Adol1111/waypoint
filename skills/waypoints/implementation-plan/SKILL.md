---
name: implementation-plan
description: Create or revise an implementation plan only when sequencing, migration, compatibility, rollout, or cross-module coordination creates real execution risk. Use to capture strategy, change map, ordered delivery slices, risk and rollback constraints, and final verification without prescribing commits.
---

# Implementation Plan

Make risky execution order and recovery boundaries explicit. Do not create a plan for straightforward work.

## Decide whether a plan is warranted

Create or update a plan when at least one material trigger exists:

- modification or deployment order affects correctness;
- data, schema, protocol, or persisted-format migration is involved;
- compatibility must be maintained across versions or modules;
- rollout, feature flags, dual operation, or backout behavior matters;
- ownership spans modules or systems and coordination is non-obvious;
- verification must occur in a particular order to contain risk.

If none applies, explain briefly that the task can be implemented directly and stop without creating an artifact.

## Work independently

1. Read repository instructions, the task or spec, any relevant technical design, relevant code, and existing plan conventions.
2. Update an existing plan when it fits. Otherwise propose the smallest Markdown artifact near its task or in a repository-consistent location.
3. Preserve the spec's scope and the technical design's choices; surface contradictions rather than adding requirements or redesigning the solution.
4. Capture the execution strategy, change map, ordered slices, constraints, rollback or containment, and final verification.
5. Make clear why the order matters and what stable state follows each slice.

Do not require `docs/tasks/`, a branch convention, a workflow stage, fixed review pauses, or a commit sequence. Never prescribe one commit per slice.

Own safe execution order, not architecture or task behavior. When a review-critical technical choice is unresolved, leave sequencing undecided and surface the need for technical design.

Use [references/plan-template.md](references/plan-template.md) only when no local format exists. Omit irrelevant headings.

## Companion skills

Use `research` for unfamiliar migration constraints, `tdd` for test-first execution when useful, `code-review` for an independent risk review, and `handoff` when another collaborator will execute the plan. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`.
