#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run this script from a git repository root (or any path inside the target repo)." >&2
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_SKILLS_DIR="$SCRIPT_DIR/skills"
TARGET_SKILLS_DIR="$REPO_ROOT/.codex/skills"

mkdir -p "$TARGET_SKILLS_DIR"

for name in create-ex list-exes delete-ex let-go ex-rollback; do
  rm -rf "$TARGET_SKILLS_DIR/$name"
  cp -R "$SOURCE_SKILLS_DIR/$name" "$TARGET_SKILLS_DIR/$name"
done

echo "Installed Codex skills into: $TARGET_SKILLS_DIR"
