---
id: kodhama-spec-0001-family-plugin-release-and-distribution-metadata
type: spec
status: gated  # v2 author self-check passed; independent v2 review/ratification remains due
version: 2
depends_on: [kodhama-0015-family-plugin-release-and-surface-contract, kodhama-0016-distribution-availability-and-effective-support]
implements: [kodhama-0015-family-plugin-release-and-surface-contract, kodhama-0016-distribution-availability-and-effective-support]
owner: agent
updated: 2026-07-24
---

# Family plugin release and distribution metadata

> **Amended 2026-07-24 — whole-spec completion protocol.**
> **WHAT:** Defined the product extension-validator process protocol,
> canonical JSON grammar, execution identity/order, a digest-bound immutable
> validator runtime and audited sandbox boundary, retained catalog
> product-contract/history resolution, and the exact public release-engine
> and local-repository-resolver interfaces.
> **WHY:** The approved v1 contract named those obligations but left their
> process and retained-byte boundaries underdetermined, so the landed partial
> implementation correctly failed closed and the remaining release engine
> could not be implemented without guessing.
> **SCOPE:** Common canonicalization, product validation, verified catalog
> validation, S24–S28, and R41–R49; all v1 behavior and ownership boundaries
> remain current.
> **POINTER:** `distribution/IMPLEMENTATION-STATUS.md` at
> `495b4cb632fc796f76200d8cf0be7442b4d41997`; intrinsic remediation triggered
> by the spec-adversary `NEEDS-REVISION` verdicts on `95fced9` and `88f1988`.
> **VALUE:** Product maintainers can ship independently while Stewards verifies
> exact release claims without interpreting or taking ownership of product
> behavior.
> **CONFIDENCE:** verified.

## Scope

This spec defines the Stewards-owned family schemas, canonical surface
registry, catalog and provisioner availability records, deterministic
validation/generation, effective-support evaluation, and bounded legacy-stock
transition.

It does not define product behavior, create product evidence, choose or bump a
product version, create a release tag, run product setup, or promote a product
surface row.

## Authority and derivation

All paths are relative to the Stewards repository root.

| Path | Role | Mutability |
|---|---|---|
| `distribution/schemas/common-types.v1.schema.json` | Shared identity, extractor, stable-reference, evidence, load-path, support-record, publication, selector, and retirement types | Versioned authority |
| `distribution/schemas/release-metadata.v1.schema.json` | Product release-metadata minimum | Versioned authority |
| `distribution/schemas/release-inventory.v1.schema.json` | Product host-manifest, payload, public-contract, and support-derivative inventory | Versioned authority |
| `distribution/schemas/release-history.v1.schema.json` | Append-only release/tag/contract history | Versioned authority |
| `distribution/schemas/extension-validator-request.v1.schema.json` | Product extension-validator request envelope | Versioned authority |
| `distribution/schemas/extension-validator-result.v1.schema.json` | Product extension-validator result envelope | Versioned authority |
| `distribution/schemas/extension-validator-runtime.v1.schema.json` | Content-addressed immutable validator runtime manifest | Versioned authority |
| `distribution/schemas/surface-contract.v1.schema.json` | Product surface-contract minimum | Versioned authority |
| `distribution/schemas/surface-registry.v1.schema.json` | Surface-registry schema | Versioned authority |
| `distribution/schemas/catalog-availability.v1.schema.json` | Catalog availability schema | Versioned authority |
| `distribution/schemas/provisioner-availability.v1.schema.json` | Provisioner availability schema | Versioned authority |
| `distribution/schemas/clean-install-evidence.v1.schema.json` | Exact clean-host installation proof | Versioned authority |
| `distribution/schemas/effective-facts.v1.schema.json` | Authoritative effective-support inputs | Versioned authority |
| `distribution/schemas/effective-result.v1.schema.json` | Effective-support output | Versioned authority |
| `distribution/schemas/legacy-baseline.v1.schema.json` | Immutable adoption-baseline schema | Versioned authority |
| `distribution/schemas/legacy-stock-initial.v1.schema.json` | Immutable initial transition-stock snapshot | Versioned authority |
| `distribution/schemas/legacy-stock.v1.schema.json` | Shrinking transition-stock schema | Versioned authority |
| `distribution/schemas/product-adoptions.v1.schema.json` | Product-local decision/ownership reconciliation records | Versioned authority |
| `distribution/surfaces.json` | Canonical surface identifiers | Source |
| `distribution/catalogs.json` | Catalog availability and host projections | Source |
| `distribution/provisioners.json` | Exact provisioner-route availability | Source |
| `distribution/legacy-baseline.json` | Immutable entries present at adoption | Write-once source; no edits or additions |
| `distribution/legacy-stock-initial.json` | Immutable one-row initial transition stock | Write-once source; no edits or additions |
| `distribution/legacy-stock.json` | Nonconforming baseline entries still transitioning | Temporary source, removals only |
| `distribution/product-adoptions.json` | Product-local adoption and supersession evidence | Source |
| `distribution/repository-scope.md` | Canonical bounded install-door scope fragment | Source |
| `.claude-plugin/marketplace.json` | Claude Code host-native catalog | Derived |
| `.agents/plugins/marketplace.json` | Codex host-native catalog | Derived |
| `distribution/availability.md` | Catalog/provisioner state and disclosures | Derived |
| `README.md`, `CLAUDE.md` | Repository-scope descriptions derived from `distribution/repository-scope.md` | Derived/checked documentation |
| `distribution/fixtures/metadata/` | Positive and negative contract fixtures | Test authority |

`distribution/catalogs.json` is the single Stewards source for entries and
selectors projected into the host-native catalogs. Host-specific values live
under a typed `host_projection` object. Product release metadata, surface
contracts, and behavioral evidence remain product-owned sources; Stewards
stores stable references, never copied product payloads.

## Common types

### Canonical JSON grammar

Every use of “canonical JSON” in this spec uses this single grammar,
recursively for arbitrary nested values:

| JSON value | Canonical encoding |
|---|---|
| object | Normalize every key as a string below, reject duplicate keys both before and after normalization, sort members lexicographically by normalized Unicode scalar-value sequence, and emit `{` plus comma-separated `<canonical-key>:<canonical-value>` pairs plus `}` |
| array | Preserve declared element order and emit `[` plus comma-separated canonical elements plus `]` |
| string, including object key | Require Unicode scalar values, normalize to NFC, then apply the exact escaping below |
| number | Parse as finite IEEE-754 binary64 and use only RFC 8785 §3.2.2.3's ECMAScript shortest round-trip number algorithm; serialize negative zero as `0`; reject NaN, infinities, overflow, and any non-JSON number token |
| boolean | Lowercase `true` or `false` |
| null | Lowercase `null` |

String encoding emits `"` and `\` as `\"` and `\\`; U+0008, U+0009,
U+000A, U+000C, and U+000D as `\b`, `\t`, `\n`, `\f`, and `\r`; and every
other U+0000–U+001F scalar as lowercase `\u00xx`. Every other scalar,
including `/`, U+2028, U+2029, and non-BMP scalars, is emitted unescaped as
UTF-8. Unpaired surrogates are not Unicode scalar values and reject. The
encoding has no BOM, insignificant whitespace, or terminal LF; a protocol
that carries canonical JSON adds its explicitly specified LF after these
bytes. Input parsing rejects invalid UTF-8 and duplicate source keys before
normalization.

Every field described as a normalized path additionally requires Unicode
scalar values in NFC before applying its POSIX segment rules.

### Identity grammar

| Field | Exact grammar |
|---|---|
| `plugin_id` | `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$` |
| `package_version` | SemVer 2.0.0, ASCII full-match, no leading `v` |
| `release_tag` | Literal `<plugin_id>-v<package_version>` |
| `source_commit` | `^[0-9a-f]{40}$` |
| `sha256` | `^[0-9a-f]{64}$` |
| `surface_id`, `route_id`, `record_id`, `evidence_id` | Dot-separated lowercase slugs; each segment matches the `plugin_id` grammar |
| timestamp | RFC 3339 UTC with `Z` and whole seconds |

The SemVer full-match expression is:

```
^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$
```

`package_version`, `release_tag`, `source_commit`, and `payload_identity` are
distinct fields. No validator or generator may derive one by copying another.

### Version extractor and carriers

A `version_extractor` contains:

| Field | Contract |
|---|---|
| `path` | Repository-relative normalized POSIX path; no empty, `.`, or `..` segment |
| `format` | `plain-text` or `json` |
| `selector` | Forbidden for `plain-text`; required RFC 6901 JSON Pointer for `json` |

Extraction is byte-deterministic:

- `plain-text` is UTF-8 without BOM and contains exactly one SemVer string
  followed by zero or one LF byte; no other whitespace is accepted.
- `json` is UTF-8 JSON with no duplicate object keys. The JSON Pointer selects
  exactly one JSON string, and that complete string matches SemVer.
- A missing path, parse error, non-string selection, multiple interpretation,
  or non-SemVer value fails extraction.

`version_authority` is one `version_extractor`.
`version_carriers` is a non-empty duplicate-free list of objects containing
`carrier_id`, `role` (`host-manifest`, `package-manifest`, or `other`), and one
`version_extractor`. Duplicate paths or duplicate `(path, selector)` pairs are
invalid. Every extracted carrier value shall equal the authority value.

The expected tag is computed only as
`<plugin_id>-v<extracted-authority-version>`. In release validation, the tag
source is the product repository's exact Git ref
`refs/tags/<expected-tag>`. The validator peels that ref to a commit and emits
the resulting full `source_commit`; neither tag nor commit is accepted from a
caller as substitute truth.

### Stable references and typed records

A `stable_reference` is exactly one of:

| `kind` | Required fields |
|---|---|
| `repo-path` | `repository`, full `source_commit`, normalized relative `path`, `sha256` |
| `https-url` | absolute `https://` URL without credentials or fragment, `sha256` |
| `artifact` | absolute artifact `uri`, `sha256` |

An `evidence_binding` contains `evidence_id`, `stable_reference`,
`plugin_id`, `package_version`, `surface_id`, `observed_at`, and
`observation`. It satisfies only that exact identity.

A `load_path` contains `kind`
(`command`, `skill`, `agent`, `hook`, `connector`, or `host-discovery`),
non-empty `locator`, and optional non-secret `invocation`. It describes how a
consumer loads or uses the plugin; common validation does not execute it.

A `support_record` contains `record_id`, `stable_reference`, `plugin_id`,
`package_version`, and `surface_id`.

A `publication_evidence` contains `stable_reference`, `manifest_path`,
`manifest_sha256`, and `observed_at`. Its manifest path and digest shall match
the generated host catalog named by the catalog record.

A `clean_install_evidence` is a
`clean-install-evidence.v1.schema.json` object containing:

| Field | Contract |
|---|---|
| `schema_version` | Integer `1` |
| `evidence_id` | Identity grammar |
| `subject` | Exact `plugin_id`, `package_version`, `release_tag`, `source_commit`, and `surface_id` |
| `catalog_key` | Exact `plugin_id` and `surface_id` |
| `distribution_binding` | Exact discriminated union below |
| `clean_environment` | Host name/version; `environment` and `mode` matching the surface; `snapshot_kind` (`machine-snapshot`, `ci-image`, or `container-image`); immutable `snapshot_id`; and snapshot `sha256` |
| `installation` | `started_at`, `finished_at`, `outcome: installed`, discovered exact release identity, and stable reference to the retained installation record |
| `observations` | Non-empty typed `evidence_binding[]`, all matching `subject` |

