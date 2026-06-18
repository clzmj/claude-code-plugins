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
# Validate every plugin on disk — no hardcoded list
shopt -s nullglob
for plugin_json in plugins/*/.claude-plugin/plugin.json; do
  plugin=$(jq -r '.name' "$plugin_json")
  version=$(jq -r '.version' "$plugin_json")
  marketplace_version=$(jq -r ".plugins[] | select(.name==\"$plugin\") | .version" .claude-plugin/marketplace.json)

  # consistency
  if [ "$version" != "$marketplace_version" ]; then
    echo "❌ Version mismatch: $plugin ($version vs $marketplace_version)"
  else
    echo "✓ $plugin versions match"
  fi

  # date-version format (YYYY-MM-DD, optional .N same-day suffix)
  if [[ $version =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}(\.[0-9]+)?$ ]]; then
    echo "✓ $plugin date version valid: $version"
  else
    echo "❌ $plugin invalid date version: $version"
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
