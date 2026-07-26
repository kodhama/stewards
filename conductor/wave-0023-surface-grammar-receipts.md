# Wave: surface-grammar receipts

Opened 2026-07-26. Authority:
[`kodhama-0023-separate-operational-availability-from-support`](../decisions/0023-separate-operational-availability-from-support.md)
as propagated under
[`kodhama-0022-propagate-collective-strategy`](../decisions/0022-propagate-collective-strategy.md).

## Scope

Create thin cross-link ADRs in the current downstream plugin repositories
affected by decision 0023:

- Grove;
- Trellis; and
- Wisp.

Stewards owns the upstream decision and therefore needs no downstream receipt.
Its active Kodhama plugin still owes separate product implementation of the
two common fields; this ledger records that follow-up without mixing it into
the communication wave. Retired Spore is not a target.

## Boundaries

- Each downstream ADR links to decisions 0023 and 0022 and states only local
  applicability or follow-up.
- No receipt repeats the shared field grammar, definitions, truth table, or
  rationale.
- No receipt authorizes code, metadata migration, package, release, setup,
  support, or adoption-posture changes.
- Grove PR #146 remains the separate product decision and resumes after this
  communication wave.
- Trellis, Wisp, and the Kodhama plugin require separate product authority
  before changing their surface metadata.

## Ledger

- [ ] Grove cross-link ADR PR opened and linked.
- [ ] Grove cross-link ADR independently reviewed and landed.
- [ ] Trellis cross-link ADR PR opened and linked.
- [ ] Trellis cross-link ADR independently reviewed and landed.
- [ ] Wisp cross-link ADR PR opened and linked.
- [ ] Wisp cross-link ADR independently reviewed and landed.
- [x] Kodhama plugin product migration recorded separately:
      [Stewards issue #42](https://github.com/kodhama/stewards/issues/42).
- [ ] Closure report appended; Grove PR #146 resumed.

## Report

Open.
