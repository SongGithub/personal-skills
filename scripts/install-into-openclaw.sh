#!/usr/bin/env bash
# Install the generated plugin wrappers into this machine's OpenClaw extension dir,
# and (re)build the plugin-skills symlinks. The repository is the source of truth:
# this script only ever copies from it, and prunes anything that no longer exists there.
#
#   ./scripts/install-into-openclaw.sh [--dry-run]
#
# Run after sync-plugins.sh, or on its own (it syncs first).
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
ext="$HOME/.openclaw/extensions"
link="$HOME/.openclaw/plugin-skills"
dry="${1:-}"

plugins=(job-search communication-style document-design)

echo "Syncing wrappers from the repo first..."
"$root/scripts/sync-plugins.sh" >/dev/null

mkdir -p "$ext" "$link"

for plugin in "${plugins[@]}"; do
  src="$root/$plugin"
  [ -d "$src" ] || { echo "skip $plugin (not in repo)"; continue; }
  dest="$ext/$plugin"

  # 1. drop plugin-skills symlinks that point into this extension (removes stale names)
  pruned=0
  for l in "$link"/*; do
    [ -L "$l" ] || continue
    tgt="$(readlink "$l")"
    case "$tgt" in
      "$dest"/*) if [ "$dry" = "--dry-run" ]; then echo "  would prune link $(basename "$l")"; else rm -f "$l"; fi; pruned=$((pruned+1));;
    esac
  done

  # 2. replace the extension copy wholesale
  if [ "$dry" = "--dry-run" ]; then
    echo "would refresh $dest from $src"
  else
    rm -rf "$dest"
    mkdir -p "$dest"
    rsync -a --exclude '.DS_Store' "$src/" "$dest/"
  fi

  # 3. recreate one symlink per skill in the refreshed copy
  added=0
  for s in "$src"/skills/*/; do
    [ -d "$s" ] || continue
    name="$(basename "$s")"
    target="$dest/skills/$name"
    if [ "$dry" = "--dry-run" ]; then echo "  would link $name"; else ln -sfn "$target" "$link/$name"; fi
    added=$((added+1))
  done
  echo "$plugin: pruned $pruned stale link(s), installed $added skill(s)"
done

echo "Done. plugin-skills now mirrors the repository."