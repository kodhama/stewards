---
id: kodhama-0030-install-door-serves-trellis-only
type: decision
status: approved  # maintainer intent act 2026-08-29, in session: "Can you remove grove, kodhama and wisp plugins from the marketplace? Just remove them completely, I don't want to serve those plugins anymore" — an in-PR flip recording that act, per .grove/lifecycle.md's gated -> approved mover rule; the merge performs the ship. The agent did not open the gate.
depends_on: [kodhama-0002-delivery-channels, kodhama-0012-codex-marketplace-channel, kodhama-0018-stewards-dual-host-plugin-package, kodhama-0020-name-overarching-plugin-kodhama, kodhama-0021-separate-adoption-posture-from-support]
owner: agent
updated: 2026-08-29
provenance: "maintainer direction, 2026-08-29, given directly and reaffirmed in the same message. The three delistings and the deletion of the in-repo package were chosen by the maintainer against a stated account of what each one breaks; the costs recorded below were put to them before any file changed."
---

# 0030 — the install door serves trellis only

> **Maintainer direction (2026-08-29, post-ratification annotation; text below
> preserved as written).** Given the same day, after ratification: *"I might
> bring back more plugins in the future, I have some ideas to re-think grove in
> a different light (as a workflow supervisor on top of existing workflows), but
> it will probably ne a project restart, so for now stewards will serve only
> trellis as a marketplace, and all the other plugins, including kodhama as a
> plugin, are to be retired."*
>
> This **reframes §Cost 1 and closes the follow-up in §What was considered and
> not done.** That section calls opening doors in `kodhama/grove` and
> `kodhama/wisp` *"the follow-up this decision most obviously owes,"* written
> on the assumption that the three plugins were delisted but live. They are
> **retired**. No install door is owed to a retired plugin, so **no issue is
> filed for it** — not because `kodhama-0027` D1 is waived, but because there
> is no outstanding work for it to track.
>
> §Cost 1 stands as a factual record of what the delisting did — grove and wisp
> resolve in no catalog — and stops being a debt. **Grove's return, if it
> comes, is a project restart** under a different premise (a supervisor over
> existing workflows), which would arrive as its own decision and would not
> restore this one's listings. D6 below is unaffected: re-listing anything here
> still supersedes this record.

## Decision

**1. Both catalogs list `trellis` and nothing else.** `grove`, `kodhama` and
`wisp` are removed from `.claude-plugin/marketplace.json` and
`.agents/plugins/marketplace.json`. This is a delisting, not a deprecation:
no tombstone entry, no `installation` policy flag, no forwarding note in the
catalogs themselves. The names simply do not appear.

**2. The repository does not enable what it will not serve.**
`.claude/settings.json` enabled `grove@kodhama` and `kodhama@kodhama` from
this very door. Both are removed; `trellis@kodhama` stands.

**3. The `kodhama` package is deleted, not merely delisted.**
`plugins/kodhama/` is gone, and with it
`scripts/validate_kodhama_plugin.py`, `scripts/keyless_admission_check.py`,
`tests/fixtures/`, and the package, workflow-authoring and issue-skill
publication tests that made up most of `tests/test_kodhama_plugin.py`. What
survives is `tests/test_install_door.py`: the trellis entry, the
`distribution-scope` block's three-way mirror, the retired-surface guard, and
four new guards asserting this record's D1–D3 hold.

**4. `kodhama-0012` AC1 is superseded.** It reads: *"A clean Codex
installation can add `kodhama/stewards`, discover `grove@kodhama`, and resolve
its `plugins/grove` source."* That criterion is now unsatisfiable by
construction. Its AC4 — *"A product without a validated Codex package is
absent from the Codex catalog"* — is unaffected and still holds vacuously.
`kodhama-0012`'s substance survives: one canonical install repository, one
host-native manifest per host, catalogs carrying only discovery metadata.
Only the Grove-specific criteria go.

