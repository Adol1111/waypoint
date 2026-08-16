# Requirement Pool Template

Use only when no stronger backlog or tracker convention exists. Keep candidates lightweight until selection.

```md
# Requirement Pool

## Candidates

### <Candidate outcome>

- Type: <feature | bug | maintenance | migration>
- Priority: <repository-native value or 0–10>
- Why now: <evidence-backed value, delay cost, risk, or commitment>
- Depends on: <Feature or public contract, when known>
- Source: <durable evidence>
- Reconsider when: <observable signal, when deferred>
```

Do not pre-create detailed specifications, designs, or Tasks for unselected candidates.

When a candidate becomes a durable Feature, remove the selected outcome from this active pool. If selection is partial, rewrite and rescore only the unselected remainder. Never duplicate the same full outcome in both this pool and a Feature.
