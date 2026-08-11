---
name: feature-spec
description: Write or revise the durable behavioral contract for one Feature. Use when collaborators or execution agents need shared outcome, scope, observable rules, failure and compatibility behavior, and completion proof without relying on chat or prescribing implementation.
---

# Feature Spec

Capture agreed behavior once so every Task consumes the same contract.

## Establish the Feature boundary

1. Read repository instructions, the requirement or Feature record, relevant product context, existing behavior, and local specification conventions.
2. Identify the stable Feature ID, owner, intended outcome, scope, non-goals, and observable completion proof.
3. Synthesize decisions already established by the user and repository. Do not interview again, widen scope, add technical choices, or silently settle future intent while writing.
4. Stop and return the unresolved decision when behavior is still ambiguous enough to change Acceptance or Task boundaries.

A Feature split across executors must have one durable behavioral contract before Task planning. A small unsplit Feature may keep a compact contract in `feature.md` when its outcome, scope, rules, and Acceptance are already reviewable; do not create a separate file solely to satisfy a layout.

## Write behavior, not implementation

Include only the smallest useful set of:

- problem, motivation, outcome, and actors;
- included behavior and meaningful non-goals;
- observable inputs, outputs, rules, and state transitions;
- failure, compatibility, security, or operational behavior visible at the contract boundary;
- representative scenarios when they clarify a material edge;
- externally imposed constraints;
- authoritative Feature Acceptance when no stronger Feature record owns it.

Do not include architecture, module seams, schemas, algorithms, file paths, Task decomposition, execution order, test-writing steps, rollout mechanics, or commit instructions. Link an existing design rather than summarizing it.

Update an existing repository-native specification when one fits. Otherwise use [references/spec-template.md](references/spec-template.md). Keep canonical Acceptance in `feature.md` when that Feature record exists; the spec explains the behavior that makes those checks meaningful without copying the checklist.

Finish after the agreed behavior is durable. Approval authorizes this specification only; do not continue into design, Task planning, implementation planning, or code unless the current request explicitly names that separate planning outcome. Planning never authorizes implementation.

## Companion skills

Use `grilling` for unresolved product intent and `research` for material external facts when installed. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and remain optional.

Install only the needed companion with `npx skills add mattpocock/skills --skill <name>`.
