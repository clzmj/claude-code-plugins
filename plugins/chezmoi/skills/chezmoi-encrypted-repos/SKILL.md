---
name: chezmoi-encrypted-repos
description: Design a chezmoi dotfiles architecture spanning multiple public and private repos split by responsibility, where private content is always pushed ENCRYPTED and the decryption key is kept elsewhere (outside the repo), bootstrapped by an interactive prompt-driven init. Use when the user wants to ARCHITECT or restructure their dotfiles — choosing repo topology, what goes public vs private, how secrets stay encrypted at rest with the key off-repo, and how `chezmoi init` provisions a new machine. For day-to-day chezmoi mechanics use the chezmoi skill; this skill references its commands.md / encryption.md / architecture.md / templating.md.
---

# chezmoi: encrypted multi-repo architecture

Design guide for a dotfiles setup that is **safe to make public**, splits content **by responsibility** across repos, keeps **private content encrypted at rest with the key off-repo**, and **provisions new machines through a prompt-driven `chezmoi init`**.

Mechanics live in the `chezmoi` skill's reference files — `encryption.md`, `architecture.md`, `templating.md`, `attributes.md`, `commands.md`. This skill is about *which* topology to choose and *how the pieces fit*.

## Three load-bearing facts

1. **chezmoi encrypts per file, not per repo.** Mark files `encrypted_` (via `chezmoi add --encrypt`); their ciphertext is committed, everything else is plaintext. There is no "encrypt the whole repo" switch — you encrypt each secret. → `encryption.md`.
2. **The decryption key never lives in the repo.** The age `identity` (private key) sits at a path *outside* the source dir (e.g. `~/.config/chezmoi/key.txt`); only the public `recipient` is committed. This is what makes a repo publishable.
3. **The config holds per-machine state and is not committed.** `~/.config/chezmoi/chezmoi.toml` is generated on `init` from `.chezmoi.toml.tmpl` and carries the prompt answers (`.work`, `.trusted`, …) that gate everything else.

## Choosing a topology

Two ways to split by responsibility. Pick per the decision below.

```
Do the responsibilities have DIFFERENT trust/visibility (public vs private),
and should ALL of them apply together on a given machine?
├── YES → ONE public main repo + PRIVATE repos pulled in as .chezmoiexternal git-repo entries,
│         gated on machine identity. Single `chezmoi apply` composes them.  → Pattern A
└── Mostly SEPARATE contexts you switch between (personal box vs work box),
    rarely both at once?
    └── SEPARATE source dirs, one repo each, selected with --source / sourceDir.  → Pattern B
```

You can combine them: a public base (Pattern A) on every machine, plus a work-only source dir (Pattern B) on work machines.

### Pattern A — one public repo composing private externals (recommended default)

```
github.com/you/dotfiles            (PUBLIC)
  .chezmoi.toml.tmpl               → init questionnaire (name, email, work?, trusted?)
  dot_zshrc.tmpl                   → public config, templated per machine
  encrypted_private_dot_*.age      → secrets, ciphertext, decrypt key is off-repo
  .chezmoiignore                   → hides private targets on untrusted machines
  .chezmoiexternal.toml            → templated; pulls private repos when entitled

github.com/you/dotfiles-private    (PRIVATE, SSH-only)   ← referenced, never embedded
github.com/you-org/work-dotfiles   (PRIVATE, SSH-only)   ← gated on .work
```

`.chezmoiexternal.toml` (templated — emit the entry only when the machine is entitled):

```toml
{{ if .trusted }}
[".config/private"]
    type = "git-repo"
    url = "git@github.com:you/dotfiles-private.git"
    refreshPeriod = "168h"
    pull.args = ["--ff-only"]
{{ end }}
{{ if .work }}
[".config/work"]
    type = "git-repo"
    url = "git@github.com-org:you-org/work-dotfiles.git"
    refreshPeriod = "168h"
{{ end }}
```

On a new machine, one `chezmoi init --apply you/dotfiles` clones the public repo, asks the questionnaire, and pulls only the private repos that machine is entitled to. The public repo contains **only the reference** to the private repos plus encrypted blobs — never a key, never plaintext secrets. → `architecture.md`.

**Two encryption choices for the private material:**
- **Encrypted-in-public** — keep secrets as `encrypted_*.age` in the *public* repo. Simplest; everything is one clone. Use when secrets are small/few.
- **Private external repo** — keep secrets in a separate private repo pulled via `git-repo` external (optionally *also* encrypted inside it). Use when the private set is large, or you want a hard repo boundary, or different people get different access.

Most setups use encrypted-in-public for a handful of secrets and a private external for bulky/segregated material.

### Pattern B — separate source dirs by context

```bash
chezmoi init --source ~/.local/share/chezmoi      git@github.com:you/dotfiles.git
chezmoi init --source ~/.local/share/chezmoi-work git@github.com:org/work-dotfiles.git
# select per command, or set sourceDir in a per-context config
chezmoi --source ~/.local/share/chezmoi-work apply
```

Each repo is independent (own encryption config, own questionnaire). No automatic merge — you choose which one applies. Good for cleanly air-gapped work/personal. → `architecture.md`.

