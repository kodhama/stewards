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

- [x] Grove cross-link ADR PR opened and linked:
      [Grove PR #147](https://github.com/kodhama/grove/pull/147).
- [x] Grove cross-link ADR independently reviewed and landed:
      [SOUND](https://github.com/kodhama/grove/pull/147#issuecomment-5082269216),
      merge `a8f18a5`.
- [x] Trellis cross-link ADR PR opened and linked:
      [Trellis PR #195](https://github.com/kodhama/trellis/pull/195).
- [x] Trellis cross-link ADR independently reviewed and landed:
      [SOUND](https://github.com/kodhama/trellis/pull/195#pullrequestreview-4781086284),
      merge `9995337`.
- [x] Wisp cross-link ADR PR opened and linked:
      [Wisp PR #47](https://github.com/kodhama/wisp/pull/47).
- [x] Wisp cross-link ADR independently reviewed and landed:
      [SOUND](https://github.com/kodhama/wisp/pull/47#issuecomment-5082266778),
      merge `ad8730b`.
- [x] Kodhama plugin product migration recorded separately:
      [Stewards issue #42](https://github.com/kodhama/stewards/issues/42).
- [x] Closure report appended; Grove PR #146 resumed.

## Report

Closed 2026-07-26. The maintainer ratified decision 0023 and directed the
receipt rollout. Grove merged at `a8f18a5`, Trellis at `9995337`, and Wisp at
`ad8730b`. Every receipt was independently `SOUND` and remained a thin
cross-link with product implementation explicitly separate.

Grove and Wisp required checks passed. Trellis's ratification guard passed;
its optional Claude Code Review workflow failed without producing a review
comment and did not replace or invalidate the separately persisted independent
soundness review.

The same-repository Kodhama plugin needs no receipt. Its product migration is
tracked in [Stewards issue #42](https://github.com/kodhama/stewards/issues/42).
Retired Spore was excluded as directed by decision 0023.

The communication wave is complete. Product work resumes at Grove
[PR #146](https://github.com/kodhama/grove/pull/146), which owns the planner
dogfood setup behavior.
