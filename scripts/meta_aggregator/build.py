"""Render the MMRS meta-aggregator draft (census schema v2): index with traversal table + one page per aggregator.
Each page carries two nodes: the MMRS record (ours) and the entity it describes (theirs)."""
import json, html, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from articles import ARTICLES
CENSUS = ROOT / "data/meta-aggregator/census.json"
D = json.load(open(CENSUS)); ROWS = D["rows"]; BY = {r["slug"]: r for r in ROWS}
OUT = ROOT / "aggregators"; BASE = "https://www.machinemediation.org/aggregators/"
e = lambda s: html.escape(str(s), quote=True)
BASIS = {"operator": ("op", "operator statement"), "third-party": ("3p", "third-party report"), "observed": ("obs", "our observation"), "reading": ("rd", "our reading")}
REL = {"part_of": "Part of", "has_part": "Has part", "holding": "Holdings in scope", "merge_example": "Merge on record", "data_dump": "Data dump",
       "replacement_by_operator": "Replacement named at the sunset", "claimed_successor": "Claimed successor", "revival": "Revival", "neighbour": "Neighbours in the basin", "used_by": "Used by", "derived_from": "Derived from", "claims_succession_to": "Claims succession to", "capture": "Captures: the composition layer's account", "revives": "Revives"}
PROPS = [("admission_requires_harm", "Admission requires harm?"), ("preserves_original_outputs", "Preserves original outputs?"), ("version_history", "Version history?"), ("records_attribution", "Records attribution?")]
CSS = open(HERE / "style.css").read()
def kernel(r):
    if r["slug"] in ARTICLES: return ARTICLES[r["slug"]]["kernel"]
    return f'{r["name"]} is a {r["kind"]} run by {r["operator"]}.' + (f' Unit: {r["unit"]}.' if r.get("unit") else "")
def life(r):
    L = r["lifecycle"]; return L["state"] + (f' ({L["detail"]})' if L.get("detail") else "")
def chips(r):
    st = r["lifecycle"]["state"]; c = {"ended": "dead", "active": "live"}.get(st, "")
    return '<div class="chips">' + f'<span class="chip">{e(r["kind"])}</span>' + "".join(f'<span class="chip">{e(x)}</span>' for x in r["roles"]) + f'<span class="chip {c}">{e(st)}</span></div>'
def link(slug):
    r = BY.get(slug); return f'<a href="../{slug}/">{e(r["name"])}</a>' if r else e(slug)
def bchip(r, f):
    v = r.get("evidence", {}).get(f)
    if not v: return ""
    s = r["sources"].get(v["src"]) if v.get("src") else None; ab, full = BASIS[v["basis"]]
    t = f'<span class="b" title="{e(full)}">{ab}</span>'
    return f' <a class="bl" href="{e(s["url"])}">{t}</a>' if s else " " + t
def jsonld(r):
    rec, ent = BASE + r["slug"] + "/", BASE + r["slug"] + "/#entity"
    sch = {"database": "Dataset", "monitor": "Dataset", "audit series": "CreativeWorkSeries", "curated list": "CreativeWork", "leaderboard": "Dataset"}.get(r["kind"], "CreativeWork")
    entity = {"@id": ent, "@type": [sch, "spxi:IndexedEntity"], "name": r["name"], "alternateName": r.get("aka", []), "url": r["url"], "sameAs": [r["url"]],
              "creator": {"@type": "Organization", "name": r["operator"]}, "spxi:canonicalName": r["name"], "spxi:entityType": r["kind"], "spxi:roles": r["roles"],
              "spxi:lifecycle": r["lifecycle"], "spxi:negativeTag": r.get("negative_tags", []),
              "spxi:collisionNeighbour": [BASE + n["neighbour"] + "/#entity" if n.get("neighbour") else n.get("label") for n in r.get("disambiguation", []) if not n.get("self")]}
    if r.get("self_description"): entity["description"] = r["self_description"]
    if r.get("founded"): entity["foundingDate"] = r["founded"]
    for x in r["relations"]:
        if x["rel"] == "part_of": entity["isPartOf"] = {"@id": BASE + x["target"] + "/#entity"}
    record = {"@id": rec, "@type": "WebPage", "name": f'{r["name"]} — MMRS meta-aggregator record', "mainEntity": {"@id": ent}, "about": {"@id": ent},
              "abstract": kernel(r), "spxi:compressionSurvivalSummary": kernel(r), "dateCreated": D["compiled"], "dateModified": D["compiled"],
              "publisher": {"@type": "Organization", "name": "Machine-Mediated Reception Studies", "url": "https://www.machinemediation.org/"},
              "editor": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
              "isPartOf": {"@type": "Dataset", "name": "MMRS meta-aggregator", "url": BASE},
              "citation": [s["url"] for s in r["sources"].values()],
              "spxi:assertion": [{"field": f, "source": r["sources"][v["src"]]["url"] if v.get("src") in r["sources"] else None, "basis": BASIS[v["basis"]][1],
                                  "dateRead": r["sources"][v["src"]]["read"] if v.get("src") in r["sources"] else None} for f, v in r.get("evidence", {}).items()],
              "spxi:observation": r["observed"]}
    return json.dumps({"@context": {"@vocab": "https://schema.org/", "spxi": "https://spxi.dev/vocabulary#"}, "@graph": [record, entity]}, ensure_ascii=False, indent=1).replace("</", "<\\/")
