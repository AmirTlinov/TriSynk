#!/usr/bin/env python3
"""Minimal validator for TriSynk Intent DSL drafts."""
import json
import sys
try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

REQUIRED_TOP_LEVEL = {"intent", "meta", "requirements", "constraints", "interop", "verifications", "telemetry"}


def load(stream):
    data = yaml.safe_load(stream)
    if not isinstance(data, dict):
        raise TypeError("Intent must be a mapping")
    missing = REQUIRED_TOP_LEVEL - data.keys()
    if missing:
        raise KeyError(f"Missing sections: {sorted(missing)}")
    if not data["meta"].get("issue"):
        raise ValueError("meta.issue is required")
    if not data["meta"].get("docs"):
        raise ValueError("meta.docs must reference documentation anchors")
    if not data["telemetry"].get("slos"):
        raise ValueError("telemetry.slos required")
    return data


def main() -> None:
    content = sys.stdin.read()
    try:
        load(content)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "fail", "error": str(exc)}))
        sys.exit(1)
    print(json.dumps({"status": "ok"}))


if __name__ == "__main__":
    main()
