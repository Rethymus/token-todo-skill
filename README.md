# Token Todo

Token Todo is a user-invoked, instruction-only Codex skill for turning eligible, time-bounded coding capacity into useful engineering progress that is reviewable, verifiable, and reversible.

[简体中文 README](README.zh-CN.md)

> It is a planning and execution protocol, not a quota reader, reset monitor, billing optimizer, background scheduler, or request-volume maximizer.

## Why it exists

AI coding makes a previously small problem visible: a user may have temporary, expiring, or reset-bound capacity, but the safest way to use it is not to exhaust it. The skill helps choose a bounded maintenance outcome while preserving the next workday's reserve:

```text
user-eligible capacity -> ranked task choice -> explicit approval
        -> checkpointed change -> verification -> reversible handoff
```

The project-specific task list lives in an optional `.codex/token-todo.md` ledger. The ledger is deliberately local to a project; it does not become a global account or cross-project queue.

## What it does

- Takes a user-stated resource envelope: source, eligible cap/range, expiry, timezone, reserve, timebox, risk tolerance, and permitted side effects.
- Finds useful, low-drama maintenance candidates from project context: tests, docs, diagnostics, narrow refactors, backlog hygiene, and other bounded work.
- Estimates effort and wall-clock time as ranges with confidence and uncertainty; it never pretends to know provider tokens or billing.
- Offers conservative, balanced, and deeper checkpointed plan options instead of silently choosing an opaque batch.
- Requires explicit approval before writes, preserves unrelated changes, verifies each atomic slice, and records a rollback path.
- Supports reusable Codex Goal prompts while keeping the user in control of scope, interruption, and resumption.

## What it does not do

- It does not inspect or infer account quota, reset time, billing status, model limits, or provider-side usage.
- It does not schedule recurring checks, wake up later, send reminders, or run a hidden background queue.
- It does not use paid overage, team/shared capacity, multiple accounts, request flooding, or fair-use bypasses.
- It does not choose production, credential, auth, billing, migration, destructive, or broad speculative work merely because a resource window is closing.
- It does not commit, push, open a PR, deploy, or contact external services without separate explicit approval.

## Package layout

```text
token-todo-skill/
├── .codex-plugin/plugin.json       # skill-only plugin manifest
├── .agents/plugins/marketplace.json # local/Git-backed marketplace entry
├── skills/token-todo/
│   ├── SKILL.md                    # concise agent instructions
│   ├── agents/openai.yaml          # explicit-only invocation and UI metadata
│   └── references/
│       ├── operating-model.md
│       ├── scheduling-policy.md
│       ├── task-ledger.md
│       ├── safety-and-rollback.md
│       └── goals-and-prompts.md
├── tests/trigger-cases.md          # human-readable forward-test cases
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

## Install

### Recommended: add the skill-only plugin

From Codex, add this repository as a marketplace source:

```text
codex plugin marketplace add Rethymus/token-todo-skill --ref main
```

Then install `Token Todo` from the Codex desktop Plugins Directory. If you are testing a local checkout, the repository includes a marketplace entry at `.agents/plugins/marketplace.json`:

```text
codex plugin marketplace add ./path/to/token-todo-skill
```

### Direct skill installation

For a standalone skill install, use the skill installer with the skill directory URL:

```text
$skill-installer install https://github.com/Rethymus/token-todo-skill/tree/main/skills/token-todo
```

After installation or an update, restart Codex if the skill does not appear. The skill is configured for explicit invocation only, so installing it does not make ordinary coding requests consume the workflow automatically.

## Use it safely

Start with a plan-only request. Use abstract work units or a unit that you define; they are planning units, not provider token or dollar estimates:

```text
$token-todo plan only.
Project: ./my-repo
Resource source: user-stated limited-time grant
Eligible capacity: up to 12 work units
Eligible until: 2026-09-02 23:00 Asia/Shanghai
Next-workday reserve: 8 work units and 90 minutes
Hard timebox: 75 minutes
Risk tolerance: low
External effects: local changes only; no overage or shared capacity
Please inspect read-only, curate candidates, and present conservative/balanced/deep options.
```

Then approve only a named option or task IDs:

```text
Approve option A for TT-014 and TT-018 only, within the stated cap and timebox. Leave the stated reserve untouched. Stop if scope, risk, estimate, or resource source changes.
```

Useful controls include `plan only`, `stop now`, `pause after the current safe atomic step`, `resume only TT-014 from the last checkpoint with a fresh approval`, and `roll back only the approved Token Todo changes for TT-014`.

## Default scheduling model

The skill applies hard constraints before ranking. It preserves the user's next-workday reserve and a deadline buffer, then prefers value density, reversibility, verification strength, and dependency value. The default modes are:

| Mode | Default shape | Default bound |
| --- | --- | --- |
| Conservative harvest | One or two XS/S tests, docs, diagnostics, or narrow cleanup tasks | Up to 35% of spendable capacity and 60 minutes |
| Balanced maintenance | One S task or one M task split into atomic slices | Up to 60% of spendable capacity and 90 minutes |
| Deep bounded pass | One theme, isolated branch/worktree, checkpoint after every slice | Only the explicitly approved remainder and at most 3 hours |

These are conservative planning defaults, not provider guarantees. If reserve, timezone, source eligibility, or ownership is unknown, the result stays plan-only.

## Safety model

Every mutation passes through:

```text
candidate -> proposed -> approved -> in_progress -> checkpoint
                                      -> verified -> delivered
                                      -> paused / blocked / rolled_back
```

The skill stops when the user withdraws approval, a hard cap or timebox is reached, the deadline buffer is too small for verification and rollback, unrelated changes could be overwritten, tests regress, risk rises, credentials become relevant, or the next action would require overage/shared capacity or a policy exception.

## Design references

The package follows the current Agent Skills directory/frontmatter conventions, progressive disclosure, and skill-only plugin packaging guidance:

- [OpenAI: Build skills](https://developers.openai.com/codex/skills/)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Plugins repository](https://github.com/openai/plugins)
- [OpenAI's legacy skills catalog](https://github.com/openai/skills) (the repository currently points new examples to `openai/plugins`)

The local `SKILL.md` is intentionally short; detailed policy is loaded from focused references only when the current mode needs it.

## Development and validation

Run the bundled Codex skill validator against the actual skill directory:

```text
python <path-to-codex>/skills/.system/skill-creator/scripts/quick_validate.py skills/token-todo
```

Also review the JSON manifest, the explicit-only policy, the [forward-test cases](tests/trigger-cases.md), and every user-facing link before publishing.

## License

MIT. See [LICENSE](LICENSE).
