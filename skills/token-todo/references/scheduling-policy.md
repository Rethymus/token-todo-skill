# Scheduling and estimation policy

Use this reference whenever the user asks which tasks fit a resource window, asks for a forecast, or asks for a Goal that will run within a time and capacity envelope.

## 1. Treat the resource envelope as an input, not telemetry

Ask the user to provide the smallest useful envelope. A reusable form is:

```text
project: <one repository or project path>
resource_source: <periodic plan | temporary top-up | limited-time grant | other>
eligible_capacity: <user-stated cap/range and unit, or a relative share>
eligible_until: <date and time>
timezone: <IANA name or an unambiguous user label>
next_workday_reserve: <capacity and wall-clock reserve>
execution_timebox: <hard wall-clock maximum>
risk_tolerance: <low | medium | high, with high never implied by expiry>
external_effects: <local changes only | commit | push/PR | other, explicitly named>
overage_policy: <default: deny>
shared_capacity: <default: deny>
```

The envelope is a resource contract, not a request to maximize consumption. Also identify the target outcome, acceptance check, allowed paths, and non-goals for the run. If `eligible_capacity` is a range, commit only against its conservative lower bound; treat the upper bound as an optional planning scenario, never as permission to consume the reserve. If there is no defensible lower bound, stay plan-only.

Use abstract `work units` or the user's own units. They are planning units, not provider tokens and not a billing estimate. Never convert a provider's undocumented plan into token, request, or dollar math.

Hard constraints are applied before ranking:

```text
commitment_capacity = user-stated cap or conservative lower bound of the stated range
spendable_capacity = max(0, commitment_capacity - next_workday_reserve)
usable_time = eligible_until - time_reserve - current_time_in_user_timezone
```

If the user does not state a reserve, do not execute. For a proposal only, show a clearly labeled conservative scenario that leaves at least half of the stated eligible capacity and at least 60 minutes of wall-clock time untouched, then request confirmation. If the capacity unit, deadline, timezone, or ownership is unknown, keep the result qualitative and plan-only.

Always leave enough time for one verification checkpoint and a rollback decision. Do not treat the last minute before expiry as usable execution time.

Before scoring, reject a candidate that has no current project reason, no observable acceptance check, no rollback route, or whose only justification is that capacity is about to expire. Expiry may influence deadline fit among already-valid candidates; it never creates value or overrides risk.

## 2. Resource-source rules

| Source label | Default treatment | Additional guard |
| --- | --- | --- |
| Periodic plan capacity | Eligible only to the extent the user states it | Preserve the next-workday reserve and the user's deadline buffer |
| Temporary or promotional top-up | Eligible only if the user explicitly identifies it as available for this run | Do not infer its terms or extend its expiry |
| Limited-time free grant | Eligible only with a user-stated expiry and legitimate use | Never increase request volume just to exhaust it |
| Paid overage or pay-as-you-go | Deny; Token Todo does not select it | Route any paid work through the provider's normal billing approval workflow outside this skill; never silently fall back to it |
| Team/shared allowance | Deny; Token Todo does not select it | Use the normal owner-coordinated workflow outside this skill; never create a hidden shared queue |
| Unknown or mixed source | Not eligible | Separate the sources before planning; do not blend them into one balance |

No user instruction can authorize violating provider terms, organizational policy, fair-use limits, access controls, or another person's allocation.

## 3. Estimate in ranges

Use the following bands as communication aids, not promises. Adjust them for repository familiarity, test availability, tool calls, build times, generated files, external dependencies, and review complexity.

| Band | Typical shape | Forecasted agent interaction | Wall-clock forecast | Default fit |
| --- | --- | --- | --- | --- |
| XS | One narrow file or a focused test/doc change | 1-2 focused turns | 10-25 minutes | Safe harvest |
| S | Small behavior-preserving change with a targeted check | 2-5 turns | 25-60 minutes | Safe or balanced |
| M | Several related files or a refactor with broader checks | 5-12 turns | 1-2 hours | Split into checkpoints |
| L | Cross-cutting, uncertain, or multi-stage work | 12+ turns | More than 2 hours | Split or defer; never run as one opaque task |

Report a lower and upper bound, confidence (`high`, `medium`, or `low`), and the main uncertainty. A visible turn or tool count is not actual provider usage. If a task crosses its upper bound or its risk class changes, stop and re-plan.

## 4. Candidate scoring

First reject candidates that do not fit the hard capacity/time constraints, lack a validation method, lack a rollback path, or violate the resource-source policy. For the survivors, use ordinal judgments rather than fake precision:

1. current value: impact on current work and maintenance burden;
2. unblock value: whether it removes a known blocker or reduces future risk;
3. deadline fit: whether waiting loses the opportunity without creating urgency-driven risk;
4. verification strength: how easily correctness can be checked;
5. reversibility: how small and isolated the change is;
6. uncertainty and risk: unknown behavior, sensitive surfaces, or cross-cutting effects;
7. context-switch cost: how much new domain knowledge or setup is needed.

Prefer high value density: meaningful current outcome per unit of effort, time, and risk. Use this as an ordering heuristic, not a numerical claim:

```text
value density ~= (impact + unblock + urgency + confidence + reversibility)
                / (effort + time + risk + context switching)
```

When two candidates are close, choose the one with stronger verification and rollback. Do not choose a riskier task simply because it is larger or closer to expiry.

## 5. Default plan modes

Offer choices instead of silently selecting one. Percentages apply to `spendable_capacity`, not the user's total capacity, and may be reduced whenever uncertainty is high.

| Mode | Shape | Default cap | Use when |
| --- | --- | --- | --- |
| Conservative harvest | One or two XS/S tasks; docs, tests, diagnostics, narrow cleanup | Up to 35% of spendable capacity and 60 minutes | The next workday or project criticality matters most |
| Balanced maintenance | One S or one M split into atomic slices; targeted checks | Up to 60% of spendable capacity and 90 minutes | The user wants visible progress with moderate confidence |
| Deep bounded pass | One theme only; branch/worktree; checkpoints after every atomic slice | At most the explicitly approved remainder and 3 hours | The user confirms reserve, review availability, and medium-risk controls |

These are defaults, not entitlements. High-risk work is never selected solely because a window is expiring. A missing reserve or ambiguous ownership collapses the plan to a read-only shortlist.

## 6. Scheduling strategies

- **Reserve-aware deadline scheduling:** prioritize eligible work that may expire, but stop before the deadline buffer and preserve the next workday reserve.
- **Reversibility-first:** prefer isolated tests, documentation, diagnostics, and behavior-preserving refactors over irreversible changes.
- **Dependency-aware sequencing:** do the smallest prerequisite that unlocks later work; do not start a broad feature to justify a deadline.
- **Checkpointed small batches:** after each atomic task, compare the forecast, diff, tests, and risk with the approved envelope.
- **Value-density ordering:** choose high-value, high-confidence work before low-confidence “maybe useful” work.
- **Current-reason review:** before each checkpoint, re-check that the next task and every retained artifact still serve the approved current target; remove expiry-only residue from the plan or ledger.
- **Context locality:** stay in one project and one theme unless the user explicitly requests a multi-project allocation.
- **Fairness and rotation:** for an explicitly named multi-project run, allocate a separate cap per project and rotate only at checkpoints; never let one project consume an unbounded remainder.
- **Anti-gaming:** do not add artificial TODOs, run redundant tests, retry failures without new information, fan out requests, or use parallelism to evade a cap.
- **Timezone discipline:** normalize the expiry and next-workday boundary in the user's stated timezone; never infer it from the host, path, or locale.
