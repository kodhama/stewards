---
id: kodhama-0028
type: decision
status: approved  # maintainer intent act 2026-08-02, in session: "Merge it", given after being shown the full ratification packet, which stated that the gated -> approved flip was theirs and that merging performs the ship. An in-PR flip recording that act per grove/charters/lifecycle.md:61. Author (agent) != approver (maintainer). NOTE: three review findings landed AFTER that act and are in the merged record — the amends: relation removed, a self-check added, and D4 narrowed to surfaces that state a Codex posture (the previous wording contradicted this record's own Consequences). The narrowing is the only one that moves a ruling. Raised by the maintainer 2026-08-02: "Codex and other harnesses are still a target, just for a future I don't want to put a date on. That was always so, but running out of tokens in Claude made it more urgent, but with the way the knot got more tangled I should have just waited a while."
depends_on: [kodhama-0013-family-codex-native-product-support, kodhama-0021-separate-adoption-posture-from-support, kodhama-0023-separate-operational-availability-from-support]
owner: agent
date: 2026-08-02
---

# 0028 — Codex is an undated target, not a standing obligation

## Context

`kodhama-0013` is `approved` (maintainer intent act 2026-08-02) and its
direction is not in question here. One clause in it does more than name a
direction:

> Each user-facing product **must** gain a Codex-native surface; **trellis**,
> **grove**, and **wisp** are the initial **required** products.

Together with the record's *"in parallel with its existing Claude Code
support"*, that converts a target into a **standing obligation**: from the
moment it was ratified, every change on the Claude path owed a Codex
counterpart, and every divergence between the two read as a defect.

**Why it was written that way, from the maintainer, 2026-08-02:**

> *"We went there because I ran out of tokens on Claude. So my instinct was to
> try to increase the support for Codex … it did increase the support, but at
> the same time it set the model on a task that created more machinery and more
> craziness than it removed. So now I'm still paying that price."*

And, correcting the reading that this is a withdrawal:

> *"Codex and other harnesses are still a target, just for a future I don't want
> to put a date on. That was always so."*

So the urgency was a **capacity constraint on the maintainer's Claude usage**,
not a product finding. The target predates it and outlives it. What does not
survive is the deadline the obligation implies.

### The obligation is not being met, measured

Trellis is the first of the three named required products. On `main`,
2026-08-02:

- **The core mechanism is unverified.** `trellis#199` — *"Whether the Codex
  SessionStart hook works against a live session"* — is open. The hook exists
  and is tested against fixtures; nothing has exercised it in a real Codex
  session.
- **A defect class fixed on the Claude side is still open on the Codex side.**
  `trellis#214` — `block-codex.md` validates delivery by prose landmarks, the
  exact shape `#212` removed everywhere on the Claude path.
- **There is no distribution.** `trellis#220` — *"Codex support exists as a
  capability but not as a distribution."*
- **Trellis does not govern itself on Codex, and that was ratified.**
  `trellis/decision-0071` D5 accepts the repository is ungoverned on Codex
  until `#220` closes.

A record that says a product **must** have native Codex support, sitting above
a product that has an unverified mechanism, a known unfixed defect and no
distribution, is not describing the world. It is accruing debt in the reader's
name.

### The parity clause is the expensive half

The cost is not the Codex code. It is the obligation to keep two paths
consistent, and it lands on work that has nothing to do with Codex. Two
instances from this week alone:

- Retiring `/trellis:setup` (`trellis/decision-0072`) drew a review finding that
  the retirement *"removed the only documented way a Codex consumer gets
  governed"*. The first fix wrote a Codex adoption path into the plugin README —
  new prose, on an unsupported path, produced by a Claude-path cleanup.
- The same README asserted project-scope adoption **host-neutrally**, in a file
  titled *"for Claude Code and local Codex"*. That was false on Codex:
  `trellis/decision-0070` D7 and `codex-context.mjs` both make the config file
  the adoption signal there. A parity claim written without a parity measurement.

Undating the tranche while leaving *"in parallel with"* in force would remove
the deadline and keep the tax — the worst available combination.

## Decision

**1. `kodhama-0013`'s direction stands, unchanged.** Native Codex support
remains a delivery target for every user-facing Kodhama product, and Codex
plugin distribution remains the preferred mechanism. This record does not
supersede that record; it amends two of its clauses.

**2. The target carries no date, and no product is required to reach it.**
`kodhama-0013`'s *"must gain a Codex-native surface"* and its **required**
initial tranche (trellis, grove, wisp) are amended to a **named intent without a
schedule**. No product is out of compliance for lacking Codex support, and no
wave owes Codex work by virtue of this decision alone.

**3. Parity is not owed in the meantime.** `kodhama-0013`'s *"in parallel with
its existing Claude Code support"* is amended: a Claude-path change does **not**
oblige a Codex counterpart, and a divergence between the two paths is an
**expected consequence of the undated state, not a defect to file**. A Codex
issue is opened when someone wants Codex to work, never because Claude moved.

