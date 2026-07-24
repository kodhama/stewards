---
id: stewards-distribution-tests-deps
type: test-dependencies
status: gated
depends_on:
  - kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v2
  - kodhama-spec-0002-bounded-pre-agent-provisioner@v2
  - kodhama-0015-family-plugin-release-and-surface-contract
  - kodhama-0016-distribution-availability-and-effective-support
owner: agent
updated: 2026-07-24
---

# Distribution test dependencies

The `distribution/tests` package guards the landed subset of
`kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v2`.
That spec derives from approved decisions
`kodhama-0015-family-plugin-release-and-surface-contract` and
`kodhama-0016-distribution-availability-and-effective-support`.

Tests additionally name the exact spec scenario or requirement above each
test function. Existing `@v1` annotations remain accurate provenance because
v2 preserves those clauses; S24–S28 and R41–R49 remain unimplemented and are
tracked in `distribution/IMPLEMENTATION-STATUS.md`, including S28/R49's
canonical Linux/macOS platform detection and pre-store rejection of Windows
and other hosts, explicit content-addressed runtime-store resolution, and
no-live-host-state projection boundary.

No test in the landed package implements
`kodhama-spec-0002-bounded-pre-agent-provisioner@v2`. Its S1–S32 and R1–R45
remain tracked as unimplemented in `distribution/IMPLEMENTATION-STATUS.md`,
including S27/S31 and R40/R44's two-output commit and pre-commit cleanup
contract.
