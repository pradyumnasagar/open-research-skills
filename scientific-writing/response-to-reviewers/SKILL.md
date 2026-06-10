---
name: ors-scientific-writing-response-to-reviewers
display_name: "Response to Reviewers (How-To)"
description: "Detailed how-to for the actual response-to-reviewers document: tone discipline, heading structure (Reviewer N, Comment M: ... Response: ...), line-number references, embedding revised figure panels, and when to send the response with vs. without an editor's cover letter."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: scientific-writing
tags: [response-document, line-numbers, figure-embedding, response-format, peer-review]
difficulty: intermediate
prerequisites:
  tools: []
  skills:
    - ors-scientific-writing-rebuttal-letter
sources_consulted:
  - "ICMJE Recommendations (icmje.org)"
  - "Nature peer-review policy (nature.com/nature-portfolio/editorial-policies/peer-review)"
  - "eLife reviewed-preprint model (elifesciences.org/peer-review)"
  - "PLOS peer-review policy (plos.org/peer-review)"
  - "F1000Research open peer-review platform (sample responses)"
  - "BMJ Open peer-review history (sample responses)"
last_updated: 2026-06-10
---

# Response to Reviewers (How-To)

> The response document is the technical deliverable of the revision. It pairs every reviewer comment with an author response, a manuscript location, and (where applicable) a revised figure. Done well, the document is self-contained: the editor can read it without re-opening the original review file. Done poorly, the document is a paste-and-reply that forces the editor to hunt for the changes. This skill encodes the document architecture, the line-number discipline, the figure-embedding rules, and the workflow for producing a submission-ready response file.

## When to use

- Drafting the response document that accompanies a revised manuscript submission.
- Drafting the response document for a transfer-of-review submission.
- Producing a "tracked-changes" version of the response that the editor can compare with the original review file.
- Producing a public response document (eLife, F1000Research, and similar open-review journals publish the response with the article).

## When NOT to use

