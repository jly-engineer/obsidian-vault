#!/usr/bin/env python3
"""
Vault index builder — creates/refreshes vault_index.db at the vault root.
Parses YAML frontmatter + extracts title/preview for each note.
Run: python3 build_vault_index.py [vault_root]
     vault_root defaults to $OBSIDIAN_VAULT, then ~/Documents/Vault
"""

import sqlite3
import os
import re
import sys
from datetime import datetime
from pathlib import Path

VAULT_ROOT = Path(
    sys.argv[1] if len(sys.argv) > 1
    else os.environ.get("OBSIDIAN_VAULT", str(Path.home() / "Documents" / "Vault"))
).expanduser()
DB_PATH = VAULT_ROOT / "vault_index.db"

SKIP_DIRS = {".obsidian", ".git", "90_Templates", "Excalidraw", ".claude"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
YAML_FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)
YAML_LIST_RE = re.compile(r"^\[(.+)\]$")
MARKDOWN_CLEAN_RE = re.compile(r"[#*`\[\]_>|]+")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end():]
    fields = {}
    for line in raw.splitlines():
        fm = YAML_FIELD_RE.match(line.strip())
        if not fm:
            continue
        key, val = fm.group(1), fm.group(2).strip()
        lm = YAML_LIST_RE.match(val)
        if lm:
            fields[key] = ",".join(v.strip() for v in lm.group(1).split(","))
        else:
            fields[key] = val
    return fields, body


def extract_title(body: str, stem: str) -> str:
    m = H1_RE.search(body)
    if m:
        return m.group(1).strip()
    return stem


def extract_preview(body: str, length: int = 300) -> str:
    lines = [l for l in body.splitlines() if l.strip() and not l.startswith("#")]
    raw = " ".join(lines)
    cleaned = MARKDOWN_CLEAN_RE.sub(" ", raw)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:length]


def get_folders(rel_path: str) -> tuple[str, str]:
    parts = Path(rel_path).parts
    folder = parts[0] if parts else ""
    subfolder = parts[1] if len(parts) > 2 else ""
    return folder, subfolder


def init_db(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS notes (
            path        TEXT PRIMARY KEY,
            title       TEXT,
            folder      TEXT,
            subfolder   TEXT,
            type        TEXT,
            status      TEXT,
            tags        TEXT,
            created     TEXT,
            preview     TEXT,
            updated_at  TEXT
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
            title, tags, preview,
            content=notes,
            content_rowid=rowid
        );

        CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
            INSERT INTO notes_fts(rowid, title, tags, preview)
            VALUES (new.rowid, new.title, new.tags, new.preview);
        END;

        CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
            INSERT INTO notes_fts(notes_fts, rowid, title, tags, preview)
            VALUES ('delete', old.rowid, old.title, old.tags, old.preview);
        END;

        CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
            INSERT INTO notes_fts(notes_fts, rowid, title, tags, preview)
            VALUES ('delete', old.rowid, old.title, old.tags, old.preview);
            INSERT INTO notes_fts(rowid, title, tags, preview)
            VALUES (new.rowid, new.title, new.tags, new.preview);
        END;
    """)
    conn.commit()


def scan_vault(conn: sqlite3.Connection):
    inserted = updated = skipped = 0

    existing = {
        row[0]: row[1]
        for row in conn.execute("SELECT path, updated_at FROM notes")
    }

    found_paths = set()

    for md_file in VAULT_ROOT.rglob("*.md"):
        rel = md_file.relative_to(VAULT_ROOT)
        parts = rel.parts

        if any(p in SKIP_DIRS for p in parts):
            continue

        rel_str = str(rel)
        found_paths.add(rel_str)
        mtime = datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(timespec="seconds")

        if existing.get(rel_str) == mtime:
            skipped += 1
            continue

        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        fm, body = parse_frontmatter(text)
        title = extract_title(body, md_file.stem)
        preview = extract_preview(body)
        folder, subfolder = get_folders(rel_str)
        tags = fm.get("tags", "")
        note_type = fm.get("type", "")
        status = fm.get("status", "")
        created = fm.get("created", fm.get("date", ""))

        conn.execute("""
            INSERT INTO notes (path, title, folder, subfolder, type, status, tags, created, preview, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET
                title=excluded.title, folder=excluded.folder, subfolder=excluded.subfolder,
                type=excluded.type, status=excluded.status, tags=excluded.tags,
                created=excluded.created, preview=excluded.preview, updated_at=excluded.updated_at
        """, (rel_str, title, folder, subfolder, note_type, status, tags, created, preview, mtime))

        if rel_str in existing:
            updated += 1
        else:
            inserted += 1

    # Remove deleted notes
    removed = 0
    for path in set(existing) - found_paths:
        conn.execute("DELETE FROM notes WHERE path=?", (path,))
        removed += 1

    conn.commit()
    return inserted, updated, skipped, removed


def main():
    if not VAULT_ROOT.is_dir():
        sys.exit(f"vault root not found: {VAULT_ROOT}\n"
                 f"pass it as an argument: python3 build_vault_index.py ~/path/to/vault")
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    ins, upd, skp, rem = scan_vault(conn)
    total = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    conn.close()
    print(f"vault_index.db — {total} notes total | +{ins} new | ~{upd} updated | {skp} skipped | -{rem} removed")


if __name__ == "__main__":
    main()
