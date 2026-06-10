---
name: ors-ethics-compliance-ai-disclosure
display_name: "AI / LLM Usage Disclosure in Research"
description: "Use when writing, reviewing, or editing the AI/LLM usage disclosure in a research manuscript, grant, or submission — covers venue-specific policies (Nature, Science, Cell, NEJM, Lancet, ICML, NeurIPS, AAAI, ACL), COPE position statement, ICMJE recommendations, prompt disclosure, and what is permitted vs banned per venue (2025-2026). Name the venue explicitly; when in doubt, name 'varies by venue' rather than invent."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: ethics-compliance
tags: [ai, llm, chatgpt, disclosure, authorship, coposition-statement, icmje, journal-policy]
difficulty: intermediate
prerequisites:
  tools: []
  skills: [ors-scientific-writing-imrad-drafting]
sources_consulted:
  - "Original: COPE Position Statement on Generative AI in Authorship (Feb 2023); Adapted: disclosure rules and author accountability"
  - "Original: ICMJE Recommendations (last revised to add AI/authorship language in 2023); Adapted: AI in research vs writing"
  - "Original: Nature Editorial 'Authorship policies for AI tools'; Adapted: chatgpt-cannot-be-author rule"
  - "Original: Science Editorial 'The use of generative AI in scientific publishing' (2023, updated); Adapted: ban on chatgpt-as-author and image/text rules"
  - "Original: Cell Press Editorial Policies; Adapted: generative AI disclosure template"
  - "Original: ICML / NeurIPS / AAAI / ACL conference policies; Adapted: summary of policy variation by venue"
  - "Improvisions: venue-by-venue matrix, prompt-disclosure guidance, what varies by venue section, LLM citation rules"
last_updated: 2026-06-10
---

# AI / LLM Usage Disclosure in Research

> Since 2023, every major scientific publisher and many major conferences have issued explicit policies on the use of generative AI (ChatGPT, Claude, Gemini, Llama, Mistral, and similar) in manuscripts and submissions. The policies converge on three rules — AI cannot be an author, AI use must be disclosed, and the human author is fully accountable for the content — but the implementation varies by venue, the disclosure locations vary (Methods, Acknowledgments, dedicated declaration), and the rules for AI-generated or AI-modified figures and code are stricter than the rules for AI-assisted copyediting. This skill encodes the public policies of the major publishers and conferences, the COPE position statement, the ICMJE recommendations, and the disclosure patterns that satisfy reviewers and editors across venues.

## When to use

- Writing the AI/LLM usage section of a manuscript, conference paper, grant, or thesis.
- Deciding whether an LLM can be cited as an author, a tool, or a reference.
- Reviewing a manuscript for compliance with a venue's AI policy.
- Editing a manuscript for a journal or conference submission and adding the AI disclosure to the right section.
- Training a lab or team on what AI uses are permitted and what must be disclosed.
- Preparing a reproducibility or methods statement that includes AI-assisted analysis or writing.

## When NOT to use

- The question is whether an AI output is correct or hallucinated. That is a content-integrity question; use `ors-scientific-critical-thinking` and `ors-scientific-writing-imrad-drafting`.
- The question is IRB/ethics oversight of AI used on human participants. That is a privacy and consent question; use `ors-ethics-compliance-irb-protocol` and `ors-ethics-compliance-data-privacy`.
- The question is AI tool selection (which model for which task). That is `ors-machine-learning-bio-tool-selection` and similar.
- The venue is a domain-specific journal not listed below. Find the venue's editorial policy directly; do not extrapolate from the policies in this skill.

## Prerequisites

- The manuscript or submission text in a state where you can identify which sections used AI assistance.
- A record of which AI tools were used, for what, and to what depth (grammar, ideation, code, figures, analysis).
- Access to the target venue's author guidelines or editorial policy. This skill is current as of 2026-06; always confirm against the venue's current page.
- Familiarity with the COPE position statement and the ICMJE recommendations, both of which underlie most venue policies.

## Core workflow

1. **Inventory AI use in the manuscript.** For each section (title, abstract, introduction, methods, results, discussion, figures, references, supplementary), ask: was an LLM or generative AI used, in what role, and at what depth? Output: a paragraph or table that you can re-use in the disclosure.

2. **Confirm the venue's policy.** Look up the target venue's editorial policy page; do not rely on memory or a secondary source. The matrix below is a starting point; venue policies are updated more often than this skill.

3. **Decide authorship vs acknowledgement vs method vs nothing.** The default: AI is not an author. If AI contributed to ideation, drafting, or analysis, it is acknowledged. If AI was used as a research tool (e.g., an LLM-based screening or extraction step), the methods section names it as a tool. If AI was used only for grammar and style, an acknowledgment or a brief statement is enough.

