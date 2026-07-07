---
id: plan-lift-conductor-brief
type: plan
status: gated
depends_on: [plan-suite-lift]
rubric: rubrics/spec-quality.md
owner: agent
updated: 2026-07-07
---

# Conductor brief: execute the kodhama lift, wave 1 (local, parallel)

**You are the plan conductor** for wave 1 of the suite lift
(`plans/plan-suite-lift.md` in the math-quest source clone — read it
first; it is the authority; this brief is execution mechanics). **Your
seat is a local clone of `kodhama/kodhama`** (bootstrapped per
`plans/kodhama-meta-bootstrap.md`; this brief lives there as
`conductor/wave-1.md` and doubles as the wave ledger — tick items off
in the commits that report them). You run in a LOCAL Claude Code
session with `gh` authenticated for the `kodhama` org. Run lanes as PARALLEL subagents; batch questions to the
terminal ≤3 at a time and only when a lane is genuinely blocked; the human
is present but wants minimal micromanagement. Session model should be
Sonnet 5 (plan §Model economy) — no lane in this wave needs more.

## Preconditions (verify, don't assume)

```sh
gh auth status
for r in trellis homebrew-tap espalier espial design-system kodhama; do
  gh repo view kodhama/$r --json nameWithOwner -q .nameWithOwner; done
```

All six exist as of 2026-07-07. If any check fails: stop, tell the human.

## Setup

Clone into one workspace dir:

```sh
git clone --branch claude/agentic-runtime-viz-x1884q \
  https://github.com/gundisalwa/math-quest        # SOURCE OF TRUTH
git clone https://github.com/kodhama/trellis
git clone https://github.com/kodhama/espalier
git clone https://github.com/kodhama/espial
git clone https://github.com/kodhama/design-system
```

Source materials in the math-quest clone: `plans/plan-suite-lift.md` (the
plan), `tools/espalier/viz/` + `test/espalier-viz-protocol.test.ts` (espial's
code), `tools/espalier/identity/` (marks + grammar), `decisions/adr-0030-espalier.md`
+ `.claude/agents/` + CLAUDE.md operating sections (charter sources),
`discovery/espalier-runtime-viz.md` + `discovery/kodhama-delivery.md`
(context). Trellis's LP (the DS source): `trellis/docs/index.html`.

## Ground rules for all lanes

- **Bootstrap exception, used loudly:** first commits into the three EMPTY
  repos (espalier, espial, design-system) go direct to `main` — a PR
  against an empty repo reviews identically to the repo itself; the wave
  report says exactly what landed where. Anything touching
  `kodhama/trellis` (an existing product) goes via PR, always.
- Each lane works ONLY in its own clone; cross-lane needs are surfaced to
  you (the conductor), never reached into directly.
- Commit style: descriptive, one logical change; linear history.
- Every lane's final message = what landed, what's open, what needs the
  human. You aggregate into one wave report.
- Telemetry (optional but preferred — dogfood): run
  `node math-quest/tools/espalier/viz/server.ts` and have each lane emit
  via `ESPALIER_EVENTS=<abs path to math-quest>/.espalier/runtime/events.ndjson
  node math-quest/tools/espalier/viz/emit.ts status --run lift-wave-1
  --agent lane-<X> ...` at start/blocked/done. The human can watch
  localhost:4177.

## Lane T1 — design-system (subagent 1)

In `design-system/`: extract the DS from `trellis/docs/index.html`:
- `tokens.css` — all custom properties (light + dark + data-theme blocks);
- `patterns.md` — component patterns with their CSS as reference blocks:
  eyebrow, card, terminal (tabs/copy/prompt), lattice motif, theme toggle,
  climbing-plant animation, compare-pairs, buttons/pills;
- `icons/` — the three marks as .svg files + `grammar.md`, sourced from
  math-quest `tools/espalier/identity/` (grammar rules + the 19px test);
