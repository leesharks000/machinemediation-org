"""Census v2.2 (2026-10-29): the composition layer's account of each entity, captured the same night on Google AI Overview and
seated in the Capture Registry, linked to its record; the corrections those captures occasioned, each re-read at its source;
census candidates the captures surfaced."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/meta-aggregator/census.json"
R = "2026-10-29"; CAP = "https://www.alexanarch.org/captures/{}/"
D = json.load(open(P)); B = {r["slug"]: r for r in D["rows"]}
def src(slug, url, why):
    k = url.split("//")[-1].strip("/").replace("www.", ""); B[slug]["sources"][k] = {"url": url, "read": R, "for": why}; return k
def ev(slug, f, k, basis): B[slug]["evidence"][f] = {"src": k, "basis": basis}
CAPS = {"ai-incident-database": ["ai-incident-database", "what-counts-as-an-incident-in-the-ai-incident-database"], "papers-with-code": ["papers-with-code", "is-papers-with-code-still-active"],
        "oecd-ai-incidents-monitor": ["oecd-ai-incidents-and-hazards-monitor"], "aiaaic-repository": ["aiaaic-repository"], "mit-ai-risk-repository": ["mit-ai-risk-repository"],
        "mit-ai-incident-tracker": ["mit-ai-incident-tracker"], "ai-hallucination-cases": ["ai-hallucination-cases-database"], "academ-ai": ["academ-ai"],
        "problematic-paper-screener": ["problematic-paper-screener"], "newsguard-ai-tracking-center": ["newsguard-ai-tracking-center"],
        "newsguard-ai-false-claim-monitor": ["newsguard-ai-false-claim-monitor"], "presenc-geo-papers": ["presenc-ai-geo-academic-papers"], "awesome-geo-davidhuji": ["awesome-geo"],
        "aeovision-geo-papers": ["aeo-vision-top-arxiv-papers-geo"], "codesota": ["codesota"], "data-provenance-explorer": ["data-provenance-explorer"],
        "cms-ai-copyright-tracker": ["cms-ai-and-copyright-case-tracker"], "search-arena": ["search-arena-leaderboard"]}
SEG = json.load(open(ROOT / "scripts/meta_aggregator/patches/captures_20261029_queries.json"))
for ent, qs in CAPS.items():
    for q in qs:
        slug = q + "-aio-20261029"
        B[ent]["relations"].append({"rel": "capture", "url": CAP.format(slug), "label": f"«{SEG[q]}» — Google AI Overview, 2026-10-29", "note": "the composition layer's account of the entity, seated in the Capture Registry", "dates": {"observed": R}})
for k in ("ai-incident-database", "papers-with-code"):
    B[k]["battery"]["status"] = "run 2026-10-29 on Google AI Overview; results in the capture records"

# Papers with Code: the revival, read at its source
p = B["papers-with-code"]
k = src("papers-with-code", "https://github.com/huggingface/paperswithcode", "the revival's code, licence and statement of what it recreates")
p["relations"] = [x for x in p["relations"] if x["rel"] != "revival"]
p["relations"].append({"rel": "revival", "target": "papers-with-code-revival", "note": "paperswithcode.co: 'recreates the original paperswithcode.com, which Meta retired in 2025' (its README); code under Apache-2.0 in Hugging Face's GitHub organization"})
p["lifecycle"]["detail"] = "paperswithcode.com sunset 24 July 2025; announced 25 July 2025 by Julien Chaumond, Hugging Face co-founder and CTO; its name now has a live instance, the revival at paperswithcode.co"
p["negative_tags"] = [t if not t.startswith("NOT live") else "paperswithcode.com is NOT live since 24 July 2025; the revival at paperswithcode.co is a separate entity" for t in p["negative_tags"]]
p["note"] = ("where users were sent at the end is reported two ways: to Hugging Face (CodeSOTA, hyper.ai) and to the GitHub repository (TIB's blog, and a Reddit thread of 6 August 2025, both cards in the capture of 2026-10-29). "
             "The revival's README states that Meta retired the original")
ev("papers-with-code", "note", k, "third-party")
p["unchecked"] = [u for u in p["unchecked"] if "revival" not in u] + ["the redirect target at the sunset, which sources give differently"]
D["rows"].append({"slug": "papers-with-code-revival", "name": "Papers with Code (paperswithcode.co)", "aka": ["the PapersWithCode revival"], "url": "https://paperswithcode.co/",
  "operator": "Niels Rogge, of Hugging Face's open-source team; code in the huggingface GitHub organization", "founded": "2026 (the r/MachineLearning announcement card is dated 18 May 2026)",
  "kind": "database", "roles": ["discovery"], "lifecycle": {"state": "active"}, "observed": {"on": R, "fetch": "read (title and description only; the page renders by script)"},
  "self_description": "Discover trending machine-learning papers, methods, benchmarks, datasets, and open-source implementations.",
  "unit": "paper, with its code, datasets and benchmark results", "intake": "automated imports from Hugging Face, arXiv, GitHub and public leaderboards (its README)",
  "license": "code Apache-2.0", "data_access": "code at github.com/huggingface/paperswithcode",
  "note": "the README states that it 'recreates the original paperswithcode.com, which Meta retired in 2025'. Whether it is an official Hugging Face product is described differently: Google's Overview says Hugging Face 'officially stepped in'; AI Weekly called it an individual effort",
  "relations": [{"rel": "revives", "target": "papers-with-code"}, {"rel": "capture", "url": CAP.format("is-papers-with-code-still-active-aio-20261029"), "label": "«is papers with code still active» — Google AI Overview, 2026-10-29", "note": "the capture that occasioned this record", "dates": {"observed": R}}],
  "sources": {"github.com/huggingface/paperswithcode": {"url": "https://github.com/huggingface/paperswithcode", "read": R, "for": "description, licence, README"},
              "paperswithcode.co": {"url": "https://paperswithcode.co/", "read": R, "for": "title and description"},
              "alexanarch.org/captures/is-papers-with-code-still-active-aio-20261029": {"url": CAP.format("is-papers-with-code-still-active-aio-20261029"), "read": R, "for": "the announcement date (card), the operator"}},
  "evidence": {"operator": {"src": "alexanarch.org/captures/is-papers-with-code-still-active-aio-20261029", "basis": "third-party"},
               "founded": {"src": "alexanarch.org/captures/is-papers-with-code-still-active-aio-20261029", "basis": "observed"},
               "self_description": {"src": "paperswithcode.co", "basis": "operator"}, "intake": {"src": "github.com/huggingface/paperswithcode", "basis": "operator"},
               "license": {"src": "github.com/huggingface/paperswithcode", "basis": "operator"}, "note": {"src": "github.com/huggingface/paperswithcode", "basis": "operator"}},
  "properties": {"admission_requires_harm": {"value": "no", "short": "no", "src": None, "basis": "reading"},
                 "version_history": {"value": "its code history is public; data history not read", "short": "code only", "src": "github.com/huggingface/paperswithcode", "basis": "observed"}},
  "disambiguation": [{"neighbour": "papers-with-code", "context": "paperswithcode.com, Atlas ML, Meta, 2018–2025, the data dumps"},
                     {"neighbour": "codesota", "context": "codesota.com, routing layer, /api/sota"}, {"self": True, "context": "paperswithcode.co, Niels Rogge, huggingface/paperswithcode, Apache-2.0"}],
  "negative_tags": ["NOT paperswithcode.com, which ended 24 July 2025", "NOT CodeSOTA"], "unchecked": ["its item counts", "its own statement of who runs it"]})

# CodeSOTA: the homepage's entity first
c = B["codesota"]; k = src("codesota", "https://www.codesota.com/", "homepage title and self-description")
c["self_description"] = "helps developers choose AI tools for documents, speech, and coding (its homepage, titled 'CodeSOTA — One Routing Layer for AI Tasks')"
c["unit"] = "AI task, routed to a model chosen by benchmark evidence, quality and cost"; ev("codesota", "self_description", k, "operator"); ev("codesota", "unit", k, "operator")
c["note"] = ("two faces at two addresses: the homepage presents a routing layer and names Papers with Code only in a footer link; its /papers-with-code/ pages present it as 'the v2 replacement for what PWC did', rebuilding that infrastructure 'independently'")
ev("codesota", "note", k, "observed")

# Data Provenance Explorer: the current scale, from the Initiative's own text on the capture's cards
d = B["data-provenance-explorer"]; k = src("data-provenance-explorer", CAP.format("data-provenance-explorer-aio-20261029"), "the Initiative's own page text, on the Overview's cards (the pages render nothing to this record's fetcher)")
d["count"] = {"value": "nearly 4,000 text, video and speech datasets (the Dataset Explorer); the founding audit covered more than 1,800 text datasets", "as_of": R}; ev("data-provenance-explorer", "count", k, "operator")
d["unit"] = "dataset (text, speech or video), traced to its creators, sources, licences, geographies, modalities and derivation chain"; ev("data-provenance-explorer", "unit", k, "operator")
d["unchecked"] = [u for u in d.get("unchecked", []) if "current scope" not in u] + ["the explorers' pages directly (they render by script)"]

# CMS: the US sentence quoted
cm = B["cms-ai-copyright-tracker"]
cm["note"] = "the page's summary states that 'there are now over 40 copyright claims being litigated in the US'; none is in the tracked list. Its region menu (Africa, Asia-Pacific, the Americas, the Middle East) leads to the firm's offices"
ev("cms-ai-copyright-tracker", "note", "cms.law/en/int/publication/artificial-intelligence-and-copyright-case-tracker", "observed")
cm["relations"].append({"rel": "neighbour", "url": "https://www.taylorwessing.com/", "label": "Taylor Wessing — AI & Copyright Case Tracker", "note": "a census candidate (surfaced by the capture of 2026-10-29)"})

# Collision sets observed by the captures
ac = B["academ-ai"]; ac.setdefault("disambiguation", [])
ac["disambiguation"] += [{"label": "AcademAI (academai.app)", "context": "AI training console, fluency course, certificates"}, {"label": "Academi.AI", "context": "study assistant, chat tutor"},
                         {"label": "Academiq", "context": "AI education platform, lesson plans, tools for teachers"}, {"self": True, "context": "Alex Glynn, undeclared AI use, journal articles, errata, stealth corrections"}]
ac["negative_tags"] = ["NOT AcademAI, Academi.AI or Academiq (education products)", "NOT only the dataset paper (arXiv:2411.15218): the paper analyses the database's first 768 cases"]
ag = B["awesome-geo-davidhuji"]; ag.setdefault("disambiguation", [])
ag["disambiguation"] += [{"label": "amplifying-ai/awesome-generative-engine-optimization", "context": "entity optimization, AI citations, E-E-A-T"}, {"label": "henu-wang/awesome (Awesome GEO)", "context": "resources, tools, guides"},
                         {"label": "aGEO (geo.deeflect.com)", "context": "free platforms and tools, Dmitry Kargaev"}, {"label": "Geoawesome", "context": "geospatial media, GIS, Earth observation"},
                         {"label": "Awesome GEE Community Catalog", "context": "Google Earth Engine, community geospatial datasets"}, {"self": True, "context": "DavidHuji, research papers by year, IF-GEO"}]
B["ai-incident-database"]["disambiguation"].insert(-1, {"label": "AI Incidents, Failures & Controversies Database (Kaggle)", "context": "Kaggle, 32 incidents, 29 companies, 24 columns"})
pr = B["presenc-geo-papers"]
pr["note"] = (pr["note"] + ". A sibling list, 'Essential GEO Research Papers, 10 Must-Read Studies', is on the same site; the Overview's card dates the 34-paper summary 15 April 2026, the page's byline 23 April. "
              "The vendor's name is corrected by Google to 'presence' before it is read (the capture of 2026-10-29)")
B["mit-ai-incident-tracker"]["count"]["value"] += "; Google's card summary gives 1,752, and the MIT AI Risk Navigator 'more than 1300'"

D["candidates"] = [
 {"name": "MIT AI Risk Navigator", "url": None, "surfaced_by": "mit-ai-risk-repository-aio-20261029", "note": "MIT's interactive tool linking the repository to incidents, frameworks and mitigations"},
 {"name": "AI Hallucination Cases Tracker (UK), Natural and Artificial Law", "url": None, "surfaced_by": "ai-hallucination-cases-database-aio-20261029", "note": "a UK companion to Charlotin's database"},
 {"name": "HAQQ — AI Hallucination Cases: The 2,202-Case Sanctions Tracker", "url": None, "surfaced_by": "ai-hallucination-cases-database-aio-20261029", "note": "a vendor tracker built on Charlotin's count"},
 {"name": "Taylor Wessing — AI & Copyright Case Tracker", "url": None, "surfaced_by": "cms-ai-and-copyright-case-tracker-aio-20261029", "note": "Carlsen, Penguin, GEMA and Koda cases against OpenAI, Suno and Meta"},
 {"name": "amplifying-ai/awesome-generative-engine-optimization", "url": None, "surfaced_by": "awesome-geo-aio-20261029", "note": "a GEO awesome list"},
 {"name": "henu-wang/awesome (Awesome GEO)", "url": None, "surfaced_by": "awesome-geo-aio-20261029", "note": "a GEO awesome list"},
 {"name": "aGEO — Awesome GEO platforms (geo.deeflect.com)", "url": "https://geo.deeflect.com/", "surfaced_by": "awesome-geo-aio-20261029", "note": "free GEO platforms and a repository list, by Dmitry Kargaev"},
 {"name": "AEO VC — AEO & GEO Research Papers", "url": None, "surfaced_by": "aeo-vision-top-arxiv-papers-geo-aio-20261029", "note": "a research list"},
 {"name": "GeoReady — GEO Research", "url": "https://geoready.dev/", "surfaced_by": "aeo-vision-top-arxiv-papers-geo-aio-20261029", "note": "a research list"},
 {"name": "Presenc AI — Essential GEO Research Papers, 10 Must-Read Studies", "url": None, "surfaced_by": "presenc-ai-geo-academic-papers-aio-20261029", "note": "a sibling of the 34-paper page"},
 {"name": "NewsGuard — False Claim Fingerprints", "url": None, "surfaced_by": "newsguard-ai-false-claim-monitor-aio-20261029", "note": "NewsGuard's catalogue of false claims, the monitor's prompt source"},
 {"name": "AI Incidents, Failures & Controversies Database (Kaggle)", "url": None, "surfaced_by": "ai-incident-database-aio-20261029", "note": "a dataset with a near name to AIID"}]
D["candidates_note"] = "Aggregators the composition layer surfaced in captures of the census's entities; listed for reading. Each enters the census once it has been read at its own pages."
D["compiled"] = R; D["schema_version"] = "2.2"
json.dump(D, open(P, "w"), ensure_ascii=False, indent=1); print(len(D["rows"]), "rows;", len(D["candidates"]), "candidates")
