# Stewards backlog — per-issue migration plan

**A plan, not an authorisation.** Produced 2026-08-01 by applying
`plugins/kodhama/skills/issues/SKILL.md` to every open Stewards issue. Nothing
here has been applied. Applying it is a separate act needing its own intent —
the wave brief's Boundaries hold that *"migration of legacy issues is NOT in
this wave"*, and the skill itself says it *"is never an instruction to sweep
the backlog."*

Prefix mappings follow `legacy-mapping.md`; this file adds the per-issue
judgment that the generic table cannot make.

**In force:** verified — `gh api /orgs/kodhama/issue-types` returns all six
enabled (`Task`, `Bug`, `Feature`, `Research`, `Decision`, `Epic`), and all
fifteen labels exist in this repo. Nothing here is blocked on provisioning.

**Corpus:** 14 open issues, 2026-08-01. **Zero carry any label or type today.**

---

## 1. Close instead of migrating — check these first

Applying the taxonomy surfaced two issues whose premise has expired. **Neither
should be relabelled; relabelling dead work is how a backlog stays big.**

| # | Title | Finding |
|---|-------|---------|
| **54** | *Only trellis has an automated PR reviewer — grove, wisp and stewards merge unreviewed* | **Measured false today.** `grove`, `wisp`, `stewards` and `trellis` all carry `.github/workflows/claude-code-review.yml`. The stated absence is gone; the residue — reviewers that misreport — is already tracked by **#63** and **#66**. Close as **completed**, referencing those two |
| **5** | *[high-priority] Evaluate + build a kodhama plugin for family conventions* | **Substantially delivered.** The `kodhama` plugin exists at `0.3.0` carrying the issue convention. *"Evaluate"* and the first *"build"* are done. **Judgment needed:** close as completed, or narrow to what remains — the plugin's own purpose is still undecided, which is the open Lane B item and arguably a different issue |

`gh issue close` takes `completed`, `not planned`, or `duplicate`. **There is
no `not-planned` spelling** — the hyphenated form is rejected.

## 2. Titles already conformant — metadata only

No rewrite needed. These were filed after the convention was drafted.

| # | Type | Labels |
|---|------|--------|
| **66** | `Bug` | `facing: system` · `severity: broken-feature` · `stage: ready` |
| **63** | `Bug` | `facing: system` · **`severity: blocker`** · `stage: ready` |
| **65** | `Decision` | `stage: triage` |

**Why #63 is `blocker` and #66 is not.** Both are reviewer defects. #66 fires
once and then stops — later commits ship unreviewed, and *the output says so*.
#63 reports **PASS when it produced no verdict**: a reader sees a green gate
and merges. Read by what a reader does wrongly, a false green is worse than a
visible gap.

## 3. Prefix strips — mechanical, no title rewrite

| # | Prefix | Becomes | Type | Stage |
|---|--------|---------|------|-------|
| **47** | `[deferred]` | **`deferred`** | see §5 | `triage` |
| **46** | `[consider]` | *(nothing — it was a stage all along)* | `Decision` | `triage` |
| **5** | `[high-priority]` | **`priority: high`** | see §1 | — |
| **4, 3, 2, 1** | `idea:` ×4 | *(nothing — a stage, not a kind)* | see §5 | `triage` |

**This is the taxonomy's central claim doing real work.** Six of fourteen
issues carried a prefix that looked like a kind and was really a position in a
lifecycle. All six collapse to `stage: triage` with no type violence — which
is what the 38-issue corpus study predicted, now confirmed on live data.

## 4. Title rewrites — imperative or prefix form

The skill requires titles that state the situation, not the instruction.

