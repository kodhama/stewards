---
id: kodhama-spec-0004-ci-marketplace-setup-skill
type: spec
status: superseded  # by kodhama-0030, 2026-08-29 — the skill this spec contracts was deleted with plugins/kodhama/
superseded_by: [kodhama-0030-install-door-serves-trellis-only]  # maintainer intent act 2026-08-29, in session
depends_on: [kodhama-0017-retire-family-release-certification, kodhama-0018-stewards-dual-host-plugin-package, kodhama-0020-name-overarching-plugin-kodhama]
implements: [kodhama-0017-retire-family-release-certification, kodhama-0018-stewards-dual-host-plugin-package, kodhama-0020-name-overarching-plugin-kodhama]
owner: agent
updated: 2026-07-27
version: 5
---

# GitHub Actions marketplace-setup skill

> **Superseded by `kodhama-0030-install-door-serves-trellis-only`**
> (2026-08-29). `plugins/kodhama/skills/setup-ci-marketplace/` is deleted,
> along with the fixture corpus and authoring tests that made this contract
> checkable. The workflow it authored,
> `.github/workflows/validate-marketplace-setup.yml`, survives as a
> hand-maintained file. Nothing implements this spec.

> **AMENDED 2026-07-27 — v4 → v5 (`kodhama-0025`)**
>
> **WHAT:** Removed `surfaces.json` as a version carrier, the optional
> observation inputs and emission step, and the surface-parity halves of
> R16-R17. The skill's actual job — authoring marketplace registration in
> caller-selected GitHub Actions jobs — is unchanged.
>
> **WHY:** `kodhama-0025` retired the surface matrix and the
> marketplace-observation record family-wide. Leaving this spec `approved` while
> the machinery was deleted would let an implementer following the authoritative
> contract reintroduce a deleted schema, or generate observation behaviour the
> shipped skill no longer supports.
>
> **SCOPE:** Reference reconciliation. No authoring behaviour changes.

> **Amended 2026-07-25 — decision 0020**
>
> **WHAT:** Renamed the public dual-host plugin, package source, skill
> namespace, generated identifiers, and managed checkout namespace from
> Stewards to Kodhama; made the local marketplace argument explicitly
> relative and bound registration run steps to the GitHub workspace root.
>
> **WHY:** The maintainer chose Kodhama as the overarching plugin identity,
> and exact Claude Code `2.1.199` and Codex CLI `0.145.0` runs rejected the
> v1 bare dot-directory argument as a non-local marketplace source.
>
> **SCOPE:** Plugin exposure and carrier parity, catalog-admission fixture
> paths, canonical generated block ownership, command adapter, convergence,
> package acceptance, and dependent test/index pins.
>
> **POINTER:** Issue #14 hosted validation and
> `kodhama-0020-name-overarching-plugin-kodhama`.
>
> **VALUE:** A consumer invokes one consistently named Kodhama skill whose
> generated setup resolves the verified marketplace checkout regardless of
> caller working-directory defaults.
>
> **CONFIDENCE:** verified.

## Scope

This specification defines one Stewards-owned authoring skill for
repository-owned GitHub Actions workflows. The skill locates caller-selected
jobs that invoke Claude Code, Codex, or both and adds an exact, host-native
marketplace registration before those invocations.

The skill edits workflow configuration. It is not installed into or invoked by
the resulting CI job. It provides no shared action, provisioner runtime,
container image, host-home service, credential broker, CLI installer, plugin
installer, test runner, release engine, or support resolver.

Product jobs continue to own plugin selection, plugin installation, harness
invocation, assertions, and evidence. The skill must behave identically whether
Claude Code or Codex invokes it; the invoking host is never evidence of which
host a target job uses.

## Kodhama plugin exposure

The skill is exposed from the independently versioned Kodhama plugin defined
by `kodhama-0018` and renamed by `kodhama-0020`:

- `plugins/kodhama/VERSION`;
- `plugins/kodhama/.claude-plugin/plugin.json`;
- `plugins/kodhama/.codex-plugin/plugin.json`;
- `plugins/kodhama/skills/setup-ci-marketplace/SKILL.md`.