def page(r):
    F = [("name", "Canonical name", r["name"]), ("aka", "Also known as", ", ".join(r.get("aka", []))), ("url", "Address", f'<a href="{e(r["url"])}">{e(r["url"])}</a>'),
         ("operator", "Operator", e(r["operator"])), ("founded", "Founded", e(r.get("founded") or "")), ("kind", "Kind", e(r["kind"])), ("roles", "Roles", e(", ".join(r["roles"]))),
         ("lifecycle", "Lifecycle", e(life(r))), ("observed", "Observation", e(f'{r["observed"]["on"]}: {r["observed"]["fetch"]}')),
         ("self_description", "In its own words", f'“{e(r["self_description"])}”' if r.get("self_description") else ""), ("unit", "Unit", e(r.get("unit") or "")),
         ("intake", "Intake", e(r.get("intake") or "")), ("item_fields", "What it records per item", e("; ".join(r.get("item_fields", [])))),
         ("count", "Count", f'{e(r["count"]["value"])} <span class="d">(as of {e(r["count"]["as_of"])})</span>' if r.get("count") else ""),
         ("cadence", "Cadence", e(r.get("cadence") or "")), ("data_access", "Data access", e(r.get("data_access") or "")), ("license", "Licence", e(r.get("license") or "")),
         ("note", "Note", e(r.get("note") or "")), ("identifiers", "Identifiers", e("; ".join(f"{k}: {v}" for k, v in r.get("identifiers", {}).items())))]
    tbl = "".join(f'<tr><td>{k}</td><td>{v}{bchip(r, f)}</td></tr>' for f, k, v in F if v)
    art = ARTICLES.get(r["slug"])
    body = "".join(f'<h2>{e(h)}</h2>' + "".join(f"<p>{e(p)}</p>" for p in ps) for h, ps in art["sections"]) if art else '<h2>Article</h2><p class="pend">Article pending: the fields above are read and sourced; the reading is not yet written.</p>'
    rels = list(r["relations"]) + [{"rel": "has_part", "target": x["slug"]} for x in ROWS if any(y["rel"] == "part_of" and y.get("target") == r["slug"] for y in x["relations"])]
    groups = {}
    for x in rels: groups.setdefault(x["rel"], []).append(x)
    def item(x):
        if x.get("target"): return f'<li>{link(x["target"])}' + (f'<div class="d">{e(x["note"])}</div>' if x.get("note") else "") + "</li>"
        lab = f'<a href="{e(x["url"])}">{e(x["label"])}</a>' if x.get("url") else e(x["label"])
        dt = x.get("dates"); dts = " · ".join(f"{k} {v}" for k, v in (dt or {}).items() if v)
        return f'<li>{lab}<div class="d">{e(x.get("note") or "")}{(" · " + e(dts)) if dts else ""}</div></li>'
    relhtml = "".join(f'<h3>{REL[k]}</h3><ul>{"".join(item(x) for x in v)}</ul>' for k, v in groups.items())
    props = "".join(f'<tr><td>{q}</td><td>{e(r["properties"][k]["value"])} <span class="b">{BASIS[r["properties"][k]["basis"]][0]}</span></td></tr>' for k, q in PROPS if k in r.get("properties", {}))
    dis = "".join(f'<tr><td>{"this entity" if n.get("self") else (link(n["neighbour"]) if n.get("neighbour") else e(n["label"]))}</td><td>{e(n["context"])}</td></tr>' for n in r.get("disambiguation", []))
    neg = "".join(f"<li>{e(t)}</li>" for t in r.get("negative_tags", []))
    bat = r.get("battery")
    bath = f'<h2>Reception battery</h2><p class="d" style="font-size:.74em">{e(bat["status"])}</p><h3>Queries</h3><ul>{"".join(f"<li>{e(q)}</li>" for q in bat["queries"])}</ul><h3>Checks</h3><ul>{"".join(f"<li>{e(c)}</li>" for c in bat["checks"])}</ul>' if bat else ""
    src = "".join(f'<li><a href="{e(s["url"])}">{e(s["url"])}</a><div class="d">read {e(s["read"])} · {e(s["for"])}</div></li>' for s in r["sources"].values())
    unc = "".join(f"<li>{e(u)}</li>" for u in r.get("unchecked", []))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(r["name"])} — MMRS meta-aggregator</title><meta name="description" content="{e(kernel(r))}"><link rel="canonical" href="{BASE}{r["slug"]}/">