**5. `kodhama-0002`'s one-door principle stands, and its scope shrinks to
one plugin.** The marketplace `name` is unchanged (`kodhama`) and no
consumer's `trellis@kodhama` reference changes. What changes is that "one
door" now means one door to one plugin.

**6. Re-listing any of the three requires superseding this record.**
`tests/test_install_door.py::test_the_door_serves_only_what_kodhama_0030_left_standing`
asserts exact catalog membership, so a re-listing cannot land silently.

## Why

The maintainer's reason is the whole reason: they do not want to serve these
plugins. This record exists because the append-only rule requires the
contradiction with `kodhama-0012` to be *recorded* rather than edited away,
not because the direction needed justifying.

Two things are worth writing down beside it.

**The in-repo package was already provisional in its own words.** Its catalog
description called it *"Dogfood … staged here while its home is decided"*, and
`CLAUDE.md` said the same. Deleting a package whose stated status was "staged
pending a decision" is a resolution of that question, not a reversal of a
settled one. The direction chosen is that its home is nowhere.

**Delisting and deleting were separate calls and both were made.** Delisting
alone would have left the package on disk, unserved, still paying for a
validator, an admission check and a fixture corpus in CI. The maintainer chose
the deletion when shown that trade.

## Cost, stated

**1. Grove and wisp now have no install door at all.** Verified against
GitHub on 2026-08-29: neither `kodhama/grove` nor `kodhama/wisp` carries
`.claude-plugin/marketplace.json` or `.agents/plugins/marketplace.json` — both
return 404. Each still ships a valid package (`plugins/grove/`,
`plugins/wisp/`, both with `.claude-plugin` and `.codex-plugin` manifests),
but **nothing anywhere lists it**. `grove@kodhama` and `wisp@kodhama` resolve
in no catalog, and `kodhama/grove` cannot be added as a marketplace because it
has no manifest to add. Installation is possible only from an existing cached
copy or a direct source install.

This is sharper than it looks, because `kodhama-0002`'s 2026-07-10 forward
pointer deprecated trellis's own in-repo marketplace *on the grounds that*
"the org marketplace … is now the only door". The products were told to stop
maintaining their own doors. This record closes the one they were pointed at,
for three of the four, without opening a replacement.

**2. This repository is grove-managed and just disabled grove.** `CLAUDE.md`
states that conductor work items run as grove runs and the agent roles arrive
from the grove plugin as `grove:<role>`. D2 removes `grove@kodhama` from
`enabledPlugins`. Role dispatch here now depends on a copy this record does
not provide. `CLAUDE.md` is annotated to say so rather than left implying a
resolution that does not exist.

**3. Nine existing installs of `kodhama@kodhama` lose their update path.**
Read from `~/.claude/plugins/installed_plugins.json` on 2026-08-29: project
installs under `math-quest`, `trellis`, a cyrus worktree, and six math-quest
worktrees. Cached copies keep loading; `/plugin update` and any fresh install
stop resolving. Nothing notifies those projects.

**4. The issue convention loses its carrier.** `plugins/kodhama/skills/issues/`
held the `kodhama-0026` taxonomy skill and the dry-run-by-default seeder.
`kodhama-0026` and `kodhama-0027` still require work to be tracked as typed,
labelled issues; the skill that taught the convention and the actuator that
seeded the labels are deleted. The **convention** is unaffected — it lives in
the decisions. Its **tooling** is gone, and `kodhama-0029` D3's exemplar
(`plugins/kodhama/skills/issues/SKILL.md` carrying `implements:
kodhama-0026-issue-taxonomy`) is deleted with it, leaving that decision's
"already the practice" argument resting on two `.grove/` files.

**5. Specs 0004 and 0005 are retired without replacement.** Both were
`approved` implementation contracts for the deleted package. They move to
`superseded` pointing here. No spec now describes anything this repository
builds, because this repository no longer builds anything.

**6. The CI surface shrinks to something close to trivial.** The
`repository-validation` job runs six tests. The three host-registration jobs
still prove the marketplace registers on Claude and Codex against the PR's own
SHA, which is worth keeping for a one-plugin door — but the package carriers
they used to validate afterwards no longer exist.

