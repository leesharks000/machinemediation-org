"""Census v2.4 (2026-10-29): repairs reported by the sixteen /non composers, each checked at the saved source
(alexanarch datasets/negative-of-the-negative/v2/intake/<row>-20261029/); and each record linked to its /non row."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/meta-aggregator/census.json"; A = ROOT / "scripts/meta_aggregator/articles.py"
D = json.load(open(P)); B = {r["slug"]: r for r in D["rows"]}; R = "2026-10-29"
NON = "https://www.alexanarch.org/non/{}/"
def src(s, url, why):
    k = url.split("//")[-1].strip("/").replace("www.", ""); B[s]["sources"][k] = {"url": url, "read": R, "for": why}; return k
def ev(s, f, k, basis): B[s]["evidence"][f] = {"src": k, "basis": basis}
ROWS = ["ai-incident-database", "papers-with-code", "oecd-ai-incidents-monitor", "aiaaic-repository", "mit-ai-risk-repository", "mit-ai-incident-tracker",
        "ai-hallucination-cases", "academ-ai", "problematic-paper-screener", "newsguard-ai-tracking-center", "newsguard-ai-false-claim-monitor",
        "presenc-geo-papers", "awesome-geo-davidhuji", "aeovision-geo-papers", "codesota", "data-provenance-explorer", "cms-ai-copyright-tracker", "search-arena"]
for s in ROWS:
    if not any(x["rel"] == "non_row" for x in B[s]["relations"]):
        B[s]["relations"].append({"rel": "non_row", "url": NON.format(s), "label": "its /non row (EA-NEGONT-02 v0.9, equal case)", "note": "composed 2026-10-29 against its own pages, its Wikipedia article or its absence, the capture's cards and the archive"})
# Search Arena: the page this record read was a stale render; Arena's published data is current
k = src("search-arena", "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset", "Arena's published leaderboard data (search board snapshots)")
B["search-arena"]["count"] = {"value": "42 models on the search board in Arena's published data of 2026-10-13; the leaderboard page as this record's fetcher was served it showed 247,944 votes across 22 models, dated 25 February 2026", "as_of": R}
ev("search-arena", "count", k, "operator")
B["search-arena"]["note"] = B["search-arena"]["note"] + ". The page as served to this record on 2026-10-28 and 2026-10-29 matched Arena's snapshot of 2026-02-26; Arena's own latest published board was dated 2026-10-13"
# MIT AI Risk Repository: version 4 is 74 frameworks; licence and method stated; the tracker is the Initiative's workstream
m = B["mit-ai-risk-repository"]
k = src("mit-ai-risk-repository", "https://airisk.mit.edu/risks", "the repository's own page: 1,700+ risks from 74 frameworks")
k2 = src("mit-ai-risk-repository", "https://airisk.mit.edu/llms.txt", "the site's statement to language models: licence CC BY 4.0, what to name")
m["count"] = {"value": "more than 1,700 risks from 74 frameworks (version 4, December 2025); the Initiative's home page gives 65+", "as_of": R}; ev("mit-ai-risk-repository", "count", k, "operator")
m["license"] = "CC BY 4.0 ('unless a specific page states otherwise')"; ev("mit-ai-risk-repository", "license", k2, "operator")
m["url"] = "https://airisk.mit.edu/risks"
m["unchecked"] = [u for u in m.get("unchecked", []) if "licence" not in u and "extraction method" not in u]
for x in m["relations"]:
    if x["rel"] == "has_part" and x.get("target") == "mit-ai-incident-tracker": x["rel"] = "sibling"; x["note"] = "a workstream of the MIT AI Risk Initiative beside the repository (its About page)"
t = B["mit-ai-incident-tracker"]
for x in t["relations"]:
    if x["rel"] == "part_of": x["rel"] = "sibling"; x["note"] = "a workstream of the MIT AI Risk Initiative beside the repository"
t["count"] = {"value": "1,600 (the tracker page's heading) and 'more than 1,400' (its description); Google's card summary of 2026-10-29 gives 1,752; the MIT AI Risk Navigator's heading gives 1,497 (2026-10-29)", "as_of": R}
t["unit"] = "AI Incident Database incident, classified by risk domain, cause, harm, severity and EU AI Act risk level"
# AI Hallucination Cases: the start date
h = B["ai-hallucination-cases"]; k = src("ai-hallucination-cases", "https://artificialauthority.ai/p/hallucinations-case-database-faq", "Charlotin's FAQ (Artificial Authority, 14 November 2025): 'When did you start the database, and why ? April 2025.'")
h["founded"] = "April 2025 (its maker's FAQ; Wikipedia's 'Hallucination (artificial intelligence)'); its decision-date filter begins in Q2 2023"; ev("ai-hallucination-cases", "founded", k, "operator")
for c in D.get("candidates", []):
    if c["name"].startswith("AI Hallucination Cases Tracker (UK)"):
        c["name"] = "AI Hallucination Cases Tracker, Natural and Artificial Law (Matthew Lee)"; c["note"] = "an international collection of judicial statements on AI hallucination, with a separate UK page; it does not name Charlotin's database"
    if c["name"].startswith("HAQQ"): c["url"] = "https://www.haqq.ai/blog/ai-legal-hallucination-audit"
    if c["name"].startswith("henu-wang"): c["name"] = "henu-wang/awesome-geo (Awesome GEO)"
D["candidates"].append({"name": "Canadian AI Hallucination Cases Database (courtready.ca)", "url": None, "surfaced_by": "ai-hallucination-cases-database-aio-20261029", "note": "cited in Wikipedia's 'Hallucination (artificial intelligence)', read by the /non row's composer"})
# AIAAIC: its own words, the newsletter
a = B["aiaaic-repository"]; a["self_description"] = None; a["evidence"].pop("self_description", None)
a["note"] = "its newsletter, AIAAIC Alert, is on Substack; Charlie Pownall's name is in that page's metadata. The 'private initiative' wording sometimes given for its start is EthicAI's; the OECD catalogue says 'a private, professional project'. The highest entry number on its front page on 2026-10-29 was AIAAIC2276"
ev("aiaaic-repository", "note", "aiaaicalert.substack.com/about", "observed")
# Academ-AI: scope and labels as the site gives them now
c = B["academ-ai"]; k = src("academ-ai", "https://www.academ-ai.info/about", "scope, errata label, as of 2026-10-29")
c["intake"] = ("flagged by phrasing that strongly suggests chatbot generation, quoted with the phrases highlighted; journal articles, conference papers/proceedings, books/chapters and dissertations/theses "
               "(its About page, 2026-10-29: 'Preprints, blog posts, and other media are out of scope'; eDiscovery Today's account of August 2025 listed theses as excluded)")
ev("academ-ai", "intake", k, "operator")
c["note"] = "its errata page now calls a correction made without explanation a 'stealth revision' (eDiscovery Today, August 2025: 'stealth corrections'); a publishers page counts examples by publisher (IEEE 90, Elsevier 34 in August 2025). Glynn's paper gives a second affiliation, the Meta-Research Innovation Center at Stanford (METRICS); its v1 analysed 500 examples, v2 768"
ev("academ-ai", "note", k, "operator")
# Problematic Paper Screener: the article's date
p = B["problematic-paper-screener"]; p["count"]["as_of"] = "The Conversation, 29 January 2025"
# NewsGuard: the series' figures and cadence as their pages state them
n = B["newsguard-ai-false-claim-monitor"]; k = src("newsguard-ai-false-claim-monitor", "https://www.newsguardtech.com/ai-false-claims-monitor/", "the method page")
n["cadence"] = "edition titles read 'Monthly' to mid-2025 and 'Quarterly' for January and May 2026; the method page still says 'Our analysts evaluate the top AI models monthly'"
ev("newsguard-ai-false-claim-monitor", "cadence", "newsguardtech.com/ai-monitor/may-2026", "observed")
ev("newsguard-ai-false-claim-monitor", "note", k, "operator")
g = B["newsguard-ai-tracking-center"]; g["founded"] = "8 June 2023, as the tracker of 'Unreliable AI-Generated News' websites"; g["aka"] = ["Unreliable AI-Generated News Tracking Center"]
k = src("newsguard-ai-tracking-center", "https://www.newsguardtech.com/press/newsguard-launches-tracking-center-for-ai-generated-news/", "launch release, 8 June 2023")
ev("newsguard-ai-tracking-center", "founded", k, "operator")
# Presenc: the byline
B["presenc-geo-papers"]["note"] = B["presenc-geo-papers"]["note"].replace("the page's byline 23 April", "the page's byline reads 'Last updated: April 2026' and its HTML metadata gives 23 April")
# AEO Vision: the address and what was read
v = B["aeovision-geo-papers"]; v["url"] = "https://aeovision.ai/articles/top-arxiv-papers-for-generative-engine-optimization/"
for s0 in v["sources"].values():
    if "aeovision.ai/articles/top-arxiv" in s0["url"]: s0["for"] = "all fields (the twelve papers, read 2026-10-29)"
# Awesome-GEO: vendor credits
w = B["awesome-geo-davidhuji"]; w["note"] = "its README credits two entries to the companies that built them ('Built by Corank', 'Built by Assay') and carries one vendor's claim of a '320% citation rate improvement'"
ev("awesome-geo-davidhuji", "note", "github.com/DavidHuji/Awesome-GEO", "observed")
for d0 in w.get("disambiguation", []):
    if d0.get("label", "").startswith("henu-wang"): d0["label"] = "henu-wang/awesome-geo (Awesome GEO)"
# CodeSOTA: the third face, from its about page
s = B["codesota"]; k = src("codesota", "https://www.codesota.com/about", "editor, launch date, licence, 'a registry, not a leaderboard'")
s["founded"] = "10 December 2025 ('as an explicit successor attempt', its about page)"; ev("codesota", "founded", k, "operator")
s["license"] = "registry data CC BY 4.0 (its about page)"; ev("codesota", "license", k, "operator")
s["evidence"]["operator"] = {"src": k, "basis": "operator"}
s["note"] = ("three faces at three addresses: the homepage presents a routing layer and names Papers with Code only in a footer link; its /papers-with-code/ pages present it as 'the v2 replacement for what PWC did'; "
             "its about page calls it 'an independent registry of machine-learning benchmarks' — 'a registry, not a leaderboard' — and refuses the aggregator class ('Unlike aggregator sites')")
ev("codesota", "note", k, "operator")
for d0 in B["papers-with-code"].get("disambiguation", []):
    if d0.get("neighbour") == "codesota": d0["context"] = "codesota.com, routing layer, /api/sota, 'a registry, not a leaderboard'"
# Data Provenance Explorer: the self-description's source, the venue
dp = B["data-provenance-explorer"]; dp["evidence"]["self_description"] = {"src": "dataprovenance.org", "basis": "operator"}
dp["note"] = dp["note"].replace("(NeurIPS 2024 Datasets and Benchmarks)", "(NeurIPS 2024, by the Initiative's home page)")
dp["unchecked"] = [u for u in dp.get("unchecked", []) if "render by script" not in u]
# CMS: the count is an observation
B["cms-ai-copyright-tracker"]["evidence"]["count"] = {"src": "cms.law/en/int/publication/artificial-intelligence-and-copyright-case-tracker", "basis": "observed"}
B["cms-ai-copyright-tracker"]["note"] = B["cms-ai-copyright-tracker"]["note"].replace("'there are now over 40", "'There are now over 40").replace("Its region menu (Africa, Asia-Pacific, the Americas, the Middle East)", "Its region menu (Europe, Africa, Asia-Pacific, the Americas, the Middle East, International)")
# OECD: the operator and the themes
o = B["oecd-ai-incidents-monitor"]; o["operator"] = "the OECD.AI expert group on AI incidents (OECD.AI), with the support of the Patrick J. McGovern Foundation"
o["founded"] = "the expert group was formalised in January 2023 to develop it; LLM classification from November 2024"
o["note"] = "its 14 'risk themes' are an analysis of its summaries in OECD AI Papers No. 53 (February 2026), which clustered them by k-means into 25 clusters and merged them to 14"
D["compiled"] = R; D["schema_version"] = "2.4"
json.dump(D, open(P, "w"), ensure_ascii=False, indent=1)
s_ = A.read_text()
REP = [
 ("Search Arena ranks search-enabled language models by head-to-head human votes: 247,944 votes across 22 models at its update of 25 February 2026.",
  "Search Arena ranks search-enabled language models by head-to-head human votes: 42 models on its search board in Arena's published data of 13 October 2026."),
 ("a database of more than 1,700 AI risks extracted from 65 published risk frameworks, run by the MIT AI Risk Initiative (MIT FutureTech). Version 4 went live in December 2025; its AI Incident Tracker classifies AI Incident Database reports against the same taxonomy.",
  "a database of more than 1,700 AI risks extracted from 74 published risk frameworks (version 4, December 2025; the Initiative's home page gives 65+), run by the MIT AI Risk Initiative (MIT FutureTech) under CC BY 4.0. The Initiative's AI Incident Tracker, a workstream beside it, classifies AI Incident Database incidents against the same taxonomy."),
 ("is licensed CC BY-SA 4.0, and is the subject of the AIAAIC Alert newsletter written by Charlie Pownall.", "is licensed CC BY-SA 4.0, and has a newsletter, AIAAIC Alert, on Substack."),
 ("It is the research-side list of the optimization basin, kept without vendor notes.", "It is the research-side list of the optimization basin; it adds no reading of its own to each paper, and credits two of its tools to the companies that built them."),
 ("and of an entity with two faces at two addresses: Google's Overview composes the homepage's routing layer and leaves the succession unsaid.",
  "and of an entity with three faces at three addresses: a routing layer on its homepage, a successor on its /papers-with-code/ pages, and on its about page \\\"an independent registry of machine-learning benchmarks\\\" that refuses the aggregator class. Google's Overview composes the homepage's routing layer and leaves the succession unsaid."),
 ("Journal articles, conference papers and books are admitted; theses, preprints and blog posts are excluded.", "Journal articles, conference papers, books and dissertations are admitted; preprints, blog posts and other media are out of scope (its About page, 2026-10-29)."),
 ("corrections with formal explanations, and \\\"stealth corrections\\\" made with none.", "corrections with formal explanations, and \\\"stealth revisions\\\" made with none."),
 ("The page gives its size twice, as \\\"more than 1,400\\\" in its description and 1,600 in its heading.", "The page gives its size twice, as \\\"more than 1,400\\\" in its description and 1,600 in its heading; the MIT AI Risk Navigator gives 1,497."),
 ("The OECD AI Incidents and Hazards Monitor (AIM) is an automated monitor of AI harm events in the news, run by OECD.AI.", "The OECD AI Incidents and Hazards Monitor (AIM) is an automated monitor of AI harm events in the news, developed by the OECD.AI expert group on AI incidents with the Patrick J. McGovern Foundation's support."),
 ("a recurring audit of leading chatbots on false claims in the news: monthly until mid-2025, quarterly since.", "a recurring audit of leading chatbots on false claims in the news: its editions were titled monthly until mid-2025 and quarterly since, while its method page still says monthly."),
 ("The January 2026 edition reported that the tools repeated false claims more than 28% of the time.", "The January 2026 edition reported, by the method page, that the tools repeated false claims more than 28% of the time."),
]
for o_, n_ in REP:
    if o_ in s_: s_ = s_.replace(o_, n_); print("replaced:", o_[:70])
    else: print("NOT FOUND:", o_[:70])
A.write_text(s_)
