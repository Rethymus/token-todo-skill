# Token Todo

[English](README.md) | [简体中文](README.zh-CN.md)

[![校验状态](https://github.com/Rethymus/token-todo-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Rethymus/token-todo-skill/actions/workflows/validate.yml)
[![许可证：MIT](https://img.shields.io/badge/License-MIT-0F766E.svg)](LICENSE)

一个可移植、面向编码 Agent 的通用 Skill：把用户明确提供的、符合规则且有时效的 coding capacity，转化为有价值、可审查、可验证、可回滚的工程进展，并要求明确批准、过程证据和恢复路径。

规范主体位于宿主无关的 `skills/token-todo` 目录中。Codex Plugin 文件只是可选的分发适配层；同一个 Skill 目录也可以安装到其他兼容 Agent Skills 的宿主。

## 为什么需要它

编码 Agent 很容易把“有可用容量”和“有值得做的工作”混为一谈。即将失效或绑定重置周期的窗口，可能把有价值的 backlog 变成一场消耗竞赛，即使正确结果本应是一个在窗口关闭后仍然有价值的小型、可验证修改。

Token Todo 把问题从“还能消耗什么？”转成“在保护预留的前提下，现在最值得交付什么项目结果？”它采用一个简单标准：

> 容量可以影响有效任务何时排期，但不能创造做这项工作的理由、降低验证要求或授权额外付费。

资源窗口只是上下文，不是交付物。交付物应当是具有当前价值、明确验收检查和可逆交接路径的工程结果。

## Skill 做什么

Token Todo 引导 Agent 连续完成五个决策：

1. 建立用户、资源与工作契约：相关工作画像、项目目标、当前理由、合规来源、上限或区间、单位、截止时间、时区、所有权、预留、时限、允许的副作用、验收标准、非目标、可信基线和受保护状态。
2. 只路由明确的 Token Todo 请求，把服务商数据留在范围之外，并应用当前价值检验：如果资源窗口没有即将关闭，这件事仍然值得做吗？
3. 只有通过硬约束后才排序候选，综合当前影响、验证强度、可逆性、风险、依赖解锁价值、不确定性和截止适配度。
4. 选择最小的有用形态：只做规划、整理 ledger、局部原子修补、有界维护切片、重做受影响切片，或先澄清。
5. 等待批准，以检查点执行，验证结果，在边界变化时停止或回滚，并用准确的交接收尾，而不是汇报消耗了多少容量。

| 情况 | 默认处理 |
| --- | --- |
| 用户提供完整包络并要求规划 | 只读检查；返回排序后的候选与两到三个有界方案 |
| 用户明确批准任务、路径、副作用和上限 | 只执行该范围，每个原子切片建立检查点并验证 |
| 容量、所有权、截止时间、时区、预留或验收标准未知 | 保持定性分析和只读规划；不推断服务商数据或执行权限 |
| 任务唯一理由是窗口即将关闭 | 拒绝；要求提供当前项目理由 |
| 任务暴露出错误架构、接口或根假设 | 暂停，或从可信基线重做受影响切片；保护无关工作 |
| 请求涉及 overage、共享额度、刷请求或规避政策 | 拒绝，并将其留在 Token Todo 范围之外 |

完整的 Agent 指令位于 [`skills/token-todo/SKILL.md`](skills/token-todo/SKILL.md)。

## 安装

### Skills CLI

适用于开放 Agent Skills 生态所支持的宿主：

```bash
npx skills add Rethymus/token-todo-skill --skill token-todo -g
```

如果宿主支持项目级安装，可以去掉 `-g`。

### Codex Skill Installer

在 Codex 中发送：

```text
请使用 $skill-installer 安装 https://github.com/Rethymus/token-todo-skill/tree/main/skills/token-todo
```

如果宿主只在启动时发现个人 Skill，请重启或新建任务。

### 手动安装

将 [`skills/token-todo`](skills/token-todo) 复制到 Agent 宿主所使用的个人 Skill 目录。常见位置包括 Agent Skills 兼容宿主的 `~/.agents/skills/token-todo`，以及 Codex 安装中的 `$CODEX_HOME/skills/token-todo`。

仓库同时包含 [Codex Plugin 清单](.codex-plugin/plugin.json)，因此可以作为仅含 Skill 的轻量 Plugin 打包或分发。它有意不包含额度读取器、MCP 服务、App 连接器、Hook、运行时服务或账户集成。

如果使用本地 checkout，`.agents/plugins/marketplace.json` 提供了仓库 Plugin 流程可选的 marketplace 入口。

## 使用

Token Todo 有意保持为仅显式调用。希望获得有界规划或执行时，应明确调用它，并自行提供项目理由与资源包络：

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

Goal 是已批准边界的持久化描述，不是额度监控器，也不会授权 Agent 自动继续工作。可以使用 [`goals-and-prompts.md`](skills/token-todo/references/goals-and-prompts.md) 中的模板，或参考这个精简示例：

```text
Goal：Token Todo — parser 可靠性与本地文档

本次使用 $token-todo。在仓库 [repo] 中只处理 TT-014 和 TT-018。
当前理由：下一次发布前需要维护 parser 测试与 setup 指南。
容量：来自合规临时赠送的最多 12 个用户自定义工作单位。
预留：为下一个工作日保留 8 个工作单位和 90 分钟，不得使用。
时限：75 分钟；禁止 overage 与共享额度。
验收：相关 parser 检查通过，文档修改可审查。
范围漂移、回归、截止缓冲不足、用户中止或出现未知凭据时停止。
未经单独批准，不提交、不推送、不创建 PR、不部署、不读取账户用量，也不在中断后自动恢复。
```

整理 ledger 时，应先要求 Agent 提议确切的新增、删除或状态变更，再编辑 `.codex/token-todo.md`。可用的控制语句包括：`只做规划`、`现在停止`、`当前安全的原子步骤完成后暂停`、`只从上次检查点恢复 TT-014，并重新规划和批准`、`只回滚 TT-014 已批准的 Token Todo 改动`。

这个 Skill 不是通用额度助手、失效提醒器、后台工作器或请求量优化器。不涉及明确 Token Todo 请求的普通编码，应使用宿主常规流程。

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

Skill 会先应用硬约束，再进行排序：保护下一个工作日的预留和截止缓冲，然后优先考虑当前价值、验证强度、可逆性、依赖解锁价值和较低不确定性。以下是规划辅助，不是服务商保证：

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
docs/design-notes.md                设计决策与公开实践
README.md / README.zh-CN.md         English 与简体中文指南
```

## 设计来源

README 作为面向用户的产品入口：先说明问题和运行标准，再说明连续决策、安装、使用示例、边界、验证、仓库地图、来源和治理。当前价值、受保护预留、明确批准、检查点、根因优先、按比例验证和可逆交接等规则，是 Token Todo 针对资源调度问题形成的自身规则。

本仓库同时遵循 [OpenAI 构建 Skill 指南](https://learn.chatgpt.com/docs/build-skills)、[Agent Skills 规范](https://agentskills.io/specification)、[OpenAI Plugins](https://github.com/openai/plugins)、[Anthropic Skills](https://github.com/anthropics/skills)、[Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills) 和 [Superpowers](https://github.com/obra/superpowers) 的公开约定。本仓库的实现与文字均为原创，没有内嵌第三方 Skill 代码。逐项采纳记录见 [`docs/design-notes.md`](docs/design-notes.md)。

## 贡献与安全

变更要求见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。安全敏感问题请按照 [`SECURITY.md`](SECURITY.md) 私下报告，不要发布为公开 Issue。

## 许可证

本项目以 [MIT License](LICENSE) 发布。
