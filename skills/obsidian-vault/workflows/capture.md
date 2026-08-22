<required_reading>
references/vault-config.md
references/vault-structure.md
</required_reading>

<process>
<step_1>
Get the capture content — if the user provided content, use it directly. If not: ask "What do you want to capture?"
</step_1>

<step_2>
Create inbox note — file: `<vault_root>/00_Inbox/[short-title].md`

Use a slug for the filename: lowercase, hyphens, no special chars.
Example: "idea about GPU passthrough" → `gpu-passthrough.md`

```markdown
---
tags: [inbox]
created: YYYY-MM-DD
type: note
status: active
---

# [Title]

[Content as provided — no reformatting unless user asks]

---
*Captured [YYYY-MM-DD] — process later*
```
</step_2>

<step_3>
Confirm — state the filename created. Optionally suggest which folder it should eventually move to based on content.
</step_3>
</process>

<success_criteria>
- [ ] File created in 00_Inbox/
- [ ] Has valid YAML frontmatter
- [ ] Content preserved as-is
- [ ] User notified of filename
</success_criteria>
