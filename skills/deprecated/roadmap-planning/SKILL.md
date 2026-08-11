---
name: roadmap-planning
description: Deprecated archive of the former roadmap and Milestone task-batch planner. Do not use for new work; use milestone-planning for shared Feature selection, ownership, dependencies, and replanning.
---

> [!WARNING]
> Deprecated snapshot. Use `milestone-planning` for new work. This file is retained only for migration reference.

# Roadmap Planning

Shape direction into outcomes that can be delivered and verified independently.

## Establish the planning boundary

1. Read repository instructions, existing roadmaps or issue conventions, relevant product context, and the current request.
2. Update the existing roadmap artifact when one fits. Otherwise propose the smallest useful Markdown artifact in a repository-consistent location.
3. State the goal, constraints, current evidence, and success signals before decomposing.
4. Select the branch that matches the request:
   - for a standalone goal, shape a few independently verifiable delivery slices directly, using [references/roadmap-template.md](references/roadmap-template.md) only when no local form exists;
   - for a new Milestone, prepare and score candidates before forming the task batch, then read [references/milestone-planning-handoff.md](references/milestone-planning-handoff.md) before placing the confirmed result;
   - for an existing Milestone, read the same handoff reference and reconcile its delivery map.
5. Preserve precise open decisions and keep vague future questions at their current level of uncertainty.

Remain usable without a docs layout, task tracker, labels, milestone hierarchy, workflow stage, or confirmation state.

When `milestone-workflow` supplies a Milestone outcome or exit criteria, return a complete candidate delivery map at planning granularity. Global Milestone status, task placement, discovered-work routing, and closure remain with that workflow.

## Prepare candidate work

Build a new Milestone batch from durable evidence and the full candidate set, rather than only the latest prompt or first backlog item.

1. Recover completed and open Milestones, user feedback, capability gaps, incidents, research, Future Directions, open decisions, dependencies, and the full backlog.
2. Optionally enrich the candidate set before scoring. Do this when the user asks, or offer one brief reminder when the backlog is empty, sparse, or visibly stale. A decline continues planning without another gate.
3. Use discussion, `grilling`, or `research` when chosen to explore product gaps, repeated requests, operational risks, and natural follow-ons from completed work.
4. Add only schedulable candidate outcomes with a rough boundary and plausible stage proof. Keep goal-shaped or vague ideas under Future Directions.
5. Reconcile duplicates, superseded work, and outcomes already completed elsewhere before scoring.

Candidate enrichment is opt-in. Add concrete user-approved or evidence-backed outcomes; leave speculative possibilities out of the active backlog.

## Score backlog candidates

Follow an existing repository scoring system when one exists. Otherwise use one evidence-backed holistic score from `0` to `10`:

- `9–10`: delay has significant and near-term cost;
- `7–8`: high value that deserves near-term consideration;
- `4–6`: clear value with limited current delay cost;
- `1–3`: low-impact, low-delay-cost, or opportunistic;
- `0`: recommend removal or closure, or preserve it as a Future Question instead of active backlog work.

Score the backlog candidate outcome, not the execution tasks later derived from it. Record one concise rationale based on user or business impact, delay cost, explicit commitments, strategic value, operational or security risk, and unblocking value. Do not require a component formula; use a repository's existing WSJF, RICE, or other model when present.

Keep dependencies explicit and separate from numeric priority. A prerequisite may receive the same or a higher score because it unlocks important work, especially when it unlocks several outcomes, while `Depends on` determines execution order.

Scan the full backlog before a Milestone selection. Rescore only when evidence changed; leave unchanged scores untouched and append no scoring history. When maintaining local Markdown without a stronger convention, sort by current score descending and keep equal-score order stable.

Agent-generated scores are recommendations. Ask the user when business value or strategic tradeoffs cannot be established from repository evidence, and let the user confirm the final Milestone boundary.

## Form a Milestone batch

1. Read the user's desired task count when supplied. Otherwise propose a compact batch after inspecting the leading candidates and ask the user to confirm it. Treat the number as a soft planning boundary, never a fixed repository default.
2. Treat a timebox, deadline, or release window as an optional constraint only when supplied by the user or repository.
3. Starting with the highest-scoring candidates, expand only the likely selections at planning granularity. One backlog outcome may become two or three Milestone tasks and consumes that many places in the batch.
4. Let atomicity and dependencies determine task boundaries. A smaller or larger set needs a visible reason and user agreement when it materially departs from the requested count.
5. Theme similarity is secondary. A Milestone may contain unrelated high-scoring outcomes when each selected task has a meaningful boundary.
6. Preserve the selected candidate scores and selection rationale once in the Milestone. Milestone tasks do not inherit scores; list them in the recommended execution sequence and model only real dependencies.
7. Transfer a candidate out of backlog after the Milestone durably owns its full selected outcome. When only a verifiable part is selected, rewrite the backlog entry as the remaining outcome and rescore it.

