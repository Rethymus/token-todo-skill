# Contributing to Token Todo

Thank you for helping make bounded AI-assisted engineering safer and more useful.

Contributions should improve Token Todo's present job: converting a user-stated eligible resource envelope into current-value, bounded, reviewable engineering progress without quota automation or unsafe scope expansion.

## Design principles

- Keep the skill explicit, user-bounded, project-local, and provider-agnostic.
- Prefer a small, observable workflow over a clever automation layer.
- Never add quota scraping, billing integrations, background monitoring, request flooding, or fair-use workarounds.
- Treat expiry as a scheduling constraint, never as the sole current reason for a task.
- Preserve unrelated user work and retain historical-looking mechanisms only when a current operational reason requires them.
- Keep `SKILL.md` concise. Put mode-specific detail in a focused reference and link it from the entrypoint.
- Every new rule should address a concrete failure mode or improve a real decision; avoid universal advice that constrains unrelated coding work.

## Before opening a change

- Read the current `SKILL.md`, the relevant reference, and `docs/design-notes.md`.
- Add or update a scenario when changing trigger, approval, scheduling, interruption, current-value, or safety behavior.
- Keep examples provider-neutral and use abstract user-defined work units rather than invented token prices or limits.
- Preserve the explicit-only policy unless there is a documented user-intent reason to change it.
- Keep English and Simplified Chinese README claims, installation instructions, and limitations aligned.

## Local checks

Run the skill validator against `skills/token-todo`:

```text
python <path-to-codex>/skills/.system/skill-creator/scripts/quick_validate.py skills/token-todo
```

Run the repository validator as well:

```bash
python scripts/validate_repo.py
```

Also validate `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` as JSON, run the host skill validator, check that all relative references resolve, and review the English and Chinese README instructions together. If the change affects routing or decisions, evaluate the relevant cases using [`tests/README.md`](tests/README.md).

## Pull requests

Explain the present-tense user need, the behavior that changes, the affected safety boundary, and the scenario evidence used. Do not include real account information, private repository contents, credentials, or billing data in examples or tests. Keep the pull request focused and explain the current reason for each new instruction, check, example, or repository file.