4. **Decide figure rules.** AI-generated figures and AI-modified figures are the most-restricted category. Most publishers ban fabricated experimental images; many ban any AI-generated image without explicit disclosure; a small minority require original data behind any AI-altered figure.

5. **Draft the disclosure in the section the venue requires.** Common locations: Methods, Acknowledgments, Author Contributions, a dedicated "AI use" section, or a "Declaration of generative AI use" in the submission system.

6. **For the LLM itself, do not cite it as a source of scientific fact.** A model is a tool, not a reference. If the LLM helped locate a citation, the citation is to the original paper, not to the model. If the LLM fabricated a citation, the manuscript is retracted for citation manipulation.

7. **For prompts, decide what to disclose.** A growing number of venues and methods sections now request prompt disclosure — the prompt used, the model, the version, and the date. If the prompt is short and reproducible, include it. If the prompt contains sensitive data or is long, summarize.

8. **For code, follow the venue's code-availability policy.** Most AI-assisted code is fine to share; some venues require a statement on which lines were AI-generated vs human-written.

9. **Add the statement to the submission system.** Many journals have a checkbox or a required field. Conferences vary.

10. **Update the disclosure on revision.** If you add AI-assisted analysis during revision, update the disclosure in the response letter and the manuscript.

## Code patterns

This skill is documentation-heavy. The patterns below are the canonical disclosure text structures, organized by venue category.

### Pattern 1 — Universal "no AI author" statement

Almost every venue requires or strongly recommends a statement that no AI tool is listed as an author. The shortest working text is:

> "No generative AI tools were used in the preparation of this manuscript."

If AI was used, replace the sentence above with the relevant Pattern 2-5 below. The sentence should appear in the Author Contributions section, the Acknowledgments, or both — check the venue.

### Pattern 2 — Grammar- and style-only disclosure (most lenient)

> "During the preparation of this work, the authors used [tool name, version] in order to improve language and readability of selected paragraphs. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication."

This pattern satisfies Cell Press, Science, and most general-science venues. The required pieces: tool name, version, purpose, and the accountability statement.

### Pattern 3 — Methods-and-analysis disclosure (stricter)

> "In this study, [tool name, version] was used for [task, e.g., abstractive screening of references, classification of free-text notes, code refactoring, or statistical analysis step]. All AI-generated outputs were reviewed and validated by [human author or domain expert] prior to use. Prompts and processing details are provided in Supplementary Methods S1."

This pattern appears in computational and biomedical venues where AI is a research instrument rather than a writing aid.

### Pattern 4 — Figure- and image-specific disclosure (strictest)

> "Figure [N] was generated with [tool name, version] using [input source]. The figure was reviewed by the authors for accuracy and approved for publication. No part of Figure [N] is based on fabricated experimental data; the underlying data are available at [link]."

For AI-edited or AI-styled images:

> "Figure [N] was originally captured by [method, e.g., confocal microscopy, file name]. The image was brightness/contrast-adjusted and color-balanced using [tool, version] with no change to the underlying signal. The original, unprocessed image is provided in Supplementary Figure S[N]."

Some venues require the unedited image in supplementary material; some venues require the AI tool to be declared in the methods.

### Pattern 5 — Code-availability disclosure

> "Code was written by the authors with assistance from [tool name, version] for [refactoring, docstring generation, test writing]. All code was reviewed, tested, and integrated by the authors. The full code repository, including commit history, is available at [URL]."

For venues that require it, a statement that a specific commit range was AI-generated vs human-written is acceptable.

### Pattern 6 — Reviewer-side note

> "Reviewers must not upload submitted manuscripts into public AI tools, as this can violate confidentiality and may train models on unpublished research. AI use by reviewers is permitted only with disclosure to the editor and only with tools that do not retain or learn from inputs."

This is editorial, not author-facing, but increasingly appears in reviewer guidelines.

## Common pitfalls

