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

**Lane A — trellis (principle, merge-free):**
- [ ] catalog `floor-intent-gate`: drop the merge-hardwired example
      (*"here: the maintainer's merge"*); state the principle as a human
      intent act, mechanism-agnostic
- [ ] re-render the payload (`plugins/trellis/reference/*`), bump
      `version` + `checksums` (kodhama-0007)

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

**Converge — per repo, order matters:**
- [ ] confirm `.grove/lifecycle.md` is installed + sourced **before** any
      deletion (kodhama has no `decisions/README.md` fallback at all)
- [ ] refresh each family repo via `/trellis:setup` + grove re-vendor
      (copier channels only — never per-repo hand-edits)
- [ ] `expression.md` split-migration for grove, kodhama, wisp,
      design-system (old combined layout; `/trellis:setup`'s #112 guard
      stops on the hand-appended block until it moves)
- [ ] delete the stale hand-authored lifecycle statements: grove, kodhama,
      wisp, design-system (kodhama#33). In grove, what remains is the
      mechanic half — grove#48 already reduced its enum restatements to
      pointers. math-quest: **deferred at approval** — math-quest's own
      issue, off this ledger
- [x] kodhama-0004: `superseded_in_part_by` + per-clause forward pointers
      (landed with the approval PR — same commit as the flip)
- [ ] close kodhama#29; update the kodhama#31 checkpoint

## Parked (to the maintainer, carried on the decision)

- ~~Bootstrap: which act approves kodhama-0008~~ — answered: in-PR flip,
  then merge.
- ~~math-quest: in-scope or deferred~~ — answered: deferred to
  math-quest's own tracker.
