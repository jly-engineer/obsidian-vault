<objective>
First-run setup. Get from "installed" to "working" in one exchange: find the vault,
confirm it, write the config, build the index, verify. Do not show the intake menu
and do not start the user's actual task until this completes.
</objective>

<process>

<step_1>
Check whether the Obsidian app itself is installed — the plugin only manages
files, it doesn't need Obsidian running, but a user with no Obsidian install
has nothing to open their vault with once this finishes:

```bash
command -v obsidian 2>/dev/null; command -v flatpak >/dev/null 2>&1 && flatpak list 2>/dev/null | grep -i obsidian; ls /Applications/Obsidian.app 2>/dev/null; find ~ -maxdepth 2 -iname 'Obsidian*.AppImage' 2>/dev/null
```

If nothing is found, tell the user once, then continue with vault detection —
don't block on it, and don't attempt to download or install anything
yourself (fetching and running an installer is a bigger ask than this skill's
job of managing notes). Offer the right platform instructions:

- **Linux:** download the AppImage from [obsidian.md](https://obsidian.md),
  then `chmod +x Obsidian-*.AppImage && ./Obsidian-*.AppImage`
  (or `flatpak install flathub md.obsidian.Obsidian`)
- **macOS:** download the `.dmg` from [obsidian.md](https://obsidian.md), drag
  to Applications
- **Windows:** download and run the installer from [obsidian.md](https://obsidian.md)

Detect candidate vaults — an Obsidian vault is any directory containing `.obsidian/`:

```bash
find ~ -maxdepth 5 -type d -name .obsidian -not -path '*/.*/*' 2>/dev/null | sed 's|/.obsidian$||'
```

Also check for an index built by a previous install, which points at a vault
even when `.obsidian/` is absent:

```bash
find ~ -maxdepth 5 -name vault_index.db 2>/dev/null | sed 's|/vault_index.db$||'
```
</step_1>

<step_2>
Confirm with the user — never auto-write a detected path.

- **One candidate:** "Found a vault at `<path>` — 84 markdown files. Use it?"
- **Several:** list them numbered with each one's markdown file count, ask which.
- **None:** don't ask where to put it — create it at a fixed, predictable
  default so there's no naming round-trip for the common "brand-new user"
  case: `~/Downloads/vault` (POSIX), `%USERPROFILE%\Downloads\vault`
  (Windows). Tell the user where it's going as you do it — "No existing
  vault found. Creating one at `~/Downloads/vault`." — this is a notice, not
  a question; don't wait for a reply before proceeding to step_3.
  (This is the one deliberate exception to "never auto-write a path": it
  only fires when detection found *nothing at all* to be wrong about — there
  is no existing vault this could clobber or misidentify.)

Report the file count so a wrong-but-existing directory is obvious:
```bash
find "<candidate>" -name '*.md' -not -path '*/.obsidian/*' | wc -l
```
A count of 0 almost always means the wrong directory. Say so and re-ask.

**Stop here and wait for the user's answer — except the None branch above,**
which proceeds on its own by design (nothing existing to misidentify). For
One and Several: detection produces a suggestion, never a decision. The
failure this guards against is quiet and expensive: pick
the wrong directory and the first note lands in a scratch folder or an abandoned
copy of the vault, and nothing about the run looks wrong until the user goes
hunting for that note weeks later. A real vault and a stale duplicate are
indistinguishable from the filesystem, so don't try to tell them apart — that
judgement is exactly what the user is here to supply.

Concretely: do not run step_3, do not write the config, and do not create, edit,
or append to any file anywhere until the user has named or confirmed a root —
or, for the None branch, until you've stated the fixed default path per above.
Working directory is a hint about what they're looking at, not consent.

If they don't answer, leaving the config `UNCONFIGURED` is the correct outcome.
An install that plainly isn't set up yet is easy to finish; one silently pointed
somewhere plausible is a bug the user has to discover.
</step_2>

<step_3>
Write the config — replace the `<vault_root>` line in
`references/vault-config.md`. Use Edit, replacing `UNCONFIGURED` with the
confirmed absolute path. Leave every other section alone.

If this is the None-branch fixed default and the directory doesn't exist yet,
create it first: `mkdir -p ~/Downloads/vault`. The index build in step_4 needs
somewhere to point at.
</step_3>

<step_4>
Build the index:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py" "<vault_root>"
```

Expected output:
```
vault_index.db — 84 notes total | +84 new | ~0 updated | 0 skipped | -0 removed
```

If the note total is 0 but step_2 counted markdown files, the vault root is wrong
by one level — check whether the notes are in a subdirectory and re-confirm.
</step_4>

<step_5>
Check the folder map — compare the vault's real top-level directories against the
`<folder_map>` table in `vault-config.md`:

```bash
ls -d "<vault_root>"/*/ 2>/dev/null | xargs -n1 basename
```

If the names differ from the defaults (`00_Inbox`, `10_Daily_Notes`, …), show the
user the mismatch and offer to rewrite the right-hand column to match their vault.
Do not silently keep defaults that do not exist — that is the same silent-failure
class as a stale vault root.

If the vault has no matching folders at all, ask whether to create the default set
or map to what is already there. Never create folders unprompted.

Offer the note templates: "Want the matching note templates (Standard / Daily /
Project) copied into `90_Templates/`?" If yes:
```bash
cp "${CLAUDE_PLUGIN_ROOT}"/templates/*.md "<vault_root>/90_Templates/"
```
Skip silently if the user says no — templates are optional, not required for
any workflow to function.
</step_5>

<step_6>
Ask what prompted the install — skip this step if the user's first message already
stated a concrete task (e.g. "log today's session"); run that task instead and do
not interrupt it with onboarding questions. Otherwise ask, in the user's own words:

"What made you want to set this vault up — what do you want it to help you organize?"

Do not lead with a multiple-choice list; let them answer freely. Then map the
answer to one or more Areas — the defaults are `Family`, `Business`, `Personal`,
`Health` (already routed in `<custom_routing>`), but a different area name the
user actually said is fine too. Multiple areas are normal: "I want to run my
freelance business and keep the household organized" is `Business` + `Family`.

For each Area selected:
- Create `30_Atlas/<Area> MOC.md` now (the index should exist even before content
  does), with empty `## Projects`, `## Research`, and `## Guides` sections and
  valid frontmatter (`type: moc`).
- Leave `20_Projects/<Area>/` uncreated — it comes into existence on the first
  real project write for that Area, per the vault's normal lazy-folder behavior.
- If the Area is not one of the four defaults, append a row to `<custom_routing>`
  in `vault-config.md`: `| <Area> projects | 20_Projects/<Area>/ |`.

Rebuild the index after writing the MOC(s):
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_vault_index.py" "<vault_root>"
```
</step_6>

<step_7>
Write a short getting-started note to `50_Guides/Vault Plugin - Getting Started.md`
(frontmatter `type: guide`) — this session's setup summary as something the user
can find again later instead of only living in scrollback: vault root, folder
map (as configured), Area(s) created, whether Obsidian itself was detected
(and the install link if not), and the command list from this plugin's README.
Skip it if that file already exists — first run only, don't overwrite.

Confirm and hand off — state the vault root, the indexed note count, any folder
map changes, and which Area(s) were established. Then continue to the user's
original request, or show the intake menu if they had not asked for anything yet.
</step_7>

</process>

<success_criteria>
- [ ] Obsidian app presence checked; install instructions offered if absent
- [ ] No file was created or edited before the user confirmed a root (or, for
      a fresh no-vault-found case, before the fixed default path was stated)
- [ ] Vault root confirmed by the user, never auto-written — except the
      documented None-branch default
- [ ] `vault-config.md` no longer contains UNCONFIGURED
- [ ] Index built, note count reported and non-zero
- [ ] Folder map verified against real directories
- [ ] User asked what prompted the install (unless a task was already in flight)
- [ ] Initial Area MOC(s) created from that answer, `custom_routing` updated for
      any non-default Area
- [ ] User's original task resumed, not dropped
</success_criteria>
