# Date-Versioning Playbook

The mechanics behind the `api-design` skill: how to implement Stripe-style date versioning so core code only ever speaks the latest shape, and every old client keeps working.

## Components

1. **Version registry** — an ordered list of release dates, each mapping to the set of version-changes introduced on that date.
2. **Version-change module** — one per breaking change. Self-contained: a description, an optional **request transform**, and a **response transform**. Keyed by the date it shipped.
3. **Pinned version per client** — stored on the account/API key on first request; overridable per request via a version header.
4. **Core handlers** — always read and write the **latest** shape. They know nothing about old versions.

## The walk-backward algorithm

Core logic produces a latest-shape response. The version layer then transforms it *down* to the client's pinned version:

```
response = handler(request)                      # latest shape
for change in registry.changes_after(client_version):  # newest → oldest
    response = change.response_transform_down(response)  # undo the change
return response
```

Requests go the other direction — transform the incoming (old-shape) request *up* to the latest shape before the handler sees it:

```
for change in registry.changes_after(client_version):  # oldest → newest
    request = change.request_transform_up(request)
result = handler(request)
```

Direction matters: responses are walked newest→oldest (peel changes off), requests oldest→newest (apply changes on). Each transform is the inverse pair for one change.

## A version-change module

Example: on `2026-07-01` you split a bare `amount` integer (cents) into an `amount` object `{ value, currency }`. Latest shape uses the object; clients before `2026-07-01` must still see the integer.

```python
class AmountBecameObject:
    """2026-07-01: response `amount` int (cents) -> { value, currency }."""
    version = "2026-07-01"

    def response_transform_down(self, resp):
        # newest -> older: collapse object back to a bare integer
        amt = resp.get("amount")
        if isinstance(amt, dict):
            resp["amount"] = amt["value"]
        return resp

    def request_transform_up(self, req):
        # older -> newest: promote bare integer to object (assume usd default)
        amt = req.get("amount")
        if isinstance(amt, int):
            req["amount"] = {"value": amt, "currency": "usd"}
        return req
```

The core handler only ever sees/returns the object form. The integer form lives **only** in this module.

## Registry

```python
REGISTRY = [
    # date          changes introduced that date
    ("2026-06-17", []),                       # initial version
    ("2026-07-01", [AmountBecameObject()]),
    # ("2026-08-15", [SomethingElse()]),
]

def changes_after(client_version):
    """All changes with date > client_version, oldest first."""
    return [c for date, changes in REGISTRY if date > client_version for c in changes]
```

`changes_after("2026-06-17")` → `[AmountBecameObject]`, so a client pinned to the initial version still gets the integer. A client pinned to `2026-07-01` gets `[]` → the object, untouched.

## Pinning

- On a client's **first** request, store the current latest date as their pinned version.
- Accept an explicit per-request override header (e.g. `X-Api-Version: 2026-07-01`); validate it exists in the registry.
- New SDKs default to the latest date; document how to upgrade a pin.
- Never auto-advance a client's pin — that would deliver breaking changes unasked.

## Changelog & docs generation

Because every breaking change is a dated module with a description, the changelog writes itself: iterate the registry, emit each date and its change descriptions. Keep this in the API docs so versioning is first-class, not an afterthought.

## Testing

- Snapshot tests per supported version: hit each endpoint with each pinned version, assert the response shape.
- Round-trip test: `request_transform_up` then `response_transform_down` should reproduce the old client's mental model.
- CI fails if a field is removed/renamed/retyped on an **existing** version (contract test against recorded schemas).

## When to retire a version

Date versions are cheap to keep because they're encapsulated. Retire one only when no active client is pinned to it or older, and announce well ahead. Removing a version is itself a breaking change for anyone still on it.
