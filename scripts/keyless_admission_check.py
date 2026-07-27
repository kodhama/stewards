#!/usr/bin/env python3
"""Keyless catalog-admission evidence for the Kodhama plugin.

Decision `kodhama-0018` §3 requires catalog admission to be a separate evidenced
act, and permits that evidence to be "a bounded host-native package and skill
invocation test" kept in this repository and reviewed with the catalog change.

Spec 0004 v2 elaborated that into a hand-written six-part smoke report at
`plugins/kodhama/reference/surfaces/<host>-catalog-admission-<version>.md`,
against fixtures under `plugins/kodhama/tests/fixtures/`. Neither path has ever
existed, so the requirement could not be met — and it stayed invisible only
because the plugin is absent from both catalogs, leaving the enforcing branch
unreachable. Publishing would have failed CI on an unproducible artifact.

This replaces the report with a check that runs. It installs the built plugin
through the real Claude plugin path and asserts the host exposes the declared
skill.

What it proves, precisely, because the difference matters:

- The package **installs from a catalog** through the real
  `marketplace add` → `install` path. This is the substantive part, and it fails
  closed — a package the host will not take does not get here.
- The manifest **validates cleanly**, warnings included. A stub manifest is
  reported by the CLI as "passed with warnings", so warnings are treated as
  failure; otherwise a manifest missing `version` would pass.
- The host's component inventory **matches the declared skill directories**.

What it does **not** prove, measured rather than assumed: the host reports a
skill directory in its inventory even when `SKILL.md` has no frontmatter at all,
so this is closer to a layout check than a load check — and it certainly does
not show the skill *runs*. Confirming that needs a model turn, which costs a key.

`kodhama-0018` §3 says the evidence "may be" a bounded package and skill
invocation test, not that it must be. This satisfies the package half honestly
and leaves the invocation half unmet rather than dressing up a directory listing
as behavioural proof.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "kodhama"
MARKETPLACE = "kodhama-local"


def claude(args: list[str], config_dir: Path, cwd: Path) -> str:
    """Run the CLI, returning combined output.

    Failures are reported on stdout with a ✘ marker while still exiting 0 on
    some paths, so callers assert on text rather than trusting the exit code.
    """
    result = subprocess.run(
        ["claude", *args],
        cwd=cwd,
        env={**__import__("os").environ, "CLAUDE_CONFIG_DIR": str(config_dir)},
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


def fail(message: str, context: str) -> None:
    sys.stderr.write(f"keyless-admission-check: {message}\n{context}\n")
    raise SystemExit(1)


def declared_skills() -> list[str]:
    return sorted(p.parent.name for p in (PLUGIN / "skills").glob("*/SKILL.md"))


def main() -> None:
    expected = declared_skills()
    if not expected:
        fail("the plugin declares no skills", str(PLUGIN / "skills"))

    with tempfile.TemporaryDirectory(prefix="kodhama-admission-") as workspace:
        work = Path(workspace)
        config_dir, marketplace, project = work / "config", work / "mk", work / "project"
        for path in (config_dir, project, marketplace / ".claude-plugin"):
            path.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", "."], cwd=project, check=True)

        # A local catalog carrying this commit's payload, so the check exercises
        # what the PR would publish rather than what is already published.
        shutil.copytree(PLUGIN, marketplace / "kodhama")
        (marketplace / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps(
                {
                    "name": MARKETPLACE,
                    "owner": {"name": "kodhama-ci"},
                    "plugins": [
                        {
                            "name": "kodhama",
                            "description": "package under test",
                            "source": "./kodhama",
                        }
                    ],
                },
                indent=2,
            )
            + "\n"
        )

        # `kodhama-0018` §3 requires a *valid* host package before admission.
        # Skills load from the directory rather than the manifest, so install
        # and exposure alone would pass a malformed manifest.
        validated = claude(["plugin", "validate", str(PLUGIN)], config_dir, project)
        # The CLI reports a stub manifest as "passed with warnings", so accepting
        # any "Validation passed" would let a manifest missing `version` through.
        if "Validation passed" not in validated or "warning" in validated.lower():
            fail("host did not cleanly validate the plugin manifest", validated)

        added = claude(["plugin", "marketplace", "add", str(marketplace)], config_dir, project)
        if "Successfully added marketplace" not in added:
            fail("marketplace add failed", added)

        installed = claude(
            ["plugin", "install", f"kodhama@{MARKETPLACE}", "--scope", "local"],
            config_dir,
            project,
        )
        if "Successfully installed plugin" not in installed:
            fail("plugin install failed", installed)

        details = claude(["plugin", "details", f"kodhama@{MARKETPLACE}"], config_dir, project)
        match = re.search(r"Skills \((\d+)\)\s+(.+)", details)
        if not match:
            fail("host reported no skill inventory", details)

        exposed = sorted(name.strip() for name in match.group(2).split(",") if name.strip())
        if exposed != expected:
            fail(f"host exposed {exposed}, plugin declares {expected}", details)

    print(
        "keyless-admission-check: "
        f"installed from a catalog and exposed {', '.join(expected)} — no model turn"
    )


if __name__ == "__main__":
    main()
