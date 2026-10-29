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
       "replacement_by_operator": "Replacement named at the sunset", "claimed_successor": "Claimed successor", "revival": "Revival", "neighbour": "Neighbours in the basin", "used_by": "Used by", "derived_from": "Derived from", "claims_succession_to": "Claims succession to", "capture": "Captures: the composition layer's account", "revives": "Revives", "non_row": "The /non row", "sibling": "Sibling"}
PROPS = [("admission_requires_harm", "Admission requires harm?"), ("preserves_original_outputs", "Preserves original outputs?"), ("version_history", "Version history?"), ("records_attribution", "Records attribution?")]
CSS = open(HERE / "style.css").read()
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">')
HEAD = FONTS + '<link rel="stylesheet" href="/assets/mmrs.css">'
NAV = [("Aggregators", "/aggregators/"), ("Captures", "/captures/"), ("Registry", "/registry/"), ("Terms", "/terms/"), ("Schemas", "/schemas/")]
def topbar(on=""):
    """The MMRS top bar, shared by the meta-aggregator pages and the landing page (spliced there between MMRS-TOPBAR markers).
    Search runs over the aggregators: the index reads ?q= and filters its cards."""
    nav = "".join(f'<a class="{"on" if n == on else ""}" href="{u}">{n}</a>' for n, u in NAV)
    return (f'<header class="top"><div class="in"><a class="wm" href="/"><i></i>MMRS</a><nav class="nav-top">{nav}</nav><div class="sp"></div>'
            f'<form class="srch" action="/aggregators/" method="get" role="search"><input name="q" type="search" placeholder="Search {len(ROWS)} aggregators" aria-label="Search the aggregators"></form>'
            '</div></header>')
def fold(title, inner, n=None, desc="", open_=False):
    """A collapsed section: the title stays visible, the depth opens on a tap; the content is in the page either way."""
    if not inner: return ""
    return (f'<details class="sec"{" open" if open_ else ""}><summary><span class="st">{title}</span><span class="sd">{desc}</span>'
            + (f'<span class="sn">{n}</span>' if n else "") + f'</summary><div class="body">{inner}</div></details>')
SVG = lambda d: f'<svg viewBox="0 0 32 32" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
FLOW = [  # the five questions of the meta-aggregator's own sentence, each with the fields that answer it
    ("words", "In its own words", "what it is", '<path d="M7 8h18v12H14l-5 4v-4H7z"/><path d="M11 13h10M11 16.5h6"/>',
     "What it is <b>in its own words</b>: its self-description, quoted from its own pages, with the source and the date read. MMRS's reading of it is written apart, as the article."),
    ("runs", "Who runs it", "the operator", '<circle cx="16" cy="11" r="4.5"/><path d="M7 26c1.5-5 5-7.5 9-7.5s7.5 2.5 9 7.5"/>',
     "<b>Who runs it</b>: the operator, as the entity names itself, with the founding date where its pages give one."),
    ("admits", "What it admits", "and in what unit", '<rect x="6" y="6" width="20" height="20" rx="2"/><path d="M6 13h20M13 13v13"/>',
     "<b>What it admits and in what unit</b>: its intake, its unit, what it records per item, its count with the date of the count, its cadence, its data access and licence."),
    ("leaves", "What it leaves out", "the negative tags", '<circle cx="16" cy="16" r="10"/><path d="M9 23 23 9" stroke="var(--accent)"/>',
     "<b>What it leaves out</b>: the negative tags, each a thing the entity is not, and the names it can be confused with."),
    ("ends", "Where its record goes", "when it ends", '<path d="M6 16h14"/><path d="M16 11l5 5-5 5"/><path d="M24 7v18"/>',
     "<b>Where its record goes when it ends</b>: the lifecycle, kept apart from the observation, and the relations a sunset leaves: the replacement named, the claimed successors, the revivals, the data dump."),
]
def flow_html():
    steps = '<span class="arrow" aria-hidden="true"></span>'.join(
        f'<button type="button" class="step" aria-expanded="false" aria-controls="x-{k}">{SVG(d)}<b>{t}</b><span>{u}</span></button>' for k, t, u, d, _ in FLOW)
    xs = "".join(f'<p id="x-{k}" class="x" hidden>{x}</p>' for k, _, _, _, x in FLOW)
    return (f'<div class="flow" role="group" aria-label="What each record answers">{steps}</div><div class="flow-x">{xs}</div>'
            '<noscript><style>.flow-x .x{display:block!important}</style></noscript>'
            '<p class="fig-cap">Each record answers five questions, every field with its source and its basis. Tap a step for the fields.</p>')