The plugin's Claude and Codex manifest versions shall equal its own SemVer
`VERSION`. *(v5: `surfaces.json` was a third carrier; `kodhama-0025` retired it.)*

The Claude catalog is `.claude-plugin/marketplace.json`; the Codex catalog is
`.agents/plugins/marketplace.json`. An admitted Claude entry uses the relative
source string `"./plugins/kodhama"`. An admitted Codex entry carries exactly
these host-specific fields, plus a `description` and nothing else:

```json
{
  "name": "kodhama",
  "source": {
    "source": "local",
    "path": "./plugins/kodhama"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Developer Tools"
}
```

> **Amended 2026-07-27 — v2 → v3.** The prior text required a hand-written
> six-part smoke report at
> `plugins/kodhama/reference/surfaces/<host>-catalog-admission-<version>.md`,
> proving among other things that invoking the skill on
> `plugins/kodhama/tests/fixtures/direct-cli-workflow.yml` matched a recorded
> expectation. **Neither path has ever existed**, so the requirement could not be
> met. It stayed invisible because the enforcing branch fires only when a
> `kodhama` catalog entry is present, which it never has been — so publishing the
> plugin would have failed CI on an artifact nobody could produce. Replaced with
> evidence that runs. Scope unchanged: this narrows *how* admission is evidenced,
> not *whether* it must be, which `kodhama-0018` §3 governs.

> **Amended 2026-07-27 — v3 → v4.** The prior text said an admitted Codex entry
> "uses this **exact** host-specific subset", which the validator implemented as
> whole-object equality — rejecting a `description`, the very field the sibling
> `trellis` and `wisp` Codex entries carry and the only place this repository
> discloses that support is not claimed. The word was doing two jobs at once:
> "exact" (no other fields) and "subset" (these fields, among others). It is now
> split — the four fields are exact, `description` is required, everything else
> is rejected — and S10 and R18 below follow it. **Why closed rather than open:**
> Codex 0.145.0 accepts unknown entry fields silently, so a misspelled
> `"instalation"` would reach neither a subset check nor the host. **Why
> `description` is required:** `kodhama-0021` §2 admits a dogfood or preview
> listing only when "the listing or linked product documentation clearly
> discloses that support is not claimed", and no other carrier for that
> disclosure exists in this repository.

Catalog admission is governed by decisions 0012 and 0018, not inferred by the
parity validator. `kodhama-0018` §3 requires admission to be a separate evidenced
act and permits that evidence to be "a bounded host-native package and skill
invocation test" kept in this repository and reviewed with the catalog change.

A catalog-changing PR shall retain `scripts/keyless_admission_check.py` green.
It installs the built payload through the real Claude plugin path and asserts:

1. the host validates the plugin manifest with no warnings;
2. an isolated fresh host state added a local marketplace carrying that payload;
3. the host installed the plugin from it; and
4. the host's component inventory matches the plugin's declared skill
   directories.

The check requires no API key and runs no model turn, so it is a pull-request
gate rather than an occasional ritual.

**What it does not establish.** It proves package validity, catalog install, and
declared-skill exposure. It does **not** prove the skill *runs* — measured, not
assumed: the host lists a skill directory in its inventory even when `SKILL.md`
carries no frontmatter, so this is a layout check rather than a load check.
Behavioural proof needs a model turn. `kodhama-0018` §3 says the evidence "may
be" an invocation test, not that it must be; this meets the package half and
leaves the invocation half openly unmet.

Codex has no keyless equivalent — `codex mcp list` and `codex plugin` read
configuration without launching anything — so no Codex admission evidence is
required here, and a Codex catalog entry rests on `kodhama-0012`'s boundary
alone. Repository parity checks the shape of present entries but does not decide
whether an absent entry is ready for admission.

## Supported authoring target

Version 2 supports GitHub Actions jobs with direct Claude Code `2.1.199` or
Codex CLI `0.145.0` invocations and GitHub-hosted Git marketplace repositories.
Host actions that install and invoke a CLI inside one opaque action step are
detected but unsupported in version 2: the skill does not split, wrap, or guess
their host-specific inputs. It uses an exact local checkout as the common
immutable boundary because the two host CLIs do not expose the same remote
pinning interface.

