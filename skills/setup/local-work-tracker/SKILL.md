---
name: local-work-tracker
description: Explicitly initialize or operate a repository-local collaboration tracker only when no external tracker exists. Use for local actor identity, Feature and Task assignment, status transitions, blocker checks, and generated human-readable Feature and global views without making local tracking a dependency of other skills.
---

# Local Work Tracker

Provide a deliberate, Git-backed fallback for teams without Jira, Linear, GitHub Issues, or another operational tracker.

## Require explicit use

Never invoke this skill implicitly. First inspect repository instructions and existing tracker configuration. Stop when an external tracker already owns live status unless the user explicitly asks to migrate away from it.

This tracker cannot provide strong atomic claims across unsynchronized machines or Git worktrees. Use one tracker coordinator as the live-state writer. Executors report changes; the coordinator applies them and promptly shares the resulting tracker checkpoint. Use an external tracker when autonomous concurrent claiming is required.

## Initialize local identity and storage

Run [scripts/waypoint_tracker.py](scripts/waypoint_tracker.py) from the repository root:

```bash
python3 <skill-path>/scripts/waypoint_tracker.py init --actor <stable-id> --display-name <name> --executor-harness <codex|opencode|pi|other> --executor-label <machine-or-window-label>
```

Initialization creates:

- committed `.waypoint/config.yaml` for shared tracker configuration;
- ignored `.waypoint/local.yaml` for the current actor and executor defaults;
- committed `.waypoint/tracker/` records only after Features or Tasks are registered;
- exact ignore rules for local identity and lock files;
- a generated dashboard region in the configured work index only after `render`.

Do not store credentials, tokens, cookies, or passwords. Resolve identity in this order: explicit current request, `.waypoint/local.yaml`, authenticated external-tracker identity, then user clarification. Never silently treat Git author metadata as Feature ownership.

Read [references/local-tracker-format.md](references/local-tracker-format.md) before changing generated paths or record semantics.

## Register and update exact targets

Use stable IDs independent of tracker issue numbers. Register a Feature only after Milestone selection created its durable Feature record; register a child Task only after the user approved its Task graph.

Every mutation names an exact Feature or Task. Assignment additionally requires the expected record revision. A Task becoming dependency-ready does not assign it, and no executor may claim it merely because it is ready.

Typical operations:

```bash
python3 <script> register-feature --id <feature> --title <title> --owner <actor> --milestone <milestone> --path <feature.md>
python3 <script> register-task --feature <feature> --id <task> --title <title> --path <task.md> --blocked-by <task-id>
python3 <script> assign --feature <feature> --task <task> --assignee <actor> --executor <harness/label> --branch <branch> --expect-revision <n>
python3 <script> transition --feature <feature> --task <task> --to <state> --expect-revision <n> --reason <why> --branch <branch> --mr <link> --evidence <proof>
python3 <script> transition-feature --feature <feature> --to <state> --expect-revision <n> --reason <why>
python3 <script> close-feature --feature <feature> --expect-revision <n> --confirmed-by <Feature owner> --evidence <Feature acceptance and integration proof>
python3 <script> render
python3 <script> check
```

Task states are `planned`, derived `ready`, `assigned`, `in-progress`, `blocked`, `in-review`, `completed`, and `cancelled`. `ready` is a view derived from unresolved blockers and is never stored. `completed` requires coordinator-supplied acceptance and integration evidence; code merely written on a branch remains `in-review`.

Keep stable assignee responsibility separate from the optional temporary executor. Only the Feature owner may confirm Task-graph or shared-contract changes. Only the Milestone coordinator may change Milestone scope.

## Render human views

Run `render` after each accepted state change. It updates generated marker regions rather than replacing human-authored content:

- a global Feature dashboard in `docs/work/index.md` or the configured work root;
- a linked Task checklist in every split `feature.md`.

The dashboard shows Features by default and summarizes child Task counts. Feature detail exposes Task status, assignee, executor, blockers, and MR. `[x]` means a Task is verified and safely integrated, never merely coded.

Finish after reporting changed records, revisions, generated views, and any synchronization limitation. Do not assign unspecified work, modify Feature contracts, run implementation, merge an MR, or delete branches/worktrees.
