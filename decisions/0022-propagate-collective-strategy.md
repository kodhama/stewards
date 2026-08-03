---
id: kodhama-0022-propagate-collective-strategy
type: decision
status: approved
superseded_in_part_by: [kodhama-0028-retire-propagation-receipts]  # 2026-08-03 — §2, §3, §5 and the §4 return path. §1 (a strategic decision names its affected repositories, inside itself) stands
depends_on: [kodhama-0008-family-inheritance-restate-nothing, kodhama/kodhama-0009-org-topology-spirit-stewards-trees, trellis/decision-0044]
informed_by: [kodhama-0021-separate-adoption-posture-from-support]
owner: agent
updated: 2026-07-25
provenance: "maintainer shaping, 2026-07-25: establish durable top-down communication from Stewards through thin, cross-linked ADRs whenever a strategic decision affects all plugins; exact hybrid-catch-up draft approved to proceed to independent soundness review; first adversary review returned NEEDS-REVISION; reference repairs landed; re-review returned SOUND; maintainer ratified the exact decision"
---

# Decision: propagate collective strategy through local cross-link ADRs

> **Forward pointer.** [`kodhama-0028`](0028-retire-propagation-receipts.md)
> (2026-08-03) retires the receipt artifact: **§2, §3 and §5 no longer apply,
> and §4's conductor return path is replaced by a cross-repo `Epic` with one
> sub-issue per affected repository.** §4 had in fact been unsatisfiable since
> `kodhama-0027` D2 forbade a brief from carrying per-item status, two days
> before this pointer was written.
>
> **§1 stands unchanged** — a strategic decision still names the repositories
> it affects, inside itself.
>
> Receipts already landed under this record (grove `adr-0040`/`adr-0042`,
> trellis `0062`/`0064`, wisp `adr-0012`/`adr-0013`) are not retracted.

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
- Immediate propagation targets current affected plugin repositories and
  repositories explicitly entering the affected plugin scope; later plugin
  entrants catch up on every still-current Stewards plugin strategy.

**Open** (0):

- None.

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

Immediate targets are repositories that own an affected plugin when the
Stewards decision is ratified plus repositories that decision explicitly
names as entering the affected plugin scope. Non-plugin steward repositories
receive no cross-link ADR merely because they might become relevant later.

When a repository later enters plugin scope, its entry decision inventories
the still-current Stewards strategic decisions that affect its plugin. Any
missing cross-link ADRs land as part of that entry work. Superseded strategy
requires no retrospective receipt.

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
  declares its current and explicitly entering propagation targets.
- **AC2:** Every target receives a thin local ADR linking to the Stewards
  authority and stating only local applicability and follow-up.
- **AC3:** A later plugin entrant inventories still-current Stewards plugin
  strategy and adds any missing cross-link ADRs during entry.
- **AC4:** Shared strategy is not summarized, copied, or redefined downstream.
- **AC5:** Product adoption, implementation, release, support, and posture
  decisions remain separate and product-owned.
- **AC6:** A conductor brief provides the downstream link ledger and closure
  report.
- **AC7:** No propagation schema, bot, CI gate, or certification machinery is
  introduced.
- **AC8:** Decision 0021 is the first application; Grove's planner dogfood ADR
  remains a separate product decision.

## Self-check

The decision creates a communication edge rather than a second policy home.
It narrows decision 0008 only enough to permit receipt records, preserves the
no-restatement rule, uses the settled qualified-link grammar, and keeps the
conductor in its existing ledger role.

## Lifecycle record

On 2026-07-25 the maintainer confirmed that the exact hybrid-catch-up draft
captured the intended communication model and approved proceeding to
independent soundness review. The first review returned `NEEDS-REVISION` on
two reference-bookkeeping defects; after repair, fresh re-review returned
`SOUND`. The maintainer then ratified the exact decision; the `approved`
status records that human intent act.
