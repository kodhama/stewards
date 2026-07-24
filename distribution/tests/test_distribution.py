"""Black-box contract tests for the Stewards distribution door."""

from __future__ import annotations

import hashlib
import importlib.machinery
import json
import os
from pathlib import Path
import re
import signal
import shutil
import subprocess
import tempfile
import time
import unittest
from unittest import mock

from distribution.lib import manage as contract


ROOT = Path(__file__).resolve().parents[2]
MANAGE = ROOT / "distribution" / "manage"
BASELINE_COMMIT = "8b9007dd4f4559cf2a83976391c71392a4628730"
SCHEMAS = (
    "common-types.v1.schema.json",
    "release-metadata.v1.schema.json",
    "release-inventory.v1.schema.json",
    "release-history.v1.schema.json",
    "surface-contract.v1.schema.json",
    "surface-registry.v1.schema.json",
    "catalog-availability.v1.schema.json",
    "provisioner-availability.v1.schema.json",
    "clean-install-evidence.v1.schema.json",
    "effective-facts.v1.schema.json",
    "effective-result.v1.schema.json",
    "legacy-baseline.v1.schema.json",
    "legacy-stock-initial.v1.schema.json",
    "legacy-stock.v1.schema.json",
    "product-adoptions.v1.schema.json",
)


