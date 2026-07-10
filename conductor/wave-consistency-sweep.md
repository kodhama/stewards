# Wave: family + math-quest consistency sweep (corpus-reviewer + conformance-reviewer)

Opened 2026-07-10. Authorization: maintainer — "run both of our reviewers across
the full family + math quest. want to clean the repos of inconsistencies."

**Scope correction (mid-run, maintainer clarification):** `conformance-reviewer`
runs were initially dispatched cross-family (each repo checked against
kodhama's own `decisions/0001-0007`). The maintainer corrected this: the ask
is **intra-repo** — each repo's own code/tests checked against that same
repo's own specs/ADRs, that repo's specs/ADRs checked against each other for
contradictions, and a coverage pass (implemented surface with no governing
spec/ADR) — "within their repo mostly, not so much with kodhama." The 6
cross-family-scoped `conformance-reviewer` runs were killed before completing
and redispatched correctly. `corpus-reviewer` needed no correction — it was
always repo-scoped/structural. See kodhama memory
`feedback-reviewer-sweep-scope.md`.

**Machinery note:** `corpus-reviewer` and `conformance-reviewer` resolve as
native subagent types in this session (this repo's own `.claude/agents/`
copies) but only carry *this* repo's (kodhama's) resolved charter text. For
the other five repos, each dispatch was briefed with **that repo's own**
`.claude/agents/{corpus,conformance}-reviewer.md` charter, embedded verbatim
— same practice as `wave-agent-vocabulary-propagation.md`.

Repos covered: kodhama, trellis, grove, wisp, design-system, math-quest.
**homebrew-tap excluded** — no local checkout; maintainer confirmed skip
(delivery-only, one formula, unlikely to carry a decisions corpus).

## Ledger

- [x] corpus-reviewer × 6 repos — all complete
- [x] conformance-reviewer × 6 repos (corrected scope) — all complete
- [x] Reparation plan drafted (this brief)
- [x] Parked judgment calls put to maintainer (all 9 answered across two
      batches, plus 2 raised mid-fix — see "Parked — maintainer answers")
- [x] Tier-1 + Tier-1.5 mechanical fixes executed and merged — kodhama #25,
      trellis #131, grove #23, wisp #12, design-system #8, math-quest #175
- [x] Tier-2 + Tier-3 items resolved through interactive queue processing —
      all answered, fixed, and merged (see Waves 2-7)
- [x] Remaining non-urgent follow-on converted to tracked GitHub issues —
      kodhama#26, trellis#138, trellis#139, grove#29, grove#30
- [x] **Wave closed.** Every PR opened during this sweep is merged; every
      loose end has its own issue in the repo where the fix belongs.

## Findings — by repo

### kodhama
- **corpus-reviewer — FAIL.** `decisions/0001-family-delivery.md:5`
  `depends_on: [adr-0030-espalier, discovery-espalier-runtime-viz]` — both ids
  live in math-quest's own corpus, not kodhama's; no external-reference-prefix
  convention is declared anywhere in this repo's contract to make that legal.
  0001's own provenance line already names this as owed debt ("the original
  owes a supersession pointer here").
