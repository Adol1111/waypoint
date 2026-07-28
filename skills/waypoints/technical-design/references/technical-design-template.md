# Technical Design Template

Use the smallest subset that makes review-critical implementation choices durable.

```md
# <Task> Technical Design

## Context and constraints

<Current technical facts and externally imposed constraints.>

## Proposed design

<Architecture or approach and how it satisfies the behavioral specification.>

## Responsibilities and interfaces

- <Module, interface, seam, or integration contract>

## Data and state flow

<Data ownership, schema concepts, states, transitions, control flow, or events when relevant.>

## Failure and quality behavior

<Concurrency, consistency, security, privacy, performance, operations, or recovery when relevant.>

## Decisions and tradeoffs

- <Choice, genuine alternatives, and rationale>

## Algorithm or protocol

<Pseudocode, state table, or compact schema only when prose is not precise enough.>

## Verification seams

- <Interface, observation, or evidence that can prove the design>

## Open technical decisions

- <Unresolved choice, impact, and latest useful decision point>
```

Omit unused sections. Do not expand the template into file-by-file edits, complete code, commit steps, or an implementation sequence.
