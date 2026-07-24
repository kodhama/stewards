---
id: kodhama-spec-0002-bounded-pre-agent-provisioner
type: spec
status: gated  # v2 author self-check passed; independent v2 review/ratification remains due
version: 2
depends_on: [kodhama-0016-distribution-availability-and-effective-support, kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v2]
implements: [kodhama-0016-distribution-availability-and-effective-support]
owner: agent
updated: 2026-07-24
---

# Bounded pre-agent provisioner

> **Amended 2026-07-24 — two-output commit and bounded cleanup.**
> **WHAT:** Defined committed evidence solely from retained regular-file
> paths, canonical bytes, schemas, and normal-receipt audit binding; separated
> that external predicate from producer create/fsync/read-back obligations;
> and limited same-invocation cleanup to demonstrably partial or invalid
> uncommitted leaves.
> **WHY:** v1 defined sealing order and failure receipts but did not distinguish
> a sealed audit from externally committed evidence, while its blanket
> no-delete rule left handled-failure cleanup and abrupt-termination debris
> underdetermined. The first v2 wording then made commitment depend on
> historical producer operations that an external validator cannot observe.
> **SCOPE:** Output identity, successful sealing, failure recovery, fixtures,
> S27/S31, and R40/R44; all other v1 behavior and ownership boundaries remain
> current.
> **POINTER:** `distribution/IMPLEMENTATION-STATUS.md` at
> `fe95bb93e59e4e24faaabe5ddfe1a6c8e8b9215c`; implementation-readiness review
> of `kodhama-spec-0002-bounded-pre-agent-provisioner@v1` and spec-adversary
> `NEEDS-REVISION` on `07555da` and `9a14d10`.
> **VALUE:** Maintainers can distinguish trustworthy committed evidence from
> handled-failure cleanup and operator-owned crash debris without risking
> caller-owned files.
> **CONFIDENCE:** verified.

## Scope

This spec defines one Stewards-owned provisioning interface for explicitly
selected Claude Code and Codex plugin releases before local, headless CI, or
cloud/container agent launch.

It registers the applicable host catalog, acquires and installs exact releases,
converges selected state idempotently, preserves unselected state, and emits
distribution evidence. It does not start an agent, select plugins for the
consumer, assert product behavior, run product setup/refresh, copy product
content, or coordinate releases.

## Authority paths

All paths are relative to the Stewards repository root.

| Path | Contract |
|---|---|
| `distribution/schemas/provision-request.v1.schema.json` | Request and environment grammar |
| `distribution/schemas/provision-receipt.v1.schema.json` | Conditional receipt/result/diagnostic grammar |
| `distribution/schemas/provision-evidence-bundle.v1.schema.json` | Retained two-run evidence grammar |
| `distribution/schemas/provision-state.v1.schema.json` | Canonical observable-state document and digest authority |
| `distribution/schemas/provision-write-events.v1.schema.json` | Provisioner process-tree write observation and classification authority |
| `distribution/schemas/provision-entrypoints.v1.schema.json` | Declared/discovered launch-entrypoint set authority |
| `distribution/provision` | Host-neutral core entrypoint |
| `distribution/adapters/ci-pre-agent` | Thin headless-CI adapter |
| `distribution/adapters/cloud-container-setup` | Thin cloud/container adapter |
| `distribution/evidence/provisioner/index.json` | Evidence-bundle index and digests |
| `distribution/evidence/provisioner/<route_id>/<surface_id>/<plugin_id>/<package_version>/<provisioner_version>/` | Immutable exact-route bundle |
| `distribution/fixtures/provisioner/` | Offline host doubles, requests, receipts, state snapshots, and failures |
| `distribution/provisioners.json` | Availability source governed by spec 0001 |

Thin adapters may translate environment-owned references into a request. They
shall call `distribution/provision` and contain no product-specific install,
setup, or behavior logic.

## Invocation

```
distribution/provision --request <path> --receipt <path> --write-events <path>
```

The command writes one receipt and one canonical process-tree write audit to
the two explicit paths and bounded human-readable diagnostics to standard
error. The two output paths shall be distinct, absolute, normalized, and
outside every host state root, and neither leaf may already exist. It exits
before Claude Code, Codex, or product setup is started.

## Request grammar

### Envelope and uniqueness

| Field | Exact contract |
|---|---|
| `schema_version` | Integer `1` |
| `request_id` | Lowercase RFC 4122 UUID v4 |
| `provisioner_version` | Exact SemVer |
| `targets` | Non-empty list, unique by `(host, surface_id)` |
| `environment` | Typed state roots and references |

The UUID full-match is
`^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`.

Each target contains:

| Field | Exact contract |
|---|---|
| `host` | `claude-code` or `codex` |
| `surface_id` | Active registered surface whose host equals `host` |
| `environment_ref_ids` | Duplicate-free references used by this target |
| `plugins` | Non-empty list unique by `plugin_id` |

Each plugin selection contains exactly `plugin_id`, `package_version`, and
`route_id`. Versions are exact SemVer; ranges, `latest`, branches, tags, and
mutable refs are invalid. `route_id` uses the common identity grammar and shall
select exactly one candidate or verified record whose complete
`(route_id, surface_id, plugin_id, package_version)` key matches. Missing,
unavailable, zero-match, and multiple-match selection fail before mutation.
The record's `provisioner_version` shall equal the request
`provisioner_version`, which shall also equal the executing core's embedded
SemVer. A key match with a different provisioner version is ineligible, not a
fallback.

Route lookup occurs at the `identity-resolution` boundary after request
validation phases 1–4 and before phases 5–6 and tag/commit resolution. It
groups records by the requested complete key and applies this precedence:

| Records at requested key | Result |
|---|---|
| More than one row | resolution failure / `route-ambiguous` |
| Exactly one `unavailable` row | resolution failure / `route-unavailable` |
| Exactly one candidate/verified row whose provisioner version differs | resolution failure / `route-version-mismatch` |
| No row | resolution failure / `route-not-found` |
| Exactly one candidate/verified row with equal version | continue identity resolution |

Each failure uses the resolution-failure receipt variant, forbids resolved
identity/route/adapter/later fields, and is exit class `3` when no tuple
succeeds. If other tuples succeed, aggregate outcome is partial failure `6`.
No route case is reported as request validation or prerequisite failure.
The same plugin may appear once per target and may intentionally use different
exact versions or routes on different hosts.

### Environment

`environment` contains:

| Field | Exact contract |
|---|---|
| `state_roots` | Exactly one row per distinct targeted host, unique by host |
| `references` | Duplicate-free typed non-secret references |

A state-root row contains `host` and `path`. A reference contains
`reference_id`, `kind`, and `locator`:

| `kind` | `locator` grammar |
|---|---|
| `authentication-env` | Environment variable name `^[A-Z_][A-Z0-9_]*$` |
| `mounted-configuration` | Absolute normalized POSIX path |
| `trust-store` | Absolute normalized POSIX path |
| `runtime-command` | Absolute normalized POSIX path |
| `writable-state` | Absolute normalized POSIX path |

An absolute path starts with `/`, is not `/`, contains no empty, `.`, `..`, or
NUL segment, and has no trailing slash. Reference ids use the dot-separated
slug grammar from spec 0001 and are unique. Duplicate `(kind, locator)` pairs,
unused references, unknown reference ids, missing host roots, and credential
values in the request are invalid.

Each route prerequisite names `prerequisite_id`, `request_reference_id`, and
one common prerequisite kind. The target's `environment_ref_ids` shall contain
exactly one reference with that `request_reference_id` and the mapped request
kind:

| Route prerequisite | Request reference |
|---|---|
| `authentication` | `authentication-env` |
| `trust` | `trust-store` |
| `runtime` | `runtime-command` |
| `configuration` | `mounted-configuration` |
| `writable-state` | `writable-state` |

Missing, duplicate, wrong-kind, or unselected mapped references fail before
mutation. The provisioner performs no name, path, or kind inference.

A prerequisite check node is keyed by
`(prerequisite_kind, request_reference_id, reference_kind, locator)`. It is
`shared` only when the same node key is required by at least two otherwise
valid tuples; equal descriptions or prerequisite ids alone do not make it
shared. Nodes are checked in lexicographic node-key order. The node's owner is
the member with the lowest execution key
`(host, surface_id, plugin_id, package_version, route_id)` that has not already
received a failed or skipped outcome from an earlier node.

Each node is scheduled once during global preflight and executed at most once.
On failure, its owner tuple
is `failed` at `prerequisite-check` with the mapped concrete diagnostic
(`missing-authentication`, `missing-trust`, `missing-runtime`,
`missing-configuration`, or `unwritable-state`). Every other member is
`skipped` at `prerequisite-check` with
`blocked_by: {kind: prerequisite, prerequisite_id:
<that-member-prerequisite-id>, owner_result_id: <owner-result-id>}` and
diagnostic `blocked-by-shared-prerequisite`. The owner result shall precede
each dependent in execution order. A non-shared prerequisite failure fails
its sole tuple and never creates a skip.

After each node, assigned outcomes are final for prerequisite preflight. A
later scheduled node considers only members still unassigned: if two or more
remain it executes once under the shared rule and chooses the lowest remaining
member as owner; if one remains it executes once as non-shared and that tuple
fails directly on failure; if none remain its execution state is
`not-executed-members-finalized`, it performs zero environment check and
creates no diagnostic, blocker, or tuple result. This state is an internal
preflight-plan outcome, not a skipped receipt result. Earlier failed/skipped
members retain their first outcome and are never reassigned or used as later
owners.

### Global validation order and attribution

Validation evaluates phases 1–4 in order and stops after the first phase with
an error. If phases 1–4 pass, it performs route lookup for every tuple,
finalizing any route lookup failure at `identity-resolution`. It then evaluates
phase 5 only for tuples whose route resolved. If phase 5 passes, phase 6 runs
globally across the complete decoded environment and every target, including
route-failed targets. Thus route records exist before route-dependent phase 5,
while unused-reference detection remains request-global:

1. JSON decode and envelope schema;
2. path safety;
3. target, plugin, state-root, reference-id, reference-locator, and each
   target's `environment_ref_ids` uniqueness;
4. surface/host match, targeted-host state-root coverage, and resolution of
   every target `environment_ref_id` against `environment.references`;
5. resolved-route prerequisite selection and kind mapping;
6. unused references.

Route-failed results remain finalized if phase 5 or 6 later fails. At such a
request-validation failure, affected route-resolved tuples fail, every other
route-resolved tuple is skipped by request validation, and already-finalized
route failures are neither replaced nor skipped. Exit `2` dominates route
exit class `3`, and no mutation occurs. If phases 5–6 pass, route-resolved
tuples continue while route-failed tuples remain independent failures.

Phase 6 defines “used” solely as membership in the union of every decoded
target's `environment_ref_ids`; a reference selected by a route-failed target
therefore counts as used even though that route's prerequisites are not
checked. Phase 6 still runs when some or all tuples failed route lookup, unless
phase 5 already failed. Any unused reference makes the request globally
invalid: exit `2` overrides route exit `3`, route-failed results remain
identity-resolution failures, and every otherwise valid route-resolved result
is request-validation skipped.

The request JSON Schema validates structure but deliberately does not use
`uniqueItems` or cross-row uniqueness constraints; phases 3–6 own those
semantic errors so their attribution is not preempted by phase 1.

Attribution is exact:

| Error | Receipt attribution at the stopping phase |
|---|---|
| Undecodable envelope or non-array `targets` | One envelope `invalid-request`; empty `results` |
| Invalid/unknown top-level field; invalid UUID; invalid request/executing `provisioner_version`; missing, non-object, or extra-field `environment` | One envelope `invalid-request`; every decodable tuple is skipped at `request-validation` |
| Structurally invalid target or unknown target field with an enumerable `plugins` array | Every decodable tuple position in that target fails with `invalid-request`; every other decodable tuple is skipped |
| Non-array target `plugins` | One envelope `invalid-request`; every tuple decodable from other targets is skipped; no synthetic plugin position is created |
| Structurally invalid plugin selection or unknown plugin field | That plugin position fails with `invalid-request`; every other decodable tuple is skipped |
| Structurally invalid/unknown state-root or reference field, including non-array environment collections | One envelope `invalid-request`; every decodable tuple is skipped |
| Unsafe state-root or reference path | One envelope `unsafe-path` cause per field; every enumerable tuple is skipped at `request-validation` |
| Duplicate target/plugin | Positional tuple failures under the duplicate precedence above; all other tuples are skipped at `request-validation` |
| Duplicate state-root | Every tuple targeting that host fails with one cause per later row; if no tuple targets it, those causes are envelope-scoped; all others are skipped |
| Duplicate reference id or `(kind, locator)` | Tuples selecting either duplicate fail with one cause per later row; if no tuple selects it, those causes are envelope-scoped; all others are skipped |
| Duplicate `environment_ref_ids` within a target | Every tuple in that target fails with `duplicate-reference`; all others are skipped |
| Surface/host mismatch | Every tuple in that target fails with `host-surface-mismatch`; all others are skipped |
| Missing or extra targeted-host root | Every tuple for a missing-root host fails with a `missing-state-root` cause; an extra-root row is an envelope `invalid-request` cause; all others are skipped |
| Unknown target `environment_ref_id` | Every tuple in that target fails with `invalid-request`; all others are skipped |
| Unselected or wrong-kind resolved-route prerequisite reference | Each affected route-resolved tuple fails with `invalid-request` or `wrong-reference-kind`; all other route-resolved tuples are skipped; route-failed results remain finalized |
| Unused reference | One envelope `unused-reference` cause per reference id; every otherwise valid tuple is skipped |

All tuple failures in this table have `phase: request-validation`; all table
skips use `blocked_by: {kind: request-validation}`. An envelope diagnostic
does not replace required attributable tuple failures. Missing-root detection
compares the set of distinct targeted hosts to the set of state-root hosts
after uniqueness succeeds. Unused-reference detection compares every
reference id to the union of all target `environment_ref_ids`; route lookup is
not used to excuse an unselected reference.

Duplicate and unknown target `environment_ref_ids` are therefore decided for
every enumerable target before route lookup. Any such error is global request
invalidity with exit `2`; no tuple in that request reaches route lookup, so a
would-be route failure cannot mask or replace the request error.

For phase 1, a decodable tuple position is an element position in an array
`targets[i].plugins[j]`, even when the element is non-object or has invalid
fields. Its result id remains `t<i>.p<j>` and contains only tuple fields that
decoded. Unknown fields are never copied to a receipt. Phase-1 tuple failures
and skips use diagnostic `invalid-request`; an envelope diagnostic is emitted
only by the rows that explicitly require one.

## Receipt grammar

### Envelope

When the receipt output contract is usable, the provisioner attempts to write
a receipt even when parsing or request validation fails. A successfully
written normal envelope always contains:

- `schema_version: 1`;
- `request_id` and `provisioner_version`, each the decoded value or `null`;
- `started_at`, `finished_at`, `overall_outcome`, and `exit_code`;
- `results`, in ascending `(target_index, plugin_index)` order; and
- `diagnostics`, a possibly empty list.

If the request cannot be decoded enough to enumerate tuples, `results` is
empty and one envelope diagnostic is required. Otherwise every requested tuple
has exactly one result, including duplicates and tuples not attempted.
`target_index` and `plugin_index` are zero-based positions in the decoded
request; `result_id` is exactly `t<target_index>.p<plugin_index>`. These fields,
not tuple values, make duplicate results unique.

For duplicate targets or plugins, the lowest-index occurrence is canonical and
each later duplicate result is `failed` with `duplicate-target` or
`duplicate-plugin`. On global request invalidity, every otherwise valid
enumerable result not already finalized at the route boundary is `skipped` with
`blocked_by: {kind: request-validation}` and diagnostic code
`invalid-request`.

Duplicate classification precedence is target before plugin: every result in a
later duplicate target fails with `duplicate-target`; plugin duplication is
evaluated only inside the canonical target, where each later plugin occurrence
fails with `duplicate-plugin`. No result receives both codes.

A diagnostic contains:

| Field | Contract |
|---|---|
| `code` | Enumerated code below |
| `message` | UTF-8, one line, 1–1024 characters, no credential value |
| `owner` | `stewards` or `consumer/environment` |
| `retryable` | Boolean |
| `reference_ids` | Duplicate-free known ids; empty when none |
| `causes` | Non-empty sorted exact cause list |

Each cause contains exactly `code`, `source`, RFC 6901 `field_path`, and sorted
`reference_ids`. `source` is `request`, `provisioners`, `execution`, `state`,
`result`, or `outputs`. Causes sort by
`(code-rank, source, field_path, reference_ids)`;
`diagnostic.code` and top-level `reference_ids` equal the first cause's code
and the union of all cause reference ids. Multiple errors assigned to one
tuple are represented as causes in its one diagnostic, never as competing
tuple results. A cause assigned to an envelope diagnostic is not repeated in
a tuple diagnostic.

Within a validation phase, primary code rank is:

| Phase | Lowest → highest precedence |
|---|---|
| 1 | `invalid-request` (tie by field path) |
| 2 | `unsafe-path` |
| 3 | `duplicate-target`, `duplicate-plugin`, `duplicate-state-root`, `duplicate-reference` |
| 4 | `host-surface-mismatch`, `missing-state-root`, `invalid-request` |
| 5 | `wrong-reference-kind`, `invalid-request` |
| 6 | `unused-reference` |

Non-request diagnostic rank is:

| Phase/class | Lowest → highest precedence |
|---|---|
| Identity resolution | `route-ambiguous`, `route-unavailable`, `route-version-mismatch`, `route-not-found`, `unresolved-release`, `identity-mismatch` |
| Prerequisite | `missing-authentication`, `missing-trust`, `missing-runtime`, `missing-configuration`, `unwritable-state`, `blocked-by-shared-prerequisite` |
| Execution | `acquisition-failed`, `catalog-registration-failed`, `installation-failed`, `verification-failed`, `preservation-conflict`, `preservation-breach`, `rollback-failed` |
| Output sealing | `receipt-seal-failed`, `output-parent-invalid`, `audit-seal-failed` |

Cause attribution outside request validation is exact:

| Cause | `source` / `field_path` | `reference_ids` |
|---|---|---|
| Route ambiguous/not found | `provisioners` / `/records` | requested `route_id` |
| Route unavailable/version mismatch | `provisioners` / `/records/<sorted-index>/state` or `/provisioner_version` | requested `route_id` |
| Tag/commit unresolved or identity mismatch | `execution` / `/results/<result_id>/identity-resolution` | requested `route_id` |
| Concrete prerequisite failure | `request` / exact `/environment/references/<index>/locator`, or the target `environment_ref_ids` element when missing | `prerequisite_id` plus `request_reference_id` when it exists |
| Shared-prerequisite skip | `result` / `/blocked_by/prerequisite_id` | dependent `prerequisite_id` and request-reference id |
| Acquisition/registration/installation/verification | `execution` / `/results/<result_id>/<phase>` | only request-reference ids actually consulted by that failing operation |
| Preservation conflict/breach | `state` / `/results/<result_id>/shared_catalog_changes` | empty |
| Rollback failure | `state` / `/results/<result_id>/shared_catalog_changes/<index>/rollback_status` | empty |
| Receipt parent/create/write/fsync/final validation | `outputs` / `/receipt/parent`, `/receipt/create`, `/receipt/write`, `/receipt/fsync`, or `/receipt/final-validation` | empty |
| Audit parent/create/write/fsync/read-back/final validation | `outputs` / `/audit/parent`, `/audit/create`, `/audit/write`, `/audit/fsync`, `/audit/read-back`, or `/audit/final-validation` | empty |

Provisioner records sort by their declared complete key before `<sorted-index>`
is assigned. Diagnostic owner is `consumer/environment` for request and
prerequisite causes, and `stewards` for provisioner, execution, state,
rollback, and output causes. A multi-cause diagnostic uses the owner of its
primary cause; all causes shall belong to that same owner, otherwise they are
split into one diagnostic per owner at the same envelope scope.

