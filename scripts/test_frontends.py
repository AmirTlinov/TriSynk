#!/usr/bin/env python3
"""Smoke-test frontends JSON structure."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS_SAMPLES = sorted((ROOT / "frontends" / "samples").glob("*.rs"))
CPP_SAMPLES = sorted((ROOT / "frontends" / "samples").glob("*.cpp"))
RS_FRONTEND = ROOT / "frontends" / "trisynk-rs" / "frontend.py"
CPP_FRONTEND = ROOT / "frontends" / "trisynk-cpp" / "frontend.py"
SCHEMA = json.loads((ROOT / "schema" / "frontend_ir.schema.json").read_text(encoding="utf-8"))


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def validate(payload: dict) -> None:
    for key in SCHEMA["required"]:
        if key not in payload:
            raise SystemExit(f"Missing key {key}")
    if payload["language"] not in {"rust", "cpp"}:
        raise SystemExit(f"Unsupported language {payload['language']}")
    functions = payload.get("functions", [])
    if not isinstance(functions, list) or not functions:
        raise SystemExit("Functions list empty")
    for fn in functions:
        for field in ("name", "effects", "resources"):
            if field not in fn:
                raise SystemExit(f"Function missing {field}: {fn}")
        if not isinstance(fn["effects"], list):
            raise SystemExit("effects must be list")
        if not isinstance(fn["resources"], dict):
            raise SystemExit("resources must be object")
    abi = payload.get("abi", {})
    if abi.get("calling_convention") != "trisynk_fastcall":
        raise SystemExit("ABI calling convention mismatch")


def main() -> int:
    outputs = []
    for sample in RS_SAMPLES:
        blob = run([sys.executable, str(RS_FRONTEND), str(sample)])
        outputs.append(blob)
    for sample in CPP_SAMPLES:
        blob = run([sys.executable, str(CPP_FRONTEND), str(sample)])
        outputs.append(blob)
    for blob in outputs:
        validate(json.loads(blob))
    print(f"[test-frontends] ok ({len(outputs)} artifacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
