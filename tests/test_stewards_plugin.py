"""Tests derived from specs 0003@v1 and 0004@v1."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_stewards_plugin.py"
PLUGIN = ROOT / "plugins" / "stewards"
SKILL = PLUGIN / "skills" / "setup-ci-marketplace" / "SKILL.md"
OBSERVATION_REFERENCE = (
    PLUGIN
    / "skills"
    / "setup-ci-marketplace"
    / "references"
    / "marketplace-observation-v1.md"
)
FIXTURES = ROOT / "tests" / "fixtures"


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
        self.assertIn("stewards plugin validation passed", result.stdout)

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
                "setup_step_id": "stewards_marketplace_kodhama_codex",
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

    def test_skill_carries_the_exact_v1_host_adapter(self) -> None:
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
            '- name: "Stewards marketplace: checkout <m>"',
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
        ):
            self.assertTrue((FIXTURES / name).is_file(), name)

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
