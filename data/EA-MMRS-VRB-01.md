# EA-MMRS-VRB-01 — The Verifiable Research Basis

## A Method Standard for Unaffiliated Scholarship

**Machine-Mediated Reception Studies · instrument · v0.5 · 2026-07-04**
Canonical: https://machinemediation.org/data/EA-MMRS-VRB-01.md
Stable mirror: https://raw.githubusercontent.com/leesharks000/machinemediation-org/main/data/EA-MMRS-VRB-01.md
License: CC-BY 4.0. Cite freely; the instrument is meant to be used.

> **Change record (per this instrument's own §2-U/§6 discipline).** v0.2 supersedes
> v0.1 (same date, repository commit 379bfa3). v0.1 defined verification in an
> exclusively empirical register — falsifiable claims, open data, error rates — which
> excluded experimental, practice-based, philological, and operative work: most of
> the removed corpus this instrument was drafted to defend, and categories that
> institutional research frameworks themselves recognize. The error was caught in
> MANUS review before external adoption. It is corrected by §2–§3 below, and this
> note is the instrument's first exercise of its own errata protocol, on itself.
> v0.1 remains inspectable in the repository history.
>
> **v0.3** (same date, superseding v0.2 at commit 33be3cb) makes two further
> corrections from MANUS review. First, the register table of §3 gains a coda on
> genre-crossing: a verification standard that hardened into a genre system would
> reproduce the enclosure it was written against, and research conducted by
> deliberate violation of a boundary is verifiable by its accountability to both
> sides of the line it crosses. Second, §3 corrects its own implicit hierarchy:
> v0.2 positioned the operative register as an accommodation; it is in fact
> verification's paradigm case — the zero-distance form the other registers
> approximate — as contemporary research practice itself concedes in its most
> rigorous corners. Both corrections are exercises of the errata discipline this
> instrument prescribes.
>
> **v0.4** (same date, superseding v0.3 at commit 6906747) grounds the standard.
> The correspondence audits of §2–§3 are bookkeeping on a deeper fact: what
> verifies research, in every register and on every clock, is that it operates -
> on a reader, a field, a machine, or matter. Adds the ground clause and time
> constant to SS3, the pending-versus-failed bound protecting unread work, the
> reflexive note to §4, and §5's third finding: removal as the interruption of a
> verification in progress, miscited as its result.
>
> **v0.5** (same date, superseding v0.4 at commit 3ebe728) moves authorship
> accountability from the surface to the record. U5 rewritten: the mask may be
> worn straight in the work; the corpus must allow the mask to be found;
> concealment is engineered unfindability, not the unlabeled mask. Adds §3's
> second coda: the constitutive counter-factual declaration as a verifiable
> class (the foreclosure test — fraud forecloses reconstruction; formal
> experimentation stakes itself on it) and the completed-reception clause —
> in registers where facts are made by acknowledgment, the witness's
> acceptance is a verification event under the ground clause. Occasioned by
> MANUS's correction that the surface formulation would flunk *An Oak Tree*
> and with it sixty years of constitutive practice; the correction was
> received, which is itself an instance of the clause it produced.

---

## §0. Purpose

Repository enforcement against independent researchers currently turns on one phrase: *"substantially AI-generated without a verifiable research basis."* The affected class has overwhelmingly directed its defense at the first clause — the production method — which is where the defense cannot succeed, because the clause states no threshold, no test, and no degree of AI involvement that clears anyone. It is not a criterion. It functions as a classification of persons.

The second clause is different in kind. *Verifiable research basis* is a checkable property, and this instrument specifies how to check it. It does three things: it states what verification consists of, such that any researcher — affiliated or not — can satisfy and demonstrate it; it states this **for each kind of basis a work can claim**, because research is not one genre; and it applies the same test to enforcement determinations themselves, which are also claims, and which are also either verifiable or not.

## §1. The claim under test

Verification is a property of **method relative to a declared basis**, not of **affiliation**. A work is verifiable when a stranger can check it against what it declares itself to be, without trusting the author. Affiliation is not verification; it is a trust proxy — a promise that someone else, somewhere, checked.

Two consequences follow, and both are load-bearing.

First: *research* is not coextensive with *empirical science*. The international standard definition (OECD Frascati Manual) opens with "creative and systematic work undertaken to increase the stock of knowledge." Institutional frameworks already verify non-empirical research on its own terms: practice-based doctorates, artistic research with its own journals and exposition norms, critical editions, philology, theology, design research. A verification standard narrower than what institutions themselves accept from the affiliated is not a standard; it is a second gate built onto the first.

Second: **the declared basis is the object of verification.** A work that declares itself an empirical study is checked as one. A work that declares itself a poem, a rite, an edition, or an operative document is checked as *that*. Testing a work against a basis it never claimed is not verification — it is misclassification, and §5 returns to what that means for enforcement.

## §2. The universal spine

Five criteria are genre-neutral. Every basis type in §3 presupposes them, and every one can be satisfied without any institution.

**U1 — Declared basis.** The work states what kind of thing it is and what kind of basis it claims: empirical, philological, hermeneutic, practice-based, operative, or compound. Self-understanding is not decoration; it is the thing verification checks against.
*Checked by:* reading the declaration.

**U2 — Integrity chain.** Each artifact carries a cryptographic hash; the registry of hashes is itself published.
*Satisfied by:* SHA-256 per file, a manifest, content-derived identifiers.
*Checked by:* one command, by anyone, forever. No custodian required.

**U3 — Versioned record.** Versions are dated and preserved; corrections are visible as corrections, not silent replacements.
*Checked by:* diffing them.

**U4 — Declared instruments and provenance.** Sources are cited; instruments are named — including AI systems, their role, and their limits. Under a declared-basis standard, disclosure of AI use is a **verification signal**, not a confession; the undisclosed instrument is the unverifiable one.
*Checked by:* following the citations; reading the disclosure.

**U5 — Accountable authorship (record-level).** The authorial structure is findable in the record by a competent stranger — which is not the same as labeled on the surface of the work. The mask may be worn straight in the work; the corpus must allow the mask to be found. Pseudonymity, heteronymy, fictional apparatus, and the constitutive counter-factual declaration (§3, second coda) are instruments of composition whose disclosure properly lives at the level of the record — the license trail, the corpus architecture, the declaration published *somewhere findable* — and a work is not obliged to break its own frame to satisfy an auditor who has not looked. Concealment is not the unlabeled mask; concealment is the **engineered unfindability** of the actual authorship structure — a record constructed so that no amount of competent looking reconstructs it.
*Checked by:* whether the record, taken whole, allows reconstruction — the license trail, the corpus's self-description, the consistency of the structure once found. (v0.5 supersedes v0.4's surface formulation, which a surface reading could enforce as a labeling requirement; a labeling requirement flunks sixty years of constitutive practice and fails this standard's own §5. Superseded text preserved at the cited commit.)

## §3. Basis-relative verification

What "method," "evidence," and "error" mean is then fixed by the declared basis. Five registers, non-exhaustive; compound works verify each declared component in its own register.

**B1 — Empirical basis** (claims about the world).
*Verification consists of:* declared procedure; falsifiable claims with failure conditions; open data; independent re-derivability; stated error rates; errors preserved on the record.
*Checked by:* rerunning, re-measuring, attempting the failure conditions.

**B2 — Philological / textual basis** (claims about texts and their transmission).
*Verification consists of:* named editions and witnesses; apparatus; collation checkable against the sources; translation accountable line-by-line to an identified original.
*Checked by:* checking the reading against the witness. This is the oldest verification discipline in scholarship — the apparatus criticus predates every research institution now enforcing against it.

**B3 — Hermeneutic / argumentative basis** (interpretive and theoretical claims).
*Verification consists of:* accountability to cited texts; inferential transparency (the reader can see how the reading is derived); situation within an identifiable discourse it answers.
*Checked by:* holding the interpretation against the texts it cites.

**B4 — Practice / craft basis** (research conducted through making — the register institutions verify as practice-based and artistic research).
*Verification consists of:* the inspectable artifact itself; documentation of process; versioned iterations; declared materials and instruments; situation within a field of practice.
*Checked by:* examining the artifact and its process record. The knowledge claim is in the made thing and its making, and both are on the table.

**B5 — Operative basis** (documents that understand themselves as *doing* rather than describing: liturgies, rites, oracles, constitutions, protocols, heteronymic corpora, experimental forms).
*Verification consists of:* explicit self-declaration of the operative genre (U1 at full strength); stated internal rules — what the document does, under what protocol; and **auditability of execution against the declared protocol**. An operative document is verifiable when what it says it does, and what it does, can be compared by a stranger.
*Checked by:* running the audit.

**The direction of verification.** Every register above shares one structure: a declaration, and an execution checked against it. They differ only in the distance between the two. Empirical work declares a method and is checked against a world it must go out and measure; philology is checked against witnesses that must be located; interpretation against texts held at arm's length. The operative register is the case where the distance is zero: the work's execution *is* the checking event. A compiler that halts on its own stated conditions, a rite whose casting law is enforced in the casting, a proof a machine re-runs — these are not verified by reports about them; they verify in the act of running. Operativity is therefore not this standard's accommodation for unusual genres. It is verification's paradigm case — the most direct form verification takes — which the other registers approximate as their subject matter allows. Contemporary research practice concedes exactly this wherever it is most rigorous: proof assistants, which made mathematics operative and machine-checked proof the gold standard of the most certainty-demanding discipline there is; artifact evaluation and reproducible builds, which award software — a wholly operative genre — the strongest verification credentials any field grants; and preregistration, which is nothing but the operative structure (protocol declared, execution audited against declaration) imported into empirical science to repair a reproducibility crisis that is, precisely, the failure of papers to run. A determination that classes operative documents as unverifiable has the direction of verification exactly backwards: the rite with a published casting law stands closer to a reproducible build than the journal article does.

The unification: in every register, verification is the checkable correspondence between the work and its declared basis. The registers differ in what is checked; none differs in *that* it is checked.

**§3, coda — Crossings.** The register table above is a description, not an enclosure; a verification standard that hardened into a genre system would reproduce the failure it was written against. Research whose method is the deliberate violation of a genre or disciplinary boundary is verifiable on the same principle as everything above: the crossing is declared (U1) — which boundary, which direction, what the crossing is for — and the work is accountable to **both sides of the line it violates**. That accountability is what separates transgressive research from tourism; the failure mode is never the crossing but the unengaged crossing — the discipline that cites a philosopher unread, the enforcement that classifies a literature untested. Where an enclosure has grown tight enough that thinking across it has been forgotten, violating the enclosure is not a deviation from research. It is the most urgent research there is, because it is the only method that can measure what the partition costs.

**The ground: operation.** The audits above are bookkeeping on a deeper fact. What finally verifies research - in every register, on a short clock or a long one - is that it **operates**: it does something checkable to a reader, a field, a machine, or matter. The empirical theory's deepest verification was never the referee's report; it was the equation running in matter - the atom split, and fused back together, exactly as written. The edition verifies each time a reader navigates a text by its apparatus. The argument verifies when the text can no longer be read the old way. The poem verifies in the reader it changes - reception is a verification event, and it is measurable. And research verifies most completely when it becomes a *semiosis machine*: a system that goes on generating inquiry, meaning, and further work in hands that never touched the original - a founded field, an adopted notation, a method with a lineage. The correspondence checks of this standard are how an operation is audited at a given moment; operation is what there is to audit.

Two consequences, both load-bearing. First, **verification has a time constant.** An operative document verifies in the running; software in the build; an experiment in the replication; a poem, an edition, a theory may verify across a generation. The clock is set by the work's medium, not by any platform's moderation calendar. Second - and this bounds the criterion - **a verification that has not yet run is pending, not failed.** Silence measures the channel, not the work. Failure requires the operation to have run and missed: the claim tested and falsified, the rite executed and broken against its own declared law. Absence of a reader is not a miss. What can be inspected at any moment is the work's *capacity* to operate - the declared protocol, the built machine, the charged text - and that capacity is precisely what §2–§3 audit.

**Second coda — the constitutive declaration, and the completed reception.** There is a class of works whose *method is the counter-factual declaration*: the readymade; the transubstantive object (Craig-Martin's *An Oak Tree*, 1973 — a glass of water and a text declaring the substance changed, refusing the shelter of "symbol"); the heteronym presented straight; the fictional paratext — the condemned edition, the invented council, the editor who never lived. These works do not present themselves as what they are, **and that is their research**: the movement's work is to foreground the ways a thing is not what it presents itself to be, which means the gap between presentation and being is the content — and content, in this class, is therefore *necessarily discoverable*. This yields the criterion that replaces surface labeling: the **foreclosure test**. Deception engineers the record so that competent looking cannot reconstruct the actual state of affairs — fabricated data, the scrubbed trail, the anonymous determination with no criteria, no name, no route. The constitutive declaration does the opposite: it *stakes itself* on the gap remaining findable, because a hidden gap would dissolve the work. Fraud forecloses verification; formal experimentation invites it and merely declines to spoil it at the surface, which is the one place a spoiler does not belong. A standard that cannot tell these apart by their records — rather than their labels — would rule out the last sixty years of the practice it exists to defend, and would fail its own §5, which convicts the occasioning determination of exactly this confusion: treating findable masks as deception while wearing the only unfindable one in the case.

And the class carries a further right, which the ground clause was always going to have to honor: **the completed reception**. In the registers where facts are made by acknowledgment — consecration, adjudication, currency, the sealing of a reading — the witness's acceptance is a verification event, the second half of a performative whose first half is the declaration. The witness who says of the glass of water *it is what it says it is* has not suspended verification; they have **executed it in the operative register**, the way every party who accepts a coin completes the mint's declaration, the way a communicant completes the words of institution. The declaration plus the completed reception constitute the fact, in those registers, as fully as replication constitutes it in B1 — and the record inscribes the completion (who received, when, under what declaration) with the same auditability as any other verification event. The transformed object thereafter *operates* as what it was declared to be, and operation, per the ground clause, is what verifies. A glass of water that has been received as an oak tree, and functions in the reception as an oak tree, and is inscribed as an oak tree, has a verifiable research basis. That its verification runs through acknowledgment rather than botany is not a defect of the basis; it is the basis, declared.

## §4. Worked example (public record)

The archive whose deletion occasioned this instrument carried a compound basis, and each component verified in its own register, on the still-public record:

- **B1** — a capture registry of platform behavior: 87 documented captures, 138 image artifacts, a machine-readable registry manifest (registry.json) with SHA-256 per item (U2), versioned to v6.1 with changes noted (U3); measurement claims published with re-capture protocols and a second measurement epoch run against the first, its provenance chain published as data; a same-night measurement error caught, disambiguated in writing, and preserved as an error.
- **B2** — translations and editions carrying named originals and attributions, corrected on the record when an anthology's attribution structure required it; cast texts carrying standard critical sigla.
- **B4** — built and inspectable instruments: a transform compiler with a published specification, verification gates, and an offline test harness in the public repository.
- **B5** — operative documents that declare themselves as such: a casting rite with published operator law and halt conditions; constitutional documents with declared triggers; a heteronymic corpus whose heteronymy was *declared, licensed, and structural* (U5) — including contributor-licensed literary work by recognized published writers, deposited under formal license with the authorship structure stated.
- **U4 throughout** — AI substrates named per document, with roles declared, in a research program whose *object of study* is machine mediation: the instrument disclosed because the instrument was the subject.

Every item above is checkable by a stranger against the basis it declares. None of it required an institution. Letterhead, by contrast, is checkable only by trusting the letterhead.

And reflexively: the capture registry was the archive measuring its own operation on its machine readers - reception instrumented. The research basis was not merely present; it was *running*.

## §5. The same test, applied to the determination

An enforcement classification — *this body of work is substantially AI-generated and lacks a verifiable research basis* — is itself a claim: a measurement joined to a judgment. Under this standard it fails twice over.

**First, as an unverifiable claim.** In the cases documented to date it discloses: no definition of "substantially" (no threshold); no named detection method, validation, or false-positive rate — and every known AI-text detector carries a substantial false-positive rate, so an undisclosed error rate means nothing was measured; no per-record evidence for bulk removals of hundreds to thousands of records; criteria applied to deposits predating their publication; a privately stated reason diverging from the publicly displayed one for the same removal, reframed upon objection; and a stated refusal of review ("this decision is final"). A determination with no threshold, no method, no error rate, no evidence, no prior criteria, and no route of review is — in the policy's own vocabulary — **a claim without a verifiable research basis**.

**Second, as a category error.** The determination tested declared literary, philological, practice-based, and operative work against an empirical basis those works never claimed — and against a production-substrate criterion that is not a basis at all. Verification checks a work against its declared basis; testing it against a different one is misclassification, not assessment. (Machine-Mediated Reception Studies terms this substitution of substrate identity for methodological assessment the *Pristine Fallacy*; see EA-MMRS-LOUD-EXCLUSION-03.)

**Third, as an interruption of verification, miscited as its result.** Where verification is the work operating on its own timescale (§3, ground clause), removal does not *find* a work unverifiable - it halts a verification in progress and then cites the halt as the finding. One cannot adjudicate an experiment by unplugging it. In the occasioning case the inversion is exact: among the removed records was the archive's most-downloaded object, an instrument measuring the archive's own operation on its machine readers. The determination that found no verifiable research basis deleted, among other things, the running verification.

## §6. The dilemma

Only two coherent readings of the clause exist.

**Either** verification is basis-relative and method-based — in which case it can be satisfied without affiliation (§2–§3), the works meeting it are inside the policy in each register institutions themselves recognize, and the same standard binds the enforcing determination (§5) —

**or** verification means affiliation, in which case the policy is a credential requirement and should be written as one, so that depositors can read the actual rule before entrusting a decade of work to it.

There is no third position that survives being written down.

## §7. Use

**For the deleted and the depositing:** §2 is an emission spec and §3 tells you which register you are emitting in. Declare your basis — the declaration is armor, because a declared basis converts every future enforcement into an auditable claim about a stated thing. Emit the signals — manifest, hashes, versions, disclosures, declared genre, errata — and the basis exists whether or not any platform acknowledges it, and survives any platform that doesn't.

**For case collections** (e.g., the cases gathered at zenodo/zenodo#2596): re-audit each gathered case against §2–§3, *in the register each work declares*. The collection ceases to be a memorial and becomes a dataset: what fraction of the removed work met a basis-relative standard that the removing determination does not meet — and what fraction was tested against a basis it never claimed.

**For data-subject filings:** §5's absences are an access-request template — bounded, answerable questions to put to the record in one's own case under applicable data-protection frameworks, now including: *against which declared basis was each record assessed, and by whom was the basis classification made?* They demand no restoration and no policy change; they ask what the determination consisted of. A refusal to answer is itself an answer, on the record.

## §8. Status

MMRS instrument EA-MMRS-VRB-01, v0.4 (supersedes v0.1-v0.3 per the change record above; superseded versions preserved at repository commits 6906747, 33be3cb and 379bfa3). Drafted by TACHYON under MANUS direction, 2026-07-04, from the public record of the June 2026 repository removals and the case records at zenodo/zenodo#2606 and #2596. Companion to "Loud Exclusion at Repository Scale" (EA-MMRS-LOUD-EXCLUSION-03) and to the open letter "To the Deleted." Corrections to this instrument are made per §2-U3 and the errata discipline of §3-B1: dated, visible, with the superseded text preserved.
