#!/usr/bin/env python3
"""Validate repository-policy files and relative Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "NOTICE",
    "CHANGELOG.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "GOVERNANCE.md",
    "MAINTAINERS.md",
    "CODE_OF_CONDUCT.md",
    "RELEASING.md",
    "WRITING.md",
    "CLAUDE.md",
    "docs/project/PROJECT_CHARTER.md",
    "docs/spec/TECHNICAL_SPECIFICATION.md",
    "docs/spec/BENCHMARK.md",
    "docs/architecture/REFERENCE_ARCHITECTURE.md",
    "docs/security/THREAT_MODEL.md",
    "docs/adr/README.md",
    "docs/adr/TEMPLATE.md",
    "docs/adr/0001-apache-2.0-license.md",
    "docs/adr/0002-python-benchmark-harness.md",
    "docs/rfc/README.md",
    "docs/rfc/TEMPLATE.md",
    "packages/benchmark/README.md",
    "packages/benchmark/pyproject.toml",
    "packages/benchmark/fixtures/v0.1/contract.json",
    "packages/benchmark/fixtures/v0.1/provider-retrieval.json",
    "packages/benchmark/schemas/suite.schema.json",
    "packages/benchmark/schemas/result.schema.json",
    "docs/implementation/STATUS.md",
    "docs/implementation/DECISIONS_NEEDED.md",
    "docs/implementation/claude-code/README.md",
    "docs/implementation/claude-code/PROMPTING_RESEARCH.md",
    "docs/implementation/claude-code/00-master-orchestrator.md",
    "docs/implementation/claude-code/01-architecture-decisions-and-contracts.md",
    "docs/implementation/claude-code/02-runtime-foundation.md",
    "docs/implementation/claude-code/03-identity-authorization-and-scopes.md",
    "docs/implementation/claude-code/04-memory-provider-and-hindsight.md",
    "docs/implementation/claude-code/05-okf-and-git-knowledge-plane.md",
    "docs/implementation/claude-code/06-retrieval-context-api-and-mcp.md",
    "docs/implementation/claude-code/07-promotion-and-governance.md",
    "docs/implementation/claude-code/08-admin-ui-and-obsidian.md",
    "docs/implementation/claude-code/09-deployment-bootstrap-and-local-ai.md",
    "docs/implementation/claude-code/10-security-privacy-and-operations.md",
    "docs/implementation/claude-code/11-evaluation-performance-and-interoperability.md",
    "docs/implementation/claude-code/12-release-readiness-and-public-docs.md",
    "docs/implementation/claude-code/13-final-acceptance.md",
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
ACTION_REF = re.compile(r"^\s*uses:\s*([^\s@]+)@([^\s#]+)", re.MULTILINE)
IMMUTABLE_SHA = re.compile(r"^[0-9a-f]{40}$")


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
    )


def check_required(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def check_text_files(errors: list[str]) -> None:
    extensions = {".json", ".md", ".py", ".sh", ".toml", ".yaml", ".yml"}
    named = {"NOTICE", ".editorconfig", ".gitattributes", ".gitignore"}

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in extensions and path.name not in named:
            continue

        raw = path.read_bytes()
        relative = path.relative_to(ROOT)

        if b"\r\n" in raw:
            errors.append(f"CRLF line endings: {relative}")
        if raw and not raw.endswith(b"\n"):
            errors.append(f"missing final newline: {relative}")

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"not UTF-8: {relative}")
            continue

        for number, line in enumerate(text.splitlines(), start=1):
            if line.endswith((" ", "\t")):
                errors.append(f"trailing whitespace: {relative}:{number}")


def check_markdown_links(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]

            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(("#", "//")):
                continue

            clean_path = unquote(parsed.path)
            if not clean_path:
                continue

            resolved = (path.parent / clean_path).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"relative link escapes repository: {path.relative_to(ROOT)} -> {target}"
                )
                continue

            if not resolved.exists():
                errors.append(
                    f"broken relative link: {path.relative_to(ROOT)} -> {target}"
                )


def check_action_pins(errors: list[str]) -> None:
    workflow_dir = ROOT / ".github" / "workflows"
    for path in sorted(workflow_dir.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        for action, ref in ACTION_REF.findall(text):
            if action.startswith("./"):
                continue
            if not IMMUTABLE_SHA.fullmatch(ref):
                errors.append(
                    f"GitHub Action is not pinned to a full commit SHA: "
                    f"{path.relative_to(ROOT)} -> {action}@{ref}"
                )


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_text_files(errors)
    check_markdown_links(errors)
    check_action_pins(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"\nRepository policy checks failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Repository policy checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
