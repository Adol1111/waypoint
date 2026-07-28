---
name: docs-workflow-bootstrap
description: Optionally scaffold or adapt one of two lightweight shared Markdown conventions covering flat standalone task docs and milestone-managed delivery docs. Use when a team wants repository-local engineering documentation; when the preference is absent, ask whether Milestone management is wanted before creating the task structure.
---

# Docs Workflow Bootstrap

Create only the shared documentation convention the repository will actually use.

## Inspect before asking

1. Read repository instructions and existing documentation, ADR, issue, roadmap, and planning conventions.
2. Reuse and extend existing locations when possible. Do not create a parallel `docs/` tree beside a working convention.
3. Determine whether the user already chose a workflow:
   - no Milestone management: standalone atomic skills or `waypoint-workflow`;
   - Milestone management: `milestone-workflow`.
4. If the choice is absent and a task structure would be created, ask one direct question: whether the team wants Milestone-managed delivery.
5. Do not create either task structure until that answer is known.
6. Finish when the report identifies the chosen convention, every reused or created location, and any deliberately omitted structures.

The user may explicitly request only glossary or ADR locations without task tracking. In that case, create only those accepted locations and do not ask an irrelevant Milestone question.

## Standalone convention

Use [references/standalone-convention.md](references/standalone-convention.md) when the user does not want Milestone management.

- Keep one flat task index.
- Let atomic skills work directly from tasks, issues, or supplied requests.
- Do not create milestone state, exit criteria, discovered-work routing, or milestone backlog semantics.

## Milestone convention

Use [references/milestone-convention.md](references/milestone-convention.md) when the user chooses Milestone management.

- Create a global task index with open and completed Milestones.
- Create a backlog destination for concrete deferred work.
- Let `milestone-workflow` create real milestone artifacts when real milestone content exists.
- Do not create empty milestone directories or invented roadmap content during bootstrap.

## Shared boundaries

Offer `docs/context/` for glossary and durable context and `docs/architecture/decisions/` for qualifying ADRs in either convention. Let the user accept only useful parts.

Do not create substantive glossary entries, ADRs, roadmap slices, task specs, technical designs, plans, or implementation changes while bootstrapping. Do not create labels, confirmation flags, mandatory lifecycle, branch policy, fixed review cadence, hierarchy beyond the selected convention, or commit sequence.
