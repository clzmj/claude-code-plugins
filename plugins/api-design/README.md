# api-design

A Claude Code skill that makes Claude apply **Stripe-style date-based API versioning** and strict backwards-compatibility rules whenever you design a new API or evolve an existing one.

## Installation

```bash
/plugin marketplace add clzmj/claude-code-plugins
/plugin install api-design@clzmj
```

## What it does

The `api-design` skill triggers when you create a new API or endpoint, add/change request or response fields, or refactor an existing API. It steers the work toward:

- **One rule** — never change the observable behavior of an existing version; new behavior goes in new fields, endpoints, or a new dated version.
- **Additive by default** — new endpoints/fields/optional params ship immediately on the current version.
- **Breaking changes get a date** — removals, renames, retypes, and behavior changes are cut as a new dated version with a backward transform, so existing clients are untouched.
- **Client pinning** — clients pin on first request and opt into newer versions explicitly.
- **Flat maintenance cost** — each breaking change is an encapsulated transform module; core code only ever speaks the latest shape.

See [`skills/api-design/SKILL.md`](skills/api-design/SKILL.md) for the rules and checklist, and [`skills/api-design/versioning-playbook.md`](skills/api-design/versioning-playbook.md) for the registry/transform architecture with a worked example.

## Background

Based on Stripe's API versioning approach: <https://stripe.com/blog/api-versioning>. This marketplace itself uses date versioning for its plugins — see [VERSIONING.md](../../VERSIONING.md).

## License

Apache-2.0 — Carlos Lezama (carlos@carrots.sh)
