# Wave: install grove on all projects

Opened 2026-07-08. Authorization: maintainer — "now install grove on all
projects" (follow-up queued in the marketplace wave; maintainer had
pre-authorized "either do it or ask for my help" — the conductor did it,
pinning per-repo placeholder values from established context and
delegating execution to Sonnet lanes; every value is listed in each PR
for the maintainer to veto at review).

**Scope decided (said out loud):** kodhama, trellis, design-system get
installs. **wisp** — already grove-managed (lane B4). **grove itself —
deliberately skipped**: its `.claude/agents/` ARE the shipped generic
artifact (zero-nouns, placeholder-bearing); filling them in place would
clobber the product. Grove self-hosts by running its own charters
directly (the A4 self-furrow precedent). **math-quest — skipped**: it is
the origin project and already carries filled copies, kept deliberately
by Lane C's recorded judgment call.

Method: the shipped `/grove:setup` flow executed by hand (the plugin PR
was in flight during this wave), sourcing the role files from an
immutable `git archive` snapshot of grove main (`4cdfec5`) — workspace
isolation from the live plugin lane, per the incident rule in the
marketplace wave's report. Managed CLAUDE.md blocks stamp
`grove plugin@4cdfec5`, which equals the plugin-root SHA the skill
itself would stamp. Telemetry skill installed nowhere (wisp not vendored
in any of the three; optional by construction).

## Ledger

- [x] kodhama: ten roles + README composed, placeholders resolved
      (markdown-only: no test/typecheck gates; parked items = conductor
      briefs' Parked sections; specs/ deliberately NOT seeded — the
      three-things mandate keeps decisions/ + conductor/ as the only
      stores) — rides this wave's PR
- [x] trellis: lane stopped correctly at the native
      conformance-reviewer collision; resumed after both redirects
      ratified — landed as [trellis #107](https://github.com/kodhama/trellis/pull/107)
      (stacked on [#106](https://github.com/kodhama/trellis/pull/106), the
      decision-0042 lifecycle adoption): eleven roles, native linter
      renamed to the corpus-reviewer reference instance (four surgical
      edits, diff-verified), canonical status language unchanged.
- [x] design-system: [design-system PR #4](https://github.com/kodhama/design-system/pull/4)
      — conductor-verified (+752 additive, 14 files, zero markers,
      CLAUDE.md grove block above an intact trellis block)
- [x] Conductor: verification of DS lane done; trellis lane verified in
      its stopped state (no branch, no edits — clean). The DS lane's
      quality critique of the conductor's own kodhama fills (clunky
      mechanical substitution) was confirmed and fixed — all nine
      parenthetical fill sites rewritten as prose.
- [x] Report appended; wave closed pending merges

## Maintainer redirects (mid-wave, 2026-07-08)

1. **Generalize the corpus reviewer into grove.** Trellis's native
   conformance-reviewer (corpus linter) becomes a new grove role
   (`corpus-reviewer`): checks 1–7 are already repo-agnostic; corpus
   dirs, contract paths, and repo-typed extra checks become
   placeholders. Grove's build-gate `conformance-reviewer` keeps its
   canonical name; trellis's native file becomes the trellis instance
   of the new role. Collision dissolves.
2. **Uniform lifecycle across ALL repos, including trellis-self.**
   Supersedes the consolidation's recorded trellis carve-out
   (`draft → ratified` native). Requires a cross-family decision
   (kodhama 0004), a trellis-side supersession + `ratify-guard` update,
   and makes the six-file status-language rewrite in the trellis
   install unnecessary (canonical grove wording installs unchanged).

## Parked

- Live plugin smoke (maintainer-only): `/plugin marketplace add
  kodhama/kodhama` → `/plugin install grove@kodhama` → `/grove:setup` —
  no scripted path exists in this CLI build.

## Report (close, 2026-07-08)

Wave complete pending merges. Installs landed: kodhama (conductor,
self), design-system (lane), trellis (lane, stacked on the lifecycle
PR), wisp already grove-managed since B4. Grove itself and math-quest
deliberately skipped (recorded reasons above).

Both maintainer redirects executed as ratified decisions, not patches:
`kodhama-0004-uniform-lifecycle` (merged, bumped approved) with its
trellis-side execution open as [#106](https://github.com/kodhama/trellis/pull/106)
(decision-0042 + ratify-guard + CLAUDE.md + profile mapping +
artifact-contract rubric alignment); grove `adr-0001` (merged, bumped
approved) adding the corpus-reviewer role, with catch-up PRs composing
the instance into wisp/kodhama/design-system and the plugin payload
(grove #7, wisp #7, kodhama #9 — this PR — design-system #5).

Findings owned along the way: the conductor's own kodhama fills needed
a prose rewrite (flagged by the DS lane) and had one line-wrapped
dangling charter pointer (flagged by the catch-up lane, fixed on this
branch); B4's wisp block predated the grove:begin markers (added on
wisp #7); the trellis lane's cross-reference audit caught the
artifact-contract rubric as a missed 0042 dependent (fixed on #106).
Lanes: DS install ≈122k tokens, trellis install ≈109k+139k (two
sittings), catch-up ≈107k — all Sonnet 5; decisions and instance
authoring by the conductor on Fable.

Outstanding merges, in order: trellis #106 → #107 (stacked,
auto-retargets), then grove #7 · wisp #7 · kodhama #9 ·
design-system #5 (independent). Post-merge bumps owed: trellis 0042
`gated → approved`; grove charter/adr bumps already ride grove #7.

## Report

(appended at close)
