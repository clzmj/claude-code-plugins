# Versioning Strategy

This marketplace uses **Semantic Versioning with manual releases**. Versions are determined exclusively by git tags, not by version numbers in code files.

## Semantic Versioning

Each plugin follows **Semantic Versioning 2.0.0**:

```
MAJOR.MINOR.PATCH
```

- **MAJOR** (e.g., 2.0.0): Breaking changes, removed features
- **MINOR** (e.g., 1.1.0): New features, new agents/skills (backward compatible)
- **PATCH** (e.g., 1.0.1): Bug fixes, documentation, configuration tweaks

## Source of Truth: Git Tags

The **canonical version is recorded in git tags**, not in code files. File versions are always synchronized via the release workflow.

Tag format: `PLUGIN@vMAJOR.MINOR.PATCH`

Examples:
- `python-dev@v1.0.0` — canonical tag for python-dev version 1.0.0
- `python-dev@v1.0` — floating alias (latest 1.0.x)
- `python-dev@v1` — floating alias (latest 1.x.x)
- `python-dev@latest` — floating alias (latest version overall)

## How to Release

### 1. Go to GitHub Actions

In your repository, navigate to: **Actions → Release Plugin**

### 2. Click "Run workflow"

Fill in the inputs:
- **Plugin**: Choose `rdi` or `python-dev`
- **Bump**: Choose `patch`, `minor`, or `major`

### 3. The workflow automatically:

1. Scans existing git tags for that plugin
2. Computes the new version
3. Updates `plugins/PLUGIN/.claude-plugin/plugin.json`
4. Updates `.claude-plugin/marketplace.json`
5. Creates a commit with message: `chore: release PLUGIN vX.Y.Z`
6. Pushes the commit to main
7. Creates the canonical tag (e.g., `python-dev@v1.0.1`)
8. Creates and force-pushes alias tags

### Done!

The release is complete. Users can install the new version immediately.

## Current Versions

Query existing versions via git tags:

```bash
# List all tags
git tag -l

# List tags for specific plugin
git tag -l "python-dev@*"
git tag -l "rdi@*"

# Show latest version
git describe --tags --abbrev=0 --match "python-dev@*"
```

Current:
- `rdi@v1.0.0`
- `python-dev@v1.0.0`

## Examples

### Example 1: Bug Fix (PATCH)

**Scenario**: Found a typo in ruff.toml

**Steps**:
1. Fix the typo in `plugins/python-dev/ruff.toml`
2. Commit and push: `git commit -m "fix: ruff rule typo" && git push`
3. Go to GitHub Actions → Release Plugin
4. Select: Plugin = `python-dev`, Bump = `patch`
5. Click "Run workflow"
6. ✅ Done! Version is now `1.0.1` with tags `python-dev@v1.0.1`, `python-dev@v1.0`, `python-dev@latest`, etc.

### Example 2: New Feature (MINOR)

**Scenario**: Added new agent to python-dev

**Steps**:
1. Add agent file `plugins/python-dev/agents/new-agent.md`
2. Commit and push: `git commit -m "feat: add new-agent" && git push`
3. Go to GitHub Actions → Release Plugin
4. Select: Plugin = `python-dev`, Bump = `minor`
5. Click "Run workflow"
6. ✅ Done! Version is now `1.1.0`

### Example 3: Breaking Change (MAJOR)

**Scenario**: Restructured agent interface

**Steps**:
1. Restructure `plugins/rdi/agents/*`
2. Update agent format documentation
3. Commit and push
4. Go to GitHub Actions → Release Plugin
5. Select: Plugin = `rdi`, Bump = `major`
6. Click "Run workflow"
7. ✅ Done! Version is now `2.0.0` (breaking change)

## FAQ

### Q: Do I need to manually update version numbers in code?

**A**: No. Never manually change versions in `plugin.json` or `marketplace.json`. The release workflow handles this automatically.

### Q: What if I committed code but didn't want to release yet?

**A**: That's fine! Commits to main don't automatically release. Only trigger the release workflow when you're ready to bump the version and create a tag.

### Q: Can I release multiple plugins at once?

**A**: No, release one plugin at a time via the release workflow. Each plugin has independent versioning.

### Q: What if the version computation is wrong?

**A**: The workflow scans all existing tags matching `PLUGIN@v*.*.*` and bumps the highest one. If something goes wrong, delete the incorrect tag with `git push origin --delete PLUGIN@vX.Y.Z` and re-run the workflow.

### Q: How do I revert a release?

**A**: 1. Delete the bad tag: `git push origin --delete PLUGIN@vX.Y.Z`
2. Optionally delete alias tags too
3. Reset the version files to the previous version
4. Commit the reset
5. Re-run release workflow if needed

## Glossary

- **Canonical tag**: The precise version tag (e.g., `python-dev@v1.0.1`)
- **Alias tag**: Floating pointer that moves with each release (e.g., `python-dev@latest`)
- **Semver**: Semantic Versioning (X.Y.Z format)
- **Self-hosted runner**: GitHub Actions runner on your infrastructure

## See Also

- `.github/workflows/release.yml` — The release workflow
- `.github/workflows/version-validation.yml` — Consistency validation
- `scripts/compute_plugin_version.py` — Version computation script
