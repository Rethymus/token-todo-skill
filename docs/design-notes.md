# Design notes and prior art

This document records the public practices that informed Token Todo and how they were adapted. It keeps research and design provenance reviewable without loading the entire history into the agent-facing skill.

## Sources reviewed

| Source | Practice observed | Adaptation in this repository |
| --- | --- | --- |
| [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | Focused skills, discriminating descriptions, progressive disclosure, and explicit versus implicit invocation | One narrow resource-allocation job; trigger boundaries live in frontmatter and `agents/openai.yaml`; details remain in focused references and human-facing READMEs |
| [OpenAI Plugins](https://github.com/openai/plugins) | Stable plugin identity through `.codex-plugin/plugin.json`; skills kept under `skills/` | A minimal skill-only plugin with no invented MCP, app, or marketplace runtime dependency |
| [Agent Skills specification](https://agentskills.io/specification) | Portable frontmatter contract, naming constraints, and optional metadata | Spec-compatible `token-todo` directory and frontmatter with author/version metadata |
| [Anthropic Skills](https://github.com/anthropics/skills) | Progressive disclosure and allowing simple skills to remain self-contained | Core instructions stay compact; scheduling, ledger, safety, and Goal detail load only when needed |
| [Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills) | Human-facing “use when,” installation, examples, structure, and per-skill metadata | Mirrored English/Chinese guides with trigger and non-trigger boundaries, installation paths, and repository map |
| [Superpowers: writing-skills](https://github.com/obra/superpowers/blob/master/skills/writing-skills/SKILL.md) | Trigger descriptions should not become workflow shortcuts; pressure scenarios expose unsafe decisions | The explicit-only policy is kept in metadata, while scenario cases test tempting quota, expiry, and scope decisions |
| Mature open-source skill repository practice | Product-facing README order, bilingual entry points, installation paths, behavioral boundaries, validation instructions, repository map, provenance, and governance | Token Todo uses a linear README that explains the user problem, operating standard, linked decisions, use boundaries, examples, validation, and contribution surface before pointing to deeper references |

## Design choices

### One portable skill, one optional package

The canonical capability is `skills/token-todo`. The root plugin manifest gives Codex a stable package identity without making the skill depend on account telemetry, a scheduler, an MCP server, an app connector, or a runtime service. Hosts that understand the Agent Skills layout can install only the skill directory.

### Resource pressure is a constraint, not a product goal

The motivating problem is easy to misread as “spend the balance.” Token Todo instead requires a current project target, a user-stated resource envelope, a protected reserve, and observable acceptance. Expiry may break ties among valid candidates; it cannot create value, justify artificial work, or lower the safety bar.

### Product-facing README before implementation detail

The README is deliberately organized as a user-facing product entry point. It answers, in order, what problem the skill solves, what decisions it makes, when it should or should not be used, how to install it, what a safe request looks like, what it protects, how to validate it, and where the deeper instructions live. The bilingual pages keep those claims and boundaries aligned; implementation-level policy remains in `SKILL.md` and its focused references.

### Current-state language over expiry incident language

The skill does not preserve a quota-expiry story as a reason for production artifacts. It gives the agent a positive target, a present-tense current-value rule, a root-first correction rule, a counterfactual audit, and explicit exceptions for operational history. This keeps a useful ledger after the resource window closes.

### Explicit operational exceptions

“Remove all history” would be unsafe. Compatibility, migrations, public APIs, security controls, compliance or audit evidence, and reversible rollouts can require historical mechanisms. Token Todo preserves the minimum necessary mechanism and records its current reason, while protecting unrelated user work.

### Honest testing boundary

The dependency-free validator proves repository structure, metadata consistency, documentation links, and scenario shape. It does not pretend to prove model behavior. The scenario corpus supplies repeatable prompts and decision-level expectations for evaluation on a chosen host and model.

### Minimal governance

The repository includes contribution, security, issue, pull-request, and CI guidance because they affect real collaboration. It omits runtime code, account integrations, dependency lockfiles, generated documentation, icons, and a marketplace index because none is required for this instruction-only package.

## Reuse statement

No third-party skill implementation or prose is vendored. Public repositories and specifications were used as prior art for structure and evaluation practice. The implementation and Token Todo-specific policy are original; the standard MIT license text is the only conventional legal text reproduced verbatim.
