---
name: chezmoi
description: Manage dotfiles across machines with chezmoi — the source/target mental model, the init→add→edit→apply→update lifecycle, source-state filename attributes, templating, init-time prompts, age/gpg encryption, scripts, and the daily git loop. Use whenever the user works with chezmoi, dotfiles, ~/.local/share/chezmoi, a .chezmoi.toml.tmpl, dot_/private_/encrypted_/run_ source files, or asks to add/apply/diff/update managed config files. For designing a multi-repo public+private encrypted layout, use chezmoi-encrypted-repos.
---

# chezmoi

chezmoi manages your dotfiles as a git repo of *source definitions* and applies a computed *target state* to your home directory, with per-machine templating and encryption. Verified against chezmoi v2.70.

## Mental model — four states

```
source state  ──(evaluate templates with config + data)──▶  target state
(~/.local/share/chezmoi, a git repo)                        (computed: files, dirs,
                                                             symlinks, scripts, removals)
                                                                      │ diff
                                                                      ▼
config (~/.config/chezmoi/chezmoi.toml)              destination state (your ~, "destDir")
per-machine data + settings, NOT in the repo
```

- **Source directory** `~/.local/share/chezmoi` — git working tree of source definitions. Override: `--source`/`-S` or `$CHEZMOI_SOURCE_DIR`.
- **Source state** — desired state encoded in **filenames** (attribute prefixes/suffixes) plus `.tmpl` templates.
- **Config file** `~/.config/chezmoi/chezmoi.toml` (or `.yaml`/`.json`) — machine-specific data + settings. Generated on `init` from `.chezmoi.toml.tmpl`. **Lives outside the repo** (holds per-machine answers/secrets). Edit with `chezmoi edit-config`.
- **Target state** — *computed* from source + config + data. **Destination state** = current actual contents of `~`.

`chezmoi apply` is idempotent: it only changes what differs. **Always `chezmoi diff` or `chezmoi status` before `apply`.**

## Lifecycle

```bash
# First machine — start a repo
chezmoi init                      # create source dir + git repo
chezmoi add ~/.bashrc ~/.zshrc    # capture files into source state
chezmoi add --template ~/.gitconfig   # capture as a template
chezmoi cd; git add -A && git commit -m "init" && git remote add origin … && git push; exit

# New machine — clone + apply in one step
chezmoi init --apply git@github.com:user/dotfiles.git
chezmoi init --apply user          # shorthand → github.com/user/dotfiles (HTTPS); --ssh for SSH

# Daily loop
chezmoi edit --apply ~/.zshrc      # edit SOURCE of a target, then apply
#   or edit the real file, then:  chezmoi re-add ~/.zshrc
chezmoi diff                       # preview pending changes
chezmoi apply                      # make ~ match target state
chezmoi update                     # git pull --autostash --rebase + apply (on any machine)
```

`status` columns: **col 1 = change to source**, **col 2 = change apply would make to destination**; letters `A`dded `M`odified `D`eleted `R`un-script.

## Source-state filename attributes (how filenames encode state)

Attributes are **prefixes** on the source filename; `.tmpl` is a suffix. `chezmoi add` flags set most of them; toggle manually with `chezmoi chattr +template,+encrypted ~/.x`.

