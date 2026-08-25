#!/usr/bin/env python3
"""Dependency-free repository-local Feature owner index."""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path


VALID_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
FEATURE_STATES = {"planned", "in-progress", "blocked", "integration", "completed", "cancelled"}
FEATURE_TRANSITIONS = {
    "planned": {"in-progress", "blocked", "cancelled"},
    "in-progress": {"blocked", "integration", "cancelled"},
    "blocked": {"in-progress", "cancelled"},
    "integration": {"in-progress", "blocked", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}
DASHBOARD_START = "<!-- waypoint:dashboard:start -->"
DASHBOARD_END = "<!-- waypoint:dashboard:end -->"
COMPLETED_START = "<!-- waypoint:completed:start -->"
COMPLETED_END = "<!-- waypoint:completed:end -->"


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


def require_initialized(root: Path) -> dict[str, object]:
    config = parse_flat_yaml(config_path(root))
    if config.get("tracker_mode") != "local":
        raise TrackerError("Waypoint tracker is not configured for local mode")
    return config


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
            {"version": 2, "tracker_mode": "local", "docs_root": args.docs_root},
        )
        write_flat_yaml(
            local_path(root),
            {
                "version": 2,
                "actor_id": actor,
                "actor_display_name": args.display_name or actor,
            },
        )
        ensure_ignore_rules(root)
    print(f"initialized local Feature owner index for actor {actor}")


def command_whoami(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
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
                "version": 2,
                "feature_id": feature_id,
                "title": args.title,
                "summary": args.summary or "",
                "owner": owner,
                "milestone": args.milestone or "",
                "status": "planned",
                "path": str(feature_path.relative_to(root)),
                "evidence": "",
                "revision": 0,
            },
        )
    print(f"registered Feature {feature_id} revision 0")


def load_features(root: Path) -> list[dict[str, object]]:
    directory = root / ".waypoint" / "tracker" / "features"
    return [parse_flat_yaml(path) for path in sorted(directory.glob("*.yaml"))] if directory.exists() else []


def current_actor(root: Path) -> str:
    return validate_id(str(parse_flat_yaml(local_path(root)).get("actor_id", "")), "actor ID")