`distribution_binding`, `provisioner_identity`, and every nested typed object
have `additionalProperties: false`. The binding is exactly one of these JSON
object shapes:

```
{
  "kind": "catalog-selector",
  "selector": <immutable source_selector>
}
```

or:

```
{
  "kind": "provisioner-acquisition",
  "provisioner_identity": {
    "route_id": "<route_id>",
    "surface_id": "<surface_id>",
    "plugin_id": "<plugin_id>",
    "package_version": "<package_version>",
    "provisioner_version": "<SemVer>",
    "release_tag": "<release_tag>",
    "source_commit": "<source_commit>"
  },
  "evidence_bundle": <stable_reference>
}
```

The catalog variant requires only `kind` and `selector`; it forbids
`provisioner_identity` and `evidence_bundle`. Its immutable selector ref equals
the subject release tag or commit. The provisioner variant requires only its
three shown fields and forbids `selector`; its identity and bundle path match
the exact subject and verified provisioner record. A different plugin, release,
commit, surface, environment, host, or evidence digest is invalid.

A `retirement` object is absent for an active surface and required for a
retired one. It contains `retired_at`, `decision_ref`, and `replaced_by`.
`decision_ref` is an append-only artifact id; `replaced_by` is a different
registered surface id. Retired ids remain reserved and cannot accept new
support or availability records.

## Product release metadata

The release metadata object contains only:

| Field | Required | Contract |
|---|---:|---|
| `schema_version` | yes | `1` |
| `family_contract_version` | yes | `1` |
| `plugin_id` | yes | Identity grammar |
| `version_authority` | yes | One typed extractor |
| `version_carriers` | yes | Typed non-empty carrier list |
| `surface_contract` | yes | Normalized repository-relative path |
| `release_inventory` | yes | Normalized path to one `release-inventory.v1` document |
| `release_history` | yes | Normalized path to one append-only `release-history.v1` document |
| `inventory_provider` | yes | Normalized package-relative executable path |
| `release_approval` | yes in release phase | Stable reference to the product's recorded human release-gate act |
| `payload_identity` | no | `{kind, value}`; never a package version |
| `extensions` | no | Object keyed by `plugin_id` |

Unknown common top-level fields are invalid. Product-specific values belong
under `extensions.<plugin_id>`. A declared extension validator uses a
normalized package-relative path in `extensions.<plugin_id>.validator` and
requires `extensions.<plugin_id>.validator_runtime_sha256`, the exact
immutable runtime-manifest digest defined below. Neither field is valid
without the other.

Product validation has two phases:

| Phase | Required result |
|---|---|
| `pre-tag` | Extract authority/carriers, validate parity and surface contract, emit expected tag; tag need not exist |
| `release` | Repeat `pre-tag`, require the expected Git tag, peel it to `source_commit`, and emit the release identity |

Publication and any `verified` availability require the `release` phase.
Stewards does not create the tag.

### Product extension-validator protocol

The common engine invokes only validators explicitly declared in product
release metadata or in an `other-declared-host` inventory row. It validates
the process envelope and accepts or rejects the declared extension result; it
does not interpret a product finding as family vocabulary or behavioral
evidence.

Validator paths are normalized package-relative paths. The resolved target
shall remain inside the package root, be a regular non-symlink file with no
symlink path component, and be executable. For each validation phase, the
engine invokes:

1. `extensions.<namespace>.validator` in ascending normalized
   `namespace` Unicode-scalar order; then
2. each `other-declared-host` row's `extension_validator` in ascending
   `(normalized host, normalized path)` tuple order.

Extension namespaces are unique object keys under the canonical JSON grammar.
Host-manifest identities are the unique tuples defined below. One validator
path declared by multiple identities runs once per identity with that row's
distinct request; validator-path equality never deduplicates executions.

#### Immutable validator runtime

Every validator declaration binds one locally available immutable runtime by
the lowercase 64-hex SHA-256 of a canonical
`extension-validator-runtime.v1` manifest. The digest is over the manifest's
canonical JSON bytes without a terminal LF. The manifest has
`additionalProperties: false` and exactly:

| Field | Contract |
|---|---|
| `schema_version` | Integer `1` |
| `platform` | Object with only non-empty lowercase dot-id `os`, `architecture`, and `abi`; it shall exactly equal the launcher's detected target tuple |
| `path_entries` | Non-empty, ordered, duplicate-free array of normalized absolute sandbox directories |
| `executables` | Sorted, duplicate-free array of normalized absolute sandbox paths |
| `entries` | Duplicate-free array sorted by normalized absolute sandbox path, with exactly one row for every runtime directory, regular file, and symbolic link |

Sandbox paths use `/`-rooted POSIX syntax regardless of host operating system;
the launcher projects them into the synthetic child view without exposing the
corresponding live-host path. Every parent directory is an entry. A directory
row contains only `path`, `kind: "directory"`, and `mode`. A regular-file row
contains only `path`, `kind: "file"`, `mode`,
lowercase 64-hex `sha256`, and `role`, where `role` is exactly `executable`,
`loader`, `library`, `configuration`, or `runtime-data`. A symbolic-link row
contains only `path`, `kind: "symlink"`, `mode`, and normalized absolute
`target`. Every `mode` is a string matching `0[0-7]{3}`. Every link target is
another entry, link resolution is acyclic, and the final target remains in the
manifest.

Each `path_entries` value names a manifest directory. Each `executables` value
names an executable-mode regular-file entry with role `executable`. A file
used as a program interpreter, dynamic loader, library, resolver input, locale
input, timezone input, or other runtime/configuration dependency is an
individually enumerated entry with its applicable role; directory visibility
does not imply visibility of an unlisted child.

The runtime image contains exactly the manifest entries with the declared
types, modes, link targets, and file hashes—no extra entry or implicit
live-host bind. It contains no credential, user profile, mutable host state,
device, socket, or writable file. Entries under `/home`, `/Users`, `/root`,
`/private`, `/proc`, `/sys`, `/tmp`, `/dev`, `/run/secrets`, and
`/var/run/secrets` are invalid. An individually enumerated immutable
`configuration` file may use `/etc`; `/etc` directory visibility never exposes
an unenumerated child.

Before either execution, the launcher resolves the declaration's exact digest
from its local content-addressed runtime store, validates the manifest digest,
schema, platform tuple, and complete image tree, and projects the same verified
tree read-only into both sandboxes. It does not fetch or substitute another
digest or platform. An unavailable digest, malformed manifest, digest
mismatch, platform mismatch, missing or extra image entry, type/mode/hash/link
mismatch, forbidden path, or unsupported projection fails before spawn.

Each validator is executed twice with this exact process contract:

| Process field | Exact contract |
|---|---|
| `argv` | `[<resolved-validator-absolute-path>, "--stewards-extension-validator-v1"]`; no shell and no additional argument |
| working directory | The resolved absolute package root supplied to `--package-root` |
| stdin | One canonical `extension-validator-request.v1` JSON object, UTF-8, followed by exactly one LF; both executions receive identical bytes |
| stdout | One canonical `extension-validator-result.v1` JSON object, UTF-8, followed by exactly one LF; no other bytes |
| stderr | Empty for protocol exits `0` and `1`; otherwise captured only for bounded diagnostics and never interpreted as a product result |
| timeout | 10 seconds per execution, measured from spawn through process-group termination |
| sizes | Request and stdout are each at most 1,048,576 bytes; stderr is at most 65,536 bytes; exceeding a bound fails validation |
| filesystem/runtime | Exact declared immutable runtime plus package/private overlays and audited forbidden-path behavior below |
| network | Every socket/network attempt by the process tree is denied, audited, and independently fails validation as defined below |

The child environment contains exactly these keys:

| Key | Exact value |
|---|---|
| `PATH` | The runtime manifest's `path_entries`, joined in declared order with `:`; no caller PATH entry is inherited |
| `LANG`, `LC_ALL` | `C.UTF-8` |
| `TZ` | `UTC` |
| `HOME` | `/tmp/home` |
| `TMPDIR` | `/tmp` |
| `NO_PROXY` | `*` |
| `http_proxy`, `https_proxy`, `HTTP_PROXY`, `HTTPS_PROXY` | Empty string |

No other inherited variable, file descriptor, credential, or stdin byte is
available to the child. A launcher unable to establish the filesystem or
network boundary fails closed before executing the validator.

The sandbox presents a synthetic filesystem view, using a mount namespace,
sandbox profile, or equivalent enforcement. Its complete visibility is:

| Path | Visibility and permitted use |
|---|---|
| resolved package root, at the same absolute path used as `cwd` | Entire subtree readable and executable; no write, create, rename, link, metadata, or deletion operation |
| canonical ancestors of the package root | Directory traversal and metadata needed to reach the mount only; directory listing and access to sibling entries are denied |
| exact runtime-manifest entries | Declared directories and exact file/link entries readable; declared executable files executable; no unenumerated child or live-host counterpart visible |
| `/tmp` | Fresh private tmpfs for one execution; `/tmp/home` exists and is empty; read/write/create/delete permitted only here |
| `/dev/null` | Read/write character device |

All other paths—including live-host runtime prefixes, caller/maintainer home
directories, unenumerated `/etc` children, `/proc`, `/sys`, SSH/credential
stores, the Stewards checkout outside the package root, and inherited
temporary directories—are absent. `PATH` lookup can select only a path listed
in manifest `executables`. Direct execution is permitted only for the declared
validator, an executable regular file under the package root, or a manifest
`executable`; the kernel may select only an enumerated `executable` interpreter
or `loader` while starting one of those files. Every descendant inherits the
same rules.

Before each run, the launcher records the complete package-root
path/type/mode/SHA-256 snapshot. A filesystem operation against a
non-allowlisted path returns `EACCES`; a mutating operation outside `/tmp`
returns `EROFS`. In either case the launcher sets an audited
`forbidden_path_attempt` flag before returning the error. The flag fails common
validation even when product code catches the error and returns a canonical
`pass`. After process-group termination the launcher destroys the private
tmpfs, requires the package snapshot to be byte-identical, and requires that
no persistent writable path was exposed. An unsupported filesystem-view,
canonical-path, syscall-audit, or process-tree containment mechanism fails
before spawn.

The launcher gives the process tree only stdin, stdout, and stderr file
descriptors; none is a socket. It intercepts `socket`, `socketpair`, `connect`,
`bind`, `listen`, `accept`, `accept4`, `shutdown`, `sendto`, `sendmsg`,
`sendmmsg`, `recvfrom`, `recvmsg`, `recvmmsg`, `getsockname`, `getpeername`,
`setsockopt`, and `getsockopt`, plus platform multiplexed/equivalent forms
such as `socketcall` and socket operations submitted through `io_uring`,
before the kernel performs them. Every such attempt sets a `network_attempt`
audit flag and returns `EPERM`. The flag is process-tree-wide and fails common
validation regardless of the validator's handled error, exit code, or result
bytes.
Name-service access cannot bypass this rule: network syscalls are audited, and
non-allowlisted resolver/configuration paths trigger
`forbidden_path_attempt`. A platform unable to observe and deny every listed
attempt for the complete process tree fails closed before spawn; proxy
variables and a network namespace without the audit flag are insufficient.

