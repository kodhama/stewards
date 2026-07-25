---
id: kodhama-spec-0003-marketplace-test-observation
type: spec
status: approved  # maintainer approved checkpoint 1 on 2026-07-24
depends_on: [kodhama-0017-retire-family-release-certification]
implements: [kodhama-0017-retire-family-release-certification]
owner: agent
updated: 2026-07-24
version: 1
---

# Marketplace test observation

## Scope

This specification defines one closed record for the narrow fact authorized by
`kodhama-0017`: a product-owned GitHub Actions run configured one exact
marketplace checkout through Claude Code or Codex.

The record identifies the host, product-defined surface, canonical marketplace
source, resolved revision, and workflow execution. It does not identify a
plugin, claim that a plugin was installed or behaved correctly, state that the
product supports the surface, or approve a release. Those conclusions and
their evidence remain in the product repository.

There is no central Stewards registry. A product retains the record beside its
own test evidence or links it from product-owned surface metadata.

## Record

The canonical JSON shape is:

```json
{
  "schema_version": 1,
  "host": "codex",
  "surface_id": "github-actions/codex-marketplace",
  "marketplace": {
    "name": "kodhama",
    "repository": "kodhama/stewards",
    "revision": "0123456789abcdef0123456789abcdef01234567"
  },
  "execution": {
    "repository": "kodhama/trellis",
    "commit": "89abcdef0123456789abcdef0123456789abcdef",
    "workflow": ".github/workflows/ci.yml",
    "job": "codex-marketplace",
    "run_id": 123456789,
    "run_attempt": 1,
    "setup_step_id": "kodhama_marketplace_kodhama_codex"
  },
  "observed_at": "2026-07-24T12:34:56.789Z"
}
```

The object and all nested objects are closed: unknown properties are invalid.
Every shown property is required.

| Field | Contract |
|---|---|
| `schema_version` | Integer `1`. This is the observation-schema version. |
| `host` | Exactly `claude` or `codex`. |
| `surface_id` | Product-owned stable identifier matching `^[a-z0-9][a-z0-9._/-]{0,127}$`. |
| `marketplace.name` | Nonblank host-native marketplace name, at most 128 UTF-8 bytes. |
| `marketplace.repository` | GitHub `owner/repository` matching `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`. Its canonical source is derived as `https://github.com/{marketplace.repository}.git`. |
| `marketplace.revision` | Exact 40-character lowercase hexadecimal commit resolved by the setup step. |
| `execution.repository` | GitHub `owner/repository` matching `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`. |
| `execution.commit` | Exact 40-character lowercase hexadecimal product commit tested by the run. |
| `execution.workflow` | Repository-relative path below `.github/workflows/`, ending in `.yml` or `.yaml`, with no `..` segment. |
| `execution.job` | Exact nonblank GitHub Actions job key, at most 128 UTF-8 bytes. |
| `execution.run_id` | Positive GitHub Actions run id. |
| `execution.run_attempt` | Positive attempt number for that run id. |
| `execution.setup_step_id` | Exact generated marketplace-setup step id matching `^[A-Za-z_][A-Za-z0-9_-]{0,127}$`. |
| `observed_at` | Real UTC instant in millisecond-precision `YYYY-MM-DDTHH:mm:ss.sssZ` form. |

The canonical run URL is derived, not stored:
`https://github.com/{execution.repository}/actions/runs/{execution.run_id}/attempts/{execution.run_attempt}`.

## Runtime provenance

An observation is emitted by the host-specific setup step in the named run,
not authored from workflow YAML or reconstructed later.

Before emitting it, that step shall:

1. read the checkout's `origin` with `git remote get-url origin`, normalize
   only an optional terminal `.git`, and fail unless it equals
   `https://github.com/{marketplace.repository}`;
2. read the checkout's actual commit with `git rev-parse HEAD`;
3. fail unless it exactly equals the caller-selected immutable revision;
4. invoke the selected host's marketplace-add command against that verified
   local checkout;
5. fail unless the host command succeeds and the host's machine-readable
   marketplace listing contains `marketplace.name` rooted at that checkout;
6. populate the execution fields from GitHub Actions runtime variables and the
   known workflow/job/step identifiers; and
7. when the product selected observation output, write the record to that
   deterministic product-owned artifact path.

If any input, command, lookup, or runtime variable is absent or inconsistent,
the step fails and emits no observation. A workflow edit, dry run, generated
command, catalog row, marketplace registration without the verified local
checkout, or intended future run is not an observation.

The observation schema has two validation boundaries:

- **structural validation** is offline and checks the closed shape, field
  constraints, and derived URL only; it does not query GitHub or authenticate
  a run; and
