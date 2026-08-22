<overview>
Optional registry of work that lives OUTSIDE the vault. The skill reads this so it
can reference external projects from vault notes without searching the filesystem.

**Ships empty on purpose.** Fill in your own, or delete this file and remove the
`<required_reading>` line from `workflows/update-project.md`.

Do not put secrets here — credentials, tokens, API keys. Store a *path* to the
secret, never the secret. This file is read into the model's context.
</overview>

<projects>

<example_project>
- **Vault stub:** `20_Projects/Area/Example.md`
- **External folder:** `~/code/example/`
- **Docs:** https://example.internal/docs
- **Status:** one line — what state is it in
- **Pending:** what is unfinished
</example_project>

</projects>

<shared_infrastructure>
Optional table for hosts/services referenced across many projects.

| Device | Address | Access | Role |
|---|---|---|---|
| | | | |
</shared_infrastructure>
