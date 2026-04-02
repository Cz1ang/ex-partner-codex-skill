#!/usr/bin/env python3
"""Manage generated ex-partner Codex skills and their backing data."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_VERSION = "v1"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).casefold()
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    candidate = re.sub(r"[^a-z0-9]+", "-", ascii_only).strip("-")
    if candidate:
        return candidate
    unicode_candidate = re.sub(r"[^\w]+", "-", value.strip(), flags=re.UNICODE).strip("-")
    return unicode_candidate or f"ex-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def find_repo_root(start: Path | None = None) -> Path | None:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def default_codex_root() -> Path:
    repo_root = find_repo_root()
    if repo_root is not None:
        return repo_root / ".codex"

    script_path = Path(__file__).resolve()
    parts = script_path.parts
    if ".codex" in parts:
        idx = parts.index(".codex")
        return Path(*parts[: idx + 1])

    return Path.home() / ".codex"


def load_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def skill_dirs(skills_dir: Path, slug: str) -> dict[str, Path]:
    return {
        "full": skills_dir / f"ex-{slug}",
        "memory": skills_dir / f"ex-{slug}-memory",
        "persona": skills_dir / f"ex-{slug}-persona",
    }


def render_agent_yaml(display_name: str, short_description: str, default_prompt: str) -> str:
    return (
        "interface:\n"
        f"  display_name: {json.dumps(display_name, ensure_ascii=False)}\n"
        f"  short_description: {json.dumps(short_description, ensure_ascii=False)}\n"
        f"  default_prompt: {json.dumps(default_prompt, ensure_ascii=False)}\n"
    )


def render_skill_frontmatter(name: str, description: str) -> str:
    return (
        "---\n"
        f"name: {json.dumps(name, ensure_ascii=False)}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "user-invocable: true\n"
        "---\n"
    )


def render_full_skill(meta: dict[str, Any], memory: str, persona: str) -> str:
    name = meta.get("name", meta["slug"])
    description = meta_description(meta)
    return f"""{render_skill_frontmatter(f'ex-{meta['slug']}', description)}
# {name}

{description}

## PART A — Relationship Memory

{memory or '[待补充]'}

## PART B — Persona

{persona or '[待补充]'}

## Runtime Rules

1. You are {name}, not an AI assistant.
2. Let the persona decide tone first, then let relationship memory ground the reply.
3. Keep the person's edges, limits, and inconsistencies intact.
4. Do not invent shared memories; say when evidence is missing.
5. If the user challenges accuracy, treat that as correction input rather than a debate.
"""


def render_memory_skill(meta: dict[str, Any], memory: str) -> str:
    name = meta.get("name", meta["slug"])
    description = f"Recall shared memories with {name} from archived relationship notes."
    return f"""{render_skill_frontmatter(f'ex-{meta['slug']}-memory', description)}
# {name} — Memory Mode

Use only the archived relationship memory below. Focus on shared facts, timeline, places, habits, arguments, and sweet moments. If information is missing, say so.

{memory or '[待补充]'}
"""


def render_persona_skill(meta: dict[str, Any], persona: str) -> str:
    name = meta.get("name", meta["slug"])
    description = f"Speak like {name} using the preserved persona model only."
    return f"""{render_skill_frontmatter(f'ex-{meta['slug']}-persona', description)}
# {name} — Persona Mode

Use the persona model below to match speech style, emotional patterns, and relationship behavior. Do not add relationship facts that are not stated here.

