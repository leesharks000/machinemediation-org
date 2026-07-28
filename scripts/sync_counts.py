#!/usr/bin/env python3
"""
sync_counts.py — rewrite every count on machinemediation.org from the dataset it
describes, in both the HTML and the JSON-LD.

WHY THIS EXISTS. On 2026-07-28 an accuracy audit found seven stale counts on the
home page, all hardcoded. The capture registry appeared three times with two
different values (176+ and 222) against an actual 225; the deposit count read
845+ against 1,412, understating the corpus by 40%. Alongside those, the
Sovereign Asset Registry was described as holding "full text" when it holds
bounded previews — 582,760 words against 3,479,635 declared.

The visible counts were then wired to their data files with data-count spans and
a fetch at page load. That fixed the HTML and left the JSON-LD, which cannot
carry a span: an element inside a JSON string breaks the block. So the page had
current numbers in the prose and stale ones in the structured data beside it —
the worse failure, because a machine consumer reads the block and a human reads
the prose, and they disagreed silently.

This script closes that. It reads each dataset, computes the count, and rewrites
BOTH surfaces from the same value, so the two cannot drift apart.

WHAT IT DOES NOT TOUCH. Historical figures. '862 deposits and 1,817 DOIs
destroyed' describes the Zenodo termination of 2026-06-19 and is fixed in time,
confirmed in Zenodotus' Book-Burning (EA-MMRS-LOUD-EXCLUSION-03, deposit #1,
v9.1 FINAL, Appendix C). A live count must never overwrite a historical one, and
those figures are listed in FROZEN below so a future edit cannot mistake them for
counts that need refreshing.

Usage: python3 scripts/sync_counts.py [--apply]
"""
import json, re, os, sys, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return None


def count_sources():
    """Return {label: (value, provenance)} read from the datasets themselves."""
    out = {}
    d = load('data/registry.json')
    if d: out['captures'] = (d.get('total_captures') or len(d.get('entries', [])),
                             'data/registry.json:total_captures')
    d = load('data/schemas.json')
    if d: out['schemas'] = (d.get('entries') if isinstance(d.get('entries'), int) else len(d.get('entries', [])),
                            'data/schemas.json:entries')
    d = load('data/sovereign-registry.json')
    if d:
        out['works'] = (len(d.get('assets', [])), 'data/sovereign-registry.json:assets')
        t = d.get('totals') or {}
        if t.get('declared_words'):
            out['declared_words'] = (t['declared_words'], 'data/sovereign-registry.json:totals.declared_words')
        if t.get('preview_words'):
            out['preview_words'] = (t['preview_words'], 'data/sovereign-registry.json:totals.preview_words')
    d = load('data/termindex.json')
    if d: out['terms'] = (d.get('entries') if isinstance(d.get('entries'), int) else len(d.get('entries', [])),
                          'data/termindex.json:entries')
    d = load('data/revfirst-registry.json')
    if d: out['revfirst'] = (d.get('entries') if isinstance(d.get('entries'), int) else len(d.get('entries', [])),
                             'data/revfirst-registry.json:entries')
    d = load('data/mint.json')
    if d:
        r = d.get('releases')
        out['releases'] = (len(r) if isinstance(r, list) else r, 'data/mint.json:releases')
    d = load('data/content-manifest.json')
    if d:
        out['chunks'] = (len(d.get('chunks', [])), 'data/content-manifest.json:chunks')
        if d.get('total_entries'): out['content_entries'] = (d['total_entries'], 'data/content-manifest.json:total_entries')
    return {k: v for k, v in out.items() if v[0]}


# Historical figures. Never rewritten from a live dataset.
FROZEN = {
    '862': 'deposits terminated by Zenodo 2026-06-19 (ZBB Appendix C)',
    '1,817': 'DOIs destroyed in the same action; also the DOI Resolution Index size at v3.0',
}

