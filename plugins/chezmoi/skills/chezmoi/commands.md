# chezmoi command reference

Verified against chezmoi v2.70. Global flags below apply to (almost) every command.

## Global flags (selected)

| Flag | Short | Meaning |
|---|---|---|
| `--source path` | `-S` | source directory (default `~/.local/share/chezmoi`) |
| `--destination path` | `-D` | destination dir (default `$HOME`) |
| `--config path` | `-c` | config file path |
| `--dry-run` | `-n` | make no changes (preview) |
| `--verbose` | `-v` | show diffs / details |
| `--force` | | apply without prompting |
| `--interactive` | | prompt before every change |
| `--keep-going` | `-k` | continue past errors |
| `--exclude types` | `-x` | exclude entry types (`scripts`, `encrypted`, `files`, `dirs`, `symlinks`, `externals`, …) |
| `--include types` | `-i` | restrict to entry types |
| `--refresh-externals[=always\|auto\|never]` | `-R` | refresh `.chezmoiexternal` cache |
| `--source-path` | | interpret target args as **source** paths |
| `--no-tty` | | read prompt responses from stdin |

`--dry-run --verbose` is the universal "what would happen" preview.

## init — clone/create source, generate config, optionally apply

```bash
chezmoi init                          # new source dir + git repo
chezmoi init user                     # guess URL → https://user@github.com/user/dotfiles.git
chezmoi init user --apply             # clone + apply
chezmoi init user --apply --purge     # bootstrap, then remove source+config dirs
chezmoi init git@github.com:org/dots.git
chezmoi init codeberg.org/user        # site/user form (gitlab.com/user, etc.)
```

Order: (1) clone or `git init` the source dir → (2) if `.chezmoi.$FORMAT.tmpl` exists, render config → (3) if `--apply`, apply → (4) if `--purge`, remove source/config/cache → (5) if `--purge-binary`, remove the binary.

Repo-URL guessing (`-g`, default on; `--guess-repo-url=false` to pass a full URL):

| Arg | HTTPS | SSH (`--ssh`) |
|---|---|---|
| `user` | `https://user@github.com/user/dotfiles.git` | `git@github.com:user/dotfiles.git` |
| `user/repo` | `https://user@github.com/user/repo.git` | `git@github.com:user/repo.git` |
| `site/user/repo` | `https://user@site/user/repo.git` | `git@site:user/repo.git` |
| `sr.ht/~user` | `https://user@git.sr.ht/~user/dotfiles` | `git@git.sr.ht:~user/dotfiles.git` |

Key flags: `-a/--apply`, `--branch`, `-d/--depth 1` (shallow), `--ssh`, `-p/--purge`, `-P/--purge-binary`, `--one-shot` (= `--apply --depth=1 --force --purge --purge-binary`, install-and-leave-nothing), `-C/--config-path`, `--recurse-submodules` (default true), `--git-lfs`. Prompt control: `--prompt`, `--promptDefaults`, `--promptString/Bool/Int/Choice/Multichoice key=value`.

## apply — make destination match target state

```bash
chezmoi apply                          # everything
chezmoi apply --dry-run --verbose      # preview, change nothing
chezmoi apply ~/.bashrc                # one target
chezmoi apply --init                   # regenerate config from template first, then apply
chezmoi apply --exclude=scripts        # skip run_ scripts
```

`--init` (regen+reload config before computing target), `-r/--recursive` (default true), `--source-path` (args are source paths), `-P/--parent-dirs`.

## add — copy destination files into source state

```bash
chezmoi add ~/.bashrc
chezmoi add --template ~/.gitconfig          # → .tmpl
chezmoi add --autotemplate ~/.gitconfig      # auto-replace known [data] values with {{ .var }}
chezmoi add --encrypt ~/.ssh/id_rsa          # encrypted_ + encrypt contents
chezmoi add --exact --recursive ~/.config/nvim
```

| Flag | Short | Effect |
|---|---|---|
| `--template` | `-T` | mark as template |
| `--autotemplate` | `-a` | template + auto-substitute `[data]` values (implies `-T`) |
| `--encrypt` | | encrypt contents (`add.encrypt` config) |
| `--exact` | | `exact_` on dirs (strays deleted on apply) |
| `--create` | | `create_` (created if absent, never overwritten) |
| `--follow` | | add a symlink's target contents, not the link |
| `--template-symlinks` | | rewrite abs symlink paths for portability |
| `--secrets ignore\|warning\|error` | | action on detected secret (default warning) |
| `--force` | `-f` | overwrite existing source (incl. templates) |
| `-r/--recursive` | | default true |