The generated block uses:

1. `actions/checkout@<immutable-commit>` with the caller-selected marketplace
   `repository`, full 40-character `ref`, deterministic local `path`, and
   `persist-credentials: false`;
2. `git -C <path> rev-parse HEAD` and an exact comparison with the selected
   revision before registration;
3. `claude plugin marketplace add ./.kodhama/marketplaces/<m> --scope local`
   followed by
   `claude plugin marketplace list --json` for Claude; or
4. `codex plugin marketplace add ./.kodhama/marketplaces/<m> --json`
   followed by
   `codex plugin marketplace list --json` for Codex.

The host listing must be parsed and must contain the requested marketplace
name rooted at the verified checkout. For Claude, the root is the string value
of `path`, falling back to `installLocation` only when `path` is absent. For
Codex, it is the string value of `root`. The setup step resolves that value and
the checkout path with the host filesystem's real-path operation and requires
byte-identical absolute results. An absent, non-string, nonexistent, or
non-matching root fails. No other listing field is accepted. Command success
alone is insufficient.

This command mapping and the two exact CLI versions are the version-2 adapter.
The skill determines compatibility offline from the caller-owned pinned
install declaration; it does not launch either host while authoring. It shall
not substitute a remembered command or silently fall back to a mutable remote
ref. Any other or unprovable CLI version is unsupported and remains unchanged
until this contract or its implementation adapter is updated.

## Caller inputs

Before editing, the skill shall resolve and echo this plan for confirmation:

| Input | Contract |
|---|---|
| Repository root | One trusted local Git repository whose `.github/workflows/` tree is in scope. |
| Target selection | Explicit workflow/job keys, or permission to detect candidates for caller confirmation. |
| Host selection | `claude`, `codex`, or both for each target job, derived from unambiguous job content or supplied explicitly by the caller. |
| Marketplace name | Exact expected host-native catalog name matching `^[a-z0-9][a-z0-9-]{0,63}$`. |
| Marketplace repository | Exact GitHub `owner/repository`; its only canonical URI is `https://github.com/{owner}/{repository}.git`. |
| Marketplace revision | Full 40-character lowercase commit SHA. Branches, tags, and floating refs are invalid. |
| Checkout action | Existing caller-approved full 40-character commit pin for `actions/checkout`; tags and branches are invalid. |
| CLI prerequisite | Existing repository-owned step/action that provisions exactly Claude Code `2.1.199` or Codex CLI `0.145.0` before the generated block. |
| Host-state environment | Exact caller-confirmed environment mapping inherited by the host invocation. Empty means both setup and invocation use the job's default state. |

The skill shall not choose a product or plugin from catalog contents, install a
plugin or CLI, infer a version, create credentials, or choose a CI test.

## Workflow discovery and classification

The editable set consists only of `.yml` and `.yaml` files below the trusted
repository's `.github/workflows/` directory.

The skill may classify a job from:

- an unambiguous direct `claude` or `codex` CLI invocation; or
- a repository-local reusable workflow reached by a selected caller.

An official or third-party action that performs its own host invocation is
reported as an unsupported candidate, not classified as a direct-CLI target.
An external reusable workflow is always read-only and out of scope. An opaque
local wrapper, dynamically constructed command, unpinned CLI prerequisite,
conflicting host state, or conflicting caller configuration is ambiguous. The
skill shall report the affected workflow/job and make no edit to that target;
caller input cannot make an external workflow repository-owned.

A selected target is also ambiguous when the relevant CLI prerequisite,
first product-owned plugin-install step, or first host invocation carries a
step-level `if:` condition. Version 2 does not copy, combine, or attempt to
prove condition equivalence. A job-level `if:` remains supported because it
governs the generated and caller-owned steps together and is preserved
unchanged.

