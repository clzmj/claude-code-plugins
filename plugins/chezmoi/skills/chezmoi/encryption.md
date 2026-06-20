# chezmoi encryption & secrets

Verified against chezmoi v2.70. Two distinct ways to keep secrets out of a (possibly public) repo:

1. **Encrypt files at rest** (age/gpg) — ciphertext is committed; the key lives elsewhere.
2. **Resolve secrets at apply-time** from a password manager — only the *reference* is committed.

You can mix both.

---

## age (recommended for at-rest encryption)

chezmoi encrypts **per file** via the `encrypted_` attribute; everything else stays plaintext. To "encrypt everything," `--encrypt` every sensitive file. The **private key never goes in the repo** — only the public recipient does.

### Setup

```bash
chezmoi age-keygen --output=~/.config/chezmoi/key.txt
# => Public key: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
```

`key.txt` MUST live **outside** `~/.local/share/chezmoi` (e.g. `~/.config/chezmoi/key.txt`).

```toml
encryption = "age"          # MUST be top-level, BEFORE any [section] — else silently ignored
[age]
    identity  = "~/.config/chezmoi/key.txt"
    recipient = "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"
```

```bash
chezmoi add --encrypt ~/.ssh/id_rsa     # → encrypted_private_dot_ssh/encrypted_private_id_rsa.age
```

`apply`/`diff`/`status`/`edit` decrypt transparently using `identity`.

### Multiple recipients (several machines / people)

Use plural keys; any listed identity can decrypt files encrypted to the matching recipients.

```toml
[age]
    identities = ["~/.config/chezmoi/key1.txt", "~/.config/chezmoi/key2.txt"]
    recipients = ["age1…A", "age1…B"]
    # or:  recipientsFile = "~/.config/chezmoi/recipients.txt"
```

Adding a recipient is **not retroactive** — re-encrypt existing files (see below).

### Variants & other keys

- Builtin age (used when no `age` binary on `$PATH`) does **not** support passphrases, symmetric, or SSH keys. Install the real `age` binary for those.
- SSH key as identity: `identity = "~/.ssh/id_rsa"`. Symmetric: `symmetric = true`. Passphrase: `passphrase = true` (prompts on every `add`/`apply`/`diff`/`status` — avoid for an always-encrypted repo).
- `command` / `args` (custom binary), `suffix` (default `.age`).

---

## gpg (alternative backend)

```toml
encryption = "gpg"
[gpg]
    recipient = "your-key-id-or-email"     # or recipients = ["id1","id2"]
```

Symmetric (passphrase): `symmetric = true`. gpg writes info to stderr — quiet it with `args = ["--quiet"]`. Non-interactive symmetric: `args = ["--batch","--passphrase","<pw>","--no-symkey-cache"]`. `suffix` default `.asc`.

---

## Manual encrypt/decrypt & template decryption

```bash
chezmoi encrypt < plaintext  > out.age      # or: chezmoi encrypt file
chezmoi decrypt < out.age    > plaintext
chezmoi edit-encrypted ~/.secret            # edit an encrypted target in place
```

