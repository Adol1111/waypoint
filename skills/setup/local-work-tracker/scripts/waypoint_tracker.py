#!/usr/bin/env python3
"""Dependency-free repository-local Feature/Task tracker."""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import sys
from pathlib import Path


VALID_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
STORED_TASK_STATES = {
    "planned",
    "assigned",
    "in-progress",
    "blocked",
    "in-review",
    "completed",
    "cancelled",
}
FEATURE_STATES = {"planned", "in-progress", "blocked", "integration", "completed", "cancelled"}
FEATURE_TRANSITIONS = {
    "planned": {"in-progress", "blocked", "cancelled"},
    "in-progress": {"blocked", "integration", "cancelled"},
    "blocked": {"in-progress", "cancelled"},
    "integration": {"in-progress", "blocked", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}
TRANSITIONS = {
    "planned": {"assigned", "cancelled"},
    "assigned": {"in-progress", "blocked", "cancelled"},
    "in-progress": {"blocked", "in-review", "cancelled"},
    "blocked": {"assigned", "in-progress", "cancelled"},
    "in-review": {"in-progress", "blocked", "completed", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}
DASHBOARD_START = "<!-- waypoint:dashboard:start -->"
DASHBOARD_END = "<!-- waypoint:dashboard:end -->"
TASKS_START = "<!-- waypoint:tasks:start -->"
TASKS_END = "<!-- waypoint:tasks:end -->"


class TrackerError(RuntimeError):
    pass


def repository_root(explicit: str | None) -> Path:
    root = Path(explicit or os.getcwd()).resolve()
    if not (root / ".git").exists():
        raise TrackerError(f"not a Git repository root: {root}")
    return root


def parse_flat_yaml(path: Path) -> dict[str, object]:
    if not path.exists():
        raise TrackerError(f"missing record: {path}")
    result: dict[str, object] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator or not key.strip() or not value.strip():
            raise TrackerError(f"invalid local tracker YAML at {path}:{number}")
        try:
            result[key.strip()] = json.loads(value.strip())
        except json.JSONDecodeError as error:
            raise TrackerError(f"invalid scalar at {path}:{number}: {error}") from error
    return result


def write_flat_yaml(path: Path, values: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in values.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_id(value: str, label: str) -> str:
    if not VALID_ID.fullmatch(value):
        raise TrackerError(f"invalid {label} {value!r}; use lowercase letters, digits, ., _, or -")
    return value


def config_path(root: Path) -> Path:
    return root / ".waypoint" / "config.yaml"


def local_path(root: Path) -> Path:
    return root / ".waypoint" / "local.yaml"


def feature_record_path(root: Path, feature_id: str) -> Path:
    return root / ".waypoint" / "tracker" / "features" / f"{feature_id}.yaml"


def task_record_path(root: Path, feature_id: str, task_id: str) -> Path:
    return root / ".waypoint" / "tracker" / "tasks" / feature_id / f"{task_id}.yaml"


def require_initialized(root: Path) -> dict[str, object]:
    return parse_flat_yaml(config_path(root))


def repository_relative_path(root: Path, raw: str, label: str) -> Path:
    path = (root / raw).resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise TrackerError(f"{label} must stay inside repository: {raw}") from error
    if not path.is_file():
        raise TrackerError(f"{label} does not exist: {raw}")
    return path


@contextlib.contextmanager
def mutation_lock(root: Path):
    lock_path = root / ".waypoint" / "tracker.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise TrackerError(f"local tracker is locked: {lock_path}") from error
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode())
        os.close(descriptor)
        yield
    finally:
        with contextlib.suppress(FileNotFoundError):
            lock_path.unlink()


def ensure_ignore_rules(root: Path) -> None:
    path = root / ".gitignore"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    rules = ["/.waypoint/local.yaml", "/.waypoint/tracker.lock"]
    missing = [rule for rule in rules if rule not in existing.splitlines()]
    if missing:
        separator = "" if not existing or existing.endswith("\n") else "\n"
        path.write_text(existing + separator + "\n".join(missing) + "\n", encoding="utf-8")


def command_init(args: argparse.Namespace, root: Path) -> None:
    actor = validate_id(args.actor, "actor ID")
    if config_path(root).exists() or local_path(root).exists():
        raise TrackerError("Waypoint local tracker is already initialized")
    with mutation_lock(root):
        write_flat_yaml(
            config_path(root),
            {"version": 1, "tracker_mode": "local", "docs_root": args.docs_root},
        )
        write_flat_yaml(
            local_path(root),
            {
                "version": 1,
                "actor_id": actor,
                "actor_display_name": args.display_name or actor,
                "executor_harness": args.executor_harness or "",
                "executor_label": args.executor_label or "",
            },
        )
        ensure_ignore_rules(root)
    print(f"initialized local tracker for actor {actor}")


def command_whoami(args: argparse.Namespace, root: Path) -> None:
    values = parse_flat_yaml(local_path(root))
    print(json.dumps(values, ensure_ascii=False, indent=2))


def update_local(root: Path, updates: dict[str, object]) -> None:
    with mutation_lock(root):
        values = parse_flat_yaml(local_path(root))
        values.update(updates)
        write_flat_yaml(local_path(root), values)


def command_set_actor(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    actor = validate_id(args.actor, "actor ID")
    update_local(root, {"actor_id": actor, "actor_display_name": args.display_name or actor})
    print(f"actor set to {actor}")


def command_set_executor(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    update_local(root, {"executor_harness": args.harness, "executor_label": args.label or ""})
    print(f"executor set to {args.harness}/{args.label or ''}")


def command_register_feature(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    feature_id = validate_id(args.id, "Feature ID")
    owner = validate_id(args.owner, "Feature owner")
    feature_path = repository_relative_path(root, args.path, "Feature path")
    record_path = feature_record_path(root, feature_id)
    if record_path.exists():
        raise TrackerError(f"Feature already registered: {feature_id}")
    with mutation_lock(root):
        write_flat_yaml(
            record_path,
            {
                "version": 1,
                "feature_id": feature_id,
                "title": args.title,
                "owner": owner,
                "milestone": args.milestone,
                "status": "planned",
                "path": str(feature_path.relative_to(root)),
                "evidence": "",
                "revision": 0,
            },
        )
    print(f"registered Feature {feature_id} revision 0")


def parse_blockers(raw_values: list[str] | None) -> list[str]:
    values: list[str] = []
    for raw in raw_values or []:
        for item in raw.split(","):
            item = item.strip()
            if item:
                values.append(validate_id(item, "Task blocker ID"))
    return sorted(set(values))


def command_register_task(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    feature_id = validate_id(args.feature, "Feature ID")
    task_id = validate_id(args.id, "Task ID")
    parse_flat_yaml(feature_record_path(root, feature_id))
    task_path = repository_relative_path(root, args.path, "Task path")
    record_path = task_record_path(root, feature_id, task_id)
    if record_path.exists():
        raise TrackerError(f"Task already registered: {feature_id}/{task_id}")
    blockers = parse_blockers(args.blocked_by)
    if task_id in blockers:
        raise TrackerError("a Task cannot block itself")
    for blocker in blockers:
        parse_flat_yaml(task_record_path(root, feature_id, blocker))
    with mutation_lock(root):
        write_flat_yaml(
            record_path,
            {
                "version": 1,
                "feature_id": feature_id,
                "task_id": task_id,
                "title": args.title,
                "status": "planned",
                "assignee": "",
                "executor": "",
                "blocked_by": blockers,
                "reason": "",
                "branch": "",
                "mr": "",
                "evidence": "",
                "path": str(task_path.relative_to(root)),
                "revision": 0,
            },
        )
    print(f"registered Task {feature_id}/{task_id} revision 0")


def require_revision(record: dict[str, object], expected: int) -> None:
    actual = record.get("revision")
    if actual != expected:
        raise TrackerError(f"revision mismatch: expected {expected}, current {actual}")


def blockers_completed(root: Path, record: dict[str, object]) -> bool:
    feature_id = str(record["feature_id"])
    blockers = record.get("blocked_by", [])
    if not isinstance(blockers, list):
        raise TrackerError("blocked_by must be a list")
    return all(
        parse_flat_yaml(task_record_path(root, feature_id, str(blocker))).get("status")
        == "completed"
        for blocker in blockers
    )


def local_executor(root: Path) -> str:
    values = parse_flat_yaml(local_path(root))
    harness = str(values.get("executor_harness", ""))
    label = str(values.get("executor_label", ""))
    return "/".join(part for part in (harness, label) if part)


def command_assign(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    feature_id = validate_id(args.feature, "Feature ID")
    task_id = validate_id(args.task, "Task ID")
    assignee = validate_id(args.assignee, "assignee")
    path = task_record_path(root, feature_id, task_id)
    with mutation_lock(root):
        record = parse_flat_yaml(path)
        require_revision(record, args.expect_revision)
        if record.get("status") != "planned":
            raise TrackerError(f"Task is not planned: {record.get('status')}")
        if not blockers_completed(root, record):
            raise TrackerError("Task is blocked by incomplete structural dependencies")
        record.update(
            {
                "status": "assigned",
                "assignee": assignee,
                "executor": args.executor or local_executor(root),
                "branch": args.branch or "",
                "revision": int(record["revision"]) + 1,
            }
        )
        write_flat_yaml(path, record)
    print(f"assigned {feature_id}/{task_id} revision {record['revision']}")


def command_transition(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    feature_id = validate_id(args.feature, "Feature ID")
    task_id = validate_id(args.task, "Task ID")
    target = args.to
    if target == "ready" or target not in STORED_TASK_STATES:
        raise TrackerError("ready is derived; choose a stored Task state")
    path = task_record_path(root, feature_id, task_id)
    with mutation_lock(root):
        record = parse_flat_yaml(path)
        require_revision(record, args.expect_revision)
        current = str(record.get("status"))
        if target not in TRANSITIONS.get(current, set()):
            raise TrackerError(f"invalid transition: {current} -> {target}")
        if target in {"assigned", "in-progress", "in-review", "completed"} and not blockers_completed(root, record):
            raise TrackerError("Task is blocked by incomplete structural dependencies")
        if target == "completed" and not args.evidence:
            raise TrackerError("completed requires --evidence for accepted and integrated proof")
        if target == "blocked" and not args.reason:
            raise TrackerError("blocked requires --reason")
        record["status"] = target
        if args.reason is not None:
            record["reason"] = args.reason
        if args.branch is not None:
            record["branch"] = args.branch
        if args.mr is not None:
            record["mr"] = args.mr
        if args.evidence is not None:
            record["evidence"] = args.evidence
        record["revision"] = int(record["revision"]) + 1
        write_flat_yaml(path, record)
    print(f"transitioned {feature_id}/{task_id} to {target} revision {record['revision']}")


def command_transition_feature(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    feature_id = validate_id(args.feature, "Feature ID")
    target = args.to
    if target not in FEATURE_STATES or target == "completed":
        raise TrackerError("use close-feature for completed; choose another Feature state")
    path = feature_record_path(root, feature_id)
    with mutation_lock(root):
        record = parse_flat_yaml(path)
        require_revision(record, args.expect_revision)
        current = str(record.get("status"))
        if target not in FEATURE_TRANSITIONS.get(current, set()):
            raise TrackerError(f"invalid Feature transition: {current} -> {target}")
        if target == "blocked" and not args.reason:
            raise TrackerError("blocked requires --reason")
        record["status"] = target
        if args.reason is not None:
            record["reason"] = args.reason
        record["revision"] = int(record["revision"]) + 1
        write_flat_yaml(path, record)
    print(f"transitioned Feature {feature_id} to {target} revision {record['revision']}")


def command_close_feature(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    feature_id = validate_id(args.feature, "Feature ID")
    path = feature_record_path(root, feature_id)
    tasks = load_tasks(root, feature_id)
    incomplete = [str(task["task_id"]) for task in tasks if task.get("status") != "completed"]
    if incomplete:
        raise TrackerError(f"cannot close Feature with incomplete Tasks: {', '.join(incomplete)}")
    with mutation_lock(root):
        record = parse_flat_yaml(path)
        require_revision(record, args.expect_revision)
        if args.confirmed_by != record.get("owner"):
            raise TrackerError(
                f"Feature completion must be confirmed by owner {record.get('owner')}"
            )
        if record.get("status") in {"completed", "cancelled"}:
            raise TrackerError(f"Feature is already {record.get('status')}")
        record.update(
            {
                "status": "completed",
                "evidence": args.evidence,
                "revision": int(record["revision"]) + 1,
            }
        )
        write_flat_yaml(path, record)
    print(f"closed Feature {feature_id} revision {record['revision']}")


def load_features(root: Path) -> list[dict[str, object]]:
    directory = root / ".waypoint" / "tracker" / "features"
    return [parse_flat_yaml(path) for path in sorted(directory.glob("*.yaml"))] if directory.exists() else []


def load_tasks(root: Path, feature_id: str | None = None) -> list[dict[str, object]]:
    directory = root / ".waypoint" / "tracker" / "tasks"
    pattern = f"{feature_id}/*.yaml" if feature_id else "*/*.yaml"
    return [parse_flat_yaml(path) for path in sorted(directory.glob(pattern))] if directory.exists() else []


def display_status(root: Path, task: dict[str, object]) -> str:
    if task.get("status") == "planned":
        return "ready" if blockers_completed(root, task) else "blocked"
    return str(task.get("status"))


def feature_summary(root: Path, feature: dict[str, object], tasks: list[dict[str, object]]) -> str:
    if feature.get("status") in {"completed", "cancelled"}:
        return str(feature["status"])
    if not tasks:
        return str(feature.get("status", "planned"))
    statuses = [display_status(root, task) for task in tasks]
    if all(status == "completed" for status in statuses):
        return "integration"
    active = {"assigned", "in-progress", "in-review"}
    if any(status in active | {"completed"} for status in statuses):
        return "in-progress"
    if all(status in {"blocked", "cancelled", "completed"} for status in statuses):
        return "blocked"
    return "planned"


def replace_region(text: str, start: str, end: str, heading: str, body: str) -> str:
    region = f"{start}\n{body.rstrip()}\n{end}"
    if start in text and end in text:
        before, remainder = text.split(start, 1)
        _, after = remainder.split(end, 1)
        return before + region + after
    separator = "\n" if text.endswith("\n") else "\n\n"
    return text + separator + f"## {heading}\n\n" + region + "\n"


def render_feature(root: Path, feature: dict[str, object], tasks: list[dict[str, object]]) -> None:
    if not tasks:
        return
    path = repository_relative_path(root, str(feature["path"]), "Feature path")
    lines = []
    for task in tasks:
        status = display_status(root, task)
        checked = "x" if status == "completed" else " "
        task_path = Path(str(task["path"]))
        link = os.path.relpath(root / task_path, path.parent)
        details = [status]
        if task.get("assignee"):
            details.append(f"assignee: {task['assignee']}")
        if task.get("executor"):
            details.append(f"executor: {task['executor']}")
        if task.get("branch"):
            details.append(f"branch: {task['branch']}")
        if task.get("mr"):
            details.append(f"MR: {task['mr']}")
        lines.append(f"- [{checked}] [{task['title']}]({link}) — {'; '.join(details)}")
    current = path.read_text(encoding="utf-8")
    path.write_text(replace_region(current, TASKS_START, TASKS_END, "Task progress", "\n".join(lines)), encoding="utf-8")


def render_dashboard(root: Path, config: dict[str, object], features: list[dict[str, object]]) -> Path:
    docs_root = root / str(config.get("docs_root", "docs/work"))
    path = docs_root / "index.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text(encoding="utf-8") if path.exists() else "# Work\n"
    lines = ["| Feature | Owner | Milestone | Status | Tasks |", "| --- | --- | --- | --- | --- |"]
    for feature in features:
        tasks = load_tasks(root, str(feature["feature_id"]))
        counts: dict[str, int] = {}
        for task in tasks:
            status = display_status(root, task)
            counts[status] = counts.get(status, 0) + 1
        summary = ", ".join(f"{count} {status}" for status, count in sorted(counts.items())) or "unsplit"
        feature_path = root / str(feature["path"])
        link = os.path.relpath(feature_path, path.parent)
        status = feature_summary(root, feature, tasks)
        lines.append(f"| [{feature['title']}]({link}) | {feature['owner']} | {feature['milestone']} | {status} | {summary} |")
    path.write_text(replace_region(current, DASHBOARD_START, DASHBOARD_END, "Feature dashboard", "\n".join(lines)), encoding="utf-8")
    return path


def command_render(args: argparse.Namespace, root: Path) -> None:
    config = require_initialized(root)
    features = load_features(root)
    with mutation_lock(root):
        for feature in features:
            render_feature(root, feature, load_tasks(root, str(feature["feature_id"])))
        dashboard = render_dashboard(root, config, features)
    print(f"rendered {len(features)} Features to {dashboard.relative_to(root)}")


def command_check(args: argparse.Namespace, root: Path) -> None:
    config = require_initialized(root)
    local = parse_flat_yaml(local_path(root))
    errors: list[str] = []
    if config.get("tracker_mode") != "local":
        errors.append("tracker_mode is not local")
    try:
        validate_id(str(local.get("actor_id", "")), "actor ID")
    except TrackerError as error:
        errors.append(str(error))
    ignore_lines = (root / ".gitignore").read_text(encoding="utf-8").splitlines()
    if "/.waypoint/local.yaml" not in ignore_lines:
        errors.append(".waypoint/local.yaml is not ignored")
    feature_ids = {str(feature["feature_id"]) for feature in load_features(root)}
    for feature in load_features(root):
        try:
            repository_relative_path(root, str(feature["path"]), "Feature path")
        except TrackerError as error:
            errors.append(str(error))
    for task in load_tasks(root):
        feature_id = str(task.get("feature_id"))
        task_id = str(task.get("task_id"))
        if feature_id not in feature_ids:
            errors.append(f"Task has unknown Feature: {feature_id}/{task_id}")
        if task.get("status") not in STORED_TASK_STATES:
            errors.append(f"Task has invalid status: {feature_id}/{task_id}")
        try:
            repository_relative_path(root, str(task["path"]), "Task path")
            blockers_completed(root, task)
        except TrackerError as error:
            errors.append(str(error))
    if errors:
        raise TrackerError("check failed:\n- " + "\n- ".join(errors))
    print(f"check passed for {len(feature_ids)} Features and {len(load_tasks(root))} Tasks")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Git repository root; defaults to current directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--actor", required=True)
    init.add_argument("--display-name")
    init.add_argument("--executor-harness")
    init.add_argument("--executor-label")
    init.add_argument("--docs-root", default="docs/work")
    init.set_defaults(handler=command_init)

    whoami = subparsers.add_parser("whoami")
    whoami.set_defaults(handler=command_whoami)

    set_actor = subparsers.add_parser("set-actor")
    set_actor.add_argument("--actor", required=True)
    set_actor.add_argument("--display-name")
    set_actor.set_defaults(handler=command_set_actor)

    set_executor = subparsers.add_parser("set-executor")
    set_executor.add_argument("--harness", required=True)
    set_executor.add_argument("--label")
    set_executor.set_defaults(handler=command_set_executor)

    register_feature = subparsers.add_parser("register-feature")
    register_feature.add_argument("--id", required=True)
    register_feature.add_argument("--title", required=True)
    register_feature.add_argument("--owner", required=True)
    register_feature.add_argument("--milestone", required=True)
    register_feature.add_argument("--path", required=True)
    register_feature.set_defaults(handler=command_register_feature)

    register_task = subparsers.add_parser("register-task")
    register_task.add_argument("--feature", required=True)
    register_task.add_argument("--id", required=True)
    register_task.add_argument("--title", required=True)
    register_task.add_argument("--path", required=True)
    register_task.add_argument("--blocked-by", action="append")
    register_task.set_defaults(handler=command_register_task)

    assign = subparsers.add_parser("assign")
    assign.add_argument("--feature", required=True)
    assign.add_argument("--task", required=True)
    assign.add_argument("--assignee", required=True)
    assign.add_argument("--executor")
    assign.add_argument("--branch")
    assign.add_argument("--expect-revision", required=True, type=int)
    assign.set_defaults(handler=command_assign)

    transition = subparsers.add_parser("transition")
    transition.add_argument("--feature", required=True)
    transition.add_argument("--task", required=True)
    transition.add_argument("--to", required=True)
    transition.add_argument("--expect-revision", required=True, type=int)
    transition.add_argument("--reason")
    transition.add_argument("--branch")
    transition.add_argument("--mr")
    transition.add_argument("--evidence")
    transition.set_defaults(handler=command_transition)

    transition_feature = subparsers.add_parser("transition-feature")
    transition_feature.add_argument("--feature", required=True)
    transition_feature.add_argument("--to", required=True)
    transition_feature.add_argument("--expect-revision", required=True, type=int)
    transition_feature.add_argument("--reason")
    transition_feature.set_defaults(handler=command_transition_feature)

    close_feature = subparsers.add_parser("close-feature")
    close_feature.add_argument("--feature", required=True)
    close_feature.add_argument("--expect-revision", required=True, type=int)
    close_feature.add_argument("--confirmed-by", required=True)
    close_feature.add_argument("--evidence", required=True)
    close_feature.set_defaults(handler=command_close_feature)

    render = subparsers.add_parser("render")
    render.set_defaults(handler=command_render)

    check = subparsers.add_parser("check")
    check.set_defaults(handler=command_check)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        root = repository_root(args.root)
        args.handler(args, root)
    except TrackerError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
