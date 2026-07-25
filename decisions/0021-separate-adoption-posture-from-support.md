---
id: kodhama-0021-separate-adoption-posture-from-support
type: decision
status: gated
depends_on: [kodhama-0009-org-topology-spirit-stewards-trees, kodhama-0012-codex-marketplace-channel, kodhama-0017-retire-family-release-certification, kodhama-0018-stewards-dual-host-plugin-package]
informed_by: [kodhama-0013-family-codex-native-product-support]
owner: agent
updated: 2026-07-25
provenance: "maintainer shaping, 2026-07-25: balance structured methodology with gradual exploration; stewards may cross-dogfood, trees such as math-quest may opt into preview, and support remains an earned public promise; start minimal and dogfood Grove first; exact draft approved to proceed to independent soundness review"
---

# Decision: separate adoption posture from support

## Decision state

**Decided** (maintainer shaping, 2026-07-25):

- Use three adoption postures: `dogfood`, `preview`, and `supported`.
- Stewards may cross-dogfood relevant family plugins during ordinary
  development.
- A real tree or other consumer, including Math Quest, may explicitly opt into
  preview use without making a support claim.
- Support is an affirmative, product-owned public promise earned through that
  product's chosen evidence.
- A host-valid package may be distributed or listed for disclosed dogfood or
  preview use before it is supported.
- Start minimally with Grove using its own planner; do not build a family
  maturity framework or begin a collective rollout yet.

**Open** (0):

- None.

**Parked** (3):

- Grove's exact candidate-surface confirmation and release behavior belong to
  a Grove-owned decision after this family policy settles.
- A cross-repository rollout brief belongs in `conductor/` only when a real
  rollout is authorized.
- Math Quest preview adoption remains optional and unstarted until its
  maintainer deliberately opts it in after Grove dogfood.

## Context

The collective wants more structure than unrecorded, intuition-only
development without turning a solo, exploratory plugin family into an
enterprise certification program. Current catalog-admission language in
decisions 0012 and 0018 requires a supported host surface before a plugin may
be listed. In practice that couples honest experimentation and distribution
to the strongest public support claim.

Decision 0017 already rejects a shared release-certification system and keeps
product release and support ownership in each product. This decision applies
that boundary to gradual adoption: missing support evidence blocks the word
`supported`, not clearly disclosed dogfood or preview use.

## Decision

### 1. The three terms describe adoption posture

`dogfood`, `preview`, and `supported` describe how a plugin is being relied
upon. They are not universal release tiers, package-version states, surface
schema values, or machine-enforced gates.

- **Dogfood** is use by a steward or family-maintenance repository while the
  family is actively developing and learning from the plugin. Breakage is
  acceptable, limitations are disclosed, and no support claim is made.
- **Preview** is explicit opt-in use by a real product or other consumer that
  accepts instability. It uses normal review, tests, and a practical rollback
  path, but carries no public support promise.
- **Supported** is an intentional public reliability or compatibility promise
  made by the product that owns the plugin. The product chooses and retains
  evidence adequate for that promise.

Catalog presence, installation success, versioning, and release tags do not
by themselves move a plugin between these postures.

### 2. Distribution is not a support claim

A host catalog may list a package for dogfood or preview when:

- the package is structurally valid for that host;
- the catalog pointer resolves the product-owned source; and
- the listing or linked product documentation clearly discloses that support
  is not claimed.

An invalid package, false source pointer, or misleading support statement
still blocks admission. Evidence from one host never establishes support on
another.

This partially supersedes only:

- decision 0012's requirement that Codex catalog admission wait for an already
  supported Codex surface; and
- decision 0018 section 3 and AC3 where they require a supported surface
  before either host catalog may list the package.

Their thin-catalog, valid-package, host-separation, independent-version, and
product-ownership boundaries remain current.

Decision 0013's native-support standard remains unchanged. Dogfood or preview
use does not satisfy or weaken its prohibition on advertising native support
before the product has exercised and evidenced that claim.

### 3. Products retain judgment and ownership

Stewards defines the shared words and owns its thin catalogs. Each product
independently decides:

- whether and where it permits dogfood or preview use;
- its release version and cadence;
- what limitations it discloses;
- what evidence is sufficient for its own support promise; and
- when, if ever, it promotes a surface to supported.

Math Quest is a tree and therefore a preview candidate, not a steward
dogfooding environment. Its personal-project status does not erase the
distinction: it is a real product whose work may rely on the plugin.

### 4. Minimal first

This decision creates no maturity registry, shared schema, universal evidence
format, cross-product release gate, synchronized version, support evaluator,
or rollout automation.

The first use is Grove-local dogfood of the implementation planner. Any
Grove release-policy or lifecycle change stays Grove-owned. A conductor brief
is created only when work actually spans repositories, and that first brief
must authorize one bounded step plus a stop-and-learn checkpoint rather than a
whole-family wave.

## Consequences

- The collective can explore through real package distribution without
  mislabeling exploration as support.
- Support evidence remains meaningful because only a product-owned promise
  depends on it.
- The current blocked Wisp catalog draft may later be reconsidered as preview
  distribution, but this draft decision neither approves nor merges it.
- Grove needs a separate product decision before changing its release
  validator or candidate-surface write behavior.
- Math Quest receives no plugin change until it explicitly opts into preview.

## Acceptance criteria

- **AC1:** Dogfood, preview, and supported are defined as adoption postures,
  not machine-enforced release tiers.
- **AC2:** Host-valid dogfood or preview packages may be listed with an
  explicit non-support disclosure.
- **AC3:** Catalog presence and installation never imply support.
- **AC4:** Supported remains a product-owned, evidence-backed public promise,
  with no evidence transfer across hosts.
- **AC5:** Decisions 0012 and 0018 retain every boundary except their
  supported-surface-before-listing requirement.
- **AC6:** No family registry, schema, certification engine, shared release
  gate, or rollout automation is introduced.
- **AC7:** Grove dogfood is first; collective rollout and Math Quest preview
  adoption remain unstarted.

## Open questions

None.

## Self-check

This decision records the maintainer's agreed gradual-adoption model at the
cross-collective layer, where shared catalog and steward/tree meanings belong.
It changes only the admission/support coupling that conflicts with that model,
preserves product ownership and host-specific honesty, and adds no machinery.

## Lifecycle record

This began as the first durable shaping canvas. On 2026-07-25, after reviewing
the exact draft, the maintainer confirmed that it captured the intended model
and approved proceeding to independent soundness review. That advances the
decision to `gated`; it is not yet ratified.
