# Waypoint contributor guidance

- Keep every skill independently usable. Do not make an atomic waypoint depend on a workflow, bootstrap, fixed docs tree, tracker, branch policy, or commit sequence.
- Put durable artifact templates only in the skill that owns that artifact.
- Keep workflow skills under `skills/workflows/`, atomic engineering waypoints under `skills/waypoints/`, and opt-in repository setup under `skills/setup/`.
- Keep `SKILL.md` frontmatter limited to `name` and `description`. Put OpenAI invocation policy in `agents/openai.yaml`.
- Require explicit, target-specific confirmation only for merge, branch/worktree deletion, and discarding work.
- Update English and Chinese README guidance together.
- Run `scripts/validate.sh` after changing skills, metadata, templates, fixtures, or documentation links.
- Treat `/Users/gaoxiaoyi/projects/skills/doc-driven-spec-workflow` as read-only reference material. Never apply or alter its stash.