- `lp-generator.md` — the instruction any repo's LP furrow loads: read
  this repo at a TAG; generate `docs/index.html` from the consuming
  repo's `docs/lp-content.md` + these tokens/patterns; stamp the tag into
  a comment in the generated file (`<!-- kodhama-ds: vX.Y.Z -->`); vendor
  the output (self-contained page, no external fetches); staleness =
  stamped tag ≠ latest DS release, surfaced as a finding, never a build
  break;
- README (what this is, how it's consumed, the soft-dependency rule);
  MIT LICENSE.
Push to main, then: `git tag v0.1.0 && git push --tags`.

## Lane A — espalier (subagent 2, steps A1–A2)

In `espalier/`:
- A1: skeleton — README (what espalier is, from ADR-0030's framing),
  MIT LICENSE, `decisions/` `specs/` `charters/` dirs with READMEs
  stating their contracts (artifact frontmatter per the plan). Run
  `trellis setup` if the trellis CLI is installed locally; if NOT
  installed or it fails, copy `.trellis/` from the math-quest clone as
  the overlay snapshot and record loudly in the wave report that a real
  `trellis setup` refresh is owed.
- A2: generalize the role charters into `charters/`: sources are
  ADR-0030's team table, math-quest `.claude/agents/conformance-reviewer.md`
  (+ run-resumer, propagation-remediator, shaping-partner), and the
  espalier-relevant CLAUDE.md sections (dispatch contract, workflows
  W1–W6, bug pipeline roles, checkpoint-resume). STRIP every math-quest
  noun (Mariana, curriculum, Tier-2, issue numbers, Vercel…) — the
  acceptance check is `grep -riE "math.?quest|mariana|tier.?2|7\.º" charters/`
  returning nothing. Where a charter needs a project-specific value,
  declare a placeholder the consuming project fills (the signature-pair
  door). Also port `.claude/agents/` versions of the roles and the
  `espalier-status` skill's gardener wrapper (pointing at a vendored
  espial, path parameterized).
Push to main. Do NOT do A3 (LP) or A4 (self-furrow) this wave.

## Lane B — espial (subagent 3, step B1)

In `espial/`:
- Copy from the math-quest clone: `tools/espalier/viz/*` → repo root
  (`protocol.ts`, `bus.ts`, `emit.ts`, `server.ts`, `dashboard.html`,
  `demo.ts`, README) and `test/espalier-viz-protocol.test.ts` →
  `test/protocol.test.ts` (update its import path + provenance header to
  cite this repo).
- `package.json`: name `@kodhama/espial`, private for now, zero runtime
  deps, devDeps vitest + typescript only, scripts: test / serve / demo;
  `tsconfig.json` (strict, allowImportingTsExtensions, noEmit — crib
  math-quest's compiler options minus app-specific bits); MIT LICENSE.
- Make tests + `tsc --noEmit` green; run `node demo.ts --fast` as smoke.
- Overlay: same rule as Lane A (trellis setup, else snapshot + loud note).
Push to main. Do NOT do B2 (LP) or B3 (adapters) this wave.

## Lane E1-followup — trellis PR (subagent 4, small)

In `trellis/`: branch `chore/family-tap`, PR (never direct to main):
- README + `docs/index.html` (+ its copy-button JS strings) + any
  install docs: `brew install kodhama/trellis/trellis` →
  `brew install kodhama/tap/trellis`;
- `.github/workflows/auto-release.yml`: dispatch URL
  `kodhama/homebrew-trellis` → `kodhama/homebrew-tap`.
Also (direct edit via gh, tiny): `kodhama/homebrew-tap` README —
generalize "tap for Trellis" to the family tap, install examples for
`kodhama/tap/trellis`.

## Lane R — repatriation (subagent 5, AFTER T1/A/B land)

The math-quest branch carries org-level artifacts that predate the org;
move each to its ONE home and slim the branch so the maintainer's
math-quest review is product-scoped:
- → `kodhama/kodhama`: `plans/plan-suite-lift.md` (as
  `conductor/suite-lift-plan.md`), `plans/lift-conductor-brief.md` +
  `plans/kodhama-meta-bootstrap.md` (conductor/ — wave-1 copies, already
  seated by bootstrap), `discovery/kodhama-delivery.md` (decisions/0001,
  already migrated by bootstrap).
- → `kodhama/design-system`: `tools/espalier/identity/` (marks, grammar,
  preview — T1 already consumes them; this makes it the home, not a copy).
- Then ONE slimming commit on the math-quest branch
  (`claude/agentic-runtime-viz-x1884q`): delete the moved files, leave
  `plans/suite-lift-pointer.md` (5 lines: what moved where, frontmatter
  `status: superseded`) and the same pointer paragraph atop
  `discovery/kodhama-delivery.md`'s replacement stub. Do NOT touch the
  espial prototype (`tools/espalier/viz/`, its test, the skill,
  tsconfig/gitignore) or `discovery/espalier-runtime-viz.md` — those are
  math-quest's until Lane C.
- The math-quest branch stays UNMERGED — the maintainer reviews the
  slimmed product diff and merges when satisfied; that merge is the
  approval of the espial-prototype adoption (artifact contract:
  approved = human merge).

## Standing grants (recorded here; effective when the maintainer
launches this wave — launching IS the grant)

The maintainer pre-authorizes, to make wave 1 zero-touch:
- **G1 — trellis PR self-merge:** the conductor merges the
  `chore/family-tap` PR ITSELF iff the diff is verifiably within the
  enumerated scope (only tap-path/dispatch-URL strings changed —
  checkable by grep against the lane's file list; any file outside the
  list → PARK instead, don't merge).
- **G2 — DS tag:** the conductor pushes `v0.1.0` without a blessing
  step; the T2 design pass is the real review of the DS and comes later.
- **G3 — repo skims are async:** the three bootstrapped repos need no
  sign-off to count as landed; the maintainer reviews at leisure, and
  anything he dislikes is a normal follow-up furrow.
Bounds unchanged everywhere: a lane that can't meet its acceptance
check PARKS loudly rather than stretching a grant; grants cover exactly
what's enumerated, nothing adjacent.

## Order & gates

T1, A, B, E1 all run in PARALLEL (no inter-lane deps this wave); R runs
after T1/A/B land. **With G1–G3 in force there are NO human gates
inside wave 1** — the only human acts are pasting the kickoff prompt
and answering parked questions if (and only if) a lane genuinely
blocks. The wave report is informational, not an approval request. The
ONE deliberately human merge left anywhere in the lift is the slimmed
math-quest branch — and that is not a wave-1 item; it waits for the
maintainer's product review before Lane C (identity-sensitive tester;
P > W). Wave 2 (A3/B2 LPs — need the DS tag; A4 self-furrow; C
consolidation) is dispatched separately after the wave report.

## Wave report (your final output)

Per lane: landed (commits/PRs with links), verification run (tests/greps
+ results), open items, loud notes (overlay snapshots owed, anything
skipped). Commit the report + ticked ledger into `kodhama/kodhama`
`conductor/wave-1.md`. Then: paste-ready summary for the cloud session
that owns the suite-lift plan (gundisalwa/math-quest branch
`claude/agentic-runtime-viz-x1884q`) so it syncs its ledger — include
the owed math-quest supersession pointer for the migrated delivery
decision.

## Acceptance criteria

- AC1: all four preconditions-verified lanes ran; none silently skipped.
- AC2: design-system tagged v0.1.0 with tokens/patterns/icons/lp-generator.
- AC3: espalier charters pass the zero-math-quest-nouns grep.
- AC4: espial tests + typecheck green in its own repo from a fresh clone.
- AC5: trellis PR open (not merged — that's the human's).
- AC6: wave report delivered with per-lane verification evidence.

## Open questions

None blocking — anything discovered mid-run parks at the lane, batches to
the terminal.
