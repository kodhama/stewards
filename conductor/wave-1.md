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

## Order & gates

T1, A, B, E1 all run in PARALLEL (no inter-lane deps this wave). Human
gates, batched at the END unless a lane blocks: merge the trellis PR;
bless the `v0.1.0` DS tag; skim the three bootstrapped repos. Wave 2
(A3/B2 LPs — need the DS tag; A4 self-furrow; C consolidation back into
math-quest) is dispatched separately after these gates.

- [x] merge the trellis PR — human merged #103 directly (2026-07-07T17:30:48Z,
  commit `0e3b6df`), ahead of the batched-gate schedule this brief assumed.
- [ ] bless the `v0.1.0` DS tag — open, pending human skim.
- [ ] skim the three bootstrapped repos — open, pending human skim.

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

- [x] AC1: all four preconditions-verified lanes ran; none silently skipped.
- [x] AC2: design-system tagged v0.1.0 with tokens/patterns/icons/lp-generator.
- [x] AC3: espalier charters pass the zero-math-quest-nouns grep.
- [x] AC4: espial tests + typecheck green in its own repo from a fresh clone.
- [x] AC5 (superseded in practice): brief specified "open, not merged — that's
  the human's"; the human merged #103 directly mid-wave. Intent (PR-gated,
  never direct-to-main) was honored — the lane opened it and stopped; the
  human's own action closed the gate ahead of the brief's batching plan.
- [x] AC6: wave report delivered with per-lane verification evidence (below).

## Open questions

None blocking — anything discovered mid-run parks at the lane, batches to
the terminal.

## Wave 1 report (2026-07-07)

All four lanes ran in parallel as Sonnet 5 subagents from this local
session (conductor itself ran on Fable 5 — a deviation from this brief's
"session model should be Sonnet 5," said here rather than silently). One
lane (B) was stopped mid-run by a stray human interrupt, confirmed
accidental, and relaunched clean (nothing had been committed, so nothing
was lost). Every lane's claimed landing was independently re-verified by
the conductor against the live GitHub state or a fresh clone — not taken
on the lane's word alone.

### Lane T1 — design-system

**Landed:** `kodhama/design-system` main, 6 commits, tag `v0.1.0` @ `6ade494`.
`tokens.css`, `patterns.md`, `icons/{trellis,espalier,espial}.svg` +
`icons/grammar.md`, `lp-generator.md`, `README.md`, `LICENSE`.

**Conductor verification:** fetched `tokens.css` at the `v0.1.0` tag and
diffed its custom-property pairs against `trellis-src/docs/index.html`
across all four blocks (`:root`, `prefers-color-scheme:dark`,
`[data-theme="light"]`, `[data-theme="dark"]`) — 43/43 pairs match
exactly (the only tool-reported non-matches were inline SVG animation
`--d:` delay attributes, not design tokens, correctly excluded). Tag and
full file listing (7 root files + 4 icon files) confirmed live via the
GitHub API.

**Open items:** icon set is explicitly provisional per its own source
README (marks await a dedicated design-review sitting — not attempted
here, correctly deferred); `lp-generator.md` is unexercised until a real
consumer (trellis, most likely) regenerates an LP against it.

### Lane A — espalier

**Landed:** `kodhama/espalier` main, 4 commits. `README.md`, `LICENSE`,
`decisions/`, `specs/`, `charters/` (10 charters + README), `.claude/agents/`
(9 subagent defs + README — `head-gardener` excluded by design, see
below), `.claude/skills/espalier-status/SKILL.md`, real `trellis setup
--apply` overlay (no snapshot fallback needed).

**Conductor verification:** fresh clone; reran the acceptance grep
`grep -riE "math.?quest|mariana|tier.?2|7\.º" charters/` — empty, exit 1
(no match), confirming AC3. Reran repo-wide — also empty. Confirmed 10
charter files, 9 agent files, and that `head-gardener` has a charter but
no dispatched-agent file.

