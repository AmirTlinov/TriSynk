#!/usr/bin/env python3
"""Prototype C++-to-clmr frontend stub."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FN_RE = re.compile(r"^\s*(?:inline\s+)?(?:constexpr\s+)?(?:void|int|float|double|auto)\s+(?P<name>[A-Za-z0-9_]+)\s*\(")


def parse_functions(text: str):
    names = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("//"):
            continue
        match = re.match(r"^(?:template<.*>)?\s*(?:inline\s+)?(?:constexpr\s+)?([A-Za-z0-9_:<>]+)\s+([A-Za-z0-9_]+)\s*\(", line)
        if match:
            names.append(match.group(2))
    return names


def build_ir(path: Path) -> dict:
    code = path.read_text(encoding="utf-8")
    functions = parse_functions(code)
    return {
        "module": str(path),
        "language": "cpp",
        "functions": [
            {
                "name": name,
                "effects": ["io"] if "std::cout" in code else [],
                "resources": {"memory": "capability"},
            }
            for name in functions
        ],
        "abi": {
            "calling_convention": "trisynk_fastcall",
            "layout_hash": hash(code) & 0xFFFFFFFF,
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
