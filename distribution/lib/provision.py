"""Bounded, host-neutral pre-agent provisioner protocol.

The current availability source contains no candidate or verified route.
Consequently this module implements the request, resolution-failure, audit,
and receipt boundary without providing a host mutation adapter.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, Iterable, Optional, Sequence

from .manage import (
    DOT_ID,
    PLUGIN_ID,
    SEMVER,
    canonical_json,
    load_json,
    load_json_bytes,
    validate_provisioners,
    validate_surface_registry,
)


PROVISIONER_VERSION = "0.1.0"
UUID_V4 = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
ENV_NAME = re.compile(r"^[A-Z_][A-Z0-9_]*$")
REFERENCE_KINDS = {
    "authentication-env",
    "mounted-configuration",
    "trust-store",
    "runtime-command",
    "writable-state",
}
HOSTS = {"claude-code", "codex"}


class OutputContractError(ValueError):
    """The two explicit protocol output paths cannot be safely sealed."""


def timestamp() -> str:
    """Return an RFC 3339 UTC whole-second timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def absolute_normalized_path(value: Any) -> bool:
    """Return whether value is an absolute normalized non-root POSIX path."""
    if not isinstance(value, str) or "\x00" in value:
        return False
    if not value.startswith("/") or value == "/" or value.endswith("/"):
        return False
    parts = value.split("/")[1:]
    return bool(parts) and all(part not in ("", ".", "..") for part in parts)


def is_within(path: Path, root: Path) -> bool:
    """Return whether path is root or a descendant of root."""
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_output_leaf(path_text: str, label: str) -> Path:
    """Validate a normalized, absent, non-symlinked output leaf and parent."""
    if not absolute_normalized_path(path_text):
        raise OutputContractError(f"{label}: path is not absolute and normalized")
    path = Path(path_text)
    parent = path.parent
    try:
        resolved_parent = parent.resolve(strict=True)
    except OSError as exc:
        raise OutputContractError(f"{label}: parent cannot be resolved") from exc
    if str(resolved_parent) != str(parent):
        raise OutputContractError(f"{label}: parent contains a symlink")
    if not parent.is_dir():
        raise OutputContractError(f"{label}: parent is not a directory")
    if path.exists() or path.is_symlink():
        raise OutputContractError(f"{label}: leaf already exists")
    return path


