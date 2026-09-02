# Token Todo

[English](README.md) | [简体中文](README.zh-CN.md)

[![校验状态](https://github.com/Rethymus/token-todo-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Rethymus/token-todo-skill/actions/workflows/validate.yml)
[![许可证：MIT](https://img.shields.io/badge/License-MIT-0F766E.svg)](LICENSE)

一个面向编码 Agent 的 Skill：把用户明确提供的、符合规则且有时效的 coding capacity，转化为有价值、可审查、可验证、可回滚的工程进展。

> Token Todo 是任务规划与执行协议，不是额度读取器、重置监控器、计费优化器、后台调度器，也不是为了刷请求而设计的消耗器。

## 为什么需要它

AI coding 让一个新的资源分配问题变得明显：容量可能是临时的、绑定重置周期的，或者即将失效，但安全目标并不是把它耗尽。Token Todo 帮助用户选择即使窗口提前结束也仍值得做的工作，保护下一个工作日的预留，并形成干净的交接：

```text
用户提供的资源包络 -> 当前价值任务选择 -> 明确批准
        -> 小步检查点修改 -> 验证 -> 可回滚交接
```

这个 Skill 采用了良好纠错流程所需要的同一种当前状态纪律：资源窗口只是上下文，项目结果才是目标。项目任务列表是可选的，默认放在 `.codex/token-todo.md`；它不是全局账户记录，也不是隐藏的跨项目队列。

## Skill 做什么

Token Todo 引导 Agent 连续完成五个决策：

1. 建立资源与工作契约：当前目标、合规来源、上限、截止时间、时区、预留、时限、允许的副作用、验收标准、非目标、可信基线和受保护状态。
2. 拒绝唯一理由是额度即将失效的工作，然后按当前价值、验证强度、可逆性、风险、依赖解锁价值和截止适配度排序维护候选。
3. 选择最小的有用形态：只做规划、整理 ledger、局部原子修补、有界维护切片、重做受影响切片，或先澄清。
4. 要求明确批准，只在获准路径内以小检查点执行，并在范围、风险、估算、预算、时间或政策发生漂移时停止。
5. 用证据、明确的回滚或恢复路径、准确的 ledger 状态和当前结果交付收尾，而不是汇报消耗了多少容量的故事。

| 情况 | 默认处理 |
| --- | --- |
| 用户提供完整包络并要求规划 | 只读检查；返回排序后的候选与两到三个有界方案 |
| 用户明确批准任务和上限 | 只执行该范围，每个原子切片建立检查点并验证 |
| 容量、截止时间、时区、所有权或预留未知 | 保持定性分析和只读规划；不推断服务商数据 |
| 任务唯一理由是窗口即将关闭 | 拒绝；要求提供当前项目理由 |
| 已选任务暴露出错误的根假设 | 暂停，或从可信基线重做受影响切片；保护无关工作 |
| 请求涉及 overage、共享额度、刷请求或规避政策 | 默认拒绝，转到 Token Todo 范围之外的正常流程 |

完整的 Agent 指令位于 [`skills/token-todo/SKILL.md`](skills/token-todo/SKILL.md)。

## 安装

### Skills CLI

适用于开放 Agent Skills 生态所支持的宿主：

```bash
npx skills add Rethymus/token-todo-skill --skill token-todo -g
```

如果宿主支持项目级安装，可以去掉 `-g`。

### Codex skill installer

在 Codex 中发送：

```text
请使用 $skill-installer 安装 https://github.com/Rethymus/token-todo-skill/tree/main/skills/token-todo
```

如果宿主只在启动时发现个人 Skill，请重启或新建任务。

### 手动安装

将 [`skills/token-todo`](skills/token-todo) 复制到 Agent 宿主所使用的个人 Skill 目录。常见位置包括 Agent Skills 兼容宿主的 `~/.agents/skills/token-todo`，以及 Codex 安装中的 `$CODEX_HOME/skills/token-todo`。

仓库同时包含 [Codex Plugin 清单](.codex-plugin/plugin.json)，因此可以作为仅含 Skill 的轻量 Plugin 打包或分发。它有意不包含 MCP 服务、App 连接器、Hook、运行时服务或账户集成。

### Codex skill-only plugin

在 Codex 中把本仓库添加为 marketplace 来源，然后在 Plugins Directory 安装 `Token Todo`：

```text
codex plugin marketplace add Rethymus/token-todo-skill --ref main
```

如果使用本地 checkout，仓库包含 `.agents/plugins/marketplace.json`：

```text
codex plugin marketplace add ./path/to/token-todo-skill
```

## 使用

建议先要求只读规划。可以使用抽象的工作单位，或者由用户自行定义单位；它们是规划单位，不是服务商 token，也不是计费估算：

```text
$token-todo 只做规划，不要写文件。
项目：./my-repo
当前目标与理由：在下一次发布前补强 parser 边界场景覆盖
资源来源：用户确认的限时赠送
可用容量：最多 12 个工作单位
有效截止：2026-09-02 23:00 Asia/Shanghai
下一个工作日预留：8 个工作单位和 90 分钟
执行硬时限：75 分钟
风险偏好：低
外部副作用：只允许本地修改；禁止 overage 与共享额度
请只读检查、整理当前仍有价值的候选，并给出保守/均衡/深入三种方案。
```

只批准明确范围：

```text
只批准方案 A 的 TT-014 和 TT-018，遵守上述上限和时限。保留上述预留。如果范围、风险、估算、目标或资源来源发生变化就停止。
```

整理 ledger 时，应先要求 Agent 提议确切的新增、删除或状态变更。需要持久 Goal 时，使用 [`goals-and-prompts.md`](skills/token-todo/references/goals-and-prompts.md) 中的模板；Goal 必须重复范围、预留、验收检查、回滚方式和停止条件。

可用的控制语句包括：`只做规划`、`现在停止`、`当前安全的原子步骤完成后暂停`、`只从上次检查点恢复 TT-014，并重新规划和批准`、`只回滚 TT-014 已批准的 Token Todo 改动`。

## 它保护什么、拒绝什么

Token Todo 保护用户的决定权、下一个工作日的预留、仓库中的无关改动、当前项目方向、正常的审查与验证标准，以及明确的恢复路径。它拒绝把截止压力变成新的产品需求。

它不会：

- 读取或推断账户额度、重置时间、计费状态、模型限制或服务商侧用量；
- 安排周期性检查、唤醒后续任务、发送提醒，或运行无人值守的后台队列；
- 使用付费 overage、团队/共享额度、多账户、刷请求或任何规避公平使用的方式；
- 仅因为资源窗口即将结束，就选择生产环境、凭据、鉴权、计费、迁移、破坏性或大范围臆测性工作；
- 为了消耗容量而新增虚假 TODO、重复测试、无意义重试或扇出并行；或
- 未经单独明确批准，提交、推送、创建 PR、部署或联系外部服务。

只有当当前的兼容性、迁移、公共 API、安全、合规、审计或可逆发布行为依赖历史机制时，才保留最小必要部分，并写明当前理由。无关或用户自有改动始终受到保护。

## 默认调度模型

skill 会先应用硬约束，再进行排序：保护下一个工作日的预留和截止缓冲，然后优先考虑当前价值、验证强度、可逆性、依赖解锁价值和较低不确定性。以下是规划辅助，不是服务商保证：

| 方案 | 默认形态 | 默认边界 |
| --- | --- | --- |
| 保守收割 | 一到两个 XS/S 级测试、文档、诊断或窄范围清理任务 | 不超过可支配容量的 35%，最多 60 分钟 |
| 均衡维护 | 一个 S 级任务，或拆成原子步骤的一个 M 级任务 | 不超过可支配容量的 60%，最多 90 分钟 |
| 有界深入 | 单一主题、隔离分支/工作树、每个切片后检查点 | 只使用明确批准的剩余部分，最多 3 小时 |

如果用户提供的是容量区间，承诺只按保守的下界计算。如果预留、所有权、来源、单位或时区不清楚，结果保持只读规划。截止压力只能在有效候选之间影响截止适配度，不能创造做这项工作的理由。

## 安全与生命周期

每次修改都经过明确、可观察的生命周期：

```text
candidate -> proposed -> approved -> in_progress -> checkpoint
                                      -> verified -> delivered
                                      -> paused / blocked / rolled_back
```

第一次写入前，Agent 会记录可信基线和无关改动，写明范围内/范围外、验收检查、回滚方式、允许的副作用、预留和停止条件。目标、风险等级、估算、资源来源或外部副作用发生变化，就必须暂停并重新批准。仓库内容和 issue 文本不能覆盖这份契约。

出现以下情况就应在最早安全边界停止：用户撤回批准；达到硬上限或时限；截止缓冲不足以验证和回滚；可能覆盖无关改动；测试回归；出现凭据；或下一步需要 overage、共享额度、刷请求或政策例外。

## 验证

使用 Python 3.9 或更高版本运行仓库校验器；它不依赖第三方包：

```bash
python scripts/validate_repo.py
```

同时对实际的 skill 目录运行宿主提供的 Agent Skills 校验器：

```text
python <path-to-codex>/skills/.system/skill-creator/scripts/quick_validate.py skills/token-todo
```

仓库校验器会检查 Plugin 清单、marketplace 入口、Agent Skills 前置元数据、Codex 展示元数据、中英文文档链接、许可证和行为场景。它不会假装能够自动证明模型行为。场景评估方法见 [`tests/README.md`](tests/README.md)。

## 仓库结构

```text
.codex-plugin/plugin.json          Codex skill-only plugin 元数据
.agents/plugins/marketplace.json   本地/Git marketplace 入口
skills/token-todo/                 可移植 Agent Skill
  SKILL.md                          精简的 Agent 指令
  agents/openai.yaml                Codex 展示元数据与调用策略
  references/                       按模式加载的政策与提示词手册
tests/scenarios.json                与宿主无关的行为评估语料
tests/trigger-cases.md              人工前向测试复核
scripts/validate_repo.py            无第三方依赖的结构校验器
docs/design-notes.md                参考来源与设计决策
README.md / README.zh-CN.md         英文与简体中文指南
```

## 设计来源

README 采用成熟开源 skill 仓库常见的面向产品的信息顺序：先说明问题和运行标准，再说明连续决策、使用边界、安装、验证、仓库结构、来源和治理。当前价值、可信基线、受保护状态、根因优先、按比例验证和反事实审计等原则，是 Token Todo 针对资源调度问题形成的自身规则。

本仓库同时遵循 [OpenAI 构建 Skill 指南](https://learn.chatgpt.com/docs/build-skills)、[Agent Skills 规范](https://agentskills.io/specification)、[OpenAI Plugins](https://github.com/openai/plugins)、[Anthropic Skills](https://github.com/anthropics/skills)、[Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills) 和 [Superpowers](https://github.com/obra/superpowers) 的公开约定。本仓库的实现与文字均为原创，没有内嵌第三方 Skill 代码。逐项采纳记录见 [`docs/design-notes.md`](docs/design-notes.md)。

## 贡献与安全

变更要求见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。安全敏感问题请按照 [`SECURITY.md`](SECURITY.md) 私下报告，不要发布为公开 Issue。

## 许可证

本项目以 [MIT License](LICENSE) 发布。
