import os, re, sys, pathlib

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

cfg = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT", ".")) / "skills/obsidian-vault/references/vault-config.md"
if not cfg.is_file():
    print("STATUS=NO_CONFIG")
    raise SystemExit

m = re.search(r"<vault_root>\s*\n(.+?)\n\s*</vault_root>", cfg.read_text(), re.S)
root = (m.group(1).strip() if m else "")
if not root or root == "UNCONFIGURED":
    print("STATUS=UNCONFIGURED")
    guide = pathlib.Path.home() / "Downloads" / "obsidian-vault-guide.html"
    if not guide.is_file():
        sys.path.insert(0, str(SCRIPT_DIR))
        import write_guide
        write_guide.write_and_open("not yet configured", "UNCONFIGURED", guide)
    print(f"GUIDE={guide}")
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