FLOW_JS = ("<script>document.querySelectorAll('.flow .step').forEach(b=>b.onclick=()=>{const on=b.getAttribute('aria-expanded')!=='true';"
           "document.querySelectorAll('.flow .step').forEach(x=>{x.setAttribute('aria-expanded','false');document.getElementById(x.getAttribute('aria-controls')).hidden=true});"
           "if(on){b.setAttribute('aria-expanded','true');document.getElementById(b.getAttribute('aria-controls')).hidden=false}})</script>")
def cite_text(r):
    return f'Lee Sharks, ed. "{r["name"]}." MMRS meta-aggregator, Machine-Mediated Reception Studies, compiled {D["compiled"]}. {BASE}{r["slug"]}/'
def actions(r):
    rel = {x["rel"]: x for x in r["relations"] if x.get("url")}
    a = [f'<a class="btn" href="{e(r["url"])}">Visit {e(r["name"])} ↗</a>']
    if "non_row" in rel: a.append(f'<a class="btn ghost" href="{e(rel["non_row"]["url"])}">The /non row</a>')
    caps = [x for x in r["relations"] if x["rel"] == "capture" and x.get("url")]
    if caps: a.append(f'<a class="btn ghost" href="{e(caps[0]["url"])}">{"Capture" if len(caps) == 1 else f"{len(caps)} captures"}</a>')
    a.append('<a class="btn ghost" href="#follow">Follow</a>')
    a.append('<button class="btn ghost" type="button" data-copy="cite">Copy citation</button>')
    return '<div class="act">' + "".join(a) + "</div>"
def signup(follow=None, name=None):
    """An email box. Posts to /api/subscribe, which stores the address privately (see /privacy/)."""
    if follow:
        h, t = f"Follow {e(name)}", f"An email when this record changes: the aggregator ends, comes back, changes hands, or gets a new capture."
    else:
        h, t = "The MMRS digest", "New aggregator records, lifecycle changes and captures, by email, now and then."
    return (f'<form class="signup"{' id="follow"' if follow else ''} action="/api/subscribe/" method="post">'
            f'<h4>{h}</h4><p>{t}</p><div class="fr"><input type="email" name="email" required placeholder="you@example.org" autocomplete="email" aria-label="Email address">'
            f'<button class="btn" type="submit">{"Follow" if follow else "Subscribe"}</button></div>'
            + (f'<input type="hidden" name="follow" value="{e(follow)}">' if follow else "")
            + '<input type="hidden" name="page" value=""><span class="trap" aria-hidden="true"><input type="text" name="website" tabindex="-1" autocomplete="off"></span>'
            '<label class="ok"><input type="checkbox" name="consent" value="yes" required><span>Email me from MMRS about this. My address is stored privately and never published; '
            'every email carries a one-click unsubscribe. <a href="/privacy/">Privacy</a></span></label><p class="msg" role="status"></p></form>')
SIGNUP_JS = ("<script>document.querySelectorAll('form.signup').forEach(f=>{f.page.value=location.pathname;f.onsubmit=async ev=>{ev.preventDefault();const m=f.querySelector('.msg'),b=f.querySelector('button');"
             "b.disabled=true;m.className='msg';m.textContent='Saving…';try{const r=await fetch(f.action,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f))});"
             "const j=await r.json().catch(()=>({}));if(r.ok){m.className='msg good';m.textContent='You are on the list. Thank you.';f.email.value=''}else{m.className='msg bad';m.textContent=j.error||'That did not work. Please try again.'}}"
             "catch(_){m.className='msg bad';m.textContent='That did not work. Please try again.'}b.disabled=false}})</script>")
