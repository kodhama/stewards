---
id: plan-kodhama-meta-bootstrap
type: plan
status: gated
depends_on: [plan-suite-lift]
rubric: rubrics/spec-quality.md
owner: agent
updated: 2026-07-07
---

# Bootstrap: kodhama/kodhama as the org meta home + conductor seat

Execute this INSIDE a fresh clone of `kodhama/kodhama` (empty repo), with
the math-quest source clone available as a sibling at `../mq-source`
(branch `claude/agentic-runtime-viz-x1884q`). This is E2 of
`../mq-source/plans/plan-suite-lift.md`, pulled forward because the org
conductor runs from here.

## 1. Write `CLAUDE.md` (exactly this content, then adjust only if wrong)

```markdown
# kodhama — org meta

This repo is the kodhama family's meta home. THREE things live here and
nothing else: **cross-family decisions** (`decisions/`), the **family
front door** (`docs/` — a generated derivative of kodhama/design-system,
built only after the DS ships its LP generator), and the **conductor
seat** (`conductor/` — wave briefs and ledgers for work that spans
family repos).

The family: [trellis](https://github.com/kodhama/trellis) (governance) ·
[espalier](https://github.com/kodhama/espalier) (agent swarm) ·
[espial](https://github.com/kodhama/espial) (runtime observability) ·
[design-system](https://github.com/kodhama/design-system) (brand asset,
git-tag versioned) · [homebrew-tap](https://github.com/kodhama/homebrew-tap)
(delivery). Dependency direction is strictly downward
(espial → espalier → trellis); the DS reaches consumers only through
generation-time links. This repo sits above all of them and none of
them know it.

Rules (the family's, applied here):
- **Decisions are append-only** — markdown with frontmatter
  (`id/type/status/depends_on/owner`); supersede with a forward pointer,
  never edit a ratified decision.
- **One home per kind of information** — product truths live in product
  repos; only genuinely cross-family content lands here. When in doubt,
  it belongs to a product.
- **Conductor practice**: each cross-repo wave gets a brief in
  `conductor/`; the brief IS the ledger — check items off in the same
  commits that report them; parked questions batch to the human ≤3 at a
  time; every wave ends with a report appended to its brief.
- **Model economy**: Sonnet-class for execution waves; strongest model
  only for design/judgment sittings (see the suite-lift plan §Model
  economy, until that section migrates here).
- This repo runs the kodhama stack on itself once espalier + espial are
  liftable; until then the trellis overlay alone is owed — if the
  `trellis` CLI is available run `trellis setup`, otherwise record the
  debt in `conductor/` loudly.
```

## 2. Migrate the org decisions

Copy from `../mq-source/discovery/`:
- `kodhama-delivery.md` → `decisions/0001-family-delivery.md`
- the §Adoption-&-lift + naming/DS-homing decision content is NOT copied
  (it lives in the suite-lift plan, which stays in math-quest until Lane
  C); only the delivery discovery moves now.
Adjust the moved file's frontmatter: `id: kodhama-0001-family-delivery`,
add a `provenance:` line naming the math-quest original. Note in the
wave report: **math-quest owes a supersession pointer** in
`discovery/kodhama-delivery.md` (one-paragraph stub pointing here) — to
be committed on the math-quest branch, not from this wave.

## 3. Seat the conductor

- `conductor/wave-1.md` ← copy of `../mq-source/plans/lift-conductor-brief.md`
  (it is the live brief; its checkboxes get ticked here as lanes land).
- `README.md` — three sentences: what this repo is, the family map line,
  where the conductor sits.

## 4. Commit and push

Single commit to main (bootstrap exception, loud):
`bootstrap: org meta home — CLAUDE.md, decision 0001, conductor seat (wave 1)`.
Then **restart context** (the session should reload CLAUDE.md) and
execute `conductor/wave-1.md` as the conductor.

## Acceptance criteria

- AC1: kodhama/kodhama main has CLAUDE.md, decisions/0001, conductor/wave-1.md, README.
- AC2: decision 0001 carries provenance to the math-quest original.
- AC3: the wave-1 brief executes from here with its ledger updated in-place.

## Open questions

None — anything discovered parks per conductor practice.
