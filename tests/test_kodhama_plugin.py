"""Kodhama plugin tests derived from specs 0003@v1 and 0004@v2."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_kodhama_plugin.py"
PLUGIN = ROOT / "plugins" / "kodhama"
SKILL = PLUGIN / "skills" / "setup-ci-marketplace" / "SKILL.md"
OBSERVATION_REFERENCE = (
    PLUGIN
    / "skills"
    / "setup-ci-marketplace"
    / "references"
    / "marketplace-observation-v1.md"
)
FIXTURES = ROOT / "tests" / "fixtures"
HOSTED_WORKFLOW = (
    ROOT / ".github" / "workflows" / "validate-marketplace-setup.yml"
)
OBSERVATION_EMITTER = ROOT / "scripts" / "emit_marketplace_observation.py"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


class PackageAndObservationTests(unittest.TestCase):
    """spec-0004 S10/R16-R17 and spec-0003 R1-R7."""

    def test_repository_package_and_carrier_parity_validate(self) -> None:
        result = run("python3", str(VALIDATOR))
        self.assertIn("kodhama plugin validation passed", result.stdout)

    def test_closed_observation_accepts_exact_shape_and_rejects_unknown(self) -> None:
        observation = {
            "schema_version": 1,
            "host": "codex",
            "surface_id": "github-actions/codex-marketplace",
            "marketplace": {
                "name": "kodhama",
                "repository": "kodhama/stewards",
                "revision": "0" * 40,
            },
            "execution": {
                "repository": "kodhama/trellis",
                "commit": "1" * 40,
                "workflow": ".github/workflows/ci.yml",
                "job": "codex-marketplace",
                "run_id": 123,
                "run_attempt": 1,
                "setup_step_id": "kodhama_marketplace_kodhama_codex",
            },
            "observed_at": "2026-07-24T12:34:56.789Z",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "observation.json"
            path.write_text(json.dumps(observation), encoding="utf-8")
            run("python3", str(VALIDATOR), "--observation", str(path))

            observation["result"] = "passed"
            path.write_text(json.dumps(observation), encoding="utf-8")
            rejected = run(
                "python3",
                str(VALIDATOR),
                "--observation",
                str(path),
                check=False,
            )
            self.assertNotEqual(0, rejected.returncode)
            self.assertIn("unknown properties", rejected.stderr)

            del observation["result"]
            path.write_text(json.dumps(observation), encoding="utf-8")
            accepted = run(
                "python3", str(VALIDATOR), "--observation", str(path)
            )
            self.assertIn("structural validation passed", accepted.stdout)
            self.assertIn("runtime provenance unverified", accepted.stdout)


class SkillContractTests(unittest.TestCase):
    """Static gates for spec-0004's shipped callable contract."""

    def test_skill_carries_the_exact_v2_host_adapter(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        for required in (
            "Claude Code `2.1.199`",
            "Codex CLI `0.145.0`",
            "claude plugin marketplace add",
            "--scope local",
            "claude plugin marketplace list --json",
            "codex plugin marketplace add",
            "codex plugin marketplace list --json",
            "actions/checkout@",
            "persist-credentials: false",
            "git remote get-url origin",
            "git rev-parse HEAD",
            '- name: "Kodhama marketplace: checkout <m>"',
            "working-directory: ${{ github.workspace }}",
            "./.kodhama/marketplaces/<m>",
            "step-level `if:`",
        ):
            self.assertIn(required, text)
        self.assertNotIn("claude plugin install", text)
        self.assertNotIn("codex plugin add", text)

    def test_skill_is_plan_confirm_apply_and_fail_closed(self) -> None:
        text = SKILL.read_text(encoding="utf-8").lower()
        for required in (
            "plan",
            "confirm",
            "external reusable workflow",
            "opaque host action",
            "unowned",
            "collision",
            "no edit",
            "idempotent",
            "surface_id",
            "observation",
        ):
            self.assertIn(required, text)

    def test_forward_test_fixtures_cover_supported_and_unsupported_jobs(self) -> None:
        for name in (
            "claude-direct.yml",
            "codex-direct.yml",
            "mixed-direct.yml",
            "codex-action.yml",
            "unrelated.yml",
            "ambiguous-wrapper.yml",
            "external-reusable.yml",
            "conditional-direct.yml",
            "caller-default-working-directory.yml",
            "local-reusable.yml",
            "unowned-equivalent.yml",
        ):
            self.assertTrue((FIXTURES / name).is_file(), name)

    def test_authoring_fixtures_retain_deterministic_expected_results(self) -> None:
        supported = {
            "claude-direct": ("install-claude", "kodhama_marketplace_kodhama_claude", "run-claude"),
            "codex-direct": ("install-codex", "kodhama_marketplace_kodhama_codex", "run-codex"),
            "mixed-direct": (
                "install-claude",
                "install-codex",
                "kodhama_marketplace_kodhama_claude",
                "kodhama_marketplace_kodhama_codex",
                "run-claude",
                "run-codex",
            ),
            "caller-default-working-directory": (
                "install-codex",
                "kodhama_marketplace_kodhama_codex",
                "run-codex",
            ),
            "local-reusable": (
                "install-claude",
                "kodhama_marketplace_kodhama_claude",
                "run-claude",
            ),
        }
        for stem, ordered_ids in supported.items():
            expected = (FIXTURES / f"{stem}.expected.yml").read_text(
                encoding="utf-8"
            )
            positions = [expected.index(f"id: {step_id}") for step_id in ordered_ids]
            self.assertEqual(sorted(positions), positions, stem)
            self.assertEqual(
                1,
                expected.count("id: kodhama_marketplace_kodhama_checkout"),
                stem,
            )
            self.assertEqual(
                2 if stem == "mixed-direct" else 1,
                expected.count("working-directory: ${{ github.workspace }}"),
                stem,
            )

        for stem in (
            "unrelated",
            "ambiguous-wrapper",
            "external-reusable",
            "codex-action",
            "conditional-direct",
            "unowned-equivalent",
        ):
            source = (FIXTURES / f"{stem}.yml").read_bytes()
            expected = (FIXTURES / f"{stem}.expected.yml").read_bytes()
            self.assertEqual(source, expected, stem)

    def test_hosted_workflow_runs_each_host_with_separate_state(self) -> None:
        text = HOSTED_WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "repository-validation:",
            "python3 -m unittest discover -s tests -v",
            "claude-marketplace:",
            "codex-marketplace:",
            "mixed-marketplace:",
            "@anthropic-ai/claude-code@2.1.199",
            "@openai/codex@0.145.0",
            "id: kodhama_marketplace_kodhama_claude",
            "id: kodhama_marketplace_kodhama_codex",
            "working-directory: ${{ github.workspace }}",
            "CLAUDE_CONFIG_DIR:",
            "CODEX_HOME:",
            "actions/upload-artifact@",
            "scripts/emit_marketplace_observation.py",
            "ref: ${{ github.sha }}",
            'test "$revision" = "$GITHUB_SHA"',
        ):
            self.assertIn(required, text)
        self.assertEqual(
            3,
            text.count("id: kodhama_marketplace_kodhama_checkout"),
        )

    def test_authoring_report_retains_two_pass_hashes(self) -> None:
        report = json.loads(
            (FIXTURES / "authoring-report.json").read_text(encoding="utf-8")
        )
        self.assertEqual(1, report["schema_version"])
        self.assertIn("second pass", report["method"].lower())
        self.assertEqual(
            {
                "claude-direct",
                "codex-direct",
                "mixed-direct",
                "unrelated",
                "ambiguous-wrapper",
                "external-reusable",
                "conditional-direct",
                "codex-action",
                "caller-default-working-directory",
                "local-reusable",
                "unowned-equivalent",
            },
            set(report["cases"]),
        )
        for stem, result in report["cases"].items():
            expected = (FIXTURES / f"{stem}.expected.yml").read_bytes()
            digest = hashlib.sha256(expected).hexdigest()
            self.assertEqual(digest, result["first_pass_sha256"], stem)
            self.assertEqual(digest, result["second_pass_sha256"], stem)
            self.assertTrue(result["converged"], stem)
            self.assertIn("workflow", result["inspected"])
            self.assertIn("job", result["inspected"])
            self.assertIn("generated_step_ids", result)
            self.assertIn("prerequisites", result)

        self.assertEqual(
            {
                "launched_host": False,
                "ran_product_test": False,
                "installed_plugin": False,
                "emitted_support_state": False,
                "created_marketplace_observation": False,
            },
            report["authoring_boundary"],
        )
        self.assertEqual(
            4,
            HOSTED_WORKFLOW.read_text(encoding="utf-8").count(
                "python3 scripts/validate_kodhama_plugin.py\n"
            ),
        )

    def test_runtime_observation_emitter_writes_a_valid_closed_record(self) -> None:
        env = {
            **os.environ,
            "GITHUB_REPOSITORY": "kodhama/stewards",
            "GITHUB_SHA": "1" * 40,
            "GITHUB_RUN_ID": "123",
            "GITHUB_RUN_ATTEMPT": "2",
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "observation.json"
            emitted = subprocess.run(
                [
                    "python3",
                    str(OBSERVATION_EMITTER),
                    "--host",
                    "codex",
                    "--surface-id",
                    "github-actions/codex-marketplace-setup-skill",
                    "--marketplace-name",
                    "kodhama",
                    "--marketplace-repository",
                    "kodhama/stewards",
                    "--marketplace-revision",
                    "0" * 40,
                    "--workflow",
                    ".github/workflows/validate-marketplace-setup.yml",
                    "--job",
                    "codex-marketplace",
                    "--setup-step-id",
                    "kodhama_marketplace_kodhama_codex",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            self.assertEqual("", emitted.stdout)
            validated = run(
                "python3", str(VALIDATOR), "--observation", str(output)
            )
            self.assertIn("structural validation passed", validated.stdout)

    def test_runtime_observation_emitter_fails_before_writing_invalid_record(
        self,
    ) -> None:
        env = {
            **os.environ,
            "GITHUB_REPOSITORY": "not-a-repository",
            "GITHUB_SHA": "not-a-sha",
            "GITHUB_RUN_ID": "0",
            "GITHUB_RUN_ATTEMPT": "-1",
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "invalid.json"
            output.write_text("stale observation\n", encoding="utf-8")
            emitted = subprocess.run(
                [
                    "python3",
                    str(OBSERVATION_EMITTER),
                    "--host",
                    "codex",
                    "--surface-id",
                    "github-actions/codex-marketplace-setup-skill",
                    "--marketplace-name",
                    "kodhama",
                    "--marketplace-repository",
                    "not-a-repository",
                    "--marketplace-revision",
                    "not-a-sha",
                    "--workflow",
                    "not-a-workflow",
                    "--job",
                    "",
                    "--setup-step-id",
                    "not a step id",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(0, emitted.returncode)
            self.assertFalse(output.exists())

    def test_runtime_observation_emitter_cleans_up_on_output_failure(
        self,
    ) -> None:
        env = {
            **os.environ,
            "GITHUB_REPOSITORY": "kodhama/stewards",
            "GITHUB_SHA": "1" * 40,
            "GITHUB_RUN_ID": "123",
            "GITHUB_RUN_ATTEMPT": "2",
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "observation.json"
            output.mkdir()
            emitted = subprocess.run(
                [
                    "python3",
                    str(OBSERVATION_EMITTER),
                    "--host",
                    "codex",
                    "--surface-id",
                    "github-actions/codex-marketplace-setup-skill",
                    "--marketplace-name",
                    "kodhama",
                    "--marketplace-repository",
                    "kodhama/stewards",
                    "--marketplace-revision",
                    "0" * 40,
                    "--workflow",
                    ".github/workflows/validate-marketplace-setup.yml",
                    "--job",
                    "codex-marketplace",
                    "--setup-step-id",
                    "kodhama_marketplace_kodhama_codex",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(0, emitted.returncode)
            self.assertEqual([], list(Path(tmp).glob(".observation.json.*")))

    def test_optional_observation_contract_is_shipped_with_the_skill(self) -> None:
        text = OBSERVATION_REFERENCE.read_text(encoding="utf-8")
        for required in (
            '"schema_version": 1',
            '"marketplace"',
            '"execution"',
            '"setup_step_id"',
            '"observed_at"',
            "unknown properties are invalid",
            "GITHUB_RUN_ATTEMPT",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