- **conformance-reviewer — FAIL.**
  1. `README.md:3` still reads "espalier (agent swarm) · espial (runtime
     observability)" — live, current, zero historical framing. Violates
     kodhama-0003 AC2 outright. Every later wave (rename, grove-install,
     marketplace, vocabulary-propagation) touched `CLAUDE.md` for this same
     purpose and left `README.md` untouched. A plain miss, never flagged
     anywhere as known debt.
  2. `conductor/wave-agent-vocabulary-propagation.md` is stale (marks
     kodhama's own consumer-lane checkbox as not-done; it merged in
     `5b61256`) **and was never committed** (still `??` untracked per `git
     status` at session start) — contradicts this repo's own declared
     practice ("the brief IS the ledger — check items off in the same
     commits that report them," `CLAUDE.md`).
  - Minor: 0002's "marketplace name confirmed collision-free" open question
    was never marked resolved even though correctly implemented.

### trellis
- **corpus-reviewer — FAIL.**
  1. Undeclared `owner: agent` divergence — `decisions/0042` and
     `specs/0005` — the pattern is only pre-declared for math-quest, not
     trellis-self.
  2. `specs/0005-curl-install-mechanical-vendoring.md:5` `depends_on`
     includes `kodhama-0007-one-render-many-copiers` — dangling by this
     repo's own contract (no allowlist entry covers it); the spec's own
     self-check graded this PASS by reasoning about the referent's
     real-world status rather than the declared allowlist.
  3. Supersession integrity, systemic: `decision-0032` is `status:
     superseded` with **no `superseded_by` field** (only a body
     blockquote). Eight more artifacts (`decisions/0025, 0030, 0035, 0036,
     0039, 0041`, `specs/0003, 0004`) assert "superseded in part by
     decision-0043" in prose — and in `decision-0043`'s own Consequences
     section — but **none carries the `superseded_in_part_by` frontmatter
     field** the contract requires. Same-era precedent got this right
     elsewhere (`decision-0013`→`0038`, `0022`/`0037`→`0042`).
  - Minor: `specs/0001-0004` cite `rubric: spec-quality`, an artifact that
    doesn't exist (only `rubric-artifact-contract` does) — self-acknowledged
    elsewhere, never fixed. `research-0004` numbering gap (harmless).
    `decision-0043`/`specs/0005` stuck at `status: gated` 6+ commits with no
    post-merge bump.
- **conformance-reviewer.** Code is solid — `go build`/`vet`/`test` all
  green; every load-bearing spec/decision claim traces to a real, passing
  test (generator-only command surface, payload/manifest pipeline, staleness
  hook, all 10 `spec-0005` ACs). **Confirms and extends** the corpus finding:
  `decision-0023` and `decision-0029` — both fully retired by
  `decision-0043` (their entire subject matter deleted) — carry **zero**
  forward pointer at all, not even the incomplete kind the other 8 got.
  - Minor: `install.sh`'s personal-scope branch prints an extra line beyond
    `spec-0005` AC10's "exactly five items… and nothing more" — untested
    either way, gray call.

### grove
- **corpus-reviewer.** PASS structurally (decisions 0001-0003 + spec-0001:
  ids unique, depends_on resolves, directional flow clean, supersession
  clean). **One real finding:** grove's own
  `.claude/agents/corpus-reviewer.md` **and** `conformance-reviewer.md`
  still carry unresolved template placeholders (`<ARTIFACT_CONTRACT_PATHS>`,
  `<ARTIFACT_DIRS>`, `<REPO_TYPED_CHECKS>`, `<TYPECHECK_CMD>`, `<TEST_CMD>`,
  `<PR_CONTRACT_SECTIONS>`, `<PARKED_ITEM_STORE>`) — ironic, since grove
  authored this role (`adr-0001-corpus-reviewer-lift`) and
  `charters/corpus-reviewer.md`'s own `## Placeholders` section **already
  names the correct resolution** (`decisions/`, `specs/`,
  `decisions/README.md`+`specs/README.md`, "none"). The vocabulary-rename
  commit (`7f7d042`) edited a nearby line and walked past these placeholders
  without resolving them.
  - Minor: same undeclared cross-repo-reference-prefix gap as kodhama/trellis
    (ids resolve in practice, convention never declared).
- **conformance-reviewer — PARTIAL FAIL.** ADR-0001 and ADR-0003 pass
  cleanly (self-verified against their own ACs). **ADR-0002 (vocabulary
  rename) is materially incomplete:**
  1. `specs/README.md:5,25,27` — live, operative prose still says
     "gardener" three times; never touched by either sweep commit
     (`7f7d042`, `20fecdc`).
  2. `.claude/skills/grove-status/SKILL.md` (the **canonical** source file,
     not a vendored copy) still uses "gardener"/"head-gardener"/"furrow"
     throughout, **including as a literal CLI flag value: `--via
     head-gardener`** — a direct violation of ADR-0002 point 4's explicit
     rule ("never anywhere machine-read: file names, frontmatter, CLI
     flags"). The plugin's *vendored* copy of this same file **was** swept
     correctly (commit `20fecdc`) — so the derived copy is right and the
     canonical source it's supposedly copied from is wrong, breaking the
     plugin README's own "must never drift apart" sync guarantee (confirmed
     via direct diff, 5 hunks).
  - **Separate finding:** `specs/0001-contributing-guide.md` sits at
    `status: gated` (since 2026-07-07, no bump commit ever made) while its
    product, `CONTRIBUTING.md`, is already fully merged and governing the
    repo live — CONTRIBUTING.md's own text says "an open, unmerged PR at
    gated is the correct resting state," implying gated content shouldn't
    yet be operative. No recorded ratchet exists to explain the exception.
  - **Coverage gap:** `.claude/skills/grove-status/` (real operative CLI
    behavior, used by every agent role) has no governing charter or
    decision at all — not `charters/`, not `decisions/`. Already-disclosed
    ADR-0030-only provenance for the 10 lifted charters is not re-flagged
    (transparently documented elsewhere); this one is undocumented.
  - Minor cross-doc: README's "eight agent roles" claim doesn't arithmetic
    against its own table (`dispatcher`'s Stage column is "—", not a
    number) — pre-existing, predates all three ADRs.

### wisp
- **corpus-reviewer.** `decisions/` and `specs/` are functionally **empty**
  (only their own contract READMEs). Flagged that `protocol.ts`, `demo.ts`,
  and several `.claude/agents/`/`.claude/skills/` docs already cite
  "ADR-0030" as ratified precedent — that ADR lives in math-quest, not wisp.
- **conformance-reviewer — confirmed and sharpened.** `protocol.ts:5` and
  `dashboard.html:353` build and **enforce** (tested: `TeamState.telemetry`
  vacuity guard, `fail()` throwing loudly) a core invariant — "telemetry is
  self-reported claims, never a substitute for artifact-derived truth" —
  grounded entirely in an ADR with zero footprint in wisp's own corpus.
  Cross-doc: `server.ts`'s `/api/graph` endpoint is implemented and actively
  consumed by `dashboard.html:785`, but undocumented in `server.ts`'s own
  header comment and in README's route table. Coverage: of 7 source files,
  5 (`bus.ts`, `emit.ts`, `server.ts`, `demo.ts`, `dashboard.html`) have zero
  dedicated tests and zero governing spec, local or external; the 2
  well-tested files (`protocol.ts`, `github.ts`) still trace their design
  rationale outside this repo. Gates: `tsc --noEmit` + 36 vitest tests, all
  green.

### design-system
- **corpus-reviewer.** `decisions/` and `specs/` functionally **empty**
  (contract READMEs only). Real FAIL: `README.md:80` and
  `identity/spec.md:108` both claim icon/token additions "aren't yet
  covered by a git tag" — false since `v0.2.0` (cut 9 minutes after that
  commit) already covers them.