The attribution table first assigns every same-phase cause to its envelope or
tuple scope; then each envelope scope emits one diagnostic per owner using
this rank, while every tuple's causes shall share one owner and emit its one
diagnostic. Duplicate target precedence still suppresses plugin-duplicate
evaluation inside a later duplicate target, so no suppressed cause is emitted.

Codes are `invalid-request`, `duplicate-target`, `duplicate-plugin`,
`duplicate-state-root`, `duplicate-reference`, `unsafe-path`,
`missing-state-root`, `unused-reference`, `host-surface-mismatch`,
`wrong-reference-kind`,
`route-not-found`, `route-unavailable`, `route-version-mismatch`,
`route-ambiguous`, `unresolved-release`, `identity-mismatch`, `missing-authentication`,
`missing-trust`, `missing-runtime`, `missing-configuration`,
`unwritable-state`, `acquisition-failed`, `catalog-registration-failed`,
`preservation-conflict`, `preservation-breach`, `rollback-failed`,
`installation-failed`, `verification-failed`, and
`blocked-by-shared-prerequisite`, `output-parent-invalid`,
`audit-seal-failed`, and `receipt-seal-failed`.

### Tuple result

Every result has `result_id`, `target_index`, `plugin_index`, all decodable
tuple fields (including `route_id`), `phase`, and `outcome`. Phases are
`request-validation`, `identity-resolution`, `prerequisite-check`,
`acquisition`, `catalog-registration`, `installation`, and `verification`.
Outcomes are `changed`, `already-converged`, `failed`, and `skipped`.

`blocked_by` is a discriminated union:

- `{kind: request-validation}`;
- `{kind: result, result_id: <existing-result-id>}`; or
- `{kind: prerequisite, prerequisite_id:
  <selected-route-prerequisite-id>, owner_result_id:
  <existing-failed-result-id>}`.

No other string or object is valid. A result blocker names a distinct failed
result that precedes it in execution order; self-reference, forward-reference,
and cycles are invalid. A prerequisite blocker names the dependent tuple's
selected-route prerequisite and the failed owner result for the exact shared
check node; the owner result also precedes it, and cycles are invalid.

The result schema is a discriminated union:

| Variant | Required | Forbidden |
|---|---|---|
| success | `phase: verification`; outcome `changed` or `already-converged`; resolved identity, acquisition route, host adapter, prior/final state, shared catalog changes, verification | diagnostic, blocked-by |
| validation failure | `phase: request-validation`, `outcome: failed`, one diagnostic | resolved identity, route, adapter, states, catalog changes, verification, blocked-by |
| resolution failure | `phase: identity-resolution`, `outcome: failed`, one diagnostic | resolved identity, route, adapter, states, catalog changes, verification, blocked-by |
| prerequisite failure | `phase: prerequisite-check`, `outcome: failed`, resolved identity, acquisition route, host adapter, one diagnostic | states, catalog changes, verification, blocked-by |
| execution failure | phase acquisition or later, `outcome: failed`, resolved identity, acquisition route, host adapter, prior state, final observed state, shared catalog changes, one diagnostic; verification required only when phase is verification | blocked-by |
| skipped | `outcome: skipped`, one diagnostic, one blocked-by union | fields whose producing phase did not complete |

For skipped results, `phase` is the phase at which the tuple was prevented
from starting, determined only by this precedence:

1. any global request error produces `phase: request-validation` and the
   request-validation blocker;
2. otherwise, an unmet shared prerequisite produces
   `phase: prerequisite-check` and the lexicographically lowest pair
   `(prerequisite_id, owner_result_id)`;
3. otherwise, a prior `preservation-breach` result with
   `rollback_status: restore-failed` that tainted the same host produces
   `phase: acquisition` and the earliest failed result in execution order.

No other skipped phase is valid. Request-validation skips forbid resolved
identity and later fields. Prerequisite-check skips require resolved
identity/route/adapter and forbid states and later fields. Acquisition skips
require those fields plus the retained `prior_state` captured during complete
preflight, and forbid final state, catalog changes, and verification. All
identity resolution, prerequisite checks, and prior-state snapshots for valid
tuples complete before the first mutation; therefore this acquisition skip
shape is always available. A prerequisite blocker wins over a result blocker;
ties within a class use the order above. The skipped diagnostic is
`invalid-request` for request validation,
`blocked-by-shared-prerequisite` for a prerequisite blocker, and the blocking
result's diagnostic code for a result blocker. A skipped diagnostic contains
one synthetic blocker cause rather than copying a validation cause:
`source: result, field_path: ""` for request validation,
`source: result, field_path: /blocked_by/prerequisite_id` for a prerequisite,
or `source: result, field_path: /blocked_by/result_id` for taint; its
reference ids come only from the blocker. Synthetic blocker causes do not
violate the no-duplicate source-cause rule.

`acquisition_route` contains the selected `route_id`, complete provisioner
record key, exact request/record `provisioner_version`, `kind`
(`catalog-selector`, `direct-tag`, or `direct-commit`), resolved immutable ref,
and stable reference to that provisioner record.

`host_adapter` contains `host`, normalized `adapter_path`,
`adapter_version` (SemVer), adapter `sha256`, and `launch_entrypoints`.
`launch_entrypoints` is a non-empty array sorted by `entrypoint_id`; each
additional-properties-forbidden row contains exactly `entrypoint_id` and
`command_name`. Both use the common identity grammar, and each is unique.

A `package_state` contains `presence: absent` and forbids release identity, or
`presence: installed` and requires plugin/version/tag/commit. A
`catalog_registration_state` contains `presence: absent` and forbids catalog
identity, or `presence: registered` and requires catalog name, manifest path,
selector, and manifest SHA-256. Every receipt, state document, and catalog
change selector validates against spec 0001's exact `source_selector`
discriminated union; successful verification requires its immutable tag/commit
binding. `prior_state` and `final_state` each contain exactly one selected
package state, one Kodhama catalog-registration state,
`peer_selected_packages`, `unselected_packages`, and
`unselected_catalog_entries` using the complete ordering and row grammar of
`provision-state.v1.schema.json`. `peer_selected_packages` is exactly every
other plugin selection in the same target, each with plugin id, requested
version/route, and observed package state; `unselected_packages` is every
observed installed plugin absent from the target's selection set. Both arrays
sort by `plugin_id`, and their plugin-id sets are disjoint.

A `catalog_change` contains `operation` (`add`, `update`, `remove`, or
`restore`), typed before/after catalog states, `unselected_before_sha256`,
`unselected_after_sha256`, `rollback_status` (`not-needed`, `restored`, or
`restore-failed`), and conditional `rollback_diagnostic`: required only for
`restore-failed`. Each unselected digest is SHA-256 of the complete sorted
`unselected_catalog_entries` array in the canonical state document; a
preserving successful change requires equality.
`shared_catalog_changes` is always an array. An execution failure after any
shared mutation shall record both the attempted change and every rollback
attempt, including restore failure.

`resolved_identity` contains exact package version, release tag, and full
source commit. `verification` has `additionalProperties: false` and is exactly
one of:

| `status` | Required fields | Conditional constraints |
|---|---|---|
| `passed` | `status`, `discovery`, `installed_identity`, `catalog_selector`, `unselected_state_before_sha256`, `unselected_state_after_sha256`, `allowed_write_set_sha256`, `write_events_reference`, `write_events_sha256`, `preservation: preserved` | discovery is exactly `{status: found, host, surface_id, plugin_id}`; installed identity equals `resolved_identity`; selector is the immutable `source_selector` union from spec 0001 and binds that tag/commit; before and after unselected-state digests are equal; every non-exempt observed write is allowed |
| `failed` | `status`, `discovery`, `unselected_state_before_sha256`, `unselected_state_after_sha256`, `allowed_write_set_sha256`, `write_events_reference`, `write_events_sha256`, non-empty duplicate-free `failure_codes` | discovery status is `absent`, `ambiguous`, or `found`; `installed_identity` and `catalog_selector` are required only for `found`; `preservation` is forbidden; mismatch or outside-allowlist writes appear in `failure_codes` |

The failed variant's codes are `host-not-discovered`,
`host-discovery-ambiguous`, `installed-identity-mismatch`,
`catalog-selector-mismatch`, `unselected-state-changed`, or
`outside-allowed-write`. `discovery`, installed identity, and nested selector
objects also forbid additional properties. The unselected-state fingerprint
is SHA-256 of exactly this canonical object, populated from the corresponding
retained state document:

```
{"peer_selected_packages":<complete-array>,"unselected_packages":<complete-array>,"unselected_catalog_entries":<complete-array>}
```

The shown key order, state-array ordering, and canonical JSON bytes are
mandatory. The receipt's before/after fingerprints equal recomputation from
that result's `prior_state` and `final_state`; in a promotion bundle those
states also equal the applicable retained initial/prior and run-final
documents. The
`write_events_reference` is a stable reference to the exact explicit audit
path; its digest equals `write_events_sha256`. The
`allowed_write_set_sha256` equals that result id's tuple-set digest inside the
audit, and the write audit independently binds the global write boundary.

Verification is distribution evidence, not product behavior evidence.
Envelope diagnostics are only for non-attributable parse/global errors; tuple
diagnostics occur only in their result and are not duplicated.
For `already-converged`, prior state equals final state byte-for-byte and
`shared_catalog_changes` is empty. For `changed`, prior and final state differ
in at least one selected or allowed shared field. On overall success envelope
diagnostics shall be empty.

## Resolution and execution

The provisioner performs:

1. decode and validate request phases 1–4;
2. enumerate execution keys and sort by `(host, surface_id, plugin_id,
   package_version, route_id)`;
3. resolve each route or finalize its identity-resolution lookup failure;
4. validate phase 5 against resolved route prerequisites, then run phase 6
   globally across all targets/references;
5. resolve every remaining tuple's exact package version to the computed tag
   and peeled commit;
