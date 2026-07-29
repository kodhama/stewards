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

## Cold start — read this first (state as of 2026-07-29)

If you are picking this up with no memory of it, this section is the whole
briefing. The chronological slices below are the audit trail, not the state.

> **Reconciled 2026-07-29 against live `gh` and file state.** The ledger had
> drifted badly: twelve entries were stale in both directions — items marked open
> that had landed, and items marked done that were only triaged — and the
> dispatcher section below described as "stopped" a thread that restarted and
> shipped. Worse, **fourteen items of the wave's actual plan appear nowhere in
> this brief at all**; see §The plan's items this ledger never tracked. Judged by
> this brief the wave looked nearly finished. It is not.

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
| **trellis#204** — `decision-0066`, retire Trellis's `surfaces.json` | an intent act. **It bundles the implementation deliberately** — approved `kodhama-0025`'s AC requires `surfaces.json` and its `install.sh` manifest entry be removed *"in the same commit — the bundle fetches a moving `main`, so splitting them breaks `curl \| sh` for every user immediately."* Verified unmet on trellis `main`. A Codex P1 asked for them to be split; doing so would break the public install command, so the record's own "no code until approved" comment is what gets amended. |
| **grove#186** — `adr-0048`, parsers are dependencies | the ship act. The record is already `approved` and says so: *"The PR merge is the separate ship act and is NOT performed by this flip."* Carries grove#169's VERSION bump. |
| **`spec-0006-voluntary-dispatch`** | flip `gated` → `approved`. Its own status line: *"`approved` remains a human act; ship = human stands."* |
| **grove#189**, **stewards#61** | merges. Two supersession frontmatter edges `adr-0047` ordered in ratified text, and this ledger commit. Both green. |
| **grove#187**, **grove#188**, **grove#184** | three parked decisions: may a plan be persisted? do artifact types get their own lifecycles? does security review get its own role? |
| ~~grove#161~~ | **STALE — merged 2026-07-28T06:33.** |
| ~~stewards#54~~ | **STALE in substance.** Six repos now carry `claude-code-review.yml` and the secret. Only spore and kodhama remain, and neither has a `.github/` directory at all. Narrow or close it. |
| grove#142, grove#135 | stale Codex PRs; judgment calls, not debris. Left open on purpose. |

### The dispatcher thread — status: RESTARTED AND SHIPPED

> **This section's "STOPPED" verdict is superseded, 2026-07-29.** `adr-0046` is
> **`status: approved`** (maintainer intent act 2026-07-28, *"Approved!"*), merged
> via grove#175. `spec-0006-voluntary-dispatch` exists at `status: gated`, v3,
> after an eight-round adversary convergence. **Its implementation merged as
> grove#181** on 2026-07-29, advancing `spec-0004` to v8. The `adr-0003` pointer
> fix landed as grove#173. **Everything below describing a fork awaiting the
> maintainer, a decision "never pushed", or a research pass not yet returned is
> historical.** It is kept because the reasoning that produced the reset is worth
> reading; it is not the state. Read this banner, not the paragraphs.

#### Historical — the thread as it stood on 2026-07-28

The largest thread of 2026-07-28 and the one most likely to be picked up wrong.

**The symptom:** reviewers, including `conformance-reviewer`, stopped running.

**The trace, verified:** grove's dispatch rules reach a session through its
managed instruction block. Two generations exist —

- **`0.1.0` block** carries a standing directive: *"Work items matching a grove
  workflow (W1–W6 …) run as grove runs, sequenced through grove's chartered
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

