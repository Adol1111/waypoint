# Milestone Artifact

Use this compact shape only when milestone management is requested and the repository has no existing convention. It may live in `MILESTONES.md`, a roadmap, a tracker, or the opt-in docs layout.

```md
# Milestones

## Open

### <Milestone>

Status: <planned | in-progress | blocked>

#### Outcome

<The selected engineering or product results.>

#### Selection

- Task-count target: <user request or confirmed proposal>
- Optional external constraint: <timebox, deadline, or release boundary only when supplied>
- Explicitly later: <important excluded work>

| Backlog outcome | Score at selection | Why selected |
| --- | ---: | --- |
| <outcome> | <0–10 or repository-native priority> | <evidence-backed rationale> |

#### Exit criteria

- [ ] <Observable criterion>

#### Current focus

- Task or slice: <selected work>
- Next waypoint: <atomic skill or immediate action>
- Blocked by: <blocker, if any>

#### Tasks

##### <Atomic task>

- Status: <planned | in-progress | blocked | completed>
- Outcome: <bounded and verifiable stage result>
- Rough scope: <included and excluded>
- Depends on: <hard dependency, or none>
- Stage proof: <task-level success signal>

#### Ready tasks

- <Task with no unsatisfied dependency>

#### Delivery coverage

| Exit criterion | Contributing tasks | Cross-task proof or remaining gap |
| --- | --- | --- |
| <criterion> | <durable task links> | <integration proof only when task proof is insufficient> |

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

Omit unused example entries, including Current focus when no work is selected. Record the selection and task map returned by `roadmap-planning`; this artifact does not redefine its scoring or atomic-task rules. Write each task's spec and any warranted design or plan when development begins.

For an open Milestone, keep enough Delivery coverage to show how every exit criterion can be satisfied; it is a planning map, not duplicated task detail or a guarantee that the plan cannot evolve. Add cross-task integration proof only when task-local proof is insufficient, and create an integration task only when that work is substantial. Keep findings required by the current task's acceptance in that task. Record durable out-of-task, cross-task, separately scheduled, or uncertain findings in Discovered work before routing them, defaulting to `untriaged` when placement is not explicit. A destination task counts only when its durable acceptance, scope, or state explicitly owns the finding. Preserve resolved entries as source history. Closure requires an individually checked disposition plus any required destination, evidence, or rationale; an empty section is not proof. Keep concrete deferred outcomes in a backlog and goal-shaped uncertainty under Future directions.
