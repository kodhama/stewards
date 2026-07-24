---
id: stewards-distribution-implementation-status-0001
type: implementation-status
status: gated
depends_on: [kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v1]
owner: agent
updated: 2026-07-24
---

# Spec 0001 implementation status

This change is an explicitly partial implementation of
`kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v1`. It
delivers the coherent metadata, install-door, legacy-transition, and
effective-support slice. It does not claim whole-spec conformance.

## Implemented

- Versioned schemas and common validators for identity, typed references,
  surface, catalog, provisioner-availability, clean-install, effective-facts,
  legacy-stock, and product-adoption records: S2–S8, S12–S15, S18–S20 and
  R1–R14, R20, R23, R25–R28, R33–R37.
- Exact six-row surface registry, fixed-commit catalog discovery, canonical
  selector fingerprints, immutable baseline/initial stock, removal-only
  transition stock, and `wave-close`: S9, S10, S23 and R15–R17, R24, R40.
- Deterministic host-catalog, availability, README, and CLAUDE generation,
  including no-write stale checking: S11 and R18–R19, R36.
- Product pre-tag version extraction/carrier parity and exact expected-tag
  derivation, plus release-phase peeling of only the computed Git ref: the
  release-identity subset of S1 and R1–R4.
- Product-local adoption references for Grove and Trellis. Trellis remains
  bounded legacy published stock because adoption alone does not establish a
  conforming product release.

## Remaining before whole-spec conformance

- S16, S22, R29–R30, and R39: execute and validate the complete inventory
  extractor grammar, public-contract fingerprints, support-derivative
  projection, payload/history completeness, surface change derivation, and
  approval projection/final augmentation.
- S17, S21, R31–R32, and R38: enforce append-only history against every
  repository package tag, prior-tag immutability, exact SemVer transition and
  cumulative prerelease rules, minimum compatibility bumps, and the
  product-human approval binding.
- R21: run a declared product extension validator. Spec 0001 defines only its
  path; it does not define argv, working directory, environment/network
  boundary, input/output, or exit contract. That protocol requires an
  upstream spec revision before safe execution.

The historical external dependencies tracked by issue #20 remain unchanged.
