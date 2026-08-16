# Shared Milestone Template

```md
# <Milestone>

Coordinator: <stable actor identity>
Status: <planned | in-progress | blocked | completed | cancelled>

## Outcome

<Shared iteration, stage, or release result.>

## Features

- [ ] [<Feature>](<feature-link>) — owner: <actor>; status: <current summary>

## Exit criteria

- [ ] <Observable Milestone-level result> — <Feature links>

## Cross-Feature dependencies

<When at least one real blocking edge exists, add a Mermaid `flowchart LR` DAG. Include every required Feature as a node, including disconnected Features that can proceed in parallel. Draw prerequisite --> dependent, label non-obvious edges with the public contract or completion gate, and add concise notes only when the graph cannot explain the dependency. Omit this section when no blocking edges exist.>

## Scope changes

- <Added, removed, or transferred Feature and explicit reason. Omit until replanning occurs.>
```

Store this artifact as `milestones/<milestone>/milestone.md` when using the fallback layout. Nest newly materialized Features below its `features/` directory only when the repository selected Milestone-grouped Feature documentation; otherwise link standalone Feature paths. The Feature list and DAG are frozen after confirmation except through explicit replanning. The DAG contains stable Feature dependencies only: never derive edges from priority, list order, shared ownership, delivery preference, or internal Tasks, and never encode live status in it. Do not add child Tasks, current focus, branch policy, commit state, or a serial execution cursor.
