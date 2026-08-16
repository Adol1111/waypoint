---
name: docs-workflow-bootstrap
description: Explicitly scaffold or adapt an optional repository-local Markdown convention for requirement and completion indexes, shared Milestones, Feature-owned specifications and designs, and nested child Task contracts. Use only when a team asks Waypoint to initialize human-readable engineering documentation without requiring local tracking or a fixed workflow.
---

# Docs Workflow Bootstrap

Create only the durable documentation convention the repository will actually use.

## Inspect and confirm

1. Read repository instructions and existing documentation, ADR, issue, roadmap, Feature, and tracker conventions.
2. Reuse existing locations. Do not create a parallel `docs/` tree beside a working convention.
3. Show the exact roots and files that would be created or adapted. Ask the user to confirm before scaffolding.
4. Create no placeholder Milestones, Features, Tasks, specs, designs, plans, or tracker records.

Use [references/feature-convention.md](references/feature-convention.md) only when no stronger local form exists. The same Feature layout works with an external tracker, the optional `local-work-tracker`, or no operational tracker. This setup skill does not choose or initialize a tracker.

Offer `docs/context/` for glossary and durable context and `docs/architecture/decisions/` for qualifying ADRs only when useful. A user may request either location without accepting the delivery layout.

Do not create substantive requirements, Milestone scope, Feature ownership, specifications, technical designs, Task graphs, implementation plans, identity configuration, branch policy, labels, or code. Finish after reporting created, reused, and deliberately omitted locations.
