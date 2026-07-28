---
name: task-spec
description: Write or revise a compact behavioral specification for one concrete engineering task. Use when a collaborator needs durable problem and outcome, scope and non-goals, observable rules, relevant failure or compatibility requirements, and completion proof without relying on chat history.
---

# Task Spec

Create the smallest specification from which a reviewer can understand and challenge the task.

## Work independently

1. Read repository instructions, the supplied task, relevant code and docs, and any existing spec convention.
2. Update the existing task or spec artifact when it can remain clear. Otherwise propose a small local Markdown file near the task or in a repository-consistent location.
3. Resolve present-state facts from the repository. Ask only about future intent that materially changes the result.
4. Write the spec so a reviewer with no chat history can evaluate it.
5. Re-read it as that reviewer and remove assumptions that exist only in conversation.

Do not require a roadmap, tracker, docs directory, branch, plan, or review ceremony.

Before writing, test the task boundary. If the requested acceptance contains multiple outcomes that can be delivered, reviewed, or rejected independently, do not hide them inside one specification. Return the boundary issue to the supplied roadmap or chosen workflow, or propose separate specs when the user asked for that decomposition.

## Required information, adaptive structure

Make these facts explicit somewhere in the artifact:

- problem or motivation, desired outcome, and why it matters;
- in-scope behavior and meaningful non-goals;
- actors, inputs, outputs, rules, and user- or operator-visible state transitions when relevant;
- material product or behavioral decisions and why they were chosen;
- observable error, fallback, partial-failure, or compatibility requirements when relevant;
- externally imposed constraints that limit an acceptable solution;
- completion proof, including what evidence demonstrates success.

Use headings that fit the task. Do not force empty sections, an option matrix, a diagram, or alternatives that were never genuinely considered. A compact spec may be a few focused sections; compact must not mean implicit.

Own what the system must do, not the internal mechanism used to do it. Do not choose architecture, module seams, internal interfaces, database schema, persistence strategy, internal state machines, concurrency control, caches, algorithms, file paths, or code structure. Preserve a mandated technical constraint when it is part of the request, but route unresolved review-critical implementation choices to `technical-design`.

Keep implementation sequencing out. When sequencing, migration, compatibility, rollout, or cross-module coordination is risky, leave the specification stable and use `implementation-plan` separately.

Use [references/spec-template.md](references/spec-template.md) only when no stronger local pattern exists.

## Companion skills

Use `grilling` for consequential unresolved intent, `research` for external facts, and `tdd` when test-first design would improve the task. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`. Do not copy their protocols into the spec.
