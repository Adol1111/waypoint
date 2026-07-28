---
name: task-execution-simple
description: Implement a supplied engineering task or specification directly with context-appropriate isolation, verification, documentation updates, and companion skills. Use when the requested scope is implementable without requiring Waypoint's optional docs convention or any fixed task structure.
---

# Task Execution Simple

Implement the supplied scope and leave truthful evidence.

## Work independently

1. Read repository instructions, the supplied task or spec, relevant code and tests, and current version-control state.
2. Confirm the task is implementable. If behavior or boundaries are materially ambiguous, surface the need for a task specification; if review-critical architecture, interfaces, data or state models, algorithms, concurrency, security, performance, or test seams are unresolved, surface the need for technical design; if risky order is unresolved, surface the need for an implementation plan.
3. Before editing, state a concise approach preview: the change surface, core strategy, material constraints, and verification seam. Do not create a formal artifact for straightforward work.
4. Choose isolation based on repository practice, current dirty state, collision risk, task size, and user direction. Do not assume a task branch or worktree is required.
5. Implement only the supplied scope. Preserve unrelated user changes.
6. Run the most relevant practical verification and inspect the resulting diff.
7. Update existing docs or task state when implementation changes their stated facts or when requested.
8. Report result, verification evidence, residual risk, and current working state.

Do not require another local skill, a docs layout, tracker, branch convention, mandatory commit, or fixed review pause.

Report durable out-of-scope discoveries without silently expanding the task. When milestone context was supplied, identify their impact and source clearly enough for the calling workflow to record and classify them.

Do not bury a material technical decision in code. Follow an established repository decision when evidence is clear and record it in an existing suitable artifact when it remains review-critical. When genuine alternatives would materially change the result, stop before editing and ask for the missing decision; another local skill is never a prerequisite for using this one.

## Adaptive verification

Prefer the highest-signal seam available: focused tests, type or static checks, integration checks, build, runtime exercise, or targeted manual evidence. Record commands and outcomes durably when completion depends on them. Do not claim completion when required checks failed or were not run; state the limitation.

Preserve the intent of existing tests. Do not silently delete, skip, loosen, or rewrite an assertion merely to make the implementation pass. When an intentional behavior change makes a test obsolete, make the changed contract and replacement evidence explicit in the task artifact or completion report.

Use an installed `tdd` skill when test-first development fits the change. Use `code-review` for risk, complexity, or user-requested independent review. Use `research` for unstable external facts. Use `handoff` when execution will continue with another collaborator. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`. They are companions, not prerequisites.

## Safe finish

Use the repository's existing task artifact when acceptance or status should be updated; otherwise keep the report concise. If isolated work exists, require explicit confirmation before merging, deleting a branch or worktree, or discarding commits or uncommitted work. Make the action and target explicit; confirmation of merge does not authorize later deletion. Never infer destructive authorization from a request to finish.