The request object has `additionalProperties: false` and these common fields:

| Field | Contract |
|---|---|
| `schema_version` | Integer `1` |
| `request_kind` | `product-extension` or `host-manifest-extension` |
| `phase` | `pre-tag` or `release` |
| `plugin_id` | Extracted release-metadata plugin id |
| `namespace` | Metadata extension key for `product-extension`; `plugin_id` for `host-manifest-extension` |
| `package_version` | Extracted authority version |
| `expected_tag` | Computed `<plugin_id>-v<package_version>` |
| `source_commit` | `null` in `pre-tag`; the tag's peeled full commit in `release` |
| `validator_runtime_sha256` | Exact digest from the validator declaration and verified runtime manifest |
| `release_metadata_path`, `surface_contract_path`, `release_inventory_path`, `release_history_path` | The four normalized package-relative paths used by the common validator |

A `product-extension` request additionally requires `extension`, the complete
JSON value from `extensions.<namespace>` after removing the reserved
`validator` and `validator_runtime_sha256` members, and forbids
`host_manifest`. A
`host-manifest-extension` request additionally requires `host_manifest`, the
complete inventory row after removing `extension_validator` and
`extension_validator_runtime_sha256`, and forbids `extension`. The engine
constructs these values only after common schema, path, version, carrier,
inventory, and runtime validation; validators do not receive unvalidated
common fields.

The result object has `additionalProperties: false` and exactly:

| Field | Contract |
|---|---|
| `schema_version` | Integer `1` |
| `request_sha256` | SHA-256 of the exact stdin bytes, including its terminal LF |
| `outcome` | `pass` or `fail` |
| `findings` | Sorted, duplicate-free array of exact finding objects |

A finding contains exactly non-empty dot-id `code`, non-empty single-line
`message`, and RFC 6901 `instance_pointer`. Findings sort by
`(instance_pointer, code, message)` using Unicode code-point order. `pass`
requires an empty array and process exit `0`; `fail` requires a non-empty array
and process exit `1`. Any other exit, signal, stderr byte, malformed or
non-canonical result, request-hash mismatch, outcome/exit mismatch, differing
stdout across the two executions, timeout, network attempt, or persistent
filesystem mutation fails common validation. Product `fail` findings may be
reported with their namespace and pointer, but Stewards shall not transform
their codes or messages into common support facts.

### Complete product release inventory

The common validator invokes the product-owned `inventory_provider` twice in a
network-disabled clean checkout as:

```
<inventory_provider> --package-root <path> --emit-release-inventory
```

Both stdout byte streams shall be identical canonical
`release-inventory.v1` JSON and shall equal the checked-in
`release_inventory` file. A provider failure, filesystem mutation, stderr
credential, byte difference, or inventory mismatch fails validation. This
provider is the product-owned discovery boundary permitted by the common
schema; omitting an existing item is a product contract violation and fails
the product's human release gate.

The inventory contains exact duplicate-free arrays:

| Array | Required row |
|---|---|
| `host_manifests` | `host`, normalized `path`, manifest kind, version extractor, extracted package version, and the conditional extension-validator fields below |
| `payload_identities` | `payload_id`, normalized source path, deterministic extractor, exact kind/value, and whether consumers act on it |
| `public_contract_items` | stable `contract_id`, category, stable source/extractor, canonical fingerprint, and compatibility annotation |
| `support_derivatives` | derivative id, kind (`public-support-table` or `host-manifest-claim`), path/extractor, and exact surface-contract projection |

`host_manifests[].host` is a non-empty, single-line Unicode scalar string
normalized to NFC. A host-manifest identity is exactly `(host, path)` after
that normalization and normalized-path validation. The array is
duplicate-free and sorted ascending by that tuple using Unicode scalar-value
lexicographic order. No other field, including `manifest_kind`,
`extension_validator`, or version, participates in identity or execution
order.

`manifest kind` is exactly `claude-plugin`, `codex-plugin`, `npm-package`, or
`other-declared-host`; the last requires normalized package-relative
`extension_validator` and lowercase 64-hex
`extension_validator_runtime_sha256`. Neither field is valid without the
other, and neither is valid for another manifest kind.
Every payload, public-contract, and support-derivative extractor is exactly one
additional-properties-forbidden object:

| `kind` | Required fields | Extracted canonical bytes |
|---|---|---|
| `file-bytes` | `kind`, normalized `path` | Raw file bytes |
| `text-line` | `kind`, normalized `path`, zero-based `line` | That UTF-8, BOM-free, LF-delimited line without LF; CR and invalid UTF-8 reject |
| `json-pointer` | `kind`, normalized `path`, RFC 6901 `pointer` | Selected JSON value canonicalized with this spec's NFC/key-order/escaping rules; duplicate keys reject |

Missing paths, directories, symlinks escaping the package root, invalid
pointer/line, or extra extractor fields reject. A payload row's kind is
`content-hash`, `version-stamp`, or a namespaced extension kind. Its value is
the extracted UTF-8 string for a text/JSON string or `sha256:<hex>` for other
canonical bytes.

Each public-contract fingerprint is SHA-256 of exactly:

```
{"category":"<category>","contract_id":"<contract_id>","extracted_sha256":"<sha256-of-extracted-canonical-bytes>"}
```

using the shown key order and canonical JSON bytes. Its compatibility
annotation is exactly `initial`, `unchanged`,
`backward-compatible-fix`, `backward-compatible-capability`,
`supported-surface-addition`, `breaking-change`,
`false-claim-correction`, or `supported-surface-withdrawal`.

`public_contract_items.category` is exactly `installation-coordinate`,
`installation-input`, `host-visible-entrypoint`, `configuration`,
`managed-state`, `runtime-requirement`, `surface-support`, or
`consumed-output-protocol`. Internal refactors and unpublished fixtures are
forbidden from this array. A payload row whose consumer-acted flag is true
also appears as a `consumed-output-protocol` public-contract item.

Every discovered host manifest shall appear once in `host_manifests` and once
in `version_carriers` with role `host-manifest` and the same extractor; no
host-manifest carrier may lack an inventory row. Every extracted host-manifest
version equals the authority. Every discovered payload identity appears once
in both the inventory and the release-history row; the optional singular
release-metadata `payload_identity` is allowed only when the inventory has
exactly one payload row and shall equal it.

For each support derivative, validation recomputes its declared projection
from the exact version-bound product surface contract. A public support table
or host-manifest support claim discovered by the provider but absent from
`support_derivatives`, or any stale/extra/missing surface claim, fails before
tagging. Host manifests remain product-owned; this check validates their
version and support claims without copying them.

### Immutable history and SemVer compatibility

The product's `release-history.v1` file is append-only and sorted by SemVer
precedence. Each row contains package version, release tag, source commit, a
`repo-path` `release_metadata_reference` to that tag's retained metadata blob,
release-inventory SHA-256, complete payload-identity array, public-contract
inventory SHA-256, surface-contract SHA-256, classified change set, and
`release_approval`. Initial family adoption inventories every existing
matching package tag and requires one product-human approval reference for
that seed. Each new row also names a stable reference to the immediately prior
ledger state. Appended-ledger validation loads that reference and requires the
current ledger to equal those prior canonical rows byte-for-byte plus exactly
one appended row. The ledger may be committed after its release tag because
its row contains that tag's source commit; catalog publication waits for the
appended ledger and cites its stable reference, avoiding a commit
self-reference.

The three release-row digests are exact:

| Field | SHA-256 preimage |
|---|---|
| `release_inventory_sha256` | The checked-in `release_inventory` file's exact bytes, which already equal the provider's canonical stdout including its terminal LF |
| `public_contract_inventory_sha256` | Canonical JSON bytes of the complete `public_contract_items` array, with no terminal LF |
| `surface_contract_sha256` | The checked-in `surface_contract` file's exact bytes |

In `pre-tag`, `release_history` contains only seed/prior rows and the expected
tag need not exist. In `release`, the expected tag exists and the current
checked-in ledger contains exactly one appended last row for it. The engine
reads release metadata, inventory, and surface bytes from the tag commit,
loads the appended row's prior reference, and requires the current ledger to
equal that prior ledger plus the one derived row. The release-validation
checkout commit shall equal or descend from the release commit; files other
than the append-only ledger shall match their tagged retained bytes. For a
first family release, an empty prior ledger is valid only when no earlier
matching package tag exists; otherwise the product-human-approved seed rows
cover every earlier matching tag.

When the prior ledger is non-empty, the appended row's
`prior_history_reference` is a derived `repo-path` reference to the prior
ledger blob at the release tag's `source_commit`: `repository` is the exact
GitHub origin repository, `path` is the repository-relative composition of
the package root and `release_history`, and `sha256` covers its raw bytes. The
field is absent only for an empty ledger. The validator recomputes this
reference and never trusts the row's supplied value.
Every appended or seeded row's `release_metadata_reference` is likewise a
derived `repo-path` reference to that row's exact tag commit and
repository-relative metadata path, with SHA-256 over the raw metadata blob.
The engine resolves that reference first to recover each historical
inventory/surface path and bytes; a digest without this retained input cannot
satisfy history validation.

The classified change set is a sorted duplicate-free array of exact objects
`{contract_id, change_kind, before_fingerprint, after_fingerprint,
evidence_refs}`. It sorts by `(contract_id, change_kind)`;
`before_fingerprint`/`after_fingerprint` are SHA-256 or `null` for
addition/removal; `evidence_refs` is a non-empty sorted stable-reference array.
`change_kind` is exactly one compatibility annotation other than `initial` or
`unchanged`. The validator derives this array from prior/current inventories
and surface rows; a caller classification that differs is invalid.

Every product surface row maps to contract id
`surface-support.<surface_id>`. Its fingerprint is SHA-256 of the complete
schema-valid row canonicalized with NFC strings, Unicode-code-point key order,
the exact escaping rules below, no whitespace, and no trailing LF. The
fingerprint therefore includes host, status, setup declaration, and every
conditional evidence/load/support/missing-capability/disclosure field.

Surface change objects use that contract id and encode:

| Change | `before_fingerprint` | `after_fingerprint` | `change_kind` | Required `evidence_refs` |
|---|---|---|---|---|
| Absent/non-supported → supported | prior row fingerprint or `null` | supported row fingerprint | `supported-surface-addition` | Every after-row evidence and support-record stable reference |
| Supported → candidate/unsupported | supported row fingerprint | after-row fingerprint | `supported-surface-withdrawal` or `false-claim-correction` | Prior support-record reference, current surface-contract stable reference, and release approval |
| Supported → absent/retired | supported row fingerprint | `null` | `supported-surface-withdrawal` or `false-claim-correction` | Prior support-record reference, current release-inventory stable reference, and release approval |
| Absent → candidate | `null` | after-row fingerprint | `backward-compatible-capability` | Exact set below |
| Absent → unsupported | `null` | after-row fingerprint | `backward-compatible-fix` | Exact set below |
| Unsupported → candidate | prior fingerprint | after fingerprint | `backward-compatible-capability`, unless a breaking field change below wins | Exact set below |
| Candidate → unsupported/absent | prior fingerprint | after fingerprint or `null` | `breaking-change` | Exact set below |
| Unsupported → absent | prior fingerprint | `null` | `backward-compatible-fix` | Exact set below |
| Candidate/unsupported row-field change | prior fingerprint | after fingerprint | Ranked field rule below | Exact set below |

