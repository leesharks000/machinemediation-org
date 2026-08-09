#!/usr/bin/env python3
"""build_data_index.py — generate /data/index.html for machinemediation.org.

WHY
The front page links to /data/ and describes it as "Data Directory — all
machine-readable data files". The path returned 404: Vercel serves static files,
and a directory with no index is not a page. The archive was advertising a
directory listing it did not have, which is the availability defect it exists to
document, committed on its own surface.

The index is generated from what is actually on disk, with sizes and a one-line
account of each file, so it cannot drift from the directory it describes. Re-run
after adding or removing anything under data/.
"""
import html, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"

NOTES = {
    "axn-index.json": "AXN identifier index, mirrored from alexanarch",
    "sovereign-registry.json": "Sovereign asset registry — machine-readable master index",
    "revfirst-registry.json": "Revelation First registry",
    "content-manifest.json": "Content store manifest",
    "blogspot-mirror-inventory.xml": "Blogspot mirror inventory",
    "TACHYON-CHAIN-RECONSTRUCTION.md": "Continuity chain reconstruction",
    "GIT-SAFETY-RULES.md": "Repository safety rules",
    "EA-MMRS-VRB-01.md": "MMRS verb specification",
    "EA-MMRS-LOUD-EXCLUSION-03.md": "Loud exclusion, third treatment",
}


def human(n):
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{n:,.0f} {unit}" if unit == "B" else f"{n / 1:.0f} {unit}"
        n /= 1024
    return f"{n:.0f} MB"


def size(n):
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.0f} KB"
    return f"{n / 1024 / 1024:.1f} MB"


def main():
    entries, dirs = [], []
    for p in sorted(DATA.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        if p.name.startswith(".") or p.name == "index.html":
            continue
        if p.is_dir():
            n = sum(1 for _ in p.rglob("*") if _.is_file())
            dirs.append((p.name, n))
        else:
            entries.append((p.name, p.stat().st_size, NOTES.get(p.name, "")))

    rows = "".join(
        f'<tr><td><a href="/data/{html.escape(n)}">{html.escape(n)}</a></td>'
        f'<td class="sz">{size(s)}</td><td class="note">{html.escape(note)}</td></tr>'
        for n, s, note in entries)
    drows = "".join(
        f'<tr><td><a href="/data/{html.escape(n)}/">{html.escape(n)}/</a></td>'
        f'<td class="sz">{c} file{"s" if c != 1 else ""}</td>'
        f'<td class="note">directory</td></tr>' for n, c in dirs)

    page = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Data Directory — Machine-Mediated Reception Studies</title>
<meta name="description" content="All machine-readable data files served by
machinemediation.org: {len(entries)} files and {len(dirs)} directories, listed with
sizes. Fetch anything here without an account.">
<style>
:root{{--bg:#0a0a0a;--fg:#e0ddd5;--accent:#c23b22;--accent2:#d4a537;--dim:#666;
--border:#1a1a1a;--mono:'IBM Plex Mono','Courier New',monospace}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--mono);background:var(--bg);color:var(--fg);line-height:1.6}}
.wrap{{max-width:820px;margin:0 auto;padding:40px 20px}}
h1{{font-size:1.2em;color:var(--accent);letter-spacing:.08em;text-transform:uppercase}}
.sub{{color:var(--dim);font-size:.82em;margin:6px 0 26px;line-height:1.6}}
a{{color:#a8bcd0;text-decoration:none;border-bottom:1px dotted var(--border)}}
a:hover{{color:var(--accent2)}}
table{{width:100%;border-collapse:collapse;font-size:.82em}}
td{{padding:6px 10px 6px 0;vertical-align:top;border-top:1px solid var(--border)}}
.sz{{color:var(--dim);white-space:nowrap;text-align:right}}
.note{{color:var(--dim)}}
h2{{font-size:.72em;text-transform:uppercase;letter-spacing:.12em;color:var(--dim);
margin:26px 0 4px;font-weight:400}}
.back{{margin-top:30px;font-size:.8em}}
</style></head><body><div class="wrap">
<h1>Data Directory</h1>
<p class="sub">All machine-readable data files served by machinemediation.org &mdash;
{len(entries)} file{"s" if len(entries) != 1 else ""} and {len(dirs)}
director{"ies" if len(dirs) != 1 else "y"}. Everything here is fetchable without an
account, a key, or a referrer. CORS is open on this path; copy what you need.</p>
<h2>Directories</h2><table><tbody>{drows}</tbody></table>
<h2>Files</h2><table><tbody>{rows}</tbody></table>
<p class="back"><a href="/">&larr; machinemediation.org</a></p>
</div></body></html>
"""
    (DATA / "index.html").write_text(page, encoding="utf-8")
    print(f"/data/index.html written: {len(entries)} files, {len(dirs)} directories")


if __name__ == "__main__":
    main()
