# Standalone Docs Convention

Use when the user wants shared local docs without Milestone management. Create only the accepted files.

```text
docs/
├── index.md
├── context/
│   └── glossary.md
├── architecture/
│   └── decisions/
│       └── index.md
└── tasks/
    └── index.md
```

Suggested `docs/tasks/index.md`:

```md
# Tasks

## Active

- <Task link and status>

## Completed

- <Task link and completion evidence>

## Deferred

- <Concrete follow-up, or link to the repository's existing tracker>
```

Task-local `spec.md`, optional `design.md`, and optional `plan.md` may live beside a task. A repository may instead keep distinct specification and technical-design sections in one task artifact. Do not create placeholder task directories or files.