For a same-status candidate/unsupported row, field-change rank is:

1. `breaking-change` when a load path is removed/changed, setup changes from
   not-required to required, or a required setup contract changes;
2. `backward-compatible-capability` when a load path is added and no breaking
   change exists;
3. `backward-compatible-fix` when setup changes required→not-required or only
   evidence, support record, missing capability, or disclosure changes; and
4. no change object when the row fingerprint is equal.

For unsupported→candidate, any simultaneous rank-1 field change overrides the
status capability classification. The exact pre-approval evidence set for
every non-supported addition/change/removal is the union of: prior
surface-contract reference iff a prior row exists; current surface-contract
reference iff an after row exists, otherwise current release-inventory
reference; and every stable reference embedded in changed before/after
evidence, support record, or setup contract. Supported changes use the same
union plus the table-specific references. The final set adds exactly the
release-approval stable reference. References sort by canonical bytes and are
duplicate-free. Missing prior/current rows use `null`; no synthetic
fingerprint/reference is permitted.

In the table, “release approval” is a **final-set-only** reference. It is
excluded from every pre-approval table-specific/general union and from
`approval_projection`, including supported withdrawal/retirement rows. All
other table-specific references are included before approval. After the
approval artifact exists, its stable reference is appended exactly once to
every final row without changing the approved projection or any other
evidence reference.

Approval is non-self-referential and ordered:

1. freeze prior/current inventory and surface-contract references, derive
   every change object with its pre-approval evidence set, and canonicalize
   `approval_projection` containing plugin id, prior/proposed versions,
   prior/current inventory and surface digests, proposed bump, and that
   complete pre-approval change set;
2. compute `approval_projection_sha256`;
3. materialize the human approval artifact at an immutable artifact URI or
   pre-release repository commit. It contains exactly schema version, plugin
   id, human approver, approval timestamp, proposed version/bump, and the
   projection digest; it contains no own stable reference, final change
   set/history digest, release tag, or release commit;
4. form the final change set by adding the approval artifact's stable
   reference to each evidence set and changing no other projection field; and
5. bind the approval reference in release metadata before tagging, then bind
   the final set/reference in the post-tag history row under the separate
   ledger ordering.

Validation recomputes the projection hash and final-set transformation. An
approval artifact created in the release commit it approves, or whose digest
depends on its own stable reference/final set, is invalid.

Release validation enumerates every repository ref matching
`refs/tags/<plugin_id>-v<SemVer>`. Every prior history tag shall still exist
and peel to its recorded commit; every enumerated prior tag shall have exactly
one history row. A tag moved, deleted, reused for another version/commit, or
omitted from history fails all later releases. The new tag/version shall be
greater by SemVer precedence than the last history row and absent from prior
history. History permits one full version at each precedence position:
because build metadata is ignored by SemVer precedence, versions differing
only by build metadata are equal-precedence duplicates and are rejected, not
treated as a bump.

Version transitions are exact:

| Transition | Rule |
|---|---|
| Core `(major, minor, patch)` increases | The first changed core component determines actual major/minor/patch level and shall meet the minimum-bump table |
| Same core, prerelease → greater prerelease | Allowed only when the cumulative public-contract diff from the most recent stable release before that prerelease line is covered by the line's core bump; with no prior stable release, compare to the line's first prerelease inventory |
| Same core, prerelease → stable | Allowed only as promotion and subject to the same cumulative check; any new current diff is included |
| Same core, stable → prerelease; prerelease decrease; build-only/equal-precedence change | Rejected |

Prerelease identifiers compare by SemVer precedence. A prerelease iteration or
promotion does not itself satisfy a missing core patch/minor/major bump; the
line's core tuple shall already encode the required cumulative compatibility
level.

The validator compares the current `public_contract_items` and supported
surface rows with the last release:

| Classified change | Minimum bump |
|---|---|
| Backward-compatible fix or evidence/provenance correction adding no capability and withdrawing no public promise | patch |
| Backward-compatible public-contract capability or supported-surface addition | minor |
| Removal/incompatible change of any public-contract item, or withdrawal/retirement of a previously valid supported-surface promise, while prior major is `0` | minor |
| The same breaking change when prior major is at least `1` | major |

A false support claim is withdrawn immediately and tagged
`false-claim-correction` in the change set. Because the published claim was
consumer-observable, its withdrawal uses the breaking-change row; it is never
delayed or mislabeled as unchanged evidence. The recorded product-human
`release_approval` shall bind the canonical pre-approval projection above.
Validation checks the exact approval-reference augmentation and that the
actual bump is at least the table minimum; Stewards neither chooses the bump
nor creates/approves the release.

## Product surface contract

The object contains `schema_version: 1`, `family_contract_version: 1`,
`version`, duplicate-free `surfaces`, and optional `extensions`. `version`
equals the extracted authority.

Each row is keyed by `surface_id` and contains `host`, `status`, and
`post_install_setup: {required: <boolean>, contract: <stable_reference|null>}`.
When setup is required, `contract` is required; otherwise it is `null`.

| Field | `supported` | `candidate` | `unsupported` |
|---|---:|---:|---:|
| `evidence` (`evidence_binding[]`) | non-empty | optional | optional |
| `load_path` (typed object) | required | optional | optional |
| `support_record` (typed object) | required | optional | optional |
| `missing_capability` (non-empty string) | forbidden | required | required |
| `disclosure` (non-empty string) | forbidden | required | required |

Only `supported` is a behavioral support claim. Common validation checks
shape, exact identity, and stable references; it does not judge or create the
behavioral evidence.

## Surface registry

`distribution/surfaces.json` contains `schema_version: 1`,
positive-integer `registry_version`, and duplicate-free rows containing
`surface_id`, `host`, `environment`, `mode`, `label`, `lifecycle`, and
conditional `retirement`.

Version 1 contains:

| `surface_id` | `host` | `environment` | `mode` |
|---|---|---|---|
| `claude-code.local.interactive` | `claude-code` | `local` | `interactive` |
| `claude-code.ci.headless` | `claude-code` | `ci` | `headless` |
| `claude-code.cloud-container.headless` | `claude-code` | `cloud-container` | `headless` |
| `codex.local.interactive` | `codex` | `local` | `interactive` |
| `codex.ci.headless` | `codex` | `ci` | `headless` |
| `codex.cloud-container.headless` | `codex` | `cloud-container` | `headless` |

`lifecycle` is `active` or `retired`. Active rows forbid `retirement`; retired
rows require it. Renaming or changing dimensions creates a new id and retires
the old one; an id is never reused.

## Availability records

### Catalog

A catalog key is `(plugin_id, surface_id)`. `manifest_path` shall equal
`.claude-plugin/marketplace.json` for Claude Code or
`.agents/plugins/marketplace.json` for Codex.

A `source_selector` has `additionalProperties: false` and is exactly one of:

```
{
  "kind": "mutable",
  "repository": "<owner>/<repository>",
  "path": "<normalized-relative-path-or-empty>"
}
```

or:

```
{
  "kind": "immutable",
  "repository": "<owner>/<repository>",
  "path": "<normalized-relative-path-or-empty>",
  "ref": {
    "kind": "tag",
    "value": "<release_tag>"
  }
}
```

or the same immutable shape with
`"ref": {"kind": "commit", "value": "<source_commit>"}`. The nested `ref`
also has `additionalProperties: false`. `repository` matches
`^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`, contains exactly one slash, and has no
`.git` suffix. `path` is `""` for repository root or a normalized relative
POSIX path with no empty, `.`, or `..` segment. The mutable shape forbids
`ref`; each immutable shape requires exactly its shown ref fields. A tag ref
shall equal the subject `release_tag`; a commit ref shall equal the subject
`source_commit`.

| State | Required | Forbidden |
|---|---|---|
| `absent` | key, `state`, non-empty `reason` | selector, product paths, projection, publication, release identity, clean-install evidence |
| `published` | key, `state`, `manifest_path`, typed `source_selector`, typed `publication_evidence`, host-specific `host_projection`, and exactly one conforming or transition shape below | identity binding, release identity, clean-install evidence |
| `verified` | every published field, `package_version`, `release_tag`, `source_commit`, `identity_binding`, one typed `clean_install_evidence` | mutable-selector identity claim |

`host_projection` contains `host`, `entry_name`, and `fields`; `fields` is
validated by the selected host adapter and is the only host-specific object.

A conforming published/verified record requires normalized
`release_metadata_path`, normalized `surface_contract_path`, and
`product_contract_version: 1`, equal to the product surface contract's
`family_contract_version`; it forbids `transition_exception`. A verified row
additionally requires a stable `release_history_reference` whose last row
binds its exact release.

The only nonconforming shape is a published record with
`transition_exception` and without those three product-contract fields. Its
exception object contains exactly the immutable baseline key/fingerprint,
non-empty sorted `missing_contract_elements`, literal disclosure
`legacy published stock`, and `terminal_action: adopt-or-delist`. It is valid
only while the identical row remains in both `legacy-baseline.json` and
`legacy-stock.json`. It is forbidden for new/uninventoried entries, cannot be
verified or used in effective facts, and becomes invalid immediately when its
stock row is removed. This bounded waiver is the sole way ordinary validation
accepts a nonconforming pre-adoption publication.

`identity_binding` is `catalog-selector` only when the immutable selector ref
equals the release tag or commit, or `provisioner-acquisition` only when a
matching verified provisioner record carries the same identity. A mutable
selector is capped at `published`.

#### Retained product-contract and history resolution

`validate-door` resolves product bytes only for `verified` catalog rows. It
never executes product inventory providers or extension validators. Published
rows retain their existing shape/publication checks but make no retained
release-identity claim.

Resolution uses the required `STEWARDS_PRODUCT_REPOSITORIES` environment
variable. Its value is one UTF-8 JSON object with no duplicate keys or
additional envelope: every key is a selector `owner/repository`, and every
value is a non-empty local checkout path. Relative values resolve from the
Stewards repository root; absolute values remain absolute. Every required
repository shall have exactly one entry. Extra entries are permitted and
ignored. Each selected checkout shall have an `origin` URL in
`https://github.com/<owner>/<repository>[.git]`,
`ssh://git@github.com/<owner>/<repository>[.git]`, or
`git@github.com:<owner>/<repository>[.git]` form that normalizes exactly to
the key. Validation performs no fetch and never reads a product working-tree
file; an absent checkout/object is a contract failure.

For a verified row, resolution is ordered and fail-closed:

1. Resolve `source_selector.repository` through the mapping. Require
   `source_commit` to be a commit object. For a tag selector, require the exact
   ref `refs/tags/<release_tag>` to exist and peel to that commit; for a commit
   selector, require its ref value to equal that commit.
2. Define `package_prefix` as `source_selector.path`. Compose any
   package-relative `p` as `p` when the prefix is empty and
   `<package_prefix>/<p>` otherwise. Both inputs are independently normalized;
   no absolute path, empty segment, `.`, `..`, backslash, or percent-decoded
   alternate is accepted.
3. At `source_commit`, resolve the composed `release_metadata_path`,
   `surface_contract_path`, and the metadata-declared `release_inventory`
   path as Git blobs of mode `100644` or `100755`; symlinks, submodules,
   directories, missing objects, and working-tree fallbacks fail. Parse JSON
   as UTF-8 without BOM or duplicate keys.