6. check every environment prerequisite node and capture
   every valid tuple's preflight state, completing this global preflight before
   any mutation;
7. acquire the immutable tag or commit;
8. register or reconcile the host-native `kodhama` catalog;
9. install or reconcile only the selected plugin/version;
10. verify host discovery and installed identity without launching an agent;
11. emit the complete receipt.

Immediately before an executable tuple begins acquisition, the adapter takes a
fresh `prior_state`; after it finishes, it takes `final_state`. A tuple skipped
at acquisition uses its preflight snapshot as `prior_state`. This makes
peer-selected before/after equality relative to the current tuple even when an
earlier tuple legitimately converged that peer.

A globally invalid request causes no mutation. For a valid request, independent
tuples—including later tuples on the same host—continue after an ordinary
resolution, prerequisite, acquisition, registration, installation, or
verification failure. Only an unrecovered preservation breach taints host
state and blocks remaining tuples for that host. A skipped tuple uses the
single blocker and phase selected by the normative precedence in Receipt
grammar; it is never omitted.

The provisioner never substitutes another release. Matching selected state is
`already-converged`. Nonmatching selected state may change only to the explicit
version.

## Selected convergence and preservation

The preservation claim is limited to **writes performed by the provisioner
process tree during this invocation, excluding only the two declared protocol
output files**. It does not claim that unrelated concurrent processes cannot
change state.

Before monitoring, the core resolves the exact receipt and audit paths and
opens only their existing parent-directory descriptors. Each leaf shall not
exist; each path and parent realpath shall be absolute, normalized,
non-symlinked, distinct, and outside every host state root. Those two resolved
leaf paths form the complete `exempt_output_paths`; no directory or sibling
path is exempt. After both initial checks pass and immediately before request
work, the core repeats both parent-identity and descriptor-relative no-follow
leaf-absence checks. Failure follows the output-parent rules below and no
request work begins.

Output ownership and commitment are exact:

Ownership for mutation and commitment for external evidence are independent.
A retained witness may be foreign to the running invocation, and therefore
immutable by it, while still satisfying the committed-evidence predicate.

| State | Contract |
|---|---|
| pre-existing or foreign | A leaf that existed before this invocation's exclusive create, or whose current identity differs from the identity returned by that create; the invocation shall not modify or remove it |
| invocation-created, uncommitted | A leaf successfully exclusive-created through the held parent descriptor by this invocation, whose file identity is retained, and whose retained state does not satisfy the applicable committed-evidence predicate |
| sealed, uncommitted audit | A retained regular audit whose bytes are canonical and schema-valid but for which no retained committed normal receipt binds the requested audit path and digest |
| committed normal evidence | A retained regular normal receipt at the exact requested receipt path whose canonical schema-valid bytes bind the exact requested audit path and SHA-256 of the retained regular canonical schema-valid audit |
| committed minimal receipt | A retained regular minimal output-failure receipt at the exact requested receipt path whose canonical bytes satisfy the minimal-receipt schema variant |

A sealed audit alone and a partial, non-canonical, schema-invalid, non-regular,
or audit-mismatched receipt are uncommitted and are not valid distribution
evidence. External validation resolves each exact absolute normalized
requested path through currently non-symlinked parents and without following
a leaf symlink, and classifies evidence solely from the currently retained
path, regular-file type, canonical bytes, schema, and digest binding.
For normal evidence, `write_events_reference` shall equal the exact requested
audit path and `write_events_sha256` shall equal SHA-256 of that retained
canonical schema-valid audit. The minimal variant instead forbids the audit
reference and digest and commits failure evidence from its own retained
canonical schema-valid bytes.

The external predicate is independent of who wrote identical retained bytes
and of whether exclusive-create, fsync, descriptor-read-back, or producer file
identity history can later be proven. Those operations remain mandatory
producer obligations and failure diagnostics; they are not predicates of
external commitment. No separate marker or in-memory transition participates
in commitment.

For each executable tuple, the core computes a tuple allowed-write set
containing only:

- `<target-state-root>/.kodhama-provision/tmp/<request_id>` as the only scratch
  subtree;
- the current selected plugin's exact host installation subtree; and
- the selected host's exact Kodhama catalog-registration paths.

The current tuple's package/catalog paths come from exact fields in the
resolved host adapter and are included in its digest. Every allowed-write row
contains exactly `path`, `match` (`exact` or `subtree`), and
`classification`; rows sort by path, cannot overlap, and are hashed with the
canonical JSON rules. Tuple sets sort by `result_id`. Before tuple execution,
only the scratch subtree is allowed.

The core activates a process-tree write monitor before its first non-exempt
write and buffers events in memory. The explicit audit document validates
against `provision-write-events.v1.schema.json`, forbids additional
properties, and contains exactly `schema_version: 1`, `request_id`,
`exempt_output_paths`, `preflight_allowed_write_set`,
`tuple_allowed_write_sets`, `events`, and `sealed_at`. It contains no receipt
digest, audit digest, or self-fingerprint. The monitor records every
non-exempt create, modify, rename, and delete. Each event contains exactly monotonic
`sequence`, `result_id` (or `null` before tuple execution), operation,
normalized path, process id, before/after
SHA-256 or `null` when absent, and classification
(`receipt-evidence-scratch`, `selected-package`, `selected-kodhama-catalog`, or
`outside-allowed-write`). Events sort by sequence; sequence is unique.
Classification uses the sole matching exact/subtree row; no match is
`outside-allowed-write`. For create, `before_sha256` is null; for delete,
`after_sha256` is null; modify requires both; rename is represented by two
adjacent events, delete then create, with the same process id.

The normal producer sealing order applies only to a successful two-output
write;
“successful” here describes the output transaction, regardless of the
receipt's tuple aggregate outcome:

1. wait for the core and every descendant to quiesce, stop the monitor, set
   `finished_at`/`sealed_at` to that stop instant, and forbid further
   non-exempt process-tree writes;
2. canonicalize the audit object and write it exactly once through its
   parent descriptor using no-follow/exclusive-create, then fsync the file and
   held parent directory and compute SHA-256 from descriptor-read-back bytes.
   The held parent descriptor, requested parent path, and descriptor-relative
   leaf lookup shall still identify the preflight parent and the regular file
   returned by this invocation's create; the bytes shall be canonical and
   schema-valid;
3. construct the complete normal receipt in memory with that audit stable
   reference/digest, canonicalize it, and schema-validate it before creating
   the receipt leaf;
4. while retaining the audit descriptor and verifying immediately before
   receipt creation that the requested audit leaf is still a regular file
   with the canonical schema-valid bytes and digest bound by the receipt,
   exclusive-create
   the receipt through its held parent descriptor, write exactly the
   prevalidated canonical bytes, fsync the file and held parent directory, and
   descriptor-read the file back. The receipt's requested parent/leaf identity
   shall remain the preflight parent and this invocation's regular file;
   read-back bytes shall equal the prevalidated bytes and shall still
   schema-validate. Final retained-state validation shall confirm that the
   requested audit path still holds the regular canonical schema-valid bytes
   and digest bound by that receipt. These checks are required for the
   producer to report successful output sealing; and
5. perform no further process-tree write, modification, or deletion before
   exit.

As soon as retained output satisfies the external committed-evidence
predicate, it is committed even if the producer later cannot prove that it
completed an obligation above or another writer created identical bytes.
Conversely, completing the producer operations does not commit retained state
that fails the external predicate.

On the successful path the monitor intentionally omits only the two writes in
steps 2 and 4, whose exact paths are sealed inside the audit. Failure cleanup
below may operate only on those same exempt leaves after monitoring stops and
never supports a success or preservation claim. Because the audit contains
neither its own digest nor receipt bytes, and the receipt is written only
after the audit digest exists, no receipt/audit digest cycle is permitted.

During the same invocation, handled-failure pre-commit cleanup is permitted
only for a partial or invalid audit, a canonical audit orphaned by the absence
of a valid bound normal receipt, or a demonstrably partial or invalid normal
receipt. Before considering any unlink, the core shall classify the retained
receipt and audit using the external committed-evidence predicate. A valid
normal or minimal receipt is committed and ineligible for cleanup regardless
of reported producer failure or provable creation history. If retained-state
classification is uncertain because path, type, bytes, schema, or digest
binding cannot be read or validated, cleanup is forbidden and the leaves
become operator-owned. For each otherwise eligible candidate, the core shall
also prove through the retained parent descriptor that:

1. this invocation created the leaf by no-follow/exclusive-create;
2. the output is demonstrably partial or invalid under the retained-state
   predicate, or is an orphan audit with no valid bound normal receipt;
3. the parent identity is unchanged; and
4. descriptor-relative no-follow lookup still identifies that invocation's
   recorded file identity.

It then may unlink only that leaf relative to the held parent descriptor.
The identity guarantee shall cover the unlink itself; if the platform cannot
prevent substitution between identity verification and unlink, cleanup is not
permitted and the leaf remains. Cleanup never resolves the leaf from an
absolute path and never unlinks a missing, pre-existing, foreign,
identity-changed, or committed output.

Abrupt termination ends that cleanup authority. On recovery, retained
path/type/bytes/schema/digest validation alone determines whether a normal or
minimal committed receipt witness exists. Any other invocation-created leaf
is pre-commit operator-owned crash debris: a later invocation has no retained
creation identity that authorizes recovery, treats the leaf as pre-existing,
fails closed under the ordinary parent/leaf rules, and never modifies or
deletes it. If validation is uncertain, the provisioner likewise fails closed
and leaves resolution to an operator. A valid retained witness remains
committed even when the process terminated before reporting success.

Output failure handling is exact and never requires an impossible receipt:

1. validate the receipt parent/leaf first. Parent open/realpath failure,
   existing leaf, or unsafe leaf emits `receipt-seal-failed` to stderr and
   exits `7`; no request work, receipt, or audit is promised;
2. validate the audit parent/leaf second. Failure writes, when possible, one
   minimal receipt with `overall_outcome: output-failure`, exit `7`, empty
   results, and envelope diagnostic `output-parent-invalid`; it creates no
   audit and performs no request work;