<script type="application/ld+json">{jsonld(r)}</script><style>{CSS}</style></head><body><div class="wrap">
<div class="crumb"><a href="../">MMRS meta-aggregator</a> / {e(r["kind"])}</div><h1>{e(r["name"])}</h1>{chips(r)}<div class="kernel">{e(kernel(r))}</div>
<h2>Entity</h2><table>{tbl}</table><p class="d" style="font-size:.66em;margin-top:6px">op operator statement · 3p third-party report · obs our observation · rd our reading</p>
<div class="art">{body}</div>{f'<h2>For a research question</h2><table>{props}</table>' if props else ''}
<h2>Relations</h2>{relhtml or '<p class="pend">None recorded yet.</p>'}
{f'<h2>Disambiguation</h2><table>{dis}</table>' if dis else ''}{f'<h2>Negative tags</h2><ul>{neg}</ul>' if neg else ''}{bath}
<h2>Provenance</h2><ul>{src}</ul>{f'<h2>Not yet checked</h2><ul>{unc}</ul>' if unc else ''}
<div class="foot">Editor: Lee Sharks (<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>). This page is the MMRS record of the entity above: its reading, fields and relations are MMRS's, and each field carries its source and basis. Record {BASE}{r["slug"]}/ · entity {BASE}{r["slug"]}/#entity · compiled {D["compiled"]}</div></div></body></html>"""
def cand_html():
    C = D.get("candidates") or []
    if not C: return ""
    li = ""
    for c in C:
        nm = f'<a href="{e(c["url"])}">{e(c["name"])}</a>' if c.get("url") else e(c["name"])
        li += f'<li>{nm}<div class="d">{e(c["note"])} · surfaced by <a href="https://www.alexanarch.org/captures/{e(c["surfaced_by"])}/">{e(c["surfaced_by"])}</a></div></li>'
    return f'<h2>Candidates</h2><p class="d" style="font-size:.74em;margin-bottom:8px">{e(D.get("candidates_note", ""))}</p><ul>{li}</ul>'
def index():
    roles = sorted({x for r in ROWS for x in r["roles"]}); kinds = sorted({r["kind"] for r in ROWS})
    top = [r for r in sorted(ROWS, key=lambda r: r["name"].lower()) if not any(x["rel"] == "part_of" for x in r["relations"])]
    rows = "".join(f'<div class="row" data-roles="{e(" ".join(r["roles"]))}" data-kind="{e(r["kind"])}"><div class="n"><a href="{r["slug"]}/">{e(r["name"])}</a></div>{chips(r)}<div class="k">{e(kernel(r))}</div></div>' for r in top)
    btn = lambda key, vals: "".join(f'<button data-{key}="{e(v)}">{e(v)}</button>' for v in vals)
    cell = lambda r, k: f'<span title="{e(r["properties"][k]["value"])}">{e(r["properties"][k]["short"])}</span>' if k in r.get("properties", {}) else '<span class="d">·</span>'
    cand = cand_html()
    trav = "".join(f'<tr><td><a href="{r["slug"]}/">{e(r["name"])}</a></td>' + "".join(f"<td>{cell(r, k)}</td>" for k, _ in PROPS) + "</tr>" for r in sorted(ROWS, key=lambda r: r["name"].lower()))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MMRS meta-aggregator</title><link rel="canonical" href="{BASE}"><style>{CSS}</style></head><body><div class="wrap">\n<div class="crumb"><a href="/">Machine-Mediated Reception Studies</a> / aggregators</div><h1>MMRS meta-aggregator</h1><div class="kernel">The aggregators of machine-mediated reception work, each formalized as an entity: what it is in its own words, who runs it, what it admits and in what unit, what it leaves out, and where its record goes when it ends. {len(ROWS)} aggregators, compiled {D["compiled"]}.</div>