4. Require release metadata `plugin_id`, extracted authority/carriers,
   computed tag, `surface_contract`, and `family_contract_version` to equal the
   catalog plugin id, release identity, catalog path, and
   `product_contract_version`. Require the retained surface contract's version
   and family version to match the same values. Require raw inventory/surface
   digests and complete payload identities to match the release row below.
5. `release_history_reference` shall be a `repo-path` stable reference with
   the same repository and with `path` exactly equal to the composition of
   `package_prefix` and metadata `release_history`. Its `source_commit` shall
   be a commit descendant of or equal to the release `source_commit`. Resolve
   that exact commit/path as a regular Git blob; its raw SHA-256 shall equal
   the reference digest before parsing it as `release-history.v1`.
6. Require a non-empty ledger whose last row has exact `package_version`,
   `release_tag`, `source_commit`, `release_inventory_sha256`,
   `public_contract_inventory_sha256`, `surface_contract_sha256`,
   `payload_identities`, and `release_approval` for the retained release. Its
   `release_metadata_reference` shall equal the repository, source commit,
   composed path, and raw digest resolved in steps 1–4. Resolve every row's
   metadata reference before validating the whole ledger's order, prior
   references, tag immutability, change set, bump, and approval bindings; a
   matching last-row identity alone is insufficient.

No `https-url` or `artifact` reference can satisfy a verified catalog
`release_history_reference`, because this no-fetch resolver cannot establish
its retained repository/tag/path relations. Those stable-reference variants
remain valid in the other fields that explicitly permit them.

### Provisioner

Every provisioner record, including `unavailable`, has the same complete key:
`(route_id, surface_id, plugin_id, package_version)` plus `state`. Missing rows
mean unavailable and make no claim.

A candidate or verified record additionally carries `provisioner_version`
(SemVer), `adapter_path` (normalized repository-relative path), and typed
`prerequisites[]`. A prerequisite contains `prerequisite_id`,
`request_reference_id`, `kind` (`authentication`, `trust`, `runtime`,
`configuration`, or `writable-state`), and non-empty `description`.
Prerequisite and request-reference ids use the common identity grammar and are
unique within the route.

The mapping to spec 0002 request references is fixed:

| Prerequisite `kind` | Required request-reference `kind` |
|---|---|
| `authentication` | `authentication-env` |
| `trust` | `trust-store` |
| `runtime` | `runtime-command` |
| `configuration` | `mounted-configuration` |
| `writable-state` | `writable-state` |

The selected target shall name exactly one request reference whose
`reference_id` equals `request_reference_id` and whose kind is the mapped kind.
No name, path, or kind inference is permitted.

| State | Conditional fields |
|---|---|
| `unavailable` | requires `reason`; forbids `provisioner_version`, `adapter_path`, prerequisites, release identity, and evidence |
| `candidate` | requires adapter path, prerequisites, `missing_proof`, and `disclosure`; forbids verified evidence |
| `verified` | requires adapter path, prerequisites, `release_tag`, `source_commit`, and one typed retained evidence-bundle reference governed by spec 0002 |

The key's package version, release tag, commit, evidence bundle, surface, and
provisioner version shall match exactly.

## Effective-support facts and result

`effective --facts <path>` accepts only an
`effective-facts.v1.schema.json` document, never caller-supplied factor
booleans. The document contains:

- `subject`: exact `plugin_id`, `package_version`, `release_tag`,
  `source_commit`, and `surface_id`;
- `product_contract`: the required product-input union below;
- `distribution_record`: the required discriminated union below;
- `consumer_selection`: the required consumer-input union below;
- `environment_assessment`: the required environment-input union below;
- `product_setup`: the required discriminated union below.

Every factor input and nested object forbids additional properties. For
product, consumer, and environment inputs, the exact variants are:

| Input | Positive/present variant | Typed negative variants |
|---|---|---|
| `product_contract` | `kind: record`, stable `source_reference`, exact release identity, and one schema-valid surface row in any product state | `kind: missing` with source reference and exact subject lookup; or `kind: invalid` with source reference, lookup, and non-empty errors `row-schema-invalid`, `duplicate-surface`, or `stable-reference-mismatch` |
| `consumer_selection` | `state: selected`, request id, selected plugin/version/surface/route, and stable request/receipt reference | `state: missing` with subject and source reference; or `state: invalid` with subject, source reference, and errors `selection-mismatch` or `selection-reference-invalid` |
| `environment_assessment` | `state: ready` or `not-ready`, exact subject, typed evidence, and, for not-ready, non-empty missing prerequisites | `state: missing` with subject and source reference; or `state: invalid` with subject, source reference, and errors `assessment-schema-invalid`, `assessment-reference-invalid`, or `assessment-identity-mismatch` |

The product `record` row state `supported` may satisfy product support;
`candidate` or `unsupported` yields `product-not-supported`. Product
`missing` yields `product-row-missing`; product `invalid` yields
`product-row-invalid`. Consumer `missing` yields `consumer-not-selected`;
consumer `invalid` yields `selection-mismatch`. Environment `not-ready`,
`missing`, and `invalid` yield respectively `environment-not-ready`,
`environment-assessment-missing`, and `environment-assessment-invalid`.
Owners are product, consumer/environment, and consumer/environment,
respectively.

`distribution_record` and its nested objects have
`additionalProperties: false`. It is exactly one of:

| `kind` | Required fields | Meaning |
|---|---|---|
| `record` | `kind`, `source_reference`, `record_type`, `record` | `record` is one complete schema-valid catalog or provisioner availability row in any declared state |
| `missing` | `kind`, `source_reference`, `record_type`, `lookup_key` | The schema-valid authority source contains no row for the exact key |
| `invalid` | `kind`, `source_reference`, `record_type`, `lookup_key`, non-empty duplicate-free `error_codes` | The authority source contains a row for the key but that row or its duplicate-key relation is invalid |

`source_reference` is a stable reference to `distribution/catalogs.json` or
`distribution/provisioners.json`. `record_type` is `catalog` or
`provisioner`. Its exact `lookup_key` is `{plugin_id, surface_id}` for catalog
or `{route_id, surface_id, plugin_id, package_version}` for provisioner.
`error_codes` contains only `row-schema-invalid`, `duplicate-key`, or
`stable-reference-mismatch`. A `record` variant forbids `lookup_key` and
`error_codes`; the other variants forbid `record`.

Evaluation maps these schema-valid inputs exactly:

| Input | Distribution factor |
|---|---|
| `record` whose state is `verified` and whose identity/evidence bind the subject | satisfied |
| `record` whose state is `absent`, `published`, `unavailable`, or `candidate` | false / `distribution-not-verified` |
| `missing` | false / `distribution-row-missing` |
| `invalid` | false / `distribution-row-invalid` |

A missing `distribution_record` property, an object matching no or multiple
variants, a malformed stable-reference object, a record/record-type mismatch,
or an invalid lookup-key shape is facts-schema rejection and emits no
effective result. A well-formed reference whose resolved bytes/digest mismatch
is the typed invalid `stable-reference-mismatch` case. Thus typed negative
facts produce a false factor; malformed effective facts do not.

The `product_setup` property itself is required. Its object and every nested
object have `additionalProperties: false`. Every variant contains `subject`,
the complete exact top-level identity, and is exactly one of:

| `state` | Required fields | Forbidden fields |
|---|---|---|
| `not-required` | `subject`, `state`, `requirement_reference`, `contract: null` | `completion_reference`, `completion_identity`, `reason_code`, `reason_source` |
| `complete` | `subject`, `state`, `requirement_reference`, non-null `contract`, `completion_reference`, `completion_identity` | `reason_code`, `reason_source` |
| `incomplete` | `subject`, `state`, `requirement_reference`, non-null `contract`, `reason_code`, `reason_source` | `completion_reference`, `completion_identity` |
| `missing` | `subject`, `state`, `missing_kind`, `source_reference` | requirement, contract, completion, reason, and error fields |
| `invalid` | `subject`, `state`, `source_reference`, non-empty duplicate-free `error_codes` | requirement, contract, completion, reason, and missing-kind fields |

`requirement_reference`, `contract`, completion/reason references,
and `source_reference` are stable references. `reason_code` is
`setup-not-run` or `setup-failed`. `missing_kind` is
`product-requirement` or `completion-proof`; invalid error codes are
`product-requirement-invalid`, `consumer-setup-fact-invalid`, or
`setup-identity-mismatch`.

The `not-required` variant is valid only when the exact product row says
setup is not required; its requirement reference identifies that row. The
`complete` and `incomplete` variants are valid only when that row requires
setup; their `contract` equals its contract. A complete
`completion_reference` identifies a product-defined receipt whose validated
subject equals `completion_identity`; an incomplete `reason_source` identifies
the retained failed/not-run fact. Common evaluation validates identity
binding without interpreting product setup behavior.

Typed setup `missing` yields `setup-requirement-missing` owned by product or
`setup-completion-proof-missing` owned by consumer/environment. Typed
`invalid` maps its exact error codes to product for
`product-requirement-invalid`, consumer/environment for
`consumer-setup-fact-invalid`, and both owners for
`setup-identity-mismatch`. A missing property, malformed stable-reference
object, or object matching no or multiple variants is facts-schema rejection
and emits no effective result; a well-formed reference to an invalid setup
fact uses the typed invalid variant.

The evaluator derives, in order:

```
effective =
  product_supported
  and distribution_verified
  and identity_match
  and consumer_selected
  and environment_ready
  and product_setup_complete
```

`identity_match` is computed, not input. The product, distribution, and
environment identities participate in that factor and may yield false when
well-formed but unequal. Consumer selection shall equal its
plugin/version/surface fields and name the distribution route when applicable.
The setup `subject` is a schema constraint and shall equal the complete
top-level subject. A well-formed unequal `completion_identity` is represented
by the typed invalid `setup-identity-mismatch` variant and produces false.
Candidate, unsupported, unavailable, or mismatched non-setup authoritative
input is false only through its schema-valid facts variant. A missing or
malformed required top-level facts property or malformed factor union is
schema rejection and produces no result; typed missing/invalid variants
produce false.

`identity_match` is satisfied only when all three participating inputs expose
well-formed complete identities equal to the subject. A typed missing input
yields `identity-source-missing`; a typed invalid input yields
`identity-source-invalid`; and a schema-valid non-verified distribution row
without release identity yields `identity-source-unavailable`. Owners are the
union of the corresponding product, Stewards, or consumer/environment source
owners. These identity-factor failures are emitted in addition to the owning
source factor; no identity is fabricated.

The result contains the subject, `effective`, and exactly six factor objects.
Each factor contains `factor`, `satisfied`, `reason_codes`, `source_refs`, and
`owners`. A satisfied factor has empty `reason_codes` and `owners` and the
stable source references used to prove it. A failed factor has non-empty
reason codes, every source that produced the result, and only these
attributions:

| Failure | `reason_codes` | `owners` |
|---|---|---|
| Product row missing/candidate-or-unsupported/invalid | `product-row-missing`, `product-not-supported`, or `product-row-invalid` | `product` |
| Distribution row missing/not verified/invalid | `distribution-row-missing`, `distribution-not-verified`, or `distribution-row-invalid` | `stewards` |
| Identity differs between valid sources | `identity-mismatch` | owner union of every differing product, Stewards, and/or consumer/environment source |
| Identity source missing/invalid/unavailable | `identity-source-missing`, `identity-source-invalid`, or `identity-source-unavailable` | owner union of the unavailable product, Stewards, and/or consumer/environment sources |
| Selection missing/different | `consumer-not-selected` or `selection-mismatch` | `consumer/environment` |
| Environment missing/not ready/invalid | `environment-assessment-missing`, `environment-not-ready`, or `environment-assessment-invalid` | `consumer/environment` |
| Setup requirement missing/invalid | `setup-requirement-missing` or `product-requirement-invalid` | `product` |
| Required setup incomplete | `setup-not-run` or `setup-failed` | `consumer/environment` |
| Setup completion missing/invalid | `setup-completion-proof-missing` or `consumer-setup-fact-invalid` | `consumer/environment` |
| Setup completion identity mismatch | `setup-identity-mismatch` | `product`, `consumer/environment` |

`source_refs` contains every available stable source used by the factor. For
typed missing/invalid input it contains that variant's `source_reference`;
for incomplete setup it contains the product surface-contract reference and
`reason_source`. Unavailable sources are never fabricated.

The result is emitted or generated and is never an independently editable
authority matrix.

## Repository and product rollout obligations

`distribution/repository-scope.md` contains one canonical fragment stating
that the install door includes host-native catalogs, distribution metadata and
schemas, validators, and bounded pre-agent provisioner adapters, and excludes
product builds/content, copied product contracts, shared runtime, automatic
plugin selection, and release coordination. `generate` projects that fragment
between named managed markers in both `README.md` and `CLAUDE.md`;
`generate --check` requires byte equality and fails on a missing/stale block.

`distribution/product-adoptions.json` has `schema_version: 1` and one row per
distributed or legacy-stock plugin. Each row contains `plugin_id`,
`repository`, `state` (`required` or `complete`), sorted
`standing_decisions_to_reconcile`, sorted `ownership_changes`, and conditional
`adoption_decision`: forbidden while required and required as a stable
reference to an approved product-local decision while complete.

The initial obligations are exact:

| Product | Required product-local record |
|---|---|
| Grove | Adopt the family release/surface contract and partially supersede only `adr-0029`'s generic uniform-rollout-carrier ownership; retain Grove load, bridge, launcher, setup, and behavioral evidence ownership |
| Trellis | Supersede `decision-0036-plugin-versions-by-commit` for package releases only; introduce SemVer/tag/surface adoption; retain the payload content stamp as a distinct identity and retain Trellis hook/fallback/live-rule/refresh evidence |
| Wisp or later plugin | Approve its own release/surface and ownership adoption before first catalog publication |

A `required` row blocks conforming publication and verification. The bounded
legacy transition may keep only an already-baselined row published with its
transition exception while adoption remains required; it still blocks
`wave-close` and effective support. Product adoption records are stable
references only—Stewards does not edit an outside product repository or
ratify its decision.

## Validation and generation interface

`distribution/manage` supplies:

| Command | Required result |
|---|---|
| `validate-product --phase pre-tag --package-root <path> --release-metadata <path>` | Preserve the landed interface: validate the pre-tag contract and emit exactly `{"expected_tag": string, "package_version": string}` |
| `validate-product --phase release --package-root <path> --release-metadata <path>` | Repeat pre-tag validation, validate extensions with the peeled commit, resolve/validate every package tag, appended history row, compatibility change, bump, and approval, then preserve v1's release-identity result as exactly `{"expected_tag": string, "package_version": string, "source_commit": string}` |
| `validate-door` | Validate all schemas, sources, cross-references, identities, baselines, host projections, and verified retained product bytes through `STEWARDS_PRODUCT_REPOSITORIES` |
| `generate` | Deterministically write both host catalogs and `distribution/availability.md` |
| `generate --check` | Make no writes; fail and name every stale catalog, availability, README, or CLAUDE derivative |
| `legacy-discover --baseline-commit <commit>` | Read only the two host manifests at that commit and emit sorted entry keys/fingerprints |
| `wave-close` | Run `validate-door`; fail while transition stock remains |
| `effective --facts <path>` | Validate authoritative facts and emit the typed result |

`--package-root` resolves to an existing package directory inside a Git
checkout; `--release-metadata` is a normalized path relative to that root.
The validator reads package inputs from that root, resolves repository refs
with `git -C <package-root>`, and passes the same resolved root to the
inventory-provider and extension protocols. It does not fetch. In `release`,
the checkout's exact tag ref supplies `source_commit`; caller or working-tree
HEAD identity cannot substitute for it.

Every emitted object uses the canonical JSON grammar already defined by this
spec, followed by one LF. Successful non-emitting commands write no stdout or
stderr. A contract failure exits `1`, writes no stdout, and writes exactly one
UTF-8 stderr line `error: <message>\n`, where `message` contains no CR or LF.
Argument parsing retains the command-line parser's exit `2`. An emitting
command exits `0` only after its complete validation succeeds; no partial
identity or projection is emitted on failure.

Generation orders maps by schema-defined key and arrays by their declared
identity key, emits UTF-8 JSON with LF and no insignificant whitespace, and
emits Markdown rows in the same key order.

## Immutable transition baseline

`distribution/legacy-baseline.json` has
`baseline_source_commit: 8b9007dd4f4559cf2a83976391c71392a4628730`,
the exact post-PR-21 main commit,
`fingerprint_algorithm: kodhama-selector-v1-sha256`, and sorted rows containing
catalog key, manifest path, normalized selector, and selector fingerprint. It
contains no discovery-time value.

The required discovered key set is immutable:

| `plugin_id` | `surface_id` | Manifest |
|---|---|---|
| `trellis` | `claude-code.local.interactive` | `.claude-plugin/marketplace.json` |
| `grove` | `claude-code.local.interactive` | `.claude-plugin/marketplace.json` |
| `grove` | `codex.local.interactive` | `.agents/plugins/marketplace.json` |

`legacy-discover` reads those manifests from the baseline commit, not the
working tree. Its sorted output must match this set and the checked-in
fingerprints exactly. A discrepancy fails and requires upstream decision
clarification; it never adds eligibility.

For each host-native entry, the host adapter first validates spec 0001's exact
selector union, then extracts the fingerprint projection with `repository`,
normalized relative `path`, `kind`, and flat `ref`. A mutable selector
normalizes to `ref: ""`; an immutable selector normalizes to its nested
`ref.value`.

The selector fingerprint is SHA-256 over the UTF-8 bytes of exactly this JSON
object, with keys in the shown order, no whitespace or trailing LF, strings
normalized to Unicode NFC, and this exact escaping: `"` and `\` use `\"` and
`\\`; U+0000–U+001F use lowercase `\u00xx`; `/` and every other code point are
not escaped and are encoded directly as UTF-8:

```
{"kind":"<kind>","manifest_path":"<manifest_path>","path":"<path>","plugin_id":"<plugin_id>","ref":"<ref-or-empty>","repository":"<repository>","surface_id":"<surface_id>"}
```

All values are JSON strings; numbers, booleans, null, additional keys, alternate
key order, or non-NFC strings are invalid. Baseline rows sort by
`(surface_id, plugin_id)`.

`distribution/legacy-stock-initial.json` is the immutable initial
nonconforming subset. It contains exactly one row: the baseline
`(trellis, claude-code.local.interactive)` key, manifest path, and selector
fingerprint, plus this sorted `missing_contract_elements` set:
`canonical-semver-authority`, `immutable-release-tag`,
`product-adoption-decision`, `version-bound-surface-contract`; literal
disclosure `legacy published stock`; and
`terminal_action: adopt-or-delist`.

`distribution/legacy-stock.json` always retains
`initial_stock_reference`, a `repo-path` stable reference to the exact initial
file at the full source commit that first materialized it, including its
SHA-256. Its `rows` initially equal the initial file's single row and later
permit removals only; the reference and every retained row/field are
immutable.

`validate-door` resolves
`initial_stock_reference.source_commit:distribution/legacy-stock-initial.json`
with Git, requires its raw-byte SHA-256 to equal the reference, requires the
working-tree initial file to be byte-identical, validates the exact one-row
contents above against the baseline fingerprint, and requires current stock
rows to be an exact ordered subset. A missing/unresolvable comparison commit,
digest mismatch, changed initial file/reference/row, addition, or reordering
fails.

The baseline and initial-stock file are write-once and immutable, not
append-only: version 1 permits neither edits nor appended rows. A future
differently scoped baseline requires a new schema/file identity and a new
decision; it never changes these files or grants this transition new
eligibility.

Ordinary validation requires every remaining stock row to be `published`,
forbids verified/effective/clean-install claims, and renders its disclosure.
`wave-close` fails until the stock file is empty. A removal is valid only with
the same-change conforming catalog record or delisting.

## Fixtures

`distribution/fixtures/metadata/manifest.json` names each fixture, command,
expected exit class, and guarded requirement.

Positive fixtures:

| Fixture | Proves |
|---|---|
| `positive/plain-authority-json-carriers/` | Deterministic VERSION plus JSON Pointer extraction and parity |
| `positive/release-tag-resolution/` | Expected Git tag is the only tag source and peels to the emitted commit |
| `positive/typed-supported-row/` | Exact evidence/load/support/setup objects validate |
| `positive/product-extension/` | Nested namespaced product data survives canonicalization; distinct metadata/host identities bind exact runtime digests, run in exact order, and pass the repeated v1 process protocol |
| `positive/immutable-extension-runtime/` | An exact platform manifest and image enumerate every executable, loader, library, configuration file, and link; only that read-only runtime plus package/private overlays is visible |
| `positive/canonical-nested-json/` | Nested objects, arrays, NFC strings, control/non-BMP scalars, booleans, null, and numbers produce the single canonical byte stream |
| `positive/retained-verified-release/` | Local no-fetch resolution binds selector, product blobs, history, and catalog identity |
| `positive/published-mutable-catalog/` | Typed mutable selector remains published |
| `positive/verified-immutable-catalog/` | Exact tag/commit and clean-install-evidence schema validate |
| `positive/unavailable-exact-key/` | Unavailable uses the complete provisioner identity |
| `positive/effective-supported/` | Authoritative sources derive all six true factors |
| `positive/effective-setup-complete/` | Required setup identity/reference derive a true setup factor |
| `positive/legacy-baseline/` | Exact PR-21 discovery matches immutable baseline |
| `positive/selector-fingerprint/` | Canonical selector bytes produce the checked-in SHA-256 |
| `positive/complete-release-inventory/` | Every host manifest, payload identity, public-contract item, and support derivative is bound |
| `positive/pre-1.0-breaking-minor/` | Human-ratified breaking change below 1.0 uses at least a minor bump |
| `positive/typed-negative-effective-facts/` | Missing/candidate/unsupported/unavailable typed facts produce owned false factors |
| `positive/legacy-transition-exception/` | Only an immutable-baseline stock row receives the bounded publication waiver |

Negative fixtures:

| Fixture | Required failure |
|---|---|
| `negative/ambiguous-version-bytes/` | Reject BOM, whitespace, duplicate JSON keys, non-string, or ambiguous extraction |
| `negative/carrier-mismatch/` | Reject unequal extracted carrier |
| `negative/caller-supplied-tag/` | Reject tag/commit substitution for the expected Git ref |
| `negative/identity-substitution/` | Reject package version as commit or payload |
| `negative/untyped-evidence-or-path/` | Reject stringly evidence, load, support, publication, or retirement fields |
| `negative/surface-version-mismatch/` | Reject another package version |
| `negative/unknown-or-duplicate-surface/` | Reject unknown/duplicate/retired use |
| `negative/supported-without-proof/` | Reject incomplete typed proof |
| `negative/non-support-without-disclosure/` | Reject incomplete candidate/unsupported row |
| `negative/verified-mutable-selector/` | Reject mutable identity binding |
| `negative/clean-install-identity-mismatch/` | Reject clean-host proof for another identity/environment |
| `negative/unavailable-partial-key/` | Reject omitted plugin/version identity |
| `negative/effective-boolean-input/` | Reject caller-authored factor booleans |
| `negative/effective-identity-mismatch/` | Emit false with deterministic owners |
| `negative/effective-setup-conditional-fields/` | Reject setup status/identity/reason/source inconsistency |
| `negative/effective-setup-missing-or-invalid/` | Reject facts before evaluation and emit no effective result |
| `negative/source-selector-union/` | Reject extra fields, mutable ref, malformed repository/path, or non-binding immutable ref |
| `negative/distribution-binding-union/` | Reject mixed catalog/provisioner fields or incomplete provisioner identity |
| `negative/omitted-host-manifest-or-payload/` | Reject inventory/carrier/history incompleteness |
| `negative/stale-support-derivative/` | Reject a support document or manifest claim that differs from the product surface contract |
| `negative/prior-tag-moved-reused-or-unrecorded/` | Reject deleted, moved, reused, or history-omitted prior tags |
| `negative/semver-underbump-or-unratified/` | Reject a bump below the compatibility minimum or without product-human approval |
| `negative/false-claim-or-retirement-underbump/` | Reject delayed/unclassified claim withdrawal or an insufficient breaking bump |
| `negative/catalog-contract-version/` | Reject missing/mismatched product contract version outside the bounded legacy exception |
| `negative/rollout-reconciliation/` | Reject conforming publication without product-local adoption or stale repository-scope docs |
| `negative/prerelease-or-build-transition/` | Reject prerelease regression, stable-to-same-core prerelease, equal-precedence build-only release, or an uncovered cumulative bump |
| `negative/inventory-extractor-or-change-set/` | Reject unknown manifest/extractor/annotation grammar, wrong fingerprint bytes, or caller-misclassified changes |
| `negative/legacy-stock-initial-drift/` | Reject a missing comparison commit, digest mismatch, changed initial row/reference, addition, or reorder |
| `negative/baseline-working-tree-discovery/` | Reject discovery not sourced from the baseline commit |
| `negative/baseline-extra-entry/` | Reject expanded legacy eligibility |
| `negative/baseline-fingerprint-canonicalization/` | Reject alternate ordering, normalization, or bytes |
| `negative/wave-close-with-stock/` | Reject first-wave completion |
| `negative/stale-derived/` | Name every stale derivative without writes |
| `negative/extension-validator-protocol/` | Reject wrong identity/order, argv/env/request/result/exit, stderr, differing runs, timeout, oversize output, forbidden path/write, caught socket attempt, or persistent mutation |
| `negative/extension-runtime-unavailable-or-drifted/` | Reject absent/mismatched digest, platform mismatch, missing/extra or type/mode/hash/link-drifted entry, unenumerated loader/configuration/executable, forbidden runtime path, or live-host runtime substitution before spawn |
| `negative/canonical-json-ambiguity/` | Reject invalid UTF-8/scalars/numbers, duplicate pre/post-NFC keys, or non-canonical key order, escaping, number bytes, whitespace, or LF |
| `negative/retained-verified-release/` | Reject absent/wrong checkout, origin, Git object mode, path composition, digest, ancestry, last row, or release binding |
| `negative/release-interface-output/` | Reject partial or non-canonical success/failure output and a release ledger other than prior rows plus one exact append |

## Acceptance criteria

### Scenarios

**S1 — Deterministic release identity**

Given valid typed extractors and an expected Git tag, when release validation
runs, then it derives one authority version, equal carriers, the computed tag,
and the peeled full commit without accepting caller identity substitutions.

**S2 — Extraction ambiguity**

Given ambiguous bytes, duplicate JSON keys, a missing pointer, or a non-string
selection, when version extraction runs, then validation fails before release.

**S3 — Typed supported row**

Given a supported row, when any evidence, load path, support record, setup
declaration, or exact binding is missing or stringly typed, then validation
fails.

**S4 — Non-support**

Given candidate, unsupported, or absent product state, when availability or
effective support is rendered, then no behavioral support claim is produced.

**S5 — Typed catalog verification**

Given a typed immutable selector or exact verified acquisition plus matching
release identity and clean-host evidence, when the row is validated, then only
that exact catalog key becomes verified and the evidence schema binds the same
release, surface, environment, and distribution route.

**S6 — Mutable publication**

Given a mutable selector and typed publication proof, when validated, then
published succeeds and verified fails.

**S7 — Coherent unavailable route**

Given an unavailable route row, when its plugin or package version is omitted,
then validation fails; when its complete key and reason are present, then it
makes only an unavailable claim.

**S8 — Effective support**

Given authoritative product, distribution, selection, environment, and setup
sources, when evaluation runs, then it derives all six factors, computes
identity match, and emits deterministic failure owners without accepting
caller factor booleans; setup completion is true only for its conditionally
valid exact identity/reference.

**S9 — Immutable adoption baseline**

Given the post-PR-21 commit, when legacy discovery runs, then it reads that
commit's two manifests, canonicalizes each selector with
`kodhama-selector-v1-sha256`, and matches exactly the three enumerated keys and
fingerprints without expanding or appending eligibility.

**S10 — Terminating legacy stock**

Given remaining transition stock, when ordinary validation runs, then it is
disclosed as published-only; when `wave-close` runs, then it fails until every
row is adopted or delisted.

**S11 — Deterministic derivatives**

Given valid source records, when generation runs twice, then every derivative
is byte-identical; when a derivative is stale, then check mode names it without
writing.

**S12 — Evidence isolation**

Given proof for one exact identity, when another row is validated, then the
first proof cannot satisfy the second.

**S13 — Exact distribution union**

Given a clean-install binding or catalog selector with an extra, missing,
mixed-variant, mutable-ref, or non-binding field, when schema and identity
validation run, then validation rejects it before verified availability.

**S14 — Setup schema outcome**

Given a missing or invalid setup input, when effective facts validation runs,
then its exact typed variant produces a false setup factor with deterministic
owners; given a malformed variant, when validation runs, then it rejects the
facts and emits no result.

**S15 — Distribution negative facts**

Given a schema-valid non-verified, missing, or invalid distribution-record
variant, when effective evaluation runs, then the distribution factor is false
with its exact reason and Stewards owner; given a malformed union, when facts
validation runs, then it rejects the input and emits no result.

**S16 — Complete release inventory**

Given a package with host manifests, payload identities, public-contract
items, support documentation, or host-manifest claims, when pre-tag validation
runs, then every discovered item is declared, every host version carrier
matches, every payload is release-bound, and every support derivative equals
the version-bound surface contract.

**S17 — Immutable tags and ratified compatibility**

Given prior release history and a current public-contract diff, when release
validation runs, then every prior tag still peels to its recorded commit, the
new version meets the patch/minor/major table including pre-1.0, false-claim,
and supported-surface retirement rules, and a product-human approval binds the
comparison.

**S18 — Catalog contract and legacy exception**

Given a conforming catalog row, when validation runs, then its product contract
path/version match the release; given a nonconforming row, then only an
identical remaining immutable legacy-stock row may stay published and it can
never become verified or effective.

**S19 — Rollout ownership**

Given Grove, Trellis, or another distributed plugin, when conforming
publication is attempted, then its product-local adoption record reconciles
the enumerated standing release/rollout ownership and both repository-scope
documents match the bounded install-door source.

**S20 — Complete false-result ownership**

Given typed missing, candidate, unsupported, unavailable, mismatched,
not-ready, incomplete, or invalid factor inputs, when evaluation runs, then
every affected source and identity factor is false with exact reason codes,
source references, and owner unions.

**S21 — Prerelease and build ordering**

Given release history containing prerelease or build metadata, when release
validation compares the next version, then SemVer precedence, unique
equal-precedence positions, cumulative prerelease-line compatibility, and the
exact transition table determine acceptance and minimum bump.

**S22 — Executable inventory grammar**

Given host manifests, payloads, public-contract items, derivatives, and a
classified change set, when inventory validation runs, then every kind,
extractor, canonical fingerprint, annotation, and derived change object
matches the exact grammar and bytes, including deterministic
`surface-support.<surface_id>` supported/candidate/unsupported transitions and
the non-self-referential approval projection/final augmentation.

**S23 — Immutable initial stock**

Given current transition stock, when `validate-door` runs, then it resolves
the immutable initial-stock comparison commit, verifies raw digest and exact
one-row contents, and accepts only an ordered removal-only subset.

**S24 — Bounded product extension validation**

Given declared metadata and other-host extension validators, when pre-tag or
release validation runs, then each unique identity runs in the exact order
with the exact v1 request and filesystem/runtime boundary twice and passes only
when both executions return identical matching canonical `pass` results with
exit `0`, no stderr, no forbidden-path or network-attempt audit flag, and no
persistent mutation.

**S25 — Retained verified catalog release**

Given a verified catalog row and explicit local repository mapping, when
`validate-door` runs, then it resolves the immutable selector, retained
metadata/surface/inventory blobs, and descendant history-reference blob
without fetching and accepts only when the complete last history row and
digests bind the row's exact product release.

**S26 — Public release-engine result**

Given a valid pre-tag package, when `validate-product --phase pre-tag` runs,
then it preserves the two-field canonical result; given the subsequently
tagged approved release and one correctly appended ledger row, when
`--phase release` runs, then it validates that exact append and preserves the
three-field release-identity result, and any contract failure emits no partial
result.

**S27 — Canonical arbitrary JSON**

Given arbitrarily nested schema-valid JSON containing objects, arrays,
strings, numbers, booleans, and null, when any canonical request, result,
fingerprint, or digest preimage is formed, then the recursive grammar emits
one NFC, scalar-key-ordered, exactly escaped, shortest-number UTF-8 byte stream
and rejects invalid or normalization-duplicate input.

**S28 — Immutable validator runtime**

Given a validator declaration with an exact runtime-manifest digest and a
matching launcher platform, when extension validation starts, then the
launcher resolves and verifies that exact local manifest and complete image,
exposes only its enumerated read-only entries plus the package, private
temporary directory, and `/dev/null` overlays, and fails before spawn when the
digest, platform, content, or enforcement is unavailable or differs.

### Requirements and invariants

- **R1:** The system shall extract the canonical package version and every
  carrier using the declared deterministic extractor grammar.
- **R2:** When release validation runs, the system shall compute the expected
  tag from plugin id and extracted version and shall derive source commit only
  by peeling that exact repository tag.
- **R3:** When extraction is ambiguous or a carrier differs, the system shall
  fail before publication.
- **R4:** The system shall keep package version, release tag, source commit,
  and payload identity distinct.
- **R5:** The system shall require typed stable references, evidence bindings,
  load paths, support records, publication evidence, and retirement objects.
- **R6:** When a surface is retired, the system shall reserve its id and reject
  new support or availability rows for it.
