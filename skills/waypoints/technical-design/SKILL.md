---
name: technical-design
description: Decide and document review-critical technical choices for one explicitly targeted or unambiguously current Feature or child Task when architecture, ownership, data, state, algorithm, concurrency, security, performance, or verification has materially different plausible approaches or a non-obvious invariant. Straightforward work needs no design artifact.
---

# Technical Design

Make consequential implementation choices reviewable without turning the design into a coding recipe.

## Decide whether design is warranted

First identify the concrete technical questions still unresolved after reading the specification and repository conventions. A question warrants design only when it cannot safely be left to implementation-time judgment and it involves:

- architecture, module responsibilities, interfaces, or seams;
- data ownership, persistence shape, state transitions, or event flow;
- a non-trivial algorithm or protocol;
- concurrency, consistency, security, privacy, performance, or operational behavior;
- integration contracts or testing seams that shape the solution;
- genuine technical alternatives with different long-term consequences.

A question is material when plausible approaches have meaningfully different consequences, or when the choice establishes a non-obvious invariant, ownership boundary, data contract, lifecycle, concurrency model, migration rule, security boundary, or operational constraint. Feature size, a missing design file, or merely touching data, state, security, or multiple modules is not sufficient evidence.

Create a design artifact only after at least one concrete question passes this materiality gate. If the specification and repository practice already determine the approach and only mechanically derivable implementation remains, report that a concise approach preview is sufficient and stop. Create neither a design artifact nor a skipped-design marker. Do not begin implementation unless the user's current request separately assigns that exact Feature or Task.

## Work independently

1. Resolve one exact Feature or Task before designing. Prefer an ID, link, path, or artifact from the request. Otherwise read `.waypoint/local.yaml` and filter active owned Features or assigned Tasks by `actor_id`. Continue only when exactly one candidate remains; otherwise ask. Never fall back to another actor's work, queue order, recency, Git history, or the current branch.
2. Read repository instructions, the resolved Feature or Task contract, relevant code and tests, existing architecture and decision records, and local design conventions.
3. Separate behavior already fixed by `feature-spec`, repository facts and conventions, mechanically derivable implementation, and concrete questions that still need technical judgment. Apply the materiality gate before creating or updating an artifact.
4. When at least one question passes, update an existing suitable design artifact or technical-design section when possible. Otherwise propose the smallest Markdown artifact beside its Feature or Task.
5. Preserve the Feature behavioral contract and child Task ownership. Surface contradictions or missing requirements instead of silently redefining them.
6. For each included area, make the technical question, chosen approach, rationale, and resulting invariant or consequence reviewable; include alternatives only when they were genuine.
7. Finish only when every section adds a review-critical implementation choice beyond the Feature/Task contract and repository conventions. Remove assumptions that exist only in chat, repeated requirements, routine mechanics, and code-level detail that carries no durable decision.
8. Add a design Reference to `feature.md` or the owning `task.md` only after the design artifact exists. Link only the actual repository-native filename and do not create placeholder References.

When several executors may implement one Feature, make shared ownership, interfaces, schemas, lifecycle rules, and verification seams stable enough for `task-planning` to split work without letting parallel Tasks redefine them. If the unresolved choice affects observable behavior, return it to `feature-spec` instead of designing around it.

Do not require a separate Feature spec for an unsplit Feature whose behavioral contract is already reviewable, or require a workflow, docs directory, tracker, branch, plan, or review ceremony. A technical design may share a file with a Feature specification when repository practice prefers one artifact; keep their sections and ownership distinct.

## Design at the durable level

Document the decision, not the derivation. Reference the relevant behavioral requirement instead of restating it. When an unresolved choice would change user- or operator-visible behavior, compatibility, or product policy, return it to `feature-spec` before designing its mechanism.

Include only the material parts of:

- current technical context and constraints;
- proposed architecture or approach;
- module responsibilities, interfaces, seams, and integration contracts;
- data model, ownership, persisted shape, lifecycle, state transitions, or event flow;
- execution model and side-effect boundaries, such as request-time, background, scheduled, or event-driven work;
- failure mechanisms, concurrency, atomicity, consistency, security, privacy, performance, and operations;
- technical alternatives and rationale;
- verification seams and observability needed to prove the design;
- unresolved technical decisions and their impact.

Choose the representation that makes each material decision easiest to review. Do not omit concrete structure merely to keep the artifact short:

- For relational persistence changes, show the affected tables, columns and logical types, primary and foreign keys, nullability or defaults, uniqueness and other constraints, indexes justified by access paths, ownership, and migration or compatibility implications. Use a compact table or DDL-like sketch; do not invent physical details the decision does not require.
- For document, event, cache, or wire formats, show the durable shape, identity and versioning rules, producer and consumer ownership, compatibility expectations, and representative payloads when they clarify the contract.
- For lifecycle-heavy behavior, use a state table or state diagram that names valid transitions, guards, side effects, terminal states, and invalid transitions.
- For branching business or system logic, use a flowchart when prose would hide decisions, loops, or failure paths.
- For interaction across actors, modules, services, transactions, queues, or time boundaries, use a sequence diagram that exposes ordering, sync versus async calls, retries, acknowledgements, timeouts, and failure ownership when material.
- For architecture or deployment boundaries, use a component or container diagram when ownership, direction of dependency, trust boundary, or data movement is otherwise hard to see.

Prefer repository-native text, Markdown tables, and Mermaid diagrams when supported so the source remains diffable and reviewable. Give every diagram a short title, use the same names as the surrounding design, and explain the decision or invariant it proves; a diagram is not decoration and does not replace necessary constraints. If the repository cannot render Mermaid, use its established diagram format or a compact text diagram.

Leave routine parsing, validation, normalization, mapping, and ordinary control flow to implementation. Record them only when their semantics define a durable contract or affect identity, persistence, invalidation, compatibility, security, or another material invariant. Describe that invariant and chosen representation, not the obvious processing steps.

Prefer stable module, interface, contract, and data concepts over file-by-file instructions. Mention an existing path only when it locates an important owner; do not prescribe private functions, line edits, complete code, commit steps, or mechanical test cases.

Use pseudocode only when it expresses a non-trivial algorithm or protocol more precisely than prose. Keep it decision-rich rather than executable. Express a single linear sequence as concise prose or a short ordered list.

Keep delivery ordering out unless it is part of the technical invariant. When sequencing, migration, compatibility, rollout, or rollback risk is material, leave the design stable and use `implementation-plan` separately.

Use [references/technical-design-template.md](references/technical-design-template.md) only when no stronger local pattern exists.

Finish after the material choices are reviewable. Design approval authorizes this artifact only; do not decompose Tasks, write an implementation plan, or modify production code unless the user's current request explicitly includes that separate planning outcome. Planning never authorizes implementation.

## Durable decision boundaries

Keep Feature- or Task-level implementation choices in the technical design even when they may later qualify for an ADR. If a choice is hard to reverse, surprising without context, and based on genuine alternatives, surface it as an ADR candidate without making an ADR or another skill a prerequisite.

## Companion skills

Use `codebase-design` for module, interface, and seam reasoning, `research` for external technical constraints, and `grilling` for consequential unresolved choices when installed. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`. They are optional and do not own the design artifact.
