# Technical Design Template

Use the smallest subset that makes review-critical implementation choices durable.

```md
# <Feature or Task> Technical Design

## Context and constraints

<Only the current technical facts and constraints that shape an implementation choice. Link to the behavioral specification instead of summarizing it.>

## Proposed technical design

<Architecture, ownership boundaries, and technical mechanism.>

## Technical decisions

### <Technical question>

- Choice: <selected implementation approach>
- Why: <material rationale>
- Alternatives: <genuine alternatives and why they were not selected; omit when none>
- Invariant or consequence: <durable effect of the choice>

## Responsibilities and interfaces

- <Module, interface, seam, or integration contract>

## Cross-Task contracts

- Owner: <single owner of the mutable contract>
- Consumers: <Tasks or modules that rely on it>
- Invariant: <what parallel work must not redefine>

## Data, storage, and lifecycle

<Data ownership, persisted shape, identity, lifecycle, state transitions, or events when a material choice is involved. For relational storage, include a compact schema covering logical types, keys, nullability/defaults, constraints, justified indexes, ownership, and migration/compatibility impact. For other durable formats, cover shape, versioning, producers, consumers, and compatibility.>

### Schema

<Markdown table, DDL-like sketch, or representative payload when concrete structure is needed. Omit otherwise.>

### State model

<State table or Mermaid state diagram for material transitions, guards, side effects, terminal states, and invalid transitions. Omit otherwise.>

## Execution model and side effects

<Request-time, background, scheduled, or event-driven execution; transaction, atomicity, concurrency, and side-effect boundaries.>

### Flow or interaction

<Use the smallest useful diagram: a flowchart for branching and failure paths; a sequence diagram for cross-actor/component ordering, async boundaries, retries, acknowledgements, or timeouts; a component diagram for ownership, dependency, trust, or data-movement boundaries. Prefer Mermaid when the repository supports it. Omit when prose is clearer.>

## Failure and quality mechanisms

<Mechanisms for consistency, security, privacy, performance, operations, or recovery. Reference observable requirements rather than repeating them.>

## Algorithm or protocol

<Pseudocode only when a non-trivial algorithm or protocol is not precise enough in prose.>

## Verification seams

- <Technical seam or observation that can prove the chosen mechanism without repeating the specification's completion cases>

## Open technical decisions

- <Unresolved implementation choice, impact, and latest useful decision point; return observable behavior questions to the specification>
```

Omit unused sections, including `Cross-Task contracts` when one executor owns the whole change. Every included section must add a review-critical implementation choice beyond the specification and repository conventions. Keep diagrams diffable, name them, use terminology consistent with the prose, and state the decision or invariant each one clarifies. Leave mechanically derivable parsing, validation, normalization, mapping, and ordinary control flow to implementation. Do not expand the template into file-by-file edits, complete code, commit steps, or an implementation sequence.
