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

## Cold start — read this first (state as of 2026-07-28)

If you are picking this up with no memory of it, this section is the whole
briefing. The chronological slices below are the audit trail, not the state.

### What this wave is

A consolidation pass over the kodhama family after a period where scope creep
added heavy machinery faster than it added value. The corrective, learned the
hard way in Slice 2 and reaffirmed since: **trace what runs, what depends on it,
and which approved artifact governs it — and report that trace — before
proposing removal.** Slice 4 added a second: **stating that a claim was verified
is not verifying it.** Slice 5 added a third, the sharpest: **a search narrow
enough to miss the evidence is not evidence.**

### Working rules for this repo family

- The local checkout of any repo **other than `stewards`** may be owned by
  another session. Never edit files or switch branches there. Clone fresh to a
  scratch directory and work in the clone; the deliverable is a pushed branch.
- Decisions are append-only. Supersede with a forward pointer; never edit
  ratified substance.
- **The intent gate is closed to the agent.** Decisions are drafted `gated`;
  only the maintainer flips `approved`. Merging a gated decision is their act.
- Ratification packets go to the maintainer as **HTML artifacts**, not raw prose.
- Run adversarial review before pushing, and **again after every fix round** —
  a review that only saw the original code cannot find defects the fixes
  introduced. Three consecutive rounds on grove#161 each found a defect
  introduced by the previous fix.
- Mutation-test every guard: revert the fix and confirm the test goes red. Two
  tests written this week passed against the broken code.

### Open, blocked on the maintainer

| item | what it needs |
|---|---|
| **trellis#204** — `decision-0066`, retire Trellis's `surfaces.json` | an intent act. Third draft; two adversary rounds. Nothing lands under it until `approved`. |
| **grove#161** — setup overwrite preserves consumer rows | green and mergeable, deliberately unmerged. Three review rounds each found a defect introduced by the last; the fourth was self-caught. Wanted a human look before merge. |
| **stewards#54** — no automated PR reviewer outside trellis | **resolved 2026-07-28** for grove, stewards, wisp, design-system: reviewer + parity control merged in each, and the maintainer set `CLAUDE_CODE_OAUTH_TOKEN` in all four. |
| **trellis#205** — trellis's reviewer reports `success` while delivering nothing | a merge call. Left open deliberately: trellis was not in the roll-out ask, it already holds a token so the fix bites immediately, and merging suspends review on #204 until #204 merges `main` back in. |
| grove#142, grove#135 | stale Codex PRs; judgment calls, not debris. Left open on purpose. |

### The dispatcher thread — status: STOPPED, direction reset

The largest thread of 2026-07-28 and the one most likely to be picked up wrong.

**The symptom:** reviewers, including `conformance-reviewer`, stopped running.

**The trace, verified:** grove'"'"'s dispatch rules reach a session through its
managed instruction block. Two generations exist —

- **`0.1.0` block** carries a standing directive: *"Work items matching a grove
  workflow (W1–W6 …) run as grove runs, sequenced through grove'"'"'s chartered
  agent roles, loaded from the grove plugin as `grove:<role>` subagents (all
  thirteen)."* Five repos have this: wisp, trellis, design-system, spore,
  math-quest.
- **`0.3.0` block** replaces it with two "Load the charter" pointers and no
  routing rule. One repo has this: stewards, since #53.

The two have **never coexisted**. Stewards never had the directive at all, which
is why routing failed there specifically.

