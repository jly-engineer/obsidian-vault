<required_reading>
references/vault-config.md
references/vault-structure.md
</required_reading>

<process>
<step_1>
Check today's daily note — daily notes live at: `10_Daily_Notes/YYYY/MM/YYYY-MM-DD.md`

Query vault_index.db for today's date:
```bash
python3 -c "
import sqlite3, os
from datetime import date
conn = sqlite3.connect(os.path.expanduser('<vault_root>/vault_index.db'))
today = date.today().isoformat()
for r in conn.execute(\"SELECT path FROM notes WHERE folder='10_Daily_Notes' AND created=?\", (today,)):
    print(r[0])
conn.close()
"
```

If not found: create year/month subdirectories if needed, then create the file using the Daily Note template (copy from `90_Templates/Daily Note.md`, replace `{{date:YYYY-MM-DD}}` with today's date).
</step_1>

<step_2>
Determine what to log — if the user provided a summary, use it. If not: summarize the current session — what was discussed, what was built, what decisions were made, what's pending.
</step_2>

<step_3>
Append work log entry — use the Read tool to read the existing file first, then Edit to append — never overwrite.

Append to the `## Work Log` section of today's note:

```markdown
### [Short session title] — [HH:MM]

[2-5 bullet points: what happened, what was built, what changed]

**Decisions:**
- [Any choices locked in]

**Open items:**
- [ ] [Anything unresolved]
```
</step_3>

<step_4>
Update project Session Log tables — for each project touched during the session, append a row to its `## Session Log` table in `20_Projects/`:

```markdown
| YYYY-MM-DD | One-line summary of what changed | [[YYYY-MM-DD]] |
```

Rules:
- Read the project file first, then Edit — never overwrite
- One row per session per project — keep summaries tight (under 80 chars)
- Link always points to today's daily note via `[[YYYY-MM-DD]]`
- Only update projects where real work happened — skip untouched projects
</step_4>

<step_4b>
Promote priority open items to the dashboard note — if `<dashboard>` in `references/vault-config.md` is blank, **skip this step entirely**. Otherwise that note's `## Needs Attention` list is hand-maintained and does not self-update.

Apply this test to each open item logged in step 3. **Both** conditions must hold:

1. **Consequence if it slips a week** — something breaks, expires, or gets harder.
2. **Actionable now** — not blocked on someone else's reply or a prior step.

Condition 2 does most of the filtering. Typical pass rate is 2-3 items out of 10.

Overrides:
- User prefixed the open item with `!` → promote regardless of the test.
- Never auto-promote more than 3 per session. A Needs Attention list past ~7 lines stops being read.

**Present candidates to the user before writing** — list the items that passed and let them approve or cut. Do not write to the dashboard note unprompted.

On approval, Read the dashboard note, then Edit the `## Needs Attention` section — append, never overwrite:

```markdown
- [ ] **YYYY-MM-DD** — [Action] — [[source-note]]
- [ ] [Action, no deadline] — [[source-note]]
```

Rules:
- Dated items first, soonest at top; undated below them
- Link back to the source draft/project note so the item is actionable from the dashboard
- Before appending, scan existing entries — check off or remove any the session resolved, and skip duplicates
</step_4b>

<step_5>
Confirm — state: "Logged to `10_Daily_Notes/YYYY-MM-DD.md`" with a one-line summary of what was logged, list which project files were updated, and note any items promoted to or cleared from the dashboard note.
</step_5>
</process>

<success_criteria>
- [ ] Today's daily note exists
- [ ] Work log entry appended (not overwritten)
- [ ] Entry includes what happened + any open items
- [ ] Priority items offered for promotion to the dashboard note (or step skipped if unconfigured); resolved items cleared
- [ ] User confirmed
</success_criteria>
