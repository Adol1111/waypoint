# Local Tracker Format

The bundled script owns this fallback format. Do not edit generated dashboard regions manually.

```text
.waypoint/
├── config.yaml
├── local.yaml                 # ignored
└── tracker/
    ├── features/<feature>.yaml
    └── tasks/<feature>/<task>.yaml

docs/work/
├── index.md                   # generated dashboard region
├── completed.md               # generated completed timeline region
├── features/<feature>/        # standalone layout when Milestones are unused
│   ├── feature.md             # generated Task progress region
│   └── tasks/<task>/task.md
└── milestones/<milestone>/    # optional Milestone-grouped layout
    ├── milestone.md
    └── features/<feature>/...
```

Files use a dependency-free flat YAML subset: one key per line with JSON-compatible scalar or list values. Records carry monotonically increasing integer revisions. Mutations fail when `--expect-revision` does not match current state.

Feature records remain flat under `.waypoint/tracker/features/` and contain operational identity, status, owner, optional current Milestone grouping, repository-relative document path, optional one-line outcome, completion date, evidence, and revision. The flat machine index does not define the human documentation layout. A planned Feature move rebases registered Task paths and revisions; a carried active Feature changes Milestone grouping without changing its document path. Task records contain only operational data: stable IDs, parent Feature, status, assignee, executor, structural blockers, branch, MR, evidence, paths, and revision. Durable Outcome, Scope, Acceptance, ownership contracts, and verification requirements remain in Feature-owned Markdown.

`ready` is computed for a stored `planned` Task when all `blocked_by` Tasks are completed. It is not persisted. Feature summary is computed from child Tasks, but only `close-feature` records authoritative Feature completion after owner confirmation.

The script updates content only between these markers:

```md
<!-- waypoint:dashboard:start -->
<!-- waypoint:dashboard:end -->

<!-- waypoint:completed:start -->
<!-- waypoint:completed:end -->

<!-- waypoint:tasks:start -->
<!-- waypoint:tasks:end -->
```

When a marker region is absent, the script appends the corresponding generated section without replacing existing prose.
