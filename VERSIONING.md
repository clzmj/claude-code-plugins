# Versioning Strategy

This marketplace uses **Semantic Versioning** with automated GitHub Actions guardrails to ensure consistency.

## Semantic Versioning

Each plugin follows **Semantic Versioning 2.0.0**:

```
MAJOR.MINOR.PATCH
```

- **MAJOR** (e.g., 2.0.0): Breaking changes, removed features
- **MINOR** (e.g., 1.1.0): New features, new agents/skills (backward compatible)
- **PATCH** (e.g., 1.0.1): Bug fixes, documentation, config tweaks

## When to Bump Each

### PATCH (1.0.1)
- Bug fixes
- Documentation updates
- Configuration refinements
- Typo corrections
- Security patches

**Example**: Fix in `ruff.toml` configuration

### MINOR (1.1.0)
- New agents added
- New skills added
- New templates or examples
- Feature additions

**Example**: Add new `python-lsp-migrator` agent

### MAJOR (2.0.0)
- Removed agents or skills
- Breaking changes to agent/skill interface
- Removed plugin components
- Incompatible plugin.json structure changes

**Example**: Restructure agent interface format

## How to Release

### 1. Make your code changes

```bash
# Edit plugin files
vim plugins/python-dev/skills/uv/uv-workflows.md
git add plugins/python-dev/
```

### 2. Bump version in TWO places

**File 1**: `plugins/PLUGIN/.claude-plugin/plugin.json`
```json
{
  "name": "python-dev",
  "version": "1.0.1"
}
```

**File 2**: `.claude-plugin/marketplace.json`
```json
{
  "plugins": [
    {
      "name": "python-dev",
      "version": "1.0.1"
    }
  ]
}
```

⚠️ **Both must match or CI will fail!**

### 3. Commit with version bump message

```bash
git add plugins/python-dev/.claude-plugin/plugin.json
git add .claude-plugin/marketplace.json

git commit -m "chore: bump python-dev to 1.0.1

- Fix ruff configuration rule
- Update LSP documentation"
```

### 4. Push to main

```bash
git push origin main
```

**GitHub Actions will automatically**:
- ✅ Validate version consistency
- ✅ Validate semver format
- ✅ Ensure code changes had version bumps
- ✅ Create git tag (e.g., `python-dev@1.0.1`)

## Current Versions

| Plugin | Version | Git Tag |
|--------|---------|---------|
| `rdi` | 1.0.0 | `rdi@1.0.0` |
| `python-dev` | 1.0.0 | `python-dev@1.0.0` |

## GitHub Actions Guardrails

### On Pull Requests

When you open a PR:
1. ✅ Versions must match between `plugin.json` and `marketplace.json`
2. ✅ Versions must follow semver format (e.g., `1.0.0`)
3. ✅ If code changed, version must be bumped

### On Push to Main

When you push to main:
1. ✅ Same validation as PR
2. ✅ Git tags are automatically created for new versions
3. ✅ Tags are pushed to repository

## Examples

### Example 1: Bug Fix (PATCH)

```bash
# Current version: python-dev@1.0.0

# 1. Fix the bug
vim plugins/python-dev/ruff.toml

# 2. Bump PATCH version in both files
# plugins/python-dev/.claude-plugin/plugin.json: 1.0.0 → 1.0.1
# .claude-plugin/marketplace.json: 1.0.0 → 1.0.1

# 3. Commit
git commit -m "fix: update ruff rule configuration

- Fix E731 lambda assignment rule
- Improve docstring formatting"

# 4. Push
git push origin main

# GitHub Actions automatically creates: python-dev@1.0.1
```

### Example 2: New Feature (MINOR)

```bash
# Current version: python-dev@1.0.1

# 1. Add new agent
touch plugins/python-dev/agents/python-lsp-migrator.md

# 2. Bump MINOR version in both files
# plugins/python-dev/.claude-plugin/plugin.json: 1.0.1 → 1.1.0
# .claude-plugin/marketplace.json: 1.0.1 → 1.1.0

# 3. Commit
git commit -m "feat: add python-lsp-migrator agent

- New agent for migrating LSP configurations
- Includes templates for ruff and ty"

# 4. Push
git push origin main

# GitHub Actions automatically creates: python-dev@1.1.0
```

### Example 3: Breaking Change (MAJOR)

```bash
# Current version: rdi@1.0.0

# 1. Restructure agent interface
# (significant changes to agents/)

# 2. Bump MAJOR version in both files
# plugins/rdi/.claude-plugin/plugin.json: 1.0.0 → 2.0.0
# .claude-plugin/marketplace.json: 1.0.0 → 2.0.0

# 3. Commit
git commit -m "BREAKING: restructure agent interface

Agent format changed from markdown to YAML.
See MIGRATION.md for upgrade guide."

# 4. Push
git push origin main

# GitHub Actions automatically creates: rdi@2.0.0
```

## Checking Current Versions

### List all tags

```bash
git tag -l
```

### List tags for specific plugin

```bash
git tag -l "python-dev@*"
git tag -l "rdi@*"
```

### View tag details

```bash
git show python-dev@1.0.1
```

## If Something Goes Wrong

### Version mismatch error

**Error**: `Version mismatch for python-dev!`

**Fix**: Ensure both files have same version:
```bash
# Check current versions
jq '.version' plugins/python-dev/.claude-plugin/plugin.json
jq '.plugins[] | select(.name=="python-dev") | .version' .claude-plugin/marketplace.json

# Update the one that's out of sync
```

### Semver format error

**Error**: `Invalid semver format for python-dev: 1.0`

**Fix**: Use MAJOR.MINOR.PATCH format:
```bash
# Wrong:  1.0, 1, 1.0.0.1
# Right:  1.0.0, 1.0.1, 2.0.0
```

### Code changed but version not bumped

**Error**: `Code changed in python-dev but version not bumped!`

**Fix**: Update version in both files before pushing:
```bash
# Update .claude-plugin/plugin.json version
# Update .claude-plugin/marketplace.json version
git add . && git commit --amend --no-edit
git push origin main --force-with-lease
```

## Best Practices

1. **Bump versions with code changes** - Don't separate version bumps into different commits
2. **Keep both locations in sync** - Always update plugin.json AND marketplace.json
3. **Use meaningful commit messages** - Include what changed and why
4. **One version per release** - Don't bump twice in one PR
5. **Increment correctly** - Follow semver rules consistently
6. **Document breaking changes** - MAJOR versions need migration guidance

## Version Bump Checklist

- [ ] Code changes are complete and tested
- [ ] Determined version type (MAJOR, MINOR, PATCH)
- [ ] Updated `plugins/PLUGIN/.claude-plugin/plugin.json`
- [ ] Updated `.claude-plugin/marketplace.json`
- [ ] Versions match between both files
- [ ] Committed with descriptive message
- [ ] Pushed to main
- [ ] GitHub Actions passed validation
- [ ] Git tag was created automatically

## Resources

- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- GitHub Actions workflows in `.github/workflows/`
