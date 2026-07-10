---
id: kodhama-0006-lp-ownership-to-design-system
type: decision
status: gated
depends_on: [kodhama-0002-delivery-channels]
owner: agent
updated: 2026-07-09
provenance: maintainer, 2026-07-09, directing a reconciliation pass on family install-path claims after a landing-page design session kept assuming vendoring — "An LP generator should be a feature of the design system anyway, not the project, so should live outside of it."
---

# Decision: landing-page generation is a design-system feature, not a per-product one — grove and wisp retire their per-repo LPs; trellis keeps its as the DS's own origin

**Context.** `kodhama-0002` established `design-system`'s `lp-generator.md`
as a contract each *consuming* repo runs against itself, producing its own
`docs/index.html` from its own `docs/lp-content.md`. In practice this meant
three near-identical, independently-regenerated LP artifacts (trellis,
grove, wisp) — and a reconciliation pass this session found them already
drifting, from each other and from reality:

- grove's generated page undercounted its own agent roster: the hero
  heading read "Eight agent roles... plus two... **Ten** agents... druids"
  (omitting `corpus-reviewer`), while a paragraph six lines further down the
  *same page* correctly said "default: all eleven." The stale count also
  matched grove's own `plugins/grove/.claude-plugin/plugin.json` and this
  repo's `marketplace.json` — both said "ten," both now fixed to "eleven"
  in this pass.
- every Claude Code install command on every trellis surface — README,
  plugin README, LP source, and the live GitHub-Pages-hosted generated
  page — named trellis's own pre-org-marketplace alias
  (`kodhama/trellis` → `trellis@trellis`) rather than the org marketplace
  `kodhama-0002` itself designates canonical (`kodhama/kodhama` →
  `trellis@kodhama`). All fixed in this pass.

The maintainer's call: generation should be a **feature design-system
provides**, not a contract each consuming repo separately discharges —
one fewer duplicated surface to drift.

## Decision

1. **grove and wisp retire their per-repo LP artifacts.** `docs/index.html`
   and `docs/lp-content.md` removed from both repos (this session). Neither
   repo had GitHub Pages actually configured to serve `/docs` (verified via
   `gh api repos/kodhama/{grove,wisp}/pages` → both `404`), so this has no
   live-site impact — the files existed in-repo but were never hosted.
2. **trellis keeps its LP as the exception, not as a precedent.** Its
   `docs/index.html` is design-system's own origin — `tokens.css` and
   `patterns.md` were extracted verbatim from this exact page (per
   `docs/lp-content.md`'s own header) — and it's the one repo where GitHub
   Pages is actually live (`kodhama.github.io/trellis/`, verified serving
   from `main:/docs`). Removing it would delete the DS's own source
   material, not just a derivative.
3. **Where the generator feature itself lives is not decided here.** This
   record retires the per-repo duplicates and states the direction only;
   designing what a design-system-owned generator looks like (a command, a
   hosted service, a script consuming repos call) is separate work, not
   done as part of this pass.

**Amends `kodhama-0002` §5 / AC4** (forward pointer, not an edit to that
decision's text): the per-product "canonical LP install blocks" for grove
and wisp no longer apply — those products currently have no LP at all,
pending the design-system-owned generator this decision points at.
trellis's block is unaffected.

4. **Neither repo tracks a future LP as its own work, and neither
   mentions one going forward** (a superseded decision's own historical
   text is exempt — this is about live docs, not the record). grove's and
   wisp's READMEs no longer reference a forthcoming "generated landing
   page" as wave-2 work (grove's ADR-0030-lift Status section retired step
   A3; wisp's Provenance section dropped "landing page" from its wave-2
   follow-up line). `wisp/dashboard.html`'s header comment, which claimed
   a mechanism "this repo's own `docs/index.html` already uses," was
   corrected — that file no longer exists. Generation, when it happens, is
   **triggered externally** (a design-system-owned run against the
   consuming repo), not dispatched from inside grove's or wisp's own
   conductor/plan work.

## Acceptance criteria

- **AC1** grove and wisp have no `docs/index.html` / `docs/lp-content.md`
  in their repos.
- **AC2** trellis's `docs/index.html`, its plugin README, its top-level
  README, and `docs/lp-content.md` all name the org marketplace
  (`kodhama/kodhama` → `trellis@kodhama`), not the repo-local alias.
- **AC3** No live GitHub Pages site broke as a result (verified: grove/wisp
  had none configured; trellis's is unaffected, only its content corrected).

## Open questions (parked, ≤3)

- What does "a feature of the design system" concretely look like — a
  script in `design-system/`, a Claude Code command, something else? Not
  designed here — the maintainer's own stated plan is to trigger it from a
  separate Claude design run, not from a mechanism built in this pass.
- Does trellis's in-repo marketplace alias (`kodhama/trellis`) deprecate
  now that its README/LP point at the org marketplace, or stay as a
  documented-but-unadvertised fallback? Same open question `kodhama-0002`
  already parked, still unresolved.

## Self-check (gate)

Maintainer's own words quoted as provenance; the live-Pages claim verified
via `gh api` before being stated as fact, not assumed; grove's undercounted
roster verified by reading the actual generated HTML (lines 426/428 vs
542), not inferred from `lp-content.md` alone; trellis's exception is
justified by two independent, checked facts (DS provenance + live Pages),
not asserted alone. Promote `draft → gated`. `approved` = human merge, per
this repo's own lifecycle mapping (`.trellis/profile.md`).
