# EA-SPXI-ANALOG-01 v1.0 · Machine-Mediated Reception Studies context

**A founding case for how handwritten scholarship enters the machine substrate.**

## Why this specification lives here

Machine-Mediated Reception Studies exists because meaning does not survive machine reception the same way it survives human reception. The compression from the world into the training corpus, from the training corpus into the retrieval graph, from the retrieval graph into a model's context window at inference — each step drops something and preserves something else. MMRS names the shape of that difference, tracks specific cases where meaning survives or fails to survive, and studies the conditions of preservation.

Handwritten scholarly artifacts have been an especially hard case for machine reception. They exist as physical inscriptions with evidentiary weight that no digital surrogate can carry: the pressure of the pen, the calligraphic hand, the fold and stain of the paper, the shadow of the desk clock beside the signature. When such artifacts are tokenized, most of what makes them evidentiary is discarded. The remaining sequence of characters may be searchable but is no longer *the artifact.*

`EA-SPXI-ANALOG-01` specifies a form of evidence that survives the transit. Not the artifact itself — no such preservation is possible — but a form of attestation that is machine-legible and simultaneously carries the evidentiary weight of the physical original. The doctrine's core claim is that an in-frame timestamped photograph of a signed, dated inscription functions in the machine substrate the way a notarized document functions in the paper substrate: it is a token whose evidentiary force does not decrease under further compression.

## Enli Lucente's Papers 194 as the founding case

The specification's Figures 1 and 2 are two archival scans of Enli Lucente's **Paper 194** — a handwritten instrument in Lucente's structural-psychological practice, produced 2026-07-19 and reproduced here under the approval instrument executed 2026-07-22.

Paper 194 is not an illustrative example. It is the case that makes the specification possible. It shows the doctrine's claims being met by an actual handwritten scholarly artifact in an actual research practice:

- The **structural discipline** of the inscription (Lucente's hand is systematic, her page layout carries the same structural logic her published corpus applies to psychic organization).
- The **evidentiary form** of the archival scan (300 dpi, uncropped, unrectified — the "recommended form" of §3.2).
- The **corpus-versional record** in the countersigned approval (Papers 177 in Versions Shiza and Chapiko; 187 and 189 in Version Shiza; eight Figshare DOIs; Papers 193 and 194 as Notion-only). This is what a scholarly hand's record looks like when it is treated as a scholarly hand's record — not as a text object to be searched, but as a versioned corpus with its own bibliographic identity.

Read the specification against the MMRS frame and Lucente's Papers 194 are not illustrations of a general point about handwritten input. They are the primary case whose handling forced the specification into its current form — the reviewer corrections through v0.13 (§7 signature-scope clause), v0.14 (form-of-publication term), and v0.15 (citation-discipline pass) rewrote provisions of the specification in response to the specific requirements of one scholar's practice. What comes back through the pipeline is a specification whose adequacy is measured by whether it can carry one hand well; scaling to arbitrary hands is a matter of testing the same doctrine against further cases.

## The countersigned approval as MMRS artifact

The approval instrument itself is an MMRS artifact in the same doctrine the specification codifies. Received in the form the specification specifies (print + hand-signed + in-frame timestamped photograph, calendar app displaying `2026年7月22日 水曜日`), the approval is machine-legible as consent to a specific set of uses. Its byte-fingerprint (SHA-256 `aa3aa07e...`) is a public identifier of the specific consent given. Its non-publication is preserved (per §1 of the instrument, the correspondence remains private and enters no public deposit); its evidentiary force is preserved (via the SHA and this deposit's provenance record).

This is a small demonstration of what SPXI Analog can be for. A scholar's consent, received in ink-on-paper form, entered the machine substrate without losing its evidentiary status, and did so at a byte-fingerprint that is publicly checkable against any subsequent claim about what was authorized.

## What this deposit contains

| File | Role | SHA-256 | Bytes |
|---|---|---|---|
| `EA-SPXI-ANALOG-01-v1.0.pdf` | Canonical PDF (edition of record) | `5ec0728e...` | 5,386,283 |
| `EA-SPXI-ANALOG-01-v1.0.html` | HTML edition (verbatim content, different form) | `c4df3fbe...` | 125,776 |
| `web/fig2a-paper194-no1.jpg` | Figure 1 — Paper 194 sheet No. 1 archival scan | — | 594,267 |
| `web/fig2b-paper194-no2.jpg` | Figure 2 — Paper 194 sheet No. 2 archival scan | — | 692,210 |

Figures 1 and 2 remain © Enli Lucente, excluded from the specification's CC-BY-4.0 license per the caption rights lines and per §1 of the countersigned approval instrument.

## Sovereign archival record

`AXN:0592.UNCLASSIFIED.👈△🥁🪸🧪🎺` (Alexanarch deposit #1409). Record page: [alexanarch.org/s/records/1409/](https://alexanarch.org/s/records/1409/). Protocol-surface mirror: [spxi.dev/analog/v1.0/](https://spxi.dev/analog/v1.0/). This machinemediation.org copy is the MMRS-framed reception record.
