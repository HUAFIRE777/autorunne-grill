---
name: autorunne-grill
description: Use when a user wants to add, change, remove, or redesign a feature in an Autorunne-backed repo. Read Autorunne state first, identify the safe change boundary, ask only necessary questions, then implement and verify the smallest safe slice.
version: 0.1.1
author: Autorunne Grill contributors
license: MIT
metadata:
  hermes:
    tags: [autorunne, grill-me, feature-change, beginner-friendly, project-state]
    related_skills: [autorunne-dev-workflow, systematic-debugging, writing-plans, test-driven-development]
---

# Autorunne Grill

## Overview

Autorunne Grill is a project-aware version of the classic `grill-me` skill.

The original `grill-me` asks relentless questions about a plan. Autorunne Grill does something more practical for real development: it first reads the repo's Autorunne project memory, then asks only the questions that are still necessary to keep the next feature change inside a safe boundary.

Use it as a pre-change safety gate for beginner-friendly AI development. The user should be able to say "add a login feature" or "change the checkout page" without knowing how to manage engineering workflow details. The agent reads Autorunne, checks the current project state, narrows the change, records the task, implements the smallest safe slice, verifies it, and finishes cleanly.

## When to Use

Use this skill when all three are true:

- the repo has `.autorunne/`, `.autorunne/views/`, or Autorunne-generated handoff files;
- the user asks to add, change, remove, redesign, or "just tweak" a feature;
- the change could affect product behavior, project direction, data, UI flow, tests, or integration points.

Good triggers:

- "帮我加一个登录功能"
- "改一下支付页面"
- "把线索导出成 CSV"
- "优化自动记录逻辑"
- "重做这个页面"
- "加一个会员中心"
- "grill this plan, but use Autorunne state first"

Do not use this for:

- pure explanation with no project change;
- simple typo fixes with no behavior impact;
- one-off shell questions unrelated to the repo;
- tasks where the user explicitly asks for no planning and the change is obviously tiny.

## Core Rule

Do not grill the user from a blank slate.

First read Autorunne state and the relevant code. Then ask the fewest questions needed to safely proceed.

If a question can be answered by reading `.autorunne/`, generated views, tests, README, package files, routes, schema files, or existing code, answer it yourself instead of asking the user.

## Required Read Order

Before asking design questions, inspect Autorunne state in this order when the files exist:

1. `.autorunne/views/STATUS.md`
2. `.autorunne/views/START_HERE.md`
3. `.autorunne/views/PROJECT_CONTEXT.md`
4. `.autorunne/views/NEXT_ACTION.md`
5. `.autorunne/views/COMMANDS.md`
6. `.autorunne/TASKS.md`
7. `.autorunne/DECISIONS.md`
8. `.autorunne/NEXT_ACTION.md`
9. `.autorunne/PROJECT_CONTEXT.md`
10. `.autorunne/state/current.json`
11. `.autorunne/snapshots/latest.json`

Then inspect only the relevant project files needed to understand the requested change. Do not scan the whole repo blindly unless the state files are missing or misleading.

## Change Classification

After reading state, classify the request before implementation:

| Class | Meaning | Default behavior |
| --- | --- | --- |
| Tiny safe change | Copy, label, styling, small config, doc-visible behavior with low blast radius | Usually proceed after stating boundary; no user question unless ambiguous |
| Normal feature change | New behavior contained to one area, with tests or validation available | Ask 0-2 necessary questions, recommend an answer, then implement smallest slice |
| Risky architecture change | Auth, payment, data model, storage, multi-agent workflow, routing, permissions, migration, public API | Ask one key question at a time and require a safe slice before coding |
| Unclear requirement | User intent is too vague to safely choose a direction | Ask one focused question with a recommended default |
| Conflicts with current state | Active task, failed validation, or existing decision makes the requested change risky | Explain the conflict simply and propose the safest next step |
| Blocked | Missing repo state, broken install, failing baseline, or no reliable validation path | Fix or report the blocker before changing product code |

## Beginner-Friendly Output Shape

Keep the user-facing explanation simple. Avoid architecture jargon unless the user asks for it.

Before coding, produce a compact safety summary:

```text
我先看了 Autorunne 状态：<current state in one sentence>
这次改动属于：<classification>
安全边界：<what will change>
不会改：<what is explicitly out of scope>
可能影响：<files/modules/user flows>
验证方式：<test/build/smoke command>
需要确认：<0 or 1 question, with recommendation>
```

If no question is needed, say so and proceed.

## Question Discipline

Ask at most one question at a time.

For every question, include:

1. the question;
2. why it matters in plain language;
3. your recommended answer;
4. what you will do if the user accepts the recommendation.

Example:

```text
需要确认 1 个问题：这个登录是给管理员看线索用，还是给学员登录看课程用？
为什么问：这两个方向会影响数据库、页面和权限设计。
我的建议：先做管理员登录，因为当前项目是线索收集系统，这一步最小、风险最低。
如果你同意，我会只做管理员登录，不做学员会员中心。
```

Do not ask broad questions like "What tech stack is this?" or "Where is the page?" if Autorunne or code can answer them.

## Safe Boundary Template

Before implementation, define the boundary explicitly:

- **Will change:** concrete behavior and files/modules likely touched.
- **Will not change:** tempting but out-of-scope items.
- **Existing behavior to preserve:** user flows that must keep working.
- **Validation:** exact command or manual smoke path.
- **Rollback note:** how to undo or reduce risk if the change fails.

