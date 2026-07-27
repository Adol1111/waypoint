---
name: task-state
description: Maintain visible task acceptance, status, blockers, verification evidence, and safe closing state in any existing task system or a minimal Markdown artifact. Use when marking work planned, in-progress, blocked, or completed, or when isolated branch/worktree work may be merged, deleted, or discarded.
---

# Task State

Keep the task recoverable without imposing a tracker or lifecycle.

## Work independently

1. Find the repository's existing issue, task file, checklist, roadmap entry, or other state convention.
2. Update that artifact. If none exists and durable state is useful, propose the smallest Markdown task record in a repository-consistent location.
3. Preserve acceptance criteria and record status as `planned`, `in-progress`, `blocked`, or `completed`.
4. Record evidence or blockers next to the state, not only in chat.
5. Report any mismatch between claimed state and available evidence.

Use [references/task-state-template.md](references/task-state-template.md) only when no local format exists. Do not require a docs directory, labels, a branch scheme, or a fixed transition sequence.

When milestone context is supplied, update the selected task truthfully and return its evidence or blocker to the calling workflow. Do not own milestone placement, discovered-work routing, or milestone closure.

## State rules

- `planned`: intent and acceptance are visible enough to select later.
- `in-progress`: active work has started; preserve the current working surface when useful.
- `blocked`: name the blocking condition, its impact, and what would unblock it. Do not use it for ordinary uncertainty or incomplete work.
- `completed`: acceptance is satisfied and durable verification evidence is recorded. Do not equate “code written” with completion.

Update stale status when evidence clearly supports a non-destructive change. Ask when acceptance itself is ambiguous or changing it would hide unfinished scope.

## Closing safety

Inspect the current branch, worktree, uncommitted changes, and repository policy before proposing closing actions. Keep these actions as explicit gates:

- merge only after the user explicitly confirms the exact merge outcome;
- delete a branch or worktree only after explicit confirmation of the exact target;
- discard commits or uncommitted work only after fresh explicit confirmation of the exact work at risk.

Generic replies such as “continue”, “finish”, or “clean up” do not confirm merge, delete, or discard. Confirmation of merge does not imply confirmation of later deletion. Prefer recoverable cleanup when available and state what remains recoverable.

Use `handoff` when installed and cross-person continuation needs more operational context than the task record. It comes from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill handoff`.
