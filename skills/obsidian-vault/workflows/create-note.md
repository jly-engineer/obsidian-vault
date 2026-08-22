<required_reading>
references/vault-config.md
references/vault-structure.md
</required_reading>

<process>
<step_1>
Determine folder from content type:

| Content type | Folder |
|---|---|
| Quick idea, unprocessed thought | `00_Inbox/` |
| Daily log entry | `10_Daily_Notes/` |
| Active project note | `20_Projects/` |
| Index, hub, MOC | `30_Atlas/` |
| Permanent knowledge (won't change) | `40_Research/` |

When unsure: `00_Inbox/` — can be moved later.
</step_1>

<step_2>
Generate filename:
- Lowercase, hyphens, no special chars
- Descriptive but concise
- Examples: `backup-strategy.md`, `oauth-token-refresh.md`

For dated notes: `YYYY-MM-DD-topic.md`
</step_2>

<step_3>
Write the note:

```markdown
---
tags: [relevant-tags]
created: YYYY-MM-DD
type: [note|project|moc]
status: active
---

# [Title]

## Summary
[One paragraph]

## Content
[Main body]

## Links
[Related notes using [[double brackets]]]
```
</step_3>

<step_4>
Add links to related notes — after creating, check if any existing notes should link to the new one. If so, append the link to their `## Links` section using Edit tool.
</step_4>

<step_5>
Confirm — state: filename, folder, and any links added.
</step_5>
</process>

<success_criteria>
- [ ] File in correct folder
- [ ] Valid YAML frontmatter
- [ ] Internal links use [[double brackets]]
- [ ] Related notes updated with back-links if relevant
</success_criteria>
