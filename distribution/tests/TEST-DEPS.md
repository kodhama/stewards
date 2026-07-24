---
id: stewards-distribution-tests-deps
type: test-dependencies
status: gated
depends_on:
  - kodhama-0017-retire-family-release-certification
  - kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v2
  - kodhama-spec-0002-bounded-pre-agent-provisioner@v3
  - kodhama-0015-family-plugin-release-and-surface-contract
  - kodhama-0016-distribution-availability-and-effective-support
owner: agent
updated: 2026-07-24
---

# Distribution test dependencies

> **Temporary legacy map after
> `kodhama-0017-retire-family-release-certification` (2026-07-24).** These
> references preserve provenance for the still-running legacy tests until the
> separate implementation-removal change. The superseded specs and decisions
> are no longer implementation inputs, and this map authorizes no new
> conformance work.

The `distribution/tests` package guards
`kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v2` and
`kodhama-spec-0002-bounded-pre-agent-provisioner@v3`. Those specs derived from
the now-superseded decisions
`kodhama-0015-family-plugin-release-and-surface-contract` and
`kodhama-0016-distribution-availability-and-effective-support`.

Tests additionally name the exact spec scenario or requirement above each
test function. Existing `@v1` annotations remain accurate provenance because
v2 preserves those clauses; S24–S28 and R41–R49 remain unimplemented and are
tracked in `distribution/IMPLEMENTATION-STATUS.md`, including S28/R49's
canonical Linux/macOS platform detection and pre-store rejection of Windows
and other hosts, explicit content-addressed runtime-store resolution, and
no-live-host-state projection boundary.

The provisioner tests implement
`kodhama-spec-0002-bounded-pre-agent-provisioner@v3` and name its exact
scenario or requirement above each test function.
