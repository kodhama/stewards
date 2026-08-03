---
id: kodhama-0028-receive-issue-taxonomy
type: decision
status: gated
depends_on: [kodhama-0009-org-topology-spirit-stewards-trees, kodhama-0022-propagate-collective-strategy, kodhama-0026-issue-taxonomy]
owner: agent
updated: 2026-08-03
---

# 0028 — receive the issue taxonomy

## Context

Stewards owns the `kodhama` plugin, so the approved
[`kodhama-0026`](https://github.com/kodhama/kodhama/blob/main/decisions/0026-issue-taxonomy.md)
issue taxonomy applies here. This receipt follows the approved
[`kodhama-0022`](0022-propagate-collective-strategy.md) propagation decision.

**Stewards is downstream of its own id namespace here.** `kodhama-0026` §Propagation
names Stewards a cross-link target *"because the upstream record is not its
own"* — the record sits at the org layer in `kodhama/kodhama`, and the
`kodhama-NNNN` namespace spans both repositories, split by the layer that owns
each decision (`kodhama-0009`). A receipt is therefore not circular: it links
one layer to another, not this repository to itself.

That also makes this the receipt where `kodhama-0022`'s wording bites hardest —
its text names *"the approved Stewards decision"* as the authority a downstream
ADR must cite, and here the authority is an org-layer record instead.
`kodhama-0026` records the gap and rules it non-blocking (its open question 2).
Recorded, not resolved.

## Decision

Stewards records receipt of the shared convention. This cross-link communicates
the upstream constraint without restating it — no dimension tables, no
vocabularies, no rationale, no README index, per `kodhama-0008` §4.

Two clauses land locally, and neither is decided here:

- **Decision 9** — *"the convention is carried by GitHub itself… A skill
  teaches agents to apply it, and that skill arrives by plugin."* Stewards
  carries that plugin today. **Which plugin carries the skill is explicitly
  not a term of `kodhama-0026`** — it is *"a delivery choice owned by the
  wave"*, and it remains open as #70.
- **Decision 11** — *"the convention binds the whole forest… The plugin does
  not."* Enablement in any repository, this one included, is that
  repository's own act under `kodhama-0021`.

## Consequences

The convention is discoverable in this repository's local decision graph
without being copied or redefined.

**No local follow-up is required by this receipt.** Stewards' 24 open issues
were migrated on 2026-08-01 and the plugin was published and enabled — all of
which are separate acts that this record neither performs nor ratifies.
`kodhama-0022` holds that *"receipt is distinct from product adoption."*

This receipt authorizes no schema, behavior, setup, package, release,
distribution, validation, or support change, and asserts no scope for the
`kodhama` plugin.

Written under `kodhama-0026` §Propagation. Status is `gated`: no maintainer
rollout direction has been given for these receipts, so approval is the
maintainer's act, not this record's.
