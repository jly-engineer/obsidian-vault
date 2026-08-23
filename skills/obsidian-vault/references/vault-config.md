<overview>
**This is the only file you must edit to install.** Everything else reads from here.

You do not have to edit it by hand — run `/vault` once and it will detect your
vault, confirm it with you, write this file, and build the index.
</overview>

<vault_root>
UNCONFIGURED
</vault_root>

<!--
UNCONFIGURED is a deliberate sentinel, not a placeholder path. A plausible-looking
default (~/Documents/Vault) fails silently when wrong — the model routes a note to
a directory that does not exist and only errors on write. The sentinel cannot be
mistaken for a real vault, so preflight always catches it.
Replace the whole line with your vault root, e.g. ~/Documents/MyVault

Prefer a `~/`-relative path over an absolute one — preflight resolves `~` per
environment, so a config written on one machine still works after a repo move,
a new container, or a fresh account. An absolute path baked in from a different
environment is exactly what produces BAD_ROOT after a move.
-->

<folder_map>
Change the right column to match your vault. The left column is what the skill
routes on — leave it alone. Delete rows you do not use.

| Purpose | Your folder |
|---|---|
| Raw captures, unprocessed ideas | `00_Inbox` |
| Daily / session logs | `10_Daily_Notes` |
| Active project notes | `20_Projects` |
| Maps of Content, indexes | `30_Atlas` |
| Permanent reference notes | `40_Research` |
| Guides, runbooks, how-tos | `50_Guides` |
| Templates (never written to) | `90_Templates` |

Daily note path pattern: `10_Daily_Notes/YYYY/MM/YYYY-MM-DD.md`
Flat instead? Change to `10_Daily_Notes/YYYY-MM-DD.md`.
</folder_map>

<index_db>
Path: `<vault_root>/vault_index.db`
Builder: `${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py`

`${CLAUDE_PLUGIN_ROOT}` is set automatically when installed as a plugin. Installed
the skill by hand instead? Replace it with the path you copied the repo to.

Build the index once before first use:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py" ~/Documents/Vault
```
</index_db>

<dashboard>
Optional. If your vault has a dashboard note with a hand-maintained
`## Needs Attention` list, name it here. Leave blank to disable step_4b
of the session-log workflow.

Dashboard note: `Home.md`
</dashboard>

<custom_routing>
Optional. Exact-path overrides for content that must always land in one place.

| Content | Exact path |
|---|---|
| Family projects | `20_Projects/Family/` |
| Business projects | `20_Projects/Business/` |
| Personal projects | `20_Projects/Personal/` |
| Health projects | `20_Projects/Health/` |

Research (`40_Research/`) and Guides (`50_Guides/`) stay flat regardless of
Area — cross-link them from the matching Area's MOC in `30_Atlas/` instead of
subfoldering them. New Areas get a row here automatically during first-run
setup (`workflows/setup.md`) based on what the user says they want to organize.
</custom_routing>
