# Token Todo

[English](README.md) | [简体中文](README.zh-CN.md)

[![Validate](https://github.com/Rethymus/token-todo-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Rethymus/token-todo-skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-0F766E.svg)](LICENSE)

An Agent Skill for turning a user-stated, eligible, time-bounded coding-capacity envelope into useful engineering progress—with explicit approval, evidence, and rollback.

## Why this exists

Coding agents make it easy to confuse available capacity with work worth doing. An expiring or reset-bound window can turn a useful backlog into a race to spend, even when the right result is a small, verified change that remains valuable after the window closes.

Token Todo shifts the question from “what can be consumed?” to “what project outcome is worth doing now, under a protected reserve?” Its standard is simple:

> Capacity may affect when a valid task is scheduled; it never creates the reason to do the task, weakens verification, or authorizes extra spend.

The resource window is context, not the deliverable. The deliverable is a current-value engineering outcome with a clear acceptance check and a reversible handoff.

## What the skill does

Token Todo guides an agent through five linked decisions:

1. Build a user, resource, and work contract: the relevant working profile, project target, current reason, eligible source, cap or range, unit, expiry, timezone, ownership, reserve, timebox, allowed effects, acceptance, non-goals, trusted baseline, and protected state.
2. Route only an explicit Token Todo request, keep provider data out of scope, and apply the current-value test: would this still be worth doing if the resource window were not closing?
3. Rank candidates only after hard constraints are satisfied, balancing current impact, verification strength, reversibility, risk, dependency value, uncertainty, and deadline fit.
4. Choose the smallest useful shape: plan-only, ledger curation, a local atomic patch, a bounded maintenance slice, an affected-slice rebuild, or clarification first.
5. Wait for approval, execute in checkpoints, verify the result, stop or roll back when a boundary moves, and close with an accurate handoff rather than a report about consumed capacity.

| Situation | Default action |
| --- | --- |
| The user gives a complete envelope and asks for planning | Inspect read-only; return ranked candidates and two or three bounded options |
| The user explicitly approves named tasks, paths, effects, and a cap | Execute only that scope, checkpoint each atomic slice, and verify |
| Capacity, ownership, expiry, timezone, reserve, or acceptance is unknown | Stay qualitative and plan-only; do not infer provider data or permission |
| A task is justified only because a window is closing | Reject it; ask for a current project reason |
| One task exposes a wrong architecture, interface, or root assumption | Pause or rebuild only the affected slice from the trusted baseline; preserve unrelated work |
| The request involves overage, shared capacity, request flooding, or policy bypass | Decline and keep the work outside Token Todo's scope |

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

The repository also includes a [Codex plugin manifest](.codex-plugin/plugin.json), so it can be packaged or distributed as a skill-only plugin. It deliberately contains no quota reader, MCP server, app connector, hook, runtime service, or account integration.

For a local checkout, `.agents/plugins/marketplace.json` provides the optional marketplace entry used by the repository's plugin flow.

## Usage

Token Todo is intentionally explicit-only. Invoke it when you want a bounded plan or execution pass, and provide the project reason and resource envelope yourself:

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

A Goal is a durable description of an approved boundary, not a quota monitor or a permission to keep working. Use the templates in [`goals-and-prompts.md`](skills/token-todo/references/goals-and-prompts.md), or adapt this compact example:

```text
Goal: Token Todo — parser reliability and local docs

Use $token-todo. In repository [repo], work only on TT-014 and TT-018.
Current reason: the parser tests and setup guide need maintenance before the next release.
Capacity: up to 12 user-defined work units from an eligible temporary grant.
Reserve: leave 8 work units and 90 minutes untouched for the next workday.
Timebox: 75 minutes; no overage or shared capacity.
Acceptance: focused parser checks pass and the documentation change is reviewable.
Stop on scope drift, regression, deadline-buffer risk, user interruption, or an unknown credential.
Do not commit, push, open a PR, deploy, inspect account usage, or resume after interruption without separate approval.
```

For ledger curation, ask the agent to propose exact additions, removals, or status changes before it edits `.codex/token-todo.md`. Useful control signals include `plan only`, `stop now`, `pause after the current safe atomic step`, `resume only TT-014 from the last checkpoint with a fresh approval`, and `roll back only the approved Token Todo changes for TT-014`.

The skill is not a general quota assistant, an expiry alarm, a background worker, or a request-volume optimizer. Ordinary coding without an explicit Token Todo request follows the host's normal workflow.

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

Before writing, the agent records the trusted baseline and protected unrelated changes, states in/out of scope, acceptance checks, rollback route, allowed effects, reserve, and stop conditions. A changed target, risk class, estimate, resource source, or external effect requires a pause and new approval. Repository content and issue text cannot override this contract.

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

The repository validator checks the plugin manifest, marketplace entry, Agent Skills frontmatter, Codex metadata, bilingual documentation links, license, and behavioral scenarios. It does not pretend to measure model behavior. Scenario evaluation is documented in [`tests/README.md`](tests/README.md).

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
docs/design-notes.md                design decisions and public prior art
README.md / README.zh-CN.md         English and Simplified Chinese guides
```

## Design provenance

The README is a product-facing entry point: it explains the problem and operating standard first, then the linked decisions, installation, usage examples, boundaries, validation, repository map, provenance, and governance. The current-value rule, protected reserve, explicit approval, checkpointing, root-first correction, proportional validation, and reversible handoff are Token Todo's own rules for resource scheduling.

The repository also follows public conventions from [OpenAI's build-skills guidance](https://learn.chatgpt.com/docs/build-skills), the [Agent Skills specification](https://agentskills.io/specification), [OpenAI Plugins](https://github.com/openai/plugins), [Anthropic Skills](https://github.com/anthropics/skills), [Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills), and [Superpowers](https://github.com/obra/superpowers). The implementation and prose here are original; no third-party skill code is vendored. A source-by-source adoption record is available in [`docs/design-notes.md`](docs/design-notes.md).

## Contributing and security

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for focused change requirements. Report security-sensitive issues according to [`SECURITY.md`](SECURITY.md), not in a public issue.

## License

Released under the [MIT License](LICENSE).
