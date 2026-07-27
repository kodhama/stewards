#!/usr/bin/env python3
"""Validate the Kodhama plugin's version carriers and catalog entries.

Scope is deliberately small (`kodhama-0025`): VERSION is valid SemVer, both
host manifests agree with it, and any present catalog entry has the right
shape and carries its non-support disclosure. The surface matrix and the
marketplace-observation record are retired — nothing read their values, and
what proves the package installs is `scripts/keyless_admission_check.py`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "kodhama"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
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


def validate_manifest(path: Path, version: str) -> None:
    manifest = require_object(load_json(path), str(path))
    if manifest.get("name") != "kodhama":
        raise Invalid(f"{path}: name must equal 'kodhama'")
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
        if isinstance(item, dict) and item.get("name") == "kodhama"
    ]
    if len(entries) > 1:
        raise Invalid(f"{path}: duplicate kodhama catalog entries")
    return entries[0] if entries else None


def validate_catalogs(version: str) -> None:
    claude_path = ROOT / ".claude-plugin" / "marketplace.json"
    codex_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    claude = find_catalog_entry(claude_path)
    codex = find_catalog_entry(codex_path)
    # `kodhama-0021` §2 admits a dogfood or preview listing only when "the
    # listing or linked product documentation clearly discloses that support is
    # not claimed", and AC3 adds that catalog presence never implies support.
    # No such disclosure exists anywhere else in this repository, so the entry's
    # own `description` is the only carrier — hence required, on both hosts.
    # Its exact wording is pinned by the tests, next to the trellis and wisp
    # descriptions that carry the same disclosure.
    if claude is not None:
        expected = {
            "name": "kodhama",
            "source": "./plugins/kodhama",
        }
        if {key: claude.get(key) for key in expected} != expected:
            raise Invalid(
                f"{claude_path}: kodhama entry must use source "
                "'./plugins/kodhama'"
            )
        require_string(
            claude.get("description"), f"{claude_path}: kodhama description"
        )
    if codex is not None:
        expected = {
            "name": "kodhama",
            "source": {"source": "local", "path": "./plugins/kodhama"},
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Developer Tools",
        }
        # Closed rather than compared for whole-object equality. Equality
        # rejected *any* additional field — including `description`, which the
        # sibling trellis and wisp Codex entries both carry and which the real
        # host accepts (`codex plugin marketplace add` takes this file, and
        # `codex plugin add kodhama@kodhama` installs from it on 0.145.0). It
        # was stricter than the catalog it validates. Merely relaxing it to a
        # key-by-key subset would have gone too far the other way: Codex itself
        # accepts unknown entry fields silently, so a typo like `"instalation"`
        # would have passed both this check and the host. Closing the object
        # keeps the typo rejected while admitting the description.
        codex = require_closed(
            codex,
            f"{codex_path}: kodhama entry",
            (*expected, "description"),
        )
        if {key: codex[key] for key in expected} != expected:
            raise Invalid(
                f"{codex_path}: kodhama entry must use the Codex "
                "local-source shape"
            )
        require_string(
            codex["description"], f"{codex_path}: kodhama description"
        )
    # Admission evidence is `scripts/keyless_admission_check.py`, which runs.
    # This validator previously demanded a hand-written six-part smoke report
    # under `plugins/kodhama/reference/surfaces/`, against fixtures under
    # `plugins/kodhama/tests/fixtures/`. Neither path has ever existed, so the
    # requirement was unsatisfiable — and invisible, because it fires only when
    # a `kodhama` catalog entry is present, which it never has been. Publishing
    # would have failed CI on an artifact nobody could produce.


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
    validate_catalogs(version)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    try:
        validate_repository()
        print("kodhama plugin validation passed")
    except Invalid as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
