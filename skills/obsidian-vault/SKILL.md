---
name: obsidian-vault
description: Read and write notes in the user's Obsidian vault or Markdown note collection — capture ideas to an inbox, log what was worked on, create or update project notes, write research notes and how-to guides, maintain Maps of Content, and find existing notes through a SQLite full-text index rather than searching the filesystem. Use this whenever the user wants something written down, remembered, filed, logged, looked up, or updated in their notes — including phrasings that never say "vault" or "Obsidian", such as "make a note of this", "capture that", "log today's session", "what did I write about X", "where did I put my notes on Y", "add this to my project notes", or "write that up". Also use it before answering a question about the user's own past decisions, contacts, or project state, since the answer usually lives in their notes rather than in this conversation.
---

<objective>
Manage an Obsidian vault. Create, update, and retrieve notes across the vault's
folder hierarchy. Maintain session logs, project stubs, research notes,
implementation guides, and Maps of Content using the vault's conventions and a
SQLite index for navigation.
</objective>

<preflight>
**Run this before anything else — before the intake menu, before routing, before
reading any workflow. No exceptions.** A stale or unset vault root does not fail
loudly; it fails three steps into a workflow after the model has already decided
what to write and where. Catch it here.

```bash
python3 - <<'PF'
import os, re, pathlib
cfg = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT", ".")) / "skills/obsidian-vault/references/vault-config.md"
if not cfg.is_file():
    print("STATUS=NO_CONFIG"); raise SystemExit
m = re.search(r"<vault_root>\s*\n(.+?)\n\s*</vault_root>", cfg.read_text(), re.S)
root = (m.group(1).strip() if m else "")
if not root or root == "UNCONFIGURED":
    print("STATUS=UNCONFIGURED"); raise SystemExit
p = pathlib.Path(root).expanduser()
if not p.is_dir():
    print(f"STATUS=BAD_ROOT ROOT={p}"); raise SystemExit
db = p / "vault_index.db"
n = len([f for f in p.rglob("*.md") if ".obsidian" not in f.parts])
if not db.is_file():
    print(f"STATUS=NO_INDEX ROOT={p} MD_FILES={n}"); raise SystemExit
print(f"STATUS=READY ROOT={p} MD_FILES={n}")
PF
```

Act on `STATUS`:

| STATUS | Action |
|---|---|
| `READY` | Proceed normally. Do not mention preflight to the user. |
| `UNCONFIGURED` | First run. Read `workflows/setup.md` and follow it. **Do not show the intake menu first.** |
| `BAD_ROOT` | Configured root does not exist — moved or mistyped. Tell the user the path that failed, then read `workflows/setup.md` to re-detect. |
| `NO_INDEX` | Root is valid, index missing. Say so, build it, then continue: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py" "<root>"` |
| `NO_CONFIG` | Install is broken — `vault-config.md` is missing. Report it; do not guess a path. |

Until `STATUS=READY`, the vault root is unknown, and a write to an unknown root
is a write to the wrong place. So while the status is anything else, no file gets
created, edited, or appended anywhere — not a note, not a daily log, not a
placeholder folder. The one exception is the config edit that setup.md makes
after the user confirms a path, because that edit is what produces a known root.

A guessed root is never a substitute for a failed one. If you cannot reach
`READY`, say what's wrong and stop; that leaves the user one clear thing to fix,
which beats handing back a note they now have to go find.
</preflight>

<quick_start>
1. Run `<preflight>` above. On anything but `READY`, resolve that first.
2. Read `references/vault-config.md` — it defines the vault root and folder names.
   Never assume a path.
3. Most common task, session logging: read `workflows/log-session.md` and follow it.
4. Anything else: match the intent-routing table in `<intake>`, then read that workflow.
</quick_start>

<essential_principles>

<vault_root>
Defined in `references/vault-config.md`. Read it before touching any file.
Referred to below as `<vault_root>`.
</vault_root>

<note_frontmatter>
Required on every note:
```yaml
---
tags: []
created: YYYY-MM-DD
type: [note|project|daily|moc|template]
status: [active|archived|someday]
---
```
</note_frontmatter>

<folder_routing>
Default map — `references/vault-config.md` overrides it.

| Content | Folder |
|---|---|
| Raw captures, quick ideas | `00_Inbox/` |
| Daily logs, session logs | `10_Daily_Notes/YYYY/MM/YYYY-MM-DD.md` |
| Active project notes | `20_Projects/` |
| Maps of Content, indexes | `30_Atlas/` |
| Permanent reference notes | `40_Research/` |
| Implementation guides, runbooks, how-tos | `50_Guides/` |
| Templates only | `90_Templates/` |

Exact-path overrides live in the `<custom_routing>` table of `vault-config.md`.
Check it before routing — a matching row wins over this table.
</folder_routing>

<vault_index>
`<vault_root>/vault_index.db` is a SQLite index of every note in the vault.
**Always query it before reading files** — one query returns the exact path,
eliminating filesystem searches and MOC traversal.

Query via python3 (the sqlite3 CLI is often not installed):

```bash
python3 -c "
import sqlite3, sys, os
conn = sqlite3.connect(os.path.expanduser(sys.argv[1] + '/vault_index.db'))
for r in conn.execute(\"SELECT n.path, n.title, n.tags FROM notes n JOIN notes_fts ON notes_fts.rowid=n.rowid WHERE notes_fts MATCH ? ORDER BY rank LIMIT 5\", (sys.argv[2],)):
    print(r)
conn.close()
" '<vault_root>' 'search term'
```

Common query patterns:

