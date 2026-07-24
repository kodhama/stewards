---
id: kodhama-0002-delivery-channels
type: decision
status: approved  # ratified by PR #1 merge (2026-07-07); names read through kodhama-0003-family-naming
depends_on: [kodhama-0001-family-delivery]
superseded_in_part_by: [kodhama-0009-org-topology-spirit-stewards-trees]  # 2026-07-15 — §Decision 2's host-repo clause only ("in kodhama/kodhama"); the one-marketplace principle and the "kodhama" name stand
owner: agent
updated: 2026-07-07
provenance: maintainer review session 2026-07-07 — re-examination of family delivery prompted by espalier's interim vendoring UX; ratifies 0001's core and answers its marketplace open question
---

# Decision: family delivery — one marketplace front door, npx for espial

> **Superseded in part by `kodhama-0009-org-topology-spirit-stewards-trees`**
> (2026-07-15 annotation; text below preserved as written). §Decision 2's
> clause "one org marketplace **in `kodhama/kodhama`**" is superseded: the
> marketplace's host repo moved to `kodhama/stewards` when the org was
> reframed as the forest (spirit / stewards / trees). The *principle* (one
> canonical org marketplace) and the marketplace **`name`** (`kodhama`) are
> unchanged — so no consumer's `@kodhama` plugin references change. Read the
> install strings below (`/plugin marketplace add kodhama/kodhama`) as
> `kodhama/stewards`.

> **Amended in part by `kodhama-0007-one-render-many-copiers`**
> (2026-07-10 annotation; text below preserved as written). The trellis
> rows' end-user binary channels are retired by 0007 rule 5: brew
> (`kodhama/tap`) goes with the tap deprecation, and the curl installer
> as a *binary* channel goes with it (kodhama/trellis#120). A curl path
> may return as a thin mechanical *copier* script — kodhama/trellis#124.
> Espalier/espial rows stand.


> **Forward pointer (2026-07-07, post-ratification annotation).**
> `kodhama-0003-family-naming` renames espalier → **grove** and
> espial → **wisp**. This decision was ratified carrying the pre-rename
> names; per the append-only rule its text below is preserved as merged.
> Read every espalier/espial through that mapping — in particular the
> delivery strings: plugin **`grove@kodhama`**, setup skill
> **`/grove:setup`**, npm **`@kodhama/wisp`**.

> **Forward pointer (2026-07-09, post-ratification annotation).**
> `kodhama-0006-lp-ownership-to-design-system` amends §5 / AC4 in part:
> the per-product canonical LP install blocks for grove and wisp no
> longer apply — both retired their per-repo `docs/index.html` /
> `docs/lp-content.md`, pending a design-system-owned LP generator.
> trellis's LP block is unaffected.

> **Forward pointer (2026-07-10, post-ratification annotation).**
> The "Open questions" alias question, resolved: **trellis's in-repo
> marketplace is deprecated.** `.claude-plugin/marketplace.json` removed
> from `kodhama/trellis`; the org marketplace (`kodhama/kodhama`) is now
> the only door. Maintainer's call — nothing in trellis's own docs or
> self-hosting depended on the alias, and its own honesty section already
> puts external adoption at "validated on essentially one project," so
> the migration cost of retiring it is judged near-zero.

> **Forward pointer (2026-07-23, post-ratification annotation).**
> `kodhama-0012-codex-marketplace-channel` amends “one marketplace front
> door” from one Claude-specific manifest to one canonical marketplace
> **repository** with one host-native manifest per supported plugin host.
> The marketplace name `kodhama`, thin-catalog principle, and product-owned
> release cadence stand unchanged.

**Context (maintainer, 2026-07-07).** Espalier's current delivery
("vendor the charters by hand", espalier README §Adopting) reads as
inconsistent with trellis (brew + curl + Claude plugin). The maintainer
raised four alternatives: same-mechanism-for-all, npx, an org-wide CLI
repo bundling every product's assets, and (again) a monorepo. Assessment
against the repos and `kodhama-0001-family-delivery` found the
inconsistency real but already anticipated: 0001's channel matrix marks
espalier's vendoring as the *interim* state with the Claude plugin
marketplace as target. This decision closes the loop: it ratifies 0001's
core, answers its open marketplace question, and amends the channel
matrix — so the LP/design work has a settled install story to build on.

## Decision

1. **Ratify 0001's core: polyrepo, no builder repo, no monorepo.**
   Monorepo was re-examined at the maintainer's prompt; nothing observed
   trips 0001's recorded revisit trigger (>⅓ of family furrows needing
   coordinated multi-repo PRs), and its rationale (three product natures,
   independent cadences, repo-rooted tap/marketplace mechanics) stands.
   The org-wide-CLI idea is the "Lane E builder repo" 0001 §Decision 5
   already superseded — it recreates release-cadence coupling and
   reintroduces a binary for products that don't need one. Rejected on
   the same grounds.

