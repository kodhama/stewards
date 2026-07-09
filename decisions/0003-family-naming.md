---
id: kodhama-0003-family-naming
type: decision
status: approved  # ratified by PR #2 merge (2026-07-07)
depends_on: [kodhama-0001-family-delivery, kodhama-0002-delivery-channels]
owner: agent
updated: 2026-07-07
provenance: maintainer naming sitting 2026-07-07 (design/judgment, strongest model per model-economy rule) — full identity review of the family names against the recorded DS identity and the maintainer's lore. 0001/0002 were ratified (PR #1) before this landed; their pre-rename names read through this decision via forward pointers.
---

# Decision: family naming — the swarm is **grove**, the watcher is **wisp**

**Decision.** `espalier` → **grove** (the agent swarm). `espial` →
**wisp** (runtime observability). `kodhama` and `trellis` are unchanged —
explicitly reviewed and kept. The family reads **kodhama · trellis ·
grove · wisp**.

## Why the old names failed

Confirmed against sources this session:

- **Confusability** — `espalier`/`espial` share the `esp-` prefix with
  near-anagram bodies; the family's own docs must disambiguate
  ("Espial — watching the espalier").
- **Say/spell burden** — both dictionary-obscure; maintainer's own
  testimony: "not working for me."
- **Namespace** — both bare npm names belong to strangers (checked:
  `espial` is a third-party *node event layer* — same domain; `espalier`
  is a third-party placeholder squat). The `@kodhama/` scope hides this
  (0001), but the friction is everywhere else.

The recorded metaphor was NOT the problem and is kept intact: the DS
identity (`design-system/identity/README.md`, `icons/grammar.md`) defines
one scene — structure / growth under the frame / "the kodama watching —
who is working, right now" — and the marks already draw it. This decision
renames two words in that scene; it does not touch the scene.

## Why these names

The triad is one name per order of being, in causal order: **trellis**
the *built* thing, **grove** the *living* thing, **wisp** the *spirit*
thing — *you build the trellis; the grove grows along it; and when the
grove is healthy, the wisps appear.* That last beat is the kodama myth
itself, which makes observability's core story (presence of signal =
health of the swarm) carried by the org's founding metaphor.

- **grove** — a community of trees *and* the actual term for a local
  druidic community (OBOD and ADF chapters are "groves"; ADF starters are
  "protogroves") — so the name covers both readings of the swarm (the
  growth being trained and the crew tending it). WoW resonance: the
  Dreamgrove, the druid order hall. The espalier *concept* survives as
  the tagline: **"a grove trained along a trellis."** One syllable,
  common word, no devtools squatter found (GitHub/npm checked; bare npm
  `grove` is a third-party TODO squat, covered by the `@kodhama/` scope).
- **wisp** — a small spirit-light that reveals: in Warcraft, wisps are
  the night-elf/druid faction's worker-and-scout lights; in *Mononoke*,
  the kodama are small pale forest spirits — visually near-wisps. The
  wisp mark needs no redesign: the existing watcher mark's *lit node* IS
  a wisp. Reading: **"the wisps watch over the grove — who is working,
  right now."** Collisions (checked): an active Gleam web framework
  (~1.4k★), a dormant npm Lisp dialect, an archived NVIDIA research
  lib — none in observability or agents; `@kodhama/wisp` is the
  published surface regardless.
- **trellis kept** — the maintainer likes it; it is the only component
  with shipped delivery surface (released binary, tap formula, plugin
  id, its own ratified decision corpus); and the triad *wants* exactly
  one built-artifact word — all-nature names would erase the built-ness
  of governance from the language. Its neighbors changing is what fixed
  it: next to grove and wisp it is the lone made thing among living
  things.
- **Distinctness** — k/t/g/w initials, 3/2/1/1 syllables, all common
  words, all sayable after hearing and spellable after reading (the
  espalier failure, inverted).

## Considered and rejected (recorded so it isn't re-litigated)

- **perch** (watcher) — cleanest namespace, but names the furniture of
  watching, not the watcher; spends none of the founding myth; also a
  fish. Maintainer unconvinced; superseded by wisp.