- **provenance validation** is the runtime procedure above. Products retain
  the generated record as a run artifact and own its access, retention, and
  any later authentication against GitHub.

An unavailable API, expired artifact, or insufficient authorization therefore
does not turn structural validation into a false outcome. It means external
run provenance cannot presently be re-authenticated, and consumers must say
so rather than infer success.

The record has no plugin coordinate/version, result, support, availability,
approval, release, or qualification field. Consumers must not infer any such
state from the record's existence.

## Consumer integration boundary

Products own package identity and may independently adopt Grove's pattern of a
SemVer `VERSION` file, host-specific Claude and Codex plugin manifests, and
version-bound product surface metadata. This specification neither requires
those files nor validates parity among them. No relation exists between
different products' versions or release timing.

## Acceptance criteria

### Scenarios

**S1 — Claude observation**

- **Given** a product-owned GitHub Actions setup step with an exact marketplace
  checkout that invokes Claude's marketplace-add command and a
  product-selected observation output,
- **When** the checkout SHA, host registration, and machine-readable listing
  all verify,
- **Then** the step emits the closed record with `host: "claude"` and runtime
  identifiers from that attempt.

**S2 — Codex observation**

- **Given** the equivalent verified Codex setup with a product-selected
  observation output,
- **When** the same provenance checks pass,
- **Then** the same record shape uses `host: "codex"` and introduces no
  Claude-specific field.

**S3 — Authored but unexecuted workflow**

- **Given** a workflow containing marketplace setup that has not run,
- **When** an agent considers producing an observation,
- **Then** no observation exists because static configuration is not runtime
  provenance.

**S4 — Marketplace fact remains narrow**

- **Given** a valid observation whose later plugin test failed, passed, or was
  inconclusive,
- **When** a consumer reads the observation alone,
- **Then** the consumer learns only which exact marketplace checkout the host
  registered and derives no plugin, behavior, support, qualification, or
  release state.

**S5 — Source or revision mismatch**

- **Given** a checkout whose normalized origin differs from the selected
  repository or whose actual HEAD differs from the selected revision,
- **When** the setup step validates provenance,
- **Then** the step fails before host registration and emits no observation.

**S6 — Host listing mismatch**

- **Given** a successful marketplace-add command whose machine-readable list
  does not contain the expected name rooted at the verified checkout,
- **When** the setup step validates provenance,
- **Then** it fails and emits no observation.

**S7 — Offline structural validation**

- **Given** a retained record and no GitHub API access,
- **When** structural validation runs,
- **Then** it deterministically accepts or rejects the closed shape without
  claiming that the external run was authenticated.

### Requirements

- **R1 (ubiquitous):** Every observation shall use the exact closed version-1
  shape and field contracts above.
- **R2 (event-driven):** When a product selected observation output and the
  exact checkout source/revision, host registration, and machine-readable host
  listing all verify in one setup step, that step shall emit one observation
  from runtime values.
- **R3 (unwanted behavior):** If any runtime provenance check fails, no
  observation shall be emitted.
- **R4 (ubiquitous):** An observation shall contain no plugin, result, support,
  availability, approval, release, qualification, or effective-state field.
- **R5 (ubiquitous):** Offline structural validation shall reject any absent,
  unknown, malformed, or internally inconsistent field without querying
  external services.
- **R6 (state-driven):** While external run evidence is unavailable or cannot
  be authenticated, consumers shall report provenance as unverified and shall
  not convert that state into a pass or failure conclusion.
- **R7 (ubiquitous):** Products shall own observation storage, run artifacts,
  product evidence, behavioral conclusions, and any integration with product
  surface metadata.

## Open questions

None.

## Rubric check

No dedicated spec rubric or `.grove/config.toml` exists. Against
`specs/README.md`, the contract-author role, and the installed lifecycle and
versioning companions: required frontmatter is complete; the only behavioral
upstream is approved and declared through `depends_on` and `implements`;
version `1` is initialized; structural and provenance validation are explicit
and testable; both GWT and EARS acceptance grammars are present; and no
unresolved design choice is hidden. Result: **PASS**, promoting this artifact
from `draft` to `gated`.

This is a change-scoped self-check only. It does not claim that the malformed
legacy metadata tracked by issue #20 has been repaired or that the full corpus
passes strict validation.

## Lifecycle record

The maintainer explicitly approved checkpoint 1 on 2026-07-24 after the spec
adversary returned `APPROVE-READY`, the conformance reviewer returned `PASS`,
and the change-scoped corpus review returned `PASS`. The `approved` status
records that human spec-gate act.
