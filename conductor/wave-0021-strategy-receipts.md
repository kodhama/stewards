# Wave: strategy receipts for adoption posture

Opened 2026-07-25. Authority:
[`kodhama-0021-separate-adoption-posture-from-support`](../decisions/0021-separate-adoption-posture-from-support.md)
as propagated under
[`kodhama-0022-propagate-collective-strategy`](../decisions/0022-propagate-collective-strategy.md).

## Scope

Create thin cross-link ADRs in the current downstream plugin repositories
affected by decision 0021:

- Grove; and
- Trellis; and
- Wisp.

Stewards owns the upstream decision and therefore needs no downstream receipt.
Design System and Homebrew Tap are not plugin targets for this decision.

## Boundaries

- Each downstream ADR links to decisions 0021 and 0022 and states only local
  applicability.
- No downstream ADR summarizes the shared posture definitions.
- No receipt chooses dogfood, preview, or supported; product posture remains a
  separate local decision.
- No receipt authorizes code, packaging, release, catalog, setup, surface,
  support, or experiment work.
- Grove PR #144 remains the separate planner-dogfood decision and resumes
  after this communication wave.

## Ledger

- [x] Grove cross-link ADR PR opened and linked:
      [grove PR #145](https://github.com/kodhama/grove/pull/145).
- [x] Grove cross-link ADR independently reviewed:
      [SOUND](https://github.com/kodhama/grove/pull/145#issuecomment-5080201927).
- [x] Trellis cross-link ADR PR opened and linked:
      [trellis PR #193](https://github.com/kodhama/trellis/pull/193).
- [x] Trellis cross-link ADR independently reviewed:
      [SOUND](https://github.com/kodhama/trellis/pull/193#issuecomment-5080202446).
- [x] Wisp cross-link ADR PR opened and linked:
      [wisp PR #46](https://github.com/kodhama/wisp/pull/46).
- [x] Wisp cross-link ADR independently reviewed:
      [SOUND](https://github.com/kodhama/wisp/pull/46#issuecomment-5080223713).
- [x] Maintainer ratification and merges recorded:
      [Grove #145](https://github.com/kodhama/grove/pull/145),
      [Trellis #193](https://github.com/kodhama/trellis/pull/193), and
      [Wisp #46](https://github.com/kodhama/wisp/pull/46).
- [x] Closure report appended; original Grove plan resumed.

## Report

Closed 2026-07-25. The maintainer explicitly ratified and authorized all three
receipts. Grove merged at `eec370b`, Trellis at `431407b`, and Wisp at
`7112d26`. All were independently `SOUND`; Grove and Wisp CI passed. Trellis's
human ratification guard passed, while its non-required Claude review action
failed during model execution with no finding or comment and did not replace
the independent soundness review.

The conductor corrected its mistaken use of catalog presence as a proxy for
plugin ownership before closure. Wisp's product-owned dual-host package made
it an active target regardless of catalog presence. No receipt made a product
choice.

Catalog-admission simplification discovered during this wave is tracked
separately in [Stewards issue #39](https://github.com/kodhama/stewards/issues/39).
It does not block these communication-only receipts or authorize catalog work.

The communication detour is complete. Work resumes at Grove
[PR #144](https://github.com/kodhama/grove/pull/144), the separate
planner-dogfood product decision.
