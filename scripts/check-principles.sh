#!/usr/bin/env bash
# Fails if personal data appears in this repository.
#
# Two layers:
#   1. Generic checks needing no configuration — real email addresses, phone
#      numbers, currency amounts, credential prefixes.
#   2. A private denylist of names, employers and circumstances, supplied from
#      OUTSIDE this repository so the list itself is never published.
#
# Denylist sources, in order:
#   $PERSONAL_DENYLIST_FILE   path to a local file
#   $PERSONAL_DENYLIST        the list itself (CI supplies it from a repo secret)
#   ~/.config/job-search/denylist.txt
#
# Without a denylist the generic checks still run, and the script says so.
set -uo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
status=0

report() {
  echo "FAIL: $1"
  printf '%s\n' "$2" | sed "s|$root/||" | head -8
  echo
  status=1
}

# skip this script: it contains the patterns it searches for
scan() {
  local hits
  hits="$(grep -rInE --exclude-dir=.git --exclude-dir=out --exclude-dir=evals \
    --exclude=check-principles.sh -- "$2" "$root" 2>/dev/null || true)"
  [ -n "$hits" ] && report "$1" "$hits"
  return 0
}

echo "== generic checks =="

emails="$(grep -rInE --exclude-dir=.git --exclude-dir=out --exclude-dir=evals \
  -- '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$root" 2>/dev/null \
  | grep -vE 'example\.(com|org|net)|@example' || true)"
[ -n "$emails" ] && report "real email address" "$emails"

phones="$(grep -rInE --exclude-dir=.git --exclude-dir=out --exclude-dir=evals \
  -- '(\+61[ -]?|\b0)[0-9]{3}[ -][0-9]{3}[ -][0-9]{3}\b' "$root" 2>/dev/null \
  | grep -vE '0{3}[ -]0{3}' || true)"
[ -n "$phones" ] && report "phone number" "$phones"

# grouped or k-suffixed amounts only, so shell variables like $1 do not match
scan "currency amount" '\$[0-9]{2,3}[kK]|\$[0-9]{1,3},[0-9]{3}'

for p in 'ATATT3' 'gho_' 'ghp_' 'sk-[A-Za-z0-9]{20,}'; do
  scan "credential prefix" "$p"
done

echo "== private denylist =="
deny_file="${PERSONAL_DENYLIST_FILE:-$HOME/.config/job-search/denylist.txt}"
patterns=""
if [ -n "${PERSONAL_DENYLIST:-}" ]; then
  patterns="${PERSONAL_DENYLIST}"
  source_desc="PERSONAL_DENYLIST environment variable"
elif [ -f "$deny_file" ]; then
  patterns="$(cat "$deny_file")"
  source_desc="$deny_file"
else
  source_desc=""
fi

if [ -z "$patterns" ]; then
  echo "SKIP: no private denylist available; name and employer checks not run."
  echo "      Set PERSONAL_DENYLIST_FILE, PERSONAL_DENYLIST, or create $deny_file"
else
  echo "using $source_desc"
  while IFS= read -r pattern || [ -n "$pattern" ]; do
    case "$pattern" in ''|'#'*) continue ;; esac
    scan "'$pattern'" "$pattern"
  done <<< "$patterns"
fi

if [ "$status" -eq 0 ]; then
  echo "OK: no personal data found"
else
  echo "Personal data found. Move it to \$JOB_SEARCH_HOME and keep only examples here."
fi
exit $status
