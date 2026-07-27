# Task State Template

Use only when no existing tracker or task artifact fits.

```md
# <Task>

Status: <planned | in-progress | blocked | completed>

## Acceptance

- [ ] <observable acceptance condition>

## Evidence

- <command, result, review, or delivered artifact>

## Blocker

<For blocked work: condition, impact, and unblocking event. Omit otherwise.>

## Working state

<Branch, worktree, or uncommitted surface only when useful for recovery.>

## Selection context

- Why now: <Reason this task is currently selected.>
- Start when: <Dependency, precondition, or activation signal.>
- Revisit when: <Signal for reconsidering deferred work.>
```

Omit the Selection context section or any unused entry when it adds no recovery value. Do not invent scheduling information.
