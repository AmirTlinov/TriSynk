#!/usr/bin/env python3
"""Sync docs/issues + intents into GitHub Issues/Projects descriptors."""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib import request, error

GRAPH_PATH = Path("data/outbox/issues_intents.json")
GITHUB_API = "https://api.github.com"


def load_graph(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing graph export: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_payloads(graph: dict[str, Any]) -> list[dict[str, Any]]:
    intents_by_issue: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for intent in graph.get("intents", []):
        issue_id = intent.get("issue")
        if issue_id:
            intents_by_issue[issue_id].append(intent)
    payloads: list[dict[str, Any]] = []
    for issue in graph.get("issues", []):
        body_parts = [issue["body"]]
        linked = intents_by_issue.get(issue["id"], [])
        if linked:
            lines = ["### Linked Intents"]
            for intent in linked:
                link = intent["file"]
                goal = intent.get("requirements", {}).get("goal", "")
                lines.append(f"- `{intent['meta'].get('id', 'INT-???')}` ({link}): {goal}")
            body_parts.append("\n".join(lines))
        body = "\n\n".join(body_parts)
        payloads.append(
            {
                "title": f"{issue['id']}: {issue['title']}",
                "body": body,
                "labels": ["tri-sync"],
                "tri_id": issue["id"],
                "dependencies": issue.get("dependencies", []),
                "references": issue.get("references", []),
            }
        )
    return payloads


def github_request(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> Any:
    data = None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=data, method=method, headers=headers)
    try:
        with request.urlopen(req) as resp:
            charset = resp.headers.get_content_charset("utf-8")
            return json.loads(resp.read().decode(charset))
    except error.HTTPError as exc:  # noqa: BLE001
        text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API error {exc.code}: {text}") from exc


def push_payloads(payloads: list[dict[str, Any]], repo: str | None, token: str, dry_run: bool, mock_output: Path | None) -> None:
    if dry_run:
        print(json.dumps({"preview": payloads}, indent=2, ensure_ascii=False))
        return
    if repo in {None, "local"} or mock_output is not None:
        target = mock_output or Path("data/outbox/github_sync_payload.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payloads, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[sync-issues] Mock sync wrote {target}")
        return
    for payload in payloads:
        title = payload["title"]
        url = f"{GITHUB_API}/repos/{repo}/issues"
        body = {
            "title": title,
            "body": payload["body"],
            "labels": payload["labels"],
        }
        print(f"[sync-issues] Creating issue for {title}")
        github_request("POST", url, token, body)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", default=str(GRAPH_PATH))
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPO"))
    parser.add_argument("--apply", action="store_true", help="Create issues via GitHub API")
    parser.add_argument("--mock-output", type=Path, help="Write payloads to file instead of hitting GitHub")
    args = parser.parse_args()

    graph = load_graph(Path(args.graph))
    payloads = build_payloads(graph)
    token = os.environ.get("GITHUB_TOKEN")
    dry_run = not args.apply
    if args.apply and (not token or not args.repo):
        raise SystemExit("--apply requires GITHUB_TOKEN and --repo or GITHUB_REPO")
    push_payloads(payloads, args.repo, token or "", dry_run=dry_run, mock_output=args.mock_output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
