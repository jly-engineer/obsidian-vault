<vault_root>
Defined in `references/vault-config.md`. Read that first — never assume a path.
</vault_root>

<folder_tree>
Default layout. Yours may differ — `vault-config.md` is the source of truth.

```
<vault_root>/
├── .obsidian/
├── 00_Inbox/                    # Raw captures — process later
├── 10_Daily_Notes/              # One file per day: YYYY/MM/YYYY-MM-DD.md
├── 20_Projects/                 # Active project stubs, grouped by area
├── 30_Atlas/                    # MOCs and index notes
├── 40_Research/                 # Permanent knowledge notes
├── 50_Guides/                   # Implementation guides and runbooks
└── 90_Templates/                # Templates only (never written to)
    ├── Standard Note.md
    ├── Daily Note.md
    └── Project Note.md
```

This is a PARA variant: Inbox → Projects → Atlas/Research → Guides. Numeric
prefixes keep folder order stable in Obsidian's file explorer. Rename freely —
update `vault-config.md` to match.
</folder_tree>

<vault_index>
`<vault_root>/vault_index.db` — SQLite index of every note. Query it instead of
searching the filesystem: one query returns an exact path, no MOC traversal.

Builder: `scripts/build_vault_index.py <vault_root>`

Schema, table `notes`:
`path` (relative), `title`, `folder`, `subfolder`, `type`, `status`, `tags`,
`created`, `preview` (300-char body excerpt), `updated_at` (mtime)

FTS5 table `notes_fts` covers title + tags + preview, kept in sync by triggers.
Re-running the builder is incremental — unchanged files are skipped by mtime.

Refresh after creating notes in a session:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py" <vault_root>
```
</vault_index>

<frontmatter_reference>
```yaml
---
tags: []
created: 2026-01-15
type: note
status: active
---
```

type values: `note` | `project` | `daily` | `moc` | `template`
status values: `active` | `archived` | `someday`

Tags are free-form. Pick a small controlled set and stay consistent — the FTS
index searches them, so sloppy tags degrade retrieval.
</frontmatter_reference>

<daily_note_format>
```markdown
---
tags: [daily]
created: YYYY-MM-DD
type: daily
---

# YYYY-MM-DD — Daily Log

## Focus
<!-- 1-3 priorities -->

## Work Log
<!-- What happened -->

## Decisions Made
<!-- Choices locked in -->

## Open Questions
<!-- Unresolved items -->

## Tomorrow
<!-- Carries forward -->
```
</daily_note_format>

<create_daily_note>
Check whether today's note exists by querying the index:

```bash
python3 -c "
import sqlite3, os, sys
from datetime import date
conn = sqlite3.connect(os.path.expanduser(sys.argv[1] + '/vault_index.db'))
rows = list(conn.execute(\"SELECT path FROM notes WHERE folder='10_Daily_Notes' AND created=?\", (date.today().isoformat(),)))
print(rows[0][0] if rows else 'NOT FOUND')
conn.close()
" '<vault_root>'
```

If missing: create the year/month subdirectories, then create the file from
`90_Templates/Daily Note.md`, replacing `{{date:YYYY-MM-DD}}` with today's date.
</create_daily_note>
