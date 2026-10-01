#!/usr/bin/env bash
# Verifies the repo layout is intact: symlinks resolve, referenced files exist.
set -uo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
status=0

# 1. every symlink resolves to something real
while IFS= read -r link; do
  if [ ! -e "$link" ]; then
    echo "FAIL: broken symlink: ${link#$root/}"
    status=1
  fi
done < <(find "$root" -type l -not -path '*/.git/*')

# 2. each plugin exposes its skills
for p in job-search communication-style document-design; do
  dir="$root/$p/skills"
  if [ ! -d "$dir" ] || [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
    echo "FAIL: plugin '$p' has no skills"
    status=1
  fi
done

# 3. every references/* path mentioned in a SKILL.md exists
while IFS= read -r file; do
  d="$(dirname "$file")"
  while IFS= read -r ref; do
    if [ ! -e "$d/$ref" ]; then
      echo "FAIL: ${file#$root/} references missing ${ref}"
      status=1
    fi
  done < <(grep -oE 'references/[A-Za-z0-9._-]+' "$file" | sort -u)
done < <(find "$root/skills" -name SKILL.md)

# 4. example files must still be placeholders
for f in preferences.example.yaml profile.example.md; do
  p="$(find "$root/skills" -name "$f" | head -1)"
  if [ -z "$p" ]; then echo "FAIL: missing $f"; status=1; fi
done

[ "$status" -eq 0 ] && echo "OK: layout intact"
exit $status
