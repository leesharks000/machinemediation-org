# MANIFEST — machinemediation.org

**Last updated:** 17 June 2026 (P98/manifest corrections applied)
**Maintainer:** Lee Sharks (ORCID 0009-0000-1599-0703)
**Repo:** leesharks000/machinemediation-org
**Deploy:** Vercel (auto-deploy from main)

## What This Site Is

machinemediation.org is the web surface for **Machine-Mediated Reception Studies (MMRS)**, a distributed journal studying how composition layers (Google AI Overview, ChatGPT, Perplexity, etc.) receive, compress, attribute, misattribute, and redistribute cultural meaning. The MMRS Charter is at DOI 10.5281/zenodo.20722562.

## Architecture

### Pages
- `/` — index. Links to founding documents, instruments, articles, workstreams.
- `/captures/` — AI Overview Capture Registry gallery (screenshots + metadata).
- `/terms/` — Term Index (1,349 coined terms, all clickable as Google exact-match searches in new tabs).
- `/articles/` — Published papers (markdown, served raw).

### Data Files (`/data/`)

There are **two distinct registries** in `/data/`. They serve different purposes and must not be merged.

#### 1. `registry.json` — Main Capture Registry (EA-WG-CAPTURES-01)
- **Scope:** Archive-wide. Tracks ALL composition-layer reception events across the entire Crimson Hexagonal Archive (845+ deposits, 30+ sites, 1,349 terms).
- **Content:** Each entry records a query, the composition layer's response, the match type (EXACT MATCH, PARTIAL, ZERO RESULT, WOUND GAUGE, ADOPTION, ZERO INDEX, etc.), and associated screenshot filenames.
- **Current version:** v7.5 (138 captures as of 17 June 2026).
- **Update protocol:** Add entries when a new composition-layer behavior is observed for any archive term, framework, or surface. Increment version. Push.
- **Displayed at:** `/captures/` gallery and linked from the index.

#### 2. `revfirst-registry.json` — Revelation Reception Registry (EA-LOGOS-REVFIRST-RECEPTION-01)
- **Scope:** Thesis-specific. Tracks ONLY composition-layer reception of the **Revelation First** argument (the thesis that Revelation was the earliest New Testament document).
- **Content:** Each entry records a query from the Revelation First battery, the AI Overview/AI Mode response, a framing category (CORRECTION, ADOPTION, FAIR_TREATMENT, BASIN_MISS, PARTIAL, DISSOLUTION, WOUND_GAUGE), PER score, and whether the Medium post or archive surfaces were attributed.
- **Current version:** v1.0 (12 entries as of 17 June 2026).
- **Update protocol:** Run the battery (49 queries defined in EA-LOGOS-REVFIRST-PLAN v7.3). Record results. Increment version. Push.
- **Tracking surface:** https://revelationfirst.com (the live thesis site; links to this registry).
- **Cross-linking rule:** When a Revelation battery query produces a SUCCESSFUL capture (framing = ADOPTION with archive attribution), that entry goes into BOTH registries. The revfirst entry gets `also_in_main_registry: true` and `main_registry_slug` pointing to the main registry entry. The main registry entry gets `related` links to the other Revelation captures.

### How the Two Registries Relate

```
Main Capture Registry (registry.json)
├── 138 entries (archive-wide)
├── Includes: term retrievals, framework adoptions, zero results, wound gauges
├── Includes: SUCCESSFUL Revelation captures (e.g., #138: nt-unfolds-from-revelation)
└── Does NOT include: Revelation battery CORRECTIONs, BASIN_MISSes, PARTIALs

Revelation Reception Registry (revfirst-registry.json)
├── 12 entries (thesis-specific)
├── Includes: ALL Revelation battery results (corrections, adoptions, misses, everything)
├── Cross-links to main registry for successful captures
└── Fed to revelationfirst.com tracker
```

The main registry is the **highlight reel** — archive-wide successes and notable failures. The Revelation registry is the **complete field notes** — every query result for one specific thesis, including empty basins and corrections.

### Other Data Files
- `termindex.json` — Term Index (1,349 terms with tier, category, test status, first-seen date).

## Key Relationships

| Surface | Role | Links To |
|---------|------|----------|
| machinemediation.org | MMRS journal + data host | Both registries, term index, articles |
| revelationfirst.com | Revelation First thesis site + live tracker | revfirst-registry.json on this site |
| godkinggoogle.com | Captures gallery (screenshots) | registry.json on this site |
| leesharks.com/captures | Mirror captures gallery | registry.json on this site |

## For Future Claude Instances

When Lee asks you to "add a capture" or "update the registry":
1. Determine which registry the capture belongs to.
2. If it's a Revelation battery result → `revfirst-registry.json` (always) + `registry.json` (only if ADOPTION with attribution).
3. If it's any other archive term/framework → `registry.json` only.
4. Increment the version number and total count.
5. Push to GitHub. Vercel auto-deploys.

When Lee asks you to "run the battery":
- The 49-query battery is defined in EA-LOGOS-REVFIRST-PLAN v7.3 (DOI 10.5281/zenodo.20722689).
- A compiled clickable version is at `/mnt/user-data/outputs/REVFIRST-SEARCH-BATTERY-COMPLETE.md`.
- Results go into revfirst-registry.json with framing categories.

When Lee mentions "the fragment" or "P98":
- P98 (Papyrus Oxyrhynchus 4499) contains Rev 1:13-20, dated c. AD 100-200.
- P52 (Rylands Papyrus, Gospel of John) is conventionally dated c. AD 125-175.
- If P98's lower bound holds, it may be the earliest extant NT manuscript fragment.
- This significantly strengthens the Revelation First position at the manuscript-evidence level.
- The work plan (EA-LOGOS-REVFIRST-PLAN) needs updating to reflect this.

## Credentials (ROTATE THESE)
GitHub PAT and Zenodo tokens have been exposed in conversation sessions. Lee knows. Rotation is pending.