3. after request work, any audit exclusive-create, write, fsync,
   read-back/hash/final-validation failure first classifies retained outputs,
   never deletes a valid committed receipt witness, attempts eligible cleanup
   only of a demonstrably partial or invalid audit or an orphan audit, and
   attempts the same minimal receipt with `audit-seal-failed`; any remaining
   unbound audit is invalid evidence and no tuple success is claimed; and
4. after a valid audit, any receipt exclusive-create, write, fsync,
   or final-validation failure first classifies retained outputs, reports
   `receipt-seal-failed` to stderr, exits `7`, preserves any valid committed
   receipt witness, and attempts eligible cleanup only of a demonstrably
   partial or invalid normal receipt and an orphaned audit. A producer failure
   report does not negate valid retained evidence.

If an audit failure is discovered after a normal receipt may exist, the core
shall first apply the retained-state predicate. A valid canonical normal
receipt binding the retained regular audit is already committed and
ineligible for cleanup. An unreadable or otherwise uncertain receipt is also
ineligible for cleanup and becomes operator-owned. The core may replace only
a demonstrably partial or invalid uncommitted receipt, and only when the
receipt parent and leaf still
satisfy every cleanup identity condition above. It descriptor-unlinks the
normal receipt, confirms leaf absence through the same parent descriptor, and
exclusive-creates the minimal `audit-seal-failed` receipt at that leaf; it
never truncates or edits the normal receipt in place. The minimal receipt is
externally committed whenever the exact requested receipt path retains a
regular file with canonical bytes satisfying the minimal schema variant. The
producer shall still precompute and schema-validate those bytes, then
exclusive-create, write, file-and-parent-fsync, and descriptor-read them back
before reporting successful minimal-receipt sealing. If any replacement step
fails or retained-state classification is uncertain, the core leaves the
existing leaf untouched from that point and promises no producer success.

The minimal output-failure receipt is a separate envelope variant: it contains
the ordinary schema/request/version/timestamps when decoded, otherwise null,
requires empty results and exactly one output diagnostic, and forbids tuple
success, audit reference/digest, and preservation fields. Failure while
creating, writing, fsyncing, or finally validating that minimal receipt
reports `receipt-seal-failed` to stderr, but does not negate a retained minimal
receipt that independently satisfies the external predicate.
Exit `7` overrides every tuple aggregate outcome. Recovery never modifies or
deletes a pre-existing, foreign, identity-changed, or committed output; it may
leave invocation-created uncommitted debris when identity-safe cleanup cannot
be proven.

A successful tuple requires zero `outside-allowed-write` events. Consequently,
provisioner-authored writes to unselected plugin installation/configuration
state, a peer-selected plugin while another tuple is active, another host's
state, or a non-Kodhama catalog are observable
preservation breaches. The contract makes no preservation claim about
unobserved external-process writes or state outside the provisioner
process-tree write boundary.

Before changing shared catalog registration, the adapter snapshots the entire
selected host Kodhama catalog and proves the proposed projection preserves
every unselected entry and installed identity. If it cannot, the tuple fails
before registration with `preservation-conflict`.

After registration, the adapter compares the shared-state diff to the allowed
projection. An unexpected unselected change fails verification and restores
the catalog-registration snapshot. If restoration succeeds, the result is
failed with `preservation-conflict` and records `rollback_status: restored`.
If restoration fails, the result is failed with `preservation-breach` plus a
`rollback-failed` diagnostic, records the observed final state and
`rollback_status: restore-failed`, marks that host state tainted, and skips
every remaining tuple for that host with `blocked_by` pointing to the breach
result. No success or preservation claim is made for that run.

Rollback is limited to the shared catalog registration; it does not claim
cross-host or package rollback. Every attempted shared change and rollback is
reported in `shared_catalog_changes`. The canonical state documents plus the
complete process-tree write log are coextensive with this bounded preservation
claim: selected-host unselected state is compared by snapshot, and every
provisioner-authored write elsewhere is classified by the monitor.

## Deterministic aggregate result

`changed` and `already-converged` are successful tuple outcomes.

| Condition | Exit / overall outcome |
|---|---|
| Global request invalid | `2` / `invalid-request`; no mutation |
| Output contract or sealing failure | `7` / `output-failure`; rules above determine whether a valid minimal receipt exists |
| Every tuple successful | `0` / `success` |
| At least one successful and at least one failed or skipped | `6` / `partial-failure` |
| No successful tuple; any identity-resolution failure, including route lookup | `3` / `failed` |
| No successful tuple; no identity-resolution failure; any prerequisite failure | `4` / `failed` |
| No successful tuple; only acquisition/registration/install/verification failures | `5` / `failed` |

Skipped tuples inherit the originating failure class for aggregation and never
create a new class. This precedence is independent of request order.

Successful tuple state remains after a partial failure. Repeating the same
request resumes deterministically: successful tuples become
`already-converged`; failed/skipped tuples are retried when their blocker is
gone. No cross-host transaction or rollback is promised.

## Retained evidence and promotion

For an exact route key and provisioner version, the evidence directory is:

```
distribution/evidence/provisioner/<route_id>/<surface_id>/<plugin_id>/<package_version>/<provisioner_version>/
```

It contains exactly:

| File | Content |
|---|---|
| `request.json` | Canonical request for one tuple |
| `environment.json` | Clean image/snapshot id and digest, host version, surface, PATH, and state-root identities |
| `entrypoints.json` | Adapter declaration, deterministic discovery rows, and declaration/discovery digests |
| `state-initial.json` | Complete canonical state before run 1 |
| `state-run-1.json` | Complete canonical state after run 1 quiesces |
| `state-run-2.json` | Complete canonical state after run 2 quiesces |
| `run-1.receipt.json` | First clean-state receipt |
| `run-2.receipt.json` | Immediate identical repeat receipt |
| `launch-events.json` | Active launch-interceptor events |
| `run-1.write-events.json` | Complete run-1 provisioner-process-tree writes and allowlist classifications |
| `run-2.write-events.json` | Complete run-2 provisioner-process-tree writes and allowlist classifications |
| `harness.json` | Interceptor/monitor configuration and ordered references to retained state, launch, and write documents with digests |
| `manifest.json` | Schema version, exact route identity, and SHA-256 for every other file |

`distribution/evidence/provisioner/index.json` lists each bundle path, exact
route key, provisioner version, manifest digest, and retention timestamp.
The request, both receipts, acquisition route, manifest, index row, directory
version segment, and cited availability record shall carry the same
`provisioner_version`; it also equals the executing core version recorded by
the harness. Any mismatch invalidates the bundle and route verification.
Bundles referenced by a verified route and by catalog clean-install evidence
are immutable; byte change, missing file, digest mismatch, or index mismatch
invalidates verification.

Before either run, the harness discovers and intercepts the target host's
complete launch-entrypoint set. The adapter's `launch_entrypoints` declaration
is authoritative for the exact `(host, host_version, adapter_version)` and is
included verbatim in `entrypoints.json`. Discovery is:

1. split the clean environment's literal `PATH` on `:`; reject an empty,
   relative, non-normalized, duplicate, or nonexistent directory element;
2. for each declared `command_name`, scan PATH directories in order and select
   the first executable regular file with that exact basename;
3. resolve the complete symlink chain to an executable regular file, rejecting
   cycles, escapes from the clean environment, or more than 40 links;
4. record exactly `{entrypoint_id, command_name, invoked_path, real_path,
   real_sha256}`; and
5. sort rows by `entrypoint_id`, requiring exactly one row per declaration,
   unique command names, and unique invoked paths. Multiple rows may resolve
   to the same real binary.

The declaration digest hashes the canonical declared array; the discovery
digest hashes the canonical discovery array. No filesystem executable absent
from the adapter declaration is inferred to be a host entrypoint.

The harness replaces every discovered `invoked_path` with a distinct wrapper
and installs a descendant-process deny monitor for every distinct
`real_sha256`. The wrapper or monitor atomically appends an event containing
`interception_kind` (`wrapper` or `direct-binary`), `entrypoint_id` (required
for wrapper; `null` for direct binary), host, invoked path, real path,
real SHA-256, `argv_sha256`, parent process id, and timestamp, then blocks the
real launch. A direct-binary event additionally requires its distinct real
path.

`argv_sha256` is SHA-256 of the exact canonical JSON array of exec-boundary
argv byte strings decoded as UTF-8; each decoded string is required already to
be NFC. The array uses the
same exact escaping, no whitespace, and no trailing LF; element order is
unchanged, `argv[0]` is the exact invoked executable path, and no shell
re-parsing or redaction occurs before hashing. Invalid UTF-8 makes the bundle
invalid. The harness retains every wrapper path/digest and entrypoint id, each
distinct real path/digest, monitor identity/deny-rule digest, and activation
time. Any missing wrapper/monitor coverage invalidates the bundle.

Each retained `state-*.json` validates against the versioned
`provision-state.v1.schema.json` authority and is the canonical state
document—not merely a digest carrier. It contains only
`schema_version`, `host`, `surface_id`, selected `route_id` and package state,
Kodhama catalog-registration state, `peer_selected_packages`,
`unselected_packages`, and `unselected_catalog_entries`. Peer-selected rows
are exactly the other request selections in the target and include requested
version/route plus observed state; unselected rows exclude the entire target
selection set. Both package arrays sort by `plugin_id`;
unselected catalog entries sort by `entry_name` and contain only entry name,
selector, installed identity, and selector fingerprint. Duplicate sort keys
are invalid. Secrets and volatile timestamps are excluded.

Before hashing, strings are Unicode NFC; object keys sort by Unicode code
point; JSON uses UTF-8 and spec 0001's exact quote/backslash/control-only
escaping, with no insignificant whitespace or trailing LF. Numbers are base-10
integers only. The state digest is SHA-256 of those exact bytes.

