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

**2. `specs/` is deleted** — 6 files, 6,153 lines. All five specs were already
`superseded`; `specs/README.md` said in its own first line that none was an
implementation input.

**3. `.grove/lifecycle.md` is deleted, and the enum it carried moves to one
line in `CLAUDE.md`:** `draft → gated → approved → superseded`, with
**`approved` requiring a recorded human intent act**. That clause is the only
part anything here consumes — every `status:` line in `decisions/` quotes the
act that set it — and it survives at full strength. The other 89 lines
described roles this repository does not run (`contract-author`,
`spec-adversary`, `executor`) against a `specs/` directory that D2 removes.

**4. Git history is the archive.** Nothing is lost; it stops occupying the
working tree. `git log --diff-filter=D` finds every deleted path, and every
file is recoverable at its last commit.

**5. Ratified decisions keep their now-dangling references, unedited.** Nine
records point at something this change removes: **three** name a
`kodhama-spec-NNNN` (`kodhama-0017`, `-0020`, `-0025`) and **six** cite the
lifecycle charter's path (`kodhama-0013`, `-0027`, `-0028`, `-0029`, `-0030`,
`-0031`). **Those pointers are not repaired**, because repairing them means
editing ratified text, which `kodhama-0004` forbids and which is a worse defect
than a stale path. They resolve through git history.

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

**The protected material was 63% of the repository and served nothing.** 10,774
of 16,964 lines, none of it read as current state by construction: briefs were
archive by `kodhama-0027` D5, specs were historical by their own index. A
reader could not act on any of it, and an agent had to read past it to find
what was live.

**The ratio was the problem named a week earlier and never fixed.**
`kodhama-0030` is 224 lines governing a catalog with one entry. Adding a
protected 10,774-line archive around it is the same failure at directory scale.

## Cost, stated

**1. Nine ratified decisions now name paths not in the tree**, enumerated in
D5. The `kodhama-spec-0004@v5` and `kodhama-spec-0005@v13` edges in
`tests/TEST_DEPS.md` are repaired because that file is not ratified; the ones
inside `decisions/` are not, per D5. **A reader following one gets a 404 in the
working tree and must reach for `git log`.** This is the price of D5's refusal
to edit ratified text, and it is the right trade only because git preserves the
target.

**2. The conductor seat is now a name with no directory.** `CLAUDE.md` and
`README.md` both listed it as one of the hub's three long-standing jobs. It is
removed from both. If a brief is ever wanted again, `kodhama-0027` D2–D4 still
describe its shape — but nothing in the tree points at them.

**3. This repository can no longer state its own artifact lifecycle in full.**
D3 keeps the enum and the human-act rule; it drops the per-state guidance on
who moves an artifact between states and what each state means for a role.
Those were written for a grove-run corpus with specs and executors. **If this
repository ever runs that model again, the charter is reinstalled, not
rewritten from memory.**

**4. `kodhama-0004-uniform-lifecycle` now has no local carrier.** It is the
decision the deleted charter implemented. It keeps `status: approved` and is
not retracted; what it mandates simply is not described anywhere in this tree
beyond D3's one line.

## Consequences

`kodhama-0027` keeps `status: approved` with D1 superseded by `kodhama-0031`
and D5's second sentence superseded here; D2–D4 live. Annotated by forward
pointer, per `kodhama-0004` and this repository's rule that a ratified decision
is never edited.

`.grove/relations.md` and `.grove/versioning.md` stay. Both open with *"This
file is not an agent role. Like `lifecycle.md` …"* — that cross-reference now
names a deleted file and is left as written, since both are grove-managed and
this repository does not author them.

The repository is **47 files and 6,296 lines** after this, from 76 and 16,964
— 10,831 deletions across 30 changed paths.