| Attr | Target effect |
|---|---|
| `dot_` | leading `.` (`dot_bashrc` → `.bashrc`) |
| `private_` | strip group/world perms (0600/0700) |
| `readonly_` | remove write bits |
| `executable_` | add execute bit |
| `empty_` | keep a zero-length file (empties are removed otherwise) |
| `exact_` (dirs) | delete any dir entry not present in source |
| `encrypted_` | content stored encrypted in source (suffix `.age`/`.asc`) |
| `symlink_` | target is a symlink; file content = link target |
| `create_` | create only if missing, never overwrite |
| `modify_` | source is a script; its stdout becomes the new file content (current content on stdin) |
| `remove_` | remove the target |
| `external_` | treat children literally (don't parse attrs) — submodules/checked-in dirs |
| `literal_` | stop attribute parsing |

**Prefix order is fixed:** `remove_`→`external_`→`exact_`→`private_`→`readonly_`→`empty_`→`executable_`→`encrypted_`→`create_`/`modify_`/`run_`/`symlink_`→(`once_`|`onchange_`)→(`before_`|`after_`)→`dot_`.

Examples: `private_dot_ssh/private_config` → `~/.ssh/config` 0600 inside 0700. `encrypted_private_dot_netrc.tmpl.age` → `~/.netrc`, decrypted + templated + 0600. `exact_dot_config/exact_nvim/` → `~/.config/nvim` with strays deleted.

**Scripts:** `run_` (every apply), `run_once_` (once per unique content hash, ever), `run_onchange_` (when rendered content changes). Combine with `before_`/`after_` to order vs. file application. Hashing is **post-templating**; a script that renders empty does not run; scripts must be idempotent; `--dry-run` never runs them. See `attributes.md`.

## Templating (per-machine differences)

A file is a template if its source name ends `.tmpl` or it lives under `.chezmoitemplates/`. Go `text/template` syntax. Test with `chezmoi execute-template '{{ .chezmoi.os }}'`.

```
{{ if eq .chezmoi.os "darwin" }}…{{ else if eq .chezmoi.os "linux" }}…{{ end }}
```

Key built-ins (full list: `chezmoi data`): `.chezmoi.os`, `.chezmoi.arch`, `.chezmoi.hostname` (up to first `.`), `.chezmoi.fqdnHostname`, `.chezmoi.username`, `.chezmoi.homeDir`, `.chezmoi.sourceDir`, `.chezmoi.config.*`. `.chezmoi.kernel`/`.chezmoi.osRelease` are **Linux-only** — guard with `if eq .chezmoi.os "linux"`. Your own data comes from `.chezmoidata/*` and the config `[data]` section. Full reference: `templating.md`.

## Init-time prompts that persist (questionnaire on `chezmoi init`)

Put a config template `.chezmoi.toml.tmpl` at the source root. On `init` it renders to `~/.config/chezmoi/chezmoi.toml`. Whatever you write under `[data]` becomes template data (`.email`, `.work`, …) everywhere afterward. **Prompt functions only work during init.**

```toml
{{- $email := promptStringOnce . "email" "Email address" -}}
{{- $work  := promptBoolOnce   . "work"  "Is this a work machine" false -}}
[data]
    email = {{ $email | quote }}    # strings: pipe through | quote
    work  = {{ $work }}             # bools/ints: emit bare
```

`*Once` variants only prompt if the value isn't already in `[data]` → idempotent re-init across machines. `--prompt` forces re-ask; `--promptString "Email address=x"` / `--promptDefaults` drive it non-interactively (CI). **Gotcha:** the `path` arg (`"email"`) must match the `[data]` key, or it re-prompts every time. Full signatures: `templating.md`.

## Encryption (secrets at rest)

chezmoi encrypts **per file** via the `encrypted_` attribute (not the whole repo). The **decryption key lives outside the repo**, so the repo can be public while secrets stay sealed.

```toml
encryption = "age"          # MUST be top-level, before any [section], or silently ignored
[age]
    identity  = "~/.config/chezmoi/key.txt"   # private key — NEVER committed
    recipient = "age1…"                       # public recipient — safe to commit
```

```bash
chezmoi age-keygen --output=~/.config/chezmoi/key.txt   # store OUTSIDE the source dir
chezmoi add --encrypt ~/.ssh/id_rsa                     # → encrypted_private_dot_ssh/…age
```

`apply`/`diff`/`status` decrypt transparently. Adding a new recipient is **not** retroactive — re-add to re-encrypt (`chezmoi re-add --re-encrypt`). gpg is the alternative backend.

A file can be both encrypted **and** a template (`encrypted_private_dot_netrc.tmpl.age` — backend suffix comes after `.tmpl`): on apply chezmoi **decrypts first, then renders**. But `prompt*` functions are **init-only** — you cannot prompt while applying an encrypted template; prompt once at init, persist to `[data]`, and the encrypted template reads that. Note a prompted value persisted to `[data]` is **plaintext in config**, so don't prompt for secrets — prompt for a passphrase that unlocks a key instead. Full guide incl. encrypted-templates-plus-prompts and the passphrase-protected-key bootstrap: `encryption.md`.

## Pulling in other repos & secrets

- **`.chezmoiexternal.toml`** — declare `git-repo`/`archive`/`file` externals to compose a public repo that references private repos (gated on SSH-key presence). See `architecture.md`.
- **Password managers** — resolve secrets at apply-time from 1Password/pass/keyring with template functions (`onepasswordRead`, `pass`, `keyring`); nothing encrypted lives in the repo, only the reference. See `encryption.md`.

## Designing public + private + encrypted multi-repo setups

When the user wants to *architect* their dotfiles — public and private content, everything pushed encrypted with the key kept elsewhere, multiple repos split by responsibility, a prompt-driven bootstrap — use the **chezmoi-encrypted-repos** skill.

## Command reference

Full flags and semantics for every command (`init`, `add`, `apply`, `re-add`, `edit`, `diff`, `status`, `managed`, `forget`, `destroy`, `merge`, `chattr`, `state`, …): **`commands.md`**.

## Top gotchas

- Run `chezmoi diff`/`status` before `apply`; use `--dry-run --verbose` to preview anything (incl. `.chezmoiremove`).
- `encryption = "…"` must precede all `[section]` tables in the config.
- The age/gpg **identity (private key) never goes in the repo**; only the public recipient does.
- `re-add` only updates already-managed files and **leaves templates alone** — edit templates with `chezmoi edit`, or force-overwrite with `chezmoi add --force`.
- `forget` stops managing but keeps the file in `~`; `destroy` permanently deletes it from both — irreversible.
- `.chezmoiignore` is **excludes-win**, not gitignore last-match-wins; it's templated, so use it to keep private files off public machines.
- With a **public** repo, `git.autoPush = true` will push any plaintext secret you accidentally `add` — encrypt or use a password manager.
- The config file holds per-machine answers/secrets and is intentionally **not** in the repo; regenerate it with `chezmoi init` (re-runs `.chezmoi.toml.tmpl`).
