"""Kodhama plugin tests derived from specs 0003@v1 and 0004@v2."""

from __future__ import annotations

import collections
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

    def test_every_payload_relative_pointer_resolves(self) -> None:
        """spec-0005 S7/R6: no shipped file points at something that is gone.

        The extraction rule is the spec's, and the `/` qualifier belongs on
        the **token**, not on the pattern's tail. An earlier form required a
        `/` *after* the first path component, which `../../../DIRECTION.md`
        does not have — so it returned no match and passed against a
        genuinely dangling pointer.

        The qualifier is required rather than incidental:
        `skills/issues/reference/taxonomy.md` names bare `SKILL.md` three
        times, and without it those become demands that
        `skills/issues/reference/SKILL.md` exist, which it must not.

        A bounded heuristic, stated so it is not mistaken for more: it sees
        path-shaped tokens ending `.md` or `.sh`, and skips anything a `://`
        introduces.
        """
        token = re.compile(r"(?:\.\.?/)*[\w.-]+(?:/[\w.-]+)*\.(?:md|sh)")
        dangling: list[str] = []
        for path in sorted(PLUGIN.rglob("*")):
            if not path.is_file() or path.suffix not in (".md", ".sh"):
                continue
            text = path.read_text(encoding="utf-8")
            for match in token.finditer(text):
                pointer = match.group(0)
                if "/" not in pointer:
                    continue
                if text[max(0, match.start() - 3) : match.start()] == "://":
                    continue
                if not (path.parent / pointer).resolve().exists():
                    rel = path.relative_to(ROOT).as_posix()
                    dangling.append(f"{rel} -> {pointer}")
        self.assertEqual([], dangling)

    def test_capabilities_enumerates_the_skill_directories(self) -> None:
        """spec-0005 R16: one element per skill directory, derived not
        remembered.

        The rule is stated so it is checkable: `interface.capabilities` shall
        contain exactly one element per directory under
        `plugins/kodhama/skills/`, in the order those names sort, each
        containing `skills/<directory-name>`. That makes the array's length,
        ordering and membership derivable from the package, so this compares
        it against the filesystem rather than against a remembered list.

        `is_dir()` guards the derivation: a stray `.DS_Store` or a `README.md`
        beside the skill directories would otherwise make the *expected*
        array wrong and fail a correct package.
        """
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        capabilities = manifest["interface"]["capabilities"]
        directories = sorted(
            entry.name for entry in (PLUGIN / "skills").iterdir() if entry.is_dir()
        )
        self.assertEqual(len(directories), len(capabilities), capabilities)
        for directory, capability in zip(directories, capabilities):
            self.assertIn(f"skills/{directory}", capability)

    def test_seed_script_is_runnable_and_fails_closed(self) -> None:
        """spec-0005 S4: the actuator ships runnable, and refuses what it
        does not understand.

        Both invocations return before any `gh` call, so this needs no
        network and no credentials — an actuator's test that reached the
        network would be the actuator running.

        The executable bit is asserted rather than assumed: publication moved
        this file with `git mv`, and a copy-then-delete would have dropped
        `100755` silently, leaving a script the host can read and nobody can
        run.
        """
        script = PLUGIN / "scripts" / "seed-issue-taxonomy.sh"
        self.assertTrue(os.access(script, os.X_OK), "the actuator is not executable")

        syntax = run("bash", "-n", str(script), check=False)
        self.assertEqual(0, syntax.returncode, syntax.stderr)

        helped = run(str(script), "--help", check=False)
        self.assertEqual(0, helped.returncode, helped.stderr)
        self.assertIn("Dry-run by default", helped.stdout)

        # Fail closed: an argument it does not recognise is an operator
        # error on a script that can create org-level state.
        bogus = run(str(script), "--bogus", check=False)
        self.assertEqual(2, bogus.returncode, bogus.stdout)
        self.assertIn("unknown argument: --bogus", bogus.stderr)

    def test_the_skill_never_reaches_the_actuator(self) -> None:
        """spec-0005 S5/R3: instruction and actuator stay apart.

        `scripts/seed-issue-taxonomy.sh` creates org issue types and
        repository labels; the skill only teaches. Everything under `skills/`
        is agent-reachable context by construction, and the staging record
        states the cost of merging the two: bundling an actuator into
        reference content is what forced guardrails into the first draft.

        So an agent that reads the skill learns the convention and cannot
        learn, *from the skill*, that a provisioning command exists. A later
        reader who moves the script under `skills/` to "keep the skill
        together" reverses this, and fails here.

        This constrains `skills/` only. The shipped `README.md` names the
        actuator by design — hiding it from the skill is context safety;
        hiding it from the human who installed the package is not — and S16
        requires it there.

        `gh api --method POST` is banned, not `gh api`: the shipped
        `SKILL.md` requires the `gh api /orgs/<org>/issue-types` probe under
        S8, so banning the broader form would make two criteria contradict
        and go red on a correct package.
        """
        skills = PLUGIN / "skills"
        # R3's first clause. The scan below cannot establish it: a script
        # moved to `skills/issues/` is neither a `SKILL.md` nor a reference,
        # so nothing would read it and the "keep the skill together"
        # reversal would pass the very test that names R3. The closed
        # inventory does catch it — measured — but the requirement belongs
        # here too, where a reader looks for it.
        self.assertEqual(
            [],
            [
                path.relative_to(PLUGIN).as_posix()
                for path in sorted(skills.rglob("*"))
                if path.is_file() and path.name == "seed-issue-taxonomy.sh"
            ],
            "the actuator moved under skills/, where everything is "
            "agent-reachable by construction",
        )

        scanned: list[Path] = []
        for path in sorted(skills.rglob("*")):
            if not path.is_file():
                continue
            parts = path.relative_to(skills).parts
            if path.name == "SKILL.md" or "reference" in parts:
                scanned.append(path)
        self.assertTrue(scanned, "no skill content was scanned")
        for path in scanned:
            text = path.read_text(encoding="utf-8")
            for forbidden in (
                "seed-issue-taxonomy",
                "gh label create",
                "gh api --method POST",
            ):
                self.assertNotIn(forbidden, text, path.relative_to(ROOT).as_posix())

    def test_the_migration_mapping_stays_out_of_the_package(self) -> None:
        """spec-0005 S6/R4: the mapping is not published.

        Two independent reasons, both already written down. It is not
        standing agent context — its own header says a mapping table plus
        occurrence counts reads as a backlog-sweep plan, and no agent should
        be handed one as ambient context. And it authorises nothing:
        `kodhama-0026` open question 5 leaves migration unauthorised, while a
        file shipping with an installable plugin reads as available to act
        on.

        A later reader who "reunites" the mapping with the skill it explains
        reverses both, and fails here. Walked with `rglob` rather than
        matching two exact paths, so a rename does not walk past it.
        """
        offenders = []
        for path in sorted(PLUGIN.rglob("*")):
            rel = path.relative_to(PLUGIN).as_posix()
            if path.is_dir() and path.name == "migration":
                offenders.append(f"{rel}/ (migration directory)")
            if path.is_file() and path.name == "legacy-mapping.md":
                offenders.append(f"{rel} (the mapping itself)")
        self.assertEqual([], offenders)

    def test_the_in_force_gate_ships_intact(self) -> None:
        """spec-0005 S8/R9: the shipped skill still stops when it must.

        `kodhama-0026` D12 makes the convention inert until all six issue
        types exist **and are enabled**, and the skill's own first
        instruction is to check that and stop. This is the single clause that
        makes publication a non-event for every repository, so it is asserted
        literally rather than trusted to survive an edit.

        The six type names are quoted from `kodhama-0026` D2 **as check
        inputs**. This test owns neither their membership nor their meaning.

        Normalised whitespace, so a re-wrap cannot make a required sentence
        "absent" and quietly weaken the guard.
        """
        text = " ".join(
            (PLUGIN / "skills" / "issues" / "SKILL.md")
            .read_text(encoding="utf-8")
            .split()
        )
        self.assertIn("gh api /orgs/<org>/issue-types", text)
        # Selection on `is_enabled`, not on presence: a disabled type still
        # appears in the list and still cannot be set on an issue.
        self.assertIn("select(.is_enabled)", text)
        self.assertIn("**Select on `is_enabled`**", text)
        for issue_type in ("Bug", "Feature", "Task", "Research", "Decision", "Epic"):
            self.assertIn(f"`{issue_type}`", text)
        self.assertIn(
            "**If any of the six is absent or disabled** — `Bug`, `Feature`, "
            "`Task`, `Research`, `Decision`, `Epic` — **this convention is not "
            "yet in force in that org.** Say so and stop.",
            text,
        )

    def test_the_actuator_gh_surface_is_pinned(self) -> None:
        """spec-0005 S9/R11: a closed multiset, not a denylist.

        The previous form called itself an allowlist and implemented a
        denylist. Injected into this same script, four of five added mutating
        commands survived it. A denylist can only forbid what someone thought
        of; pinning the whole surface means **any** added `gh` invocation
        changes the multiset, whatever its verb.

        Two of the nine occurrences are prose — the sentence "your gh token
        lacks the 'admin:org' scope" and the advice printed under it. The
        extractor does not model shell quoting, so both are counted.
        Excluding them would need a shell parser; including them means
        editing those two sentences trips this test and a human re-confirms
        the surface. Cheap, and fail-safe for an actuator.

        The head for the prose line is `gh token lacks`, not `gh token`: the
        second group is optional but **greedy**. Anyone changing the
        extractor must re-derive this table from it rather than reconciling
        the two by eye — an arbiter that fails where it should pass teaches
        its reader to override the check.
        """
        script = PLUGIN / "scripts" / "seed-issue-taxonomy.sh"
        text = script.read_text(encoding="utf-8")
        heads = collections.Counter(
            " ".join(part for part in ("gh", *match.groups()) if part)
            for match in re.finditer(
                r"\bgh\s+([a-z][a-z-]*)(?:\s+([a-z][a-z-]*))?", text
            )
        )
        self.assertEqual(
            {
                "gh api": 3,
                "gh auth refresh": 1,
                "gh auth status": 1,
                "gh issue list": 1,
                "gh label create": 1,
                "gh label list": 1,
                "gh token lacks": 1,
            },
            dict(heads),
        )

        # The multiset alone cannot see a same-head substitution: swapping
        # `--method PATCH` for `--method DELETE` leaves the head `gh api` and
        # the count at three. The literals are what catch it.
        for mutating in (
            'gh api --method POST "/orgs/$ORG/issue-types"',
            'gh api --method PATCH "/orgs/$ORG/issue-types/$id"',
            'gh label create "$name" -R "$ORG/$repo"',
        ):
            self.assertIn(mutating, text)

        # Command forms, not the bare substring `delete`: the file promises
        # the opposite of what a substring ban would forbid, in four separate
        # sentences ("This script NEVER deletes a label", "Reported, never
        # deleted", "now redundant, NOT deleted", "No label is ever deleted").
        for forbidden in (
            "gh label delete",
            "gh issue delete",
            "gh repo delete",
            "--method DELETE",
            "--method PUT",
            "-X DELETE",
            "-X PUT",
        ):
            self.assertNotIn(forbidden, text)

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