def write_once(path: Path, raw: bytes) -> None:
    """Exclusively create, write, flush, and close one protocol output."""
    descriptor = os.open(
        str(path),
        os.O_CREAT | os.O_EXCL | os.O_WRONLY,
        0o600,
    )
    try:
        written = 0
        while written < len(raw):
            written += os.write(descriptor, raw[written:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def cause(
    code: str,
    source: str,
    field_path: str,
    reference_ids: Iterable[str] = (),
) -> dict[str, Any]:
    """Build one exact diagnostic cause."""
    return {
        "code": code,
        "source": source,
        "field_path": field_path,
        "reference_ids": sorted(set(reference_ids)),
    }


def diagnostic(
    causes: list[dict[str, Any]],
    owner: str,
    message: str,
    retryable: bool = False,
) -> dict[str, Any]:
    """Build one deterministic diagnostic from already ranked causes."""
    primary = causes[0]
    return {
        "code": primary["code"],
        "message": message,
        "owner": owner,
        "retryable": retryable,
        "reference_ids": sorted(
            {
                reference_id
                for item in causes
                for reference_id in item["reference_ids"]
            }
        ),
        "causes": causes,
    }


def tuple_positions(document: Any) -> list[dict[str, Any]]:
    """Enumerate every decodable target/plugin position."""
    positions: list[dict[str, Any]] = []
    if not isinstance(document, dict) or not isinstance(document.get("targets"), list):
        return positions
    for target_index, target in enumerate(document["targets"]):
        if not isinstance(target, dict) or not isinstance(target.get("plugins"), list):
            continue
        for plugin_index, plugin in enumerate(target["plugins"]):
            position: dict[str, Any] = {
                "result_id": f"t{target_index}.p{plugin_index}",
                "target_index": target_index,
                "plugin_index": plugin_index,
            }
            if isinstance(target.get("host"), str):
                position["host"] = target["host"]
            if isinstance(target.get("surface_id"), str):
                position["surface_id"] = target["surface_id"]
            if isinstance(plugin, dict):
                for field in ("plugin_id", "package_version", "route_id"):
                    if isinstance(plugin.get(field), str):
                        position[field] = plugin[field]
            positions.append(position)
    return positions


def skip_result(position: dict[str, Any]) -> dict[str, Any]:
    """Build the global request-validation skipped variant."""
    return {
        **position,
        "phase": "request-validation",
        "outcome": "skipped",
        "blocked_by": {"kind": "request-validation"},
        "diagnostic": diagnostic(
            [cause("invalid-request", "result", "")],
            "consumer/environment",
            "Request validation prevented this tuple from starting.",
        ),
    }


def failed_validation_result(
    position: dict[str, Any],
    causes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a request-validation failure variant."""
    return {
        **position,
        "phase": "request-validation",
        "outcome": "failed",
        "diagnostic": diagnostic(
            causes,
            "consumer/environment",
            "The requested tuple is invalid.",
        ),
    }


def phase_one(
    document: Any,
    positions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    """Validate JSON envelope and structural request grammar."""
    envelope: list[dict[str, Any]] = []
    assigned: dict[str, list[dict[str, Any]]] = {}
    if not isinstance(document, dict):
        return [cause("invalid-request", "request", "")], assigned

    expected = {
        "schema_version",
        "request_id",
        "provisioner_version",
        "targets",
        "environment",
    }
    for field in sorted(expected - set(document)):
        envelope.append(cause("invalid-request", "request", f"/{field}"))
    for field in sorted(set(document) - expected):
        envelope.append(cause("invalid-request", "request", f"/{field}"))
    if document.get("schema_version") != 1:
        envelope.append(cause("invalid-request", "request", "/schema_version"))
    if not isinstance(document.get("request_id"), str) or not UUID_V4.fullmatch(
        document["request_id"]
    ):
        envelope.append(cause("invalid-request", "request", "/request_id"))
    version = document.get("provisioner_version")
    if (
        not isinstance(version, str)
        or SEMVER.fullmatch(version) is None
        or version != PROVISIONER_VERSION
    ):
        envelope.append(cause("invalid-request", "request", "/provisioner_version"))

    targets = document.get("targets")
    if not isinstance(targets, list) or not targets:
        envelope.append(cause("invalid-request", "request", "/targets"))
        return envelope, assigned

    position_map = {
        (position["target_index"], position["plugin_index"]): position
        for position in positions
    }
    target_expected = {"host", "surface_id", "environment_ref_ids", "plugins"}
    plugin_expected = {"plugin_id", "package_version", "route_id"}
    for target_index, target in enumerate(targets):
        if not isinstance(target, dict):
            envelope.append(
                cause("invalid-request", "request", f"/targets/{target_index}")
            )
            continue
        target_bad = set(target) != target_expected
        target_bad = target_bad or target.get("host") not in HOSTS
        target_bad = target_bad or not isinstance(target.get("surface_id"), str)
        target_bad = target_bad or (
            isinstance(target.get("surface_id"), str)
            and DOT_ID.fullmatch(target["surface_id"]) is None
        )
        references = target.get("environment_ref_ids")
        target_bad = target_bad or not isinstance(references, list)
        if isinstance(references, list):
            target_bad = target_bad or any(
                not isinstance(item, str) or DOT_ID.fullmatch(item) is None
                for item in references
            )
        plugins = target.get("plugins")
        if not isinstance(plugins, list):
            envelope.append(
                cause(
                    "invalid-request",
                    "request",
                    f"/targets/{target_index}/plugins",
                )
            )
            continue
        if not plugins:
            envelope.append(
                cause(
                    "invalid-request",
                    "request",
                    f"/targets/{target_index}/plugins",
                )
            )
        if target_bad:
            for plugin_index in range(len(plugins)):
                position = position_map[(target_index, plugin_index)]
                assigned[position["result_id"]] = [
                    cause(
                        "invalid-request",
                        "request",
                        f"/targets/{target_index}",
                    )
                ]
            continue
        for plugin_index, plugin in enumerate(plugins):
            position = position_map[(target_index, plugin_index)]
            invalid_paths: list[str] = []
            if not isinstance(plugin, dict):
                invalid_paths.append(
                    f"/targets/{target_index}/plugins/{plugin_index}"
                )
            else:
                if set(plugin) != plugin_expected:
                    invalid_paths.append(
                        f"/targets/{target_index}/plugins/{plugin_index}"
                    )
                if not isinstance(plugin.get("plugin_id"), str) or PLUGIN_ID.fullmatch(
                    plugin["plugin_id"]
                ) is None:
                    invalid_paths.append(
                        f"/targets/{target_index}/plugins/{plugin_index}/plugin_id"
                    )
                package_version = plugin.get("package_version")
                if (
                    not isinstance(package_version, str)
                    or SEMVER.fullmatch(package_version) is None
                ):
                    invalid_paths.append(
                        f"/targets/{target_index}/plugins/{plugin_index}/package_version"
                    )
                if not isinstance(plugin.get("route_id"), str) or DOT_ID.fullmatch(
                    plugin["route_id"]
                ) is None:
                    invalid_paths.append(
                        f"/targets/{target_index}/plugins/{plugin_index}/route_id"
                    )
            if invalid_paths:
                assigned[position["result_id"]] = [
                    cause("invalid-request", "request", path)
                    for path in sorted(set(invalid_paths))
                ]

    environment = document.get("environment")
    if not isinstance(environment, dict) or set(environment) != {
        "state_roots",
        "references",
    }:
        envelope.append(cause("invalid-request", "request", "/environment"))
        return envelope, assigned
    roots = environment.get("state_roots")
    references = environment.get("references")
    if not isinstance(roots, list):
        envelope.append(
            cause("invalid-request", "request", "/environment/state_roots")
        )
    else:
        for index, row in enumerate(roots):
            if (
                not isinstance(row, dict)
                or set(row) != {"host", "path"}
                or row.get("host") not in HOSTS
                or not isinstance(row.get("path"), str)
            ):
                envelope.append(
                    cause(
                        "invalid-request",
                        "request",
                        f"/environment/state_roots/{index}",
                    )
                )
    if not isinstance(references, list):
        envelope.append(
            cause("invalid-request", "request", "/environment/references")
        )
    else:
        for index, row in enumerate(references):
            path = f"/environment/references/{index}"
            if (
                not isinstance(row, dict)
                or set(row) != {"reference_id", "kind", "locator"}
                or not isinstance(row.get("reference_id"), str)
                or DOT_ID.fullmatch(row["reference_id"]) is None
                or row.get("kind") not in REFERENCE_KINDS
                or not isinstance(row.get("locator"), str)
            ):
                envelope.append(cause("invalid-request", "request", path))
                continue
            locator = row["locator"]
            if row["kind"] == "authentication-env":
                if ENV_NAME.fullmatch(locator) is None:
                    envelope.append(
                        cause("invalid-request", "request", f"{path}/locator")
                    )
    return envelope, assigned


def request_validation_results(
    positions: list[dict[str, Any]],
    assigned: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Finalize all tuple positions after a global validation failure."""
    return [
        failed_validation_result(position, assigned[position["result_id"]])
        if position["result_id"] in assigned
        else skip_result(position)
        for position in positions
    ]


def phase_two_causes(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate all state-root and non-authentication locator paths."""
    causes: list[dict[str, Any]] = []
    for index, row in enumerate(document["environment"]["state_roots"]):
        if not absolute_normalized_path(row["path"]):
            causes.append(
                cause(
                    "unsafe-path",
                    "request",
                    f"/environment/state_roots/{index}/path",
                )
            )
    for index, row in enumerate(document["environment"]["references"]):
        if row["kind"] != "authentication-env" and not absolute_normalized_path(
            row["locator"]
        ):
            causes.append(
                cause(
                    "unsafe-path",
                    "request",
                    f"/environment/references/{index}/locator",
                    [row["reference_id"]],
                )
            )
    return causes


def phase_three(
    document: dict[str, Any],
    positions: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Validate target, plugin, root, reference, and selection uniqueness."""
    assigned: dict[str, list[dict[str, Any]]] = {}
    by_position = {
        (item["target_index"], item["plugin_index"]): item for item in positions
    }
    canonical_targets: dict[tuple[str, str], int] = {}
    for target_index, target in enumerate(document["targets"]):
        key = (target["host"], target["surface_id"])
        if key in canonical_targets:
            for plugin_index in range(len(target["plugins"])):
                item = by_position[(target_index, plugin_index)]
                assigned[item["result_id"]] = [
                    cause(
                        "duplicate-target",
                        "request",
                        f"/targets/{target_index}",
                    )
                ]
            continue
        canonical_targets[key] = target_index
        canonical_plugins: dict[str, int] = {}
        for plugin_index, plugin in enumerate(target["plugins"]):
            plugin_id = plugin["plugin_id"]
            if plugin_id in canonical_plugins:
                item = by_position[(target_index, plugin_index)]
                assigned[item["result_id"]] = [
                    cause(
                        "duplicate-plugin",
                        "request",
                        f"/targets/{target_index}/plugins/{plugin_index}",
                    )
                ]
            else:
                canonical_plugins[plugin_id] = plugin_index
        if len(set(target["environment_ref_ids"])) != len(
            target["environment_ref_ids"]
        ):
            for plugin_index in range(len(target["plugins"])):
                item = by_position[(target_index, plugin_index)]
                current = assigned.setdefault(item["result_id"], [])
                if not current or current[0]["code"] != "duplicate-target":
                    current.append(
                        cause(
                            "duplicate-reference",
                            "request",
                            f"/targets/{target_index}/environment_ref_ids",
                        )
                    )

    root_hosts: dict[str, int] = {}
    for index, row in enumerate(document["environment"]["state_roots"]):
        if row["host"] in root_hosts:
            for item in positions:
                if item.get("host") == row["host"]:
                    current = assigned.setdefault(item["result_id"], [])
                    if current and current[0]["code"] == "duplicate-target":
                        continue
                    current.append(
                        cause(
                            "duplicate-state-root",
                            "request",
                            f"/environment/state_roots/{index}",
                        )
                    )
        else:
            root_hosts[row["host"]] = index

    reference_ids: dict[str, int] = {}
    reference_pairs: dict[tuple[str, str], int] = {}
    duplicate_ids: set[str] = set()
    for index, row in enumerate(document["environment"]["references"]):
        if row["reference_id"] in reference_ids:
            duplicate_ids.add(row["reference_id"])
        else:
            reference_ids[row["reference_id"]] = index
        pair = (row["kind"], row["locator"])
        if pair in reference_pairs:
            duplicate_ids.add(row["reference_id"])
            duplicate_ids.add(
                document["environment"]["references"][reference_pairs[pair]][
                    "reference_id"
                ]
            )
        else:
            reference_pairs[pair] = index
    for target_index, target in enumerate(document["targets"]):
        if duplicate_ids.intersection(target["environment_ref_ids"]):
            for plugin_index in range(len(target["plugins"])):
                item = by_position[(target_index, plugin_index)]
                current = assigned.setdefault(item["result_id"], [])
                if current and current[0]["code"] == "duplicate-target":
                    continue
                current.append(
                    cause(
                        "duplicate-reference",
                        "request",
                        f"/targets/{target_index}/environment_ref_ids",
                        duplicate_ids.intersection(target["environment_ref_ids"]),
                    )
                )
    rank = {
        "duplicate-target": 0,
        "duplicate-plugin": 1,
        "duplicate-state-root": 2,
        "duplicate-reference": 3,
    }
    for causes in assigned.values():
        causes.sort(
            key=lambda item: (
                rank[item["code"]],
                item["source"],
                item["field_path"],
                item["reference_ids"],
            )
        )
    return assigned


def phase_four(
    root: Path,
    document: dict[str, Any],
    positions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    """Validate surface/host, state-root coverage, and selected references."""
    envelope: list[dict[str, Any]] = []
    assigned: dict[str, list[dict[str, Any]]] = {}
    by_position = {
        (item["target_index"], item["plugin_index"]): item for item in positions
    }
    registry = validate_surface_registry(
        load_json(root / "distribution" / "surfaces.json")
    )
    surfaces = {
        row["surface_id"]: row
        for row in registry["surfaces"]
        if row["lifecycle"] == "active"
    }
    root_hosts = {
        row["host"] for row in document["environment"]["state_roots"]
    }
    targeted_hosts = {target["host"] for target in document["targets"]}
    for host in sorted(root_hosts - targeted_hosts):
        envelope.append(
            cause("invalid-request", "request", "/environment/state_roots")
        )
    reference_ids = {
        row["reference_id"] for row in document["environment"]["references"]
    }
    for target_index, target in enumerate(document["targets"]):
        target_causes: list[dict[str, Any]] = []
        surface = surfaces.get(target["surface_id"])
        if surface is None or surface["host"] != target["host"]:
            target_causes.append(
                cause(
                    "host-surface-mismatch",
                    "request",
                    f"/targets/{target_index}/surface_id",
                )
            )
        if target["host"] not in root_hosts:
            target_causes.append(
                cause(
                    "missing-state-root",
                    "request",
                    "/environment/state_roots",
                )
            )
        unknown = [
            reference_id
            for reference_id in target["environment_ref_ids"]
            if reference_id not in reference_ids
        ]
        if unknown:
            target_causes.append(
                cause(
                    "invalid-request",
                    "request",
                    f"/targets/{target_index}/environment_ref_ids",
                    unknown,
                )
            )
        if target_causes:
            for plugin_index in range(len(target["plugins"])):
                item = by_position[(target_index, plugin_index)]
                assigned[item["result_id"]] = target_causes
    return envelope, assigned


def route_failure(
    position: dict[str, Any],
    code: str,
    field_path: str,
) -> dict[str, Any]:
    """Build a route-boundary resolution failure."""
    route_id = position.get("route_id")
    references = [route_id] if isinstance(route_id, str) else []
    return {
        **position,
        "phase": "identity-resolution",
        "outcome": "failed",
        "diagnostic": diagnostic(
            [cause(code, "provisioners", field_path, references)],
            "stewards",
            f"Provisioning route resolution failed: {code}.",
        ),
    }


def resolve_routes(
    root: Path,
    positions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Resolve complete availability keys and fail closed before mutation."""
    provisioners = validate_provisioners(
        load_json(root / "distribution" / "provisioners.json")
    )
    sorted_records = sorted(
        provisioners["records"],
        key=lambda row: (
            row["route_id"],
            row["surface_id"],
            row["plugin_id"],
            row["package_version"],
            row["state"],
        ),
    )
    failures: dict[str, dict[str, Any]] = {}
    resolved: list[dict[str, Any]] = []
    for position in positions:
        key = (
            position["route_id"],
            position["surface_id"],
            position["plugin_id"],
            position["package_version"],
        )
        rows = [
            (index, row)
            for index, row in enumerate(sorted_records)
            if (
                row["route_id"],
                row["surface_id"],
                row["plugin_id"],
                row["package_version"],
            )
            == key
        ]
        if len(rows) > 1:
            failures[position["result_id"]] = route_failure(
                position,
                "route-ambiguous",
                "/records",
            )
        elif not rows:
            failures[position["result_id"]] = route_failure(
                position,
                "route-not-found",
                "/records",
            )
        else:
            index, row = rows[0]
            if row["state"] == "unavailable":
                failures[position["result_id"]] = route_failure(
                    position,
                    "route-unavailable",
                    f"/records/{index}/state",
                )
            elif row["provisioner_version"] != PROVISIONER_VERSION:
                failures[position["result_id"]] = route_failure(
                    position,
                    "route-version-mismatch",
                    f"/records/{index}/provisioner_version",
                )
            else:
                resolved.append(position)
    for position in resolved:
        failures[position["result_id"]] = {
            **position,
            "phase": "identity-resolution",
            "outcome": "failed",
            "diagnostic": diagnostic(
                [
                    cause(
                        "unresolved-release",
                        "execution",
                        f"/results/{position['result_id']}/identity-resolution",
                        [position["route_id"]],
                    )
                ],
                "stewards",
                "No executable host route adapter is present in this build.",
            ),
        }
    return [failures[position["result_id"]] for position in positions], resolved


def unused_reference_diagnostics(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the phase-six envelope diagnostics."""
    used = {
        reference_id
        for target in document["targets"]
        for reference_id in target["environment_ref_ids"]
    }
    unused = [
        row["reference_id"]
        for row in document["environment"]["references"]
        if row["reference_id"] not in used
    ]
    if not unused:
        return []
    causes = [
        cause(
            "unused-reference",
            "request",
            f"/environment/references/{index}",
            [row["reference_id"]],
        )
        for index, row in enumerate(document["environment"]["references"])
        if row["reference_id"] in unused
    ]
    return [
        diagnostic(
            causes,
            "consumer/environment",
            "The request contains an unused environment reference.",
        )
    ]


def build_audit(
    request_id: Optional[str],
    receipt: Path,
    audit: Path,
    document: Any,
    sealed_at: str,
) -> dict[str, Any]:
    """Build the self-digest-free process-tree write audit."""
    preflight: list[dict[str, str]] = []
    if isinstance(document, dict) and isinstance(document.get("environment"), dict):
        roots = document["environment"].get("state_roots")
        if isinstance(roots, list) and isinstance(request_id, str):
            for row in roots:
                if (
                    isinstance(row, dict)
                    and absolute_normalized_path(row.get("path"))
                ):
                    path = (
                        PurePosixPath(row["path"])
                        / ".kodhama-provision"
                        / "tmp"
                        / request_id
                    )
                    preflight.append(
                        {
                            "path": str(path),
                            "match": "subtree",
                            "classification": "receipt-evidence-scratch",
                        }
                    )
    return {
        "schema_version": 1,
        "request_id": request_id,
        "exempt_output_paths": sorted([str(receipt), str(audit)]),
        "preflight_allowed_write_set": sorted(
            preflight,
            key=lambda row: row["path"],
        ),
        "tuple_allowed_write_sets": [],
        "events": [],
        "sealed_at": sealed_at,
    }


def seal_normal_outputs(
    receipt_path: Path,
    audit_path: Path,
    receipt: dict[str, Any],
    audit: dict[str, Any],
) -> None:
    """Write audit once, hash read-back bytes, then write receipt once."""
    audit_raw = canonical_json(audit)
    write_once(audit_path, audit_raw)
    read_back = audit_path.read_bytes()
    digest = hashlib.sha256(read_back).hexdigest()
    receipt["write_events_reference"] = str(audit_path)
    receipt["write_events_sha256"] = digest
    write_once(receipt_path, canonical_json(receipt))


def seal_minimal_output_failure(
    receipt_path: Path,
    started_at: str,
    code: str,
    field_path: str,
) -> None:
    """Seal the exact minimal receipt when no request work has started."""
    finished_at = timestamp()
    value = {
        "schema_version": 1,
        "request_id": None,
        "provisioner_version": None,
        "started_at": started_at,
        "finished_at": finished_at,
        "overall_outcome": "output-failure",
        "exit_code": 7,
        "results": [],
        "diagnostics": [
            diagnostic(
                [cause(code, "outputs", field_path)],
                "stewards",
                "The provisioner output contract could not be established.",
            )
        ],
    }
    write_once(receipt_path, canonical_json(value))


def envelope_diagnostic(
    causes: list[dict[str, Any]],
    code: Optional[str] = None,
) -> dict[str, Any]:
    """Build one consumer-owned request envelope diagnostic."""
    if code is not None:
        causes = [{**item, "code": code} for item in causes]
    return diagnostic(
        causes,
        "consumer/environment",
        "The provision request is invalid.",
    )


def execute(
    root: Path,
    request_path: Path,
    receipt_text: str,
    audit_text: str,
) -> int:
    """Execute the bounded protocol through the available route boundary."""
    started = timestamp()
    try:
        receipt_path = validate_output_leaf(receipt_text, "receipt")
    except OutputContractError as exc:
        print(f"receipt-seal-failed: {exc}", file=sys.stderr)
        return 7
    try:
        audit_path = validate_output_leaf(audit_text, "audit")
        if receipt_path == audit_path:
            raise OutputContractError("receipt and audit paths must be distinct")
    except OutputContractError as exc:
        print(f"output-parent-invalid: {exc}", file=sys.stderr)
        try:
            seal_minimal_output_failure(
                receipt_path,
                started,
                "output-parent-invalid",
                "/audit/parent",
            )
        except OSError as write_error:
            print(f"receipt-seal-failed: {write_error}", file=sys.stderr)
        return 7

    document: Any = None
    positions: list[dict[str, Any]] = []
    request_id: Optional[str] = None
    provisioner_version: Optional[str] = None
    envelope_diagnostics: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    exit_code = 2
    overall = "invalid-request"
    try:
        document = load_json_bytes(request_path.read_bytes(), str(request_path))
        positions = tuple_positions(document)
        if isinstance(document, dict):
            if isinstance(document.get("request_id"), str):
                request_id = document["request_id"]
            if isinstance(document.get("provisioner_version"), str):
                provisioner_version = document["provisioner_version"]
        phase_one_envelope, assigned = phase_one(document, positions)
        if phase_one_envelope or assigned:
            if phase_one_envelope:
                envelope_diagnostics.append(
                    envelope_diagnostic(phase_one_envelope)
                )
            results = request_validation_results(positions, assigned)
        else:
            assert isinstance(document, dict)
            phase_two = phase_two_causes(document)
            state_roots = [
                Path(row["path"]) for row in document["environment"]["state_roots"]
            ]
            for output_path, label in (
                (receipt_path, "receipt"),
                (audit_path, "audit"),
            ):
                if any(is_within(output_path, state_root) for state_root in state_roots):
                    phase_two.append(
                        cause("unsafe-path", "outputs", f"/{label}/parent")
                    )
            if phase_two:
                envelope_diagnostics.append(envelope_diagnostic(phase_two))
                results = [skip_result(position) for position in positions]
            else:
                phase_three_assigned = phase_three(document, positions)
                if phase_three_assigned:
                    results = request_validation_results(
                        positions,
                        phase_three_assigned,
                    )
                else:
                    phase_four_envelope, phase_four_assigned = phase_four(
                        root,
                        document,
                        positions,
                    )
                    if phase_four_envelope or phase_four_assigned:
                        if phase_four_envelope:
                            envelope_diagnostics.append(
                                envelope_diagnostic(phase_four_envelope)
                            )
                        results = request_validation_results(
                            positions,
                            phase_four_assigned,
                        )
                    else:
                        route_results, resolved = resolve_routes(root, positions)
                        envelope_diagnostics = unused_reference_diagnostics(document)
                        if envelope_diagnostics:
                            resolved_ids = {
                                position["result_id"] for position in resolved
                            }
                            route_results = [
                                skip_result(position)
                                if position["result_id"] in resolved_ids
                                else result
                                for position, result in zip(
                                    positions,
                                    route_results,
                                )
                            ]
                            results = route_results
                        else:
                            results = route_results
                            exit_code = 3
                            overall = "failed"
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        envelope_diagnostics = [
            envelope_diagnostic(
                [cause("invalid-request", "request", "")],
            )
        ]
        positions = []
        results = []
        print(f"invalid-request: {exc}", file=sys.stderr)

    finished = timestamp()
    receipt = {
        "schema_version": 1,
        "request_id": request_id,
        "provisioner_version": provisioner_version,
        "started_at": started,
        "finished_at": finished,
        "overall_outcome": overall,
        "exit_code": exit_code,
        "results": sorted(
            results,
            key=lambda item: (item["target_index"], item["plugin_index"]),
        ),
        "diagnostics": envelope_diagnostics,
    }
    audit = build_audit(
        request_id,
        receipt_path,
        audit_path,
        document,
        finished,
    )
    try:
        seal_normal_outputs(receipt_path, audit_path, receipt, audit)
    except OSError as exc:
        print(f"audit-seal-failed: {exc}", file=sys.stderr)
        return 7
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    """Build the exact host-neutral command-line interface."""
    parser = argparse.ArgumentParser(prog="distribution/provision")
    parser.add_argument("--request", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--write-events", required=True)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Provisioner entrypoint."""
    args = build_parser().parse_args(argv)
    return execute(
        Path(__file__).resolve().parents[2],
        Path(args.request),
        args.receipt,
        args.write_events,
    )
