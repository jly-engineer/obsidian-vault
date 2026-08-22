<required_reading>
references/vault-config.md
references/vault-structure.md
</required_reading>

<process>
<step_1>
Confirm this is an implementation guide — guides (`50_Guides/`) are for actionable, procedural content:
- Step-by-step setup or installation instructions
- Update/upgrade runbooks
- Incident fix procedures
- How-to workflows (not just what something is — how to do it)

If it's conceptual reference (what something is, how it works) → use `40_Research/` instead.
If it's project-specific in-progress work → use `20_Projects/` instead.
</step_1>

<step_2>
Write the guide — file: `<vault_root>/50_Guides/[topic].md`

```markdown
---
tags: [relevant-tags]
created: YYYY-MM-DD
type: note
status: active
---

# [Guide Title]

## Summary
[One sentence — what this guide accomplishes and when to use it]

## Prerequisites
- [What must be true before starting]
- [Access, credentials, dependencies]

## Steps

### Step 1 — [Action]
[What to do and why]

```bash
# commands if applicable
```

### Step 2 — [Action]
[Continue...]

## Verification
[How to confirm the guide succeeded — expected output, test command, UI state]

## Rollback / Undo
[How to reverse this if something goes wrong — omit if not applicable]

## Notes
[Edge cases, gotchas, known issues]
```
</step_2>

<step_3>
Update relevant MOC — check if a MOC in `30_Atlas/` should reference this guide. If yes, append under the `## Guides (50_Guides)` section using Edit tool.

- Match the guide topic to an existing MOC (query `type='moc'`)
- No matching MOC → skip this step, do not create one
</step_3>

<step_4>
Confirm — state: filename created, any MOC updated.
</step_4>
</process>

<success_criteria>
- [ ] File in 50_Guides/
- [ ] Content is procedural/actionable (not just informative)
- [ ] Steps are ordered and unambiguous
- [ ] Relevant MOC updated with link
- [ ] Valid YAML frontmatter
</success_criteria>
