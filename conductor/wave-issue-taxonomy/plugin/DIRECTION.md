# Direction — where this skill is going

Not a decision and not a plan. Maintainer direction recorded 2026-07-31 so the
reasoning survives the wave that produced it. Nothing here is ratified; nothing
here authorises work.

## What this artifact actually is

**A GitHub backlog adapter.** It is not a grove concern, and the reasoning is
grove's own shape rather than a preference:

- grove's adapter axis is `claude` / `codex` — **hosts, not trackers**. A
  GitHub adapter would be a new axis, not an existing slot.
- **None of grove's thirteen roles is a product owner.** The consumer this
  skill is written for does not exist yet.
- **Two of grove's fourteen charters mention GitHub.** Grove is not
  conceptually tied to it, and is less tied still to backlog management. Its
  loose GitHub coupling is prose drift, not design.

Putting this in grove today would invent a tracker axis for an absent role and
deepen a coupling grove has mostly avoided.

## The home, in three steps — the middle one is skippable

1. **Now — the `kodhama` plugin in Stewards, as a staging area.** This is a
   parking spot and is meant to be one. **What the `kodhama` plugin is for
   remains undecided**, and putting this skill there defers that question
   rather than answering it. The alternative was minting a name and a home for
   something whose shape is still moving, which costs more than it buys today.
   *(An observation, not a ruling: that plugin currently carries a GitHub
   Actions skill and would now carry a GitHub issues skill. If the question
   ever gets taken up, "how the family operates on GitHub" is one available
   reading of it. Nobody has decided that.)*
2. **Later — its own plugin**, potentially still hosted in Stewards. The
   trigger is whenever the `kodhama` plugin's own purpose gets decided: this
   skill either fits that purpose and stays, or does not and moves. Skippable
   if step 3's trigger arrives first.
3. **Later still — its own repository**, on the `git-subdir` pattern grove,
   trellis and wisp use. The trigger is non-kodhama consumers or a release
   cadence of its own.

Step 2 may be skipped entirely. Do not create a repository to hold one skill
and one script.

**Nothing about this sequence claims the `kodhama` plugin's scope.** Its
declared distribution scope stays narrow until someone decides otherwise; a
staged skill sitting in it is a deferral, not an amendment.

## The split that is coming

Today this skill carries **both** the abstract backlog concepts and their
GitHub encoding. Eventually a product-owner or backlog-manager role — plausibly
a grove role — owns the abstract half: what kinds of work exist, how to
decompose an epic, why commitment level is not a kind. This skill then becomes
**thin**: the mapping from concept to surface, and nothing else.

Once that holds, other adapters swap in for other backlog surfaces — Linear,
Jira, a tracker that is not GitHub — against the same abstract role.

**The seam is already half-cut, and it is worth knowing which half.**

| concept | state today |
|---|---|
| **Story** | **Already adapter-shaped.** It appears only as a reading of the encoding — *"a `Feature` at `facing: user` is what agile calls a Story"*. Concept and encoding are already distinct words. Lifts out cleanly |
| **Epic** | **Not separated.** The word is both the abstract container *and* the literal GitHub type name. Extraction requires splitting them first — the concept "a coherent set of independently-deliverable children" from the type spelled `Epic` |
| **Enabler** | Adapter-shaped, same as Story — a reading of `facing: system` |
| `stage:`, `priority:`, status | Encoding only. Stay here |
| §3 type-vs-stage, §5 no-`Idea`-type, §5a no-`Story`-type | **Abstract reasoning.** This is what moves to the role |

*Rule of thumb for the eventual extraction:* if a passage would still be true
on Linear, it belongs to the role. If it names a `gh` flag, a GitHub type or a
label, it belongs here.

## What this direction does not settle

- Whether grove ever grows that role. It has no product-owner role today and
  no tracker axis; both would be its own decisions.
- Whether the abstract half becomes a grove role, a separate skill, or stays
  written down nowhere until someone needs it.
- Whether `kodhama-0026` should name any of this. It should not — a decision
  records what was decided, and this is direction.
