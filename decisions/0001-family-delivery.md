---
id: kodhama-0001-family-delivery
type: discovery
status: approved  # ratified by the kodhama-0002-delivery-channels PR merge (maintainer review 2026-07-07)
depends_on: [adr-0030-espalier, discovery-espalier-runtime-viz]
rubric: rubrics/research-quality.md
owner: agent
updated: 2026-07-07
provenance: gundisalwa/math-quest discovery/kodhama-delivery.md (branch claude/agentic-runtime-viz-x1884q) — migrated at org-meta bootstrap; the original owes a supersession pointer here
---

# Discovery: delivering the kodhama family (trellis · espalier · espial · next)

**Question (maintainer, 2026-07-07).** How should the family's artifacts be
distributed — separate per-module delivery, a combined "builder" repo, or a
monorepo? Where do cross-kodhama decisions and artifacts live? Concern
driving it: a fourth standalone CLI seemed to create a dependency on the
trellis LP for its installer reference, and "a bunch of tools for small
things" feels wrong — but the combined mechanism was unclear. Note: this is
an org-level question; this artifact lives here temporarily (next to the
plan that consumes it) and moves to the org meta repo when that exists.

## Findings

- **F1 — One org-level Homebrew tap serving many separate repos is
  established practice.** charmbracelet/homebrew-tap hosts 15+ formulas
  (gum, glow, vhs, mods, …) for tools that each live in their own repo
  ([github.com/charmbracelet/homebrew-tap](https://github.com/charmbracelet/homebrew-tap),
  fetched 2026-07-07) — `verified`. goreleaser's own docs and common
  guidance recommend a generically-named tap (`homebrew-tap`/`-tools`) when
  an org ships multiple tools, with each product's release pipeline pushing
  its formula into the shared tap
  ([goreleaser.com/customization/homebrew](https://goreleaser.com/customization/homebrew/),
  [appliedgo.net/release2](https://appliedgo.net/release2/)) — `verified`
  (vendor docs + practitioner writeup). Once a tap exists, "publishing
  additional CLI tools … becomes almost trivial"
  ([justin.searls.co](https://justin.searls.co/posts/how-to-distribute-your-own-scripts-via-homebrew/)) —
  `verified` (practitioner source).
- **F2 — Tool families at comparable scale run polyrepo with per-product
  releases**, sharing only thin org surfaces (tap, brand site): Charm (F1),
  HashiCorp (per-product repos/releases; their own monorepo-vs-multi debate
  is about *user configs*, not products —
  [hashicorp.com blog](https://www.hashicorp.com/en/blog/terraform-mono-repo-vs-multi-repo-the-great-debate)) —
  `verified` for Charm, `inferred` for the generalization. The literature's
  monorepo advantages are atomic cross-cutting changes and easy code
  sharing; polyrepo's are independent release cycles, clear ownership,
  simpler CI ([spacelift.io](https://spacelift.io/blog/monorepo-vs-polyrepo),
  [aviator.co](https://www.aviator.co/blog/monorepo-vs-polyrepo/)) —
  `verified` (secondary syntheses agree).
- **F3 — Channel-preference data is thin.** No primary survey ranking
  curl-vs-brew-vs-marketplace was found in this pass; ecosystem norms
  (Homebrew as the macOS devtool default; curl|sh for zero-prereq installs;
  language package managers where the runtime already exists) are
  consistently described in secondary sources
  ([docs.brew.sh](https://docs.brew.sh/Installation), searls, dev.to
  roundups) — `inferred`, flagged honestly: keep all three trellis channels
  since each serves a distinct entry path, and let real users generate the
  data.
- **F4 — Family facts that constrain the design** (repo-local, `verified`):
  espalier is charters/skills/agents — *there is no espalier binary to
  deliver*; its natural channel is the Claude Code plugin marketplace +
  trellis-style overlay. Espial is zero-dep TypeScript — its natural
  channels are vendored copy (now) and npm (at release), where the npm
  *scope* `@kodhama/espial` sidesteps the `espial` npm collision recorded in
  plan-suite-lift §Naming. Trellis's release fan-out (goreleaser-style
  auto-release + tap dispatch) already exists per-repo.

## Decision (recommendation — ratifies via the plan/ADR at merge)

**Each product delivers itself; the org owns two thin shared surfaces. No
builder repo, no monorepo.**

1. **Products stay polyrepo** (trellis / espalier / espial, each with its
   own releases, LP, and espalier operating model). Monorepo rejected for
   this family: three languages/natures (Go binary, markdown charters, TS
   tool), deliberately independent release cadences, per-repo self-hosting
   is part of the W experiment, and the marketplace/tap mechanics assume
   repo-rooted products. Its one real advantage — atomic cross-cutting
   changes — is mostly the design system, which has ONE home at org
   level (`kodhama/design-system`, see point 3) and reaches products
   through generation-time links, not builds. *Revisit trigger:* furrow ledgers showing
   cross-repo change friction dominating (e.g., >⅓ of family furrows
   needing coordinated multi-repo PRs).
2. **`kodhama/homebrew-tap`** (rename of homebrew-trellis, F1 pattern):
   one tap, N formulas; each product's release workflow pushes its own
   formula (trellis already dispatches; espial adds a formula if/when a
   CLI ships). Install reads `brew install kodhama/tap/trellis`. This
   dissolves the "bunch of small delivery repos" worry — the tap is the
   only shared delivery repo the family will ever need, and it contains
   no build logic.
3. **`kodhama/kodhama`** — the org meta repo: cross-kodhama decisions
   (this artifact's future home), the family front page (links each
   product's own LP + canonical install), — and the design system, amended same
   day TWICE, lands as **its own repo `kodhama/design-system`** (the
   Primer/Polaris/Carbon shape): the DS is a family asset consumed by all
   products *including trellis* and the family page itself, so homing it
   in trellis was wrong and folding it into the meta repo was second-best;
   a standalone repo gives a self-describing dependency link, git-tag
   versioning, and its own dogfooding furrows. product LPs become derived artifacts generated
   from the DS + each repo's own lp-content, DS-version-stamped, with
   staleness surfaced by check (the trellis decision-0028 derived-pairs
   rule, applied cross-repo through soft/agentic links — no build
   coupling). See plan-suite-lift §Lane T for the mechanism. A front door and decision archive — **not a builder**.
   Each product's installer reference lives on its OWN LP; the family page
   only links — so no product's installer depends on another product's
   page (the maintainer's original concern, resolved by inverting the
   dependency onto a neutral org surface).
4. **Per-artifact channel matrix:**

   | Artifact | Now | At first release | Channels long-run |
   |---|---|---|---|
   | trellis | unchanged | — | curl (own repo) · `kodhama/tap` brew · Claude marketplace |
   | espalier | overlay via lift | Claude plugin `kodhama/espalier` | marketplace + overlay — never a binary |
   | espial | vendored copy | npm `@kodhama/espial` (scope kills the name clash) | npm · vendored · tap formula only if a real CLI emerges |
   | future tools | own repo | formula/scope entry in the shared surfaces | inherit this matrix |

5. **Release machinery lives in each product repo** (goreleaser-style,
   as trellis does today). The former "Lane E builder repo" idea is
   superseded by 2+3: same benefits (one install story, family coherence),
   none of the coupling.

## Assumptions

- The tap rename (`homebrew-trellis → kodhama/homebrew-tap`) happens now,
  while user count ≈ 0 — the maintainer's own "settle it before anyone
  uses it" principle. Old tap redirects during the window.
- npm org `kodhama` is claimable (check at espial release, not before).
- Family page naming (`kodhama/kodhama` project page vs
  `kodhama.github.io` org site) is a detail decided when the page ships.

## Acceptance criteria

- **AC1** Plan-suite-lift's Lane E reflects this decision (org surfaces,
  not a builder) — checkable by reading the plan.
- **AC2** After the tap rename: `brew install kodhama/tap/trellis` works
  from a clean machine and zero formulas reference `homebrew-trellis`.
- **AC3** When espial releases: `@kodhama/espial` installs via npm and its
  LP carries its own canonical install block (no reference to trellis's LP).
- **AC4** Cross-kodhama decisions have exactly one home (`kodhama/kodhama`
  once created; this artifact moves there with a supersession pointer).

## Open questions

- Does espial ever grow a real CLI wanting a tap formula, or does npm +
  vendored cover it indefinitely?
- Claude marketplace: one marketplace per repo, or one org marketplace in
  `kodhama/kodhama` listing all plugins? (Check marketplace mechanics when
  espalier's plugin ships.) → **Answered by `kodhama-0002-delivery-channels`:
  one org marketplace here; mechanics doc-verified.**
- Linux beyond curl (apt/AUR/nix): out of scope until someone asks.

## Rubric check

Rubric: `rubrics/research-quality.md`.

| Item | Result | Evidence |
|---|---|---|
| 1–2. Load-bearing claims sourced + tagged; verified = primary | PASS | F1 charm tap fetched directly; goreleaser vendor docs; F3 honestly `inferred` with the gap named. |
| 3. Unsourced → speculated | PASS | None presented as fact; F2's generalization tagged `inferred`. |
| 4. Preflight | PASS | WebFetch/WebSearch exercised this session (4 queries this pass). |
| 5. Findings vs recommendation separated | PASS | §Findings tagged; §Decision reasons from F1–F4. |
| 6. Frontmatter, deps gated | PASS | Both deps `gated`. |
| 7. ≥3 ACs + Open questions | PASS | AC1–AC4; three OQs. |
| 8. Residual unknowns logged | PASS | Channel-preference data gap, npm org, marketplace mechanics. |

**Verdict: promote `draft → gated`.** Org-level ratification = the
maintainer's nod + Lane E execution; moves to `kodhama/kodhama` at lift.
