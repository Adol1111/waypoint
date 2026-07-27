---
name: roadmap-planning
description: Turn product or engineering goals into independently verifiable delivery slices while preserving unresolved decisions. Use when a roadmap, milestone outline, delivery sequence, or coarse task breakdown is needed; prefer vertical user-facing slices and allow named preparatory work only when it unblocks a capability.
---

# Roadmap Planning

Shape direction into outcomes that can be delivered and verified independently.

## Work independently

1. Read repository instructions, existing roadmaps or issue conventions, relevant product context, and the current request.
2. Update the existing roadmap artifact when one fits. Otherwise propose the smallest useful Markdown artifact in a repository-consistent location.
3. State the goal, constraints, current evidence, and success signals before decomposing.
4. Produce only enough slices to make delivery order and proof visible.
5. Preserve open decisions precisely and vague future questions at their current level of uncertainty.

Do not require a docs layout, task tracker, labels, milestone hierarchy, workflow stage, or confirmation state.

When `milestone-workflow` supplies a milestone outcome or exit criteria, use them as planning context and return candidate slices without taking ownership of global milestone status, discovered-work routing, or closure.

## Slice well

- Prefer vertical slices that expose a user- or operator-visible capability across the necessary layers.
- Give each slice an observable outcome, boundaries, dependencies, and independent verification.
- Separate slices when they can ship, be reviewed, or fail independently.
- Keep them together when separation would create infrastructure with no independently useful outcome.
- Add refactor, migration, spike, or risk-reduction work only when it explicitly unblocks a named capability. State that link and its exit evidence.
- Keep ordering adaptive. Distinguish hard dependencies from a preferred sequence.

Do not turn every uncertainty into tasks. Record a specific unresolved choice as an open decision with its impact and decision point. Preserve a vague future question without inventing owners, dates, or a large speculative tree.

Use [references/roadmap-template.md](references/roadmap-template.md) only when no local form exists.

## Companion skills

Use `grilling` for unresolved product direction and `research` for material external uncertainty when installed. These companions come from [mattpocock/skills](https://github.com/mattpocock/skills) and can be installed with `npx skills add mattpocock/skills --skill <name>`. Send a concrete slice to `task-spec` only when the user asks for task-level specification; roadmap work does not authorize implementation.
