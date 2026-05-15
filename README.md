# autorunne-grill

**Project-aware grilling for safer AI feature changes.**

`autorunne-grill` is a small open-source skill package that adapts the popular `grill-me` idea for real Autorunne-backed development projects.

Instead of asking endless questions from a blank slate, it tells AI coding agents to:

1. read the repo's Autorunne state first;
2. understand what has already been built, verified, and decided;
3. classify the requested feature change;
4. ask only the questions that are still necessary;
5. define a safe change boundary;
6. implement the smallest safe slice;
7. validate and record the result back into Autorunne.

中文一句话：

> `autorunne-grill` 会在 AI 改代码前，先读取 Autorunne 项目状态，再帮小白确认安全修改边界。

## Why this exists

The original `grill-me` skill is useful for stress-testing plans, but it does not know your project's current state.

For beginner-friendly real development, the AI should not ask questions like:

- What is this project?
- What command runs tests?
- What did we decide last time?
- Is there already an active task?

If the repo uses Autorunne, those answers should come from `.autorunne/` first.

`autorunne-grill` is the safety layer that sits beside Autorunne:

| Tool | Responsibility |
| --- | --- |
| Autorunne | Project memory, tasks, decisions, validation, handoff state |
| autorunne-grill | Pre-change questioning, safe boundary, beginner-friendly feature review |

## Install

### Option A: install with pipx from PyPI

Recommended public install path:

```bash
pipx install autorunne-grill
autorunne-grill install
```

This installs the skill for your Hermes user profile:

```text
~/.hermes/skills/productivity/autorunne-grill/SKILL.md
```

If you want the skill copied into one specific Autorunne repo so Codex/Claude-style agents can see it from the project itself:

```bash
cd your-project
autorunne open --path .
autorunne-grill install --scope repo --repo .
```

This creates agent instructions for Codex-style agents, Claude Code, and Cursor:

```text
.agents/skills/autorunne-grill/SKILL.md
.claude/skills/autorunne-grill/SKILL.md
.cursor/rules/autorunne-grill.mdc
```

Cursor support is repo-local: the installer writes a Cursor rule that tells Cursor to read `.autorunne/` first, classify the change, state the safe boundary, and record the result with `autorunne ingest --source cursor` / `autorunne finish`.

For both user-level and repo-local install:

```bash
autorunne-grill install --scope both --repo .
```

Or with pip:

```bash
python -m pip install autorunne-grill
python -m autorunne_grill install
```

### Option B: install from GitHub with the skills installer

If your agent supports the `skills` installer pattern:

```bash
npx skills@latest add HUAFIRE777/autorunne-grill
```

Then select `autorunne-grill` for your coding agent if prompted.

### Option C: install directly from GitHub

```bash
pipx install git+https://github.com/HUAFIRE777/autorunne-grill.git
autorunne-grill install
```

This copies the skill to:

```text
~/.hermes/skills/productivity/autorunne-grill/SKILL.md
```

### Option D: manual install

```bash
mkdir -p ~/.hermes/skills/productivity/autorunne-grill
cp skills/productivity/autorunne-grill/SKILL.md ~/.hermes/skills/productivity/autorunne-grill/SKILL.md
```

## Prerequisite

Use this together with Autorunne:

```bash
pipx install autorunne
cd your-project
autorunne open --path .
autorunne-grill install --scope repo --repo .
```

After that, your AI agent can use `autorunne-grill` when you ask for feature changes.

## How to use in real development

A practical beginner workflow looks like this:

1. Open your project folder.
2. Run `autorunne open --path .` once to create or refresh project memory.
3. Install `autorunne-grill` globally or into the repo.
4. Tell the AI the product task in normal language.
5. The AI should read Autorunne state, classify risk, make the smallest safe change, test it, and finish with Autorunne.

Example prompt:

```text
用 autorunne-grill 帮我先看一下安全边界，然后把统计卡片展示到首页。改完跑测试，并记录到 Autorunne。
```

For a low-risk change, the agent should not waste time asking questions. It should produce a compact safety summary like:

```text
我先看了 Autorunne 状态：项目已准备好，上次测试通过，没有活跃任务。
这次改动属于：普通功能改动。
安全边界：只展示现有 /api/stats 数据。
不会改：不改存储格式、不改 API 返回结构、不改提交线索流程。
验证方式：python -m pytest -q。
需要确认：无，我会按最小安全切片直接做。
```

## Agent support

Repo-local install now covers the main coding-agent entry files:

| Agent | Installed file |
| --- | --- |
| Codex-style agents | `.agents/skills/autorunne-grill/SKILL.md` |
| Claude Code | `.claude/skills/autorunne-grill/SKILL.md` |
| Cursor | `.cursor/rules/autorunne-grill.mdc` |

The Cursor rule is deliberately small and practical. It tells Cursor to read `.autorunne/` first, avoid questions the repo can answer, make the smallest safe slice, run validation, and record the work back through Autorunne.

## Example

User:

> 帮我加一个登录功能。

Good agent behavior:

```text
我先看了 Autorunne 状态：当前项目是课程线索收集 Demo，上次验证通过，目前没有活跃任务。
这次改动属于：中等功能改动，因为登录会影响权限和页面流程。
安全边界：先做管理员登录，用来查看线索。
不会改：暂时不做学员会员中心、不做第三方 OAuth、不改现有访客提交线索流程。
可能影响：后台页面、会话处理、线索列表入口、测试。
验证方式：python -m pytest -q。
需要确认：登录是给管理员用还是给学员用？我的建议是先做管理员登录。
```

## Repository layout

```text
skills/productivity/autorunne-grill/SKILL.md   # the actual skill
src/autorunne_grill/                           # optional Python installer CLI
tests/                                         # validation tests
```

## Development

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m build
```

## PyPI

`autorunne-grill` is published on PyPI:

```bash
pipx install autorunne-grill
```

PyPI page:

```text
https://pypi.org/project/autorunne-grill/
```

GitHub and `npx skills@latest add HUAFIRE777/autorunne-grill` remain available as alternative install paths.

## License

MIT
