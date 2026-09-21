#!/usr/bin/env bash
#
# mark-skills installer
# Copies every skill in ./skills into ~/.claude/skills so Claude Code picks them up.
#
# Usage:
#   ./install.sh            # install all skills (backs up any existing dir first)
#   ./install.sh -n         # dry run — show what would happen, change nothing
#   ./install.sh ads-line ghost-chat   # install only the named skills
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$REPO_DIR/skills"
DEST_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
STAMP="$(date +%Y%m%d-%H%M%S)"

DRY_RUN=0
if [[ "${1:-}" == "-n" || "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1; shift
fi

if [[ ! -d "$SRC_DIR" ]]; then
  echo "ERROR: skills/ not found next to install.sh ($SRC_DIR)" >&2
  exit 1
fi

# Which skills? args = specific list, else all dirs under skills/
if [[ $# -gt 0 ]]; then
  wanted=("$@")
else
  wanted=()
  for d in "$SRC_DIR"/*/; do wanted+=("$(basename "$d")"); done
fi

echo "Source : $SRC_DIR"
echo "Target : $DEST_DIR"
[[ $DRY_RUN -eq 1 ]] && echo "Mode   : DRY RUN (no changes)"
echo

mkdir -p "$DEST_DIR"
installed=0; skipped=0

for name in "${wanted[@]}"; do
  src="$SRC_DIR/$name"
  dest="$DEST_DIR/$name"
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "  skip  $name  (no SKILL.md in repo)"; skipped=$((skipped+1)); continue
  fi

  action="install"
  if [[ -e "$dest" || -L "$dest" ]]; then action="replace (backup first)"; fi

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "  would $action  $name"; continue
  fi

  # Back up whatever is already there (real dir or symlink) before overwriting.
  if [[ -e "$dest" || -L "$dest" ]]; then
    mv "$dest" "$dest.bak-$STAMP"
  fi
  cp -R "$src" "$dest"
  echo "  ok    $name"
  installed=$((installed+1))
done

echo
if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run complete."
else
  echo "Installed $installed skill(s), skipped $skipped."
  echo "Existing dirs were backed up as <name>.bak-$STAMP in $DEST_DIR"
  echo "Restart Claude Code (or start a new session) to load them."
fi
