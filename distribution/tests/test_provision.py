"""Black-box tests for the bounded pre-agent provisioner."""

from __future__ import annotations

from contextlib import redirect_stderr
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from distribution.lib import provision as contract

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
            from distribution.lib import schema_validation

            schema_validation.validate_document(
                ROOT,
                "provision-receipt.v1.schema.json",
                value,
            )

    # spec-0002@v1 S27, R40; conformance output-parent TOCTOU finding
    def test_output_creation_is_relative_to_retained_nofollow_parent_fd(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            parent = temp / "outputs"
            moved_parent = temp / "retained-output-parent"
            parent.mkdir()
            target = contract.validate_output_leaf(
                str(parent / "receipt.json"),
                "receipt",
            )
            self.assertGreaterEqual(os.fstat(target.parent_fd).st_ino, 1)
            parent.rename(moved_parent)
            parent.mkdir()
            try:
                with mock.patch.object(
                    contract.os,
                    "open",
                    wraps=os.open,
                ) as open_call:
                    digest = contract.write_once(target, b"sealed")
                leaf_calls = [
                    call
                    for call in open_call.call_args_list
                    if call.args
                    and call.args[0] == "receipt.json"
                    and call.kwargs.get("dir_fd") == target.parent_fd
                ]
                self.assertEqual(len(leaf_calls), 1)
                self.assertTrue(leaf_calls[0].args[1] & os.O_EXCL)
                self.assertTrue(leaf_calls[0].args[1] & os.O_NOFOLLOW)
                self.assertEqual(
                    digest,
                    hashlib.sha256(b"sealed").hexdigest(),
                )
                self.assertEqual(
                    (moved_parent / "receipt.json").read_bytes(),
                    b"sealed",
                )
                self.assertFalse((parent / "receipt.json").exists())
            finally:
                target.close()

    # spec-0002@v1 S31, R40, R44; conformance post-work audit failure finding
    def test_post_work_audit_flush_failure_seals_typed_minimal_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_for("codex", state_root))
            real_fsync = os.fsync
            calls = 0

            def fail_first_fsync(descriptor: int) -> None:
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise OSError("forced audit flush failure")
                real_fsync(descriptor)

            stderr = io.StringIO()
            with mock.patch.object(
                contract.os,
                "fsync",
                side_effect=fail_first_fsync,
            ), redirect_stderr(stderr):
                exit_code = contract.execute(
                    ROOT,
                    request,
                    str(receipt),
                    str(audit),
                )

            self.assertEqual(exit_code, 7)
            value = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(
                value["request_id"],
                request_for("codex", state_root)["request_id"],
            )
            self.assertEqual(value["provisioner_version"], PROVISIONER_VERSION)
            self.assertEqual(value["results"], [])
            self.assertEqual(
                value["diagnostics"][0]["code"],
                "audit-seal-failed",
            )
            self.assertIn("audit-seal-failed", stderr.getvalue())
            self.assertNotIn("receipt-seal-failed", stderr.getvalue())
            self.assertFalse(audit.exists())
            from distribution.lib import schema_validation

            schema_validation.validate_document(
                ROOT,
                "provision-receipt.v1.schema.json",
                value,
            )

            retry_receipt = temp / "retry-receipt.json"
            retry_exit = contract.execute(
                ROOT,
                request,
                str(retry_receipt),
                str(audit),
            )
            self.assertEqual(retry_exit, 3)
            self.assertTrue(audit.is_file())

    # spec-0002@v1 S27, S31, R40, R44; conformance descriptor read-back finding
    def test_audit_readback_failure_uses_fd_and_seals_minimal_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_for("claude-code", state_root))
            real_read = os.read
            calls = 0

            def fail_first_read(descriptor: int, size: int) -> bytes:
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise OSError("forced audit read-back failure")
                return real_read(descriptor, size)

            with mock.patch.object(
                contract.os,
                "read",
                side_effect=fail_first_read,
            ):
                exit_code = contract.execute(
                    ROOT,
                    request,
                    str(receipt),
                    str(audit),
                )

            self.assertEqual(exit_code, 7)
            value = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(
                value["diagnostics"][0]["code"],
                "audit-seal-failed",
            )
            self.assertFalse(audit.exists())

    # spec-0002@v1 S27, S31, R40, R44; conformance receipt attribution finding
    def test_receipt_flush_failure_is_not_misattributed_to_audit(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_for("codex", state_root))
            real_fsync = os.fsync
            calls = 0

            def fail_second_fsync(descriptor: int) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("forced receipt flush failure")
                real_fsync(descriptor)

            stderr = io.StringIO()
            with mock.patch.object(
                contract.os,
                "fsync",
                side_effect=fail_second_fsync,
            ), redirect_stderr(stderr):
                exit_code = contract.execute(
                    ROOT,
                    request,
                    str(receipt),
                    str(audit),
                )

            self.assertEqual(exit_code, 7)
            self.assertTrue(audit.is_file())
            self.assertFalse(receipt.exists())
            self.assertIn("receipt-seal-failed", stderr.getvalue())
            self.assertNotIn("audit-seal-failed", stderr.getvalue())

    # spec-0002@v1 S27, S31, R40, R44; conformance receipt read-back finding
    def test_receipt_is_read_back_from_its_open_descriptor_before_success(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_for("codex", state_root))
            real_read = os.read
            calls = 0

            def fail_receipt_read(descriptor: int, size: int) -> bytes:
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise OSError("forced receipt read-back failure")
                return real_read(descriptor, size)

            stderr = io.StringIO()
            with mock.patch.object(
                contract.os,
                "read",
                side_effect=fail_receipt_read,
            ), redirect_stderr(stderr):
                exit_code = contract.execute(
                    ROOT,
                    request,
                    str(receipt),
                    str(audit),
                )

            self.assertEqual(exit_code, 7)
            self.assertFalse(receipt.exists())
            self.assertIn("receipt-seal-failed", stderr.getvalue())
            self.assertNotIn("audit-seal-failed", stderr.getvalue())

    # spec-0002@v1 bounded implementation disclosure; conformance status finding
    def test_implementation_status_does_not_claim_whole_protocol_conformance(self) -> None:
        status = (
            ROOT / "distribution" / "PROVISIONER-IMPLEMENTATION-STATUS.md"
        ).read_text(encoding="utf-8")
        self.assertIn("No whole-spec conformance is claimed", status)
        self.assertIn("descriptor-relative", status.lower())
        self.assertNotIn(
            "Host-neutral request decoding, phases 1–4",
            status,
        )

    # spec-0002@v1 invocation path safety, R14; code-review H1
    def test_physical_output_alias_inside_symlinked_state_root_is_not_sealed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            physical_state = temp / "physical-state"
            physical_state.mkdir()
            state_alias = temp / "state-alias"
            state_alias.symlink_to(physical_state, target_is_directory=True)
            request = temp / "request.json"
            receipt = physical_state / "receipt.json"
            audit = physical_state / "audit.json"
            write_json(request, request_for("codex", state_alias))

            result = run_provision(PROVISION, request, receipt, audit)

            self.assertEqual(result.returncode, 7)
            self.assertFalse(receipt.exists())
            self.assertFalse(audit.exists())
            self.assertIn("receipt-seal-failed", result.stderr)

    # spec-0002@v1 output path distinctness, S31; code-review H4
    def test_casefold_alias_is_rejected_before_request_work(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request = temp / "request.json"
            receipt = temp / "Result.json"
            audit = temp / "result.json"
            write_json(request, request_for("codex", state_root))

            with mock.patch.object(
                contract,
                "detect_case_sensitivity",
                return_value=False,
            ), mock.patch.object(
                Path,
                "read_bytes",
                side_effect=AssertionError("request work started"),
            ):
                exit_code = contract.execute(
                    ROOT,
                    request,
                    str(receipt),
                    str(audit),
                )

            self.assertEqual(exit_code, 7)
            self.assertFalse(receipt.exists())
            self.assertFalse(audit.exists())

    # spec-0002@v1 R7, R20, R43; code-review H3
    def test_repository_authority_failure_is_stewards_owned_not_invalid_request(
        self,
    ) -> None:
        for validator_name in (
            "validate_surface_registry",
            "validate_provisioners",
        ):
            with self.subTest(validator=validator_name), tempfile.TemporaryDirectory() as raw:
                temp = Path(raw).resolve()
                state_root = temp / "state"
                state_root.mkdir()
                request = temp / "request.json"
                receipt = temp / "receipt.json"
                audit = temp / "audit.json"
                write_json(request, request_for("codex", state_root))

                with mock.patch.object(
                    contract,
                    validator_name,
                    side_effect=ValueError("forced repository authority failure"),
                ):
                    exit_code = contract.execute(
                        ROOT,
                        request,
                        str(receipt),
                        str(audit),
                    )

                self.assertEqual(exit_code, 3)
                value = json.loads(receipt.read_text(encoding="utf-8"))
                self.assertEqual(value["overall_outcome"], "failed")
                self.assertEqual(value["diagnostics"], [])
                result = value["results"][0]
                self.assertEqual(result["phase"], "identity-resolution")
                self.assertEqual(result["diagnostic"]["owner"], "stewards")
                self.assertEqual(
                    result["diagnostic"]["code"],
                    "unresolved-release",
                )

    # spec-0002@v1 authority schemas, S25, S27, R27, R36-R37; code-review M1
    def test_all_provisioner_fixtures_and_emitted_documents_validate_full_schemas(
        self,
    ) -> None:
        from distribution.lib import schema_validation

        fixture_root = ROOT / "distribution" / "fixtures" / "provisioner"
        manifest = json.loads(
            (fixture_root / "manifest.json").read_text(encoding="utf-8")
        )
        for row in manifest["fixtures"]:
            document = json.loads(
                (fixture_root / row["path"]).read_text(encoding="utf-8")
            )
            if row["path"] == "version-range.json":
                with self.assertRaises(
                    schema_validation.SchemaValidationError
                ):
                    schema_validation.validate_document(
                        ROOT,
                        "provision-request.v1.schema.json",
                        document,
                    )
            else:
                schema_validation.validate_document(
                    ROOT,
                    "provision-request.v1.schema.json",
                    document,
                )
            with tempfile.TemporaryDirectory() as raw:
                temp = Path(raw).resolve()
                request = temp / "request.json"
                receipt = temp / "receipt.json"
                audit = temp / "audit.json"
                write_json(request, document)
                result = run_provision(PROVISION, request, receipt, audit)
                self.assertEqual(
                    result.returncode,
                    row["expected_exit"],
                    result.stderr,
                )
                schema_validation.validate_document(
                    ROOT,
                    "provision-receipt.v1.schema.json",
                    json.loads(receipt.read_text(encoding="utf-8")),
                )
                schema_validation.validate_document(
                    ROOT,
                    "provision-write-events.v1.schema.json",
                    json.loads(audit.read_text(encoding="utf-8")),
                )

    # spec-0002@v1 deterministic aggregate result; code-review H5
    def test_receipt_schema_rejects_contradictory_outcome_and_exit(self) -> None:
        from distribution.lib import schema_validation

        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_for("codex", state_root))
            result = run_provision(PROVISION, request, receipt, audit)
            self.assertEqual(result.returncode, 3, result.stderr)
            value = json.loads(receipt.read_text(encoding="utf-8"))

        contradictory = dict(value)
        contradictory["overall_outcome"] = "success"
        contradictory["exit_code"] = 6
        with self.assertRaises(schema_validation.SchemaValidationError):
            schema_validation.validate_document(
                ROOT,
                "provision-receipt.v1.schema.json",
                contradictory,
            )

        contradictory = dict(value)
        contradictory["exit_code"] = 6
        with self.assertRaises(schema_validation.SchemaValidationError):
            schema_validation.validate_document(
                ROOT,
                "provision-receipt.v1.schema.json",
                contradictory,
            )

    # spec-0002@v1 S5, R27, R32; second code-review H1
    def test_json_schema_literals_are_json_type_sensitive(self) -> None:
        from distribution.lib import schema_validation

        validator = schema_validation.Validator(
            ROOT / "distribution" / "schemas"
        )
        for schema, instance in (
            ({"const": 1}, True),
            ({"enum": [0, 2]}, False),
        ):
            with self.subTest(
                schema=schema,
                instance=instance,
            ), self.assertRaises(
                schema_validation.SchemaValidationError
            ):
                validator.validate(schema, instance, "inline")

        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request_value = request_for("codex", state_root)
            request_value["schema_version"] = True
            with self.assertRaises(schema_validation.SchemaValidationError):
                schema_validation.validate_document(
                    ROOT,
                    "provision-request.v1.schema.json",
                    request_value,
                )

            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_value)
            result = run_provision(PROVISION, request, receipt, audit)

            self.assertEqual(result.returncode, 2, result.stderr)
            value = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(value["overall_outcome"], "invalid-request")
            self.assertEqual(value["exit_code"], 2)
            self.assertEqual(
                value["diagnostics"][0]["causes"][0]["field_path"],
                "/schema_version",
            )
            schema_validation.validate_document(
                ROOT,
                "provision-receipt.v1.schema.json",
                value,
            )

    # spec-0002@v1 sealing order and output failure rule 3; second review H2
    def test_audit_path_identity_is_revalidated_before_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            receipt_parent = temp / "receipt-output"
            audit_parent = temp / "audit-output"
            moved_audit_parent = temp / "moved-audit-output"
            state_root.mkdir()
            receipt_parent.mkdir()
            audit_parent.mkdir()
            request = temp / "request.json"
            receipt = receipt_parent / "receipt.json"
            audit = audit_parent / "audit.json"
            write_json(request, request_for("codex", state_root))
            real_write_once = contract.write_once

            def move_parent_after_audit(
                target: contract.OutputTarget,
                raw_bytes: bytes,
            ) -> str:
                digest = real_write_once(target, raw_bytes)
                if target.label == "audit":
                    audit_parent.rename(moved_audit_parent)
                    audit_parent.mkdir()
                return digest

            stderr = io.StringIO()
            with mock.patch.object(
                contract,
                "write_once",
                side_effect=move_parent_after_audit,
            ), redirect_stderr(stderr):
                exit_code = contract.execute(
                    ROOT,
                    request,
                    str(receipt),
                    str(audit),
                )

            self.assertEqual(exit_code, 7)
            self.assertFalse(audit.exists())
            self.assertFalse((moved_audit_parent / "audit.json").exists())
            value = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(value["overall_outcome"], "output-failure")
            self.assertEqual(value["exit_code"], 7)
            self.assertEqual(
                value["diagnostics"][0]["code"],
                "audit-seal-failed",
            )
            self.assertNotIn("write_events_reference", value)
            self.assertNotIn("write_events_sha256", value)
            self.assertIn("audit-seal-failed", stderr.getvalue())

    # spec-0002@v1 Receipt grammar and phase-6 precedence; second review H3
    def test_invalid_request_receipt_requires_a_request_failure_reason(self) -> None:
        from distribution.lib import schema_validation

        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_for("codex", state_root))
            result = run_provision(PROVISION, request, receipt, audit)
            self.assertEqual(result.returncode, 3, result.stderr)
            route_failed = json.loads(receipt.read_text(encoding="utf-8"))

        reasonless = dict(route_failed)
        reasonless["overall_outcome"] = "invalid-request"
        reasonless["exit_code"] = 2
        reasonless["results"] = []
        with self.assertRaises(schema_validation.SchemaValidationError):
            schema_validation.validate_document(
                ROOT,
                "provision-receipt.v1.schema.json",
                reasonless,
            )

        relabeled_route_failure = dict(route_failed)
        relabeled_route_failure["overall_outcome"] = "invalid-request"
        relabeled_route_failure["exit_code"] = 2
        with self.assertRaises(schema_validation.SchemaValidationError):
            schema_validation.validate_document(
                ROOT,
                "provision-receipt.v1.schema.json",
                relabeled_route_failure,
            )

        with tempfile.TemporaryDirectory() as raw:
            temp = Path(raw).resolve()
            state_root = temp / "state"
            state_root.mkdir()
            request_value = request_for("codex", state_root)
            request_value["targets"][0]["plugins"][0]["package_version"] = "latest"
            request = temp / "request.json"
            receipt = temp / "receipt.json"
            audit = temp / "audit.json"
            write_json(request, request_value)
            result = run_provision(PROVISION, request, receipt, audit)
            self.assertEqual(result.returncode, 2, result.stderr)
            schema_validation.validate_document(
                ROOT,
                "provision-receipt.v1.schema.json",
                json.loads(receipt.read_text(encoding="utf-8")),
            )


if __name__ == "__main__":
    unittest.main()
