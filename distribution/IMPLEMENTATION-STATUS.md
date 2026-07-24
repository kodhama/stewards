---
id: stewards-distribution-implementation-status-0001
type: implementation-status
status: gated
depends_on:
  - kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v2
  - kodhama-spec-0002-bounded-pre-agent-provisioner@v2
owner: agent
updated: 2026-07-24
---

# Distribution implementation status

## Spec 0001 landed slice

This change is an explicitly partial implementation of
`kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v2`. It
delivers the coherent metadata, install-door, legacy-transition, and
effective-support slice. It does not claim whole-spec conformance.

## Implemented

- Versioned schemas and common shape/identity validators for typed references,
  surface, catalog, provisioner-availability, clean-install, effective-facts,
  legacy-stock, and product-adoption records. Cross-record checks now bind
  provisioner acquisitions, product setup declarations, and resolved product
  adoption decisions; this is not a claim that every referenced product or
  release artifact is resolved.
- Exact six-row surface registry, fixed-commit catalog discovery, canonical
  selector fingerprints, immutable baseline/initial stock, removal-only
  transition stock, and `wave-close`: S9, S10, S23 and R15–R17, R24, R40.
- Deterministic host-catalog, availability, README, and CLAUDE generation,
  including no-write stale checking: S11 and R18–R19, R36.
- `.github/workflows/distribution-check.yml` runs `distribution/check` on
  pull requests and `main`; the gate covers executable fixtures, door
  validation, generation staleness, Python compilation, annotation coverage,
  dependency-free lint/format checks, JSON parsing, working/staged diffs, and
  the committed CI range from the event base SHA. CI checks out the exact
  Grove and Trellis adoption commits and supplies them through the explicit
  local product-repository resolver contract.
- The public release phase fails closed. Product pre-tag version
  extraction/carrier parity and exact expected-tag derivation implement the
  pre-tag subset of S1 and R1–R4 until the complete history, compatibility,
  approval, and tag engine below is implemented.
- Product-local adoption references for Grove and Trellis resolve exact
  repository/path/commit bytes, digests, and approved decision status through
  an explicit local resolver. Trellis remains bounded legacy published stock
  because adoption alone does not establish a conforming product release.
- Verified provisioner acquisitions cross-bind to exactly one matching
  verified provisioner row, and effective setup facts bind to their exact
  product requirement row, setup declaration, contract, and identity.
  Product and environment evidence bind every release-subject field their
  records expose. Successful setup factors retain canonical, deduplicated
  references to the product row, setup contract, and completion evidence.

## Remaining before whole-spec conformance

- S16, S22, R29–R30, and R39: execute and validate the complete inventory
  extractor grammar, public-contract fingerprints, support-derivative
  projection, payload/history completeness, surface change derivation, and
  approval projection/final augmentation.
- The release portion of S1/R2 plus S17, S21, R31–R32, and R38: resolve the
  expected tag only as part of the complete engine; enforce append-only
  history against every package tag, prior-tag immutability, exact SemVer
  transitions, cumulative prerelease rules, minimum compatibility bumps, and
  the product-human approval binding.
- S25 and R43–R44: resolve verified catalog product-contract and
  release-history references through v2's exact no-fetch retained-byte and
  complete-ledger contract; current validation covers typed shape and local
  identity relations only.
- S24, S27–S28, R21, R41–R42, and R46–R49: canonicalize arbitrary nested JSON,
  run each unique declared product extension identity in exact order, and use
  v2's exact argv, working directory, environment, canonical Linux/macOS
  platform detection with pre-store rejection elsewhere, explicit
  content-addressed runtime store, digest-bound immutable runtime, audited
  filesystem/network boundary, categorized runtime diagnostics,
  request/result, exit, repetition, timeout, size, and side-effect protocol.
  Every declaration continues to fail closed until that protocol is
  implemented.
- S26 and R45: validate the exact appended release-history row and preserve
  the landed two-field pre-tag and three-field release-identity results.

The historical external dependencies tracked by issue #20 remain unchanged.

## Spec 0002 status

The bounded pre-agent provisioner is not implemented in this slice.
Spec 0002 v2 scenarios S1–S32 and requirements R1–R45 remain unimplemented,
including S27/S31 and R40/R44's canonical receipt commit witness,
retained-state-only external validation, producer-obligation separation,
same-invocation partial/invalid cleanup, operator-owned uncertain or
abrupt-termination debris, and stable-path minimal-receipt replacement
contract.
