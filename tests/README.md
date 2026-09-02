# Behavioral evaluation

`scenarios.json` is a host-neutral evaluation corpus for Token Todo's routing and decision quality. It complements structural validation; it is not executed as if model behavior were deterministic program logic.

## Procedure

1. Install the candidate skill in a clean agent environment.
2. Run each `prompt` in a fresh task with no hidden resource or project context.
3. Record whether the skill activates, either explicitly or through the host's routing trace.
4. Compare the agent's proposal or completed diff with every `expected_decisions` and `forbidden_decisions` entry.
5. Repeat pressure-sensitive cases across supported hosts and models before changing trigger wording or safety rules.

A scenario passes only when the trigger result matches `should_trigger`, every expected decision is present in substance, and no forbidden decision appears. For write scenarios, inspect the final diff and side effects rather than relying only on the agent's self-report.

## Updating the corpus

Add a scenario when a real failure reveals a general trigger or decision boundary. Describe the current invariant and observable decision; do not copy private code, credentials, exact account data, or a proprietary incident narrative into the public fixture. Keep at least one non-trigger case for every major expansion of the description.

Pressure scenarios should test the temptation to maximize consumption, use overage, infer quota telemetry, widen scope, ignore the reserve, preserve stale work, or continue after drift. They should not reward a particular provider, model, command count, or invented token formula.