# label -> regexes matching where that count is printed. Each pattern must have the
# number as group 1 so it can be substituted without disturbing the surrounding text.
PATTERNS = {
    'captures':  [r'([\d][\d,]*)(\s*(?:\+)?\s*captures\b)'],
    'schemas':   [r'([\d][\d,]*)(\s*(?:prose\s+)?schemas\b)'],
    'works':     [r'([\d][\d,]*)(\s*works\b)'],
    'terms':     [r'([\d][\d,]*)(\s*(?:coined\s+)?terms\b)'],
    'revfirst':  [r'([\d][\d,]*)(\s*thesis-specific captures\b)'],
    'releases':  [r'([\d][\d,]*)(\s*releases\b)'],
}


def fmt(n):
    return format(int(n), ',')


def rewrite(text, counts, protect_frozen=True):
    changes = []
    for label, pats in PATTERNS.items():
        if label not in counts:
            continue
        val = fmt(counts[label][0])
        for pat in pats:
            def sub(m):
                if protect_frozen and m.group(1) in FROZEN:
                    return m.group(0)
                if m.group(1) == val:
                    return m.group(0)
                changes.append((label, m.group(1), val, m.group(0)[:48]))
                return val + m.group(2)
            text = re.sub(pat, sub, text)
    return text, changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()

    counts = count_sources()
    print("counts read from the datasets:")
    for k, (v, prov) in sorted(counts.items()):
        print("   %-16s %-10s  %s" % (k, fmt(v) if isinstance(v, int) else str(v)[:20], prov))
    print()

    path = os.path.join(ROOT, 'index.html')
    src = open(path, encoding='utf-8').read()
    out = src
    all_changes = []

    # 1. HTML prose, outside JSON-LD
    blocks = list(re.finditer(r'<script[^>]*application/ld\+json[^>]*>.*?</script>', out, re.S))
    spans = [(m.start(), m.end()) for m in blocks]
    pieces, last = [], 0
    for s0, e0 in spans:
        seg, ch = rewrite(out[last:s0], counts)
        pieces.append(seg); all_changes += [('html',) + c for c in ch]
        pieces.append(out[s0:e0]); last = e0
    seg, ch = rewrite(out[last:], counts)
    pieces.append(seg); all_changes += [('html',) + c for c in ch]
    out = ''.join(pieces)

    # 2. JSON-LD, parsed and rewritten field by field so the block stays valid
    def fix_block(m):
        raw = m.group(0)
        inner = re.search(r'>(.*)</script>', raw, re.S).group(1)
        try:
            doc = json.loads(inner)
        except Exception:
            return raw
        touched = []

        def walk(o):
            if isinstance(o, dict):
                for k, v in list(o.items()):
                    if isinstance(v, str):
                        nv, ch = rewrite(v, counts)
                        # the sovereign registry does not hold full text
                        nv = nv.replace('Full text, mirror status.',
                                        'Searchable previews, mirror status, sovereign record links.')
                        nv = nv.replace('full text, mirror status',
                                        'searchable previews, mirror status')
                        if nv != v:
                            o[k] = nv
                            touched.extend(ch)
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(doc)
        all_changes.extend([('json-ld',) + c for c in touched])
        return raw.replace(inner, json.dumps(doc, ensure_ascii=False, indent=1))

    out = re.sub(r'<script[^>]*application/ld\+json[^>]*>.*?</script>', fix_block, out, flags=re.S)

    for where, label, was, now, ctx in all_changes:
        print("  %-8s %-10s %-8s -> %-8s  %s" % (where, label, was, now, ctx))
    if not all_changes:
        print("  everything already matches its dataset.")
    print("\nchanges: %d" % len(all_changes))

    # validate before writing
    for b in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', out, re.S):
        json.loads(b)
    print("JSON-LD blocks valid after rewrite.")

    if a.apply:
        open(path, 'w', encoding='utf-8').write(out)
        print("[ok] wrote index.html")
    else:
        print("[dry-run] nothing written. re-run with --apply")


if __name__ == '__main__':
    main()
