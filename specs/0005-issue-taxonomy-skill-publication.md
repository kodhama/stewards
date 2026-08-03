---
id: kodhama-spec-0005-issue-taxonomy-skill-publication
type: spec
status: approved  # maintainer intent act 2026-07-31 ("approved", in session, answering a question that named this flip and the merge as separate acts) — the agent did not open the gate. Recorded at v9, the version the suite was then written against; the suite and `tests/TEST_DEPS.md` have since moved with the counter (v11 anchors the pin to this frontmatter); the flip is a lifecycle act and changes no testable clause, so it does not bump
depends_on: [kodhama-0026-issue-taxonomy, kodhama-0017-retire-family-release-certification, kodhama-0018-stewards-dual-host-plugin-package, kodhama-0020-name-overarching-plugin-kodhama, kodhama-0021-separate-adoption-posture-from-support, kodhama-0025-retire-the-surface-matrix, kodhama-spec-0004-ci-marketplace-setup-skill@v5]
implements: [kodhama-0026-issue-taxonomy]
owner: agent
updated: 2026-08-03
version: 11
---

# Publishing the issue-convention skill into the Kodhama plugin

> **AMENDED 2026-08-03 — v10 → v11**
>
> **WHAT:** Repairs from the `spec-adversary` pass in run
> `20260803-140655-retro-review`, which returned **NEEDS-REVISION** on v10.
> Three load-bearing items. **R18's arbiter could not fail**: v10 removed its
> literal from the clause and left the expected version as a literal in the
> test body, so the test asserted itself — setting `tests/TEST_DEPS.md` and
> that literal both to `@v3` left the suite green while R18 was violated,
> reproduced and confirmed. The arbiter now reads the expected version from
> **this file's own `version:` frontmatter**, and the same mutation goes red.
> **`§Package changes`' `TEST_DEPS.md` row** was rewritten by v10 from `@v9`
> to `@v10`; that row records what the publication act did, and the act
> pinned `@v9` — restored, matching how rows `0.2.0 → 0.3.0` were correctly
> left alone in the same table. **v10's own SCOPE was false**: it says *"R5
> and F are testable clauses, so this bumps; nothing else moves"*, and R18
> moved too, in a fixup that never reached the delta note. Corrected below
> rather than by editing v10's block, which is history.
>
> **WHY:** All three are the pattern v10 named and then repeated — *"a spec
> that recorded one act's particulars as a permanent property"*. The R18 one
> is worse than the defect it fixed: v9's stale anchor was at least visible
> to a reader, and v10 traded it for no anchor at all. This repository's own
> discipline is that **a guard you can revert without turning a test red is
> not a guard**.
>
> **SCOPE:** R18's arbiter changes, so this bumps. Also corrected, none
> testable: the frontmatter status note, the R5 arbiter row's missing pass
> condition, three rubric statements v10 falsified, and two line-number
> citations replaced by string anchors — v8 already ruled that class
> (*"Anchored by string, never by line number"*) and v10 reintroduced it.
>
> **POINTER:** run `20260803-140655-retro-review`; the artifact was merged
> before any adversary pass, which is what the run exists to correct.
>
> **CONFIDENCE:** The R18 repair is mutation-verified in both directions.
> The prose corrections are checked against the text they describe. What is
> **not** established: whether an `approved` spec's testable-clause
> amendment needs a fresh human intent act — the reviewer surfaced it and I
> do not hold that ruling.
>
> **VALUE:** R18 is now enforced by something a wrong value cannot satisfy.

