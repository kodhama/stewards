#!/usr/bin/env bash
# Provision the kodhama issue taxonomy: org-level issue types + per-repo labels.
#
# Dry-run by default. Nothing is created or changed without --apply.
# This script NEVER deletes a label. Redundant stock labels are reported only.
#
#   ./seed-issue-taxonomy.sh                        # plan for every family repo
#   ./seed-issue-taxonomy.sh --repo grove           # plan for one repo
#   ./seed-issue-taxonomy.sh --repo grove --apply   # execute for one repo
#   ./seed-issue-taxonomy.sh --types-only --apply   # org issue types only
#
# Requires: gh, with scopes `repo` (labels) and `admin:org` (issue types).
set -euo pipefail

ORG="kodhama"
APPLY=0
TYPES_ONLY=0
LABELS_ONLY=0
REPOS=()

ALL_REPOS=(trellis grove wisp math-quest design-system kodhama stewards sdd-gauntlet homebrew-tap)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --org)         ORG="$2"; shift 2 ;;
    --repo)        REPOS+=("$2"); shift 2 ;;
    --apply)       APPLY=1; shift ;;
    --types-only)  TYPES_ONLY=1; shift ;;
    --labels-only) LABELS_ONLY=1; shift ;;
    -h|--help)     sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
[[ ${#REPOS[@]} -eq 0 ]] && REPOS=("${ALL_REPOS[@]}")

if [[ $APPLY -eq 0 ]]; then
  echo "DRY RUN — nothing will be changed. Re-run with --apply to execute."
  echo
fi

run() {  # run <description> <command...>
  local desc="$1"; shift
  if [[ $APPLY -eq 1 ]]; then
    if "$@" >/dev/null 2>&1; then echo "  ✓ $desc"
    else echo "  ✗ $desc  (failed — see notes below)"; fi
  else
    echo "  + would create: $desc"
  fi
}

# ---------------------------------------------------------------- issue types

# name|color|description   — Task, Bug, Feature ship with every org already.
CUSTOM_TYPES=(
  "Research|purple|An open question to answer. The deliverable is a finding, not a change"
  "Decision|orange|A choice that must be made and recorded"
  "Epic|green|Children that ship separately, plus the guarantee the set is coherent and complete"
)

seed_types() {
  echo "== org issue types: $ORG =="

  if ! gh auth status 2>&1 | grep -q 'admin:org'; then
    echo "  ! your gh token lacks the 'admin:org' scope — creating types will fail."
    echo "    fix with:  gh auth refresh -h github.com -s admin:org"
    echo
  fi

  local existing
  existing="$(gh api "/orgs/$ORG/issue-types" --jq '.[].name' 2>/dev/null || echo "")"

  for spec in "${CUSTOM_TYPES[@]}"; do
    IFS='|' read -r name color desc <<< "$spec"
    if grep -qxF "$name" <<< "$existing"; then
      echo "  = $name (exists)"
    else
      run "type $name" gh api --method POST "/orgs/$ORG/issue-types" \
        -f "name=$name" -f "color=$color" -f "description=$desc" -F is_enabled=true
    fi
  done
  echo
}

# --------------------------------------------------------------------- labels

# name|color|description
LABELS=(
  "priority: p0|b60205|Drop other work — broken or blocking now"
  "priority: p1|d93f0b|Next up, ahead of unlabelled work"
  "priority: p2|c5def5|Accepted and wanted, ranked below normal"

  "stage: triage|fef2c0|Noticed, not yet committed to — the type may still be unset"
  "stage: shaping|c2e0c6|Accepted; the problem is not yet settled"
  "stage: drafting|bfd4f2|The defining artifact is not yet finished"
  "stage: ready|0e8a16|Defining artifact approved; dispatchable unless a status label says otherwise"
  "stage: active|1d76db|Approved and started, not yet done"
  "stage: review|5319e7|Done, not yet verified"

  "facing: user|0e8a16|Changes what a consumer of this repo gets"
  "facing: system|5319e7|Changes only how this repo is built or maintained"

  "blocked|b60205|Blocked by something that is not an issue (issue-to-issue is a native dependency)"
  "deferred|cfd3d7|Accepted, but waiting on a condition stated in the body"
  "needs-human|fbca04|Requires a person; an agent must not proceed alone"
  "needs-design-system|d4c5f9|Waiting on an upstream design-system change"
)

# Stock labels this taxonomy makes redundant. Reported, never deleted.
REDUNDANT=(bug enhancement documentation question duplicate invalid wontfix idea chore
           consider shaping agent-task meta program design-upstream design-feedback
           user-feedback "priority: high" "priority: medium" "priority: low")

seed_labels() {
  local repo="$1"
  echo "== labels: $ORG/$repo =="

  local existing
  if ! existing="$(gh label list -R "$ORG/$repo" --limit 200 --json name --jq '.[].name' 2>/dev/null)"; then
    echo "  ! cannot read labels (missing repo or permission) — skipped"; echo; return
  fi

  for spec in "${LABELS[@]}"; do
    IFS='|' read -r name color desc <<< "$spec"
    if grep -qxF "$name" <<< "$existing"; then
      echo "  = $name (exists)"
    else
      run "$name" gh label create "$name" -R "$ORG/$repo" -c "$color" -d "$desc"
    fi
  done

  local found=()
  for r in "${REDUNDANT[@]}"; do
    grep -qxF "$r" <<< "$existing" && found+=("$r")
  done
  if [[ ${#found[@]} -gt 0 ]]; then
    echo "  ─ now redundant, NOT deleted: ${found[*]}"
    echo "    migrate the issues carrying them first (see migration/legacy-mapping.md),"
    echo "    then remove by hand once each is at zero uses."
  fi
  echo
}

# ----------------------------------------------------------------------- main

[[ $LABELS_ONLY -eq 0 ]] && seed_types
if [[ $TYPES_ONLY -eq 0 ]]; then
  for repo in "${REPOS[@]}"; do seed_labels "$repo"; done
fi

cat <<'EOF'
Notes
  · Issue types are org-wide — seed them once, not per repo.
  · No `area:` label is seeded. They are deliberately repo-local — add them
    by hand, and only when three or more issues would carry one.
  · No label is ever deleted by this script, and no existing issue is touched.
    Migrating existing issues is a separate, explicitly approved action.
EOF
