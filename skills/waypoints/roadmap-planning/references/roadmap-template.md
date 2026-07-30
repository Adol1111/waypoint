# Roadmap Template

Adapt this shape to the repository. Do not create empty sections or speculative task trees.

```md
# <Goal>

## Outcome and constraints

<Desired future state, success signals, and material constraints.>

## Why this direction now

- Evidence: <product gap, feedback, incident, research, dependency, or other durable signal>
- Alternatives considered: <other plausible Milestone directions, when genuine>
- Why selected: <expected result and cost of delay>
- Task-count target: <user request or confirmed agent proposal>
- Optional external constraint: <timebox, deadline, or release boundary only when supplied>
- Explicitly later: <important work excluded from this boundary>

## Selected backlog outcomes

| Candidate outcome | Score at selection | Why selected | Expanded tasks |
| --- | ---: | --- | --- |
| <backlog outcome> | <0–10 or repository-native priority> | <evidence-backed rationale> | <task links or names> |

## Atomic tasks

### <Meaningful engineering delivery>

- Outcome: <bounded stage result>
- Rough scope: <included and excluded>
- Depends on: <hard dependency, or none>
- Unblocks: <named task or candidate outcome, when relevant>
- Stage proof: <task-level success signal; implementation verification stays in this task>

## Milestone coverage

<Account for every exit criterion without repeating task-level spec, design, or plan detail.>

| Exit criterion | Contributing tasks | Cross-task proof or remaining gap |
| --- | --- | --- |
| <observable criterion> | <completed, active, or proposed tasks> | <integration proof only when task proof is insufficient> |

## Delivery shape

- Hard dependencies: <only ordering that cannot change>
- Ready tasks: <tasks with no unsatisfied dependency>
- Parallel paths: <tasks that can progress independently>
- Integration task: <only when substantial cross-task work is required>

## Open decisions

- <Precise choice>: <impact and latest useful decision point>

## Future questions

- <Question preserved without invented decomposition>
```

For a standalone goal, omit Milestone coverage and unused delivery-shape fields. For a Milestone, retain the coverage table before identifying a next ready task.

When maintaining a backlog alongside this roadmap, keep each item as a schedulable candidate outcome:

```md
### <Backlog outcome>

- Priority score: <0–10, or repository-native priority>
- Priority rationale: <delay cost, urgency, commitment, value, strategic fit, risk reduction, and unblocking value>
- Selection constraints: <readiness, confidence, dependency, proof, migration, release, or external wait when material>
- Source: <durable evidence or discovery>
- Reason deferred: <why no open Milestone owns it>
- Reconsider when: <observable signal>
```

Apply the scoring, selection, and atomic-task rules in `roadmap-planning`; this template only records their result.