Milestone planning defines task boundaries, rough scope, success signals, dependencies, and any genuine cross-task integration need. Create the task spec and any warranted design or plan when development of the individual task begins.

## Place the planning result

Follow the repository's existing tracker and artifact convention:

- In a tracker, create or update one durable item for every confirmed atomic task and link those items from the Milestone.
- In a local Milestone folder convention, materialize the planning handoff from the Milestone reference as one non-empty task artifact for every confirmed atomic task.
- In a single-file convention, keep the task map compact and inline only the fields that have no other durable owner.

Keep the Milestone artifact as a linked global map. Keep each planning handoff in its task artifact when task artifacts exist. Every confirmed task receives one durable individual owner.

## Complete the Milestone map

Cover the whole Milestone before recommending its next task:

1. Check that the selected outcomes, optional external constraints, exit criteria, and material constraints are explicit.
2. Inventory completed, active, and proposed tasks that contribute to the selected outcomes. Preserve valid completed work rather than replanning it.
3. Link every exit criterion directly to the task or tasks that satisfy it. An uncovered criterion means the plan is incomplete: add a task, adjust the criterion, or preserve a genuinely global unresolved choice under Open Decisions.
4. Add the smallest missing meaningful tasks needed for complete coverage. Keep each at outcome level so task behavior and technical design remain with their owning skills.
5. Keep an ordered task link and status list in the Milestone index. Let top-to-bottom order express the recommended execution sequence, not a hard dependency. When cross-task start or completion dependencies exist, show them in a Mermaid graph and label completion or verification gates distinctly. Omit the graph when tasks are independent.
6. Preserve only global planning gaps as open decisions or future questions instead of hiding them inside an apparently complete task list.

A Milestone plan makes its full delivery shape and closure path reviewable. Task status and true dependencies are sufficient to recover what can proceed; do not add a global current-focus cursor.

Replan when selected outcomes or exit criteria change, discovered work changes coverage, a completed task invalidates an assumption, or a closure audit reveals a gap. Reconcile the affected remaining map while preserving stable completed work. Closing a Milestone reconciles and rescores affected backlog work; a new Milestone begins only with user direction.

## Shape atomic tasks

- Treat one task as the smallest meaningful engineering delivery that one spec can describe and that can be implemented, reviewed, handed off, verified, and completed independently.
- Permit a non-user-visible or partial capability only when it creates a bounded, verifiable state that is safe to retain and directly supports later work.
- Keep implementation, tests, necessary documentation, task-level verification, and review corrections inside the task.
- Keep file edits, endpoints, migration commands, test-writing steps, and other isolated actions inside the meaningful delivery they support.
- Split only when each result supports an independent spec and meaningful stage proof. Combine work that has value only as one outcome.
- When a backlog candidate expands into several tasks, count each atomic task toward the user-confirmed batch.
- Keep priority on backlog candidates and selected-outcome rationale. Express Milestone execution through list order and hard dependencies.
- Add Milestone-level integration proof only when task-local verification cannot cover a real cross-task interaction, compatibility, migration, release, or end-to-end risk. Make it a separate task only when the integration work is substantial.

Record a specific unresolved choice as an open decision with its impact and decision point. Preserve a vague future question without inventing owners, dates, or a speculative task tree.

## Completion criteria

Planning is complete when:

- the artifact reflects the requested branch and its durable evidence;
- each slice or atomic task has a meaningful outcome, rough boundary, and stage proof;
- a Milestone selection has a user-confirmed batch, durable ownership for every confirmed task, and reconciled ownership for selected and remaining backlog outcomes;
- every Milestone exit criterion links to its contributing tasks;
- real hard dependencies are visible without turning list order into a dependency;
- task-local details live in their task artifacts when the repository uses them, while the Milestone remains a linked global map;
- open decisions and future questions preserve their actual uncertainty;
- task-level specification, technical design, and implementation sequencing remain deferred until their owning work begins.

## Companion skills

Use `grilling` for unresolved product direction and `research` for material external uncertainty when installed. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`. Send a concrete slice to `task-spec` only when the user asks for task-level specification; roadmap work does not authorize implementation.
