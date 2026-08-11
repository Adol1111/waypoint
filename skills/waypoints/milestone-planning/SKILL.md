---
name: milestone-planning
description: Select or revise a shared Milestone as a frozen batch of owned Features from a requirement pool. Use for backlog scoring, shared iteration or release scope, Feature ownership, cross-Feature dependencies, exit coverage, or explicit Milestone replanning; never decompose Feature Tasks or drive implementation.
---

# Milestone Planning

Turn requirement candidates into a shared, reviewable Feature commitment without creating a serial execution queue.

## Prepare the candidate pool

1. Read repository instructions, the full requirement pool, active and completed Milestones, current product evidence, incidents, dependencies, and supplied constraints.
2. Reconcile completed, duplicate, obsolete, and partially selected outcomes before scoring. Preserve vague future questions without inventing delivery structure.
3. Follow an existing priority model. Otherwise recommend one evidence-backed `0–10` score using impact, delay cost, explicit commitments, risk, strategic value, and unblocking value.
4. Score Feature candidates, not their future Tasks. Keep hard dependencies separate from priority.

Use [references/requirement-pool-template.md](references/requirement-pool-template.md) only when no stronger pool or tracker convention exists.

## Select a shared Feature batch

Build a compact, user-confirmed batch. Every selected Feature needs:

- a tracker-neutral stable ID;
- one stable Feature owner, never only a temporary session ID;
- a bounded outcome and contribution to Milestone exit criteria;
- known cross-Feature dependencies expressed against a Feature or its public contract, never another Feature's internal Task;
- dependencies completed or backed by an explicit owner and delivery commitment;
- optional type: `feature`, `bug`, `maintenance`, or `migration`.

The Milestone has one coordinator and may contain Features owned by different people or durable agent identities. It does not contain child Tasks, maintain a global current item, require serial execution, or own a branch, commit, push, MR, or merge boundary.

Default to a frozen Feature batch. Do not refill it when one contributor becomes free. Contributors may assist ready Tasks or accept an explicit ownership transfer for an existing Feature. Add, remove, or transfer a Feature only through explicit replanning that records the change and reason.

Present the proposed Feature set, owners, dependencies, exit coverage, and material selection tradeoffs before publishing. Iterate until the user confirms the batch. Approval authorizes the Milestone artifact and Feature handoffs only, never Feature planning or implementation.

## Publish without duplicating state

Follow the repository's tracker and documentation convention. Otherwise use:

- [references/milestone-template.md](references/milestone-template.md) for the shared Milestone;
- [references/feature-handoff-template.md](references/feature-handoff-template.md) for each selected Feature.

Keep live status, assignment, and priority in the external tracker when one exists. When the user has explicitly initialized `local-work-tracker`, use its records instead. With neither tracker, keep only the confirmed Feature owners and planning facts in repository-native Markdown, report the collaboration limitation, and never initialize tracking implicitly. Keep the Milestone as a compact linked Feature view; do not copy child Task state into it.

Feature status may summarize child Tasks, but only the Feature owner can confirm Feature completion after Feature Acceptance and integration proof pass. The Milestone completes only when exit criteria and required Features are complete and the coordinator confirms closure.

Finish after reporting planned, blocked, and dependency-ready Features. Do not invoke Feature specification, Task planning, or implementation.

## Companion skills

Use `grilling` for unresolved product direction and `research` for material external uncertainty when installed. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and remain optional.

Install only the needed companion with `npx skills add mattpocock/skills --skill <name>`.
