---
name: ors-open-science-preprints
display_name: "Preprints: Servers, Licensing, and Journal Transfer"
description: Use when choosing a preprint server (bioRxiv, medRxiv, ChemRxiv, SSRN, arXiv), selecting a license (CC-BY vs CC-BY-NC-ND), versioning, scoop protection, or planning journal transfer with In Review / Reviewed Preprint services.
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: open-science
tags: [preprints, biorxiv, medrxiv, open-access, licensing, scoop-protection, journal-transfer]
difficulty: beginner
prerequisites:
  tools: [web-browser, orcid, latex-or-word]
  skills: []
sources_consulted:
  - "Original: Cold Spring Harbor Laboratory bioRxiv/medRxiv posting guide (https://www.biorxiv.org/)."
  - "Original: ASAPbio preprint server list (https://asapbio.org/preprint-servers)."
  - "Original: Creative Commons license chooser (https://creativecommons.org/choose/)."
  - "Original: NIH Preprint Pilot in PubMed Central (https://www.ncbi.nlm.nih.gov/pmc/)."
  - "Original: STM 2024 statement on co-reviewed preprints."
  - "Original: bioRxiv/medRxiv In Review and Reviewed Preprint (https://www.biorxiv.org/)."
  - "Improvisions: Pradyumna Jayaram — server-selection decision tree, license comparison table, scoop-protection timeline, journal-transfer flow diagram."
last_updated: 2026-06-10
---

# Preprints

> A preprint is a complete, draft manuscript posted to a public server before peer review. Preprints accelerate dissemination, establish priority ("scoop protection"), invite community feedback, and increasingly count as formal scholarly outputs (NIH allows preprints in grant submissions, Plan S funders require immediate open access, and PubMed Central indexes NIH-funded preprints since 2020). This skill covers server selection, licensing, versioning, and the journal transfer process — the four decisions a researcher must make before the first click.

## When to use

- Choosing **which server** to post a manuscript (bioRxiv vs medRxiv vs ChemRxiv vs SSRN vs arXiv vs EarthArXiv vs PsyArXiv).
- Selecting a **license** for the preprint (CC-BY-4.0 vs CC-BY-NC-ND-4.0 vs CC-BY-NC-4.0 vs no license / "all rights reserved" until acceptance).
- Planning **versioning**: how to handle v1, v2 (after reviewer feedback), v3 (post-acceptance).
- Understanding **scoop protection**: what a preprint does and does not protect.
- Navigating **journal transfer**: In Review, Reviewed Preprint, and direct-to-journal workflows.
- Building a **preprint-first lab culture**: lab norms, timing, and policy.
- Grant or job applications that ask for a list of preprints.

## When NOT to use

- For **preregistration** of a study design (no results yet) — see `ors-open-science-preregistration`.
- For **data deposits** without a manuscript — see `ors-open-science-fair-data`.
- For **clinical trials registration** (which has its own regulatory regime) — see `ors-open-science-preregistration` (ClinicalTrials.gov section).
- For **code release** (no paper) — see `ors-open-science-code-release`.
- If the manuscript reports findings on **dual-use research of concern (DURC)** or pathogens of pandemic potential — pre-publication review with NIH/NSABB may be required before posting.

## Prerequisites

- A complete draft manuscript (not an outline; not a partial study).
- ORCID iD for all authors.
- Conflict-of-interest disclosure statement (most servers require one).
- Approval of all co-authors for posting.
- Institutional preprint policy check (some institutions have rules about timing, embargoes, or which server).

## Core workflow

