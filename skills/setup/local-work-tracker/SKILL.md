---
name: local-work-tracker
description: Explicitly initialize or operate a repository-local Feature owner index only when no external tracker exists. Use for local actor identity, Feature ownership, owner-filtered target discovery, Feature lifecycle transitions, and generated Feature views without making local tracking a dependency of other skills.
---

# Local Work Tracker

Provide a deliberate, Git-backed fallback for teams without Jira, Linear, GitHub Issues, or another operational tracker.

## Require explicit use

Never invoke this skill implicitly. First inspect repository instructions and existing tracker configuration. Stop when an external tracker already owns live status unless the user explicitly asks to migrate away from it.

This is an owner index, not a Task tracker. It prevents a local agent window from selecting another person's Feature. It does not claim strong atomic ownership across unsynchronized machines or Git worktrees; use one tracker coordinator for shared mutations or an external tracker when autonomous concurrent claiming is required.

## Initialize local identity and storage

Run [scripts/waypoint_tracker.py](scripts/waypoint_tracker.py) from the repository root:

```bash
python3 <skill-path>/scripts/waypoint_tracker.py init --actor <stable-id> --display-name <name>
```

Initialization creates:

- committed `.waypoint/config.yaml` for shared local-mode configuration;
- ignored `.waypoint/local.yaml` for the current actor;
- committed `.waypoint/tracker/features/` records only after Features are registered;
- exact ignore rules for local identity and lock files.

Do not store credentials, tokens, cookies, or passwords. `.waypoint/local.yaml` identifies the current actor; it does not automatically assign ownership to unrelated Features. Never infer ownership from Git author metadata, a harness, machine, branch, or window label.

Read [references/local-tracker-format.md](references/local-tracker-format.md) before changing generated paths or record semantics.

## Register and resolve Features

Register a Feature after its durable Feature record exists and its owner is known:

```bash
python3 <script> register-feature --id <feature> --title <title> --summary <one-line outcome> --owner <actor> [--milestone <milestone>] --path <feature.md>
python3 <script> list-features --mine --active-only
python3 <script> list-features --owner <actor> --active-only
```

Feature records contain the stable ID, owner, optional Milestone grouping, document path, Feature status, completion evidence, and revision. They contain no child Task records, assignees, executors, branches, MRs, blockers, or Task status.

When a target is omitted, resolve the actor from explicit request or `.waypoint/local.yaml`, then filter active Feature records by `owner`. Continue only when exactly one candidate matches. Ask when none or several match. Never fall through to another actor's Feature, a ready queue head, recent edits, Git history, or branch naming. Once the Feature is selected, use its own `feature.md`, `feature.yml`, Task plan, or external tracker for any Task detail.

## Update Feature state

Every mutation names an exact Feature and supplies its expected revision:

```bash
python3 <script> transition-feature --feature <feature> --to <state> --expect-revision <n> --reason <why>
python3 <script> replan-feature --feature <feature> [--to-milestone <milestone> | --standalone] [--path <new-feature.md-before-execution-only>] --expect-revision <n> --reason <why>
python3 <script> close-feature --feature <feature> --expect-revision <n> --confirmed-by <Feature owner> --evidence <Feature acceptance and integration proof> --completed-at <YYYY-MM-DD>
python3 <script> render
python3 <script> check
```

Task planning remains a Feature-owned durable artifact. If a team needs live Task assignment or status, attach that data to the Feature-owned artifact or use the configured external tracker. This local tracker does not create a second Task status store or `.waypoint/tracker/tasks/` authority.

When upgrading an existing repository, legacy `.waypoint/tracker/tasks/` records are not read by the new script. Preserve any needed Task contract or status in the chosen Feature-owned or external authority, then remove obsolete records in a separately reviewed change.

## Render human views

Run `render` after an accepted Feature state change. It updates only generated marker regions:

- a global Feature dashboard grouped by Milestone when present and flat when all Features are standalone;
- a newest-first completed Feature index in `docs/work/completed.md` containing only date, Feature link, and optional one-line outcome.

The dashboard is Feature-first and owner-visible. It does not summarize or rewrite child Tasks. Finish after reporting changed records, revisions, generated views, and any synchronization limitation. Do not modify Feature contracts, run implementation, merge an MR, or delete branches/worktrees.
