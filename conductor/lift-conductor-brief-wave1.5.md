---
id: plan-lift-conductor-brief-wave1-5
type: plan
status: gated
depends_on: [plan-suite-lift, plan-lift-conductor-brief]
rubric: rubrics/spec-quality.md
owner: agent
updated: 2026-07-07
---

# Conductor brief: kodhama lift, wave 1.5 (cleanup — repatriation + one decision)

Wave 1 landed (see `plans/plan-suite-lift.md` §Wave 1). Two follow-ups
remained because the maintainer launched wave 1 from a brief snapshot
predating these sections. **Standing grants G1–G3 from
`plans/lift-conductor-brief.md` apply here too** — this wave needs zero
human touches unless a lane genuinely blocks. Run from the same
`kodhama/kodhama` local seat (already bootstrapped); no rebuild of T1/A/B
needed.

## Lane R — repatriation (now, not blocked on anything)

Move the remaining org-level artifacts out of the math-quest branch
(`claude/agentic-runtime-viz-x1884q` in `gundisalwa/math-quest`) to their
kodhama homes, exactly as specified in
`plans/lift-conductor-brief.md` §Lane R:
- `plans/plan-suite-lift.md` → `kodhama/kodhama/conductor/suite-lift-plan.md`
- `plans/lift-conductor-brief.md` + `plans/kodhama-meta-bootstrap.md` +
  `plans/lift-conductor-brief-wave1.5.md` (this file) → `kodhama/kodhama/conductor/`
- `tools/espalier/identity/` (marks, grammar, preview) → `kodhama/design-system`
  (T1 already consumed these as source; this makes the repo their home,
  not a second copy — dedupe, don't just add)

Then ONE slimming commit on the math-quest branch: delete the moved
files, leave a 5-line `plans/suite-lift-pointer.md` (frontmatter
`status: superseded`, one paragraph: what moved where, dated) and add
the same style pointer to the top of `discovery/kodhama-delivery.md`
(it already has one for the delivery decision — extend it, don't
duplicate, to also point at the plan's new home). Do NOT touch
`tools/espalier/viz/`, `test/espalier-viz-protocol.test.ts`, the
`espalier-status` skill, tsconfig/gitignore touches, or
`discovery/espalier-runtime-viz.md` — those stay in math-quest for the
maintainer's product review (unchanged from the original Lane R spec).

The math-quest branch stays UNMERGED — this lane only slims it for
review, never merges it.

## Lane S — supersede trellis decision-0032

`kodhama/trellis`'s `decisions/0032-homebrew-distribution.md` names the
pre-family per-product tap model (`gundisalwa/homebrew-trellis`) and is
stale after the family-tap move (`kodhama-0001-family-delivery` +
`chore/family-tap` PR #103, already merged). Per the org's append-only
decision rule (ADRs supersede, never edit): author
`decisions/0033-family-tap-supersedes-0032.md` in `kodhama/trellis` —
short: what changed (tap → `kodhama/homebrew-tap`, one tap/many
formulas), why (`kodhama-0001`), forward pointer from 0033; then edit
0032's own frontmatter/header to add `superseded-by: 0033` (the ONE
mutation an accepted decision may take — a forward pointer, never its
content). PR against `kodhama/trellis` main (product repo — PR always,
per the ground rules); **G1-style self-merge applies**: merge it
yourself iff the diff touches only `decisions/0032*` and the new
`decisions/0033*` file — anything else in the diff → park instead.

## Order

Lanes R and S are independent — run in parallel. Neither depends on
T1/A/B (already landed) or on each other.

## Wave report

Same format as wave 1: what landed, verification run, open items. Append
to `kodhama/kodhama/conductor/wave-1.md` under a `## Wave 1.5` heading
(don't create a new ledger file — one home for the wave-1 record).
Paste-ready summary back to the math-quest session when done.

## Acceptance criteria

- AC1: math-quest branch diff is now product-scoped only (`git diff
  --stat` shows no `plans/plan-suite-lift.md`,
  `plans/lift-conductor-brief*.md`, `plans/kodhama-meta-bootstrap.md`,
  or `tools/espalier/identity/`).
- AC2: both pointer stubs exist and resolve (link to real files at
  their new homes).
- AC3: `kodhama/trellis` decisions/ contains 0033 with a working forward
  pointer from 0032.
- AC4: no lane touched anything outside its enumerated scope (grep-checkable).