<div class="f"><button class="on" data-all="1">all</button>{btn("role", roles)}</div><div class="f">{btn("kind", kinds)}</div><div id="L">{rows}</div>
{cand}<h2>Traverse by question</h2><div class="tw"><table class="tv"><tr><td></td>{"".join(f"<td>{q}</td>" for _, q in PROPS)}</tr>{trav}</table></div><p class="d" style="font-size:.66em;margin-top:6px">· not yet read</p>
<div class="foot">Machine-Mediated Reception Studies · machinemediation.org · editor Lee Sharks (<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>)</div></div>
<script>let fs={{}};document.querySelectorAll('.f button').forEach(b=>b.onclick=()=>{{if(b.dataset.all){{fs={{}}}}else{{const k=b.dataset.role?'role':'kind',v=b.dataset[k];fs[k]=fs[k]===v?undefined:v}}document.querySelectorAll('.f button').forEach(x=>{{const k=x.dataset.role?'role':x.dataset.kind?'kind':'all';x.classList.toggle('on',k==='all'?!fs.role&&!fs.kind:fs[k]===x.dataset[k])}});document.querySelectorAll('#L .row').forEach(r=>r.style.display=(!fs.role||r.dataset.roles.split(' ').includes(fs.role))&&(!fs.kind||r.dataset.kind===fs.kind)?'':'none')}})</script></body></html>"""
def front_block():
    top = [r for r in sorted(ROWS, key=lambda r: r["name"].lower()) if not any(x["rel"] == "part_of" for x in r["relations"])]
    li = "".join(f'<li><a href="/aggregators/{r["slug"]}/">{e(r["name"])}</a> <span class="link-desc">— {e(r["kind"])} · {e(", ".join(r["roles"]))}{" · ended" if r["lifecycle"]["state"] == "ended" else ""}</span></li>' for r in top)
    return ("<!-- META-AGGREGATOR-START (generated by scripts/meta_aggregator/build.py from data/meta-aggregator/census.json) -->\n"
            '<div class="section"><div class="section-title">MMRS meta-aggregator</div>'
            f'<p class="plain">The aggregators of machine-mediated reception work, each formalized as an entity: what it is in its own words, who runs it, what it admits and in what unit, what it leaves out, and where its record goes when it ends. {len(ROWS)} aggregators, every field sourced and dated; compiled {D["compiled"]}.</p>'
            f'<ul class="link-list">{li}</ul><p class="plain" style="margin-top:10px"><a href="/aggregators/">All {len(ROWS)}, with the traversal table by research question</a> · <a href="/data/meta-aggregator/census.json">the census as data</a></p></div>\n'
            '<div class="section-title" style="margin:34px 0 14px">Machine-Mediated Reception Studies — the journal</div>\n<!-- META-AGGREGATOR-END -->')
def splice(path, start, end, block, anchor):
    t = path.read_text(encoding="utf-8")
    if start in t: t = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: block, t, count=1, flags=re.S)
    else:
        assert anchor in t, anchor; t = t.replace(anchor, block + "\n" + anchor, 1)
    path.write_text(t, encoding="utf-8")
OUT.mkdir(exist_ok=True); (OUT / "index.html").write_text(index())
for r in ROWS:
    p = OUT / r["slug"]; p.mkdir(exist_ok=True); (p / "index.html").write_text(page(r))
splice(ROOT / "index.html", "<!-- META-AGGREGATOR-START", "<!-- META-AGGREGATOR-END -->", front_block(), "<!-- INSTRUMENT CARDS -->")
llms = ("<!-- META-AGGREGATOR-START -->\n## MMRS meta-aggregator\n\nThe aggregators of machine-mediated reception work, each formalized as an entity with sourced, dated fields: "
        "https://www.machinemediation.org/aggregators/ (census as data: https://www.machinemediation.org/data/meta-aggregator/census.json)\n\n"
        + "".join(f'- {r["name"]} ({r["kind"]}; {", ".join(r["roles"])}; {r["lifecycle"]["state"]}): {BASE}{r["slug"]}/\n' for r in sorted(ROWS, key=lambda r: r["name"].lower()))
        + "<!-- META-AGGREGATOR-END -->\n")
lp = ROOT / "llms.txt"; lt = lp.read_text(encoding="utf-8")
if "<!-- META-AGGREGATOR-START -->" in lt: lt = re.sub(r"<!-- META-AGGREGATOR-START -->.*?<!-- META-AGGREGATOR-END -->\n", lambda m: llms, lt, flags=re.S)
else: lt = lt.replace("\n## The condition", "\n" + llms + "\n## The condition", 1)
lp.write_text(lt, encoding="utf-8")
sm = ROOT / "sitemap.xml"; st = sm.read_text(encoding="utf-8")
add = "".join(f'  <url><loc>{u}</loc><lastmod>{D["compiled"]}</lastmod><priority>0.7</priority></url>\n' for u in [BASE] + [BASE + r["slug"] + "/" for r in ROWS] if f"<loc>{u}</loc>" not in st)
sm.write_text(st.replace("</urlset>", add + "</urlset>"), encoding="utf-8")
print(len(ROWS), "pages")