The skill may patch a repository-local reusable workflow only after inspecting
every repository-local caller and confirming that every caller is selected and
supplies identical marketplace and host-state inputs. Otherwise
it leaves the callee and all callers unchanged and reports the shared-callee
conflict. It never inserts marketplace setup into a caller job as a substitute
for setup inside a separately executing reusable-workflow job.

## Canonical generated block

For marketplace slug `<m>` and host `<h>`, the owned identifiers and names are:

- checkout: `id: kodhama_marketplace_<m>_checkout`;
- host registration: `id: kodhama_marketplace_<m>_<h>`; and
- checkout name: `Kodhama marketplace: checkout <m>`;
- Claude name: `Kodhama marketplace: register <m> for Claude`; and
- Codex name: `Kodhama marketplace: register <m> for Codex`.

The checkout path is `.kodhama/marketplaces/<m>`. The skill validates that
`<m>` is the lowercase marketplace name with each hyphen preserved and rejects
any name that cannot form the identifiers above.

One checkout is shared when both hosts in the same job use the same marketplace
and revision. Each host gets its own registration step. Registration steps:

- run after the exact checkout and after that host's caller-owned CLI
  prerequisite;
- run before the first corresponding host or product-owned plugin-install
  invocation;
- set `working-directory: ${{ github.workspace }}` so the managed checkout
  remains workspace-rooted even when the caller declares a job or workflow
  `defaults.run.working-directory`;
- inherit the job environment plus the exact caller-confirmed host-state
  mapping used by the later invocation;
- read the checkout origin, remove only one optional terminal `.git`, and
  require exact equality with `https://github.com/<owner>/<repository>`;
- require the checkout HEAD to equal the selected revision before calling the
  host;
- call only the version-2 commands above;
- parse the machine-readable listing and fail if name or root differs.

The skill parses existing YAML and compares the owned steps against the
confirmed plan: exact ids/names, checkout action commit, checkout inputs,
dependency order, workspace-root working directory, host command sequence, and
environment mapping. A semantic match is converged and the skill writes no file,
so the existing bytes
remain unchanged. An owned id with differing semantics, or an unowned block
that appears equivalent, is a conflict: preserve it, make no target edit, and
report the collision. Field order, quoting, indentation, and unrelated comments
are not convergence inputs. The skill never adopts, rewrites, or deletes
caller-owned setup implicitly.

## Authoring behavior

For every confirmed target, the skill shall:

1. preserve workflow triggers, permissions, concurrency, environments,
   secrets, matrices, conditions, timeouts, and unrelated steps;
2. configure only the selected host or hosts through the canonical block;
3. preserve the caller-owned pinned CLI prerequisite and plugin/test steps;
4. create no shared Claude/Codex state and copy no authentication, trust, or
   session material between hosts;
5. expose no secret value in generated YAML, comments, logs, or its report;
6. preserve comments and formatting outside the smallest inserted step
   sequence; and
7. write no file when the parsed owned steps already match the confirmed plan.

For a job that intentionally uses both hosts, Claude and Codex registration
remain separate and each binds only to its own confirmed state. A successful
registration for one host does not satisfy the other.

## Report

After editing, the skill shall report:

- every inspected workflow;
- every changed workflow and job;
- the host classification for every selected job;
- the marketplace name, repository, and immutable revision per host;
- the existing pinned CLI prerequisite and confirmed host-state mapping;
- the generated checkout and host step ids;
- every ambiguous, external, conflicting, unsupported, or skipped target and
  why; and
- whether the invocation changed files or was already converged.

The authoring invocation shall not launch a host, run or judge a product test,
install a plugin or emit support state.

## Consumer packaging boundary

This contract does not define a family plugin version or package layout.
Products may independently adopt Grove's approach of a SemVer `VERSION` file,
dual host manifests, and product-owned surface metadata through their own
decisions. Versions, bump choices, carrier parity, releases, tests, and support
claims remain independent for every product.

## Acceptance criteria

### Scenarios

**S1 — Claude-only job**

- **Given** a confirmed job with a pinned compatible Claude CLI prerequisite,
  exact marketplace revision, and unambiguous Claude invocation,
