"""Black-box contract tests for the Stewards distribution door."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


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
        names = {fixture["name"] for fixture in manifest["fixtures"]}
        self.assertIn("positive/plain-authority-json-carriers", names)
        self.assertIn("positive/complete-release-inventory", names)
        self.assertIn("negative/legacy-stock-initial-drift", names)
        self.assertIn("negative/stale-derived", names)


if __name__ == "__main__":
    unittest.main()