**Do not "fix" this by refreshing the five 0.1.0 consumers** — that would delete
the working directive. Blocked pending a decision (grove#170).

**A live contradiction, owed regardless of direction:** `adr-0003` (approved,
no supersession pointer) mandates the routing rule; `adr-0031:157-158`
(approved) still requires it on `AGENTS.md`; `spec-0004:308-334` (**gated**)
specifies the loader block instead and never mentions `adr-0003`. A gated spec
overrode an approved decision. **Fix this first, whatever else happens** — a
pointer on `adr-0003` and a `spec-0004` amendment.

**Direction reset, maintainer, 2026-07-28:** always-on rules and an always-on
swarm are no longer the target. Voluntary session entry is acceptable — a
`/grove:start`-style skill that loads the dispatch rules, after which handovers
proceed autonomously; not surviving compaction is acceptable, with a refresh
skill. **A research pass into what comparable frameworks actually do was
commissioned before committing further** — primary reference
https://github.com/MartyBonacci/specswarm, plus the activation-pattern survey
and the private-framework brief the maintainer prepared but never brought back.
Superseding previous decisions is explicitly permitted.

**`adr-0046`** (drafted, `gated`, never pushed) proposed hook-only delivery and
failed three reviews: `NEEDS-REVISION`, `FAIL`, `NEEDS-REVISION`. Its central
claim — *"nothing authorizes the loader"* — was **false**, retracted publicly on
grove#170. Do not revive it as drafted. The fork that was in front of the
maintainer when the direction reset: **A** restore the rule to the generator ·
**B** hook plus a residual block carrying the rule · **C** hook only. B had been
chosen, then superseded by the reset.

### Traps that cost real time this week

- **grove'"'"'s plugin cache is version-keyed and its VERSION never moved past
  `0.3.0`.** Two different builds both answer to `0.3.0` and share one cache
  directory: the `grove` project is currently loading `stewards`'"'"' bytes.
  Verified by sha. Bump VERSION before any refresh wave (grove#169).
- **Three copies of every charter exist** with different line numbers:
  `charters/`, `plugins/grove/reference/charters/`, and the installed plugin
  cache. Always say which one a citation is against.
- **`kodhama-0025` is on `main`** and its URL resolves — a review claimed
  otherwise from a stale local ref. Fetch before concluding a ref is missing.
- Stewards'"'"' only CI workflow is **path-filtered**; a docs-only PR gets no check
  at all. Green means nothing there without reading the filter.

### Grove issues filed 2026-07-28

#163 spec-0004 Setup section describes whole-file overwrites · #164 a managed
block written by an older Grove is unmanageable forever · #165 per-host adapter
fields have no validation gate · #166 the `unavailable + claimed` invariant has
no live decision behind it · #167 refresh advertises files only setup seeds ·
#168 the non-support disclosure is emitted twice · #169 VERSION/cache collision ·
#170 the routing directive regression · #171 `contract-author` names a
`spec-adversary` `SOUND` token that role cannot emit · #172 decisions have no
body-section contract, and 40 of 45 carry acceptance criteria.

Also: stewards#42 closed (obsolete), stewards#39 narrowed, grove#149 closed
(superseded by main), grove#160 re-scoped and corrected.

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

## Slice 5 — the dispatcher thread · 2026-07-28 · STOPPED, direction reset

State and traps are in **Cold start** at the top; this is the audit trail only.

- [x] **Diagnosed why reviewers stopped running.** Not the dispatcher agent —
      the managed block. Two block generations, five repos on the `0.1.0`
      directive and one (stewards) on the `0.3.0` pointer. Stewards never had
      the directive, which is why routing failed there specifically.
- [x] **Corrected three of my own claims to the maintainer**, each caught by
      review or by going to the primary source:
      *"this used to work"* is impossible — the loader line postdates the
      maintainer's memory of it working by four days;
      *"the loader may be live in grove and math-quest"* — it is live in exactly
      one repo, and grove does not self-host at all;
      *"nothing authorizes the loader — no decision, no spec"* — **false**,
      `spec-0004:308-334` specifies it deliberately. Retracted on grove#170.
- [x] **Ten grove issues filed**, indexed under Cold start.
- [x] `adr-0046` drafted `gated`, reviewed three ways, **not pushed**. Verdicts:
      `NEEDS-REVISION` (decision-adversary), `FAIL` (conformance), and
      `NEEDS-REVISION` (spec-adversary). Every reviewer found real defects; two
      reviewers contradicted each other on byte counts and the draft's figure was
      the correct one. Kept in scratch, deliberately unpushed — a decision whose
      central claim was false should not enter the corpus even as a draft.
- [ ] **Research pass commissioned** on swarm activation patterns before any
      further design: specswarm as primary reference, the wider activation
      survey, and the maintainer's private reference framework. Nothing is drafted
      until it returns.
- [ ] **`adr-0003` ← `spec-0004` pointer fix** — owed regardless of direction,
      and the one item from this slice that should proceed on its own.

### What this slice cost, and what it bought

Three drafts and three reviews produced no merged artifact. What it bought is a
correct diagnosis of a failure the family had been living with silently, ten
filed defects, and a direction reset made on evidence rather than momentum —
including the maintainer's own read that the always-on premise deserved
challenging before more was built on it.

The pattern worth carrying forward: **every substantive error this slice was
caught by an independent reviewer or by reading the primary source, and none by
me re-reading my own work.** Three of the corrections were to claims I had
explicitly told the maintainer were verified.

---

## Slice 7 — an outside lens, and what fourteen inside rounds missed (2026-07-28)

### The finding that justifies the rest

grove#181 had passed **fourteen in-house review rounds across two lenses**. One
outside reviewer then found **two P1 defects**. The follow-up round found the
first fix had not closed the hole, and reproduced arbitrary repo-internal writes
**through the shipped CLI with an empty confirmation file**.

**Carry this forward as a trap, not as history.** The root cause is *not* in
grove#181 and is *not* fixed on `main`: `applyPlan`
(`plugins/grove/runtime/lifecycle/lib/lifecycle.mjs`) authorizes actions by
**id-string membership** while writing to `action.path`, and ids are never
recomputed at apply. A caller-supplied plan file that repeats a licensed id on a
second, unflagged action gets that action applied. It defeats the **human**
confirm gate too — confirming only the disclosed cursor id on an `open-run` plan
let a duplicate-id action write `.github/workflows/pwn.yml`. Reachable from
`grove-operation.mjs`, which also reads its plan from a file.

Both reviewers reproduced it independently. All suites were green throughout.

### PR review, family-wide

Reviewer + `agent-workflow-parity.yml` merged into grove, stewards, wisp and
design-system; trellis's existing copy has a fix open at #205.

**Do not copy trellis's `claude-code-review.yml` forward.** It is the broken one:
missing `show_full_output` and `claude_args`, and measurably silent — #204 ran
three times (45s/56s/45s), all `success`, **zero comments**; #202 ran ~5 min and
posted "No issues found". Take grove's copy instead.

**Two distinct silent-failure modes, often confused:**

1. **Byte-identity skip** — `claude-code-action` refuses to run when its workflow
   file differs from the default branch, then logs a warning, does nothing, and
   concludes **`success`**. Observed on all four roll-out PRs: `claude-review`
   "passed" in 9–14s against a 7–8 minute real review. `agent-workflow-parity.yml`
   exists solely to make this visible; it runs no agent, so it cannot itself skip
   green. **After merging any change to a reviewer workflow, merge the default
   branch into every open PR or they stay unreviewed behind a green tick.**
2. **Delivered-nothing** — the trellis case above. **Parity does not catch it**;
   none of those PRs touched the workflow file. `show_full_output` is what makes
   it diagnosable, which is why its absence is the costly one.

**Green here has never meant clean.** The exit code tracks whether the action
*ran*, never what it *found*.

### Correction made on the record

I attributed trellis's reviewer trouble to "seven consecutive red runs". Its runs
are **green** — that is the defect. Corrected on grove#182 and stewards#54.