## What was considered and not done

**A tombstone entry** — keeping the three names with
`"installation": "UNAVAILABLE"` and a pointer. Rejected on the maintainer's
words: *"Just remove them completely."*

**Opening doors in `kodhama/grove` and `kodhama/wisp` first**, so cost 1 would
not land. Not done, because it is work in two repositories this session was
not asked to touch, and because those repositories own that call — this record
names the gap rather than closing it on their behalf. **This is the follow-up
this decision most obviously owes**, and it is an issue, not a decision.

## Consequences

`kodhama-0012` keeps `status: approved` with AC1 superseded here; annotated
in place by forward pointer, per `kodhama-0004` and this repository's rule
that a ratified decision is never edited. `kodhama-0002` is annotated the
same way. `kodhama-0018` and `kodhama-0020` described a package that no longer
exists; neither is retracted, and neither is satisfiable — they are historical
from this date.

## Corrections

Appended 2026-08-29, the same day, after the automated reviews on #114 returned
two findings that were verified against the source and accepted. The fixes were
pushed while the maintainer was merging, so they missed the merge; append-only
binds from delivery, so the body above is left as written and both are corrected
here.

**C1 — D3's guard count is wrong.** It says *"four new guards asserting this
record's D1–D3 hold"*. There are **three**, one per decision:
`test_the_door_serves_only_what_kodhama_0030_left_standing` (D1),
`test_no_carrier_still_offers_the_delisted_plugins` (D2), and
`test_the_retired_package_left_no_carriers_behind` (D3). The file holds six
tests in total — those three plus the trellis entry, the `distribution-scope`
mirror, and the retired-surface guard, all three carried over rather than new.
**§Cost 6 was right and D3 contradicted it** ninety lines apart in one file,
which is the same defect `kodhama-0029` C6 records against itself. The
mutation evidence offered for D3 was loose in the same direction: four
mutations were run, but one of them drifted the `distribution-scope` block,
exercising a carried-over test rather than a new guard. Three new guards, three
discriminating mutations.

**C2 — the D3 guard was written broader than D3.** `plugins/kodhama/` is what
this record deletes; the test asserted the whole `plugins/` container was
absent. Any unrelated plugin added there later would have failed a test named
for the retired package's absence — and the scope block this record rewrote
says present contents are *"not a scope: it moves when the contents move"*.
Narrowed to `plugins/kodhama` in the same change as this correction, and
mutation-tested both directions: the package returning fires it, an unrelated
`plugins/unrelated/` does not. **The record needed no change for this one** —
the test was wrong about the decision, not the decision about itself.

**C3 — a third correction, to this corrections section itself.** Its first
draft claimed the grove/wisp install-door gap *"needs no separate issue"*,
arguing only that §Cost 1 and §What was considered and not done already
carried it. **Wrong**, and caught by review before this section merged: §What
was considered and not done says, in this record's own ratified text, *"This
is the follow-up this decision most obviously owes, and it is an issue, not a
decision"* — so the draft contradicted the body it was appended to — and
`kodhama-0027` D1 requires every *"task, a bug, a parked question, a
follow-up"* to be an issue in the repository that owns the work.

**The `kodhama-0029` D6 defence was mine, and it was not in this file.** It
was offered in #116's description and to the maintainer directly — *"D6 is
explicit that an artifact existing only to be closed is the thing to stop
producing"* — and the review rebutted it there: D6 exempts only an artifact
*"that exists only to be closed"*, while opening two install doors is
substantive outstanding work, the opposite case. An earlier version of this
paragraph attributed that citation to the record's draft, which never made it.
The motive is worth naming: the draft was written to reduce a follow-up pile,
not because the corpus supported it.

**The draft reached the right answer for the wrong reason, and the reason is
what was wrong.** Maintainer direction the same day retired the three plugins
outright, which removes the work an issue would have tracked — see the
annotation under the title. So no issue is filed, on grounds the corpus
actually supports. Had the plugins stayed live, one would be owed.
