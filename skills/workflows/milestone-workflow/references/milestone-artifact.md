# Milestone Artifact

Use this compact shape only when milestone management is requested and the repository has no existing convention. It may live in `MILESTONES.md`, a roadmap, a tracker, or the opt-in docs layout.

```md
# Milestones

## Open

### <Milestone>

Status: <planned | in-progress | blocked | completed>

#### Outcome

<The selected engineering or product results.>

#### Constraints

- <Only a cross-task constraint or key global non-goal>

#### Selection

| Backlog outcome | Score at selection | Why selected |
| --- | ---: | --- |
| <outcome> | <0–10 or repository-native priority> | <evidence-backed rationale> |

#### Exit criteria

- [ ] <Observable criterion> — <task links when ownership is clear>

#### Tasks

- `<planned | in-progress | blocked | completed>` [<atomic task>](<durable task artifact>)

## Completed

- [<Milestone>](<durable link>)
```

Record the selection and linked task map returned by `roadmap-planning`; this artifact does not redefine its scoring, atomic-task, or task-handoff rules.

Use status as current truth, not history:

- `planned`: tasks exist and none has started;
- `in-progress`: at least one task is active or another progress path remains;
- `blocked`: the whole Milestone has no progress path;
- `completed`: exit criteria, required tasks, and Discovered Work closure checks are satisfied.

A blocked task does not block the Milestone while another task can progress. Update status in place without dates or transition logs.

Add only the conditional section whose trigger exists:

- `Dependency graph`: when at least one cross-task start or completion dependency exists; use Mermaid and label completion or verification gates distinctly.
- `Open Decisions`: only for an unresolved choice that affects the Milestone boundary, multiple tasks, dependency relationships, or exit criteria; remove it after resolution or transfer to its owning artifact.
- `Discovered Work`: only after the first durable out-of-scope or unowned finding that this Milestone cannot handle now.
- `Completion Evidence`: only for cross-task integration, release, or migration proof that no individual task owns.

Omit `Constraints` and every conditional section when empty. Link every exit criterion directly to the task or tasks that satisfy it; do not add a separate coverage table. Treat each `roadmap-planning` handoff as the authoritative task-local source. The Milestone task list contains links and status only, ordered by the recommended execution sequence. This order remains advisory; the optional Mermaid graph carries real cross-task dependencies. Omit the graph when every task is independent. Do not add Current Focus, task-count targets, planning baselines, confirmation flags, or process notes.

Add cross-task integration proof only when task-local proof is insufficient, and create an integration task only when that work is substantial. Keep findings required by the current task in that task. Put a finding explicitly owned by another current task directly in that task. Use Discovered Work only for concerns the Milestone cannot handle now or whose owner is uncertain.

After the Discovered Work audit passes, compact the completed Milestone to Outcome, necessary global Constraints, Selection, checked Exit Criteria, completed task links, and final dispositions. Remove the dependency graph and resolved or transferred Open Decisions. Keep Completion Evidence only when its cross-task proof has no task owner.

Freeze completed scope. Permit factual corrections and cross-task evidence links; route new work to an open Milestone, backlog, or Future Directions.

When the repository intentionally keeps all Milestone work in one file and has no separate task items, let each compact task section be that task's durable owner. Preserve the same planning handoff fields there rather than creating a directory solely to match this example.
