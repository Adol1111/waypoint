---
name: technical-design
description: Create or revise a task-level technical design for review-critical implementation choices. Use when architecture, module or interface seams, data or state models, non-trivial algorithms, concurrency, security, performance, or testing strategy should be decided durably before coding.
---

# Technical Design

Make consequential implementation choices reviewable without turning the design into a coding recipe.

## Decide whether design is warranted

Create or update a technical design when at least one material question cannot safely be left to implementation-time judgment:

- architecture, module responsibilities, interfaces, or seams;
- data ownership, persistence shape, state transitions, or event flow;
- a non-trivial algorithm or protocol;
- concurrency, consistency, security, privacy, performance, or operational behavior;
- integration contracts or testing seams that shape the solution;
- genuine technical alternatives with different long-term consequences.

If repository practice already determines the approach and no review-critical choice remains, give a concise approach preview and stop without creating an artifact.

## Work independently

1. Read repository instructions, the task or behavioral spec, relevant code and tests, existing architecture and decision records, and local design conventions.
2. Separate repository facts and externally imposed constraints from choices that still need judgment.
3. Update an existing suitable design artifact or technical-design section when possible. Otherwise propose the smallest Markdown artifact near the task or in a repository-consistent location.
4. Preserve the task's behavioral contract. Surface contradictions or missing requirements instead of silently redefining them.
5. Capture enough design detail for a reviewer to challenge how the system will satisfy the task.
6. Re-read the result for assumptions that exist only in chat and for code-level detail that does not carry a durable decision.

Do not require a task spec, workflow, docs directory, tracker, branch, plan, or review ceremony. A technical design may share a file with a task specification when repository practice prefers one artifact; keep their sections and ownership distinct.

## Design at the durable level

Include only the material parts of:

- current technical context and constraints;
- proposed architecture or approach;
- module responsibilities, interfaces, seams, and integration contracts;
- data model, state transitions, control flow, or event flow;
- failure, concurrency, consistency, security, privacy, performance, and operational behavior;
- technical alternatives and rationale;
- verification seams and observability needed to prove the design;
- unresolved technical decisions and their impact.

Prefer stable module, interface, contract, and data concepts over file-by-file instructions. Mention an existing path only when it locates an important owner; do not prescribe private functions, line edits, complete code, commit steps, or mechanical test cases.

Use pseudocode, a state table, or a compact schema only when it expresses a non-trivial algorithm, protocol, invariant, or transition more precisely than prose. Keep it decision-rich rather than executable.

Keep delivery ordering out unless it is part of the technical invariant. When sequencing, migration, compatibility, rollout, or rollback risk is material, leave the design stable and use `implementation-plan` separately.

Use [references/technical-design-template.md](references/technical-design-template.md) only when no stronger local pattern exists.

## Durable decision boundaries

Keep task-level choices in the technical design even when they may later qualify for an ADR. If a choice is hard to reverse, surprising without context, and based on genuine alternatives, surface it as an ADR candidate without making an ADR or another skill a prerequisite.

## Companion skills

Use `codebase-design` for module, interface, and seam reasoning, `research` for external technical constraints, and `grilling` for consequential unresolved choices when installed. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`. They are optional and do not own the design artifact.
