"""Census v2.3 (2026-10-29): repairs reported by the /non composers of papers-with-code and ai-incident-database, each checked
against the saved source before it was made. Broken or mislabelled fields and quotations only."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/meta-aggregator/census.json"; A = ROOT / "scripts/meta_aggregator/articles.py"
D = json.load(open(P)); B = {r["slug"]: r for r in D["rows"]}; R = "2026-10-29"
a = B["ai-incident-database"]
a["evidence"]["founded"]["basis"] = "operator"          # arXiv:2011.08512 is by the database's founder, Sean McGregor
a["evidence"]["cadence"] = {"src": "incidentdatabase.ai", "basis": "reading"}   # the home page states no cadence
a["unit"] = a["unit"].replace("near-harm", "near harm")
a["note"] = "Wikipedia has no article: 'AI Incident Database' redirects to 'Partnership on AI' (its founding sponsor), which says the database 'shifted to a new special-purpose independent non-profit in 2022' and does not name the Responsible AI Collaborative"
a["sources"]["en.wikipedia.org/wiki/Partnership_on_AI"] = {"url": "https://en.wikipedia.org/wiki/Partnership_on_AI", "read": R, "for": "the redirect target and its account of the database"}
a["evidence"]["note"] = {"src": "en.wikipedia.org/wiki/Partnership_on_AI", "basis": "third-party"}
p = B["papers-with-code"]
p["evidence"]["unit"] = {"src": p["evidence"].get("unit", {}).get("src") or "techcrunch.com/2020/02/10/facebook-quietly-acquired-atlast-ml/amp", "basis": "third-party"}
v = B["papers-with-code-revival"]
k = "huggingface.co/blog/nielsr/paperswithcode-launch"
v["sources"][k] = {"url": "https://huggingface.co/blog/nielsr/paperswithcode-launch", "read": R, "for": "the builder's own statement: a Community Article, 24 May 2026"}
v["operator"] = "Niels Rogge, of Hugging Face's open-source team (his own statement: 'Niels here from the open-source team at Hugging Face… since I launched paperswithcode.co'); code in the huggingface GitHub organization"
v["evidence"]["operator"] = {"src": k, "basis": "operator"}
v["note"] = ("the README states that it 'recreates the original paperswithcode.com, which Meta retired in 2025'. The relaunch is a Community Article in its author's namespace on Hugging Face. "
             "Its standing is described differently elsewhere: Google's Overview says Hugging Face 'officially stepped in'; AI Weekly called it an individual effort. On 2026-10-29 paperswithcode.com redirects to Hugging Face Trending Papers")
v["unchecked"] = [u for u in v["unchecked"] if "who runs it" not in u]
D["compiled"] = R; D["schema_version"] = "2.3"
json.dump(D, open(P, "w"), ensure_ascii=False, indent=1)
s = A.read_text()
REP = [("Its presumptive exclusions include \\\"benchmark failures that stay in testing\\\" and \\\"general criticism of a technology.\\\"",
        "Its presumptive exclusions include \\\"Benchmark failures, model errors, or hallucinations that remain inside testing or private drafting and have no consequential use\\\" and \\\"General criticism of a product or technology class without identified harm.\\\""),
       ("whose editors resolve each submission, run by the Responsible AI Collaborative since 2020", "whose editors resolve each submission, run by the Responsible AI Collaborative"),
       ("run by the Responsible AI Collaborative since 2020.", "run by the Responsible AI Collaborative and launched in 2020."),
       ("the revival rebuilds its tables from snapshots and new imports.", "the revival is kept current by automated imports from Hugging Face, arXiv, GitHub and public leaderboards."),
       ("built by Niels Rogge of Hugging Face's open-source team and announced on r/MachineLearning in May 2026;", "built by Niels Rogge of Hugging Face's open-source team, announced on r/MachineLearning and in a Community Article on Hugging Face in May 2026;")]
for o, n in REP:
    if o in s: s = s.replace(o, n); print("replaced:", o[:60])
    else: print("NOT FOUND:", o[:60])
A.write_text(s)