1. **Decide the server.** Use the decision tree in "Document patterns" below.
2. **Choose a preprint license.** Default: CC-BY-4.0 (most permissive, most funder-aligned). Some journals mandate CC-BY-NC-ND-4.0 if you intend to transfer copyright later — check the journal's preprint policy.
3. **Prepare the manuscript file.** Single PDF (or Word for ChemRxiv), including all figures, tables, and supplementary material inline. Most servers allow supplementary files as separate uploads.
4. **Submit metadata.** Title, abstract, author list with ORCID iDs, conflict of interest, funding statement.
5. **Screen on submission.** Servers do a basic screen (~24-48 h): scope fit, plagiarism check, dual-use research of concern, ethics statement for human/animal work. bioRxiv/medRxiv famously do **not** perform peer review.
6. **Post v1.** Once accepted by the screen, the preprint is public with a DOI. The DOI never changes; version increments.
7. **Version up as the work evolves.** v2 after peer-review feedback, v3 after journal acceptance, v4 with the published-version link.
8. **Use the server's journal-transfer or reviewed-preprint service** (In Review, Review Commons, biOverlay) to forward the manuscript to a journal — preserving the preprint DOI.

## Document patterns

### Pattern 1: Server selection decision tree

```
What is the field?
├── Life sciences (biology, bioinformatics, ecology, neuroscience, etc.)
│   └── bioRxiv — life-sciences preprint server (Cold Spring Harbor Laboratory)
│       ├── Clinical / patient-level health science?
│       │   └── medRxiv — clinical preprint server (also CSH)
│       └── Chemistry subfield?
│           └── ChemRxiv — chemistry preprint server (ACS, RSC, DECHEMA, GDCh)
├── Physical sciences / math / CS / quantitative biology
│   └── arXiv — oldest preprint server (Cornell, 1991)
├── Social sciences / economics / law / finance
│   └── SSRN — Elsevier-owned social-sciences network
├── Earth sciences
│   └── EarthArXiv
├── Psychology
│   └── PsyArXiv
├── Engineering
│   └── engrXiv
├── Education
│   └── EdArXiv
├── Medical / health-services research (alternative to medRxiv)
│   └── medRxiv OR preprints.org (multi-disciplinary, ASAPbio-listed)
└── Truly cross-disciplinary or unsure
    └── preprints.org (multidisciplinary, accepts any field) OR Research Square
```

**Direct links to canonical server homes** (path-only, server names are well-established):

- bioRxiv: https://www.biorxiv.org/
- medRxiv: https://www.medrxiv.org/
- ChemRxiv: https://chemrxiv.org/
- arXiv: https://arxiv.org/
- SSRN: https://www.ssrn.com/
- Research Square: https://www.researchsquare.com/
- preprints.org: https://www.preprints.org/
- ASAPbio server directory: https://asapbio.org/preprint-servers

### Pattern 2: License comparison

| License | Share | Adapt | Commercial use | Journal friendly? | Notes |
|---------|-------|-------|----------------|-------------------|-------|
| **CC0 1.0** | Yes | Yes | Yes | Unusual for manuscripts | Most permissive; used for datasets more than papers. |
| **CC-BY-4.0** | Yes | Yes | Yes | **Most permissive; some journals require transfer of non-exclusive rights on top** | Funder-preferred (Plan S, NIH, Wellcome). |
| **CC-BY-SA-4.0** | Yes | Yes | Yes (with same license) | Sometimes accepted; some journals reject | "Copyleft" — derivatives must use the same license. |
| **CC-BY-NC-4.0** | Yes | Yes | No | Common compromise | "Non-commercial" clause can complicate reuse. |
| **CC-BY-NC-ND-4.0** | Yes | No | No | **Most restrictive; many journals accept this** | No derivatives; e.g., cannot use the figure in a derivative review. |
| **No license / "all rights reserved"** | Default under copyright | No | No | Yes (most journals assume this until acceptance) | Limits reuse, but some journals require it pre-acceptance. |

**Practical default:** post as **CC-BY-4.0**. If the target journal forbids this, switch to **CC-BY-NC-ND-4.0** before posting. Check the journal's preprint policy on its "Instructions for Authors" page (Sherpa Romeo lists them: https://www.sherpa.ac.uk/romeo/).

### Pattern 3: Scoop-protection timeline

