# Roadmap Template

Use this fallback only for a standalone goal with no task artifacts or local roadmap form. A Milestone index uses linked task handoffs instead of these expanded slices. Omit empty sections and keep each fact in one place.

```md
# <Goal>

## Outcome and constraints

<Desired future state, success signals, and material constraints.>

## Delivery slices

### <Meaningful delivery>

- Outcome: <bounded result>
- Planning boundary: <included and excluded>
- Depends on: <hard dependency, or none>
- Stage proof: <independent success signal>

## Open decisions

- <Precise choice>: <impact and latest useful decision point>

## Future questions

- <Question preserved without invented decomposition>
```

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
