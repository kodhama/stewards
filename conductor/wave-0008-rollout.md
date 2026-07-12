# Wave: kodhama-0008 rollout — de-merge the principle, align grove, delete the stale copies

Opened 2026-07-12. Authorization: **maintainer approved kodhama-0008 the
same day** ("approved. flip it and merge after", PR #35) — the in-PR
status flip records the act. **Wave is live.** Both parked questions were
answered at approval: the act = flip + merge; math-quest = deferred (it
inherits from grove like any adopter; its stale copy is math-quest's own
issue — **not yet filed**: an add-to-session was attempted 2026-07-12 and
refused by the platform's same-owner restriction (gundisalwa-tier repo,
kodhama-tier session), so it needs a math-quest-sourced session or a
manual filing; the debt stays recorded here, loudly).

Context: kodhama-0008 withdraws the approval mechanic from the meta layer
and retires kodhama-0004 AC1's per-repo restatement mandate. The rollout
mechanics below were shaped and twice adversaried on PR #35 before the
maintainer cut the decision to a minimal supersession record and moved the
program here. Source-verified facts are from a 2026-07-12 check of
grove@3ec08a5.

**Already true (verified in grove source, 2026-07-12):**
- the approval mechanic is encoded in grove's `charters/lifecycle.md`
  §"Who moves an artifact between states" (the adr-0008 companion,
  approved 2026-07-12) — **no new grove decision is needed**;
- grove `decisions/README.md` defers state semantics to that companion
  (its old "never set by hand" self-contradiction is gone);
