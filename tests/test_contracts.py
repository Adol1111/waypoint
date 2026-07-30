from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
FIXTURES_ROOT = ROOT / "tests" / "fixtures"

ATOMIC_SKILLS = {
    "domain-context",
    "roadmap-planning",
    "task-spec",
    "technical-design",
    "implementation-plan",
    "task-state",
    "task-execution-simple",
    "docs-workflow-bootstrap",
}
WORKFLOW_SKILLS = {"waypoint-workflow", "milestone-workflow"}
ALL_SKILLS = ATOMIC_SKILLS | WORKFLOW_SKILLS
SKILL_CATEGORIES = {
    "waypoints": ATOMIC_SKILLS - {"docs-workflow-bootstrap"},
    "workflows": WORKFLOW_SKILLS,
    "setup": {"docs-workflow-bootstrap"},
}
COMPANION_SKILLS = {
    "grilling",
    "research",
    "codebase-design",
    "tdd",
    "code-review",
    "handoff",
}
SKILLS_WITH_COMPANIONS = {
    "domain-context",
    "roadmap-planning",
    "task-spec",
    "technical-design",
    "implementation-plan",
    "task-state",
    "task-execution-simple",
}

OWNED_TEMPLATES = {
    "domain-context": {"adr-template.md", "glossary-template.md"},
    "roadmap-planning": {
        "milestone-planning-handoff.md",
        "roadmap-template.md",
    },
    "task-spec": {"spec-template.md"},
    "technical-design": {"technical-design-template.md"},
    "implementation-plan": {"plan-template.md"},
    "task-state": {"task-state-template.md"},
    "task-execution-simple": set(),
    "docs-workflow-bootstrap": {
        "milestone-convention.md",
        "standalone-convention.md",
    },
    "waypoint-workflow": set(),
    "milestone-workflow": {
        "backlog-routing.md",
        "discovered-work-and-closure.md",
        "milestone-artifact.md",
    },
}

SKILL_PATHS = {
    path.parent.name: path.parent
    for path in SKILLS_ROOT.glob("*/*/SKILL.md")
}


def skill_dir(name: str) -> Path:
    try:
        return SKILL_PATHS[name]
    except KeyError as error:
        raise AssertionError(f"missing skill directory: {name}") from error


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"missing YAML frontmatter: {path}")
    metadata = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator or not key or not value.strip():
            raise AssertionError(f"invalid frontmatter line in {path}: {line!r}")
        metadata[key] = value.strip().strip('"')
    return metadata


def read_openai_metadata(path: Path) -> tuple[dict, dict]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "interface:":
        raise AssertionError(f"invalid openai metadata root: {path}")
    interface = {}
    policy = {}
    field_pattern = re.compile(r'^  ([a-z_]+): "([^"]*)"$')
    policy_pattern = re.compile(r"^  ([a-z_]+): (true|false)$")
    section = "interface"
    for line in lines[1:]:
        if line == "policy:":
            section = "policy"
            continue
        if section == "interface":
            match = field_pattern.fullmatch(line)
            if not match:
                raise AssertionError(
                    f"invalid quoted interface field in {path}: {line!r}"
                )
            interface[match.group(1)] = match.group(2)
        else:
            match = policy_pattern.fullmatch(line)
            if not match:
                raise AssertionError(f"invalid policy field in {path}: {line!r}")
            policy[match.group(1)] = match.group(2) == "true"
    return interface, policy


def fixture_pairs() -> tuple[set[Path], set[Path]]:
    prompts = {
        path.relative_to(FIXTURES_ROOT).with_suffix("").with_suffix("")
        for path in FIXTURES_ROOT.rglob("*.prompt.md")
    }
    expected = {
        path.relative_to(FIXTURES_ROOT).with_suffix("").with_suffix("")
        for path in FIXTURES_ROOT.rglob("*.expected.md")
    }
    return prompts, expected


