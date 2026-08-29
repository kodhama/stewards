# stewards — the collective's coordination hub

The **stewards** are [kodhama](https://github.com/kodhama/kodhama)'s worker
collective. This repo is their coordination hub, holding the operational role
formerly in `kodhama/kodhama` (`kodhama-0009`): cross-collective **decisions**,
the **conductor seat**, and the **install door**. What belongs here is settled
by the rules below, not by that list.

<!-- distribution-scope:begin -->
The install door includes the host-native Claude and Codex catalogs. Both
catalogs list `trellis` and nothing else, sourced from the repository that
owns it. This repository **originates no plugin**: the `kodhama` package it
used to carry was deleted along with its listing (`kodhama-0030`), and grove
and wisp were delisted in the same act. That is a description of present
contents, not a scope: it moves when the contents move. The install door does
not certify product releases or support and owns no universal version, tag,
release-history, approval, runtime-sandbox, cross-repository-resolution, or
effective-support machinery.
<!-- distribution-scope:end -->

Decisions here keep the `kodhama-NNNN` id namespace — collective (steward)
layer; spirit/org decisions live in `kodhama/kodhama` (`kodhama-0009`).

The stewards: [trellis](https://github.com/kodhama/trellis) (governance) ·
[grove](https://github.com/kodhama/grove) (agent swarm) ·
[wisp](https://github.com/kodhama/wisp) (runtime observability) ·
[design-system](https://github.com/kodhama/design-system) (brand) ·
[homebrew-tap](https://github.com/kodhama/homebrew-tap) (delivery).
Dependency direction is strictly downward (wisp → grove → trellis).
**Trellis carries the principles; grove carries the operating model.** Repos,
this one included, restate neither (`kodhama-0008`) — so if you find yourself
explaining *why* a rule exists here, the explanation belongs in its decision.

Rules (the collective's):
- **Decisions are append-only** — frontmatter `id/type/status/depends_on/owner`;
  supersede with a forward pointer, never edit a ratified decision.
- **One home per kind of information.** Product truths live in product repos.
  When in doubt, it belongs to a product.
- **Work is not tracked here.** `kodhama-0031` retired the GitHub-issues
  mandate and the `kodhama-0026` taxonomy with it; work moves to Linear, and
  which remaining backlogs port is open by choice. Briefs in `conductor/` are
  archive — not updated, never read as current state, and never deleted
  (`kodhama-0027` D5, which outlives the tracker). A parked item is a tracker
  item, not a file here.
- **Model economy**: Sonnet-class for execution; strongest model only for
  design/judgment sittings.
- The trellis overlay is what this repo installs on itself — run
  `trellis setup` if the CLI is available, otherwise say so.

This repo is **grove-managed**: agent roles arrive from the grove plugin as
`grove:<role>`, never vendored here (`grove/adr-0026` D1). That plugin is
retired from this catalog and no door is planned (`kodhama-0030`), so grove
reaches this repo by an already-installed copy or a direct source install.
Two placeholders are resolved locally.

The test gate is `python3 -m unittest discover -s tests` — run it before
reporting done. CI runs it on any PR touching `tests/`, either marketplace
catalog, `.claude/settings.json`, or the validation workflow, and on nothing
else. The Claude review and the parity job carry no `paths:` filter and run on
every PR. There is no typecheck gate.

<!-- grove:begin (managed by grove — dials live in .grove/, not this block) -->
Load the complete driving-session dispatcher from `${CLAUDE_PLUGIN_ROOT}/reference/charters/dispatcher.md` in this current task.
Load the complete interactive shaper from `${CLAUDE_PLUGIN_ROOT}/reference/charters/shaper.md` in this current task.
Do not delegate or spawn either driving-session role. A native dispatcher remains only the scoped advisor.
At every handover, an absent `runtime_dir` resolves `runtime/gates/` relative to the active installed Grove package. A declared non-legacy runtime is exact authority and is never searched or replaced.
grove plugin@0.3.0
<!-- grove:end -->
