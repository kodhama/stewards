# stewards — the collective's coordination hub

The **stewards** are [kodhama](https://github.com/kodhama/kodhama)'s worker
collective — the scaffolding that tends the forest's trees (the products)
and tends itself. This repo is their coordination hub: it continues the
operational role formerly held by `kodhama/kodhama`, relocated here per
`kodhama-0009` so the kodhama repo can be the forest-spirit front door. Its
three long-standing jobs are cross-collective **decisions**, the **conductor
seat**, and the **install door** (the collective's canonical install
repository per `kodhama-0002`, `kodhama-0012`, and `kodhama-0017`) — but what
belongs here is settled by the rule below, not by that list.

<!-- distribution-scope:begin -->
The install door includes the host-native Claude and Codex catalogs. Those
catalogs list plugins this repository does not originate — each of those is
sourced from the repository that owns it. The only plugin **originated here**
is `kodhama`, which carries two skills and one provisioning script: verified
Claude/Codex marketplace setup for CI, the kodhama issue convention (staged
here while the issue skill's home is decided), and a dry-run-by-default
label-and-type seeder. That is a description of present contents, not a scope:
it moves when the contents move. The install door does not certify product
releases or support and owns no universal version, tag, release-history,
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
- **Work is tracked in GitHub issues**, typed and labelled per
  `kodhama-0026`; a cross-repo wave is an `Epic` with dependency edges
  (`kodhama-0027`). A conductor brief may hold narrative that has no issue
  shape — the reasoning behind a sequence, a trace justifying a removal, a
  closure report — but **never a work list**: 12 of 14 briefs went stale, and
  the one reconciled twice drifted the same way both times, because a brief
  duplicates state that issues update as a side effect of the work.
  Parked questions still batch to the human ≤3 at a time.
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
done; the **test gate** runs on any PR touching `tests/`, the two plugin
scripts under `scripts/`, `plugins/kodhama/`, the plugin subtree of the
issue-taxonomy staging tree (`conductor/wave-issue-taxonomy/plugin/`), either
marketplace catalog, or the validation workflow itself — and on nothing else,
so a docs-only PR pays none of its cost. It is not the only check: the Claude
review and the workflow-parity job carry no `paths:` filter and run on every
PR. There is no typecheck gate. A parked
item is an issue — `kodhama-0027` D2 removed the briefs' Parked sections
along with the rest of the ledger, and the last brief closed as archive on
2026-08-02. Telemetry: wisp is not vendored
here and no grove-status skill is installed — optional by construction.

<!-- grove:begin (managed by grove — dials live in .grove/, not this block) -->
Load the complete driving-session dispatcher from `${CLAUDE_PLUGIN_ROOT}/reference/charters/dispatcher.md` in this current task.
Load the complete interactive shaper from `${CLAUDE_PLUGIN_ROOT}/reference/charters/shaper.md` in this current task.
Do not delegate or spawn either driving-session role. A native dispatcher remains only the scoped advisor.
At every handover, an absent `runtime_dir` resolves `runtime/gates/` relative to the active installed Grove package. A declared non-legacy runtime is exact authority and is never searched or replaced.
grove plugin@0.3.0
<!-- grove:end -->
