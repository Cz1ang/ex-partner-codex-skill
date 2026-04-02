# Ex-Partner Codex Skill

## Project origin

This package is a **Codex-oriented adaptation and secondary development** based on the upstream project:

- Upstream project: https://github.com/therealXiaomanChu/ex-skill

In other words, this is **not the original upstream package copied verbatim**.  
It is a Codex-targeted port built on top of the upstream idea, workflow, templates, and scripts, with the runtime shape, installation layout, and management flow adjusted for Codex.

## Relationship to the upstream project

Compared with the upstream `ex-skill` project, this bundle keeps the same core product direction:

- distill an ex-partner into an AI skill
- ingest memories from multiple local sources
- build Relationship Memory + Persona
- support later append, correction, rollback, and deletion

At the same time, this package was specifically reworked for Codex by:

- adapting the structure to Codex skills layout
- adapting installation and discovery paths for Codex
- adding a Codex-oriented management flow
- making generated runtime skills usable inside Codex
- rewriting documentation and packaging around Codex instead of upstream runtime assumptions

## Repository-root installation support

Yes — this bundle now **preferentially supports git-repo-root installation**.

The default resolution order is:

1. the current git repo root's `.codex/`
2. the `.codex/` location where the script itself is installed
3. user-scope fallback `~/.codex/`

So if you want to keep this package inside a git repository, the recommended structure is:

```text
<repo>/
  .codex/
    skills/
      create-ex/
      list-exes/
      delete-ex/
      let-go/
      ex-rollback/
```

When run inside that repo, generated data and runtime skills will also prefer:

- `<repo>/.codex/exes/<slug>/`
- `<repo>/.codex/skills/ex-<slug>/`
- `<repo>/.codex/skills/ex-<slug>-memory/`
- `<repo>/.codex/skills/ex-<slug>-persona/`

## Feature set

### Data sources

| Source | Format | Notes |
|---|---|---|
| WeChat chat history | WeChatMsg / Liuhen / PyWxDump export | Recommended; richest source |
| QQ chat history | txt / mht export | Good for school-era relationships |
| Moments / Weibo | screenshots | Used to infer public persona |
| Photos | JPEG / PNG with EXIF | Used for timeline and locations |
| Narration / pasted text | plain text | Your subjective memory |

### Generated skill structure

Each generated ex skill is driven by two parts:

| Part | Content |
|---|---|
| Part A — Relationship Memory | shared experiences, date locations, inside jokes, conflict patterns, sweet moments, relationship timeline |
| Part B — Persona | a 5-layer personality structure: hard rules → identity → speaking style → emotional patterns → relationship behavior |

### Runtime logic

When a message comes in, the intended logic is:

1. **Persona** decides how they would respond
2. **Memory** injects shared context and relationship-specific details
3. the final answer is produced **in their style**

### Supported tags

#### Attachment styles

- secure
- anxious
- avoidant
- disorganized

#### Love languages

- words of affirmation
- quality time
- receiving gifts
- acts of service
- physical touch

#### Personality tags

Supported labels that can be translated into concrete behavioral rules include, but are not limited to:

- talkative
- reserved-but-flirty / “闷骚”-like behavior
- tough outside, soft inside
- cold violence / silent treatment
- clingy
- independent
- macho / strong gender-role expectations
- romantic
- pragmatic
- perfectionist
- procrastinator
- workaholic
- controlling
- insecure
- revenge bedtime procrastination
- seen-but-no-reply
- instant replier
- three-day-visible social feed
- late-night voice-note sender

#### Zodiac signs

- all 12 zodiac signs are supported
- they influence how personality tags are translated into behavior rules

#### MBTI

- all 16 MBTI types are supported
- they influence communication style and decision-making patterns

### Evolution mechanism

#### 1. Memory append

- find more chat logs / photos
- analyze the incremental material
- merge it into the relevant section

#### 2. Conversation correction

- say `they wouldn't say that`
- write the fix into a Correction layer
- make it take effect immediately

#### 3. Version management

- every update can be archived automatically
- rollback is supported

## Included base skills

- `create-ex`
- `list-exes`
- `delete-ex`
- `let-go`
- `ex-rollback`

## Prerequisites

### Required

1. A working Codex environment
2. A writable Codex skills directory, usually:
   - `~/.codex/skills`
   - `$CODEX_HOME/skills`
3. `python3` available in your shell

### Optional

4. Pillow for photo EXIF support:

```bash
pip3 install Pillow
```

5. If you want higher-quality persona reconstruction, prepare some of the following first:
   - WeChat exports
   - QQ exports
   - social screenshots or text exports
   - photo folders
   - manually written memories

## Installation

### Codex

Important: Codex looks for project-scoped skills under the **git repository root** at `.codex/skills/`. Run the install command in the correct place.

### Install into the current project (run at the git repository root)

If this package already lives inside your repository, run:

```bash
bash ./install-to-project.sh
```

This installs the 5 bundled base skills into:

```text
<repo>/.codex/skills/
```

Result:

```text
<repo>/.codex/skills/
  create-ex/
  list-exes/
  delete-ex/
  let-go/
  ex-rollback/
```

### Or install globally (available in all projects)

```bash
bash ./install-global.sh
```

Default target:

```bash
${CODEX_HOME:-$HOME/.codex}/skills
```

### Dependencies (optional)

```bash
pip3 install -r requirements.txt
```

At the moment, `Pillow` is the only optional dependency, mainly used for photo EXIF extraction.

## What gets generated after use

After you actually use `create-ex`, it will typically generate:

### Data directory

- `~/.codex/exes/<slug>/`

This may contain:

- `memory.md`
- `persona.md`
- `meta.json`
- `versions/`
- `memories/`

### Runtime skill directories

- `~/.codex/skills/ex-<slug>/`
- `~/.codex/skills/ex-<slug>-memory/`
- `~/.codex/skills/ex-<slug>-persona/`

## Usage

In Codex, invoke:

```text
create-ex
```

Then provide the requested information about the ex-partner:

- codename
- basic background
- personality profile
- source material

All fields can be partially skipped if needed; a text-only description can still be used to generate the first draft.

After creation, use the generated runtime skill:

```text
ex-<slug>
```

If you want narrower modes, you can also use:

```text
ex-<slug>-memory
ex-<slug>-persona
```

For later updates, you can:

- add more logs / photos / memories
- directly say `they wouldn't say that`
- or use:
  - `list-exes`
  - `ex-rollback <slug> <version>`
  - `delete-ex <slug>`
  - `let-go <slug>`

## Script overview

Inside `create-ex/scripts/`:

- `ex_skill_manager.py` — init, generate, list, backup, rollback, delete
- `wechat_parser.py` — parse supported WeChat exports
- `qq_parser.py` — parse QQ exports
- `social_parser.py` — scan social-media folders
- `photo_analyzer.py` — try to extract EXIF from photos

## Known limitations

1. WeChat parsing is currently most reliable for `txt / json / plaintext`
2. `html / csv / sqlite` support is not fully implemented
3. Screenshot understanding still depends on the current Codex session's image capabilities
4. Photo EXIF support depends on Pillow
5. Newly generated runtime skills may be recognized more reliably in a fresh Codex session

## Privacy and safe-use boundaries

Use this only for:

- self-reflection
- emotional processing
- creative or personal experimentation
- local private use

Do not use it for:

- harassment
- impersonation abuse
- privacy invasion
- stalking, retaliation, or coercion

## Package structure

```text
前任codexskill/
  README_EN.md
  README_CN.md
  skills/
    create-ex/
    list-exes/
    delete-ex/
    let-go/
    ex-rollback/
```
