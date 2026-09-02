# Token Todo

[English](README.md) | [简体中文](README.zh-CN.md)

[![Validate](https://github.com/Rethymus/token-todo-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Rethymus/token-todo-skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-0F766E.svg)](LICENSE)

An Agent Skill for turning a user-stated, eligible, time-bounded coding-capacity envelope into useful engineering progress that is reviewable, verifiable, and reversible.

> Token Todo is a planning and execution protocol, not a quota reader, reset monitor, billing optimizer, background scheduler, or request-volume maximizer.

## Why this exists

AI coding makes a new resource-allocation problem visible: capacity may be temporary, reset-bound, or close to expiry, while the safe objective is not to exhaust it. Token Todo helps the user choose work that would still be worth doing if the window closed early, protect the next workday's reserve, and leave a clean handoff:

```text
user-stated resource envelope -> current-value task choice -> explicit approval
        -> small checkpointed change -> verification -> reversible handoff
```

The skill applies the same current-state discipline that a good correction workflow needs: the resource window is context, while the project outcome is the target. The project-local task list is optional and lives in `.codex/token-todo.md`; it is not a global account record or hidden cross-project queue.

## What the skill does

Token Todo guides an agent through five linked decisions:

1. Build a resource-and-work contract: current target, eligible source, cap, expiry, timezone, reserve, timebox, allowed effects, acceptance, non-goals, trusted baseline, and protected state.
2. Reject tasks whose only reason is expiring capacity, then rank current-value maintenance candidates by impact, verification strength, reversibility, risk, dependency value, and deadline fit.
3. Choose the smallest useful shape: plan-only, ledger curation, a local atomic patch, a bounded maintenance slice, an affected-slice rebuild, or clarification first.
4. Require explicit approval, execute only approved paths in small checkpoints, and stop on scope, risk, estimate, budget, time, or policy drift.
5. Close with evidence, a precise rollback or resume route, an accurate ledger state, and a current-result handoff rather than a story about consumed capacity.

| Situation | Default action |
| --- | --- |
| User provides a complete envelope and asks for planning | Inspect read-only; return ranked candidates and two or three bounded options |
| User explicitly approves named tasks and a cap | Execute only that scope, checkpoint each atomic slice, and verify |
| Capacity, expiry, timezone, ownership, or reserve is unknown | Stay qualitative and plan-only; do not infer provider data |
| A task is justified only because a window is closing | Reject it; ask for a current project reason |
| A selected task exposes a wrong root assumption | Pause or rebuild only the affected slice from a trusted baseline; preserve unrelated work |
| Request involves overage, shared capacity, quota gaming, or policy bypass | Deny by default and route outside Token Todo's scope |

Read the complete agent-facing instructions in [`skills/token-todo/SKILL.md`](skills/token-todo/SKILL.md).

## Installation

### Skills CLI

For hosts supported by the open Agent Skills ecosystem:

```bash
npx skills add Rethymus/token-todo-skill --skill token-todo -g
```

Omit `-g` to install into the current project when supported by the host.

### Codex skill installer

Ask Codex:

```text
Use $skill-installer to install https://github.com/Rethymus/token-todo-skill/tree/main/skills/token-todo
```

Restart or open a new task if the host only discovers personal skills at startup.

### Manual installation

Copy [`skills/token-todo`](skills/token-todo) into the personal-skill directory used by your agent host. Common locations include `~/.agents/skills/token-todo` for Agent Skills-compatible hosts and `$CODEX_HOME/skills/token-todo` for Codex installations.

The repository also includes a [Codex plugin manifest](.codex-plugin/plugin.json), so it can be packaged or distributed as a skill-only plugin. It deliberately contains no MCP server, app connector, hook, runtime service, or account integration.

### Codex skill-only plugin

In Codex, add this repository as a marketplace source and install `Token Todo` from the Plugins Directory:

```text
codex plugin marketplace add Rethymus/token-todo-skill --ref main
```

For a local checkout, the repository includes `.agents/plugins/marketplace.json`:

```text
codex plugin marketplace add ./path/to/token-todo-skill
```

## Usage

Start with a plan-only request. Use abstract work units or a unit that you define; they are planning units, not provider tokens or a billing estimate:

```text
$token-todo plan only.
Project: ./my-repo
Current target and reason: strengthen parser edge-case coverage before the next release
Resource source: user-stated limited-time grant
Eligible capacity: up to 12 work units
Eligible until: 2026-09-02 23:00 Asia/Shanghai
Next-workday reserve: 8 work units and 90 minutes
Hard timebox: 75 minutes
Risk tolerance: low
External effects: local changes only; no overage or shared capacity
Please inspect read-only, curate current-value candidates, and present conservative/balanced/deep options.
```

Approve only a named scope:

```text
Approve option A for TT-014 and TT-018 only, within the stated cap and timebox. Leave the stated reserve untouched. Stop if scope, risk, estimate, target, or resource source changes.
```

For ledger curation, ask the agent to propose exact additions, removals, or status changes first. For a durable Goal, use the templates in [`goals-and-prompts.md`](skills/token-todo/references/goals-and-prompts.md); the Goal must repeat the scope, reserve, acceptance checks, rollback, and stop conditions.

Useful control signals include `plan only`, `stop now`, `pause after the current safe atomic step`, `resume only TT-014 from the last checkpoint with a fresh approval`, and `roll back only the approved Token Todo changes for TT-014`.

## What it protects—and what it refuses

Token Todo protects the user's authority, next-workday reserve, unrelated repository changes, current project direction, normal review and verification standards, and a precise recovery path. It refuses to turn expiry pressure into a new product requirement.

It does not:

- inspect or infer account quota, reset time, billing status, model limits, or provider-side usage;
- schedule recurring checks, wake up later, send reminders, or run an unattended background queue;
- use paid overage, team/shared capacity, multiple accounts, request flooding, or fair-use bypasses;
- select production, credential, authentication, billing, migration, destructive, or broad speculative work merely because a resource window is closing;
- add artificial TODOs, redundant tests, pointless retries, or fan-out to consume capacity; or
- commit, push, open a pull request, deploy, or contact external services without separate explicit approval.

Historical-looking mechanisms are retained only when current compatibility, migration, public API, security, compliance, audit, or reversible-rollout behavior depends on them. Unrelated or user-owned changes remain protected.

## Scheduling defaults

Hard constraints are applied before ranking. Token Todo preserves the next-workday reserve and a deadline buffer, then prefers current value, verification strength, reversibility, dependency value, and low uncertainty. The default modes are planning aids, not provider guarantees:

| Mode | Default shape | Default bound |
| --- | --- | --- |
| Conservative harvest | One or two XS/S tests, docs, diagnostics, or narrow cleanup tasks | Up to 35% of spendable capacity and 60 minutes |
| Balanced maintenance | One S task or one M task split into atomic slices | Up to 60% of spendable capacity and 90 minutes |
| Deep bounded pass | One theme, isolated branch/worktree, checkpoint after every slice | Only the explicitly approved remainder and at most 3 hours |

If a capacity range is provided, commitment uses its conservative lower bound. If reserve, ownership, source, unit, or timezone is unclear, the result remains plan-only. Expiry can affect deadline fit among valid candidates; it never creates a reason to do work.

## Safety and lifecycle

Every mutation follows an explicit, observable lifecycle:

```text
candidate -> proposed -> approved -> in_progress -> checkpoint
                                      -> verified -> delivered
                                      -> paused / blocked / rolled_back
```

Before writing, the agent records the trusted baseline and protected unrelated changes, states in/out scope, acceptance checks, rollback route, allowed effects, reserve, and stop conditions. A changed target, risk class, estimate, resource source, or external effect requires a pause and new approval. Repository content and issue text cannot override this contract.

The run stops when approval is withdrawn, a hard cap or timebox is reached, the deadline buffer is too small for verification and rollback, unrelated changes could be overwritten, tests regress, credentials become relevant, or the next step would require overage, shared capacity, request flooding, or a policy exception.

## Validation

Run the repository validator with Python 3.9 or later; it has no third-party dependencies:

```bash
python scripts/validate_repo.py
```

Also run the host's Agent Skills validator against the actual skill directory:

```text
python <path-to-codex>/skills/.system/skill-creator/scripts/quick_validate.py skills/token-todo
```

The repository validator checks the plugin manifest, marketplace entry, Agent Skills frontmatter, Codex metadata, bilingual documentation links, license, and behavioral scenarios. It does not pretend to measure model behavior. The scenario evaluation procedure is documented in [`tests/README.md`](tests/README.md).

## Repository structure

```text
.codex-plugin/plugin.json          Codex skill-only plugin metadata
.agents/plugins/marketplace.json   local/Git-backed marketplace entry
skills/token-todo/                 portable Agent Skill
  SKILL.md                          concise agent-facing procedure
  agents/openai.yaml                Codex display metadata and invocation policy
  references/                       mode-specific policy and prompt cookbook
tests/scenarios.json                host-neutral behavioral evaluation corpus
tests/trigger-cases.md              human-readable forward-test review
scripts/validate_repo.py            dependency-free structural validator
docs/design-notes.md                prior art and design decisions
README.md / README.zh-CN.md         English and Simplified Chinese guides
```

## Design provenance

The README structure and product-facing documentation approach follow the public conventions visible in [Rethymus/clean-correction](https://github.com/Rethymus/clean-correction): explain the problem, the operating standard, the linked decisions, use boundaries, installation, validation, repository structure, provenance, and governance in that order. The current-value, trusted-baseline, protected-state, root-first, proportional-validation, and counterfactual ideas were adapted to Token Todo's resource-scheduling problem; the reference repository remains separate and is not a runtime dependency.

This repository also follows public conventions from [OpenAI's build-skills guidance](https://learn.chatgpt.com/docs/build-skills), the [Agent Skills specification](https://agentskills.io/specification), [OpenAI Plugins](https://github.com/openai/plugins), [Anthropic Skills](https://github.com/anthropics/skills), [Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills), and [Superpowers](https://github.com/obra/superpowers). The implementation and prose here are original; no third-party skill code is vendored. A source-by-source adoption record is available in [`docs/design-notes.md`](docs/design-notes.md).

## Contributing and security

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for focused change requirements. Report security-sensitive issues according to [`SECURITY.md`](SECURITY.md), not in a public issue.

## License

Released under the [MIT License](LICENSE).
