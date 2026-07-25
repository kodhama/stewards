---
id: kodhama-0022-propagate-collective-strategy
type: decision
status: draft
depends_on: [kodhama-0008-family-inheritance-restate-nothing, kodhama-0009-org-topology-spirit-stewards-trees, trellis/decision-0044]
informed_by: [kodhama-0021-separate-adoption-posture-from-support]
owner: agent
updated: 2026-07-25
provenance: "maintainer shaping, 2026-07-25: establish durable top-down communication from Stewards through short, cross-linked memo ADRs whenever a strategic decision affects all plugins"
---

# Decision: propagate collective strategy through local receipt memos

## Decision state

**Decided** (maintainer shaping, 2026-07-25):

- A Stewards strategic decision that affects all plugins must be propagated to
  every applicable plugin repository.
- Each target receives a short, decision-corpus-native strategy receipt memo
  with a qualified cross-link to the Stewards decision.
- The memo records receipt and local applicability; Stewards remains the sole
  authority for the shared strategy.
- A conductor brief owns the target list, downstream links, progress ledger,
  and closure report.
- Receipt is distinct from product adoption, implementation authorization,
  release, support, or posture choices.

**Open** (1):

- Does “applicable plugin repository” mean only repositories that currently
  own or are explicitly entering the affected plugin scope, or every steward
  repository even when it has no plugin applicability?

**Parked** (3):

- Machine-readable propagation metadata, automation, and enforcement; the
  first use establishes the human-readable convention.
- Communication rules for strategic decisions that affect only one product;
  ordinary product ownership already covers them.
- Any implementation, release, support, or posture work discovered by a
  receipt memo; each belongs to its own product decision.

## Context

Stewards is the home for cross-collective decisions, while product truths
remain product-owned. A strategic decision can therefore become authoritative
at the collective layer without becoming visible in each affected product's
local decision graph until unrelated work happens to encounter it.

The adoption-posture decision, `kodhama-0021`, exposed that delay. Grove's
product-owned dogfood decision is useful, but it serves a different purpose:
it chooses Grove's local posture rather than recording the general route by
which collective strategy reaches every affected plugin repository.

Decision `kodhama-0008` correctly retired hand-authored copies of shared
principles and operating mechanics because they drift. A receipt memo is not
another copy. It is a local, durable edge to the single Stewards authority,
plus the smallest statement of what that authority means—or does not mean—in
that repository.

## Decision

### 1. Collective-wide plugin strategy declares its propagation

Every new Stewards decision whose strategy explicitly affects all Kodhama
plugins includes a short propagation section that identifies the applicable
plugin repositories from the canonical topology and states that local receipt
memos are required.

The Stewards decision may merge once it is independently sound and ratified.
Its propagation is a follow-on communication wave, not a requirement to copy
the decision into every repository before it can become authoritative.

### 2. Each target receives one short strategy receipt memo

The memo is a normal local decision artifact and contains only:

- a qualified relation and link to the approved Stewards decision;
- one sentence recording that the repository received and is subject to the
  strategy;
- the exact local applicability or non-applicability boundary; and
- any product-owned follow-up, explicitly marked as required, optional, or
  parked.

It imports rather than repeats the shared strategy. Readers follow the link
for definitions, rationale, and collective obligations.

### 3. Receipt does not make a product decision

A receipt memo does not by itself:

- adopt or configure a plugin;
- authorize implementation;
- change a package, release, catalog, support claim, or adoption posture;
- resolve a conflict with an approved local decision; or
- certify compliance.

If the strategy requires a real product choice, that choice is recorded in a
separate local decision. The receipt and product decision may share a PR when
their distinction remains explicit, but neither substitutes for the other.

### 4. The conductor provides the return path

One Stewards conductor brief lists the target repositories and links each
receipt PR and final local artifact. It is the progress ledger and closure
report; the approved strategic decision remains the policy authority.

This produces bidirectional navigation without editing the approved Stewards
decision after every downstream PR:

- each receipt links upward to the Stewards decision; and
- the conductor ledger links downward to every receipt.

The first application is decision `kodhama-0021`. Grove's dogfood decision is
tracked separately because it records a product posture, not merely receipt of
the collective strategy.

### 5. Narrow exception to “restate nothing”

This partially supersedes only decision `kodhama-0008`'s implication that no
hand-authored per-repository record may acknowledge collective operating
strategy. A reference-only strategy receipt is required under this decision.

Decision 0008's substantive rule remains current: repositories do not copy or
redefine shared principles, operating mechanics, or canonical terminology.
Those continue to arrive from their authoritative home.

## Consequences

- Collective strategy becomes discoverable from every affected plugin's local
  decision graph soon after ratification.
- The local memo remains small because it records receipt and impact, not a
  duplicate policy.
- Product autonomy remains visible: communication never silently becomes
  implementation or support.
- Each collective-wide strategy adds a bounded documentation wave and one
  small PR per applicable plugin repository.

## Acceptance criteria

- **AC1:** Every future Stewards strategic decision that affects all plugins
  declares its applicable propagation targets.
- **AC2:** Every target receives a short local receipt memo with a qualified
  link to the Stewards authority and an explicit local impact boundary.
- **AC3:** Shared strategy is not copied or redefined downstream.
- **AC4:** Product adoption, implementation, release, support, and posture
  decisions remain separate and product-owned.
- **AC5:** A conductor brief provides the downstream link ledger and closure
  report.
- **AC6:** No propagation schema, bot, CI gate, or certification machinery is
  introduced.
- **AC7:** Decision 0021 is the first application, while Grove's planner
  dogfood decision remains a separate product decision.

## Self-check

The decision establishes a communication path rather than a second policy
home. It reconciles the new receipt convention with decision 0008 by
superseding only the no-hand-authored-record implication and preserving the
no-restatement rule. Qualified cross-repository relations already have a
settled grammar, and the conductor retains its existing ledger role.