2. **One org marketplace in `kodhama/kodhama` is the family's canonical
   install front door.** This repo hosts `.claude-plugin/marketplace.json`
   whose entries point at plugins living in their own product repos —
   verified against official Claude Code docs: marketplace source and
   plugin source are separate repos, pinned and versioned independently
   ([code.claude.com/docs/en/plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)).
   The family install story becomes:

   ```
   /plugin marketplace add kodhama/kodhama
   /plugin install trellis@kodhama
   /plugin install espalier@kodhama
   ```

   This is the marketplace homolog of the shared tap (0001 §Decision 2):
   one thin repo, N entries, no build logic — and it answers 0001's open
   question "one marketplace per repo, or one org marketplace?" in favor
   of the org marketplace. Trellis's existing in-repo marketplace
   (`/plugin marketplace add kodhama/trellis`) keeps working as an alias;
   installer references on LPs/READMEs migrate to the org marketplace.
   This extends the meta repo's "family front door" mandate (CLAUDE.md) —
   the marketplace is front-door surface, not product content; CLAUDE.md
   gains one line saying so at implementation.

3. **Espalier ships as a Claude Code plugin with a composing setup
   skill — never a binary, and no npx.** The plugin (skills + agents +
   commands in one plugin is doc-verified) carries an `/espalier:setup`
   skill that composes charters into the consuming project and asks the
   placeholder questions interactively — the trellis M1 overlay pattern,
   which is what the per-project customization actually requires; a
   read-only plugin install alone cannot fill placeholders, and npx
   would add a Node dependency to deliver an unversioned snapshot (the
   exact weakness of today's hand-vendoring, automated). Hand-vendoring
   remains documented as the manual fallback path.

4. **npx joins espial's channel row.** `npx @kodhama/espial` serving the
   dashboard zero-install is the canonical npx shape for a zero-dep Node
   server, and the `@kodhama` scope is already 0001's answer to the npm
   name collision. Channels at release: npm install · npx · vendored
   copy; tap formula still only if a real CLI emerges.

5. **Canonical LP install blocks** (the input the DS/LP generation and
   the espalier LP design run consume — 0001: "each product's installer
   reference lives on its OWN LP"):
   - **trellis** — brew (`kodhama/tap`) · curl installer · plugin via org
     marketplace.
   - **espalier** — plugin via org marketplace + `/espalier:setup`;
     vendoring shown as the manual path. Pass/fail guard: the LP does not
     publish an install block whose commands don't work yet — if the LP
     ships before the plugin, the plugin block is explicitly marked as
     the target channel and vendoring as the current one.
   - **espial** — `npx @kodhama/espial` (try-it) + `npm i @kodhama/espial`
     (adopt) at release; vendored copy until then.

## Channel matrix (amends 0001 §Decision 4)

| Artifact | Now | At first release | Channels long-run |
|---|---|---|---|
| trellis | unchanged | — | curl (own repo) · `kodhama/tap` brew · **org marketplace** (in-repo marketplace stays as alias) |
| espalier | overlay via lift (hand-vendor) | **plugin `espalier@kodhama` + `/espalier:setup`** | org marketplace + composed overlay — never a binary, no npx |
| espial | vendored copy | npm `@kodhama/espial` · **`npx @kodhama/espial`** | npm · npx · vendored · tap formula only if a real CLI emerges |
| future tools | own repo | entry in tap and/or org marketplace | inherit this matrix |

## Acceptance criteria

- **AC1** From a clean machine: `/plugin marketplace add kodhama/kodhama`
  then `/plugin install trellis@kodhama` and `/plugin install
  espalier@kodhama` both succeed.
- **AC2** `/espalier:setup` composes the charters into a fresh project,
  prompting for each placeholder; espalier's README demotes hand-vendoring
  to "manual path".
- **AC3** At espial release: `npx @kodhama/espial` serves the dashboard
  on a clean machine with Node ≥ 22.18.
- **AC4** Each product LP carries its own canonical install block per §5;
  no LP publishes install commands that don't work at publish time.
- **AC5** `kodhama-0001-family-delivery` is `approved` with its
  marketplace open question annotated as answered here (same merge as
  this decision).

## Open questions (parked, ≤3)

- Does trellis's in-repo marketplace deprecate once the org marketplace
  is live, or stay as an alias indefinitely? (Decide when the org
  marketplace ships; alias until then.) **Resolved — see the
  2026-07-10 forward pointer above.**
- Marketplace `name` string (determines the `@kodhama` install suffix) —
  confirm at implementation that the org marketplace can be named
  `kodhama` and that nothing collides. **Resolved (2026-07-10) —
  implemented as `"name": "kodhama"` in `.claude-plugin/marketplace.json`;
  no collision observed.**

## Self-check (gate)

No research rubric applies (`type: decision`, not discovery; note: 0001's
`rubrics/research-quality.md` path does not exist in this repo — dangling
migration ref, flagged in the ratification PR). Gate check against the
repo's rules: load-bearing external claims (cross-repo marketplace
sources, versioned updates, multi-component plugins) verified against
official docs this session, cited inline; monorepo/builder rejections
trace to 0001's recorded rationale rather than re-arguing from scratch;
every consequential choice (org marketplace as canonical, trellis alias,
espalier no-npx, LP pass/fail guard) is stated, not implied; ACs give a
pass/fail "done". Promote `draft → gated`. `approved` = human merge of
the ratification PR.
