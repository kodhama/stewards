# kodhama — org meta

This repo is the kodhama family's meta home. THREE things live here and
nothing else: **cross-family decisions** (`decisions/`), the **family
front door** (`docs/` — a generated derivative of kodhama/design-system,
built only after the DS ships its LP generator), and the **conductor
seat** (`conductor/` — wave briefs and ledgers for work that spans
family repos).

The family: [trellis](https://github.com/kodhama/trellis) (governance) ·
[grove](https://github.com/kodhama/grove) (agent swarm) ·
[wisp](https://github.com/kodhama/wisp) (runtime observability) ·
[design-system](https://github.com/kodhama/design-system) (brand asset,
git-tag versioned) · [homebrew-tap](https://github.com/kodhama/homebrew-tap)
(delivery). Dependency direction is strictly downward
(wisp → grove → trellis); the DS reaches consumers only through
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
- This repo runs the kodhama stack on itself once grove + wisp are
  liftable; until then the trellis overlay alone is owed — if the
  `trellis` CLI is available run `trellis setup`, otherwise record the
  debt in `conductor/` loudly.

<!-- trellis:begin (managed by trellis — edit .trellis/, not this block) -->
This project follows **Trellis** — working rules you are expected to follow while you work here. They are imported below:
@.trellis/trellis.md
<!-- trellis:end -->
