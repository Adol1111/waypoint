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
COMPANION_SKILLS = {"grilling", "research", "tdd", "code-review", "handoff"}
SKILLS_WITH_COMPANIONS = {
    "domain-context",
    "roadmap-planning",
    "task-spec",
    "implementation-plan",
    "task-state",
    "task-execution-simple",
}

OWNED_TEMPLATES = {
    "domain-context": {"adr-template.md", "glossary-template.md"},
    "roadmap-planning": {"roadmap-template.md"},
    "task-spec": {"spec-template.md"},
    "implementation-plan": {"plan-template.md"},
    "task-state": {"task-state-template.md"},
    "task-execution-simple": set(),
    "docs-workflow-bootstrap": {
        "milestone-convention.md",
        "standalone-convention.md",
    },
    "waypoint-workflow": set(),
    "milestone-workflow": {"milestone-artifact.md"},
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
                self.assertIn("- Writes: nothing", text)

    def test_reviewable_spec_fixture_contains_no_chat_dependencies(self) -> None:
        text = (
            FIXTURES_ROOT / "spec-review" / "retry-policy.expected.md"
        ).read_text(encoding="utf-8")
        required = {
            "Intent",
            "Scope",
            "Non-goals",
            "Implementation surface",
            "Decision and rationale",
            "Error behavior",
            "Completion proof",
        }
        for item in required:
            self.assertIn(f"## {item}", text)
        self.assertNotRegex(text.lower(), r"\b(as discussed|from the chat|see conversation)\b")

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

    def test_milestone_workflow_owns_global_governance_without_stage_gates(self) -> None:
        text = (skill_dir("milestone-workflow") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "exit criteria",
            "discovered work",
            "completion evidence",
            "parallel milestones",
            "every discovered item has a disposition",
            "no `current milestone` finding remains unresolved",
            "current-focus pointer",
            "future directions",
        ):
            self.assertIn(phrase.lower(), text.lower())

        for forbidden in (
            "Roadmap confirmed",
            "mandatory commits",
            "single current milestone",
            "serial milestone execution",
        ):
            self.assertIn(forbidden.lower(), text.lower())

    def test_milestone_closure_fixtures_distinguish_untriaged_and_placed_work(
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
        self.assertIn("does not reopen", completed)

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
        for phrase in ("silently delete", "skip", "loosen", "replacement evidence"):
            self.assertIn(phrase, execution)

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
        self.assertIn("Do not invent dates", state)
        self.assertIn("Omit the Selection context section", state_template)

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