**Gotcha:** `--exact --recursive` can delete sibling files not in source. Seed a `.keep` first: `touch ~/.config/.keep && chezmoi add ~/.config/.keep`. `add` **replaces** existing source state for a target.

## re-add — update source from modified destination files (keep attributes)

```bash
chezmoi re-add                  # all modified managed files
chezmoi re-add ~/.bashrc
chezmoi re-add --re-encrypt     # decrypt+re-encrypt (after recipient change)
```

Only updates files **already in source state**; never adds new files, never touches dirs/symlinks/scripts; **does not regenerate templates** (leaves them alone). For an unconditional overwrite incl. templates use `chezmoi add --force`.

## edit — edit the source state in your editor

```bash
chezmoi edit ~/.bashrc
chezmoi edit --apply ~/.bashrc     # apply on editor exit
chezmoi edit --watch ~/.bashrc     # apply on every save
```

Editor: `edit.command`/`edit.args` config → `$VISUAL` → `$EDITOR`. Encrypted files are decrypted to a private temp dir, edited as cleartext, re-encrypted on exit. Templates keep their `.tmpl` extension for highlighting.

## Inspection & status

```bash
chezmoi diff [target]              # pending changes as a diff
chezmoi status                     # terse: col1=source change, col2=apply change (A/M/D/R)
chezmoi verify                     # exit non-zero if destination ≠ target (no changes)
chezmoi managed [--include encrypted] [--path-style absolute]
chezmoi unmanaged                  # home files chezmoi does not manage
chezmoi cat ~/.bashrc              # computed target contents
chezmoi data                       # all template data (built-ins + your data)
chezmoi execute-template '{{ … }}' # render a template ad hoc
chezmoi source-path ~/.bashrc      # target → source path
chezmoi target-path <srcpath>      # source → target path
chezmoi doctor                     # diagnose the install/config
```

## Lifecycle / management

```bash
chezmoi update                     # git pull --autostash --rebase + apply
chezmoi update --init              # also re-run the config template
chezmoi forget ~/.x                # stop managing; KEEP file in ~
chezmoi remove ~/.x                # delete from source AND ~  (alias: rm)
chezmoi destroy ~/.x               # permanently delete from ~ and source — irreversible, prompts
chezmoi merge ~/.x                 # 3-way merge when source & destination diverged
chezmoi merge-all                  # merge every modified file
chezmoi chattr +template,+encrypted ~/.x   # toggle attributes by renaming source
chezmoi cd                         # subshell in source dir (does NOT change parent shell cwd)
chezmoi git -- status              # run git in the source dir
chezmoi edit-config                # edit ~/.config/chezmoi/chezmoi.toml
chezmoi edit-config-template       # edit .chezmoi.$FORMAT.tmpl
```

## Encryption helpers

```bash
chezmoi age-keygen --output=~/.config/chezmoi/key.txt   # generate age identity
chezmoi encrypt < plain > out.age      # manual encrypt (configured method)
chezmoi decrypt < out.age > plain      # manual decrypt
chezmoi edit-encrypted ~/.secret       # edit an encrypted target
chezmoi age encrypt/decrypt …          # interact with age directly
```

## Persistent state (script run-history etc.)

```bash
chezmoi state data                                    # dump persistent state
chezmoi state delete-bucket --bucket=scriptState      # forget run_once_ history (force rerun)
chezmoi state delete-bucket --bucket=entryState       # forget run_onchange_ history
chezmoi state reset                                   # wipe all persistent state
```

## Bootstrap / migration

```bash
chezmoi import --strip-components 1 --destination ~/.oh-my-zsh archive.tar.gz   # bulk import
chezmoi archive --output=dotfiles.tar.gz       # tar of the target state
chezmoi dump                                    # JSON dump of target state
chezmoi purge                                   # remove chezmoi config + data dirs
chezmoi upgrade                                 # self-update the binary
chezmoi completion zsh > …                      # shell completion
chezmoi ssh host / chezmoi docker image         # run your dotfiles on a remote/container
```
