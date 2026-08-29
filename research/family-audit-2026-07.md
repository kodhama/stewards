---
id: discovery-family-audit-2026-07
type: discovery
status: gated
depends_on: []
owner: agent
updated: 2026-07-27
provenance: "maintainer-commissioned audit of stewards, trellis, grove, wisp, spore and design-system, 2026-07-26/27, with math-quest read as the consumer; every figure below verified against fresh clones of `main` at the dates given"
---

> **Dated snapshot, 2026-07. Paths below may no longer exist.** `conductor/`
> and `specs/` were deleted by `kodhama-0032` (2026-08-29); links into them
> resolve through git history, not the working tree. The text is left exactly
> as audited — including its own prediction that *"Deletion needs a rule
> change, not a cleanup"*, which is what `kodhama-0032` is.

# Discovery: the family audit of July 2026

A record of what was measured, what earns its keep, and what the audit got wrong.
It decides nothing. Its purpose is that the next person — or the next agent — starts
from evidence instead of re-deriving it.

## The headline measurement

Merged pull requests, 2026-07-22 → 07-26:

| repo | PRs | commits (all branches) |
|---|---:|---:|
| stewards | 29 | 111 |
| wisp | 21 | 66 |
| grove | 20 | 97 |
| trellis | 16 | 34 |
| kodhama · spore · design-system | 2 · 1 · 1 | 2 · 4 · 0 |
| **math-quest — the product** | **7** | **12** |

**~90 PRs and ~310 commits on the scaffolding against 7 PRs and 12 commits on the
product, in five days.** That ratio is the finding; everything below is detail.

## What earns its keep

Verified, and worth defending against future pruning — including mine.

- **Trellis's 14-rule catalog and its delivered readout.** 367 lines reach a consumer.
  Stable three weeks, and it *shrank*: `decision-0021` collapsed a rule, `0038` retired
  the display codes. This is the product.
- **Live `rules.toml` rows** (`trellis/decision-0053`). Edit a row, effective next
  session. **The only decision in the family backed by an experiment** — n=20,
  zero leak, Fisher p=1.000.
- **Grove's charter → adapter generation.** One authored source, 58 digest-stamped
  projections, `npm run check` proves them clean. This is what makes dual-host cheap.
- **Trellis's regenerate-and-diff sync guards.** Five of six are load-bearing; only
  `TestInvariantsPageMatchesCatalog` (a substring scan over a marketing page) is
  cuttable. `TestBundledCatalogInSync` exists because `//go:embed` cannot reach outside
  its package — a language workaround, not over-application.
- **Trellis self-applying through the real install boundary** (`decision-0035`).
  Seven commits since 2026-06-01 touch `.trellis/internal/`, each bundled into the
  payload commit it mirrors. Cheapest correctness guarantee in the family.
- **The recent conductor-brief form.** 63–74 lines, link-dense, honest closure reports,
  and a real stop-and-learn checkpoint. Contrast `wave-consistency-sweep` at 725 lines:
  **a brief over ~100 lines is a smell.**
- **`## Propagation` / `## Recommended next task` in PR bodies** — live and CI-enforced
  in math-quest (`pr-contract.yml`, the PR template, `.grove/config.toml`). Grove-self's
  `"none committed"` is the exception, not the rule.
- **Zero-dependency discipline and the bundle-purity check** in wisp's build.
- **"A convention, not a framework"** for experiments — written down in
  `trellis/eval/experiments/README.md`, and obeyed.
- **The explicit anti-machinery clauses** (`kodhama-0022` AC7, `0023` AC9, `0017`;
  `grove/adr-0036`). These worked. Reuse the pattern.
- **`grove/charters/dispatcher.md`** — not dead. It is the manual the interactive
  session follows; only its cold-agent projection never fires.
- **`trellis/cli/install_script_test.go`** — not a sync guard. It executes `install.sh`
  in temp dirs and proves fail-closed scope resolution, no partial write on corrupted
  fetch, and no git beyond `rev-parse`. It guards a `curl | sh` path into strangers'
  home directories; 867:348 is the right ratio.

## Measured cost of the ceremony

- **One family-wide decision costs six PRs.** `kodhama-0021` took 6 PRs across 4 repos,
  +607 lines, 3 independent adversary reviews and 4 maintainer ratifications — to record
  a hyperlink. `0023` repeated it a day later.
