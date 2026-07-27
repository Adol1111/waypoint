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
- Disposition: <untriaged | current milestone | later milestone | backlog | future question | accepted limitation | discarded>
- Destination: <artifact or tracker link when resolved>

#### Completion evidence

- <command, result, review, release, or other proof>

#### Future directions

- <Goal-shaped question, why it matters, and reconsideration signal>

## Completed

- <Milestone and durable link>
```

Omit unused example entries, including Current focus when no work is selected. Preserve resolved discovered work when it provides useful history; closure requires dispositions, not an empty section. Keep concrete deferred tasks in a backlog and goal-shaped uncertainty under Future directions.
