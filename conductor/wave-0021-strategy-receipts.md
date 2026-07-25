# Wave: strategy receipts for adoption posture

Opened 2026-07-25. Authority:
[`kodhama-0021-separate-adoption-posture-from-support`](../decisions/0021-separate-adoption-posture-from-support.md)
as propagated under
[`kodhama-0022-propagate-collective-strategy`](../decisions/0022-propagate-collective-strategy.md).

## Scope

Create thin cross-link ADRs in the current downstream plugin repositories
affected by decision 0021:

- Grove; and
- Trellis.

Stewards owns the upstream decision and therefore needs no downstream receipt.
Wisp is not currently a distributed plugin in the merged Stewards catalogs; it
will catch up on still-current strategy if and when it enters plugin scope.
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
- [ ] Maintainer ratification and merges recorded.
- [ ] Closure report appended; original Grove plan resumed.

## Report

Open. Both gated receipt ADRs are independently `SOUND`; neither makes a
product choice. They await the maintainer's exact ratification and merge.
