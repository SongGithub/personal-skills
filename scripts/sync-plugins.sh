#!/usr/bin/env bash
# Regenerate the Claude plugin wrappers from the canonical skills/ tree.
#
# Plugin directories must be SELF-CONTAINED. Some consumers (OpenClaw, for one)
# copy a single plugin directory out of the marketplace and discard the rest of
# the repository. A relative symlink like
#
#     job-search/skills/job-screening-criteria -> ../../skills/job-screening-criteria
#
# resolves correctly when the whole repo is cloned in place (Claude Code), but
# breaks once the plugin directory is copied on its own, because ../../skills no
# longer exists. Dereferencing into real files keeps both consumers working.
#
# Run after editing anything under skills/:
#     ./scripts/sync-plugins.sh
#
# CI (scripts/check-structure.sh) fails if the copies drift from the source.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
skills_src="$root/skills"

# plugin-dir -> space-separated skill names it packages
declare -a PLUGINS=(
  "job-search:job-application-preparation job-screening-criteria jira-job-records job-application-pipeline cv-generate-and-attach trello-card-rules job-board-search skill-gap-plan first-principles-startup"
  "document-design:document-design"
  "communication-style:communication-style"
  "knowledge-wiki:knowledge-compounding"
)

for entry in "${PLUGINS[@]}"; do
  plugin="${entry%%:*}"
  names="${entry#*:}"
  dest_root="$root/$plugin/skills"

  for name in $names; do
    src="$skills_src/$name"
    dest="$dest_root/$name"

    if [ ! -d "$src" ]; then
      echo "FAIL: canonical skill missing: ${src#$root/}"
      exit 1
    fi

    # Drop any existing entry (symlink or stale copy), then re-copy as real files.
    rm -rf "$dest"
    mkdir -p "$dest_root"
    rsync -a --delete --exclude '.DS_Store' "$src/" "$dest/"
    echo "synced $plugin/skills/$name"
  done
done

echo "Plugin wrappers regenerated from skills/."