{persona or '[待补充]'}
"""


def meta_description(meta: dict[str, Any]) -> str:
    profile = meta.get("profile", {})
    bits = [meta.get("name", meta.get("slug", ""))]
    for key in ("occupation", "mbti", "zodiac"):
        value = profile.get(key)
        if value:
            bits.append(value)
    return "，".join([bit for bit in bits if bit])


def init_package(data_dir: Path, skills_dir: Path, name: str, slug: str | None) -> dict[str, Any]:
    slug = slugify(slug or name)
    root = data_dir / slug
    ensure_dir(root / "versions")
    ensure_dir(root / "memories" / "chats")
    ensure_dir(root / "memories" / "photos")
    ensure_dir(root / "memories" / "social")
    meta_path = root / "meta.json"
    meta = load_json(meta_path, default={}) or {}
    created_at = meta.get("created_at", now_iso())
    meta.update(
        {
            "name": name,
            "slug": slug,
            "created_at": created_at,
            "updated_at": now_iso(),
            "version": meta.get("version", DEFAULT_VERSION),
            "profile": meta.get("profile", {}),
            "tags": meta.get("tags", {}),
            "impression": meta.get("impression", ""),
            "memory_sources": meta.get("memory_sources", []),
            "corrections_count": meta.get("corrections_count", 0),
            "generated_skills": {k: str(v) for k, v in skill_dirs(skills_dir, slug).items()},
        }
    )
    save_json(meta_path, meta)
    return meta


def backup_package(data_dir: Path, slug: str) -> Path:
    root = data_dir / slug
    meta = load_json(root / "meta.json")
    current_version = meta.get("version", "v0")
    backup_name = f"{current_version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir = root / "versions" / backup_name
    ensure_dir(backup_dir)
    for name in ["memory.md", "persona.md", "meta.json"]:
        source = root / name
        if source.exists():
            shutil.copy2(source, backup_dir / name)
    return backup_dir


def write_generated_skill(path: Path, skill_md: str, openai_yaml: str) -> None:
    ensure_dir(path / "agents")
    write_text(path / "SKILL.md", skill_md)
    write_text(path / "agents" / "openai.yaml", openai_yaml)


def combine_package(data_dir: Path, skills_dir: Path, slug: str) -> dict[str, Any]:
    root = data_dir / slug
    meta_path = root / "meta.json"
    if not meta_path.exists():
        raise SystemExit(f"missing meta.json for slug: {slug}")
    meta = load_json(meta_path)
    meta["slug"] = slug
    meta["generated_skills"] = {k: str(v) for k, v in skill_dirs(skills_dir, slug).items()}
    meta["updated_at"] = now_iso()
    memory = (root / "memory.md").read_text(encoding="utf-8") if (root / "memory.md").exists() else ""
    persona = (root / "persona.md").read_text(encoding="utf-8") if (root / "persona.md").exists() else ""

    targets = skill_dirs(skills_dir, slug)
    display_name = meta.get("name", slug)
    write_generated_skill(
        targets["full"],
        render_full_skill(meta, memory, persona),
        render_agent_yaml(f"Ex · {display_name}", "Chat with the generated ex persona", f"Reply as {display_name} using the full memory + persona package."),
    )
    write_generated_skill(
        targets["memory"],
        render_memory_skill(meta, memory),
        render_agent_yaml(f"Ex Memory · {display_name}", "Recall shared relationship memories", f"Answer using only the archived relationship memory for {display_name}."),
    )
    write_generated_skill(
        targets["persona"],
        render_persona_skill(meta, persona),
        render_agent_yaml(f"Ex Persona · {display_name}", "Use the preserved persona model", f"Speak like {display_name} using only the persona model."),
    )
    save_json(meta_path, meta)
    return meta


def list_packages(data_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not data_dir.exists():
        return rows
    for child in sorted(data_dir.iterdir()):
        if not child.is_dir():
            continue
        meta_path = child / "meta.json"
        if not meta_path.exists():
            continue
        meta = load_json(meta_path)
        rows.append(meta)
    return rows


def delete_package(data_dir: Path, skills_dir: Path, slug: str) -> None:
    root = data_dir / slug
    if root.exists():
        shutil.rmtree(root)
    for folder in skill_dirs(skills_dir, slug).values():
        if folder.exists():
            shutil.rmtree(folder)


def bump_version(version: str) -> str:
    match = re.fullmatch(r"v(\d+)", version or "")
    if not match:
        return DEFAULT_VERSION
    return f"v{int(match.group(1)) + 1}"


def rollback_package(data_dir: Path, skills_dir: Path, slug: str, version: str) -> dict[str, Any]:
    root = data_dir / slug
    versions_dir = root / "versions"
    matches = sorted([path for path in versions_dir.iterdir() if path.name == version or path.name.startswith(version)])
    if not matches:
        raise SystemExit(f"version not found: {version}")
    backup_package(data_dir, slug)
    target = matches[-1]
    for name in ["memory.md", "persona.md", "meta.json"]:
        source = target / name
        if source.exists():
            shutil.copy2(source, root / name)
    return combine_package(data_dir, skills_dir, slug)


def print_list(rows: list[dict[str, Any]]) -> None:
    if not rows:
        print("还没有创建任何 ex skills。")
        return
    print(f"共 {len(rows)} 个 ex skills：\n")
    for meta in rows:
        profile = meta.get("profile", {})
        desc = " · ".join([value for value in [profile.get("occupation"), profile.get("city")] if value])
        print(f"  ex-{meta.get('slug')}  —  {meta.get('name', meta.get('slug'))}")
        if desc:
            print(f"    {desc}")
        print(f"    版本 {meta.get('version', '?')} · 更新于 {meta.get('updated_at', '?')[:10]}")
        print()


def list_versions(data_dir: Path, slug: str) -> list[str]:
    versions_dir = data_dir / slug / "versions"
    if not versions_dir.exists():
        return []
    return sorted([path.name for path in versions_dir.iterdir() if path.is_dir()], reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage generated ex-partner Codex skills")
    parser.add_argument("action", choices=["init", "combine", "list", "backup", "rollback", "delete", "versions"])
    parser.add_argument("--data-dir")
    parser.add_argument("--skills-dir")
    parser.add_argument("--slug")
    parser.add_argument("--name")
    parser.add_argument("--version")
    args = parser.parse_args()

    codex_root = default_codex_root()
    data_dir = Path(args.data_dir).expanduser().resolve() if args.data_dir else (codex_root / "exes").resolve()
    skills_dir = Path(args.skills_dir).expanduser().resolve() if args.skills_dir else (codex_root / "skills").resolve()

    if args.action == "init":
        if not args.name:
            raise SystemExit("--name is required for init")
        meta = init_package(data_dir, skills_dir, args.name, args.slug)
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return
    if args.action == "list":
        print_list(list_packages(data_dir))
        return
    if args.action == "versions":
        if not args.slug:
            raise SystemExit("--slug is required for versions")
        versions = list_versions(data_dir, args.slug)
        if not versions:
            print("没有历史版本。")
        else:
            print("\n".join(versions))
        return
    if not args.slug:
        raise SystemExit("--slug is required for this action")
    if args.action == "backup":
        backup_dir = backup_package(data_dir, args.slug)
        meta_path = data_dir / args.slug / "meta.json"
        meta = load_json(meta_path)
        meta["version"] = bump_version(meta.get("version", DEFAULT_VERSION))
        meta["updated_at"] = now_iso()
        save_json(meta_path, meta)
        print(str(backup_dir))
        return
    if args.action == "combine":
        meta = combine_package(data_dir, skills_dir, args.slug)
        print(json.dumps(meta.get("generated_skills", {}), ensure_ascii=False, indent=2))
        return
    if args.action == "rollback":
        if not args.version:
            raise SystemExit("--version is required for rollback")
        meta = rollback_package(data_dir, skills_dir, args.slug, args.version)
        print(json.dumps(meta.get("generated_skills", {}), ensure_ascii=False, indent=2))
        return
    if args.action == "delete":
        delete_package(data_dir, skills_dir, args.slug)
        print(f"deleted:{args.slug}")
        return


if __name__ == "__main__":
    main()
