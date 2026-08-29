---
id: kodhama-0032-the-hub-keeps-only-decisions
type: decision
status: approved  # maintainer intent act 2026-08-29, in session: "Remove conductor and specs as well as well as .grove/lifecycle.md. Other that or I will hard delete and potentially leave an uncoherent state for you to fix later" — reaffirmed after the two blocking rules were quoted to them. An in-PR flip recording that act; the merge performs the ship. The agent did not open the gate.
depends_on: [kodhama-0027, kodhama-0030-install-door-serves-trellis-only, kodhama-0031-work-leaves-github-issues]
owner: agent
updated: 2026-08-29
provenance: "maintainer direction, 2026-08-29, given after being shown that kodhama-0027 D5 forbids deleting briefs and that .grove/lifecycle.md forbids editing superseded content away. Both were quoted; the direction was repeated with the alternative named as an unassisted hard delete."
---

# 0032 — the hub keeps decisions and the door, and stops keeping the rest

## Decision

**1. `conductor/` is deleted** — 23 files, 4,621 lines, every one archive since
2026-08-02.

**2. `specs/` is deleted** — 6 files, 6,117 lines, measured at `db9a73b`. All
five specs carried `status: superseded` before this change — 0001–0003 long
since, 0004 and 0005 as of `kodhama-0030` — and `specs/README.md` said in its
own first line that none was an implementation input.

**3. `.grove/lifecycle.md` is deleted, and nothing here replaces it.**
`CLAUDE.md` keeps one line naming the enum — `draft → gated → approved →
superseded` — **as a pointer to `kodhama-0004`, whose uniform enum `kodhama-0008`
D1 left standing**, not as a local restatement of grove's charter.

**The approval mechanic is not restated, and that is a rule, not an
oversight.** `kodhama-0008` D2: *"No kodhama-meta artifact defines how the
approval act is performed or recorded — this decision included."* D4: the
operating model is *"never hand-authored per repo."* A draft of this record put
the mechanic into `CLAUDE.md` — *"`approved` requires a recorded human intent
act"* — **re-creating two distinct clauses of `kodhama-0004` that `kodhama-0008`
D1 superseded separately**: the mechanic itself (0004's third Decision bullet,
*"`approved` = human PR merge … a post-merge bump commit records the act"*,
retired because no approval mechanic is defined at the meta layer) and AC1
(*"All five family repos' `.trellis/profile.md` carry the same
lifecycle-mapping section"*, retired because *"every hand-authored copy went
stale"*). One draft line, both failure modes. **Deleting the installed charter
is not a licence to hand-copy it**; caught in review before ratification.

The charter's other 89 lines described roles this repository does not run
(`contract-author`, `spec-adversary`, `executor`) against a `specs/` directory
that D2 removes.

**4. Git history is the archive.** Nothing is lost; it stops occupying the
working tree. `git log --diff-filter=D` finds every deleted path, and every
file is recoverable at its last commit.

**5. Ratified decisions keep their now-dangling references, unedited.** **Six**
records point at something this change removes: **three** name a
`kodhama-spec-NNNN` (`kodhama-0017`, `-0020`, `-0025`) and **three** cite the
local charter path `.grove/lifecycle.md` (`kodhama-0029`, `-0030`, `-0031`).
**Those pointers are not repaired**, because repairing them means editing
ratified text, which `kodhama-0004` forbids and which is a worse defect than a
stale path. They resolve through git history.

**Four further records cite grove's canonical charter** (`kodhama-0008`,
`-0013`, `-0027`, `-0028`) — **the copy in the grove repository, which this
change does not touch.** Those do not dangle, and counting them as casualties
would have inflated the six real ones to ten — an overstatement by two-thirds.
(The draft that said "by half" was arithmetic carried over from the earlier
three-record version and not re-derived when the fourth was found; 6→9 is a
half, 6→10 is two-thirds.) The distinction matters beyond
arithmetic: it is the evidence for the supersession clause above, that
declining the charter locally leaves grove's corpus intact.

**Counting them took three passes, because the corpus spells that reference
three ways**: `.grove/lifecycle.md` (local), `grove/charters/lifecycle.md`
(qualified), and bare `charters/lifecycle.md` — `kodhama-0008` uses the last,
and an exact-string search for the qualified form missed it. `kodhama-0029` C5
already recorded this: *"The corpus runs three grammars at once."* It is still
true, it is still unfixed, and it is now demonstrated to cause miscounts. **Any
future sweep over these references must match the shape, not the spelling.**

## What this supersedes

**`kodhama-0027` D5**, verbatim: *"Existing briefs become archive, not debt.
They are **not migrated or deleted.**"* The second sentence is superseded; they
are deleted. **D2, D3 and D4 stand and are now vacuous** — they govern what a
conductor brief may contain, and there are no briefs. They are not retracted:
if the seat is ever re-occupied, they still say what a brief may hold.

