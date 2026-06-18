# Python CI/CD with uv

## GitHub Actions

### Basic workflow
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
        with:
          enable-cache: true
      - run: uv sync --all-extras --dev
      - run: uv run pytest
      - run: uv run ruff check .
```

### Matrix testing (multiple Python versions)
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
        with:
          enable-cache: true
      - run: uv python install ${{ matrix.python-version }}
      - run: uv sync --frozen
      - run: uv run pytest
```

### With coverage
```yaml
- run: uv run pytest --cov=myproject --cov-report=xml
- uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

### With caching (built-in)
```yaml
- uses: astral-sh/setup-uv@v2
  with:
    enable-cache: true  # Caches uv data + Python installations
```

This automatically caches:
- Downloaded Python versions
- Package cache
- uv binary

### With artifact upload
```yaml
- run: uv build
- uses: actions/upload-artifact@v4
  with:
    name: dist
    path: dist/
```

---

## Docker

### Simple image
```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
CMD ["uv", "run", "python", "app.py"]
```

### Multi-stage build (optimized)
```dockerfile
# Builder stage
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "app.py"]
```

### With development dependencies
```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen  # Includes dev dependencies
COPY . .
CMD ["uv", "run", "pytest"]
```

### Docker Compose
```yaml
version: "3.9"

services:
  app:
    build: .
    environment:
      - DEBUG=true
    volumes:
      - .:/app
    command: uv run uvicorn app:app --reload

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
```

---

## Pre-commit Hooks

### Basic setup
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: uv-lock
        name: uv lock
        entry: uv lock
        language: system
        pass_filenames: false
        always_run: true

      - id: ruff-check
        name: ruff check
        entry: uv run ruff check --fix
        language: system
        types: [python]

      - id: ruff-format
        name: ruff format
        entry: uv run ruff format
        language: system
        types: [python]
```

### Installation
```bash
uv add --dev pre-commit
uv run pre-commit install
```

### Run manually
```bash
uv run pre-commit run --all-files
```

---

## GitLab CI

### Basic pipeline
```yaml
stages:
  - test
  - build

test:
  stage: test
  image: python:3.12
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH=$HOME/.cargo/bin:$PATH
  script:
    - uv sync --frozen --dev
    - uv run pytest
    - uv run ruff check .
  cache:
    paths:
      - .cache/uv

build:
  stage: build
  image: python:3.12
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH=$HOME/.cargo/bin:$PATH
  script:
    - uv sync --frozen
    - uv build
  artifacts:
    paths:
      - dist/
```

---

## Poetry to uv in CI

If migrating from Poetry to uv, update workflows:

**Before (Poetry)**:
```yaml
- run: pip install poetry
- run: poetry install
- run: poetry run pytest
```

**After (uv)**:
```yaml
- uses: astral-sh/setup-uv@v2
- run: uv sync --frozen
- run: uv run pytest
```

---

## Best Practices

1. **Always use `--frozen`** in CI to catch lockfile issues
2. **Cache Python installations** with `setup-uv@v2`
3. **Test multiple versions** with matrix strategy
4. **Use multi-stage Docker** builds for smaller images
5. **Commit `uv.lock`** for reproducible installs
6. **Run linting in CI** before tests
7. **Upload coverage** to track code quality
8. **Use pre-commit hooks** locally for fast feedback
9. **Document Python version** requirements
10. **Test Docker images** before deploying

---

## Common Issues

### "uv: command not found" in CI
```yaml
# Add setup-uv step
- uses: astral-sh/setup-uv@v2
```

### Slow Docker builds
Use multi-stage builds and cache layer:
```dockerfile
# Layer caching: dependencies change less often
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .  # Application code (changes more)
```

### Lockfile conflicts in CI
```bash
# Regenerate in local environment:
uv lock --upgrade
# Then commit uv.lock
```

### Cache invalidation
```yaml
# Force cache refresh on Python version change
- uses: astral-sh/setup-uv@v2
  with:
    enable-cache: true
    cache-key-prefix: python-${{ matrix.python-version }}
```
