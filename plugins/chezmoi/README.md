# chezmoi

Claude Code skills for [chezmoi](https://www.chezmoi.io), the dotfile manager that keeps your configuration in sync across machines — with per-machine templating and encryption. Built from the full `chezmoi` CLI surface (v2.70) and the chezmoi.io documentation.

## Installation

```bash
/plugin marketplace add clzmj/claude-code-plugins
/plugin install chezmoi@clzmj
```

## Skills

### `chezmoi` — using chezmoi

Triggers whenever you work with chezmoi, dotfiles, `~/.local/share/chezmoi`, a `.chezmoi.toml.tmpl`, `dot_`/`private_`/`encrypted_`/`run_` source files, or ask to add/apply/diff/update managed config. Covers:

- the source → target state **mental model** and the `init → add → edit → apply → update` lifecycle
- **filename attributes** (`dot_`, `private_`, `encrypted_`, `exact_`, `run_once_`, …) and special files
- **templating** and **init-time prompts** that persist into config
- **age/gpg encryption** and **password-manager** secrets
- the daily **git loop**

Reference files: [`commands.md`](skills/chezmoi/commands.md) (every command + flags), [`templating.md`](skills/chezmoi/templating.md), [`encryption.md`](skills/chezmoi/encryption.md), [`attributes.md`](skills/chezmoi/attributes.md) (attributes, scripts, special files), [`architecture.md`](skills/chezmoi/architecture.md) (source-dir control + externals).

### `chezmoi-encrypted-repos` — architecting public + private + encrypted setups

Triggers when you want to **design or restructure** a dotfiles layout: multiple public and private repos split by responsibility, private content always pushed **encrypted with the key kept off-repo**, provisioned by a **prompt-driven `chezmoi init`**. Gives topology decision trees, the public-repo-composing-private-externals pattern, key-delivery options (manual / passphrase-protected-key-in-repo / password manager), and an assembled reference architecture with a design checklist.

See [`skills/chezmoi-encrypted-repos/SKILL.md`](skills/chezmoi-encrypted-repos/SKILL.md).

## License

Apache-2.0 — Carlos Lezama (carlos@carrots.sh)
