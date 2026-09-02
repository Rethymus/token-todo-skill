# Project-local Token Todo ledger

The ledger is an optional, human-readable memory for one project. Use `.codex/token-todo.md` by default only after the user approves creating or updating it. If the user says plan-only, keep the result in the response.

## Design rules

- Keep one ledger per project; do not build a hidden global queue.
- Store task intent and project facts, not secrets, account IDs, access tokens, exact billing records, or guessed quota balances.
- Every item must be understandable without this skill being loaded.
- Do not turn every `TODO` or `FIXME` into a task. Keep only items with a concrete outcome, a reason to do them, a bounded scope, and evidence for why they matter.
- Record a present-tense reason for every candidate. Expiry, unused capacity, a desire to fill the ledger, or approval without a project purpose is not sufficient by itself.
- Keep the current acceptance check and rollback route close to the task. A task that cannot be verified or safely undone is not a default harvest candidate.
- Re-review stale items as the project changes. Remove or close candidates that would now cause regressions or duplicate current work.
- Use stable IDs such as `TT-001`; never reuse an ID for a different outcome.

## Suggested file shape

```markdown
# Token Todo Ledger

Purpose: project-local, user-maintained backlog for bounded engineering work.
Last reviewed: YYYY-MM-DD

## Working profile
- timezone: <user-stated timezone>
- next-workday boundary: <user-stated date/time or description>
- project criticality: <low | medium | high>
- default risk tolerance: <low | medium>
- preferred work: <tests, docs, refactors, ...>

## Run notes
- resource label: <user-provided label only>
- eligible until: <date/time + timezone, if supplied>
- reserve: <user-stated capacity/time; do not infer>
- note: forecasts are planning ranges, not provider telemetry.

## Items

| ID | Outcome and scope | Current reason | Value | Risk | Effort | Forecast | Verify | Rollback | Depends on | Eligible until | Status | Reviewed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TT-001 | <one concrete outcome> | <current requirement, risk, or approved outcome> | high | low | S | 2-5 turns / 25-60m | <command or inspection> | <specific revert path> | none | <date/time> | candidate | <date> |
```

The exact table columns may be adapted to the project, but do not remove `ID`, outcome/scope, risk, forecast, validation, rollback, status, or review date.

## Candidate task catalogue

### Good default candidates

- Add or strengthen tests for already-defined behavior.
- Fix a narrow lint, type, formatting, or documentation defect with a clear check.
- Improve diagnostics, error messages, or observability without exposing secrets.
- Perform a small behavior-preserving refactor with focused tests.
- Remove demonstrably dead code or stale documentation after confirming references.
- Curate backlog items, acceptance criteria, developer notes, or local runbooks.

### Conditional candidates

These require a more explicit scope and usually a separate approval: patch/minor dependency upgrades, CI changes, build-tool changes, generated files, public API changes, auth/permission behavior, database/schema work, data migrations, billing logic, and release configuration.

### Do not select merely to use capacity

Speculative features, broad rewrites, mass renames, security-control weakening, secret/key operations, production changes, irreversible data operations, or any task whose acceptance test is “it looks fine.”

## Status lifecycle

Use these states consistently:

```text
candidate -> proposed -> approved -> in_progress -> checkpoint -> verified -> delivered
                                      |             |              |
                                      v             v              v
                                   paused        blocked        rolled_back

proposed -> expired when the eligibility window passes before approval
```

- `candidate`: useful idea, not yet selected.
- `proposed`: included in a plan awaiting approval.
- `approved`: user approved the named scope and envelope.
- `in_progress`: actively changing only approved paths.
- `checkpoint`: safe pause with diff, tests, and next action recorded.
- `verified`: acceptance checks passed; handoff is ready.
- `delivered`: user-facing handoff completed; this does not imply commit or push.
- `paused`: intentionally stopped and safe to resume after a new approval/check.
- `blocked`: a dependency, failure, or missing decision prevents safe continuation.
- `rolled_back`: approved changes were reverted using the recorded route.
- `expired`: the user-provided window closed before the task was approved or completed.

## Review and pruning

At the beginning of each Token Todo run, review the candidate items against current project direction. Ask of every item, “If the resource window were not closing, would this still be worth doing?” Update, archive, or remove items when their assumptions no longer hold, when they are stale or duplicated, or when expiry is their only reason. At the end, record the evidence and the next smallest action; never leave a task marked delivered with unverified or unrelated changes.

Keep correction chronology out of the canonical task description unless it is required for a current migration, compatibility, security, compliance, public-API, audit, or rollout obligation. When such history is retained, state the current operational reason and the removal or review condition.