def run_manage(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    manage = cwd / "distribution" / "manage"
    return subprocess.run(
        [str(manage), *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n",
        encoding="utf-8",
    )


def stable_ref(path: str, digest_seed: str = "a") -> dict[str, str]:
    return {
        "kind": "repo-path",
        "repository": "kodhama/example",
        "source_commit": digest_seed * 40,
        "path": path,
        "sha256": digest_seed * 64,
    }


def subject() -> dict[str, str]:
    return {
        "plugin_id": "example",
        "package_version": "1.2.3",
        "release_tag": "example-v1.2.3",
        "source_commit": "a" * 40,
        "surface_id": "claude-code.local.interactive",
    }


def evidence_binding() -> dict[str, object]:
    return {
        "evidence_id": "example.install",
        "stable_reference": stable_ref("evidence/install.json"),
        **subject(),
        "observed_at": "2026-07-24T12:00:00Z",
        "observation": "Clean install and load succeeded.",
    }


def supported_surface_row() -> dict[str, object]:
    return {
        "surface_id": "claude-code.local.interactive",
        "host": "claude-code",
        "status": "supported",
        "post_install_setup": {"required": False, "contract": None},
        "evidence": [evidence_binding()],
        "load_path": {"kind": "skill", "locator": "example:setup"},
        "support_record": {
            "record_id": "example.support",
            "stable_reference": stable_ref("support.json"),
            "plugin_id": "example",
            "package_version": "1.2.3",
            "surface_id": "claude-code.local.interactive",
        },
    }


def clean_install_evidence() -> dict[str, object]:
    identity = subject()
    return {
        "schema_version": 1,
        "evidence_id": "example.clean-install",
        "subject": identity,
        "catalog_key": {
            "plugin_id": identity["plugin_id"],
            "surface_id": identity["surface_id"],
        },
        "distribution_binding": {
            "kind": "catalog-selector",
            "selector": {
                "kind": "immutable",
                "repository": "kodhama/example",
                "path": "plugins/example",
                "ref": {"kind": "tag", "value": identity["release_tag"]},
            },
        },
        "clean_environment": {
            "host": "claude-code",
            "host_version": "1.0.0",
            "environment": "local",
            "mode": "interactive",
            "snapshot_kind": "machine-snapshot",
            "snapshot_id": "snapshot-1",
            "sha256": "b" * 64,
        },
        "installation": {
            "started_at": "2026-07-24T12:00:00Z",
            "finished_at": "2026-07-24T12:00:01Z",
            "outcome": "installed",
            "discovered_identity": identity,
            "record_reference": stable_ref("install/record.json", "b"),
        },
        "observations": [evidence_binding()],
    }


def verified_catalog() -> dict[str, object]:
    identity = subject()
    selector = {
        "kind": "immutable",
        "repository": "kodhama/example",
        "path": "plugins/example",
        "ref": {"kind": "tag", "value": identity["release_tag"]},
    }
    return {
        "schema_version": 1,
        "records": [
            {
                "plugin_id": identity["plugin_id"],
                "surface_id": identity["surface_id"],
                "state": "verified",
                "manifest_path": ".claude-plugin/marketplace.json",
                "source_selector": selector,
                "publication_evidence": {
                    "stable_reference": stable_ref(
                        ".claude-plugin/marketplace.json"
                    ),
                    "manifest_path": ".claude-plugin/marketplace.json",
                    "manifest_sha256": "a" * 64,
                    "observed_at": "2026-07-24T12:00:00Z",
                },
                "host_projection": {
                    "host": "claude-code",
                    "entry_name": identity["plugin_id"],
                    "fields": {
                        "description": "Example.",
                        "source": {
                            "source": "git-subdir",
                            "url": "kodhama/example",
                            "path": "plugins/example",
                        },
                    },
                },
                "release_metadata_path": "plugins/example/release.json",
                "surface_contract_path": "plugins/example/surfaces.json",
                "product_contract_version": 1,
                "package_version": identity["package_version"],
                "release_tag": identity["release_tag"],
                "source_commit": identity["source_commit"],
                "identity_binding": {
                    "kind": "catalog-selector",
                    "selector": selector,
                },
                "clean_install_evidence": clean_install_evidence(),
                "release_history_reference": stable_ref(
                    "release-history.json"
                ),
            }
        ],
    }


class DistributionContractTests(unittest.TestCase):
    maxDiff = None

    # spec-0001@v1 S1, S2, R1-R4
    def test_pre_tag_extracts_authority_and_rejects_ambiguous_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            package = Path(raw)
            (package / "VERSION").write_bytes(b"1.2.3\n")
            write_json(package / "plugin.json", {"version": "1.2.3"})
            write_json(
                package / "surfaces.json",
                {
                    "schema_version": 1,
                    "family_contract_version": 1,
                    "version": "1.2.3",
                    "surfaces": [supported_surface_row()],
                },
            )
            write_json(
                package / "release-inventory.json",
                {
                    "schema_version": 1,
                    "host_manifests": [
                        {
                            "host": "claude-code",
                            "path": "plugin.json",
                            "manifest_kind": "claude-plugin",
                            "version_extractor": {
                                "path": "plugin.json",
                                "format": "json",
                                "selector": "/version",
                            },
                            "package_version": "1.2.3",
                        }
                    ],
                    "payload_identities": [],
                    "public_contract_items": [],
                    "support_derivatives": [],
                },
            )
            write_json(package / "release-history.json", {"schema_version": 1, "releases": []})
            provider = package / "inventory"
            provider.write_text(
                "#!/bin/sh\ncat \"$4/release-inventory.json\" 2>/dev/null || "
                "cat \"$(dirname \"$0\")/release-inventory.json\"\n",
                encoding="utf-8",
            )
            provider.chmod(0o755)
            metadata = {
                "schema_version": 1,
                "family_contract_version": 1,
                "plugin_id": "example",
                "version_authority": {"path": "VERSION", "format": "plain-text"},
                "version_carriers": [
                    {
                        "carrier_id": "claude.manifest",
                        "role": "host-manifest",
                        "path": "plugin.json",
                        "format": "json",
                        "selector": "/version",
                    }
                ],
                "surface_contract": "surfaces.json",
                "release_inventory": "release-inventory.json",
                "release_history": "release-history.json",
                "inventory_provider": "inventory",
            }
            write_json(package / "release.json", metadata)

            result = run_manage(
                "validate-product",
                "--phase",
                "pre-tag",
                "--package-root",
                str(package),
                "--release-metadata",
                "release.json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout),
                {"package_version": "1.2.3", "expected_tag": "example-v1.2.3"},
            )

            subprocess.run(["git", "init", "-q"], cwd=package, check=True)
            subprocess.run(
                ["git", "config", "user.name", "Fixture"],
                cwd=package,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "fixture@example.invalid"],
                cwd=package,
                check=True,
            )
            subprocess.run(["git", "add", "."], cwd=package, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", "fixture release"],
                cwd=package,
                check=True,
            )
            subprocess.run(
                ["git", "tag", "example-v1.2.3"],
                cwd=package,
                check=True,
            )
            metadata["release_approval"] = stable_ref("approval.json")
            write_json(package / "release.json", metadata)
            release = run_manage(
                "validate-product",
                "--phase",
                "release",
                "--package-root",
                str(package),
                "--release-metadata",
                "release.json",
            )
            self.assertNotEqual(release.returncode, 0)
            self.assertIn("release engine is not implemented", release.stderr)

            (package / "VERSION").write_bytes(b"\xef\xbb\xbf1.2.3\n")
            rejected = run_manage(
                "validate-product",
                "--phase",
                "pre-tag",
                "--package-root",
                str(package),
                "--release-metadata",
                "release.json",
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("VERSION", rejected.stderr)

    # spec-0001@v1 S3, S4, R5-R8
    def test_surface_contract_requires_typed_supported_proof(self) -> None:
        valid = {
            "schema_version": 1,
            "family_contract_version": 1,
            "version": "1.2.3",
            "surfaces": [supported_surface_row()],
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "surface.json"
            write_json(path, valid)
            accepted = run_manage("validate-document", "--schema", "surface-contract", str(path))
            self.assertEqual(accepted.returncode, 0, accepted.stderr)

            invalid = json.loads(json.dumps(valid))
            invalid["surfaces"][0]["load_path"] = "example:setup"
            write_json(path, invalid)
            rejected = run_manage("validate-document", "--schema", "surface-contract", str(path))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("load_path", rejected.stderr)

    # spec-0001@v1 S5-S7, S13, R9-R11, R25-R26
    def test_selector_and_availability_unions_are_exact(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "catalog.json"
            published = {
                "schema_version": 1,
                "records": [
                    {
                        "plugin_id": "example",
                        "surface_id": "claude-code.local.interactive",
                        "state": "published",
                        "manifest_path": ".claude-plugin/marketplace.json",
                        "source_selector": {
                            "kind": "mutable",
                            "repository": "kodhama/example",
                            "path": "plugins/example",
                        },
                        "publication_evidence": {
                            "stable_reference": stable_ref(".claude-plugin/marketplace.json"),
                            "manifest_path": ".claude-plugin/marketplace.json",
                            "manifest_sha256": "a" * 64,
                            "observed_at": "2026-07-24T12:00:00Z",
                        },
                        "host_projection": {
                            "host": "claude-code",
                            "entry_name": "example",
                            "fields": {
                                "description": "Example.",
                                "source": {
                                    "source": "git-subdir",
                                    "url": "kodhama/example",
                                    "path": "plugins/example",
                                },
                            },
                        },
                        "release_metadata_path": "plugins/example/release.json",
                        "surface_contract_path": "plugins/example/surfaces.json",
                        "product_contract_version": 1,
                    }
                ],
            }
            write_json(path, published)
            accepted = run_manage("validate-document", "--schema", "catalog-availability", str(path))
            self.assertEqual(accepted.returncode, 0, accepted.stderr)

            published["records"][0]["source_selector"]["ref"] = {
                "kind": "tag",
                "value": "example-v1.2.3",
            }
            write_json(path, published)
            rejected = run_manage("validate-document", "--schema", "catalog-availability", str(path))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("source_selector", rejected.stderr)

            provisioner = {
                "schema_version": 1,
                "records": [
                    {
                        "route_id": "claude.local",
                        "surface_id": "claude-code.local.interactive",
                        "plugin_id": "example",
                        "package_version": "1.2.3",
                        "state": "unavailable",
                        "reason": "No adapter has retained proof.",
                    }
                ],
            }
            write_json(path, provisioner)
            ok = run_manage("validate-document", "--schema", "provisioner-availability", str(path))
            self.assertEqual(ok.returncode, 0, ok.stderr)
            del provisioner["records"][0]["package_version"]
            write_json(path, provisioner)
            bad = run_manage("validate-document", "--schema", "provisioner-availability", str(path))
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("package_version", bad.stderr)

    # spec-0001@v1 S8, S14, S15, S20, R12-R14, R23, R27-R28, R37
    def test_effective_support_is_derived_from_typed_facts(self) -> None:
        source_reference = stable_ref("distribution/facts.json")
        facts = {
            "schema_version": 1,
            "subject": subject(),
            "product_contract": {
                "kind": "record",
                "source_reference": stable_ref("surfaces.json"),
                "subject": subject(),
                "row": supported_surface_row(),
            },
            "distribution_record": {
                "kind": "missing",
                "source_reference": stable_ref("distribution/catalogs.json"),
                "record_type": "catalog",
                "lookup_key": {
                    "plugin_id": "example",
                    "surface_id": "claude-code.local.interactive",
                },
            },
            "consumer_selection": {
                "state": "selected",
                "request_id": "request.example",
                "plugin_id": "example",
                "package_version": "1.2.3",
                "surface_id": "claude-code.local.interactive",
                "route_id": "catalog.claude",
                "source_reference": source_reference,
            },
            "environment_assessment": {
                "state": "ready",
                "subject": subject(),
                "evidence": [evidence_binding()],
                "source_reference": source_reference,
            },
            "product_setup": {
                "subject": subject(),
                "state": "not-required",
                "requirement_reference": stable_ref("surfaces.json"),
                "contract": None,
            },
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "facts.json"
            write_json(path, facts)
            result = run_manage("effective", "--facts", str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            body = json.loads(result.stdout)
            self.assertFalse(body["effective"])
            self.assertEqual(len(body["factors"]), 6)
            distribution = next(
                factor
                for factor in body["factors"]
                if factor["factor"] == "distribution_verified"
            )
            self.assertEqual(distribution["reason_codes"], ["distribution-row-missing"])
            self.assertEqual(distribution["owners"], ["stewards"])

            facts["product_supported"] = True
            write_json(path, facts)
            rejected = run_manage("effective", "--facts", str(path))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(rejected.stdout, "")

    # spec-0001@v1 S8, S12, R12, R20; fourth-review cross-surface finding
    def test_product_row_surface_matches_declared_subject(self) -> None:
        row = supported_surface_row()
        row["surface_id"] = "codex.local.interactive"
        row["host"] = "codex"
        for evidence in row["evidence"]:
            evidence["surface_id"] = "codex.local.interactive"
        row["support_record"]["surface_id"] = "codex.local.interactive"
        fact = {
            "kind": "record",
            "source_reference": stable_ref("surfaces.json"),
            "subject": subject(),
            "row": row,
        }
        with self.assertRaisesRegex(
            contract.ContractError,
            "row.surface_id",
        ):
            contract.validate_product_fact(fact)

    # spec-0001@v1 S8, R23; conformance setup-binding counterexamples
    def test_effective_setup_complete_binds_product_requirement(self) -> None:
        product_reference = stable_ref("surfaces.json")
        contract_reference = stable_ref("setup-contract.json", "b")
        row = supported_surface_row()
        facts = {
            "schema_version": 1,
            "subject": subject(),
            "product_contract": {
                "kind": "record",
                "source_reference": product_reference,
                "subject": subject(),
                "row": row,
            },
            "distribution_record": {
                "kind": "record",
                "source_reference": stable_ref("distribution/catalogs.json"),
                "record_type": "catalog",
                "record": verified_catalog()["records"][0],
            },
            "consumer_selection": {
                "state": "selected",
                "request_id": "request.example",
                "plugin_id": "example",
                "package_version": "1.2.3",
                "surface_id": "claude-code.local.interactive",
                "route_id": "catalog.claude",
                "source_reference": stable_ref("selection.json"),
            },
            "environment_assessment": {
                "state": "ready",
                "subject": subject(),
                "evidence": [evidence_binding()],
                "source_reference": stable_ref("environment.json"),
            },
            "product_setup": {
                "subject": subject(),
                "state": "complete",
                "requirement_reference": stable_ref("unrelated-row.json"),
                "contract": contract_reference,
                "completion_reference": stable_ref("setup-completion.json"),
                "completion_identity": subject(),
            },
        }
        with self.assertRaisesRegex(
            contract.ContractError,
            "product_setup",
        ):
            contract.evaluate_effective(facts)

        row["post_install_setup"] = {
            "required": True,
            "contract": contract_reference,
        }
        facts["product_setup"]["requirement_reference"] = product_reference
        result = contract.evaluate_effective(facts)
        setup_factor = next(
            item
            for item in result["factors"]
            if item["factor"] == "product_setup_complete"
        )
        self.assertTrue(setup_factor["satisfied"])

    # spec-0001@v1 S9, R15-R16, R24
    def test_legacy_discovery_reads_the_fixed_commit_and_matches_three_keys(self) -> None:
        result = run_manage("legacy-discover", "--baseline-commit", BASELINE_COMMIT)
        self.assertEqual(result.returncode, 0, result.stderr)
        discovered = json.loads(result.stdout)
        self.assertEqual(
            [(row["plugin_id"], row["surface_id"]) for row in discovered["rows"]],
            [
                ("grove", "claude-code.local.interactive"),
                ("trellis", "claude-code.local.interactive"),
                ("grove", "codex.local.interactive"),
            ],
        )
        for row in discovered["rows"]:
            self.assertRegex(row["selector_fingerprint"], r"^[0-9a-f]{64}$")

    # spec-0001@v1 S10, S11, S18, S19, S23, R17-R19, R33-R36, R40
    def test_door_validates_derivatives_and_stock_is_not_wave_closed(self) -> None:
        validated = run_manage("validate-door")
        self.assertEqual(validated.returncode, 0, validated.stderr)

        checked = run_manage("generate", "--check")
        self.assertEqual(checked.returncode, 0, checked.stderr)

        wave = run_manage("wave-close")
        self.assertNotEqual(wave.returncode, 0)
        self.assertIn("legacy-stock.json", wave.stderr)

    # spec-0001@v1 S19, R35; conformance adoption-resolution counterexamples
    def test_complete_adoption_requires_resolved_approved_decision(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repository = Path(raw) / "product"
            repository.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
            subprocess.run(
                ["git", "config", "user.name", "Fixture"],
                cwd=repository,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "fixture@example.invalid"],
                cwd=repository,
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    "https://github.com/kodhama/example.git",
                ],
                cwd=repository,
                check=True,
            )
            decision = repository / "decisions" / "0001-adopt.md"
            decision.parent.mkdir()
            decision.write_text(
                "---\n"
                "id: example-0001-adopt\n"
                "type: decision\n"
                "status: approved\n"
                "depends_on: []\n"
                "owner: agent\n"
                "---\n\n"
                "# Adopt\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", "adopt"],
                cwd=repository,
                check=True,
            )
            source_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repository,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout.strip()
            document = {
                "schema_version": 1,
                "products": [
                    {
                        "plugin_id": "example",
                        "repository": "kodhama/example",
                        "state": "complete",
                        "standing_decisions_to_reconcile": [],
                        "ownership_changes": ["release contract adopted"],
                        "adoption_decision": {
                            "kind": "repo-path",
                            "repository": "kodhama/example",
                            "source_commit": source_commit,
                            "path": "decisions/0001-adopt.md",
                            "sha256": hashlib.sha256(
                                decision.read_bytes()
                            ).hexdigest(),
                        },
                    }
                ],
            }
            with self.assertRaisesRegex(
                contract.ContractError,
                "resolver",
            ):
                contract.validate_product_adoptions(document)
            contract.validate_product_adoptions(
                document,
                {"kodhama/example": repository},
            )
            document_path = Path(raw) / "product-adoptions.json"
            write_json(document_path, document)
            resolved = subprocess.run(
                [
                    str(ROOT / "distribution" / "manage"),
                    "validate-document",
                    "--schema",
                    "product-adoptions",
                    str(document_path),
                ],
                cwd=ROOT,
                env={
                    **os.environ,
                    "STEWARDS_PRODUCT_REPOSITORIES": json.dumps(
                        {"kodhama/example": str(repository)}
                    ),
                },
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(resolved.returncode, 0, resolved.stderr)
            non_commit = json.loads(json.dumps(document))
            non_commit["products"][0]["adoption_decision"][
                "source_commit"
            ] = subprocess.run(
                ["git", "rev-parse", "HEAD^{tree}"],
                cwd=repository,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout.strip()
            with self.assertRaisesRegex(
                contract.ContractError,
                "not a commit",
            ):
                contract.validate_product_adoptions(
                    non_commit,
                    {"kodhama/example": repository},
                )
            fabricated = json.loads(json.dumps(document))
            fabricated["products"][0]["adoption_decision"]["sha256"] = "f" * 64
            with self.assertRaisesRegex(
                contract.ContractError,
                "digest",
            ):
                contract.validate_product_adoptions(
                    fabricated,
                    {"kodhama/example": repository},
                )
            decision.write_text(
                decision.read_text(encoding="utf-8").replace(
                    "status: approved",
                    "status: draft",
                ),
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", "draft replacement"],
                cwd=repository,
                check=True,
            )
            draft = json.loads(json.dumps(document))
            draft_reference = draft["products"][0]["adoption_decision"]
            draft_reference["source_commit"] = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repository,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout.strip()
            draft_reference["sha256"] = hashlib.sha256(
                decision.read_bytes()
            ).hexdigest()
            with self.assertRaisesRegex(
                contract.ContractError,
                "not approved",
            ):
                contract.validate_product_adoptions(
                    draft,
                    {"kodhama/example": repository},
                )

    # spec-0001@v1 S11, R18-R19
    def test_generate_check_names_all_stale_derivatives_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            clone = Path(raw) / "repo"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            stale_paths = [
                clone / ".claude-plugin" / "marketplace.json",
                clone / ".agents" / "plugins" / "marketplace.json",
                clone / "distribution" / "availability.md",
                clone / "README.md",
                clone / "CLAUDE.md",
            ]
            for path in stale_paths:
                current = path.read_text(encoding="utf-8")
                if path.name in {"README.md", "CLAUDE.md"}:
                    current = current.replace(
                        "The install door includes",
                        "STALE: The install door includes",
                        1,
                    )
                else:
                    current += "stale\n"
                path.write_text(current, encoding="utf-8")
            before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in stale_paths}

            checked = run_manage("generate", "--check", cwd=clone)
            self.assertNotEqual(checked.returncode, 0)
            for path in stale_paths:
                self.assertIn(str(path.relative_to(clone)), checked.stderr)
            after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in stale_paths}
            self.assertEqual(after, before)

    # spec-0001@v1 authority table and fixture manifest
    def test_all_versioned_schemas_and_named_fixtures_exist(self) -> None:
        for schema in SCHEMAS:
            path = ROOT / "distribution" / "schemas" / schema
            self.assertTrue(path.is_file(), schema)
            body = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(body["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertFalse(body.get("additionalProperties", True), schema)

        manifest = json.loads(
            (ROOT / "distribution" / "fixtures" / "metadata" / "manifest.json").read_text(
                encoding="utf-8"
            )
        )
        fixture_tests = [fixture["test"] for fixture in manifest["fixtures"]]
        self.assertEqual(len(fixture_tests), len(set(fixture_tests)))
        for test_name in fixture_tests:
            self.assertTrue(callable(getattr(self, test_name, None)), test_name)
        suite_tests = {
            name
            for name in dir(self)
            if name.startswith("test_") and callable(getattr(self, name))
        }
        self.assertEqual(set(fixture_tests), suite_tests)

    # spec-0001@v1 S5, S12, R10, R20; code-review identity-binding finding
    def test_verified_catalog_binds_row_binding_and_clean_subject(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "catalog.json"
            document = verified_catalog()
            write_json(path, document)
            accepted = run_manage(
                "validate-document", "--schema", "catalog-availability", str(path)
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)

            wrong_subject = json.loads(json.dumps(document))
            clean = wrong_subject["records"][0]["clean_install_evidence"]
            other = dict(clean["subject"])
            other["plugin_id"] = "other"
            other["release_tag"] = "other-v1.2.3"
            clean["subject"] = other
            clean["catalog_key"]["plugin_id"] = "other"
            clean["installation"]["discovered_identity"] = other
            clean["distribution_binding"]["selector"]["repository"] = (
                "kodhama/other"
            )
            clean["distribution_binding"]["selector"]["ref"]["value"] = (
                "other-v1.2.3"
            )
            for observation in clean["observations"]:
                observation["plugin_id"] = "other"
                observation["release_tag"] = "other-v1.2.3"
            write_json(path, wrong_subject)
            rejected = run_manage(
                "validate-document", "--schema", "catalog-availability", str(path)
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("clean_install_evidence", rejected.stderr)

            wrong_binding = json.loads(json.dumps(document))
            binding_ref = wrong_binding["records"][0]["identity_binding"]["selector"][
                "ref"
            ]
            binding_ref["value"] = "other-v1.2.3"
            write_json(path, wrong_binding)
            rejected = run_manage(
                "validate-document", "--schema", "catalog-availability", str(path)
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("identity_binding", rejected.stderr)

    # spec-0001@v1 S5, R10; conformance provisioner-binding counterexamples
    def test_verified_acquisition_requires_matching_provisioner(self) -> None:
        catalogs = verified_catalog()
        row = catalogs["records"][0]
        bundle = stable_ref("evidence/provisioner.json", "b")
        identity = {
            "route_id": "claude.local",
            "surface_id": row["surface_id"],
            "plugin_id": row["plugin_id"],
            "package_version": row["package_version"],
            "provisioner_version": "2.0.0",
            "release_tag": row["release_tag"],
            "source_commit": row["source_commit"],
        }
        binding = {
            "kind": "provisioner-acquisition",
            "provisioner_identity": identity,
            "evidence_bundle": bundle,
        }
        row["identity_binding"] = binding
        row["clean_install_evidence"]["distribution_binding"] = binding
        contract.validate_catalog(catalogs)
        with self.assertRaisesRegex(
            contract.ContractError,
            "verified provisioner",
        ):
            contract.validate_catalog_provisioner_bindings(
                catalogs,
                {"schema_version": 1, "records": []},
            )

        provisioners = {
            "schema_version": 1,
            "records": [
                {
                    **identity,
                    "state": "verified",
                    "adapter_path": "distribution/adapters/claude",
                    "prerequisites": [],
                    "evidence_bundle": bundle,
                }
            ],
        }
        contract.validate_provisioners(provisioners)
        contract.validate_catalog_provisioner_bindings(catalogs, provisioners)
        provisioners["records"][0]["evidence_bundle"] = stable_ref(
            "evidence/other.json",
            "c",
        )
        with self.assertRaisesRegex(
            contract.ContractError,
            "verified provisioner",
        ):
            contract.validate_catalog_provisioner_bindings(
                catalogs,
                provisioners,
            )

    # spec-0001@v1 R21; conformance unresolved-extension counterexamples
    def test_declared_extension_validators_fail_closed(self) -> None:
        metadata = {
            "schema_version": 1,
            "family_contract_version": 1,
            "plugin_id": "example",
            "version_authority": {
                "path": "VERSION",
                "format": "plain-text",
            },
            "version_carriers": [
                {
                    "carrier_id": "package.version",
                    "role": "package-manifest",
                    "path": "VERSION",
                    "format": "plain-text",
                }
            ],
            "surface_contract": "surfaces.json",
            "release_inventory": "release-inventory.json",
            "release_history": "release-history.json",
            "inventory_provider": "inventory",
            "extensions": {
                "example": {
                    "validator": "validate-extension",
                }
            },
        }
        with self.assertRaisesRegex(
            contract.ContractError,
            "extension validator protocol is not implemented",
        ):
            contract.validate_release_metadata(metadata, "pre-tag")

        inventory = {
            "schema_version": 1,
            "host_manifests": [
                {
                    "host": "example-host",
                    "path": "manifest.json",
                    "manifest_kind": "other-declared-host",
                    "extension_validator": "validate-host",
                    "version_extractor": {
                        "path": "manifest.json",
                        "format": "json",
                        "selector": "/version",
                    },
                    "package_version": "1.2.3",
                }
            ],
            "payload_identities": [],
            "public_contract_items": [],
            "support_derivatives": [],
        }
        with self.assertRaisesRegex(
            contract.ContractError,
            "extension validator protocol is not implemented",
        ):
            contract.validate_release_inventory(inventory)

    # spec-0001@v1 S13, R25; code-review baseline-key schema finding
    def test_transition_baseline_key_schema_is_closed_without_ref_composition(self) -> None:
        schema = json.loads(
            (
                ROOT
                / "distribution"
                / "schemas"
                / "catalog-availability.v1.schema.json"
            ).read_text(encoding="utf-8")
        )
        baseline_key = schema["$defs"]["transition_exception"]["properties"][
            "baseline_key"
        ]
        self.assertEqual(
            baseline_key["required"], ["plugin_id", "surface_id"]
        )
        self.assertEqual(
            set(baseline_key["properties"]), {"plugin_id", "surface_id"}
        )
        self.assertFalse(baseline_key["additionalProperties"])
        self.assertNotIn("allOf", baseline_key)

    # spec-0001@v1 S18, R34; code-review deterministic-type finding
    def test_mixed_transition_elements_fail_without_traceback(self) -> None:
        document = verified_catalog()
        row = document["records"][0]
        row["state"] = "published"
        for key in (
            "release_metadata_path",
            "surface_contract_path",
            "product_contract_version",
            "package_version",
            "release_tag",
            "source_commit",
            "identity_binding",
            "clean_install_evidence",
            "release_history_reference",
        ):
            row.pop(key)
        row["transition_exception"] = {
            "baseline_key": {
                "plugin_id": "example",
                "surface_id": "claude-code.local.interactive",
            },
            "selector_fingerprint": "a" * 64,
            "missing_contract_elements": ["release-tag", 7],
            "disclosure": "legacy published stock",
            "terminal_action": "adopt-or-delist",
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "catalog.json"
            write_json(path, document)
            result = run_manage(
                "validate-document", "--schema", "catalog-availability", str(path)
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing_contract_elements", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    # spec-0001@v1 complete-inventory provider; code-review resource-bound finding
    def test_inventory_provider_timeout_and_output_bounds_are_contract_failures(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output_provider = root / "output-provider"
            output_provider.write_text(
                "#!/usr/bin/env python3\n"
                "import sys\n"
                "sys.stdout.write('x' * 128)\n",
                encoding="utf-8",
            )
            output_provider.chmod(0o755)
            with mock.patch.object(contract, "PROVIDER_OUTPUT_LIMIT", 64):
                with self.assertRaisesRegex(contract.ContractError, "stdout"):
                    contract.run_inventory_provider(root, "output-provider")

            timeout_provider = root / "timeout-provider"
            timeout_provider.write_text(
                "#!/bin/sh\nsleep 1\n",
                encoding="utf-8",
            )
            timeout_provider.chmod(0o755)
            with mock.patch.object(contract, "PROVIDER_TIMEOUT_SECONDS", 0.05):
                with self.assertRaisesRegex(contract.ContractError, "timed out"):
                    contract.run_inventory_provider(root, "timeout-provider")

    # spec-0001@v1 S9, R15; code-review host ambiguity finding
    def test_host_projection_rejects_duplicate_plugin_entries(self) -> None:
        manifest = {
            "plugins": [
                {
                    "name": "grove",
                    "source": {
                        "source": "git-subdir",
                        "url": "kodhama/grove",
                        "path": "plugins/grove",
                    },
                },
                {
                    "name": "grove",
                    "source": {
                        "source": "git-subdir",
                        "url": "kodhama/grove",
                        "path": "plugins/grove",
                    },
                },
            ]
        }
        with self.assertRaisesRegex(contract.ContractError, "duplicate"):
            contract.host_entries_from_manifest(
                ".claude-plugin/marketplace.json", manifest
            )
        duplicate_projection = {
            "records": [
                {
                    "state": "published",
                    "plugin_id": "grove",
                    "surface_id": "claude-code.local.interactive",
                    "host_projection": {
                        "host": "claude-code",
                        "entry_name": "grove",
                        "fields": {},
                    },
                },
                {
                    "state": "published",
                    "plugin_id": "grove",
                    "surface_id": "claude-code.ci.headless",
                    "host_projection": {
                        "host": "claude-code",
                        "entry_name": "grove",
                        "fields": {},
                    },
                },
            ]
        }
        with self.assertRaisesRegex(contract.ContractError, "duplicate"):
            contract.build_host_catalogs(duplicate_projection)

    # spec-0001@v1 common timestamp grammar; code-review calendar finding
    def test_timestamp_rejects_impossible_calendar_date(self) -> None:
        row = supported_surface_row()
        row["evidence"][0]["observed_at"] = "2026-02-30T12:00:00Z"
        document = {
            "schema_version": 1,
            "family_contract_version": 1,
            "version": "1.2.3",
            "surfaces": [row],
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "surface.json"
            write_json(path, document)
            result = run_manage(
                "validate-document", "--schema", "surface-contract", str(path)
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("timestamp", result.stderr)

    # spec-0001@v1 S22, R39; code-review partial-validator finding
    def test_release_inventory_rejects_rows_missing_schema_fields(self) -> None:
        valid = {
            "schema_version": 1,
            "host_manifests": [
                {
                    "host": "claude-code",
                    "path": "plugin.json",
                    "manifest_kind": "claude-plugin",
                    "version_extractor": {
                        "path": "plugin.json",
                        "format": "json",
                        "selector": "/version",
                    },
                    "package_version": "1.2.3",
                }
            ],
            "payload_identities": [
                {
                    "payload_id": "payload.one",
                    "source_path": "payload.txt",
                    "extractor": {
                        "kind": "file-bytes",
                        "path": "payload.txt",
                    },
                    "kind": "content-hash",
                    "value": "sha256:" + "a" * 64,
                    "consumer_acted": True,
                }
            ],
            "public_contract_items": [
                {
                    "contract_id": "contract.one",
                    "category": "consumed-output-protocol",
                    "source": stable_ref("contract.txt"),
                    "extractor": {
                        "kind": "file-bytes",
                        "path": "contract.txt",
                    },
                    "fingerprint": "a" * 64,
                    "compatibility": "initial",
                }
            ],
            "support_derivatives": [
                {
                    "derivative_id": "support.one",
                    "kind": "public-support-table",
                    "path": "support.json",
                    "extractor": {
                        "kind": "file-bytes",
                        "path": "support.json",
                    },
                    "surface_projection": [],
                }
            ],
        }
        inventory = {
            "schema_version": 1,
            "host_manifests": [],
            "payload_identities": [{"payload_id": "payload.one"}],
            "public_contract_items": [{"contract_id": "contract.one"}],
            "support_derivatives": [{"derivative_id": "support.one"}],
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "inventory.json"
            write_json(path, valid)
            accepted = run_manage(
                "validate-document", "--schema", "release-inventory", str(path)
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)

            write_json(path, inventory)
            result = run_manage(
                "validate-document", "--schema", "release-inventory", str(path)
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("payload_identities", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    # spec-0001@v1 validation/generation interface; code-review gate finding
    def test_repository_quality_gate_runs_all_checks(self) -> None:
        if os.environ.get("STEWARDS_CHECK_INNER") == "1":
            return
        gate = ROOT / "distribution" / "check"
        self.assertTrue(gate.is_file())
        workflow = ROOT / ".github" / "workflows" / "distribution-check.yml"
        self.assertTrue(workflow.is_file())
        self.assertIn(
            "distribution/check",
            workflow.read_text(encoding="utf-8"),
        )
        result = subprocess.run(
            [str(gate)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    # spec-0001@v1 validation/generation interface; second-review portability/range finding
    def test_quality_gate_uses_portable_cache_and_committed_ci_range(self) -> None:
        gate = ROOT / "distribution" / "check"
        source = gate.read_text(encoding="utf-8")
        self.assertNotIn("/private/tmp", source)
        module = importlib.machinery.SourceFileLoader(
            "distribution_quality_gate",
            str(gate),
        ).load_module()
        self.assertEqual(
            module.diff_check_commands("a" * 40),
            [
                ["git", "diff", "--check"],
                ["git", "diff", "--cached", "--check"],
                ["git", "diff", "--check", "a" * 40 + "..HEAD"],
            ],
        )
        workflow = (
            ROOT / ".github" / "workflows" / "distribution-check.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("STEWARDS_BASE_SHA", workflow)
        self.assertIn("github.event.pull_request.base.sha", workflow)
        self.assertIn("github.event.before", workflow)
        self.assertIn("STEWARDS_PRODUCT_REPOSITORIES", workflow)
        self.assertIn(
            "db650fe5855a197eb65375b50e3e81b1065ebddb",
            workflow,
        )
        self.assertIn(
            "4062120cea71737bd28cb171785a2dcdd6192deb",
            workflow,
        )
        instructions = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("STEWARDS_PRODUCT_REPOSITORIES", instructions)
        self.assertIn(
            "db650fe5855a197eb65375b50e3e81b1065ebddb",
            instructions,
        )
        self.assertIn(
            "4062120cea71737bd28cb171785a2dcdd6192deb",
            instructions,
        )
        self.assertIn("fails closed", instructions)

    # spec-0001@v1 complete-inventory provider; third-review escaped-session finding
    def test_provider_capture_returns_with_setsid_descendant(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            child = root / "escaped-child.py"
            child.write_text(
                "import os\n"
                "from pathlib import Path\n"
                "import time\n"
                "os.setsid()\n"
                "Path('escaped.pid').write_text(str(os.getpid()), encoding='utf-8')\n"
                "time.sleep(5)\n",
                encoding="utf-8",
            )
            provider = root / "escape-provider"
            provider.write_text(
                "#!/bin/sh\n"
                "python3 escaped-child.py &\n"
                "while [ ! -s escaped.pid ]; do sleep 0.01; done\n"
                "exit 0\n",
                encoding="utf-8",
            )
            provider.chmod(0o755)
            started = time.monotonic()
            escaped_pid = None
            try:
                result = contract.run_bounded_process(
                    [str(provider)],
                    cwd=root,
                    env={"PATH": os.environ.get("PATH", "")},
                )
                elapsed = time.monotonic() - started
                escaped_pid = int(
                    (root / "escaped.pid").read_text(encoding="utf-8")
                )
                self.assertEqual(result.returncode, 0)
                self.assertLess(elapsed, 1.0)
            finally:
                if escaped_pid is None and (root / "escaped.pid").is_file():
                    escaped_pid = int(
                        (root / "escaped.pid").read_text(encoding="utf-8")
                    )
                if escaped_pid is not None:
                    try:
                        os.kill(escaped_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    # spec-0001@v1 S22, R39; third-review enum type finding
    def test_enum_and_set_membership_types_fail_deterministically(
        self,
    ) -> None:
        base_inventory = {
            "schema_version": 1,
            "host_manifests": [
                {
                    "host": "claude-code",
                    "path": "plugin.json",
                    "manifest_kind": "claude-plugin",
                    "version_extractor": {
                        "path": "plugin.json",
                        "format": "json",
                        "selector": "/version",
                    },
                    "package_version": "1.2.3",
                }
            ],
            "payload_identities": [
                {
                    "payload_id": "payload.one",
                    "source_path": "payload.txt",
                    "extractor": {
                        "kind": "file-bytes",
                        "path": "payload.txt",
                    },
                    "kind": "content-hash",
                    "value": "sha256:" + "a" * 64,
                    "consumer_acted": True,
                }
            ],
            "public_contract_items": [],
            "support_derivatives": [],
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "inventory.json"
            malformed = (
                ("manifest_kind", ("host_manifests", 0, "manifest_kind")),
                ("payload kind", ("payload_identities", 0, "kind")),
            )
            for label, (collection, index, field) in malformed:
                with self.subTest(label=label):
                    inventory = json.loads(json.dumps(base_inventory))
                    inventory[collection][index][field] = {"not": "hashable"}
                    write_json(path, inventory)
                    result = run_manage(
                        "validate-document",
                        "--schema",
                        "release-inventory",
                        str(path),
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(field, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
        invalid_fact = {
            "kind": "invalid",
            "source_reference": stable_ref("facts/product.json"),
            "lookup": subject(),
            "errors": [{"not": "hashable"}],
        }
        with self.assertRaisesRegex(
            contract.ContractError,
            "errors: invalid",
        ):
            contract.validate_product_fact(invalid_fact)

    # spec-0001@v1 clean-install evidence; second-review interval finding
    def test_clean_install_finished_at_precedes_started_at_is_rejected(
        self,
    ) -> None:
        evidence = clean_install_evidence()
        evidence["installation"]["started_at"] = "2026-07-24T12:00:02Z"
        evidence["installation"]["finished_at"] = "2026-07-24T12:00:01Z"
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "evidence.json"
            write_json(path, evidence)
            result = run_manage(
                "validate-document",
                "--schema",
                "clean-install-evidence",
                str(path),
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("finished_at", result.stderr)

    # spec-0001@v1 S11, R18; second-review catalog projection ambiguity finding
    def test_catalog_validator_rejects_duplicate_per_host_projection(
        self,
    ) -> None:
        base = verified_catalog()["records"][0]
        for key in (
            "package_version",
            "release_tag",
            "source_commit",
            "identity_binding",
            "clean_install_evidence",
            "release_history_reference",
        ):
            base.pop(key)
        base["state"] = "published"
        local = json.loads(json.dumps(base))
        ci = json.loads(json.dumps(base))
        ci["surface_id"] = "claude-code.ci.headless"
        document = {"schema_version": 1, "records": [ci, local]}
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "catalog.json"
            write_json(path, document)
            result = run_manage(
                "validate-document",
                "--schema",
                "catalog-availability",
                str(path),
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate", result.stderr)

    # spec-0001@v1 version/inventory extractor grammar; second-review pointer finding
    def test_json_pointer_schemas_allow_nested_segments_like_runtime(self) -> None:
        common = json.loads(
            (
                ROOT / "distribution" / "schemas" / "common-types.v1.schema.json"
            ).read_text(encoding="utf-8")
        )
        version_pattern = common["$defs"]["version_extractor"]["oneOf"][1][
            "properties"
        ]["selector"]["pattern"]
        inventory = json.loads(
            (
                ROOT
                / "distribution"
                / "schemas"
                / "release-inventory.v1.schema.json"
            ).read_text(encoding="utf-8")
        )
        pointer_pattern = inventory["$defs"]["extractor"]["oneOf"][2][
            "properties"
        ]["pointer"]["pattern"]
        for pattern in (version_pattern, pointer_pattern):
            self.assertIsNotNone(re.fullmatch(pattern, ""))
            self.assertIsNotNone(re.fullmatch(pattern, "/version/nested~1key"))
            self.assertIsNone(re.fullmatch(pattern, "/invalid~2escape"))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "version.json").write_text('"1.2.3"\n', encoding="utf-8")
            actual = contract.extract_version(
                root,
                {
                    "path": "version.json",
                    "format": "json",
                    "selector": "",
                },
                "root-version",
            )
        self.assertEqual(actual, "1.2.3")

    # spec-0001@v1 repository quality; second-review Python lint finding
    def test_python_lint_gate_is_real_and_rejects_bad_source(self) -> None:
        lint = ROOT / "distribution" / "python-lint"
        self.assertTrue(lint.is_file())
        check_source = (ROOT / "distribution" / "check").read_text(
            encoding="utf-8"
        )
        self.assertIn("distribution/python-lint", check_source)
        instructions = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertNotIn("Python compilation/typecheck", instructions)
        self.assertIn("annotation coverage", instructions)
        status = (
            ROOT / "distribution" / "IMPLEMENTATION-STATUS.md"
        ).read_text(encoding="utf-8")
        self.assertIn("annotation coverage", status)
        self.assertIn("release phase fails closed", status)
        self.assertNotIn("release-phase peeling", status)
        with tempfile.TemporaryDirectory() as raw:
            bad = Path(raw) / "bad.py"
            bad.write_text("from os import *  \n", encoding="utf-8")
            result = subprocess.run(
                [str(lint), str(bad)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
