---
name: thesis-structure
description: "Use when planning or checking the architecture of a PhD / MPhil thesis in the life sciences or bioinformatics — monograph vs article-based, chapter sequence, IMRaD-based chapters, abstract-to-conclusion flow, and the examiner expectations that the structure must meet."
license: MIT
---
<!-- metadata:
  category: thesis-writing
  oversight: medium
  version: 1.0.0
  author: Pradyumna Jayaram
  tags: [thesis-writing, structure, imrad, monograph]
  difficulty: intermediate
-->

# PhD Thesis Structure (Life Sciences & Bioinformatics)

The structural spine of a thesis before a word is written. Choosing between a
**monograph** (original chapters) and an **article-based** thesis (submitted
papers with an integrative frame) is the first decision, and it fixes everything
downstream: chapter order, the role of the Introduction, and what the
examiner will expect to find at each position.

## Hard rules

1. **No fabricated citations.** Every in-text citation you list in the
   structure check must resolve to a verifiable record (DOI, PMID, arXiv ID,
   ISBN, or URL with a retrieval date). A structure that asserts "chapter 3
   builds on (Kumar 2019)" when that record does not resolve is a defect, not
   a placeholder.
2. **No claim without provenance.** Every structural claim about *your* thesis
   (this chapter is chapter 4, it contains n=X results, it follows chapter 3)
   must point to a section, heading, or figure the agent can open and confirm.
3. **No silent failure.** Every tool that scans or outlines the draft (a
   heading extractor, a section-counting pass, a word-count) must report what
   happened on non-zero. A "your draft has no methods section" that came from a
   parse error, not the document, is a false finding — flag the parse, not the
   thesis.
4. **Decide monograph vs article-based first, and say so.** The two have
   different examiner expectations; an unlabeled hybrid confuses the reviewer.

## When to use

- Before writing, to set the chapter sequence and fix the monograph /
  article-based choice.
- Mid-thesis, to check that each chapter has the IMRaD shape examiners expect.
- At the "does this read as a thesis, or as a pile of papers?" review.

## When NOT to use

- The reproducibility of methods and code — use `thesis-methods-reproducibility`.
- The viva / defense — use `thesis-defense-viva`.
- The single-particle of an Introduction or Abstract paragraph — use
  `manuscript-structure`.
- A journal paper, not a thesis — use the `scientific-writing` skills
  (`manuscript-structure`, `cover-letter`).

## Prerequisites

- The supervisor has confirmed the thesis type the department expects
  (monograph is the default in many Indian and UK programs; article-based needs
  explicit permission in others).
- A rough inventory of completed work: which experiments / datasets / papers
  exist, and in what order they were done.

## The two archetypes

| | **Monograph** | **Article-based** |
|---|---|---|
| Core | Original chapters written by you | 2–3 submitted/published papers + an integrative frame |
| Ch 1 | Literature review (you own the narrative) | Intro that integrates the papers into one argument |
| Ch 2..n | One theme/organism/method each | Each paper becomes a chapter (often verbatim, with permission) |
| Final | Discussion + general conclusion | General discussion reconciling all papers |
| Examiner risk | Coherence: one argument across chapters | Redundancy: repeated intros/methods; need one unifying thread |

## The IMRaD spine

Most life-science chapters are **IMRaD** (Introduction–Methods–Results–
Discussion). For a *whole thesis*, map that onto chapters:

1. **Chapter 1 — Introduction / Background.** The whole-thesis "why now."
   Build the gap, not a survey. (This is the thesis-scale version of a paper
   intro; keep it ~8–15% of the thesis.)
2. **Chapter 2 — (thesis-scale) Methods & resources**, *or* fold into each
   chapter. In monographs a shared-methods chapter de-duplicates; in
   article-based the methods live inside each paper chapter.
3. **Chapters 3..n — Results chapters**, one theme each, IMRaD internally.
4. **Final chapter — General discussion + conclusion.** Synthesize across
   chapters; state the contribution and the limits; name the follow-ups.

An abstract at the very front must contain: context → the gap → what you did →
the main finding → the contribution, in 250–350 words (or the program's limit).

## Structure workflow

1. **Choose the archetype** and record it in the draft's front matter so the
   examiner sees the intent.
2. **Draft the chapter map** — one bullet per chapter with a single-sentence
   "this chapter establishes ___." If a chapter's sentence is empty, cut it.
3. **Assign every result to exactly one chapter.** No result sits in two; no
   chapter is empty. (A shared methods chapter is the one legitimate exception.)
4. **Check IMRaD internally** per results chapter: does it have intro (what
   this chapter does), methods (how), results (what), discussion (so what)?
5. **Front + back matter:** title page, abstract, list of figures, list of
   tables, abbreviations, acknowledgements, then the body, then references,
   then appendices. Order and presence are checked mechanically, so run a
   heading scan.
6. **Length sanity-check** against the program's word/page cap (many programs cap
   ~60–80 pages of body text). A thesis that is too long is a structure
   problem, not a writing problem.

## Pitfalls

- **The unlabeled hybrid** — some monograph chapters, some paper chapters, and
  no statement of which it is. Examiners read the mess as "I did not think
  about the structure."
- **Article-based redundancy** — three near-identical introductions; no
  integrative thread. The frame chapter is what makes it a thesis, not a
  folder of PDFs.
- **Results in two chapters** — the same figure appears in ch. 4 and ch. 6;
  the examiner is left to work out which is canonical.
- **A Discussion that re-lists Results** instead of interpreting across
  chapters.
- **Missing front/back matter** (no list of figures, no abbreviations) — small,
  but read as sloppiness on day one.
- **Too long** — padding dilutes the contribution; trim to one argument.

## Validation

- The archetype (monograph / article-based) is stated on the title/foreword.
- A heading scan confirms the full front → body → back matter sequence, with no
  duplicate results chapters.
- Each results chapter passes the internal IMRaD check.
- The abstract is within the program's word cap and carries all five beats.
- Every citation named in the structure check resolves.

## Cross-references

- thesis-methods-reproducibility — the methods, code, and figure discipline
  the structure must support.
- thesis-defense-viva — what the examiner will probe at the boundary of each
  chapter.
- manuscript-structure — the IMRaD / structure models for a single paper,
  which a thesis chapter reuses at sentence and paragraph scale.

## References

- IMRaD and the five standard structure models: local
  `academic-research-skills-main/academic-paper/references/paper_structure_patterns.md`.
- Article-based thesis guidance: `bioinformatics-thesis-main/thesis-writing/SKILL.md`
  and `thesis-writing-skills-main` (local reference collections).
- Program-specific page caps and monograph-vs-article rules live in your
  department's thesis manual — the authoritative, local source.

## Changelog

- **1.0.0** (2026-06-18) — Initial release. Monograph vs article-based
  decision, the IMRaD chapter spine, front/back-matter sequence, and the
  examiner-expectation checks that structure must satisfy.
