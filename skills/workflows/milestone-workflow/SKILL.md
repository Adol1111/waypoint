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

- Define a milestone by a meaningful delivery outcome, release or migration boundary, or shared exit criteria.
- Use `roadmap-planning` for independently verifiable slices when useful, then place those slices or tasks in the milestone artifact.
- Keep task placement above task-local behavior, technical design, and implementation sequencing. Use their atomic owners when that detail is needed.
- Allow parallel milestones when repository practice and delivery reality support them.
- Keep concrete deferred work in an existing backlog or tracker. Preserve broader future questions without inventing tasks.
- Distinguish task-shaped backlog items from goal-shaped future directions. Give each deferred item a reconsideration signal rather than expanding it into a speculative tree.
- Do not require numeric milestone names, `Roadmap confirmed` flags, modules, or a fixed milestone sequence.

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

Revisit unresolved discoveries, backlog candidates, and future directions when selecting a new milestone and when closing one. Promote an item only when its outcome and placement are concrete enough; otherwise preserve its uncertainty.

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

Closing a milestone updates delivery state and does not itself require destructive confirmation. If closing also proposes merge, branch/worktree deletion, or discard, keep those as separate explicit gates.

Freeze a completed milestone's scope. Permit factual corrections and evidence links, but route new work to an open milestone, backlog, or future question instead of silently reopening it.

## Boundaries

Do not impose bootstrap, fixed review pauses, mandatory commits, branch policy, a single current milestone, or serial milestone execution. Do not write task specs, technical designs, implementation plans, or code in place of their atomic owners.
