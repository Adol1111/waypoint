# Milestone Artifact

Use this compact shape only when milestone management is requested and the repository has no existing convention. It may live in `MILESTONES.md`, a roadmap, a tracker, or the opt-in docs layout.

```md
# Milestones

## Open

### <Milestone>

Status: <planned | in-progress | blocked>

#### Outcome

<The shared delivery result.>

#### Exit criteria

- [ ] <Observable criterion>

#### Current focus

- Task or slice: <selected work>
- Next waypoint: <atomic skill or immediate action>
- Blocked by: <blocker, if any>

#### Tasks or delivery slices

- `completed`: <item>
- `in-progress`: <item>
- `planned`: <item>

#### Discovered work

##### <Finding>

- Impact: <why it matters>
- Source: <task, verification, or event>
- Disposition: <untriaged | current milestone | resolved | later milestone | backlog | future question | accepted limitation | discarded>
- Destination: <artifact or tracker link for later milestone, backlog, or another durable placement; omit otherwise>
- Resolution: <completion evidence, future-question reconsideration signal, or accepted/discarded rationale; omit while untriaged or current milestone>

#### Completion evidence

- <command, result, review, release, or other proof>

#### Future directions

- <Goal-shaped question, why it matters, and reconsideration signal>

## Completed

- <Milestone and durable link>
```

Omit unused example entries, including Current focus when no work is selected. Keep findings required by the current task's acceptance in that task. Record durable out-of-task, cross-task, separately scheduled, or uncertain findings in Discovered work before routing them, defaulting to `untriaged` when placement is not explicit. A destination task counts only when its durable acceptance, scope, or state explicitly owns the finding. Preserve resolved entries as source history. Closure requires an individually checked disposition plus any required destination, evidence, or rationale; an empty section is not proof. Keep concrete deferred tasks in a backlog and goal-shaped uncertainty under Future directions.
