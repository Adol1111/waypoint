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

Create `docs/tasks/<milestone>/index.md` only when a real Milestone is planned. Put task-local `spec.md`, optional `design.md`, and optional `plan.md` beside their task when useful, or keep distinct specification and technical-design sections in one task artifact. Do not create placeholder Milestones.
