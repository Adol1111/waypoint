# Technical Design Template

Use the smallest subset that makes review-critical implementation choices durable.

```md
# <Task> Technical Design

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

## Data, storage, and lifecycle

<Data ownership, persisted shape, identity, lifecycle, state transitions, or events when a material choice is involved.>

## Execution model and side effects

<Request-time, background, scheduled, or event-driven execution; transaction, atomicity, concurrency, and side-effect boundaries.>

## Failure and quality mechanisms

<Mechanisms for consistency, security, privacy, performance, operations, or recovery. Reference observable requirements rather than repeating them.>

## Algorithm or protocol

<Pseudocode, state table, or compact schema only when prose is not precise enough.>

## Verification seams

- <Technical seam or observation that can prove the chosen mechanism without repeating the specification's completion cases>

## Open technical decisions

- <Unresolved implementation choice, impact, and latest useful decision point; return observable behavior questions to the specification>
```

Omit unused sections. Every included section must add a review-critical implementation choice beyond the specification and repository conventions. Leave mechanically derivable parsing, validation, normalization, mapping, and ordinary control flow to implementation. Do not expand the template into file-by-file edits, complete code, commit steps, or an implementation sequence.
