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

### Option A: install from GitHub with the skills installer

If your agent supports the `skills` installer pattern:

```bash
npx skills@latest add HUAFIRE777/autorunne-grill
```

Then select `autorunne-grill` for your coding agent if prompted.

### Option B: install with pipx / pip

This repo also ships a tiny Python installer CLI.

```bash
pipx install git+https://github.com/HUAFIRE777/autorunne-grill.git
autorunne-grill install
```

Or with pip:

```bash
python -m pip install git+https://github.com/HUAFIRE777/autorunne-grill.git
python -m autorunne_grill install
```

This copies the skill to:

```text
~/.hermes/skills/productivity/autorunne-grill/SKILL.md
```

### Option C: manual install

```bash
mkdir -p ~/.hermes/skills/productivity/autorunne-grill
cp skills/productivity/autorunne-grill/SKILL.md ~/.hermes/skills/productivity/autorunne-grill/SKILL.md
```

## Prerequisite

Use this together with Autorunne:

```bash
pipx install autorunne
cd your-project
autorunne open
```

After that, your AI agent can use `autorunne-grill` when you ask for feature changes.

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

## PyPI status

The project is packaged so it can be published to PyPI later. PyPI publishing requires the maintainer to configure a PyPI trusted publisher for this GitHub repo first.

Users do **not** need PyPI for one-line GitHub installation via:

```bash
npx skills@latest add HUAFIRE777/autorunne-grill
```

PyPI is useful if you want this install path:

```bash
pipx install autorunne-grill
```

## License

MIT
