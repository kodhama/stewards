# Wave: T3 (tokenize trellis LP) + B3 (wisp GitHub adapter)

Opened 2026-07-08. Authorization: maintainer — "Do T3 + B3 and we'll
evaluate after." Scope fixed by the suite-lift plan: T3 (§Phases/Lane T,
"tokenize the trellis LP") closes AC6's remaining derivative; B3
(§Phases/Lane B, "adapters") closes AC3's round-trip requirement.

Model economy: both lanes dispatched on Sonnet 5 (enumerated execution
lanes); conductor (Fable, this session) verifies independently.
PR-first policy applies to trellis and wisp (human ruling, wave-2 entry);
no agent merges anything.

## Ledger

- [x] T3: trellis `docs/lp-content.md` extracted + `docs/index.html`
      regenerated per `lp-generator.md` @ DS `v0.1.0`, parity vs the
      hand-built page evidenced — [trellis PR #105](https://github.com/kodhama/trellis/pull/105)
- [x] B3: wisp GitHub adapter (comments emitter + check-equivalent
      reader), offline round-trip tests green, live smoke evidenced,
      genericity budget documented — [wisp PR #5](https://github.com/kodhama/wisp/pull/5)
- [x] Conductor: independent verification of both lanes (not builder
      claims) — see report
- [x] Report appended; wave closed pending PR merges

## Parked

- DS `v0.1.0` `patterns.md` carries a stale install example
  (`brew install kodhama/trellis/trellis`, pre-decision-0041; lines
  123/139) — found by the T3 lane, independently confirmed by the
  conductor against the tag. Not trellis's to fix (install content is
  the product's per the generator contract); routed to whoever cuts the
  next DS tag — naturally the in-flight T2 pass.

## Report

Executed 2026-07-08. Both lanes dispatched in parallel on **Sonnet 5**
(per model economy; conductor on Fable). Lane cost: T3 ≈ 97k subagent
tokens / 28 tool uses; B3 ≈ 72k / 31.

**T3 — landed as [trellis PR #105](https://github.com/kodhama/trellis/pull/105)
(open, not merged).** `docs/lp-content.md` (new, 213 lines) +
`docs/index.html` gains only a 21-line DS provenance stamp block —
additive-only, `docs/invariants.html` untouched. Conductor verification:
diff scope confirmed (2 files, +234/−0); **43/43 unique token
declarations identical** to `v0.1.0` `tokens.css` (normalized
extraction; the conductor's first two comparison attempts were its own
regex artifacts — one-sided dedup, then `^`-anchored `grep -o` missing
packed declarations — documented here so nobody re-runs the broken
checks). Self-containment holds trivially (the only functional-file
change is an HTML comment). The lane's stylistic call (no retroactive
`patterns.md` attribution comments — parity over decoration) is
endorsed. AC6's last derivative gap closes when this merges.

**B3 — landed as [wisp PR #5](https://github.com/kodhama/wisp/pull/5)
(open, not merged).** `github.ts` (196 lines: config, emitter, reader,
CLI) + `test/github.test.ts` (10 offline tests, fetch mocked) + README
§Adapters. Conductor verification, not builder claims: fresh `npm test`
**36/36 green**, `tsc --noEmit` clean, diff scope 3 files additive-only,
protected files (protocol/bus/emit/server/dashboard, package.json)
zero-diff — **zero new dependencies**; no old family names introduced;
live-smoke scratch issue kodhama/wisp#4 independently confirmed CLOSED
(round-trip deep-equal true per the lane's evidence; comment deleted).
The lane's one interpretation call — vacuity parity with `readBus`
(missing-vs-empty collapse identically, matching the existing transport
rather than inventing metadata) — is reasoned, documented inline, and
endorsed as exactly the genericity budget's intent. AC3's round-trip
requirement closes when this merges.

**Human gates:** merge trellis #105 and wisp #5 (plus this ledger PR).
Nothing else dispatched; T2 remains with the parallel design process,
now also owed the parked patterns.md staleness above.
