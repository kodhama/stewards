# stewards — the collective's coordination hub

The **stewards** are [kodhama](https://github.com/kodhama/kodhama)'s worker
collective — the scaffolding that tends the forest's trees (the products)
and tends itself. This repo is their coordination hub: it continues the
operational role formerly held by `kodhama/kodhama`, relocated here per
`kodhama-0009` so the kodhama repo can be the forest-spirit front door.
THREE things live here and nothing else: **cross-collective decisions**
(`decisions/`), the **conductor seat** (`conductor/` — wave briefs and
ledgers for work that spans the collective's repos), and the **install
door** (the collective's canonical install repository per `kodhama-0002`,
`kodhama-0012`, and `kodhama-0017`).

<!-- distribution-scope:begin -->
The install door includes the host-native Claude and Codex catalogs. Its
future distribution scope is deliberately narrow: metadata that records which
marketplace a test exercised, and a generic Stewards skill that adds
caller-selected Claude/Codex marketplace setup to CI. It does not certify
product releases or support and owns no universal version, tag, release-history,
approval, runtime-sandbox, cross-repository-resolution, or effective-support
machinery. The superseded implementation remains temporarily pending its
separate removal change.
<!-- distribution-scope:end -->

Decisions made here keep the `kodhama-NNNN` id namespace — they are kodhama
decisions made at the collective (steward) layer; spirit/org-level decisions
live in `kodhama/kodhama` (see `kodhama-0009`).

The stewards: [trellis](https://github.com/kodhama/trellis) (governance) ·
[grove](https://github.com/kodhama/grove) (agent swarm) ·
[wisp](https://github.com/kodhama/wisp) (runtime observability) ·
[design-system](https://github.com/kodhama/design-system) (brand asset,
git-tag versioned) · [homebrew-tap](https://github.com/kodhama/homebrew-tap)
(delivery).
Dependency direction is strictly downward
(wisp → grove → trellis); the DS reaches consumers only through
generation-time links. Layering: **trellis carries the principles; grove
carries the operating model** — mechanics included. Repos, this one
included, restate neither (`kodhama-0008`). This hub sits above all of them
and none of them know it.

Rules (the collective's):
- **Decisions are append-only** — markdown with frontmatter
  (`id/type/status/depends_on/owner`); supersede with a forward pointer,
  never edit a ratified decision.
- **One home per kind of information** — product truths live in product
  repos; only genuinely cross-collective content lands here. When in doubt,
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
- **Legacy distribution quality gate (temporary until the superseded
  implementation is removed):** changes under the existing `distribution/`
  tree still run
  `distribution/check`. It executes the spec-anchored tests, door validation,
  generated-file staleness check, Python compilation, annotation coverage,
  dependency-free Python lint/format checks, JSON parsing, and both working-tree
  and committed CI-range whitespace checks. This project-owned rule supersedes the managed
  block's older “no test/typecheck gates” description for distribution files;
  the next Grove refresh should update that adapter projection.
  CI provisions product-adoption repositories automatically. Local runs require
  these exact pinned checkouts and resolver mapping:

      git clone https://github.com/kodhama/grove.git .product-repositories/grove
      git -C .product-repositories/grove checkout db650fe5855a197eb65375b50e3e81b1065ebddb
      git clone https://github.com/kodhama/trellis.git .product-repositories/trellis
      git -C .product-repositories/trellis checkout 4062120cea71737bd28cb171785a2dcdd6192deb
      export STEWARDS_PRODUCT_REPOSITORIES='{"kodhama/grove":".product-repositories/grove","kodhama/trellis":".product-repositories/trellis"}'
      distribution/check

  Without that mapping, the gate intentionally fails closed with the
  product-adoption resolver prerequisite instead of trusting unresolved
  references.

<!-- grove:begin (managed by grove — edit .claude/agents/, not this block) -->
This repo is **grove-managed**: conductor work items run as
[grove](https://github.com/kodhama/grove) runs. The agent roles
live in `.claude/agents/` (placeholders resolved for this repo — no
test/typecheck gates, parked items ride the conductor briefs' Parked
sections). Telemetry: wisp not vendored here, no grove-status skill
installed (optional by construction). grove plugin@bf7c835
<!-- grove:end -->

<!-- trellis:begin (managed by trellis — edit .trellis/, not this block) -->
This project follows **Trellis** — working rules you are expected to follow while you work here. They are imported below:
@.trellis/internal/trellis.md
@.trellis/rules.toml
<!-- trellis:end -->
