# chezmoi source-directory control & external repos

Verified against chezmoi v2.70. How to point chezmoi at different source dirs and compose multiple repos.

## Source directory selection

- Default: `~/.local/share/chezmoi`.
- CLI: `-S` / `--source <dir>`; config equivalent `sourceDir`.
  ```bash
  chezmoi --source ~/.local/share/chezmoi-work apply
  ```
  ```toml
  sourceDir = "~/.local/share/chezmoi-work"
  ```
- Init a second repo into its own dir:
  ```bash
  chezmoi init --source ~/.local/share/chezmoi-work git@github.com:org/work-dotfiles.git
  chezmoi --source ~/.local/share/chezmoi-work apply
  ```
- **`--source-path`** is unrelated: it reinterprets target *args* as source paths. Don't confuse with `--source`.

**"Multiple repos by responsibility":** keep each responsibility (personal / work / machine-class / secrets) in its own git repo cloned to a distinct dir, and select with `--source`/`sourceDir`. There is **no built-in merge of two source dirs into one apply** — to *compose* repos into a single apply, use `.chezmoiexternal` (below), not two `sourceDir`s.

## `workingTree` vs `sourceDir` vs `.chezmoiroot`

- `workingTree` (config) — the git repo root; **defaults to `sourceDir`**. Set it to a **parent** of `sourceDir` so one git repo can hold the chezmoi source under a subpath alongside non-dotfile content.
- `.chezmoiroot` (file at repo root) — names a subdir as the source root (e.g. `home`). Complementary to `workingTree`: `workingTree` = git tree root, `.chezmoiroot` = where source state is read.

## `.chezmoiexternal.<format>` — pull in files/archives/git repos

Filename `.chezmoiexternal.toml`/`.yaml`/`.json` (also `.jsonc`). Can live anywhere in the source state; entries are relative to that dir. **Always interpreted as a template**, even without `.tmpl` — use `{{ .chezmoi.os }}`, `stat`, `gitHubLatestReleaseAssetURL`, etc.

### Types

```toml
# single file
[".vim/autoload/plug.vim"]
    type = "file"
    url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    refreshPeriod = "168h"

# extracted archive
[".oh-my-zsh"]
    type = "archive"
    url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
    exact = true
    stripComponents = 1
    refreshPeriod = "168h"
    include = ["*/*.zsh"]

# one file out of an archive (e.g. a release binary)
[".local/bin/age"]
    type = "archive-file"
    url = "https://github.com/FiloSottile/age/releases/download/v1.1.1/age-v1.1.1-{{ .chezmoi.os }}-{{ .chezmoi.arch }}.tar.gz"
    path = "age/age"
    executable = true

# clone/pull a repo (incl. private)
[".vim/pack/foo/start/plugin"]
    type = "git-repo"
    url = "https://github.com/user/plugin.git"
    refreshPeriod = "168h"
    clone.args = ["--depth", "1"]
    pull.args  = ["--ff-only"]
```

### Common keys

`url`/`urls` (fallback list), `refreshPeriod` (e.g. `"168h"`; `0`=never re-download), `encrypted` (content is chezmoi-encrypted), `private`/`readonly`/`executable`, `exact`, `stripComponents`, `include`/`exclude` (globs; exclude wins), `path` (archive-file), `targetPath` (redirect; multiple entries → one dir), `decompress` (`bzip2`/`gzip`/`xz`/`zstd`), `filter.command`/`filter.args`, `checksum.sha256/384/512`, `checksum.size`.

`.chezmoiexternals/` directory: every file inside is treated as a `.chezmoiexternal.<format>` (flat only — no subdirs).

### Refresh

`refreshPeriod = 0` (default) = never re-fetch. Force: `chezmoi apply -R` (`--refresh-externals=always`); `auto` = only past their period.

## Composing a PUBLIC repo that references PRIVATE repos (the core pattern)

Public repo is your normal source dir. Declare private content as `git-repo` externals over SSH, **conditionally emitted** when the key is present, so machines without the key skip them and no secret lands in the public repo:

```toml
# .chezmoiexternal.toml (templated)
{{ if stat (joinPath .chezmoi.homeDir ".ssh" "id_ed25519") }}
[".config/private-stuff"]
    type = "git-repo"
    url = "git@github.com:org/private-dotfiles.git"
    refreshPeriod = "168h"
    pull.args = ["--ff-only"]
{{ end }}
```

Drive it off the init questionnaire instead of (or with) key-presence:

```toml
{{ if .work }}
[".config/work"]
    type = "git-repo"
    url = "git@github.com:org/work-dotfiles.git"
{{ end }}
```

On a fresh machine `chezmoi apply` clones the externals into place; the public repo only ever contains the *reference* to the private repo.

## git submodules (alternative to externals)

If you commit real submodules, set the **`external_`** attribute on every dir that contains a submodule so chezmoi doesn't parse submodule filenames as attributes. `init`/`update` use `--recurse-submodules` (default true); disable with `--recurse-submodules=false` or `update.recurseSubmodules = false`. Prefer `git-repo` externals when you want refresh-period control and conditional/private gating.

## One-shot import (no external entry)

```bash
curl -sL -o /tmp/a.tar.gz <url>
chezmoi import --strip-components 1 --destination ~/.oh-my-zsh /tmp/a.tar.gz
chezmoi apply
```
