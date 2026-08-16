# Deprecated Skills

Retired skill implementations were archived for the `0.3.x` migration window and removed in `0.4.0`. This directory now keeps only replacement and uninstall guidance; it contains no installable skills.

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
