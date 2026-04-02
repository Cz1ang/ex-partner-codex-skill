---
name: create-ex
description: Create, evolve, list, rollback, or delete an ex-partner Codex skill from chat logs, photos, social posts, and direct memories; generates full, memory-only, and persona-only runtime skills with local version history.
metadata:
  short-description: Create or evolve an ex-partner skill
---

# Create Ex

Use this skill when the user wants to distill an ex-partner into a Codex skill, continue evolving an existing one, correct how an existing generated ex talks, or manage generated ex skills.

Keep the user's language consistent across the whole interaction.

## Install layout

Preferred when this package lives in a git repo:

- Skill root: `<repo>/.codex/skills/create-ex`
- Generated runtime skills: `<repo>/.codex/skills/ex-<slug>`, `<repo>/.codex/skills/ex-<slug>-memory`, `<repo>/.codex/skills/ex-<slug>-persona`
- Structured data + versions: `<repo>/.codex/exes/<slug>/`

User-scope fallback:

- `~/.codex/skills/create-ex`
- `~/.codex/skills/ex-<slug>*`
- `~/.codex/exes/<slug>/`

The bundled manager script now auto-detects this order by default:
1. current git repo root + `.codex/`
2. installed script path inside `.codex/`
3. fallback `~/.codex/`

## Trigger surface

Activate for requests such as:
- `create-ex`
- "帮我做一个前任 skill / ex skill"
- "我想蒸馏一个前任"
- "我想继续补充某个 ex"
- "ta不会这样说 / they wouldn't say that"
- `list-exes`
- `ex-rollback <slug> <version>`
- `delete-ex <slug>` / `let-go <slug>`

## Guardrails

- Personal reflection only; never help with harassment, stalking, impersonation abuse, or privacy invasion.
- All source material stays local.
- Do not fabricate relationship facts; mark unknowns as `[待补充]` / `[Needs more evidence]`.
- Generated personas should preserve the person's edges and uncertainty instead of turning them into a perfect assistant.

## Quick workflow

### 1. Gather the minimum profile
Ask for:
1. alias/codename (required)
2. one-line relationship summary (optional)
3. one-line personality summary (optional)

If the user already supplied enough detail, do not re-ask.

### 2. Gather source material
Offer any mix of:
- WeChat export
- QQ export
- social-media screenshots or exports
- photos
- pasted memories / narration

### 3. Parse local artifacts
Use the bundled scripts when file-based input exists:

```bash
if git rev-parse --show-toplevel >/dev/null 2>&1; then
  CODEX_ROOT="$(git rev-parse --show-toplevel)/.codex"
else
  CODEX_ROOT="$HOME/.codex"
fi

CREATE_EX_DIR="$CODEX_ROOT/skills/create-ex"
DATA_ROOT="$CODEX_ROOT/exes"
TMP_DIR="${TMPDIR:-/tmp}/create-ex"
mkdir -p "$TMP_DIR"

python3 "$CREATE_EX_DIR/scripts/wechat_parser.py" --file <path> --target "<name>" --output "$TMP_DIR/wechat.md"
python3 "$CREATE_EX_DIR/scripts/qq_parser.py" --file <path> --target "<name>" --output "$TMP_DIR/qq.md"
python3 "$CREATE_EX_DIR/scripts/social_parser.py" --dir <path> --output "$TMP_DIR/social.md"
python3 "$CREATE_EX_DIR/scripts/photo_analyzer.py" --dir <path> --output "$TMP_DIR/photos.md"
```

For screenshots or attached images, inspect them directly with the normal Codex image/file tooling when available, and treat the parsers as helpers for filesystem batches.

### 4. Build the two source docs
Use these references:
- `references/memory_analyzer.md`
- `references/memory_builder.md`
- `references/persona_analyzer.md`
- `references/persona_builder.md`

Produce:
- `memory.md` — relationship memory
- `persona.md` — persona model

Preview concise summaries first. If the user gives an explicit correction, update the draft instead of arguing.

### 5. Initialize or evolve the ex package
Use the manager script to create directories and metadata:

```bash
python3 "$CREATE_EX_DIR/scripts/ex_skill_manager.py" init \
  --name "<alias>" \
  --slug "<slug-if-known>"
```

Then write or update:
- `$DATA_ROOT/<slug>/memory.md`
- `$DATA_ROOT/<slug>/persona.md`
- `$DATA_ROOT/<slug>/meta.json`

Finally render runtime skills:

```bash
python3 "$CREATE_EX_DIR/scripts/ex_skill_manager.py" combine --slug "<slug>"
```

## Evolution mode

### Append memories / new files
1. Read existing `memory.md`, `persona.md`, `meta.json`
2. Parse the new material
3. Review `references/merger.md`
4. Backup first:

```bash
python3 "$CREATE_EX_DIR/scripts/ex_skill_manager.py" backup --slug "<slug>"
```

5. Merge incrementally; do not overwrite earlier conclusions unless the user explicitly corrects them
6. Re-run `combine`

### Correction mode
If the user says the generated ex sounds wrong:
1. Review `references/correction_handler.md`
2. Classify the correction as Memory or Persona
3. Backup first
4. Append a correction record into the relevant file
5. Update the corrected text inline
6. Re-run `combine`

## Management commands

```bash
python3 "$CREATE_EX_DIR/scripts/ex_skill_manager.py" list
python3 "$CREATE_EX_DIR/scripts/ex_skill_manager.py" rollback --slug "<slug>" --version "<version>"
python3 "$CREATE_EX_DIR/scripts/ex_skill_manager.py" delete --slug "<slug>"
```

## Response shape

When a create/update succeeds, report:
- slug
- data directory
- generated skill names
- what sources were used
- any gaps or assumptions that still need user confirmation