**4. A surface that states a Codex support posture states it as undated.**
The trigger is a surface that *says something about Codex support*, not every
surface that mentions Codex: product documentation, READMEs, a listing's support
sentence. This needs no new machinery: `kodhama-0021` §2 already permits a listing when
*"the listing or linked product documentation clearly discloses that support is
not claimed"*, and `kodhama-0023` already separates operational availability
from support. What this decision adds is that the disclosure is **required**
rather than merely permitted, and that it must say the target is undated rather
than reading as withdrawal — *"not supported yet"*, not *"not supported"*.

**5. Existing Codex machinery is retained, not removed.** The hooks, manifests
and catalog entries already built stay where they are. They are the asset the
undated future is built from, and deleting them would spend more than carrying
them costs — carrying costs nothing once D3 removes the consistency obligation.
This does not authorize new Codex machinery; see D6.

**6. Leaving the undated state is an explicit act.** A product claims Codex
support by a decision that names the surface, the evidence, and the
distribution — not by accumulating enough machinery that support seems implied.
`kodhama-0013`'s existing distinction holds: *"Native support and plugin
distribution are related but distinct completion claims … the former must never
be relabelled as the latter."*

## Consequences

- **`kodhama-0013`** gains `superseded_in_part_by: [kodhama-0028]` — its two
  amended clauses named exactly. Its direction, its Grove delivery record, its
  Spore deferral and its parked question are untouched.
- **`trellis/decision-0071` D5** stops being an exception that needs closing.
  Trellis being ungoverned on Codex is the expected state under D2, not a debt.
- **`trellis#220`, `#214`, `#199`** stay open and stay unscheduled. They
  describe what a supported Codex path would need; none of them is now blocking
  anything.
- **Product documentation** that names Codex must satisfy D4. `trellis`'s plugin
  README is updated in `kodhama/trellis#227`; the remaining surfaces are not
  swept by this record.
- **The Codex marketplace catalog** in this repository is out of D4's scope, and
  the reason matters: its entries make *no support claim at all* rather than
  stating a Codex posture, so there is nothing in them that could read as
  withdrawal. An earlier draft of this record called them "already compliant",
  which was an over-claim — they carry `kodhama-0021` §2's no-claim disclosure,
  which is a different thing from D4's undated-target disclosure. If a catalog
  entry ever states a Codex posture, D4 fires on it.

## What this does NOT decide

- **It does not retire Codex support, or any harness.** D1 is the whole answer
  to that question.
- **It does not rule on which harness comes next.** "Other harnesses" appear in
  the maintainer's framing; `trellis/decision-0069` already retains the manual
  copy path for harnesses the plugin does not cover. Whether any specific
  harness becomes a named target is a separate decision.
- **It does not sweep existing Codex prose across the family.** D4 states the
  requirement; finding every surface that violates it is work, not a ruling.
- **It does not touch `kodhama-0012`'s catalog channel** or any admission rule.

## Open questions

1. **Does D3 need a carrier in the test suites?** Today a Codex/Claude
   divergence is caught, if at all, by a reviewer noticing. Under D3 that is
   correct — but there is no marker distinguishing *"diverges, expected"* from
   *"diverges, nobody looked"*. Worth an issue rather than a clause here.

## Self-check

Run before the `draft → gated` promotion, recorded honestly rather than passed
silently.

| check | verdict |
|---|---|
| Type and required sections | **PASS** — `type: decision`; Context, Decision, Consequences, What this does NOT decide, Open questions all present. |
| Directional flow | **PASS** — `depends_on` names `kodhama-0013`, `-0021`, `-0023`, all `approved`. No dependency is `draft`. |
| Author ≠ approver | **PASS** — drafted by agent, `gated`; the flip is the maintainer's act. |
| Supersession integrity | **PASS** — `kodhama-0013` gains `superseded_in_part_by: [kodhama-0028]` in frontmatter only, naming the two amended clauses. Its body is not edited; append-only holds. |
| Claims verified against source | **PASS for the four evidence rows** (`trellis#199`, `#214`, `#220`, `decision-0071` D5 — each read on `main` 2026-08-02) and **for both quoted `kodhama-0013` clauses**. |
| Relation vocabulary | **FAILED, then fixed.** An earlier draft carried `amends:` in frontmatter — a relation this family does not define and no other record uses. Removed; the amendment is carried by `kodhama-0013`'s `superseded_in_part_by` pointer and by D1–D3 in prose. |
| Internal consistency | **FAILED, then fixed.** D4 originally read as firing on any surface, and the Consequences then asserted the Codex catalog was "already compliant" — two statements that could not both hold. D4 is now scoped to surfaces that state a Codex posture, and the catalog line says why it is out of scope instead of claiming compliance. |
| Scope discipline | **PASS** — two files. This record does not sweep Codex prose, does not name a next harness, and does not touch `kodhama-0012`'s catalog channel. |

Two of the eight failed on first pass. Both were found by an independent
reviewer on the PR, not by the author, which is the honest reading of this
table: the self-check as run by the author alone would have recorded eight
passes.

The check passes, so the record is promoted `draft → gated`. It was then
`approved` on the maintainer's in-session intent act — *"Merge it"* — given
after they were shown the ratification packet. The three findings above landed
between that act and the merge; D4's narrowing is the only one that moves a
ruling, and it moves it toward what the Consequences already said.