> **AMENDED 2026-08-02 — v9 → v10**
>
> **WHAT:** Two clauses stopped being true of the thing they describe. **R5**
> pinned the literal SemVer `0.3.0` in a `(ubiquitous)` clause — a standing
> invariant — so the package could not be versioned again without violating
> this spec; it now requires one identical, valid SemVer string and pins no
> value. **Literal F** claimed the test gate runs on *"the issue-taxonomy
> staging tree under `conductor/`"*; the workflow's filter is
> `conductor/wave-issue-taxonomy/plugin/**`, the plugin subtree only. S3 and
> the R5 arbiter row follow R5; `CLAUDE.md` and the suite's
> `CLAUDE_MD_TEST_GATE_SENTENCE` follow F.
>
> **WHY:** R5 was found by trying to ship one — a content change to the
> `issues` skill wanted `0.4.0`, and the bump was reverted rather than
> violate an approved spec (#94). F was found by observing it: #82, #86 and
> #88 each touched that staging tree outside `plugin/` and **ran no suite**,
> while a sentence loaded into every session said they would (#91). Both are
> the same failure at different scales — **a spec that recorded one act's
> particulars as a permanent property.**
>
> **SCOPE:** No behaviour changes. R5 and F are testable clauses, so this
> bumps; nothing else moves. The gate's `paths:` filter is **not** touched —
> it protects exactly what the ruling intended, and only its description was
> wrong.
>
> **VALUE:** The package can be released again, and the sentence agents read
> every session describes the gate that actually runs.

> **AMENDED 2026-07-31 — v8 → v9**
>
> **WHAT:** **S17 and R19 are new**, and they close a real hole: the actuator's
> dry-run default was asserted in **six pinned literals and guarded by
> nothing**. The criterion is behavioural — the script runs against a stub `gh`
> and its call log is inspected — and carries the four measured mutations that
> survived the v8 suite. Three smaller items: the S5/R3 arbiter row now records
> the assertion that makes this spec's own sentence true, the `DIRECTION.md:55`
> false-positive citation is repointed at the path publication creates, and the
> wave ledger records the build.
>
> **WHY:** `APPLY=0` → `APPLY=1` in the shipped actuator — apply-by-default
> against a live org with `admin:org` — passed the full gate: **27 tests OK,
> validator green.** Three further mutations survive. The only test touching
> the property asserted `assertIn("Dry-run by default", stdout)`, which pins
> **the help text's claim, not the default**. The build is faithful to the
> spec; the spec was the gap. This repository's own recorded discipline is that
> a guard you can revert without turning a test red is not a guard.
>
> **SCOPE:** One new scenario and one new requirement — **the only things in
> v9 that change behaviour**. Everything else is one arbiter row, one citation,
> and a ledger entry.
>
> **POINTER:** `kodhama/stewards#64` — conformance **PASS**, code review one
> **HIGH**, both against the built implementation.
>
> **VALUE:** Someone who reverts the dry-run default finds out from CI instead
> of from an org that has been written to.
>
> **CONFIDENCE:** verified for the gap — the mutation and its green gate were
> reproduced before this revision. **Inferred for the fix**: the stub-`gh`
> technique and its credential-free read-only call set are the code reviewer's
> measurement, not mine, and S17 is written to be falsified by the four named
> mutations rather than trusted.

> **AMENDED 2026-07-31 — v7 → v8**
>
> **WHAT:** The false-positive table claimed to cover *"every non-carrier hit
> the widened command returns"*; it does not, and the claim is withdrawn rather
> than made true by padding the table. One row added for `specs/0004:141`,
> which two agents have now separately adjudicated. Literal **H** is re-anchored
> to a **string** at all four sites that named its line number.
>
> **WHY:** Two of the three are the wave's own recurring failure modes caught
> one last time in the document that describes them. The completeness claim is
> **false enumeration** — the class §Standing scope claims exists to kill —
> asserted, this time, about the instrument rather than the carriers, and in
> direct contradiction of this spec's own *"a clean run is evidence, not
> proof"*. Literal **H**'s line number is a **dependant thirty lines below its
> own edit in the same file**: literal **B** turns 9 lines into 26, moving H's
> target from line 22 to 39, so an executor keying on 22 ships a red test
> against a correct package.
>
> **SCOPE:** One disclosure restated, one table row, one anchoring change
> propagated to four sites. **No scenario, requirement, literal, arbiter or
> criterion moves** — H's replacement text is byte-identical; only how it is
> located changes.
>
> **POINTER:** `kodhama/stewards#64`; an implementation planner read v7 cold
> and returned *executable as written*, having re-derived S9 and S7 and
> confirmed all fourteen `new: test_*` map to arbiters with no gaps.
>
> **VALUE:** The executor locates the one-word edit by the text it is changing,
> and no reader mistakes a curated table for a complete one.
>
> **CONFIDENCE:** verified — `specs/0004:141-142` was read and the wrap
> confirmed (*"the plugin's declared skill / directories"*, already plural), and
> H's post-**B** displacement is arithmetic on literals pinned in this document:
> 22 − 9 + 26 = 39.

> **AMENDED 2026-07-31 — v6 → v7**
>
> **WHAT:** v6's two rulings — that `kodhama-0017` AC3 is a frozen record and
> that the debt is a **disclosure** gap rather than a conformance failure — were
> stated at the rule and at open question 6, and **not carried back** into the
> three older passages that still used the retired framing. Those are aligned.
> The new ground for dropping the marketplace-metadata item is now sourced to
> `decisions/0025:113` directly instead of through a derived restatement. Two
> citation corrections and one accounting fix.
>
> **WHY:** The distinction is consequential exactly where it is handed over:
> *conformance failure* implies an edit obligation on an append-only record —
> the loophole v6 closed — while *disclosure gap* implies an optional
> annotation, and open question 6 hands that call to the maintainer. Two
> framings pointing opposite ways is worse than either one alone.
>
> **SCOPE:** Three passages realigned to a ruling already made, one citation
> upgraded to its primary source, three corrections. **Nothing decided here that
> was not decided in v6**; no criterion, literal, arbiter or requirement moves.
>
> **POINTER:** `kodhama/stewards#64`, conformance round 8. Labels F1–F3 are the
> reviewer's, kept verbatim.
>
> **VALUE:** The maintainer answering open question 6 reads one framing of the
> debt, not two that imply different answers.
>
> **CONFIDENCE:** verified — `CLAUDE.md:44`, `decisions/0025:113`, and
> `conductor/wave-issue-taxonomy.md:99/:104/:105` were each read at the line
> cited before this revision was written, and all three findings reproduced.

> **AMENDED 2026-07-31 — v5 → v6**
>
> **WHAT:** The stated ground for dropping the marketplace-metadata item from
> the `distribution-scope` block was a **false claim about two approved
> decisions** — that `kodhama-0025` retired it. It did not: the goal survives
> and only its schema-shaped implementation retires, which this spec quotes
> elsewhere to prove the opposite. Restated on the ground that actually holds.
> The carrier/non-carrier status of `kodhama-0017` AC3 is now decided rather
> than used both ways. Open question 6 records the second falsification and the
> standing practice this parks against. Four rubric miscounts, one repudiated
> rule still asserted in present tense, and four minors.
>
> **WHY:** A spec that cites approved records as authority must read them
> correctly, and this one contradicted itself across two sections of its own
> text. The scope widening it justified is still right — the outcome never
> depended on the falsity claim, only on the framing.
>
> **SCOPE:** One rationale section, one rule clause, one open question, the
> rubric's edge accounting, and eight small corrections. **No change to what
> ships or where it lands** — no literal, criterion or requirement changes
> behaviour.
>
> **POINTER:** `kodhama/stewards#64`, conformance round 7. Labels B1, M1–M3 and
> m1–m4 are the reviewer's own and are kept verbatim in the change table.
>
> **VALUE:** A reader can follow every authority this spec cites back to a
> record that says what the spec says it says.
>
> **CONFIDENCE:** verified — `kodhama-0017:15-18`, `:119-121`, `:208`,
> `kodhama-0025:142` and `:151-153`, `kodhama-0002:33/:36/:41`, and
> `specs/README.md:34-36` were each read at the line cited before this
> revision was written.

> **AMENDED 2026-07-31 — v4 → v5**
>
> **WHAT:** S13 asserted that the **staged** `DIRECTION.md` carries literal
> **G**, while S10 and R12 require that same path to be gone — both evaluated
> after publication. Repointed at the published path, with the edit/verify
> split stated. `kodhama-0017` is now cited, declared in `depends_on`, and
> parked as open question 6: its AC3 is the clause literal **A** renders, it is
> accurate today, and **this publication is what makes it false**. The
> discovery command gained two paths and three alternatives, plus a disclosure
> that a regex cannot be complete against a semantically stated rule, plus a
> table of known false positives.
>
> **WHY:** The S13/S10 collision would have shipped a red test against a
> correct package — D1 one criterion over. And v4 justified the append-only
> exclusion on `kodhama-0018` §1, a record already inaccurate for other
> reasons, which made the exclusion look costless; the case it actually costs
> is `kodhama-0017`, which v4 never cited anywhere.
>
> **SCOPE:** One scenario, one requirement clause, one carrier-table cell, the
> discovery instrument, one new open question, one new declared dependency.
> **No change to what ships or where it lands.**
>
> **POINTER:** `kodhama/stewards#64` — conformance round 6 (the blocker) and
> the spec-adversary's round-5 gate, which returned **APPROVE-READY on v4**;
> its three errata are folded in here and recorded as errata, not findings.
>
> **VALUE:** The executor ships a package whose tests look for the moved file
> where it was moved to, and the corpus keeps a record of the one conformance
> debt publication creates rather than losing it to an exclusion.
>
> **CONFIDENCE:** verified — `kodhama-0017:33`, `:208` and `:228`,
> `kodhama-0025:142`, and `DIRECTION.md:55` were each read at the line cited,
> and the widened pattern was run against the widened paths.

> **AMENDED 2026-07-31 — v3 → v4**
>
> **WHAT:** Two arbiters were wrong about the world. S9's pinned head table
> said `gh token` where its own extractor produces `gh token lacks`, so the
> check would have gone **red on a correct package**. Literal **F** would have
> pinned *"a docs-only PR gets no check at all"*, which is **already false**:
> two of the three workflows carry no `paths:` filter and run on every PR. The
> generating rule in §Standing scope claims was scoped to "anywhere in this
> repository", which reaches ratified decisions that may not be edited; it is
> now scoped to statements of **present** state.
>
> **WHY:** F3 inverted — an arbiter that fails where it should pass is the same
> class of defect as one that passes where it should fail, and costs more,
> because it trains a reader to override the check. And literal **F** would
> have made this spec do the exact thing it twice condemns: pin a clause known
> to be false, converting a stale sentence into a defended one.
>
> **SCOPE:** One table cell, one pinned literal and the three places that
> follow it, the rule's reach, and four small arbiter corrections. **No change
> to what ships or where it lands.**
>
> **POINTER:** `kodhama/stewards#64`. The upstream `kodhama-0026` was corrected
> pre-merge in `fcb7779` — see §What the plugin is for.
>
> **VALUE:** The publishing PR goes green when it is right and red when it is
> wrong, and leaves behind no sentence about CI that the repository's own
> workflows contradict.
>
> **CONFIDENCE:** verified — D2's premise was re-checked here rather than
> taken on report: `agent-workflow-parity.yml` and `claude-code-review.yml`
> both declare a bare `pull_request:` trigger, and only
> `validate-marketplace-setup.yml` has `paths:`.

> **AMENDED 2026-07-31 — v2 → v3**
>
> **WHAT:** §Standing scope claims was itself an incomplete closed enumeration
> — the defect it exists to fix. It now names **eight** falsified statements
> across six files (was four), states the **rule** that generates the list
> and a command for finding the next one, and authorises a **second** edit to
> staged text (`DIRECTION.md`). Literal **A** asserted this repository
> distributes one plugin; both catalogs list four, so it is rewritten around
> what this repository *originates*. The staging phrase is scoped to the issue
> skill, since `kodhama-0020` fixed the CI skill's home. Literal **B** gains an
> actuator disclosure. S9's arbiter was a denylist wearing an allowlist's name
> and let four injected mutating commands through; it is now a closed
> `gh`-surface multiset. S10 no longer asserts a state Lane A will delete, and
> S15 no longer needs a YAML parser the repository does not have.
>
> **WHY:** `spec-adversary` returned NEEDS-REVISION and `conformance-reviewer`
> FAIL against v2, both concentrated in the v2 repair rather than the contract.
> The through-line: **a pinned enumeration that is wrong is worse than a loose
> sentence that is wrong**, because pinning freezes it into three files and a
> parity test and converts a stale claim into a defended one.
>
> **SCOPE:** The falsified-statement set, the pinned literals, three acceptance
> criteria whose arbiters could not establish their property, and the ledger
> entry recording the two rulings. **No change to what ships or where it
> lands.**
>
> **POINTER:** `kodhama/stewards#64`; the two rulings are now recorded in
> `conductor/wave-issue-taxonomy.md` Lane B.
>
> **VALUE:** A consumer who installs this package is told what is in it —
> including that it contains an actuator — and no statement left standing in
> the repository or the package contradicts what shipped.
>
> **CONFIDENCE:** verified for the carriers — every newly named one was read at
> the line cited. **Partial for S9:** all nine `gh` occurrences were read and
> classified by hand, but the extractor itself was not run, which is how the
> `gh token lacks` head reached v3 uncaught. v4 fixes it.

> **AMENDED 2026-07-31 — v1 → v2**
>
> **WHAT:** Two maintainer rulings landed as new obligations — amending the
> standing statements that the plugin's scope is narrow (S13, R15), and
> closing the CI blind spot v1 merely disclosed (S15, R17). Three checks that
> could not do their job were repaired: S7's extraction rule was
> mutation-proven blind to `../../../DIRECTION.md`, S9 asserted six conditions
> of which three fail against the file they govern, and **S1's coverage was a
> strict subset of R1**. The replacement literals for every human-readable
> field are pinned in the spec rather than described. Open question 2 is
> answered by a recorded host run and closed.
>
> **WHY:** Independent review returned `conformance-reviewer` **FAIL** (three
> blockers) and `spec-adversary` **NEEDS-REVISION** (F1–F6) against v1. A spec
> whose acceptance criteria pass while the property they name is false is worse
> than one with no criterion, because it converts a missing check into a
> claimed one.
>
> **SCOPE:** Acceptance criteria, pinned literals, two new obligations, and
> factual corrections. **No change to what ships or where it lands.**
>
> **POINTER:** `kodhama/stewards#64` carries both review records in full.
>
> **VALUE:** An executor building from this spec produces a package whose
> layout guards actually fail when the layout is wrong.
>
> **CONFIDENCE:** verified.

## Scope

This specification defines **one delivery act**: moving the issue-convention
artifacts staged at `conductor/wave-issue-taxonomy/plugin/` into the existing
Kodhama plugin at `plugins/kodhama/`, so that a repository which has already
chosen to install that plugin receives the skill.

The taxonomy itself is out of scope. `kodhama-0026-issue-taxonomy` is approved
and its twelve Decision clauses settle the vocabularies, their membership, and
the reasoning. **This spec never restates a vocabulary and never adds one** —
with one deliberate exception, admitted rather than hidden: **S8 and R9 name
all six issue types.** A literal check that the shipped in-force gate survived
publication cannot be written without the strings it must find. Those six names
are quoted from `kodhama-0026` D2 **as check inputs**, and this spec owns
neither their membership nor their meaning.

Where this spec and that record appear to disagree about the convention, the
record wins; where they appear to disagree about *where a file goes*, this spec
wins, because the record deliberately owns no delivery criterion — *"Nothing
about delivery is a criterion here"* (`kodhama-0026` §Done when).

Three boundaries are inherited, not chosen here, and none of them is this
spec's to relax:

| Boundary | Source | Consequence for this spec |
|---|---|---|
| The convention is carried by GitHub's issue types and labels; **the skill teaches it** | `kodhama-0026` D9 | The skill is never specified as the carrier. A repository with the types and labels but without this plugin still has the convention. |
| Until `Research`, `Decision` and `Epic` exist **and are enabled**, the convention is not in force | `kodhama-0026` D12 | Shipping this payload changes no repository's behaviour. The skill's own first instruction is to stop. |
| Adoption is each repository's own act | `kodhama-0026` D11, `kodhama-0021` | This spec covers **publication only**. It enables nothing, anywhere. |

## What the `kodhama` plugin is for stays undecided

`conductor/wave-issue-taxonomy/plugin/DIRECTION.md` records the plugin home as
a **staging area** and states plainly that *"what the `kodhama` plugin is for
remains undecided"* and *"Nothing about this sequence claims the `kodhama`
plugin's scope."*

This spec therefore describes the package **by enumeration, never by purpose**.
Minting one — "how the family operates on GitHub", or any equivalent — would
answer, in a manifest string, a question DIRECTION.md records as open. R8
forbids it, and §Pinned replacement literals fixes the exact wording so the
judgment is made once, by a human at review time, rather than re-made by every
later editor.

**The upstream was corrected pre-merge, which is why the spec and the record
agree** *(noted in v4)*. Until `fcb7779`, `kodhama-0026` open question 1 still
described the plugin as one *"whose identity is the family's GitHub
operations"*, and three lines below called its scope *"deliberately narrow (CI
marketplace setup)"* — the first being a claim the maintainer had already
rejected in `06f7f1d`, which reached `DIRECTION.md` and the wave brief but
never the record itself. Conformance review caught it, the maintainer directed
a pre-merge correction, and both clauses were repaired with the authority
recorded in the record's own status line. A later reader finding this spec and
that record in agreement should know the agreement was made, not inherited.
**It was correctable only because the PR carrying its status flip had not
merged** — see the scoping note in §Standing scope claims.

**Two precisions v3 adds, because v2's wording overreached in both
directions.** First, *"staged while their home is decided"* is true of the
issue skill and **false of `setup-ci-marketplace`**, whose package directory
and namespace approved `kodhama-0020` fixed; every literal below scopes the
phrase to the issue skill alone. Second, "this package asserts no purpose of
its own" is stronger than the corpus supports — `kodhama-0020` does name it
*the overarching dual-host plugin*. The accurate statement is narrower and is
what literal **B** carries: that plugin exists and is named, and **what it is
*for* has never been decided.**

## What ships, and where

Four files move out of staging. The destination of each is fixed by something
already written, not by preference:

| Staged source (under `conductor/wave-issue-taxonomy/plugin/`) | Destination | Why exactly there |
|---|---|---|
| `skills/issues/SKILL.md` | `plugins/kodhama/skills/issues/SKILL.md` | Host skill discovery reads `<plugin>/skills/<name>/SKILL.md`; the Codex manifest already declares `"skills": "./skills/"`. The directory name must equal the skill's `name: issues`. |
| `skills/issues/reference/taxonomy.md` | `plugins/kodhama/skills/issues/reference/taxonomy.md` | `SKILL.md` closes with a pointer to `` `reference/taxonomy.md` ``, resolved from the skill directory. Progressive disclosure: `SKILL.md` loads on trigger, the reference on demand. |
| `scripts/seed-issue-taxonomy.sh` | `plugins/kodhama/scripts/seed-issue-taxonomy.sh` | **Outside `skills/` deliberately** — see below. |
| `DIRECTION.md` | `plugins/kodhama/DIRECTION.md` | `reference/taxonomy.md` §6.5 points at `` `../../../DIRECTION.md` ``, which from `skills/issues/reference/` resolves to the plugin root and nowhere else. |

### Why the actuator sits outside `skills/`

`scripts/seed-issue-taxonomy.sh` creates org issue types and repository labels.
It is an **actuator**; the skill is **instruction**. Everything under
`skills/` is agent-reachable context by construction, and the staging record
states the cost of merging them: *"bundling an actuator into reference content
is what forced guardrails into the first draft"*
(`conductor/wave-issue-taxonomy/README.md`).

The separation is load-bearing rather than tidy, so it gets a guard: R3 requires
that no `SKILL.md` or skill reference under `plugins/kodhama/skills/` name the
script at all. An agent that reads the skill learns the convention and cannot
learn, from the skill, that a provisioning command exists. Provisioning is Lane
E of `conductor/wave-issue-taxonomy.md`, run by a person holding `admin:org`.

**A later reader who moves the script under `skills/` to "keep the skill
together" reverses this.** S5 and R3 fail if they do.

**A consumer, however, must be told the package contains one.** Hiding the
actuator from the *skill* is a context-safety measure; hiding it from the
*human who installed the package* is not. Literal **B** discloses it in the
shipped README, which sits outside `skills/` and therefore outside the concern
R3 protects. v2 shipped an actuator that no consumer-facing text mentioned:
`specs/README.md`'s index row named it, and nothing inside the package did.

## What does not ship

`migration/legacy-mapping.md` is **not published in the plugin.** Its final home
is recorded in the staging table as *"rides the ratified decision, not the
plugin"*, and the decision relocates to `kodhama/kodhama` under Lane A. Until
that lane resolves, the mapping stays at
`conductor/wave-issue-taxonomy/plugin/migration/legacy-mapping.md`.

Two independent reasons, both already written down:

1. **It is not standing agent context.** Its own header: *"a mapping table plus
   occurrence counts reads as a backlog-sweep plan, and no agent should be
   handed one as ambient context."*
2. **It authorises nothing.** `kodhama-0026` open question 5 leaves migration
   unauthorised, and the wave brief puts it under Boundaries as explicitly out
   of scope. A file that ships with an installable plugin reads as available to
   act on; this one is not.

**A later reader who "reunites" the mapping with the skill it explains reverses
both.** S6 fails if they do.

### The two authorised edits to staged text, quoted

Publication carries the staged files over byte-for-byte **except at these two
places.** Every other byte is unchanged: the taxonomy content is settled and
reviewed, and re-editing it here would put a further reviewed state into a wave
whose recurring failure mode was repairs made without re-walking what depended
on them.

**Edit 1 — the seed script's dangling pointer.** Line 158 of
`conductor/wave-issue-taxonomy/plugin/scripts/seed-issue-taxonomy.sh`, inside
`seed_labels()`, in the `if [[ ${#found[@]} -gt 0 ]]` branch. It prints a
plugin-root-relative path that will not resolve once the script ships and the
mapping does not.

**Before** (verbatim, including leading whitespace):

```bash
    echo "    migrate the issues carrying them first (see migration/legacy-mapping.md),"
```

**After** (verbatim, one line for one line):

```bash
    echo "    migrate the issues carrying them first (see the legacy-issue mapping that rides kodhama-0026),"
```

The replacement names the mapping instead of pointing at it, so it survives the
Lane A relocation. It prints wider than its two neighbours; that is accepted
deliberately, because a one-for-one line replacement is easier to review than a
re-flowed block. The preceding line (`─ now redundant, NOT deleted: …`) and the
following line (`then remove by hand once each is at zero uses.`) are unchanged.

**Edit 2 — `DIRECTION.md` lines 45–47, which ship to consumers.** Literal
**G** below. v2 quoted the sentence immediately before this one and left this
one standing, which would have produced a package whose `DIRECTION.md` asserts
a narrow declared scope while its `README.md` enumerates a wider contents.
**The conflict is resolved by editing, not by explaining:** a shipped document
contradicting its shipped sibling is not a defensible state, and the
maintainer's ruling authorises the class. The clause worth keeping — *a staged
skill sitting in it is a deferral, not an amendment* — is kept; the clause
publication falsifies is removed.

## Standing scope claims this publication falsifies

Publishing a second skill and widening the CI filter makes **eight statements
across six files** false. v2 named four. That miss is the same defect this
section exists to repair — **a closed enumeration whose own enumeration is
incomplete** — so v3 states the generating rule first and the list second.

**The rule.** A statement is a carrier of this obligation when **both** hold:

1. it enumerates what the install door distributes or originates, what the
   `kodhama` package contains, or which paths CI gates; **and**
2. it describes **present state** — repository documentation, ledgers, or text
   shipped inside the package — rather than recording a past act.

Any such sentence is in scope whether or not it appears below.

**Is `kodhama-0017` AC3 a carrier? No — and v6 picks that side explicitly**,
because v5 used the past-act reading to justify the exclusion and the
present-state reading to assert the debt, which cannot both be had. An
acceptance criterion **records a past act**: it states what had to be true for
a decision to be ratified, and it is frozen at ratification. AC3 therefore
fails condition 2 and is **not** a carrier, so no edit is owed against it and
the append-only exclusion is not a loophole.

**The debt is real anyway, and it is a different kind of debt.** What
publication creates is not a conformance failure — a frozen record and a
current document are each correct as the kind of artifact they are — but a
**disclosure** gap: a reader arriving at `kodhama-0017` today has no way to
learn that its AC3 no longer describes this repository. The corpus's remedy for
exactly that is the forward pointer, which is an annotation rather than an edit
and so does not touch append-only at all. Open question 6 carries it.

**Ratified decisions are out of scope, and that is not an oversight**
*(scoped in v4)*. A decision under `decisions/` is append-only: it records what
was decided when it was decided, and the corpus corrects it by **forward
pointer or supersession, never by amendment**. v3's rule said *"anywhere in
this repository"*, which swept those records in and made R15 a `shall` no
executor could discharge — S13's closing clause passed only because the
discovery command never searched `decisions/`. A rule whose satisfaction
depends on where you happen not to look is not a rule.

**The record the exclusion actually costs is `kodhama-0017`, not
`kodhama-0018`** *(v5)*. v4 justified the exclusion on `kodhama-0018` §1, which
enumerates the package's contents and is **already** inaccurate for reasons
predating this work — so nothing is lost by excluding it, and the example was
chosen badly because it made the exclusion look free. It is not free:

> `decisions/0017-retire-family-release-certification.md:33` — *"Stewards
> retains **only** a narrow future distribution goal:"*, followed by two
> sub-items.
>
> `:208` **AC3** — *"Current repository scope **describes only** host-native
> catalogs, the future marketplace-tested metadata, and the future generic CI
> setup skill."*

**The `distribution-scope` block literal A rewrites is that clause's
rendering.** Unlike `kodhama-0018` §1, AC3 describes this repository accurately
as of its ratification, and **this publication is what makes it diverge — in
both directions** *(v7: this passage stated only the addition, 25 lines below
the ruling that named both)*:

- **added** — a third distributed thing in the issue skill, and a fourth in the
  actuator; and
- **removed** — the marketplace-metadata description AC3 names, which leaves
  literal **A** because `kodhama-0025` §4 redirected that goal to the GitHub
  Actions run log, and a run log is not something the door distributes.

`kodhama-0025` does not retire the enumeration: `decisions/0025:142` says
*"`kodhama-0017` §2 — amended, not superseded. Its retained goal survives"*.

So publication leaves this repository's canonical scope document describing
different contents from the ones AC3 records. **That is a disclosure gap, not a
conformance failure** — AC3 is a frozen record and the scope document is a
statement of present state, so each is correct as the kind of artifact it is,
and neither is owed an edit *(v7: this passage said "out of conformance with an
approved decision", the framing the rule above retired)*. What is missing is a
pointer at the record. **The exclusion removes the class from the edit
obligation and v4 put nothing in its place**; open question 6 names the corpus's
own remedy — the forward pointer, which `kodhama-0017` already carries two of.

**The one adjacent case, and why it is different.** `kodhama-0026` carried the
same shape of stale clause and *was* corrected, in `fcb7779`. That was possible
because **the PR carrying its status flip — stewards#64 — had not merged**.

*Stated carefully, because v4 stated it three ways and only two were right.*
The boundary is **the merge that delivers the record**, not the intent act and
not the file's eventual location. `kodhama-0026` already carried
`status: approved` when `fcb7779` corrected it, so the intent act cannot be the
line; and `kodhama-0008`'s own status line puts it at the merge — *"the #35
merge performs the delivery"* — as does `fcb7779`'s commit message, *"#64 has
not merged, so delivery has not happened"*. v4 said *"had not yet merged into
`kodhama/kodhama`"*, which would have left `kodhama-0026` editable after #64
merges and until Lane A relocates it; and it said *"the distinction is the
intent act"*, which is contradicted by the correction it was explaining. **Once
#64 merges, `kodhama-0026` is append-only like any other delivered record.**

*A supporting datum and an unreconciled one, both v6.* Supporting:
`decisions/0002:36` — *"per the append-only rule its text below is preserved
**as merged**"* — the corpus stating the boundary in its own words. Cutting the
other way: **`CLAUDE.md:44` says *"never edit a **ratified** decision"***, which
on a literal reading would have forbidden `fcb7779`. The reconciliation is that
`CLAUDE.md` uses "ratified" loosely, as shorthand for a decision that has
landed; the operative event in every worked instance is the merge.

That looseness is noted rather than fixed. Line 44 fails carrier condition 1 —
it enumerates nothing — so R15 does not reach it. **But this publication edits
`CLAUDE.md` twice**, so declining to tighten a third sentence in the same file
is a **scope choice, not a limit**: those two edits are obligations the rule
generates, while rewriting a governance rule about append-only editing is a
different act needing its own authority. *(v7: this cited line 42, the bullet
head; the sentence is at line 44. v6's CONFIDENCE line did not list `CLAUDE.md`
among what was re-read, so the slip fell exactly outside the verified set —
which is the case for keeping that list honest rather than generous.)*

**Finding the next one** (reviewer-runnable, and **a heuristic that cannot be
complete** — see the disclosure below):

```
rg -n 'nothing else|stays narrow|narrow scope|distribution scope|declared skill\b|retains only|describes only|retained goal' \
   CLAUDE.md README.md distribution/ plugins/kodhama/ specs/ decisions/ \
   conductor/wave-issue-taxonomy.md conductor/wave-issue-taxonomy/plugin/
```

**The instrument is weaker than the rule, and v4 hid that** *(v5)*. The rule is
stated **semantically** — *does this sentence enumerate?* — while the command is
a fixed alternation over a fixed path list. v4's version returned **zero** hits
on `kodhama-0017`, whose clauses read *"retains only"*, *"describes only"* and
*"Its other retained goal"*: none of the five alternatives could match the
hardest carrier in the corpus. **That is the v3 defect one level up — the
discovery instrument had become the incomplete enumeration.** v5 adds three
alternatives and two paths, which closes the case that was found; it does not
make the command complete, and no regex over a semantic rule can be.

**Two consequences a reviewer must hold.** First, a clean run is **evidence,
not proof** — the reviewer's read is the arbiter and the command is only a way
to spend it well. Second, hits under `decisions/` are **not edit obligations**:
that class is excluded by the rule above. They are **forward-pointer
candidates**, which is a different disposition and the corpus's own remedy.

**Known false positives, recorded so the next reviewer does not re-adjudicate
them:**

| Hit | Why it is not a carrier |
|---|---|
| `plugins/kodhama/DIRECTION.md`, §The split that is coming | *"This skill then becomes **thin**: the mapping from concept to surface, and nothing else."* Describes a **future** shape of the issue skill under a hypothesised abstract/concrete split — not what the package contains today. *(v9: cited as `conductor/wave-issue-taxonomy/plugin/DIRECTION.md:55`, **a path R12 deletes**. Same displacement class as literal **H**: the file moves in the change that names it.)* |
| `decisions/0018-stewards-dual-host-plugin-package.md:130` | *"`plugins/stewards/surfaces.json` describes only the Stewards plugin's own host…"* — an enumeration about an artifact `kodhama-0025` retired. Under `decisions/` and therefore excluded regardless. |
| `decisions/0017…:228` | *"draws a positive boundary around the only retained goals"* — the record's own self-check describing its reasoning, not the repository's contents. |
| `decisions/0017:16` | The forward pointer `kodhama-0025` wrote. It is the corpus **doing** the disclosure this rule cares about, so a hit here is a worked example, not a defect. |
| `CLAUDE.md:8` and `README.md:5` | *"THREE things live here and nothing else"* — enumerates the repository's **top-level structure** (decisions, conductor, install door), which this publication does not change. |
| `specs/0004:86` | *"carries exactly these host-specific fields, plus a `description` and nothing else"* — a JSON schema constraint on a catalog entry, unrelated to package contents. Still true. |
| `specs/0004:141` | *"the host's component inventory matches the plugin's declared skill"* — reads like carrier 5's singular, and is not: **the line wraps**, and the full phrase at `:141-142` is *"the plugin's declared skill **directories**"*, already plural. The regex matches `declared skill\b` across the break. **Round 5's spec-adversary adjudicated this exact line for this exact reason, and an implementation planner adjudicated it again on v7** — twice, by two agents, because it was not in the table. It earns its row on that alone. |
| `conductor/wave-issue-taxonomy.md:99`, `:104`, `:105` | **Lane B ruling text quoting the carriers themselves** — `:99` quotes carrier 4, `:104` carrier 8, `:105` carrier 5. They are the authorisation naming what to repair, so a hit is the ledger working, not a carrier. *(v7: v6 called these "Lane C/D scope text about which repositories receive receipts", which is wrong twice — Lane C begins at `:121` and returns no hits, and that reason would not have excluded them anyway, since carrier 7 proves Lane B text **can** be a carrier.)* |

**What this table is, and is not** *(restated v8)*. It holds **the hits a
reviewer would otherwise re-adjudicate** — non-carriers whose disposition is
not obvious from the line itself. **It is not an enumeration of the command's
output, and v7's claim that it covered "every non-carrier hit the widened
command returns" was false.** The command returns roughly two dozen hits
outside this spec; eight remain untabled, and two of those — `decisions/0017:33`
and `:208` — are the most consequential hits it produces, adjudicated at length
in §Why the marketplace-metadata item leaves the block and open question 6
rather than in a table row.

**The command also hits this spec, and the records this spec quotes** —
`decisions/0017:33`, `:208`, `decisions/0025:142`, `specs/README.md:34`, `:40`,
`:41`. That is **self-reference by construction**: a document that discusses
scope enumerations contains the phrases that find scope enumerations, and so
does the index entry describing it. Those hits carry no disposition because
there is nothing to dispose of.

*That correction matters more than its size.* This spec says one level up that
**a clean run is evidence, not proof**; claiming a complete enumeration of the
instrument's own output contradicted exactly that, and it is the same false-
completeness class the §Standing scope claims rule exists to eliminate — this
time in the artifact describing the instrument rather than in the carrier list.

| # | Where | The false part | Replacement |
|---|---|---|---|
| 1 | `distribution/repository-scope.md` — canonical | *"Its future distribution scope is deliberately narrow: metadata that records which marketplace a test exercised, and a generic Stewards skill that adds caller-selected Claude/Codex marketplace setup to CI."* A two-item enumeration; the package carries a third thing. | **A** |
| 2 | `CLAUDE.md` lines 14–22 | Hand-mirrored copy of the same block. | **A** |
| 3 | `README.md` lines 7–15 | The second hand-mirrored copy. | **A** |
| 4 | `plugins/kodhama/README.md` lines 1–9 | *"It edits workflow configuration and nothing else."* **Ships to consumers**, so the package tells its installer it does not contain the skill they just received. | **B** |
| 5 | `plugins/kodhama/README.md`, the `declared skill` sentence — line 22 before literal **B** applies, **line 39 after**; match it by string | *"reports the declared skill in its component inventory"* — **singular**, and the package now declares two. **Ships to consumers.** Already out of step with `scripts/keyless_admission_check.py` line 27, which says *"skill directories"*. | **H** |
| 6 | `conductor/wave-issue-taxonomy/plugin/DIRECTION.md` lines 45–47 — **edited here, verified at `plugins/kodhama/DIRECTION.md`**, since publication moves the file (R12) | *"Its declared distribution scope stays narrow until someone decides otherwise."* **Ships to consumers.** | **G** |
| 7 | `conductor/wave-issue-taxonomy.md` Lane B | *"Its declared narrow scope is untouched."* The wave's own ledger asserting the opposite of the ruling that governs the wave. | corrected in the ledger commit that records the rulings — see below |
| 8 | `CLAUDE.md` lines 66–68 | *"CI enforces them on any PR touching `tests/`, `scripts/`, `plugins/`, or either marketplace catalog, **and on nothing else**, so a docs-only PR gets no check at all."* R17 falsifies the path list — and the trailing clause is **already false**, independently of this publication: two of three workflows have no `paths:` filter. | **F** |

**Carrier 7 is already corrected**, in the same commit that records the two
maintainer rulings in `conductor/wave-issue-taxonomy.md` Lane B. It is listed
here for completeness of the enumeration, not as an outstanding obligation:
the falsehood is the ledger's own bookkeeping, and a ledger that states a
ruling and contradicts it two lines earlier is the defect this wave has been
correcting everywhere else.

**Carrier 8 is quoted by this spec as a rationale and amended by it.**
§Closing the CI blind spot leaned on *"a docs-only PR gets no check at all"* to
justify keeping the filter narrow. **v4 finding: that clause is false, and was
false before this publication** — `agent-workflow-parity.yml` and
`claude-code-review.yml` declare a bare `pull_request:` trigger with no
`paths:` key, so both run on every PR, and PR #61 (one `conductor/` file
changed) ran two checks. Only `validate-marketplace-setup.yml` is filtered.

The ruling is unaffected: what it protects is that the **test gate** — suite,
validator, two `npm install`s, admission check — does not run on a prose edit.
Literal **F** states that narrower property and adds the sentence naming the
two unfiltered workflows. Using a sentence as authority while leaving it false
would be the same error in a different place, and **pinning it into three
files would have been that error made permanent** — which is the argument this
spec already makes about the `kodhama-0025` clause, applying unchanged here.

### Why the marketplace-metadata item leaves the block

*Restated in v6. The v5 ground was a false claim about two approved
decisions.* It said *"metadata that records which marketplace a test
exercised"* named an artifact `kodhama-0025` retired, and that the clause was
therefore **already false before this publication**. **The corpus says the
opposite, four ways:**

- `decisions/0017:15-18`, the forward pointer `kodhama-0025` itself wrote:
  *"the retained goal of recording which marketplace a test exercised
  **survives**, but its schema-shaped implementation retires."*
- `decisions/0025:142`: *"**`kodhama-0017` §2 — amended, not superseded.** Its
  retained goal survives; only the schema-shaped implementation of it goes."*
  **This spec quotes that exact line elsewhere to prove the opposite
  proposition.**
- `decisions/0017:119-121`: §2 *"authorizes the goal, not a schema."* It never
  named an artifact, so nothing could be retired out of it.
- **`decisions/0025:113` — the approved record saying where the goal went**:
  *"That goal is met by the GitHub Actions run log, which records the checkout
  revision with better provenance than a checked-in file."* This is the primary
  source for the replacement ground below; *(v7: v6 routed the claim through
  `specs/README.md`, a derived restatement, when the decision itself says it)*.
- `specs/README.md:34-36` — this repository's own spec index, standing directly
  above the paragraph v5 added to it, agreeing: the goal *"is met by the GitHub
  Actions run log rather than a schema, per `kodhama-0025`."*

The claim was also self-contradicting: of the same two-item enumeration, this
spec said AC3 *"is accurate today"* in one section and *"was already false"* in
another. Both cannot hold, whichever reading a reader prefers.

**The correct ground reaches the same outcome and asserts no falsity.**
`kodhama-0025` §4 **redirected** the goal — from a distributed schema to the
GitHub Actions run log (`decisions/0025:113`). Literal **A** reframes the block as *a description of
present distributed contents*. A run log is not a distributed artifact: the
install door does not ship it, and nobody installs it. So the item leaves the
block because **it is no longer a description of anything the door
distributes**, not because it is false. The goal survives exactly as
`kodhama-0017` and `kodhama-0025` say it does; what changed is that it is no
longer met by something this block is about.

**That removal is itself a second falsification of AC3**, and open question 6
records it: literal **A** does not merely add a third and fourth distributed
thing, it also drops the retained-goal description that AC3 names. Both
directions of the divergence are the parked debt.

Three reasons the removal belongs in this change rather than a follow-up:

1. **This change rewrites and pins the block.** A clause left in becomes a
   *defended* falsehood — carried into literal **A**, mirrored to three files,
   and guarded by S14's parity test. Leaving it is not neutral.
2. **It needs no new judgment.** `kodhama-0025` is approved and its redirection
   of the goal to the run log is already recorded in this repository's spec
   index; nothing is being decided here.
3. **Splitting costs more than it saves.** Two PRs would touch the same mirrored
   block, and the second would re-pin a literal already known to be changing.

Disclosed as a deliberate widening, not smuggled in.

### Pinned replacement literals

Pinning is not mechanisation. R8 — *no field shall imply a purpose* — stays
reviewer judgment; what pinning changes is **when** that judgment happens: once,
by a human reading these strings at the spec gate, after which drift is
mechanically detectable. This is the discipline
`test_kodhama_catalog_entries_disclose_no_support_claim` already applies to the
catalog disclosure.

**A. The `distribution-scope` block** — byte-identical in all three carriers,
markers included:

```markdown
<!-- distribution-scope:begin -->
The install door includes the host-native Claude and Codex catalogs. Those
catalogs list plugins this repository does not originate — each of those is
sourced from the repository that owns it. The only plugin **originated here**
is `kodhama`, which carries two skills and one provisioning script: verified
Claude/Codex marketplace setup for CI, the kodhama issue convention (staged
here while the issue skill's home is decided), and a dry-run-by-default
label-and-type seeder. That is a description of present contents, not a scope:
it moves when the contents move. The install door does not certify product
releases or support and owns no universal version, tag, release-history,
approval, runtime-sandbox, cross-repository-resolution, or effective-support
machinery.
<!-- distribution-scope:end -->
```

*What v2 got wrong here:* it said *"What it distributes today is the `kodhama`
plugin"*. Both catalogs list **four** — `grove`, `kodhama`, `trellis`, `wisp` —
so that replaced a false scope claim with a false contents claim. The accurate
relation is **origination**: three entries are `git-subdir` sources pointing at
the repositories that own them, and only `kodhama` is local to this one. The
replacement deliberately does **not** enumerate the other three, because a fresh
closed list of catalog membership would go stale exactly the way the sentence it
replaces did.

**B. `plugins/kodhama/README.md`** — replaces its lines 1–9. Everything from
`## Where this works, and what that claim rests on` onward is **unchanged**,
which keeps the five literals the existing README test pins:

```markdown
# Kodhama

This package carries two skills and one script.

- **`skills/setup-ci-marketplace`** — adds verified Claude Code or Codex
  marketplace setup to repository-owned GitHub Actions workflows. You point it
  at the jobs that invoke a host CLI; it writes the exact, host-native
  marketplace registration those jobs need, before they run. *That skill* edits
  workflow configuration and nothing else: it is not installed into the
  resulting CI job, and it provides no shared action, runtime, container, or
  installer.
- **`skills/issues`** — teaches the kodhama issue convention: titles are prose,
  and every machine-readable dimension lives in GitHub's native issue types and
  labels. **It only teaches.** The convention is carried by GitHub itself, not
  by this package, and until an org's issue types exist and are enabled it is
  not in force — the skill's first instruction is then to stop. This skill is
  staged here while its home is decided; see `DIRECTION.md`.
- **`scripts/seed-issue-taxonomy.sh`** — **an actuator, not a skill.** It
  creates org issue types and repository labels, which is why it sits outside
  `skills/` and why no skill points at it. It is dry-run by default, deletes
  nothing, and changes nothing without `--apply`. Running it needs `admin:org`.

**What this plugin is *for* has never been decided.** `kodhama-0020` named it
the family's overarching dual-host plugin; what that plugin is for is a
separate question nobody has answered, and `DIRECTION.md` records it. The list
above is the package's present contents, not a statement of purpose.
```

Two repairs to v2's wording are visible here. *"edits workflow configuration and
nothing else"* is **re-scoped to the skill it is true of** rather than deleted —
it was never wrong about `setup-ci-marketplace`, only about the package. And
*"It teaches and carries nothing"* became *"It only teaches"* plus a separate
sentence, because the v2 form parses as "teaches nothing".

**C. Both host manifest `description` fields** — identical string:

```
Two skills: verified Claude and Codex marketplace setup in repository-owned GitHub Actions workflows, and the kodhama issue convention, staged here while its home is decided.
```

**D. Both catalog entries' `description`** — identical string, retaining the
`kodhama-0021` §2 disclosure:

```
Dogfood — verified Claude and Codex marketplace setup in repository-owned GitHub Actions workflows, plus the kodhama issue convention, staged here while its home is decided; support is not claimed.
```

**E. `plugins/kodhama/.codex-plugin/plugin.json` `interface`** — the four
fields that describe contents:

```json
"shortDescription": "Two skills: CI marketplace setup, and the issue convention.",
"longDescription": "Carries two skills. One authors immutable, host-native marketplace setup for direct Claude Code and Codex CLI invocations in repository-owned GitHub Actions jobs. The other teaches the kodhama issue convention — prose titles, with every machine-readable dimension in GitHub's native issue types and labels — and is staged here while its home is decided.",
"capabilities": [
  "GitHub issue convention (skills/issues)",
  "GitHub Actions workflow authoring (skills/setup-ci-marketplace)"
],
"defaultPrompt": "Use the kodhama skill that fits: CI marketplace setup, or the issue convention."
```

**What "enumerate both skills" means for an array** (`capabilities` is the only
array among these fields), stated as a rule because a rule is checkable where a
prose instruction is not:

> `interface.capabilities` shall contain **exactly one element per directory
> under `plugins/kodhama/skills/`**, in the order those directory names sort,
> and each element shall contain the string `skills/<directory-name>`.

That makes the array's length, ordering, and membership derivable from the
package, so R16's check compares it against the filesystem rather than against a
remembered list. `defaultPrompt` keeps its key and becomes enumerative: a single
default prompt naming one skill would elect that skill the package's purpose,
which R8 forbids.

**F. `CLAUDE.md`, the CI-gate sentence** — anchored by string, not line number, per v8's ruling on literal H; replacing from `done; CI
enforces` to `no check at all.`:

```markdown
done; the **test gate** runs on any PR touching `tests/`, the two plugin
scripts under `scripts/`, `plugins/kodhama/`, the plugin subtree of the
issue-taxonomy staging tree (`conductor/wave-issue-taxonomy/plugin/`), either
marketplace catalog, or the validation workflow itself — and on nothing else,
so a docs-only PR pays none of its cost. It is not the only check: the Claude
review and the workflow-parity job carry no `paths:` filter and run on every
PR.
```

**v4 correction, and it matters more than the path list.** v3's replacement
preserved the clause *"an ordinary docs-only PR still gets no check at all"* on
the grounds that it is the property the narrow-filter ruling protects. **That
clause is already false, and was false before this publication.** Measured:
`agent-workflow-parity.yml` and `claude-code-review.yml` both declare a bare
`pull_request:` trigger with no `paths:` key, so both run on every PR;
`validate-marketplace-setup.yml` is the only filtered workflow. PR #61 changed
exactly one file, under `conductor/`, and ran two checks.

Pinning it would have made this spec do precisely what it condemns twice —
*"a clause left in becomes a defended falsehood"*, and carrier 8's *"using a
sentence as authority while leaving it false would be the same error in a
different place."* **The ruling survives untouched; only the wording was
wrong.** The true property is narrower and still holds: the **test gate** — the
unittest suite, the validator, the `npm install` of two CLIs, and the keyless
admission check — does not run on a docs-only PR. That is the expensive thing
the narrow filter protects, and it is what the ruling was about.

The replacement is also more accurate than the original in a second way, which
v3 did get right: it said `scripts/` and `plugins/` where the filter has always
named two specific scripts and one plugin directory.

**G. `conductor/wave-issue-taxonomy/plugin/DIRECTION.md` lines 45–47:**

```markdown
**Nothing about this sequence claims the `kodhama` plugin's scope.** A staged
skill sitting in it is a deferral, not an amendment. What publication does
change is the *description* of what the package contains — a factual
enumeration, not a scope — because deferring the question of what a plugin is
for is not a licence to misdescribe what is in it
(`kodhama-spec-0005-issue-taxonomy-skill-publication`).
```

**H. `plugins/kodhama/README.md`, the Claude row of the evidence table** — one
word, singular to plural. **Anchored by string, never by line number:**

- **Before:** `and reports the declared skill in its component inventory.`
- **After:** `and reports the declared skills in its component inventory.`

**Why the line number must not be used** *(v8; both this literal and its two
dependants named "line 22", which is the pre-edit position)*. Literal **B**
replaces the file's first 9 lines with 26, and **both edits land in the same
file in the same change**. After **B** applies, this sentence sits at **line
39**, not 22. An executor reading `readme.splitlines()[21]` would assert
against the wrong line and ship **a red test against a correct package** —
D1's defect class, and this wave's own failure mode in miniature: an edit whose
dependant sits thirty lines below it in the same file. Locate the sentence by
its `Before` string; if `B` has already applied, that string is still unique in
the file and still the only occurrence.

This touches none of the five strings the existing README test pins, and brings
the sentence into line with `scripts/keyless_admission_check.py`, which has said
*"skill directories"* since it was written.

## Package changes

| Carrier | Change | Constraint |
|---|---|---|
| `plugins/kodhama/VERSION` | `0.2.0` → `0.3.0` | Additive payload, so a minor bump. `validate_kodhama_plugin.py` enforces valid SemVer and manifest equality; it does **not** enforce the value. |
| `plugins/kodhama/.claude-plugin/plugin.json` | `version` → `0.3.0`; `description` → **C** | Must equal `VERSION` exactly. |
| `plugins/kodhama/.codex-plugin/plugin.json` | `version` → `0.3.0`; `description` → **C**; `interface` fields → **E** | Must equal `VERSION` exactly. `"skills": "./skills/"` is a directory declaration and needs no change. |
| `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json` | the `kodhama` entry's `description` → **D** | The entry `description` is this repository's only carrier of the `kodhama-0021` §2 disclosure. The literal is pinned in `tests/test_kodhama_plugin.py`, updated in the same change. |
| `plugins/kodhama/README.md` | lines 1–9 → **B**; the `declared skill` sentence → **H**, located **by string** | Everything else unchanged, preserving the five strings the existing README test pins. **H's target is not at a fixed line:** **B** turns 9 lines into 26 in the same file, moving it from 22 to 39. |
| `distribution/repository-scope.md`, `CLAUDE.md`, `README.md` | the marked block → **A**, byte-identical in all three | See §Standing scope claims. |
| `CLAUDE.md` | lines 66–68 → **F** | Separate from the marked block; same file, different obligation. |
| `conductor/wave-issue-taxonomy/plugin/DIRECTION.md` | lines 45–47 → **G** | Authorised edit 2 to staged text. |
| `.github/workflows/validate-marketplace-setup.yml` | add `"conductor/wave-issue-taxonomy/plugin/**"` to `on.pull_request.paths` | See §Closing the CI blind spot. |
| `tests/TEST_DEPS.md` | `depends_on` gains this spec, pinned `@v9` | R18. Its own text says the tests *"derive from the dependencies above"*; the new tests derive from this spec. |
| `tests/test_kodhama_plugin.py` | the **fourteen** distinct `new: test_*` named in §How each criterion is checked, plus the updated literal **D** in `test_kodhama_catalog_entries_disclose_no_support_claim` | The criteria table is the authority for which tests exist; this row is a summary of it. The existing tests must keep passing unchanged; the module docstring, which names specs 0003 and 0004, gains this one. |
| `conductor/wave-issue-taxonomy/README.md` | the staging table records each moved file's published home | S10's second clause. Reviewer-checked; prose currency is not mechanically checkable. |

No catalog **source shape** changes: both entries already exist and already use
the local-source shape spec 0004 §Kodhama plugin exposure fixes.

## Closing the CI blind spot

v1 disclosed that the anti-drift guard is blind to a PR touching only
`conductor/`. Maintainer ruling, now recorded in
`conductor/wave-issue-taxonomy.md` Lane B: close it, narrowly. Publication adds
exactly one entry to `on.pull_request.paths` in
`.github/workflows/validate-marketplace-setup.yml`:

```yaml
      - "conductor/wave-issue-taxonomy/plugin/**"
```

The filter after the change is these eight entries:

```
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
.github/workflows/validate-marketplace-setup.yml
conductor/wave-issue-taxonomy/plugin/**
plugins/kodhama/**
scripts/validate_kodhama_plugin.py
scripts/keyless_admission_check.py
tests/**
```

**Deliberately not widened further.** The property the ruling protects is that
**the test gate does not run on a docs-only PR** — the unittest suite, the
validator, the `npm install` of two CLIs, and the keyless admission check are
the expensive things, and a prose edit should pay none of it. That is why
`conductor/**` is not added wholesale, and only the one staging subtree whose
re-population S10 forbids.

*Stated this way in v4 because the wider claim is false.* `CLAUDE.md` said a
docs-only PR *"gets no check at all"*; two of the three workflows carry no
`paths:` filter and run on every PR, so it never did. Literal **F** repairs the
sentence; the ruling is unaffected, because it was always about cost.

**A limit that follows from the same property, and is therefore not a
defect.** The `distribution-scope` block's three copies live in
`distribution/repository-scope.md`, `CLAUDE.md` and `README.md`, none of which
is in the filter. S14's parity check therefore fires on any PR that also
touches a gated path — including this publication, which touches all three
copies — and not on a PR that edits only one copy. Making it fire there would
put `CLAUDE.md` and `README.md` inside the test gate, which is the cost the
ruling declines to pay for a prose edit. The guard is worth having for the PRs
it does cover; the residual gap is inherent, not overlooked.

*The gap is also smaller than it looks, and this is measured rather than
assumed:* a PR editing only `CLAUDE.md` still draws the Claude review, which
reads the diff. That is a reviewer, not a gate, so it is not offered as a
substitute for S14 — but "no check at all" was never the situation.

## Relationship to spec 0004

Spec 0004 lists four paths under *"Kodhama plugin exposure"*, ending with
`plugins/kodhama/skills/setup-ci-marketplace/SKILL.md`, introduced by *"The
skill is exposed from the independently versioned Kodhama plugin"*. That
sentence enumerates the carriers of **that one skill**, not a closed inventory
of the package. Read as closed it would forbid the package from ever carrying a
second skill, which no decision states.

This publication therefore **does not amend spec 0004**. Its clauses that bind
the package as a whole — S10 and R16 (VERSION/manifest parity, present-entry
catalog shape) — are satisfied unchanged.

**Spec 0004's R18 does not fire here, and this spec claims no compliance with
it.** R18 is event-driven: *"When a PR adds a Kodhama host catalog entry"*. Both
entries already exist; this publication **modifies** their `description` and
adds nothing. `scripts/keyless_admission_check.py` does run against this change
— but because the `repository-validation` job runs it unconditionally on every
triggering PR, which is a fact about the workflow, not R18 being met. Reporting
an untriggered obligation as satisfied would make the next catalog-adding PR
look pre-cleared.

Open question 1 records the alternative reading of the exposure list.

## Publication is not adoption, and not force

Three separate non-events, each stated because each has a plausible reader who
would assume otherwise:

- **No repository is enabled.** This repository's `enabledPlugins` is untouched,
  and no other repository is edited. Lane D of the wave brief records opt-ins;
  it does not perform them.
- **No org is provisioned.** No issue type is created, no label is seeded, no
  existing issue is edited. That is Lane E, and it needs a token scope this
  change does not use.
- **The convention does not come into force.** By `kodhama-0026` D12 and the
  skill's own gate, an agent that loads the shipped skill in an org lacking any
  of the six enabled types is instructed to say so and stop.

## Acceptance criteria

### Scenarios

**S1 — the package's file inventory is closed** *(amended v2; was: "the skill
lands as a real skill", which asserted only that two files exist and so left
`DIRECTION.md` and R1's "no other file" half checked by nothing)*

- **Given** the published package,
- **When** every file under `plugins/kodhama/` is listed,
- **Then** the set of paths relative to `plugins/kodhama/` is exactly:

  ```
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  DIRECTION.md
  README.md
  VERSION
  scripts/seed-issue-taxonomy.sh
  skills/issues/SKILL.md
  skills/issues/reference/taxonomy.md
  skills/setup-ci-marketplace/SKILL.md
  ```

  and the `name` in `skills/issues/SKILL.md`'s frontmatter equals `issues`.

  *A closed set rather than nine presence assertions: it proves `DIRECTION.md`
  landed at the plugin root, proves nothing stray came with it, and makes any
  later legitimate growth a deliberate spec revision instead of a silent one.*

**S2 — the host exposes exactly the declared skills**

- **Given** the published package,
- **When** `python3 scripts/keyless_admission_check.py` runs,
- **Then** the Claude host validates the manifest with **no warnings**, installs
  the plugin from a local catalog, and reports a component inventory equal to
  `issues, setup-ci-marketplace`.

**S3 — the version carriers move together**

- **Given** the added payload,
- **When** `python3 scripts/validate_kodhama_plugin.py` runs,
- **Then** it passes with `plugins/kodhama/VERSION` reading a valid SemVer
  string and both host manifests carrying that identical string.

**S4 — the actuator ships runnable and outside `skills/`**

- **Given** the staged seed script,
- **When** publication lands,
- **Then** it is at `plugins/kodhama/scripts/seed-issue-taxonomy.sh`, is
  executable, `bash -n` reports no syntax error, `--help` exits `0`, and an
  unrecognised argument exits `2` without contacting a network.

**S5 — the skill does not reach the actuator**

- **Given** the published payload,
- **When** every `SKILL.md` and every file under a skill's `reference/`
  directory is scanned,
- **Then** none of them names `seed-issue-taxonomy`, `gh label create`, or
  `gh api --method POST`.

*This constrains `skills/` only. The shipped `README.md` names the actuator by
design — see §Why the actuator sits outside `skills/` — and S16 requires it.*

**S6 — the migration mapping stays out of the package**

- **Given** the mapping at
  `conductor/wave-issue-taxonomy/plugin/migration/legacy-mapping.md`,
- **When** publication lands,
- **Then** no file under `plugins/kodhama/` is named `legacy-mapping.md`, no
  `migration/` directory exists under `plugins/kodhama/`, and no published file
  names a relative path resolving into one.

**S7 — every payload-relative pointer resolves** *(amended v2; was: an
extraction regex that returned no match on `../../../DIRECTION.md`, so the
check passed against a genuinely dangling pointer)*

- **Given** every `.md` and `.sh` file under `plugins/kodhama/`,
- **When** each token matching a relative path that ends in `.md` or `.sh`
  **and contains at least one `/`** is resolved against the naming file's own
  directory,
- **Then** every resolved path exists.

*Extraction rule, stated so an implementation can be checked against it rather
than trusted:* match `(?:\.\.?/)*[\w.-]+(?:/[\w.-]+)*\.(?:md|sh)`, then **keep
only tokens containing `/`**. The v1 form `(\.\./)*[\w-]+(/[\w.-]+)+\.(md|sh)`
required a `/` *after* the first path component, which `../../../DIRECTION.md`
does not have; the `/`-containing filter belongs on the token, not on the
pattern's tail. Tokens introduced by `://` are skipped.

*Why the filter is required, not incidental:* `skills/issues/reference/taxonomy.md`
names bare `SKILL.md` three times (its lines 3, 8 and 153). Without the
qualifier those three become demands that `skills/issues/reference/SKILL.md`
exist, which it must not.

*Consequences, which is the point of the check:* `DIRECTION.md` anywhere but
the plugin root fails it; the seed script fails it until authorised edit 1
lands; moving `reference/taxonomy.md` out of the skill directory fails it.

*Mutation obligation:* prove the implementation by temporarily moving
`plugins/kodhama/DIRECTION.md` and confirming the test **fails**. A check that
passes in both states is what v1 shipped.

**S8 — the in-force gate ships intact**

- **Given** the published `SKILL.md`,
- **When** it is scanned,
- **Then** it retains the `gh api /orgs/<org>/issue-types` probe, selection on
  `is_enabled`, all six type names (`Bug`, `Feature`, `Task`, `Research`,
  `Decision`, `Epic`), and an instruction to stop when any is absent or
  disabled.

**S9 — the actuator's entire `gh` surface is pinned**

*(Amended v3. The v2 form called itself an allowlist and implemented a denylist.
Injected into the real script, four of five added mutating commands survived
it: `gh issue edit --add-label`, `gh api -X DELETE` in its short-flag form, a
POST to `/orgs/$ORG/teams`, and `gh repo edit --visibility`.)*

- **Given** the shipped seed script,
- **When** every occurrence of `gh` followed by a lowercase word, and
  optionally a second lowercase word, is extracted,
- **Then** the resulting multiset is **exactly**:

  | Command head | Count |
  |---|---:|
  | `gh api` | 3 |
  | `gh auth refresh` | 1 |
  | `gh auth status` | 1 |
  | `gh issue list` | 1 |
  | `gh label create` | 1 |
  | `gh label list` | 1 |
  | `gh token lacks` | 1 |

- **And** these three literals appear, quoted exactly as the source writes them:

  ```
  gh api --method POST "/orgs/$ORG/issue-types"
  gh api --method PATCH "/orgs/$ORG/issue-types/$id"
  gh label create "$name" -R "$ORG/$repo"
  ```

- **And** none of `gh label delete`, `gh issue delete`, `gh repo delete`,
  `--method DELETE`, `--method PUT`, `-X DELETE`, `-X PUT` appears anywhere in
  the file.

*Why a closed multiset and not a denylist:* a denylist can only forbid what
someone thought of. The nine occurrences sit at lines 67, 68, 69, 76, 83, 92,
133, 139 and 148, and pinning the set means **any** added `gh` invocation
changes it, whatever its verb.

*Two of the nine are prose, and that is deliberate.* Line 68 is the sentence
*"your gh token lacks the 'admin:org' scope"*, and line 69 is advice printed
inside an `echo`. The extractor does not model shell quoting, so both are
counted. Excluding them would need a shell parser; including them means editing
those two sentences trips the test and a human re-confirms the surface — cheap,
and fail-safe for an actuator.

**The head for line 68 is `gh token lacks`, not `gh token`** *(corrected v4)*.
The extractor's second group is optional but **greedy**, so it captures the
word after `token`. v3's table said `gh token`, which would have made S9 fail
against a correct package — an arbiter red where it should be green, which is
worse than one green where it should be red, because it teaches a reader to
override the check. The other eight heads were exact. **Anyone changing the
extractor must re-derive this table from it rather than editing one to match
the other by eye**, which is the mistake v3 made.

*Why the exact literals are still needed on top of the multiset:* changing
`--method PATCH` to `--method DELETE` leaves the head `gh api` and the count at
three. The literal assertion is what catches it.

*Why the substring `delete` is not banned:* the file says *"This script NEVER
deletes a label"*, *"Reported, never deleted"*, *"now redundant, NOT deleted"*
and *"No label is ever deleted by this script"*. A bare substring ban fails on
four sentences promising the opposite of what it forbids.

*Mutation obligation:* prove the implementation by injecting each of the four
survivors named above into a copy and confirming each **fails**.

**S10 — publication moves rather than copies** *(amended v3; the v2 form also
asserted that `migration/legacy-mapping.md` still exists, which Lane A will
make false — the same reason S12 was kept out of the permanent suite)*

- **Given** publication has landed,
- **When** `conductor/wave-issue-taxonomy/plugin/` is listed,
- **Then** it contains no `skills/` directory, no `scripts/` directory and no
  `DIRECTION.md`, and `conductor/wave-issue-taxonomy/README.md` records the
  published home for each moved file.

*R12 is established by these negatives together with S1's closed inventory. No
assertion about the mapping's continued presence is needed, and one would go
red on a legitimate Lane A relocation.*

**S11 — both listings describe what the package carries**

- **Given** both marketplace catalogs,
- **When** `validate_kodhama_plugin.py` and the pinned-description test run,
- **Then** each `kodhama` entry's `description` equals literal **D**, the Codex
  entry carries no field beyond its four exact fields plus `description`, and
  the literal pinned in `tests/test_kodhama_plugin.py` equals what the catalogs
  carry.

**S12 — publication enables nothing** *(amended v2; the allowlist now admits
the workflow file S15 requires editing)*

- **Given** the publication change,
- **When** its diff is reviewed,
- **Then** it touches no `.claude/settings.json`, no `enabledPlugins` value, no
  repository other than this one, and creates no issue type, label, or issue;
  and every changed path is under `specs/`, `plugins/kodhama/`, `tests/`,
  `conductor/`, `distribution/`, or is one of `CLAUDE.md`, `README.md`,
  `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`,
  `.github/workflows/validate-marketplace-setup.yml`.

**S13 — no standing statement survives that the package is narrower than it is**
*(amended v3; the v2 form covered four carriers of eight)*

- **Given** the eight carriers listed in §Standing scope claims,
- **When** publication lands,
- **Then** `distribution/repository-scope.md`, `CLAUDE.md` and `README.md` each
  carry literal **A** between their `distribution-scope` markers; `CLAUDE.md`
  carries literal **F**; `plugins/kodhama/README.md` carries literal **B** as
  its opening and literal **H** as its `declared skill` sentence — **matched as
  a string, not at a line number, since **B** displaces it from line 22 to line
  39 in the same change**; **`plugins/kodhama/DIRECTION.md`**
  carries literal **G**; `conductor/wave-issue-taxonomy.md` Lane B asserts no
  untouched scope; and the discovery command in §Standing scope claims surfaces
  no further carrier.

*(Amended v5. The v4 text asserted that
`conductor/wave-issue-taxonomy/plugin/DIRECTION.md` carries literal **G** —
the **staged** path, which S10 and R12 require to be **gone** by the time this
scenario is evaluated. A deleted file cannot carry a literal, so an executor
building v4 literally would have shipped a red test against a correct package.
Both are post-publication assertions; the edit is applied at the staged path
and verified at the published one.)*

**S14 — the three mirrored copies stay identical**

- **Given** `distribution/repository-scope.md`, `CLAUDE.md` and `README.md`,
- **When** the text between `<!-- distribution-scope:begin -->` and
  `<!-- distribution-scope:end -->` is extracted from each,
- **Then** all three extractions are byte-identical, and each file contains
  exactly one begin marker and one end marker.

**S15 — the CI filter covers the staging directory** *(amended v3; the v2
arbiter needed a YAML parse this repository cannot perform)*

- **Given** `.github/workflows/validate-marketplace-setup.yml`,
- **When** its `on.pull_request.paths` list is read **by regex** — the region
  from the line matching `^\s*paths:\s*$` to the first following line whose
  indentation is not deeper, with each entry taken from `^\s*-\s*"([^"]+)"\s*$`
  —
- **Then** the extracted list equals the eight entries in §Closing the CI blind
  spot, in that order, and contains no bare `conductor/**`.

*No YAML dependency:* neither `tests/` nor `scripts/` imports `yaml` today, and
the `repository-validation` job installs no Python packages before running the
suite, so an `import yaml` would fail at collection on a clean runner.
`tests/TEST_DEPS.md` declares **artifact** dependencies, not runtime packages,
so it is not the place to add one.

**S16 — the shipped README enumerates the package's contents** *(amended v3;
adds the actuator disclosure and the corrected purpose wording)*

- **Given** `plugins/kodhama/README.md`,
- **When** it is scanned,
- **Then** it names `skills/issues`, `skills/setup-ci-marketplace` and
  `scripts/seed-issue-taxonomy.sh`; describes the last as an actuator that is
  dry-run by default; states that what the plugin is *for* has never been
  decided; and still contains the five strings the existing README test pins.

**S17 — the actuator's dry-run default is a behaviour, not a claim**
*(new in v9)*

- **Given** the shipped `scripts/seed-issue-taxonomy.sh` and a stub `gh` first
  on `PATH` that appends its own `"$@"` to a log and exits 0,
- **When** the script is invoked **without `--apply`**,
- **Then** the log contains **no write call** — none of
  `api --method POST`, `api --method PATCH`, `label create` — and contains only
  read calls drawn from `auth status`, `api /orgs/<org>/issue-types`,
  `issue list`, `label list`.
- **And** the same holds for a default invocation carrying **any** other
  accepted flag: `--org`, `--repo`, `--types-only`, `--labels-only`, `--force`.
  **`--apply` is the only argument that may set `APPLY=1`.**
- **And** when the stub reports an empty backlog and `--force` is absent, the
  log contains **no `label list` call for that repository** — the skip gate
  holds.

*Credential-free and offline.* The stub intercepts every `gh` invocation, so
nothing reaches GitHub and no token is read; the test needs only an `env=`
parameter on the existing `run()` helper in `tests/test_kodhama_plugin.py` so
`PATH` can be prepended.

*Mutation obligation — these four are measured survivors of the v8 suite, not
hypotheses. Each must turn this criterion red:*

| Mutation | Property it must break |
|---|---|
| `APPLY=0` → `APPLY=1` | no write call on a default invocation |
| `run()`'s `if [[ $APPLY -eq 1 ]]` → `if true` | no write call on a default invocation |
| `APPLY=1` added to the `--labels-only` handler | `--apply` is the only path that sets it |
| the empty-backlog gate → `if false` | the skip gate holds without `--force` |

*Why behavioural and not a static pin on `APPLY=0`.* A grep for the assignment
catches the first mutation and the third, and **misses `if true` entirely** —
the one that silently converts every `run()` call into an execution while the
default still reads as `0`. The property that matters is what the script
*does*, and only running it establishes that.

*Why the third property is here, when the first two do not reach it.* The
empty-backlog gate protects `--force`, not `--apply`, so neither write-call
property fails when it is removed. Listing that mutation without a property
that catches it would be a mutation obligation this criterion cannot discharge
— the defect S9 and D1 were both about.

### Requirements

- **R1 (ubiquitous):** The files under `plugins/kodhama/` shall be exactly the
  nine paths enumerated in S1, adding
  `skills/issues/SKILL.md`, `skills/issues/reference/taxonomy.md`,
  `scripts/seed-issue-taxonomy.sh` and `DIRECTION.md` to the five already
  present, and no other.
- **R2 (ubiquitous):** The issue skill shall be the only new entry under
  `plugins/kodhama/skills/`, its directory name shall equal its frontmatter
  `name`, and its reference shall sit at `skills/issues/reference/taxonomy.md`.
- **R3 (ubiquitous):** The seed script shall sit outside
  `plugins/kodhama/skills/`, and no `SKILL.md` or skill reference shall name it
  or any provisioning command.
- **R4 (ubiquitous):** `migration/legacy-mapping.md` shall not be published in
  the plugin, and no published file shall name a relative path that resolves
  into it.
- **R5 (ubiquitous):** `plugins/kodhama/VERSION` and both host manifest
  `version` fields shall carry one identical, valid SemVer string. **The value
  is not pinned here** — v9 wrote `0.3.0` into a `(ubiquitous)` clause, which
  is a standing invariant, so the package could never be versioned again
  without violating this spec (#94).
- **R6 (ubiquitous):** Every relative path a published payload file names that
  ends in `.md` or `.sh` **and contains at least one `/`** shall resolve to an
  existing file relative to that file's own directory.
- **R7 (unwanted behavior):** The publication shall not enable the plugin in any
  repository, alter any `enabledPlugins` value, create an org issue type,
  create or delete a label, or edit an existing issue.
- **R8 (unwanted behavior):** No manifest field, catalog `description`, README
  sentence, `distribution-scope` block, or spec clause introduced by this
  publication shall state or imply a purpose, theme, or scope for the `kodhama`
  plugin; each shall enumerate the package's present contents, and shall
  attribute staging only to the issue skill.
- **R9 (state-driven):** While any of `Bug`, `Feature`, `Task`, `Research`,
  `Decision` or `Epic` is absent or disabled in the org under inspection, the
  shipped skill shall instruct the agent to say so and stop.
- **R10 (event-driven):** When the payload under `plugins/kodhama/` changes,
  `scripts/keyless_admission_check.py` shall report the Claude host exposing
  exactly the plugin's declared skill directories.
- **R11 (ubiquitous):** The shipped actuator shall change nothing without
  `--apply`, **its complete `gh` surface shall be the closed multiset pinned in
  S9**, its mutating members shall be exactly the three literals there, and it
  shall exit non-zero on an argument it does not recognise. *(v3: "exactly" was
  asserted against a denylist that could not establish it.)*
- **R12 (ubiquitous):** Publication shall move rather than copy: no staged copy
  of a published file shall remain under `conductor/`.
- **R13 (ubiquitous):** Each present `kodhama` catalog entry shall carry
  literal **D** as its `description`, and the literal pinned in
  `tests/test_kodhama_plugin.py` shall equal it.
- **R14 (ubiquitous):** The shipped `SKILL.md` frontmatter shall carry only keys
  **the Claude host** accepts without emitting a validation warning.
  `codex plugin` 0.145.0 has no `validate` subcommand, so no Codex-side arbiter
  exists — see §Recorded host finding.
- **R15 (ubiquitous):** No statement of **present state** — repository
  documentation, ledgers, or text shipped inside the package — shall enumerate
  what the install door distributes or originates, what the `kodhama` package
  contains, or which paths CI gates, in a way that omits what this publication
  adds; the **seven literal-bearing** carriers in §Standing scope claims shall
  carry literals **A**, **B**, **F**, **G** and **H**, **each verified at its
  post-publication path** — carrier 6 is edited at the staged `DIRECTION.md`
  and verified at `plugins/kodhama/DIRECTION.md`, which R12 requires the staged
  copy to have vacated. **Carrier 7 bears no literal** and is discharged by its
  ledger correction alone, which S13 already asserts correctly; *(v6: R15 said
  "the eight carriers … shall carry literals", which read alone was
  undischargeable for the one carrier that has none.)* **Ratified decisions are excluded**: they are append-only records of
  a past act, corrected by forward pointer and never edited, so no executor
  could discharge this requirement against them. The exclusion removes them
  from the *edit* obligation only — see open question 6 for what replaces it.
- **R16 (ubiquitous):** `interface.capabilities` shall contain exactly one
  element per directory under `plugins/kodhama/skills/`, ordered by directory
  name, each containing the string `skills/<directory-name>`.
- **R17 (ubiquitous):** `.github/workflows/validate-marketplace-setup.yml`
  shall trigger on changes under `conductor/wave-issue-taxonomy/plugin/` and
  shall not trigger on `conductor/` generally.
- **R18 (ubiquitous):** `tests/TEST_DEPS.md` shall declare this spec among its
  `depends_on` **in the pinned `id@vN` form**, at the version the tests were
  written against. `specs/README.md` requires the pinned form for versioned
  spec dependencies, and the file already pins its sibling `@v5`; an unpinned
  entry would have satisfied v3's wording and matched neither. **No version
  literal here** — v9 named `@v9` "as of this revision", so the v10 bump put
  the artifact in violation of the clause while the suite stayed green, its
  assertion having been updated independently. The version lives in the
  arbiter, which is what moves with the tests. Same defect as R5, found by the
  reviewer on #97.
- **R19 (unwanted behavior):** If the shipped actuator is invoked without
  `--apply`, it shall issue no call that creates or modifies an org issue type,
  a repository label, or an issue — **established by execution against a stub
  `gh`, never by the presence of `APPLY=0` or by the help text's claim**. No
  argument other than `--apply` shall set `APPLY=1`, and a repository with an
  empty backlog shall be skipped unless `--force` is given. *(v9: R11 already
  said "shall change nothing without `--apply`", and six pinned literals
  asserted it in prose; **nothing made it fail when it stopped being true.**)*

### How each criterion is checked

Every row names one arbiter. `new:` marks a test this publication must add to
`tests/test_kodhama_plugin.py`; the others already exist.

| Criterion | Checked by |
|---|---|
| S1, R1, R2 | `new: test_the_package_inventory_is_closed` — `sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob("*") if p.is_file() and p.name != ".DS_Store")` equals the nine-path list, plus `name: issues` matches its directory. *(v5: the filter carries D6's rationale one criterion over. The repository has no `.gitignore`, and `CLAUDE.md` tells the executor to run the suite locally — on macOS that means a stray `.DS_Store` fails a correct package. CI is safe on a fresh clone, so this is a local-red risk only.)* |
| S2, R10, R14 | `python3 scripts/keyless_admission_check.py`, unchanged. Its `declared_skills()` globs `skills/*/SKILL.md` and asserts host inventory equality, so it extends itself to the new skill with no edit. CI runs it in the `repository-validation` job |
| S3 | `python3 scripts/validate_kodhama_plugin.py`, already re-run by `test_repository_package_and_carrier_parity_validate` |
| R5, the value | **Reviewer**, not the validator: `git diff origin/main...HEAD -- plugins/kodhama/VERSION`. The validator checks that the three carriers agree and that the string is valid SemVer, never whether the value is the right one for the change. **Pass condition:** the new value is valid SemVer, differs from the old, and moves in the direction the payload implies — additive payload, minor bump. *(v10: this row previously read "the value `0.3.0`", the tell — an arbiter naming a constant for a field that moves every release. v11: it had no pass condition at all, so it was a third unmechanizable item and the rubric's count of two was short.)* |
| S4 | `new: test_seed_script_is_runnable_and_fails_closed` — `os.access(X_OK)`, `bash -n`, `--help` exit `0`, `--bogus` exit `2`. Both invocations return before any `gh` call, so the test needs no network and no credentials |
| S5, R3 | `new: test_the_skill_never_reaches_the_actuator` — scans every `SKILL.md` and `reference/*.md` under `plugins/kodhama/skills/` for `seed-issue-taxonomy`, `gh label create`, `gh api --method POST`, **and asserts no `*.sh` exists anywhere under `plugins/kodhama/skills/`**. *(v9: the text scan alone does **not** make §Why the actuator sits outside `skills/` true — conformance measured it, and moving the actuator into `skills/issues/` left this test green. Four other tests caught the move, so the protection held; the **named arbiter** did not. The executor added the `*.sh` assertion, which conformance ruled inside the contract because it makes a sentence the spec asserts about itself true and cannot false-red. It is recorded here rather than left implicit. **Match on `path.suffix == ".sh"`, not on the exact filename** — an exact match lets `skills/issues/seed.sh` through, and the technique is the one `test_the_migration_mapping_stays_out_of_the_package` argues for forty lines away: walk the tree so a rename does not walk past.)* |
| S17, R19 | `new: test_the_actuator_makes_no_write_call_without_apply` — writes a stub `gh` into a temp dir, prepends it to `PATH` via a new `env=` parameter on the module's `run()` helper, invokes the shipped script with no `--apply` and then with each other accepted flag, and asserts the stub's log holds only read calls. A third case stubs an empty backlog and asserts no `label list` for that repository. **Mutation obligation: all four survivors named in S17 must fail it.** Credential-free, offline, no model turn |
| S6, R4 | `new: test_the_migration_mapping_stays_out_of_the_package` — no `legacy-mapping.md` and no `migration/` under `plugins/kodhama/`, walked with `rglob` so a rename does not walk past it |
| S7, R6 | `new: test_every_payload_relative_pointer_resolves` — the extraction rule quoted in S7, with the `/`-containing filter applied to the **token**. **Mutation obligation applies.** Bounded heuristic: path-shaped tokens only, `://` skipped |
| S8, R9 | `new: test_the_in_force_gate_ships_intact` — literal `assertIn` on the probe, `is_enabled`, the six type names, and the stop instruction |
| S9, R11 | `new: test_the_actuator_gh_surface_is_pinned` — extract `\bgh\s+([a-z][a-z-]*)(?:\s+([a-z][a-z-]*))?`, compare the `collections.Counter` to the seven-head table, then three `assertIn` on the exact literals and seven `assertNotIn` on the forbidden forms. **Mutation obligation: all four named survivors must fail it** |
| S10, R12 | `new: test_the_staging_copies_are_gone` — negatives only; the three paths must not exist. Reachable on a `conductor/`-only PR because S15 adds that subtree to the filter |
| S11, R13 | `validate_kodhama_plugin.py` for the nonblank `description` and the closed Codex entry; `test_kodhama_catalog_entries_disclose_no_support_claim` for literal **D**, whose expected string this publication updates in the same commit |
| S13, R15 | `new: test_no_standing_statement_understates_the_package` — literal **A** in all three block carriers, **F** in `CLAUDE.md`, **B** and **H** in the shipped README, **G** in **`plugins/kodhama/DIRECTION.md`** (the published path, not the staged one R12 empties), and the absence of the Lane B claim. **The rule's open half is reviewer judgment**: the test checks eight known carriers, not that a ninth was never written. The discovery command in §Standing scope claims is the reviewer's instrument for that half |
| S14 | `new: test_the_distribution_scope_block_is_mirrored_exactly` — extract between markers from the three files, assert byte identity and exactly one marker pair each. **Disclosed limit:** none of the three is in CI's `paths:` filter, so this fires on PRs that also touch a gated path — including this one — and not on a PR editing only `CLAUDE.md`. That follows from the docs-only-PR property the ruling protects |
| S15, R17 | `new: test_the_ci_filter_covers_the_staging_subtree` — the regex extraction in S15, asserting the eight entries in order. No new dependency. Editing the workflow triggers the workflow, since it lists itself |
| S16 | `new: test_shipped_readme_enumerates_the_package_contents`, alongside the existing `test_shipped_readme_discloses_hosts_and_makes_no_support_claim`, which must still pass unchanged |
| R16 | `new: test_capabilities_enumerates_the_skill_directories` — compares the array against `sorted(d.name for d in (PLUGIN/"skills").iterdir() if d.is_dir())`, so it is derived from the package rather than remembered. *(v4: the `is_dir()` guard was missing; a stray `.DS_Store` or `README.md` beside the skill directories would have made the expected array wrong and failed a correct package.)* |
| R18 | `new: test_test_deps_declares_this_spec` — asserts `tests/TEST_DEPS.md`'s `depends_on` contains the spec id **with an `@vN` pin**, not the bare id, **and that N equals this file's own `version:` frontmatter**. *(v11: the version half had no arbiter. v10 left the expected value as a literal in the test body, so the test asserted itself and a wrong pin in both places passed. Reading it from the spec is the anchor a test edit cannot satisfy.)* |
| The staging README's updated pointer (S10) | **Reviewer**, reading the diff of `conductor/wave-issue-taxonomy/README.md`. Prose currency is not mechanically checkable |
| S12, R7 | **Reviewer**: `git diff --name-only origin/main...HEAD` against S12's allowlist. Deliberately **not** a permanent test — Lane D expects this repository to opt in eventually, and a test forbidding that would have to be deleted the day it mattered |
| R8, "no purpose is minted" | **Not mechanically checkable.** Pinning literals **A**–**H** moves the judgment to one human read at the spec gate and freezes the result; drift from the frozen strings is then caught by S11, S13, S14 and R16. Whether the frozen strings themselves imply a purpose is the reviewer's call, and this spec claims no check for it |
| "Publication changes no repository's issue behaviour" (`kodhama-0026` D12) | **Not mechanically checkable, and not checked.** It is a claim about the world outside this repository. The nearest evidence is S8: the shipped instruction that stops. That the instruction is *obeyed* needs a model turn, which needs a key — the same honest gap `plugins/kodhama/README.md` already discloses for the marketplace skill |

## Recorded host finding — `implements:` in skill frontmatter

v1 parked this as open question 2. It is now answered by a run, recorded here
because the answer changes what R14 is worth.

**Observed:** `claude plugin validate` **does** parse `SKILL.md` frontmatter —
malformed YAML fails validation, a missing frontmatter block produces a warning
— and it tolerates unknown keys silently. **Host and version: Claude Code
`2.1.220`.**

1. `implements: kodhama-0026-issue-taxonomy` is legal and ships unchanged.
2. **R14 is load-bearing, not vacuous.** It catches malformed YAML and a missing
   block — the two failure modes that would silently disarm the skill — and
   `keyless_admission_check.py` fails on any warning, so it is enforced on every
   triggering PR.
3. **Version skew, disclosed:** the observation is from `2.1.220`; CI pins
   `2.1.199`. This needs no separate verification, because the check *is* the
   verification: if `2.1.199` behaves differently the publishing PR goes red
   rather than shipping a wrong assumption.
4. **R14 binds the Claude host only.** `codex plugin` `0.145.0` has no
   `validate` subcommand, so the Codex manifest and the Codex-side skill load
   are **unchecked by construction** — the same asymmetry spec 0004 records for
   admission evidence.

## Open questions

**1. Whether spec 0004's exposure list is per-skill or per-package.** This spec
reads its four paths as the carriers of that one skill, so a second skill needs
no amendment there. A reviewer who reads the list as the package's closed
inventory would require a 0004 amendment and a version bump. **Not blocking:**
on either reading the acceptance criteria above are unchanged.

**2. The mapping's own pointers break on relocation.**
`migration/legacy-mapping.md` names `reference/taxonomy.md` (twice) and
`scripts/seed-issue-taxonomy.sh` as plugin-root-relative paths. Once it rides
the decision to `kodhama/kodhama` and the payload lives here, none of the three
resolves. **Not this spec's to fix** — the mapping is not published by it — but
it is a consequence this split makes visible, and Lane A should not inherit it
silently.

**3. The seed script's defaults aim inside the family, at a repository
`kodhama-0021` names.** `ORG` defaults to `kodhama` and `ALL_REPOS` hardcodes
nine repositories **including `math-quest`** — the repository 0021 reserves by
name (*"Math Quest receives no plugin change until it explicitly opts into
preview"*). So `--apply` with no `--repo` aims label creation at it.

*Stated precisely:* 0021 reserves **plugin adoption**, and seeding a label is a
different act, so this is **adjacency, not a violation**. What is true is that
the shipped default sweeps in the one repository the corpus singles out for
restraint, and a hurried operator would not notice. The mitigations are in the
script and pinned by R11. Whether the default should be `--repo`-required is the
plugin owner's call, and the plugin has no decided owner.

**4. Which repository's `depends_on` grammar this spec should use.**
`kodhama-0026` relocates to `kodhama/kodhama`, and its own open question 3
records that no ruling exists on bare versus `<repo>/<id>` referents, with four
of five existing records bare. This spec uses the **bare** form. A ruling would
rewrite this line and five others; it changes no criterion here.

**5. Whether `interface.defaultPrompt` may be dropped rather than made
enumerative.** Literal **E** keeps the key with enumerative wording. Dropping it
would be cleaner — a package with two skills has no single default — but
`codex plugin` `0.145.0` offers no `validate` subcommand, so neither the
presence nor the absence of the key can be checked before shipping. Keeping it
is the lower-risk branch of an unverifiable choice.

**6. Whether `kodhama-0017` should receive a forward pointer recording that its
AC3 scope enumeration no longer describes this repository** *(new in v5;
extended in v6)*. Publication diverges from `:33` (*"retains only a narrow
future distribution goal"*) and `:208` (AC3, *"describes only …"*) **in both
directions**:

- it **adds** two things the enumeration does not contain — the issue skill and
  the actuator; and
- it **removes** one the enumeration names — the marketplace-metadata
  description, which leaves literal **A** because `kodhama-0025` redirected the
  goal to the GitHub Actions run log, and a run log is not distributed. *(v6:
  v5 recorded only the addition.)*

AC3 is a frozen record and not a carrier, so no edit is owed and none is
proposed; what is missing is disclosure at the record. The remedy is the
forward pointer, an annotation rather than an edit — `kodhama-0017` already
carries two, `kodhama-0018` two plus a dated annotation.

**This parks against standing practice, and that is the point of saying so**
*(v6)*. In every corpus instance, **the falsifying change writes the pointer in
the same change**: `kodhama-0025` wrote `0017:15-18`; `kodhama-0003` wrote
`0002:33`; `kodhama-0006` wrote `0002:41`. `decisions/0025:151-153` even
budgets for it — *"Each gets a one-line forward pointer to this record — a
pointer each, not another propagation wave."* And the `depends_on` edge this
spec declares **neither satisfies nor evades** that practice: it is a claim
about this spec's inputs and leaves no trace where a reader of `kodhama-0017`
would encounter it.

**Why parked rather than done, stated so the choice is made knowingly.** Every
precedent above is a *decision* annotating a decision. This is a **spec**, and
a spec annotating an approved decision is a different act with no precedent in
this corpus. That difference may not matter — but it is the maintainer's call,
not the author's, and writing the pointer unilaterally would have settled it by
doing. Not blocking; it changes no criterion here.

## Rubric check

No spec-quality rubric and no `.grove/config.toml` exist in this repository, so
the self-check runs against `specs/README.md`, the `contract-author` charter,
and the installed `.grove/versioning.md` and `.grove/relations.md`.

- **Frontmatter** — complete. `kodhama-0020` was added to `depends_on` in v3,
  because §What the plugin is for and literal **B** rest on its naming of the
  overarching plugin and its fixing of the CI skill's home. **`kodhama-0017`
  was added in v5** and is the reason open question 6 exists; see the edge
  breakdown below. *(v6: this bullet documented only the v3 addition, which was
  its whole job in the round that added the v5 one.)*
- **Upstream is approved** — `kodhama-0026-issue-taxonomy` carries
  `status: approved`. `implements` names it alone. `depends_on` carries **seven**
  ids, and they are not all the same kind of edge *(re-walked in v6; v5 called
  them "five" in two bullets, for two different sets, so at least one was wrong
  either way)*:
  - **Five constraints this spec must not break** — `kodhama-0018`,
    `kodhama-0020`, `kodhama-0021`, `kodhama-0025`, and
    `kodhama-spec-0004@v5`.
  - **One the spec diverges from, declared for exactly that reason** —
    `kodhama-0017`, **added in v6's predecessor v5**. Its AC3 is the clause
    literal **A** renders, and publication changes that rendering in both
    directions. Calling it a constraint "this spec must not break" would have
    been false: open question 6 exists because the divergence is real. It is a
    drift-bearing input, disclosed rather than satisfied.
- **Authority for the two new obligations** — recorded in
  `conductor/wave-issue-taxonomy.md` Lane B as of this change, not only in this
  spec's prose. v2's obligations rested on the spec's own account of a
  conversation, which is the defect this wave has been correcting elsewhere.
- **Version pin** — spec 0004 pinned `@v5`; the **six** decisions
  (`kodhama-0017`, `-0018`, `-0020`, `-0021`, `-0025`, `-0026`) are append-only
  and correctly unpinned.
- **Counter** — bumped `10 → 11` at v11 (R18's arbiter), `9 → 10` at v10 (R5, F, R18). The v9 entry below is kept as written. **Required, and the clearest case since v6:**
  S17 and R19 are new testable clauses, so `.grove/versioning.md:59-61` binds
  directly. They are also the only part of v9 that changes behaviour.
- *(Prior counters, retained.)* **v6's bump was required**, per
  `.grove/versioning.md:59-61`: a testable-clause change bumps, and R15's
  `shall` text changed scope. v7 and v8 are the weaker case — no scenario,
  requirement, literal, arbiter or criterion moves in either. v7 realigned three
  passages stating the debt's *kind* to a ruling the maintainer is being asked
  to act on; v8 withdraws a false completeness claim and changes how literal
  **H** is located, which is a correctness-of-application change an executor
  reads as binding. A reader pinning `@v7` would be pinning both defects.
  `tests/TEST_DEPS.md` did not yet name this spec at v9, so no pin went stale then — **it names it now, and the pin going stale is exactly what R18's v11 arbiter catches** — and
  R18's `@vN` is written by the executor at whatever version lands. The section-level delta note carries the five
  fields plus VALUE and CONFIDENCE; S9, S10, S13, S15 and S16 carry
  scenario-level inline tags.
- **Rule scope** — R15 binds statements of present state only. Ratified
  decisions are excluded by construction, not by omission, the exclusion is
  stated where the rule is, and **what the exclusion costs is now named**:
  `kodhama-0017` AC3, parked as open question 6 rather than left silent.
- **Instrument honesty** — the discovery command is disclosed as a heuristic
  that cannot be complete against a semantically stated rule, with its known
  false positives tabulated and its `decisions/` hits typed as forward-pointer
  candidates rather than edit obligations.
- **Both grammars present** — **seventeen** GWT scenarios and **nineteen** EARS
  `shall` requirements.
- **Testability** — every criterion is mapped to one named arbiter. **Two are
  declared unmechanizable and are not dressed up as tests**: whether the pinned
  strings imply a plugin purpose, and whether publication changes behaviour
  outside this repository. Three limits are disclosed rather than hidden: R15's
  open half (a ninth carrier nobody wrote down) is reviewer judgment with a
  discovery command supplied; S14's parity check is unreachable on a PR editing
  only `CLAUDE.md`; and two of S9's nine pinned `gh` occurrences are prose the
  extractor cannot distinguish from commands.
- **No invented scope** — the taxonomy is not restated except for the six type
  names S8 and R9 need as check inputs; **six** unresolved matters are parked
  as open questions, the newest being the one **disclosure** debt this
  publication creates against the append-only corpus — a missing pointer at
  `kodhama-0017`, not a conformance failure, per the ruling in §Standing scope
  claims.

### What v2 changed, and why

| Finding | Repair |
|---|---|
| Maintainer ruling 1 | §Standing scope claims, §Pinned replacement literals, S13, S14, R15 |
| Maintainer ruling 2 | §Closing the CI blind spot, S15, R17; S12's allowlist widened by the workflow file |
| F3 / B1 — S9 could not pass | Rewritten to quote the mutating literals as the source writes them, and to forbid command forms rather than the substring `delete` |
| F1 / B2 — S7 was mutation-proven blind | Extraction rule replaced; the `/` requirement moved onto the token. R6 gained the same qualifier. Mutation obligation written in |
| F2 — S1's coverage was a strict subset of R1 | S1 became a closed nine-path inventory; S16 gave the README requirement the scenario it lacked |
| F5 — literals described, not pinned | §Pinned replacement literals, plus the `capabilities` array rule |
| F6 — the authorised edit was loosely scoped | Quoted verbatim before and after |
| OQ2 open on a wrong premise | Answered by a recorded run; R14 narrowed to the Claude host |
| CI filter misstated; 0004's R18 reported as satisfied; §Scope contradicted S8/R9; open questions miscounted; S10 named the staging README only in prose; the actuator question aimed outward | All corrected in v2 |

### What v3 changed, and why

| Finding | Repair |
|---|---|
| **C1 — literal A stated a falsehood.** *"What it distributes today is the `kodhama` plugin"*; both catalogs list four | **A** rewritten around what this repository **originates**. Deliberately does not enumerate the other three, which would be a fresh closed list with the same failure mode |
| **C2 — three more standing statements falsified and unnamed** | Carriers 6, 7 and 8 added: `DIRECTION.md` §45–47 (literal **G**, a second authorised edit to staged text, with the shipped-document conflict resolved by editing rather than explaining), the wave ledger's Lane B line (corrected in the ruling commit), and `CLAUDE.md`'s *"and on nothing else"* (literal **F**, which preserves the docs-only-PR property this spec relies on) |
| **C3 — `plugins/kodhama/README.md:22` singular** | Literal **H**. Ships to consumers, blocked S13's third clause, and was already out of step with `keyless_admission_check.py`. Flagged in v1's F2 and left standing by v2 |
| **C4 — the prose claimed literal A cites `kodhama-0025`; it does not** | Resolved by keeping the citation in the spec and saying so: the block is repository-facing prose, and S13/S14 compare it byte-for-byte, so any citation not in the pinned text is a mismatch an executor would have to invent |
| **C5 — "while their home is decided" asserts an undecided home for `setup-ci-marketplace`** | Scoped to the issue skill in **B**, **C**, **D** and **E**; `kodhama-0020` fixed the CI skill's directory and namespace, and is now a declared dependency |
| **C6 — nothing in the package disclosed the actuator** | One bullet in **B**, plus a paragraph in §Why the actuator sits outside `skills/` distinguishing context safety from consumer disclosure. Free under R8, which scopes enumeration to contents |
| **Take 7 — S9's arbiter was a denylist named allowlist** | Closed `gh` multiset of seven heads over nine occurrences, plus the three exact literals, plus the denylist retained for the same-head substitution case. Mutation obligation names all four survivors |
| **Take 8 — a test asserting a state Lane A will delete** | S10's positive half dropped; R12 rests on the negatives plus S1 |
| **Take 9 — S15 needed an absent YAML parser** | Regex extraction specified; `tests/TEST_DEPS.md` identified as an artifact-dependency file, not a package manifest |
| Rulings absent from the ledger | Both recorded in `conductor/wave-issue-taxonomy.md` Lane B, which also fixes carrier 7 |
| Erratum inherited from a reviewer's own note | *"R1's coverage was a strict subset of R1"* corrected to **S1's** in both places |
| Bookkeeping the same class defect would have missed | R18: `tests/TEST_DEPS.md` must declare this spec, since its own text says its tests derive from what it lists |
| Advisory — *"It teaches and carries nothing"* parsed as "teaches nothing" | Split into *"It only teaches"* plus a separate sentence |
| Advisory — "asserts no purpose of its own" overshot `kodhama-0020` | Narrowed to *"What this plugin is **for** has never been decided"*, which cites 0020 rather than contradicting it |

### What v4 changed, and why

| Finding | Repair |
|---|---|
| **D1 — S9's pinned table did not match S9's extractor.** The optional second group is greedy, so line 68's prose yields `gh token lacks`, not `gh token`. S9 would have gone **red on a correct package** | Table cell corrected; the prose note now quotes the head the extractor actually produces, and instructs anyone changing the extractor to **re-derive the table from it** rather than reconciling the two by eye. The other eight heads were exact. This is F3 inverted, and worse than F3: a check that fails when it should pass teaches its reader to override it |
| **D2 — literal F would have pinned an already-false clause.** *"a docs-only PR gets no check at all"* is stale today, not stale-by-this-publication | **Verified here, not taken on report:** `agent-workflow-parity.yml` and `claude-code-review.yml` both declare a bare `pull_request:` trigger with no `paths:` key; only `validate-marketplace-setup.yml` is filtered. **F** now states the narrower true property — *the test gate* (suite, validator, two `npm install`s, admission check) does not run on a prose edit — and names the two unfiltered workflows. The same narrowing applied to §Closing the CI blind spot, the S14 disclosure, carrier 8, and ruling 2 in the ledger. The ruling itself is untouched: it was always about cost |
| **D3 — the generating rule reached into the append-only corpus** | The rule requires **both** an enumeration *and* a description of present state; ratified decisions are excluded. v3's R15 was a `shall` no executor could discharge, and S13 passed only because the discovery command never searched `decisions/`. *(This row is v4's account. v5 replaced its `kodhama-0018` justification with `kodhama-0017` — see the v5 table — and v6 corrects its closing clause, which said "the line is the intent act, not the file": that rule is repudiated in §Standing scope claims, where the binding event is **the merge that delivers the record**. The row is left rather than rewritten because it is history; the correction is here so no reader takes it as current.)* |
| **D4 — the ledger's authorisation undercounted, in the round about undercounting** | Lane B said *"three further carriers"* and listed three; there are four. `plugins/kodhama/README.md:22` — literal **H**'s target — was authorised nowhere. Corrected in the ledger |
| **D5 — R18 did not say whether to pin** | Pinned `id@vN` form required, at the version the tests were written against; `specs/README.md` requires it for versioned spec dependencies and the file already pins its sibling `@v5` |
| **D6 — R16's arbiter walked files, not directories** | `if d.is_dir()` added; a stray `.DS_Store` beside the skill directories would have failed a correct package |
| Conformance advisories | §Package changes gained the two rows it omitted — `tests/test_kodhama_plugin.py` and `conductor/wave-issue-taxonomy/README.md`, both already named in the criteria table. The v3 CONFIDENCE line claimed S9 *"was checked against all nine occurrences"*; it now says what was done — the surface was read and classified by hand, the extractor was **not** run, which is exactly how D1 got through |
| Upstream corrected pre-merge | §What the plugin is for records `fcb7779`, so a later reader knows the spec/record agreement was made rather than inherited |

### What v5 changed, and why

Each finding gets its own row. The S13/S10 collision reached v4 because a
routing label folded two distinct findings under one name and only one was
answered; a row per finding is the cheap guard against that.

| Finding | Repair |
|---|---|
| **S13 and S10 demanded opposite states of one path.** S13 asserted `conductor/wave-issue-taxonomy/plugin/DIRECTION.md` carries literal **G**; S10 and R12 require that path to be gone. Both are post-publication assertions, so a deleted file was required to carry a literal | S13 repointed at `plugins/kodhama/DIRECTION.md`; R15 gained *"each verified at its post-publication path"*; carrier 6's row now reads *edited here, verified at the published path*. **The rest of the spec was already right** — §What ships, S1 and the arbiter row all name the plugin root — which is why this survived four rounds: it was one clause out of step with its own document. An executor building v4 literally would have shipped a **red test against a correct package**, which is D1 one criterion over |
| **The append-only exclusion was justified on the wrong record.** v4 cited `kodhama-0018` §1, already inaccurate for reasons predating this work, so the exclusion looked free | It is not free. `kodhama-0017:33` (*"retains **only** a narrow future distribution goal"*) and `:208` (AC3, *"**describes only** host-native catalogs, the future marketplace-tested metadata, and the future generic CI setup skill"*) are the clauses literal **A** renders. AC3 is **accurate today and falsified by this publication** — a third distributed thing, and a fourth in the actuator. `kodhama-0025:142` explicitly leaves it standing: *"amended, not superseded. Its retained goal survives."* Now cited in prose, declared in `depends_on`, and parked as open question 6 |
| **The exclusion removed a class from the edit obligation and put nothing in its place** | Open question 6 names the corpus's own remedy — the forward pointer, which `kodhama-0017` already carries two of. Parked rather than done: a forward pointer on an approved record is an act on the corpus, not a delivery step, and this spec covers publication only. OQ4 is the precedent |
| **The discovery instrument could not see its hardest case.** Run against `specs/` and `decisions/`, v4's pattern returned **zero** hits on `kodhama-0017`: `retains only`, `describes only` and `retained goal` matched none of the five alternatives | Three alternatives and two paths added. **And the gap is now stated rather than papered over**: the rule is semantic, the command is a regex, and no regex over a semantic rule can be complete — a clean run is evidence, not proof. Hits under `decisions/` are marked **forward-pointer candidates, not edit obligations**. This was the v3 defect one level up: the instrument had become the incomplete enumeration |
| Advisory — false positives being re-adjudicated each round | Three recorded in a table: `DIRECTION.md:55` (a *future* shape of the skill), `kodhama-0018:130` (a retired artifact, and excluded anyway), `kodhama-0017:228` (the record's own self-check) |

**Errata folded into v5, from the spec-adversary's round-5 gate — which
returned APPROVE-READY on v4.** These are recorded as errata rather than
findings, and the distinction is the gate's own: none of the three makes an
arbiter decide wrongly, pins a falsehood into a shipped file, or leaves a
`shall` undischargeable. Those are the three tests that produced
NEEDS-REVISION in earlier rounds, and none is met here.

| Erratum | Repair |
|---|---|
| **The binding event was named wrong in one of three places.** *"had not yet merged **into `kodhama/kodhama`**"* put the boundary at the Lane A relocation, which would leave `kodhama-0026` editable after #64 merges | Corrected to the merge of the PR carrying the status flip. **I went one clause further than the erratum asked:** the same passage also said *"the distinction is the intent act"*, which the correction it was explaining contradicts — `kodhama-0026` already carried `status: approved` when `fcb7779` corrected it. Both now point at the merge, with `kodhama-0008`'s *"the #35 merge performs the delivery"* and `fcb7779`'s own commit message as the evidence. Two other statements of the rule were already unqualified and correct |
| **The `tests/test_kodhama_plugin.py` row said "eleven `new:` tests"; there are fourteen** distinct `new: test_*` in the criteria table | Corrected, and the row now says the criteria table is the authority and this is a summary of it. **This was D4's own defect — an undercount — sitting inside one of the two rows v4 added to fix D4.** Harmless in practice, since an executor follows the complete table |
| **"eight statements across seven files"; it is six.** `CLAUDE.md` carries rows 2 and 8, `plugins/kodhama/README.md` carries rows 4 and 5 | Corrected in both places the count appears. The statement count was right |
| Non-blocking note — D6's rationale applied verbatim to S1's unguarded arbiter | `p.name != ".DS_Store"` added to S1. One line, no restructuring |

### What v6 changed, and why

Labels are the round-7 reviewer's, kept verbatim. One row each.

| Label | Repair |
|---|---|
| **B1** — the spec asserted a clause was *"already false"* that the corpus says survives, and contradicted itself doing it | **The corpus is right and this spec was wrong.** `kodhama-0017:15-18` (the pointer `kodhama-0025` itself wrote): the goal *"survives, but its schema-shaped implementation retires"*. `kodhama-0025:142`: *"amended, not superseded. Its retained goal survives"* — **the line this spec quotes elsewhere for the opposite proposition**. `kodhama-0017:119-121`: §2 *"authorizes the goal, not a schema"*, so no artifact existed to retire. `specs/README.md:34-36`, standing above the paragraph v5 added: met *"by the GitHub Actions run log rather than a schema"*. §Why the marketplace-metadata item leaves the block is restated on the reviewer's ground — **0025 redirected the goal to the run log, and a run log is not a distributed artifact**, so the item leaves a block about distributed contents without any falsity claim. Same outcome, no contradiction |
| **B1** (second half) — the parked debt was understated | Literal **A** does not only add; it also **removes** the retained-goal description AC3 names. Open question 6 now records both directions |
| **B1** (second-order) — the rule used the past-act reading for the exclusion and the present-state reading for the debt | **Decided: AC3 is a past-act record and therefore *not* a carrier.** No edit is owed and the exclusion is not a loophole. The debt is re-typed as a **disclosure** debt rather than a conformance failure — a frozen record and a current document are each correct as their own kind of artifact; what is missing is a pointer at the record. Stated at the rule, where the ambiguity was |
| **M1** — the repudiated rule still asserted in present tense | The v4 change-table row's closing clause (*"the line is the intent act, not the file"*) is corrected in place, with a note that the row is history and §Standing scope claims is current. Its stale `kodhama-0018` justification is pointed at the v5 replacement. The v5 errata row said *"two other statements … were already correct"*; there are **three** others, and this was the fourth |
| **M1** (support) — the rule was better supported than shown, and one datum cuts against it | `decisions/0002:36` added — *"preserved **as merged**"*. And the tension is named rather than hidden: **`CLAUDE.md:42` says *"never edit a **ratified** decision"*** *(v6's line number, wrong; the sentence is at `:44` — see F3)*, which read literally would forbid `fcb7779`. Reconciled as loose usage, noted, and deliberately not fixed — that line is not a carrier and tightening governance prose is not this publication's job |
| **M2** — the rubric was not re-walked against the dependency v5 added | `depends_on` carries **seven** ids. The two "five" bullets are replaced: five constraints the spec must not break, plus **one it diverges from**. The frontmatter bullet now documents 0017's v5 addition, which was its job that round. **And the edge is re-typed:** calling 0017 a constraint *"this spec must not break"* was false while open question 6 records that it does — it is a drift-bearing input, disclosed rather than satisfied |
| **M3** — parking OQ6 against a precedent never surfaced | Open question 6 now names the standing practice and that this parks against it: `kodhama-0025` wrote `0017:15-18`, `-0003` wrote `0002:33`, `-0006` wrote `0002:41`, and `0025:151-153` budgets for exactly this. It also states that the `depends_on` edge **neither satisfies nor evades** — it leaves no trace where a reader of 0017 would find it. The reason for parking is given as a real distinction (every precedent is a *decision* annotating a decision; this is a spec) and explicitly left as the maintainer's call, since writing the pointer unilaterally would settle it by doing |
| **m1** — R15 said all eight carriers *shall* carry literals; carrier 7 carries none | Scoped to the **seven literal-bearing** carriers; carrier 7 is discharged by its ledger correction, which S13 already asserted correctly |
| **m2** — one arbiter row still said *"**G** in `DIRECTION.md`"* unqualified | Qualified to `plugins/kodhama/DIRECTION.md`. Last unnamed site of the v5 repair |
| **m3** — the false-positive table covered three of ~eight non-carrier hits | **Four** rows added: `decisions/0017:16`, `CLAUDE.md:8`/`README.md:5`, `specs/0004:86`, and `conductor/wave-issue-taxonomy.md:99/104/105`. Leaving the rest uncovered imposed exactly the re-adjudication cost the table exists to remove. *(v7: this row said "Five rows added" and listed four, while the table's own note said "the last four rows plus `0017:16`" — which is one of the four. Rows and hits were being counted interchangeably.)* |
| **m4** — `specs/README.md` cited *"`kodhama-0017` §33"* | Corrected to line 33, with §2 named as the amended section. That paragraph also now states the divergence in both directions and calls the debt a disclosure debt |

### What v7 changed, and why

Labels are the round-8 reviewer's, kept verbatim.

| Label | Repair |
|---|---|
| **F1** — the v6 re-typing was stated at the rule and nowhere else | Three older passages still carried the retired framing, forty and a thousand lines from the ruling. `§Standing scope claims` no longer says publication leaves the scope document *"out of conformance with an approved decision"* — it says the two artifacts describe different contents, that each is correct as its own kind, and that the gap is one of **disclosure**. The Rubric check's *"one conformance debt this publication creates"* is likewise re-typed. **v6's own change table claimed the fix was "stated at the rule, where the ambiguity was" — which is exactly what happened, and exactly the defect**: a ruling landed in one place and its dependants were not re-walked, which is the failure mode this wave has hit in four separate rounds |
| **F1** (fourth site) — the in-section divergence statement gave one direction | `§Standing scope claims` said AC3 *"becomes inaccurate … a third distributed thing, and a fourth in the actuator"*. It now states **both** directions as a list — added: the skill and the actuator; removed: the marketplace-metadata description — matching the ruling 25 lines above it and open question 6 |
| **F2** — a v6-added false-positive row described text that is not at the lines it cites | `conductor/wave-issue-taxonomy.md:99/:104/:105` are **Lane B ruling text quoting the carriers themselves** (`:99` carrier 4, `:104` carrier 8, `:105` carrier 5), not *"Lane C/D scope text about which repositories receive receipts"* — Lane C starts at `:121` and returns no hits. The disposition was right and the reason was wrong, **and the wrong reason would not have excluded them anyway**, since carrier 7 proves Lane B text can be a carrier. Real reason given: they are the authorisation naming what to repair |
| **F3** — `CLAUDE.md:42` cited for a sentence at `:44` | Corrected. Line 42 is the bullet head. Noted in place that v6's CONFIDENCE line did not list `CLAUDE.md` among what was re-read, so the slip fell outside the verified set — the confidence claim was accurate, which is the argument for keeping such lists honest rather than generous |
| **F3** (follow-on) — whether naming the `CLAUDE.md` tension suffices | Left as-is per the reviewer, since line 44 fails carrier condition 1 and R15 does not reach it. **One clause added**: this publication edits `CLAUDE.md` twice, so declining to tighten a third sentence there is a **scope choice, not a limit** — the two edits are obligations the rule generates; rewriting a governance rule is a different act needing its own authority |
| Uncited primary source | `decisions/0025:113` now cited directly — *"That goal is met by the GitHub Actions run log, which records the checkout revision with better provenance than a checked-in file."* v6 routed the claim through `specs/README.md:34-36`, a derived restatement of it. The approved record says it itself |
| Accounting wobble | The false-positive table's note said *"the last four rows plus `0017:16`"* — which is one of the four — while its change-table row said *"Five rows added"* and listed four. **Four rows** in both places; the table now covers every non-carrier hit the widened command returns *(v8: that last clause was false and is withdrawn — see the v8 table)* |

**Corpus support the reviewer supplied and v7 records.**
`decisions/0025:139-140` calls that record's own acceptance criteria *"false
**when written**"* — the corpus indexing AC truth to the moment of writing,
which is the past-act ruling in §Standing scope claims stated by an approved
decision rather than inferred here. It was not cited when the ruling was made.

### What v8 changed, and why

| Finding | Repair |
|---|---|
| **Blocking — a false completeness claim about the discovery command's output.** The table and the v7 change table both said it covered *"every non-carrier hit the widened command returns"*. It returns roughly two dozen hits outside this spec; **eight are untabled** | The claim is withdrawn, not satisfied by padding. The table is now described as what it is — **the hits a reviewer would otherwise re-adjudicate** — with the untabled residue named, including that `decisions/0017:33` and `:208` are its two most consequential hits and are adjudicated in prose and open question 6 rather than in a row. The command's hits on **this spec and the records it quotes** are disclosed as **self-reference by construction**: a document that discusses scope enumerations contains the phrases that find them. **This was false enumeration one level up again** — the class §Standing scope claims exists to kill, asserted about the instrument, and flatly contradicting this spec's own *"a clean run is evidence, not proof"* |
| **`specs/0004:141` looked like a ninth carrier and is not** | Tabled with the real reason, which is narrower than the one first reached: **the line wraps**, and `:141-142` reads *"the plugin's declared skill **directories**"* — already plural. The regex matches `declared skill\b` across the break. **Round 5's spec-adversary adjudicated this line for this reason, and an implementation planner adjudicated it again on v7.** Twice, by two agents, because it was absent from the table — which is the exact cost the table exists to remove, so the row earns its place on that alone |
| **Literal H was pinned by a line number that its own sibling edit invalidates** | Re-anchored to a **string** at all four sites — the literal's own heading, carrier 5's row, S13, and the §Package changes row. **B** replaces 9 lines with 26 in the same file in the same change, displacing H's target from line 22 to **39**; an executor reading `readme.splitlines()[21]` asserts against the wrong line and ships **a red test against a correct package**. That is D1's class, and the wave's failure mode in miniature: **a dependant thirty lines below its own edit, in the same file**. The replacement text is unchanged; only its locator is |

### What v9 changed, and why

| Finding | Repair |
|---|---|
| **HIGH — the actuator's safety promise shipped unguarded through eight review rounds.** Dry-run-by-default is pinned **six times as prose** — literal **A** in three files, the shipped README twice, both catalog descriptions — and **zero times as behaviour**. The one test touching it asserted `assertIn("Dry-run by default", stdout)`, pinning the help text's claim rather than the default. Mutating `APPLY=0` → `APPLY=1` in the shipped script — apply-by-default against a live org with `admin:org` — passed the full gate: **27 tests OK, validator green.** Three more mutations survive | **S17 and R19**, behavioural. The script is run against a stub `gh` on `PATH` and its call log inspected for three properties: no write call on a default invocation, `--apply` as the only path that sets `APPLY=1`, and the empty-backlog skip holding without `--force`. The four measured survivors are named as the mutation obligation. **A static pin on `APPLY=0` was rejected** — it catches two of the four and misses `if true` entirely, which is the one that converts every `run()` into an execution while the default still *reads* as `0`. The third property exists because the empty-backlog mutation breaks neither write-call property, and naming a mutation this criterion could not discharge would be the defect S9 and D1 were both about |
| **How it survived, stated plainly** | Every round tested the *literals* that assert the property and none tested the property. Sixteen scenarios and eighteen requirements, and R11's *"shall change nothing without `--apply`"* had **no arbiter that could fail** — S4 asked only for path, `X_OK`, `bash -n`, `--help` exit 0, `--bogus` exit 2, and the implementation matched S4 exactly. **The build was faithful; the contract was the gap.** Pinning a claim in six places creates the appearance of a guarded property, which is why it went eight rounds unexamined |
| **m1 — the S5/R3 arbiter row over-claimed** | §Why the actuator sits outside `skills/` asserts *"S5 and R3 fail if they do"*. Conformance measured it: with the executor's addition stripped, moving the actuator into `skills/issues/` left the named test **green** — four other tests caught the move, so protection held in effect, but the named arbiter did not. The executor's `*.sh` assertion is recorded in the row as inside the contract, since it makes a sentence the spec asserts about itself true and cannot false-red. **And corrected while recording it:** match `path.suffix == ".sh"`, not the exact filename, or `skills/issues/seed.sh` walks through — the same technique `test_the_migration_mapping_stays_out_of_the_package` argues for forty lines away |
| **m2 — a false-positive row cited a path R12 deletes** | `conductor/wave-issue-taxonomy/plugin/DIRECTION.md:55` → `plugins/kodhama/DIRECTION.md:58`. **Same displacement class as literal H**: a citation into a file the change relocates |
| **m3 — the ledger is the ledger and no implementation commit touched it** | Lane B's publication item now records the build, the conformance PASS, the HIGH and its closure, and states it **ticks at merge, not before** — nothing is published until #64 lands, and the tick is publication, never enablement. Lane B's pointer at the staging `DIRECTION.md` now names both the staged and published paths |
| Accounting, corrected rather than repeated | Against a fully pre-change tree, **four** criteria were vacuous (S7, S14, S6, S5/R3), and this spec carried **two** explicit mutation obligations (S7, S9 — S9 was never vacuous; it errors on the missing file). v9 adds a third, on S17. All are mutation-proven guarded |

Result at v9: **PASS**, holding at `gated`. *(Superseded by events: the
maintainer's intent act of 2026-07-31 flipped this spec to `approved`, and the
frontmatter records it. Left as the v9 rubric's own finding rather than
rewritten — but it is not current state, and v10 flipped the `specs/README.md`
index row while leaving this sentence asserting the opposite.)*

This is a change-scoped self-check only. It does not claim the malformed legacy
decision metadata tracked by [issue #20](https://github.com/kodhama/stewards/issues/20)
has been repaired, or that the full corpus passes strict validation.