- **grove's plugin cache is version-keyed and its VERSION never moved past
  `0.3.0`.** Two different builds both answer to `0.3.0` and share one cache
  directory: the `grove` project is currently loading `stewards`' bytes.
  Verified by sha. Bump VERSION before any refresh wave (grove#169).
- **Three copies of every charter exist** with different line numbers:
  `charters/`, `plugins/grove/reference/charters/`, and the installed plugin
  cache. Always say which one a citation is against.
- **`kodhama-0025` is on `main`** and its URL resolves — a review claimed
  otherwise from a stale local ref. Fetch before concluding a ref is missing.
- ~~Stewards' only CI workflow is path-filtered; a docs-only PR gets no check at
  all.~~ **No longer true for review, 2026-07-29.** Stewards has three workflows;
  `claude-code-review.yml` and `agent-workflow-parity.yml` run on every PR —
  verified, docs-only PR #61 got both green. Still true for the *test* gate.
  **`stewards/CLAUDE.md` repeats the old claim and is now inaccurate there.**
- **A draft PR bails the Claude reviewer in ~30-60s** at its eligibility check,
  instead of a ~15-minute review. Keeping a PR draft through fix rounds is the
  single biggest lever on review cost — **but see the next trap before relying on
  flipping it ready.**
- **A PR gets exactly ONE Claude review, ever — the first one.** Measured
  2026-07-29 on grove#186: flipping `ready_for_review` produced no review. The
  run's own verdict: *"Claude has already left a code review comment on this PR …
  Per the review instructions, when Claude has already commented on a PR, I should
  stop and not proceed with another review."* The check is **condition 4 inside
  the host-native `/code-review` skill**, not in our workflow file, so it cannot
  be fixed by editing `claude-code-review.yml` — which is byte-identity-pinned
  anyway. **Consequence:** if Claude comments early, every later push is
  unreviewed by Claude no matter how much changes. grove#186 had ~60 files change
  after its only Claude review. This is the **sixth** silent-failure mode of this
  reviewer and it contradicts the working rule above it — *"run adversarial review
  again after every fix round"* — which the tooling cannot deliver. Re-review has
  to come from Codex (explicit tag), a local `grove:code-reviewer` run, or a fresh
  PR.

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

### The plan's items this ledger never tracked

**The consequential finding of the 2026-07-29 reconciliation.** This brief is the
*ledger of* a working plan held outside the repo — §Scope says so, and the plan
reciprocates. But fourteen plan items, most of them medium-to-large, appear
nowhere in these slices, not even as Parked. **Closing the wave on the slices
alone would close it on a ledger that never recorded most of its work.**

Status verified 2026-07-29 by `gh` and file checks; re-verify each at execution
rather than trusting this table wholesale.

| id | what | status | blocked on | size |
|---|---|---|---|---|
| **W0.3** | stewards + kodhama thin-vendor migration | not done — neither repo has `.grove/config.toml` or `gates.toml`; both still carry vendored `lifecycle.md`/`relations.md`/`versioning.md` | rides W0.4 / W1.5 | medium |
| **W0.4** | overlay refresh in 7 repos | not done — 7 of 8 stale on two payload stamps. **The remedy has changed:** trellis `decision-0065` (approved) removed vendoring from the plugin path, so the move is probably to migrate off `.trellis/internal/` entirely, not refresh the stamp. No decision settles which. math-quest's hand-rolled hook is *dead*, not merely wrong-pathed — it reads `.trellis/version`, which does not exist there | **maintainer** at an interactive prompt, + grove#169 | medium–large |
| **W0.6** | trellis CI recurrence guard | recovered on its own; nothing prevents recurrence | maintainer's call | small |
| **P4** | wisp root implementation | not done — **and both stated preconditions are void.** No "rich-dashboard" branch or PR ever existed (the dashboard landed as wisp#27/#28), and math-quest no longer carries `vendor/wisp/`. The "non-lossy" and "ratified byte-copy" constraints are gone | needs a re-scope first | large |
| **P7** | `reference/gates/enforcement.toml`, "24 lines" | not done — **and it is not a leaf delete.** 14 inbound references incl. `profile.mjs`, `lifecycle.mjs`, `release.mjs`, `package-allowlist.json`, `legacy-ownership.json` (records its sha256), 3 tests, `adr-0008`/`0018`/`0035`, `specs/0004` | unblocked | medium |
| **P8** | trellis eval transcripts | not done — 181 blobs; `decision-0053` (approved) pins the directory byte-untouched | **needs a decision** | medium |
| **P9** | grove probe ritual | not done — interacts with grove#159, which is what asserts `candidate` | unblocked; sequence after #159 | medium–large |
| **W1.5** | grove setup/refresh in 5 repos so the runtime consumes `legacy-ownership.json` | not done — `lifecycle.mjs` reads it via `inspectLegacyState()`; the release validator checks its schema | same gate as W0.4 | medium |
| **W1.6** | drop the dispatcher's `claude_agent`/`codex_skill` outputs (grove#130) | not done — **but now UNBLOCKED.** The plan gated this on "W3 naming the instruction carrier"; that carrier is now named twice — grove `adr-0046` and trellis `decision-0065` | unblocked | small–medium |
| **W1.7** | retire trellis `install.sh` | not done — `install.sh` is 19,830 b, `spec-0005` is `gated` and entirely about it, and `design-system/patterns.md:119,138` still renders the `curl \| sh` command. Live shaping exists as trellis#197/#201 | **a channel-retirement decision**, then LP copy in two repos, then code | large |
| **W2.1** | supersede `kodhama-0022` — index row + per-repo pointer | not done — **`stewards/decisions/README.md` does not exist at all** | **needs a decision** | medium |
| **W2.2** | retire the prose-affidavit `status:` → `status` + `approved_by` + `approved_on` | not done — `approved_by`/`approved_on` return **zero** hits repo-wide | **needs a decision** | medium |
| **W2.3** | retire the test-deps ledger requirement (grove#118) | **partially done, in a different direction** — `adr-0043` + `spec-0005` + grove#154 landed the structured canary; the ledger requirement at `charters/executor.md:71` survives | unblocked; write the ~50-line checker | small |
| **W3** | plugin-resident instruction delivery, Claude half | **DONE** — trellis `decision-0065` / PR #198; `staleness.sh` injects rules via SessionStart when no vendored overlay exists. Residuals: `trellis/research/0013` is still only a branch (likely moot), and **grove#117** — the `agents` array is still hand-written, 13 paths against 14 roles, and ~15 files carry a hardcoded roster count | grove#117 unblocked | medium |

**Also absent from this ledger, filed 2026-07-28/29:** grove#156 (stale, close it —
superseded by #159) · grove#159 (retire `release_state`, unblock the release gate;
unblocked) · grove#179 (spec-0004 owes a provenance scheme for multi-source entry
skills) · grove#180 (nine build-gate follow-ups, one MEDIUM: `implements:`
classification misses YAML comments/blank lines before the first block item — the
fail-open direction) · stewards#39's two residuals.

