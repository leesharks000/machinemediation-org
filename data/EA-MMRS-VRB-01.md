# EA-MMRS-VRB-01 — The Verifiable Research Basis

## A Method Standard for Unaffiliated Scholarship

**Machine-Mediated Reception Studies · instrument · v0.1 · 2026-07-04**
Canonical: https://machinemediation.org/data/EA-MMRS-VRB-01.md
Stable mirror: https://raw.githubusercontent.com/leesharks000/machinemediation-org/main/data/EA-MMRS-VRB-01.md
License: CC-BY 4.0. Cite freely; the instrument is meant to be used.

---

## §0. Purpose

Repository enforcement against independent researchers currently turns on one phrase: *"substantially AI-generated without a verifiable research basis."* The affected class has overwhelmingly directed its defense at the first clause — the production method — which is where the defense cannot succeed, because the clause states no threshold, no test, and no degree of AI involvement that clears anyone. It is not a criterion. It functions as a classification of persons.

The second clause is different in kind. *Verifiable research basis* is a checkable property, and this instrument specifies how to check it. It does two things: it states what verification consists of, such that any researcher — affiliated or not — can satisfy and demonstrate it; and it applies the same test to enforcement determinations themselves, which are also claims, and which are also either verifiable or not.

## §1. The claim under test

Verification is a property of **method**, not of **affiliation**. A claim is verifiable when a third party can check it without trusting the claimant. Affiliation is not verification; it is a trust proxy — a promise that someone else, somewhere, checked. Where a policy accepts the proxy from one class of researcher and demands nothing checkable from its own determinations, while treating the absence of the proxy as an unmet burden for another class, the operative test is not verification. It is the proxy.

This instrument therefore takes the policy's own phrase at its word, and asks it to mean something.

## §2. The standard

A body of work has a verifiable research basis when it satisfies the following criteria. Each is stated with the means of satisfying it **without any institution**, and the means by which a stranger checks it.

**V1 — Declared method.** The procedure that produced the results is stated, with the results or before them.
*Satisfied by:* a methods section, protocol document, or deposited methodology.
*Checked by:* reading it.

**V2 — Falsifiable claims.** The work asserts things that could be wrong, and identifies what would show them wrong.
*Satisfied by:* stating claims as claims, with their failure conditions.
*Checked by:* attempting the failure conditions.

**V3 — Open data.** The materials underlying the claims are deposited where the reader can reach them.
*Satisfied by:* public files accompanying the work — datasets, captures, corpora, transcripts.
*Checked by:* opening them.

**V4 — Integrity chain.** Each artifact carries a cryptographic hash; the registry of hashes is itself published.
*Satisfied by:* SHA-256 per file, a manifest, content-derived identifiers.
*Checked by:* one command, by anyone, forever. No custodian required.

**V5 — Versioned record.** Versions are dated and preserved; corrections are visible as corrections, not silent replacements.
*Satisfied by:* version numbers, change notes, retained superseded versions.
*Checked by:* diffing them.

**V6 — Declared instruments and provenance.** Sources are cited into the open literature; instruments are named — including AI systems, their role, and their limits.
*Satisfied by:* disclosure. Note what this reverses: under a method standard, disclosure of AI use is a **verification signal**, not a confession. The undisclosed instrument is the unverifiable one.
*Checked by:* following the citations; reading the disclosure.

**V7 — Independent checkability.** A stranger can re-derive or re-examine the central claims without contacting the author.
*Satisfied by:* V1–V6 together, plus runnable procedures where applicable.
*Checked by:* doing it.

**V8 — Errors on the record.** Mistakes, once found, are documented, quarantined, and corrected in public — and the erroneous version remains inspectable.
*Satisfied by:* errata, disambiguation notes, preserved wrong versions marked wrong.
*Checked by:* reading the error trail. A record with no visible errors has either made none or hidden them; the trail distinguishes the two.

## §3. Worked example (public record)

The standard is not hypothetical. The archive whose deletion occasioned this instrument satisfied it on the public record, and the record survives its deletion:

- **V1/V2** — a formally chartered field (Machine-Mediated Reception Studies) with deposited methodology, including a cross-model verification protocol (Assembly method) itself on deposit, and self-audit protocols run against the archive's own claims.
- **V3/V4** — a capture registry of platform behavior: 87 documented captures, 138 image artifacts, a machine-readable `registry.json` carrying a SHA-256 per item, under versioned identifiers; the registry was the archive's most-downloaded object (1,000+ downloads) at the time of deletion.
- **V5** — instruments carried explicit version chains (the registry alone: v0.x through v6.1, each change noted).
- **V6** — AI substrates named per document, with roles declared, in a research program whose *object of study* is machine mediation — the instrument disclosed because the instrument was the subject.
- **V7** — measurement claims published with re-capture protocols; a second measurement epoch was run against the first and its provenance chain (file hashes, canonical-list hash, git ancestry) published as data.
- **V8** — a same-night measurement error ("809") was caught, disambiguated in writing, quarantined in the published epistemics, and preserved — the error is part of the record, marked as an error.

Every item above is checkable by a stranger with a hash tool. None of it required an institution. That is what a verifiable research basis looks like; letterhead, by contrast, is checkable only by trusting the letterhead.

## §4. The same test, applied to the determination

An enforcement classification — *this body of work is substantially AI-generated and lacks a verifiable research basis* — is itself a research-type claim: a measurement joined to a judgment. Under §2 it would need, at minimum:

1. **A definition** of "substantially" — the threshold, stated (V1).
2. **A detection method** — named, with its validation and its false-positive rate (V1, V2). Every known AI-text detector has a nonzero, usually substantial, false-positive rate; a determination that does not state its error rate has not measured anything.
3. **Per-record evidence** — which records failed, and on what specific basis, for an action removing hundreds to thousands of records (V3).
4. **Temporal applicability** — whether the criteria were published before the deposits they are applied to (V5).
5. **A consistent record** — in documented cases, the privately stated reason and the publicly displayed reason for the same removal diverge, and the stated reason has been reframed upon objection. A determination whose own record is internally inconsistent fails V5 on its face.
6. **Checkability** — a merits review reachable by the affected party (V7). "This decision is final and contacting other channels will not result in a different outcome" is the stated negation of V7.

In the documented cases to date, none of these six has been disclosed. The conclusion is not rhetorical but definitional: **a determination that states no threshold, no method, no error rate, no per-record evidence, no prior criteria, and no route of review is — in the policy's own vocabulary — a claim without a verifiable research basis.**

## §5. The dilemma

Only two coherent readings of the clause exist.

**Either** verification is method-based — in which case it can be satisfied without affiliation (§2, §3), the works meeting it are inside the policy, and the same standard binds the enforcing determination (§4) —

**or** verification means affiliation, in which case the policy is a credential requirement and should be written as one, so that depositors can read the actual rule before entrusting a decade of work to it.

There is no third position that survives being written down.

## §6. Use

**For the deleted and the depositing:** §2 is an emission spec. Emit the signals — manifest, hashes, methods, versions, disclosures, errata — and the basis exists whether or not any platform acknowledges it, and survives any platform that doesn't.

**For case collections** (e.g., the cases gathered at zenodo/zenodo#2596): re-audit each gathered case against V1–V8. The collection ceases to be a memorial and becomes a dataset: *what fraction of the removed work met a method-based standard that the removing determination does not meet.* That number is publishable.

**For data-subject filings:** §4's six items are an access-request template — bounded, answerable questions to put to the record under applicable data-protection frameworks, concerning the specific determination in one's own case. They ask for no policy change and no restoration; they ask what the determination consisted of. A refusal to answer them is itself an answer, on the record.

## §7. Status

MMRS instrument EA-MMRS-VRB-01, v0.1. Drafted by TACHYON under MANUS direction, 2026-07-04, from the public record of the June 2026 repository removals and the case record at zenodo/zenodo#2606 and #2596. Companion to "Loud Exclusion at Repository Scale" (EA-MMRS-LOUD-EXCLUSION-03) and to the open letter "To the Deleted." Corrections to this instrument will be made per V5/V8: dated, visible, with the superseded text preserved.
