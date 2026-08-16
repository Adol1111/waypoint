# Waypoint Architecture

## Purpose

Waypoint preserves the engineering contracts needed when planning and execution move between people, agent windows, models, and harnesses. It complements Matt Pocock's general-purpose skills instead of replacing them.

## Collaboration hierarchy

```text
Requirement pool
  └── Shared Milestone
      └── Feature — one stable owner
          └── Task — one assignee, optional temporary executor
```

- A requirement-pool entry is a lightweight candidate outcome.
- A Milestone is a shared, normally frozen Feature batch with one coordinator and potentially many Feature owners. It is not a serial queue or Git boundary.
- A Feature is a complete behavioral and final-acceptance boundary with one stable owner.
- A Task is an optional Feature-owned execution unit used only when work spans people, windows, harnesses, or sessions. Small Features remain unsplit.

Cross-Feature dependencies bind to another Feature or its public contract. A Feature's internal Task graph never becomes another Feature's API.

## Repository layout

```text
skills/
├── waypoints/   # independently useful durable engineering outcomes
├── workflows/   # explicitly invoked read-only navigation
├── setup/       # opt-in repository scaffolding or local tracking
└── deprecated/  # replacement and uninstall guidance only
```

Every atomic skill remains usable without a workflow, bootstrap, fixed docs tree, tracker, branch policy, or commit sequence. A template is a fallback owned only by the skill that creates that artifact.

The deprecated directory contains no installable skills. It preserves replacement and uninstall guidance after retired implementations leave the repository.

## Artifact ownership

| Artifact or action | Owner |
| --- | --- |
| Glossary entry and qualifying ADR | `domain-context` |
| Requirement-pool scoring and consumption, shared Milestone Feature selection, ownership, cross-Feature dependencies, replanning, and completed-Feature index | `milestone-planning` |
| Feature behavioral contract | `feature-spec` |
| Review-critical technical choices and shared implementation contracts | `technical-design` |
| Feature-owned child Task DAG, ownership surfaces, blockers, safe parallelism, and integration proof | `task-planning` |
| One Feature or Task's durable internal execution strategy, stable slices, migration, containment, and rollback | `implementation-plan` |
| Optional local identity, operational state, and generated Feature-first views when no external tracker exists | `local-work-tracker` |
| Optional Feature-centered docs scaffold | `docs-workflow-bootstrap` |
| One next-skill recommendation only | `waypoint-workflow` |

Matt Pocock's skills own general clarification, implementation, test-first execution, review, and handoff:

- `grilling` resolves intent;
- `implement` executes an explicitly assigned implementation-ready Feature or Task;
- `tdd` and `code-review` support implementation quality;
- `handoff` transfers work without copying durable artifacts;
- `to-tickets` supplies the tracer-bullet planning method adapted by `task-planning`.

Waypoint does not duplicate these protocols.

## Feature documentation

Artifact ownership is semantic, not filename-prescriptive. The fallback convention is:

```text
docs/work/
├── index.md
├── requirements.md
├── completed.md
└── features/<feature>/
    ├── feature.md
    ├── spec.md
    ├── design.md
    ├── task-plan.md
    ├── plan.md
    └── tasks/<task>/
        ├── task.md
        └── plan.md
```

`feature.md` is always the human entry point after a Feature is materialized. It owns stable identity, Feature owner, outcome, canonical Acceptance, references, and a generated linked Task checklist when the Feature is split.

Other artifacts are threshold-driven:

- a split Feature requires one shared behavioral specification; an unsplit small Feature may keep a compact contract in `feature.md`;
- `design.md` exists only for a concrete material technical choice;
- `task-plan.md` exists only after the user confirms a real child Task graph;
- `plan.md` exists only when one already-bounded execution unit needs durable strategy or recovery beyond an approach preview.

Child Tasks remain under their Feature. There is no second authoritative global Task directory.

The global lifecycle is `requirements.md` → active Feature → `completed.md`. A wholly selected requirement leaves the active pool when its Feature is materialized; partial selection rewrites and rescores only the remainder. Completion removes the Feature from the active view but never moves or deletes its directory. `completed.md` is an ungrouped, newest-first history containing only date, Feature link, and optional one-line outcome.

## Tracking model

Live operational state has exactly one owner:

- use Jira, Linear, GitHub Issues, or another external tracker when configured;
- otherwise explicitly initialize `local-work-tracker`;
- never maintain both as competing authorities.

Tracking data reaches Task granularity so assignment, executor, blockers, MR, and safe parallelism remain visible. The default global view remains Feature-first and expands Task detail only on demand. `feature.md` always carries a simple generated Task checklist for human readers when child Tasks exist.

Feature completion is not a percentage calculation. Task summaries may be derived, but only the Feature owner confirms completion after Feature Acceptance and integration proof pass. The Milestone coordinator alone confirms Milestone scope changes and closure.

The local fallback uses committed shared configuration and ignored machine-local identity:

```text
.waypoint/config.yaml
.waypoint/local.yaml      # ignored
.waypoint/tracker/        # committed operational records
```

Resolve ownership from the target artifact or configured tracker, explicit request, `.waypoint/local.yaml`, authenticated external identity, then user clarification. Atomic skills read `.waypoint/local.yaml` directly when present; they do not require `local-work-tracker` to be invoked. Its `actor_id` identifies the current actor only. Git author metadata, harness, machine, branch, and temporary window labels are never silently treated as ownership. The local tracker uses one coordinator as writer and does not claim strong consistency across unsynchronized machines or worktrees.

Target resolution is separate from identity resolution. Prefer an exact ID, link, path, or artifact from the current request. When it is omitted, filter active Feature ownership and Task assignment by the resolved current actor. Proceed only for exactly one matching target; ask when zero or multiple targets remain. Never choose another actor's work, the first ready or unchecked item, recent edits, Git history, or branch naming merely to keep moving.

## Git integration

- An unsplit small Feature uses a short-lived Feature branch.
- A split Feature gives every Task its own branch or worktree.
- Executors may commit, push, open or update an MR, run verification, and respond to review.
- Safe Tasks should reach `main` through separate MRs early; use flags, compatibility layers, or expand–migrate–contract when intermediate behavior must remain hidden or compatible.
- Use a temporary Feature integration branch only when Tasks cannot safely merge independently. It has one coordinator and accepts changes through MRs, not shared direct pushes.
- Milestones never own branches, commits, pushes, MRs, or merge timing.

Task `completed` means accepted, verified, and safely integrated—not merely coded on a branch. Feature completion adds Feature-level integration proof.

## Authorization boundaries

These are separate permissions:

1. confirming discussion or shared understanding;
2. creating or approving a planning artifact;
3. implementing one explicitly assigned Feature or Task;
4. merging one specific MR;
5. deleting a branch/worktree or discarding work.

`ok`, `continue`, planning approval, automatic tool approval, or a ready Task never implies a later permission. A workflow recommends one skill and stops. No skill automatically chains specification, design, planning, implementation, merge, or cleanup.

## Optional workflow

`waypoint-workflow` is a read-only navigator. It inspects current evidence, recommends exactly one next local or installed Matt skill, and stops. There is no stateful Milestone or Feature workflow: the shared Milestone, Feature ownership, Task DAG, and tracker are the durable coordination model.
