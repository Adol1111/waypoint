<div align="center">

# Waypoint Skills

**Durable engineering context without a mandatory workflow**

Keep agent-driven work recoverable across sessions, models, and collaborators.

[中文](README_CN.md) · [Architecture](ARCHITECTURE.md) · [Skills](#standalone-skills) · [Workflows](#choose-a-workflow) · [Installation](#installation)

</div>

Waypoint provides small, standalone agent skills that preserve the engineering facts worth carrying forward: terminology, consequential decisions, delivery slices, behavioral task boundaries, technical designs, risky execution strategy, verification evidence, and safe closing state.

> [!IMPORTANT]
> Every atomic skill works independently. Optional workflows coordinate them without making a fixed `docs/` layout, task tracker, branch convention, review cadence, or commit sequence mandatory.

During implementation, optional does not mean absent: `task-execution-simple` chooses isolation from repository and collision risk, creates cohesive verified commits before advancing when permitted, and reports why when work must remain uncommitted.

## Why Waypoint?

Agent conversations are temporary; engineering decisions and proof should not be. Each atomic Waypoint skill follows the same lightweight contract:

1. Read the repository's existing practice and relevant artifacts.
2. Update a suitable artifact when one already exists.
3. Otherwise propose the smallest useful local Markdown artifact.
4. Keep review-critical facts in the repository—not only in chat.

## Standalone skills

Install or invoke only the skill needed for the current outcome.

| Skill | Use it to |
| --- | --- |
| [`domain-context`](skills/waypoints/domain-context/SKILL.md) | Maintain durable terminology and create only qualifying ADRs |
| [`roadmap-planning`](skills/waypoints/roadmap-planning/SKILL.md) | Shape goals into verifiable slices, or score backlog outcomes and plan a confirmed Milestone task batch |
| [`task-spec`](skills/waypoints/task-spec/SKILL.md) | Define reviewable task behavior and requirements without prescribing implementation |
| [`technical-design`](skills/waypoints/technical-design/SKILL.md) | Make review-critical architecture and implementation choices durable before coding |
| [`implementation-plan`](skills/waypoints/implementation-plan/SKILL.md) | Plan real sequencing, migration, compatibility, or rollout risk |
| [`task-state`](skills/waypoints/task-state/SKILL.md) | Preserve acceptance, status, blockers, evidence, and safe closing state |
| [`task-execution-simple`](skills/waypoints/task-execution-simple/SKILL.md) | Implement supplied scope with adaptive isolation, verification, and Git checkpoints |
| [`docs-workflow-bootstrap`](skills/setup/docs-workflow-bootstrap/SKILL.md) | Optionally scaffold a lightweight shared docs convention |

Example invocations:

```text
Use $task-spec to make this change reviewable without relying on this chat.
Use $technical-design to design the technical approach without writing a coding recipe.
Use $roadmap-planning to turn this goal into independently verifiable slices.
Use $task-execution-simple to implement the supplied task.
```

## Installation

The commands below install from the published `Adol1111/waypoint` repository. Contributors working from a local checkout can use `./skills` as the source; that intentionally excludes ignored development-only skills elsewhere in the working tree.

List the skills available from a source:

```bash
npx skills add Adol1111/waypoint --list
```

Install one standalone skill:

```bash
npx skills add Adol1111/waypoint --skill task-spec
```

Repeat `--skill` to install a selected set. Installation is project-local by default; add `-g` for a user-level installation or `-a codex` to target a specific supported agent.

Install every Waypoint skill:

```bash
npx skills add Adol1111/waypoint --skill '*'
```

The [`skills` CLI](https://github.com/vercel-labs/skills) supports Codex, Claude Code, Cursor, and other Agent Skills-compatible tools.

## Choose a workflow

Waypoint has two optional workflows. They share the same atomic skills but provide different amounts of coordination.

| Workflow | Choose it when | Behavior |
| --- | --- | --- |
| [`waypoint-workflow`](skills/workflows/waypoint-workflow/SKILL.md) | You want lightweight, request-local guidance | Reads existing evidence, recommends exactly one atomic skill, and keeps no Milestone state |
| [`milestone-workflow`](skills/workflows/milestone-workflow/SKILL.md) | Delivery spans tasks or sessions and needs global recovery | Maintains Milestone outcomes, exit criteria, task placement and status, discovered work, evidence, and closure |

Both workflows are explicitly invoked; installing one does not let it take over ordinary requests.

### Lightweight workflow bundle

Installing only `waypoint-workflow` is technically valid, but it may recommend an atomic skill that is not installed. For complete routing coverage, install the workflow plus all seven engineering waypoints:

```bash
npx skills add Adol1111/waypoint \
  --skill waypoint-workflow \
  --skill domain-context \
  --skill roadmap-planning \
  --skill task-spec \
  --skill technical-design \
  --skill implementation-plan \
  --skill task-state \
  --skill task-execution-simple
```

Invoke it with:

```text
Use $waypoint-workflow to recommend the next atomic waypoint.
```

### Milestone-managed workflow bundle

`milestone-workflow` coordinates the same seven atomic waypoints and adds durable Milestone governance:

```bash
npx skills add Adol1111/waypoint \
  --skill milestone-workflow \
  --skill domain-context \
  --skill roadmap-planning \
  --skill task-spec \
  --skill technical-design \
  --skill implementation-plan \
  --skill task-state \
  --skill task-execution-simple
```

Invoke it with:

```text
Use $milestone-workflow to plan, continue, or close this delivery.
```

Add `docs-workflow-bootstrap` to either bundle only when the team wants Waypoint to initialize a shared local docs convention:

```bash
npx skills add Adol1111/waypoint --skill docs-workflow-bootstrap
```

> [!NOTE]
> Milestone management and docs bootstrap are opt-in. Missing docs never select either one automatically, and neither workflow prevents direct use of an atomic skill. If you want no workflow, install only the standalone skills you choose.

## Optional docs convention

Teams that want shared repository-local documentation can invoke `docs-workflow-bootstrap`. If the request does not already say whether Milestones are wanted, bootstrap asks before creating task docs.

| Bootstrap choice | Task structure |
| --- | --- |
| Standalone | Flat active/completed/deferred task index |
| Milestone-managed | Open/completed Milestone index, backlog, and linked task-local artifacts |

Both choices may include `docs/context/` and `docs/architecture/decisions/`. In the local Milestone convention, confirming a task creates a non-empty `<milestone>/<task>/task.md` planning handoff and links it from the Milestone index. The index contains global outcome, selection, linked exit criteria, and an ordered ``- `status` [Task](...)`` list. Top-to-bottom order suggests execution sequence; Mermaid appears only for real cross-task dependencies. When development begins, `task-spec` creates or updates a separate spec and writes canonical Acceptance plus existing artifact links to `task.md`, replacing superseded planning fields. Technical design and plan files remain threshold-driven and follow repository-native names. Existing repository locations always take precedence, and bootstrap does not create placeholder Milestones or tasks.

Milestone `Discovered Work` is not a development log. Current-task corrections stay with that task, and findings already owned by another current task go directly there. Only work the Milestone cannot handle now, or whose owner is uncertain, is recorded globally; closure routes it durably or records why it was discarded.

In the Milestone convention, backlog is an active queue of scored candidate outcomes rather than a history log. Waypoint follows an existing scoring system or suggests an evidence-backed `0–10` score and rationale. Before scoring, the user may optionally discuss product gaps and add concrete candidates; sparse or stale backlogs receive one non-blocking reminder. The user chooses an approximate Milestone task count, or confirms an agent proposal. Leading candidates are expanded only far enough to reveal atomic tasks: one backlog outcome that becomes three tasks uses three places. Tasks are meaningful one-spec delivery units that include implementation and verification, not isolated actions. Timeboxes are optional external constraints, not defaults. Selected outcomes leave backlog only after durable ownership; unchanged scores receive no review log.

## Companion skills

Waypoint deliberately does not copy general-purpose protocols. The following optional companions come from [**mattpocock/skills**](https://github.com/mattpocock/skills):

| Skill | Purpose | Details |
| --- | --- | --- |
| `grilling` | Sustained clarification and stress-testing | [skills.sh](https://www.skills.sh/mattpocock/skills/grilling) |
| `research` | Research grounded in primary sources | [skills.sh](https://www.skills.sh/mattpocock/skills/research) |
| `codebase-design` | Module, interface, seam, and deep-design reasoning | [skills.sh](https://www.skills.sh/mattpocock/skills/codebase-design) |
| `tdd` | Red-green-refactor implementation | [skills.sh](https://www.skills.sh/mattpocock/skills/tdd) |
| `code-review` | Independent standards and specification review | [skills.sh](https://www.skills.sh/mattpocock/skills/code-review) |
| `handoff` | Cross-session or cross-collaborator continuation | [skills.sh](https://www.skills.sh/mattpocock/skills/handoff) |

### Installing across both repositories

Waypoint and its companions have different sources, so install them with separate commands. The companions are not required for either workflow; install only the protocols you want available.

Install all six companions:

```bash
npx skills add mattpocock/skills \
  --skill grilling \
  --skill research \
  --skill codebase-design \
  --skill tdd \
  --skill code-review \
  --skill handoff
```

Or replace the repeated `--skill` arguments with the single companion you need. They are optional integrations, not Waypoint dependencies.

For a complete local Waypoint installation plus all companions:

```bash
npx skills add Adol1111/waypoint --skill '*'
npx skills add mattpocock/skills \
  --skill grilling \
  --skill research \
  --skill codebase-design \
  --skill tdd \
  --skill code-review \
  --skill handoff
```

## Non-goals and safety

Waypoint is not:

- a Superpowers/OpenSpec-style mandatory lifecycle;
- a tracker state machine, label system, or Milestone requirement for every user;
- a fixed review cadence, commit per phase, or prescribed commit sequence;
- a branch or worktree policy;
- a replacement for interviewing, research, TDD, review, or handoff skills.

Explicit confirmation is reserved for consequential closing operations: merge, deleting a branch or worktree, and discarding work. Confirmation must identify the action and target; “continue” or “finish” is not enough.

This does not leave stable work indefinitely uncommitted. Routine isolation and cohesive task commits use repository practice, task risk, and user direction; only their sequence is not prescribed.

## Validation

Run the focused contract suite with Python's standard library:

```bash
python3 -m unittest discover -s tests -v
```

The suite validates independent no-`docs/` usage, both bootstrap choices, lightweight coordinator recommendations, optional backlog enrichment, scored atomic-task Milestone selection, Milestone discovery and closure rules, separation of chat-independent behavioral specifications from technical designs, destructive closing confirmation, frontmatter, `agents/openai.yaml`, template ownership, and fixture pairing. See [ARCHITECTURE.md](ARCHITECTURE.md) for the atomic-skill contract and safety boundaries.

## Releases

Waypoint uses [Changesets](https://github.com/changesets/changesets) to collect release notes and create versioned GitHub changelogs.

For a user-visible skill or workflow change:

```bash
pnpm install --frozen-lockfile
pnpm changeset
```

Commit the generated `.changeset/*.md` fragment with the change. After it reaches `main`, the release workflow creates or updates a Version PR. Merging that PR updates `CHANGELOG.md`, removes consumed fragments, creates the version tag, and publishes the corresponding GitHub release. Documentation-only, test-only, and internal maintenance changes do not normally need a fragment.
