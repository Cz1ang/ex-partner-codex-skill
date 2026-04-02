# Task 1 — Installation verification

Date: 2026-04-02
Worker: worker-1

## Scope
- Verify `install-to-project.sh` in a clean temp git repo.
- Verify `install-global.sh` against an isolated `CODEX_HOME`.
- Verify optional dependency behavior for `Pillow` / `photo_analyzer.py`.

## Environment
- Repo under test: `/mnt/c/Users/묘은위/Downloads/前任codexskill/.omx/team/verify-ex-partner-codex-skill/worktrees/worker-1`
- Temp workspace: `/tmp/task1-verify-fccqb3yd`
- `Pillow` present in current Python env: no (`ModuleNotFoundError: No module named 'PIL'`)

## Checks

### PASS — `install-to-project.sh` rejects non-git directories
Command:
```bash
cd /tmp/task1-verify-fccqb3yd/nonrepo
bash /mnt/c/Users/묘은위/Downloads/前任codexskill/.omx/team/verify-ex-partner-codex-skill/worktrees/worker-1/install-to-project.sh
```
Result:
- exit code: `1`
- stderr: `Error: run this script from a git repository root (or any path inside the target repo).`

### PASS — `install-to-project.sh` installs the expected skill set into a clean temp repo
Commands:
```bash
cd /tmp/task1-verify-fccqb3yd/project-repo
git init
bash /mnt/c/Users/묘은위/Downloads/前任codexskill/.omx/team/verify-ex-partner-codex-skill/worktrees/worker-1/install-to-project.sh
python3 .codex/skills/create-ex/scripts/ex_skill_manager.py list
```
Result:
- install exit code: `0`
- installed path: `/tmp/task1-verify-fccqb3yd/project-repo/.codex/skills`
- installed skills:
  - `.codex/skills/create-ex`
  - `.codex/skills/delete-ex`
  - `.codex/skills/ex-rollback`
  - `.codex/skills/let-go`
  - `.codex/skills/list-exes`
- manager list exit code: `0`
- manager stdout: `还没有创建任何 ex skills。`

### PASS — `install-global.sh` installs into an isolated `CODEX_HOME`
Commands:
```bash
CODEX_HOME=/tmp/task1-verify-fccqb3yd/codehome \
  bash /mnt/c/Users/묘은위/Downloads/前任codexskill/.omx/team/verify-ex-partner-codex-skill/worktrees/worker-1/install-global.sh
CODEX_HOME=/tmp/task1-verify-fccqb3yd/codehome \
  python3 /tmp/task1-verify-fccqb3yd/codehome/skills/create-ex/scripts/ex_skill_manager.py list
```
Result:
- install exit code: `0`
- installed path: `/tmp/task1-verify-fccqb3yd/codehome/skills`
- installed skills:
  - `skills/create-ex`
  - `skills/delete-ex`
  - `skills/ex-rollback`
  - `skills/let-go`
  - `skills/list-exes`
- manager list exit code: `0`
- manager stdout: `还没有创建任何 ex skills。`

### FAIL — optional dependency fallback loses filenames without Pillow
Command:
```bash
python3 skills/create-ex/scripts/photo_analyzer.py \
  --dir /tmp/task1-verify-fccqb3yd/photos \
  --output /tmp/task1-verify-fccqb3yd/photo-report.md
```
Result:
- exit code: `0`
- stdout: `分析完成，结果已写入 /tmp/task1-verify-fccqb3yd/photo-report.md`
- output excerpt:

```md
# 照片时间线分析

扫描目录：/tmp/task1-verify-fccqb3yd/photos
总照片数：1
有时间信息：0
有位置信息：0

## 无时间信息的照片（1 张）

- unknown

⚠️ Pillow 未安装，仅列出文件。安装方法：pip3 install Pillow
```

Expected fallback behavior from the script comment and README wording is “list files only” when Pillow is missing, but the current fallback drops both `file` and `path`, so the generated report shows `unknown` instead of the actual filename.

## Additional verification

### PASS — shell syntax
Command:
```bash
bash -n install-global.sh
bash -n install-to-project.sh
```
Result:
- both scripts passed shell parsing

### PASS — Python syntax compilation
Command:
```bash
python3 -m compileall skills
```
Result:
- all bundled Python scripts compiled successfully

## Summary
- Installation flows passed in both project-local and global-isolated modes.
- Optional dependency handling is partially degraded: `photo_analyzer.py` does not crash without Pillow, but the fallback report loses filenames and prints `unknown` entries.
