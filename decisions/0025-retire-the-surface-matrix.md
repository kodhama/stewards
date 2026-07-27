---
id: kodhama-0025-retire-the-surface-matrix
type: decision
status: approved  # maintainer intent act 2026-07-27: "Approved" — on the direction that the surface-matrix ceremony is retired family-wide
depends_on: [kodhama-0017-retire-family-release-certification, kodhama-0018-stewards-dual-host-plugin-package, kodhama-0021-separate-adoption-posture-from-support, kodhama-0023-separate-operational-availability-from-support]
owner: agent
updated: 2026-07-27
---

# Decision: retire the surface matrix as a family contract

## Decision state

### Decided

- **The family surface-matrix contract is retired.** No plugin is required to
  carry a `surfaces.json`, exact surface rows, `availability_state`,
  `support_claim`, or a marketplace-observation record.
- **A product may keep any of it for its own reasons.** `kodhama-0017` §1
  already permits this and it is unchanged. Grove does keep it: it has the
  family's only runtime consumer, a lifecycle gate that decides whether to
  write into a consumer repository. That is a product mechanism answering a
  product question, not a family contract.
- **What replaces it is prose in each plugin's shipped README, plus the CI
  checks that already run.** One paragraph naming the hosts a plugin works on
  and stating that support is not claimed, guarded by an assertion.
- **Stewards deletes its own machinery**: `plugins/kodhama/surfaces.json`, the
  committed observation evidence, `scripts/emit_marketplace_observation.py`,
  `validate_surfaces`, `validate_observation`, the `--observation` CLI mode, and
  the tests anchored to them.
- **The CI steps that genuinely exercise a host are kept.** Running
  `claude plugin marketplace add` and `codex plugin marketplace add` against a
  real checkout and verifying the host's listing is an honest integration test.
  Emitting a JSON record about having done so is not.

### Open

- None.

### Parked

- Whether Grove eventually retires its own copy. That is Grove's call, and its
  gate currently protects a real write decision.

## Context

`surfaces.json` was propagated across the family in a week of over-building. The
maintainer's assessment, 2026-07-27: *"I try to generalize a bit to keep doors
open and explore it, but we're way past the point where any of the boilerplate is
useful."*

**Measured, not asserted.** Outside Grove, nothing in the family reads a *value*
out of this machinery. In Stewards, `surfaces.json` has exactly two readers —
`scripts/validate_kodhama_plugin.py:290` and `tests/test_kodhama_plugin.py:318` —
and both are self-referential: the validator checks the file against itself and
the test checks that the validator did. The committed evidence under
`plugins/kodhama/evidence/` is a frozen snapshot of one CI run; CI emits fresh
observations to `artifacts/` and never compares them to it. In Trellis both
`marketplace_test_observations` arrays are empty, so a 79-line observation
validator validates a record the repository never instantiates.

**Wisp already did this retirement and came out ahead.** It replaced its matrix,
its qualification file, a 152-line verifier and a 170-line test with **four lines
of README and four regex assertions**, plus a repo-wide grep test that fails CI if
`surfaces.json` is ever reintroduced. Its replacement is strictly better than what
it replaced: the claim is user-visible, it ships inside the package so it survives
outside the marketplace, and CI enforces it.

**The two failures this machinery was meant to prevent are already prevented by
things that do not touch it.** Publishing a broken package is caught by
`scripts/keyless_admission_check.py`, which installs through the real Claude
marketplace path and fails closed. Making a false support claim is caught by the
catalog `description` disclosure and the test that pins it literally.

A support matrix has two possible states and both are poor. Where nothing enforces
it, it is documentation with a schema. Where something does — Grove — it became a
gate that refused every operation on every surface for the product's whole life.
Meanwhile the question a reader actually has, *"does this work on my host?"*, is
answered better by a check that ran this morning than by a row that has said
`pending` since it was written.

## Decision

### 1. The family contract goes

No Stewards decision requires a plugin to declare exact surface rows or to record
marketplace observations in a structured file. A product that wants either owns
that choice locally.

### 2. What each plugin says instead

Each plugin's **shipped** `README.md` — inside the package, so it survives outside
the marketplace — carries one paragraph naming the hosts it is known to work on,
which check establishes that, and that support is not claimed. One assertion per
repository guards it.

`plugins/kodhama/` has no README today. It gains one.

### 3. What Stewards keeps

- `scripts/keyless_admission_check.py` in full. It is the only thing that proves
  the published package installs.
- The catalog-parity half of `validate_kodhama_plugin.py`: `VERSION`, both host
  manifests, and the shape of any present catalog entry.