| Need | Query |
|------|-------|
| Topic keyword | `WHERE notes_fts MATCH 'keyword'` (use the FTS join above) |
| Projects in one area | `SELECT path,title FROM notes WHERE folder='20_Projects' AND subfolder='Area'` |
| By tag | `SELECT path,title FROM notes WHERE tags LIKE '%tagname%'` |
| By type | `SELECT path,title FROM notes WHERE type='moc'` |
| Today's daily note | `SELECT path FROM notes WHERE folder='10_Daily_Notes' AND created='YYYY-MM-DD'` |

Read the returned `path` prefixed with `<vault_root>/`. Do NOT grep the
filesystem or read MOCs just to find a file.

Refresh the index if a note isn't found, or after creating notes this session:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py" <vault_root>
```
</vault_index>

<atlas_lookup_rule>
Before any task needing details that live in the vault — addresses, hostnames,
service ports, IDs, project-specific config — read the relevant `30_Atlas/` note
first. Query the index for `type='moc'` to list them.

Never supply such details from memory or from an earlier session. If Atlas
doesn't cover it, check the matching `20_Projects/` note next, then ask.
</atlas_lookup_rule>

<link_convention>
Always use `[[Double Brackets]]` for internal links. Never relative paths.
</link_convention>

<session_logging_rule>
At the end of every session:

1. **Daily note** — append a work log entry to
   `10_Daily_Notes/YYYY/MM/YYYY-MM-DD.md`. Create the year/month subdirectories
   if absent. Create the file from the Daily Note template if absent.

2. **Project Session Log tables** — for each `20_Projects/` file touched this
   session, append a row to its `## Session Log` table:

   ```
   | YYYY-MM-DD | One-line summary of what changed | [[YYYY-MM-DD]] |
   ```

   Rules:
   - Read the project file first, then Edit — never overwrite
   - One row per session per project — summaries under 80 chars
   - Link always points to today's daily note via `[[YYYY-MM-DD]]`
   - Only update projects where real work happened
</session_logging_rule>

<write_scope_rule>
Never modify files outside the vault root. Never delete existing non-markdown
files. Prefer Edit over Write on any file that already exists.

The vault holds notes and nothing else. Scratch files — a throwaway Python
script, a scraped page, intermediate output — go under `/tmp`, never in the vault
root, because the vault is a place the user browses by hand and syncs across
machines. A stray `.py` there is litter they have to identify and clean up
themselves, and Obsidian will happily sync it to every device first.

Prefer `python3 -c` or a heredoc over writing a script file at all; if a run
genuinely needs a file on disk, `mktemp` gives you one that cleans itself up.
</write_scope_rule>

</essential_principles>

<intake>
Preflight must have returned `READY` before this section runs.

If the user's message already contains clear intent, route directly without
presenting the menu:

| Intent signal | Route to |
|---|---|
| "log", "session", "log the session", "what we did" | `workflows/log-session.md` |
| "capture", "inbox", "quick note", "idea" | `workflows/capture.md` |
| "update project", project name + change described | `workflows/update-project.md` |
| "create note", "new note", "write note" | `workflows/create-note.md` |
| "research", "permanent note", "40_Research" | `workflows/create-research.md` |
| "guide", "runbook", "how-to", "50_Guides" | `workflows/create-guide.md` |
| "moc", "map of content", "atlas", "index" | `workflows/update-moc.md` |
| "read", "find", "search", "what's in" | `workflows/read-vault.md` |

Otherwise, ask:

What would you like to do?

1. **Log session** — append what we did to today's daily note
2. **Capture** — drop a raw idea into the Inbox
3. **Update project** — read and update a project stub in 20_Projects/
4. **Create note** — create a new note in the right folder
5. **Research** — create or update a permanent note in 40_Research/
6. **Guide** — create or update an implementation guide in 50_Guides/
7. **Update MOC** — add links to a Map of Content in 30_Atlas/
8. **Read vault** — find and read existing notes
</intake>

<routing>
| Response | Workflow |
|---|---|
| 1, "log", "session log", "what we did" | `workflows/log-session.md` |
| 2, "capture", "inbox", "quick note", "idea" | `workflows/capture.md` |
| 3, "update project", "project stub", "project note" | `workflows/update-project.md` |
| 4, "create note", "new note", "write note" | `workflows/create-note.md` |
| 5, "research", "permanent note", "40_Research" | `workflows/create-research.md` |
| 6, "guide", "runbook", "how-to", "50_Guides" | `workflows/create-guide.md` |
| 7, "moc", "map of content", "atlas", "index" | `workflows/update-moc.md` |
| 8, "read", "find", "search", "what's in" | `workflows/read-vault.md` |

After reading the workflow, follow it exactly.
</routing>

<reference_index>
**Install config (read first):** references/vault-config.md
**Vault knowledge:** references/vault-structure.md
**External project registry:** references/external-projects.md
</reference_index>

<workflows_index>
| Workflow | Purpose |
|---|---|
| log-session.md | Append session summary to today's daily note |
| capture.md | Quick capture to 00_Inbox |
| update-project.md | Read and update a 20_Projects stub |
| create-note.md | Create a new note routed to the correct folder |
| create-research.md | Create a permanent knowledge note in 40_Research |
| create-guide.md | Create an implementation guide or runbook in 50_Guides |
| update-moc.md | Add links to a 30_Atlas MOC |
| read-vault.md | Find and read existing vault notes |
| setup.md | First-run: detect vault, write config, build index, ask what prompted the install and set up initial Areas |
</workflows_index>

<success_criteria>
- [ ] Preflight run first; returned READY or setup completed
- [ ] vault-config.md read before any path was used
- [ ] Task routed to the correct workflow
- [ ] Vault index queried before reading files
- [ ] Atlas consulted before using vault-stored details
- [ ] All created/edited notes have valid YAML frontmatter
- [ ] Internal links use [[double brackets]]
- [ ] Session log updated at session end
</success_criteria>
