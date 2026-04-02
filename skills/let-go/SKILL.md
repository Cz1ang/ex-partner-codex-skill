---
name: let-go
description: Gentle alias for deleting a generated ex-partner Codex skill while keeping the tone soft and explicit about what was removed.
metadata:
  short-description: Gently delete a generated ex skill
---

# Let Go

Use the same deletion flow as `delete-ex`:

```bash
python3 "$(if git rev-parse --show-toplevel >/dev/null 2>&1; then git rev-parse --show-toplevel; else printf '%s' "$HOME"; fi)/.codex/skills/create-ex/scripts/ex_skill_manager.py" delete \
  --slug "<slug>"
```

Close with a gentle confirmation such as: `已经放下了。祝你一切都好。`
