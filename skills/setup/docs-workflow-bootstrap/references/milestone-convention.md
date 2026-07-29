# Milestone Docs Convention

Use only when the user explicitly chooses Milestone-managed delivery. Create only the accepted files.

```text
docs/
├── index.md
├── context/
│   └── glossary.md
├── architecture/
│   └── decisions/
│       └── index.md
└── tasks/
    ├── index.md
    └── backlog.md
```

Suggested `docs/tasks/index.md`:

```md
# Delivery

Workflow: milestone-managed

## Open Milestones

- <Milestone link and status>

## Completed Milestones

- <Milestone link and completion evidence>

## Backlog

- [Deferred work](./backlog.md)

## Future Directions

- <Goal-shaped question and reconsideration signal>
```

Suggested `docs/tasks/backlog.md`:

```md
# Backlog

Concrete, task-shaped deferred work that is not assigned to an open Milestone lives here. Broader goals and future questions remain under Future Directions in the roadmap or milestone artifact without invented task detail.

## Items

### <Outcome>

- Source: <Milestone discovery, task, issue, or request>
- Reason deferred: <why no active artifact owns it now>
- Reconsider when: <observable signal>
```

Backlog is an active queue rather than history. Promote an item only after a destination Milestone, task, or slice explicitly owns it, then remove it. Remove resolved items after their evidence is durable elsewhere. Leave unchanged entries untouched; do not append review dates, retained states, or review history.

Create `docs/tasks/<milestone>/index.md` only when a real Milestone is planned. Put task-local `spec.md`, optional `design.md`, and optional `plan.md` beside their task when useful, or keep distinct specification and technical-design sections in one task artifact. Do not create placeholder Milestones.