**The plan's own header pointers are wrong** and should be corrected wherever it
lives: it cites `stewards/decisions/0024-family-audit-2026-07.md` and
`conductor/wave-0024-family-consolidation.md`. Neither exists — the audit is
`stewards/research/family-audit-2026-07.md` (`type: discovery`) and the ledger is
this file. There is no decision `0024` in stewards; the ids jump 0023 → 0025.

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
      keyless asset half, inside current Stewards scope. **The checkmark records
      triage, not delivery** — the issue is still open with zero comments and no
      implementation. No workflow reads the published catalogs today. *Unblocked,
      needs no new authority, small–medium.*
- [x] [#47](https://github.com/kodhama/stewards/issues/47) — live-session ping; needs
      `kodhama-0017` widened. **Deferred by the maintainer, not blocked.** Also
      triage-only; it needs a **decision**, not an implementation PR.
- [x] `wisp/adr-0018` — **`approved` 2026-07-27** (maintainer intent act in
      conversation), merged in wisp#54. Retired on cost-for-value with the losses
      named, after three drafts failed on a redundancy argument.
- [x] Implementation — **landed in the same PR**: `codex-canary.mjs` (−780),
      `codex-canary.yml` (−89), the 753-line driver test, `spec-0002` (−324).
- [ ] **wisp#55's open debt** — `spec-0002`'s 4,194,304-byte boundary is normative
      with **no test at any value**. The issue itself calls the fix small and
      independent. *Unblocked, trivial.*

## Parked

- [#46](https://github.com/kodhama/stewards/issues/46) — compacting the decision and spec
  corpora. A rule change, not maintenance; needs its own shaping.
- The stewards/kodhama thin-vendor migration. Their vendored charters carry config tokens
  resolved in prose and neither repo has a `.grove/config.toml` to hold them.
- **[grove#187](https://github.com/kodhama/grove/issues/187) — should a plan ever be a
  persisted artifact?** *(high, maintainer-raised 2026-07-29.)* `adr-0037` (`approved`)
  says no in four places; grove#186 shipped one anyway on a practice call that was never
  traced against it, and the corpus baseline had already classified it
  `implements-bearing+unclaimed` — the plan had enrolled itself as a fidelity-bearing
  upstream. Unblocked by deleting the file and relaying it on the PR. The open question is
  whether a *durable but non-authoritative* plan form should exist, since the value was
  real and the prohibition is about authority, not persistence.
- **[grove#188](https://github.com/kodhama/grove/issues/188) — the lifecycle enum is
  one-size-fits-all.** *(high, maintainer-raised 2026-07-29: "each artifact needs its own
  lifecycle, not the same for all of them.")* `charters/lifecycle.md` says "exactly four
  values" and forbids restating them anywhere; **four grove `type: research` files have run
  a fifth value, `recorded`, since 2026-07-22**, each escaping by a frontmatter comment
  rather than a decision. `research/orchestrator-patterns.md:4` flagged the gap itself and
  nothing followed. The #186 plan then invented the same value on the same prose exemption
  — a convention escaping twice, which is `inv-self-improvement`'s exact failure shape.
  Neither escape was visible to any gate: `research/` and `plans/` are both outside
  `.grove/config.toml`'s `ARTIFACT_DIRS`.

  **Both are parked deliberately, not deferred by oversight.** The maintainer's call:
  *"let's do whatever unblocks the thing now."* Neither blocks grove#186, and the wave's
  own cost is the reason — every touch has been surfacing a new governance question, and
  answering them inline is what would prevent the consolidation from ever finishing.

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

## Slice 5 — the dispatcher thread · 2026-07-28 · reset, then RESTARTED AND SHIPPED

> Closed 2026-07-29: `adr-0046` approved and merged (grove#175), `spec-0006`
> authored and gated, implementation merged (grove#181). See the cold-start banner.

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
- [x] **Research pass commissioned** on swarm activation patterns before any
      further design. **Delivered** — grove#174 and #178 merged;
      `research/rule-delivery-and-activation.md`, `orchestrator-patterns.md` and
      `supervisor-composition.md` are on main and `adr-0046` cites them in
      `informed_by:`.
- [x] **`adr-0003` ← `spec-0004` pointer fix** — **landed**, grove#173, 2026-07-28.
      `adr-0003` now carries `superseded_in_part_by: [adr-0026, adr-0046]` plus
      three in-body forward pointers.

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
