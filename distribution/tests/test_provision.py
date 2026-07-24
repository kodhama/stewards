"""Black-box tests for the bounded pre-agent provisioner."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROVISION = ROOT / "distribution" / "provision"
PROVISIONER_VERSION = "0.1.0"
SCHEMAS = (
    "provision-request.v1.schema.json",
    "provision-receipt.v1.schema.json",
    "provision-evidence-bundle.v1.schema.json",
    "provision-state.v1.schema.json",
    "provision-write-events.v1.schema.json",
    "provision-entrypoints.v1.schema.json",
)


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n",
        encoding="utf-8",
    )


def request_for(host: str, state_root: Path) -> dict[str, object]:
    surface = f"{host}.local.interactive"
    return {
        "schema_version": 1,
        "request_id": "123e4567-e89b-42d3-a456-426614174000",
        "provisioner_version": PROVISIONER_VERSION,
        "targets": [
            {
                "host": host,
                "surface_id": surface,
                "environment_ref_ids": [],
                "plugins": [
                    {
                        "plugin_id": "grove",
                        "package_version": "1.2.3",
                        "route_id": f"{host}.local",
                    }
                ],
            }
        ],
        "environment": {
            "state_roots": [{"host": host, "path": str(state_root)}],
            "references": [],
        },
    }


def run_provision(
    executable: Path,
    request: Path,
    receipt: Path,
    audit: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(executable),
            "--request",
            str(request),
            "--receipt",
            str(receipt),
            "--write-events",
            str(audit),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class ProvisionContractTests(unittest.TestCase):
    maxDiff = None

    # spec-0002@v1 authority paths, R7, R27, R31, R34-R40
    def test_six_provisioner_schema_authorities_are_closed_v1_documents(self) -> None:
        self.assertEqual(
            (ROOT / "distribution" / "PROVISIONER_VERSION")
            .read_text(encoding="utf-8")
            .strip(),
            PROVISIONER_VERSION,
        )
        for name in SCHEMAS:
            with self.subTest(name=name):
                path = ROOT / "distribution" / "schemas" / name
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(
                    schema["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )
                self.assertTrue(schema["$id"].endswith(f"/{name}"))
                self.assertEqual(schema["type"], "object")
                self.assertFalse(schema["additionalProperties"])
        fixture_root = ROOT / "distribution" / "fixtures" / "provisioner"
        fixture_manifest = json.loads(
            (fixture_root / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(fixture_manifest["schema_version"], 1)
        self.assertEqual(
            sorted(row["expected_exit"] for row in fixture_manifest["fixtures"]),
            [2, 2, 3, 3],
        )
        for row in fixture_manifest["fixtures"]:
            self.assertTrue((fixture_root / row["path"]).is_file())
        evidence_index = json.loads(
            (
                ROOT
                / "distribution"
                / "evidence"
                / "provisioner"
                / "index.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(evidence_index, {"schema_version": 1, "bundles": []})

    # spec-0002@v1 S1, S2, S6, S16, S30, R1, R7-R9, R16, R26, R43
    def test_empty_availability_fails_closed_for_both_hosts(self) -> None:
        availability = json.loads(
            (ROOT / "distribution" / "provisioners.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(availability, {"schema_version": 1, "records": []})
        for host in ("claude-code", "codex"):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as raw:
                temp = Path(raw).resolve()
                state_root = temp / "state"
                state_root.mkdir()
                request = temp / "request.json"
                receipt = temp / "receipt.json"
                audit = temp / "audit.json"
                write_json(request, request_for(host, state_root))

                result = run_provision(PROVISION, request, receipt, audit)

                self.assertEqual(result.returncode, 3, result.stderr)
                self.assertEqual(list(state_root.iterdir()), [])
                receipt_value = json.loads(receipt.read_text(encoding="utf-8"))
                self.assertEqual(receipt_value["overall_outcome"], "failed")
                self.assertEqual(receipt_value["exit_code"], 3)
                self.assertEqual(receipt_value["diagnostics"], [])
                self.assertEqual(len(receipt_value["results"]), 1)
                tuple_result = receipt_value["results"][0]
                self.assertEqual(tuple_result["result_id"], "t0.p0")
                self.assertEqual(tuple_result["phase"], "identity-resolution")
                self.assertEqual(tuple_result["outcome"], "failed")
                self.assertEqual(
                    tuple_result["diagnostic"]["code"], "route-not-found"
                )
                for forbidden in (
                    "resolved_identity",
                    "acquisition_route",
                    "host_adapter",
                    "prior_state",
                    "final_state",
                    "shared_catalog_changes",
                    "verification",
                    "blocked_by",
                ):
                    self.assertNotIn(forbidden, tuple_result)
                audit_raw = audit.read_bytes()
                self.assertEqual(
                    receipt_value["write_events_reference"], str(audit)
                )
                self.assertEqual(
                    receipt_value["write_events_sha256"],
                    hashlib.sha256(audit_raw).hexdigest(),
                )
                audit_value = json.loads(audit_raw)
                self.assertEqual(audit_value["events"], [])
                self.assertEqual(audit_value["tuple_allowed_write_sets"], [])
                self.assertEqual(
                    audit_value["exempt_output_paths"],
                    sorted([str(receipt), str(audit)]),
                )

    # spec-0002@v1 S5, S8, S17, S21, R2-R4, R29, R32
    def test_request_validation_precedes_route_lookup_and_preserves_state(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request_value = request_for("claude-code", state_root)
            request_value["targets"][0]["plugins"][0]["package_version"] = "latest"
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_value)

            result = run_provision(PROVISION, request, receipt, audit)

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(list(state_root.iterdir()), [])
            value = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(value["overall_outcome"], "invalid-request")
            self.assertEqual(value["results"][0]["phase"], "request-validation")
            self.assertEqual(value["results"][0]["outcome"], "failed")
            self.assertEqual(
                value["results"][0]["diagnostic"]["code"], "invalid-request"
            )
            self.assertNotIn("acquisition_route", value["results"][0])

    # spec-0002@v1 S30, R32, R43
    def test_unused_reference_exit_two_overrides_missing_route_exit_three(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request_value = request_for("codex", state_root)
            request_value["environment"]["references"] = [
                {
                    "reference_id": "unused.runtime",
                    "kind": "runtime-command",
                    "locator": "/usr/bin/env",
                }
            ]
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_value)

            result = run_provision(PROVISION, request, receipt, audit)

            self.assertEqual(result.returncode, 2, result.stderr)
            value = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(value["overall_outcome"], "invalid-request")
            self.assertEqual(
                value["results"][0]["diagnostic"]["code"], "route-not-found"
            )
            self.assertEqual(
                value["diagnostics"][0]["code"], "unused-reference"
            )

    # spec-0002@v1 S3, S4, S12, R16-R18
    def test_ci_and_container_adapters_are_thin_core_delegates(self) -> None:
        adapters = (
            ROOT / "distribution" / "adapters" / "ci-pre-agent",
            ROOT / "distribution" / "adapters" / "cloud-container-setup",
        )
        for adapter in adapters:
            with self.subTest(adapter=adapter), tempfile.TemporaryDirectory() as raw:
                temp = Path(raw).resolve()
                state_root = temp / "state"
                state_root.mkdir()
                request = temp / "request.json"
                receipt = temp / "receipt.json"
                audit = temp / "audit.json"
                write_json(request, request_for("claude-code", state_root))

                result = run_provision(adapter, request, receipt, audit)

                self.assertEqual(result.returncode, 3, result.stderr)
                self.assertEqual(
                    json.loads(receipt.read_text(encoding="utf-8"))["results"][0][
                        "diagnostic"
                    ]["code"],
                    "route-not-found",
                )
                source = adapter.read_text(encoding="utf-8")
                self.assertIn("distribution/provision", source)
                self.assertNotRegex(
                    source,
                    r"\b(claude|codex|grove|trellis|wisp)\b",
                )

    # spec-0002@v1 S31, R44
    def test_invalid_audit_parent_seals_minimal_output_failure_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "missing-parent" / "audit.json"
            write_json(request, request_for("codex", state_root))

            result = run_provision(PROVISION, request, receipt, audit)

            self.assertEqual(result.returncode, 7, result.stderr)
            self.assertFalse(audit.exists())
            value = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(value["overall_outcome"], "output-failure")
            self.assertEqual(value["exit_code"], 7)
            self.assertEqual(value["results"], [])
            self.assertEqual(
                value["diagnostics"][0]["code"], "output-parent-invalid"
            )
            self.assertNotIn("write_events_reference", value)
            self.assertNotIn("write_events_sha256", value)


if __name__ == "__main__":
    unittest.main()
