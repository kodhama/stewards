# stewards — the collective's coordination hub

The **stewards** are [kodhama](https://github.com/kodhama/kodhama)'s worker
collective — the scaffolding that tends the forest's trees (the products)
and tends itself. This repo is their coordination hub: it continues the
operational role formerly held by `kodhama/kodhama`, relocated here per
`kodhama-0009` so the kodhama repo can be the forest-spirit front door.
THREE things live here and nothing else: **cross-collective decisions**
(`decisions/`), the **conductor seat** (`conductor/` — wave briefs and
ledgers for work that spans the collective's repos), and the **install
door** (the collective's canonical install repository per `kodhama-0002`,
`kodhama-0012`, and `kodhama-0017`).

<!-- distribution-scope:begin -->
The install door includes the host-native Claude and Codex catalogs. Its
future distribution scope is deliberately narrow: metadata that records which
marketplace a test exercised, and a generic Stewards skill that adds
caller-selected Claude/Codex marketplace setup to CI. It does not certify
product releases or support and owns no universal version, tag, release-history,
approval, runtime-sandbox, cross-repository-resolution, or effective-support
machinery.
<!-- distribution-scope:end -->

Decisions made here keep the `kodhama-NNNN` id namespace — they are kodhama
decisions made at the collective (steward) layer; spirit/org-level decisions
live in `kodhama/kodhama` (see `kodhama-0009`).

The stewards: [trellis](https://github.com/kodhama/trellis) (governance) ·
[grove](https://github.com/kodhama/grove) (agent swarm) ·
[wisp](https://github.com/kodhama/wisp) (runtime observability) ·
[design-system](https://github.com/kodhama/design-system) (brand asset,
git-tag versioned) · [homebrew-tap](https://github.com/kodhama/homebrew-tap)
(delivery).
Dependency direction is strictly downward
(wisp → grove → trellis); the DS reaches consumers only through
generation-time links. Layering: **trellis carries the principles; grove
carries the operating model** — mechanics included. Repos, this one
included, restate neither (`kodhama-0008`). This hub sits above all of them
and none of them know it.

Rules (the collective's):
- **Decisions are append-only** — markdown with frontmatter
  (`id/type/status/depends_on/owner`); supersede with a forward pointer,
  never edit a ratified decision.
- **One home per kind of information** — product truths live in product
  repos; only genuinely cross-collective content lands here. When in doubt,
  it belongs to a product.
- **Conductor practice**: each cross-repo wave gets a brief in
  `conductor/`; the brief IS the ledger — check items off in the same
  commits that report them; parked questions batch to the human ≤3 at a
  time; every wave ends with a report appended to its brief.
- **Model economy**: Sonnet-class for execution waves; strongest model
  only for design/judgment sittings (see the suite-lift plan §Model
  economy, until that section migrates here).
- This repo runs the kodhama stack on itself once grove + wisp are
  liftable; until then the trellis overlay alone is owed — if the
  `trellis` CLI is available run `trellis setup`, otherwise record the
  debt in `conductor/` loudly.

This repo is **grove-managed**: conductor work items run as
[grove](https://github.com/kodhama/grove) runs, and the agent roles arrive
from the grove plugin as `grove:<role>` — never vendored here (`grove/adr-0026`
D1; the stale vendored copies were removed in #52). Two placeholders are
resolved locally. The test gate is `python3 -m unittest discover -s tests`
plus `python3 scripts/validate_kodhama_plugin.py` — run both before reporting
done; CI enforces them on any PR touching `tests/`, `scripts/`, `plugins/`, or
either marketplace catalog, and on nothing else, so a docs-only PR gets no
check at all. There is no typecheck gate. Parked items ride the conductor
briefs' Parked sections. Telemetry: wisp is not vendored here and no
grove-status skill is installed — optional by construction.

<!-- grove:begin (managed by grove — dials live in .grove/, not this block) -->
Grove is installed. Run /grove:start to open a governed run, or /grove:enter to make Grove's dispatch rules available without opening one.
grove plugin@0.4.0
<!-- grove:end -->
