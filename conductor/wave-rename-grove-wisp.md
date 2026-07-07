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

- [x] GitHub: rename `kodhama/espalier` → `kodhama/grove` (redirects on)
- [x] GitHub: rename `kodhama/espial` → `kodhama/wisp` (redirects on)
- [x] GitHub: wisp repo description updated (old one said "watching the espalier")
- [x] Local checkouts moved (`~/Projects/grove`, `~/Projects/wisp`) + remotes re-pointed
- [x] kodhama meta: CLAUDE.md family links → grove/wisp (this branch)
- [x] kodhama meta: 0003 status bump `gated → approved` recording PR #2 merge (this branch)
- [x] grove: forward-looking sweep — [grove PR #4](https://github.com/kodhama/grove/pull/4) (docs/ deliberately excluded: the in-flight LP sitting owns it)
- [x] wisp: forward-looking sweep — [wisp PR #3](https://github.com/kodhama/wisp/pull/3) (26/26 tests pass; server smoke-booted on the renamed bus path)
- [x] design-system: icon renames + label sweep — [design-system PR #2](https://github.com/kodhama/design-system/pull/2)
- [x] trellis: verified clean (binary-tolerant re-grep) — no PR needed
- [x] Report appended below; wave closed pending PR merges

## Parked

(none — the one candidate, LP-sitting timing, was pre-answered by the
maintainer: "already told it")

## Report

Executed 2026-07-07, same day as ratification. Four PRs await merge:
this one (ledger + CLAUDE.md links + 0003 status bump), grove #4,
wisp #3, design-system #2. GitHub renames and repo description are live
(redirects on); local checkouts moved and re-pointed.

Deviations and findings, said loudly:

1. **Ledger rides a PR, not main.** Conductor practice here commits the
   brief straight to main; the harness policy in this session requires
   PRs for main. The wave brief therefore lands via this wave PR — same
   content, one extra merge.
2. **`ESPALIER_PORT` → `WISP_PORT`** (wisp PR): the wisp server's own
   port env var — inside AC2's "no forward-looking old names" but not in
   0003 §3's enumerated list. Scope addition, called out in the PR.
3. **Root cause fixed: a raw NUL byte in wisp's `protocol.ts`** (inside
   a template-literal composite key) made `grep`/`file` treat the file
   as binary and silently skip it — it was invisible to this wave's own
   first inventory and would corrupt every future sweep. Replaced with
   the equivalent six-character escape (identical runtime string; 26/26
   tests pass). All four repos then re-verified with binary-tolerant
   grep; no other affected files (trellis's only binary file is an empty
   `docs/.nojekyll`).
4. **grove/docs/ untouched by design**: the LP design sitting owns it
   and has the new name from the maintainer directly.
5. Historical records keep old names per 0003 §5 — ADR-0030 quotes,
   grove's specs/0001, wisp's flagged-stale provenance comments, DS
   lift-time lines. Verified remaining occurrences are exactly these.