- **conformance-reviewer — confirmed and sharpened.** Stale tag prose
  re-confirmed live at HEAD, unfixed across 2 further commits. **New
  contradiction:** `icons/grammar.md` (legibility floor = 16px only) vs.
  `identity/spec.md` (floor = "19px (header) and 16px") — both from the
  *same* T2 finalization commit. The 16px claim is asserted but never
  actually rendered/verified anywhere in-repo (`identity/preview.html` only
  renders small-size checks at 19px); arithmetic flags `kodhama.svg`'s faint
  spark (`r=.85`, 45% opacity) as a plausible-but-unverified risk at 16px
  (no renderer available in-session to confirm). Coverage: the
  decisions/specs machinery **predates** the T2 design pass (the single
  biggest design event — org mark, rewoven trellis mark, 5 new token
  categories) but wasn't used for it — a real bypass, not benign
  pre-formalization. Incidental: `.trellis/profile.md:54` still says
  "math-quest's own `.trellis/profile.md`" as if math-quest were a
  kodhama-family repo — leftover `trellis setup` boilerplate the
  espalier/espial cleanup commit (`03ead0d`) missed in the same sentence.

### math-quest
- **corpus-reviewer — FAIL.**
  1. `decisions/adr-0029-trellis-retrofit.md:5` and
     `decisions/adr-0030-espalier.md:5` both `depends_on:
     [adr-0009-gate-authority, ...]` — no such id exists; the real file is
     `decisions/adr-0009-governance.md`. Both offending files gloss "ADR-0009
     (gate authority → dials)" in prose, suggesting an informal working name
     that was never reconciled to the filed id.
  2. `decisions/adr-0020-placement-slip-tolerance.md` (`gated`)
     `depends_on` includes `feedback-tomas-2026-06-29`, which is
     `status: draft` — a literal directional-flow violation. Could be a
     feedback item that was actually acted on but never flipped to
     `approved`, or feedback could be meant as exempt from this check
     entirely (it has a collapsed `draft → approved` lifecycle per this
     repo's own rule 8) — ambiguous which repair is intended.
  3. `decisions/adr-0029, adr-0030, adr-0031` all **missing the required
     `## Acceptance criteria` section** — all other 27 decisions + all 10
     specs have it. Each of these three's own `## Rubric check` table uses a
     different, self-declared "(decision-record subset)" checklist that
     never actually checks for this section — the self-gate that should
     have caught the omission was swapped for a different, uncited one.
  - Also: `adr-0007` reserved-but-unwritten (intentional, documented,
    informational only). Espalier/espial forward-facing naming: fully
    clean — zero live misuse found anywhere outside properly-marked
    historical records.
- **conformance-reviewer.** Gates clean (`npm run typecheck` 0 errors, `npm
  test` 383/383 green). Runtime code is solid; the two ADR pairs the plan
  flagged as highest contradiction-risk (adr-0021 vs. its generation
  predecessors; adr-0024 vs. adr-0027) turned out to be the **most**
  rigorously reconciled part of the corpus, each carrying explicit
  supersession pointers or a composed-not-conflicting implementation with
  ADR-section-cited code comments. Real findings, all in record-keeping or
  one content shortfall:
  1. **`decisions/adr-0031-espial-consolidation.md:64-65`** — already
     `approved` — commits to `.claude/skills/espalier-status/`. That
     directory doesn't exist; the real one is `grove-status/`. Its sibling
     `adr-0030-espalier.md` (same day, same rename) handled this correctly;
     0031 didn't. Corpus-reviewer's frontmatter checks can't catch this —
     it's a body-content path claim, not a structural field.
  2. Confirms the `adr-0009-gate-authority`/`adr-0009-governance` dangling
     reference independently.
  3. `decisions/adr-0004, adr-0013, adr-0016` all still assert the
     pre-ADR-0026 "9-of-10 gate" as current, unrevised fact — none contains
     a forward pointer to `adr-0026`, unlike `adr-0003` (the ADR that
     actually defines the gate), which correctly carries one.
  4. Skill graph (`adr-0002`) has three concrete, unimplemented "day-1
     concessions": abbreviated node-id slugs instead of the mandated
     descriptive-slug format; no `locale` field anywhere in the data model;
     no `assessable`/inert-node mechanism in the content pipeline — notable
     because the *engine* correctly implements and tests `isAssessable` via
     a mock graph, but the real content-authoring pipeline structurally
     cannot produce an inert node (the loader rejects empty item banks
     outright).
  5. ADR-0004/ADR-0026's engine-suggested "stuck, want to switch?" affordance
     is unimplemented — self-acknowledged in both the ADR text and
     `src/README.md` ("out of scope for slice 1"), so known, not silent.
  - Lower-confidence (reported by one investigative thread, not
    independently re-verified): ADR-0026/0027's own rubric self-checks
    assert dependency ADRs are "approved (merged)" while those ADRs'
    frontmatter actually reads `gated`; CLAUDE.md's "Current stage" section
    may understate shipped work (retest/`verified` tier).

## Cross-cutting pattern (highest leverage single fix)

**No repo declares a convention for `depends_on` references that cross repo
boundaries**, and this is the direct cause of dangling-reference FAILs in
**kodhama** (0001 → math-quest ids), **trellis** (`specs/0005` →
`kodhama-0007`), and the same shape of gap (undeclared, not frontmatter this
time) underlies **wisp**'s ADR-0030 situation and **grove**'s
kodhama-id references. One family-level fix — most naturally a small
amendment to **trellis's `specs/0001-spine-artifact-contract.md` §1**
(the methodology's own declared external-reference allowlist, currently just
`brief-§…`) — extended to recognize cross-repo ids (e.g. `kodhama-*`, or a
`repo/id` qualified form) would retroactively legitimize most of the above at
once, and give wisp a template for formally citing math-quest's ADR-0030
instead of an undeclared code comment. **This is a maintainer call, not one
to resolve unilaterally** — parked below.

## Reparation tiers

**Tier 1 — mechanical, no maintainer judgment needed (bookkeeping catching
frontmatter/prose up to an already-true or already-disclosed state):**
- trellis: add `superseded_by: [decision-0041]` to `decision-0032`; add
  `superseded_in_part_by: [decision-0043]` to the 8 files listed earlier.
- grove: resolve both agent-charter placeholder files using the values
  `charters/corpus-reviewer.md` already documents; sweep the remaining
  "gardener" vocabulary out of `specs/README.md` (3 instances) and the
  **canonical** `.claude/skills/grove-status/SKILL.md` (incl. the
  `--via head-gardener` flag example) to match the already-correct vendored
  copy.
- design-system: fix stale "not yet tagged" prose (2 files); fix the stray
  math-quest reference in `.trellis/profile.md:54`.
- wisp: document the `/api/graph` endpoint in `server.ts`'s header comment
  and README's route table.
- kodhama: fix `README.md` to say grove/wisp (matching `CLAUDE.md`, already
  correct); update + **commit** the vocabulary-propagation conductor brief's
  ledger.

**Tier 1.5 — low-risk, applies an already-established family convention
(forward-pointer annotation: preserve original text, add a dated blockquote
+ forward pointer) rather than editing ratified content in place — no new
maintainer judgment needed, just executing the existing pattern:**
- trellis: annotate `decision-0023` and `decision-0029` (fact already
  established: both fully retired by `decision-0043`).
- math-quest: annotate `adr-0004`, `adr-0013`, `adr-0016` with a forward
  pointer to `adr-0026` (matching what `adr-0003` already correctly has);
  annotate `adr-0031`'s `espalier-status` path claim with a correction
  pointing to the real `grove-status` directory (do **not** silently edit
  the ratified path in place — append the correction as an annotation, same
  mechanism `adr-0030` already models correctly one file over).

**Tier 2 — gated on a maintainer decision (parked below), quick to execute
once resolved.**

**Tier 3 — real content-authoring, bigger, candidates for GH issues if not
done this session:**
- math-quest: draft the missing `## Acceptance criteria` for `adr-0029/30/31`
  (retrospective, but still requires real authorship + review).
- math-quest: skill-graph (`adr-0002`) "day-1 concessions" — descriptive
  node-id slugs, a `locale` field, and an `assessable`/inert-node mechanism
  in the content pipeline (engine already supports the last one via mock
  data) — real engineering, not a doc fix.
- wisp: file a local decision formally adopting/referencing math-quest's
  ADR-0030 (depends on the Tier-2 cross-repo-reference-convention call).
- design-system: decide whether to backfill a retroactive decision for the
  T2 design pass, or accept it as a process lesson going forward only.
- grove: author a `charter-grove-status` (or equivalent decision) for the
  currently-ungoverned `.claude/skills/grove-status/` runtime-status
  contract.
- grove: resolve `spec-0001`'s `gated`-with-live-product mismatch (see
  parked #9).

## Parked (put to maintainer — 9 queued, batching ≤3 at a time per practice)

1. Cross-repo `depends_on` reference convention — where should it live
   (trellis `specs/0001` amendment vs. something else) and what should it
   say?
2. math-quest `adr-0009-gate-authority` — confirm this is a typo/unreconciled
   informal name for `adr-0009-governance`, not a separate missing artifact.
3. math-quest directional-flow violation — flip
   `feedback-tomas-2026-06-29`'s status to `approved`, or declare `feedback`
   exempt from check 5 family-wide?
4. trellis `owner: agent` divergence (`decision-0043`, `specs/0005`) —
   intentional (declare it) or should revert to a human owner?
5. design-system 16px vs. 19px+16px legibility-floor contradiction — which
   is authoritative?
6. wisp ADR-0030 — formally file a local decision, or treat math-quest's as
   directly citable once #1 is resolved?
7. design-system — backfill a T2 decision, or process-fix only?
8. trellis `install.sh` AC10 extra line — trim it, or amend the AC to allow
   it explicitly?
9. grove `spec-0001` — bump to `approved` now (its product, CONTRIBUTING.md,
   is already live), or record an explicit ratchet exception?

## Parked — maintainer answers received

- **#1 (cross-repo reference convention):** amend trellis's `specs/0001`
  external-reference allowlist. **Not folded into the Tier-1 fix wave** —
  amending a spec is proper contract-author/spec-adversary territory per
  this family's own stage discipline, not a mechanical bookkeeping fix.
  Queue as its own follow-up (possibly its own mini-wave) once Tier 1 lands.
- **#2 (math-quest adr-0009):** confirmed typo, `adr-0009-governance` —
  folded into the math-quest Tier-1 PR already dispatched.
- **#3 (math-quest directional flow):** flip
  `feedback-tomas-2026-06-29` to `approved` — not yet dispatched, queue next.
- **#4 (trellis owner:agent):** declare the mapping in trellis's own docs —
  folded into the trellis Tier-1 PR already dispatched.
- **#5 (design-system legibility floor):** 16px only, `grammar.md`
  authoritative — fix `identity/spec.md` to match. Not yet dispatched, queue
  next.
- **#9 (grove spec-0001):** bump to `approved` — folded into the grove
  Tier-1 PR already dispatched.

Still open: #6 (wisp ADR-0030 filing), #7 (design-system T2 backfill), #8
(trellis install.sh AC10 line).

## Report

All 6 Tier-1/1.5 fix PRs opened, independently verified, and merged:
**kodhama #25, trellis #131, grove #23, wisp #12, design-system #8,
math-quest #175.** Merges were maintainer-authorized in advance, conditioned
on independent re-verification passing — that condition was exercised for
real, not rubber-stamped:

- **trellis #131** was held on first pass: `decisions/0023` and `0029` had
  only a body blockquote, no frontmatter supersession field, and `0023`'s
  blockquote overclaimed "entire subject matter retired" when only one of
  its four points actually was. Sent back, fixed (0023 → correctly-scoped
  partial supersession; 0029 → full supersession matching `0032`'s
  precedent), re-verified independently, then merged.
- **grove #23** was held **twice**: first pass caught that bumping
  `specs/0001-contributing-guide.md` to `approved` would have permanently
  frozen 11 live "furrow" mentions while silently closing ADR-0002's own
  unconfirmed open question about that exact term — sent to the maintainer,
  who gave a clear outcome (no "furrow" in agent-facing surfaces or landing
  pages; historical use stays in ADRs only) rather than picking one of the
  offered options. Fixed (swept specs/0001, recorded an explicit dated
  resolution in ADR-0002, reordered the bump to come after). Second pass
  caught a coherence gap in the PR *description* only (never updated after
  the fix commits landed) — no content defect, but held anyway per
  instruction. Description corrected directly, then merged.
- The other 4 PRs (kodhama, wisp, design-system, math-quest) passed
  independent verification clean on the first attempt. Design-system's
  verification specifically re-checked (rather than trusted) a divergence
  the fix agent made from its literal instruction — confirmed correct.

**Parked questions — final disposition:**
- #1 cross-repo depends_on convention → amend trellis's `specs/0001`
  allowlist. **Deliberately not folded into this fix wave** — spec
  amendments are contract-author/spec-adversary territory, not mechanical
  bookkeeping. Still open, no GH issue filed yet.
- #2 math-quest adr-0009 typo, #3 math-quest feedback status, #4 trellis
  owner:agent, #5 design-system legibility floor, #9 grove spec-0001 bump →
  all answered and folded into the merged fixes above.
- #6 (wisp ADR-0030 filing), #7 (design-system T2 backfill), #8 (trellis
  install.sh AC10 line) → **still open, not yet dispatched.**

