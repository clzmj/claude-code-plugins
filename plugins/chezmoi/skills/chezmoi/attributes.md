# chezmoi source-state attributes, scripts & special files

Verified against chezmoi v2.70.

## Filename attribute prefixes

State is encoded in source **filenames**. `chezmoi add` flags set most; toggle manually with `chezmoi chattr +attr,-attr <target>`.

| Attr | Target effect |
|---|---|
| `dot_` | leading `.` (`dot_bashrc` → `.bashrc`) |
| `private_` | strip group/world perms (0600/0700) |
| `readonly_` | remove write bits |
| `executable_` | add execute bit |
| `empty_` | keep a zero-length file (empties removed otherwise) |
| `exact_` (dirs) | remove any dir entry not in source (no merge) |
| `encrypted_` | content stored encrypted (suffix `.age`/`.asc`) |
| `symlink_` | target is a symlink; file content = link target |
| `create_` | create only if missing; never overwrite afterward (perms still enforced) |
| `modify_` | source is a script; its stdout becomes new content (current content on stdin) |
| `remove_` | remove the target |
| `external_` | treat children literally — for git submodules / checked-in dirs |
| `literal_` | stop attribute parsing (also `.literal` suffix) |

**Order (must appear in this sequence):** `remove_`→`external_`→`exact_`→`private_`→`readonly_`→`empty_`→`executable_`→`encrypted_`→`create_`/`modify_`/`run_`/`symlink_`→(`once_`|`onchange_`)→(`before_`|`after_`)→`dot_`.

**Suffixes:** `.tmpl` → render as a Go template; the encryption backend suffix (`.age`/`.asc`) is appended **last, after `.tmpl`**. Both are stripped from the target name.

### Examples

```
private_dot_ssh/private_config              → ~/.ssh/config           0600 in 0700
encrypted_private_dot_netrc.tmpl.age        → ~/.netrc                decrypted + templated + 0600
exact_dot_config/exact_nvim/                → ~/.config/nvim          strays deleted
symlink_dot_vimrc                           → ~/.vimrc -> (file contents = link target)
create_dot_npmrc                            → ~/.npmrc                created once, never overwritten
run_onchange_before_packages.sh.tmpl        → templated script, runs before files, on content change
```

## File-type recipes

```bash
chezmoi add ~/.f                       # plain
chezmoi add --template ~/.f            # template (.tmpl)
chezmoi add --encrypt ~/.f            # encrypted_
chmod 600 ~/.f; chezmoi add ~/.f       # private_ (perms inferred), or: chezmoi chattr +private ~/.f
chezmoi chattr +executable ~/.f        # executable bit (no chmod needed — chezmoi sets it)
```

- **Symlink:** source `symlink_<name>` whose contents are the link target (supports `.tmpl`; empty rendered content removes the link).
- **Empty dir:** `chezmoi add` an empty dir auto-creates a `.keep`; or `mkdir -p $(chezmoi source-path)/dir` + a `.keep`.
- **`modify_` script:** named `modify_<name>` (NO `.tmpl`), receives current target on **stdin**, writes new content to **stdout** (empty stdin if target absent). Modify-template mode: add comment `{{- /* chezmoi:modify-template */ -}}`; chezmoi strips it and runs the rest as a template with current contents in `.chezmoi.stdin`, e.g. `{{- .chezmoi.stdin | replaceAllRegex "old" "new" }}`. A modify-template must **not** carry a `.tmpl` extension.

## Scripts (`run_`)

| Prefix | Behavior |
|---|---|
| `run_` | runs on every `apply` |
| `run_once_` | runs once per unique **content hash**, ever (even under a different filename) — state in `scriptState` |
| `run_onchange_` | runs whenever rendered content differs from last success for that filename — state in `entryState` |
| `…_before_` / `…_after_` | run before / after the destination is updated |

