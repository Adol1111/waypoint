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
    ├── backlog.md
    └── <milestone>/
        ├── index.md
        └── <task>/
            ├── task.md
            ├── spec.md              # when behavior is specified
            ├── technical-design.md  # optional, repository-native name may differ
            └── plan.md    # optional
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

Concrete deferred candidate outcomes that are not assigned to an open Milestone live here. One candidate may later expand into several atomic tasks. Broader goals and future questions remain under Future Directions in the roadmap or milestone artifact without invented task detail.

## Items

### <Outcome>

- Priority score: <0–10, or repository-native priority>
- Priority rationale: <impact, delay cost, commitment, risk, strategic value, and unblocking value>
- Selection constraints: <readiness, confidence, dependency, proof, migration, release, or external wait when material>
- Source: <Milestone discovery, task, issue, or request>
- Reason deferred: <why no active artifact owns it now>
- Reconsider when: <observable signal>
```

Backlog is an active queue rather than history. These fields preserve each candidate's current priority, evidence, deferral reason, and reconsideration signal without imposing a scoring system or planning algorithm. The selected roadmap or workflow skill determines how candidates are evaluated and transferred; bootstrap only creates the agreed storage convention.

At bootstrap, create only the accepted shared roots; the `<milestone>` and `<task>` entries above describe the convention rather than placeholder directories.

When a real Milestone and its atomic tasks are confirmed, create `docs/tasks/<milestone>/index.md` plus one non-empty `docs/tasks/<milestone>/<task>/task.md` planning handoff for each selected task. The index keeps an ordered list such as ``- `planned` [Task](./task/task.md)``, retains global selection and exit criteria, and adds a Mermaid graph only when real cross-task dependencies exist. Task status is the global recovery signal; there is no Milestone-level Current Focus.

Development skills own later task contents. This convention adds References only for artifacts that exist and follows repository-native locations and filenames.