The same byte rules canonicalize bundle JSON. Request targets sort by
`(host, surface_id)`, their plugins by
`(plugin_id, package_version, route_id)`, state roots by host, and references
by reference id. Receipt results sort by numeric
`(target_index, plugin_index)`;
diagnostics sort by `(code, message)` and their reference ids lexicographically.
Launch events sort by
`(timestamp, interception_kind, entrypoint_id|null, real_sha256, real_path)`;
manifest file rows sort by path; evidence-index rows sort by bundle path.
Duplicate sort keys are invalid.

An observation occurs only after the provisioner and every descendant process
has exited and the host adapter has completed one fresh state read. Each
`harness.json` observation names one retained `state-*.json` path, its
SHA-256, the then-current `launch-events.json` SHA-256, and the then-current
run's `run-N.write-events.json` SHA-256 (or `null` for the initial observation).
Validators recompute each digest from the retained canonical document using
the named versioned schema and byte rules; no receipt or harness-stated digest
is trusted independently.

The exact harness sequence is:

1. create a clean environment; discover the exact entrypoint set; activate
   every wrapper, distinct-real-binary deny control, and process-tree write
   monitor; record empty launch events; and retain/observe
   `state-initial.json`;
2. run the provisioner once; require exact identity success and at least one
   `changed`, with explicit audit path `run-1.write-events.json`;
   retain/observe `state-run-1.json`; require launch events empty and every
   write allowed;
3. run the identical request immediately; require all
   `already-converged`, with explicit audit path
   `run-2.write-events.json`; retain/observe `state-run-2.json`; require its
   exact bytes equal `state-run-1.json`, launch events remain empty, and every
   write is allowed;
4. after run 2 and descendants exit, invoke every discovered wrapper exactly
   once with argv `[<wrapper-path>, "--kodhama-launch-probe"]`, in
   `entrypoint_id` order, then invoke every distinct real binary exactly once
   with argv `[<real-path>, "--kodhama-launch-probe"]`, in
   `(real_sha256, real_path)` order;
5. require the launch-event set to equal exactly one `wrapper` event for every
   discovery row plus one `direct-binary` event for every distinct
   `(real_sha256, real_path)`: no missing or extra event, exact
   entrypoint/path/digest and argv preimage, all blocked, all timestamped after
   both receipt `finished_at` values;
6. take the final canonical observation, canonicalize every JSON file with the
   same JSON rules, hash every non-manifest file, write `manifest.json`, hash
   its exact bytes, and add that digest to the sorted evidence index.

Only this exact bundle can promote its matching provisioner row to `verified`.
Offline doubles prove contract behavior but cannot replace retained clean-host
evidence. Local, CI, cloud/container, Claude Code, and Codex bundles remain
independent.

## Fixtures

The offline harness supplies deterministic Claude Code and Codex host doubles.

Positive fixtures:

| Fixture | Proves |
|---|---|
| `positive/claude-local/` | Claude Code local/bootstrap exact installation |
| `positive/codex-local/` | Codex local/bootstrap exact installation |
| `positive/claude-ci/` | Claude Code before headless CI launch |
| `positive/codex-ci/` | Codex before headless CI launch |
| `positive/claude-container/` | Claude Code cloud/container setup |
| `positive/codex-container/` | Codex cloud/container setup |
| `positive/dual-host/` | One explicit request for both hosts |
| `positive/explicit-route-selection/` | Requested route resolves one exact provisioner record |
| `positive/prerequisite-reference-map/` | Every route kind maps to the exact request-reference kind/id |
| `positive/idempotent-repeat/` | Second identical invocation changes nothing |
| `positive/explicit-version-change/` | Selected tuple converges exactly |
| `positive/shared-catalog-preserved/` | Allowed catalog change preserves unselected entries |
| `positive/partial-resume/` | Success remains and skipped/failed tuples retry |
| `positive/duplicate-result-identities/` | Duplicate inputs retain unique positional failed result ids |
| `positive/two-run-launch-intercept-bundle/` | Actual launch interception, canonical state digests, and immutable evidence layout |
| `positive/multi-entrypoint-controls/` | Every declared entrypoint and distinct real binary has exact positive-control coverage |
| `positive/retained-state-recompute/` | State and unselected fingerprints recompute from retained schema-valid documents |
| `positive/two-output-commit/` | A retained regular canonical schema-valid normal receipt binding the exact retained regular canonical audit path/digest is committed evidence regardless of writer or provable create/fsync/read-back history; the producer independently performs every sealing obligation |

Negative fixtures:

| Fixture | Required failure |
|---|---|
| `negative/default-family-set/` | Reject implicit plugin selection |
| `negative/duplicate-target-or-plugin/` | Reject non-unique request identities |
| `negative/environment-reference-grammar/` | Reject missing, duplicate, unused, secret-valued, or unsafe references |
| `negative/global-validation-attribution/` | Apply the first failing validation phase and exact tuple/envelope attribution |
| `negative/same-phase-multiple-errors/` | Preserve every assigned cause under the deterministic primary diagnostic |
| `negative/prerequisite-kind-map/` | Reject missing/wrong-kind mapped request reference |
| `negative/route-zero-or-multiple-match/` | Emit exact identity-resolution variant/code/exit for absent, unavailable, version-mismatched, or ambiguous route selection |
| `negative/version-range/` | Reject non-exact selection |
| `negative/host-surface-mismatch/` | Reject wrong host |
| `negative/mutable-only-resolution/` | Reject unresolved exact identity |
| `negative/pre-resolution-receipt-fields/` | Reject tag/commit/state fields on early failure |
| `negative/result-union-fields/` | Reject missing/forbidden route, adapter, state, change, diagnostic, or verification fields |
| `negative/missing-authentication/` | Fail before mutation with typed diagnostic |
| `negative/shared-prerequisite-skips/` | Emit every blocked tuple and deterministic aggregate exit |
| `negative/identity-mismatch-after-install/` | Fail verification |
| `negative/unselected-plugin-change/` | Restore catalog snapshot and fail preservation |
| `negative/rollback-failed/` | Report preservation breach, final state, failed change, and skip same-host remainder |
| `negative/skip-blocker-precedence/` | Reject any skipped phase/blocker other than the deterministic winning blocker |
| `negative/later-shared-node-ownership/` | Recompute ownership from only unassigned members and never reassign finalized results |
| `negative/outside-allowed-write/` | Fail when the provisioner process tree writes unselected config, other-host state, or a non-Kodhama catalog |
| `negative/agent-launched-by-adapter/` | Active interceptor detects and blocks pre-agent boundary violation |
| `negative/launch-interceptor-disabled/` | Reject evidence whose positive-control launch is not intercepted |
| `negative/entrypoint-discovery-set/` | Reject missing/extra declaration rows, unsafe PATH, incomplete symlink resolution, or missing per-entrypoint/distinct-binary controls |
| `negative/argv-digest-preimage/` | Reject altered argv order/path, non-NFC or invalid UTF-8, alternate escaping, whitespace, or trailing LF |
| `negative/state-digest-canonicalization/` | Reject alternate state projection, ordering, normalization, or observation timing |
| `negative/state-document-missing/` | Reject a digest without its retained schema-valid canonical state document |
| `negative/product-setup-invoked/` | Detect product operation |
| `negative/credential-in-output/` | Detect secret material |
| `negative/evidence-bundle-digest/` | Reject missing/changed/unindexed evidence |
| `negative/cross-surface-evidence/` | Reject another exact row's evidence |
| `negative/output-sealing-failure/` | Apply exact exit 7 behavior for producer parent/create/fsync/read-back/final-validation failures while classifying any retained normal/minimal evidence only from path/type/bytes/schema/digest |
| `negative/output-cleanup-identity/` | During one handled invocation, descriptor-unlink only its demonstrably partial/invalid audit or receipt or its orphan audit; preserve every pre-existing, foreign, identity-changed, uncertain, or committed output |
| `negative/audit-failure-receipt-replacement/` | Replace an uncommitted invalid/partial normal receipt with a minimal audit-seal-failed receipt only through identity-safe unlink plus exclusive-create at the stable leaf |
| `negative/abrupt-output-termination/` | At each abrupt boundary, classify retained evidence solely by path/type/bytes/schema/digest; preserve any valid normal/minimal witness as committed and treat invalid or uncertain remaining leaves as operator-owned pre-existing debris that later invocations never reclaim |
| `negative/ordinary-same-host-failure/` | Continue later same-host tuples unless an unrecovered preservation breach taints the host |

## Acceptance criteria

### Scenarios

**S1 — Claude Code local bootstrap**

Given an explicit Claude Code local target and valid environment references,
when the core runs, then it installs and verifies only the requested exact
releases and exits before Claude Code starts.

**S2 — Codex local bootstrap**

Given an explicit Codex local target and valid environment references, when
the core runs, then it installs and verifies only the requested exact releases
and exits before Codex starts.

**S3 — Headless CI**

Given an explicit Claude Code or Codex CI target, when the CI adapter runs
before the agent step, then the requested exact releases are verified before
the adapter returns.

**S4 — Cloud/container setup**

Given an explicit Claude Code or Codex cloud-container target, when the setup
adapter runs before launch, then it uses the same core and the active launch
interceptor records no attempt until after provisioner exit.

**S5 — Request uniqueness and environment grammar**

Given duplicate targets/plugins/references, missing host roots, unsafe paths,
unused references, or credential values, when request validation runs, then
exit `2` occurs before mutation with deterministic diagnostics.

**S6 — Early failure receipt**

Given an unresolved release, when provisioning ends before identity
resolution, then its failed result contains a diagnostic and forbids release
tag, commit, route, state, and verification fields.

**S7 — Shared prerequisite skip**

Given a shared prerequisite failure blocking two tuples and an independent
third tuple, when provisioning runs, then the lowest execution-key dependent
owns one failed result, the other dependent is skipped with its prerequisite
id and that owner result id, the independent tuple runs, and aggregate exit is
`6`.

**S8 — Exact identity**

Given only a mutable selector or non-exact version, when resolution runs, then
the tuple fails instead of installing the current mutable target.

**S9 — Idempotent repeat**

Given a successful request and its final state, when the identical request
runs again, then every tuple is `already-converged` and no package or shared
state changes.

**S10 — Selected convergence with preservation**

