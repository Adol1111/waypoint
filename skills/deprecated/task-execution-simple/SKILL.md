---
name: task-execution-simple
description: Deprecated archive of the former Waypoint implementation skill. Do not use for new work; explicitly assign an implementation-ready Feature or Task and invoke Matt Pocock's implement skill.
---

> [!WARNING]
> Deprecated snapshot. Explicitly invoke Matt Pocock's `implement` skill for new work. This file is retained only for migration reference.

# Task Execution Simple

Implement the supplied scope and leave a verified, recoverable result.

## Work independently

1. Read repository instructions, the supplied task or spec, relevant code and tests, and current version-control state.
2. Confirm the task is implementable from repository evidence. Stop before editing only when a missing behavioral boundary, technical choice, or execution-order decision would materially change the result. Name the missing decision and why current evidence does not decide it so the user can resolve it directly or capture it in a suitable artifact.
3. Before editing, state a concise approach preview: the change surface, core strategy, material constraints, and verification seam. Do not create a formal artifact for straightforward work.
4. Choose isolation before editing. Reuse suitable existing isolation. Create a branch or worktree for non-trivial work on a default or shared branch, possible collision with existing dirty changes, parallel work, or likely cross-session execution. Stay in place for a small safe change or explicit user direction.
5. Implement only the supplied scope. Preserve unrelated user changes.
6. Run the most relevant practical verification, complete the implementation-review correction loop, and inspect the resulting diff.
7. Update existing docs or task state when implementation changes their stated facts or when requested.
8. Before advancing to another task or waypoint, create a cohesive Git checkpoint for stable scoped changes when repository policy and user direction permit routine commits. Include task documents whose truth changed.
9. If a checkpoint is intentionally unavailable, report the exact reason and uncommitted surface instead of silently continuing with completed work.
10. Report result, verification, residual risk, commit or uncommitted state, and any closing action still awaiting confirmation.

Finish only when acceptance is satisfied, final verification reflects current code, review findings are resolved, and stable changes are committed or explicitly accounted for. Do not require another local skill, docs layout, tracker, branch convention, fixed commit sequence, or review pause.

Report durable out-of-scope discoveries without silently expanding the task. When milestone context was supplied, identify their impact and source clearly enough for the calling workflow to record and classify them.

Treat established technical choices as repository evidence. Keep a review-critical choice visible in an existing suitable artifact; otherwise keep the work focused on the supplied scope.

## Adaptive verification

Prefer the highest-signal seam available: focused tests, type or static checks, integration checks, build, runtime exercise, or targeted manual evidence. Record commands and outcomes durably when completion depends on them. Do not claim completion when required checks failed or were not run; state the limitation.

Preserve the intent of existing tests. Do not silently delete, skip, loosen, or rewrite an assertion merely to make the implementation pass. When an intentional behavior change makes a test obsolete, make the changed contract and replacement evidence explicit in the task artifact or completion report.

## Adaptive Git checkpoints

Treat branch/worktree creation and task-scoped commits as routine, reversible progress when they are within the implementation request. Preserve repository practice and explicit user direction.

Commit at a stable, reviewable boundary. Prefer one cohesive final task commit for small work. Split only when parts are independently understandable and verified, or repository practice requires it; do not manufacture commits per file, layer, plan step, or review round. Review may continue after a commit through follow-up commits or later squash.

Keep stable specifications, designs, plans, task updates, and implementation together when they form one reviewable change. Commit a document earlier when another session, collaborator, or implementation step will depend on that stable waypoint.

Never include unrelated user changes. When scoped and unrelated work cannot be separated safely, or the user or repository forbids commits, leave the work uncommitted and report why.

Use an installed `tdd` skill when test-first development fits the change. Use `code-review` for risk, complexity, or user-requested independent review. Use `research` for unstable external facts. Use `handoff` when execution will continue with another collaborator. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`. They are companions, not prerequisites.

## Safe finish

Use the repository's existing task artifact when acceptance or status should be updated; otherwise keep the report concise. If isolated work exists, require explicit confirmation before merging, deleting a branch or worktree, or discarding commits or uncommitted work. Make the action and target explicit; confirmation of merge does not authorize later deletion. Never infer destructive authorization from a request to finish.
