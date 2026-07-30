# Milestone Planning Handoff

Read this reference only for new or existing Milestone planning.

## Planning result

Return or persist:

- selected candidate outcomes, scores, and rationale;
- supplied external constraints that still affect delivery;
- every exit criterion linked to its task owners;
- one planning handoff for every confirmed atomic task;
- start and completion dependencies and substantial cross-task integration needs;
- durable ownership for selected outcomes, partial remainders, and unchanged backlog work.

The coordinating Milestone artifact is a linked global map. It keeps outcome, global constraints, selection context, exit criteria, an ordered task link and status list, and an optional dependency graph. List order communicates the recommended execution sequence; the task handoffs and graph carry actual dependencies. Task-local planning facts and recovery state live once in the task artifact.

## Task planning handoff

Use the repository's task item or artifact. For a local Markdown convention:

```md
# <Task>

Status: planned
Milestone: <link>

## Outcome

<Bounded and verifiable stage result.>

## Planning boundary

- Includes: <coarse scope>
- Excludes: <important non-goals>

## Stage proof

<Success signal sufficient to justify the task boundary.>

## Dependencies

- Start: <hard prerequisite>
- Completion: <completion or verification gate>

## Open decisions

- <Task-local choice and whether specification or design owns it>
```

Omit `Dependencies` when none exist. Add `Why this task` only when a split slice, non-user-visible prerequisite, or otherwise non-obvious Milestone membership needs explanation. Omit `Open decisions` when none are already known.

The planning handoff is complete when every confirmed task has one non-empty durable owner and every included optional section contains real information. Later task-artifact evolution belongs to `task-spec`, `technical-design`, `implementation-plan`, and `task-state`.

## Compact dependency view

Keep the task handoff's dependencies authoritative. When at least one cross-task start or completion dependency exists, add a Mermaid graph to the Milestone and label completion or verification gates distinctly. Omit the dependency graph when every task is independent.

## Coverage representation

Link task owners directly from each exit criterion. Do not add a separate coverage table. If a criterion has no owner, add or reshape a task, adjust the criterion, or preserve a genuinely global unresolved choice under Open Decisions.
