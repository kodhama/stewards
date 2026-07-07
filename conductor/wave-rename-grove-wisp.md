# Wave: rename espalier→grove, espial→wisp (execution of kodhama-0003)

Opened 2026-07-07. Authorization: `kodhama-0003-family-naming` ratified
(PR #2 merged) + maintainer's explicit go-ahead ("go ahead with the
renames. feel free to move the repos."). Scope is 0003 §Rename scope,
fixed; anything outside it parks.

Rules applied: historical records keep old names (0001/0002 ratified
text, ADR-0030 lineage quotes, provenance sections, past briefs);
forward-looking surfaces rename; gardeners/furrows/head-gardener
vocabulary unchanged; icon drawings unchanged (labels only); DS
provenance/lore layer is NOT this wave (T2 design pass owns it).

## Ledger

- [ ] GitHub: rename `kodhama/espalier` → `kodhama/grove` (redirects on)
- [ ] GitHub: rename `kodhama/espial` → `kodhama/wisp` (redirects on)
- [ ] GitHub: wisp repo description updated (old one said "watching the espalier")
- [ ] Local checkouts moved (`~/Projects/grove`, `~/Projects/wisp`) + remotes re-pointed
- [ ] kodhama meta: CLAUDE.md family links → grove/wisp (this commit)
- [ ] kodhama meta: 0003 status bump `gated → approved` recording PR #2 merge (this commit)
- [ ] grove: forward-looking sweep (README, CONTRIBUTING, charters, agents, `espalier-status` skill → `grove-status`, specs/decisions READMEs, docs/lp-content + docs/index.html, `.trellis/profile.md`) — PR
- [ ] wisp: forward-looking sweep (README, code strings `.espalier/`→`.grove/`, `$ESPALIER_EVENTS`→`$GROVE_EVENTS`, `<ESPIAL_VENDOR_PATH>`→`<WISP_VENDOR_PATH>`, package.json name, dashboard.html, .gitignore, docs) — PR
- [ ] design-system: icon file renames + grammar/identity/patterns label sweep — PR
- [ ] trellis: verified clean (grep found zero references) — no PR needed
- [ ] Report appended below; wave closed

## Parked

(none yet; ≤3 before batching to the human)

## Report

(appended at close)
