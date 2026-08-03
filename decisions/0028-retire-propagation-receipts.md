---
id: kodhama-0028-retire-propagation-receipts
type: decision
status: gated
depends_on: [kodhama-0008-family-inheritance-restate-nothing, kodhama-0022-propagate-collective-strategy, kodhama-0027]
supersedes: [kodhama-0022-propagate-collective-strategy]
owner: agent
updated: 2026-08-03
provenance: "maintainer direction, 2026-08-03, on being shown the cost: nine receipt artifacts drafted for one convention, each restating nothing and authorising nothing. The four cross-link ADRs and five product-ownership issues were closed unmerged rather than landed. kodhama-0022 §4's return path had already been retired by kodhama-0027 D2 two days earlier, unnoticed."
---

# 0028 — retire the propagation receipt

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

**3. A strategic decision still names the repositories it affects, inside
itself.** This is `kodhama-0022` §1 and it survives unchanged — it costs a
section in a record that is being written anyway, and it is what makes the
affected set reviewable.

**4. Propagation is tracked as a cross-repo `Epic` with one sub-issue per
affected repository**, per `kodhama-0027` and `kodhama-0026`. The Epic closes
when its children do. This replaces §4's conductor ledger.

**5. Work is the receipt.** A sub-issue exists only where the decision creates
local work. **Where a decision creates none, nothing is filed** — that is the
whole saving. Silence means nothing was owed, not that nothing was received.

**6. The two completed propagations stand.** `kodhama-0021` and `kodhama-0023`
were received under the old model; grove `adr-0040`/`adr-0042`, trellis
`0062`/`0064` and wisp `adr-0012`/`adr-0013` are not retracted, retrospectively
amended, or held against this record. `kodhama-0022` §1 already says superseded
strategy needs no retrospective receipt; the same applies to its own retirement.

## Cost, stated

**A local decision graph no longer shows collective strategy.** That was
`kodhama-0022`'s real contribution and this record gives it up. What replaces it
is weaker in kind: the upstream decision names the repository, and any local
work is an issue in it.

The bet is that a strategy producing no local work did not need a local record,
and a strategy producing local work is already visible as that work. **If a
strategy is ever adopted family-wide and leaves no trace in an affected
repository, this decision is the reason** — supersede it rather than
reintroducing the receipt by habit.

## Consequences

The nine artifacts drafted for `kodhama-0026` are closed unmerged. One is kept
for its content rather than its form: `kodhama/sdd-gauntlet#11` records that
nine issues there were never migrated, which is a finding, not a receipt.

`kodhama-0022` keeps `status: approved` with §1 live; §2–§5 are superseded here.
