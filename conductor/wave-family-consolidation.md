# Wave: family consolidation

Opened 2026-07-26. Evidence:
[`discovery-family-audit-2026-07`](../research/family-audit-2026-07.md).

## Scope

Act on the July 2026 audit in reviewable slices: fix what is broken first, then remove
what is genuinely dead, then cut recurring ceremony. Each slice lands as its own PRs and
is reviewed before the next opens.

The full working plan lives outside the repo with the maintainer; this brief is the
ledger and the closure report. **Boundaries:** no math-quest product work, no decision is
ratified by an agent, and nothing is removed without a trace of what governs it.

## Slice 1 — correctness · CLOSED 2026-07-26

- [x] grove [#155](https://github.com/kodhama/grove/pull/155) — `/grove:setup` resolved
      its own package root one directory short and died before any surface rule ran.
      One-hop fix plus a regression test that drives the CLI from both a source checkout
      and an installed copy at a path containing a space.
- [x] Committed plugin enablement so a fresh clone has a fleet — stewards
      [#44](https://github.com/kodhama/stewards/pull/44), kodhama
      [#54](https://github.com/kodhama/kodhama/pull/54), design-system
      [#20](https://github.com/kodhama/design-system/pull/20), wisp
      [#51](https://github.com/kodhama/wisp/pull/51), trellis
      [#196](https://github.com/kodhama/trellis/pull/196), math-quest
      [#363](https://github.com/kodhama/math-quest/pull/363).
- [x] 111 debris branches deleted across six repos; `trellis/research/0013` preserved as
      closed-unmerged work.
- [x] Trellis's PR-review workflow, red for seven consecutive runs, recovered on its own.
      Cause unaddressed.

## Slice 2 — dead weight · WITHDRAWN 2026-07-27

- [x] Withdrawn without changes. Three of the proposed removals were refuted on contact:
      two by `grove/adr-0036` D3, which retains the specs deliberately, and one by the
      lifecycle rule that `superseded` is terminal. Recorded in the audit artifact.

## Slice 3 — the marketplace canary · OPEN

- [x] Mechanism archived, loadable, at
      [`wisp@archive/codex-marketplace-canary`](https://github.com/kodhama/wisp/tree/archive/codex-marketplace-canary).
- [x] [#45](https://github.com/kodhama/stewards/issues/45) — family marketplace check,
      keyless asset half, inside current Stewards scope.
- [x] [#47](https://github.com/kodhama/stewards/issues/47) — live-session ping; needs
      `kodhama-0017` widened. **Deferred by the maintainer, not blocked.**
- [ ] `wisp/adr-0018` — second draft, in independent review. First returned `UNSOUND`.
- [ ] Implementation, gated on that decision reaching `approved`.

## Parked

- [#46](https://github.com/kodhama/stewards/issues/46) — compacting the decision and spec
  corpora. A rule change, not maintenance; needs its own shaping.
- The stewards/kodhama thin-vendor migration. Their vendored charters carry config tokens
  resolved in prose and neither repo has a `.grove/config.toml` to hold them.

## Stop-and-learn checkpoint

Slice 1 landed clean. Slice 2 did not survive first contact, and the reason generalises:
**removals were proposed from names and line counts rather than from a trace of what runs
and what governs it.** Three of ten items withdrew; a fourth changed direction twice.

Two near-misses were caught by verification rather than by reading — nine repo-owned
`.grove/agents/` addenda staged for deletion as if they were stale charter copies, and a
closed-unmerged research branch that a debris sweep would have destroyed.

**The corrective is in the audit artifact and is already binding**: trace first, report
the trace, and where it contradicts a ratified decision, supersede openly. The cost is
visible — `wisp/adr-0018` has taken two drafts and two adversary passes for one workflow
removal. That is the correct price and it should not be optimised away.
