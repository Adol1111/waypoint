# Task State Template

Use only when no existing tracker or task artifact fits.

Start with the smallest durable record:

```md
# <Task>

Status: <planned | in-progress | blocked | completed>

## Acceptance

- [ ] <observable acceptance condition>
```

Add only the branch required by the current state.

For work stopping or handing off:

```md
## Recovery checkpoint

- Remaining: <unresolved acceptance, decision, or review finding>
- Next: <next meaningful action>

## Working state

<Only non-obvious state required for safe continuation>
```

For blocked work:

```md
## Blocker

<Condition, impact, and unblocking event>
```

For completed work:

```md
## Final verification

- <Final checks or review, outcomes, and acceptance demonstrated>
- Verified revision or run: <commit, PR, CI, release, or artifact link when one exists>
```

When useful, add one selection signal: `Why now`, `Start when`, or `Revisit when`. Add unresolved review details beneath `Remaining` or link their durable review location. The completed form contains Acceptance and Final verification, not transient recovery sections.