```
Day 0          Manuscript complete. Post to preprint server. DOI minted.
Day 1-2        Screen (~48 h). Authors notified.
Day 3          Preprint public. Author priority established.
               Note: priority is social/convention-based, not legal.
               No formal "patent" or "first-to-publish" right is granted.
Day 30-180     Submit to journal. Referee reports received.
Day 180-365    Revise; version v2 of preprint with reviewer response.
Day 365-540    Journal accepts; v3 with accepted manuscript.
               Add DOI of the published version.
Day 540+       v4 (optional) with the version of record link.
```

**What scooping means in practice:** if a competing group publishes the same finding before you submit, the preprint timestamp is evidence that you had the finding first. It does **not** guarantee authorship priority — the convention is "whoever's paper comes out first" in many fields. Post early for protection, but don't expect legal rights.

### Pattern 4: Version metadata

Each version of a preprint has the same DOI, with a version suffix. Use the README to record changes:

```markdown
## Versions
- v1 (2025-09-12): Initial submission.
- v2 (2025-12-04): Revised after bioRxiv community comments; added
  Supplementary Figure 3; clarified methods section 2.4.
- v3 (2026-03-22): Revised after journal peer review at Nature
  Communications; added replication cohort; reviewer responses in
  supplementary material.
- v4 (2026-06-15): Added link to published version (DOI 10.1038/...).
```

### Pattern 5: Journal-transfer flow with In Review / Reviewed Preprint

```
bioRxiv / medRxiv (v1)
        │
        │ (In Review partnership)        ← optional
        ▼
Review Commons (peer review at a journal-independent platform)
        │
        ▼
Journal transfer: eLife, PLOS, Nature Communications, etc.
        │
        ▼
Reviewed Preprint (peer-reviewed version with reviews + response)
        │
        ▼
Version of record at the journal
```

- **In Review** (bioRxiv/medRxiv partnership): forwards the preprint + supporting info to a partner journal.
- **Review Commons** (EMBO): journal-independent peer review; you choose the journal after reviews.
- **eLife's Reviewed Preprints**: eLife reviews the preprint and publishes a Reviewed Preprint (DOI + reviews + author response) before any journal's version of record.

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| **Posting to the wrong server** | Scope-mismatch → desk rejection by the server | Use the decision tree; ASAPbio has a unified submission portal. |
| **No ORCID iDs** | Authorship ambiguity; some servers require them | Add ORCID iDs for all authors at submission. |
| **Posting before all co-authors approve** | Authorship dispute (COPE case database is full of these) | Get email approval from every co-author; keep a record. |
| **Posting clinical advice or "treats COVID"** | medRxiv/ChemRxiv/bioRxiv explicitly forbid clinical recommendations; legal risk | Restrict to the scientific finding; refer clinical readers to clinical guidelines. |
| **Choosing CC-BY-NC-ND when a funder requires CC-BY** | Plan S / Wellcome / Horizon Europe compliance failure | Default to CC-BY-4.0. |
| **Claiming "priority" in cover letter** | Reviewers find it off-putting; "scooping" is a social convention, not a legal claim | Don't lean on the preprint in cover letters; submit normally. |
| **Posting a paper under review at Nature/Science without checking** | Most Nature/Science family journals now allow preprints; Cell family allows; Elsevier/Wiley/ACS/Springer allow; some holdouts (some IEEE, some medical) prohibit | Check the journal's preprint policy; Sherpa Romeo aggregates them. |
| **No version annotation** | Readers don't know if v1 differs from the published version | Add a "v1 vs published" note; update v1's metadata with the published DOI. |
| **Screen rejection because of ethics** | Human-subject research needs an ethics statement; animal research needs IACUC approval number | Add to methods before posting. |
| **Dual-use research posted without DURC review** | Federal DURC/PEPP review is required for certain pathogens | Pre-screen with institutional review board; do not post gain-of-function or enhanced-pandemic pathogen work without explicit approval. |
| **Preprint cited as "peer-reviewed"** | It is not; reviewers will catch this | In the paper, write "preprint (not peer-reviewed)"; in the journal version, cite the published version. |
| **Self-archiving a journal-published PDF on a preprint server** | Most journals require you to use the AAM (author accepted manuscript), not the VoR; some allow a 6/12/24-month embargo | Read the journal's self-archiving policy; Sherpa Romeo lists it. |