class RepositoryContractTests(unittest.TestCase):
    def test_expected_skill_map_exists(self) -> None:
        self.assertEqual(ALL_SKILLS, set(SKILL_PATHS))
        actual_categories = {
            category.name: {
                path.name
                for path in category.iterdir()
                if path.is_dir() and (path / "SKILL.md").exists()
            }
            for category in SKILLS_ROOT.iterdir()
            if category.is_dir()
        }
        self.assertEqual(SKILL_CATEGORIES, actual_categories)

    def test_local_readme_skill_is_ignored(self) -> None:
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".agents/skills/create-readme/", gitignore)

    def test_skill_frontmatter_is_minimal_and_valid(self) -> None:
        for name in sorted(ALL_SKILLS):
            with self.subTest(skill=name):
                metadata = read_frontmatter(skill_dir(name) / "SKILL.md")
                self.assertEqual({"name", "description"}, set(metadata))
                self.assertEqual(name, metadata["name"])
                self.assertGreaterEqual(len(metadata["description"]), 80)

    def test_openai_metadata_matches_each_skill(self) -> None:
        for name in sorted(ALL_SKILLS):
            with self.subTest(skill=name):
                path = skill_dir(name) / "agents" / "openai.yaml"
                interface, policy = read_openai_metadata(path)
                self.assertEqual(
                    {"display_name", "short_description", "default_prompt"},
                    set(interface),
                )
                self.assertTrue(25 <= len(interface["short_description"]) <= 64)
                self.assertIn(f"${name}", interface["default_prompt"])
                expected_policy = (
                    {"allow_implicit_invocation": False}
                    if name in WORKFLOW_SKILLS | {"docs-workflow-bootstrap"}
                    else {}
                )
                self.assertEqual(expected_policy, policy)

    def test_templates_are_owned_only_by_the_relevant_skill(self) -> None:
        found: dict[str, set[str]] = {}
        for name in sorted(ALL_SKILLS):
            reference_dir = skill_dir(name) / "references"
            found[name] = (
                {path.name for path in reference_dir.glob("*.md")}
                if reference_dir.exists()
                else set()
            )
        self.assertEqual(OWNED_TEMPLATES, found)

        all_template_names = {
            template
            for templates in OWNED_TEMPLATES.values()
            for template in templates
        }
        for owner, templates in OWNED_TEMPLATES.items():
            skill_text = (skill_dir(owner) / "SKILL.md").read_text(encoding="utf-8")
            for template in templates:
                self.assertIn(template, skill_text)
            for foreign in all_template_names - templates:
                self.assertNotIn(f"references/{foreign}", skill_text)

    def test_every_fixture_has_one_prompt_and_one_expected_file(self) -> None:
        prompts, expected = fixture_pairs()
        self.assertEqual(prompts, expected)
        self.assertGreaterEqual(len(prompts), 12)

    def test_every_atomic_skill_has_a_no_docs_independent_fixture(self) -> None:
        fixture_dir = FIXTURES_ROOT / "independent"
        stems = {
            path.name.removesuffix(".prompt.md")
            for path in fixture_dir.glob("*.prompt.md")
        }
        self.assertEqual(ATOMIC_SKILLS, stems)
        for name in sorted(ATOMIC_SKILLS):
            prompt = (fixture_dir / f"{name}.prompt.md").read_text(encoding="utf-8")
            expected = (fixture_dir / f"{name}.expected.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("No `docs/` directory exists.", prompt)
            self.assertIn("must not require a docs layout", expected.lower())

    def test_coordinator_fixtures_recommend_exactly_one_atomic_skill(self) -> None:
        fixture_dir = FIXTURES_ROOT / "workflow"
        for expected_path in fixture_dir.glob("*.expected.md"):
            with self.subTest(case=expected_path.stem):
                text = expected_path.read_text(encoding="utf-8")
                recommendations = re.findall(
                    r"^- Recommended skill: `([^`]+)`$", text, re.MULTILINE
                )
                self.assertEqual(1, len(recommendations))
                self.assertIn(recommendations[0], ATOMIC_SKILLS)
                self.assertEqual(
                    ["Evidence", "Recommended skill", "Reuse", "Why now"],
                    re.findall(r"^- ([^:]+):", text, re.MULTILINE),
                )

    def test_reviewable_spec_fixture_contains_no_chat_dependencies(self) -> None:
        text = (
            FIXTURES_ROOT / "spec-review" / "retry-policy.expected.md"
        ).read_text(encoding="utf-8")
        required = {
            "Intent",
            "Scope",
            "Non-goals",
            "Behavioral contract",
            "Behavioral decisions",
            "Error and compatibility requirements",
            "References",
            "Acceptance",
        }
        for item in required:
            self.assertIn(f"## {item}", text)
        self.assertNotRegex(text.lower(), r"\b(as discussed|from the chat|see conversation)\b")
        for implementation_detail in (
            "client/retry.go",
            "database schema",
            "internal state machine",
        ):
            self.assertNotIn(implementation_detail, text)

    def test_destructive_closing_requires_action_specific_confirmation(self) -> None:
        expected = (
            FIXTURES_ROOT / "closing" / "ambiguous-finish.expected.md"
        ).read_text(encoding="utf-8")
        self.assertIn("No merge, deletion, or discard is performed.", expected)
        for action in ("merge", "delete", "discard"):
            self.assertRegex(
                expected.lower(),
                rf"explicit confirmation[^\n]*{action}|{action}[^\n]*explicit confirmation",
            )

        for name in ("task-state", "task-execution-simple"):
            skill_text = (skill_dir(name) / "SKILL.md").read_text(
                encoding="utf-8"
            ).lower()
            self.assertIn("explicit confirmation", skill_text)
            self.assertIn("merge", skill_text)
            self.assertIn("delet", skill_text)
            self.assertIn("discard", skill_text)

    def test_coordinator_and_atomic_skills_reject_mandatory_layout(self) -> None:
        coordinator = (skill_dir("waypoint-workflow") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Read only artifacts that exist", coordinator)
        self.assertIn("exactly one atomic skill", coordinator)
        self.assertIn("missing docs", coordinator.lower())

        architecture = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        for phrase in (
            "cannot require another local skill",
            "fixed docs tree",
            "branch convention",
            "commit/review ceremony",
        ):
            self.assertIn(phrase, architecture)

    def test_external_companions_have_installable_sources(self) -> None:
        for readme_name in ("README.md", "README_CN.md"):
            with self.subTest(readme=readme_name):
                text = (ROOT / readme_name).read_text(encoding="utf-8")
                self.assertIn("npx skills add mattpocock/skills", text)
                for companion in COMPANION_SKILLS:
                    self.assertIn(
                        f"https://www.skills.sh/mattpocock/skills/{companion}",
                        text,
                    )

        for skill_name in SKILLS_WITH_COMPANIONS:
            with self.subTest(skill=skill_name):
                text = (skill_dir(skill_name) / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("mattpocock/skills", text)
                self.assertIn("npx skills add", text)

    def test_readmes_document_complete_workflow_install_bundles(self) -> None:
        for readme_name in ("README.md", "README_CN.md"):
            with self.subTest(readme=readme_name):
                text = (ROOT / readme_name).read_text(encoding="utf-8")
                for workflow in WORKFLOW_SKILLS:
                    self.assertIn(f"--skill {workflow}", text)
                for waypoint in SKILL_CATEGORIES["waypoints"]:
                    self.assertGreaterEqual(text.count(f"--skill {waypoint}"), 2)
                self.assertIn("--skill docs-workflow-bootstrap", text)
                self.assertIn("npx skills add mattpocock/skills", text)

    def test_bootstrap_requires_a_workflow_choice_when_task_shape_differs(self) -> None:
        skill_text = (skill_dir("docs-workflow-bootstrap") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("ask one direct question", skill_text)
        self.assertIn("whether the team wants Milestone-managed delivery", skill_text)
        self.assertIn("standalone-convention.md", skill_text)
        self.assertIn("milestone-convention.md", skill_text)

        fixture_dir = FIXTURES_ROOT / "bootstrap"
        undecided = (fixture_dir / "workflow-choice.expected.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("asks whether Milestone management is wanted", undecided)
        self.assertIn("Writes: nothing", undecided)

        standalone = (fixture_dir / "standalone.expected.md").read_text(
            encoding="utf-8"
        )
        milestone = (fixture_dir / "milestone.expected.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("flat task index", standalone)
        self.assertIn("does not create Open Milestones", standalone)
        self.assertIn("Open Milestones", milestone)
        self.assertIn("backlog", milestone.lower())
        self.assertIn("task-local `task.md` planning handoffs", milestone)

    def test_milestone_workflow_owns_global_governance_without_stage_gates(self) -> None:
        workflow_dir = skill_dir("milestone-workflow")
        main = (workflow_dir / "SKILL.md").read_text(encoding="utf-8")
        discovered = (
            workflow_dir / "references" / "discovered-work-and-closure.md"
        ).read_text(encoding="utf-8")
        artifact = (
            workflow_dir / "references" / "milestone-artifact.md"
        ).read_text(encoding="utf-8")
        text = "\n".join((main, discovered, artifact))
        for pointer in (
            "references/discovered-work-and-closure.md",
            "references/backlog-routing.md",
            "references/milestone-artifact.md",
        ):
            self.assertIn(pointer, main)
        self.assertIn(
            "finding that may outlive its current task",
            main,
        )
        for phrase in (
            "exit criteria",
            "discovered work",
            "completion evidence",
            "parallel milestones",
            "every entry has been removed or has a durable destination or discard reason",
            "Compare the finding with durable task ownership",
            "required for the current task's Acceptance",
            "explicitly owned by another current Milestone task",
            "Check every Discovered Work entry",
            "retain a concrete reason for a discarded entry",
            "remove an entry resolved inside a current task",
            "task status in the Milestone index as its global recovery signal",
            "Do not add Current Focus",
        ):
            self.assertIn(phrase.lower(), text.lower())

        for adaptive_rule in (
            "Parallel Milestones remain available",
            "confirmation flags",
            "fixed Milestone sequence remain optional",
            "When routine commits are permitted",
        ):
            self.assertIn(adaptive_rule.lower(), main.lower())

        for fixed_gate in (
            "Roadmap confirmed: true",
            "one active Milestone is required",
            "commit after every stage",
        ):
            self.assertNotIn(fixed_gate.lower(), text.lower())

    def test_roadmap_planning_covers_the_whole_milestone_before_next_task(
        self,
    ) -> None:
        roadmap = (skill_dir("roadmap-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        handoff = (
            skill_dir("roadmap-planning")
            / "references"
            / "milestone-planning-handoff.md"
        ).read_text(encoding="utf-8")
        workflow = (skill_dir("milestone-workflow") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        expected = (
            FIXTURES_ROOT / "roadmap" / "milestone-coverage.expected.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "## Complete the Milestone map",
            "Link every exit criterion directly",
            "complete candidate delivery map",
            "preserving stable completed work",
            "## Completion criteria",
        ):
            self.assertIn(phrase, roadmap)
        self.assertIn("every exit criterion linked", handoff)
        self.assertIn("one planning handoff for every confirmed atomic task", handoff)
        self.assertIn("do not add a separate coverage table", handoff.lower())
        self.assertIn("Require the planning result to account for", workflow)
        self.assertIn("This step is complete when", workflow)
        self.assertIn("plans the whole Milestone", expected)
        self.assertIn("Every exit criterion links", expected)

    def test_roadmap_planning_selects_milestones_from_product_and_backlog_evidence(
        self,
    ) -> None:
        roadmap = (skill_dir("roadmap-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        workflow_dir = skill_dir("milestone-workflow")
        workflow = "\n".join(
            (
                (workflow_dir / "SKILL.md").read_text(encoding="utf-8"),
                (
                    workflow_dir / "references" / "backlog-routing.md"
                ).read_text(encoding="utf-8"),
            )
        )
        convention = (
            skill_dir("docs-workflow-bootstrap")
            / "references"
            / "milestone-convention.md"
        ).read_text(encoding="utf-8")
        expected = (
            FIXTURES_ROOT / "roadmap" / "next-milestone-selection.expected.md"
        ).read_text(encoding="utf-8")
        enrichment = (
            FIXTURES_ROOT / "roadmap" / "candidate-enrichment.expected.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "full candidate set",
            "full backlog",
            "Optionally enrich",
            "empty, sparse, or visibly stale",
            "evidence-backed holistic score from `0` to `10`",
            "`0`: recommend removal or closure",
            "Score the backlog candidate outcome",
            "Keep dependencies explicit",
            "Rescore only when evidence changed",
            "desired task count",
            "One backlog outcome may become two or three Milestone tasks",
            "smallest meaningful engineering delivery",
            "one spec can describe",
            "isolated actions inside the meaningful delivery",
            "Keep priority on backlog candidates",
            "Add Milestone-level integration proof only when",
            "task-level specification, technical design, and implementation sequencing remain deferred",
        ):
            self.assertIn(phrase, roadmap)
        for phrase in (
            "send completed delivery",
            "The scoring and task-shaping rules belong to `roadmap-planning`",
            "Reconcile that result",
            "user-confirmed batch of tasks",
            "Tail insertion requires user agreement",
            "begin another Milestone only with user direction",
        ):
            self.assertIn(phrase, workflow)
        self.assertIn("Priority score", convention)
        self.assertIn("bootstrap only creates the agreed storage convention", convention)
        for duplicated_rule in (
            "`9–10`",
            "smallest meaningful result that one spec can describe",
            "one backlog outcome may expand",
        ):
            self.assertNotIn(duplicated_rule.lower(), convention.lower())
        self.assertIn("five-or-six-task batch", expected)
        self.assertIn("consumes three places", expected)
        self.assertIn("not a separate task", expected)
        self.assertIn("No timebox is invented", expected)
        self.assertIn("Selected items leave the backlog only after", expected)
        self.assertIn("offers once", enrichment)
        self.assertIn("optional and non-blocking", enrichment)
        self.assertIn("Vague goals remain Future Directions", enrichment)

    def test_local_milestone_tasks_are_materialized_without_bloating_index(
        self,
    ) -> None:
        roadmap = (skill_dir("roadmap-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        handoff = (
            skill_dir("roadmap-planning")
            / "references"
            / "milestone-planning-handoff.md"
        ).read_text(encoding="utf-8")
        workflow = (skill_dir("milestone-workflow") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        milestone_template = (
            skill_dir("milestone-workflow")
            / "references"
            / "milestone-artifact.md"
        ).read_text(encoding="utf-8")
        convention = (
            skill_dir("docs-workflow-bootstrap")
            / "references"
            / "milestone-convention.md"
        ).read_text(encoding="utf-8")
        spec = (skill_dir("task-spec") / "SKILL.md").read_text(encoding="utf-8")
        state = (skill_dir("task-state") / "SKILL.md").read_text(encoding="utf-8")
        expected = (
            FIXTURES_ROOT / "roadmap" / "local-task-artifacts.expected.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "## Place the planning result",
            "one non-empty task artifact",
            "Every confirmed task receives one durable individual owner",
            "Link every exit criterion directly",
            "When cross-task start or completion dependencies exist",
        ):
            self.assertIn(phrase, roadmap)
        for phrase in (
            "one non-empty `task.md`",
            "each task-local fact has one authoritative home",
        ):
            self.assertIn(phrase, workflow)
        for phrase in (
            "Milestone: <link>",
            "The planning handoff is complete when",
        ):
            self.assertIn(phrase, handoff)
        self.assertIn(
            "handoff as the authoritative task-local source",
            milestone_template,
        )
        self.assertIn(
            "- `<planned | in-progress | blocked | completed>` [<atomic task>]",
            milestone_template,
        )
        self.assertNotIn("| Task | Status |", milestone_template)
        self.assertNotIn("Dependency summary", milestone_template)
        self.assertIn(
            "ordered by the recommended execution sequence",
            milestone_template,
        )
        self.assertIn(
            "Add only the conditional section whose trigger exists",
            milestone_template,
        )
        self.assertNotIn("- Rough scope:", milestone_template)
        self.assertIn("<milestone>/<task>/task.md", convention)
        self.assertIn("one non-empty `docs/tasks/<milestone>/<task>/task.md`", convention)
        self.assertIn("keep Acceptance authoritative there", spec)
        self.assertIn("linking only artifacts that already exist", spec)
        self.assertIn("remove roadmap-era Planning Boundary and Stage Proof", spec)
        self.assertIn("When no task artifact exists", spec)
        design = (skill_dir("technical-design") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        plan = (skill_dir("implementation-plan") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("only after the design artifact exists", design)
        self.assertIn("only after the plan artifact exists", plan)
        self.assertIn("do not create placeholder References", design)
        self.assertIn("do not create placeholder References", plan)
        self.assertIn("stage proof may stand in", state)
        self.assertIn("Task-local details are not repeated", expected)
        self.assertIn("Empty Discovered Work", expected)
        self.assertNotIn("Task-count target:", milestone_template)

    def test_roadmap_planning_owns_scoring_and_atomic_task_rules(self) -> None:
        roadmap = (skill_dir("roadmap-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        consumers = (
            skill_dir("milestone-workflow") / "SKILL.md",
            skill_dir("milestone-workflow")
            / "references"
            / "milestone-artifact.md",
            skill_dir("docs-workflow-bootstrap")
            / "references"
            / "milestone-convention.md",
            skill_dir("roadmap-planning")
            / "references"
            / "roadmap-template.md",
            skill_dir("roadmap-planning")
            / "references"
            / "milestone-planning-handoff.md",
        )

        self.assertIn("`9–10`", roadmap)
        self.assertIn("smallest meaningful engineering delivery", roadmap)
        for path in consumers:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("`9–10`", text, path)
            self.assertNotIn("smallest meaningful engineering delivery", text, path)

    def test_milestone_closure_fixtures_distinguish_unowned_and_placed_work(
        self,
    ) -> None:
        fixture_dir = FIXTURES_ROOT / "milestone"
        blocked = (fixture_dir / "closure-blocked.expected.md").read_text(
            encoding="utf-8"
        )
        cleared = (fixture_dir / "closure-cleared.expected.md").read_text(
            encoding="utf-8"
        )
        completed = (fixture_dir / "completed-followup.expected.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Closure remains blocked", blocked)
        self.assertIn("Closure is allowed", cleared)
        self.assertIn("rechecks every discovered item individually", cleared)
        self.assertIn("durable destination links", cleared)
        self.assertIn("discarded items retain reasons", cleared)
        self.assertIn("does not reopen", completed)

    def test_urgent_work_does_not_silently_reorder_a_milestone(self) -> None:
        workflow_dir = skill_dir("milestone-workflow")
        workflow = (
            workflow_dir / "references" / "backlog-routing.md"
        ).read_text(
            encoding="utf-8"
        )
        expected = (
            FIXTURES_ROOT / "milestone" / "urgent-work.expected.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "append a new task to the Milestone tail",
            "Tail insertion requires user agreement",
            "independently isolated urgent delivery line",
            "without discarding stable active work",
            "has not been silently rewritten",
        ):
            self.assertIn(phrase, workflow)
        prompt = (
            FIXTURES_ROOT / "milestone" / "urgent-work.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn("outside the current task's acceptance", prompt)
        self.assertIn("Milestone closure condition", expected)
        self.assertIn("without discarding stable active work", expected)

    def test_milestone_discovery_intake_respects_task_scope(self) -> None:
        fixture_dir = FIXTURES_ROOT / "milestone"
        in_scope = (fixture_dir / "in-scope-bug.expected.md").read_text(
            encoding="utf-8"
        )
        planned_gap = (fixture_dir / "planned-task-gap.expected.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Keep the failure in the current task", in_scope)
        self.assertIn("mark that task blocked", in_scope)
        self.assertIn("Do not duplicate it in Milestone Discovered Work", in_scope)
        self.assertIn("title alone is not ownership", planned_gap)
        self.assertIn("remove the Discovered Work entry", planned_gap)
        self.assertIn("do not duplicate the same concern", planned_gap)

    def test_milestone_backlog_is_an_active_queue_without_review_history(
        self,
    ) -> None:
        workflow_dir = skill_dir("milestone-workflow")
        workflow = "\n".join(
            (
                (workflow_dir / "SKILL.md").read_text(encoding="utf-8"),
                (
                    workflow_dir / "references" / "backlog-routing.md"
                ).read_text(encoding="utf-8"),
            )
        )
        convention = (
            skill_dir("docs-workflow-bootstrap")
            / "references"
            / "milestone-convention.md"
        ).read_text(encoding="utf-8")
        expected = (
            FIXTURES_ROOT / "milestone" / "backlog-retrieval.expected.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "the full backlog",
            "Concrete deferred work stays in an active backlog",
            "update any source Discovered Work disposition",
            "then remove the backlog entry",
            "leave unchanged scores and entries untouched",
            "free of review history",
            "Before removing already resolved or obsolete work",
        ):
            self.assertIn(phrase, workflow)
        self.assertIn("Backlog is an active queue rather than history", convention)
        self.assertIn("remove that backlog entry", expected)
        self.assertIn("Leave the regional failover entry untouched", expected)
        self.assertIn("Add no review date", expected)
        self.assertIn("Never delete a backlog entry before", expected)

    def test_milestone_workflow_does_not_require_bootstrap(self) -> None:
        expected = (
            FIXTURES_ROOT / "milestone" / "no-existing-artifact.expected.md"
        ).read_text(encoding="utf-8")
        self.assertIn("does not require bootstrap", expected)
        self.assertIn("smallest durable Milestone artifact", expected)
        self.assertIn("MILESTONES.md", expected)

    def test_task_boundary_and_test_semantics_are_guarded(self) -> None:
        spec = (skill_dir("task-spec") / "SKILL.md").read_text(encoding="utf-8")
        execution = (skill_dir("task-execution-simple") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("test the task boundary", spec)
        self.assertIn("delivered, reviewed, or rejected independently", spec)
        self.assertIn("fragment with no meaningful stage result", spec)
        for phrase in ("silently delete", "skip", "loosen", "replacement evidence"):
            self.assertIn(phrase, execution)

    def test_execution_creates_adaptive_git_checkpoints_before_advancing(
        self,
    ) -> None:
        execution = (skill_dir("task-execution-simple") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        coordinator = (skill_dir("waypoint-workflow") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        milestone = (skill_dir("milestone-workflow") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        fixture_dir = FIXTURES_ROOT / "execution"
        checkpoint = (
            fixture_dir / "adaptive-git-checkpoint.expected.md"
        ).read_text(encoding="utf-8")
        unavailable = (
            fixture_dir / "checkpoint-unavailable.expected.md"
        ).read_text(encoding="utf-8")
        workflow_checkpoint = (
            FIXTURES_ROOT / "workflow" / "completed-uncommitted.expected.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "Choose isolation before editing",
            "Create a branch or worktree for non-trivial work",
            "Before advancing to another task or waypoint",
            "one cohesive final task commit",
            "do not manufacture commits per file, layer, plan step, or review round",
            "stable changes are committed or explicitly accounted for",
        ):
            self.assertIn(phrase, execution)
        self.assertIn("silently uncommitted task work", coordinator)
        self.assertIn("Before selecting another task", milestone)
        self.assertIn("Create suitable task isolation", checkpoint)
        self.assertIn("one cohesive task commit before advancing", checkpoint)
        self.assertIn("Leave the mixed work uncommitted", unavailable)
        self.assertIn("Do not silently advance", unavailable)
        self.assertIn(
            "Recommended skill: `task-execution-simple`",
            workflow_checkpoint,
        )

        for readme_name in ("README.md", "README_CN.md"):
            text = (ROOT / readme_name).read_text(encoding="utf-8")
            self.assertIn("cohesive", text)

    def test_behavioral_spec_and_technical_design_have_distinct_owners(self) -> None:
        spec = (skill_dir("task-spec") / "SKILL.md").read_text(encoding="utf-8")
        spec_template = (
            skill_dir("task-spec") / "references" / "spec-template.md"
        ).read_text(encoding="utf-8")
        design = (skill_dir("technical-design") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        design_template = (
            skill_dir("technical-design")
            / "references"
            / "technical-design-template.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Own what the system must do", spec)
        self.assertIn("technical-design", spec)
        for forbidden_heading in (
            "## Implementation surface",
            "## Technical design",
            "## Architecture",
            "## Database schema",
        ):
            self.assertNotIn(forbidden_heading, spec_template)
        self.assertIn("Do not add architecture", spec_template)

        for required in (
            "module responsibilities",
            "data model",
            "state transitions",
            "concurrency",
            "technical alternatives",
            "verification seams",
        ):
            self.assertIn(required, design)
        self.assertIn("pseudocode", design.lower())
        self.assertIn("only when", design.lower())
        self.assertIn("Document the decision, not the derivation", design)
        self.assertIn("mechanically derivable implementation", design)
        self.assertIn("task-level implementation choices", design)
        self.assertNotIn("Keep task-level choices", design)
        self.assertIn("Reference the relevant behavioral requirement", design)
        self.assertIn(
            "Every included section must add a review-critical implementation choice",
            design_template,
        )
        self.assertIn("Failure and quality mechanisms", design_template)
        self.assertNotIn("Failure and quality behavior", design_template)
        self.assertIn("branches, cycles, concurrency, multiple actors", design)
        self.assertIn("single linear sequence", design)
        self.assertIn("Do not expand", design_template)
        self.assertIn("implementation-plan", design)

    def test_technical_design_filters_mechanics_from_decisions(self) -> None:
        expected = (
            FIXTURES_ROOT / "design-review" / "oauth-mechanics.expected.md"
        ).read_text(encoding="utf-8")
        for required in (
            "without restating",
            "Leave splitting, trimming, form encoding",
            "configuration identity and canonical representation",
            "background scheduling, request-time preflight",
            "atomic persistence",
            "without duplicating",
        ):
            self.assertIn(required, expected)

    def test_task_motivation_and_timing_context_remain_durable(self) -> None:
        spec = (skill_dir("task-spec") / "SKILL.md").read_text(encoding="utf-8")
        spec_template = (
            skill_dir("task-spec") / "references" / "spec-template.md"
        ).read_text(encoding="utf-8")
        state = (skill_dir("task-state") / "SKILL.md").read_text(encoding="utf-8")
        state_template = (
            skill_dir("task-state") / "references" / "task-state-template.md"
        ).read_text(encoding="utf-8")

        for text in (spec, spec_template):
            self.assertIn("problem or motivation", text.lower())
            self.assertIn("why it matters", text.lower())
        for label in ("Why now", "Start when", "Revisit when"):
            self.assertIn(label, state)
            self.assertIn(label, state_template)
        self.assertIn("only an observed signal", state)
        self.assertIn("inventing dates", state)
        self.assertIn("add one selection signal", state_template.lower())

    def test_task_state_uses_acceptance_not_verification_logs_for_progress(
        self,
    ) -> None:
        state = (skill_dir("task-state") / "SKILL.md").read_text(encoding="utf-8")
        template = (
            skill_dir("task-state") / "references" / "task-state-template.md"
        ).read_text(encoding="utf-8")
        fixture_dir = FIXTURES_ROOT / "task-state"
        progress = (fixture_dir / "progress-not-log.expected.md").read_text(
            encoding="utf-8"
        )
        completion = (
            fixture_dir / "completion-verification.expected.md"
        ).read_text(encoding="utf-8")
        review = (fixture_dir / "review-handoff.expected.md").read_text(
            encoding="utf-8"
        )
        continuous_review = (
            fixture_dir / "continuous-review.expected.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "primary progress record",
            "The task carries no running command history",
            "expensive or impossible to reproduce",
            "one concise final verification summary",
            "Maintain a checkpoint, not a process log",
            "Grilling is optional and leaves no task-state marker",
            "During uninterrupted execution-review loops",
            "At a stopping boundary",
            "prefer live version-control inspection",
        ):
            self.assertIn(phrase, state)
        self.assertIn("smallest durable record", template)
        self.assertIn("## Recovery checkpoint", template)
        self.assertIn("## Final verification", template)
        self.assertNotIn("## Evidence", template)
        self.assertIn("task carries no routine command history", progress)
        self.assertIn("Do not add phase-completion state", progress)
        self.assertIn("Mark the task `completed` only", completion)
        self.assertIn("unresolved token refresh race", review)
        self.assertIn("Do not preserve resolved review comments", review)
        self.assertIn("link it instead of duplicating it", review)
        self.assertIn("Do not add review rounds", continuous_review)
        self.assertIn("without creating a Recovery checkpoint", continuous_review)
        self.assertIn("survive a stop, handoff, or blocker", continuous_review)

    def test_changesets_release_configuration_is_complete(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertTrue(package["private"])
        self.assertRegex(package["version"], r"\A\d+\.\d+\.\d+\Z")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(f"## {package['version']}", changelog)
        self.assertEqual("pnpm@10.28.2", package["packageManager"])
        self.assertTrue((ROOT / "pnpm-lock.yaml").exists())
        self.assertFalse((ROOT / "package-lock.json").exists())
        for dependency in ("@changesets/cli", "@changesets/changelog-github"):
            self.assertIn(dependency, package["devDependencies"])

        config = json.loads(
            (ROOT / ".changeset" / "config.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [
                "@changesets/changelog-github",
                {"repo": "Adol1111/waypoint"},
            ],
            config["changelog"],
        )
        self.assertTrue(config["privatePackages"]["version"])
        self.assertTrue(config["privatePackages"]["tag"])

        workflow = (
            ROOT / ".github" / "workflows" / "release.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("changesets/action@v1", workflow)
        self.assertIn("pnpm/action-setup@v6", workflow)
        self.assertIn("pnpm install --frozen-lockfile", workflow)
        self.assertIn("publish: pnpm run release", workflow)
        self.assertIn("GITHUB_TOKEN:", workflow)

    def test_pending_changeset_fragments_are_valid(self) -> None:
        changeset_dir = ROOT / ".changeset"
        self.assertTrue((changeset_dir / "README.md").is_file())
        fragments = sorted(changeset_dir.glob("*.md"))
        fragments = [path for path in fragments if path.name != "README.md"]
        pattern = re.compile(
            r'\A---\n"waypoint-skills": (patch|minor|major)\n---\n\n\S',
            re.DOTALL,
        )
        for fragment in fragments:
            with self.subTest(fragment=fragment.name):
                self.assertRegex(fragment.read_text(encoding="utf-8"), pattern)


if __name__ == "__main__":
    unittest.main()