- the enum home is executed (adr-0008 / grove#48): companion installed to
  consumers at `.grove/lifecycle.md`, `corpus-reviewer` repointed.

Scope notes carried from the shaped ACs: "restatement" = the living,
propagated-adjacent surfaces (profile lifecycle sections, charters,
READMEs/CLAUDE.md rule blocks); append-only `decisions/` history and
per-repo `expression.md` dials are exempt; bare pointers to the
plugin-carried source are fine. Each lane lands as its own PR in its own
repo.

## Ledger

**Lane A — trellis (principle, merge-free):** **DONE — trellis#149
merged 2026-07-12** (rebase, head `b35455e`), conformance-gated. The
directive-verb-list question was RULED by the maintainer (de-merge
targets mechanic *mappings*; the "finalize, ship, or merge" delivery-act
list stands) — ruling recorded in the catalog's amendment note itself.
- [x] catalog `floor-intent-gate`: merge-hardwired example dropped;
      principle stated as a human intent act, mechanism-agnostic
- [x] re-render the payload + bump `version` + `checksums`
      (kodhama-0007) — landed as `payload@a805fd8f83d6`

**Lane B — grove (operational alignment):** **DONE — grove#49 merged
2026-07-12** (squash `49a35aa`), conformance-gated (one FAIL — a
spec-vs-product R8 divergence — found and fixed pre-PR; maintainer
merge authorization "go ahead").
- [x] sweep all 12 charters + the spec corpus for restatements of the
      superseded kodhama-0004 mechanic → each becomes a **pointer** to
      `charters/lifecycle.md`, never a fresh restatement (adr-0008's own
      single-home rule). Landed targets: `charters/shaper.md`,
      `charters/contract-author.md`, `specs/0001-contributing-guide.md`
      (R2 + R8, adr-0004 delta note), `CONTRIBUTING.md` (shaper
      exception + R8 resting-state clause)
- [x] add decision-0046's clarify-when-ambiguous rule where the act is
      consumed (shaper) — added, all three copies
- [x] re-vendor (three-copy sync). Historical ADR self-check texts:
      append-only, exempt
- [x] *(rider, maintainer rule 2026-07-12)* counter-initialization rule
      in `contract-author` step 4 (+ copies); `spec-0001` counter
      initialized at `version: 1`. The decision-0045 twin of the rule is
      a trellis-side amendment — rides Lane A if the maintainer wants it
      in the primitive too

**Converge — per repo, order matters:** *(all four items ride the five
`wave-0008-converge` PRs, 2026-07-12, gated by ONE combined
conformance review — 4 repos FAILed round 1 (dangling corpus-reviewer
contract pointers in kodhama; missed README enum/mechanic restatements
in wisp+DS; trellis contract-author half-currency + missing version
stamp; a false grove#40 deferral pointer), all fixed or re-tracked
pre-PR; boxes get checked when the PRs merge)*
- [x] confirm `.grove/lifecycle.md` is installed + sourced **before** any
      deletion (kodhama has no `decisions/README.md` fallback at all) —
      companions installed in kodhama/wisp/DS; kodhama's corpus-reviewer
      + wisp/DS READMEs repointed to the companion in the same PRs
- [x] refresh each family repo via `/trellis:setup` + grove re-vendor
      (copier channels only — never per-repo hand-edits). **Stated
      deviation:** overlay = clean byte-copies to `payload@a805fd8f83d6`;
      the grove agent copies got surgical mechanic-passage splices, NOT
      a full re-vendor — duty currency (adr-0006/0010 additions,
      trellis's contract-author step 2/4 content) is tracked as
      **grove#53** (the earlier grove#40 pointer was wrong — gate
      finding, corrected)
- [x] `expression.md` split-migration for grove, kodhama, wisp,
      design-system (old combined layout) — done in the four PRs;
      wisp needed a `.gitignore` narrowing (`.grove/` → `.grove/runtime/`;
      the runtime-bus namespace collided with adr-0008's committed
      companions — dispositioned per the grove#48 one-class-per-path
      precedent, revertable if the namespace should be re-ruled)
- [x] delete the stale hand-authored lifecycle statements: grove, kodhama,
      wisp, design-system (kodhama#33) — done in the four PRs (wisp+DS
      also had README restatements, caught by the gate, now pointers).
      math-quest: **deferred at approval** — math-quest's own issue, off
      this ledger
- [x] kodhama-0004: `superseded_in_part_by` + per-clause forward pointers
      (landed with the approval PR — same commit as the flip)
- [x] close kodhama#29; update the kodhama#31 checkpoint

## Adjacent decision spun out mid-wave (2026-07-12)

**Status:** adr-0010 APPROVED + merged (grove#50, in-PR flip).
Consequence 1 **DONE** — grove#51 merged 2026-07-12 (companion approved
by in-PR flip at the maintainer's act; cross-check duty homed
corpus-reviewer-only, maintainer deferring to the builder's
source-backed recommendation). Consequence 2 **DONE** —
**trellis#150 merged 2026-07-12** (rebase `2aa7535`; nothing on the PR
sat at `gated`, so no flip was owed — stated, not skipped):
`.grove/lifecycle.md` + `.grove/versioning.md` installed in trellis
(clears trellis's adr-0008 per-consumer prerequisite too), spec-0001 +
rubric de-reflected to shape-only, spec-0001 `version: 1` initialized,
0045 marked per-clause. **The adr-0010 arc is closed.** Riders
dispositioned: trellis's installed grove agent copies stale vs grove#51
→ the converge refresh item below; adr-0010's missing `changes:` field
→ filed as **grove#52** (`[consider]`, soft direction, no violation).


The maintainer's trellis#149 ruling generalized: **versioning is not a
principle** — sync is the principle (already trellis's); versioning is
detection mechanics → grove's. **grove adr-0010** (PR grove#50, gated,
one adversary round folded) declares the forward home: a
`.grove/versioning.md` companion; decision-0045 stays as origin record
with scoped supersession-in-part marks; trellis de-reflects (spec-0001 +
rubric → shape-only methodology-defined clauses) AFTER the companion
ships. Its trellis-side execution joins this wave's converge lane. It
also answers this brief's parked 0045-twin question: **grove-only, by
construction**.

## Parked (to the maintainer, carried on the decision)

- ~~Bootstrap: which act approves kodhama-0008~~ — answered: in-PR flip,
  then merge.
- ~~math-quest: in-scope or deferred~~ — answered: deferred to
  math-quest's own tracker.
- ~~decision-0045 counter-init twin~~ — answered by adr-0010
  (grove-only); at the maintainer's gate on grove#50.

## Wave report (closed 2026-07-12)

Opened and closed the same day. Every ledger item landed, all
maintainer-gated:

- **kodhama-0008 approved** (in-PR flip + merge, PR kodhama#35) after two
  independent spec-adversary rounds, three maintainer re-shapes, and a
  final cut to a one-page supersession record. kodhama-0004 carries the
  per-clause forward pointers.
- **Lane A** (trellis#149): catalog de-merged, mechanism-agnostic;
  directive-verb-list scope ruling recorded in the artifact.
- **Lane B** (grove#49): 12-charter mechanic sweep -> pointers to the
  lifecycle companion; clarify-when-ambiguous added; spec-0001 R2/R8
  amended with delta note; counter-initialization rule (maintainer,
  2026-07-12) added to contract-author + first applied.
- **Mid-wave spur — adr-0010** (grove#50/#51, trellis#150): versioning
  ruled operational; `.grove/versioning.md` companion shipped; trellis
  de-reflected to shape-only; decision-0045 marked per-clause;
  trellis spec-0001 counter-initialized at v1 by the new rule.
- **Converge** (kodhama#36, wisp#16, design-system#13, grove#54,
  trellis#151): all five repos byte-current at payload@a805fd8f83d6;
  `.grove/` companions installed everywhere they belong; expression
  split-migrations done; every stale hand-authored lifecycle statement
  and README restatement deleted or pointer-ized. One combined
  conformance gate FAILed four repos in round 1 (dangling
  corpus-reviewer pointers, missed README restatements, a false
  deferral pointer, trellis's missing version stamp) — all fixed
  pre-merge.

Every independent gate in this wave (2 adversary rounds on 0008, 1 on
adr-0010, 5 conformance reviews) returned real findings; all were fixed
or re-tracked before the human act, none waived silently.

Open debts, each with a tracked home: **grove#53** (full re-vendor of
consumer-installed agent copies — duty currency), **grove#52**
(adr-0010's missing `changes:` field), **trellis#148** (`cites`
relation), **grove#47** (README role), **grove#40** (grove-internal
copy-sync mechanics), math-quest's stale expression copy (needs a
math-quest-sourced session — cross-tier restriction verified 2026-07-12).
kodhama#33 closes with this wave; kodhama#29 closed at approval.
**Wave closed.**
