---
name: ex-rollback
description: Roll a generated ex-partner Codex skill back to a previous archived version and re-render its runtime skills.
metadata:
  short-description: Roll back an ex skill version
---

# Ex Rollback

List versions first if the target version is unclear:

```bash
python3 "$(if git rev-parse --show-toplevel >/dev/null 2>&1; then git rev-parse --show-toplevel; else printf '%s' "$HOME"; fi)/.codex/skills/create-ex/scripts/ex_skill_manager.py" versions --slug "<slug>"
```

Then roll back:

```bash
python3 "$(if git rev-parse --show-toplevel >/dev/null 2>&1; then git rev-parse --show-toplevel; else printf '%s' "$HOME"; fi)/.codex/skills/create-ex/scripts/ex_skill_manager.py" rollback \
  --slug "<slug>" \
  --version "<version>"
```

After rollback, report the restored version and regenerated runtime skills.
