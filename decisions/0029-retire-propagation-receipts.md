---
id: kodhama-0029-retire-propagation-receipts
type: decision
status: approved  # maintainer intent act 2026-08-03, in session: "approved" — an in-PR flip recording that act, per .grove/lifecycle.md's gated -> approved mover rule; the merge performs the ship. The agent did not open the gate. Raised by the maintainer the same day: "This is turning into a lot of bureaucracy", then "I still want to be able to track decisions to where they were made. Just not in a bureaucratic way" — which is Decision 3
depends_on: [kodhama-0008-family-inheritance-restate-nothing, kodhama-0022-propagate-collective-strategy, kodhama-0027]
owner: agent
updated: 2026-08-03
provenance: "maintainer direction, 2026-08-03, on being shown the cost: nine receipt artifacts drafted for one convention, each restating nothing and authorising nothing. The four cross-link ADRs and five product-ownership issues were closed unmerged rather than landed. kodhama-0022 §4's return path had already been retired by kodhama-0027 D2 two days earlier, unnoticed."
---

# 0029 — retire the propagation receipt

## Why

`kodhama-0022` requires one hand-authored document per affected repository per
strategic decision. Applying it to `kodhama-0026` produced **nine artifacts** —
four cross-link ADRs and five product-ownership issues — none of which could
state anything, because `kodhama-0022` §2 forbids repeating definitions,
rationale, criteria or obligations, and §3 forbids making any product decision.
A document whose permitted content is a link and an acknowledgement.

Three things have changed since 2026-07-25, and each weakens the case that
produced it.

**1. Its return path no longer exists.** §4 requires *"one Stewards conductor
brief"* to link every landed ADR, and holds that a propagation *"closes only
after every target is linked."* `kodhama-0027` D2 forbids exactly that artifact
— *"no checkbox lists, no per-item status"* — and D5 made existing briefs
archive. The last one closed 2026-08-02 with its propagation lane unticked.
**Neither record cites the other**, so `kodhama-0022` has been unsatisfiable for
two days without anything saying so.

**2. A better mechanism arrived.** `kodhama-0027` moved work to issues, and
`kodhama-0026` gave them cross-repo `Epic` and native sub-issue edges. That
delivers the bidirectional navigation §4 was built for — and it updates as a
side effect of the work rather than by hand, which is precisely the failure
`kodhama-0027` retired the brief over.

**3. Adoption is now self-evidencing where it matters.** `kodhama-0022`'s stated
problem was that a strategy *"can become authoritative without appearing in an
affected plugin's local decision graph."* For `kodhama-0026` the evidence is the
backlog: 144 typed issues, no legacy prefix anywhere. A receipt asserting the
convention had been received would have been the weakest evidence available.

The approved family-consolidation wave already mandates this direction — *"cut
recurring ceremony."*

## Decision

**1. No repository writes a receipt for a collective strategic decision.**
`kodhama-0022` §2, §3 and §5 are retired with the artifact they describe.

**2. `kodhama-0008` §4 returns to absolute.** §5 of `kodhama-0022` carved the
only exception to *"repos restate nothing"*; with the receipt gone the carve-out
goes too. No repository hand-authors a record of collective strategy in any
form.

**3. Traceability rides the carrier.** **Anything that carries a collective
decision's effect names the deciding record by id** — in `implements:`,
`depends_on:`, or a `Provenance:` line, whichever the artifact type already
uses. This is the requirement the receipt was a poor substitute for: standing
in front of a rule, you can reach the record that made it.

It is not new. It is already the practice everywhere it matters, unmandated:

- `plugins/kodhama/skills/issues/SKILL.md` — `implements: kodhama-0026-issue-taxonomy`
- `.grove/lifecycle.md` — *"Provenance: created per `adr-0008-lifecycle-enum-companion`"*
- `.grove/versioning.md` — *"Provenance: created per `adr-0010-versioning-is-operational`"*

**An id is a locator.** `kodhama-NNNN` is unique across the spirit and steward
repositories (`kodhama-0009`), and cross-repo referents are qualified
(`grove/adr-0026`, `trellis/decision-0044`). So the id alone resolves to one
record without any repository holding a map.

**This is a forward lookup and that is deliberate** — from the artifact you are
holding to the decision behind it, which is where the question actually gets
asked. A carrier that names no record is the defect to look for.

**4. A strategic decision still names the repositories it affects, inside
itself.** `kodhama-0022` §1, kept — it costs a section in a record being written
anyway.

**Recorded honestly: §1 has been complied with once in four.** `kodhama-0021`,
`kodhama-0023` and `kodhama-0025` carry no propagation section; only
`kodhama-0026` does, and only because a wave brief made it a lane. So the
reverse lookup — *"which decisions bind this repository?"* — is **not** reliably
answerable from the corpus today, and this record does not pretend otherwise.
Fixing that is writing one section in future decisions, not a new artifact.

**5. Where a decision creates local work, that work is tracked as a cross-repo
`Epic` with one sub-issue per repository it creates work in** — per
`kodhama-0027` and `kodhama-0026`. The Epic closes when its children do. This
replaces §4's conductor ledger.

**6. Where a decision creates no local work in a repository, nothing is filed
there.** That is the whole saving, and it is why Decision 5 is scoped to
repositories with work rather than to every affected repository: a sub-issue
that exists only to be closed is the empty artifact this record retires, wearing
a different shape. **Silence means nothing was owed, not that nothing was
received** — Decision 3 carries the receiving.

**7. The two completed propagations stand.** `kodhama-0021` and `kodhama-0023`
were received under the old model; grove `adr-0040`/`adr-0042`, trellis
`0062`/`0064` and wisp `adr-0012`/`adr-0013` are not retracted, retrospectively
amended, or held against this record. `kodhama-0022` §1 already says superseded
strategy needs no retrospective receipt; the same applies to its own retirement.

## Cost, stated

**A local decision graph no longer shows collective strategy.** Decision 3
recovers the part that was load-bearing — from any carrier you reach the
deciding record — but it does not recover the *inventory*: opening a
repository's `decisions/` and seeing which collective strategies bind it.

What is left in its place is weaker in kind. Forward lookup is guaranteed by
Decision 3 and already works. Reverse lookup depends on Decision 4, which is
complied with once in four.

The bet is that a strategy producing no local work did not need a local record,
and a strategy producing local work is already visible as that work — plus a
carrier that names its record wherever a rule is actually carried.

**The failure to watch for is a rule with no traceable origin**: a constraint
in a repository that no artifact attributes to any decision. That is the
symptom this record can produce, and Decision 3 is the thing to enforce when it
appears. **If it happens anyway, this decision is the reason** — supersede it
rather than reintroducing the receipt by habit.

## Consequences

The nine artifacts drafted for `kodhama-0026` are closed unmerged. One is kept
for its content rather than its form: `kodhama/sdd-gauntlet#11` records that
nine issues there were never migrated, which is a finding, not a receipt.

`kodhama-0022` keeps `status: approved` with §1 live; §2–§5 are superseded here.