def simple_page(path, title, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} — MMRS</title>'
            f'<link rel="canonical" href="https://www.machinemediation.org{path}">{HEAD}</head><body>{topbar()}<div class="wrap"><div class="crumb"><a href="/">Machine-Mediated Reception Studies</a> / {e(title.lower())}</div>'
            f'<h1>{e(title)}</h1><div class="prose">{body}</div><div class="foot">Machine-Mediated Reception Studies · machinemediation.org · editor Lee Sharks</div></div></body></html>')
PRIVACY = ("<p>MMRS asks for one thing: an email address, typed in by the person who owns it, with a box ticked to agree to the emails.</p>"
           "<h2>What is stored</h2><p>The address, which list it joined (the digest, or a follow of one aggregator, and which), the date, and the page the form was on. Nothing else: no name, no IP address, no tracking.</p>"
           "<h2>Where</h2><p>In a private store of the site's host, Vercel. Private means no web address serves the records; only the site's own signup code and its operator can read them. Addresses are never published, sold or shared.</p>"
           "<h2>What it is used for</h2><p>The emails the person asked for: the digest, or notice that a followed aggregator's record changed. Every email carries a one-click unsubscribe, and an unsubscribe removes the address from that list.</p>"
           "<h2>Removal</h2><p>Anyone can ask for their address to be deleted entirely, from any email, and it is.</p>")
COPY_JS = ("<script>document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>{const t=document.getElementById(b.dataset.copy).innerText;"
           "(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{const o=b.textContent;b.textContent='Copied';setTimeout(()=>b.textContent=o,1600)})"
           ".catch(()=>{const s=getSelection(),g=document.createRange();g.selectNodeContents(document.getElementById(b.dataset.copy));s.removeAllRanges();s.addRange(g)})})</script>")
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
    bath = f'<p class="d">{e(bat["status"])}</p><h3>Queries</h3><ul>{"".join(f"<li>{e(q)}</li>" for q in bat["queries"])}</ul><h3>Checks</h3><ul>{"".join(f"<li>{e(c)}</li>" for c in bat["checks"])}</ul>' if bat else ""
    src = "".join(f'<li><a href="{e(s["url"])}">{e(s["url"])}</a><div class="d">read {e(s["read"])} · {e(s["for"])}</div></li>' for s in r["sources"].values())
    unc = "".join(f"<li>{e(u)}</li>" for u in r.get("unchecked", []))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(r["name"])} — MMRS meta-aggregator</title><meta name="description" content="{e(kernel(r))}"><link rel="canonical" href="{BASE}{r["slug"]}/">
<script type="application/ld+json">{jsonld(r)}</script>{HEAD}</head><body>{topbar("Aggregators")}<div class="wrap">
<div class="crumb"><a href="../">MMRS meta-aggregator</a> / {e(r["kind"])}</div><h1>{e(r["name"])}</h1>{chips(r)}<div class="kernel">{e(kernel(r))}</div>{actions(r)}
<h2>Entity</h2><table>{tbl}</table><p class="legend">op operator statement · 3p third-party report · obs our observation · rd our reading</p>
<div class="art">{body}</div>{f'<h2>For a research question</h2><table>{props}</table>' if props else ''}
<h2>Relations</h2>{relhtml or '<p class="pend">None recorded yet.</p>'}
<div style="margin-top:34px">{fold("Disambiguation", f'<table>{dis}</table>' if dis else '', len(r.get("disambiguation", [])), "the names it can be confused with")}{fold("Negative tags", f'<ul>{neg}</ul>' if neg else '', len(r.get("negative_tags", [])), "what it is not")}{fold("Reception battery", bath, len(bat["queries"]) if bat else None, "the queries and checks for its machine reception")}{fold("Provenance", f'<ul>{src}</ul>', len(r["sources"]), "every source read, with its date")}{fold("Not yet checked", f'<ul>{unc}</ul>' if unc else '', len(r.get("unchecked", [])), "what remains to read")}</div>
<div style="margin-top:34px">{signup(r["slug"], r["name"])}</div><h2>Cite this record</h2><div class="cite"><p id="cite">{e(cite_text(r))}</p><p class="d">Record {BASE}{r["slug"]}/ · entity {BASE}{r["slug"]}/#entity</p></div>
<div class="foot">Editor: Lee Sharks (<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>). This page is the MMRS record of the entity above: its reading, fields and relations are MMRS's, and each field carries its source and basis. Record {BASE}{r["slug"]}/ · entity {BASE}{r["slug"]}/#entity · compiled {D["compiled"]}</div></div>{COPY_JS}{SIGNUP_JS}</body></html>"""
def cand_html():
    C = D.get("candidates") or []
    if not C: return ""
    li = ""
    for c in C:
        nm = f'<a href="{e(c["url"])}">{e(c["name"])}</a>' if c.get("url") else e(c["name"])
        li += f'<li>{nm}<div class="d">{e(c["note"])} · surfaced by <a href="https://www.alexanarch.org/captures/{e(c["surfaced_by"])}/">{e(c["surfaced_by"])}</a></div></li>'
    return f'<h2>Candidates</h2><p class="d" style="margin-bottom:10px">{e(D.get("candidates_note", ""))}</p><ul>{li}</ul>'
