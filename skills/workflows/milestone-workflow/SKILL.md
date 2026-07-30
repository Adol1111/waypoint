---
name: milestone-workflow
description: Coordinate Milestone-managed delivery when the user wants to plan, continue, or close a multi-task Milestone, or route its backlog and discovered work.
---

# Milestone Workflow

Maintain the durable global view for users who explicitly choose milestone-managed delivery.

## Recover state

1. Read repository instructions, the current request, and existing milestone, roadmap, task, backlog, and issue artifacts.
2. Follow the repository's existing system. Do not require `docs/`, local task files, one active milestone, or a fixed tracker.
3. If milestone management was requested but no artifact exists, propose the smallest durable milestone artifact. Use [references/milestone-artifact.md](references/milestone-artifact.md) only when no stronger convention exists.
4. Recover open and completed milestones, outcomes, exit criteria, task state, unresolved discovered work, and any cross-task completion evidence.
5. Update global milestone state whenever task-level results would otherwise remain only in chat.

This workflow owns milestone governance. It does not replace the atomic skill that owns a task-level artifact or implementation.

## Plan and place work

1. Define a Milestone by selected candidate outcomes, a user-confirmed batch of tasks, and observable exit criteria. Treat a timebox, deadline, or release window as an optional user or repository constraint.
2. For a new Milestone, send completed delivery, product evidence, Future Directions, the full backlog, and the user's boundary to `roadmap-planning`. For an existing Milestone, send its outcomes, exit criteria, completed and active tasks, dependencies, and changed evidence.
3. Require the planning result to account for candidate scoring, atomic task boundaries, selected and remaining backlog ownership, exit-criterion ownership, real dependencies, and genuine cross-task integration gaps. The scoring and task-shaping rules belong to `roadmap-planning`.
4. Reconcile that result into the durable Milestone, task, and backlog artifacts. When the repository uses local Milestone task folders, materialize each `roadmap-planning` handoff as one non-empty `task.md` or repository-native equivalent and link it from the Milestone index.
5. Update task status after the known delivery boundary has coverage. Allow the map to evolve when new evidence changes it, and preserve valid completed work.

Parallel Milestones remain available when repository practice and delivery reality support them. Concrete deferred work stays in an active backlog or tracker; broader uncertainty stays under Future Directions. Numeric names, confirmation flags, modules, and a fixed Milestone sequence remain optional repository choices.

This step is complete when the Milestone artifact durably records its selected outcomes and rationale, exit criteria with task links, linked atomic task map, real dependencies, and backlog transfers or remainders. Every confirmed local task has a non-empty durable artifact, and each task-local fact has one authoritative home.

## Coordinate the next waypoint

Choose the next action from current evidence rather than a mandatory stage chain:

- shape milestone boundaries or slices with `roadmap-planning`;
- make one selected task reviewable with `task-spec`;
- make review-critical implementation choices durable with `technical-design`;
- plan real execution risk with `implementation-plan`;
- implement scoped work with `task-execution-simple`;
- update one task's acceptance, status, blocker, or evidence with `task-state`;
- preserve qualifying terminology or decisions with `domain-context`.

When continuing task-level work, carry the milestone, selected task, relevant exit criteria, and unresolved discovered work into the atomic skill. Afterward, reconcile its durable result and new discoveries back into milestone state.

Before selecting another task, inspect whether the current task has stable uncommitted changes. When routine commits are permitted, return completed uncommitted work to `task-execution-simple` for a cohesive Git checkpoint. Otherwise record the user or repository no-commit policy, or the concrete mixed-work reason that prevents safe separation; do not advance silently.

Use task status in the Milestone index as its global recovery signal. Do not add Current Focus or another global cursor. When work pauses, keep only otherwise unrecoverable remaining work, next action, blocker, and non-obvious working state in the relevant task artifact through `task-state`. Parallel work appears as multiple `in-progress` tasks.

## Route lifecycle branches

- For a finding that may outlive its current task, an unresolved-finding handoff, or Milestone closure, read and apply [references/discovered-work-and-closure.md](references/discovered-work-and-closure.md).
- For Milestone selection, backlog retrieval or resolution, or urgent insertion, read and apply [references/backlog-routing.md](references/backlog-routing.md).
- To create, update, or complete the global artifact, read and apply [references/milestone-artifact.md](references/milestone-artifact.md).

Closing is complete only when exit criteria and required tasks are complete, any necessary cross-task proof is durable, the Discovered Work audit passes, and the artifact is compacted. Reconcile affected backlog work through `roadmap-planning`; begin another Milestone only with user direction.

Milestone closure itself is non-destructive. Keep merge, branch/worktree deletion, and discard as separate target-specific confirmation gates.

## Boundaries

Do not impose bootstrap, fixed review pauses, mandatory commits, branch policy, a single current milestone, or serial milestone execution. Do not write task specs, technical designs, implementation plans, or code in place of their atomic owners.
