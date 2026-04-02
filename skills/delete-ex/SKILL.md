---
name: delete-ex
description: Delete one generated ex-partner Codex skill plus its stored memories and version history after confirmation of the target slug.
metadata:
  short-description: Delete a generated ex skill
---

# Delete Ex

Confirm the target slug if it is ambiguous, then run:

```bash
python3 "$(if git rev-parse --show-toplevel >/dev/null 2>&1; then git rev-parse --show-toplevel; else printf '%s' "$HOME"; fi)/.codex/skills/create-ex/scripts/ex_skill_manager.py" delete \
  --slug "<slug>"
```

Report which data directory and runtime skill folders were removed.
