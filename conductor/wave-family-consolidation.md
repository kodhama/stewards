# Wave: family consolidation

Opened 2026-07-26. Evidence:
[`discovery-family-audit-2026-07`](../research/family-audit-2026-07.md).

## Scope

Act on the July 2026 audit in reviewable slices: fix what is broken first, then remove
what is genuinely dead, then cut recurring ceremony. Each slice lands as its own PRs and
is reviewed before the next opens.

The full working plan lives outside the repo with the maintainer; this brief is the
ledger and the closure report. **Boundaries:** no math-quest product work, no decision is
ratified by an agent, and nothing is removed without a trace of what governs it.

## Slice 1 — correctness · CLOSED 2026-07-26

- [x] grove [#155](https://github.com/kodhama/grove/pull/155) — `/grove:setup` resolved
      its own package root one directory short and died before any surface rule ran.
      One-hop fix plus a regression test that drives the CLI from both a source checkout
      and an installed copy at a path containing a space.
- [x] Committed plugin enablement so a fresh clone has a fleet — stewards
      [#44](https://github.com/kodhama/stewards/pull/44), kodhama
      [#54](https://github.com/kodhama/kodhama/pull/54), design-system
      [#20](https://github.com/kodhama/design-system/pull/20), wisp
      [#51](https://github.com/kodhama/wisp/pull/51), trellis
      [#196](https://github.com/kodhama/trellis/pull/196), math-quest
      [#363](https://github.com/kodhama/math-quest/pull/363).
- [x] 111 debris branches deleted across six repos; `trellis/research/0013` preserved as
      closed-unmerged work.
- [x] Trellis's PR-review workflow, red for seven consecutive runs, recovered on its own.
      Cause unaddressed.

## Slice 2 — dead weight · WITHDRAWN 2026-07-27

- [x] Withdrawn without changes. Three of the proposed removals were refuted on contact:
      two by `grove/adr-0036` D3, which retains the specs deliberately, and one by the
      lifecycle rule that `superseded` is terminal. Recorded in the audit artifact.

## Slice 3 — the marketplace canary · OPEN

- [x] Mechanism archived, loadable, at
      [`wisp@archive/codex-marketplace-canary`](https://github.com/kodhama/wisp/tree/archive/codex-marketplace-canary).
- [x] [#45](https://github.com/kodhama/stewards/issues/45) — family marketplace check,
      keyless asset half, inside current Stewards scope.
- [x] [#47](https://github.com/kodhama/stewards/issues/47) — live-session ping; needs
      `kodhama-0017` widened. **Deferred by the maintainer, not blocked.**
- [ ] `wisp/adr-0018` — second draft, in independent review. First returned `UNSOUND`.
- [ ] Implementation, gated on that decision reaching `approved`.

## Parked

- [#46](https://github.com/kodhama/stewards/issues/46) — compacting the decision and spec
  corpora. A rule change, not maintenance; needs its own shaping.
- The stewards/kodhama thin-vendor migration. Their vendored charters carry config tokens
  resolved in prose and neither repo has a `.grove/config.toml` to hold them.

## Stop-and-learn checkpoint

Slice 1 landed clean. Slice 2 did not survive first contact, and the reason generalises:
**removals were proposed from names and line counts rather than from a trace of what runs
and what governs it.** Three of ten items withdrew; a fourth changed direction twice.

Two near-misses were caught by verification rather than by reading — nine repo-owned
`.grove/agents/` addenda staged for deletion as if they were stale charter copies, and a
closed-unmerged research branch that a debris sweep would have destroyed.

**The corrective is in the audit artifact and is already binding**: trace first, report
the trace, and where it contradicts a ratified decision, supersede openly. The cost is
visible — `wisp/adr-0018` has taken two drafts and two adversary passes for one workflow
removal. That is the correct price and it should not be optimised away.

## Slice 4 — receipts, review, and what review found · 2026-07-28 (overnight)

Run autonomously under a standing instruction to progress what did not need the
maintainer, review adversarially before pushing, and merge only what was stable
and uncontroversial.

### Landed

- [x] **`kodhama-0025` receipts closed in all three receiving repos** — its
      acceptance criterion *"Each receiving repository carries a forward pointer
      to this record."* [wisp#56](https://github.com/kodhama/wisp/pull/56),
      [grove#162](https://github.com/kodhama/grove/pull/162),
      [trellis#203](https://github.com/kodhama/trellis/pull/203). Each pointer is
      scoped to what actually stops binding; grove's says explicitly that grove's
      own use is *untouched*, since `kodhama-0025` keeps its fields on purpose.
- [x] **[trellis#202](https://github.com/kodhama/trellis/pull/202)** — the
      staleness nudge no longer reads *"ships payload payload@…"*. It survived
      because until #198 the hook emitted an envelope Claude Code discards, so
      nobody had ever read one.
- [x] **[stewards#53](https://github.com/kodhama/stewards/pull/53)** — grove's
      managed block in `CLAUDE.md` had been **unparseable by grove's runtime**
      for an unknown length of time: the begin marker and the stamp format both
      predate the current schema, and grove ships no migration for either. Every
      lifecycle operation refused this repo while writing nothing, so the block's
      content was frozen — including an *instruction* to edit `.claude/agents/`,
      a directory #52 deleted. Repaired by hand, then regenerated through grove's
      real plan/confirm/apply path.
- [x] **stewards#42 closed** — the artifact it asked to migrate no longer exists
      and the mandate it migrated toward is retired.
- [x] **[grove#149](https://github.com/kodhama/grove/pull/149) closed** — its
      content reached `main` by another route in #158; the branch had been
      conflicting since.

### Gated on the maintainer

- [ ] **[trellis#204](https://github.com/kodhama/trellis/pull/204)** —
      `decision-0066`, retiring Trellis's `surfaces.json`. **Third draft.** Two
      independent review rounds, both `NEEDS-REVISION`; the diff is one file and
      nothing lands under it until it is `approved`.
- [ ] **[grove#161](https://github.com/kodhama/grove/pull/161)** — reviewed three
      times, green, awaiting the last verdict at the time of writing.

### What review found, and why it is the point

Every defect below was found **after CI was green**, by review rather than by
tests — the family's recurring failure mode is a passing suite over a broken
product.

| where | found |
|---|---|
| grove#161 | an approved `setup` overwrite **crashed** on five consumer repo states that previously returned a normal plan; the crash bypassed `fail()` and dropped a disclosure an approved decision requires on every plan |
| grove#161, round 2 | a defect introduced by round 1's fix — a test fixture that did not match its own comment and routed around the one function still unguarded |
| grove#162 | a **false citation I wrote**: `adr-0041` clause 5 is the load-path rule, not the combination invariant, and `adr-0041` twice defers that invariant to the retired upstream |
| stewards#53 | a claim I had asserted was verified — *"no test/typecheck gates in this repo"* — moved from frozen legacy text into **live** project instructions, while CI enforces a test gate |
| stewards#52 (post-merge) | the commit message said the grove plugin does not ship `shaper`. It ships, as a Codex skill plus a managed-block directive. The claim had already propagated into grove#160 |

Three of those five are corrections to my own work, two of them to claims I had
explicitly said were checked. The corrective from Slice 2 — *trace first, report
the trace* — holds, and needs one addition: **stating that a claim was verified
is not verifying it.** Each of the three was a sentence asserting a check that
had not been run.

### The systemic finding

**Only trellis has an automated PR reviewer.** grove, wisp and stewards merge on
tests alone, and stewards' single workflow is path-filtered so a docs-only PR
gets no check at all. All five defects above were found in repos with no
reviewer, by agents spawned by hand. Trellis's reviewer runs on **every push**,
which is what catches fix-introduced regressions; a one-shot review before the
first push structurally cannot. Filed as
[stewards#54](https://github.com/kodhama/stewards/issues/54) — it needs a
per-repo secret only the maintainer can add, so no workflow files were written.

### Filed, not fixed

grove [#163](https://github.com/kodhama/grove/issues/163) (spec-0004's Setup
section describes whole-file overwrites) ·
[#164](https://github.com/kodhama/grove/issues/164) (a managed block written by
an older Grove is unmanageable forever) ·
[#165](https://github.com/kodhama/grove/issues/165) (per-host adapter fields have
no validation gate) · [#166](https://github.com/kodhama/grove/issues/166) (the
`unavailable + claimed` invariant has no live decision behind it) ·
[#167](https://github.com/kodhama/grove/issues/167) (refresh advertises files
only setup seeds). grove#160 re-scoped and corrected;
stewards#39 narrowed to what actually remains.

### Parked for the maintainer

- **`/grove:setup` has never run in this repo**, so `.grove/config.toml` and
  `.grove/gates.toml` do not exist — which is why `<TEST_CMD>` had no home and
  ended up as stale prose in `CLAUDE.md`. Seeding `gates.toml` sets who must
  ratify which gate. Not an overnight decision.
- Two stale Codex PRs left open deliberately: grove#142 (a draft ADR) and
  grove#135 (`AGENTS.md` as canonical instructions, conflicting since 2026-07-24).
  Both are judgment calls, not debris.
