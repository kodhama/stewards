---
id: kodhama-0028
type: decision
status: gated  # drafted by agent; awaiting the maintainer's intent act. Raised by the maintainer 2026-08-02: "Codex and other harnesses are still a target, just for a future I don't want to put a date on. That was always so, but running out of tokens in Claude made it more urgent, but with the way the knot got more tangled I should have just waited a while."
depends_on: [kodhama-0013-family-codex-native-product-support, kodhama-0021-separate-adoption-posture-from-support, kodhama-0023-separate-operational-availability-from-support]
amends: [kodhama-0013-family-codex-native-product-support]
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

**4. Until a product claims Codex support, it discloses that it does not.**
This needs no new machinery: `kodhama-0021` §2 already permits a listing when
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
- **The Codex marketplace catalog** in this repository is unaffected — it
  already carries the `kodhama-0021` §2 disclosure, marked dogfood.

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
