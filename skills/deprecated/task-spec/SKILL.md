---
name: task-spec
description: Deprecated archive of the former task-level behavioral specification skill. Do not use for new work; use feature-spec so one Feature owns the shared behavioral contract consumed by child Tasks.
---

> [!WARNING]
> Deprecated snapshot. Use `feature-spec` for new work. This file is retained only for migration reference.

# Task Spec

Create the smallest specification from which a reviewer can understand and challenge the task.

## Work independently

1. Read repository instructions, the supplied task, relevant code and docs, and any existing spec convention.
2. Update an existing specification when one fits. Otherwise create the smallest repository-consistent specification, normally beside the task artifact when one exists.
3. Resolve present-state facts from the repository. Ask only about future intent that materially changes the result.
4. Write the spec so a reviewer with no chat history can evaluate it.
5. Re-read it as that reviewer and remove assumptions that exist only in conversation.
6. When a task artifact exists, keep Acceptance authoritative there:
   - create or update its observable Acceptance checklist from the agreed behavior;
   - add a References section only after the specification exists, linking only artifacts that already exist;
   - remove roadmap-era Planning Boundary and Stage Proof once the specification and Acceptance supersede them;
   - remove task-local Open Decisions after transferring each decision to the specification, technical design, or another durable owner.
7. When no task artifact exists, keep the observable Acceptance or completion proof in the specification itself so independent use does not lose it.

Do not require a roadmap, tracker, docs directory, branch, plan, or review ceremony.

Before writing, test the task boundary in both directions. If the requested acceptance contains multiple outcomes that can be delivered, reviewed, or rejected independently, do not hide them inside one specification. If it is only a file edit, endpoint, test step, migration action, or other fragment with no meaningful stage result by itself, return the undersized boundary instead of manufacturing a task spec. Route either issue to the supplied roadmap or chosen workflow, or propose separate specs when the user asked for decomposition.

## Required information, adaptive structure

Make these facts explicit somewhere in the artifact:

- problem or motivation, desired outcome, and why it matters;
- in-scope behavior and meaningful non-goals;
- actors, inputs, outputs, rules, and user- or operator-visible state transitions when relevant;
- material product or behavioral decisions and why they were chosen;
- observable error, fallback, partial-failure, or compatibility requirements when relevant;
- externally imposed constraints that limit an acceptable solution;
- observable Acceptance or completion proof, stored in the task artifact when one exists and otherwise in the specification.

Use headings that fit the task. Do not force empty sections, an option matrix, a diagram, or alternatives that were never genuinely considered. A compact spec may be a few focused sections; compact must not mean implicit.

The specification is complete when a reviewer without chat history can identify the intent, boundary, behavioral contract, material rationale, relevant failure or compatibility behavior, and the single durable Acceptance owner.

Own what the system must do, not the internal mechanism used to do it. Do not choose architecture, module seams, internal interfaces, database schema, persistence strategy, internal state machines, concurrency control, caches, algorithms, file paths, or code structure. Preserve a mandated technical constraint when it is part of the request, but route unresolved review-critical implementation choices to `technical-design`.

Do not duplicate the task's Acceptance checklist in the specification. The specification explains the behavioral contract; `task.md` tracks whether that contract has been satisfied. Keep implementation sequencing out. When sequencing, migration, compatibility, rollout, or cross-module coordination is risky, leave the specification stable and use `implementation-plan` separately.

Use [references/spec-template.md](references/spec-template.md) only when no stronger local pattern exists.

## Companion skills

Use `grilling` for consequential unresolved intent, `research` for external facts, and `tdd` when test-first design would improve the task. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`. Do not copy their protocols into the spec.
