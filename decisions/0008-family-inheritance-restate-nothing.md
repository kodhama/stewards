---
id: kodhama-0008-family-inheritance-restate-nothing
type: decision
status: approved  # maintainer's intent act 2026-07-12 ("approved. flip it and merge after", PR #35) — in-PR flip recording the act; the #35 merge performs the delivery
depends_on: [kodhama-0004-uniform-lifecycle, kodhama-0007-one-render-many-copiers, trellis/decision-0046, grove/adr-0008]
owner: agent
updated: 2026-07-12
provenance: shaped on PR kodhama/kodhama#35 (2026-07-12) — two independent spec-adversary rounds and three maintainer re-shape calls; the full shaping history, including the grove source check that found the approval mechanic already encoded operationally, lives on that PR. Final maintainer call, same day — "sometimes we are putting too much bureaucracy" — cut to a minimal supersession record: the rollout program moved to conductor/wave-0008-rollout.md, the layering orientation line to CLAUDE.md. DRAFT — the maintainer's approval (the intent act) is pending; the intent gate is not opened by an agent.
---

# Decision (DRAFT): kodhama-0004 superseded in part — no approval mechanic is defined at the meta layer, and the per-repo restatement mandate retires

## Why

kodhama-0004 (approved) fixed the approval mechanic family-wide (*"`approved` = human PR merge; nobody writes `approved` inside the PR's own diff; a post-merge bump commit records the act"*) and mandated a hand-authored lifecycle section in every repo (AC1). trellis/decision-0046 (approved 2026-07-11) legitimately revised that mechanic for trellis-self — and the revision could not propagate: every hand-authored copy went stale. The conflict is verified and quoted in full on PR #35; the duplication AC1 mandated is what made it fester.

## Decision

1. **Superseded in kodhama-0004:** the mechanic clause (the third Decision bullet), its Execution-step restatements (steps 2, 3, and 5), AC1, and its parked open question (a post-merge-bump CI check — mooted with the mechanic). The uniform enum and the no-historical-rewrite rule **stand**.
2. **Nothing replaces the mechanic here.** No kodhama-meta artifact defines how the approval act is performed or recorded — this decision included.
3. **Why that is stable:** mechanics are operational content, and operational content is grove's; principles are trellis's, stated mechanism-free. (The layering line lives in CLAUDE.md as family orientation; grove already encodes the mechanic in its lifecycle companion, `charters/lifecycle.md`, approved 2026-07-12.)
4. **Repos restate nothing.** The operating model and the principles arrive by installing the plugins — never hand-authored per repo (kodhama-0007's "one render, many copiers," generalized past the flow rules). That is why AC1 retires instead of being rewritten.

## Done when

- kodhama-0004 carries `superseded_in_part_by: [kodhama-0008-family-inheritance-restate-nothing]` and each superseded clause its in-place forward pointer (lands with the approval PR).
- The rollout brief `conductor/wave-0008-rollout.md` is open and fires on this approval; rollout completion is the **brief's** ledger, not this record's.

## Open questions (both resolved at approval, 2026-07-12)

- **Bootstrap — resolved:** the maintainer named the act: **in-PR flip records it, merge follows** ("approved. flip it and merge after").
- **math-quest — resolved: deferred.** math-quest inherits the model from grove like any adopter; its stale copy is **math-quest's own issue**, not this wave's scope. The wave's delete list is the four family repos.

## Self-check (gate)

Minimal supersession record by maintainer instruction (PR #35); the shaping history, both adversary verdicts (rounds 1 and 2, each NEEDS-REVISION, all findings folded before the cut), and the rollout program live on the PR and in the wave brief, not here. Supersession is scoped clause-by-clause; the enum and the append-only rule are preserved; nothing consumed is a draft (all four `depends_on` are approved). An independent look at the final one-page shape was offered and waived by the maintainer at approval — stated here, not silently skipped; both earlier shapes were independently adversaried. **Approved** — the maintainer's intent act (2026-07-12, PR #35: "approved. flip it and merge after") is recorded by this in-PR flip; both parked questions were answered in the same act. The builder did not grade its own decision and did not open the gate.

## Proposed forward annotation — kodhama-0022 (draft, 2026-07-25)

Draft `kodhama-0022-propagate-collective-strategy` proposes to narrow only the
implication that no hand-authored per-repository record may acknowledge a
collective strategic decision. Under that proposal, affected plugin
repositories receive thin, reference-only cross-link ADRs. The ban on copying
or redefining shared principles, operating mechanics, and canonical
terminology remains current. This annotation is non-operative unless decision
0022 is ratified.
