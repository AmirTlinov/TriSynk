#!/usr/bin/env python3
"""Prototype Rust-to-clmr frontend stub."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FN_RE = re.compile(r"^\s*fn\s+(?P<name>[A-Za-z0-9_]+)")


def parse_functions(text: str):
    return [match.group("name") for match in FN_RE.finditer(text)]


def build_ir(path: Path) -> dict:
    code = path.read_text(encoding="utf-8")
    fns = parse_functions(code)
    return {
        "module": str(path),
        "language": "rust",
        "functions": [
            {
                "name": name,
                "effects": ["io"] if "print" in code else [],
                "resources": {"memory": "affine"},
            }
            for name in fns
        ],
        "abi": {
            "calling_convention": "trisynk_fastcall",
            "capabilities": ["borrow", "mut" if "mut" in code else "immut"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    ir = build_ir(args.input)
    payload = json.dumps(ir, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
