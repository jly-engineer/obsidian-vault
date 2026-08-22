# obsidian-vault

**Obsidian vault operations for Claude Code — backed by a SQLite FTS index instead of filesystem search.**

Most vault integrations make Claude grep your notes folder, or read a Map of Content
and follow links until it finds something. Both burn tokens and both get slower as the
vault grows. This one keeps a SQLite index with an FTS5 table over every note's title,
tags, and body preview. Finding a note is one query returning one exact path.

```
/vault log session
/vault capture idea about batching the nightly export
/vault find oauth refresh
/vault update project Widget Pipeline
```

---

## Install

```
/plugin marketplace add jly-engineer/obsidian-vault
/plugin install obsidian-vault@jly-engineer
```

## Setup

Run it:

```
/vault
```

First run detects your vault, confirms the path with you, writes the config, and
builds the index. One exchange, no files to open.

```
Found a vault at ~/Documents/Notes — 84 markdown files. Use it?
> yes
vault_index.db — 84 notes total | +84 new | ~0 updated | 0 skipped | -0 removed
Your folders are Inbox/, Daily/, Projects/ — not the defaults. Remap?
```

Python 3 only, stdlib only. No pip install, no external deps.

**Prefer to do it by hand?** Edit `<vault_root>` in
`skills/obsidian-vault/references/vault-config.md` and run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py" ~/Documents/Notes
```

Every invocation runs a preflight check — unset config, a vault root that moved,
or a missing index each stop the skill and get resolved before it touches a note.
A stale path never silently half-executes a workflow.

Copy the three files in `templates/` into your vault's `90_Templates/` if you want
the matching note formats.

---

## What it does

| Command | Result |
|---|---|
| `/vault log session` | Appends a work-log entry to today's daily note, then adds a row to the `## Session Log` table of every project note touched this session |
| `/vault capture <idea>` | Slugged note into `00_Inbox/`, content preserved verbatim |
| `/vault update project <name>` | Locates the stub by index query, reads it, makes a surgical edit, bumps `Last updated` |
| `/vault create note <title>` | Routes to the right folder by content type, adds frontmatter, back-links related notes |
| `/vault research <topic>` | Permanent note in `40_Research/`, linked into the relevant MOC |
| `/vault guide <topic>` | Runbook in `50_Guides/` with prerequisites, steps, verification, and rollback |
| `/vault update moc <name>` | Appends links to a Map of Content in `30_Atlas/` |
| `/vault find <term>` | FTS query, reads the match, summarizes the relevant section only |

Run `/vault` bare to get a numbered menu instead.

## How it's built

Progressive disclosure. `SKILL.md` is the router — roughly 8KB, always loaded. Each of
the eight workflows is a separate file read only when that workflow is selected. You pay
context for the task you asked for, not for all eight.

```
skills/obsidian-vault/
├── SKILL.md                  # router + rules, always loaded
├── references/
│   ├── vault-config.md       # the only file you edit
│   ├── vault-structure.md    # folder scheme, index schema, frontmatter
│   └── external-projects.md  # optional registry of work outside the vault
└── workflows/                # 8 files, loaded on demand
scripts/build_vault_index.py  # stdlib-only indexer
templates/                    # Standard / Daily / Project note
```

Every workflow ends in a `success_criteria` checklist, so the model has something
concrete to verify against rather than declaring itself done.

## Vault conventions

The default layout is a PARA variant with numeric prefixes to fix folder ordering:

```
00_Inbox/         raw captures
10_Daily_Notes/   YYYY/MM/YYYY-MM-DD.md
20_Projects/      active project stubs, grouped by area
30_Atlas/         MOCs and index notes
40_Research/      permanent knowledge
50_Guides/        runbooks and how-tos
90_Templates/     never written to
```

**Your vault is not this vault, and that's fine.** The folder map in
`vault-config.md` is the source of truth — rename the folders, delete rows you don't
use, or point `10_Daily_Notes` at a flat `YYYY-MM-DD.md` scheme. Nothing else needs
editing.

Notes carry four frontmatter fields, all indexed:

```yaml
---
tags: []
created: 2026-01-15
type: note      # note | project | daily | moc | template
status: active  # active | archived | someday
---
```

## Index schema

Table `notes`: `path`, `title`, `folder`, `subfolder`, `type`, `status`, `tags`,
`created`, `preview` (300-char body excerpt), `updated_at`.

Virtual table `notes_fts` (FTS5) covers `title`, `tags`, `preview`, kept in sync by
insert/update/delete triggers. Query it directly if you want:

```bash
python3 -c "
import sqlite3
c = sqlite3.connect('$HOME/Documents/MyVault/vault_index.db')
for r in c.execute(\"SELECT n.path, n.title FROM notes n JOIN notes_fts ON notes_fts.rowid=n.rowid WHERE notes_fts MATCH 'backup' ORDER BY rank LIMIT 5\"):
    print(r)
"
```

The DB is disposable. Delete it and rebuild any time.

## Optional bits

- **`external-projects.md`** — a registry of work living outside the vault, so notes can
  reference it without a filesystem hunt. Ships empty. Delete it if unused.
  Store *paths* to credentials, never credentials — this file enters the model's context.
- **Dashboard promotion** — if you keep a dashboard note with a hand-maintained
  `## Needs Attention` list, name it in `vault-config.md` and session logging will offer
  to promote qualifying open items to it (never writes unprompted, caps at 3 per session).
  Leave it blank and the step is skipped.

## Notes

- Writes are scoped to the vault root. The skill will not modify files outside it and
  will not delete non-markdown files.
- Edits are surgical — existing notes are read, then edited, never overwritten.
- Index build is read-only against your notes; it only writes `vault_index.db`.

## License

MIT
