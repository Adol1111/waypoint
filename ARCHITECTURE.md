# Waypoint Architecture

## Repository layout

The published skill catalog uses one shallow responsibility layer:

```text
skills/
├── waypoints/   # independently useful engineering outcomes
├── workflows/   # explicitly selected coordination modes
└── setup/       # opt-in repository scaffolding
```

Skill names remain globally unique and installation is by skill name, not category. The categories explain ownership without creating workflow prerequisites.

## Atomic-skill contract

Each atomic skill owns one durable engineering outcome and must be usable directly. It:

1. reads repository instructions and relevant existing artifacts;
2. follows local naming, location, language, and formatting practice;
3. updates an existing suitable artifact when possible;
4. otherwise proposes the smallest useful local Markdown artifact;
5. leaves review-critical facts in that artifact rather than only in chat;
6. reports evidence and unresolved boundaries honestly.

An atomic skill cannot require another local skill, the optional coordinator, a fixed docs tree, a tracker, a workflow stage, a branch convention, or a commit/review ceremony. Companion skills may improve the work but remain optional.

## Optional workflows

Users may invoke atomic skills directly or choose one of two workflows:

- `waypoint-workflow` is a read-only recommendation layer for lightweight, non-Milestone work. It searches by meaning rather than fixed paths, reads only artifacts that exist, selects exactly one atomic skill, and stops.
- `milestone-workflow` is an opt-in, stateful global coordinator for multi-task delivery. It owns Milestone outcomes, exit criteria, task placement and status, discovered-work reconciliation, future directions, completion evidence, and closure. It delegates task-local recovery, artifacts, and implementation to their atomic owners.

Choosing `milestone-workflow` does not make its lifecycle mandatory for other users. Atomic skills remain independently invocable.

`docs-workflow-bootstrap` is also optional. Before creating task docs, it uses an explicit user preference to choose a flat standalone convention or a Milestone-managed convention. If that preference is missing and the distinction matters, it asks before writing either structure.

## Artifact ownership

| Artifact or action | Owner |
| --- | --- |
| Glossary entry and qualifying ADR | `domain-context` |
| Optional candidate enrichment, backlog scoring, Milestone task-batch selection, atomic decomposition, task planning handoff, and planning-level coverage | `roadmap-planning` |
| Reviewable task behavior and requirements; task Acceptance derived from them | `task-spec` |
| Review-critical architecture, interfaces, data and state models, algorithms, quality attributes, and verification seams | `technical-design` |
| Risk-driven execution order and rollback | `implementation-plan` |
| Acceptance, status, blockers, recovery checkpoint, final verification, and closing safety | `task-state` |
| Code changes, execution verification, adaptive isolation, and task-scoped Git checkpoints | `task-execution-simple` |
| Optional docs scaffold only | `docs-workflow-bootstrap` |
| One next-skill recommendation only | `waypoint-workflow` |
| Milestone definition, global task placement and materialization, state, discoveries, evidence, and closure | `milestone-workflow` |

Templates live only with the skill that owns the artifact or scaffold. They are fallbacks when the repository has no stronger convention, not schemas to enforce. The bootstrap skill owns its two scaffold conventions but does not generate substantive artifacts for other skills. `milestone-workflow` owns the fallback Milestone artifact shape and its global state.

Artifact ownership is semantic rather than filename-prescriptive. `task-spec` normally maintains a separate behavioral specification and the owning task's canonical Acceptance; `technical-design` may use `design.md`, `technical-design.md`, or another repository-native name. Behavioral requirements remain owned by `task-spec`; internal architecture and implementation choices remain owned by `technical-design`. `implementation-plan` consumes either form only when execution order itself creates risk. A task References section links only artifacts that already exist.

When a repository uses local Milestone task folders, confirming a Milestone materializes every selected atomic task as a non-empty planning handoff. `roadmap-planning` owns that handoff, while `milestone-workflow` creates or links the repository-native task artifact and keeps the Milestone index as the global map. Its ordered task list contains links and status only; list order suggests execution sequence, while an optional Mermaid graph carries actual cross-task dependencies. When development begins, `task-spec` creates or updates a separate specification, writes canonical Acceptance to `task.md`, and removes superseded planning fields. Technical design and implementation plans remain threshold-driven.

## Milestone governance

A Milestone is optional and bounded by selected candidate outcomes, a user-confirmed approximate atomic-task count, and observable exit criteria. A user or repository may add a timebox, deadline, or release boundary, but Waypoint does not invent one. The workflow does not require a functional theme, numeric names, one active Milestone, or serial execution.

Findings required to satisfy the current task stay in that task's acceptance, state, and correction loop. A finding explicitly owned by another current task goes directly there. Only durable work the Milestone cannot handle now, or whose owner remains uncertain, enters Discovered Work. At closure, resolved current-task findings disappear; routed work retains only its disposition and destination link, while discarded work also retains a reason.

Backlog is an active queue of candidate outcomes. Waypoint follows a repository scoring model or recommends a holistic `0–10` score with one evidence-based rationale. Candidate enrichment is optional and user-directed; vague ideas remain Future Directions. Full-backlog scans remove stale work, while only changed evidence rewrites scores. Leading candidates are expanded at planning granularity into atomic tasks, and one candidate may consume several places in the confirmed batch. A task is the smallest meaningful one-spec engineering delivery that includes its implementation, necessary docs, verification, and review correction; it may be a non-user-visible but safe and verifiable stage. Milestone tasks carry list order and real dependencies, not scores.

Selection or durable resolution removes a whole candidate. Partial selection rewrites and rescores the remaining outcome. Closure requires satisfied exit criteria, completed required tasks, any necessary cross-task proof, and a destination or discard reason for remaining Discovered Work; it reconciles affected backlog scores but does not automatically create another Milestone. Follow-up work already placed elsewhere does not block closure.

Completed Milestone scope is frozen and compact: it retains outcome, necessary global constraints, selection, checked exit criteria, completed task links, and final discovered-work dispositions. Dependency graphs, resolved decisions, process notes, and implementation summaries do not become history. Factual corrections and cross-task evidence links remain allowed; new scope goes elsewhere.

## Safety boundaries

Ordinary, reversible progress uses adaptive judgment based on repository practice, task risk, and user direction. Waypoint does not require confirmation for routine edits, questions, tests, commits, reviews, or isolation when those actions are already within the user's request.

Optional branch and commit policy means there is no prescribed sequence, not that stable work remains indefinitely uncommitted. Task execution chooses isolation from collision and recovery risk, commits cohesive verified work before advancing when permitted, and reports an explicit reason when a safe checkpoint is unavailable.

Three closing operations require explicit confirmation:

- merging isolated work;
- deleting a branch or worktree;
- discarding commits or uncommitted work.

Confirmation is action- and target-specific. Merge approval does not authorize later deletion, and generic forward-motion language does not authorize any of the three. Skills inspect version-control state before presenting a closing action and prefer recoverable cleanup where practical.

## Deliberate separation from the legacy workflow

The legacy repository supplied useful lessons about durable docs, task-local specs, embedded technical decisions, optional plans, Milestone closure, discovered-work routing, verification, and closing safety. Waypoint retains the valuable information but gives behavioral specification and technical design separate semantic owners. It retains Milestone capabilities only inside the user-selected `milestone-workflow` and removes the fixed stage chain, required docs entry points, roadmap confirmation flags, tracker-specific transitions, mandatory review pauses, default commit checkpoints, default task branches, prescribed cross-Milestone serialization, and fixed closing-choice lifecycle. Adaptive isolation and cohesive Git checkpoints remain available when repository state and task risk justify them.
