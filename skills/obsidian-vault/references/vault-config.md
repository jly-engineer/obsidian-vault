<overview>
**This is the only file you must edit to install.** Everything else reads from here.
Set your vault root, then adjust the folder map if your vault uses different names.
</overview>

<vault_root>
~/Documents/Vault
</vault_root>

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
Empty by default.

| Content | Exact path |
|---|---|
| | |
</custom_routing>
