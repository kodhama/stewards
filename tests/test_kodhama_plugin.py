"""Kodhama plugin tests derived from specs 0003@v1 and 0004@v2."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_kodhama_plugin.py"
PLUGIN = ROOT / "plugins" / "kodhama"
SKILL = PLUGIN / "skills" / "setup-ci-marketplace" / "SKILL.md"
FIXTURES = ROOT / "tests" / "fixtures"
HOSTED_WORKFLOW = (
    ROOT / ".github" / "workflows" / "validate-marketplace-setup.yml"
)


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


class PackageAndCatalogTests(unittest.TestCase):
    """spec-0004 S10/R16-R17. The observation half retired with `kodhama-0025`."""

    def test_trellis_codex_preview_catalog_entry_makes_no_support_claim(
        self,
    ) -> None:
        """trellis decision-0063 and kodhama-0021 AC2."""
        claude = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        codex = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        codex_trellis = [
            entry for entry in codex["plugins"] if entry["name"] == "trellis"
        ]
        self.assertEqual(1, len(codex_trellis))
        self.assertEqual(
            {
                "category": "Developer Tools",
                "description": (
                    "Preview — Trellis governance with live project rules. "
                    "This catalog listing makes no support claim; consult "
                    "Trellis product documentation for exact host and "
                    "surface boundaries."
                ),
                "name": "trellis",
                "policy": {
                    "authentication": "ON_INSTALL",
                    "installation": "AVAILABLE",
                },
                "source": {
                    "path": "plugins/trellis",
                    "source": "git-subdir",
                    "url": "kodhama/trellis",
                },
            },
            codex_trellis[0],
        )

        claude_trellis = [
            entry for entry in claude["plugins"] if entry["name"] == "trellis"
        ]
        self.assertEqual(1, len(claude_trellis))
        self.assertEqual(
            (
                "Install and consult Trellis in a Claude Code project: "
                "the invariants, expressed at your strength."
            ),
            claude_trellis[0]["description"],
        )

    def test_wisp_preview_catalog_entries_disclose_no_support_claim(self) -> None:
        """kodhama-0021 AC2: preview listings never imply support."""
        claude = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        codex = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        expected_description = (
            "Preview — project-scoped MCP lifecycle bus and dashboard; "
            "support is not claimed."
        )

        claude_wisp = next(
            entry for entry in claude["plugins"] if entry["name"] == "wisp"
        )
        codex_wisp = next(
            entry for entry in codex["plugins"] if entry["name"] == "wisp"
        )
        self.assertEqual(expected_description, claude_wisp["description"])
        self.assertEqual(expected_description, codex_wisp["description"])

    def test_kodhama_catalog_entries_disclose_no_support_claim(self) -> None:
        """kodhama-0021 §2: a listing must disclose that support is not claimed.

        The disclosure has no other carrier — no README, product doc, or
        plugin file in this repository states it — so the entry's own
        `description` is it, on both hosts. The text is pinned literally
        here rather than read from a manifest, because `kodhama-0018` §1
        explicitly permits the two host manifests to carry *different*
        descriptions; coupling a catalog to one of them would break the
        moment that grant is exercised.
        """
        expected = (
            "Dogfood — author verified Claude and Codex marketplace setup "
            "in repository-owned GitHub Actions workflows; support is not "
            "claimed."
        )
        for path in (
            ROOT / ".claude-plugin" / "marketplace.json",
            ROOT / ".agents" / "plugins" / "marketplace.json",
        ):
            catalog = json.loads(path.read_text(encoding="utf-8"))
            entry = next(
                item
                for item in catalog["plugins"]
                if item["name"] == "kodhama"
            )
            self.assertEqual(expected, entry.get("description"), path)

    def test_codex_catalog_entry_stays_closed_around_its_description(
        self,
    ) -> None:
        """The Codex branch admits `description` and nothing else.

        It used to compare the whole entry for equality, which rejected the
        `description` its trellis and wisp siblings carry. Relaxing that to a
        key-by-key subset would have overshot: Codex itself accepts unknown
        entry fields silently — a typo like `instalation` reaches neither
        this check nor the host — so the object is closed instead. Driving
        the validator against mutated copies proves both halves; asserting
        only that the real catalog passes would not.
        """
        validator = self._load_validator()
        with tempfile.TemporaryDirectory() as workspace:
            root = Path(workspace)
            (root / ".claude-plugin").mkdir(parents=True)
            (root / ".agents" / "plugins").mkdir(parents=True)
            claude_path = root / ".claude-plugin" / "marketplace.json"
            codex_path = root / ".agents" / "plugins" / "marketplace.json"

            def write(entry: dict) -> None:
                claude_path.write_text(
                    json.dumps(
                        {
                            "name": "kodhama",
                            "plugins": [
                                {
                                    "name": "kodhama",
                                    "source": "./plugins/kodhama",
                                    "description": "disclosed",
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                codex_path.write_text(
                    json.dumps({"name": "kodhama", "plugins": [entry]}),
                    encoding="utf-8",
                )

            valid = {
                "name": "kodhama",
                "source": {"source": "local", "path": "./plugins/kodhama"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
                "description": "disclosed",
            }
            with mock.patch.object(validator, "ROOT", root):
                write(valid)
                validator.validate_catalogs("0.2.0")

                for label, mutation in (
                    ("unknown field", {"instalation": "AVAILABLE"}),
                    ("misspelled policy", {"policyy": {}}),
                    ("stray posture", {"suport": "GA"}),
                ):
                    write({**valid, **mutation})
                    with self.assertRaises(validator.Invalid, msg=label):
                        validator.validate_catalogs("0.2.0")

                write({k: v for k, v in valid.items() if k != "description"})
                with self.assertRaises(validator.Invalid, msg="no disclosure"):
                    validator.validate_catalogs("0.2.0")

                write({**valid, "description": "   "})
                with self.assertRaises(validator.Invalid, msg="blank"):
                    validator.validate_catalogs("0.2.0")

                write({**valid, "source": {"source": "local", "path": "./x"}})
                with self.assertRaises(validator.Invalid, msg="wrong source"):
                    validator.validate_catalogs("0.2.0")

    @staticmethod
    def _load_validator():
        spec = importlib.util.spec_from_file_location(
            "kodhama_plugin_validator", VALIDATOR
        )
        if spec is None or spec.loader is None:
            raise AssertionError("cannot load validator")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_shipped_readme_discloses_hosts_and_makes_no_support_claim(self) -> None:
        """kodhama-0025 §2: the README is the replacement for the surface matrix.

        It ships inside the package, so the disclosure survives outside the
        marketplace — which the catalog `description` does not. This is the
        whole of what replaced ~500 lines of matrix, schema, validator and
        frozen evidence, so it is guarded rather than trusted.
        """
        readme = PLUGIN / "README.md"
        self.assertTrue(readme.is_file(), "the shipped package must carry a README")
        # Normalised, so a line wrap in the source cannot make a required
        # sentence "absent" and quietly weaken the guard.
        text = " ".join(readme.read_text(encoding="utf-8").split())
        for required in (
            "Support is not claimed",
            "keyless_admission_check.py",
            "codex plugin marketplace add",
            # The sentences that keep the claim honest. An earlier version of
            # this test asserted `X if X in text else Y`, which is a tautology
            # — it cannot fail, and it guarded exactly the paragraph that stops
            # the README overclaiming. Assert the literals.
            "closer to a layout check than a load check",
            "that the skill *runs*",
        ):
            self.assertIn(required, text)

    def test_the_surface_matrix_stays_retired(self) -> None:
        """kodhama-0025: it should not grow back.

        Wisp's retirement shipped exactly this guard and it is the reason its
        matrix has not returned. A tree-wide check is cheap and catches a
        reintroduction by any route, including a well-meaning propagation wave.
        """
        # Matching two exact filenames let a rename walk straight past this —
        # `surface-matrix.json`, `emit_observation.py`, or a fresh
        # `evidence/run-1/claude.json` all reintroduced the retired shape with
        # the suite green. Match the shape, not the spelling.
        offenders = []
        for path in ROOT.rglob("*"):
            rel = path.relative_to(ROOT)
            if ".git" in rel.parts or not path.is_file():
                continue
            name = path.name.lower()
            if "surface" in name and name.endswith(".json"):
                offenders.append(f"{rel} (surface matrix)")
            if name.startswith("emit_") and "observation" in name:
                offenders.append(f"{rel} (observation emitter)")
            if "marketplace-observations" in rel.as_posix():
                offenders.append(f"{rel} (committed observation evidence)")
        self.assertEqual([], offenders, "the retired surface/observation shape came back")

    def test_repository_package_and_carrier_parity_validate(self) -> None:
        result = run("python3", str(VALIDATOR))
        self.assertIn("kodhama plugin validation passed", result.stdout)


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
            '".claude-plugin/marketplace.json"',
            '".agents/plugins/marketplace.json"',
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
            # The evidence upload and the observation emitter retired with
            # `kodhama-0025`. What the workflow proves is unchanged: it runs a
            # real `marketplace add` on each host against this exact commit and
            # verifies the host resolved it. That is the honest integration
            # test; emitting a JSON record about having done so was not.
            "claude plugin marketplace add",
            "codex plugin marketplace add",
            "ref: ${{ github.sha }}",
            'test "$revision" = "$GITHUB_SHA"',
        ):
            self.assertIn(required, text)
        self.assertEqual(
            3,
            text.count("id: kodhama_marketplace_kodhama_checkout"),
        )
        self.assertEqual(2, text.count('mkdir -p "$CODEX_HOME"'))

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

        for stem in (
            "codex-direct",
            "mixed-direct",
            "caller-default-working-directory",
        ):
            source = (FIXTURES / f"{stem}.yml").read_text(encoding="utf-8")
            expected = (FIXTURES / f"{stem}.expected.yml").read_text(
                encoding="utf-8"
            )
            self.assertIn('mkdir -p "$CODEX_HOME"', source)
            self.assertIn('mkdir -p "$CODEX_HOME"', expected)

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


class IssueSkillPublicationTests(unittest.TestCase):
    """spec-0005: the issue-convention payload's publication into the package."""

    def test_test_deps_declares_this_spec(self) -> None:
        """spec-0005 R18: declared, and declared *pinned*.

        `TEST_DEPS.md` says its tests "derive from the dependencies above",
        and the tests below derive from spec 0005. `specs/README.md` requires
        the `id@vN` form for a versioned spec dependency — the file already
        pins its sibling `@v5` — so a bare id would satisfy the sentence and
        match neither the file's own practice nor the spec's requirement.
        """
        text = (ROOT / "tests" / "TEST_DEPS.md").read_text(encoding="utf-8")
        entries = [
            line.strip()[2:].strip()
            for line in text.splitlines()
            if line.startswith("  - ")
        ]
        spec_id = "kodhama-spec-0005-issue-taxonomy-skill-publication"
        matching = [entry for entry in entries if entry.split("@")[0] == spec_id]
        self.assertEqual([f"{spec_id}@v8"], matching, entries)
        self.assertNotIn(spec_id, [entry for entry in entries if "@" not in entry])

    def test_the_ci_filter_covers_the_staging_subtree(self) -> None:
        """spec-0005 S15/R17: the anti-drift guard reaches the staging tree.

        Read by regex rather than by a YAML parse: neither `tests/` nor
        `scripts/` imports `yaml` today, and the `repository-validation` job
        installs no Python packages before running this suite, so an
        `import yaml` would fail at collection on a clean runner.

        The order is asserted, and the list is *not* sorted — the two plugin
        scripts sit in the order they were added. Tidying them into
        alphabetical order would produce a correct filter and a red test,
        which is the wrong trade: the point of pinning order is that any
        edit to the filter is read by a human.
        """
        lines = HOSTED_WORKFLOW.read_text(encoding="utf-8").splitlines()
        start = next(
            index
            for index, line in enumerate(lines)
            if re.fullmatch(r"\s*paths:\s*", line)
        )
        indent = len(lines[start]) - len(lines[start].lstrip())
        entries: list[str] = []
        for line in lines[start + 1 :]:
            if not line.strip():
                continue
            if len(line) - len(line.lstrip()) <= indent:
                break
            match = re.fullmatch(r'\s*-\s*"([^"]+)"\s*', line)
            self.assertIsNotNone(match, line)
            assert match is not None
            entries.append(match.group(1))

        self.assertEqual(
            [
                ".agents/plugins/marketplace.json",
                ".claude-plugin/marketplace.json",
                ".github/workflows/validate-marketplace-setup.yml",
                "conductor/wave-issue-taxonomy/plugin/**",
                "plugins/kodhama/**",
                "scripts/validate_kodhama_plugin.py",
                "scripts/keyless_admission_check.py",
                "tests/**",
            ],
            entries,
        )
        # R17's second half. The ruling closed the blind spot *narrowly*: the
        # test gate must not run on a prose edit under `conductor/`.
        self.assertNotIn("conductor/**", entries)

    def test_the_package_inventory_is_closed(self) -> None:
        """spec-0005 S1/R1/R2: exactly these nine files, and no other.

        A closed set rather than nine presence assertions. It proves
        `DIRECTION.md` landed at the plugin root — where `taxonomy.md` §6.5's
        `../../../DIRECTION.md` resolves and nowhere else — proves nothing
        stray came with the payload, and makes any later legitimate growth a
        deliberate spec revision instead of a silent one.

        `.DS_Store` is filtered because this repository has no `.gitignore`
        and `CLAUDE.md` tells the executor to run this suite locally; on macOS
        a stray finder file would otherwise fail a correct package. CI is safe
        on a fresh clone, so the risk this closes is local-red only.
        """
        self.assertEqual(
            [
                ".claude-plugin/plugin.json",
                ".codex-plugin/plugin.json",
                "DIRECTION.md",
                "README.md",
                "VERSION",
                "scripts/seed-issue-taxonomy.sh",
                "skills/issues/SKILL.md",
                "skills/issues/reference/taxonomy.md",
                "skills/setup-ci-marketplace/SKILL.md",
            ],
            sorted(
                path.relative_to(PLUGIN).as_posix()
                for path in PLUGIN.rglob("*")
                if path.is_file() and path.name != ".DS_Store"
            ),
        )
        # R2: the directory name must equal the skill's frontmatter `name`,
        # because host discovery keys on the directory.
        skill = (PLUGIN / "skills" / "issues" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("\nname: issues\n", skill)

    def test_the_staging_copies_are_gone(self) -> None:
        """spec-0005 S10/R12: publication moves rather than copies.

        Negatives only. An earlier form also asserted that
        `migration/legacy-mapping.md` is still staged, which Lane A will make
        false when the mapping rides the decision to `kodhama/kodhama` — a
        test that must be deleted the day it matters is worse than no test.
        R12 is established by these three absences together with the closed
        inventory in `test_the_package_inventory_is_closed`.

        Reachable on a `conductor/`-only PR, because the CI filter now names
        this subtree.
        """
        staged = ROOT / "conductor" / "wave-issue-taxonomy" / "plugin"
        for leftover in ("skills", "scripts", "DIRECTION.md"):
            self.assertFalse(
                (staged / leftover).exists(),
                f"{leftover} is still staged: publication copied instead of moving",
            )