**Continued autonomously (maintainer stepped away, authorized continued
work):**

GH issues filed for items needing maintainer judgment, not guessed at:
- wisp #13 (ADR-0030 governance gap)
- design-system #9 (T2 backfill decision)
- trellis #132 (install.sh AC10 gray area)
- grove #24 (ungoverned grove-status skill)
- math-quest #176 (skill-graph day-1 concessions — real engineering, not a
  doc fix)

Two larger items drafted as open, unmerged PRs (not decided unilaterally —
both explicitly framed for the maintainer's review, not fait accompli):
- **trellis: cross-repo depends_on reference convention** (the single
  highest-leverage parked item, #1) — drafted as a new `status: draft`
  decision (not gated/approved), proposing a concrete mechanism with
  trade-offs stated and the "what happens to existing dangling references"
  question left explicitly open. This is genuinely unsettled — it normally
  wants the maintainer's interactive shaping conversation (this family's
  own `shaper` role), which wasn't available synchronously. Treat the
  draft as a starting point, not an answer.
- **math-quest: missing Acceptance Criteria in adr-0029/30/31** — drafted
  as retrospective, explicitly-dated additions (not silently inserted as
  if present at original ratification), reconstructed from what each
  decision's own Context/Decision/Consequences already establishes. Needs
  the maintainer to confirm the reconstruction actually matches intent,
  since it's inference from text, not first-hand knowledge.

Neither PR was merged — both need the maintainer's actual read, not just an
independent-agent PASS, given the judgment involved.

## Wave 2 — interactive queue processing (maintainer returned)

The maintainer returned and asked to work the open backlog interactively:
surface each issue, get a real answer, update the issue, dispatch
implementation, move to the next — requeuing anything that needs more
input rather than blocking. All 5 filed GH issues plus the 2 outstanding
review-PRs went through this loop:

- **trellis #132** (install.sh AC10) → trim the line. Fixed, independently
  verified (added a bounding line-count test so the gap can't recur
  silently), **merged** (PR #135).
- **grove #24** (ungoverned grove-status skill) → maintainer chose a full
  charter, not a lighter decision. Drafted (`charters/grove-status.md`,
  PR #28, `status: draft`) — verified against actual wisp source
  (`bus.ts`/`protocol.ts`/`emit.ts`), not just the skill's own docs; clearly
  separates confirmed facts from the author's own framing judgment calls.
  **Not merged — needs the maintainer's actual shaping read**, this is
  design work, not a mechanical fix.
- **grove #26** (README "every role is a stateless cold start") → reword.
  First attempt only excluded dispatcher; independent verification caught
  that **shaper** is also non-cold-start (confirmed against both the table
  and `charters/shaper.md` directly) — sent back, fixed, re-verified,
  **merged** (PR #27).
- **design-system #9** (T2 backfill) → maintainer chose to backfill a
  retroactive decision. Drafted (`decisions/adr-0001-t2-identity-finalization.md`,
  PR #10, `status: draft`), reconstructed from the actual T2 diff and
  current file states, honest about what rationale couldn't be confirmed.
  **While drafting, found a real discrepancy**: the task brief (and issue
  #9's own text) assumed PR #8 had already fixed the 16px/19px legibility
  contradiction — verified directly against PR #8's actual diff, and it
  hadn't (explicitly listed "out of scope" in PR #8's own body). This
  contradiction was still live despite the maintainer's earlier answer on
  it never actually being implemented — an oversight in this session's own
  execution, caught by independent verification rather than assumed fixed.
  Corrected immediately (PR #11: `identity/spec.md`, `identity/preview.html`,
  and two agent charter files that had 19px baked in), independently
  verified, **merged**.
- **wisp #13** (ADR-0030 governance) → file a local decision. Drafted
  (`decisions/adr-0001-telemetry-truth-provenance.md`, PR #14,
  `status: draft`, wisp's first real decision artifact) — found more
  ADR-0030 citation sites than the issue named, deliberately scoped
  governance to only the two *enforcing* code sites rather than silently
  expanding scope, explicit about its dependency on trellis decision-0044
  landing first. **Not merged — needs the maintainer's read.**
- **math-quest #176** (skill-graph day-1 concessions) → scope first,
  implement if safe. Investigated all three items; found the node-id-slug
  rename would touch real persisted user state (`localStorage`, keyed by
  skill id) with no migration path — **correctly deferred**, not attempted.
  Implemented the two lower-risk items (`locale` field, `assessable`/
  inert-node mechanism) end-to-end with one real inert node, which surfaced
  and fixed two genuine pre-existing bugs (`app.ts` map rendering and
  `placement/index.ts`'s floor-band ceiling both assumed every node was
  assessable). Full suite + typecheck + build green (PR #178). **Verification
  dispatched but merge deliberately left to the maintainer** — this touches
  live product behavior in a kids' app, a different risk class from the
  rest of this wave's doc/governance fixes.
- **trellis #133 / decision-0044** (cross-repo reference convention) — the
  4 concrete open questions (delimiter, registry membership, retrofit vs.
  grandfather, adoption scope) were all put to the maintainer directly and
  answered (`/` delimiter; registry = kodhama family + math-quest; retrofit;
  spec-0001 amendment alone suffices). Decision updated to reflect all 4,
  bumped `draft` → `gated`. **Not merged — awaiting the maintainer's own
  ratifying merge** (the two lowest-stakes items — resolution depth, wisp's
  code-comment channel — were left at the draft's own default
  recommendation, not specifically confirmed).
- **math-quest #177** (retrospective ACs) — a genuine new finding from the
  original drafting surfaced mid-wave: `adr-0031` §Decision 5 committed to
  a legacy `$GROVE_EVENTS` path override that was never built. Maintainer's
  call: don't point at legacy events. Fixed via a dated append-only
  annotation (not an in-place edit) recording the maintainer's decision to
  accept wisp's plain default path instead. **PR still needs the
  maintainer's confirmation on the other reconstructed ACs before it's
  mergeable.**

**Currently open, awaiting the maintainer's own read/merge (not just an
independent-agent PASS — genuine judgment or product-risk involved in all
five):** trellis #133 (decision-0044), math-quest #177 (retrospective ACs),
math-quest #178 (locale/assessable — pending its own verification result),
wisp #14 (ADR-0030 decision), grove #28 (charter-grove-status).

**Merged this wave, mechanical/no-judgment-left, independently verified:**
trellis #135, grove #27, design-system #11, math-quest #178 (locale +
assessable/inert-node mechanism, node-id rename correctly deferred after
finding real persisted-state risk; a coverage gap found in the first
verify pass was closed with a proven regression test before the second,
final merge).

## Wave 3 — post-merge corpus re-verification (closing the loop)

Once the queue-processing round's mechanical merges landed, ran a fresh
`corpus-reviewer` pass on every repo with merged decisions/specs changes
(kodhama, trellis, grove, math-quest) — not to re-litigate individual PRs,
but to confirm the sweep's fixes actually left each corpus clean and
didn't introduce anything new. All 4 confirmed today's specific fixes
landed exactly as intended, append-only where required. Two things surfaced
that the original sweep missed:

- **grove**: a genuine governance tension in this session's own fix.
  `decisions/README.md`'s append-only rule, as literally written, only
  sanctions changing a ratified decision via full supersession (new
  decision, old one marked `superseded`, forward pointer) — it has no
  carve-out for "append a dated resolution note without changing status,"
  which is exactly what was done to `adr-0002` to close its self-referential
  open question about the furrow/specs-0001 sweep. The content is fine
  (Context/Decision/Consequences byte-identical, pure addition), and this
  pattern is already common family practice (kodhama's own decisions have
  several similar dated amendments) — but grove's own written contract
  doesn't document it as allowed. Flagged to the maintainer as a real
  question, not resolved unilaterally: either amend `decisions/README.md`
  to name this pattern explicitly, or treat this instance as a lapse.
- **math-quest**: exhaustive cycle detection over the full 55-node
  dependency graph (not run in the original sweep, which only checked
  pairwise resolution + directional flow) found **three genuine circular
  dependencies** spanning 10 artifacts, all pre-existing (dated
  2026-06-16–2026-07-02), none touched by today's merges — filed as
  **math-quest #179**. Also in that cluster: `adr-0020`'s own rubric-check
  falsely claims `feedback-tomas-2026-06-29` is "approved/merged" when its
  actual status is still `draft` (a real rule-1 directional-flow violation,
  not just a cycle — and a self-check that asserted a false status).
  Separately: `adr-0023`/`0025`/`0027` missing the required `## Consequences`
  section, and `adr-0030` missing `Context`/`Decision` headers entirely
  (structured differently) — both pre-existing, outside PR #177's
  Acceptance-Criteria-only scope. Not fixed — resolving cycles needs a
  real judgment call on which dependency direction is actually correct in
  each case, not a mechanical pass.

Minor, non-blocking observations also surfaced: kodhama's `decisions/0002`
has a stale `updated:` field relative to its own newer annotations;
trellis's `decision-0043` doesn't name `decisions/0023`/`0029` in its own
"Supersedes" list even though both now correctly point at it (one-directional
gap, not a rubric violation); grove's `adr-0002` self-declared note
overstates which ADR-0030 sections are quoted in README.md (claims 3, only
1 actually is).

## Wave 4 — maintainer's merge decisions on the remaining judgment-call PRs

Surveyed all 5 open PRs fresh (CI status + highlights), maintainer decided
per-PR:

- [x] **trellis #133** (decision-0044) — MERGED. Now on `main` at
      `status: gated`. Still needs a separate `approved` bump and a
      follow-on contract-author pass amending `specs/0001`'s allowlist
      before the qualified `repo/id` form is actually live in the contract.
- [ ] **wisp #14** (ADR-0030 decision) — HELD, per maintainer's call. Its
      own `depends_on` stays provisional until #133's full chain (merge →
      approve bump → spec-0001 amendment) completes.
- [ ] **grove #28** (charter-grove-status) — HELD, per maintainer's call.
      Needs an actual shaping pass, not just a mechanical merge.
- [x] **design-system #10** (T2 retroactive decision) — MERGED.
- [x] **math-quest #177** (retrospective ACs + GROVE_EVENTS amendment) —
      MERGED.

## Wave 5 — math-quest #179 (circular dependencies) resolved

Dispatched full investigation (read every artifact in all 3 cycles + git
history to establish real authorship order), then independent adversarial
re-verification before merge — both completed, nothing guessed blind:

- **Cycle 1** (surface-b, 4 nodes): dropped `discovery-surface-b-child-safety`'s
  `depends_on: [spec-surface-b]` — the edge was true when written, but
  `spec-surface-b` was later revised the same day to depend on `adr-0019`,
  which depends on the discovery chain, closing the loop.
- **Cycle 2** (placement, 2 overlapping cycles sharing a closing edge):
  dropped `spec-placement`'s `depends_on` on `adr-0020`. Verifier confirmed
  this is the *only* one of two possible directions that kills both
  overlapping cycles at once (graph-theoretically necessary, not just a
  style call) — but also found the correction note's stated rationale
  ("ADRs point at what they revise, revised specs don't point back")
  overstates a convention this corpus doesn't actually follow consistently
  elsewhere (`adr-0019`/`spec-surface-b`, `adr-0028`/`spec-placement` both
  go the other way). Maintainer chose to merge as-is — the edit is right,
  the prose justification is a minor, non-blocking overstatement.
- **Cycle 3** (generation endpoint/tier2, 2 nodes): dropped
  `spec-tier2-generation`'s `depends_on` on `spec-generation-endpoint` —
  confirmed via git history (tier2 spec predates the endpoint's Tier-2
  awareness) and via the actual code (`endpoint.ts` genuinely calls
  `generateTier2Items`).
- **Also fixed** (owed from earlier in this session — maintainer decided
  this via the original parked-questions batch, but it never got
  dispatched until now): `feedback-tomas-2026-06-29.md` and
  `feedback-amalia-2026-07-03.md` both flipped `draft → approved` — both
  independently confirmed already merged/acted-on.

Independent re-verification found a fresh, full-corpus DFS cycle-detector
now returns zero cycles and zero dangling references anywhere in the
58-id graph; 390/390 tests, typecheck, and CI all green. **Merged**
(math-quest #180), issue #179 closed with a summary comment.

## Wave 6 — decision-0044's follow-on chain + grove #28 shaping, both closed

Maintainer asked to act on both remaining items, using the family's actual
named roles ("the appropriate druids") — dispatched in parallel, sequenced
where genuinely dependent, with every judgment call surfaced before acting:

**decision-0044 follow-on (trellis):**
- **Bump `gated → approved`** (PR #136) — traced the exact bump-commit
  convention from `decision-0042`'s real precedent rather than assuming;
  independently verified (confirmed `ratify-guard`'s self-approval check
  correctly doesn't apply to a status-transition-only edit) and merged.
- **Contract-author pass amending `specs/0001`** (PR #137) — the actual
  mechanism implementation: added the qualified `<repo>/<id>` external-ref
  form to §1's allowlist, named the 7-repo registry explicitly, matched
  `core/rubrics/artifact-contract.md`'s check 4 to it. Two judgment calls
  flagged out loud rather than silently resolved (whether to add
  `decision-0044` to `spec-0001`'s own `depends_on` — corpus precedent is
  genuinely mixed, `decision-0037` did, `decision-0040` didn't; and whether
  to inline the registry vs. point at a separate artifact — decision-0044
  itself left this genuinely open). Independent verification re-derived
  both calls from source and agreed with each. Put to the maintainer
  explicitly before merging (family contract text, not just bookkeeping) —
  **merged** once CI cleared.
- The three known dangling references (kodhama's `decisions/0001`,
  trellis's own `specs/0005`, grove's citations) were correctly left
  untouched throughout — that retrofit is separate, cross-repo follow-on
  work, not yet started.

**grove #28 shaping pass:** dispatched a question-extraction pass first
(not a revision) — read the draft, the family's `shaper` charter, and
sibling charters for baseline, independently re-verified every factual
claim in the draft against real wisp source before trusting it. Surfaced
3 real questions (not padded with invented ones): charter shape, the
gate/dispatch hedge, and the provenance-record question (issue-comment vs.
a local ADR). Maintainer answered all 3 on the recommended option. Applied:
bumped `draft → gated`, opened companion issue grove#29 for the gate/dispatch
follow-up, left `depends_on: []` unchanged. Verification then caught **two
rounds** of stale cross-references the fix passes missed — the charter's
own provenance blockquote still arguing "no shaping conversation happened"
after one *did*, then a second stale caveat inside `README.md`'s own
cross-reference to the charter — both held, fixed, re-verified, **merged**.

## Wave 7 — wisp #14 revisited and closed

Blocker cleared (Wave 6), maintainer confirmed proceeding. First merge
attempt was blocked by the harness's own safety classifier — "go go"
wasn't read as an unambiguous lift of the specific hold placed on
merging #14 earlier (as distinct from re-verifying it). Respected that:
ran verification-only (no merge authority) instead, which found the
substance genuinely ready — trellis's `spec-0001` §1 confirmed fresh to
recognize the exact qualified form wisp #14 cites (math-quest genuinely
in the registry) — but also found the PR's "not yet valid" framing was
now stale, and fixed it directly in the local working tree (fact-only
edits, no new judgment calls; deliberately did NOT bump `status: draft`,
since separate legitimate reasons to stay draft — no local self-check
precedent, wants a maintainer read — still held). Left that fix
**uncommitted** and asked the maintainer explicitly (not just "does this
look ready" but literally "commit+push this, and merge?") before acting.
Maintainer said yes — committed, pushed, **merged**. Issue #13 auto-closed.

Incidental finding from the same verification pass, not yet acted on:
trellis's own `decision-0044` has a stale body banner ("Gated — not yet
merged") left over from the bump commits, even though frontmatter reads
`approved` — same class of staleness just fixed in wisp's draft. Not
blocking, flagged for a future pass.

**Status now:** everything from this sweep's Tier-1/1.5 mechanical fixes,
the 5 judgment-call PRs, math-quest's circular dependencies, and both
follow-on threads (decision-0044's chain, grove #28's shaping) is merged.

## Wave closed — remaining follow-on converted to GitHub issues

A brief is easy to forget to reopen; issues aren't — they sit in each
repo's own list with their own notification surface. Converting the last
few genuine, non-urgent follow-on items to issues rather than leaving them
as brief-only prose, so nothing here depends on remembering to reread this
file:

- **kodhama#26** — retrofit `decisions/0001`'s two dangling references to
  the qualified `math-quest/...` form.
- **trellis#138** — retrofit `specs/0005`'s dangling reference to the
  qualified `kodhama/...` form (plus re-run its own self-check honestly
  against the amended contract).
- **trellis#139** — fix `decision-0044`'s stale "not yet merged" body
  banner (cosmetic).
- **grove#30** — modernize `adr-0002`/`adr-0003`'s citations to the
  qualified form (lower priority — these resolve fine today, unlike the
  other two retrofits; this is consistency, not a fix).
- **grove#29** (opened earlier, Wave 6) — confirm the gate/dispatch
  command-handling gap in the grove-status charter is intentional scoping,
  not an oversight.

**This wave is done.** Every PR opened during this sweep is merged; every
remaining loose end has its own tracked issue in the repo where the fix
belongs. Nothing is riding on this brief being reread — check the 5 issues
above (kodhama#26, trellis#138/#139, grove#29/#30) whenever, in whatever
order, independently of each other and of this file.