Decrypt inside a template (prefix the source file with `.` so it's ignored as a standalone target):

```
{{ joinPath .chezmoi.sourceDir ".ignored-secret.age" | include | decrypt }}
```

---

## Re-encryption / migrating recipients or backend

Adding a recipient or switching backend does **not** re-encrypt existing files. Either:

```bash
chezmoi re-add --re-encrypt              # decrypt + re-encrypt managed encrypted files
```

or the full forget/re-add loop (also migrates gpg→age):

```bash
chezmoi apply                            # ensure plaintext exists on disk
# …edit config to new encryption settings…
for f in $(chezmoi managed --include encrypted --path-style absolute); do
    chezmoi forget "$f"
    chezmoi add --encrypt "${f}"
done
```

---

## Bootstrap pattern: passphrase-protected key in the repo, no plaintext key, no plaintext passphrase in config

Lets a fresh `chezmoi init --apply` prompt for a passphrase **once**, decrypt the real key to a path outside the repo, then decrypt everything else transparently.

1. Create a passphrase-protected age key (ciphertext is safe to commit):
   ```bash
   chezmoi age-keygen | chezmoi age encrypt --passphrase --output=key.txt.age
   ```
2. Add a `run_once_before_decrypt-private-key.sh.tmpl` that decrypts `key.txt.age` → `~/.config/chezmoi/key.txt`.
3. Point the config at that identity + the public recipient:
   ```toml
   encryption = "age"
   [age]
       identity  = "~/.config/chezmoi/key.txt"
       recipient = "age1…"
   ```
4. `chezmoi init --apply <repo>` → prompts once, decrypts the key, applies.

> Avoid `[data] passphrase = "…"` in `.chezmoi.toml.tmpl` — that writes the passphrase **plaintext** into the on-disk config.

---

## Encrypted templates + init prompts (how they combine)

A source file can be **both** encrypted and a template, e.g. `encrypted_private_dot_netrc.tmpl.age` (the backend suffix `.age`/`.asc` is appended **after** `.tmpl`). On `apply` chezmoi **decrypts first, then renders the template** — so the decrypted body is a normal template with full data (`.email`, `.work`, … and `.chezmoi.*`) available. *(Verified in a container against v2.70.)*

**Hard constraint:** `promptString`/`promptBool`/`promptInt`/… are **init-only** functions. They error inside *any* applied template, encrypted or not. You therefore **cannot prompt while applying an encrypted template.** The only valid wiring is:

```
chezmoi init  ──prompt once──▶  config [data]  ──apply──▶  encrypted_*.tmpl reads .value
(.chezmoi.toml.tmpl,            (persisted,                (decrypted, then rendered
 promptStringOnce)               plaintext on disk)         with that data)
```

```toml
# .chezmoi.toml.tmpl — prompt once, persist
{{- $email := promptStringOnce . "email" "Email address" -}}
[data]
    email = {{ $email | quote }}
```
```
# encrypted_private_dot_netrc.tmpl.age — ciphertext in the repo; on apply: decrypt → render
machine api.example.com login {{ .email }} password {{ (onepasswordRead "op://Private/api/pass") }}
```

**Privacy footgun:** a value you `promptStringOnce` into `[data]` lands **plaintext** in `~/.config/chezmoi/chezmoi.toml`. So "prompt for a *secret* at init and bake it into an encrypted template" defeats the encryption — the secret is now plaintext in config. Instead:

- Prompt only for **non-secret selectors** (email, work?, trusted?, hostname class) and let those gate encrypted content.
- For an actual secret, prompt for a **passphrase** that decrypts a key file via the `run_once` bootstrap (above), and keep the secret itself in `encrypted_` files. The passphrase is consumed by the key-decrypt script, not persisted.
- Or resolve the secret at apply-time from a password manager inside the (encrypted or plain) template — the repo holds only the reference.

If you genuinely want the encryption tool itself to prompt **at every apply** (not init), that's `passphrase = true` for age/gpg — the encryption layer prompts for the passphrase on each `apply`/`diff`/`status`. This is independent of template prompt functions.

## `encryption = "transparent"` (git-filter, different mechanism)

Not chezmoi crypto — delegates to a git clean/smudge filter (transcrypt/git-crypt). Init the tool in the source dir, then in source `.gitattributes`:

```
encrypted_* filter=crypt diff=crypt merge=crypt
```

Add files normally (no `--encrypt`); locally `git show`/`diff` show cleartext, only the pushed blob is ciphertext. Use only if you specifically want git-native transparent encryption.

---

## Secrets from a password manager (resolved at apply-time)

Nothing encrypted is stored; the repo holds only the *reference* (`op://…`, pass-name, service/user), resolved per-apply. Authenticate the PM CLI **before** `chezmoi apply` (or rely on its interactive sign-in).

```
# 1Password
password = {{ onepasswordRead "op://Personal/GitHub/token" | quote }}
{{ (onepassword "uuid").fields.password }}        # full item (one cached CLI call)

# pass
token = {{ pass "github/token" | quote }}
{{ (passFields "github").token }}                  # multiple fields from one entry

# system keychain / keyring (macOS Keychain, GNOME Keyring, Windows Cred Manager)
token = {{ keyring "github" .github.user | quote }}
```

Store into keyring from the CLI: `chezmoi secret keyring set --service=github --user=$USER`.

Other backends via `secret`/`secretJSON` and the documented `*Read`/`*Fields`/`*Raw` functions (Bitwarden, Vault, AWS/Azure, Doppler, KeePassXC, …).

### Bootstrap the PM CLI on init (ordering-critical)

Install the PM CLI **after** clone but **before** source state is read, via a `read-source-state.pre` hook (so secret functions resolve later in the same `init --apply`):

```toml
# chezmoi.toml
[hooks.read-source-state.pre]
    command = ".local/share/chezmoi/.install-password-manager.sh"
```

The hook is **not** a template (detect OS with `uname`), runs on essentially every command, so it **must be idempotent** (guard with `type pm-binary >/dev/null 2>&1 && exit`). Lead its filename with `.` so chezmoi ignores it as managed state.

---

## Encryption gotchas

- `encryption = "…"` must precede all `[section]` tables, or it's silently ignored.
- The identity/private key never enters the repo; only the public recipient does.
- Builtin age = no passphrase/symmetric/SSH; install the real `age` binary for those.
- `suffix` must match the backend (`.age` vs `.asc`) or decryption breaks.
- New recipients / backend changes are not retroactive — re-encrypt explicitly.
- With a public repo + `git.autoPush = true`, a plaintext `add` gets pushed — always `--encrypt` or use a PM.
