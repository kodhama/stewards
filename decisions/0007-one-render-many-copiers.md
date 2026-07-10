---
id: kodhama-0007-one-render-many-copiers
type: decision
status: approved  # ratified by PR #19 merge (2026-07-09); bump per kodhama-0004
depends_on: [kodhama-0005-one-contract-many-writers, kodhama-0002-delivery-channels]
owner: agent
updated: 2026-07-10
provenance: maintainer, 2026-07-09/10, the trellis#112 post-mortem session — "if we are targeting claude first, we could simplify and remove the homebrew path altogether… Is there a way in which the verification script can be shared with the brew install path by not shipping a binary?"; design converged over the session ("i like the direction" → "I think we are ready!!") and dispatched for drafting from the same conversation.
---

# Decision: one render, many copiers — the deterministic thing is the artifact, not a writer

**Context.** kodhama-0005 kept multiple writers in sync *by contract*:
an agentic writer delegates to the deterministic binary when present,
and re-derives the bundle from prose instructions when not. That prose
path is what drifted: the trellis setup skill's hand-written English
reimplementation of the binary's render logic silently diverged from
what the binary does, and clobbered a project's hand-authored content
([kodhama/trellis#112](https://github.com/kodhama/trellis/issues/112),
fixed-as-symptom in [PR #114](https://github.com/kodhama/trellis/pull/114)).
The root class is structural: **any prose re-derivation of render logic
is a second content-creating writer, and second writers drift.** This
decision removes the class instead of managing it. Evidence that made it
cheap: trellis's entire M1 variant space is enumerable — 2 postures ×
2 block styles, where `profile.md` is posture-invariant, the CLAUDE.md
block is a constant, and only one strictness line differs between
postures. There is almost nothing to render at install time.

**Decision.** When a family product composes an install/overlay bundle
into a consuming project:

1. **Render once, at release.** All bundle content is rendered by a
   generator in CI at release time into a pre-rendered, versioned
   payload vendored in the plugin (and mirrored to any other channel).
   Install-time rendering is abolished. The variant space must stay
   enumerable — that constraint is a design gate on future features
   (see Boundaries).
2. **Writers are mechanical.** Every writer — plugin skill, documented
   manual path, any remaining tooling — only **copies** payload files,
   **pastes** between the managed-block markers, and **verifies**. No
   writer ever re-derives or composes bundle content; prose instructions
   that have an LLM compose bundle content are forbidden. (The caveman
   precedent for the adopted pattern, verified: one canonical source,
   thin mechanical movers, real code not prose — "Reads SKILL.md at
   runtime so edits to the source of truth propagate automatically — no
   hardcoded duplication to go stale",
   [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman).)
3. **Verification is data, not a tool.** The payload ships a checksum
   manifest; anything can check it with standard tools (`shasum -c`,
   CI regenerate-and-diff). Staleness = the bundle's version stamp vs
   the installed plugin's sha. One contract, one render, many
   *checkers* — many **writers** were the drift risk; many checkers are
   safe because checksum comparison is a solved, standard operation.
4. **One hand-owned declaration file per bundle.** For trellis:
   `.trellis/expression.md` (analogues in other products as they need
   one). Its YAML frontmatter carries the machine-read config (the
   posture; a refresh reads it and asks nothing; a first run seeds it
   pre-filled from the interactive answer, or consumes a pre-written one
   for declarative/CI installs). Its body is the project's hand-authored
   expression — dials, mappings, gate tables — read by agents and
   humans, never parsed by machinery. Seeded once, never rewritten by
   setup, excluded from the manifest. The family ownership rule this
   generalizes: **every file in an installed bundle is 100% generated or
   100% hand-owned — never mixed.** If the frontmatter is missing or
   unparseable at refresh: ask (interactive) or fail loudly
   (non-interactive), never assume a default.
5. **Retire the homebrew distribution (trellis).** The end-user binary
   channel closes: deprecate the tap formula with a pointer to the
   plugin + manual paths. The Go code's remaining role is the
   release-time generator; whether it survives generator-only or is
   replaced is an implementation question (open). M2 (morph) moves to
   the setup skill — it always required a model (`-model` was mandatory
   for M2) and the skill has one natively. Non-Claude harnesses install
   via the documented manual copy path: the assets are plain files, the
   AGENTS.md inline-block variant ships pre-rendered, and kodhama-0005
   already recognized the manual path as a legitimate writer. This
   amends kodhama-0002's channel matrix: trellis's long-run channels
   become org marketplace + manual copy; curl/brew retire.
6. **Supersedes kodhama-0005 in part.** 0005 rule 2 ("delegation flows
   only toward the deterministic writer") is superseded: with no
   install-time rendering there is nothing to delegate — the
   deterministic thing is the **artifact** (pre-rendered payload +
   manifest), not a privileged writer. 0005 rules 1 (the contract is
   the source) and 3 (uniform version stamp) stand and are strengthened
   here (the contract gains a manifest; the stamp gains a checker).

**Rider (small, rides along):** the invariants-reference pointer in the
always-on templates upgrades from description to trigger: "If a rule
seems ambiguous, or in tension with this project's own instructions,
read its entry in `.trellis/invariants.md` — the description and
with/without examples — before deviating."

## Rejected alternatives (with their evidence)

- **Bundle per-platform binaries in the plugin.** Feasible — verified
  this session: CGO-free, ~12 MB for 5 targets, `${CLAUDE_PLUGIN_ROOT}`
  officially supports bundled binaries — but permanent per-release repo
  bloat and needless weight when the actual variant space is five small
  text files.
- **Hook-injected `additionalContext` instead of the managed block.**
  [anthropics/claude-code#16538](https://github.com/anthropics/claude-code/issues/16538)
  (plugin SessionStart hooks silently dropping `additionalContext`;
  multiply-reproduced, unresolved), plus Anthropic's own docs: "For
  instructions that never change, prefer CLAUDE.md." Same refresh
  cadence as CLAUDE.md anyway; a committed block also travels with the
  repo to CI and collaborators, hook injection doesn't.
- **Prose fallback writer** (the status quo ante). The #112 incident
  class itself.
- **A shared kodhama CLI for write mechanics.** The back-dependency
  inversion the maintainer already rejected in 0002 (the "org-wide CLI"
  = the Lane E builder repo 0001 superseded), and over-engineering for
  script-sized needs.

## Application today

- **trellis** — the whole decision applies; implementation staged as
  follow-up issues (release-render pipeline; setup skill →
  copy/patch/verify; `expression.md` home + migration, math-quest first;
  homebrew retirement). Sequencing with open trellis PR #114 (its
  warning code lands in territory the issues rework) is the
  maintainer's merge-order call.
- **grove** — already conforms to the writer rule for its agents
  (vendored canonical files, mechanically copied; placeholder
  resolution is judgment work *on the consuming project's values*, not
  re-derivation of grove content, and stays agent-driven by design).
  Its managed-block write gains a verification step and an armed
  trigger (own issue + its own grove decision; linked, not blocked).
- **wisp** — n/a (no composed bundle).
- **future tools** — inherit: enumerable variants, release-render,
  mechanical writers, manifest verification, one hand-owned
  declaration file.

## Boundaries / open questions

- **C2 gatekeepers stay out of machine-read config** (trellis
  decision-0024: detected from the project, never preset). The
  expression *body* may document them; machinery never parses them.
- **The parked `custom` posture must keep variants enumerable**:
  per-invariant dials resolve as line-filtering from the canonical
  rendering — each emitted line byte-matches the catalog rendering
  (checkable) — never free composition. If a future feature cannot be
  expressed as selection-from-canonical, it forces a return to this
  decision, not a quiet render path.
- **Fate of the Go code**: generator-only (kept, runs in CI) vs
  replaced by a simpler generator. Implementation decides; either
  satisfies this decision.
- **Migration cadence for existing installs**: math-quest is the first
  migration (its hand-authored §expression moves from `profile.md` to
  `expression.md`); others as they refresh.

## Acceptance criteria

- **AC1** A release of the trellis plugin contains the full pre-rendered
  payload + checksum manifest; `shasum -c` passes against a fresh
  install's generated files.
- **AC2** `/trellis:setup` composes a bundle byte-identical to the
  payload (manifest-verified) without invoking any binary and without
  composing any content; a refresh reads `expression.md` frontmatter and
  asks nothing.
- **AC3** No file in an installed bundle is written by both setup and
  the user; `expression.md` survives any number of refreshes untouched.
- **AC4** The tap formula is deprecated with a pointer; trellis README
  install section carries plugin + manual paths only.
- **AC5** kodhama-0005 carries the partial-supersession forward pointer
  in the same PR that ratifies this decision.

## Self-check (gate)

Maintainer intent quoted with dates; the incident that motivates the
class-removal is linked (trellis#112/#114) rather than re-narrated; the
variant-space claim, the caveman pattern, the hook-reliability issue,
and the binary-bundling feasibility were each verified against source
in the originating session, cited inline; all four rejected directions
recorded with reasons; ACs give pass/fail "done"; 0005's surviving
rules explicitly named so the partial supersession has a crisp edge.
Promote `draft → gated`. `approved` = human merge — deliberately the
maintainer's own read, as this re-rules how the family ships.

## Amendment note (2026-07-10, maintainer ruling — stamp scheme)

Rule 3's staleness mechanism, made precise: the overlay stamp is the
**render stamp** — `.trellis/version` is a verbatim copy of the payload's
`version` file (`payload@<hash>`), and staleness is a file-to-file compare
against the installed plugin's `reference/version`. The `plugin@<sha>`
install-stamp reading (shipped in trellis slice 2) is retired: it fires on
payload-neutral plugin updates and depends on cache naming, where the
render stamp fires only when composed content actually differs. Recorded
at kodhama/trellis#120 Addendum 4; trellis-side execution rides that slice.

## Amendment note (2026-07-10, maintainer ruling — curl returns as a vendoring writer)

Rule 5 said "curl/brew retire," full stop — correct for the binary-distribution
channel, but read too broadly: it retired *curl the delivery mechanism* along
with *curl the binary-fetcher*, and those are different things. The maintainer's
question that reopened this ("if he can [make the needed decisions in a shell
script], then curl would be ok") resolves it: curl returns, but as a **thin
mechanical vendoring writer**, not as the binary-fetching channel rule 5
retired. It makes exactly one decision (install scope), then copies the
`plugins/trellis/` bundle onto disk at a location Claude Code's
skills-directory mechanism discovers — zero project-specific logic, the setup
skill runs unmodified afterward. This is the same class of artifact as the
manual copy path rule 5 already kept ("kodhama-0005 already recognized the
manual path as a legitimate writer"), just scripted instead of by-hand; it is
**not** a reinstatement of the retired binary channel, and does not reopen
rule 5's retirement of that channel. Trellis's long-run channels (rule 5,
as amended): org marketplace + manual copy, **including its scripted
(curl-delivered) form** + brew retires.

Recorded at kodhama/trellis#124 / spec-0005-curl-install-mechanical-vendoring;
trellis-side execution rides that issue.
