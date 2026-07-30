---
name: milestone-workflow
description: Govern opt-in, milestone-managed engineering delivery across tasks and sessions. Use when the user wants persistent global coordination for milestone outcomes, exit criteria, task placement, discovered work, progress recovery, or milestone closure while retaining Waypoint's atomic skills for task-level work.
---

# Milestone Workflow

Maintain the durable global view for users who explicitly choose milestone-managed delivery.

## Recover state

1. Read repository instructions, the current request, and existing milestone, roadmap, task, backlog, and issue artifacts.
2. Follow the repository's existing system. Do not require `docs/`, local task files, one active milestone, or a fixed tracker.
3. If milestone management was requested but no artifact exists, propose the smallest durable milestone artifact. Use [references/milestone-artifact.md](references/milestone-artifact.md) only when no stronger convention exists.
4. Recover open and completed milestones, outcomes, exit criteria, the current focus, task state, discovered work, future directions, and completion evidence.
5. Update global milestone state whenever task-level results would otherwise remain only in chat.

This workflow owns milestone governance. It does not replace the atomic skill that owns a task-level artifact or implementation.

## Plan and place work

1. Define a Milestone by selected candidate outcomes, a user-confirmed approximate task count, and observable exit criteria. Treat a timebox, deadline, or release window as an optional user or repository constraint.
2. For a new Milestone, send completed delivery, product evidence, Future Directions, the full backlog, and the user's boundary to `roadmap-planning`. For an existing Milestone, send its outcomes, exit criteria, completed and active tasks, dependencies, and changed evidence.
3. Require the planning result to account for candidate scoring, atomic task boundaries, selected and remaining backlog ownership, complete exit-criterion coverage, dependencies, the ready set, and genuine cross-task integration gaps. The scoring and task-shaping rules belong to `roadmap-planning`.
4. Reconcile that result into the durable Milestone and backlog artifacts. Keep task placement above task-local behavior, technical design, and implementation sequencing.
5. Select current focus after the known delivery boundary has coverage. Allow the map to evolve when new evidence changes it, and preserve valid completed work.

Parallel Milestones remain available when repository practice and delivery reality support them. Concrete deferred work stays in an active backlog or tracker; broader uncertainty stays under Future Directions. Numeric names, confirmation flags, modules, and a fixed Milestone sequence remain optional repository choices.

This step is complete when the Milestone artifact durably records its selected outcomes and rationale, task-count boundary, exit criteria, atomic task map, dependencies, ready set, backlog transfers or remainders, and explicit coverage gaps.

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

Keep a compact current-focus pointer when work spans sessions: the selected milestone, selected task or slice, next atomic waypoint, and blocker when present. This is recovery context, not a required tracker state or a claim that only one milestone may be active.

## Record discovered work

Compare each finding with the selected task's accepted scope before recording it globally:

- If fixing the finding is necessary to satisfy the current task's acceptance or the correctness of its supplied scope, record it in that task's artifact or state and keep it in the current task. Fix and verify it before completing the task, or mark the task blocked; do not defer it merely because the correction is difficult. Escalate it to `Discovered work` only if it remains unresolved at handoff or changes a Milestone-level boundary.
- If it exceeds the current task, exposes a systemic or cross-task concern, needs separate work, or belongs to another current or future task, append it to the active Milestone's `Discovered work` before routing it elsewhere.
- If the boundary or placement is uncertain, record it as `untriaged` rather than silently expanding the task or assuming another task will cover it.

Use `Discovered work` only for durable findings that affect correctness, exit criteria, compatibility, migration, operations, or future capability. Do not use it as a debugging diary. Keep the source entry after creating or linking its destination.

When routing a finding to an existing task, verify that task's durable acceptance, scope, or state explicitly owns it. A task link or similar title is not enough. Keep the finding `untriaged` or `current milestone` until that ownership is explicit.

Capture:

- finding;
- impact;
- source task or verification;
- disposition;
- destination when routed elsewhere;
- resolution evidence, reconsideration signal, or rationale when the disposition closes or durably places the finding.

Use these adaptive dispositions:

- `untriaged`;
- `current milestone`;
- `resolved`;
- `later milestone`;
- `backlog`;
- `future question`;
- `accepted limitation`;
- `discarded`.

Do not expand current scope silently. Ask when classifying a finding would change product intent, exit criteria, or a consequential delivery boundary.

## Retrieve backlog work

Review backlog candidates when selecting or planning a Milestone, when a reconsideration signal is observed, when new evidence changes value, risk, or dependencies, or when the user requests backlog work.

- At next-Milestone selection, scan every backlog item for changed evidence, completion, duplication, or obsolescence. Rescore changed candidates, sort by current score when the local format supports it, and expand only likely selections to atomic task boundaries.
- To select an item, first make a destination Milestone, task, or slice explicitly own its outcome through scope or acceptance. Update its source discovered-work entry when one exists, then remove the backlog entry.
- When an item is already resolved, first preserve its evidence in a completed task, issue, PR, commit, or source discovered-work entry, then remove the backlog entry.
- When another durable item owns it or a decision makes it obsolete, preserve that owner or rationale at the source when useful, then remove the backlog entry.
- When nothing changed, leave the backlog entry untouched. Add no review date, retained disposition, or review history.

Never remove an item before its destination, evidence, owner, or rationale is durable. Backlog contains only unresolved work that no other active artifact owns; completed tasks and source discovered-work entries carry history.

## Close a milestone

Audit every discovered-work entry individually before closure:

- change completed current-Milestone work to `resolved` and record its evidence;
- verify that a finding assigned to another current-Milestone task is explicitly owned there and has completion evidence before resolving it;
- link `later milestone` and `backlog` items to a durable destination;
- preserve a `future question` with its uncertainty and reconsideration signal;
- record the accepted consequence for an `accepted limitation`;
- give a concrete reason for `discarded`.

Close only when:

- exit criteria are satisfied;
- required tasks are complete;
- completion evidence is durable;
- every discovered item has a disposition;
- no `current milestone` finding remains unresolved.

Follow-up work elsewhere does not block closure once its destination is durable. An `untriaged` item, unresolved current-milestone item, missing destination, or missing closure rationale does.

Closing validates any backlog entries created from this Milestone but does not append backlog review history or rewrite unchanged older items.

At closure, send backlog items affected by completed delivery or discovered evidence to `roadmap-planning` for reconciliation and rescoring. Closing does not automatically create the next Milestone; continue into selection only when the user asks or explicitly agrees.

## Handle urgent work

Do not silently reorder an active Milestone when a newly discovered item receives a high score.

- If the finding is required for the current task's acceptance or correctness, keep it in that task.
- Otherwise record it durably and discuss whether to append it to the Milestone tail, leave it in backlog, or run an independent urgent delivery line.
- Tail insertion requires user agreement, formally expands Milestone scope, and blocks closure until the added task is complete.
- An independent urgent delivery line does not require Milestone membership. Select branch or worktree isolation adaptively through `task-execution-simple`; this workflow does not impose Git policy.
- Reconcile the urgent result and discoveries back into Milestone and backlog state without discarding stable active work.

Closing a milestone updates delivery state and does not itself require destructive confirmation. If closing also proposes merge, branch/worktree deletion, or discard, keep those as separate explicit gates.

Freeze a completed milestone's scope. Permit factual corrections and evidence links, but route new work to an open milestone, backlog, or future question instead of silently reopening it.

## Boundaries

Do not impose bootstrap, fixed review pauses, mandatory commits, branch policy, a single current milestone, or serial milestone execution. Do not write task specs, technical designs, implementation plans, or code in place of their atomic owners.
