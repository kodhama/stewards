---
id: kodhama-0012-codex-marketplace-channel
type: decision
status: approved  # ratified by maintainer merge of PR #9 on 2026-07-24; this records the human-owned ship act named below
depends_on: [kodhama-0002-delivery-channels]
owner: agent
updated: 2026-07-24
provenance: maintainer approval on 2026-07-23 to implement Grove distribution for both Claude Code and Codex; maintainer merge of PR #9 on 2026-07-24 performed the final ship act
---

# Decision: the install door gains a native Codex catalog

## Decision

`kodhama/stewards` remains the one canonical install repository and the
marketplace name remains `kodhama`. It carries one host-native catalog
manifest for each supported plugin host:

- `.claude-plugin/marketplace.json` is the Claude Code catalog;
- `.agents/plugins/marketplace.json` is the Codex catalog.

The Codex catalog initially lists only Grove. A steward joins that catalog
only after its own package has a valid Codex manifest and a supported Codex
surface; Claude availability does not imply Codex support. Product code,
role contracts, and release cadence remain in the product repositories.
The catalogs contain only discovery metadata and source pointers.

For Grove, the Codex source is the same `plugins/grove` subdirectory used by
Claude distribution. Grove's package owns host manifests and release
validation; stewards owns only the catalog pointer.

## Why

The standing “one org marketplace” decision chose a thin canonical install
door, not a Claude-only architecture. Codex has a native marketplace
manifest and can install Grove's Codex package from the same product source.
Adding that host projection preserves one install repository without
pretending the two hosts share a manifest schema or support matrix.

Listing only proven products avoids turning an existing Claude entry into an
unsupported Codex claim.

## Acceptance criteria

- A clean Codex installation can add `kodhama/stewards`, discover
  `grove@kodhama`, and resolve its `plugins/grove` source.
- The Claude marketplace remains functionally unchanged except for correcting
  stale Grove discovery metadata.
- Both catalogs are named `kodhama`; neither contains product code or role
  contracts.
- A product without a validated Codex package is absent from the Codex
  catalog.

## Gate

The maintainer approved implementation on 2026-07-23. This decision remains
`gated`; merging its change request is the human-owned ship act.

## Lifecycle record

The maintainer merged PR #9 on 2026-07-24. That merge performed the
human-owned ship act specified above; the `approved` frontmatter records it.

## Forward annotation — kodhama-0016 (2026-07-24)

Approved `kodhama-0016-distribution-availability-and-effective-support`
supersedes only this decision's rule that catalog admission requires an
already supported product surface. A valid package may be published for
staged testing while product support remains candidate, unsupported, or
absent; catalog presence still creates no behavioral or effective-support
claim. The one-repository, host-native, thin-catalog, and product-owned
package boundaries stand.

## Forward annotation — kodhama-0017 (2026-07-24)

Gated `kodhama-0017-retire-family-release-certification` supersedes
`kodhama-0016` in full. Its staged-testing admission exception and its
availability/effective-support model are therefore retired; this decision's
catalog-admission and thin-catalog boundaries stand again. The narrow
marketplace-tested metadata authorized by `kodhama-0017` records which
marketplace a test exercised and creates no admission or support exception.