- **Spec mass exceeds implementation mass.** `wisp/spec-0001` is 2,565 lines for a plugin
  whose source is ~2,400. `stewards/specs/0001`+`0002` are 3,343 lines, both superseded.
  `trellis/specs/0008` was authored and superseded within 5.5 hours.
- **Decision size tripled in 27 days** in trellis: mean 66 lines for `0001–0042`,
  156 for `0043–0057`.
- **A role addition costs 42 files** in grove (measured on PR #140), largely because the
  role count is hand-restated in eight places — with **four different values live
  simultaneously**: `plugin.json` says "fourteen" beside a 13-entry array, `README.md`
  says "ten" and "fourteen" one paragraph apart, `CLAUDE.md` says "twelve",
  `adr-0031` says "thirteen".
- **114 remote branches, 111 of them debris** with a merged or closed PR.

## Correctness defects found

All verified by execution or by reading the governing source, not inferred from names.

1. **`/grove:setup` failed on every surface, for two independent reasons.** The CLI
   resolved its own package root one directory short, so it died on the surface matrix
   before any rule ran; and the support gate rejects every non-`remove` operation while
   no row is `supported` (0 of 12 qualify). **First cause fixed** (grove #155); the
   second is `adr-0041`/`spec-0004 v7` territory (grove #149).
2. **Five repos would start with no agent fleet** on a fresh clone — committed
   `enabledPlugins` existed in three, and `extraKnownMarketplaces` in one. **Fixed.**
3. **Seven of eight repos run a stale Trellis overlay**, and math-quest's staleness hook
   has never fired once: a hand-rolled duplicate reads `.trellis/version`, which does not
   exist — the real path is `.trellis/internal/version`. **Diagnosed, not yet fixed.**
4. **An armed landmine in stewards.** `specs/0004` requires a six-part admission report
   under `plugins/kodhama/reference/surfaces/`, enforced by the validator. Neither that
   directory nor the fixtures it names exist; it passes only because the plugin is absent
   from both catalogs. Publishing detonates it. Tracked as **#39**.
5. **`grove/metadata/legacy-ownership.json` is a live migration manifest**, not dead
   weight. Its four recorded SHA-256 values still match in wisp, trellis, design-system,
   spore and math-quest — the migration has not run because setup is broken. Deleting it
   would strand ~20 committed files permanently.
6. **A live safety limit with one test, in the wrong place.** The 4,194,304-byte output
   budget bounding `runSanitizedCommand` is asserted only inside the canary driver's
   tests. Retiring the canary without re-anchoring it leaves the constant unguarded.

## What this audit got wrong

The durable part of the record. Of ten proposed Wave 1 removals, **three withdrew on
contact and a fourth changed direction twice.**

- **Two contradicted a ratified decision.** `grove/adr-0036` D3 — `owner: human` — says
  *"Existing ADRs and specs remain readable as archival records."* Retaining the specs I
  proposed deleting is what was decided the day their runtime was deleted. Their
  retirement banners already sit above every clause, so the "lines a cold agent may load
  and act on" premise was false.
- **One ignored the lifecycle.** `superseded` is terminal and *"the original content is
  never edited away"*. Neither stewards nor grove has ever deleted an artifact from
  `decisions/` or `specs/`. Deletion needs a rule change, not a cleanup — see **#46**.
- **One conflated two mechanisms with similar names.** "Codex CI-proof machinery" was
  ~3,700 lines; roughly half is the Playwright dashboard suite that runs on every PR at
  no API cost, and is the maintainer's own idea. Only the weekly marketplace canary was
  the target.
- **Near-misses caught by checks rather than by reading.** `.grove/agents/<role>.md` are
  repo-owned addenda, not stale charter copies — nine were staged for deletion.
  `trellis`'s `research/0013` was closed-unmerged and is the foundation of the
  configuration-not-vendoring work; the branch sweep would have destroyed the only
  remote copy.

**Common cause: removals proposed from names, line counts and file paths, without
reading what the thing does or which approved artifact governs it.**

**The rule that follows:** trace what actually runs, what depends on it, and which
approved artifact governs it — and report that trace — *before* proposing removal. Where
the trace contradicts a ratified decision, supersede it openly rather than route around
it. Applied from 2026-07-27; it is why `wisp/adr-0018` cost two drafts and two
independent adversary passes.

## Scope note

This artifact records findings. It authorises nothing, supersedes nothing, and is not a
propagation target. The consolidation work it informs is tracked in
[`conductor/wave-0024-family-consolidation.md`](../conductor/wave-family-consolidation.md).
