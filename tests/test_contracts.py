from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
FIXTURES_ROOT = ROOT / "tests" / "fixtures"

WAYPOINT_SKILLS = {
    "domain-context",
    "milestone-planning",
    "feature-spec",
    "technical-design",
    "task-planning",
    "implementation-plan",
}
SETUP_SKILLS = {"docs-workflow-bootstrap", "local-work-tracker"}
WORKFLOW_SKILLS = {"waypoint-workflow"}
ALL_SKILLS = WAYPOINT_SKILLS | SETUP_SKILLS | WORKFLOW_SKILLS
DEPRECATED_SKILLS: set[str] = set()
EXPLICIT_ONLY = SETUP_SKILLS | WORKFLOW_SKILLS | {"task-planning"}

OWNED_TEMPLATES = {
    "domain-context": {"adr-template.md", "glossary-template.md"},
    "milestone-planning": {
        "completed-feature-index.md",
        "requirement-pool-template.md",
        "milestone-template.md",
        "feature-handoff-template.md",
    },
    "feature-spec": {"spec-template.md"},
    "technical-design": {"technical-design-template.md"},
    "task-planning": {"task-plan-template.md"},
    "implementation-plan": {"plan-template.md"},
    "docs-workflow-bootstrap": {"feature-convention.md"},
    "local-work-tracker": {"local-tracker-format.md"},
    "waypoint-workflow": set(),
}

SKILL_PATHS = {
    path.parent.name: path.parent
    for category in ("waypoints", "setup", "workflows")
    for path in (SKILLS_ROOT / category).glob("*/SKILL.md")
}


def skill_dir(name: str) -> Path:
    return SKILL_PATHS[name]


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"missing YAML frontmatter: {path}")
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator or not key or not value.strip():
            raise AssertionError(f"invalid frontmatter line in {path}: {line!r}")
        metadata[key] = value.strip().strip('"')
    return metadata


