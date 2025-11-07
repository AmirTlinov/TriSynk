#!/usr/bin/env python3
"""Smoke-test frontends JSON structure."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "frontends" / "samples" / "sample.rs"
CPP = ROOT / "frontends" / "samples" / "sample.cpp"
RS_FRONTEND = ROOT / "frontends" / "trisynk-rs" / "frontend.py"
CPP_FRONTEND = ROOT / "frontends" / "trisynk-cpp" / "frontend.py"


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def validate(payload: dict) -> None:
    required = {"module", "language", "functions", "abi"}
    missing = required - payload.keys()
    if missing:
        raise SystemExit(f"Payload missing keys: {missing}")
    if not isinstance(payload["functions"], list) or not payload["functions"]:
        raise SystemExit("Functions list empty")
    for fn in payload["functions"]:
        if "name" not in fn:
            raise SystemExit(f"Function missing name: {fn}")


def main() -> int:
    outputs = [
        run([sys.executable, str(RS_FRONTEND), str(RS)]),
        run([sys.executable, str(CPP_FRONTEND), str(CPP)]),
    ]
    for blob in outputs:
        validate(json.loads(blob))
    print("[test-frontends] ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