**Judgment call flagged for human skim:** `head-gardener` was deliberately
not ported to `.claude/agents/` — ADR-0030 charters it as the interactive
driving session itself (v0), not a role a session dispatches. Verified
consistent with the charter text; a genuine interpretive call, not a gap,
but worth a second pair of eyes since it diverges from the "port the
subagent versions of the roles" instruction's literal reading.

### Lane B — espial

**Landed:** `kodhama/espial` main, 6 commits (one relaunch after an
accidental mid-run stop; original attempt had committed nothing, so the
relaunch started clean). Flat-root viz code (`protocol.ts`, `bus.ts`,
`emit.ts`, `server.ts`, `dashboard.html`, `demo.ts`), `test/protocol.test.ts`,
`package.json` (`@kodhama/espial`), `tsconfig.json`, `LICENSE`,
`.gitignore`, `README.md`, real trellis overlay.

**Conductor verification:** fresh clone, `npm install`, `npx vitest run`
→ 26/26 passed; `npx tsc --noEmit` → clean, exit 0; confirmed
`package.json` has zero runtime `dependencies` and exactly 3 devDeps
(`@types/node`, `typescript`, `vitest`) — satisfies AC4.

**Deviation flagged by the lane, confirmed reasonable by the conductor:**
added `@types/node` as a devDependency beyond the brief's literal
"vitest + typescript only." Without it `tsc --noEmit` fails with ~29
errors (Node builtins/globals unresolvable) — it is type-only, adds zero
runtime footprint, and the actual invariant (zero *runtime* deps) holds.
Also added `.espalier/` to `.gitignore` (bus.ts's own runtime-telemetry
output dir) — consistent with the source repo's convention, not
mentioned in the brief but not a meaningful deviation either.
**Open item:** stale in-comment usage-example paths in `emit.ts`/`server.ts`/
`demo.ts` (referencing the old `tools/espalier/viz/...` layout) were left
untouched per "don't rewrite the code, this is a lift" — flagged in the
new README for the B3 (adapters) wave to reconcile.

### Lane E1 — trellis PR + tap README

**Landed:** trellis PR [#103](https://github.com/kodhama/trellis/pull/103)
(`chore/family-tap`, commit `c6d85c0`) — README, `docs/index.html` (incl.
copy-button JS), `.github/workflows/auto-release.yml` repointed from
`kodhama/homebrew-trellis`/`kodhama/trellis/trellis` to
`kodhama/tap`/`kodhama/homebrew-tap`. `kodhama/homebrew-tap` README
rewritten direct-to-main (commit `4b0fc54`) to frame the tap as the
family's, not just trellis's.

**Conductor verification:** confirmed via `gh pr view` that #103 carries
exactly the three expected changed files and — as of this report — is
**merged** (`0e3b6df`, 2026-07-07T17:30:48Z), by direct human action
outside the lane (see Order & gates above). Confirmed the tap README on
`main` reads as reported.

**Open item, correctly left alone:** `decisions/0032-homebrew-distribution.md`
in trellis (ratified, append-only) still names the old per-product tap
path. Per this repo's own decision rules that file must not be edited in
place — it needs a **superseding decision** in trellis, referencing
`kodhama-0001-family-delivery`, not a patch. Flagged in the PR body;
not fixed by the lane, correctly.

### Cross-wave note: math-quest owes a supersession pointer

`discovery/kodhama-delivery.md` in `gundisalwa/math-quest`
(branch `claude/agentic-runtime-viz-x1884q`) is now migrated here as
`decisions/0001-family-delivery.md` (id `kodhama-0001-family-delivery`).
The math-quest original needs a one-paragraph stub pointing here — owed
on the math-quest branch, not from this repo. See the paste-ready summary
below.

### Wave-level verdict

AC1–AC6 met (AC5 met in substance, not literal form — see above). No
lane silently skipped a step; every deviation from the brief's literal
text was flagged by the lane and independently re-verified here, not
taken on trust. Two open human gates remain: bless the DS `v0.1.0` tag,
skim the three bootstrapped repos (espalier's `head-gardener` call is the
one item most worth a deliberate look). Wave 2 (A3/B2 LPs, A4
self-furrow, C consolidation) is unblocked and can be dispatched once
those gates close.
