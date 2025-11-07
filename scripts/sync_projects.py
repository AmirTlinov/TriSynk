#!/usr/bin/env python3
"""Synchronize tri-sync Issues with GitHub Projects v2 via GraphQL."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib import error, request

GRAPH_PATH = Path("data/outbox/issues_intents.json")
GRAPHQL_URL = "https://api.github.com/graphql"
REST_ROOT = "https://api.github.com"


def load_graph(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing graph export: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_issue_payloads(graph: dict[str, Any]) -> list[dict[str, Any]]:
    intents_by_issue: dict[str, list[dict[str, Any]]] = {}
    for intent in graph.get("intents", []):
        issue_id = intent.get("issue")
        if not issue_id:
            continue
        intents_by_issue.setdefault(issue_id, []).append(intent)

    payloads: list[dict[str, Any]] = []
    for issue in graph.get("issues", []):
        tri_id = issue["id"]
        linked = intents_by_issue.get(tri_id, [])
        desired_state = "open"
        for intent in linked:
            state = intent.get("state", "open")
            if state != "open":
                desired_state = state
        payloads.append(
            {
                "tri_id": tri_id,
                "title": issue["title"],
                "state": desired_state,
            }
        )
    return payloads


def rest_request(token: str, url: str) -> Any:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(url, headers=headers)
    with request.urlopen(req) as resp:  # noqa: S310
        charset = resp.headers.get_content_charset("utf-8")
        return json.loads(resp.read().decode(charset))


def graphql_request(token: str, query: str, variables: dict[str, Any]) -> Any:
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    req = request.Request(GRAPHQL_URL, data=body, headers=headers)
    try:
        with request.urlopen(req) as resp:  # noqa: S310
            charset = resp.headers.get_content_charset("utf-8")
            return json.loads(resp.read().decode(charset))
    except error.HTTPError as exc:  # noqa: BLE001
        text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GraphQL error {exc.code}: {text}") from exc


def fetch_tri_issues(repo: str, token: str) -> dict[str, dict[str, Any]]:
    issues: dict[str, dict[str, Any]] = {}
    page = 1
    while True:
        url = f"{REST_ROOT}/repos/{repo}/issues?state=all&labels=tri-sync&per_page=100&page={page}"
        batch = rest_request(token, url)
        if not batch:
            break
        for issue in batch:
            tri_id = issue.get("title", "").split(":", 1)[0]
            issues[tri_id] = issue
        page += 1
        if len(batch) < 100:
            break
    return issues


def fetch_project_items(project_id: str, token: str) -> dict[str, str]:
    items: dict[str, str] = {}
    cursor = None
    query = """
    query($project: ID!, $after: String) {
      node(id: $project) {
        ... on ProjectV2 {
          items(first: 100, after: $after) {
            nodes {
              id
              content {
                ... on Issue { id title }
              }
            }
            pageInfo { hasNextPage endCursor }
          }
        }
      }
    }
    """
    while True:
        data = graphql_request(token, query, {"project": project_id, "after": cursor})
        node = data.get("data", {}).get("node")
        if not node:
            break
        items_page = node["items"]
        for entry in items_page["nodes"]:
            content = entry.get("content") or {}
            issue_id = content.get("id")
            if issue_id:
                items[issue_id] = entry["id"]
        page_info = items_page["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]
    return items


def add_project_item(project_id: str, content_id: str, token: str) -> str:
    mutation = """
    mutation($project: ID!, $content: ID!) {
      addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
        item { id }
      }
    }
    """
    data = graphql_request(token, mutation, {"project": project_id, "content": content_id})
    item = data.get("data", {}).get("addProjectV2ItemById", {}).get("item")
    if not item:
        raise RuntimeError("Failed to add project item")
    return item["id"]


def update_project_status(project_id: str, item_id: str, field_id: str, option_id: str, token: str) -> None:
    mutation = """
    mutation($project: ID!, $item: ID!, $field: ID!, $option: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $project,
        itemId: $item,
        fieldId: $field,
        value: { singleSelectOptionId: $option }
      }) {
        projectV2Item { id }
      }
    }
    """
    graphql_request(token, mutation, {"project": project_id, "item": item_id, "field": field_id, "option": option_id})


def write_plan(plan: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", default=str(GRAPH_PATH))
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPO"))
    parser.add_argument("--apply", action="store_true", help="Apply mutations against GitHub")
    parser.add_argument("--plan", default="data/outbox/projects_sync_payload.json", help="Where to store dry-run plan")
    args = parser.parse_args()

    graph = load_graph(Path(args.graph))
    payloads = build_issue_payloads(graph)

    if not args.apply:
        write_plan(payloads, Path(args.plan))
        print(f"[sync-projects] dry-run wrote {args.plan}")
        return 0

    token = os.environ.get("GITHUB_TOKEN")
    project_id = os.environ.get("PROJECT_ID")
    field_id = os.environ.get("PROJECT_FIELD_STATUS_ID")
    status_map_raw = os.environ.get("PROJECT_STATUS_MAP")
    repo = args.repo
    if not all([token, project_id, field_id, status_map_raw, repo]):
        raise SystemExit("Missing PROJECT_ID/PROJECT_FIELD_STATUS_ID/PROJECT_STATUS_MAP/GITHUB_TOKEN/GITHUB_REPO")
    status_map = json.loads(status_map_raw)

    tri_issues = fetch_tri_issues(repo, token)
    project_items = fetch_project_items(project_id, token)

    plan: list[dict[str, Any]] = []
    for payload in payloads:
        tri_id = payload["tri_id"]
        desired_state = payload["state"]
        issue = tri_issues.get(tri_id)
        record = {"issue": tri_id, "state": desired_state, "actions": []}
        if not issue:
            record["actions"].append("missing_issue")
            plan.append(record)
            continue
        content_id = issue.get("node_id")
        if not content_id:
            record["actions"].append("missing_node_id")
            plan.append(record)
            continue
        item_id = project_items.get(content_id)
        if not item_id:
            item_id = add_project_item(project_id, content_id, token)
            project_items[content_id] = item_id
            record["actions"].append("added_item")
        option_id = status_map.get(desired_state) or status_map.get("default")
        if not option_id:
            raise SystemExit(f"Missing status option for state {desired_state}")
        update_project_status(project_id, item_id, field_id, option_id, token)
        record["actions"].append("updated_status")
        plan.append(record)

    write_plan(plan, Path(args.plan))
    print(f"[sync-projects] applied plan written to {args.plan}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