- **Execution order: alphabetical by filename**, within each before/after phase. Common idiom: numeric prefixes (`run_once_before_00-…`).
- Must start with a `#!` shebang (or be a binary). Windows interpreters chosen by extension via `[interpreters]`.
- Hashing is **post-templating**. A script that renders to only whitespace **does not run** (lets you no-op per-OS).
- Scripts are **never installed** to the target — they only execute. **`--dry-run` does not run them.** Make them idempotent.
- `.chezmoiscripts/` at the source root: scripts there run without creating a target dir.
- Extra env: `[scriptEnv]` in config; chezmoi sets `CHEZMOI=1`, `CHEZMOI_OS`, `CHEZMOI_ARCH`, plus template data.
- Force rerun: `chezmoi state delete-bucket --bucket=scriptState` (once) / `--bucket=entryState` (onchange).

### Per-OS templated script

```bash
# run_onchange_install-ripgrep.sh.tmpl
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/sh
brew install ripgrep
{{ else if eq .chezmoi.os "linux" -}}
#!/bin/sh
sudo apt-get install -y ripgrep
{{ end -}}
```

### Re-run when an external file changes

`run_onchange_` only tracks its own rendered content — embed a hash of the watched file in a comment:

```bash
#!/bin/bash
# dconf.ini hash: {{ include "dconf.ini" | sha256sum }}
dconf load / < {{ joinPath .chezmoi.sourceDir "dconf.ini" | quote }}
```

### Declarative package install (data + onchange)

`.chezmoidata/packages.yaml`:
```yaml
packages:
  darwin:
    brews: ['git', 'ripgrep']
    casks: ['google-chrome']
```
`run_onchange_darwin-install-packages.sh.tmpl` — the rendered list is in the body, so editing the data re-runs the script:
```bash
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/bash
brew bundle --file=/dev/stdin <<EOF
{{ range .packages.darwin.brews -}}
brew {{ . | quote }}
{{ end -}}
{{ range .packages.darwin.casks -}}
cask {{ . | quote }}
{{ end -}}
EOF
{{ end -}}
```

## Special files & directories

| Name | Purpose |
|---|---|
| `.chezmoi.<fmt>.tmpl` | config template → generates `~/.config/chezmoi/chezmoi.<fmt>` on init |
| `.chezmoiignore` | templated; patterns of **targets** to exclude (per-machine) |
| `.chezmoiremove` | templated; patterns of **targets** to delete on apply |
| `.chezmoiroot` | relocate the source root to a subdir |
| `.chezmoiversion` | minimum chezmoi version (semver); refuses older |
| `.chezmoidata.<fmt>` / `.chezmoidata/` | static template data |
| `.chezmoitemplates/` | named partial templates |
| `.chezmoiscripts/` | scripts that run without creating a target dir |
| `.chezmoiexternal.<fmt>` / `.chezmoiexternals/` | pull in files/archives/git repos (see architecture.md) |

### `.chezmoiignore` (excludes win — NOT gitignore semantics)

Always templated. Patterns use `doublestar.Match` against the **target path**. `!`-negations re-include, but **all excludes take priority over all includes** (not last-match-wins). A source-subdir `.chezmoiignore` applies only to that subdir.

```
README.md
*/*.txt
backups/**              # ignore contents, keep folder
{{- if ne .email "me@work.com" }}
.work-only-config
{{- end }}
{{- if not .trusted }}
.ssh/**                 # never write secrets to untrusted machines
{{- end }}
```

Core private-file pattern: keep private files in the repo, ignore them on machines where a data condition (e.g. `.trusted`, `.work`, `.chezmoi.hostname`) is false → they never land there.

### `.chezmoiremove`

Templated patterns of targets to delete on `apply`. `!`-negations and anything in `.chezmoiignore` are never removed. Always preview: `chezmoi apply --dry-run --verbose`.

### `.chezmoiroot`

A file at the repo root containing a relative path (e.g. `home`). Source state is then read from that subdir — lets the repo keep CI/README/scripts at top level with dotfiles under `home/`. **Gotcha:** all source-root special files (`.chezmoi.toml.tmpl`, `.chezmoiexternal.*`, …) must move into the rooted subdir.
