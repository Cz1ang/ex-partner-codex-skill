---
name: list-exes
description: List generated ex-partner Codex skills and summarize their current version, update time, and profile metadata.
metadata:
  short-description: List generated ex skills
---

# List Exes

If this package is installed inside a git repo, prefer running it from that repo so the manager resolves `<repo>/.codex/` automatically. Otherwise it falls back to `~/.codex/`.

Run:

```bash
python3 "$(if git rev-parse --show-toplevel >/dev/null 2>&1; then git rev-parse --show-toplevel; else printf '%s' "$HOME"; fi)/.codex/skills/create-ex/scripts/ex_skill_manager.py" list
```

Then summarize each generated ex by slug, display name, current version, and last updated date.
