# Feature Task Plan Template

Use only when no stronger repository convention exists. Keep status out of this durable graph; render current status into `feature.md` from the configured tracker.

## Coordinating graph

```md
# <Feature> Task Plan

Feature: <stable Feature ID and link>
Owner: <stable Feature owner>

## Source contracts

- Behavior: <Feature spec>
- Technical design: <link only when one exists>

## Tasks

- [<Task>](tasks/<task>/task.md) — <bounded outcome>

## Dependency graph

<Mermaid graph only when at least one real blocking edge exists.>

## Integration proof

<Only proof that no child Task can provide locally.>
```

List Tasks for reading convenience only. Omit dependency and integration sections when their triggers do not exist.

## Child Task contract

```md
# <Task>

Task ID: <feature-id/task-id>
Feature: <link>
Tracker: <link when external tracking exists>

## Outcome

<Bounded result that can be assigned, retained, and integrated independently.>

## Scope

- Includes: <owned behavior or responsibility>
- Excludes: <important adjacent work>

## Acceptance

- [ ] <Observable condition this Task verifies independently>

## Ownership and contracts

- Owns: <stable module, interface, data, or behavior surface>
- Consumes: <shared contract, when relevant>
- Provides: <shared contract, when relevant>
- Must not change: <cross-Task invariant, when relevant>

## Structural dependencies

- Start: <hard prerequisite Task in this Feature>
- Completion: <integration or verification gate>

## Verification

<Task-local proof required before MR acceptance.>

## References

- <Feature spec, design, plan, ADR, issue, or source artifact>
```

Keep live Status, Assignee, Executor, MR, and blocker state in the configured tracker. Without an external tracker, `local-work-tracker` owns those fields. Omit unused optional sections. Task Acceptance remains authoritative here; do not create a second behavioral specification for the child Task.
