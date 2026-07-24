"""Deterministic validation and generation for the family distribution door.

This module implements kodhama-spec-0001-family-plugin-release-and-
distribution-metadata@v1.  It intentionally does not implement the spec 0002
provisioner request protocol or execute a provisioner.
"""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import sys
import threading
import time
from typing import Any, Callable, Iterable, Optional, Sequence
import unicodedata
from urllib.parse import urlsplit


SEMVER_TEXT = (
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
SEMVER = re.compile("^" + SEMVER_TEXT + "$")
PLUGIN_ID = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
DOT_ID = re.compile(
    r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:\.[a-z][a-z0-9]*(?:-[a-z0-9]+)*)*$"
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
TIMESTAMP = re.compile(
    r"^[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])"
    r"T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z$"
)
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
BASELINE_COMMIT = "8b9007dd4f4559cf2a83976391c71392a4628730"
BASELINE_ALGORITHM = "kodhama-selector-v1-sha256"
SURFACES = {
    "claude-code.local.interactive": ("claude-code", "local", "interactive"),
    "claude-code.ci.headless": ("claude-code", "ci", "headless"),
    "claude-code.cloud-container.headless": (
        "claude-code",
        "cloud-container",
        "headless",
    ),
    "codex.local.interactive": ("codex", "local", "interactive"),
    "codex.ci.headless": ("codex", "ci", "headless"),
    "codex.cloud-container.headless": ("codex", "cloud-container", "headless"),
}
FACTOR_ORDER = (
    "product_supported",
    "distribution_verified",
    "identity_match",
    "consumer_selected",
    "environment_ready",
    "product_setup_complete",
)
PROVIDER_TIMEOUT_SECONDS = 10
PROVIDER_OUTPUT_LIMIT = 1024 * 1024
PROVIDER_STDERR_LIMIT = 64 * 1024
PROVIDER_READER_JOIN_SECONDS = 1


class ContractError(ValueError):
    """A deterministic contract-validation failure."""


def reject(message: str) -> None:
    raise ContractError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        reject(message)


def exact_keys(
    value: Any,
    required: Iterable[str],
    optional: Iterable[str] = (),
    where: str = "object",
) -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected object")
    required_set = set(required)
    allowed = required_set | set(optional)
    missing = sorted(required_set - set(value))
    extra = sorted(set(value) - allowed)
    require(not missing, f"{where}: missing {', '.join(missing)}")
    require(not extra, f"{where}: unexpected {', '.join(extra)}")
    return value


def no_duplicates(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            reject(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_bytes(raw: bytes, where: str) -> Any:
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{where}: UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError(f"{where}: invalid UTF-8") from exc
    try:
        return json.loads(text, object_pairs_hook=no_duplicates)
    except (json.JSONDecodeError, ContractError) as exc:
        raise ContractError(f"{where}: invalid JSON: {exc}") from exc


def load_json(path: Path) -> Any:
    try:
        return load_json_bytes(path.read_bytes(), str(path))
    except OSError as exc:
        raise ContractError(f"{path}: {exc.strerror}") from exc


def canonical_json(value: Any, newline: bool = False) -> bytes:
    normalized = normalize_strings(value)
    body = json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return body + (b"\n" if newline else b"")


def normalize_strings(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [normalize_strings(item) for item in value]
    if isinstance(value, dict):
        return {
            unicodedata.normalize("NFC", key): normalize_strings(item)
            for key, item in value.items()
        }
    return value


def validate_slug(value: Any, where: str, dotted: bool = False) -> str:
    regex = DOT_ID if dotted else PLUGIN_ID
    require(isinstance(value, str) and regex.fullmatch(value) is not None, f"{where}: invalid id")
    return value


def validate_semver(value: Any, where: str) -> str:
    require(isinstance(value, str) and SEMVER.fullmatch(value) is not None, f"{where}: invalid SemVer")
    return value


def validate_timestamp(value: Any, where: str) -> str:
    require(
        isinstance(value, str) and TIMESTAMP.fullmatch(value) is not None,
        f"{where}: expected RFC 3339 UTC whole-second timestamp",
    )
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError as exc:
        raise ContractError(f"{where}: invalid calendar timestamp") from exc
    require(
        parsed.strftime("%Y-%m-%dT%H:%M:%SZ") == value,
        f"{where}: invalid calendar timestamp",
    )
    return value


def normalized_path(value: Any, where: str, allow_empty: bool = False) -> str:
    require(isinstance(value, str), f"{where}: expected path string")
    if value == "" and allow_empty:
        return value
    require(value != "", f"{where}: empty path")
    require("\\" not in value and not value.startswith("/"), f"{where}: path is not normalized relative POSIX")
    parts = value.split("/")
    require(all(part not in ("", ".", "..") for part in parts), f"{where}: path is not normalized")
    require(str(PurePosixPath(value)) == value, f"{where}: path is not normalized")
    return value


def validate_stable_reference(value: Any, where: str = "stable_reference") -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected object")
    kind = value.get("kind")
    if kind == "repo-path":
        obj = exact_keys(
            value,
            ("kind", "repository", "source_commit", "path", "sha256"),
            where=where,
        )
        validate_repository(obj["repository"], f"{where}.repository")
        require(isinstance(obj["source_commit"], str) and COMMIT.fullmatch(obj["source_commit"]), f"{where}.source_commit: invalid")
        normalized_path(obj["path"], f"{where}.path")
    elif kind == "https-url":
        obj = exact_keys(value, ("kind", "url", "sha256"), where=where)
        require(isinstance(obj["url"], str), f"{where}.url: expected string")
        parsed = urlsplit(obj["url"])
        require(
            parsed.scheme == "https"
            and bool(parsed.netloc)
            and parsed.username is None
            and parsed.password is None
            and parsed.fragment == "",
            f"{where}.url: expected absolute credential-free fragment-free https URL",
        )
    elif kind == "artifact":
        obj = exact_keys(value, ("kind", "uri", "sha256"), where=where)
        require(
            isinstance(obj["uri"], str) and bool(urlsplit(obj["uri"]).scheme),
            f"{where}.uri: expected absolute artifact URI",
        )
    else:
        reject(f"{where}.kind: unknown stable-reference kind")
    require(isinstance(value["sha256"], str) and SHA256.fullmatch(value["sha256"]), f"{where}.sha256: invalid")
    return value


def validate_repository(value: Any, where: str) -> str:
    require(
        isinstance(value, str)
        and REPOSITORY.fullmatch(value) is not None
        and value.count("/") == 1
        and not value.endswith(".git"),
        f"{where}: invalid repository",
    )
    return value


def validate_subject(value: Any, where: str = "subject") -> dict[str, str]:
    obj = exact_keys(
        value,
        ("plugin_id", "package_version", "release_tag", "source_commit", "surface_id"),
        where=where,
    )
    validate_slug(obj["plugin_id"], f"{where}.plugin_id")
    validate_semver(obj["package_version"], f"{where}.package_version")
    require(
        obj["release_tag"] == f"{obj['plugin_id']}-v{obj['package_version']}",
        f"{where}.release_tag: does not bind package version",
    )
    require(isinstance(obj["source_commit"], str) and COMMIT.fullmatch(obj["source_commit"]), f"{where}.source_commit: invalid")
    validate_slug(obj["surface_id"], f"{where}.surface_id", dotted=True)
    return obj


def validate_evidence_binding(value: Any, where: str) -> dict[str, Any]:
    obj = exact_keys(
        value,
        (
            "evidence_id",
            "stable_reference",
            "plugin_id",
            "package_version",
            "release_tag",
            "source_commit",
            "surface_id",
            "observed_at",
            "observation",
        ),
        where=where,
    )
    validate_slug(obj["evidence_id"], f"{where}.evidence_id", dotted=True)
    validate_stable_reference(obj["stable_reference"], f"{where}.stable_reference")
    validate_subject(
        {key: obj[key] for key in ("plugin_id", "package_version", "release_tag", "source_commit", "surface_id")},
        where,
    )
    validate_timestamp(obj["observed_at"], f"{where}.observed_at")
    require(isinstance(obj["observation"], str) and bool(obj["observation"]), f"{where}.observation: empty")
    return obj


def validate_load_path(value: Any, where: str) -> dict[str, Any]:
    obj = exact_keys(value, ("kind", "locator"), ("invocation",), where)
    require(obj["kind"] in {"command", "skill", "agent", "hook", "connector", "host-discovery"}, f"{where}.kind: invalid")
    require(isinstance(obj["locator"], str) and bool(obj["locator"]), f"{where}.locator: empty")
    if "invocation" in obj:
        require(isinstance(obj["invocation"], str) and bool(obj["invocation"]), f"{where}.invocation: empty")
        secret_terms = ("token=", "password=", "secret=", "authorization:")
        require(not any(term in obj["invocation"].lower() for term in secret_terms), f"{where}.invocation: apparent secret")
    return obj


def validate_support_record(value: Any, where: str) -> dict[str, Any]:
    obj = exact_keys(
        value,
        ("record_id", "stable_reference", "plugin_id", "package_version", "surface_id"),
        where=where,
    )
    validate_slug(obj["record_id"], f"{where}.record_id", dotted=True)
    validate_stable_reference(obj["stable_reference"], f"{where}.stable_reference")
    validate_slug(obj["plugin_id"], f"{where}.plugin_id")
    validate_semver(obj["package_version"], f"{where}.package_version")
    validate_slug(obj["surface_id"], f"{where}.surface_id", dotted=True)
    return obj


def validate_setup_declaration(value: Any, where: str) -> dict[str, Any]:
    obj = exact_keys(value, ("required", "contract"), where=where)
    require(type(obj["required"]) is bool, f"{where}.required: expected boolean")
    if obj["required"]:
        validate_stable_reference(obj["contract"], f"{where}.contract")
    else:
        require(obj["contract"] is None, f"{where}.contract: must be null when setup is not required")
    return obj


def validate_surface_row(value: Any, package_version: str, where: str) -> dict[str, Any]:
    common = {"surface_id", "host", "status", "post_install_setup"}
    require(isinstance(value, dict), f"{where}: expected object")
    status = value.get("status")
    if status == "supported":
        exact_keys(value, common | {"evidence", "load_path", "support_record"}, where=where)
    elif status in {"candidate", "unsupported"}:
        exact_keys(
            value,
            common | {"missing_capability", "disclosure"},
            {"evidence", "load_path", "support_record"},
            where,
        )
    else:
        reject(f"{where}.status: invalid")
    surface_id = validate_slug(value["surface_id"], f"{where}.surface_id", dotted=True)
    require(surface_id in SURFACES, f"{where}.surface_id: unknown surface")
    require(value["host"] == SURFACES[surface_id][0], f"{where}.host: does not match surface")
    validate_setup_declaration(value["post_install_setup"], f"{where}.post_install_setup")
    if "evidence" in value:
        require(isinstance(value["evidence"], list) and bool(value["evidence"]), f"{where}.evidence: expected non-empty array")
        ids = set()
        for index, item in enumerate(value["evidence"]):
            evidence = validate_evidence_binding(item, f"{where}.evidence[{index}]")
            require(evidence["package_version"] == package_version, f"{where}.evidence[{index}]: version mismatch")
            require(evidence["surface_id"] == surface_id, f"{where}.evidence[{index}]: surface mismatch")
            require(evidence["evidence_id"] not in ids, f"{where}.evidence: duplicate evidence_id")
            ids.add(evidence["evidence_id"])
    if "load_path" in value:
        validate_load_path(value["load_path"], f"{where}.load_path")
    if "support_record" in value:
        record = validate_support_record(value["support_record"], f"{where}.support_record")
        require(record["package_version"] == package_version and record["surface_id"] == surface_id, f"{where}.support_record: identity mismatch")
    if status != "supported":
        require(isinstance(value["missing_capability"], str) and bool(value["missing_capability"]), f"{where}.missing_capability: empty")
        require(isinstance(value["disclosure"], str) and bool(value["disclosure"]), f"{where}.disclosure: empty")
    return value


def validate_surface_contract(value: Any) -> dict[str, Any]:
    obj = exact_keys(
        value,
        ("schema_version", "family_contract_version", "version", "surfaces"),
        ("extensions",),
        "surface_contract",
    )
    require(obj["schema_version"] == 1, "surface_contract.schema_version: expected 1")
    require(obj["family_contract_version"] == 1, "surface_contract.family_contract_version: expected 1")
    version = validate_semver(obj["version"], "surface_contract.version")
    require(isinstance(obj["surfaces"], list), "surface_contract.surfaces: expected array")
    seen = set()
    for index, row in enumerate(obj["surfaces"]):
        validate_surface_row(row, version, f"surface_contract.surfaces[{index}]")
        require(row["surface_id"] not in seen, "surface_contract.surfaces: duplicate surface_id")
        seen.add(row["surface_id"])
    if "extensions" in obj:
        require(isinstance(obj["extensions"], dict), "surface_contract.extensions: expected object")
        for key in obj["extensions"]:
            validate_slug(key, f"surface_contract.extensions.{key}")
    return obj


def validate_source_selector(value: Any, where: str = "source_selector") -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected object")
    kind = value.get("kind")
    if kind == "mutable":
        obj = exact_keys(value, ("kind", "repository", "path"), where=where)
    elif kind == "immutable":
        obj = exact_keys(value, ("kind", "repository", "path", "ref"), where=where)
        ref = exact_keys(obj["ref"], ("kind", "value"), where=f"{where}.ref")
        require(ref["kind"] in {"tag", "commit"}, f"{where}.ref.kind: invalid")
        if ref["kind"] == "tag":
            require(isinstance(ref["value"], str) and bool(ref["value"]), f"{where}.ref.value: invalid")
        else:
            require(isinstance(ref["value"], str) and COMMIT.fullmatch(ref["value"]), f"{where}.ref.value: invalid commit")
    else:
        reject(f"{where}.kind: invalid")
    validate_repository(obj["repository"], f"{where}.repository")
    normalized_path(obj["path"], f"{where}.path", allow_empty=True)
    return obj


def validate_publication_evidence(value: Any, manifest_path: str, where: str) -> dict[str, Any]:
    obj = exact_keys(
        value,
        ("stable_reference", "manifest_path", "manifest_sha256", "observed_at"),
        where=where,
    )
    validate_stable_reference(obj["stable_reference"], f"{where}.stable_reference")
    require(obj["manifest_path"] == manifest_path, f"{where}.manifest_path: mismatch")
    require(isinstance(obj["manifest_sha256"], str) and SHA256.fullmatch(obj["manifest_sha256"]), f"{where}.manifest_sha256: invalid")
    stable = obj["stable_reference"]
    require(
        stable["kind"] == "repo-path"
        and stable["path"] == manifest_path
        and stable["sha256"] == obj["manifest_sha256"],
        f"{where}.stable_reference: must bind the generated manifest path and digest",
    )
    validate_timestamp(obj["observed_at"], f"{where}.observed_at")
    return obj


def validate_host_projection(value: Any, expected_host: str, where: str) -> dict[str, Any]:
    obj = exact_keys(value, ("host", "entry_name", "fields"), where=where)
    require(obj["host"] == expected_host, f"{where}.host: mismatch")
    validate_slug(obj["entry_name"], f"{where}.entry_name")
    if expected_host == "claude-code":
        fields = exact_keys(obj["fields"], ("source", "description"), where=f"{where}.fields")
        require(isinstance(fields["description"], str) and bool(fields["description"]), f"{where}.fields.description: empty")
    elif expected_host == "codex":
        fields = exact_keys(obj["fields"], ("source", "policy", "category"), where=f"{where}.fields")
        require(isinstance(fields["category"], str) and bool(fields["category"]), f"{where}.fields.category: empty")
        policy = exact_keys(fields["policy"], ("installation", "authentication"), where=f"{where}.fields.policy")
        require(
            policy["installation"] in {"AVAILABLE", "REQUIRED", "BLOCKED"}
            and policy["authentication"] in {"ON_INSTALL", "ON_USE", "NONE"},
            f"{where}.fields.policy: invalid",
        )
    else:
        reject(f"{where}.host: unsupported host adapter")
    source = exact_keys(fields["source"], ("source", "url", "path"), where=f"{where}.fields.source")
    require(source["source"] == "git-subdir", f"{where}.fields.source.source: expected git-subdir")
    validate_repository(source["url"], f"{where}.fields.source.url")
    normalized_path(source["path"], f"{where}.fields.source.path")
    return obj


def manifest_for_surface(surface_id: str) -> str:
    host = SURFACES.get(surface_id, ("", "", ""))[0]
    if host == "claude-code":
        return ".claude-plugin/marketplace.json"
    if host == "codex":
        return ".agents/plugins/marketplace.json"
    reject(f"surface_id: unknown host for {surface_id}")
    return ""


def validate_transition_exception(value: Any, where: str) -> dict[str, Any]:
    obj = exact_keys(
        value,
        (
            "baseline_key",
            "selector_fingerprint",
            "missing_contract_elements",
            "disclosure",
            "terminal_action",
        ),
        where=where,
    )
    exact_keys(obj["baseline_key"], ("plugin_id", "surface_id"), where=f"{where}.baseline_key")
    require(isinstance(obj["selector_fingerprint"], str) and SHA256.fullmatch(obj["selector_fingerprint"]), f"{where}.selector_fingerprint: invalid")
    elements = obj["missing_contract_elements"]
    require(
        isinstance(elements, list)
        and bool(elements)
        and all(isinstance(item, str) and bool(item) for item in elements),
        f"{where}.missing_contract_elements: must contain non-empty strings",
    )
    require(
        elements == sorted(set(elements)),
        f"{where}.missing_contract_elements: must be sorted and unique",
    )
    require(obj["disclosure"] == "legacy published stock", f"{where}.disclosure: invalid")
    require(obj["terminal_action"] == "adopt-or-delist", f"{where}.terminal_action: invalid")
    return obj


def validate_catalog_row(value: Any, where: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected object")
    state = value.get("state")
    base = {"plugin_id", "surface_id", "state"}
    if state == "absent":
        exact_keys(value, base | {"reason"}, where=where)
        require(isinstance(value["reason"], str) and bool(value["reason"]), f"{where}.reason: empty")
    elif state in {"published", "verified"}:
        shared = base | {
            "manifest_path",
            "source_selector",
            "publication_evidence",
            "host_projection",
        }
        conforming = {
            "release_metadata_path",
            "surface_contract_path",
            "product_contract_version",
        }
        verified = {
            "package_version",
            "release_tag",
            "source_commit",
            "identity_binding",
            "clean_install_evidence",
            "release_history_reference",
        }
        if "transition_exception" in value:
            require(state == "published", f"{where}.transition_exception: only published")
            exact_keys(value, shared | {"transition_exception"}, where=where)
            validate_transition_exception(value["transition_exception"], f"{where}.transition_exception")
        else:
            exact_keys(value, shared | conforming | (verified if state == "verified" else set()), where=where)
            normalized_path(value["release_metadata_path"], f"{where}.release_metadata_path")
            normalized_path(value["surface_contract_path"], f"{where}.surface_contract_path")
            require(value["product_contract_version"] == 1, f"{where}.product_contract_version: expected 1")
        selector = validate_source_selector(value["source_selector"], f"{where}.source_selector")
        expected_manifest = manifest_for_surface(value["surface_id"])
        require(value["manifest_path"] == expected_manifest, f"{where}.manifest_path: host mismatch")
        validate_publication_evidence(value["publication_evidence"], expected_manifest, f"{where}.publication_evidence")
        projection = validate_host_projection(value["host_projection"], SURFACES[value["surface_id"]][0], f"{where}.host_projection")
        require(projection["entry_name"] == value["plugin_id"], f"{where}.host_projection.entry_name: plugin mismatch")
        require(
            projection["fields"]["source"]["url"] == selector["repository"]
            and projection["fields"]["source"]["path"] == selector["path"],
            f"{where}.host_projection.fields.source: selector mismatch",
        )
        if state == "verified":
            require(selector["kind"] == "immutable", f"{where}.source_selector: verified requires immutable")
            version = validate_semver(value["package_version"], f"{where}.package_version")
            expected_tag = f"{value['plugin_id']}-v{version}"
            require(value["release_tag"] == expected_tag, f"{where}.release_tag: mismatch")
            require(isinstance(value["source_commit"], str) and COMMIT.fullmatch(value["source_commit"]), f"{where}.source_commit: invalid")
            ref = selector["ref"]
            expected = value["release_tag"] if ref["kind"] == "tag" else value["source_commit"]
            require(ref["value"] == expected, f"{where}.source_selector: immutable ref does not bind subject")
            validate_stable_reference(value["release_history_reference"], f"{where}.release_history_reference")
            binding = validate_distribution_binding(value["identity_binding"], f"{where}.identity_binding")
            clean = validate_clean_install_evidence(value["clean_install_evidence"])
            row_subject = {
                key: value[key]
                for key in (
                    "plugin_id",
                    "package_version",
                    "release_tag",
                    "source_commit",
                    "surface_id",
                )
            }
            require(
                clean["subject"] == row_subject,
                f"{where}.clean_install_evidence.subject: catalog identity mismatch",
            )
            require(
                clean["catalog_key"]
                == {
                    "plugin_id": value["plugin_id"],
                    "surface_id": value["surface_id"],
                },
                f"{where}.clean_install_evidence.catalog_key: catalog identity mismatch",
            )
            require(
                binding == clean["distribution_binding"],
                f"{where}.identity_binding: clean-install binding mismatch",
            )
            if binding["kind"] == "catalog-selector":
                require(
                    binding["selector"] == selector,
                    f"{where}.identity_binding.selector: catalog selector mismatch",
                )
    else:
        reject(f"{where}.state: invalid")
    validate_slug(value["plugin_id"], f"{where}.plugin_id")
    surface = validate_slug(value["surface_id"], f"{where}.surface_id", dotted=True)
    require(surface in SURFACES, f"{where}.surface_id: unknown")
    return value


def validate_catalog(value: Any) -> dict[str, Any]:
    obj = exact_keys(value, ("schema_version", "records"), where="catalog_availability")
    require(obj["schema_version"] == 1, "catalog_availability.schema_version: expected 1")
    require(isinstance(obj["records"], list), "catalog_availability.records: expected array")
    keys = set()
    projections = set()
    prior = None
    for index, row in enumerate(obj["records"]):
        validate_catalog_row(row, f"catalog_availability.records[{index}]")
        key = (row["plugin_id"], row["surface_id"])
        require(key not in keys, "catalog_availability.records: duplicate key")
        require(prior is None or prior < key, "catalog_availability.records: records are not in key order")
        keys.add(key)
        prior = key
        if row["state"] != "absent":
            projection = (
                row["host_projection"]["host"],
                row["host_projection"]["entry_name"],
            )
            require(
                projection not in projections,
                "catalog_availability.records: duplicate per-host plugin projection",
            )
            projections.add(projection)
    return obj


def validate_distribution_binding(value: Any, where: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected object")
    if value.get("kind") == "catalog-selector":
        obj = exact_keys(value, ("kind", "selector"), where=where)
        selector = validate_source_selector(obj["selector"], f"{where}.selector")
        require(selector["kind"] == "immutable", f"{where}.selector: must be immutable")
    elif value.get("kind") == "provisioner-acquisition":
        obj = exact_keys(value, ("kind", "provisioner_identity", "evidence_bundle"), where=where)
        identity = exact_keys(
            obj["provisioner_identity"],
            (
                "route_id",
                "surface_id",
                "plugin_id",
                "package_version",
                "provisioner_version",
                "release_tag",
                "source_commit",
            ),
            where=f"{where}.provisioner_identity",
        )
        validate_slug(identity["route_id"], f"{where}.provisioner_identity.route_id", dotted=True)
        validate_subject(
            {key: identity[key] for key in ("plugin_id", "package_version", "release_tag", "source_commit", "surface_id")},
            f"{where}.provisioner_identity",
        )
        validate_semver(identity["provisioner_version"], f"{where}.provisioner_identity.provisioner_version")
        validate_stable_reference(obj["evidence_bundle"], f"{where}.evidence_bundle")
    else:
        reject(f"{where}.kind: invalid")
    return value


def validate_clean_install_evidence(value: Any) -> dict[str, Any]:
    obj = exact_keys(
        value,
        (
            "schema_version",
            "evidence_id",
            "subject",
            "catalog_key",
            "distribution_binding",
            "clean_environment",
            "installation",
            "observations",
        ),
        where="clean_install_evidence",
    )
    require(obj["schema_version"] == 1, "clean_install_evidence.schema_version: expected 1")
    validate_slug(obj["evidence_id"], "clean_install_evidence.evidence_id", dotted=True)
    subject = validate_subject(obj["subject"], "clean_install_evidence.subject")
    key = exact_keys(obj["catalog_key"], ("plugin_id", "surface_id"), where="clean_install_evidence.catalog_key")
    require(key["plugin_id"] == subject["plugin_id"] and key["surface_id"] == subject["surface_id"], "clean_install_evidence.catalog_key: identity mismatch")
    binding = validate_distribution_binding(
        obj["distribution_binding"],
        "clean_install_evidence.distribution_binding",
    )
    if binding["kind"] == "catalog-selector":
        ref = binding["selector"]["ref"]
        expected_ref = (
            subject["release_tag"]
            if ref["kind"] == "tag"
            else subject["source_commit"]
        )
        require(
            ref["value"] == expected_ref,
            "clean_install_evidence.distribution_binding: subject release mismatch",
        )
    else:
        identity = binding["provisioner_identity"]
        require(
            all(identity[key] == subject[key] for key in subject),
            "clean_install_evidence.distribution_binding: subject identity mismatch",
        )
    environment = exact_keys(
        obj["clean_environment"],
        ("host", "host_version", "environment", "mode", "snapshot_kind", "snapshot_id", "sha256"),
        where="clean_install_evidence.clean_environment",
    )
    surface = SURFACES.get(subject["surface_id"])
    require(surface is not None, "clean_install_evidence.subject.surface_id: unknown")
    require(
        environment["host"] == surface[0]
        and environment["environment"] == surface[1]
        and environment["mode"] == surface[2],
        "clean_install_evidence.clean_environment: surface mismatch",
    )
    require(environment["snapshot_kind"] in {"machine-snapshot", "ci-image", "container-image"}, "clean_install_evidence.clean_environment.snapshot_kind: invalid")
    require(isinstance(environment["snapshot_id"], str) and bool(environment["snapshot_id"]), "clean_install_evidence.clean_environment.snapshot_id: empty")
    require(isinstance(environment["sha256"], str) and SHA256.fullmatch(environment["sha256"]), "clean_install_evidence.clean_environment.sha256: invalid")
    installation = exact_keys(
        obj["installation"],
        ("started_at", "finished_at", "outcome", "discovered_identity", "record_reference"),
        where="clean_install_evidence.installation",
    )
    validate_timestamp(installation["started_at"], "clean_install_evidence.installation.started_at")
    validate_timestamp(installation["finished_at"], "clean_install_evidence.installation.finished_at")
    started_at = datetime.strptime(
        installation["started_at"],
        "%Y-%m-%dT%H:%M:%SZ",
    )
    finished_at = datetime.strptime(
        installation["finished_at"],
        "%Y-%m-%dT%H:%M:%SZ",
    )
    require(
        finished_at >= started_at,
        "clean_install_evidence.installation.finished_at: precedes started_at",
    )
    require(installation["outcome"] == "installed", "clean_install_evidence.installation.outcome: expected installed")
    require(validate_subject(installation["discovered_identity"]) == subject, "clean_install_evidence.installation.discovered_identity: mismatch")
    validate_stable_reference(installation["record_reference"], "clean_install_evidence.installation.record_reference")
    require(isinstance(obj["observations"], list) and bool(obj["observations"]), "clean_install_evidence.observations: expected non-empty array")
    for index, item in enumerate(obj["observations"]):
        binding = validate_evidence_binding(item, f"clean_install_evidence.observations[{index}]")
        require(all(binding[key] == subject[key] for key in subject), f"clean_install_evidence.observations[{index}]: identity mismatch")
    return obj


def validate_prerequisite(value: Any, where: str) -> dict[str, Any]:
    obj = exact_keys(
        value,
        ("prerequisite_id", "request_reference_id", "kind", "description"),
        where=where,
    )
    validate_slug(obj["prerequisite_id"], f"{where}.prerequisite_id", dotted=True)
    validate_slug(obj["request_reference_id"], f"{where}.request_reference_id", dotted=True)
    require(obj["kind"] in {"authentication", "trust", "runtime", "configuration", "writable-state"}, f"{where}.kind: invalid")
    require(isinstance(obj["description"], str) and bool(obj["description"]), f"{where}.description: empty")
    return obj


def validate_provisioner_row(value: Any, where: str) -> dict[str, Any]:
    base = {"route_id", "surface_id", "plugin_id", "package_version", "state"}
    require(isinstance(value, dict), f"{where}: expected object")
    state = value.get("state")
    if state == "unavailable":
        exact_keys(value, base | {"reason"}, where=where)
        require(isinstance(value["reason"], str) and bool(value["reason"]), f"{where}.reason: empty")
    elif state == "candidate":
        exact_keys(
            value,
            base | {"provisioner_version", "adapter_path", "prerequisites", "missing_proof", "disclosure"},
            where=where,
        )
    elif state == "verified":
        exact_keys(
            value,
            base
            | {
                "provisioner_version",
                "adapter_path",
                "prerequisites",
                "release_tag",
                "source_commit",
                "evidence_bundle",
            },
            where=where,
        )
    else:
        reject(f"{where}.state: invalid")
    validate_slug(value["route_id"], f"{where}.route_id", dotted=True)
    validate_slug(value["surface_id"], f"{where}.surface_id", dotted=True)
    require(value["surface_id"] in SURFACES, f"{where}.surface_id: unknown")
    validate_slug(value["plugin_id"], f"{where}.plugin_id")
    validate_semver(value["package_version"], f"{where}.package_version")
    if state != "unavailable":
        validate_semver(value["provisioner_version"], f"{where}.provisioner_version")
        normalized_path(value["adapter_path"], f"{where}.adapter_path")
        require(isinstance(value["prerequisites"], list), f"{where}.prerequisites: expected array")
        ids = set()
        refs = set()
        for index, item in enumerate(value["prerequisites"]):
            prerequisite = validate_prerequisite(item, f"{where}.prerequisites[{index}]")
            require(prerequisite["prerequisite_id"] not in ids, f"{where}.prerequisites: duplicate prerequisite_id")
            require(prerequisite["request_reference_id"] not in refs, f"{where}.prerequisites: duplicate request_reference_id")
            ids.add(prerequisite["prerequisite_id"])
            refs.add(prerequisite["request_reference_id"])
    if state == "candidate":
        require(isinstance(value["missing_proof"], str) and bool(value["missing_proof"]), f"{where}.missing_proof: empty")
        require(isinstance(value["disclosure"], str) and bool(value["disclosure"]), f"{where}.disclosure: empty")
    if state == "verified":
        require(value["release_tag"] == f"{value['plugin_id']}-v{value['package_version']}", f"{where}.release_tag: mismatch")
        require(isinstance(value["source_commit"], str) and COMMIT.fullmatch(value["source_commit"]), f"{where}.source_commit: invalid")
        validate_stable_reference(value["evidence_bundle"], f"{where}.evidence_bundle")
    return value


def validate_provisioners(value: Any) -> dict[str, Any]:
    obj = exact_keys(value, ("schema_version", "records"), where="provisioner_availability")
    require(obj["schema_version"] == 1, "provisioner_availability.schema_version: expected 1")
    require(isinstance(obj["records"], list), "provisioner_availability.records: expected array")
    keys = set()
    prior = None
    for index, row in enumerate(obj["records"]):
        validate_provisioner_row(row, f"provisioner_availability.records[{index}]")
        key = (row["route_id"], row["surface_id"], row["plugin_id"], row["package_version"])
        require(key not in keys, "provisioner_availability.records: duplicate key")
        require(prior is None or prior < key, "provisioner_availability.records: records are not in key order")
        keys.add(key)
        prior = key
    return obj


def validate_surface_registry(value: Any) -> dict[str, Any]:
    obj = exact_keys(value, ("schema_version", "registry_version", "surfaces"), where="surface_registry")
    require(obj["schema_version"] == 1 and type(obj["registry_version"]) is int and obj["registry_version"] > 0, "surface_registry: invalid version")
    require(isinstance(obj["surfaces"], list), "surface_registry.surfaces: expected array")
    ids = set()
    for index, row in enumerate(obj["surfaces"]):
        where = f"surface_registry.surfaces[{index}]"
        exact_keys(row, ("surface_id", "host", "environment", "mode", "label", "lifecycle"), ("retirement",), where)
        surface_id = validate_slug(row["surface_id"], f"{where}.surface_id", dotted=True)
        require(surface_id not in ids, "surface_registry.surfaces: duplicate surface_id")
        ids.add(surface_id)
        require(row["lifecycle"] in {"active", "retired"}, f"{where}.lifecycle: invalid")
        require(isinstance(row["label"], str) and bool(row["label"]), f"{where}.label: empty")
        if row["lifecycle"] == "active":
            require("retirement" not in row, f"{where}.retirement: forbidden for active")
        else:
            retirement = exact_keys(row.get("retirement"), ("retired_at", "decision_ref", "replaced_by"), where=f"{where}.retirement")
            validate_timestamp(retirement["retired_at"], f"{where}.retirement.retired_at")
            validate_slug(retirement["decision_ref"], f"{where}.retirement.decision_ref", dotted=True)
            validate_slug(retirement["replaced_by"], f"{where}.retirement.replaced_by", dotted=True)
            require(retirement["replaced_by"] != surface_id, f"{where}.retirement.replaced_by: same id")
    return obj


def json_pointer(document: Any, pointer: str, where: str) -> Any:
    require(isinstance(pointer, str) and (pointer == "" or pointer.startswith("/")), f"{where}: invalid JSON Pointer")
    current = document
    if pointer == "":
        return current
    for raw in pointer[1:].split("/"):
        require(re.search(r"~(?:[^01]|$)", raw) is None, f"{where}: invalid JSON Pointer escape")
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            require(token in current, f"{where}: missing JSON Pointer token {token}")
            current = current[token]
        elif isinstance(current, list):
            require(token.isdigit() and (token == "0" or not token.startswith("0")), f"{where}: invalid array index")
            index = int(token)
            require(index < len(current), f"{where}: array index out of range")
            current = current[index]
        else:
            reject(f"{where}: pointer traverses scalar")
    return current


def validate_extractor(value: Any, where: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected object")
    if value.get("format") == "plain-text":
        obj = exact_keys(value, ("path", "format"), where=where)
    elif value.get("format") == "json":
        obj = exact_keys(value, ("path", "format", "selector"), where=where)
        require(isinstance(obj["selector"], str), f"{where}.selector: expected JSON Pointer")
        json_pointer({}, obj["selector"], f"{where}.selector") if obj["selector"] == "" else None
        require(obj["selector"].startswith("/"), f"{where}.selector: expected RFC 6901 JSON Pointer")
    else:
        reject(f"{where}.format: invalid")
    normalized_path(obj["path"], f"{where}.path")
    return obj


def extract_version(root: Path, extractor: dict[str, Any], where: str) -> str:
    validate_extractor(extractor, where)
    path = root / extractor["path"]
    require(path.is_file() and not path.is_symlink(), f"{where}.path: missing or unsafe path {extractor['path']}")
    raw = path.read_bytes()
    if extractor["format"] == "plain-text":
        require(not raw.startswith(b"\xef\xbb\xbf"), f"{extractor['path']}: UTF-8 BOM is forbidden")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ContractError(f"{extractor['path']}: invalid UTF-8") from exc
        if text.endswith("\n"):
            text = text[:-1]
        require("\n" not in text and "\r" not in text and text == text.strip(), f"{extractor['path']}: ambiguous version bytes")
        return validate_semver(text, extractor["path"])
    document = load_json_bytes(raw, extractor["path"])
    selected = json_pointer(document, extractor["selector"], f"{extractor['path']}#{extractor['selector']}")
    require(isinstance(selected, str), f"{extractor['path']}: selected version is not a string")
    return validate_semver(selected, extractor["path"])


def validate_release_metadata(value: Any, phase: str) -> dict[str, Any]:
    required = {
        "schema_version",
        "family_contract_version",
        "plugin_id",
        "version_authority",
        "version_carriers",
        "surface_contract",
        "release_inventory",
        "release_history",
        "inventory_provider",
    }
    if phase == "release":
        required.add("release_approval")
    obj = exact_keys(value, required, {"release_approval", "payload_identity", "extensions"}, "release_metadata")
    require(obj["schema_version"] == 1 and obj["family_contract_version"] == 1, "release_metadata: expected schema/family version 1")
    validate_slug(obj["plugin_id"], "release_metadata.plugin_id")
    validate_extractor(obj["version_authority"], "release_metadata.version_authority")
    require(isinstance(obj["version_carriers"], list) and bool(obj["version_carriers"]), "release_metadata.version_carriers: expected non-empty array")
    carrier_ids = set()
    extractor_pairs = set()
    paths = set()
    for index, carrier in enumerate(obj["version_carriers"]):
        where = f"release_metadata.version_carriers[{index}]"
        exact_keys(carrier, ("carrier_id", "role", "path", "format"), ("selector",), where)
        validate_slug(carrier["carrier_id"], f"{where}.carrier_id", dotted=True)
        require(carrier["role"] in {"host-manifest", "package-manifest", "other"}, f"{where}.role: invalid")
        extractor = {key: carrier[key] for key in ("path", "format", "selector") if key in carrier}
        validate_extractor(extractor, where)
        pair = (carrier["path"], carrier.get("selector"))
        require(carrier["carrier_id"] not in carrier_ids, "release_metadata.version_carriers: duplicate carrier_id")
        require(carrier["path"] not in paths and pair not in extractor_pairs, "release_metadata.version_carriers: duplicate extractor")
        carrier_ids.add(carrier["carrier_id"])
        paths.add(carrier["path"])
        extractor_pairs.add(pair)
    for key in ("surface_contract", "release_inventory", "release_history", "inventory_provider"):
        normalized_path(obj[key], f"release_metadata.{key}")
    if "release_approval" in obj:
        validate_stable_reference(obj["release_approval"], "release_metadata.release_approval")
    if "payload_identity" in obj:
        payload = exact_keys(obj["payload_identity"], ("kind", "value"), where="release_metadata.payload_identity")
        require(isinstance(payload["kind"], str) and isinstance(payload["value"], str), "release_metadata.payload_identity: invalid")
        require(not SEMVER.fullmatch(payload["value"]), "release_metadata.payload_identity: package version substitution")
    if "extensions" in obj:
        require(isinstance(obj["extensions"], dict), "release_metadata.extensions: expected object")
        for key, extension in obj["extensions"].items():
            validate_slug(key, f"release_metadata.extensions.{key}")
            require(isinstance(extension, dict), f"release_metadata.extensions.{key}: expected object")
            if "validator" in extension:
                normalized_path(extension["validator"], f"release_metadata.extensions.{key}.validator")
    return obj


def tree_snapshot(root: Path) -> dict[str, str]:
    snapshot = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            snapshot[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def run_bounded_process(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.Popen(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    streams = {
        "stdout": (process.stdout, PROVIDER_OUTPUT_LIMIT),
        "stderr": (process.stderr, PROVIDER_STDERR_LIMIT),
    }
    output: dict[str, bytes] = {}
    reader_errors: list[Exception] = []

    def kill_process_group() -> None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    def close_streams() -> None:
        for stream, _ in streams.values():
            try:
                stream.close()
            except OSError as exc:
                reader_errors.append(exc)

    def read_stream(name: str, stream: Any, limit: int) -> None:
        try:
            output[name] = stream.read(limit + 1)
            if len(output[name]) > limit:
                kill_process_group()
        except (OSError, ValueError) as exc:
            reader_errors.append(exc)

    def join_readers() -> bool:
        deadline = time.monotonic() + PROVIDER_READER_JOIN_SECONDS
        for reader in readers:
            reader.join(max(0.0, deadline - time.monotonic()))
        return all(not reader.is_alive() for reader in readers)

    readers = [
        threading.Thread(
            target=read_stream,
            args=(name, stream, limit),
            daemon=True,
        )
        for name, (stream, limit) in streams.items()
    ]
    for reader in readers:
        reader.start()
    try:
        returncode = process.wait(timeout=PROVIDER_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as exc:
        kill_process_group()
        process.wait()
        joined = join_readers()
        close_streams()
        require(joined, "inventory_provider: pipe readers did not terminate")
        raise ContractError(
            f"inventory_provider: timed out after {PROVIDER_TIMEOUT_SECONDS}s"
        ) from exc
    joined = join_readers()
    held_pipes_open = not joined
    if not joined:
        kill_process_group()
        joined = join_readers()
    if not joined:
        close_streams()
        join_readers()
        reject("inventory_provider: pipe readers did not terminate")
    close_streams()
    require(
        not held_pipes_open,
        "inventory_provider: child process held output pipe open",
    )
    require(not reader_errors, "inventory_provider: failed while reading output pipes")
    stdout = output.get("stdout", b"")
    stderr = output.get("stderr", b"")
    require(
        len(stdout) <= PROVIDER_OUTPUT_LIMIT,
        f"inventory_provider: stdout exceeds {PROVIDER_OUTPUT_LIMIT} bytes",
    )
    require(
        len(stderr) <= PROVIDER_STDERR_LIMIT,
        f"inventory_provider: stderr exceeds {PROVIDER_STDERR_LIMIT} bytes",
    )
    return subprocess.CompletedProcess(command, returncode, stdout, stderr)


def run_inventory_provider(root: Path, provider_path: str) -> bytes:
    provider = root / provider_path
    require(provider.is_file() and os.access(provider, os.X_OK), "release_metadata.inventory_provider: not executable")
    command = [str(provider), "--package-root", str(root), "--emit-release-inventory"]
    safe_env = {
        "PATH": os.environ.get("PATH", ""),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_PROXY": "*",
        "http_proxy": "",
        "https_proxy": "",
        "HTTP_PROXY": "",
        "HTTPS_PROXY": "",
    }
    before = tree_snapshot(root)
    outputs = []
    for _ in range(2):
        result = run_bounded_process(command, cwd=root, env=safe_env)
        require(result.returncode == 0, f"inventory_provider: exited {result.returncode}")
        lowered = result.stderr.lower()
        require(not any(term in lowered for term in (b"token", b"password", b"secret", b"credential", b"authorization")), "inventory_provider: stderr contains credential term")
        require(result.stderr == b"", "inventory_provider: stderr is not empty")
        outputs.append(result.stdout)
        require(tree_snapshot(root) == before, "inventory_provider: mutated package filesystem")
    require(outputs[0] == outputs[1], "inventory_provider: nondeterministic stdout")
    return outputs[0]


def validate_inventory_extractor(value: Any, where: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected object")
    kind = value.get("kind")
    if kind == "file-bytes":
        obj = exact_keys(value, ("kind", "path"), where=where)
    elif kind == "text-line":
        obj = exact_keys(value, ("kind", "path", "line"), where=where)
        require(
            type(obj["line"]) is int and obj["line"] >= 0,
            f"{where}.line: expected non-negative integer",
        )
    elif kind == "json-pointer":
        obj = exact_keys(value, ("kind", "path", "pointer"), where=where)
        pointer = obj["pointer"]
        require(
            isinstance(pointer, str)
            and (pointer == "" or pointer.startswith("/"))
            and re.search(r"~(?:[^01]|$)", pointer) is None,
            f"{where}.pointer: invalid RFC 6901 JSON Pointer",
        )
    else:
        reject(f"{where}.kind: invalid inventory extractor")
    normalized_path(obj["path"], f"{where}.path")
    return obj


def validate_release_inventory(value: Any, package_version: Optional[str] = None) -> dict[str, Any]:
    obj = exact_keys(
        value,
        ("schema_version", "host_manifests", "payload_identities", "public_contract_items", "support_derivatives"),
        where="release_inventory",
    )
    require(obj["schema_version"] == 1, "release_inventory.schema_version: expected 1")
    for key in ("host_manifests", "payload_identities", "public_contract_items", "support_derivatives"):
        require(isinstance(obj[key], list), f"release_inventory.{key}: expected array")
    hosts = set()
    prior_host = None
    for index, row in enumerate(obj["host_manifests"]):
        where = f"release_inventory.host_manifests[{index}]"
        exact_keys(row, ("host", "path", "manifest_kind", "version_extractor", "package_version"), ("extension_validator",), where)
        normalized_path(row["path"], f"{where}.path")
        require(
            isinstance(row["manifest_kind"], str)
            and row["manifest_kind"]
            in {
                "claude-plugin",
                "codex-plugin",
                "npm-package",
                "other-declared-host",
            },
            f"{where}.manifest_kind: invalid",
        )
        if row["manifest_kind"] == "other-declared-host":
            normalized_path(row.get("extension_validator"), f"{where}.extension_validator")
        else:
            require(
                "extension_validator" not in row,
                f"{where}.extension_validator: forbidden for standard manifest kind",
            )
        validate_extractor(row["version_extractor"], f"{where}.version_extractor")
        require(
            row["version_extractor"]["path"] == row["path"],
            f"{where}.version_extractor.path: manifest path mismatch",
        )
        validate_semver(row["package_version"], f"{where}.package_version")
        if package_version is not None:
            require(row["package_version"] == package_version, f"{where}.package_version: carrier mismatch")
        key = (row["host"], row["path"])
        require(key not in hosts, "release_inventory.host_manifests: duplicate row")
        require(
            prior_host is None or prior_host < key,
            "release_inventory.host_manifests: rows are not in identity order",
        )
        hosts.add(key)
        prior_host = key

    seen = set()
    prior_id = None
    for index, row in enumerate(obj["payload_identities"]):
        where = f"release_inventory.payload_identities[{index}]"
        exact_keys(
            row,
            (
                "payload_id",
                "source_path",
                "extractor",
                "kind",
                "value",
                "consumer_acted",
            ),
            where=where,
        )
        payload_id = validate_slug(row["payload_id"], f"{where}.payload_id", dotted=True)
        normalized_path(row["source_path"], f"{where}.source_path")
        extractor = validate_inventory_extractor(row["extractor"], f"{where}.extractor")
        require(
            extractor["path"] == row["source_path"],
            f"{where}.extractor.path: source_path mismatch",
        )
        kind = row["kind"]
        require(
            kind in {"content-hash", "version-stamp"}
            or (
                isinstance(kind, str)
                and re.fullmatch(
                    r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*:[a-z][a-z0-9-]*",
                    kind,
                )
                is not None
            ),
            f"{where}.kind: invalid",
        )
        require(isinstance(row["value"], str) and bool(row["value"]), f"{where}.value: empty")
        require(type(row["consumer_acted"]) is bool, f"{where}.consumer_acted: expected boolean")
        require(payload_id not in seen, "release_inventory.payload_identities: duplicate payload_id")
        require(prior_id is None or prior_id < payload_id, "release_inventory.payload_identities: rows are not in identity order")
        seen.add(payload_id)
        prior_id = payload_id

    categories = {
        "installation-coordinate",
        "installation-input",
        "host-visible-entrypoint",
        "configuration",
        "managed-state",
        "runtime-requirement",
        "surface-support",
        "consumed-output-protocol",
    }
    compatibilities = {
        "initial",
        "unchanged",
        "backward-compatible-fix",
        "backward-compatible-capability",
        "supported-surface-addition",
        "breaking-change",
        "false-claim-correction",
        "supported-surface-withdrawal",
    }
    seen = set()
    prior_id = None
    for index, row in enumerate(obj["public_contract_items"]):
        where = f"release_inventory.public_contract_items[{index}]"
        exact_keys(
            row,
            (
                "contract_id",
                "category",
                "source",
                "extractor",
                "fingerprint",
                "compatibility",
            ),
            where=where,
        )
        contract_id = validate_slug(row["contract_id"], f"{where}.contract_id", dotted=True)
        require(row["category"] in categories, f"{where}.category: invalid")
        validate_stable_reference(row["source"], f"{where}.source")
        validate_inventory_extractor(row["extractor"], f"{where}.extractor")
        require(
            isinstance(row["fingerprint"], str)
            and SHA256.fullmatch(row["fingerprint"]),
            f"{where}.fingerprint: invalid",
        )
        require(row["compatibility"] in compatibilities, f"{where}.compatibility: invalid")
        require(contract_id not in seen, "release_inventory.public_contract_items: duplicate contract_id")
        require(prior_id is None or prior_id < contract_id, "release_inventory.public_contract_items: rows are not in identity order")
        seen.add(contract_id)
        prior_id = contract_id

    seen = set()
    prior_id = None
    for index, row in enumerate(obj["support_derivatives"]):
        where = f"release_inventory.support_derivatives[{index}]"
        exact_keys(
            row,
            ("derivative_id", "kind", "path", "extractor", "surface_projection"),
            where=where,
        )
        derivative_id = validate_slug(row["derivative_id"], f"{where}.derivative_id", dotted=True)
        require(
            row["kind"] in {"public-support-table", "host-manifest-claim"},
            f"{where}.kind: invalid",
        )
        normalized_path(row["path"], f"{where}.path")
        extractor = validate_inventory_extractor(row["extractor"], f"{where}.extractor")
        require(extractor["path"] == row["path"], f"{where}.extractor.path: path mismatch")
        require(isinstance(row["surface_projection"], list), f"{where}.surface_projection: expected array")
        surfaces = set()
        for surface_index, surface_row in enumerate(row["surface_projection"]):
            candidate_version = package_version
            if candidate_version is None and isinstance(surface_row, dict):
                support = surface_row.get("support_record")
                evidence = surface_row.get("evidence", [])
                if isinstance(support, dict):
                    candidate_version = support.get("package_version")
                elif isinstance(evidence, list) and evidence and isinstance(evidence[0], dict):
                    candidate_version = evidence[0].get("package_version")
            if not isinstance(candidate_version, str) or not SEMVER.fullmatch(candidate_version):
                candidate_version = "0.0.0"
            validate_surface_row(
                surface_row,
                candidate_version,
                f"{where}.surface_projection[{surface_index}]",
            )
            surface_id = surface_row["surface_id"]
            require(surface_id not in surfaces, f"{where}.surface_projection: duplicate surface_id")
            surfaces.add(surface_id)
        require(derivative_id not in seen, "release_inventory.support_derivatives: duplicate derivative_id")
        require(prior_id is None or prior_id < derivative_id, "release_inventory.support_derivatives: rows are not in identity order")
        seen.add(derivative_id)
        prior_id = derivative_id
    return obj


def validate_product(root: Path, metadata_path: str, phase: str) -> dict[str, Any]:
    root = root.resolve()
    metadata_file = (root / metadata_path).resolve()
    require(root in metadata_file.parents, "release_metadata: outside package root")
    metadata = validate_release_metadata(load_json(metadata_file), phase)
    version = extract_version(root, metadata["version_authority"], "release_metadata.version_authority")
    for index, carrier in enumerate(metadata["version_carriers"]):
        extractor = {key: carrier[key] for key in ("path", "format", "selector") if key in carrier}
        actual = extract_version(root, extractor, f"release_metadata.version_carriers[{index}]")
        require(actual == version, f"release_metadata.version_carriers[{index}]: carrier mismatch")
    surface = validate_surface_contract(load_json(root / metadata["surface_contract"]))
    require(surface["version"] == version, "surface_contract.version: authority mismatch")

    provider_bytes = run_inventory_provider(root, metadata["inventory_provider"])
    provider_inventory = load_json_bytes(provider_bytes, "inventory_provider.stdout")
    checked_inventory_path = root / metadata["release_inventory"]
    checked_bytes = checked_inventory_path.read_bytes()
    require(provider_bytes == checked_bytes, "release_inventory: provider bytes differ from checked-in inventory")
    inventory = validate_release_inventory(provider_inventory, version)
    inventory_hosts = {
        (
            row["path"],
            row["version_extractor"]["format"],
            row["version_extractor"].get("selector"),
        )
        for row in inventory["host_manifests"]
    }
    carriers = {
        (row["path"], row["format"], row.get("selector"))
        for row in metadata["version_carriers"]
        if row["role"] == "host-manifest"
    }
    require(inventory_hosts == carriers, "release_inventory.host_manifests: host-manifest/carrier completeness mismatch")
    if "payload_identity" in metadata:
        require(len(inventory["payload_identities"]) == 1, "release_metadata.payload_identity: inventory must contain exactly one payload")
        item = inventory["payload_identities"][0]
        require(
            metadata["payload_identity"] == {"kind": item.get("kind"), "value": item.get("value")},
            "release_metadata.payload_identity: inventory mismatch",
        )
    history = load_json(root / metadata["release_history"])
    validate_release_history(history)

    expected_tag = f"{metadata['plugin_id']}-v{version}"
    result: dict[str, Any] = {"package_version": version, "expected_tag": expected_tag}
    if phase == "release":
        ref = f"refs/tags/{expected_tag}"
        git = subprocess.run(
            ["git", "-C", str(root), "rev-parse", f"{ref}^{{commit}}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        require(git.returncode == 0 and COMMIT.fullmatch(git.stdout.strip()) is not None, f"release tag missing: {ref}")
        result["release_tag"] = expected_tag
        result["source_commit"] = git.stdout.strip()
    return result


def validate_release_history(value: Any) -> dict[str, Any]:
    obj = exact_keys(value, ("schema_version", "releases"), where="release_history")
    require(obj["schema_version"] == 1, "release_history.schema_version: expected 1")
    require(isinstance(obj["releases"], list), "release_history.releases: expected array")
    prior: Optional[tuple[Any, ...]] = None
    versions = set()
    for index, row in enumerate(obj["releases"]):
        where = f"release_history.releases[{index}]"
        require(isinstance(row, dict), f"{where}: expected object")
        for key in (
            "package_version",
            "release_tag",
            "source_commit",
            "release_inventory_sha256",
            "payload_identities",
            "public_contract_inventory_sha256",
            "surface_contract_sha256",
            "change_set",
            "release_approval",
        ):
            require(key in row, f"{where}: missing {key}")
        version = validate_semver(row["package_version"], f"{where}.package_version")
        require(row["release_tag"].endswith("-v" + version), f"{where}.release_tag: version mismatch")
        require(isinstance(row["source_commit"], str) and COMMIT.fullmatch(row["source_commit"]), f"{where}.source_commit: invalid")
        precedence = semver_precedence(version)
        require(precedence not in versions, f"{where}.package_version: equal-precedence duplicate")
        if prior is not None:
            require(compare_precedence(prior, precedence) < 0, f"{where}.package_version: not increasing")
        prior = precedence
        versions.add(precedence)
        for digest in ("release_inventory_sha256", "public_contract_inventory_sha256", "surface_contract_sha256"):
            require(isinstance(row[digest], str) and SHA256.fullmatch(row[digest]), f"{where}.{digest}: invalid")
        validate_stable_reference(row["release_approval"], f"{where}.release_approval")
        require(isinstance(row["payload_identities"], list) and isinstance(row["change_set"], list), f"{where}: invalid arrays")
        if index > 0:
            require("prior_history_reference" in row, f"{where}: missing prior_history_reference")
            validate_stable_reference(row["prior_history_reference"], f"{where}.prior_history_reference")
    return obj


def semver_precedence(version: str) -> tuple[int, int, int, Optional[tuple[tuple[bool, Any], ...]]]:
    match = SEMVER.fullmatch(version)
    assert match is not None
    major, minor, patch = (int(match.group(i)) for i in range(1, 4))
    prerelease = match.group(4)
    if prerelease is None:
        return (major, minor, patch, None)
    identifiers = tuple(
        (part.isdigit(), int(part) if part.isdigit() else part) for part in prerelease.split(".")
    )
    return (major, minor, patch, identifiers)


def compare_precedence(left: tuple[Any, ...], right: tuple[Any, ...]) -> int:
    if left[:3] != right[:3]:
        return -1 if left[:3] < right[:3] else 1
    left_pre, right_pre = left[3], right[3]
    if left_pre is None or right_pre is None:
        if left_pre is right_pre:
            return 0
        return 1 if left_pre is None else -1
    for left_id, right_id in zip(left_pre, right_pre):
        if left_id == right_id:
            continue
        left_num, left_value = left_id
        right_num, right_value = right_id
        if left_num != right_num:
            return -1 if left_num else 1
        return -1 if left_value < right_value else 1
    return (len(left_pre) > len(right_pre)) - (len(left_pre) < len(right_pre))


def validate_product_adoptions(value: Any) -> dict[str, Any]:
    obj = exact_keys(value, ("schema_version", "products"), where="product_adoptions")
    require(obj["schema_version"] == 1, "product_adoptions.schema_version: expected 1")
    require(isinstance(obj["products"], list), "product_adoptions.products: expected array")
    seen = set()
    prior = None
    for index, row in enumerate(obj["products"]):
        where = f"product_adoptions.products[{index}]"
        required = {"plugin_id", "repository", "state", "standing_decisions_to_reconcile", "ownership_changes"}
        optional = {"adoption_decision"}
        exact_keys(row, required, optional, where)
        plugin = validate_slug(row["plugin_id"], f"{where}.plugin_id")
        require(plugin not in seen, "product_adoptions.products: duplicate plugin_id")
        require(prior is None or prior < plugin, "product_adoptions.products: products are not in plugin_id order")
        seen.add(plugin)
        prior = plugin
        validate_repository(row["repository"], f"{where}.repository")
        require(row["state"] in {"required", "complete"}, f"{where}.state: invalid")
        for key in ("standing_decisions_to_reconcile", "ownership_changes"):
            require(
                isinstance(row[key], list)
                and row[key] == sorted(set(row[key]))
                and all(isinstance(item, str) and item for item in row[key]),
                f"{where}.{key}: expected sorted unique strings",
            )
        if row["state"] == "complete":
            validate_stable_reference(row.get("adoption_decision"), f"{where}.adoption_decision")
        else:
            require("adoption_decision" not in row, f"{where}.adoption_decision: forbidden while required")
    return obj


def validate_baseline(value: Any) -> dict[str, Any]:
    obj = exact_keys(
        value,
        ("schema_version", "baseline_source_commit", "fingerprint_algorithm", "rows"),
        where="legacy_baseline",
    )
    require(obj["schema_version"] == 1, "legacy_baseline.schema_version: expected 1")
    require(obj["baseline_source_commit"] == BASELINE_COMMIT, "legacy_baseline.baseline_source_commit: fixed commit mismatch")
    require(obj["fingerprint_algorithm"] == BASELINE_ALGORITHM, "legacy_baseline.fingerprint_algorithm: mismatch")
    validate_legacy_rows(obj["rows"], "legacy_baseline.rows", baseline=True)
    return obj


def validate_legacy_rows(value: Any, where: str, baseline: bool = False) -> list[dict[str, Any]]:
    require(isinstance(value, list), f"{where}: expected array")
    prior = None
    keys = set()
    for index, row in enumerate(value):
        row_where = f"{where}[{index}]"
        required = {"plugin_id", "surface_id", "manifest_path", "selector_fingerprint"}
        if baseline:
            required |= {"kind", "repository", "path", "ref"}
            optional: set[str] = set()
        else:
            optional = {"missing_contract_elements", "disclosure", "terminal_action"}
        exact_keys(row, required, optional, row_where)
        validate_slug(row["plugin_id"], f"{row_where}.plugin_id")
        validate_slug(row["surface_id"], f"{row_where}.surface_id", dotted=True)
        require(row["manifest_path"] == manifest_for_surface(row["surface_id"]), f"{row_where}.manifest_path: mismatch")
        require(isinstance(row["selector_fingerprint"], str) and SHA256.fullmatch(row["selector_fingerprint"]), f"{row_where}.selector_fingerprint: invalid")
        if baseline:
            require(row["kind"] in {"mutable", "immutable"}, f"{row_where}.kind: invalid")
            validate_repository(row["repository"], f"{row_where}.repository")
            normalized_path(row["path"], f"{row_where}.path", allow_empty=True)
            require(isinstance(row["ref"], str), f"{row_where}.ref: expected string")
        key = (row["surface_id"], row["plugin_id"])
        require(key not in keys and (prior is None or prior < key), f"{where}: duplicate or unsorted key")
        keys.add(key)
        prior = key
        if not baseline:
            require(
                row.get("missing_contract_elements") == sorted(set(row.get("missing_contract_elements", [])))
                and bool(row.get("missing_contract_elements")),
                f"{row_where}.missing_contract_elements: invalid",
            )
            require(row.get("disclosure") == "legacy published stock", f"{row_where}.disclosure: invalid")
            require(row.get("terminal_action") == "adopt-or-delist", f"{row_where}.terminal_action: invalid")
    return value


def selector_projection(
    plugin_id: str,
    surface_id: str,
    manifest_path: str,
    selector: dict[str, Any],
) -> dict[str, str]:
    validate_source_selector(selector)
    return {
        "kind": selector["kind"],
        "manifest_path": manifest_path,
        "path": selector["path"],
        "plugin_id": plugin_id,
        "ref": "" if selector["kind"] == "mutable" else selector["ref"]["value"],
        "repository": selector["repository"],
        "surface_id": surface_id,
    }


def selector_fingerprint(projection: dict[str, str]) -> str:
    ordered = {
        "kind": projection["kind"],
        "manifest_path": projection["manifest_path"],
        "path": projection["path"],
        "plugin_id": projection["plugin_id"],
        "ref": projection["ref"],
        "repository": projection["repository"],
        "surface_id": projection["surface_id"],
    }
    raw = json.dumps(
        normalize_strings(ordered),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def host_entries_from_manifest(manifest_path: str, document: dict[str, Any]) -> list[dict[str, Any]]:
    require(isinstance(document, dict) and isinstance(document.get("plugins"), list), f"{manifest_path}: invalid host manifest")
    surface_id = "claude-code.local.interactive" if manifest_path.startswith(".claude") else "codex.local.interactive"
    rows = []
    plugin_ids = set()
    for index, plugin in enumerate(document["plugins"]):
        require(isinstance(plugin, dict), f"{manifest_path}.plugins[{index}]: invalid")
        name = plugin.get("name")
        validate_slug(name, f"{manifest_path}.plugins[{index}].name")
        require(
            name not in plugin_ids,
            f"{manifest_path}.plugins: duplicate plugin entry {name}",
        )
        plugin_ids.add(name)
        source = plugin.get("source")
        require(
            isinstance(source, dict)
            and source.get("source") == "git-subdir"
            and set(source) == {"source", "url", "path"},
            f"{manifest_path}.plugins[{index}].source: unsupported selector",
        )
        selector = {
            "kind": "mutable",
            "repository": source["url"],
            "path": source["path"],
        }
        projection = selector_projection(name, surface_id, manifest_path, selector)
        rows.append({**projection, "selector_fingerprint": selector_fingerprint(projection)})
    return rows


def legacy_discover(root: Path, baseline_commit: str) -> dict[str, Any]:
    require(baseline_commit == BASELINE_COMMIT, "legacy-discover: baseline commit is immutable")
    rows = []
    for manifest in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
        result = subprocess.run(
            ["git", "-C", str(root), "show", f"{baseline_commit}:{manifest}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(result.returncode == 0, f"legacy-discover: cannot read {manifest} at {baseline_commit}")
        document = load_json_bytes(result.stdout, f"{baseline_commit}:{manifest}")
        rows.extend(host_entries_from_manifest(manifest, document))
    rows.sort(key=lambda row: (row["surface_id"], row["plugin_id"]))
    return {
        "schema_version": 1,
        "baseline_source_commit": baseline_commit,
        "fingerprint_algorithm": BASELINE_ALGORITHM,
        "rows": rows,
    }


def root_from_manage() -> Path:
    return Path(__file__).resolve().parents[2]


def validate_initial_stock(root: Path, baseline: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    initial_path = root / "distribution" / "legacy-stock-initial.json"
    current_path = root / "distribution" / "legacy-stock.json"
    initial = load_json(initial_path)
    exact_keys(initial, ("schema_version", "rows"), where="legacy_stock_initial")
    require(initial["schema_version"] == 1, "legacy_stock_initial.schema_version: expected 1")
    validate_legacy_rows(initial["rows"], "legacy_stock_initial.rows")
    require(len(initial["rows"]) == 1, "legacy_stock_initial.rows: expected exact one-row stock")
    row = initial["rows"][0]
    require(
        (row["plugin_id"], row["surface_id"]) == ("trellis", "claude-code.local.interactive"),
        "legacy_stock_initial.rows: expected Trellis Claude row",
    )
    baseline_map = {(item["plugin_id"], item["surface_id"]): item for item in baseline["rows"]}
    baseline_row = baseline_map.get((row["plugin_id"], row["surface_id"]))
    require(
        baseline_row is not None
        and baseline_row["selector_fingerprint"] == row["selector_fingerprint"]
        and baseline_row["manifest_path"] == row["manifest_path"],
        "legacy_stock_initial.rows: baseline mismatch",
    )
    require(
        row["missing_contract_elements"]
        == [
            "canonical-semver-authority",
            "immutable-release-tag",
            "product-adoption-decision",
            "version-bound-surface-contract",
        ],
        "legacy_stock_initial.rows: exact missing contract set mismatch",
    )

    current = load_json(current_path)
    exact_keys(current, ("schema_version", "initial_stock_reference", "rows"), where="legacy_stock")
    require(current["schema_version"] == 1, "legacy_stock.schema_version: expected 1")
    reference = validate_stable_reference(current["initial_stock_reference"], "legacy_stock.initial_stock_reference")
    require(reference["kind"] == "repo-path", "legacy_stock.initial_stock_reference: expected repo-path")
    require(reference["path"] == "distribution/legacy-stock-initial.json", "legacy_stock.initial_stock_reference.path: mismatch")
    result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "show",
            f"{reference['source_commit']}:distribution/legacy-stock-initial.json",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "legacy_stock.initial_stock_reference: comparison commit is unresolvable")
    require(hashlib.sha256(result.stdout).hexdigest() == reference["sha256"], "legacy_stock.initial_stock_reference: digest mismatch")
    require(result.stdout == initial_path.read_bytes(), "legacy_stock_initial: working tree differs from immutable source")
    validate_legacy_rows(current["rows"], "legacy_stock.rows")
    initial_by_key = {(item["plugin_id"], item["surface_id"]): item for item in initial["rows"]}
    for item in current["rows"]:
        require(initial_by_key.get((item["plugin_id"], item["surface_id"])) == item, "legacy_stock.rows: not a removal-only subset")
    return initial, current


def effective_factor(
    factor: str,
    satisfied: bool,
    reason_codes: Iterable[str] = (),
    source_refs: Iterable[dict[str, Any]] = (),
    owners: Iterable[str] = (),
) -> dict[str, Any]:
    return {
        "factor": factor,
        "satisfied": satisfied,
        "reason_codes": sorted(set(reason_codes)),
        "source_refs": sorted(
            (copy.deepcopy(item) for item in source_refs),
            key=lambda item: canonical_json(item),
        ),
        "owners": sorted(set(owners)),
    }


def source_reference(value: dict[str, Any], where: str) -> dict[str, Any]:
    return validate_stable_reference(value.get("source_reference"), f"{where}.source_reference")


def validate_effective_facts(value: Any) -> dict[str, Any]:
    obj = exact_keys(
        value,
        (
            "schema_version",
            "subject",
            "product_contract",
            "distribution_record",
            "consumer_selection",
            "environment_assessment",
            "product_setup",
        ),
        where="effective_facts",
    )
    require(obj["schema_version"] == 1, "effective_facts.schema_version: expected 1")
    validate_subject(obj["subject"], "effective_facts.subject")
    validate_product_fact(obj["product_contract"])
    validate_distribution_fact(obj["distribution_record"])
    validate_selection_fact(obj["consumer_selection"])
    validate_environment_fact(obj["environment_assessment"])
    validate_setup_fact(obj["product_setup"])
    return obj


def validate_product_fact(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "effective_facts.product_contract: expected object")
    kind = value.get("kind")
    if kind == "record":
        obj = exact_keys(value, ("kind", "source_reference", "subject", "row"), where="effective_facts.product_contract")
        subject = validate_subject(obj["subject"], "effective_facts.product_contract.subject")
        validate_stable_reference(obj["source_reference"], "effective_facts.product_contract.source_reference")
        validate_surface_row(obj["row"], subject["package_version"], "effective_facts.product_contract.row")
    elif kind == "missing":
        obj = exact_keys(value, ("kind", "source_reference", "lookup"), where="effective_facts.product_contract")
        validate_stable_reference(obj["source_reference"])
        validate_subject(obj["lookup"])
    elif kind == "invalid":
        obj = exact_keys(value, ("kind", "source_reference", "lookup", "errors"), where="effective_facts.product_contract")
        validate_stable_reference(obj["source_reference"])
        validate_subject(obj["lookup"])
        allowed = {"row-schema-invalid", "duplicate-surface", "stable-reference-mismatch"}
        require(isinstance(obj["errors"], list) and bool(obj["errors"]) and set(obj["errors"]) <= allowed, "effective_facts.product_contract.errors: invalid")
    else:
        reject("effective_facts.product_contract.kind: invalid")
    return value


def validate_distribution_fact(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "effective_facts.distribution_record: expected object")
    kind = value.get("kind")
    if kind == "record":
        obj = exact_keys(value, ("kind", "source_reference", "record_type", "record"), where="effective_facts.distribution_record")
        validate_stable_reference(obj["source_reference"])
        if obj["record_type"] == "catalog":
            validate_catalog_row(obj["record"], "effective_facts.distribution_record.record")
        elif obj["record_type"] == "provisioner":
            validate_provisioner_row(obj["record"], "effective_facts.distribution_record.record")
        else:
            reject("effective_facts.distribution_record.record_type: invalid")
    elif kind in {"missing", "invalid"}:
        required = {"kind", "source_reference", "record_type", "lookup_key"}
        if kind == "invalid":
            required.add("error_codes")
        obj = exact_keys(value, required, where="effective_facts.distribution_record")
        validate_stable_reference(obj["source_reference"])
        if obj["record_type"] == "catalog":
            exact_keys(obj["lookup_key"], ("plugin_id", "surface_id"), where="effective_facts.distribution_record.lookup_key")
        elif obj["record_type"] == "provisioner":
            exact_keys(obj["lookup_key"], ("route_id", "surface_id", "plugin_id", "package_version"), where="effective_facts.distribution_record.lookup_key")
        else:
            reject("effective_facts.distribution_record.record_type: invalid")
        if kind == "invalid":
            allowed = {"row-schema-invalid", "duplicate-key", "stable-reference-mismatch"}
            require(isinstance(obj["error_codes"], list) and bool(obj["error_codes"]) and len(obj["error_codes"]) == len(set(obj["error_codes"])) and set(obj["error_codes"]) <= allowed, "effective_facts.distribution_record.error_codes: invalid")
    else:
        reject("effective_facts.distribution_record.kind: invalid")
    return value


def validate_selection_fact(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "effective_facts.consumer_selection: expected object")
    state = value.get("state")
    if state == "selected":
        obj = exact_keys(
            value,
            ("state", "request_id", "plugin_id", "package_version", "surface_id", "route_id", "source_reference"),
            where="effective_facts.consumer_selection",
        )
        validate_slug(obj["request_id"], "effective_facts.consumer_selection.request_id", dotted=True)
        validate_slug(obj["route_id"], "effective_facts.consumer_selection.route_id", dotted=True)
        validate_slug(obj["plugin_id"], "effective_facts.consumer_selection.plugin_id")
        validate_semver(obj["package_version"], "effective_facts.consumer_selection.package_version")
        validate_slug(obj["surface_id"], "effective_facts.consumer_selection.surface_id", dotted=True)
        validate_stable_reference(obj["source_reference"])
    elif state == "missing":
        obj = exact_keys(value, ("state", "subject", "source_reference"), where="effective_facts.consumer_selection")
        validate_subject(obj["subject"])
        validate_stable_reference(obj["source_reference"])
    elif state == "invalid":
        obj = exact_keys(value, ("state", "subject", "source_reference", "errors"), where="effective_facts.consumer_selection")
        validate_subject(obj["subject"])
        validate_stable_reference(obj["source_reference"])
        require(isinstance(obj["errors"], list) and bool(obj["errors"]) and set(obj["errors"]) <= {"selection-mismatch", "selection-reference-invalid"}, "effective_facts.consumer_selection.errors: invalid")
    else:
        reject("effective_facts.consumer_selection.state: invalid")
    return value


def validate_environment_fact(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "effective_facts.environment_assessment: expected object")
    state = value.get("state")
    if state in {"ready", "not-ready"}:
        required = {"state", "subject", "evidence", "source_reference"}
        if state == "not-ready":
            required.add("missing_prerequisites")
        obj = exact_keys(value, required, where="effective_facts.environment_assessment")
        validate_subject(obj["subject"])
        validate_stable_reference(obj["source_reference"])
        require(isinstance(obj["evidence"], list) and bool(obj["evidence"]), "effective_facts.environment_assessment.evidence: expected non-empty array")
        for index, evidence in enumerate(obj["evidence"]):
            validate_evidence_binding(evidence, f"effective_facts.environment_assessment.evidence[{index}]")
        if state == "not-ready":
            require(isinstance(obj["missing_prerequisites"], list) and bool(obj["missing_prerequisites"]), "effective_facts.environment_assessment.missing_prerequisites: empty")
    elif state == "missing":
        obj = exact_keys(value, ("state", "subject", "source_reference"), where="effective_facts.environment_assessment")
        validate_subject(obj["subject"])
        validate_stable_reference(obj["source_reference"])
    elif state == "invalid":
        obj = exact_keys(value, ("state", "subject", "source_reference", "errors"), where="effective_facts.environment_assessment")
        validate_subject(obj["subject"])
        validate_stable_reference(obj["source_reference"])
        allowed = {"assessment-schema-invalid", "assessment-reference-invalid", "assessment-identity-mismatch"}
        require(isinstance(obj["errors"], list) and bool(obj["errors"]) and set(obj["errors"]) <= allowed, "effective_facts.environment_assessment.errors: invalid")
    else:
        reject("effective_facts.environment_assessment.state: invalid")
    return value


def validate_setup_fact(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "effective_facts.product_setup: expected object")
    state = value.get("state")
    if state == "not-required":
        obj = exact_keys(value, ("subject", "state", "requirement_reference", "contract"), where="effective_facts.product_setup")
        require(obj["contract"] is None, "effective_facts.product_setup.contract: expected null")
        validate_stable_reference(obj["requirement_reference"])
    elif state == "complete":
        obj = exact_keys(value, ("subject", "state", "requirement_reference", "contract", "completion_reference", "completion_identity"), where="effective_facts.product_setup")
        validate_stable_reference(obj["requirement_reference"])
        validate_stable_reference(obj["contract"])
        validate_stable_reference(obj["completion_reference"])
        validate_subject(obj["completion_identity"])
    elif state == "incomplete":
        obj = exact_keys(value, ("subject", "state", "requirement_reference", "contract", "reason_code", "reason_source"), where="effective_facts.product_setup")
        validate_stable_reference(obj["requirement_reference"])
        validate_stable_reference(obj["contract"])
        require(obj["reason_code"] in {"setup-not-run", "setup-failed"}, "effective_facts.product_setup.reason_code: invalid")
        validate_stable_reference(obj["reason_source"])
    elif state == "missing":
        obj = exact_keys(value, ("subject", "state", "missing_kind", "source_reference"), where="effective_facts.product_setup")
        require(obj["missing_kind"] in {"product-requirement", "completion-proof"}, "effective_facts.product_setup.missing_kind: invalid")
        validate_stable_reference(obj["source_reference"])
    elif state == "invalid":
        obj = exact_keys(value, ("subject", "state", "source_reference", "error_codes"), where="effective_facts.product_setup")
        allowed = {"product-requirement-invalid", "consumer-setup-fact-invalid", "setup-identity-mismatch"}
        require(isinstance(obj["error_codes"], list) and bool(obj["error_codes"]) and len(obj["error_codes"]) == len(set(obj["error_codes"])) and set(obj["error_codes"]) <= allowed, "effective_facts.product_setup.error_codes: invalid")
        validate_stable_reference(obj["source_reference"])
    else:
        reject("effective_facts.product_setup.state: invalid")
    validate_subject(obj["subject"], "effective_facts.product_setup.subject")
    return value


def evaluate_effective(value: Any) -> dict[str, Any]:
    facts = validate_effective_facts(value)
    subject = facts["subject"]
    factors: dict[str, dict[str, Any]] = {}

    product = facts["product_contract"]
    product_ref = product["source_reference"]
    if product["kind"] == "record":
        product_match = product["subject"] == subject
        supported = product["row"]["status"] == "supported" and product_match
        factors["product_supported"] = effective_factor(
            "product_supported",
            supported,
            () if supported else ("product-not-supported",),
            (product_ref,),
            () if supported else ("product",),
        )
    elif product["kind"] == "missing":
        product_match = False
        factors["product_supported"] = effective_factor("product_supported", False, ("product-row-missing",), (product_ref,), ("product",))
    else:
        product_match = False
        factors["product_supported"] = effective_factor("product_supported", False, ("product-row-invalid",), (product_ref,), ("product",))

    distribution = facts["distribution_record"]
    distribution_ref = distribution["source_reference"]
    distribution_match = False
    if distribution["kind"] == "record":
        record = distribution["record"]
        verified = record["state"] == "verified"
        if verified:
            distribution_identity = {
                key: record[key]
                for key in ("plugin_id", "package_version", "release_tag", "source_commit", "surface_id")
            }
            distribution_match = distribution_identity == subject
        factors["distribution_verified"] = effective_factor(
            "distribution_verified",
            verified and distribution_match,
            () if verified and distribution_match else ("distribution-not-verified",),
            (distribution_ref,),
            () if verified and distribution_match else ("stewards",),
        )
    elif distribution["kind"] == "missing":
        factors["distribution_verified"] = effective_factor("distribution_verified", False, ("distribution-row-missing",), (distribution_ref,), ("stewards",))
    else:
        factors["distribution_verified"] = effective_factor("distribution_verified", False, ("distribution-row-invalid",), (distribution_ref,), ("stewards",))

    selection = facts["consumer_selection"]
    selection_ref = selection["source_reference"]
    selection_match = False
    if selection["state"] == "selected":
        selection_match = all(selection[key] == subject[key] for key in ("plugin_id", "package_version", "surface_id"))
        factors["consumer_selected"] = effective_factor(
            "consumer_selected",
            selection_match,
            () if selection_match else ("selection-mismatch",),
            (selection_ref,),
            () if selection_match else ("consumer/environment",),
        )
    elif selection["state"] == "missing":
        factors["consumer_selected"] = effective_factor("consumer_selected", False, ("consumer-not-selected",), (selection_ref,), ("consumer/environment",))
    else:
        factors["consumer_selected"] = effective_factor("consumer_selected", False, ("selection-mismatch",), (selection_ref,), ("consumer/environment",))

    environment = facts["environment_assessment"]
    environment_ref = environment["source_reference"]
    environment_match = environment.get("subject") == subject
    if environment["state"] == "ready":
        factors["environment_ready"] = effective_factor(
            "environment_ready",
            environment_match,
            () if environment_match else ("environment-assessment-invalid",),
            (environment_ref,),
            () if environment_match else ("consumer/environment",),
        )
    elif environment["state"] == "not-ready":
        factors["environment_ready"] = effective_factor("environment_ready", False, ("environment-not-ready",), (environment_ref,), ("consumer/environment",))
    elif environment["state"] == "missing":
        factors["environment_ready"] = effective_factor("environment_ready", False, ("environment-assessment-missing",), (environment_ref,), ("consumer/environment",))
    else:
        factors["environment_ready"] = effective_factor("environment_ready", False, ("environment-assessment-invalid",), (environment_ref,), ("consumer/environment",))

    setup = facts["product_setup"]
    setup_refs = [setup.get("requirement_reference") or setup.get("source_reference")]
    setup_refs.extend(item for item in (setup.get("completion_reference"), setup.get("reason_source")) if item)
    setup_match = setup["subject"] == subject
    if setup["state"] == "not-required":
        setup_ok = setup_match and product["kind"] == "record" and not product["row"]["post_install_setup"]["required"]
        factors["product_setup_complete"] = effective_factor(
            "product_setup_complete",
            setup_ok,
            () if setup_ok else ("product-requirement-invalid",),
            setup_refs,
            () if setup_ok else ("product",),
        )
    elif setup["state"] == "complete":
        setup_ok = setup_match and setup["completion_identity"] == subject
        factors["product_setup_complete"] = effective_factor(
            "product_setup_complete",
            setup_ok,
            () if setup_ok else ("setup-identity-mismatch",),
            setup_refs,
            () if setup_ok else ("product", "consumer/environment"),
        )
    elif setup["state"] == "incomplete":
        factors["product_setup_complete"] = effective_factor("product_setup_complete", False, (setup["reason_code"],), setup_refs, ("consumer/environment",))
    elif setup["state"] == "missing":
        code = "setup-requirement-missing" if setup["missing_kind"] == "product-requirement" else "setup-completion-proof-missing"
        owner = "product" if setup["missing_kind"] == "product-requirement" else "consumer/environment"
        factors["product_setup_complete"] = effective_factor("product_setup_complete", False, (code,), setup_refs, (owner,))
    else:
        owners = set()
        codes = []
        for code in setup["error_codes"]:
            codes.append(code)
            if code == "product-requirement-invalid":
                owners.add("product")
            elif code == "consumer-setup-fact-invalid":
                owners.add("consumer/environment")
            else:
                owners.update(("product", "consumer/environment"))
        factors["product_setup_complete"] = effective_factor("product_setup_complete", False, codes, setup_refs, owners)

    identity_sources = (product_match, distribution_match, environment_match)
    if all(identity_sources):
        factors["identity_match"] = effective_factor(
            "identity_match",
            True,
            source_refs=(product_ref, distribution_ref, environment_ref),
        )
    else:
        unavailable = []
        owners = []
        if not product_match:
            unavailable.append("identity-source-missing" if product["kind"] == "missing" else "identity-source-invalid" if product["kind"] == "invalid" else "identity-mismatch")
            owners.append("product")
        if not distribution_match:
            if distribution["kind"] == "missing":
                unavailable.append("identity-source-missing")
            elif distribution["kind"] == "invalid":
                unavailable.append("identity-source-invalid")
            elif distribution["record"]["state"] != "verified":
                unavailable.append("identity-source-unavailable")
            else:
                unavailable.append("identity-mismatch")
            owners.append("stewards")
        if not environment_match:
            unavailable.append("identity-source-missing" if environment["state"] == "missing" else "identity-source-invalid" if environment["state"] == "invalid" else "identity-mismatch")
            owners.append("consumer/environment")
        factors["identity_match"] = effective_factor(
            "identity_match",
            False,
            unavailable,
            (product_ref, distribution_ref, environment_ref),
            owners,
        )

    ordered = [factors[name] for name in FACTOR_ORDER]
    return {
        "schema_version": 1,
        "subject": copy.deepcopy(subject),
        "effective": all(item["satisfied"] for item in ordered),
        "factors": ordered,
    }


def build_host_catalogs(catalogs: dict[str, Any]) -> dict[str, bytes]:
    records = sorted(
        (row for row in catalogs["records"] if row["state"] != "absent"),
        key=lambda row: (row["surface_id"], row["plugin_id"]),
    )
    claude_plugins = []
    codex_plugins = []
    host_entries: dict[str, set[str]] = {
        "claude-code": set(),
        "codex": set(),
    }
    for row in records:
        fields = copy.deepcopy(row["host_projection"]["fields"])
        host = row["host_projection"]["host"]
        entry_name = row["host_projection"]["entry_name"]
        require(
            entry_name not in host_entries[host],
            f"host projection: duplicate {host} plugin entry {entry_name}",
        )
        host_entries[host].add(entry_name)
        entry = {"name": entry_name, **fields}
        if host == "claude-code":
            claude_plugins.append(entry)
        elif host == "codex":
            codex_plugins.append(entry)
    return {
        ".claude-plugin/marketplace.json": canonical_json(
            {
                "name": "kodhama",
                "owner": {"name": "kodhama"},
                "description": "The kodhama marketplace — one install door for the stewards.",
                "plugins": claude_plugins,
            },
            newline=True,
        ),
        ".agents/plugins/marketplace.json": canonical_json(
            {
                "name": "kodhama",
                "interface": {"displayName": "kodhama stewards"},
                "plugins": codex_plugins,
            },
            newline=True,
        ),
    }


def build_availability(catalogs: dict[str, Any], provisioners: dict[str, Any]) -> bytes:
    lines = [
        "---",
        "id: stewards-distribution-availability",
        "type: generated-documentation",
        "status: gated",
        "depends_on: [kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v1]",
        "owner: agent",
        "updated: 2026-07-24",
        "---",
        "",
        "# Distribution availability",
        "",
        "> GENERATED by `distribution/manage generate`; edit the JSON sources.",
        "",
        "## Catalogs",
        "",
        "| Plugin | Surface | State | Selector | Disclosure |",
        "|---|---|---|---|---|",
    ]
    for row in sorted(catalogs["records"], key=lambda item: (item["plugin_id"], item["surface_id"])):
        selector = row.get("source_selector")
        selector_text = "—"
        if selector:
            selector_text = f"{selector['kind']} `{selector['repository']}/{selector['path']}`"
        disclosure = row.get("reason", "—")
        if "transition_exception" in row:
            disclosure = row["transition_exception"]["disclosure"]
        lines.append(
            f"| {row['plugin_id']} | `{row['surface_id']}` | {row['state']} | {selector_text} | {disclosure} |"
        )
    lines.extend(
        [
            "",
            "Catalog publication and verification are distribution facts, not behavioral support claims.",
            "",
            "## Provisioners",
            "",
            "| Route | Surface | Plugin | Version | State | Disclosure |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in sorted(
        provisioners["records"],
        key=lambda item: (item["route_id"], item["surface_id"], item["plugin_id"], item["package_version"]),
    ):
        disclosure = row.get("reason", row.get("disclosure", "—"))
        lines.append(
            f"| `{row['route_id']}` | `{row['surface_id']}` | {row['plugin_id']} | `{row['package_version']}` | {row['state']} | {disclosure} |"
        )
    lines.extend(
        [
            "",
            "Provisioner metadata records exact route availability; this repository does not execute spec 0002 requests in this slice.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def replace_managed_scope(document: bytes, fragment: bytes) -> bytes:
    begin = b"<!-- distribution-scope:begin -->"
    end = b"<!-- distribution-scope:end -->"
    require(begin in document and end in document, "repository-scope managed block is missing")
    prefix, remainder = document.split(begin, 1)
    _, suffix = remainder.split(end, 1)
    return prefix + begin + b"\n" + fragment.rstrip(b"\n") + b"\n" + end + suffix


def derivatives(root: Path) -> dict[str, bytes]:
    catalogs = validate_catalog(load_json(root / "distribution" / "catalogs.json"))
    provisioners = validate_provisioners(load_json(root / "distribution" / "provisioners.json"))
    generated = build_host_catalogs(catalogs)
    generated["distribution/availability.md"] = build_availability(catalogs, provisioners)
    fragment = (root / "distribution" / "repository-scope.md").read_bytes()
    for name in ("README.md", "CLAUDE.md"):
        generated[name] = replace_managed_scope((root / name).read_bytes(), fragment)
    return generated


def generate(root: Path, check: bool) -> None:
    expected = derivatives(root)
    stale = []
    for relative, content in expected.items():
        path = root / relative
        if not path.is_file() or path.read_bytes() != content:
            stale.append(relative)
    if check:
        if stale:
            reject("stale derivatives: " + ", ".join(stale))
        return
    for relative in stale:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(expected[relative])


def validate_catalog_cross_refs(
    catalogs: dict[str, Any],
    baseline: dict[str, Any],
    stock: dict[str, Any],
    adoptions: dict[str, Any],
) -> None:
    baseline_map = {(row["plugin_id"], row["surface_id"]): row for row in baseline["rows"]}
    stock_map = {(row["plugin_id"], row["surface_id"]): row for row in stock["rows"]}
    adoption_map = {row["plugin_id"]: row for row in adoptions["products"]}
    catalog_map = {(row["plugin_id"], row["surface_id"]): row for row in catalogs["records"]}
    for row in catalogs["records"]:
        key = (row["plugin_id"], row["surface_id"])
        if "transition_exception" in row:
            require(key in baseline_map and key in stock_map, f"catalog {key}: transition row absent from baseline/stock")
            exception = row["transition_exception"]
            require(exception["baseline_key"] == {"plugin_id": key[0], "surface_id": key[1]}, f"catalog {key}: transition baseline key mismatch")
            require(exception["selector_fingerprint"] == stock_map[key]["selector_fingerprint"], f"catalog {key}: transition fingerprint mismatch")
        elif row["state"] in {"published", "verified"}:
            adoption = adoption_map.get(row["plugin_id"])
            require(adoption is not None and adoption["state"] == "complete", f"catalog {key}: product adoption is not complete")
    for key in stock_map:
        row = catalog_map.get(key)
        require(
            row is not None
            and row["state"] == "published"
            and "transition_exception" in row,
            f"legacy stock {key}: missing published transition catalog row",
        )


def validate_door(root: Path) -> None:
    registry = validate_surface_registry(load_json(root / "distribution" / "surfaces.json"))
    require(
        {
            (row["surface_id"], row["host"], row["environment"], row["mode"])
            for row in registry["surfaces"]
        }
        == {(key, *dimensions) for key, dimensions in SURFACES.items()},
        "surface_registry: version 1 does not contain the exact six rows",
    )
    require(
        all(row["lifecycle"] == "active" for row in registry["surfaces"]),
        "surface_registry: version 1 rows must be active",
    )
    catalogs = validate_catalog(load_json(root / "distribution" / "catalogs.json"))
    validate_provisioners(load_json(root / "distribution" / "provisioners.json"))
    baseline = validate_baseline(load_json(root / "distribution" / "legacy-baseline.json"))
    discovered = legacy_discover(root, BASELINE_COMMIT)
    require(discovered == baseline, "legacy_baseline: fixed-commit discovery mismatch")
    _, stock = validate_initial_stock(root, baseline)
    adoptions = validate_product_adoptions(load_json(root / "distribution" / "product-adoptions.json"))
    validate_catalog_cross_refs(catalogs, baseline, stock, adoptions)
    host_catalogs = build_host_catalogs(catalogs)
    for row in catalogs["records"]:
        if row["state"] == "absent":
            continue
        expected = host_catalogs[row["manifest_path"]]
        digest = hashlib.sha256(expected).hexdigest()
        require(
            row["publication_evidence"]["manifest_sha256"] == digest,
            f"catalog {(row['plugin_id'], row['surface_id'])}: publication digest does not match generated manifest",
        )
        stable = row["publication_evidence"]["stable_reference"]
        require(stable["repository"] == "kodhama/stewards", "catalog publication reference: expected Stewards repository")
        retained = subprocess.run(
            ["git", "-C", str(root), "show", f"{stable['source_commit']}:{stable['path']}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(retained.returncode == 0, "catalog publication reference: comparison commit is unresolvable")
        require(
            retained.stdout == expected and hashlib.sha256(retained.stdout).hexdigest() == stable["sha256"],
            "catalog publication reference: retained bytes or digest mismatch",
        )
    generate(root, check=True)


DOCUMENT_VALIDATORS: dict[str, Callable[[Any], Any]] = {
    "surface-contract": validate_surface_contract,
    "surface-registry": validate_surface_registry,
    "catalog-availability": validate_catalog,
    "provisioner-availability": validate_provisioners,
    "clean-install-evidence": validate_clean_install_evidence,
    "effective-facts": validate_effective_facts,
    "release-history": validate_release_history,
    "release-inventory": validate_release_inventory,
    "product-adoptions": validate_product_adoptions,
    "legacy-baseline": validate_baseline,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="distribution/manage")
    commands = parser.add_subparsers(dest="command", required=True)

    product = commands.add_parser("validate-product")
    product.add_argument("--phase", required=True, choices=("pre-tag", "release"))
    product.add_argument("--package-root", required=True)
    product.add_argument("--release-metadata", required=True)

    document = commands.add_parser("validate-document", help=argparse.SUPPRESS)
    document.add_argument("--schema", required=True, choices=sorted(DOCUMENT_VALIDATORS))
    document.add_argument("path")

    commands.add_parser("validate-door")

    generation = commands.add_parser("generate")
    generation.add_argument("--check", action="store_true")

    legacy = commands.add_parser("legacy-discover")
    legacy.add_argument("--baseline-commit", required=True)

    commands.add_parser("wave-close")

    effective = commands.add_parser("effective")
    effective.add_argument("--facts", required=True)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = root_from_manage()
    try:
        if args.command == "validate-product":
            result = validate_product(
                Path(args.package_root),
                args.release_metadata,
                args.phase,
            )
            sys.stdout.buffer.write(canonical_json(result, newline=True))
        elif args.command == "validate-document":
            DOCUMENT_VALIDATORS[args.schema](load_json(Path(args.path)))
        elif args.command == "validate-door":
            validate_door(root)
        elif args.command == "generate":
            generate(root, args.check)
        elif args.command == "legacy-discover":
            sys.stdout.buffer.write(
                canonical_json(
                    legacy_discover(root, args.baseline_commit),
                    newline=True,
                )
            )
        elif args.command == "wave-close":
            validate_door(root)
            stock = load_json(root / "distribution" / "legacy-stock.json")
            require(not stock["rows"], "wave-close: distribution/legacy-stock.json still contains transition stock")
        elif args.command == "effective":
            result = evaluate_effective(load_json(Path(args.facts)))
            sys.stdout.buffer.write(canonical_json(result, newline=True))
        return 0
    except (ContractError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