- **When** the skill authors setup,
- **Then** it inserts the exact checkout and Claude registration block before
  caller-owned plugin/test steps and installs no plugin.

**S2 — Codex-only job**

- **Given** the equivalent Codex job,
- **When** the skill authors setup,
- **Then** it inserts the exact checkout and Codex registration block and
  installs no plugin.

**S3 — Mixed-host job**

- **Given** one confirmed job that invokes both hosts with compatible pinned
  CLIs and one marketplace revision,
- **When** the skill authors setup for both,
- **Then** it shares one verified checkout and creates independent host
  registration steps without sharing host state.

**S3a — Caller working-directory defaults**

- **Given** a selected job or workflow whose caller-owned
  `defaults.run.working-directory` is not the repository root,
- **When** the skill authors marketplace registration,
- **Then** each generated registration step overrides its working directory to
  `${{ github.workspace }}` and resolves `./.kodhama/marketplaces/<m>` to the
  checkout action's workspace-rooted path.

**S4 — Invoker independence**

- **Given** the same repository and confirmed plan,
- **When** Claude Code and Codex independently invoke the skill,
- **Then** both produce the same target classification and semantically
  equivalent owned steps; YAML presentation may follow the existing file.

**S5 — Local reusable workflow**

- **Given** every repository-local caller of one local reusable workflow is
  selected with identical inputs,
- **When** the skill authors setup,
- **Then** it patches the local callee once.

**S6 — Shared or external reusable workflow**

- **Given** an unselected or conflicting caller of a local callee, or any
  external reusable workflow,
- **When** the skill classifies the target,
- **Then** it changes neither caller nor callee and reports the exact reason.

**S6a — Opaque host action**

- **Given** a job whose first Claude or Codex invocation occurs inside a host
  action,
- **When** the skill classifies the job,
- **Then** it makes no edit and reports that action-native configuration needs
  a later adapter contract.

**S6b — Conditional insertion boundary**

- **Given** a selected job whose relevant CLI prerequisite, first
  product-owned plugin-install step, or first host invocation carries a
  step-level `if:` condition,
- **When** the skill classifies the job,
- **Then** it makes no edit and reports that version 2 cannot safely preserve
  the conditional insertion boundary.

**S7 — Idempotent repeat**

- **Given** a canonical owned block already equal to the confirmed plan,
- **When** the skill runs again,
- **Then** it writes no file, preserving every byte, and reports that the
  target was converged.

**S8 — Existing unowned equivalent**

- **Given** caller-owned steps that appear to perform equivalent setup,
- **When** no exact Kodhama-owned canonical block exists,
- **Then** the skill preserves the steps, makes no target edit, and reports a
  collision rather than duplicating or adopting them.

**S9 — Authoring is not evidence**

- **Given** a successfully edited workflow that has not run,
- **When** the skill completes,
- **Then** it emits no test result and no support claim.

**S10 — Dual-host package parity**

- **Given** the Kodhama plugin's `VERSION`, two host manifests,
  and zero, one, or two catalog entries,
- **When** repository parity validation runs,
- **Then** the three version carriers match, both manifests name `kodhama`,
  every present Claude or Codex entry uses its exact local source shape and
  carries a nonblank `description`, a present Codex entry carries no field
  beyond those, and no other product version is read or compared.

**S11 — Runtime source or revision mismatch**

- **Given** a generated workflow whose checkout resolves to a different
  repository or SHA, or whose host listing resolves a different marketplace
  root,
- **When** the setup step runs,
- **Then** it fails before product-owned plugin installation or harness
  invocation.

### Requirements

- **R1 (ubiquitous):** The skill shall operate only on repository-owned GitHub
  Actions workflows under `.github/workflows/`.
- **R2 (ubiquitous):** Target jobs, hosts, marketplace name/repository/SHA,
  pinned checkout action, exact supported CLI prerequisites, and host-state
  mappings shall be explicit or confirmed before editing.
- **R3 (event-driven):** When a selected job unambiguously invokes one host,
  the skill shall author only that host's canonical registration block.
- **R4 (event-driven):** When a selected job invokes both hosts, the skill
  shall share only the verified checkout and keep host registration/state
  separate.
