# Token Todo

Token Todo 是一个由用户主动调用、纯指令式的 Codex skill：把用户明确提供的、符合规则且有时效的 coding capacity，转化为有价值、可审查、可验证、可回滚的工程成果。

[English README](README.md)

> 它是任务规划与安全执行协议，不是额度读取器、重置监控器、计费优化器、后台调度器，也不是为了刷请求而设计的消耗器。

## 为什么需要它

AI coding 让一个新的资源分配问题变得明显：用户可能拥有临时赠送、即将重置或有截止时间的容量，但最安全的方式不是把它耗尽。这个 skill 帮助用户在保护下一个工作日预留的前提下，选择一项边界清楚的维护工作：

```text
用户提供的可用容量 -> 排序后的任务选择 -> 明确批准
        -> 分检查点执行 -> 验证 -> 可回滚交付
```

项目任务列表可以保存在项目内的 `.codex/token-todo.md`。它是可选的、按项目隔离的，不会变成全局账户状态或跨项目隐藏队列。

## 它能做什么

- 接收用户提供的资源包络：来源、可用上限/区间、截止时间、时区、下一个工作日预留、执行时限、风险偏好和允许的副作用。
- 从项目上下文中找出有实际价值且范围小的维护候选：测试、文档、诊断、窄范围重构、积压整理等。
- 以区间、置信度和不确定性说明预计耗时与工作量；不会假装知道服务商的真实 token 或计费。
- 提供保守、均衡和更深入但有检查点的多种方案，不会静默地批量执行。
- 在写入前要求明确批准，保护无关改动，逐个原子任务验证，并记录回滚方式。
- 提供可复用的 Codex Goal 模板，同时让用户控制范围、中止和恢复。

## 它明确不做什么

- 不读取或推断账户额度、重置时间、计费状态、模型限制或服务商侧用量。
- 不安排周期性检查、不唤醒后续任务、不发提醒，也不运行隐藏的后台队列。
- 不使用付费 overage、团队/共享额度、多账户、刷请求或任何规避公平使用的方式。
- 不会仅因为资源窗口即将结束，就选择生产环境、凭据、鉴权、计费、迁移、破坏性或大范围臆测性工作。
- 未经单独明确批准，不提交、推送、创建 PR、部署或联系外部服务。

## 仓库结构

```text
token-todo-skill/
├── .codex-plugin/plugin.json        # skill-only plugin 清单
├── .agents/plugins/marketplace.json # 本地/Git marketplace 入口
├── skills/token-todo/
│   ├── SKILL.md                     # 精简的 agent 指令
│   ├── agents/openai.yaml           # 仅显式调用与 UI 元数据
│   └── references/
│       ├── operating-model.md
│       ├── scheduling-policy.md
│       ├── task-ledger.md
│       ├── safety-and-rollback.md
│       └── goals-and-prompts.md
├── tests/trigger-cases.md           # 人工前向测试用例
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

## 安装

### 推荐：添加 skill-only plugin

在 Codex 中把仓库添加为 marketplace 来源：

```text
codex plugin marketplace add Rethymus/token-todo-skill --ref main
```

然后在 Codex 桌面端 Plugins Directory 中安装 `Token Todo`。如果测试本地 checkout，仓库里已经提供 `.agents/plugins/marketplace.json`：

```text
codex plugin marketplace add ./path/to/token-todo-skill
```

### 直接安装 skill

如果只需要独立 skill，可以使用 skill installer 指向 skill 目录：

```text
$skill-installer install https://github.com/Rethymus/token-todo-skill/tree/main/skills/token-todo
```

安装或更新后，如果 skill 没有出现，请重启 Codex。它配置为只接受显式调用，因此安装本身不会让普通编码请求自动进入这个流程。

## 安全使用方式

建议先要求只读规划。可以使用抽象的工作单位，或者由用户自行定义单位；它们是规划单位，不是服务商 token 或金额估算：

```text
$token-todo 只做规划，不要写文件。
项目：./my-repo
资源来源：用户确认的限时赠送
可用容量：最多 12 个工作单位
有效截止：2026-09-02 23:00 Asia/Shanghai
下一个工作日预留：8 个工作单位和 90 分钟
执行硬时限：75 分钟
风险偏好：低
外部副作用：只允许本地修改；禁止 overage 与共享额度
请只读检查、整理候选，并给出保守/均衡/深入三种方案。
```

然后只批准明确的方案或任务 ID：

```text
只批准方案 A 的 TT-014 和 TT-018，遵守上述上限和时限。保留上述预留。如果范围、风险、估算或资源来源发生变化就停止。
```

可用的控制语句包括：`只做规划`、`现在停止`、`当前安全的原子步骤完成后暂停`、`只从上次检查点恢复 TT-014，并重新规划和批准`、`只回滚 TT-014 已批准的 Token Todo 改动`。

## 默认调度模型

skill 会先应用硬约束，再进行排序：保护用户的下一个工作日预留和截止缓冲，然后优先考虑单位价值、可逆性、验证强度和依赖解锁价值。默认方案如下：

| 方案 | 默认形态 | 默认边界 |
| --- | --- | --- |
| 保守收割 | 一到两个 XS/S 级测试、文档、诊断或窄范围清理任务 | 不超过可支配容量的 35%，最多 60 分钟 |
| 均衡维护 | 一个 S 级任务，或拆成原子步骤的一个 M 级任务 | 不超过可支配容量的 60%，最多 90 分钟 |
| 有界深入 | 单一主题、分支/工作树、每个步骤后检查点 | 只使用明确批准的剩余部分，最多 3 小时 |

这些是保守的规划默认值，不是服务商保证。如果预留、时区、资源来源或所有权不明确，就只能停留在只读规划阶段。

## 安全模型

每次修改都经过下面的生命周期：

```text
candidate -> proposed -> approved -> in_progress -> checkpoint
                                      -> verified -> delivered
                                      -> paused / blocked / rolled_back
```

出现以下情况就应在最早安全边界停止：用户撤回批准；达到硬上限或时限；截止缓冲不足以验证和回滚；可能覆盖无关改动；测试回归；风险等级上升；出现凭据；或下一步需要 overage、共享额度或违反政策。

## 设计参考

本包遵循当前 Agent Skills 的目录/前置元数据约定、渐进式披露和 skill-only plugin 打包方式：

- [OpenAI：Build skills](https://developers.openai.com/codex/skills/)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Plugins repository](https://github.com/openai/plugins)
- [OpenAI legacy skills catalog](https://github.com/openai/skills)（该仓库目前已将新的示例指向 `openai/plugins`）

本 skill 的 `SKILL.md` 刻意保持精简，只有当前模式需要时才读取聚焦的 reference。

## 开发与校验

对实际的 skill 目录运行 Codex 自带的校验器：

```text
python <path-to-codex>/skills/.system/skill-creator/scripts/quick_validate.py skills/token-todo
```

发布前还应检查 JSON 清单、仅显式调用策略、[前向测试用例](tests/trigger-cases.md)以及全部面向用户的链接。

## 许可证

MIT，详见 [LICENSE](LICENSE)。