def index():
    roles = sorted({x for r in ROWS for x in r["roles"]}); kinds = sorted({r["kind"] for r in ROWS})
    top = [r for r in sorted(ROWS, key=lambda r: r["name"].lower()) if not any(x["rel"] == "part_of" for x in r["relations"])]
    rows = "".join(f'<div class="row" data-roles="{e(" ".join(r["roles"]))}" data-kind="{e(r["kind"])}" data-text="{e((r["name"] + " " + " ".join(r.get("aka", [])) + " " + r["operator"] + " " + kernel(r)).lower())}"><div class="n"><a href="{r["slug"]}/">{e(r["name"])}</a></div>{chips(r)}<div class="k">{e(kernel(r))}</div></div>' for r in top)
    btn = lambda key, vals: "".join(f'<button data-{key}="{e(v)}">{e(v)}</button>' for v in vals)
    cell = lambda r, k: f'<span title="{e(r["properties"][k]["value"])}">{e(r["properties"][k]["short"])}</span>' if k in r.get("properties", {}) else '<span class="d">·</span>'
    cand = cand_html()
    trav = "".join(f'<tr><td><a href="{r["slug"]}/">{e(r["name"])}</a></td>' + "".join(f"<td>{cell(r, k)}</td>" for k, _ in PROPS) + "</tr>" for r in sorted(ROWS, key=lambda r: r["name"].lower()))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MMRS meta-aggregator</title><meta name="description" content="The aggregators of machine-mediated reception work, each formalized as an entity with sourced, dated fields."><link rel="canonical" href="{BASE}">{HEAD}</head><body>{topbar("Aggregators")}<div class="wrap">\n<div class="crumb"><a href="/">Machine-Mediated Reception Studies</a> / aggregators</div><h1>MMRS meta-aggregator</h1><div class="kernel">The aggregators of machine-mediated reception work, each formalized as an entity: what it is in its own words, who runs it, what it admits and in what unit, what it leaves out, and where its record goes when it ends. {len(ROWS)} aggregators, compiled {D["compiled"]}.</div>{flow_html()}
