#!/usr/bin/env python3
"""Export issue + intent graph for automation."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

ISSUE_MD = Path("docs/issues.md")
INTENT_DIR = Path("intents")
DOC_REF_RE = re.compile(r"([A-Za-z0-9_./-]+\.md#[A-Za-z0-9_./-]+)")
ISSUE_LINK_RE = re.compile(r"ISS-\d+")


def extract_sections(text: str):
    header_re = re.compile(r"^##\s+(ISS-\d+)\s+\u2013\s+(.+)$", re.MULTILINE)
    matches = list(header_re.finditer(text))
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        yield match.group(1), match.group(2).strip(), text[start:end].strip()


def parse_issues() -> list[dict]:
    raw = ISSUE_MD.read_text(encoding="utf-8")
    issues: list[dict] = []
    for issue_id, title, body in extract_sections(raw):
        references = sorted(set(DOC_REF_RE.findall(body)))
        deps = sorted({match for match in ISSUE_LINK_RE.findall(body) if match != issue_id})
        issues.append(
            {
                "id": issue_id,
                "title": title,
                "references": references,
                "dependencies": deps,
                "body": body,
            }
        )
    return issues


def parse_intents() -> list[dict]:
    intents: list[dict] = []
    for path in sorted(INTENT_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        intents.append(
            {
                "file": str(path),
                "meta": data.get("meta", {}),
                "issue": data.get("meta", {}).get("issue"),
                "docs": data.get("meta", {}).get("docs", []),
                "requirements": data.get("requirements", {}),
                "constraints": data.get("constraints", {}),
                "interop": data.get("interop", {}),
            }
        )
    return intents


def export_graph(dest: Path) -> None:
    payload = {
        "issues": parse_issues(),
        "intents": parse_intents(),
        "source": {
            "issues": str(ISSUE_MD),
            "intents": str(INTENT_DIR),
        },
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[export-graph] wrote {dest}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="data/outbox/issues_intents.json")
    args = parser.parse_args()
    export_graph(Path(args.output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