## Encryption strategy: keeping the key elsewhere

The key must be present on the machine but never in the repo. Pick how it gets there:

| Key delivery | How | When |
|---|---|---|
| **Manual** | user copies `key.txt` to `~/.config/chezmoi/` before `init` | simplest; few machines |
| **Passphrase-protected key in repo** | commit `key.txt.age`; a `run_once_before_` script decrypts it to `~/.config/chezmoi/key.txt` after prompting for the passphrase once on init | one secret to remember; nothing plaintext committed |
| **Password manager** | `key.txt` (or the secrets themselves) resolved from 1Password/pass/keyring at apply-time | already using a PM; bootstrap the PM CLI via a `read-source-state.pre` hook |

The passphrase-protected-key flow (full steps in `encryption.md`) is the sweet spot for "everything pushed encrypted, key kept elsewhere, single passphrase bootstraps a new machine":

```bash
chezmoi age-keygen | chezmoi age encrypt --passphrase --output=key.txt.age   # commit this
# run_once_before_00-decrypt-key.sh.tmpl  → decrypts key.txt.age to ~/.config/chezmoi/key.txt
```

```toml
# chezmoi.toml (top-level, before any [section])
encryption = "age"
[age]
    identity  = "~/.config/chezmoi/key.txt"   # off-repo
    recipient = "age1…"                       # public, committed
```

**Multiple machines / people:** add each machine's public key under `[age].recipients` so any can decrypt; re-encrypt existing files after adding one (`chezmoi re-add --re-encrypt`). → `encryption.md`.

## The prompt-driven bootstrap (`.chezmoi.toml.tmpl`)

The questionnaire is the spine: its answers persist into `[data]` and gate ignores, externals, and which secrets decrypt. Use `*Once` so re-running `init` never re-asks. → `templating.md`.

```toml
{{- $email   := promptStringOnce . "email"   "Email address" -}}
{{- $work    := promptBoolOnce   . "work"    "Is this a work machine" false -}}
{{- $trusted := promptBoolOnce   . "trusted" "Is this machine trusted/private" false -}}

encryption = "age"
[age]
    identity  = "~/.config/chezmoi/key.txt"
    recipient = "age1…"

[data]
    email   = {{ $email | quote }}
    work    = {{ $work }}
    trusted = {{ $trusted }}
```

Then everything keys off those answers:
- `.chezmoiexternal.toml` → `{{ if .work }}` pulls the work repo (above).
- `.chezmoiignore` → keep private targets off untrusted machines:
  ```
  {{- if not .trusted }}
  .ssh/**
  private/**
  {{- end }}
  ```
- Refuse to configure an untrusted host outright: `{{ if not .trusted }}{{ exit 1 }}{{ end }}`.

New machine, one command: `chezmoi init --apply git@github.com:you/dotfiles.git`. CI/unattended: add `--promptString/Bool …` or `--promptDefaults`. → `commands.md`, `templating.md`.

## Reference architecture (assembled)

```
PUBLIC  github.com/you/dotfiles
├── .chezmoi.toml.tmpl              # questionnaire → email/work/trusted + age config
├── .chezmoiexternal.toml          # gated git-repo externals → private repos
├── .chezmoiignore                 # {{ if not .trusted }} hide private targets {{ end }}
├── key.txt.age                    # passphrase-protected age key (ciphertext only)
├── run_once_before_00-decrypt-key.sh.tmpl   # decrypts key.txt.age → ~/.config/chezmoi/key.txt
├── dot_zshrc.tmpl                 # public, per-machine via templates
├── dot_gitconfig.tmpl             # uses .email
└── encrypted_private_dot_ssh/
    └── encrypted_private_id_ed25519.age      # secret, ciphertext, key off-repo

PRIVATE github.com/you/dotfiles-private       # pulled via external when .trusted
PRIVATE github.com/org/work-dotfiles          # pulled via external when .work
```

Invariants this preserves:
- The public repo is safe to publish: no private keys, no plaintext secrets — only ciphertext and references.
- A machine sees private content **only** if its questionnaire answers (and/or its SSH key) entitle it.
- One `chezmoi init --apply` provisions any machine; one passphrase unlocks the key; `chezmoi update` keeps it current.

## Design checklist

- [ ] Decide topology: Pattern A (compose) vs B (separate dirs) vs both.
- [ ] `encryption = "age"` is at the **top level**, before any `[section]`.
- [ ] The age `identity` path is **outside** the source dir; only the `recipient` is committed.
- [ ] Every secret is `--encrypt`ed (or lives in a private external); nothing plaintext is committed.
- [ ] Key delivery chosen (manual / passphrase-protected-in-repo / password manager).
- [ ] `.chezmoi.toml.tmpl` uses `*Once` prompts and writes answers to `[data]`.
- [ ] `.chezmoiexternal.toml` and `.chezmoiignore` are **gated** on those answers / key presence.
- [ ] Tested on a throwaway machine/container: `chezmoi init --apply <repo>` then `chezmoi doctor`.
- [ ] Multi-machine: all machines' public keys in `[age].recipients`; re-encrypted after adding one.
- [ ] `git.autoPush` off, or every commit verified secret-free (a public repo pushes whatever you add).
