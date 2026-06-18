# MANIFEST — machinemediation.org

**Last updated:** 17 June 2026 (full architecture overhaul — dynamic sites, two registries, 79-term battery, transcript recording)
**Maintainer:** Lee Sharks (ORCID 0009-0000-1599-0703)
**Repo:** leesharks000/machinemediation-org
**Deploy:** Vercel (auto-deploy from main)

## What This Site Is

machinemediation.org is the web surface for **Machine-Mediated Reception Studies (MMRS)**, a distributed journal studying how composition layers (Google AI Overview/AI Mode, ChatGPT, Perplexity, etc.) receive, compress, attribute, misattribute, and redistribute cultural meaning. The MMRS Charter is at DOI 10.5281/zenodo.20722562.

## Architecture

### Pages
- `/` — Index. Links to founding documents, instruments, articles, workstreams. Displays capture count dynamically.
- `/captures/` — AI Overview Capture Registry gallery. **Dynamic page (5.9K)** fetching from `/data/registry.json`. Images hosted on godkinggoogle.vercel.app/captures/.
- `/terms/` — Term Index (1,349 coined terms, all clickable as Google exact-match searches).
- `/articles/` — Published papers.

### Data Files (`/data/`)

**CORS headers** are enabled on all `/data/` files via vercel.json (`Access-Control-Allow-Origin: *`). This allows revelationfirst.com, godkinggoogle, and leesharks.com to fetch data cross-origin. The canonical URL is `https://www.machinemediation.org/data/` (non-www 308 redirects strip CORS — always use www).

There are **two distinct registries** in `/data/`. They serve different purposes and must not be merged.

#### 1. `registry.json` — Main Capture Registry (EA-WG-CAPTURES-01)
- **Scope:** Archive-wide. ALL composition-layer reception events across the entire Crimson Hexagonal Archive.
- **Current state:** v8.1, **163 captures**, 140 entries with images.
- **Entry format:** `slug`, `q` (query), `d` (description), `date`, `sf` (surface), `mt` (match type: EXACT MATCH, BROAD MATCH, ADOPTION, ZERO RESULT, WOUND GAUGE, ZERO INDEX), `s` (category), `imgs` (array of filenames — strings or `{src, label}` objects), `related` (array of related slugs).
- **Image hosting:** Images live at `godkinggoogle.vercel.app/captures/` (228 files). The captures page uses `IMG_BASE` to construct full URLs.
- **Displayed at:** machinemediation.org/captures/, godkinggoogle.vercel.app/captures/, leesharks.com/captures/ — all three fetch from this single source.