## Validation

A preprint is "well-posted" when:

- [ ] All co-authors have approved the version.
- [ ] ORCID iDs are linked for every author.
- [ ] License is explicitly declared (default CC-BY-4.0).
- [ ] Ethics statement and conflict-of-interest statement are present.
- [ ] Funding statement and grant numbers are present.
- [ ] A "Comments" link (bioRxiv, medRxiv) is monitored and replied to.
- [ ] The DOI is included in the lab's ORCID, Google Scholar, and the journal submission cover letter.
- [ ] The preprint is listed on the lab's website and the authors' Twitter/X/Bluesky.
- [ ] A v2 is posted when the journal reviews come back.
- [ ] The published-version DOI is added to the preprint record.

## Open alternatives

| "Premium" / commercial service | Open alternative | Trade-off |
|--------------------------------|------------------|-----------|
| Research Square (Elsevier, paid editing + DOI) | bioRxiv / medRxiv (free) | Research Square offers paid editing; bioRxiv is free with no editing. |
| SSRN (Elsevier) | SocArXiv, MetaArXiv | SSRN is dominant in social sciences; SocArXiv is smaller but open. |
| Authorea (Wiley-owned) | Manubot, Quarto | Authorea has nicer UX; Manubot is git-native, fully open. |
| Peerus (paid preprint commenting) | bioRxiv's native comment thread; PubPeer | PubPeer allows anonymous posting; bioRxiv's comments are public and tied to ORCID. |
| Journal "open access" fee ($11,690 for Nature) | bioRxiv + self-archive (free) | Journal OA is fee-based; preprint + self-archive is free but has no version of record. |

## References

- bioRxiv FAQ and posting guide: https://www.biorxiv.org/about/FAQ
- medRxiv FAQ: https://www.medrxiv.org/about/FAQ
- ChemRxiv author guide: https://chemrxiv.org/engage/chemrxiv/author-guidelines
- arXiv submission help: https://info.arxiv.org/help/
- ASAPbio preprint server list and FAQ: https://asapbio.org/preprint-servers
- ASAPbio norms preprint: https://asapbio.org/preprint-info
- Sherpa Romeo (journal preprint policies): https://www.sherpa.ac.uk/romeo/
- Creative Commons license chooser: https://creativecommons.org/choose/
- Creative Commons license deeds: https://creativecommons.org/licenses/
- NIH Preprint Policy (NOT-OD-17-050, extended 2023): https://sharing.nih.gov/
- PubMed Central preprint pilot: https://www.ncbi.nlm.nih.gov/pmc/about/nihpreprints/
- Plan S preprint requirement: https://www.coalition-s.org/
- eLife Reviewed Preprints: https://elifesciences.org/articles/reviewed-preprint
- Review Commons: https://reviewcommons.org/
- bioRxiv/medRxiv In Review: https://www.biorxiv.org/content/in-review
- COPE authorship guidelines: https://publicationethics.org/

## Related skills

- `ors-open-science-preregistration` — for studies without results yet.
- `ors-open-science-licensing` — deep dive on license choice.
- `ors-scientific-writing-imrad-drafting` — writing the manuscript before posting.
- `ors-ethics-compliance-` (separate skills) — IRB / IACUC / DURC for clinical or pathogen work.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesised bioRxiv/medRxiv posting guides; ChemRxiv author guidelines; arXiv help; ASAPbio server directory; Creative Commons license deeds; NIH Preprint Policy; Plan S; eLife Reviewed Preprints; Review Commons. Server decision tree, license comparison, scoop-protection timeline, and journal-transfer flow are original compositions.
