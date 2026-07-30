---
name: task-state
description: Maintain a recoverable task checkpoint in an existing tracker or minimal Markdown artifact. Use when work is planned, paused, handed off, blocked, or completed, and when isolated branch or worktree changes may be merged, deleted, or discarded.
---

# Task State

Maintain a checkpoint, not a process log.

## Update the task

1. Find the repository's existing issue, task file, checklist, roadmap entry, or other state convention.
2. Update it in place. If none exists and a durable checkpoint is useful, propose the smallest repository-consistent Markdown record.
3. Use acceptance checkboxes as the primary progress record and set `planned`, `in-progress`, `blocked`, or `completed` from the definitions below.
4. Add only the state required by the current branch:
   - while work continues: update satisfied acceptance;
   - when stopping or handing off: add a recovery checkpoint only for context another session cannot readily reconstruct;
   - when blocked: record the blocker;
   - when completing: replace transient recovery state with one final verification summary.
5. Report any mismatch among status, acceptance, blocker, and final verification.

Finish when the artifact states the current truth without preserving routine activity. Use [references/task-state-template.md](references/task-state-template.md) only when no local format fits. Require no docs directory, labels, branch scheme, or fixed transition sequence.

With milestone context, update only the selected task and return its result or blocker to the workflow; milestone placement, discovered-work routing, and closure remain workflow-owned.

## State definitions

- `planned`: the outcome and planning boundary are visible enough to select later; stage proof may stand in until task specification refines acceptance.
- `in-progress`: work has started and at least one acceptance item or recovery fact remains open.
- `blocked`: a named condition prevents progress; record its impact and the event or decision that would unblock it.
- `completed`: every acceptance item is satisfied and one final verification summary reflects the final implementation state.

Update stale status when evidence clearly supports a non-destructive change. Ask when acceptance itself is ambiguous or changing it would hide unfinished scope.

## Acceptance

Mark `[x]` only after the observable condition is satisfied and verified. Leave compound criteria open while any part remains.

Treat specifications, designs, plans, and research as inputs rather than progress. Artifact existence is normally visible; add links only when they materially improve navigation. Grilling is optional and leaves no task-state marker.

## Recovery checkpoint

Create a checkpoint only when work is stopping, handing off, or blocked and live repository inspection cannot recover enough context:

- `Remaining`: unresolved acceptance, decision, or review finding;
- `Next`: the next meaningful action.

During uninterrupted execution-review loops, address findings directly. At a stopping boundary, preserve only unresolved findings that would otherwise live only in chat: state the concrete finding, affected surface, and required follow-up, or link the durable PR/review comment that already owns them. Remove resolved findings instead of retaining review history.

Keep task-semantic recovery in the checkpoint. Add a separate Working State note only for non-obvious branch, worktree, uncommitted, or transient state needed for safe continuation; prefer live version-control inspection for ordinary facts. Remove Recovery and Working State when work resumes or completes.

Use `handoff` when installed and cross-person continuation needs more operational detail than this checkpoint. It comes from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill handoff`.

## Verification

Keep routine test, build, lint, and formatting runs in execution context and rerun them against current code when needed. The task carries no running command history.

Preserve intermediate verification only when it retires a material risk and is expensive or impossible to reproduce, depends on an external system, or remains valid independently of ordinary code changes. Record its conclusion and scope.

On completion, write one concise final verification summary after the final changes. State the checks or review, their outcomes, and the acceptance they demonstrate. Link the verified revision, PR, CI run, release, or artifact when one exists. A date or command alone proves nothing.

## Selection and timing context

When timing affects later selection, preserve only an observed signal: `Why now` for current priority, `Start when` for a real precondition, or `Revisit when` for deferred work. Omit absent timing context rather than inventing dates, priorities, or dependencies. Runtime behavior belongs in the specification; roadmap placement belongs in the planning system.

## Closing safety

Inspect the current branch, worktree, uncommitted changes, and repository policy before proposing closing actions. Keep these actions as explicit gates:

- merge only after the user explicitly confirms the exact merge outcome;
- delete a branch or worktree only after explicit confirmation of the exact target;
- discard commits or uncommitted work only after fresh explicit confirmation of the exact work at risk.

Generic replies such as “continue”, “finish”, or “clean up” do not confirm merge, delete, or discard. Confirmation of merge does not imply confirmation of later deletion. Prefer recoverable cleanup when available and state what remains recoverable.