- **R5 (unwanted behavior):** If ownership, classification, CLI compatibility,
  state binding, conditional insertion boundary, existing-step ownership, or
  caller configuration is ambiguous, the skill shall leave the affected
  target unchanged and report the ambiguity.
- **R6 (ubiquitous):** External reusable workflows shall never be edited.
- **R7 (state-driven):** While any repository-local caller is unselected or
  supplies differing inputs, its shared local callee shall remain unchanged.
- **R8 (ubiquitous):** The generated checkout shall use the caller-selected
  immutable action commit and verify the exact normalized GitHub repository
  origin and full commit SHA before host registration.
- **R9 (ubiquitous):** Host registration shall run from the GitHub workspace
  root, use only the version-2 command adapter, accept only Claude `path` or
  fallback `installLocation` and Codex `root`, and require the listing root's
  real path to equal the checkout's real path.
- **R10 (ubiquitous):** The skill shall preserve unrelated workflow semantics,
  caller-owned CLI/plugin/test steps, and YAML outside the smallest insertion.
- **R11 (ubiquitous):** Reapplying the same confirmed plan to a canonical owned
  block shall write no file and therefore preserve the existing bytes.
- **R12 (unwanted behavior):** The skill shall not expose, copy, create, or
  cache credentials, authentication, trust, or session state.
- **R13 (unwanted behavior):** The authoring invocation shall not launch a
  host, install a CLI or plugin, run or judge product tests, or emit support
  state.
- **R14 (ubiquitous):** Products shall own CLI provisioning, plugin selection
  and installation, CI environment, tests, evidence, versions, releases, and
  support claims.
- **R15 (ubiquitous):** The completion report shall enumerate changed,
  converged, ambiguous, external, conflicting, unsupported, and skipped
  targets.
- **R16 (ubiquitous):** The Kodhama plugin shall satisfy
  `kodhama-0018`'s local VERSION, dual-manifest, and present-catalog-source
  parity without imposing that package shape on a consumer. *(v5: surface-version
  parity went with `surfaces.json`; `kodhama-0025` supersedes `kodhama-0018` AC2.)*
- **R18 (event-driven):** When a PR adds a Kodhama host catalog entry, it
  shall run `scripts/keyless_admission_check.py` and review its result with
  that change. *(v3 → v4: this named "the exact product-local path above",
  whose only remaining mention is the v2 → v3 amendment note recording that
  the path never existed. The v3 amendment replaced the report with a check
  that runs but left this requirement pointing at the deleted artifact, so it
  was unsatisfiable for exactly the event it governs — a PR adding a catalog
  entry. Repointed at the check that replaced it.)*

## Open questions

None.

## Rubric check

No dedicated spec rubric or `.grove/config.toml` exists. Against
`specs/README.md`, the contract-author role, and the installed lifecycle and
versioning companions: required frontmatter is complete; approved upstreams
are declared through `depends_on` and `implements`; the significant Kodhama
identity/adapter amendment advances the behavioral counter to version `2` and
includes the required section-level delta note; the immutable checkout, exact
host adapters, workspace-root binding, closed listing-root normalization,
conditional-boundary rejection, ownership markers, reusable-workflow boundary,
and failure behavior are testable; both GWT and EARS acceptance grammars are
present; and no unresolved design choice is hidden. Result:
**PASS**, promoting the v2 amendment from `draft` to `gated`.

This is a change-scoped self-check only. It does not claim that the malformed
legacy metadata tracked by issue #20 has been repaired or that the full corpus
passes strict validation.

## Lifecycle record

Version 1 was approved by the maintainer on 2026-07-24 after the spec adversary
returned `APPROVE-READY`, the conformance reviewer returned `PASS`, and the
change-scoped corpus review returned `PASS`.

The version 2 amendment implements approved decision 0020. The spec adversary
returned `APPROVE-READY`, the conformance reviewer returned `PASS`, and the
change-scoped corpus review returned `PASS`. The maintainer then approved v2
on 2026-07-25; the `approved` status records that human spec-gate act.
