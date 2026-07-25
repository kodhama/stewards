---
id: kodhama-0022-propagate-collective-strategy
type: decision
status: draft
depends_on: [kodhama-0008-family-inheritance-restate-nothing, kodhama-0009-org-topology-spirit-stewards-trees, trellis/decision-0044]
informed_by: [kodhama-0021-separate-adoption-posture-from-support]
owner: agent
updated: 2026-07-25
provenance: "maintainer shaping, 2026-07-25: establish durable top-down communication from Stewards through thin, cross-linked ADRs whenever a strategic decision affects all plugins"
---

# Decision: propagate collective strategy through local cross-link ADRs

## Decision state

**Decided** (maintainer shaping, 2026-07-25):

- A Stewards strategic decision that affects all plugins must be propagated to
  every applicable plugin repository.
- Each target receives a thin, decision-corpus-native cross-link ADR.
- The local ADR points to the Stewards authority and records only local
  applicability or follow-up; it does not summarize shared strategy.
- A conductor brief owns the target list, downstream links, progress ledger,
  and closure report.
- Receipt is distinct from product adoption, implementation authorization,
  release, support, or posture choices.
- Decision `kodhama-0021` is the first application of this model.

**Open** (1):

- Does “applicable plugin repository” mean only repositories that currently
  own or are explicitly entering the affected plugin scope, or every steward
  repository even when it has no plugin applicability?

**Parked** (3):

- Machine-readable propagation metadata, automation, and enforcement; the
  first use establishes the human-readable convention.
- Communication rules for strategic decisions that affect only one product;
  ordinary product ownership already covers them.
- Any implementation, release, support, or posture work discovered through a
  cross-link; each belongs to its own product decision.

## Context

Stewards is the home for cross-collective decisions, while product truths
remain product-owned. A collective strategy can therefore become
authoritative without appearing in an affected plugin's local decision graph
until unrelated work happens to encounter it.

Decision `kodhama-0021` exposed that delay. Grove's separate planner-dogfood
ADR is useful, but it chooses a product posture. It is not the general
communication record.

Decision `kodhama-0008` correctly retired hand-authored copies of shared
principles and operating mechanics because they drift. A cross-link ADR is not
another copy: it records one durable edge to the Stewards source of truth and
only the local consequence of receiving it.

## Decision

### 1. Collective-wide plugin strategy declares its targets

Every new Stewards decision whose strategy explicitly affects all Kodhama
plugins includes a short propagation section naming its applicable plugin
repositories from the canonical topology.

The Stewards decision may merge once independently sound and ratified.
Propagation follows as communication work; downstream copies are never needed
to make the upstream decision authoritative.

### 2. The downstream artifact is deliberately thin

Each target repository receives one local cross-link ADR containing only:

- frontmatter with a qualified dependency on the approved Stewards decision;
- a direct link to that decision;
- one short statement of local applicability or non-applicability;
- any local follow-up named as required, optional, or parked; and
- an explicit statement that the Stewards decision remains authoritative.

The ADR does not repeat definitions, rationale, acceptance criteria, or shared
obligations. Local corpus rules may require headings or lifecycle notes, but
they should remain minimal.

### 3. Receipt does not make a product decision

A cross-link ADR does not by itself adopt or configure a plugin, authorize
implementation, resolve a local conflict, change a package or release, make a
support claim, select an adoption posture, or certify compliance.

When a real product choice is needed, it remains a separate local decision.
The cross-link and product decision may share a PR if their distinct purposes
stay explicit.

### 4. The conductor provides the return path

One Stewards conductor brief lists the targets and links each local PR and
landed ADR. This produces bidirectional navigation without repeatedly editing
an approved Stewards decision:

- each local ADR links upward to the Stewards authority; and
- the conductor ledger links downward to every local ADR.

The conductor closes only after every target is linked or explicitly recorded
as not applicable. It owns progress, not policy.

### 5. Narrow exception to “restate nothing”

This partially supersedes only decision `kodhama-0008`'s implication that no
hand-authored per-repository record may acknowledge collective operating
strategy. Thin, reference-only cross-link ADRs are required here.

Decision 0008's substantive rule remains current: repositories do not copy or
redefine shared principles, operating mechanics, or canonical terminology.
Those continue to arrive from their authoritative home.

## Alternatives considered

- **Conductor ledger only:** useful for central tracking, but leaves no durable
  edge in the affected repository's own decision graph.
- **README, issue, or PR notice:** easy to publish, but mutable or easy to
  lose and not part of the local append-only decision record.
- **Plugin-delivered notice:** useful as a future discovery aid, but receipt
  would depend on installation and version timing and would not state local
  applicability.
- **Copied local summary:** locally readable, but recreates the drift problem
  decision 0008 retired.

## Consequences

- Collective strategy becomes locally discoverable soon after ratification.
- The added ADRs stay small because they carry links and local impact, not
  duplicate policy.
- Product autonomy remains explicit: communication never silently becomes
  implementation or support.
- Each collective-wide plugin strategy adds one bounded documentation wave.

## Acceptance criteria

- **AC1:** Every future Stewards strategic decision affecting all plugins
  declares its propagation targets.
- **AC2:** Every target receives a thin local ADR linking to the Stewards
  authority and stating only local applicability and follow-up.
- **AC3:** Shared strategy is not summarized, copied, or redefined downstream.
- **AC4:** Product adoption, implementation, release, support, and posture
  decisions remain separate and product-owned.
- **AC5:** A conductor brief provides the downstream link ledger and closure
  report.
- **AC6:** No propagation schema, bot, CI gate, or certification machinery is
  introduced.
- **AC7:** Decision 0021 is the first application; Grove's planner dogfood ADR
  remains a separate product decision.

## Self-check

The decision creates a communication edge rather than a second policy home.
It narrows decision 0008 only enough to permit receipt records, preserves the
no-restatement rule, uses the settled qualified-link grammar, and keeps the
conductor in its existing ledger role.
