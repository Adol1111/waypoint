# Deprecated Skills

Archived snapshots of retired Waypoint skills. They remain here for migration reference and are not part of the active catalog, recommended installation bundles, routing, validation contract, or current architecture.

These snapshots retain canonical `SKILL.md` files so humans can inspect their last published form. A generic recursive skill installer may therefore still display them; each snapshot is marked deprecated and disables implicit invocation, and should not be selected for a new installation.

| Deprecated skill | Replacement |
| --- | --- |
| `roadmap-planning` | `milestone-planning` |
| `task-spec` | `feature-spec` |
| `task-state` | External tracker or explicit `local-work-tracker` |
| `task-execution-simple` | Matt Pocock's `implement` |
| `milestone-workflow` | Shared Milestone artifacts, Feature ownership, and the configured tracker |

Remove project-scoped installed copies from every agent with:

```bash
npx skills@latest remove roadmap-planning task-spec task-state task-execution-simple milestone-workflow --agent '*'
```

Add `--global` to remove global installations. Review the exact targets shown by the CLI before confirming.