def command_list_features(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    owner = current_actor(root) if args.mine else args.owner
    if owner:
        owner = validate_id(owner, "Feature owner")
    features = load_features(root)
    selected = [
        feature
        for feature in features
        if (not owner or feature.get("owner") == owner)
        and (not args.active_only or feature.get("status") not in {"completed", "cancelled"})
    ]
    print(json.dumps(selected, ensure_ascii=False, indent=2))


def require_revision(record: dict[str, object], expected: int) -> None:
    actual = record.get("revision")
    if actual != expected:
        raise TrackerError(f"revision mismatch: expected {expected}, current {actual}")


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


def command_replan_feature(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    feature_id = validate_id(args.feature, "Feature ID")
    milestone = "" if args.standalone else validate_id(args.to_milestone, "Milestone ID")
    path = feature_record_path(root, feature_id)
    with mutation_lock(root):
        record = parse_flat_yaml(path)
        require_revision(record, args.expect_revision)
        status = str(record.get("status"))
        if status in {"completed", "cancelled"}:
            raise TrackerError(f"cannot replan a {status} Feature")
        if args.path is not None:
            if status != "planned":
                raise TrackerError(
                    "cannot move a Feature after execution begins; keep its document path stable"
                )
            new_feature = repository_relative_path(root, args.path, "Feature path")
            record["path"] = str(new_feature.relative_to(root))
        record["milestone"] = milestone
        record["replan_reason"] = args.reason
        record["revision"] = int(record["revision"]) + 1
        write_flat_yaml(path, record)
    destination = milestone or "standalone"
    print(f"replanned Feature {feature_id} to {destination} revision {record['revision']}")


def command_close_feature(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    feature_id = validate_id(args.feature, "Feature ID")
    path = feature_record_path(root, feature_id)
    with mutation_lock(root):
        record = parse_flat_yaml(path)
        require_revision(record, args.expect_revision)
        if args.confirmed_by != record.get("owner"):
            raise TrackerError(f"Feature completion must be confirmed by owner {record.get('owner')}")
        if record.get("status") in {"completed", "cancelled"}:
            raise TrackerError(f"Feature is already {record.get('status')}")
        record.update(
            {
                "status": "completed",
                "evidence": args.evidence,
                "completed_at": validate_date(
                    args.completed_at or date.today().isoformat(), "completion date"
                ),
                "revision": int(record["revision"]) + 1,
            }
        )
        write_flat_yaml(path, record)
    print(f"closed Feature {feature_id} revision {record['revision']}")


def validate_date(value: str, label: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise TrackerError(f"invalid {label} {value!r}; use YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise TrackerError(f"invalid {label} {value!r}; use YYYY-MM-DD")
    return value


def replace_region(text: str, start: str, end: str, heading: str, body: str) -> str:
    region = f"{start}\n{body.rstrip()}\n{end}"
    if start in text and end in text:
        before, remainder = text.split(start, 1)
        _, after = remainder.split(end, 1)
        return before + region + after
    separator = "\n" if text.endswith("\n") else "\n\n"
    return text + separator + f"## {heading}\n\n" + region + "\n"


def render_dashboard(root: Path, config: dict[str, object], features: list[dict[str, object]]) -> Path:
    docs_root = root / str(config.get("docs_root", "docs/work"))
    path = docs_root / "index.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text(encoding="utf-8") if path.exists() else "# Work\n"
    grouped: dict[str, list[str]] = {}
    for feature in features:
        if feature.get("status") in {"completed", "cancelled"}:
            continue
        feature_path = root / str(feature["path"])
        link = os.path.relpath(feature_path, path.parent)
        milestone = str(feature.get("milestone") or "Unscheduled")
        grouped.setdefault(milestone, []).append(
            f"| [{feature['title']}]({link}) | {feature['owner']} | {feature['status']} |"
        )
    table_header = ["| Feature | Owner | Status |", "| --- | --- | --- |"]
    if set(grouped) == {"Unscheduled"}:
        lines = [*table_header, *grouped["Unscheduled"]]
    else:
        lines = []
        for milestone in sorted(grouped):
            if lines:
                lines.append("")
            lines.extend([f"### {milestone}", "", *table_header, *grouped[milestone]])
    if not grouped:
        lines = ["No active Features."]
    path.write_text(
        replace_region(current, DASHBOARD_START, DASHBOARD_END, "Feature dashboard", "\n".join(lines)),
        encoding="utf-8",
    )
    return path


def render_completed(root: Path, config: dict[str, object], features: list[dict[str, object]]) -> Path:
    docs_root = root / str(config.get("docs_root", "docs/work"))
    path = docs_root / "completed.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text(encoding="utf-8") if path.exists() else "# Completed Features\n"
    completed = [feature for feature in features if feature.get("status") == "completed"]
    completed.sort(
        key=lambda feature: (
            validate_date(str(feature.get("completed_at", "")), "completion date"),
            str(feature.get("feature_id", "")),
        ),
        reverse=True,
    )
    lines = []
    for feature in completed:
        feature_path = root / str(feature["path"])
        link = os.path.relpath(feature_path, path.parent)
        entry = f"- {feature['completed_at']} — [{feature['title']}]({link})"
        if feature.get("summary"):
            entry += f" — {feature['summary']}"
        lines.append(entry)
    body = "\n".join(lines) if lines else "No completed Features yet."
    path.write_text(replace_region(current, COMPLETED_START, COMPLETED_END, "Timeline", body), encoding="utf-8")
    return path


def command_render(args: argparse.Namespace, root: Path) -> None:
    config = require_initialized(root)
    features = load_features(root)
    with mutation_lock(root):
        dashboard = render_dashboard(root, config, features)
        completed = render_completed(root, config, features)
    print(
        f"rendered {len(features)} Features to {dashboard.relative_to(root)} "
        f"and {completed.relative_to(root)}"
    )


def command_check(args: argparse.Namespace, root: Path) -> None:
    require_initialized(root)
    local = parse_flat_yaml(local_path(root))
    errors: list[str] = []
    try:
        validate_id(str(local.get("actor_id", "")), "actor ID")
    except TrackerError as error:
        errors.append(str(error))
    ignore_lines = (root / ".gitignore").read_text(encoding="utf-8").splitlines()
    if "/.waypoint/local.yaml" not in ignore_lines:
        errors.append(".waypoint/local.yaml is not ignored")
    feature_ids: set[str] = set()
    for feature in load_features(root):
        feature_id = str(feature.get("feature_id", ""))
        feature_ids.add(feature_id)
        try:
            validate_id(feature_id, "Feature ID")
            validate_id(str(feature.get("owner", "")), "Feature owner")
            if feature.get("status") not in FEATURE_STATES:
                raise TrackerError(f"invalid Feature status: {feature.get('status')}")
            repository_relative_path(root, str(feature["path"]), "Feature path")
            if feature.get("status") == "completed":
                validate_date(str(feature.get("completed_at", "")), "completion date")
        except TrackerError as error:
            errors.append(str(error))
    if errors:
        raise TrackerError("check failed:\n- " + "\n- ".join(errors))
    print(f"check passed for {len(feature_ids)} Features; local tracker stores no Task state")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Git repository root; defaults to current directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--actor", required=True)
    init.add_argument("--display-name")
    init.add_argument("--docs-root", default="docs/work")
    init.set_defaults(handler=command_init)

    whoami = subparsers.add_parser("whoami")
    whoami.set_defaults(handler=command_whoami)

    set_actor = subparsers.add_parser("set-actor")
    set_actor.add_argument("--actor", required=True)
    set_actor.add_argument("--display-name")
    set_actor.set_defaults(handler=command_set_actor)

    register_feature = subparsers.add_parser("register-feature")
    register_feature.add_argument("--id", required=True)
    register_feature.add_argument("--title", required=True)
    register_feature.add_argument("--summary")
    register_feature.add_argument("--owner", required=True)
    register_feature.add_argument("--milestone")
    register_feature.add_argument("--path", required=True)
    register_feature.set_defaults(handler=command_register_feature)

    list_features = subparsers.add_parser("list-features")
    owner_filter = list_features.add_mutually_exclusive_group()
    owner_filter.add_argument("--owner")
    owner_filter.add_argument("--mine", action="store_true")
    list_features.add_argument("--active-only", action="store_true")
    list_features.set_defaults(handler=command_list_features)

    transition_feature = subparsers.add_parser("transition-feature")
    transition_feature.add_argument("--feature", required=True)
    transition_feature.add_argument("--to", required=True)
    transition_feature.add_argument("--expect-revision", required=True, type=int)
    transition_feature.add_argument("--reason")
    transition_feature.set_defaults(handler=command_transition_feature)

    replan_feature = subparsers.add_parser("replan-feature")
    replan_feature.add_argument("--feature", required=True)
    replan_destination = replan_feature.add_mutually_exclusive_group(required=True)
    replan_destination.add_argument("--to-milestone")
    replan_destination.add_argument("--standalone", action="store_true")
    replan_feature.add_argument("--path")
    replan_feature.add_argument("--expect-revision", required=True, type=int)
    replan_feature.add_argument("--reason", required=True)
    replan_feature.set_defaults(handler=command_replan_feature)

    close_feature = subparsers.add_parser("close-feature")
    close_feature.add_argument("--feature", required=True)
    close_feature.add_argument("--expect-revision", required=True, type=int)
    close_feature.add_argument("--confirmed-by", required=True)
    close_feature.add_argument("--evidence", required=True)
    close_feature.add_argument("--completed-at")
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
