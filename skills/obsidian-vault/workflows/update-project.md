<required_reading>
references/vault-config.md
references/vault-config.md
references/vault-structure.md
references/external-projects.md
</required_reading>

<process>
<step_1>
Identify the project — map the user's intent to the correct stub file.

Query the index by keyword first:

```bash
python3 -c "
import sqlite3, sys, os
conn = sqlite3.connect(os.path.expanduser(sys.argv[1] + '/vault_index.db'))
for r in conn.execute(\"SELECT path,title FROM notes WHERE folder='20_Projects' AND (title LIKE ? OR tags LIKE ?)\", ('%'+sys.argv[2]+'%','%'+sys.argv[2]+'%')):
    print(r)
conn.close()
" '<vault_root>' 'KEYWORD'
```

If the query returns nothing, fall back to FTS (see `references/vault-structure.md`).
If it returns more than one candidate, ask which.

**Optional — alias table.** If you refer to projects by nicknames the note titles
do not contain, add rows here so routing is one step instead of two:

| User says | File |
|---|---|
| | |
</step_1>

<step_2>
Read the current stub — use the Read tool to load the full current content before making any changes.
</step_2>

<step_3>
Determine what to update — apply the user's changes to the appropriate section:

- New info → `## Notes & Context`
- Completed task → check off in `## Goals`
- New goal → add to `## Goals`
- New decision → add row to `## Key Decisions`
- Status change → update `## Status`
- Infrastructure info → update relevant section

Update `**Last updated:**` to today's date.
</step_3>

<step_4>
Write the update — use Edit tool (not Write) to make surgical changes. Only change what needs changing.
</step_4>

<step_5>
Confirm — state what was updated and in which section.
</step_5>
</process>

<success_criteria>
- [ ] Correct stub file identified
- [ ] Current content read before editing
- [ ] Edit tool used (not full Write)
- [ ] Last updated date current
- [ ] User confirmed
</success_criteria>
