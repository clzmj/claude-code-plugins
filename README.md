# Personal agent tooling has moved

The Python tooling skill, hooks, and Rex runtime now live in [clzmj/agent-tooling](https://github.com/clzmj/agent-tooling).

```sh
bunx skills add clzmj/agent-tooling --skill python-tooling -g -a codex claude-code -y
```

The old RDI, API design, and Chezmoi plugins are retired. The separate uv, Ruff LSP, and ty LSP skills have been consolidated into `python-tooling`. Existing history and tags remain available; this repository is no longer an install source. See the new repository for hook setup.