- **R7:** When a product row is supported, the system shall require exact
  typed behavioral evidence, load path, support record, and setup declaration.
- **R8:** When a product row is candidate or unsupported, the system shall
  require missing capability and disclosure and shall make no support claim.
- **R9:** When a catalog selector is mutable, the system shall cap the record
  at published.
- **R10:** When catalog or provisioner state is verified, the system shall
  require exact identity-bound typed evidence, and catalog verification shall
  require one valid `clean-install-evidence.v1` object.
- **R11:** Every provisioner availability state shall use the complete exact
  route, surface, plugin, and package-version key.
- **R12:** The system shall derive effective-support factors from authoritative
  typed sources and shall reject caller-authored factor booleans.
- **R13:** When effective support is false, the system shall emit every failed
  factor, reason code, source reference, and deterministic owner attribution.
- **R14:** The system shall keep effective results generated and shall not
  persist a third editable matrix.
- **R15:** Legacy discovery shall read only commit
  `8b9007dd4f4559cf2a83976391c71392a4628730` and shall match the enumerated
  baseline exactly.
- **R16:** The immutable baseline shall never gain or change a row, and
  transition stock shall permit removals only.
- **R17:** While transition stock remains, the system shall disclose it,
  forbid verified/effective claims, and fail `wave-close`.
- **R18:** The system shall generate both host catalogs and availability
  documentation deterministically from named sources.
- **R19:** When a derivative is stale, check mode shall fail without writes and
  shall name every stale path.
- **R20:** Evidence shall satisfy only its exact host, surface, environment,
  mode, plugin release, selector, and provisioner version.
- **R21:** The system shall keep product extensions namespaced and shall run
  any declared product extension validator without interpreting product
  behavior.
- **R22:** The system shall not copy product payloads, product behavior, or
  product evidence into Stewards authority records.
- **R23:** When product setup is required, the system shall require
  conditionally valid completion identity/reference or incomplete
  reason/source fields and shall attribute failure by the enumerated rules.
- **R24:** The system shall derive every baseline selector fingerprint from
  the exact fixed-order NFC JSON preimage and SHA-256 algorithm.
- **R25:** Every distribution binding and source selector shall match exactly
  one additional-properties-forbidden discriminated variant.
- **R26:** When a selector is immutable, the system shall bind its typed tag
  or commit ref exactly to the subject release identity.
- **R27:** When a setup input is typed missing, incomplete, or invalid, the
  evaluator shall emit the exact false setup factor and owners; when its union
  is malformed, it shall reject facts and emit no result.
- **R28:** The evaluator shall distinguish a verified distribution record,
  a schema-valid non-verified record, a typed missing/invalid record, and a
  malformed facts union using the exact satisfied, false, or rejection
  semantics.
- **R29:** Product release validation shall inventory every host manifest,
  payload identity, public-contract item, public support derivative, and
  host-manifest support claim and shall reject any omitted or stale item.
- **R30:** Every inventoried host manifest shall be a declared host-manifest
  version carrier and shall extract the authority version.
- **R31:** Release validation shall reject any prior package tag that is
  moved, deleted, reused, or absent from append-only release history.
- **R32:** The product-human release gate shall ratify the inventory diff and
  SemVer bump, which shall meet the exact compatibility minimum including
  pre-1.0 breaks, false-claim withdrawal, and supported-surface retirement.
- **R33:** Every conforming published or verified catalog row shall record the
  matching product contract path and family contract version.
- **R34:** Only an identical remaining immutable-baseline legacy-stock row
  shall receive the bounded published-only transition exception.
- **R35:** Conforming publication shall require a complete product-local
  adoption record that preserves product behavior ownership and reconciles
  the enumerated standing decisions.
- **R36:** Repository generation shall keep README and CLAUDE install-door
  scope blocks byte-equal to the bounded canonical scope fragment.
- **R37:** Effective evaluation shall emit owned false source and identity
  factors for every typed missing, candidate, unsupported, unavailable,
  mismatched, not-ready, incomplete, or invalid input.
- **R38:** Release history shall reject equal-precedence build variants,
  prerelease regressions, and same-core stable-to-prerelease transitions and
  shall enforce cumulative minimum bumps for iterations/promotions.
- **R39:** Inventory validation shall execute only the enumerated manifest,
  extractor, fingerprint, compatibility-annotation, and classified-change-set
  grammars, including exact surface contract ids, row fingerprints,
  before/after nullability, complete non-supported transition mapping,
  evidence-reference sets, and approval projection/final ordering.
- **R40:** `validate-door` shall resolve the initial-stock comparison commit
  and shall verify its raw digest, exact immutable Trellis/Claude row, and
  current ordered removal-only subset.
- **R41:** When a product extension validator is declared, the release engine
  shall invoke each unique metadata/host identity in exact order and only with
  the exact v1 argv, working directory, environment, filesystem/runtime,
  network, stdin, output, exit, timeout, size, and side-effect contract.
- **R42:** When either repeated extension-validator execution differs, fails
  its result schema, crosses a process boundary, or sets a forbidden-path or
  network-attempt audit flag, the release engine shall fail regardless of
  handled child errors and without interpreting or promoting the product
  finding.
- **R43:** When a verified catalog row is validated, `validate-door` shall use
  only its explicit local repository mapping and retained Git objects and
  shall not fetch, read product working-tree files, or execute product code.
- **R44:** A verified catalog row shall bind its immutable selector, retained
  release metadata, surface contract, inventory, and repo-path history
  reference to the exact package version, tag, commit, payloads, digests,
  approval, and complete last ledger row.
- **R45:** The public release-engine commands shall preserve the exact pre-tag
  result and shall emit the exact release result or the one-line failure
  contract without any partial output.
- **R46:** Every canonical JSON use shall apply the single recursive object,
  array, string, number, boolean, and null grammar and shall reject invalid
  UTF-8/scalars/numbers and duplicate pre- or post-NFC object keys.
- **R47:** Every host-manifest row shall have one unique normalized
  `(host, path)` identity, and extension-validator execution shall use the
  exact metadata-namespace-then-host-identity order without path-based
  deduplication.
- **R48:** The extension launcher shall deny and audit every forbidden
  filesystem or network attempt across the complete process tree, and any
  audit flag shall fail validation even when the validator catches the error
  and otherwise returns `pass`.
- **R49:** Every extension-validator declaration shall bind an exact
  platform-specific immutable runtime-manifest digest; the launcher shall
  verify every enumerated entry and shall fail before spawn rather than fetch,
  substitute live-host content, or continue when that exact runtime or its
  credential-free read-only projection is unavailable.

## Open questions

None.

## Rubric check

No dedicated spec-quality rubric or `.grove/config.toml` token exists.
Self-check used the local contract-author rules, `specs/README.md`,
`.grove/lifecycle.md`, and `.grove/versioning.md`.

| Check | Result | Evidence |
|---|---|---|
| Frontmatter, lifecycle, dependencies | PASS | Required fields and decision `implements` edges present; direct decisions approved; append-only ids unpinned |
| Versioned amendment | PASS | Behavioral counter advanced to v2; section-level WHAT/WHY/SCOPE/POINTER/VALUE/CONFIDENCE delta is present; current dependent spec/index/test pin was updated |
| Required sections and grammars | PASS | S1–S28 are GWT; R1–R49 are EARS `shall` statements |
| Decision boundary | PASS | Stewards contract/availability machinery is typed; product behavior, evidence creation, release judgment, tag creation, and setup execution remain excluded |
| F1 deterministic version/tag source | CLOSED | Typed byte extraction, typed carriers, computed tag, and peeled repository ref are normative |
| F2 typed contract fields | CLOSED | Common schemas fully type evidence, load, support, publication, selector, retirement, and provisioner fields |
| F3 unavailable identity | CLOSED | Every state requires the same complete provisioner key |
| F4 effective facts/results | CLOSED | Authoritative input/output schemas, derived identity match, reason codes, source refs, and deterministic owners are specified |
| F5 immutable legacy discovery | CLOSED | Exact PR-21 commit and three-entry baseline are enumerated; discovery cannot expand eligibility; stock is removals-only |
| Pass-2 F1 clean-install evidence | CLOSED | Dedicated schema, exact subject/binding/environment/install/observation fields, and cross-identity rejection are normative |
| Pass-2 F2 product setup facts | CLOSED | Exact identity and status-conditional completion/reason/source fields plus deterministic reason/source/owner rules are normative |
| Pass-2 F3 baseline fingerprint | CLOSED | Fixed canonical JSON/SHA-256 algorithm is defined; baseline is write-once with neither edits nor appended rows |
| Final F1 distribution binding grammar | CLOSED | Exact catalog-selector/provisioner-acquisition union, nested identity, required/forbidden fields, and no-additional-properties rule are normative |
| Final F2 setup invalidity outcome | CLOSED | Typed missing/incomplete/invalid setup variants produce deterministic false; malformed unions are rejected with no result |
| Final F3 selector grammar | CLOSED | Mutable/tag/commit selector variants, repository/path/ref grammar, subject binding, and legacy flattening are exact |
| Final-pass F1 distribution facts semantics | CLOSED | Exact record/missing/invalid input union maps verified, non-verified, missing, invalid, and malformed cases to satisfied, typed false, or schema rejection |
| Conformance release identity/completeness | CLOSED | Implements edge, full manifest/payload inventory, carrier parity, tag history, public-contract comparison, human bump ratification, and support-derivative checks are normative |
| Conformance availability/effective semantics | CLOSED | Catalog product-contract version, bounded legacy exception, complete typed negative facts, and owner unions are normative |
| Conformance rollout/ownership | CLOSED | Canonical README/CLAUDE scope plus Grove/Trellis/future-product adoption reconciliation are required before conforming publication |
| Intrinsic F1 SemVer edge transitions | CLOSED | Core, prerelease iteration/promotion/regression, cumulative minimum, and equal-precedence build rules are exact |
| Intrinsic F2 executable inventory grammar | CLOSED | Manifest/extractor/fingerprint/annotation/change-set shapes, all surface-row transition mappings, exact evidence sets, and non-self-referential approval ordering are enumerated |
| Intrinsic F3 immutable initial stock | CLOSED | Exact initial row, stable comparison commit/digest, working-file equality, and removal-only comparison are normative |
| Adversary remediation F1–F4 | CLOSED | Generic nested canonical JSON including number bytes; unique host identity/order; manifest-derived PATH and exact immutable runtime/package/private visibility with forbidden-path audit; and process-tree network-attempt audit are normative |
| Second-adversary F3 immutable runtime | CLOSED | Every declaration binds a platform-specific canonical manifest digest; every runtime entry is content/type/mode/link enumerated; live-host substitution and unavailable or drifted images fail before spawn |
| v2 whole-spec execution boundary | CLOSED | Recursive canonical JSON, unique validator identities/order, digest-bound audited filesystem/runtime/network boundary, extension subprocess request/result/limits, retained verified-catalog resolution, release-history digest/append staging, and public CLI results are exact |
| Whole-corpus validation | NOT CLAIMED | Issue #20 blocks literal full-corpus PASS; this artifact uses strict YAML/exact ids and was checked change-scoped |

**Result: PASS for author self-check.**

## Gate record

The maintainer's 2026-07-24 act approved v1 after spec-adversary and
conformance review. This v2 amendment passed the author self-check above and
is `gated`; the prior v1 act is not reused as approval of S24–S28 or R41–R49.
