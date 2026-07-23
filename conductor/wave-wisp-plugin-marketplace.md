# Wave: Wisp plugin + marketplace channel

Opened 2026-07-23. Authorization: maintainer — all kodhama utilities should
distribute through the common marketplace in `kodhama/stewards`; “Do it all”
while keeping dual Claude / Codex distribution. Follow-up direction permits
amending specs or superseding decisions and discarding legacy that does not
help, with **minimal user friction** as the objective.

This wave executes `kodhama-0012-wisp-plugin-channel`. It is a coordinated
two-repo rollout, not a shared implementation: Wisp owns the complete plugin
payload and runtime; Stewards owns only the catalog pointer, collective
decision, and this ledger.

Product contract:
[Wisp ADR-0002](https://github.com/kodhama/wisp/blob/main/decisions/adr-0002-plugin-mcp-distribution.md) ·
[Wisp SPEC-0001 v4](https://github.com/kodhama/wisp/blob/main/specs/spec-0001-plugin-mcp-distribution.md).

## Lanes and gates

### Wisp lane — product payload

- Draft product PR: [kodhama/wisp#23](https://github.com/kodhama/wisp/pull/23).
- Build `plugins/wisp/` in `kodhama/wisp`.
- Carry dual Claude and Codex manifests/configuration in the same product-owned
  payload.
- Ship a self-contained runtime with a built-in stdio MCP server; installation
  and session startup must not fetch dependencies.
- Keep the install user-scoped and runtime processes session-scoped /
  project-bound; do not introduce a machine daemon or global Wisp instance.
- Pass Wisp's decision/spec, implementation, independent conformance,
  independent code-quality, and triggered validation gates.
- Exercise clean bundle and host-specific configuration checks before the
  product lane is declared ready.

### Stewards lane — install door

- Add append-only `kodhama-0012-wisp-plugin-channel`.
- Add exactly one `git-subdir` Wisp pointer to the canonical
  `.claude-plugin/marketplace.json`.
- Preserve causal catalog order: `trellis · grove · wisp · spore`.
- Validate manifest syntax, pointer shape, link/order consistency, and diff
  hygiene.
- Run clean marketplace/install smokes only after the Wisp payload is reachable
  on its default branch.

The lanes have independent gates. Marketplace JSON validity does not attest to
Wisp runtime behavior; Wisp unit/build checks do not attest that the live
catalog can install it.

## Merge order

1. **Wisp first.** Merge the product payload and confirm
   `kodhama/wisp`'s default branch contains `plugins/wisp/`.
2. **Stewards second.** Re-verify the live subdirectory, then merge this
   decision, ledger, and catalog pointer.

Reversing the order would publish a broken marketplace target and is not
allowed.

## Ledger

- [x] Wisp decision/spec gates passed
- [x] Wisp implementation and self-contained bundle completed
- [x] Wisp independent conformance review passed
- [x] Wisp independent code-quality review passed
- [x] Wisp triggered validation passed after propagation remediation
- [x] Claude plugin manifest/config validated
- [x] Codex plugin manifest/config validated
- [ ] Clean Claude host install/tool-discovery smoke passed
- [ ] Clean Codex host install/tool-discovery smoke passed
- [ ] Wisp payload merged to its default branch
- [x] Stewards decision authored at `gated`
- [x] Stewards marketplace entry authored
- [x] Catalog JSON/order/link and diff-hygiene checks passed locally
- [ ] Live `kodhama/wisp` → `plugins/wisp` pointer re-verified after Wisp merge
- [ ] Clean marketplace install smoke passed
- [ ] Stewards change reviewed and merged
- [ ] Report closed with final links and outcomes

## Parked

- None. Any host/install failure discovered by the pending smokes returns to
  the owning lane rather than being waived in this ledger.

## Report (pending)

The Stewards slice is prepared on a draft branch: decision, conductor ledger,
and catalog entry. [Wisp PR #23](https://github.com/kodhama/wisp/pull/23)
carries the product payload. Its product tests, build, independent reviews,
and both manifest validators pass. Claude Code 2.1.199 loaded the local plugin
skill and connected its stdio MCP server, but the account spend limit blocked
a real tool invocation; that is partial evidence, not a completed host smoke.

**This wave is not ready to merge yet.** The Wisp default-branch pointer and
clean Claude/Codex install plus tool-discovery/invocation smokes remain
pending. No completed install or host smoke is claimed by this report.