- For an outright desk-rejection with no review (no response document is required).
- For a "reject with invitation to resubmit" that requires a full new submission (the response document is folded into the cover letter).
- For comments from a preprint server (use the platform's comment-reply format).

## Prerequisites

- The original decision letter with all reviewer comments.
- The revised manuscript (with tracked changes if the journal requires them).
- A clean copy of the revised manuscript (line-numbered if the journal requires it).
- Co-author sign-off on the response to each point.
- New figures and tables ready as separate files (most journals require separate file uploads for figures, with the response document pointing to them).

## Core workflow

### 1. Lock the file format early

Most journals accept a single response document. Format choices:

| Format | When to use |
|--------|-------------|
| Word .docx with line numbers | Most common; preferred for traditional peer-reviewed journals |
| Word .docx without line numbers | When the journal does not require line numbers in the response |
| PDF | When the journal's submission system does not accept .docx |
| Markdown or plain text | Open-review platforms (e.g., F1000Research, eLife) may accept these |

The Word .docx with line numbers is the safest default. Use the journal's template if one is provided.

### 2. Number the comments in the original review first

Before drafting the response, re-number the comments in the original review so that the response can reference them. The convention:

> Reviewer 1, Comment 1
> Reviewer 1, Comment 2
> Reviewer 2, Comment 1
> Reviewer 2, Comment 2
> Reviewer 2, Comment 3
> Reviewer 3, Comment 1

This numbering carries through the response document and the marked manuscript.

### 3. Use a fixed heading structure

The heading structure for the response document is:

```
Response to Reviewers
[Manuscript title]
[Manuscript ID]

We thank the editor and the reviewers for their careful reading
of our manuscript. We have addressed each comment below. The
revised manuscript is provided as a separate file; page and line
numbers refer to the clean copy.

Summary of major changes
1. [Bullet 1]
2. [Bullet 2]
...

Reviewer 1

Comment 1: "[verbatim reviewer comment]"

Response: [our response, in 1-3 short paragraphs]

Change in manuscript: page X, line Y; Figure Z.

Comment 2: ...

Reviewer 2

Comment 1: ...

Reviewer 3

Comment 1: ...
```

The fixed structure means the editor always knows where to look.

### 4. Quote the reviewer comment verbatim (preferred) or summarize

Quoting verbatim is the safest convention; it eliminates any ambiguity about what the authors are responding to. If the reviewer comment is long, the response may quote a relevant excerpt and then summarize the rest in the response paragraph.

### 5. Reference manuscript locations precisely

A response that says "we have revised the text" is weaker than a response that says "we have revised the text on page 11, lines 4-9, and the new Figure 3F is referenced on page 12, line 16." The convention is `page X, line Y` for textual changes and `Figure N, panel M` for figure changes.

### 6. Embed revised figure panels in the response where useful

Some journals ask the authors to embed revised figure panels directly in the response document so the editor does not have to open multiple files. The convention is:

- Place the figure panel at the top of the response to the relevant comment.
- Caption: "Revised Figure 3F" with a one-sentence description.
- Do not duplicate the figure in the manuscript figure set.

Other journals require all figures to be uploaded as separate files. Read the journal's submission guidelines before embedding.

### 7. Decide whether to send the editor's cover letter with the response

The cover letter is separate from the response document. The decision:

| Scenario | Send a cover letter? |
|----------|---------------------|
| Major revision, journal requires resubmission | Yes — short cover letter summarizing the major changes |
| Minor revision | Optional; some journals do not require a cover letter for minor revisions |
| Reject-with-invitation-to-resubmit, treated as new submission | Yes — full cover letter as if first submission |
| Transfer-of-review submission | Yes — short cover letter noting the prior review file and the response document |
| Open-review journal (eLife, F1000Research) | The response document is itself the public response; no separate cover letter |

### 8. Save the document with the journal's expected file name

Many journals expect a specific file name. The convention:

- `[Manuscript ID]_Response_to_Reviewers.docx`
- `[Manuscript ID]_Response_to_Reviewers_Tracked.docx` (for the marked version)
- `[Manuscript ID]_Revised_Manuscript.docx` (for the clean version)
- `[Manuscript ID]_Revised_Manuscript_Tracked.docx` (for the marked version)

## Code patterns

### Document template (Word .docx, line-numbered)

```
[Line 1]  Response to Reviewers
[Line 2]
[Line 3]  Manuscript ID: BMJ-2025-123456
[Line 4]  Title: A single-cell atlas of METTL3-dependent m6A
[Line 5]  deposition in the aging mouse hippocampus
[Line 6]  Corresponding author: Aisha Lee, MD, PhD
[Line 7]
[Line 8]  We thank the editor and the reviewers for their
[Line 9]  careful reading of our manuscript. We have addressed
[Line 10] each comment below. The revised manuscript is provided
[Line 11] as a separate file; page and line numbers refer to
[Line 12] the clean copy.
[Line 13]
[Line 14] Summary of major changes
[Line 15] 1. New Figure 3F: METTL3 rescue experiment showing
[Line 16]    that re-expression of METTL3 restores temozolomide
[Line 17]    resistance in METTL3-knockdown cells.
[Line 18] 2. Restructured Discussion, with explicit Limitations
[Line 19]    subsection (page 18, lines 12-25).
[Line 20] 3. Added bootstrap analysis (n=10,000 resamples) to
[Line 21]    confirm the patient-cohort finding (page 12,
[Line 22]    lines 9-15; new Figure 4B).
[Line 24] 4. Revised title to reflect the new rescue finding.
[Line 25]
[Line 26] Reviewer 1
[Line 27]
[Line 28] Comment 1: "The authors should provide a rescue
[Line 29] experiment to confirm that the temozolomide-resistant
[Line 30] phenotype is METTL3-dependent."
[Line 31]
[Line 32] Response: We agree with the reviewer that a rescue
[Line 33] experiment is the appropriate control. We have now
[Line 34] performed the rescue. METTL3 was knocked down using
[Line 35] shRNA #1 in temozolomide-resistant U87-MG cells, and
[Line 36] a shRNA-resistant METTL3 cDNA was re-expressed. The
[Line 37] re-expression of METTL3 restored temozolomide
[Line 38] resistance, as shown in the new Figure 3F. The result
[Line 39] is described on page 11, lines 14-19.
[Line 40]
[Line 41] Change in manuscript: page 11, lines 14-19; new
[Line 42] Figure 3F.
```

### Heading structure summary

| Section | Heading level | Format |
|---------|--------------|--------|
| Top header | H1 | "Response to Reviewers" |
| Summary of major changes | H2 | "Summary of major changes" |
| Reviewer block | H2 | "Reviewer N" |
| Comment-response pair | H3 (or bold) | "Comment N: [quote]" followed by "Response: [text]" |
| Change in manuscript | Inline | "Change in manuscript: page X, line Y; Figure Z." |

### Embedding a revised figure panel

When the journal accepts embedded figures in the response:

```
[Embedded image: revised_Figure3F.png]

Caption: Revised Figure 3F. METTL3 rescue experiment.
Temozolomide-resistant U87-MG cells were transduced with
non-targeting shRNA (shNT), METTL3 shRNA (shMETTL3), or
shMETTL3 plus a shRNA-resistant METTL3 cDNA (rescue).
Re-expression of METTL3 restores temozolomide resistance
(IC50 18.4 ± 1.2 μM in shNT, 6.2 ± 0.5 μM in shMETTL3,
16.9 ± 0.9 μM in rescue; n=3 biological replicates).

Change in manuscript: page 11, lines 14-19; new Figure 3F.
```

The figure panel in the response document is a courtesy to the editor. The same panel must be uploaded as a separate high-resolution file in the journal's submission system. Do not embed the figure in the response document only; the editor will not extract it for the production system.

### Resolving conflicting comments

When two reviewers make conflicting comments, the response document addresses each in the reviewer's own section. The resolution is a separate paragraph that references both.

```
Reviewer 1, Comment 4: "The authors should include a
syngeneic glioblastoma model to strengthen the in vivo
finding."

Reviewer 3, Comment 2: "The patient-derived xenograft
model is the appropriate model; a syngeneic model would
not reflect the human tumor biology."

Response: We thank both reviewers for raising this
question. We agree with Reviewer 1 that a syngeneic model
would add value, and with Reviewer 3 that the PDX model
is the most relevant for human glioblastoma. We have
addressed this in the revised Discussion by adding a
Future Directions paragraph (page 19, lines 5-12) that
proposes a syngeneic model as a follow-up, and by
justifying the choice of PDX as the primary model
(page 19, lines 12-18).
```

### When the reviewer is wrong: line-number discipline

A common failure mode is the response that says "we respectfully disagree" without pointing to the new text. The editor cannot evaluate a "we disagree" response; the editor can evaluate a "we disagree, and the manuscript now says X on page Y" response. The convention:

> "We respectfully note that the reviewer's interpretation is not supported by the data. The new bootstrap analysis (Figure 4B; page 12, lines 9-15) shows that the patient-cohort effect is robust. We have also added a sentence to the Discussion acknowledging the alternative interpretation (page 18, lines 18-22)."

The response is three things at once: a polite disagreement, a pointer to new evidence, and an acknowledgment of the alternative.

### Embedding a table of changes

Some journals ask the authors to include a table that summarizes all changes. The format:

| Comment | Reviewer | Type | Change |
|---------|----------|------|--------|
| 1 | 1 | Fix | Revised Figure 1 legend (page 5, line 3) |
| 2 | 1 | New analysis | New Figure 3F (page 11, line 14) |
| 3 | 1 | Reframe | Revised Discussion paragraph (page 17, lines 5-12) |
| 4 | 2 | Disagree | Added Future Directions paragraph (page 19, lines 5-12) |

The table is at the end of the response document and is a quick-reference for the editor.

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| Pasting reviewer comments without quoting | Editor cannot verify what was said | Quote verbatim (preferred) or summarize with the original phrasing in mind |
| Response is one long paragraph per comment | Editor cannot extract the response | Two to three short paragraphs per comment, with the manuscript change clearly identified |
| No line-number references | Editor has to search the manuscript | "Page X, line Y" is the convention; "in the Methods" is not enough |
| Summary of major changes missing | Editor has to extract the changes from the response | Open with a 4-6 bullet list of the major changes |
| New figures are not referenced in the response | The figures sit in the manuscript but the response does not point to them | Reference every new figure in the response, with page and line numbers |
| Cover letter is missing or not updated | Editor still has the original cover letter | Send a short cover letter reflecting the revised title and the major changes |
| Response document is the only file submitted | The editor does not have a clean copy of the revised manuscript | Submit: clean manuscript, marked manuscript (if required), response document, updated cover letter, separate figure files |
| Disagreement is stated without evidence | The editor reads the response as a refusal to revise | Pair every "we respectfully disagree" with a pointer to new data or to a revised manuscript sentence |
| Resolving Reviewer 1 in the Reviewer 2 section | The editor reads each section in order; mis-alignment is a flag | Address each reviewer's comments in the reviewer's own section |
| Inconsistent figure numbering between response and manuscript | The editor flags the discrepancy | Renumber the figures in both files together |
| Embedding figure panels that are not in the manuscript figure set | The editor flags the discrepancy | Either embed only panels that are in the manuscript figure set, or note explicitly that the panel is supplemental |
| Track-changes version does not match the clean version | The editor flags the discrepancy | Regenerate the tracked version from the clean version after every round |
| Submitting a PDF when the journal requires .docx | The editor cannot extract the text | Match the file format to the journal's submission system |
| Line numbers in the manuscript are missing | The editor cannot find the change | Enable line numbers in the manuscript Word file before saving |

## Validation

A response document passes validation when:

- Every reviewer comment is numbered, quoted (or summarized), and paired with a response.
- The response includes a manuscript location (page and line, or figure number).
- The summary of major changes is at the top.
- The figure panels referenced in the response are in the manuscript figure set.
- The manuscript figure set is consistent with the response (no orphan references in either direction).
- The cover letter is updated to reflect the revised title and the major changes.
- The document is in the file format the journal expects.
- The tracked-changes manuscript (if required) is consistent with the clean manuscript.
- All co-authors have signed off on the response.
- The corresponding author has read the response document end-to-end.

## Open alternatives

For document-preparation tools, the open alternatives are:

| Commercial | Open alternative |
|-----------|-----------------|
| Microsoft Word | LibreOffice Writer (compatible with .docx), pandoc for Markdown-to-Word conversion |
| PerfectIt (style) | Vale (prose linter), textract + custom rules |
| Grammarly (tone) | LanguageTool (open-core) |

The response document itself is plain text; no commercial tool is required.

## References

- ICMJE Recommendations. icmje.org/icmje-recommendations.pdf
- Nature peer-review policy. nature.com/nature-portfolio/editorial-policies/peer-review
- eLife peer-review model. elifesciences.org/peer-review
- PLOS peer-review policy. plos.org/peer-review
- F1000Research open peer-review platform (sample responses).
- BMJ Open peer-review history (sample responses).
- COPE authorship discussion. publicationethics.org/authorship

## Related Skills

- ors-scientific-writing-rebuttal-letter — for the broader strategy of the rebuttal and the polite-disagreement repertoire.
- ors-scientific-writing-cover-letter — for the cover letter that accompanies a revised submission.
- ors-scientific-writing-manuscript-structure — for the manuscript structure that the response defends.
- ors-scientific-writing-ai-disclosure-writing — for the AI/LLM usage statement that should be in the manuscript.
- ors-ethics-compliance-authorship-disputes — for handling authorship disagreements that surface during revision.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Consolidated public guidance on response-document architecture (ICMJE, Nature/eLife/PLOS/BMJ peer-review policies, COPE), line-number discipline, figure-embedding rules, cover-letter bundling, and a table-of-changes convention. No specific journal policies are quoted verbatim; all sources are publicly accessible.
