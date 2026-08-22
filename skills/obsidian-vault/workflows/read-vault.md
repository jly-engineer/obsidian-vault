<required_reading>
references/vault-config.md
references/vault-structure.md
</required_reading>

<process>
<step_1>
Query the index — query vault_index.db first. One python3 call returns the exact path — no filesystem search, no MOC traversal needed.

```bash
python3 -c "
import sqlite3, sys, os
conn = sqlite3.connect(os.path.expanduser('<vault_root>/vault_index.db'))
for r in conn.execute(\"SELECT n.path, n.title, n.tags, n.preview FROM notes n JOIN notes_fts ON notes_fts.rowid=n.rowid WHERE notes_fts MATCH ? ORDER BY rank LIMIT 8\", (sys.argv[1],)):
    print(r)
conn.close()
" 'SEARCH_TERM'
```

For non-keyword lookups:

| Need | Query |
|------|-------|
| Projects by area | `SELECT path,title FROM notes WHERE folder='20_Projects' AND subfolder='HomeLab'` |
| By tag | `SELECT path,title FROM notes WHERE tags LIKE '%homelab%'` |
| MOCs only | `SELECT path,title FROM notes WHERE type='moc'` |
| Today's daily | `SELECT path FROM notes WHERE folder='10_Daily_Notes' ORDER BY created DESC LIMIT 1` |
</step_1>

<step_2>
Read the matched file:

```
Read("<vault_root>/" + path_from_query)
```

Summarize the relevant sections — don't dump the whole file unless asked.
</step_2>

<step_3>
Refresh if missing — if a note isn't found in the DB:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py" <vault_root>
```

Then re-query.
</step_3>

<step_4>
Offer next action — after reading, offer: "Want me to update this note, log something here, or create a related note?"
</step_4>
</process>

<success_criteria>
- [ ] Correct file located
- [ ] Relevant content surfaced (not full dump)
- [ ] Next action offered
</success_criteria>
