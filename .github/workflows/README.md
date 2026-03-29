# GitHub Actions Workflows

Automated quality and versioning checks for the Claude Code plugins marketplace.

## Workflows

### `version-validation.yml`

Runs on:
- Pull requests with changes to plugins or marketplace.json
- Push to main

Checks:
- ✅ Version consistency (plugin.json ↔ marketplace.json)
- ✅ Semver format validation (X.Y.Z)
- ✅ Version bump enforcement (if code changed, version must be bumped)
- ✅ Git tag validation

**Self-hosted runner**: Yes - runs on your configured runner

### `release-tags.yml`

Runs on:
- Push to main with version changes

Automatically:
- 🏷️ Creates git tags for new plugin versions
- 📤 Pushes tags to repository

**Self-hosted runner**: Yes - runs on your configured runner

## Enabling on Self-Hosted Runner

1. Ensure runner is registered:
   ```bash
   # Check runner status in repository Settings → Actions → Runners
   ```

2. Workflows automatically run on self-hosted runners

3. For `release-tags.yml` to push tags, ensure:
   ```bash
   # Runner has git configured
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"

   # Runner has access to push to repository (SSH key or token)
   ```

## Manual Testing

Test workflows locally:

```bash
# Validate version consistency
plugins=("rdi" "python-dev")
for plugin in "${plugins[@]}"; do
  plugin_version=$(jq '.version' plugins/$plugin/.claude-plugin/plugin.json)
  marketplace_version=$(jq ".plugins[] | select(.name==\"$plugin\") | .version" .claude-plugin/marketplace.json)

  if [ "$plugin_version" != "$marketplace_version" ]; then
    echo "❌ Version mismatch: $plugin"
  else
    echo "✓ $plugin versions match"
  fi
done

# Validate semver format
for plugin in rdi python-dev; do
  version=$(jq -r '.version' plugins/$plugin/.claude-plugin/plugin.json)
  if [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "✓ $plugin semver valid: $version"
  else
    echo "❌ $plugin invalid semver: $version"
  fi
done
```

## Troubleshooting

### Workflows not running
- Check runner is online in Settings → Actions → Runners
- Verify workflows are enabled in Settings → Actions → General

### Tag creation fails
- Ensure runner has git user configured
- Verify runner token has permissions to push tags

### Version validation fails
- Check both files are updated in same commit
- Verify semver format (X.Y.Z)
- Run manual test scripts above

## See Also

- [`VERSIONING.md`](../../VERSIONING.md) - Complete versioning guide
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
