# GitHub App Synchronization

## Objective
Manage Projects v2 automatically via a dedicated GitHub App that reads intent metadata (`meta.state`) and keeps project items in sync with Issues.

## App Configuration
1. **Create App** under `Settings → Developer settings → GitHub Apps`.
2. Permissions:
   - Issues: Read & write
   - Projects: Read & write (Projects v2)
   - Metadata: Read-only
3. Subscribe to events: Issues, Project item events (optional telemetry).
4. Install the app on `AmirTlinov/TriSynk` and record **App ID** and **Installation ID**.
5. Store secrets:
   - `GH_APP_ID`
   - `GH_APP_INSTALLATION_ID`
   - `GH_APP_PRIVATE_KEY` (PEM contents)
   - `PROJECT_ID` (GraphQL node ID for the target Project v2)
   - `PROJECT_FIELD_STATUS_ID` (Status single-select field ID)
   - `PROJECT_STATUS_MAP` – JSON like `{ "open": "option-id-open", "closed": "option-id-closed" }`

## Token Flow (workflow)
1. Generate JWT from App ID + private key.
2. Exchange JWT for installation access token (`POST /app/installations/{id}/access_tokens`).
3. Export the resulting token as `GITHUB_TOKEN` for GraphQL calls.
4. Run `scripts/sync_projects.py --apply` to update project items.

## Project Sync Logic
- Each tri-sync Issue corresponds to a Project item.
- Intents drive `meta.state`; `closed` intents close Issues and set the Project status option defined in `PROJECT_STATUS_MAP`.
- Missing items are created via `addProjectV2ItemById`; existing items receive `updateProjectV2ItemFieldValue` mutations.

## References
- [GitHub GraphQL Docs](https://docs.github.com/graphql)
- [`scripts/sync_projects.py`](../scripts/sync_projects.py)
- [`docs/git-projects.md`](git-projects.md)