Given a selected plugin at another version and unselected installed plugins,
when convergence runs, then only the selected package and an allowed
preserving catalog projection may change; every other target selection is
classified peer-selected and fingerprinted, and any peer/unselected impact
fails and attempts catalog-snapshot restoration without emitting success.

**S11 — Partial failure and retry**

Given independent tuples where one succeeds and one fails, when the run and
identical retry complete, then the first success is retained/no-op, the failed
tuple retries, every result is present, and exit selection follows the fixed
precedence.

**S12 — Product boundary**

Given successful installation, when provisioning exits, then no product
setup/refresh, behavior check, or agent process has run.

**S13 — Evidence promotion**

Given a clean exact-surface first run and immediate identical repeat, when the
launch-intercept harness and evidence bundle validate, then only the matching
exact route is eligible for verified.

**S14 — Evidence mutation**

Given a verified route bundle, when any retained byte, digest, path, identity,
or index entry differs, then validation withdraws verification.

**S15 — Credential handling**

Given environment-owned credential references, when any receipt, diagnostic,
or evidence bundle is emitted, then no credential value appears.

**S16 — Explicit route and prerequisites**

Given a plugin selection with one route id and route prerequisites, when
request validation runs, then exactly one complete provisioner record with the
request/executing provisioner version resolves and each prerequisite id/kind
maps to exactly one selected request reference.

**S17 — Duplicate results and request blocker**

Given duplicate target or plugin values, when request validation fails, then
each decoded input position has a unique `tN.pN` result id, later duplicates
fail, and otherwise valid results are skipped by the request-validation blocker.

**S18 — Structural execution failure**

Given a failure after catalog registration, when the receipt is validated,
then it requires typed route, adapter, prior/final state, every shared catalog
change/rollback, and diagnostic while rejecting fields outside its union
variant.

**S19 — Unrecoverable preservation breach**

Given unexpected unselected catalog impact and failed snapshot restoration,
when rollback handling completes, then the tuple fails as a preservation breach,
records observed final state and rollback failure, and skips remaining
same-host tuples without claiming preservation.

**S20 — Actual launch interception and state digest**

Given an active wrapper/descendant monitor and canonical state observer, when
the two-run harness executes, then both runs have empty launch events and equal
post-run state documents, and deliberate post-run controls produce exactly one
blocked wrapper event per declared entrypoint plus one blocked direct event per
distinct real binary with the exact argv preimage.

**S21 — Global validation attribution**

Given an enumerable request with invalid UUID/version/environment/extra fields
and errors in later phases, when request validation runs, then only phase 1 is
reported, each decodable tuple is failed or skipped by its exact structural
scope, every remaining tuple uses the request-validation blocker, and no
mutation occurs.

**S22 — Deterministic skipped blocker**

Given multiple possible blockers for a tuple, when result construction runs,
then request validation wins over prerequisite, prerequisite wins over a prior
same-host taint result, the within-class tie break is fixed, and the skipped
phase and structural fields match the winning blocker.

**S23 — Observable preservation boundary**

Given a provisioner-process-tree write to unselected configuration,
other-host state, or a non-Kodhama catalog, when verification runs, then the
write event is classified outside the allowlist and the tuple fails without a
preservation claim.

**S24 — Exact receipt verification**

Given a successful tuple, when receipt validation runs, then discovery,
installed identity, immutable catalog selector, unselected before/after
fingerprints, allowed-write-set digest, and write-events digest all bind the
retained evidence and no extra verification field is accepted.

**S25 — Retained state authority**

Given a two-run evidence bundle, when its receipt or harness digests are
checked, then each digest is independently recomputed from the named retained
schema-valid state or write document and a missing canonical document
invalidates the bundle.

**S26 — Exact launch discovery set**

Given an exact host/adapter entrypoint declaration and clean PATH, when the
harness discovers and controls launch paths, then it selects the first exact
executable for every declaration, fully resolves it, covers every wrapper and
distinct real binary, and hashes exact NFC exec argv JSON bytes.

**S27 — Receipt/audit sealing**

Given retained output leaves after any producer outcome, when external output
validation runs, then a regular canonical schema-valid normal receipt at the
exact requested receipt path is committed evidence exactly when it binds the
exact requested path and SHA-256 of a retained regular canonical schema-valid
audit, a regular canonical schema-valid minimal receipt at that receipt path
is committed failure evidence under its audit-forbidding variant, and neither
classification depends on the writer or provable exclusive-create, fsync,
descriptor-read-back, or file-identity history.

**S28 — Same-phase error representation**

Given multiple validation errors assigned to one tuple in the first failing
phase or later execution class, when diagnostics are built, then exact
source/path/reference mappings apply and one result contains every cause
sorted by class rank with its primary code first.

**S29 — Later shared prerequisite ownership**

Given an earlier prerequisite node already finalized some members, when a
later node is evaluated, then only unassigned members determine shared
cardinality and ownership, a node with none is explicitly not executed, and
finalized results remain unchanged.

**S30 — Route lookup failures**

Given zero, unavailable, version-mismatched, or multiple route rows, when
route lookup runs between request phases 4 and 5, then the tuple uses the exact
identity-resolution failure code and exit class `3` without
route/adapter/later fields or mutation, only resolved routes feed phase 5, and
global phase 6 still evaluates all targets with exit `2` precedence; duplicate
or unknown target reference ids instead fail phases 3–4 before any lookup.

**S31 — Output sealing failure**

Given an output-parent, create/write/fsync/read-back/final-validation failure
or identity change, when recovery and termination run, then exit `7`
dominates, any retained valid bound normal or valid minimal receipt is
committed and never deleted despite producer failure, same-invocation
descriptor-relative cleanup touches only a demonstrably partial or invalid
invocation-created audit or receipt or its orphan audit, an uncertain output
is left operator-owned, and every invalid or uncertain leaf surviving abrupt
termination is pre-existing debris that later invocations never modify or
delete.

**S32 — Same-host continuation**

Given an ordinary failed tuple and a later independent tuple on the same host,
when execution continues, then the later tuple runs; given an unrecovered
preservation breach, then only that taint skips remaining same-host tuples.

### Requirements and invariants

- **R1:** The provisioner shall require explicit host, active surface, plugin,
  exact package version, and route-id selection.
- **R2:** The request shall enforce unique target, plugin, state-root,
  reference-id, and reference-locator identities.
- **R3:** The environment shall use only the enumerated typed reference kinds
  and shall contain no credential value.
- **R4:** The provisioner shall reject ranges, branches, `latest`, tags, and
  mutable-only identity resolution as package-version input.
- **R5:** Before mutation, the provisioner shall resolve the computed release
  tag and peeled full commit for each tuple.
- **R6:** Before mutation, the provisioner shall verify every declared route
  prerequisite through the exact prerequisite-id/reference-id/kind mapping.
- **R7:** The provisioner shall emit a conditional receipt for parse,
  validation, resolution, prerequisite, and execution failures.
- **R8:** When a tuple fails before identity resolution, its result shall
  forbid resolved identity, route, state, and verification fields.
- **R9:** Every enumerable tuple shall have exactly one changed,
  already-converged, failed, or skipped result with a unique positional result
  id.
- **R10:** When a shared prerequisite node fails, the provisioner shall fail
  its deterministic owner once and shall skip every other dependent with its
  own prerequisite id and the failed owner result id.
- **R11:** Aggregate exit shall follow the fixed order-independent precedence.
- **R12:** When matching selected state exists, the provisioner shall make no
  change and report already-converged.
- **R13:** When selected state differs, the provisioner shall change only that
  selected package and any preserving shared catalog projection.
- **R14:** Every successful tuple shall have no provisioner-process-tree write
  outside the explicit allowed write set, thereby preserving unselected
  and peer-selected package/configuration, other-host, and non-Kodhama catalog
  state against its own writes.
- **R15:** When shared catalog reconciliation could affect unselected state,
  the provisioner shall fail before mutation; when unexpected impact is
  observed, it shall attempt snapshot restoration, record the outcome, fail,
  and make no preservation claim if restoration fails.
- **R16:** The same host-neutral core shall serve local, headless CI, and
  cloud/container invocation for Claude Code and Codex.
- **R17:** Thin adapters shall contain no product logic and shall exit before
  agent launch.
- **R18:** The provisioner shall not run product setup, refresh, behavioral
  verification, or an agent process.
- **R19:** When a multi-target run partially succeeds, successful state shall
  remain and an identical retry shall resume idempotently.
- **R20:** Receipts, diagnostics, and evidence shall not contain credential
  values.
- **R21:** A verified route shall cite one immutable evidence bundle at the
  exact authority path for its complete key and provisioner version.
- **R22:** The retained harness shall require a changed clean first run, a
  no-change immediate repeat, byte-equal retained schema-valid final-state
  documents, empty active-interceptor events during both runs, and the exact
  per-entrypoint and per-distinct-real-binary control set only after both
  exits.
- **R23:** Evidence bundles and their index entries shall be content-hashed and
  immutable while referenced by verified state.
- **R24:** Evidence shall not flow across host, surface, environment, mode,
  plugin, release, route, or provisioner-version boundaries.
- **R25:** A successful receipt shall remain distribution evidence only and
  shall not assert product or effective support.
- **R26:** Each plugin selection shall resolve its explicit route id to exactly
  one matching candidate or verified provisioner record whose
  `provisioner_version` equals both the request and executing core version.
- **R27:** Receipt results shall conform to the exact discriminated union for
  their outcome and phase, including typed route, adapter, state, catalog
  changes, diagnostics, and verification.
- **R28:** When a shared catalog mutation occurs before failure, the result
  shall record the attempted change, every rollback, observed final state, and
  any rollback diagnostic.
- **R29:** Duplicate inputs shall retain distinct positional result identities,
  and request-wide skips shall use the request-validation blocker variant.
- **R30:** The evidence harness shall intercept every adapter-declared host
  launch entrypoint and every distinct resolved real binary and shall reject
  a bundle whose exact positive-control event set is missing or has an extra
  event.
