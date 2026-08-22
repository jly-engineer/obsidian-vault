<required_reading>
references/vault-config.md
references/vault-structure.md
</required_reading>

<process>
<step_1>
Confirm this is permanent knowledge — research notes (`40_Research/`) are for knowledge that doesn't expire:
- How a technology works
- A concept explained in your own words
- A reference that will be returned to
- A decision framework

If it's project-specific or time-sensitive → use `20_Projects/` or `00_Inbox/` instead.
</step_1>

<step_2>
Write the note — file: `<vault_root>/40_Research/[topic].md`

```markdown
---
tags: [relevant-tags]
created: YYYY-MM-DD
type: note
status: active
---

# [Topic Title]

## Summary
[One paragraph — what is this and why does it matter]

## Content
[Main permanent knowledge — written to be useful months from now]

## Key Takeaways
- [Bullet points of most important facts]

## Links
[Related vault notes]

## References
[External sources, URLs, docs]
```
</step_2>

<step_3>
Update relevant MOC — check if a MOC in `30_Atlas/` should reference this new note. If yes, append a link using Edit tool.

Example: a research note on a lab tool → add it to the lab MOC in `30_Atlas/`
</step_3>

<step_4>
Confirm — state: filename created, any MOC updated.
</step_4>
</process>

<success_criteria>
- [ ] File in 40_Research/
- [ ] Content is permanent knowledge (not time-sensitive)
- [ ] Relevant MOC updated with link
- [ ] Valid YAML frontmatter
</success_criteria>
