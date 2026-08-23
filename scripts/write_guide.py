import platform
import shutil
import subprocess
import sys
from pathlib import Path

GUIDE_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Obsidian Vault Plugin — Getting Started</title>
<style>
  :root {{
    --bg: #f7f6f3; --fg: #1c1b1a; --muted: #5c5a56; --card: #ffffff;
    --border: #e3e1dc; --accent: #6d4aff; --code-bg: #f0eef9;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #17161a; --fg: #ececec; --muted: #a6a3ab; --card: #201f24;
      --border: #322f37; --accent: #a996ff; --code-bg: #26232d;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 2.5rem 1.25rem 4rem; background: var(--bg); color: var(--fg);
    font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  main {{ max-width: 720px; margin: 0 auto; }}
  h1 {{ font-size: 1.6rem; margin-bottom: .25rem; }}
  h2 {{ font-size: 1.15rem; margin-top: 2.5rem; border-bottom: 1px solid var(--border); padding-bottom: .4rem; }}
  .sub {{ color: var(--muted); margin-top: 0; }}
  .card {{
    background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 1.1rem 1.3rem; margin: 1rem 0;
  }}
  .os-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: .9rem; }}
  .os-card h3 {{ margin: 0 0 .4rem; font-size: 1rem; }}
  code, pre {{
    background: var(--code-bg); border-radius: 6px; font-family: ui-monospace, Menlo, Consolas, monospace;
    font-size: .85rem;
  }}
  code {{ padding: .15rem .35rem; }}
  pre {{ padding: .7rem .9rem; overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: .5rem; }}
  th, td {{ text-align: left; padding: .5rem .6rem; border-bottom: 1px solid var(--border); font-size: .92rem; }}
  th {{ color: var(--muted); font-weight: 600; }}
  a {{ color: var(--accent); }}
  .status {{ display: inline-block; padding: .2rem .6rem; border-radius: 999px; font-size: .8rem;
    background: var(--code-bg); color: var(--accent); font-weight: 600; }}
  footer {{ margin-top: 3rem; color: var(--muted); font-size: .85rem; }}
</style>
</head>
<body>
<main>
  <h1>Obsidian Vault Plugin</h1>
  <p class="sub">Getting started — generated on first run. <span class="status">{status_label}</span></p>

  <div class="card">
    <strong>What this is:</strong> a Claude Code skill that manages notes inside an
    <em>existing</em> Obsidian vault — capture, log sessions, project notes, research,
    guides, and a searchable index. It does not replace Obsidian; it reads and writes
    the same plain markdown files Obsidian shows you.
  </div>

  <h2>1. Install Obsidian</h2>
  <p>Skip this if you already have it. Obsidian doesn't need to be running for the
  plugin to work — it just needs to exist so you have something to open your notes with.</p>
  <div class="os-grid">
    <div class="card os-card">
      <h3>Linux</h3>
      <p>Download the AppImage from <a href="https://obsidian.md">obsidian.md</a>, then:</p>
      <pre>chmod +x Obsidian-*.AppImage
./Obsidian-*.AppImage</pre>
      <p>Or: <code>flatpak install flathub md.obsidian.Obsidian</code></p>
    </div>
    <div class="card os-card">
      <h3>macOS</h3>
      <p>Download the <code>.dmg</code> from <a href="https://obsidian.md">obsidian.md</a>,
      open it, drag Obsidian into Applications.</p>
    </div>
    <div class="card os-card">
      <h3>Windows</h3>
      <p>Download and run the installer from <a href="https://obsidian.md">obsidian.md</a>.</p>
    </div>
  </div>
  <p>Then in Obsidian: <strong>File → Open folder as vault</strong>, or create a new
  vault, pointed at <code>{vault_root}</code> — that's the folder this plugin is
  configured to manage.</p>

  <h2>2. Basic interactive tools</h2>
  <p>Everything below runs as <code>/vault &lt;command&gt;</code> in Claude Code (or
  <code>/obsidian-vault:vault …</code> if you also have another plugin using
  <code>/vault</code>). Bare <code>/vault</code> shows a numbered menu.</p>
  <table>
    <tr><th>Command</th><th>What it does</th></tr>
    <tr><td><code>log session</code></td><td>Appends today's work to the daily note and touched project stubs</td></tr>
    <tr><td><code>capture &lt;idea&gt;</code></td><td>Quick note into the Inbox, verbatim</td></tr>
    <tr><td><code>update project &lt;name&gt;</code></td><td>Finds and surgically updates a project stub</td></tr>
    <tr><td><code>create note &lt;title&gt;</code></td><td>New note, routed to the right folder</td></tr>
    <tr><td><code>research &lt;topic&gt;</code></td><td>Permanent note, linked into its Map of Content</td></tr>
    <tr><td><code>guide &lt;topic&gt;</code></td><td>Runbook with steps, verification, rollback</td></tr>
    <tr><td><code>update moc &lt;name&gt;</code></td><td>Adds links to a Map of Content</td></tr>
    <tr><td><code>find &lt;term&gt;</code></td><td>Full-text search across the vault</td></tr>
  </table>

  <h2>3. Permissions</h2>
  <p>The skill uses <code>Bash</code> (index build/query), <code>Read</code>,
  <code>Write</code> (new notes only), and <code>Edit</code> (surgical updates) —
  no network access, nothing outside the vault root. Auto-approving these four for
  your first setup session is the smoothest path; "ask each time" is fine day-to-day.</p>

  <footer>
    Vault root on this machine: <code>{vault_root}</code><br>
    <a href="https://github.com/jly-engineer/obsidian-vault">github.com/jly-engineer/obsidian-vault</a>
  </footer>
</main>
</body>
</html>
"""


def write_and_open(vault_root: str, status_label: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(GUIDE_HTML.format(vault_root=vault_root, status_label=status_label))

    system = platform.system()
    opener = None
    if system == "Linux" and shutil.which("xdg-open"):
        opener = ["xdg-open", str(out_path)]
    elif system == "Darwin":
        opener = ["open", str(out_path)]
    elif system == "Windows":
        opener = ["cmd", "/c", "start", "", str(out_path)]

    if opener:
        try:
            subprocess.Popen(opener, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            pass  # no display / no opener available — path is still printed by the caller


if __name__ == "__main__":
    vault_root = sys.argv[1] if len(sys.argv) > 1 else "not yet configured"
    status_label = sys.argv[2] if len(sys.argv) > 2 else "UNCONFIGURED"
    out = Path.home() / "Downloads" / "obsidian-vault-guide.html"
    write_and_open(vault_root, status_label, out)
    print(f"GUIDE={out}")