**`.grove/lifecycle.md`'s terminal clause**, verbatim: *"`superseded` —
retired. … the original content is **never edited away**. Terminal."* Deleting
the five superseded specs is the strongest possible form of editing away. That
charter is grove-installed and grove is retired here (`kodhama-0030`), so this
record does not amend grove's canonical copy — it removes this repository's
installed copy and declines its rule locally. **Grove's own corpus is
unaffected.**

## Why

The maintainer's direction is the reason, given twice, the second time against
a quoted statement of both rules and with the alternative named: an unassisted
hard delete leaving the tree incoherent. Doing it deliberately is strictly
better than that, and the disagreement was about *whether the rules should
bind*, which is the maintainer's call, not a factual dispute.

Two things make it more than a preference.

**The protected material was 63% of the repository and served nothing.** 10,738
of 16,911 lines (conductor 4,621 + specs 6,117), none of it read as current
state by construction: briefs were
archive by `kodhama-0027` D5, specs were historical by their own index. A
reader could not act on any of it, and an agent had to read past it to find
what was live.

**The ratio was the problem named a week earlier and never fixed.**
`kodhama-0030` is 224 lines governing a catalog with one entry. Adding a
protected 10,738-line archive around it is the same failure at directory scale.

## Cost, stated

**1. Six ratified decisions now name paths not in the tree**, enumerated in
D5 — not nine; three apparent casualties cite grove's canonical charter, which
survives. The `kodhama-spec-0004@v5` and `kodhama-spec-0005@v13` edges in
`tests/TEST_DEPS.md` are repaired because that file is not ratified; the ones
inside `decisions/` are not, per D5. **A reader following one gets a 404 in the
working tree and must reach for `git log`.** This is the price of D5's refusal
to edit ratified text, and it is the right trade only because git preserves the
target.

**2. The conductor seat is now a name with no directory.** `CLAUDE.md` and
`README.md` both listed it as one of the hub's three long-standing jobs. It is
removed from both. If a brief is ever wanted again, `kodhama-0027` D2–D4 still
describe its shape — but nothing in the tree points at them.

**3. This repository can no longer state its own artifact lifecycle at all.**
D3 keeps a pointer to the enum and nothing else — no per-state meaning, no
mover rules, and by `kodhama-0008` D2 no approval mechanic. Every `status:`
line in `decisions/` quotes the act that set it, so the practice is legible
from the corpus; **the rule behind the practice is now stated nowhere in this
tree.** That is the intended end state, not a gap to fill: `kodhama-0008` D4
puts it in the plugin, and **if this repository runs that model again the
charter is reinstalled, never rewritten from memory.**

**4. `kodhama-0004-uniform-lifecycle` now has no local carrier.** It is the
decision the deleted charter implemented. It keeps `status: approved` and is
not retracted; what it mandates simply is not described anywhere in this tree
beyond D3's one line.

## Consequences

`kodhama-0027` keeps `status: approved` with D1 superseded by `kodhama-0031`
and D5's second sentence superseded here; D2–D4 live. Annotated by forward
pointer, per `kodhama-0004` and this repository's rule that a ratified decision
is never edited.

`research/family-audit-2026-07.md` keeps its text and gains a staleness header.
It is a dated snapshot that links to `conductor/` and reasons about `specs/`;
notably it predicted this change — *"Deletion needs a rule change, not a
cleanup"* — which is what `kodhama-0032` is. Rewriting a dated audit to match a
later tree would destroy the thing that makes it evidence.

`.grove/relations.md` and `.grove/versioning.md` stay. Both open with *"This
file is not an agent role. Like `lifecycle.md` …"* — that cross-reference now
names a deleted file and is left as written, since both are grove-managed and
this repository does not author them.

**The repository goes from 75 tracked files to 46** — 30 removed, one added
(this record). What is removed, measured at `db9a73b`: `conductor/` 23 files /
4,621 lines, `specs/` 6 files / 6,117 lines, `.grove/lifecycle.md` 93 lines —
**10,831 lines of deleted files.** Two instruments, named because this
paragraph is about not mixing them: **file counts** are `git ls-tree -r <rev>`,
which lists tracked paths only — a `find` over the working tree reports one
more, since `tests/__pycache__/` exists there and is gitignored — and **line
counts** are `git show <rev>:<path> | wc -l` over those paths, which reads blob
contents and is a different question `ls-tree` cannot answer.

Those figures are stable because they describe content that no longer changes.
**A post-change line total is deliberately not stated**: this record is part of
the tree it would be counting, so every edit to it falsifies its own number.
Five drafts of this paragraph carried a precise figure and four were wrong when
read — once because a sibling PR moved the baseline, twice because editing this
file moved it, and once because the before-count used `git archive` while the
after-count used `find`, so the two halves of one comparison were taken with
different instruments. `git diff --shortstat` is
the answer to that question, and it is always current.