def read_openai_metadata(path: Path) -> tuple[dict[str, str], dict[str, bool]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "interface:":
        raise AssertionError(f"invalid OpenAI metadata root: {path}")
    interface: dict[str, str] = {}
    policy: dict[str, bool] = {}
    section = "interface"
    for line in lines[1:]:
        if line == "policy:":
            section = "policy"
            continue
        if section == "interface":
            match = re.fullmatch(r'^  ([a-z_]+): "([^"]*)"$', line)
            if not match:
                raise AssertionError(f"invalid interface line in {path}: {line!r}")
            interface[match.group(1)] = match.group(2)
        else:
            match = re.fullmatch(r"^  ([a-z_]+): (true|false)$", line)
            if not match:
                raise AssertionError(f"invalid policy line in {path}: {line!r}")
            policy[match.group(1)] = match.group(2) == "true"
    return interface, policy


class RepositoryContractTests(unittest.TestCase):
    def test_expected_skill_catalog_and_categories(self) -> None:
        self.assertEqual(ALL_SKILLS, set(SKILL_PATHS))
        actual = {
            category.name: {
                child.name
                for child in category.iterdir()
                if child.is_dir() and (child / "SKILL.md").exists()
            }
            for category in SKILLS_ROOT.iterdir()
            if category.is_dir()
        }
        self.assertEqual(
            {
                "waypoints": WAYPOINT_SKILLS,
                "setup": SETUP_SKILLS,
                "workflows": WORKFLOW_SKILLS,
                "deprecated": DEPRECATED_SKILLS,
            },
            actual,
        )

    def test_deprecated_directory_contains_guidance_not_skills(self) -> None:
        directory = SKILLS_ROOT / "deprecated"
        archived = {
            child.name
            for child in directory.iterdir()
            if child.is_dir() and (child / "SKILL.md").exists()
        }
        self.assertEqual(DEPRECATED_SKILLS, archived)
        readme = (directory / "README.md").read_text(encoding="utf-8")
        for name in (
            "roadmap-planning",
            "task-spec",
            "task-state",
            "task-execution-simple",
            "milestone-workflow",
        ):
            self.assertIn(name, readme)
        self.assertIn("contains no installable skills", readme)
        self.assertIn("npx skills@latest remove", readme)

    def test_frontmatter_is_minimal_and_complete(self) -> None:
        for name in sorted(ALL_SKILLS):
            with self.subTest(skill=name):
                metadata = read_frontmatter(skill_dir(name) / "SKILL.md")
                self.assertEqual({"name", "description"}, set(metadata))
                self.assertEqual(name, metadata["name"])
                self.assertGreaterEqual(len(metadata["description"]), 80)
                text = (skill_dir(name) / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn("[TODO", text)

    def test_openai_metadata_and_explicit_invocation_policy(self) -> None:
        for name in sorted(ALL_SKILLS):
            with self.subTest(skill=name):
                interface, policy = read_openai_metadata(
                    skill_dir(name) / "agents" / "openai.yaml"
                )
                self.assertEqual(
                    {"display_name", "short_description", "default_prompt"},
                    set(interface),
                )
                self.assertTrue(25 <= len(interface["short_description"]) <= 64)
                self.assertIn(f"${name}", interface["default_prompt"])
                expected = (
                    {"allow_implicit_invocation": False}
                    if name in EXPLICIT_ONLY
                    else {}
                )
                self.assertEqual(expected, policy)

    def test_templates_have_one_owner(self) -> None:
        found: dict[str, set[str]] = {}
        for name in sorted(ALL_SKILLS):
            directory = skill_dir(name) / "references"
            found[name] = (
                {path.name for path in directory.glob("*.md")}
                if directory.exists()
                else set()
            )
        self.assertEqual(OWNED_TEMPLATES, found)
        all_names = {item for values in OWNED_TEMPLATES.values() for item in values}
        for owner, templates in OWNED_TEMPLATES.items():
            text = (skill_dir(owner) / "SKILL.md").read_text(encoding="utf-8")
            for template in templates:
                self.assertIn(f"references/{template}", text)
            for foreign in all_names - templates:
                self.assertNotIn(f"references/{foreign}", text)

    def test_feature_hierarchy_is_explicit(self) -> None:
        architecture = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        milestone = (skill_dir("milestone-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        planning = (skill_dir("task-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "Shared Milestone",
            "Feature — one stable owner",
            "Task — one assignee",
            "There is no second authoritative global Task directory",
        ):
            self.assertIn(phrase, architecture)
        self.assertIn("Default to a frozen Feature batch", milestone)
        self.assertIn("does not contain child Tasks", milestone)
        self.assertIn("never initialize tracking implicitly", milestone)
        self.assertIn("Child Tasks remain inside their Feature", planning)
        self.assertIn("Cross-Feature dependencies", planning)
        self.assertIn("do not initialize tracking", planning)

    def test_requirement_feature_completion_lifecycle_is_single_sourced(self) -> None:
        milestone = (skill_dir("milestone-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        completed = (
            skill_dir("milestone-planning")
            / "references"
            / "completed-feature-index.md"
        ).read_text(encoding="utf-8")
        convention = (
            skill_dir("docs-workflow-bootstrap")
            / "references"
            / "feature-convention.md"
        ).read_text(encoding="utf-8")
        architecture = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        for phrase in (
            "Remove a wholly selected requirement",
            "rewrite the unselected remainder",
            "keep the Feature directory",
            "ungrouped and newest-first",
            "history, not a second live-status authority",
        ):
            self.assertIn(phrase, milestone)
        self.assertIn("YYYY-MM-DD", completed)
        self.assertIn("completed.md", convention)
        self.assertIn(
            "`requirements.md` → active Feature → `completed.md`", architecture
        )

    def test_owner_resolution_reads_local_identity_before_asking(self) -> None:
        for name in ("milestone-planning", "feature-spec", "task-planning"):
            with self.subTest(skill=name):
                text = (skill_dir(name) / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("`.waypoint/local.yaml`", text)
                self.assertIn("ask the user", text)
                self.assertIn("Git author metadata", text)
        planning = (skill_dir("task-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("too large for one safe fresh context", planning)
        self.assertIn("one owner executes them sequentially", planning)

    def test_target_specific_skills_resolve_owned_work_without_guessing(self) -> None:
        for name in (
            "feature-spec",
            "task-planning",
            "technical-design",
            "implementation-plan",
        ):
            with self.subTest(skill=name):
                text = (skill_dir(name) / "SKILL.md").read_text(encoding="utf-8")
                metadata = read_frontmatter(skill_dir(name) / "SKILL.md")
                self.assertIn("explicitly targeted or unambiguously current", metadata["description"])
                self.assertIn("`.waypoint/local.yaml`", text)
                self.assertIn("exactly one candidate remains", text)
                self.assertIn("current branch", text)
        spec = (skill_dir("feature-spec") / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Never fall back to another owner's Feature", spec)
        expected = (
            FIXTURES_ROOT / "v2" / "new-window-owned-target.expected.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "resolve the current actor as `alice`",
            "select `F-alice` only",
            "Never select `F-bob`",
            "zero or multiple active Features",
            "Git history or the current branch",
        ):
            self.assertIn(phrase, expected)

    def test_feature_spec_and_design_are_distinct_and_threshold_driven(self) -> None:
        spec = (skill_dir("feature-spec") / "SKILL.md").read_text(encoding="utf-8")
        design = (skill_dir("technical-design") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("split across executors must have one durable behavioral contract", spec)
        self.assertIn("Do not include architecture", spec)
        self.assertIn("A small unsplit Feature", spec)
        self.assertIn("missing design file", design)
        self.assertIn("materiality gate", design)
        self.assertIn("return it to `feature-spec`", design)
        for phrase in (
            "primary and foreign keys",
            "migration or compatibility implications",
            "state table or state diagram",
            "sequence diagram",
            "component or container diagram",
            "Mermaid diagrams",
            "diagram is not decoration",
        ):
            self.assertIn(phrase, design)

    def test_task_planning_adapts_matt_and_stops_before_assignment(self) -> None:
        planning = (skill_dir("task-planning") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        template = (
            skill_dir("task-planning") / "references" / "task-plan-template.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "Matt Pocock's `to-tickets`",
            "tracer-bullet",
            "Audit interference",
            "Confirm before publishing",
            "does not assign any Task",
            "Never assign yourself a Task",
            "automatic tool approval",
        ):
            self.assertIn(phrase, planning)
        for phrase in (
            "Task ID",
            "Must not change",
            "Keep live Status, Assignee, Executor, MR",
            "do not create a second behavioral specification",
        ):
            self.assertIn(phrase, template)

    def test_workflow_is_read_only_and_can_route_to_matt(self) -> None:
        workflow = (skill_dir("waypoint-workflow") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "read-only navigator",
            "Recommend exactly one next skill",
            "Matt Pocock's `implement`",
            "Do not invoke the recommendation",
            "only as the blocked next capability",
            "Do not substitute `local-work-tracker`",
            "`ready` alone is not assignment",
        ):
            self.assertIn(phrase, workflow)
        self.assertNotIn("milestone-workflow", workflow)

    def test_tracking_has_one_authority_and_feature_first_view(self) -> None:
        tracker = (skill_dir("local-work-tracker") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        feature_template = (
            skill_dir("milestone-planning")
            / "references"
            / "feature-handoff-template.md"
        ).read_text(encoding="utf-8")
        script = (
            skill_dir("local-work-tracker")
            / "scripts"
            / "waypoint_tracker.py"
        )
        for phrase in (
            "Never invoke this skill implicitly",
            "one tracker coordinator",
            "expected record revision",
            "does not assign it",
            "global Feature dashboard",
            "newest-first completed Feature index",
        ):
            self.assertIn(phrase, tracker)
        self.assertIn("<!-- waypoint:tasks:start -->", feature_template)
        self.assertIn("Executors do not edit it manually", feature_template)
        self.assertTrue(script.exists())
        self.assertTrue(script.stat().st_mode & 0o111)

    def test_planning_execution_and_merge_are_separate_authorizations(self) -> None:
        architecture = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        workflow = (skill_dir("waypoint-workflow") / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "confirming discussion or shared understanding",
            "implementing one explicitly assigned Feature or Task",
            "merging one specific MR",
            "automatic tool approval",
        ):
            self.assertIn(phrase, architecture)
        self.assertIn("planning approval", workflow)
        self.assertIn("MR merge", workflow)

    def test_readmes_are_synchronized_on_catalog_and_migration(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README_CN.md").read_text(encoding="utf-8")
        for name in sorted(ALL_SKILLS):
            self.assertIn(name, english)
            self.assertIn(name, chinese)
        for removed in (
            "roadmap-planning",
            "task-spec",
            "task-state",
            "task-execution-simple",
            "milestone-workflow",
        ):
            self.assertIn(removed, english)
            self.assertIn(removed, chinese)
        removal = "npx skills@latest remove roadmap-planning task-spec task-state task-execution-simple milestone-workflow --agent '*'"
        self.assertIn(removal, english)
        self.assertIn(removal, chinese)
        self.assertIn("Generic recursive skill installers", english)
        self.assertIn("通用递归式 skill 安装器", chinese)
        self.assertIn("mattpocock/skills", english)
        self.assertIn("mattpocock/skills", chinese)

    def test_changeset_is_valid_and_minor(self) -> None:
        fragments = [
            path
            for path in (ROOT / ".changeset").glob("*.md")
            if path.name != "README.md"
        ]
        self.assertTrue(fragments)
        texts = [path.read_text(encoding="utf-8") for path in fragments]
        for text in texts:
            self.assertRegex(
                text, r'\A---\n"waypoint-skills": (patch|minor|major)\n---\n\n\S'
            )
        self.assertTrue(
            any('"waypoint-skills": minor' in text for text in texts)
        )
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertEqual("waypoint-skills", package["name"])

    def test_fixture_pairs_remain_complete(self) -> None:
        prompts = {
            path.relative_to(FIXTURES_ROOT).with_suffix("").with_suffix("")
            for path in FIXTURES_ROOT.rglob("*.prompt.md")
        }
        expected = {
            path.relative_to(FIXTURES_ROOT).with_suffix("").with_suffix("")
            for path in FIXTURES_ROOT.rglob("*.expected.md")
        }
        self.assertEqual(prompts, expected)

    def test_v2_forward_scenarios_preserve_planning_boundaries(self) -> None:
        unresolved = (
            FIXTURES_ROOT / "v2" / "unresolved-shared-contract.expected.md"
        ).read_text(encoding="utf-8")
        unassigned = (
            FIXTURES_ROOT / "v2" / "ready-but-unassigned.expected.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Stop before Task decomposition and implementation", unresolved)
        self.assertIn("to `technical-design`", unresolved.lower())
        self.assertIn("only as the blocked next capability", unassigned)
        self.assertIn("Do not recommend `local-work-tracker`", unassigned)
        self.assertIn("automatic tool approval", unassigned)


if __name__ == "__main__":
    unittest.main()
