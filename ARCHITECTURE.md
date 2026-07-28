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
- `milestone-workflow` is an opt-in, stateful global coordinator for multi-task delivery. It owns Milestone outcomes, exit criteria, current-focus recovery, task placement, discovered-work reconciliation, future directions, completion evidence, and closure. It delegates task-local artifacts and implementation to their atomic owners.

Choosing `milestone-workflow` does not make its lifecycle mandatory for other users. Atomic skills remain independently invocable.

`docs-workflow-bootstrap` is also optional. Before creating task docs, it uses an explicit user preference to choose a flat standalone convention or a Milestone-managed convention. If that preference is missing and the distinction matters, it asks before writing either structure.

## Artifact ownership

| Artifact or action | Owner |
| --- | --- |
| Glossary entry and qualifying ADR | `domain-context` |
| Goal decomposition and delivery slices | `roadmap-planning` |
| Reviewable task behavior, requirements, and proof | `task-spec` |
| Review-critical architecture, interfaces, data and state models, algorithms, quality attributes, and verification seams | `technical-design` |
| Risk-driven execution order and rollback | `implementation-plan` |
| Acceptance, status, blockers, evidence, closing state | `task-state` |
| Code changes and execution verification | `task-execution-simple` |
| Optional docs scaffold only | `docs-workflow-bootstrap` |
| One next-skill recommendation only | `waypoint-workflow` |
| Milestone definition, global placement, discoveries, evidence, and closure | `milestone-workflow` |

Templates live only with the skill that owns the artifact or scaffold. They are fallbacks when the repository has no stronger convention, not schemas to enforce. The bootstrap skill owns its two scaffold conventions but does not generate substantive artifacts for other skills. `milestone-workflow` owns the fallback Milestone artifact shape and its global state.

Artifact ownership is semantic rather than file-prescriptive. `task-spec` and `technical-design` may maintain separate sections in one task artifact when that matches repository practice, or use separate `spec.md` and `design.md` files. Behavioral requirements remain owned by `task-spec`; internal architecture and implementation choices remain owned by `technical-design`. `implementation-plan` consumes either form only when execution order itself creates risk.

## Milestone governance

A Milestone is optional and justified by a shared delivery outcome, release or migration boundary, or common exit criteria. The workflow does not require numeric names, one active Milestone, or serial execution.

Durable findings discovered during delivery remain in the active Milestone until classified as current work, later-Milestone work, backlog, a future question, an accepted limitation, or discarded. Concrete task-shaped deferrals go to a backlog; goal-shaped uncertainty remains a future direction until it has a meaningful promotion signal. Closure requires satisfied exit criteria, completion evidence, dispositions for every finding, and no unresolved current-Milestone work. Follow-up work already placed elsewhere does not block closure.

Completed Milestone scope is frozen. Factual corrections and evidence links remain allowed; new scope goes elsewhere.

## Safety boundaries

Ordinary, reversible progress uses adaptive judgment based on repository practice, task risk, and user direction. Waypoint does not require confirmation for routine edits, questions, tests, commits, reviews, or isolation when those actions are already within the user's request.

Three closing operations require explicit confirmation:

- merging isolated work;
- deleting a branch or worktree;
- discarding commits or uncommitted work.

Confirmation is action- and target-specific. Merge approval does not authorize later deletion, and generic forward-motion language does not authorize any of the three. Skills inspect version-control state before presenting a closing action and prefer recoverable cleanup where practical.

## Deliberate separation from the legacy workflow

The legacy repository supplied useful lessons about durable docs, task-local specs, embedded technical decisions, optional plans, Milestone closure, discovered-work routing, verification, and closing safety. Waypoint retains the valuable information but gives behavioral specification and technical design separate semantic owners. It retains Milestone capabilities only inside the user-selected `milestone-workflow` and removes the fixed stage chain, required docs entry points, roadmap confirmation flags, tracker-specific transitions, mandatory review pauses, default commit checkpoints, default task branches, prescribed cross-Milestone serialization, and fixed closing-choice lifecycle.
