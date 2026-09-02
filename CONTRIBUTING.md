# Contributing to Token Todo

Thank you for helping make bounded AI-assisted engineering safer and more useful.

## Design principles

- Keep the skill explicit, user-bounded, project-local, and provider-agnostic.
- Prefer a small, observable workflow over a clever automation layer.
- Never add quota scraping, billing integrations, background monitoring, request flooding, or fair-use workarounds.
- Keep `SKILL.md` concise. Put mode-specific detail in a focused reference and link it from the entrypoint.
- Every new rule should address a concrete failure mode or improve a real decision; avoid universal advice that constrains unrelated coding work.

## Before opening a change

- Read the current `SKILL.md` and the relevant reference.
- Add or update a forward-test case when changing trigger, approval, scheduling, interruption, or safety behavior.
- Keep examples provider-neutral and use abstract user-defined work units rather than invented token prices or limits.
- Preserve the explicit-only policy unless there is a documented user-intent reason to change it.

## Local checks

Run the skill validator against `skills/token-todo`:

```text
python <path-to-codex>/skills/.system/skill-creator/scripts/quick_validate.py skills/token-todo
```

Also validate `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` as JSON, check that all relative references resolve, and review the English and Chinese README instructions together.

## Pull requests

Explain the failure mode or user need, the behavior that changes, the affected safety boundary, and the forward-test cases used. Do not include real account information, private repository contents, credentials, or billing data in examples or tests.
