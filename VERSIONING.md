# Versioning Strategy

This marketplace uses **date-based versioning** (Stripe-style), not semantic versioning. A plugin's version **is its release date**.

> Inspired by Stripe's API versioning: <https://stripe.com/blog/api-versioning>. The `api-design` plugin in this repo teaches the same approach for APIs you build.

## Format

```
YYYY-MM-DD          e.g. 2026-06-17
YYYY-MM-DD.N        e.g. 2026-06-17.2   (second release on the same day)
```

The version string is what Claude Code uses as the **update cache key** — when it changes, users receive the update. The optional `.N` suffix exists only so a same-day re-release still produces a new string.

Tag format: `PLUGIN@YYYY-MM-DD` (e.g. `ruff-lsp@2026-06-17`), plus a floating `PLUGIN@latest` alias.

## Source of Truth: Git Tags

The canonical version is recorded in **git tags**. File versions in `plugin.json` and `marketplace.json` are synchronized by the release workflow.

## How to Release

1. **Actions → Release Plugin → Run workflow**
2. Inputs:
   - **Plugin**: the plugin's directory name under `plugins/` (e.g. `ruff-lsp`). The release script validates it against the plugins on disk, so there's no list to keep in sync.
   - **Date** *(optional)*: `YYYY-MM-DD`; leave blank to use today (UTC on the runner)
3. The workflow:
   1. Computes the version = the release date (adding `.N` if that date is already tagged for this plugin)
   2. Updates `plugins/PLUGIN/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
   3. Commits `chore: release PLUGIN YYYY-MM-DD` and pushes to main
   4. Creates the canonical tag `PLUGIN@YYYY-MM-DD` and force-updates `PLUGIN@latest`

## Current Versions

```bash
git tag -l                        # all tags
git tag -l "ruff-lsp@*"           # tags for one plugin
git describe --tags --abbrev=0 --match "ruff-lsp@*"   # latest for a plugin
```

All plugins are currently at `2026-06-17` (initial date-versioned release; tags are created on first run of the release workflow).

> **History note:** `rdi` previously used semver tags (`rdi@v1.0.x`). Those tags remain in git history but are superseded by date versions. New releases use the `PLUGIN@YYYY-MM-DD` scheme.

## Examples

### Backwards-compatible change (docs, bug fix, new optional behavior)
1. Make the change in `plugins/PLUGIN/...`
2. Commit and push
3. Release Plugin → Plugin = `PLUGIN`, Date = blank (today)
4. ✅ Version becomes today's date.

### Two releases in one day
1. Release once → `2026-06-17`
2. Later that day, release again → workflow computes `2026-06-17.2` automatically.

### Backdated / coordinated release
1. Release Plugin → Plugin = `PLUGIN`, Date = `2026-06-20`
2. ✅ Version and tag use the supplied date.

## FAQ

**Do I manually edit version numbers?** No — the release workflow writes them. (For quick local iteration you can leave `version` unset to fall back to commit-SHA versioning, but published plugins here pin a date.)

**Why dates instead of semver?** Releases here are snapshots, not API contracts with consumers who need semver ranges. Dates make "when did this ship" obvious and match the API-design philosophy this marketplace promotes. Breaking-change semantics for *APIs you build* are handled by the `api-design` plugin, not by the plugin's own release version.

**How do I revert a release?** Delete the tag (`git push origin --delete PLUGIN@YYYY-MM-DD`), reset the `version` fields, commit, and re-run if needed.

## See Also

- `.github/workflows/release.yml` — release workflow
- `.github/workflows/version-validation.yml` — version consistency + date-format check
- `scripts/compute_plugin_version.py` — date version computation
- `plugins/api-design/` — Stripe-style date versioning for APIs you design