- **R31:** State and evidence digests shall use the defined post-descendant-exit
  observation and canonical UTF-8 NFC JSON SHA-256 algorithm.
- **R32:** Global request validation shall stop at the first failing
  validation phase and shall apply the exact sorted envelope/tuple attribution
  table, including enumerable phase-1 UUID, version, environment, structural,
  and unknown-field failures.
- **R33:** A skipped result shall use the deterministic blocker precedence,
  tie break, phase, and structural field set.
- **R34:** Receipt verification shall match exactly one passed/failed union
  variant and shall bind discovery, installed identity, typed immutable
  selector, unselected-state fingerprints, allowed-write set, and write log.
- **R35:** The process-tree monitor shall observe and classify every
  non-exempt create, modify, rename, and delete and shall fail a tuple for any
  outside-allowed-write event.
- **R36:** Each evidence bundle shall retain the canonical initial, run-1, and
  run-2 state documents and complete run-1/run-2 write-event documents under their
  versioned schema authorities.
- **R37:** A validator shall recompute state, unselected-state, write-event,
  harness, and manifest digests from retained canonical documents rather than
  trusting a stated digest.
- **R38:** Launch discovery shall use the exact declared-entrypoint/PATH/
  symlink algorithm and shall produce exactly one sorted discovery row per
  declaration.
- **R39:** Every launch event shall hash the exact NFC UTF-8 argv JSON-array
  preimage with exact element order, escaping, and no whitespace or trailing
  LF.
- **R40:** The provisioner shall break receipt/audit self-reference by sealing
  a digest-free audit after monitoring quiesces, writing it once, hashing its
  read-back bytes, fully canonicalizing and schema-validating the normal
  receipt with that digest before leaf creation, and performing
  no-follow/exclusive-create, file-and-parent-fsync, descriptor-read-back, and
  producer identity checks before reporting output-sealing success; external
  commitment shall depend only on the retained exact requested paths,
  regular-file types, canonical bytes, schemas, and normal-receipt audit
  path/digest binding and shall not depend on writer or provable producer
  operation history.
- **R41:** A same-phase diagnostic shall contain every assigned cause exactly
  once and shall use the exact source/path/reference attribution and fixed
  code rank for request, route, prerequisite, execution, rollback, and output
  sealing.
- **R42:** Later prerequisite nodes shall choose ownership from only
  unassigned members, shall explicitly not execute when none remain, and shall
  never reassign or diagnose a finalized member.
- **R43:** Every route lookup failure shall use its exact
  identity-resolution variant/code and aggregate exit class, and route lookup
  shall complete before route-dependent request phase 5; phase 6 shall still
  run globally after phase 5 passes and exit `2` shall override route exit `3`
  for unused references, while duplicate/unknown target reference ids shall
  fail globally before route lookup.
- **R44:** When output parent/create/write/fsync/read-back/final validation
  fails, the provisioner shall terminate with exit `7`, shall descriptor-unlink
  only during that invocation and only a demonstrably partial or invalid
  invocation-created audit or receipt or its orphan audit, may replace an
  invalid or partial normal receipt with a minimal `audit-seal-failed` receipt
  only by unlink plus exclusive-create at the stable leaf, shall never delete
  a retained valid normal/minimal receipt or an output whose retained-state
  classification is uncertain, shall classify surviving invalid or uncertain
  abrupt-termination debris as operator-owned for later invocations, and
  shall never modify or delete a pre-existing, foreign, identity-changed,
  crash-debris, or committed output.
- **R45:** An ordinary same-host tuple failure shall not block later
  independent tuples; only an unrecovered preservation breach shall taint and
  block that host.

## Open questions

None.

## Rubric check

No dedicated spec-quality rubric or `.grove/config.toml` token exists.
Self-check used the local contract-author rules, `specs/README.md`,
`.grove/lifecycle.md`, and `.grove/versioning.md`.

| Check | Result | Evidence |
|---|---|---|
| Frontmatter, lifecycle, dependencies | PASS | Required fields and decision `implements` edge present; approved decision unpinned; metadata spec pinned at current `@v2` after rechecking the unchanged selector and availability types consumed here |
| Versioned amendment | PASS | Behavioral counter advanced to v2; section-level WHAT/WHY/SCOPE/POINTER/VALUE/CONFIDENCE delta is present; index and implementation/test tracking pins were updated |
| Required sections and grammars | PASS | S1–S32 are GWT; R1–R45 are EARS `shall` statements |
| Decision boundary | PASS | Exact pre-agent distribution is specified; product behavior/setup, selection defaults, agent launch, and release coordination remain excluded |
| F6 environment and uniqueness grammar | CLOSED | UUID, target/plugin uniqueness, typed roots/references, path/env grammars, and no-secret inputs are normative |
| F7 conditional receipt fields | CLOSED | Envelope and per-phase result tables define required/forbidden identity, state, verification, and diagnostics |
| F8 aggregate exit and skipped tuples | CLOSED | Canonical tuple order, explicit skipped results, blocker links, and order-independent exit precedence are defined |
| F9 selected versus unselected state | CLOSED | Selected package plus preserving catalog projection is the only mutable scope; preservation conflict and snapshot restore are explicit |
| F10 retained evidence authority | CLOSED | Exact directory/files/index, content hashes, two-run state observations, and launch-intercept evidence are normative |
| F11 local host fixtures | CLOSED | Claude Code and Codex local/bootstrap positive fixtures and GWT scenarios are present |
| Pass-2 F4 prerequisite mapping | CLOSED | Route prerequisite ids/kinds map one-to-one to selected request reference ids and enumerated kinds |
| Pass-2 F5 route selection | CLOSED | Every plugin request carries `route_id` and must resolve exactly one complete candidate/verified record |
| Pass-2 F6 duplicate result identity | CLOSED | Positional result ids preserve duplicates; request-validation is an explicit blocker union variant |
| Pass-2 F7 receipt structure | CLOSED | Route, adapter, state, catalog-change, diagnostic, verification, and failed-shared-change types are conditionally structural |
| Pass-2 F8 preservation/rollback | CLOSED | Preservation is a success condition; restored conflict and unrecoverable breach are distinct recorded failures |
| Pass-2 F9 launch/digest proof | CLOSED | Active wrapper plus descendant monitor, post-run positive control, quiescent observation, canonical state bytes, and SHA-256 are normative |
| Final F3 receipt/selector/fingerprint grammar | CLOSED | Exact verification union, typed spec-0001 selector, canonical unselected preimage, and catalog-change before/after digests are normative |
| Final F4 global validation attribution | CLOSED | Two-stage six-phase precedence with the route boundary, same-phase sort, and exact envelope/tuple attribution cover unsafe paths, roots, refs, and host/surface mismatches |
| Final F5 skip blocker/phase | CLOSED | Three-class blocker precedence, tie breaks, permitted skipped phases, and structural fields are exact |
| Final F6 preservation observability | CLOSED | Claim is explicitly limited to provisioner-process-tree writes; complete write events plus selected-host snapshots cover that boundary |
| Final F7 canonical retained state | CLOSED | Versioned schema authorities and retained initial/run-1/run-2/write documents permit independent digest recomputation |
| Final F8 launch discovery/argv | CLOSED | Declared set, PATH/symlink algorithm, wrapper/distinct-binary coverage, exact control set, and argv digest preimage are normative |
| Final-pass F2 audit sealing | CLOSED | Exact output exemptions and monitor-stop → digest-free audit → read-back hash → receipt ordering remove self-reference |
| Final-pass F3 enumerable phase-1 attribution | CLOSED | UUID, version, environment, extra-field, target, and plugin schema failures have deterministic envelope/tuple results |
| Final-pass F4 shared prerequisites | CLOSED | Shared-node identity, single deterministic owner failure, dependent blocker graph, and independent execution are exact |
| Final-pass F5 peer-selected preservation | CLOSED | Every other target selection is classified and included in tuple state/fingerprints; prior state refresh prevents cross-tuple false breaches |
| Final-pass F6 provisioner-version identity | CLOSED | Route eligibility and request/core/record/receipt/bundle/index/availability evidence require one exact provisioner version |
| Intrinsic F4 same-phase diagnostics | CLOSED | Exact all-class code ranks, source/path/reference mapping, cause sorting, single-result representation, and no-duplicate attribution are normative |
| Intrinsic F5 later shared ownership | CLOSED | Node evaluation filters finalized members, explicitly does not execute with none, and never reassigns outcomes |
| Intrinsic F6 route lookup failures | CLOSED | Duplicate/unknown target refs fail pre-route; lookup occurs before route-dependent phase 5; phase 6 remains global across route failures with exit-2 precedence |
| Intrinsic F7 sealing failures | CLOSED | Parent/create/write/fsync/read-back/receipt failure paths distinguish minimal receipt from impossible receipt and use exit 7 |
| Intrinsic F8 same-host continuation | CLOSED | Ordinary failures continue; only restore-failed preservation breach taints and blocks the host |
| v2 two-output commit and cleanup | CLOSED | Retained path/type/canonical-byte/schema/digest state alone defines the normal/minimal receipt witness; cleanup authority is same-invocation and limited to demonstrably partial/invalid uncommitted leaves; abrupt debris becomes operator-owned |
| v2 adversary F1 durable witness | CLOSED | External commitment is independent of writer and provable exclusive-create/fsync/read-back/identity history; those facts remain producer obligations and diagnostics only |
| v2 adversary F2 crash recovery | CLOSED | Recovery preserves every valid retained witness, leaves uncertain state operator-owned, and treats surviving invalid debris as pre-existing without reclaiming it |
| Whole-corpus validation | NOT CLAIMED | Issue #20 blocks literal full-corpus PASS; this artifact uses strict YAML/exact ids and was checked change-scoped |

**Result: PASS for author self-check.**

## Gate record

On 2026-07-24 the maintainer approved v1 after spec-adversary
`APPROVE-READY` and conformance `PASS` against approved decision 0016. This v2
amendment passed the author self-check above and is `gated`; the prior v1 act
is not reused as approval of the amended S27/S31 or R40/R44 output contract.