| # | Current | Proposed |
|---|---------|----------|
| **46** | `[consider] A compacting run over the decision and spec corpora — and whether append-only permits it` | *Whether append-only permits a compacting run over the decision and spec corpora* |
| **45** | `Family marketplace check: verify every published plugin's assets resolve, no key required` | *No check verifies that a published plugin's assets resolve from the marketplace* |
| **39** | `Untangle and simplify catalog admission after posture/support decoupling` | *Catalog admission is more complex than the posture/support split now requires* |
| **20** | `Define evidence-preserving handling for malformed legacy artifact metadata` | *Malformed legacy artifact metadata has no defined evidence-preserving handling* |
| **4** | `idea: unify CI/cloud config across all family repos on shared primitives` | *Family repos each carry their own CI and cloud configuration* |
| **3** | `idea: spec the process layer itself — processes as first-class artifacts` | *Whether processes become first-class specified artifacts* |
| **2** | `idea: operationalize the conductor — a PM/PO agent team across related projects` | *The conductor role is performed by hand rather than by a standing agent team* |
| **1** | `idea: one product/project-management model for the stack` | *The stack has no single recorded product- and project-management model* |

**#45's prefix is not an area.** `legacy-mapping.md` maps `Word:` prefixes to
`area: *` because in the product repos they were areas all along. *"Family
marketplace check:"* is a scope phrase, not a recurring area, and this repo
defines no `area:` labels — the three-issue minimum is unmet. Rewrite as prose;
coin nothing.

## 5. Where the skill does not decide — these need you

**Four issues, and the pattern in two of them is worth more than the answers.**

| # | The fork | What it turns on |
|---|----------|------------------|
| **39** | `Decision` or `Task` | The body says *"Define the smallest honest catalog-admission path"* — is the definition the deliverable, or is the correct state derivable from `kodhama-0021` and only unimplemented? |
| **20** | `Decision` or `Task` | Same shape: *"Define evidence-preserving handling…"* |
| **47** | `Decision` or `Feature` + `deferred` | It needs `kodhama-0017` widened first. The threshold — *"until the choice is made there is nothing to build"* — is met, which argues `Decision`. But the issue's own deliverable is the ping |
| **1, 3** | `Decision` or `Research` | *"one model for the stack"*, *"processes as first-class artifacts"* — is the deliverable a finding or a choice? |
| **2, 4** | `Epic` or `Feature` | Both plausibly have children shipping separately. `Epic` needs **both** children *and* coherence-of-the-set as its own deliverable. Neither has children today |

**#39 and #20 are the same defect twice: a `Define X` title where the
definition is the deliverable.** The skill's `Decision` row says the threshold
is *"until the choice is made there is nothing to build"*, and its `Task` row
claims *"a change to something that already exists"*. Both fire. **This is a
real gap in the vocabulary, not a gap in these two issues** — worth carrying
back to `kodhama-0026` if a third instance appears.

**None of the four blocks the rest.** Under the skill's own rule — *"never stop
at an unknown: leave that field unset and continue"* — every other dimension
can be set now and the type left unset while these sit in `triage`, where an
unset type is legitimate.

## 6. Sequencing, if this is approved

1. **Close #54 and settle #5 first.** Migrating dead issues is wasted work and
   inflates every count downstream.
2. **Apply §2** — three issues, metadata only, no title touched. Lowest risk,
   and it proves the label set works before anything is rewritten.
3. **Apply §3** — strip prefixes, set `stage:`. Mechanical.
4. **Apply §4** — title rewrites. Each is a judgment about wording and should
   be read, not batched blind.
5. **Bring §5 to the maintainer** as one batch of four. `CLAUDE.md` caps parked
   questions at three at a time, so this is one over — split it or accept the
   overage deliberately.
6. **Leave the stock labels alone.** `bug`, `enhancement`, `documentation`,
   `question`, `duplicate`, `invalid`, `wontfix` are unused here and the
   actuator deliberately does not delete them. Removing them is its own act,
   after every issue carrying one has moved.

## 7. What this plan does not do

- **It does not touch a single issue.** No `gh issue edit` has run.
- **It does not authorise migration** in any other repository. The other eight
  repos have their own backlogs and their own maintainer judgment; only
  math-quest's is comparable in size and it is a `preview` candidate, not a
  steward.
- **It proposes no new label, type, or namespace.** Every value used here is in
  `kodhama-0026`'s closed vocabularies.
- **It does not delete anything.**
