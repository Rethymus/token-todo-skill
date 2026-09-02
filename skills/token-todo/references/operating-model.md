# Token Todo operating model

This reference explains who the skill serves, when it should be invoked, and what success means. It is intentionally product-level; the execution rules live in the scheduling and safety references.

## Product thesis

AI coding creates a new resource-allocation problem: a user may have a temporary or expiring coding-plan allowance, but the safest way to use it is not to maximize requests. The useful conversion is:

> eligible, time-bounded capacity -> valuable engineering outcome -> observable evidence -> reversible handoff

The skill exists to help the user choose a small amount of work that remains worthwhile if the window closes early, while protecting the next workday and honoring provider, team, and billing boundaries.

## Current-value rule

An expiring window creates a scheduling opportunity, not a project requirement. Every selected task must have a present-tense reason tied to the current project: a requirement, acceptance check, known maintenance risk, dependency, project standard, or explicitly approved outcome with a substantive project purpose. Approval sets scope; it does not make expiry-only work valuable. Ask whether the task would still be worth doing if the window were not closing. If not, reject it rather than inventing work to consume capacity.

When a task or implementation direction has already been rejected, reconstruct the current target from the trusted project state and simplify the affected slice from its root. Do not preserve a wrapper, fallback, name, test, or ledger entry merely because it appeared in the correction history. Preserve history only when current compatibility, migration, security, compliance, public API, audit, or rollout behavior depends on it.

## User profiles

Do not infer a profile from the repository name, operating-system locale, code language, or account. Ask the user to state only the fields that matter for the current run. A profile may be kept in the project-local ledger, but account identifiers and exact billing data should not be stored there.

| Profile | Typical need | Default posture |
| --- | --- | --- |
| Solo maintainer | Turn a periodic reset or short grant into small, useful maintenance | Low-risk, one project, strong reserve |
| Product builder | Reduce friction around a roadmap without opening a new feature branch of work | Prefer tests, docs, diagnostics, and bounded refactors |
| Multi-project maintainer | Decide where a limited window has the highest value | Allocate per project; never use one shared hidden queue |
| Team or enterprise user | Avoid spending shared capacity or creating an unreviewed change | Require ownership, explicit cap, and normal review path |
| Learner or side-project user | Make progress without risking the main project | Isolated branch/worktree, teaching-oriented handoff |
| User with unknown plan details | Wants a shortlist but cannot state a balance or expiry | Qualitative planning only; no quota claim or execution |

Useful profile fields are: timezone, working hours or next-workday boundary, project criticality, risk tolerance, preferred maintenance types, expected review availability, and the minimum reserve needed for the next workday.

## Trigger contract

### Activate when all of these are true

1. The user explicitly selects or names `$token-todo` (or the host's equivalent explicit skill selector).
2. The user wants to curate or execute bounded engineering work using capacity that they say is eligible, temporary, expiring, or otherwise available for this purpose.
3. The work can produce a concrete, reviewable artifact in a named project.

The user may invoke the skill for a plan-only pass, a ledger-maintenance pass, a Goal draft, or an approved execution pass. The activation itself never grants write permission.

An explicit invocation is a routing signal, not evidence that the user has eligible capacity. The run still needs a user-stated resource envelope before it can move beyond qualitative planning.

### Do not activate for these jobs

- Reading or estimating the user's actual account quota, reset timer, billing status, or provider-side usage.
- Monitoring a provider, scheduling recurring checks, sending reminders, or waking up later without a separate automation workflow.
- Emptying a balance for its own sake, flooding requests, retrying pointless prompts, using multiple accounts, or bypassing rate/fair-use controls.
- Spending paid overage, a team/shared allowance, or someone else's capacity without explicit ownership and a cap; the default is to decline.
- Production deployment, destructive cleanup, credential work, auth/billing changes, data migrations, or broad feature development solely because capacity is expiring.
- Ordinary coding tasks that do not involve this resource-allocation decision.

If a request is ambiguous, explain the boundary and ask for a compact envelope rather than silently activating execution mode.

## Product goals and non-goals

### Goals

- Convert user-offered eligible capacity into high-value, bounded engineering progress.
- Make tradeoffs visible: value, risk, effort, wall-clock time, uncertainty, reserve, and deadline buffer.
- Keep the project backlog useful after the resource window expires.
- Keep every selected task and retained ledger item justified by current project value rather than expiry pressure alone.
- Require explicit approval, small checkpoints, verification, and a known rollback route.
- Support plan/Goal workflows without pretending that a Goal is a quota monitor or a guarantee of completion.
- Work across languages, frameworks, and repositories using project-local context rather than provider-specific integrations.

### Non-goals

- Detecting, scraping, or reverse-engineering quotas, tokens, reset windows, or billing rules.
- Guaranteeing a token count, dollar amount, model behavior, or provider outcome.
- Making unattended changes that survive a missing approval, an exceeded budget, or a user cancellation.
- Creating a universal cross-project database of private work or account state.
- Replacing the project's tests, code review, deployment controls, or service terms.

## Success conditions

A run is successful when it leaves one or more of the following with evidence: a verified low-risk change, a curated and understandable task ledger, a paused but resumable checkpoint, or a clear blocked handoff. It is not successful merely because the forecasted capacity was consumed.

Track qualitative quality signals rather than provider telemetry:

- every executed task has a scope, acceptance check, and rollback route;
- reserve and deadline buffer were preserved;
- unrelated changes were not overwritten;
- verification results and unknowns are visible;
- no overage, shared-capacity, fair-use, or policy boundary was crossed;
- unfinished work is accurately labeled rather than hidden in a partial diff.
- stale, duplicate, and expiry-only candidates are not carried forward as if they were delivered value.
