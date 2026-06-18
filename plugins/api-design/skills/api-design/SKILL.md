---
name: api-design
description: Design and evolve HTTP/RPC APIs with Stripe-style date-based versioning and strict backwards-compatibility rules. Use whenever creating a NEW API or endpoint, adding or changing request/response fields, or refactoring an existing API — to keep changes additive, version breaking changes by date, pin clients, and never break callers silently.
---

# API Design (date-versioned, backwards-compatible)

Apply this whenever you design a new API or change an existing one. The model is Stripe's: **rolling date-based versions**, additive-by-default, with breaking changes isolated behind a new dated version and a backward transform. The goal is that **a client written today keeps working forever** without code changes, while you keep shipping improvements.

## The one rule

> Never change the observable behavior of an existing version. Fields present today stay present, keep their name, and keep their type. New behavior goes in new fields, new endpoints, or a new dated version.

If a change can break a client that worked yesterday, it is a **breaking change** and requires a new version. Otherwise it is **additive** and ships immediately on the current version.

## Compatible vs. breaking

| Additive — ship now, no version bump | Breaking — needs a new dated version |
|---|---|
| Add a new endpoint | Remove or rename an endpoint |
| Add a new **optional** request field | Add a **required** request field |
| Add a new response field | Remove or rename a response field |
| Add a new enum value *(if clients are told to tolerate unknowns)* | Change a field's type, format, or units |
| Add a new optional query param | Change default values or pagination behavior |
| Loosen a validation rule | Tighten validation / add new error cases |
| | Change the meaning of an existing field |

When unsure, assume breaking. The cost of a needless version is small; the cost of a silent break is a paged engineer.

## Designing a NEW API

1. **Resource-oriented**: nouns for paths (`/invoices`, `/invoices/{id}`), verbs via HTTP methods. Consistent plural names.
2. **Stable identifiers**: opaque string IDs, prefixed by type (`inv_…`), never leak internal sequence numbers.
3. **Expansion over breakage**: design responses so growth is *additive* — return objects you can hang new fields on, not bare scalars. Prefer `{ "amount": { "value": 1200, "currency": "usd" } }` when a scalar might later need units.
4. **Pin from day one**: every response is rendered *as of* a version. Stamp the very first dated version now (today's date) and record it. Clients are pinned to the current version on their first request and send it explicitly thereafter (e.g. an `X-Api-Version: 2026-06-17` header).
5. **Tolerant readers**: document that clients must ignore unknown fields and unknown enum values. This is what makes additive changes safe.
6. **Errors are part of the contract**: stable, documented error shapes and codes. New error *codes* are additive only if clients have a documented default for unknown codes.

## Changing an EXISTING API

```
Is the change additive (left column above)?
├── YES → ship it on the current version. Update docs/changelog. Done.
└── NO  → it's breaking:
         1. Cut a new dated version (today's date).
         2. Make the new behavior the default in that version.
         3. Write a BACKWARD transform: given a new-shape response, produce the
            old shape for clients pinned to any earlier version. (And forward
            transform the request if its shape changed.)
         4. Register the version → change mapping. Add a changelog entry.
         5. Old clients keep getting old behavior; only clients that opt into
            the new version see the change.
```

Never edit an old version's behavior to "fix" it — that *is* the break. Add a version instead.

## Encapsulation (keeps maintenance cost flat)

Each breaking change is a self-contained module: its documentation, its request transform, and its response transform, keyed by the date it was introduced. Core handlers always speak the **latest** shape; the version layer walks backward through registered changes, applying transforms until it reaches the client's pinned version. New code never carries `if (oldVersion)` branches — that logic lives only in the encapsulated transforms.

See `versioning-playbook.md` for the registry/transform architecture, the walk-backward algorithm, request vs. response direction, pinning storage, changelog generation, and a worked example.

## Pre-ship checklist

- [ ] Every existing field keeps its name, type, and meaning in the current version.
- [ ] New request fields are optional (or the change is gated behind a new version).
- [ ] Breaking change? New dated version cut + backward transform written + registered.
- [ ] Changelog entry added, keyed by version date.
- [ ] Docs note: clients must ignore unknown fields/enum values.
- [ ] Tested against the **oldest supported version**, not just the latest.
- [ ] Default version for brand-new clients is the latest date.

## Anti-patterns

- A `/v2/` path copy of the whole API → use dated versions + transforms, not parallel trees.
- "Just one tiny rename" on the live version → it's a break; version it.
- Required new request field on an existing endpoint → breaks every current caller.
- Returning a bare scalar you'll later need to enrich → return an object.
- `if (version < X)` branches sprinkled in business logic → move them into transforms.
