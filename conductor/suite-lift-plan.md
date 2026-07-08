---
id: plan-suite-lift
type: plan
status: gated
depends_on: [adr-0030-espalier, discovery-espalier-runtime-viz]
rubric: rubrics/spec-quality.md
owner: agent
updated: 2026-07-07
---

# Plan: the suite lift — trellis / espalier / runtime-viz as one family

`Serves: W — new pattern: conductor-run multi-repo lift executed by the
swarm being lifted.`

**Objective.** Lift Espalier out of math-quest into its own repo; lift the
runtime viz into its own repo (standalone, preferred); consolidate the three
packages — **trellis** (governance), **espalier** (swarm), **runtime viz**
(observability) — as a coherent unit sharing primitives and one design
language; re-point math-quest to consume Espalier as its operating model.
This plan is written to be **startable at any time** and run by a
**conductor** (see §Conductor) with terminal interactivity assumed.

## End state (the target topology)

```
kodhama/design-system — THE family brand asset (own repo, 2026-07-07):
                  tokens + component patterns + icon grammar + the LP
                  generator instruction; versioned by git tags
kodhama/kodhama — org meta: cross-family decisions + family front door
                  (itself a generated derivative of the DS)
     ▲  (soft/agentic dependency: each repo's LP furrow reads the DS by
     │   link at a TAG and stamps that tag into the generated page — no
     │   build coupling; staleness = stamped tag ≠ latest DS release,
     │   a surfaced check, never a broken build)
trellis    — governance layer, invariants, overlay/CLI/plugin
   ▲    ▲
   │    │ (overlay: espalier repo runs trellis)
   │  espalier — the gardener swarm: role charters, workflows W1–W6,
   │            dispatch contract; managed BY espalier itself (self-hosted
   │            operating model); LP in the family design
   │      ▲
   │      │ (operating model: viz repo's furrows run under espalier)
   └── espial — protocol + reducers + dashboard;
       standalone repo; espalier is its reference consumer
          ▲
          │ (dependency: tool vendored/installed; overlay: espalier)
       math-quest — consumer: runs espalier furrows, emits onto the viz
                    bus; keeps only project-specific config
```

Dependency direction is strictly downward (espial → espalier → trellis;
all → the DS in kodhama/design-system via soft/agentic links only). Nothing in
trellis knows about espalier; nothing in espalier requires espial (it
emits if present — telemetry is optional by construction, D3 of the
discovery).

### The kodhama stack (uniform self-application)

**Every family repo runs the full family stack on itself** — trellis
overlay (governance), espalier (operating model), espial (telemetry on
its own furrows) — and each product's own development runs are dogfood
evidence for that product. Bootstrap order: trellis already self-hosts;
espalier gains the overlay at A1 and proves itself at A4; espial runs
under espalier + trellis from B1 and watches its own furrows with its
own vendored build from day one. Changes born in one repo's dogfooding
propagate as W4-style surfaced findings to the product they belong to,
never as silent local forks. (math-quest consumes the same stack as the
first external consumer — outside family scope.)

## Shared primitives (the "coherent unit" register)

