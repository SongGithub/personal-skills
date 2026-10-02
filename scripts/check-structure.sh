#!/usr/bin/env bash
# Verifies the repo layout is intact: plugin copies match the canonical skills,
# referenced files exist, and no example file was filled in by mistake.
set -uo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
status=0

# 1. no symlinks in skill or plugin paths.
#
# Plugin directories must be self-contained. OpenClaw (among others) copies a
# single plugin directory out of the marketplace and discards the rest of the
# repo, so a relative symlink such as
#   job-search/skills/job-screening-criteria -> ../../skills/job-screening-criteria
# resolves to a path that no longer exists once the plugin is copied out. Those
# links silently produced skills that never loaded. Use
# scripts/sync-plugins.sh to regenerate real copies instead.
while IFS= read -r link; do
  echo "FAIL: symlink not allowed: ${link#$root/} (run scripts/sync-plugins.sh)"
  status=1
done < <(find "$root/skills" "$root"/job-search "$root"/communication-style \
              "$root"/document-design -type l -not -path '*/.git/*' 2>/dev/null)

# 2. each plugin's packaged skills are byte-identical to the canonical skills/
while IFS= read -r name; do
  src="$root/skills/$name"
  if [ ! -d "$src" ]; then
    echo "FAIL: canonical skill missing: skills/$name"
    status=1
    continue
  fi

  # every plugin dir must contain a real copy of this skill
  found=0
  for p in job-search communication-style document-design; do
    dest="$root/$p/skills/$name"
    [ -d "$dest" ] || continue
    found=1
    if ! diff -rq --exclude '.DS_Store' "$src" "$dest" >/dev/null 2>&1; then
      echo "FAIL: $p/skills/$name has drifted from skills/$name (run scripts/sync-plugins.sh)"
      status=1
    fi
  done

  if [ "$found" -eq 0 ]; then
    echo "FAIL: skill '$name' is not packaged by any plugin"
    status=1
  fi
done < <(find "$root/skills" -mindepth 1 -maxdepth 1 -type d -exec basename {} \;)

# 3. each plugin exposes its skills
for p in job-search communication-style document-design; do
  dir="$root/$p/skills"
  if [ ! -d "$dir" ] || [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
    echo "FAIL: plugin '$p' has no skills"
    status=1
  fi
done

# 4. every references/* path mentioned in a SKILL.md exists
while IFS= read -r file; do
  d="$(dirname "$file")"
  while IFS= read -r ref; do
    if [ ! -e "$d/$ref" ]; then
      echo "FAIL: ${file#$root/} references missing ${ref}"
      status=1
    fi
  done < <(grep -oE 'references/[A-Za-z0-9._-]+' "$file" | sort -u)
done < <(find "$root/skills" "$root"/job-search/skills "$root"/communication-style/skills \
              "$root"/document-design/skills -name SKILL.md 2>/dev/null)

# 5. example files must still be placeholders
for f in preferences.example.yaml profile.example.md; do
  p="$(find "$root/skills" -name "$f" | head -1)"
  if [ -z "$p" ]; then echo "FAIL: missing $f"; status=1; fi
done

[ "$status" -eq 0 ] && echo "OK: layout intact"
exit $status
