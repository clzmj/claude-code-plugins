# chezmoi templating & init prompts

Verified against chezmoi v2.70.

## When a file is a template

- Its source name ends in `.tmpl` (suffix stripped from the target name), **or**
- It lives under `.chezmoitemplates/` (named partials).
- All `.chezmoi*` special files (`.chezmoiignore`, `.chezmoiremove`, `.chezmoiexternal.*`) are **always** templated, with or without `.tmpl`.

Text outside `{{ … }}` is copied literally. Go `text/template` syntax.

## Test rendering

```bash
chezmoi execute-template '{{ .chezmoi.hostname }}'
chezmoi execute-template < dot_zshrc.tmpl
cat foo.txt | chezmoi execute-template
# Config template (init context + prompt answers):
chezmoi execute-template --init --promptString "email=me@home.org" \
    < ~/.local/share/chezmoi/.chezmoi.toml.tmpl
```

## Built-in `.chezmoi.*` variables

Dump all with `chezmoi data`. Common ones:

| Variable | Notes |
|---|---|
| `.chezmoi.os` | `darwin`, `linux`, `windows`, … |
| `.chezmoi.arch` | `amd64`, `arm64`, … |
| `.chezmoi.hostname` | hostname up to first `.` |
| `.chezmoi.fqdnHostname` | fully-qualified |
| `.chezmoi.username` | current user |
| `.chezmoi.homeDir` | forward slashes even on Windows |
| `.chezmoi.sourceDir` / `.destDir` / `.cacheDir` | dirs |
| `.chezmoi.config` | parsed config (`.chezmoi.config.age.identity`, …) |
| `.chezmoi.kernel` | **Linux only** (`/proc/sys/kernel`) |
| `.chezmoi.osRelease` | **Linux only** (`/etc/os-release`, e.g. `.id`) |
| `.chezmoi.version.version` / `.commit` / `.date` | build info |

**Gotcha:** guard Linux-only vars: `{{ if eq .chezmoi.os "linux" }}{{ .chezmoi.osRelease.id }}{{ end }}`.

## Control flow

```
{{ if eq .chezmoi.os "darwin" }}…{{ else if eq .chezmoi.os "linux" }}…{{ else }}…{{ end }}
```

