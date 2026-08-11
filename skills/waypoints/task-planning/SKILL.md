---
name: task-planning
description: Adapt an agreed Feature into a user-confirmed graph of independent, agent-ready child Tasks. Use when a Feature spans people, agent windows, harnesses, or sessions and needs durable ownership surfaces, blockers, shared contracts, safe parallelism, and independently verifiable handoffs before implementation.
---

# Task Planning

Apply Matt Pocock's `to-tickets` tracer-bullet principles to Waypoint's Feature-owned, repository-readable collaboration model.

## Establish readiness

1. Read repository instructions, `feature.md`, the agreed Feature specification, relevant technical design and code, tracker conventions, and current Feature state.
2. Require one stable Feature owner and a tracker-neutral Feature ID.
3. Stop when unresolved behavior would change Task Acceptance, or when an unresolved technical choice would change ownership, shared contracts, ordering, or safe parallelism. Return the decision to `feature-spec` or `technical-design`.
4. Treat approved behavior, public contracts, and repository facts as fixed inputs. Do not redesign them while splitting work.

A small Feature that one executor can safely complete in one fresh context does not need child Tasks. Do not require a tracker, Milestone, docs tree, branch convention, or implementation plan.

## Draft tracer-bullet Tasks

Create the smallest useful set of Tasks that can each be assigned, implemented, reviewed, verified, and safely integrated:

- Prefer a narrow complete path through behavior over horizontal fragments such as types, tests, database, or documentation.
- Keep implementation, tests, necessary docs, and review corrections inside the Task that owns the outcome.
- Size each Task for one fresh execution context. Split unrelated decisions or independently useful results; combine fragments that cannot remain correct and verifiable alone.
- Name stable ownership surfaces, consumed and provided contracts, and anything the Task must not change. Avoid speculative file lists.
- Record only real blockers. List order is never a dependency.
- Add a separate integration Task only when Task-local proof cannot cover a material cross-Task interaction.

Use expand–migrate–contract for a wide change that cannot stay correct as direct vertical slices. Keep old and new forms compatible, make migration batches independently safe, and block contraction on every migration.

Child Tasks remain inside their Feature. Cross-Feature dependencies bind to another Feature or its public contract, never to the other Feature's internal Task.

## Audit interference

Check the graph in both directions:

1. Coverage: every Feature Acceptance condition has an owner.
2. Ownership: parallel Tasks do not own the same mutable surface.
3. Contracts: producers and consumers use the same frozen interface, schema, lifecycle, or compatibility rule.
4. Mergeability: each Task can reach a safe MR boundary, or a real integration dependency is explicit.
5. Verification: every Task has local proof and only irreducible global proof remains at Feature level.

Resolve overlap by reshaping Tasks, freezing a shared contract in technical design, or adding a real blocker. Never claim conflict-free parallelism without repository evidence.

## Confirm before publishing

Present the proposed graph with each Task's outcome, ownership surface, blockers, independent proof, and shared-contract responsibility. Ask the user to confirm granularity, blockers, overlap, merge/split choices, and any integration Task. Iterate until approved.

Approval authorizes only the task plan and child Task records. It does not assign any Task or authorize implementation.

## Publish Feature-owned Tasks

Follow an existing tracker and repository convention. Otherwise use [references/task-plan-template.md](references/task-plan-template.md).

- Keep `task-plan.md` beside the Feature as the coordinating DAG.
- Keep each Task's durable contract under `features/<feature>/tasks/<task>/task.md` or the repository-native equivalent.
- Keep live status, assignee, executor, MR, and blocker state in an external tracker, or in `local-work-tracker` only after the user explicitly initialized it. With neither tracker, publish the durable graph, require user-directed assignment, report that claims are not atomic, and do not initialize tracking.
- Keep a generated, linked Task checklist in `feature.md` whether status comes from an external or local tracker.
- Use stable Feature/Task IDs independent of tracker issue numbers.
- Preserve completed Tasks and stable contracts while replanning. Only the Feature owner may confirm graph or shared-contract changes.

Report ready, blocked, safely parallel, and still-unassigned Tasks, then stop. Never assign yourself a Task, invoke implementation, edit production code, or treat planning approval, `ok`, `continue`, or automatic tool approval as execution authorization.

## Companion skills

Use Matt Pocock's `grilling` for unresolved intent, `codebase-design` for seam reasoning, `to-tickets` as the source methodology, and `handoff` when a confirmed Task moves to another harness. Install only the needed companion with `npx skills add mattpocock/skills --skill <name>`.