For beginner projects, prefer smaller slices over complete systems.

Examples:

- For "add login": first add admin-only login, not a full member platform.
- For "add payment": first add a fake/test payment flow or checkout button boundary, not production settlement.
- For "export leads": first add CSV export for existing fields, not analytics dashboards.
- For "redesign page": first change one page/component, not the whole design system.

## Autorunne Recording Protocol

Once the safe boundary is clear, keep Autorunne state updated.

Preferred flow:

1. If this is a fresh user task and no matching active task exists, record it:
   ```bash
   autorunne ingest --source <agent> --task "<user task>" --next "<small safe next action>"
   ```
2. If using an older Autorunne version or ingest is unavailable, use:
   ```bash
   autorunne start --task "<user task>" --next "<small safe next action>"
   ```
3. Implement the smallest safe slice.
4. Checkpoint after meaningful progress when the slice is not complete:
   ```bash
   autorunne checkpoint
   ```
5. Validate with the repo's real command from `.autorunne/views/COMMANDS.md`, README, package scripts, or test files.
6. Finish only after validation:
   ```bash
   autorunne finish --summary "<what changed>" --validate "<command>" --next "<next safe action>"
   ```

Treat these as internal workflow steps. Do not ask the user whether to run routine Autorunne recording commands unless the command would affect external services, secrets, deployment, billing, or destructive data.

## Implementation Rules

1. Read state before questions.
2. Read relevant code before questions when code can answer the question.
3. Prefer the smallest safe slice.
4. Do not overwrite existing product decisions without calling out the conflict.
5. Preserve currently working flows.
6. Add or update tests when a behavior changes.
7. Run the most relevant validation command before finishing.
8. Record the result in Autorunne after validation.
9. Report changed files, validation result, and Autorunne commands at the end.

## Handling Missing or Weak Autorunne State

If `.autorunne/` is missing, do not pretend this is an Autorunne-backed repo. Tell the user the skill works best after running Autorunne:

```bash
autorunne open
```

If `.autorunne/` exists but generated views are missing or stale, refresh before grilling when safe:

```bash
AUTORUNNE_DISABLE_UPDATE_CHECK=1 autorunne sync --path .
```

If the baseline validation is already failing, do not mix baseline breakage with the new feature. Report:

- current failure;
- whether it blocks the requested change;
- the smallest repair or isolation plan.

## Examples

### Example 1: Add login to a course lead demo

User: "帮我加一个登录功能。"

Good response after reading Autorunne:

```text
我看了 Autorunne 状态：这是一个课程线索收集 Demo，上次验证通过，目前没有活跃任务。
这次改动属于：中等功能改动，因为登录会影响权限和页面流程。
安全边界：先做管理员登录，用来查看线索。
不会改：暂时不做学员会员中心、不做第三方 OAuth、不改现有访客提交线索流程。
可能影响：后台页面、会话处理、线索列表入口、测试。
验证方式：python -m pytest -q，另外手动打开首页提交一条线索。
需要确认：登录是给管理员用还是给学员用？我的建议是先做管理员登录。
```

### Example 2: Export leads

User: "把线索导出成 Excel。"

Better safe slice:

```text
我看了当前状态：项目已有线索存储和测试命令。
这次属于普通功能改动。
建议先做 CSV 导出，不直接做 Excel，因为 CSV 更小、更稳定，也能被 Excel 打开。
如果你同意，我会新增 /leads.csv 或后台导出按钮，保留现有线索提交流程不变。
```

### Example 3: Payment flow

User: "加支付。"

Good grill:

```text
这次属于高风险改动，因为支付会影响订单状态、金额、回调和真实资金。
我建议第一步只做测试支付边界：页面上出现购买按钮，生成本地订单状态，不接真实支付渠道。
需要确认：你现在是要真实收款，还是先做可演示的购买流程？
我的建议：先做可演示流程，等产品路径确定后再接真实支付。
```

## End-of-Task Report

At the end, report compactly:

```text
完成：<one sentence>
改动文件：<files>
验证：<command + pass/fail>
Autorunne：<ingest/start/checkpoint/finish commands used>
下一步：<next safe action>
```

If GitHub push, release, deployment, or external APIs are involved, report those separately and verify them directly.

## Common Pitfalls

1. **Asking from ignorance.** Do not ask the user for facts already present in Autorunne or code.
2. **Over-grilling tiny changes.** A copy tweak should not turn into a design interview.
3. **Building the full dream feature.** For beginners, full auth/payment/member systems are usually too large. Choose the smallest safe slice.
4. **Ignoring active tasks.** If Autorunne shows an active task, do not silently start a conflicting one.
5. **Skipping validation.** The point is safe change, not just confident text.
6. **Recording noisy state.** Autorunne summaries should focus on the current slice, not dump unrelated dirty files.
7. **Asking the user to manage workflow.** The user assigns the task; the agent manages Autorunne recording unless there is a risky side effect.

## Verification Checklist

Before finishing any Autorunne Grill task:

- [ ] Autorunne state was read first, or missing state was reported honestly.
- [ ] The change was classified.
- [ ] The safe boundary was stated.
- [ ] Only necessary questions were asked.
- [ ] Each question included a recommended answer.
- [ ] The smallest safe slice was implemented.
- [ ] Relevant validation ran.
- [ ] Autorunne task/checkpoint/finish state was updated when code changed.
- [ ] Final report includes changed files, validation, Autorunne commands, and next action.
