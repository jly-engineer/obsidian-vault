<required_reading>
references/vault-config.md
references/vault-structure.md
</required_reading>

<process>
<step_1>
Identify the MOC — list what exists, then match the user's words to a title:

```bash
python3 -c "
import sqlite3, sys, os
conn = sqlite3.connect(os.path.expanduser(sys.argv[1] + '/vault_index.db'))
for r in conn.execute(\"SELECT path,title FROM notes WHERE type='moc' OR folder='30_Atlas'\"):
    print(r)
conn.close()
" '<vault_root>'
```

No match, and the user clearly wants a new index → create a new file in `30_Atlas/`
with `type: moc` frontmatter. Ambiguous match → ask which.
</step_1>

<step_2>
Read current MOC — use Read tool to load the full current content.
</step_2>

<step_3>
Apply the update — common operations:
- **Add a link:** append `- [[Note Name]] — [one-line description]` to the relevant section
- **Add a section:** create new H2 section with links under it
- **Update a status:** edit the existing line

Use Edit tool for surgical changes.
</step_3>

<step_4>
Confirm — state what was added/changed and in which MOC.
</step_4>
</process>

<success_criteria>
- [ ] Correct MOC identified and read
- [ ] Links use [[double brackets]]
- [ ] Edit tool used (not full Write)
- [ ] User confirmed
</success_criteria>
