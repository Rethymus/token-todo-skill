# Goal and prompt cookbook

Use these templates as starting points. Replace every bracketed field with user-confirmed information. A Goal is a durable description of an approved boundary; it is not a quota monitor and does not grant permission beyond the text it contains.

## Canonical Goal template (English)

```text
Goal: Token Todo — bounded maintenance for [project]

Use $token-todo for this run.

Project and scope:
- Repository: [path or repository name]
- Allowed task IDs: [TT-###, TT-###]
- Allowed paths: [paths]
- Out of scope: [features, production, migrations, etc.]
- Current target and reason: [what should be true now, and why it remains valuable without expiry pressure]

User-provided resource envelope:
- Source: [periodic plan / temporary grant / other]
- Eligible capacity cap: [number/range] [user-defined work units]
- Leave untouched for next workday: [capacity reserve]
- Eligible until: [date/time] in [user timezone]
- Hard execution timebox: [duration]
- Overage and shared capacity: deny

Execution rules:
- Plan and restate the scope before the first write.
- Re-check the current target and reason before each checkpoint; do not continue an expiry-only task.
- Use a branch/worktree when the task is medium-risk or multi-file.
- Work one atomic task at a time and checkpoint after each.
- Run [acceptance checks] after each relevant change.
- Stop on user interruption, cap/timebox, deadline-buffer risk, scope drift, regression, or unknown credentials/data.
- Do not inspect account quota, use paid overage, use shared capacity, flood requests, commit, push, open a PR, or deploy unless separately approved.

Completion evidence:
- Summarize files changed, checks and results, remaining uncertainty, and the exact rollback route.
- If unfinished, mark the task paused or blocked with a next action.
```

## Canonical Goal template (简体中文)

```text
Goal：Token Todo — [项目] 的有界维护

本次使用 $token-todo。

项目与范围：
- 仓库：[路径或仓库名称]
- 允许的任务 ID：[TT-###、TT-###]
- 允许修改的路径：[路径]
- 明确排除：[新功能、生产环境、迁移等]
- 当前目标与理由：[现在应达到什么状态，以及即使没有额度压力为什么仍有价值]

用户提供的资源包络：
- 资源来源：[周期性计划 / 临时赠送 / 其他]
- 可使用上限：[数量/区间] [用户自定义工作单位]
- 为下一个工作日保留：[额度预留]
- 有效截止：[日期时间]，时区为 [用户时区]
- 执行硬时限：[时长]
- 付费 overage 与共享额度：禁止

执行规则：
- 第一次写入前先复述范围与计划。
- 每个检查点前重新检查当前目标与理由；不要继续只因额度即将失效而存在的任务。
- 中风险或多文件修改使用分支/工作树。
- 一次只处理一个原子任务，每个任务后建立检查点。
- 每个相关修改后运行：[验收命令]
- 用户中止、达到上限/时限、截止缓冲不足、范围漂移、回归或出现未知凭据/数据时立即停止。
- 不读取账户额度、不使用付费 overage/共享额度、不刷请求；提交、推送、PR、部署需另行明确批准。

交付证据：
- 汇报改动文件、检查结果、未决不确定性和精确回滚方式。
- 未完成的任务标记为 paused 或 blocked，并写明下一步。
```

## Plan-only prompt

```text
$token-todo plan only.
Project: [path]
Resource source: [user-stated eligible source]
Eligible window: [deadline + timezone]
Capacity: [user-defined cap/range, or say unknown]
Next-workday reserve: [capacity + time]
Timebox: [maximum]
Please inspect read-only, curate candidates, and present conservative/balanced/deep options. Do not edit the ledger or code.
```

## Ledger curation prompt

```text
$token-todo curate this project's token todo ledger.
Read the current project and existing changes, remove stale or duplicate candidates, and propose updates to .codex/token-todo.md. Use only project-local context. Plan first; do not write until I approve the exact ledger changes.
```

## Approval prompt

```text
Approve option [A/B/C] for [task IDs] only.
Hard cap: [capacity and unit].
Reserve: leave [reserve] untouched.
Timebox: [duration], with [timezone/deadline buffer].
Allowed effects: [local changes / commit / other].
Stop and ask again if scope, risk, estimate, or resource source changes.
```

## Stop, pause, and resume prompts

The following should be understood as immediate control signals:

```text
Stop now. Preserve the current checkpoint and do not run more commands.
Pause after the current safe atomic step; do not resume automatically.
Resume only TT-### from the last checkpoint, with a fresh plan and approval.
Roll back only the approved Token Todo changes for TT-###; preserve unrelated work.
```

## Example Goal with a concrete but abstract envelope

```text
Goal: Token Todo — parser reliability and local docs

Use $token-todo. In repository [repo], work only on TT-014 (add regression tests for the existing parser edge cases) and TT-018 (clarify the local setup guide). The user reports 12 eligible work units from a temporary grant, expiring at 2026-09-02 23:00 Asia/Shanghai, and explicitly reserves 8 units plus 90 minutes for the next workday. Hard execution timebox is 75 minutes; use no overage or shared capacity.

Plan first and wait for approval unless this exact scope is approved in the initiating message. Use a branch if the test change touches more than one logical area. Do not change parser behavior, dependencies, CI, production files, or credentials. After each task, run the focused parser tests and documentation checks, record the result, and stop if the upper forecast or the deadline buffer is reached. Do not commit, push, open a PR, deploy, inspect account usage, or resume after interruption. Finish with a diff summary, verification evidence, and rollback instructions.
```
