#!/usr/bin/env bash
# Verifies the workflow definition honours the spec's FR-001: one versioned
# definition, no retired skill names, and every cross-reference resolving.
#
# Run locally, or let CI run it on every push.
set -uo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root" || exit 1
status=0

# 1. the workflow spec must exist and carry its mandatory sections
spec="specs/001-job-search-workflow/spec.md"
if [ ! -f "$spec" ]; then
  echo "FAIL: workflow spec missing: $spec"
  exit 1
fi
for section in "User Scenarios" "Functional Requirements" "Success Criteria" "Edge Cases"; do
  if ! grep -q "$section" "$spec"; then
    echo "FAIL: spec missing section: $section"
    status=1
  fi
done

# 2. FR-001: no retired skill name may survive as a reference anywhere
#    (matches path forms and backticked names, not incidental prose words)
retired=(job-scraper job-search-quality job-application-assistant apply-jobs-workflow cv-attach-workflow upskill)
for name in "${retired[@]}"; do
  hits=$(git grep -n -E "(skills/$name(/|\`|\$)|\`$name\`|/$name/SKILL\.md)" -- . ':!specs' 2>/dev/null || true)
  if [ -n "$hits" ]; then
    echo "FAIL: retired skill name '$name' still referenced:"
    echo "$hits" | head -3 | sed 's/^/    /'
    status=1
  fi
done

# 3. every relative cross-reference from a skill must resolve
while IFS= read -r f; do
  refs=$(grep -oE "\.\./[A-Za-z0-9_-]+/" "$f" 2>/dev/null | sort -u || true)
  for r in $refs; do
    target="$(dirname "$f")/$r"
    if [ ! -d "$target" ] && [ ! -f "${target}SKILL.md" ]; then
      echo "FAIL: broken cross-reference in $f -> $r"
      status=1
    fi
  done
done < <(find skills -name 'SKILL.md' -not -path '*/.git/*')

if [ "$status" -eq 0 ]; then echo "OK: workflow conforms to the spec"; fi
exit "$status"