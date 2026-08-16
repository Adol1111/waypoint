# Feature Docs Convention

Use only after the user explicitly accepts this fallback layout. Existing repository conventions take precedence.

Choose one Feature placement that matches how the user coordinates work.

For Milestone-managed delivery:

```text
docs/work/
├── index.md
├── requirements.md
├── completed.md
└── milestones/<milestone>/
    ├── milestone.md
    └── features/<feature>/
        ├── feature.md
        ├── spec.md
        ├── design.md
        ├── task-plan.md
        ├── plan.md
        └── tasks/<task>/
            ├── task.md
            └── plan.md
```

For standalone delivery without Milestones:

```text
docs/work/
├── index.md
├── requirements.md
├── completed.md
└── features/<feature>/
    ├── feature.md
    ├── spec.md
    ├── design.md
    ├── task-plan.md
    ├── plan.md
    └── tasks/<task>/
        ├── task.md
        └── plan.md
```

`feature.md` is the Feature entry point and owns its globally unique stable ID, owner, outcome, canonical Acceptance, references, and generated Task checklist. Child Tasks are always nested under their Feature. Milestones are optional; do not create one merely to hold a Feature. Do not duplicate a Feature between flat and Milestone-grouped roots or create a second authoritative Task directory.

The global `docs/work/index.md` is the active Feature-first view. Group it by Milestone when Milestones are used; otherwise keep the flat Feature view. An external tracker or `local-work-tracker` may update a generated dashboard region; human-authored context stays outside its markers. `requirements.md` contains only unselected lightweight candidates. Materializing a Feature consumes the selected requirement; partial selection rewrites the remainder. `completed.md` is an ungrouped, newest-first index containing only completion date, Feature link, and an optional one-sentence outcome. Feature directories remain at their stable path as durable detail after completion.

When the user later adopts or changes a Milestone, explicit replanning may move an unstarted Feature directory and update all durable references and tracker paths atomically. After execution begins, keep the directory stable and let the Milestone link the Feature instead of moving work underneath active branches. The Milestone owns optional grouping and cross-Feature dependencies, not Feature ownership, child Tasks, or Git boundaries.

Bootstrap creates accepted roots and index headings only. Artifact-owning skills create substantive Milestones, Features, specs, designs, Task plans, Task contracts, and plans when their actual triggers exist.
