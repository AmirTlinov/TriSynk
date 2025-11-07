#!/usr/bin/env python3
"""Validate docs/issues.md structure and references."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ISSUE_MD = Path("docs/issues.md")
HEADER_RE = re.compile(r"^##\s+(ISS-\d+)\s+\u2013\s+(.+)$", re.MULTILINE)


def extract_sections(text: str):
    matches = list(HEADER_RE.finditer(text))
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        yield match.group(1), text[start:end]


def validate_section(issue_id: str, body: str):
    errors = []
    required_snippets = {
        "scope": "**Scope:**",
        "deliverables": "**Deliverables:**",
        "dependencies": "**Dependencies:**",
    }
    for name, snippet in required_snippets.items():
        if snippet not in body:
            errors.append(f"missing {name} block")
    if ".md#" not in body:
        errors.append("missing documentation anchor link ('.md#')")
    if "issues.md" in body and issue_id in body:
        errors.append("self-referential dependency")
    return errors


def main() -> int:
    text = ISSUE_MD.read_text(encoding="utf-8")
    sections = list(extract_sections(text))
    if not sections:
        print("[validate-issues] No issue sections found", file=sys.stderr)
        return 1
    failures: list[str] = []
    for issue_id, body in sections:
        errs = validate_section(issue_id, body)
        if errs:
            failures.append(f"{issue_id}: {', '.join(errs)}")
    if failures:
        print("[validate-issues] FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("[validate-issues] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
