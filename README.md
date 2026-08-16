<div align="center">

# Waypoint Skills

**Human-readable Feature planning for work that moves across people and agents**

[中文](README_CN.md) · [Architecture](ARCHITECTURE.md) · [Skills](#waypoint-skills) · [Installation](#installation)

</div>

Waypoint adds durable Milestone, Feature, Task, ownership, and tracking contracts around Matt Pocock's clarification, implementation, review, and handoff skills. It is designed for Codex planning followed by implementation in another Codex window, OpenCode, Pi, DeepSeek, or a human collaborator.

> [!IMPORTANT]
> Planning and execution are separate permissions. Confirming discussion, a specification, design, Task graph, or plan never authorizes implementation. Automatic tool approval changes tool mechanics, not delivery scope.

## Collaboration model

```text
Requirement pool
  └── Shared Milestone
      └── Feature — one stable owner
          └── Task — one assignee, optional executor
```

- A shared Milestone is a normally frozen batch of owned Features, not a serial task queue or Git branch.
- A Feature is the complete behavior and final-acceptance boundary.
- A small Feature may be implemented directly. Create child Tasks when work is too large for one safe fresh context or needs independent delivery boundaries across collaborators, windows, harnesses, or sessions.
- Tasks stay under their Feature and carry independent ownership, Acceptance, contracts, blockers, verification, branch, and MR.
- Git integrates at the smallest safe Feature or Task boundary; Milestone completion never delays push or merge.

## Waypoint skills

| Skill | Use it to |
| --- | --- |
| [`domain-context`](skills/waypoints/domain-context/SKILL.md) | Preserve durable terminology and qualifying ADRs |
| [`milestone-planning`](skills/waypoints/milestone-planning/SKILL.md) | Select or replan a shared, owned Feature batch from the requirement pool |
| [`feature-spec`](skills/waypoints/feature-spec/SKILL.md) | Capture one Feature's observable behavior without prescribing implementation |
| [`technical-design`](skills/waypoints/technical-design/SKILL.md) | Decide review-critical technical choices and express material schemas, states, and interactions concretely |
| [`task-planning`](skills/waypoints/task-planning/SKILL.md) | Adapt a Feature into a user-confirmed graph of independent child Tasks |
| [`implementation-plan`](skills/waypoints/implementation-plan/SKILL.md) | Make one Feature or Task's risky internal execution strategy durable |
| [`local-work-tracker`](skills/setup/local-work-tracker/SKILL.md) | Explicitly initialize or update local tracking when no external tracker exists |
| [`docs-workflow-bootstrap`](skills/setup/docs-workflow-bootstrap/SKILL.md) | Explicitly scaffold the optional Feature-centered docs convention |
| [`waypoint-workflow`](skills/workflows/waypoint-workflow/SKILL.md) | Read evidence, recommend exactly one next skill, and stop |

Every skill remains independently useful. The workflow is only a read-only navigator and never invokes its recommendation.

Example invocations:

```text
Use $milestone-planning to select the next shared Feature batch and owners.
Use $feature-spec to record this Feature's agreed behavior.
Use $task-planning to split this Feature across collaborators and stop before assignment.
Use $local-work-tracker to initialize local tracking because this repository has no external tracker.
Use $waypoint-workflow to recommend one next skill without doing its work.
```

## Tracking and human-readable docs

Operational state has one authority:

- use the configured external tracker when one exists;
- otherwise invoke `local-work-tracker` manually;
- do not maintain both as competing live state.

Tracking reaches Task granularity for assignment and conflict detection, while the default global dashboard remains Feature-first. Every split `feature.md` contains a generated linked Task checklist regardless of tracker choice.

The optional fallback layout is:

```text
docs/work/
├── index.md
├── requirements.md
├── completed.md
├── milestones/<milestone>.md
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

Only `feature.md` is the normal Feature entry point. A split Feature requires one shared spec; design, Task plan, and execution plan remain threshold-driven.

The global lifecycle is `requirements.md` → active Feature → `completed.md`. Materializing a complete candidate removes it from the active requirement pool; partial selection rewrites only the remainder. Completed Feature directories stay in place, while `completed.md` lists date, link, and an optional one-line outcome newest-first without grouping.

`local-work-tracker` creates committed `.waypoint/config.yaml`, ignored `.waypoint/local.yaml`, and committed operational records. It includes a dependency-free script for identity, revision-checked assignment, state transitions, validation, active and completed views. Other Waypoint skills read `.waypoint/local.yaml` directly when they need the current actor; if no durable owner, explicit identity, or valid local actor resolves ownership, they ask instead of guessing from Git or execution metadata. Because Git cannot provide strong claims across unsynchronized machines, the local fallback uses one coordinator as its writer.

Identity does not imply a target. A target-specific skill first uses an exact Feature or Task named by the request; otherwise it filters active ownership or assignment by `.waypoint/local.yaml`. It continues only when exactly one target remains and asks when the result is empty or ambiguous. It never selects another actor's work just because it is ready, first, recent, or branch-adjacent.

## Reuse from Matt Pocock

Waypoint deliberately uses [mattpocock/skills](https://github.com/mattpocock/skills) rather than copying general-purpose protocols:

| Matt skill | Responsibility |
| --- | --- |
| `grilling` | Resolve intent before planning |
| `to-tickets` | Source tracer-bullet and Task-DAG methodology adapted by `task-planning` |
| `implement` | Implement one explicitly assigned, implementation-ready Feature or Task |
| `tdd` | Test-first execution |
| `code-review` | Independent implementation review |
| `handoff` | Cross-window or cross-harness transfer without copying durable docs |
| `codebase-design` | Module and seam reasoning |
| `research` | External research |

Waypoint keeps its own Feature spec because Matt's spec combines implementation and testing decisions and assumes tracker publication. Waypoint keeps `task-planning` only for Feature nesting, ownership contracts, tracker-neutral IDs, repo-local handoffs, and assignment boundaries.

## Git and authorization

- Use a short-lived Feature branch for an unsplit Feature and independent Task branches for a split Feature.
- Executors may commit, push, create or update an MR, verify, and respond to review.
- Merge safe Tasks to `main` early. Use a temporary integration branch only when independent merge cannot keep the target correct.
- A Task is completed only after Acceptance, verification, review, and safe integration.
- Merging a specific MR, deleting a branch/worktree, and discarding work each require separate target-specific confirmation.
- `ok`, `continue`, shared-understanding confirmation, planning approval, `ready`, and automatic tool approval do not authorize implementation or merge.

## Installation

List available Waypoint skills:

```bash
npx skills add Adol1111/waypoint --list
```

Install the core planning set:

```bash
npx skills add Adol1111/waypoint \
  --skill milestone-planning \
  --skill feature-spec \
  --skill technical-design \
  --skill task-planning \
  --skill implementation-plan
```

Add optional navigation, context, docs, or local tracking individually:

```bash
npx skills add Adol1111/waypoint --skill waypoint-workflow
npx skills add Adol1111/waypoint --skill domain-context
npx skills add Adol1111/waypoint --skill docs-workflow-bootstrap
npx skills add Adol1111/waypoint --skill local-work-tracker
```

Install Matt skills separately:

```bash
npx skills add mattpocock/skills \
  --skill grilling \
  --skill to-tickets \
  --skill implement \
  --skill tdd \
  --skill code-review \
  --skill handoff \
  --skill codebase-design \
  --skill research
```

The [`skills` CLI](https://github.com/vercel-labs/skills) supports Codex, Claude Code, Cursor, and other Agent Skills-compatible tools.

## Migration from the previous catalog

- `roadmap-planning` → `milestone-planning`
- `task-spec` → `feature-spec`
- `task-state` → external tracker or explicit `local-work-tracker`
- `task-execution-simple` → Matt `implement`
- `milestone-workflow` → shared Milestone artifacts plus tracker; no stateful workflow replacement

The retired snapshots live under [`skills/deprecated/`](skills/deprecated/README.md) for migration reference and are not part of the active catalog. Generic recursive skill installers may still display these canonical snapshots, so do not select them for new installations. Remove project-scoped installed copies from every agent with:

```bash
npx skills@latest remove roadmap-planning task-spec task-state task-execution-simple milestone-workflow --agent '*'
```

Add `--global` when removing global installations. Review the targets shown by the CLI before confirming.

## Validation

```bash
scripts/validate.sh
```

The suite validates skill metadata, independent usage, template ownership, authorization boundaries, Feature/Task semantics, and the local tracker script.

## Releases

Waypoint uses [Changesets](https://github.com/changesets/changesets). Add one `.changeset/*.md` fragment for every user-visible skill change.
