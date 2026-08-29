"""Install-door tests.

What remains after `kodhama-0030` emptied the catalogs of everything but
trellis: the surviving catalog entry, the scope block its three carriers
mirror, and the guard that keeps the retired surface/observation shape from
growing back. The package, workflow-authoring and issue-skill publication
tests went with `plugins/kodhama/`, which no longer exists.
"""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLAUDE_CATALOG = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_CATALOG = ROOT / ".agents" / "plugins" / "marketplace.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CatalogTests(unittest.TestCase):
    def test_trellis_codex_preview_catalog_entry_makes_no_support_claim(
        self,
    ) -> None:
        """trellis decision-0063 and kodhama-0021 AC2."""
        codex_trellis = [
            entry
            for entry in load(CODEX_CATALOG)["plugins"]
            if entry["name"] == "trellis"
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
            entry
            for entry in load(CLAUDE_CATALOG)["plugins"]
            if entry["name"] == "trellis"
        ]
        self.assertEqual(1, len(claude_trellis))
        self.assertEqual(
            (
                "Install and consult Trellis in a Claude Code project: "
                "the invariants, expressed at your strength."
            ),
            claude_trellis[0]["description"],
        )

    def test_the_door_serves_only_what_kodhama_0030_left_standing(self) -> None:
        """`kodhama-0030` D1: grove, kodhama and wisp are delisted on both hosts.

        Asserted as an exact membership rather than three absences, so a
        fourth name cannot be added to either catalog without this test
        saying so. `kodhama-0030` D4 is what a re-listing has to supersede;
        this is the check that makes the supersession non-optional.
        """
        for path in (CLAUDE_CATALOG, CODEX_CATALOG):
            catalog = load(path)
            self.assertEqual("kodhama", catalog["name"], path)
            self.assertEqual(
                ["trellis"],
                [entry["name"] for entry in catalog["plugins"]],
                path,
            )

    def test_no_carrier_still_offers_the_delisted_plugins(self) -> None:
        """`kodhama-0030` D2: the repository does not enable what it will not serve.

        `.claude/settings.json` enabled `grove@kodhama` and `kodhama@kodhama`
        from this very door. Delisting them there and leaving them enabled
        here would have left the repository pointing at install strings its
        own catalog can no longer resolve.
        """
        settings = load(ROOT / ".claude" / "settings.json")
        self.assertEqual(
            {"trellis@kodhama": True}, settings["enabledPlugins"]
        )

    def test_the_retired_package_left_no_carriers_behind(self) -> None:
        """`kodhama-0030` D3: the deleted package's machinery is gone with it.

        Named paths rather than a tree walk, because each of these was a
        *reason to keep the package* — a validator, an admission check, a
        fixture corpus — and a half-deletion that stranded one of them would
        otherwise sit green.
        """
        for relative in (
            "plugins",
            "scripts/validate_kodhama_plugin.py",
            "scripts/keyless_admission_check.py",
            "tests/fixtures",
        ):
            self.assertFalse(
                (ROOT / relative).exists(), f"{relative} outlived the package"
            )


class RepositoryShapeTests(unittest.TestCase):
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

    def test_the_distribution_scope_block_is_mirrored_exactly(self) -> None:
        """spec-0005 S14: three hand-mirrored copies, byte for byte.

        `distribution/repository-scope.md` is canonical and `CLAUDE.md` and
        `README.md` copy it by hand, which is exactly the arrangement that
        drifts. Byte identity is asserted rather than "says roughly the same
        thing", because a paraphrase is how one copy quietly outlives the
        others.

        **Disclosed limit:** none of the three files is in the CI `paths:`
        filter, so this fires on any PR that also touches a gated path — and
        not on a PR editing only `CLAUDE.md`. Putting them in the filter would
        drag `CLAUDE.md` and `README.md` into the test gate, which is the cost
        the narrow-filter ruling declines to pay for a prose edit. The residual
        gap is inherent, not overlooked.
        """
        begin = "<!-- distribution-scope:begin -->"
        end = "<!-- distribution-scope:end -->"
        blocks: dict[str, str] = {}
        for name in (
            "distribution/repository-scope.md",
            "CLAUDE.md",
            "README.md",
        ):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertEqual(1, text.count(begin), name)
            self.assertEqual(1, text.count(end), name)
            blocks[name] = text.split(begin, 1)[1].split(end, 1)[0]
        self.assertEqual(1, len(set(blocks.values())), blocks)


if __name__ == "__main__":
    unittest.main()
