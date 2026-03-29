#!/usr/bin/env python3
"""Compute the next semantic version for a plugin based on existing git tags."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Match tags like: python-dev@v1.0.0
TAG_PATTERN = re.compile(r"^([a-z-]+)@v(\d+)\.(\d+)\.(\d+)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute next semantic version for a plugin")
    parser.add_argument("--plugin", required=True, choices=["rdi", "python-dev"], help="Plugin name")
    parser.add_argument("--bump", required=True, choices=["patch", "minor", "major"], help="Version bump type")
    parser.add_argument("--github-output", help="Path to GitHub Actions output file")
    return parser.parse_args()


def list_tags() -> list[str]:
    """Get all git tags."""
    output = subprocess.check_output(["git", "tag", "--list"], cwd=ROOT, text=True)
    return [line.strip() for line in output.splitlines() if line.strip()]


def latest_version_for_plugin(plugin: str, tags: list[str]) -> tuple[int, int, int]:
    """Find the highest semantic version for a given plugin."""
    versions: list[tuple[int, int, int]] = []
    for tag in tags:
        match = TAG_PATTERN.match(tag)
        if match:
            tag_plugin, major, minor, patch = match.groups()
            if tag_plugin == plugin:
                versions.append((int(major), int(minor), int(patch)))
    if not versions:
        # Default to v0.0.0 if no versions exist
        return (0, 0, 0)
    return max(versions)


def bump_version(version: tuple[int, int, int], bump: str) -> tuple[int, int, int]:
    """Bump the version according to semver rules."""
    major, minor, patch = version
    if bump == "major":
        return (major + 1, 0, 0)
    if bump == "minor":
        return (major, minor + 1, 0)
    # patch
    return (major, minor, patch + 1)


def render_tags(plugin: str, version: tuple[int, int, int]) -> tuple[str, list[str]]:
    """Render canonical tag and alias tags for a version."""
    major, minor, patch = version
    canonical = f"{plugin}@v{major}.{minor}.{patch}"
    aliases = [
        f"{plugin}@v{major}.{minor}",
        f"{plugin}@v{major}",
        f"{plugin}@latest",
    ]
    return canonical, aliases


def render_semver(version: tuple[int, int, int]) -> str:
    """Render version as semver string without 'v' prefix."""
    major, minor, patch = version
    return f"{major}.{minor}.{patch}"


def main() -> None:
    args = parse_args()

    # Get all tags and compute next version
    tags = list_tags()
    current_version = latest_version_for_plugin(args.plugin, tags)
    next_version = bump_version(current_version, args.bump)
    canonical_tag, alias_tags = render_tags(args.plugin, next_version)
    new_semver = render_semver(next_version)

    # Output for GitHub Actions
    if args.github_output:
        output_path = Path(args.github_output)
        with output_path.open("a") as fh:
            fh.write(f"canonical_tag={canonical_tag}\n")
            fh.write(f"alias_tags={','.join(alias_tags)}\n")
            fh.write(f"new_version={new_semver}\n")

    # Print for user visibility
    print(f"Plugin: {args.plugin}")
    print(f"Current version: {render_semver(current_version)}")
    print(f"New version: {new_semver}")
    print(f"Canonical tag: {canonical_tag}")
    print(f"Alias tags: {', '.join(alias_tags)}")


if __name__ == "__main__":
    main()
