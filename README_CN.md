# 前任 Codex Skill

## 项目来源说明

这个包是**基于上游项目进行的 Codex 定向二次开发版本**：

- 上游项目：https://github.com/therealXiaomanChu/ex-skill

也就是说，这不是把上游仓库原样复制后直接打包。  
它是在上游 `ex-skill` 的产品思路、交互流程、模板和脚本基础上，针对 **Codex 运行环境** 做的适配开发与重新封装。

## 我们和上游项目的关系

相对上游 `ex-skill`，这个包保留了相同的核心目标：

- 把“前任 / 旧关系对象”蒸馏成一个 AI skill
- 从多种本地材料中提取记忆和人格信息
- 生成 Relationship Memory + Persona
- 支持后续追加、纠正、回滚和删除

同时，这个包已经针对 Codex 做了专门调整，包括：

- 改成 Codex 的 skills 目录结构
- 改成 Codex 的技能发现与安装路径
- 增加适合 Codex 的管理脚本流转
- 让生成后的 runtime skills 能在 Codex 中使用
- 文档与安装方式也改成面向 Codex，而不是直接沿用上游的原始运行假设

## 仓库级安装支持说明

支持，而且现在已经改成**优先支持 git 仓库根目录安装**。

默认解析顺序是：

1. 当前 git 仓库根目录下的 `.codex/`
2. 如果脚本本身安装在某个 `.codex/` 下，则使用那个安装位置
3. 最后才回退到用户级 `~/.codex/`

也就是说，如果你们准备把它直接放进 git 仓库里，推荐结构就是：

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

这样在仓库里运行时，生成的数据和 runtime skills 也会优先落在：

- `<repo>/.codex/exes/<slug>/`
- `<repo>/.codex/skills/ex-<slug>/`
- `<repo>/.codex/skills/ex-<slug>-memory/`
- `<repo>/.codex/skills/ex-<slug>-persona/`

## 功能特性

### 数据源

| 来源 | 格式 | 备注 |
|---|---|---|
| 微信聊天记录 | WeChatMsg / 留痕 / PyWxDump 导出 | 推荐，信息最丰富 |
| QQ 聊天记录 | txt / mht 导出 | 适合学生时代的恋情 |
| 朋友圈 / 微博 | 截图 | 提取公开人设 |
| 照片 | JPEG / PNG（含 EXIF） | 提取时间线和地点 |
| 口述 / 粘贴 | 纯文本 | 你的主观记忆 |

### 生成的 Skill 结构

每个前任 Skill 由两部分组成，共同驱动输出：

| 部分 | 内容 |
|---|---|
| Part A — Relationship Memory | 共同经历、约会地点、inside jokes、争吵模式、甜蜜瞬间、关系时间线 |
| Part B — Persona | 5 层性格结构：硬规则 → 身份 → 说话风格 → 情感模式 → 关系行为 |

### 运行逻辑

收到消息后，整体逻辑是：

1. **Persona** 先判断 ta 会怎么回
2. **Memory** 再补充你们之间的共同记忆
3. 最终**用 ta 的方式输出**

### 支持的标签

#### 依恋类型

- 安全型
- 焦虑型
- 回避型
- 混乱型

#### 爱的语言

- 肯定的言辞
- 精心的时刻
- 接受礼物
- 服务的行动
- 身体的接触

#### 性格标签

支持并可用于翻译成具体行为规则的标签包括但不限于：

- 话痨
- 闷骚
- 嘴硬心软
- 冷暴力
- 粘人
- 独立
- 大男 / 女子主义
- 浪漫主义
- 实用主义
- 完美主义
- 拖延症
- 工作狂
- 控制欲
- 没有安全感
- 报复性熬夜
- 已读不回
- 秒回选手
- 朋友圈三天可见
- 半夜发语音

#### 星座

- 十二星座全支持
- 影响性格标签的翻译规则

#### MBTI

- 16 型全支持
- 影响沟通风格和决策模式

### 进化机制

#### 1. 追加记忆

