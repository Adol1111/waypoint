# Local Tracker Format

The bundled script owns this fallback format. Do not edit generated dashboard regions manually.

```text
.waypoint/
├── config.yaml
├── local.yaml                 # ignored
└── tracker/
    └── features/<feature>.yaml

docs/work/
├── index.md                   # generated Feature dashboard region
├── completed.md               # generated completed timeline region
└── features/<feature>/        # or a repository-native Feature layout
    └── feature.md
```

`.waypoint/local.yaml` is machine-local identity and must never contain credentials. `.waypoint/tracker/features/<feature>.yaml` is a flat machine index for Feature ownership and lifecycle lookup. It contains the stable Feature ID, title, summary, owner, optional Milestone, document path, status, completion evidence/date, and revision. Records use a dependency-free flat YAML subset: one key per line with JSON-compatible scalar or list values.

The local tracker deliberately has no `.waypoint/tracker/tasks/` directory. Child Tasks, Task plans, blockers, assignees, branches, MRs, and Task status belong in the Feature-owned artifact or an external tracker. This avoids maintaining a second Task authority just to resolve the current Feature.

During migration from the former format, existing Task records are ignored rather than interpreted. Move any information worth keeping to the chosen authority before deleting those legacy files in a separately reviewed change.

Feature records carry monotonically increasing integer revisions. Mutations fail when `--expect-revision` does not match current state. A planned Feature may change its document path during `replan-feature`; after execution begins, its path stays stable. Replanning changes grouping and does not copy or rebase child Task records because the local tracker does not own them.

The script updates content only between these markers:

```md
<!-- waypoint:dashboard:start -->
<!-- waypoint:dashboard:end -->

<!-- waypoint:completed:start -->
<!-- waypoint:completed:end -->
```

When a marker region is absent, the script appends the corresponding generated section without replacing existing prose.