| Primitive | Home (ONE home each) | Consumers |
|---|---|---|
| Invariants + overlay mechanism | trellis | espalier, viz, math-quest |
| Design tokens + component patterns + icon grammar | **kodhama/design-system** (own repo, git-tag versioned — the Primer/Polaris/Carbon shape; amended 2026-07-07, was trellis, then kodhama/kodhama) | ALL LPs incl. trellis's own AND the family front door, espial dashboard, future tools |
| LP generator (instruction + content schema + DS-tag stamp) | kodhama/design-system `lp-generator.md` | every product LP + the family page — pages are DERIVED artifacts: LP = generate(DS@tag, repo's lp-content) |
| Artifact contract (frontmatter, gated/approved, rubrics) | trellis profile → project expressions | all |
| Role charters + workflows W1–W6 + dispatch contract | espalier | viz repo furrows, math-quest furrows |
| Runtime event protocol v1 + reducers (`protocol.ts`) | viz repo | espalier skill, any team |
| Status-emission skill (generic half) | viz repo; espalier keeps the gardener-flavored wrapper | agents everywhere |

Evidence the design language transfers: the math-quest dashboard now wears
the Trellis tokens directly (commit on this branch — lattice motif, mono
eyebrows, accent green as `working`, terminal-styled event feed). That
restyle is the *mock* for the family look; the reusable extraction happens
in T1 below.

## Naming the runtime viz (decision gate — maintainer)

Constraint set: horticultural family (trellis = the structure, espalier =
the practice), names the *function* (watching the garden), namespace-clean,
short enough for a CLI. Candidates:

| Name | Why | Risk |
|---|---|---|
| **Espial** (recommended) | "the act of catching sight of something" — a real English word that is nearly an anagram-echo of *espalier*; the pun is the pitch: *Espial — watching the espalier.* CLI `espial`. | Espial Group (TV middleware co.) exists — different field, but run the ADR-0030-style adversarial naming check before committing. |
| Mirador | PT/ES for a garden viewpoint — fits the family's Iberian thread (miradouro) and the function exactly. | Mirador is a well-known IIIF image *viewer* — same "viewer" semantic field; likely disqualifying. |
| Belvedere | The garden structure built to command a view; elegant. | Long; weaker CLI ergonomics; scattered small collisions. |
| Pergola | Family-adjacent garden structure. | Names a *support* structure, not viewing — semantically wrong function. |

**DECIDED (2026-07-07, maintainer): Espial.** The adversarial run surfaced
real collisions (three GitHub tools incl. jonschoning/espial, the npm
name, Espial Group) and a forest-spirit shortlist was considered
(Curupira/Medeina/Leshy/Dryad/Tapio; Kodama rejected as confusably close
to the org). The maintainer holds the line on the espalier echo: the tool
is a *companion* to espalier, discovered through it, not a standalone
brand fighting for the global name — and `kodhama/espial` + a
tap-namespaced formula sidestep most of the collision surface. Residual
risk accepted and recorded: the bare `espial` binary/npm name clashes;
mitigation if it ever bites is renaming the *binary* (cheap), not the
project. Repo: `kodhama/espial`.

## Operation model (recommendation + open research)

Three tiers; adopt the first two, research the third:

1. **Local (adopt now).** Interactive/session-hosted furrows run the server
   locally off the file bus — today's model, zero infrastructure, commands
   land on the same machine the agents poll. This remains the default
   whenever a human is at the terminal.
2. **Cloud read view (adopt at lift).** For runner-hosted furrows and
   phone monitoring: adapters push events out — first the **GitHub adapter**
   (events batched into issue/PR comments, which runner checkpointing
   already half-does), then optionally an HTTPS gateway to a small hosted
   read-only dashboard. Telemetry is already claims-only and gitignored, so
   a read view leaks no authority.
3. **Cloud commands (research before adopting).** Commands are the human's
   authority channel; hosting it requires auth, transport, and storage
   decisions none of which should be improvised. Parked as research lane D
   with an explicit trigger: *first runner-hosted furrow where the
   maintainer wanted to answer a parked question from the phone and
   couldn't.*

**For math-quest specifically (item 5): both.** Local dashboard during
interactive furrows; the GitHub adapter mirrors events outward so any
future hosted view picks them up. Local-first, hook-to-cloud — never
cloud-required.

## Phases and lanes

Phase -1 (org migration) can start immediately; Phase 0 is a gate; lanes
A/B/D then run in parallel; C closes.

**Phase -1 — kodhama migration (org exists as of 2026-07-07; startable
now, independent of Phase 0).**
*Ledger 2026-07-07:* transfers **done** (maintainer, `gh api`; both repos
verified live under `kodhama/*`). Update sweeps **prepared and committed**
on `chore/kodhama-org-migration` branches in the session clones — 26
substitutions in trellis (go build + JSON verified, grep-zero outside
`decisions/`+LICENSE), 10 in homebrew-trellis — and exported as patches
for local landing: this session's git proxy reads moved repos through
GitHub's redirect but refuses the write path (deterministic 503), and v1
sessions can't add cross-owner sources, so pushing + PR-opening lands via
the maintainer's local agent (patches handed off) or a fresh
kodhama-scoped session.
*Ledger update, same day:* both migration PRs **merged** (landed by the
local agent from the handed-off patches); verified remotely —
`install.sh` on main reads `REPO="kodhama/trellis"`, the formula's
homepage + release URLs are kodhama, zero stale refs in either fetched
file. *(b) `TAP_DISPATCH_TOKEN` re-issued under kodhama and set on
`kodhama/trellis` — done (maintainer, same day; secret existence not
remotely verifiable from this session, will be proven by the next
release's tap dispatch).* *(a) Pages re-enabled and serving at
`kodhama.github.io/trellis` — verified in the maintainer's browser; note:
the remote session's egress proxy blocks `*.github.io` (CONNECT 403), so
its earlier "Pages still 403" readings were the proxy, not GitHub. (c)
brew + curl install smoke test — done (maintainer's machine).*

*Board ledger (2026-07-07, later):* all six org repos verified live —
`trellis`, `homebrew-tap` (E1 rename DONE by maintainer), `espalier`,
`espial`, `design-system`, `kodhama` (all public, created by maintainer).
E1 follow-ups now agent-work in kodhama-scoped sessions: trellis PR
updating brew install text `kodhama/trellis/trellis → kodhama/tap/
trellis` + auto-release dispatch target `homebrew-trellis →
homebrew-tap`; tap README generalized from "tap for Trellis" to the
family tap; repo descriptions backfill. Lanes T1/A1/B1 physically
unblocked.

**Phase -1 / AC0: COMPLETE (2026-07-07).** Both repos re-homed, sweeps
merged, token re-issued, LP serving, installs verified. All later lanes
create under `kodhama/*` with zero migration debt. Next gate: Phase 0
decisions batch. Move the existing repos to the family's
home so every later lane creates under `kodhama/*` from birth with zero
migration debt. Reference surface enumerated 2026-07-07 against the live
trellis clone (`grep -rn gundisalwa`):

0. **Transfer runbook (local `gh` CLI, ~2 min):**
   ```sh
   gh auth status                                   # logged in, repo scope
   gh api orgs/kodhama/memberships/gundisalwa       # expect role: admin
   gh api -X POST repos/gundisalwa/trellis/transfer -f new_owner=kodhama
   gh api -X POST repos/gundisalwa/homebrew-trellis/transfer -f new_owner=kodhama
   gh repo view kodhama/trellis --json nameWithOwner          # verify
   gh repo view kodhama/homebrew-trellis --json nameWithOwner
   gh api repos/kodhama/trellis/pages --jq .html_url          # new LP URL
   ```
   Then, one-time so phone/remote sessions can drive the follow-up PRs:
   install the Claude GitHub app on the kodhama org. Post-transfer token
   note: `TAP_DISPATCH_TOKEN` is a **fine-grained PAT** (auto-release.yml
   comment) — fine-grained PATs are scoped to their resource owner, so the
   existing one dies with the move; re-issue with kodhama as resource
   owner (and check the org policy allows fine-grained PATs). Harmless
   meanwhile: the workflow explicitly no-ops when the secret is empty.
   Update local clones: `git remote set-url origin
   https://github.com/kodhama/<repo>`.
1. **Transfers (maintainer acts):** `gundisalwa/trellis → kodhama/trellis`
   and `gundisalwa/homebrew-trellis → kodhama/homebrew-trellis`. Git and
   web URLs redirect automatically after transfer, **but GitHub Pages does
   not**: `gundisalwa.github.io/trellis` dies and the LP re-homes at
   `kodhama.github.io/trellis` — the one hard break, and README line 62
   links it. Guardrail: never recreate a `gundisalwa/trellis` repo — a
   name reuse kills the redirects for every stale link in the wild.
2. **Trellis update PR (one PR, post-transfer):**
   - `install.sh`: header comment + `REPO="gundisalwa/trellis"` (drives
     release-asset downloads);
   - `docs/index.html` (~9 refs: nav, three install tabs, CTAs, footer,
     copy-button JS strings) + `docs/invariants.html`;
   - `README.md`: brew tap path, curl URL, marketplace add, the Pages link;
   - `.claude-plugin/marketplace.json` `owner.name` +
     `plugins/trellis/` plugin.json author and README refs (check how
     existing plugin installs re-resolve the marketplace name);
   - `.github/workflows/auto-release.yml`: the `repository_dispatch` to
     `gundisalwa/homebrew-trellis` → kodhama, and VERIFY the PAT/secret it
     uses is authorized for the org (org-owned repos can need re-granted
     tokens — audit secrets/webhooks/deploy keys post-transfer rather than
     assuming they carried);
   - `cli/go.mod` module path `github.com/gundisalwa/trellis/cli` +
     internal imports (binary/brew distribution makes this safe; still one
     deliberate commit);
   - `LICENSE` holder name — maintainer call;
   - `decisions/*` mentions stay untouched — ADRs are history (supersede,
     never edit).
3. **homebrew-trellis update PR:** formula `url`/`homepage` → kodhama; tap
   becomes `brew install kodhama/trellis/trellis`; README note for
   existing users (`brew untap gundisalwa/trellis && brew tap
   kodhama/trellis` — old tap keeps working on redirects, re-tap is the
   clean state).
4. **Verification (the phase's gate, all from clean machines/sessions):**
   curl install from the new raw URL; `brew install kodhama/trellis/trellis`;
   `/plugin marketplace add kodhama/trellis`; one auto-release
   dispatch round-trip; Pages live at the new URL; math-quest overlay
   refresh picks up the new source in `.trellis/version` on its next
   by-hand refresh (ADR-0029 — no URL refs exist in math-quest today,
   verified by grep).

**Phase 0 — decisions batch (interactive, ~30 min of maintainer time).**
Conductor asks, in ONE terminal batch: (a) viz name (post-adversarial-run
shortlist); (b) repo names/visibility; (c) license (trellis's as default);
(d) distribution: vendored copy vs npm publish (default: vendored copy at
first — publishing is reversible-later and adds release process now);
(e) confirm lane order below. *(A former (f) — confirm the kodhama org —
resolved 2026-07-07: the org exists; the family's home is `kodhama/*`, a
play on the kodama tree spirits of Mononoke Hime. Migration of the
existing repos is Phase -1.)* Blocks lanes T/A/B/C; Phase -1 does not
wait for it.

*Phase 0 ledger (2026-07-07, first sitting):* **(b) visibility: PUBLIC**
for both new repos (matches trellis; Pages needs it; W is meant to be
shown). **(c) license: MIT**, same as trellis — one license across the
family. **(d) distribution: vendored copy per module (the trellis
pattern), decided** — with the maintainer-raised alternative registered
as an explicit later option: a single family CLI (`kodhama <module>
...`) wrapping all three. Analysis: a suite CLI must live ABOVE the
three modules (a fourth, thin artifact — trellis must never know about
espalier/viz, so absorbing them into the trellis CLI is out); the
language split (Go CLI vs zero-dep TS viz) means it would only ever
shell out or demand a Go rewrite of the viz; and module maturities
diverge too much today (shipped / v0 / prototype) to couple release
cadences. **Superseded same day by the researched delivery decision**
(`discovery/kodhama-delivery.md` — sourced against the Charm/goreleaser
org-tap pattern and the monorepo/polyrepo literature): **no builder
repo, no monorepo — each product delivers itself; the org owns two thin
shared surfaces.** Lane E becomes:
- **E1 (can run now):** rename `homebrew-trellis → kodhama/homebrew-tap`
  (one tap, N formulas — the Charm pattern); update trellis's dispatch
  + install text to `brew install kodhama/tap/trellis`. Doing it at
  user-count ≈ 0 is the whole point.
- **E2 (restored 2026-07-07 after the DS got its own repo):** create
  `kodhama/kodhama` — org decisions (the kodhama discovery artifacts
  move in with supersession pointers) + the family front door, itself
  generated from the DS like any product LP. Never a builder; each
  product's installer lives on its OWN generated LP. Trigger: the first
  decision migration or the family page, whichever comes first.
- **E3 (at espial's first release):** npm scope `@kodhama/espial` (the
  scope also kills the espial npm collision); tap formula only if a real
  CLI emerges. Espalier's channel is the Claude plugin marketplace +
  overlay — never a binary. Release machinery stays per-repo
  (goreleaser-style, as trellis today).
Also settled: **espial stays standalone** (the fold-into-espalier
option was considered and rejected by the maintainer's own argument —
adapting to other agentic teams is part of the point, and the
team-agnostic protocol is the door; espalier remains the reference
consumer). **(a)
name: still open** — Espial disqualified in the adversarial run (three
GitHub tools incl. jonschoning/espial bookmarking server + Espial
Group; npm/CLI taken), Kodama rejected by the maintainer as confusably
close to the org name; a forest-spirit shortlist is with the maintainer
(Curupira / Medeina / Leshy / Dryad / Tapio). Blocks only B1's repo
creation. **(e) lane order: confirmed as written** (no objection
raised).

**Lane T — the design plane (revised 2026-07-07: DS is an org asset).**
- T0: create `kodhama/design-system` (amended 2026-07-07: the DS is its
  own repo — self-describing dependency link, git-tag versioning for
  free, and it runs the kodhama stack on itself like any family member;
  E2's `kodhama/kodhama` returns to Lane E timing). First tag `v0.1.0`
  after T1.
- T1: extract the DS from the trellis LP into `kodhama/design-system`:
  `tokens.css`, component patterns (eyebrow, card, terminal, lattice,
  toggle, climbing-plant flourish), the icon grammar + marks (from
  math-quest `tools/espalier/identity/`), and `design/lp-generator.md` —
  the agent instruction every LP furrow loads by link: consume the DS,
  generate the page from the repo's own `docs/lp-content.md`, stamp the
  generated file with the DS version, vendor the output (pages stay
  self-contained; the dependency is generation-time, agentic, soft).
- T2: design-system pass (Claude design) — the DS repo's first major
  furrow; reviews icon family + tokens + component patterns as one
  system against real usage (post A3/B2); output is a new DS tag.
- T3: **tokenize the trellis LP** — the retrofit that proves the
  generator: extract trellis's LP copy into `docs/lp-content.md`,
  regenerate `docs/index.html` via the T3 generator, byte-diff against
  the hand-built page for visual parity, stamp the DS version. From then
  on the trellis LP is a derivative like the others (decision-0028's
  derived-pairs rule, applied cross-repo: the DS names its derivative
  LPs; each repo carries a staleness check comparing its LP's DS-version
  stamp against the live DS — stale = surfaced finding + a regeneration
  furrow, never a silent drift and never a build break).

**Lane A — espalier lift.**
- A1: create `kodhama/espalier` (after Phase -1); skeleton per its own artifact contract;
  `trellis setup` (the overlay is the first commit after init — the repo
  *uses trellis from birth*); CI (tests + pr-contract, ported).
- A2: generalize role charters through the signature-pair door (ADR-0030
  §Lift path): strip math-quest nouns; workflows W1–W6, dispatch contract,
  checkpoint/resume, remediation roles move over.
- A3: LP generated per the T1 generator pattern: espalier writes its
  `docs/lp-content.md` (copy + its trained-tree motif), the LP furrow
  reads the DS by link and emits the DS-version-stamped page.
- A4: **first self-furrow** — espalier's first tracked work item is run *as
  an espalier furrow inside its own repo* (e.g. "write espalier's
  CONTRIBUTING from the charters"). Passing gate: the full W1 loop runs
  outside math-quest. This is the lift's conformance test.
- A5: math-quest ADR: ADR-0030 gets "superseded in part" pointer (charters'
  home moved; the math-quest *adoption* of espalier stays local).

**Lane B — viz lift (standalone, preferred).**
- B1: create `kodhama/espial`; move `tools/espalier/viz/` + tests (they run
  under plain vitest with no math-quest imports today — verified); add
  `package.json` (bin: serve/emit), keep zero runtime deps; `trellis
  setup` via the espalier overlay once A1 exists (until then, trellis
  directly — swap is one command).
- B2: LP generated per the T1 generator pattern (espial's
  `docs/lp-content.md`; the hero is the live graph replaying the demo
  furrow — the demo becomes the LP's animation, same file, real tool).
- B3: adapters: GitHub comments emitter (runner-hosted telemetry out),
  `check`-equivalent reader; protocol/docs mark the genericity budget —
  **espalier is the reference consumer; generalize only what falls out
  naturally, never speculatively** (the discovery's D4 stance, kept).
- B4: espalier-managed from then on: viz work items run as espalier furrows
  (espalier is installed in the viz repo as operating model).

**Lane C — math-quest consolidation (after A4 + B1).**
- C1: delete `tools/espalier/viz/` in favor of the vendored/installed viz;
  the `espalier-status` skill stays (it's the math-quest-flavored wrapper)
  pointing at the installed tool; `.espalier/` bus path unchanged.
- C2: CLAUDE.md §Current stage + operating sections point at the espalier
  repo as the swarm's home; math-quest keeps only project expressions
  (dials, run-ids, curriculum nouns).
- C3: supersession pointers: ADR-0030 (per A5), discovery-espalier-
  runtime-viz gains "implemented; moved to <viz repo>" forward link; tests
  that anchored the prototype move with the code (provenance headers
  updated).
- C4: closing ADR in math-quest recording the consolidation (this plan is
  the draft of its rationale).

**Lane D — cloud-ops research (parallel, non-blocking).** Research
artifact in the viz repo per the research discipline (preflight, tagged
claims): hosting options for the read view, auth models for a command
channel, cost floor. Gate: rubric self-check; informs tier-3 adoption only.
*Ledger 2026-07-08: Lane D closed unstarted — moved to the grove backlog
as [kodhama/grove#8](https://github.com/kodhama/grove/issues/8) at the
maintainer's instruction; the family's backlog/roadmap model itself is
now [kodhama/kodhama#10](https://github.com/kodhama/kodhama/issues/10).*

## Conductor (item 8 — "everything automatic")

The conductor is the **head-gardener session of whichever repo the phase
belongs to** (Phase 0/A/C: math-quest session until A4, then espalier's own;
B after B1: the viz repo's). Its contract, extending ADR-0030 §Dispatch:

- **Scheduling:** holds the lane DAG above; launches every lane whose
  dependencies are met as parallel subagent furrows; sequences within lanes.
- **Interactivity:** questions park at the asking furrow (park-file-and-
  exit); the conductor batches them to the terminal at natural seams, ≤3 at
  a time (the shaping-partner rule); it is allowed to WAIT — idle-blocked
  on the human is a valid conductor state, never a failure.
- **Ledger:** this plan file is the ledger — the conductor checks lanes off
  by commit as they gate (plan updates ride the work's own PRs, SI-2).
- **Telemetry (dogfood):** every lane emits onto the viz bus; the lift is
  monitored by the tool being lifted. The parallel lanes are exactly the
  parallel-nodes case the graph view was built for.
- **Bounds (inherited):** repair cascades ≤ gen-2; auto-resume ≤ 2; every
  gate distinguishes verified-clean from never-ran (vacuity); LOUD stop to
  the maintainer at any bound.

### Wave 1 — LANDED (2026-07-07, local conductor seated at kodhama/kodhama)

Lanes T1 (design-system, 6 commits), A1–A2 (espalier skeleton +
charters, 4 commits), B1 (espial, 6 commits), E1-followup (trellis
`chore/family-tap` PR #103) all ran in parallel and landed. Verification,
independently re-checked by the conductor before reporting: espial
26/26 tests + typecheck clean from a fresh clone; espalier charters
grep-clean of math-quest nouns; DS tagged `v0.1.0`; PR #103 merged.
Two notes worth keeping: (a) a stray human interrupt hit Lane B mid-run —
caught, confirmed accidental, relaunched clean, nothing lost (the
re-verification step is exactly what caught it); (b) `head-gardener`
was deliberately excluded from the dispatched agent set — charter-only,
per ADR-0030's "the interactive session, not an agent" framing — a
correct call, flagged loudly by the conductor rather than assumed.

**Two items did NOT run**, because the maintainer launched the wave
from a brief snapshot taken before the standing-grants (G1–G3) and Lane
R (repatriation) sections were added here — a timing gap, not a miss:
- **Human gates were NOT self-cleared.** The `v0.1.0` tag and the three
  bootstrapped repos are sitting at "awaiting blessing" / "pending
  skim" in the executed brief. Nothing blocks on this — G2/G3 make both
  no-ops going forward; the maintainer can bless/skim at leisure, or
  just proceed to wave 2 (recommended: DS v0.1.0 is good — grep/build
  verified — and there is no reason to gate on a re-read the design
  pass (T2) will redo properly anyway).
- **Lane R (repatriation) has not run.** `plans/plan-suite-lift.md`,
  `plans/lift-conductor-brief.md`, `plans/kodhama-meta-bootstrap.md`,
  and `tools/espalier/identity/` are still only in math-quest. The
  `discovery/kodhama-delivery.md` half of repatriation DID land, via
  the bootstrap step (not Lane R) — it's now `kodhama-0001-family-delivery`
  and this branch's copy carries the supersession stub. **Lane R is
  now Wave 1.5**: dispatch it standalone (no rebuild needed, T1/A/B are
  already done) the next time a kodhama-scoped local session runs;
  it slims this math-quest branch to the product-scoped review diff.
- **New finding from this wave, action needed:** `kodhama/trellis`'s
  `decisions/0032-homebrew-distribution.md` names the pre-family
  per-product tap model and is now stale — per the org's own
  append-only rule (ADRs are superseded, never edited) it needs a new
  decision in `kodhama/trellis/decisions/` superseding 0032 with a
  forward pointer to the family-tap model (`kodhama-0001` +
  `chore/family-tap`/PR #103). Folds naturally into Wave 1.5 alongside
  Lane R, same local session, same org credentials.

## Model economy (added 2026-07-07 — maintainer constraint)

Fable access and overall model budget are scarce; the plan spends them
deliberately. This generalizes the routing math-quest already runs in
`claude.yml` (strongest model for research/shaping, default model for
execution):

| Work | Model | Why |
|---|---|---|
| Phase 0 facilitation, adversarial naming run, shaping/ADR drafting | Fable | few tokens, high judgment-per-token; one sitting |
| T2 design-system pass (Claude design) | Fable | taste + cross-artifact coherence is the whole job |
| Spec authoring + spec-adversary rounds | Fable preferred, Sonnet 5 acceptable | the intent-adjacent layer is where errors are expensive |
| ALL execution lanes (A1–A5, B1–B4, C1–C4 builds, sweeps, LPs from existing tokens) | Sonnet 5 | mechanical against enumerated checklists + gates catch slips |
| Conformance review / validator | Sonnet 5 | independence comes from the role, not the tier; a different model than the builder adds diversity for free |
| Bulk mechanical fan-out (reference sweeps, file moves) | Haiku 4.5 optional | cheapest tier where a grep verifies the result |

Rules: (a) **start every lane on Sonnet 5; escalate a single stuck item
to Fable rather than running a lane on it** — escalation is an event,
not a mode; (b) **batch the Fable moments** (Phase 0 + naming + any
shaping) into one sitting so the scarce window is spent once; (c) Fable
never touches enumerated-checklist work; (d) each furrow records its
model in the run's telemetry `meta` so the ledger shows what the lift
actually cost per tier. If Fable access lapses entirely, the plan
degrades gracefully: Sonnet 5 everywhere, T2 deferred until access
returns — no lane hard-requires Fable.

## Acceptance criteria

- **AC0 (Phase -1)** Both repos live under `kodhama/*`; zero `gundisalwa/`
  references remain in trellis + homebrew-trellis outside `decisions/`
  (greppable); all four verification installs/round-trips pass; the Pages
  LP serves from its new URL.
- **AC1 (Phase 0)** All remaining decisions recorded (plan updated in
  place with the answers + date) before lanes T/A/B/C start.
- **AC2 (Lane A)** `kodhama/espalier` exists with trellis overlay active
  (`trellis status` clean), generalized charters (zero math-quest nouns —
  greppable), an LP on the shared tokens, and one completed self-furrow
  whose artifacts live in that repo.
- **AC3 (Lane B)** Viz repo: tests green standalone, `node` serve/emit/demo
  work from a fresh clone, LP live, GitHub adapter emits and reads back a
  round-trip event batch.
- **AC4 (Lane C)** math-quest contains no copy of the viz code; a furrow
  run in math-quest appears on the dashboard served from the installed
  tool; CLAUDE.md points at espalier's repo; supersession pointers resolve.
- **AC5 (conductor)** At least two lanes ran concurrently with their
  questions batched through one terminal gate; the plan file's lane
  checkboxes match repo reality at close.
- **AC6 (design)** All three LPs + the dashboard consume one token source
  (post-T1) — checkable by grepping for the tokens' provenance header.

## Assumptions

- Repo creation, license, and naming are maintainer acts (intent layer) —
  embedded as Phase-0/T1 gates, not assumed done.
- Distribution default is vendored-copy, revisable at Phase 0(d).
- The trellis-side token extraction (T1) is a PR to another repo and
  follows *that* repo's rules; this plan only sequences it.
- Timeline deliberately unstated: the Tavira validation window owns the
  calendar (P > W, ADR-0023); this plan starts when the maintainer says so.

## Open questions

- Viz name — Phase 0(a), adversarial run pending.
- Cloud command channel (tier 3) — Lane D research, with its named trigger.
- npm publish vs vendored copy long-term — revisit when a consumer outside
  the family appears.
- Does math-quest's `.claude/agents/*` fully retire in C2, or keep thin
  local shims? (Decide in C2 with the diff in hand.)

## Rubric check

Rubric: `rubrics/spec-quality.md` (plan subset).

| Item | Result | Evidence |
|---|---|---|
| Declarative, testable statements | PASS | Lane steps + AC1–AC6 are checkable; end-state topology explicit. |
| Dependencies live | PASS | ADR-0030 (gated), discovery-espalier-runtime-viz (gated). |
| Alternatives recorded | PASS | Naming table w/ risks; standalone-vs-inside-espalier (standalone chosen, genericity budget bounded); vendored-vs-npm defaulted with reversal condition. |
| Open questions present | PASS | Four, each with its decision point. |
| Human gates explicit | PASS | Phase 0 batch, T1 merge, name decision, tier-3 adoption — all maintainer-owned. |

**Verdict: promote `draft → gated`.** Execution start is a maintainer call
(Phase 0 is the first act and it is his).
