# Feature Docs Convention

Use only after the user explicitly accepts this fallback layout. Existing repository conventions take precedence.

```text
docs/
├── context/
│   └── glossary.md
├── architecture/
│   └── decisions/
│       └── index.md
└── work/
    ├── index.md
    ├── requirements.md
    ├── completed.md
    ├── milestones/
    │   └── <milestone>.md
    └── features/
        └── <feature>/
            ├── feature.md
            ├── spec.md          # required for split Features; otherwise optional
            ├── design.md        # only for material technical choices
            ├── task-plan.md     # only for confirmed child Task DAGs
            ├── plan.md          # optional unsplit Feature execution strategy
            └── tasks/
                └── <task>/
                    ├── task.md
                    └── plan.md  # optional Task-internal execution strategy
```

`feature.md` is the Feature entry point and owns its stable ID, owner, outcome, canonical Acceptance, references, and generated Task checklist. Child Tasks are always nested under their Feature. Do not create a second global authoritative Task directory.

The global `docs/work/index.md` is the active Feature-first view. An external tracker or `local-work-tracker` may update a generated dashboard region; human-authored context stays outside its markers. `requirements.md` contains only unselected lightweight candidates. Selection materializes a Feature and consumes the selected requirement; partial selection rewrites the remainder. `completed.md` is an ungrouped, newest-first index containing only completion date, Feature link, and an optional one-sentence outcome. Feature directories remain in place as durable detail. A shared Milestone links Features and owners, never child Tasks or Git boundaries.

Bootstrap creates accepted roots and index headings only. Artifact-owning skills create substantive Milestones, Features, specs, designs, Task plans, Task contracts, and plans when their actual triggers exist.
