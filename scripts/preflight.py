import os, re, pathlib

cfg = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT", ".")) / "skills/obsidian-vault/references/vault-config.md"
if not cfg.is_file():
    print("STATUS=NO_CONFIG")
    raise SystemExit

m = re.search(r"<vault_root>\s*\n(.+?)\n\s*</vault_root>", cfg.read_text(), re.S)
root = (m.group(1).strip() if m else "")
if not root or root == "UNCONFIGURED":
    print("STATUS=UNCONFIGURED")
    raise SystemExit

p = pathlib.Path(root).expanduser()
if not p.is_dir():
    print(f"STATUS=BAD_ROOT ROOT={p}")
    raise SystemExit

db = p / "vault_index.db"
n = len([f for f in p.rglob("*.md") if ".obsidian" not in f.parts])
if not db.is_file():
    print(f"STATUS=NO_INDEX ROOT={p} MD_FILES={n}")
    raise SystemExit

print(f"STATUS=READY ROOT={p} MD_FILES={n}")
