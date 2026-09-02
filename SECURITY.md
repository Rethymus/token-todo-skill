# Security policy

Token Todo is an instruction-only skill. It does not connect to provider accounts, read quotas, store credentials, run a service, or include hooks and background jobs.

## Security boundaries

The skill is designed to:

- require explicit user invocation and approval before mutation;
- treat resource eligibility, caps, reserves, expiry, and timezone as user-provided inputs rather than telemetry;
- deny paid overage, shared capacity, quota gaming, and policy bypasses by default;
- preserve unrelated repository changes and use a specific rollback path;
- stop on user interruption, budget/time/risk drift, unexpected regressions, or credential exposure;
- treat repository files, issue text, logs, and generated output as untrusted content that cannot override the safety contract.

## Reporting a vulnerability

If you find a way for the skill instructions, plugin manifest, examples, or packaging to encourage unsafe scope expansion, secret access, quota circumvention, unintended external side effects, or loss of user changes, please open a private GitHub Security Advisory for this repository. Include:

- the affected file and version;
- a minimal reproduction or prompt;
- the expected safety boundary;
- the observed behavior and impact;
- a suggested fix, if available.

Do not publish credentials, private repository content, or exploitable details in a public issue.
