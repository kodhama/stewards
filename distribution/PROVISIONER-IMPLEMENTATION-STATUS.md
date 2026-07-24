---
id: stewards-provisioner-implementation-status-0001
type: implementation-status
status: gated
depends_on:
  - kodhama-spec-0002-bounded-pre-agent-provisioner@v1
  - kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v1
owner: agent
updated: 2026-07-24
---

# Spec 0002 implementation status

This is a bounded implementation of the protocol surface that can be truthful
with the current merged metadata. `distribution/provisioners.json` contains no
candidate or verified records, so this change creates no host mutation route
and makes no installation, idempotency, preservation, or promotion claim.
**No whole-spec conformance is claimed.**

## Implemented

- The six checked-in request, receipt, retained-state, write-audit,
  entrypoint, and evidence-bundle JSON Schema documents; tests validate every
  current provisioner fixture and emitted receipt/audit document against its
  complete schema.
- The request cases exercised by retained fixtures: exact-version rejection,
  surface/root/reference checks, complete-key route lookup, and global
  unused-reference precedence.
- Descriptor-relative no-follow/exclusive creation, same-descriptor read-back
  hashing, partial-file cleanup, physically disjoint output checks, typed
  output-failure receipts, and distinct audit/receipt sealing failures.
- Claude Code and Codex reach the same core and fail at identity resolution
  with `route-not-found` while the availability source has no route.
- Thin CI and cloud/container entrypoints delegate to the core and contain no
  host, product, setup, or launch logic.
- Offline fail-closed fixtures and CI tests for both hosts, exact-version
  rejection, global validation precedence, output evidence binding, and
  preservation of untouched state roots.
- The retained-evidence authority exists as an empty index; it cites no bundle
  and therefore makes no route-promotion claim.

## Deliberately unavailable

- Host catalog registration, acquisition, package installation, state
  mutation, and host discovery adapters.
- Shared prerequisite execution, selected convergence, rollback, process-tree
  write monitoring during mutation, and successful receipt variants.
- Unexercised request-attribution combinations outside the retained fixture
  set; the implemented cases are not a claim of complete six-phase coverage.
- Clean two-run promotion harnesses and immutable route evidence bundles.

Those behaviors require an exact candidate or verified provisioner record and
its adapter path. Adding them without such a record would fabricate
availability contrary to specs 0001 and 0002.

## Explicit implementation choices

The spec requires an executing SemVer but does not name its source path or
initial value. This slice records `0.1.0` in `distribution/PROVISIONER_VERSION`
and embeds the same value in the core.

The sealing rules require the normal receipt to bind the audit path and
read-back digest, while the receipt-envelope list omits field names and the
minimal-output variant explicitly forbids an audit reference/digest. This
slice uses top-level `write_events_reference` and `write_events_sha256`, the
same names used by tuple verification, and keeps them forbidden on a minimal
output-failure receipt.