- **augury** (watcher) — semantically the most precise ("reading
  voluntarily emitted signs" = wisp's telemetry-is-a-claim invariant),
  but 3 syllables and an archived same-domain Angular devtool (2k★)
  held the name. Wisp's understudy.
- **hamadryad, scry** (watcher) — spelling burden / MtG register.
- **kodama** (watcher) — lore-perfect and fatally colliding with the
  org's own name in speech.
- **strix** — 38k★ AI pentest agent owns it in our exact domain.
- **treant, sapling, sentinel, vigil, watchtower, glade, dryad,
  mycelium, coppice, wildgrowth** (swarm/watcher) — prefix clash with
  trellis (tre-), Meta SCM, existing monitoring products, GNOME tool,
  datadryad.org, crypto wallets, espalier-grade obscurity, ungoverned
  connotation, respectively.
- **Whole-triad alternatives** — `ogham·grove·wisp` (all-Celtic; ogham
  has the say/spell disease and costs trellis's shipped surface),
  `torii·grove·wisp` (sharp gate metaphor, but trades trellis's
  grow-along meaning for pure threshold and mixes three lore languages),
  `roots·grove·canopy` (lovely vertical logic, dead namespace, costs
  trellis). All rejected in favor of keeping trellis.

## Rename scope (the execution wave's fixed target)

1. **Repos**: `kodhama/espalier` → `kodhama/grove`; `kodhama/espial` →
   `kodhama/wisp` (GitHub auto-redirects old URLs). Local checkouts
   follow.
2. **Delivery strings**: kodhama-0002 was ratified pre-rename and
   carries a forward-pointer annotation to this decision; its strings
   read through this mapping — plugin **`grove@kodhama`** with
   **`/grove:setup`**; npm **`@kodhama/wisp`** (wisp has never published
   to npm, so no package migration exists).
3. **Runtime surfaces** (live in wisp's code, named after the swarm):
   `.espalier/runtime/events.ndjson` → `.grove/runtime/events.ndjson`;
   `$ESPALIER_EVENTS` → `$GROVE_EVENTS`; `<ESPIAL_VENDOR_PATH>` →
   `<WISP_VENDOR_PATH>`.
4. **Unchanged**: the swarm's internal vocabulary (gardeners, furrows,
   head-gardener), the icon grammar and marks (relabel
   `espalier.svg`→`grove.svg`, `espial.svg`→`wisp.svg`; the drawings
   stay). *[Superseded in part 2026-07-09 by
   `grove/adr-0002-agent-vocabulary`: gardener→agent, head-gardener→
   dispatcher, furrow→run become grove's official vocabulary, with
   druid/archdruid sanctioned as conversational/marketing register —
   a grove-level decision, not a family one, since it governs grove's
   own internal naming rather than any org-level identifier.]*
5. **Historical records keep their names** — 0001, 0002's ratified text,
   the source repos' ADR-0030-espalier lineage, past conductor briefs
   are not rewritten (append-only); forward pointers only where a doc is
   still consumed.
6. **DS identity absorbs the provenance layer at the T2 design pass**:
   kodhama = the maintainer's WoW druid Gundisalwa Kod'hama (nature
   shapeshifter, guardian) × the kodama of Japanese folklore; the
   shapeshifter reading (trellis = guardian form, grove = restoration,
   wisp = balance); grove as the druidic-chapter term; the wisp–kodama
   bridge; the oral-canon inversion ("the druids kept their canon oral
   and lost it; kodhama is the grove that writes it down — append-only,
   like ogham on stone"). One home: the DS identity page, not here.

## Acceptance criteria

- **AC1** Repos renamed; old GitHub URLs redirect.
- **AC2** No forward-looking family surface (READMEs, LPs, decisions
  after this one, new conductor briefs) uses `espalier`/`espial` except
  as an explicit historical mention.
- **AC3** DS icons and identity tables carry grove/wisp; the provenance
  layer lands with the T2 design pass.
- **AC4** Runtime strings renamed per §3 in the grove and wisp repos.
- **AC5** kodhama-0002 carries its forward-pointer annotation and its
  post-merge status bump to `approved` (landed alongside this decision);
  its ratified text is otherwise untouched.

## Open questions (parked, ≤3)

- The in-flight LP design sitting was briefed as "espalier LP" — does it
  absorb the rename mid-flight or restart its name-dependent parts?
  (Maintainer coordinates; the LP is now grove's.)

## Self-check (gate)

Load-bearing claims verified this session against sources: the DS
identity text quoted from its files; npm ownership of
espalier/espial/grove/wisp checked against the registry; collision
landscape checked on GitHub (strix, wisp, grove, perch, augury);
druidic-grove usage and the oral-canon account are general-knowledge
claims flagged to the maintainer during the sitting, with the
brehon–druid succession explicitly marked inference. Alternatives and
rejections recorded so the choice isn't re-litigated. The append-only
recovery (0001/0002 ratified pre-rename → forward pointers, no rewrite)
is stated, not silent. ACs give pass/fail. Promote `draft → gated`.
`approved` = human merge of the ratification PR.