<div class="f"><button class="on" data-all="1">all</button>{btn("role", roles)}</div><div class="f">{btn("kind", kinds)}</div><div id="L" class="grid">{rows}</div><p class="none" id="none">No aggregator matches.</p><div style="margin-top:34px">{signup()}</div>
{cand}<h2>Traverse by question</h2><div class="tw"><table class="tv"><tr><td></td>{"".join(f"<td>{q}</td>" for _, q in PROPS)}</tr>{trav}</table></div><p class="legend">· not yet read</p>
<div class="foot">Machine-Mediated Reception Studies · machinemediation.org · editor Lee Sharks (<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>)</div></div>
<script>let fs={{}};const q0=new URLSearchParams(location.search).get('q')||'';const qi=document.querySelector('.srch input');qi.value=q0;const qf=document.querySelector('.srch');qf.onsubmit=ev=>{{ev.preventDefault();apply()}};qi.oninput=()=>apply();function apply(){{const q=qi.value.trim().toLowerCase();let n=0;document.querySelectorAll('.f button').forEach(x=>{{const k=x.dataset.role?'role':x.dataset.kind?'kind':'all';x.classList.toggle('on',k==='all'?!fs.role&&!fs.kind:fs[k]===x.dataset[k])}});document.querySelectorAll('#L .row').forEach(r=>{{const ok=(!fs.role||r.dataset.roles.split(' ').includes(fs.role))&&(!fs.kind||r.dataset.kind===fs.kind)&&(!q||q.split(' ').filter(Boolean).every(w=>r.dataset.text.includes(w)));r.style.display=ok?'':'none';n+=ok}});document.getElementById('none').style.display=n?'none':'block'}}document.querySelectorAll('.f button').forEach(b=>b.onclick=()=>{{if(b.dataset.all){{fs={{}}}}else{{const k=b.dataset.role?'role':'kind',v=b.dataset[k];fs[k]=fs[k]===v?undefined:v}}apply()}});apply()</script>{SIGNUP_JS}{FLOW_JS}</body></html>"""
def front_block():
    top = [r for r in sorted(ROWS, key=lambda r: r["name"].lower()) if not any(x["rel"] == "part_of" for x in r["relations"])]
    li = "".join(f'<a class="mini" href="/aggregators/{r["slug"]}/"><b>{e(r["name"])}</b><span>{e(r["kind"])} · {e(", ".join(r["roles"]))}{" · ended" if r["lifecycle"]["state"] == "ended" else ""}</span></a>' for r in top)
    return ("<!-- META-AGGREGATOR-START (generated by scripts/meta_aggregator/build.py from data/meta-aggregator/census.json) -->\n"
            '<div class="section"><div class="section-title">MMRS meta-aggregator</div>'
            f'<p class="plain">The aggregators of machine-mediated reception work, each formalized as an entity: what it is in its own words, who runs it, what it admits and in what unit, what it leaves out, and where its record goes when it ends. {len(ROWS)} aggregators, every field sourced and dated; compiled {D["compiled"]}.</p>'
            f'<div class="minis">{li}</div><p class="plain" style="margin-top:14px"><a href="/aggregators/">All {len(ROWS)}, with the traversal table by research question</a> · <a href="/data/meta-aggregator/census.json">the census as data</a></p>' + signup() + SIGNUP_JS + '</div>\n'
            '<div class="section-title" style="margin:34px 0 14px">Machine-Mediated Reception Studies — the journal</div>\n<!-- META-AGGREGATOR-END -->')
def splice(path, start, end, block, anchor):
    t = path.read_text(encoding="utf-8")
    if start in t: t = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: block, t, count=1, flags=re.S)
    else:
        assert anchor in t, anchor; t = t.replace(anchor, block + "\n" + anchor, 1)
    path.write_text(t, encoding="utf-8")
for _p, _t, _b in [("/privacy/", "Privacy", PRIVACY), ("/subscribed/", "Subscribed", "<p>You are on the list. Thank you.</p><p><a href=\"/aggregators/\">Back to the aggregators</a></p>")]:
    (ROOT / _p.strip("/")).mkdir(exist_ok=True); (ROOT / _p.strip("/") / "index.html").write_text(simple_page(_p, _t, _b), encoding="utf-8")
(ROOT / "assets").mkdir(exist_ok=True); (ROOT / "assets/mmrs.css").write_text(CSS, encoding="utf-8")
OUT.mkdir(exist_ok=True); (OUT / "index.html").write_text(index())
for r in ROWS:
    p = OUT / r["slug"]; p.mkdir(exist_ok=True); (p / "index.html").write_text(page(r))
splice(ROOT / "index.html", "<!-- META-AGGREGATOR-START", "<!-- META-AGGREGATOR-END -->", front_block(), "<!-- INSTRUMENT CARDS -->")
splice(ROOT / "index.html", "<!-- MMRS-TOPBAR-START", "<!-- MMRS-TOPBAR-END -->",
       "<!-- MMRS-TOPBAR-START (generated by scripts/meta_aggregator/build.py) -->" + topbar() + "<!-- MMRS-TOPBAR-END -->", "<!-- MSP-IDSTRIP-START -->")
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