- **Listing an LLM as an author.** Universally banned by COPE, ICMJE, Nature, Science, Cell, NEJM, Lancet, and the major conferences. The first author of a paper with "ChatGPT" as a co-author is asking for a desk reject.
- **Citing the LLM as a reference.** A model is a tool, not a citable source. If the LLM produced a factual claim, the citation is to the original source. If the LLM fabricated a citation, remove it and verify the references manually.
- **Failure to disclose any AI use.** Most venues require disclosure of all AI use, including grammar-only assistance. Silence is treated as a violation.
- **Disclosure in the wrong section.** Nature has required a specific declaration format; Science requires a Methods statement; Cell Press allows Methods or Acknowledgments. Wrong-section disclosures are the most common stipulation.
- **Treating a private model as exempt.** Local LLM use is not exempt from disclosure. The disclosure is about the *role* of AI, not the *location* of the model.
- **Treating AI translation as exempt.** Most venues treat AI translation the same as AI writing — it must be disclosed.
- **Disclosure that does not name the version.** A disclosure that says "we used ChatGPT" without naming the version (e.g., "GPT-4o, OpenAI, August 2024") is incomplete.
- **Failure to disclose AI use in figures.** Generated, modified, or AI-assisted images must be disclosed in the figure caption and the methods. The figure-rules bar is higher than the writing bar.
- **Failure to disclose AI use in analysis.** An LLM that screens references, extracts data, or labels images is a research instrument and must be in the Methods.
- **Treating a model output as a "primary source."** LLMs are trained on secondary text; the model output is not a primary source for any factual claim.
- **Not updating the disclosure on revision.** If AI was used in revision but not the original submission, the revision letter and the manuscript should both reflect this.
- **Failure to disclose prompt.** A growing minority of venues expect prompt disclosure for reproducibility. A 2026 best practice: include the prompt in supplementary methods when the AI step is part of the research.

## Validation

- The manuscript contains a disclosure statement in the section the venue requires.
- The disclosure names the tool, the version, the date (or version date), the purpose, and the accountability statement.
- The author contributions section lists only human authors.
- The reference list does not cite a model as a source of fact.
- Figures that used AI assistance are labeled and disclosed in the caption and methods.
- AI-assisted analysis steps are in the Methods with a version number.
- The submission system's AI declaration field is filled.
- The disclosure has been cross-checked against the current venue policy page.

## Venue-by-venue summary (publicly stated, 2025-2026)

The matrix below summarizes publicly stated policies of major venues as of 2026-06. It is not exhaustive. **Always confirm against the current editorial policy page of the venue you are submitting to — policies are updated frequently.**

| Venue | AI as author | Disclosure required | Writing assistance | Figures | Notes |
|---|---|---|---|---|---|
| **Nature Portfolio** | Banned | Yes, dedicated declaration in submission system | Disclose if used | AI-generated images banned without explicit exception; AI-edited images with disclosure | First major publisher to ban AI-as-author (Jan 2023). |
| **Science (AAAS)** | Banned | Yes, in Methods | Disclose if used | Stricter rules for image manipulation; original data required | "The use of generative AI in scientific publishing" editorial. |
| **Cell Press (Cell, Cell Reports, etc.)** | Banned | Yes, in Methods or Acknowledgments | Disclose if used | AI-generated/modified images must be disclosed | Consistent across the family. |
| **NEJM** | Banned | Yes | Disclose if used | Stricter rules | ICMJE-aligned. |
| **The Lancet** | Banned | Yes | Disclose if used | Stricter rules | ICMJE-aligned. |
| **JAMA Network** | Banned | Yes, in Acknowledgments | Disclose if used | Stricter rules | ICMJE-aligned. |
| **ICMJE recommendations** | Banned (basis for many journal policies) | Yes | Disclose if used | — | AI in research vs writing distinction. |
| **COPE position statement (Feb 2023)** | Banned | Yes, all AI use | Disclose if used | — | Foundation document; most venue policies reference COPE. |
| **ICML** | Banned | Yes | Varies by year; check current CFP | Varies | Has updated policies each year since 2023. |
| **NeurIPS** | Banned | Yes | Varies | Varies | Author guidelines updated annually. |
| **AAAI** | Banned | Yes | Disclose if used | Varies | Policy has been updated; check current CFP. |
| **ACL (and ACL Anthology)** | Banned | Yes, in Limitations and Acknowledgments | Disclose if used | Varies | Policy update in 2023. |

**What varies by venue:**
- The exact location of the disclosure (Methods vs Acknowledgments vs Author Contributions vs dedicated submission-system field).
- Whether the disclosure must include a tool *version* or just a tool *name*.
- Whether AI-generated *figures* are banned outright, banned with exceptions, or allowed with disclosure.
- Whether *code* generated by AI must be flagged in the commit history.
- Whether AI use in *peer review* is permitted and what conditions apply.
- Whether the venue requires a *prompt* disclosure in supplementary material.

When a policy detail is not publicly posted or is ambiguous, name it as "varies by venue" and link to the venue's current policy page. Do not invent rules.

## Open alternatives