- 找到更多聊天记录 / 照片
- 自动分析增量内容
- merge 进对应部分

#### 2. 对话纠正

- 说 `ta不会这样说`
- 写入 Correction 层
- 立即生效

#### 3. 版本管理

- 每次更新自动存档
- 支持回滚

## 包含的基础 skills

- `create-ex`
- `list-exes`
- `delete-ex`
- `let-go`
- `ex-rollback`

## 运行前置条件

### 必需

1. 你已经能正常使用 Codex
2. 你有可写的 Codex skills 目录，通常是：
   - `~/.codex/skills`
   - `$CODEX_HOME/skills`
3. 系统里有 `python3`

### 可选

4. 如果你要分析照片 EXIF，建议安装 Pillow：

```bash
pip3 install Pillow
```

5. 如果你想要更高质量还原，建议提前准备：
   - 微信聊天导出
   - QQ 聊天导出
   - 社交媒体截图或文本导出
   - 照片目录
   - 手动回忆文本

## 安装

### Codex

重要：Codex 从 **git 仓库根目录** 的 `.codex/skills/` 查找项目级 skill。请在正确的位置执行。

### 安装到当前项目（在 git 仓库根目录执行）

如果你已经把这个包放进仓库里，直接运行：

```bash
bash ./install-to-project.sh
```

这会把内置的 5 个基础 skills 安装到当前仓库的：

```text
<repo>/.codex/skills/
```

安装后结构类似：

```text
<repo>/.codex/skills/
  create-ex/
  list-exes/
  delete-ex/
  let-go/
  ex-rollback/
```

### 或安装到全局（所有项目都能用）

```bash
bash ./install-global.sh
```

默认安装位置：

```bash
${CODEX_HOME:-$HOME/.codex}/skills
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

目前唯一的可选依赖是 `Pillow`，主要用于照片 EXIF 分析。

## 安装后会生成什么

当你实际使用 `create-ex` 创建角色后，通常会生成：

### 数据目录

- `~/.codex/exes/<slug>/`

其中可能包含：

- `memory.md`
- `persona.md`
- `meta.json`
- `versions/`
- `memories/`

### 运行时技能目录

- `~/.codex/skills/ex-<slug>/`
- `~/.codex/skills/ex-<slug>-memory/`
- `~/.codex/skills/ex-<slug>-persona/`

## 使用

在 Codex 中输入：

```text
create-ex
```

按提示输入前任的：

- 代号
- 基本信息
- 性格画像
- 数据来源

所有字段都可以跳过一部分；即使只有描述，也可以先生成。

完成后，使用生成的 runtime skill：

```text
ex-<slug>
```

如果你要更聚焦的模式，也可以使用：

```text
ex-<slug>-memory
ex-<slug>-persona
```

如果后续还要继续调整，可以：

- 追加更多聊天记录 / 照片 / 回忆
- 直接说 `ta不会这样说`
- 或使用：
  - `list-exes`
  - `ex-rollback <slug> <version>`
  - `delete-ex <slug>`
  - `let-go <slug>`

## 脚本说明

位于 `create-ex/scripts/`：

- `ex_skill_manager.py`：初始化、生成、列表、备份、回滚、删除
- `wechat_parser.py`：解析部分微信导出
- `qq_parser.py`：解析 QQ 导出
- `social_parser.py`：扫描社交媒体目录
- `photo_analyzer.py`：尝试读取照片 EXIF

## 已知限制

1. 微信解析当前对 `txt / json / plaintext` 更可靠
2. `html / csv / sqlite` 支持并未完全补齐
3. 社交媒体截图的“语义理解”依赖 Codex 当前会话能力
4. 照片 EXIF 对 Pillow 有依赖
5. 新生成的 runtime skills 有时需要新开 Codex 会话才会稳定识别

## 隐私与使用边界

请仅用于：

- 自我整理
- 情感回顾
- 创作或实验
- 本地私人使用

不要用于：

- 骚扰真人
- 冒充真人
- 侵犯隐私
- 跟踪、报复、纠缠

## 文件结构

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