- The catalog `description` disclosure required by `kodhama-0021` §2, and the
  test pinning it literally.
- The CI jobs that run a real `marketplace add` on both hosts and verify the
  host's listing.

### 4. The record of which marketplace a test used

`kodhama-0017` §2 retains the *goal* of recording which marketplace on which host
a test exercised. That goal is met by the GitHub Actions run log, which records
the checkout revision with better provenance than a checked-in file whose own spec
admits it *"does not claim that the external run was authenticated."* The
structured record is retired; the goal is not.

## Supersession

**`kodhama-0023` — superseded in full.** Its field grammar was the family mandate
that propagated this machinery, and AC6 (*"Every active plugin's declared exact
surface rows use `availability_state` and `support_claim`"*) is what would regrow
it. Grove may keep the names for its own runtime; no other plugin is required to.

**`kodhama-0018` §1 and AC2 — partially superseded.** `surfaces.json` is no longer
one of the version carriers a Stewards package must maintain. The rest of 0018
stands: `VERSION`, both host manifests, and their parity are unchanged.

**`kodhama-spec-0003` — superseded.** The marketplace-observation record, its
closed schema and its emitter retire together. `specs/README.md` and
`tests/TEST_DEPS.md` are updated in the same change, so the retired schema is not
still advertised as an active implementation input.

**`kodhama-spec-0004` — amended, v4 → v5.** It remains `approved` and its
authoring behaviour is untouched, but it required `surfaces.json` as a version
carrier, specified the observation inputs and emission, and carried surface
parity in R16-R17. An implementer following it could have reintroduced the
deleted contract. Flagged in review against this very record's acceptance
criteria, which asserted no spec required any of it — that was false when
written.

**`kodhama-0017` §2 — amended, not superseded.** Its retained goal survives; only
the schema-shaped implementation of it goes. Its §4 exclusion of *"surface
registries and contracts, catalog/provisioner availability state"* is unchanged
and, read today, argues for this decision rather than against it.

**`kodhama-0021` is untouched.** The non-support disclosure requirement is
strengthened here, not weakened: it moves from a field nobody reads into prose a
user sees.

**Receipts.** `trellis/decision-0064`, `wisp/adr-0013` and `grove/adr-0042`
received the retired strategy. Each gets a one-line forward pointer to this
record — a pointer each, not another propagation wave.

## The risk this decision accepts

**A prospective user loses a machine-readable statement of where a plugin works.**
Nothing consumes it today and no consumer has asked for one, so this is a capability
withdrawn before it was used rather than one taken away. If a consumer ever needs
it, the honest version is generated from checks that ran, not hand-maintained rows.

**Grove diverges from the rest of the family.** It keeps the fields; nobody else
does. That is the intended outcome — `kodhama-0017` §1 explicitly permits a product
to keep a mechanism for its own reasons — but it does mean the family no longer has
one shape here, and a future reader should not mistake Grove's copy for a standard.

## Acceptance criteria

- No Stewards decision or spec requires a `surfaces.json`, exact surface rows, or a
  structured marketplace-observation record from any plugin.
- `plugins/kodhama/` ships a README naming its hosts and disclosing that support is
  not claimed, guarded by a test.
- `scripts/keyless_admission_check.py`, the catalog-parity checks, the disclosure
  test, and the real `marketplace add` CI steps all survive unchanged.
- `python3 scripts/validate_kodhama_plugin.py` passes, and the test suite is green,
  with the surface and observation machinery gone.
- Each receiving repository carries a forward pointer to this record.
- Trellis's `surfaces.json` and its `install.sh` bundle-manifest entry are removed
  **in the same commit** — the bundle fetches a moving `main`, so splitting them
  breaks `curl | sh` for every user immediately.

## Lifecycle record

Authored 2026-07-27 from the maintainer's direction to retire the surface-matrix
ceremony family-wide, with the balance they set: *"Not hacky but also not
over-engineered. Independent but not forgetting the main user."*

An earlier reading of `kodhama-0017` in this session claimed it *mandated* the
observation machinery, and that claim was wrong: `:113-115` says the decision
*"authorizes the goal, not a schema"*, and `:147-148` excludes surface registries
outright. The machinery came from `kodhama-0018` and `spec-0003`. The error is
recorded because it was stated confidently and acted on.

**`approved` 2026-07-27** by the maintainer's intent act. The direction was given
earlier the same day — *"the retiring direction of the ceremony is exactly what I
want to do… we're way past the point where any of the boilerplate is useful"* —
and this record is its ratification.