- **Disclosure generators**: The only credible generator is the one published by the target venue; do not use a third-party generator that may not match the venue's current text.
- **AI policy trackers**: Several community-maintained trackers exist (e.g., the "AI in academic publishing" tracker maintained by academic libraries). These are useful but lag official policies.
- **Local LLMs as substitutes for cloud APIs**: Local models do not exempt the disclosure, but they do eliminate the data-leakage concern of uploading unpublished work to a public AI service. Local models are an open alternative for draft work; disclosure still required.

## References

- COPE Position Statement on Generative AI in Authorship, Feb 2023.
- ICMJE Recommendations (last revised to add AI/authorship language in 2023).
- Nature Editorial, "Authorship policies for AI tools" and updates on the Nature Portfolio editorial policy page.
- Science Editorial, "The use of generative AI in scientific publishing" and subsequent updates on the Science author information page.
- Cell Press Editorial Policies — AI and generative AI section.
- ICML / NeurIPS / AAAI / ACL call-for-papers and author guidelines (current year).
- Related skills: `ors-scientific-writing-imrad-drafting` (Methods and Acknowledgments sections), `ors-scientific-critical-thinking` (verifying LLM outputs and references), `ors-ethics-compliance-data-privacy` (privacy of unpublished data uploaded to AI tools).

## Worked Examples

The examples below are illustrative. Names, datasets, and results are fictitious. Substitute your own; do not copy verbatim.

### Worked example 1 — Grammar-only disclosure for a clinical trial

> "During the preparation of this work, the authors used Claude (Anthropic, claude-opus-4-8, accessed 2026-04-12) in order to improve the language and readability of selected paragraphs in the Introduction and Discussion. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication."

This is the standard Cell Press / Science form. The four required pieces — tool name, version, purpose, accountability statement — are all present.

### Worked example 2 — Methods-and-analysis disclosure for a systematic review

> "Methods: We used GPT-4o (OpenAI, gpt-4o-2024-08, accessed 2024-09-15) to assist with two steps of the review workflow. First, GPT-4o was used to screen titles and abstracts against inclusion criteria; all AI-screened records were re-screened by two human reviewers. Second, GPT-4o was used to extract structured data from full-text reports; all extracted data were verified against the source by a human reviewer. Prompts, model versions, and processing details are provided in Supplementary Methods S1."

The disclosure covers (a) the two research-instrument uses, (b) the human verification of every AI step, (c) the prompt and version disclosure for reproducibility. This pattern is increasingly common in systematic-review and screening studies.

### Worked example 3 — Figure disclosure for an AI-edited microscopy image

> "Methods: Figure 4A shows representative images from confocal microscopy (Leica TCS SP8, 63x objective). Raw TIFFs are available on Figshare (DOI). Images were deconvolved (Huygens Professional) and linearly brightness/contrast-adjusted (FIJI, ImageJ 2.14) using the same parameters for all images in the panel. The lookup table is 'magma' (Matplotlib 3.9). The image in panel A4 was AI-denoised using Adobe Firefly (firefly-image-2, accessed 2025-02-03) with the 'reduce noise' preset; the original, unprocessed image is shown in Supplementary Figure S4."

This is a more elaborate example. The disclosure names the tool, the version, the access date, the parameters, the underlying data, and the original image. The bar for AI-edited images is higher than for AI-assisted writing, and a defensive protocol reflects this.

### Worked example 4 — Code-availability disclosure for an AI-assisted analysis pipeline

> "Code availability: The analysis pipeline is available at github.com/example/analysis (v1.2.0, DOI on Zenodo). The pipeline was written by the authors with assistance from GitHub Copilot (model claude-3.5-sonnet, accessed 2024-10) for code refactoring, docstring generation, and unit-test writing. All code was reviewed, tested, and integrated by the authors. Commit history is preserved; commits tagged 'copilot-generated' were produced with AI assistance and reviewed by the authors."

The pattern that satisfies reviewers: name the tool, the use case, the human-review step, and (where possible) tag the commits in the repository.

### Worked example 5 — Reviewer-side non-disclosure

> "Reviewer guidelines: Reviewers must not upload submitted manuscripts into public AI tools. Confidential peer-review material is a privileged channel; uploading it to a model that retains or trains on user input is a confidentiality breach. AI use to improve the clarity of the review report is permitted with disclosure to the editor."

This is not author-facing, but increasingly appears in editorial-style documents and reviewer guidelines. It is included here because the same principle — confidentiality of unpublished material — applies to authors as well.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesized from COPE Position Statement (Feb 2023), ICMJE Recommendations (AI language added 2023), Nature Editorial, Science Editorial (2023, updated), Cell Press Editorial Policies, and current ICML / NeurIPS / AAAI / ACL guidelines. Venue-by-venue matrix is original synthesis as of 2026-06.