- `eq a b…` true if `a` equals any later arg; also `ne`, `and`, `or`, `not`.
- **Parentheses required** when nesting: `{{ if (and (eq .chezmoi.os "linux") .work) }}…{{ end }}`.
- Whitespace trim: `{{-` strips preceding, `-}}` strips following whitespace.
- chezmoi adds [sprig](https://masterminds.github.io/sprig/) functions plus its own (`include`, `joinPath`, `stat`, `lookPath`, `output`, `fromJson`, `fromYaml`, `decrypt`, secret functions, …).

## Data sources (later overrides earlier)

1. Built-in `.chezmoi.*`
2. `.chezmoidata.$FORMAT` files and `.chezmoidata/` dirs — **static** structured data (JSON/JSONC/TOML/YAML), merged at the data **root** in lexical filename order. Cannot be templates. **Dicts merge; lists/scalars are replaced** (last wins).
3. `[data]` section of the config file (per-machine, set by the init questionnaire).

## Reusable partials — `.chezmoitemplates/`

Each file becomes a template named by its path under `.chezmoitemplates/`. **Default data is `nil`** — pass `.` to forward context:

```
{{ template "foo" . }}                       {{/* forward all data */}}
{{ template "alacritty" 12 }}                {{/* single arg as . */}}
{{ template "alacritty" (dict "size" 12) }}  {{/* multiple via dict */}}
```

## The config template — `.chezmoi.<format>.tmpl`

`<format>` ∈ `toml`, `yaml`, `json`, `jsonc`. Lives at the source root. **Runs during `chezmoi init` and any `--init` command** (e.g. `chezmoi update --init`) to generate `~/.config/chezmoi/chezmoi.<format>`.

**Critical:** it runs **before source state is read**, so inside it you have template + init/prompt functions and any existing config data, but **not** `.chezmoidata.*` or `.chezmoitemplates/`. Whatever lands under `[data]` becomes template data (`.email`, …) for all other templates afterward.

## Init / prompt functions

Only available during `init` (and `execute-template --init`). Calling them in a normal template errors. (Docs live under `/reference/templates/init-functions/`.)

```
promptString      PROMPT [DEFAULT]                       -> string
promptStringOnce  MAP PATH PROMPT [DEFAULT]              -> string
promptBool        PROMPT [DEFAULT]                       -> bool
promptBoolOnce    MAP PATH PROMPT [DEFAULT]              -> bool
promptInt         PROMPT [DEFAULT]                       -> int
promptIntOnce     MAP PATH PROMPT [DEFAULT]              -> int
promptChoice      PROMPT CHOICES [DEFAULT]               -> string   (CHOICES = list of strings)
promptChoiceOnce  MAP PATH PROMPT CHOICES [DEFAULT]      -> string
promptMultichoice[Once] …                                -> list
writeToStdout STRINGS…     stdinIsATTY -> bool     exit CODE
```

**`*Once` semantics:** returns `MAP` at `PATH` (typically `.` + a key) if already set and correctly typed, otherwise prompts. So it asks on the first `init` and reuses the stored answer on later inits → idempotent across machines. Force re-ask: `chezmoi init --prompt`.

- `promptString` strips whitespace; empty + default → default.
- `promptBool` truthy: `1,on,t,true,y,yes`; falsy: `0,off,f,false,n,no`.
- `promptChoice` validates the response against `CHOICES` (build with `list "a" "b"`).
- `writeToStdout` prints a message during init; `exit CODE` aborts init; `stdinIsATTY` guards prompts in non-interactive runs.

### Canonical questionnaire (`.chezmoi.toml.tmpl`)

```toml
{{- writeToStdout "Configuring chezmoi for this machine...\n" -}}
{{- $name    := promptStringOnce . "name"    "Full name" -}}
{{- $email   := promptStringOnce . "email"   "Email address" -}}
{{- $work    := promptBoolOnce   . "work"    "Is this a work machine" false -}}
{{- $trusted := promptBoolOnce   . "trusted" "Is this machine trusted/private" false -}}
{{- $host    := promptChoiceOnce . "hosttype" "Host type" (list "desktop" "laptop" "server") "laptop" -}}

[data]
    name     = {{ $name | quote }}
    email    = {{ $email | quote }}
    work     = {{ $work }}
    trusted  = {{ $trusted }}
    hosttype = {{ $host | quote }}
```

Use later as `.name`, `.work`, `.trusted`, `.hosttype` in any template, in `.chezmoiignore`, or to gate `.chezmoiexternal` entries.

**Formatting gotchas:**
- Strings → `| quote`; bools/ints → emit bare (`work = {{ $work }}`).
- Trim markers (`{{- … -}}`) keep prompt lines from injecting blank lines into the rendered config; the **prompt message** still prints to the terminal regardless.
- The `PATH` you pass to a `*Once` fn (`"email"`) **must match** the `[data]` key, or it never finds the stored value and re-prompts every time.

### Non-interactive / CI

```bash
chezmoi init --apply --promptString "Email address=me@x.com,Full name=Me" repo
chezmoi init --apply --promptDefaults repo      # use defaults where available
chezmoi init --apply --no-tty < answers repo    # read responses from stdin
```

`--promptBool/Int/Choice key=value` per type; multichoice uses `key=value1/value2`. Gate interactive prompts with `{{ if stdinIsATTY }}…{{ end }}`.

## Template directives (per-file behavior, written as comments)

Line format `chezmoi:template:KEY=VALUE`; the directive line is removed from output; later overrides earlier.

| Directive | Values |
|---|---|
| `left-delimiter` / `right-delimiter` | e.g. `# chezmoi:template:left-delimiter="# [[" right-delimiter=]]` (avoid `{{` clashes) |
| `line-endings` | `lf` (default), `crlf`, `native` |
| `missing-key` | `error` (default), `invalid` (`<no value>`), `zero` |
| `encoding` | `utf-8` (default), `utf-8-bom`, `utf-16-*` |
| `format-indent` / `format-indent-width` | for `toJson`/`toToml`/`toYaml` output |

```
{{/* chezmoi:template:missing-key=zero */}}
```

## Convert an existing managed file to a template

```bash
chezmoi chattr +template ~/.zshrc      # rename source to add .tmpl
chezmoi edit ~/.zshrc                  # then add {{ … }} actions
```
