# Backlog Routing

Read this reference when selecting, retrieving, resolving, or urgently inserting backlog work.

## Retrieve or resolve work

Review candidates during Milestone selection, when a reconsideration signal occurs, when evidence changes value, risk, or dependencies, or when the user requests backlog work.

1. Scan every backlog item for changed evidence, completion, duplication, or obsolescence. Rescore changed candidates through `roadmap-planning`; leave unchanged scores and entries untouched.
2. Before selecting an item, make a destination Milestone, task, or slice durably own its outcome, update any source Discovered Work disposition, then remove the backlog entry.
3. Before removing already resolved or obsolete work, preserve its evidence, owner, or rationale in a durable task, issue, PR, commit, or source Discovered Work disposition.

Retrieval is complete when selected or resolved entries have durable destinations and are removed, while unchanged entries remain byte-for-byte free of review history.

## Place urgent work

Keep a finding required for the current task's Acceptance or correctness in that task. For other urgent work, preserve it durably and ask the user to choose among:

- append a new task to the Milestone tail, expanding its closure boundary;
- leave it in backlog;
- run an independently isolated urgent delivery line.

Tail insertion requires user agreement. An independent delivery line chooses branch or worktree isolation adaptively through `task-execution-simple`. Reconcile the result into Milestone and backlog state without discarding stable active work.

Urgent placement is complete when the chosen destination owns the work and the active Milestone's existing order has not been silently rewritten.
