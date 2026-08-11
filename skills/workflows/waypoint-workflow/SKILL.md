---
name: waypoint-workflow
description: Read repository evidence and recommend exactly one next standalone Waypoint or installed Matt Pocock skill for shared Milestone, Feature, Task, tracking, handoff, or implementation work. Use only when the user asks what to do next; never invoke the recommendation, mutate state, or chain stages.
---

# Waypoint Workflow

Act as a read-only navigator, never an orchestrator.

## Inspect current evidence

Read repository instructions, configured tracker state, requirement pool, shared Milestone, selected Feature, child Task, relevant artifacts, blockers, assignment, branch/worktree, and current request. Do not create or update any artifact or operational state.

## Recommend exactly one next skill

Choose the capability closest to the user's requested outcome:

- shared Milestone selection, Feature ownership, requirement-pool priority, cross-Feature dependencies, or explicit replanning: `milestone-planning`;
- one Feature's durable observable behavior: `feature-spec`;
- a concrete review-critical architecture, ownership, data, interface, algorithm, security, performance, or verification choice: `technical-design`;
- one Feature's user-confirmed child Task DAG, ownership surfaces, blockers, contracts, and safe parallelism: `task-planning`;
- one already-bounded Feature or Task's durable execution strategy, migration, compatibility, rollback, or recoverable internal slices: `implementation-plan`;
- explicit user request for repository-local tracking setup or an exact state update, after confirming no external tracker exists: `local-work-tracker`;
- explicitly assigned implementation-ready Feature or Task: Matt Pocock's `implement` when installed;
- cross-window or cross-harness transfer: Matt Pocock's `handoff` when installed;
- qualifying terminology or durable architecture decision: `domain-context`;
- explicitly requested docs convention: `docs-workflow-bootstrap`.

Require a real trigger. A missing `spec.md`, `design.md`, `task-plan.md`, or `plan.md` is not a trigger by itself. A split Feature does require one shared behavioral contract, but a small unsplit Feature may keep it in `feature.md`.

Recommend implementation as immediately eligible only when the current request names an exact assigned Feature or Task, its blockers and Acceptance are clear, and no unresolved behavior, technical choice, shared contract, or execution-order risk blocks coding. When an exact Task is otherwise ready but unassigned, name Matt Pocock's `implement` only as the blocked next capability and report that the user or authorized Feature owner must explicitly assign it first. Do not substitute `local-work-tracker`, infer an assignee, or perform the assignment. `ready` alone is not assignment.

## Return and stop

Return exactly:

- current evidence;
- recommended skill;
- artifact or tracker state to reuse;
- why it is the smallest next durable outcome;
- any blocker that prevents that skill from completing.

Do not invoke the recommendation. Do not interpret `ok`, shared-understanding confirmation, planning approval, `continue`, or automatic tool approval as authorization for another waypoint, implementation, MR merge, branch/worktree deletion, or discard.
