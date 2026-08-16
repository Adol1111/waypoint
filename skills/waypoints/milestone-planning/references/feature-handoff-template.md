# Feature Handoff Template

Create one non-empty Feature record for every selected Feature when no stronger convention exists.

When the repository uses Milestone-grouped documentation, store it at `milestones/<milestone>/features/<feature>/feature.md`. Otherwise preserve the repository's standalone Feature root and link it from the Milestone. The Feature ID remains globally unique; directory placement does not transfer ownership to the Milestone coordinator.

```md
# <Feature>

Feature ID: <tracker-neutral stable ID>
Type: <feature | bug | maintenance | migration>
Owner: <stable actor identity>
Milestone: <link>
Tracker: <link when external tracking exists>

## Outcome

<Complete, independently accepted result.>

## Scope

- Includes: <coarse behavioral boundary>
- Excludes: <important adjacent outcome>

## Acceptance

- [ ] <Observable Feature completion condition>

## Task progress

<!-- waypoint:tasks:start -->
<Generated linked checklist when child Tasks exist. Omit this section for an unsplit Feature.>
<!-- waypoint:tasks:end -->

## References

- <Existing spec, design, task plan, ADR, or source link>
```

An external tracker or `local-work-tracker` renders the Task progress region. Executors do not edit it manually. Omit empty optional fields and sections.