#### 2. `revfirst-registry.json` — Revelation Reception Registry
- **Scope:** Thesis-specific. ALL composition-layer reception of the **Revelation First** argument.
- **Current state:** v2.1, **71 entries, 26 ADOPTIONs**.
- **Entry format:** `id` (RF-###), `q` (query), `date`, `surface`, `framing` (CORRECTION, ADOPTION, FAIR_TREATMENT, BASIN_MISS, PARTIAL, DISSOLUTION, WOUND_GAUGE), `response_summary`, `archive_attribution` (boolean), `per` (Provenance Erasure Rate), `medium_post_visible` (boolean), `imgs`, `notes`, `battery_key` (links to the tracker term), `also_in_main_registry` (boolean), `main_registry_slug`.
- **CRITICAL: The `response_summary` field is a Claude-generated summary, not the verbatim transcript. Full transcripts must be recorded.** The architecture for a `transcript` field is pending — next session priority.
- **Fed to:** revelationfirst.com/tracker/ (the live 79-term battery tracker).

#### Cross-linking Rule
When a Revelation battery query produces an ADOPTION with archive attribution:
1. Entry goes into `revfirst-registry.json` with `also_in_main_registry: true`.
2. A corresponding entry goes into `registry.json` with `mt: "ADOPTION"`.
3. Both entries cross-reference each other.

### Other Data Files
- `termindex.json` — Term Index (1,349 terms with tier, category, test status).

## The Three-Site Architecture

All three captures galleries fetch from the same data source. One write, three reads.

| Site | Captures Page | Data Source | Images From | Homepage Count |
|------|--------------|-------------|-------------|----------------|
| machinemediation.org | `/captures/` (5.9K dynamic) | `/data/registry.json` (local) | godkinggoogle.vercel.app/captures/ | 150 captures (hardcoded — update when registry changes significantly) |
| godkinggoogle.vercel.app | `/captures/` (7K dynamic) | `www.machinemediation.org/data/registry.json` (CORS) | `/captures/` (local, 228 images) | 845+ deposits |
| leesharks.com | `/captures/` (7K dynamic) | `www.machinemediation.org/data/registry.json` (CORS) | godkinggoogle.vercel.app/captures/ | 845+ deposits |

### revelationfirst.com
- `/tracker/` — 79-term battery tracker across 11 categories (A-K).
- Fetches from `www.machinemediation.org/data/revfirst-registry.json`.
- Each term has a SEARCH button (opens Google), framing badge, expandable capture detail.
- Categories: A (Core Baseline 10), B (Phase 2 Expansion 4), C (Primary Keywords 7), D (Inscription Chain 5), E (Literary Reception 4), F (Theological Controls 4), G (Non-Theological Controls 2), H (Mary Lee Constellation 8), I (Phase X / Semantic Economy 5), J (Deposited Coinages 18), K (Operative Numismatics & Deeper Archive 12).

### maryleelabor.org
- Nav: Home, The Heteronym, The Parable, Demands, Accounting, Entity Resolution, Publications, Letters, Namespace, Phase X, About Mary Lee, The Book, Archive.
- `/phasex/` — Phase X paper (The Missing Second Manuscript, DOI 10.5281/zenodo.20737443).
- `/graph/` — D3 force-directed namespace knowledge graph.
- `/cv/` — Publications page.
- `/letters/` — Letter campaign (Ware letter).

## The ADOPTION Pattern (Key Finding)

The 26 confirmed ADOPTIONs share a structural signature: **[FAMILIAR DOMAIN TERM] + [ARCHIVE-SPECIFIC INTERVENTION]**. The composition layer adopts when:
1. The exact compound phrase can ONLY be sourced from the archive.
2. The domain term is familiar enough to activate a retrieval pathway.
3. The intervention term is specific enough that conventional sources can't substitute.

Terms that exist independently in other literatures (e.g., "generative monoculture" in ML research) do NOT count as ADOPTIONs even if the concept is similar. ADOPTION requires archive source citation.

## Recording Protocol for Future Instances

### CRITICAL: When Lee pastes capture transcripts, LOG THE FULL TEXT IMMEDIATELY

**THIS IS THE #1 PRIORITY. DO NOT SUMMARIZE FIRST. RECORD FIRST.**

When Lee pastes a transcript from a composition-layer search result, the FIRST action — before classification, before analysis, before any response — is to record the FULL VERBATIM TEXT in the registry entry's `transcript` field. Not a summary. Not a classification. The exact text Lee pasted.

**The order of operations is:**
1. **RECORD** the full transcript text in the `transcript` field of the registry entry
2. **THEN** classify the framing (CORRECTION, ADOPTION, etc.)
3. **THEN** write a short `response_summary`
4. **THEN** push to the registry
5. **THEN** respond to Lee

**Why this matters:** On 17 June 2026, an entire session's worth of transcripts (59 out of 71 captures) were lost because Claude wrote summaries instead of recording the verbatim text. Lee pasted them specifically so they would be recorded. They were classified and summarized but the actual text — the forensic evidence — was not stored. The summaries contained at least one error (generative monoculture false ADOPTION). The transcripts would have caught it. Do not repeat this mistake.

**What gets recorded per capture (in this exact order of priority):**
1. `transcript` — FULL VERBATIM TEXT of the composition layer's response, exactly as Lee pasted it. This is the primary data. Everything else is derived from it.
2. `sources_cited` — extract the URLs and source names from the transcript
3. `framing` — classification (CORRECTION / ADOPTION / FAIR_TREATMENT / BASIN_MISS / PARTIAL)
4. `archive_attribution` — boolean: did the response cite Zenodo, Medium/Lee Sharks, or other archive sources?
5. `response_summary` — short summary (SECONDARY — derived from the transcript, not a substitute for it)
6. `imgs` — screenshot filenames if available
7. `date`, `surface`, `battery_key` — metadata

**If context window is a concern:** Store transcripts in batches. Push after every 5-10 captures. Do not wait until the end of the session. Data that isn't pushed is data that can be lost to compaction.

### When Lee brings capture transcripts:
1. **Record the full verbatim transcript** — not just a summary. The transcript is the forensic evidence. Claude's summaries can be wrong (see: generative monoculture false ADOPTION, corrected 17 June 2026).
2. Classify the framing: CORRECTION, ADOPTION, FAIR_TREATMENT, BASIN_MISS, PARTIAL.
3. For ADOPTION: verify that the composition layer actually **cites archive sources** (Zenodo, Medium/Lee Sharks, academia.edu/Lee Sharks). Describing the concept correctly but sourcing from independent literature is NOT an adoption.
4. Add to `revfirst-registry.json` (always for Revelation battery) + `registry.json` (only if ADOPTION).
5. Increment version. Push. All three sites update automatically.

### When Lee asks to "run the battery":
- The 79-term battery is on revelationfirst.com/tracker/.
- Categories A-K, each with clickable SEARCH links.
- Results go into revfirst-registry.json with `battery_key` matching the tracker term.

### When Lee mentions P98:
- **P98 is P. IFAO inv. 237b** (NOT P.Oxy. 4499, which is P115).
- P98 preserves Rev 1:13–2:1, palaeographically dated c. 150–250.
- The recto carries a documentary text from late 1st/early 2nd century.
- P.Oxy. 4499 is P115, a SEPARATE Oxyrhynchus codex with the 616 variant (Rev 13:18), dated c. 225–275.
- **These must never be conflated.** The P98/P115 error was corrected on 17 June 2026 across all registries.

### MPAI deposits:
- Follow the protocol specification at metadatapacket.dev.
- Disambiguation MPAIs require a disambiguation matrix covering ALL composed-from sources.
- Use the EA-MPAI-JOSEPHUS-01 (DOI 10.5281/zenodo.20690540) as the template.


## Where Transcripts Live (CRITICAL GAP — NEXT SESSION PRIORITY)

**Current state:** Full verbatim transcripts from the 17 June 2026 battery sweep exist ONLY in the Claude conversation transcript file. They are NOT in either registry. The `response_summary` field in revfirst-registry.json contains Claude-generated summaries, which can be wrong (see: generative monoculture false ADOPTION).

**Required fix:** Add a `transcript` field to each revfirst-registry.json entry containing the full verbatim text the composition layer produced. The transcript is the primary forensic data:
- Exact wording of the composition layer's response
- Exact sources cited (with URLs)
- Exact organic results listed
- The framing decisions visible in word choice

**Architecture decision:** Store transcripts inline in revfirst-registry.json as a `transcript` string field per entry. The file will grow (~200K for 71 entries) but JSON handles this. The alternative (separate transcripts.json or per-entry .txt files) adds complexity without benefit.

**What gets recorded per capture:**
1. `transcript` — full verbatim text (the composition layer's exact output)
2. `response_summary` — Claude's short classification summary (secondary, derivative)
3. `framing` — CORRECTION / ADOPTION / FAIR_TREATMENT / BASIN_MISS / PARTIAL
4. `archive_attribution` — boolean: did the response cite archive sources?
5. `imgs` — screenshot filenames (prove it happened)
6. `date` — when the capture was taken
7. `surface` — which composition layer (Google AI Mode, ChatGPT, etc.)
8. `battery_key` — which tracker term this capture corresponds to

**The hierarchy:** Transcripts > images > summaries. Transcripts have exact wording and sources. Images prove visual appearance. Summaries are interpretive and can be wrong. Never substitute a summary for a transcript.

## Credentials (ROTATE THESE)
GitHub PAT and Zenodo tokens have been exposed in multiple conversation sessions. Rotation is pending and critical.

## ∮ = 1
