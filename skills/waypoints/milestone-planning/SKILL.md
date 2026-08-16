---
name: milestone-planning
description: Select or revise a shared Milestone as a frozen batch of owned Features from a requirement pool, and reconcile completed Features into a concise global history. Use for backlog scoring, shared iteration or release scope, Feature ownership, cross-Feature dependencies, exit coverage, completion indexing, or explicit Milestone replanning; never decompose Feature Tasks or drive implementation.
---

# Milestone Planning

Turn requirement candidates into a shared, reviewable Feature commitment without creating a serial execution queue.

## Prepare the candidate pool

1. Read repository instructions, the full requirement pool, active and completed Milestones, current product evidence, incidents, dependencies, and supplied constraints.
2. Reconcile completed, duplicate, obsolete, and partially selected outcomes before scoring. Preserve vague future questions without inventing delivery structure.
3. Follow an existing priority model. Otherwise recommend one evidence-backed `0–10` score using impact, delay cost, explicit commitments, risk, strategic value, and unblocking value.
4. Score Feature candidates, not their future Tasks. Keep hard dependencies separate from priority.

Use [references/requirement-pool-template.md](references/requirement-pool-template.md) only when no stronger pool or tracker convention exists.

Consume a selected candidate only after its Feature record is durable. Remove a wholly selected requirement from the active pool in the same change that materializes the Feature. For partial selection, materialize the selected outcome, rewrite the unselected remainder as a bounded candidate, and rescore it. Never keep the same full outcome authoritative in both the requirement pool and a Feature. Using this skill is optional; Features may be created and delivered without a Milestone. When the repository has chosen Milestone-grouped fallback documentation, materialize the Feature at `milestones/<milestone>/features/<feature>/feature.md`; otherwise create or preserve its single repository-native Feature record and link it from the Milestone.

## Resolve stable actors

Reuse an owner or coordinator already recorded in the Feature, Milestone, or configured external tracker. Otherwise use an identity explicitly supplied by the current request. If the current actor is still needed, read `.waypoint/local.yaml` directly when it exists, even when `local-work-tracker` was not invoked or installed, and use its `actor_id` as the current actor identity. If the file is absent, invalid, or does not answer which participant should own the work, ask the user. Never infer ownership from Git author metadata, a harness, machine, branch, or temporary window label.

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

After the batch is confirmed, add a Feature dependency DAG when at least one real blocking edge exists. Include every required Feature as a node so disconnected nodes make parallel work visible. Draw each edge from prerequisite to dependent and label it with the public contract or completion gate when the relationship is not obvious. Never infer an edge from priority, list order, shared ownership, delivery preference, or an internal Task. The graph explains stable coordination structure; it is not a serial execution queue or a live status board.

## Publish without duplicating state

Follow the repository's tracker and documentation convention. Otherwise use:

- [references/milestone-template.md](references/milestone-template.md) for the shared Milestone;
- [references/feature-handoff-template.md](references/feature-handoff-template.md) for each selected Feature.

When the repository uses Milestone-grouped fallback documentation, keep each Milestone as one directory containing `milestone.md` and its newly materialized `features/<feature>/` directories. In a repository that keeps standalone flat Features, keep those paths and let the Milestone link them. Feature IDs remain globally unique in either layout. Before Feature execution begins, explicit replanning may move the entire Feature directory and update every durable reference and tracker path in the same change. Once execution has begun, keep its path stable and let a later Milestone link the carried Feature rather than moving files underneath active branches.

Keep live status, assignment, and priority in the external tracker when one exists. When the user has explicitly initialized `local-work-tracker`, use its records instead. With neither tracker, keep only the confirmed Feature owners and planning facts in repository-native Markdown, report the collaboration limitation, and never initialize tracking implicitly. Keep the Milestone as a compact linked Feature view; do not copy child Task state into it or encode live status in the DAG. Update the graph only when explicit replanning changes a Feature or a cross-Feature dependency.

Feature status may summarize child Tasks, but only the Feature owner can confirm Feature completion after Feature Acceptance and integration proof pass. The Milestone completes only when exit criteria and required Features are complete and the coordinator confirms closure.

## Reconcile completed Features

After the Feature owner confirms Acceptance and integration proof, keep the Feature directory as the durable detailed record, remove it from the active Feature view, and add one entry to the repository's completed-Feature index. Use [references/completed-feature-index.md](references/completed-feature-index.md) only when no stronger convention exists.

Keep the index ungrouped and newest-first. Record only the completion date, Feature link, and an optional one-sentence outcome. Do not copy owner, Tasks, MR, verification, or Milestone detail. The index is history, not a second live-status authority. With an external tracker, follow its accepted completion event; with `local-work-tracker`, let its coordinator render the entry. Otherwise the Milestone coordinator is the single writer so parallel Feature branches do not contend on one global file.

Finish after reporting planned, blocked, dependency-ready, and newly reconciled completed Features. Do not invoke Feature specification, Task planning, or implementation.

## Companion skills

Use `grilling` for unresolved product direction and `research` for material external uncertainty when installed. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and remain optional.

Install only the needed companion with `npx skills add mattpocock/skills --skill <name>`.
