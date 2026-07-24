#!/usr/bin/env python3
"""Validate the Stewards plugin carriers and marketplace observations."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "stewards"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
SURFACE_ID = re.compile(r"^[a-z0-9][a-z0-9._/-]{0,127}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-f]{40}$")
STEP_ID = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]{0,127}$")
OBSERVED_AT = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
)


class Invalid(ValueError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise Invalid(f"{path}: invalid JSON: {error}") from error


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise Invalid(f"{label}: expected object")
    return value


def require_closed(
    value: Any, label: str, fields: Iterable[str]
) -> dict[str, Any]:
    obj = require_object(value, label)
    expected = set(fields)
    actual = set(obj)
    unknown = sorted(actual - expected)
    missing = sorted(expected - actual)
    if unknown:
        raise Invalid(f"{label}: unknown properties: {', '.join(unknown)}")
    if missing:
        raise Invalid(f"{label}: missing properties: {', '.join(missing)}")
    return obj


def require_string(value: Any, label: str, *, nonblank: bool = True) -> str:
    if not isinstance(value, str):
        raise Invalid(f"{label}: expected string")
    if nonblank and not value.strip():
        raise Invalid(f"{label}: must be nonblank")
    return value


def require_positive_integer(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise Invalid(f"{label}: expected positive integer")
    return value


def require_regex(value: Any, label: str, pattern: re.Pattern[str]) -> str:
    text = require_string(value, label)
    if pattern.fullmatch(text) is None:
        raise Invalid(f"{label}: invalid value {text!r}")
    return text


def require_bounded_text(value: Any, label: str, limit: int) -> str:
    text = require_string(value, label)
    if len(text.encode("utf-8")) > limit:
        raise Invalid(f"{label}: exceeds {limit} UTF-8 bytes")
    return text


def normalized_relative_json_path(value: Any, label: str) -> str:
    text = require_string(value, label)
    path = PurePosixPath(text)
    if (
        path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or text != path.as_posix()
        or path.suffix != ".json"
    ):
        raise Invalid(f"{label}: expected normalized repository-relative JSON path")
    return text


def validate_observation(value: Any, label: str) -> dict[str, Any]:
    observation = require_closed(
        value,
        label,
        (
            "schema_version",
            "host",
            "surface_id",
            "marketplace",
            "execution",
            "observed_at",
        ),
    )
    if observation["schema_version"] != 1 or isinstance(
        observation["schema_version"], bool
    ):
        raise Invalid(f"{label}.schema_version: expected integer 1")
    if observation["host"] not in ("claude", "codex"):
        raise Invalid(f"{label}.host: expected 'claude' or 'codex'")
    require_regex(observation["surface_id"], f"{label}.surface_id", SURFACE_ID)

    marketplace = require_closed(
        observation["marketplace"],
        f"{label}.marketplace",
        ("name", "repository", "revision"),
    )
    require_bounded_text(
        marketplace["name"], f"{label}.marketplace.name", 128
    )
    require_regex(
        marketplace["repository"],
        f"{label}.marketplace.repository",
        REPOSITORY,
    )
    require_regex(
        marketplace["revision"], f"{label}.marketplace.revision", SHA
    )

    execution = require_closed(
        observation["execution"],
        f"{label}.execution",
        (
            "repository",
            "commit",
            "workflow",
            "job",
            "run_id",
            "run_attempt",
            "setup_step_id",
        ),
    )
    require_regex(
        execution["repository"], f"{label}.execution.repository", REPOSITORY
    )
    require_regex(execution["commit"], f"{label}.execution.commit", SHA)
    workflow = require_string(
        execution["workflow"], f"{label}.execution.workflow"
    )
    workflow_path = PurePosixPath(workflow)
    if (
        workflow_path.is_absolute()
        or len(workflow_path.parts) < 3
        or workflow_path.parts[:2] != (".github", "workflows")
        or ".." in workflow_path.parts
        or "." in workflow_path.parts
        or workflow != workflow_path.as_posix()
        or workflow_path.suffix not in (".yml", ".yaml")
    ):
        raise Invalid(
            f"{label}.execution.workflow: expected normalized path below "
            ".github/workflows/"
        )
    require_bounded_text(execution["job"], f"{label}.execution.job", 128)
    require_positive_integer(
        execution["run_id"], f"{label}.execution.run_id"
    )
    require_positive_integer(
        execution["run_attempt"], f"{label}.execution.run_attempt"
    )
    require_regex(
        execution["setup_step_id"], f"{label}.execution.setup_step_id", STEP_ID
    )

    observed_at = require_regex(
        observation["observed_at"], f"{label}.observed_at", OBSERVED_AT
    )
    try:
        datetime.strptime(observed_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as error:
        raise Invalid(f"{label}.observed_at: invalid UTC instant") from error
    return observation


def validate_manifest(path: Path, version: str) -> None:
    manifest = require_object(load_json(path), str(path))
    if manifest.get("name") != "stewards":
        raise Invalid(f"{path}: name must equal 'stewards'")
    if manifest.get("version") != version:
        raise Invalid(f"{path}: version must equal VERSION {version!r}")


def find_catalog_entry(path: Path) -> dict[str, Any] | None:
    catalog = require_object(load_json(path), str(path))
    plugins = catalog.get("plugins")
    if not isinstance(plugins, list):
        raise Invalid(f"{path}: plugins must be an array")
    entries = [
        require_object(item, f"{path}.plugins[{index}]")
        for index, item in enumerate(plugins)
        if isinstance(item, dict) and item.get("name") == "stewards"
    ]
    if len(entries) > 1:
        raise Invalid(f"{path}: duplicate stewards catalog entries")
    return entries[0] if entries else None


def validate_catalogs(version: str) -> None:
    claude_path = ROOT / ".claude-plugin" / "marketplace.json"
    codex_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    claude = find_catalog_entry(claude_path)
    codex = find_catalog_entry(codex_path)
    if claude is not None:
        expected = {
            "name": "stewards",
            "source": "./plugins/stewards",
        }
        if {key: claude.get(key) for key in expected} != expected:
            raise Invalid(
                f"{claude_path}: stewards entry must use source "
                "'./plugins/stewards'"
            )
        report = (
            PLUGIN
            / "reference"
            / "surfaces"
            / f"claude-catalog-admission-{version}.md"
        )
        if not report.is_file():
            raise Invalid(f"{claude_path}: missing admission report {report}")
    if codex is not None:
        expected = {
            "name": "stewards",
            "source": {"source": "local", "path": "./plugins/stewards"},
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Developer Tools",
        }
        if codex != expected:
            raise Invalid(
                f"{codex_path}: stewards entry does not match the exact "
                "Codex local-source shape"
            )
        report = (
            PLUGIN
            / "reference"
            / "surfaces"
            / f"codex-catalog-admission-{version}.md"
        )
        if not report.is_file():
            raise Invalid(f"{codex_path}: missing admission report {report}")


def validate_surfaces(version: str) -> None:
    path = PLUGIN / "surfaces.json"
    surfaces = require_closed(
        load_json(path), str(path), ("schema_version", "version", "rows")
    )
    if surfaces["schema_version"] != 1 or isinstance(
        surfaces["schema_version"], bool
    ):
        raise Invalid(f"{path}.schema_version: expected integer 1")
    if surfaces["version"] != version:
        raise Invalid(f"{path}.version: must equal VERSION {version!r}")
    rows = surfaces["rows"]
    if not isinstance(rows, list):
        raise Invalid(f"{path}.rows: expected array")
    seen: set[str] = set()
    for index, value in enumerate(rows):
        label = f"{path}.rows[{index}]"
        row = require_closed(
            value,
            label,
            ("surface_id", "host", "marketplace_test_observations"),
        )
        surface_id = require_regex(
            row["surface_id"], f"{label}.surface_id", SURFACE_ID
        )
        if surface_id in seen:
            raise Invalid(f"{label}.surface_id: duplicate {surface_id!r}")
        seen.add(surface_id)
        host = row["host"]
        if host not in ("claude", "codex"):
            raise Invalid(f"{label}.host: expected 'claude' or 'codex'")
        observations = row["marketplace_test_observations"]
        if not isinstance(observations, list):
            raise Invalid(
                f"{label}.marketplace_test_observations: expected array"
            )
        for obs_index, raw_observation_path in enumerate(observations):
            obs_label = (
                f"{label}.marketplace_test_observations[{obs_index}]"
            )
            relative = normalized_relative_json_path(
                raw_observation_path, obs_label
            )
            observation_path = ROOT / relative
            observation = validate_observation(
                load_json(observation_path), str(observation_path)
            )
            if observation["host"] != host:
                raise Invalid(f"{observation_path}: host does not match row")
            if observation["surface_id"] != surface_id:
                raise Invalid(
                    f"{observation_path}: surface_id does not match row"
                )


def validate_repository() -> None:
    version_path = PLUGIN / "VERSION"
    try:
        version = version_path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as error:
        raise Invalid(f"{version_path}: cannot read VERSION: {error}") from error
    if SEMVER.fullmatch(version) is None:
        raise Invalid(f"{version_path}: expected valid SemVer")
    validate_manifest(PLUGIN / ".claude-plugin" / "plugin.json", version)
    validate_manifest(PLUGIN / ".codex-plugin" / "plugin.json", version)
    validate_surfaces(version)
    validate_catalogs(version)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--observation",
        type=Path,
        help="Validate one spec-0003 marketplace observation instead",
    )
    args = parser.parse_args()
    try:
        if args.observation:
            validate_observation(
                load_json(args.observation), str(args.observation)
            )
            print(
                "marketplace observation structural validation passed; "
                f"runtime provenance unverified: {args.observation}"
            )
        else:
            validate_repository()
            print("stewards plugin validation passed")
    except Invalid as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
