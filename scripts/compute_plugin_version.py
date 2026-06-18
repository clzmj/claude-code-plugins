#!/usr/bin/env python3
"""Compute the next date-based version for a plugin (Stripe-style date versioning).

A plugin's version IS its release date (``YYYY-MM-DD``). If the plugin is already
released on the same day, a ``.N`` counter is appended so the version string still
changes (Claude Code uses the version string as the update cache key).
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

# Match tags like: ruff-lsp@2026-06-17  or  ruff-lsp@2026-06-17.2
TAG_PATTERN = re.compile(r"^([a-z-]+)@(\d{4}-\d{2}-\d{2})(?:\.(\d+))?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def discover_plugins() -> list[str]:
    """Every plugin directory under plugins/ with a manifest — no hardcoded list."""
    return sorted(p.parent.parent.name for p in ROOT.glob("plugins/*/.claude-plugin/plugin.json"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute next date-based version for a plugin")
    parser.add_argument("--plugin", required=True, help="Plugin name (directory under plugins/)")
    parser.add_argument(
        "--date",
        help="Release date YYYY-MM-DD (default: today, UTC on CI runners)",
    )
    parser.add_argument("--github-output", help="Path to GitHub Actions output file")
    return parser.parse_args()


def list_tags() -> list[str]:
    """Get all git tags."""
    output = subprocess.check_output(["git", "tag", "--list"], cwd=ROOT, text=True)
    return [line.strip() for line in output.splitlines() if line.strip()]


def next_version(plugin: str, day: str, tags: list[str]) -> str:
    """Return the version string for ``day``, adding ``.N`` if that date is taken."""
    counters: list[int] = []
    for tag in tags:
        match = TAG_PATTERN.match(tag)
        if match and match.group(1) == plugin and match.group(2) == day:
            counters.append(int(match.group(3) or 0))
    if not counters:
        return day
    return f"{day}.{max(counters) + 1}"


def render_tags(plugin: str, version: str) -> tuple[str, list[str]]:
    """Render canonical tag and the single floating alias for a date version."""
    canonical = f"{plugin}@{version}"
    aliases = [f"{plugin}@latest"]
    return canonical, aliases


def main() -> None:
    args = parse_args()

    known = discover_plugins()
    if args.plugin not in known:
        raise SystemExit(f"unknown plugin '{args.plugin}'. Known plugins: {', '.join(known)}")

    day = args.date or date.today().isoformat()
    if not DATE_RE.match(day):
        raise SystemExit(f"--date must be YYYY-MM-DD, got: {day}")
    try:
        datetime.strptime(day, "%Y-%m-%d")  # reject impossible dates (e.g. 2026-13-40)
    except ValueError as exc:
        raise SystemExit(f"--date is not a real date: {day} ({exc})")

    tags = list_tags()
    version = next_version(args.plugin, day, tags)
    canonical_tag, alias_tags = render_tags(args.plugin, version)

    if args.github_output:
        with Path(args.github_output).open("a") as fh:
            fh.write(f"canonical_tag={canonical_tag}\n")
            fh.write(f"alias_tags={','.join(alias_tags)}\n")
            fh.write(f"new_version={version}\n")

    print(f"Plugin: {args.plugin}")
    print(f"New version: {version}")
    print(f"Canonical tag: {canonical_tag}")
    print(f"Alias tags: {', '.join(alias_tags)}")


if __name__ == "__main__":
    main()
