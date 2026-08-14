#!/usr/bin/env python3
"""sync_capture_mirror.py — pull the capture registry from canonical.

machinemediation.org is the ONLY fleet node that HOSTS the capture registry
rather than fetching it at render. leesharks.com and godkinggoogle.com are
renderers: they read https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json
directly and cannot drift. This node keeps a copy, and a copy without a refresh
path becomes a claim about the past presented identically to a claim about the
present — the atlas calls that PATHOLOGY-26/28.

It had drifted to v10.0 / 300 entries while canonical stood at v10.5 / 315, and
nothing reported it.

HOSTING IS DELIBERATE, not an oversight: the archive's own doctrine is that no
single custodian should control whether a work remains reachable, and a mirror
that fetches from alexanarch is a mirror that dies with alexanarch. So the copy
stays, and this script is the refresh path it lacked. Every sync stamps
`_mirror` with the source, the upstream version and the time, so a reader can
see how old the copy is without comparing it to anything.

    python3 scripts/sync_capture_mirror.py
"""
import json, pathlib, urllib.request, datetime, hashlib, sys

SRC = "https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json"
DEST = pathlib.Path(__file__).resolve().parents[1] / "data/registry.json"


def main():
    raw = urllib.request.urlopen(SRC, timeout=120).read()
    up = json.loads(raw)
    was = {}
    if DEST.exists():
        old = json.loads(DEST.read_text())
        was = {"version": old.get("version"), "entries": len(old.get("entries") or [])}
    up["_mirror"] = {
        "role": "HOSTED MIRROR. This file is a COPY. The canonical projection is at " + SRC +
                ", derived in turn from rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json in the "
                "alexanarch repository. Nothing here is written to; nothing downstream reads back into it.",
        "why_hosted": ("A mirror that fetches from the origin dies with the origin. This node holds bytes so the "
                       "registry survives the loss of alexanarch.org — which is the archive's own thesis applied "
                       "to itself."),
        "synced_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "upstream_version": up.get("version"),
        "upstream_entries": len(up.get("entries") or []),
        "upstream_sha256": hashlib.sha256(raw).hexdigest(),
        "previous_local": was,
        "refresh": "python3 scripts/sync_capture_mirror.py"}
    DEST.write_text(json.dumps(up, indent=1, ensure_ascii=False))
    print(f"synced  {was or '(no prior copy)'}  ->  v{up.get('version')} / {len(up['entries'])} entries")
    print(f"  sha256 {up['_mirror']['upstream_sha256'][:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
