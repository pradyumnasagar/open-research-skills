---

name: ai-disclosure-writing
description: "AI/LLM usage disclosure for biomedical manuscripts: which journals require disclosure (Nature, Science, Cell), what counts as AI authorship (banned) vs. AI tool use (allowed with disclosure), text snippets for common policies, ICMJE/COPE positions, and image-AI specific rules."
license: MIT
---




<!-- metadata:
category: scientific-writing
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - scientific-writing
  - research
difficulty: intermediate
-->

# AI/LLM Usage Disclosure in Manuscripts

> AI tools — large language models (LLMs), image generators, code assistants, transcription services — are now used at almost every stage of the research and writing process. Biomedical journals have converged on a position: AI tools cannot be authors, but their use must be disclosed. The position is consistent across ICMJE, COPE, Nature, Science, Cell, and the major general-interest journals. The details vary (which use cases require disclosure, where the disclosure goes, and whether image generation is permitted at all), and the policies are evolving quickly. This skill encodes the consensus framework, the journal-specific variations, the language templates for the Methods and Acknowledgments sections, and the image-AI specific rules that have tightened considerably since 2023.

## When to use

- Drafting a manuscript that has used an LLM (ChatGPT, Claude, Gemini, Llama, etc.) for text drafting, editing, translation, code generation, or figure generation.
- Responding to a journal's AI-disclosure requirement during submission.
- Updating the Methods or Acknowledgments section to declare AI use.
- Drafting the AI-disclosure section for a preprint server.
- Reviewing a manuscript for compliance with the target journal's AI policy.
- Responding to a peer-review comment about AI use in a manuscript.

## When NOT to use

- For non-AI editing tools (spell-check, grammar-check without an LLM) — these are typically not in scope of AI-disclosure policies.
- For pure computational tools (sequence aligners, statistical models, image-analysis software) — these are methods, not AI authorship.
- For AI use in the peer-review process (this is governed by the journal's reviewer guidelines, not the manuscript's disclosure).
- For grant applications (different policies; consult the funder).

## Prerequisites

- An audit log of which AI tools were used, for which tasks, and by which author.
- Knowledge of the target journal's AI policy (read the journal's policy page before drafting)."
- Co-author agreement on the disclosure language, especially the boundary between "AI-assisted" and "AI-authored."
- A decision on whether any figure was generated or modified by an image-AI tool (most top-tier journals prohibit this).

## Core workflow

### 1. Audit AI use before drafting the disclosure

The disclosure must be specific. Audit the manuscript for AI use in five categories:

| Category | Example | Disclose? |
|----------|---------|-----------|
| Text drafting | LLM drafted the first draft of a paragraph | Yes |
| Text editing | LLM edited the authors' text for grammar and clarity | Yes (most journals) |
| Text summarization | LLM summarized a paper for the literature review | Yes |
| Code generation | LLM wrote the analysis code | Yes (Methods section) |
| Code debugging | LLM identified a bug in the analysis code | Yes (most journals) |
| Figure generation | AI generated a figure or a figure panel | Yes (most journals prohibit) |
| Figure editing | AI modified a microscope or radiology image | Yes (most journals prohibit) |
| Image annotation | AI labeled cells in a histology image | Yes (Methods section) |
| Translation | LLM translated text into English for non-native authors | Yes (Acknowledgments) |
| Literature search | LLM helped identify candidate papers | Usually no (the search results must still be verified) |
| Statistical analysis | LLM suggested a statistical test | Yes (Methods section) |
| Spell-check, grammar-check without an LLM | Standard writing tool | No |
| Computational tool (BLAST, DESeq2, Cellpose) | Not AI authorship | No (standard methods citation) |

### 2. Read the target journal's AI policy before drafting

The policy pages that govern this skill, all publicly accessible:

| Publisher | Policy page (publicly known URL) |
|-----------|----------------------------------|
| Nature Portfolio | nature.com/nature-portfolio/editorial-policies/ai |
| Science | science.org/policies/ai-use |
| Cell Press | cell.com/press-room/ai |
| Elsevier | elsevier.com/about/policies-and-standards/publishing-ethics |
| Springer Nature | nature.com/nature-portfolio/editorial-policies/ai (overlaps with Nature Portfolio) |
| PLOS | plos.org/ai-policy |
| eLife | elifesciences.org/peer-review (peer-review AI section) |
| JAMA Network | jamanetwork.com/journals/jama/pages/instructions-for-authors |
| NEJM | nejm.org/author-center |
| Lancet | thelancet.com/publishing-with-us |

The policies evolve. Always check the current version of the policy page before drafting the disclosure.

### 3. Place the disclosure in the right section

| Disclosure content | Section |
|--------------------|---------|
| LLM used for text drafting or editing | Acknowledgments or Methods (per journal) |
| LLM used for code generation or debugging | Methods (with version, date, query logs) |
| LLM used for image analysis or annotation | Methods (with model, version, parameters) |
| Image-AI generated or modified a figure | Methods + a note in the figure legend (most journals prohibit) |
| LLM used for translation | Acknowledgments |
| AI tool used for literature search | Generally not disclosed (but verifiable by the authors) |

### 4. Write the disclosure in three parts

Every AI disclosure has three parts:

1. **What tool was used** (model name, version, vendor).
2. **For what purpose** (text drafting, code generation, image annotation, etc.).
3. **To what extent** (entire draft, specific sections, line-edits only, etc.).

Vague disclosures ("we used AI to improve the manuscript") are increasingly desk-reject triggers. Specific disclosures ("GPT-4 was used to draft the first version of the Methods section, which the authors then reviewed and revised") are accepted.

### 5. Do not list the AI as an author

Across all major biomedical journals, AI tools cannot be authors or co-authors. The author byline must list only human authors who meet the ICMJE four-criterion authorship standard. The disclosure goes in the Acknowledgments or Methods, not in the author list.

## Code patterns

### Disclosure snippets by use case

**Text drafting, LLM**

> "GPT-4 (OpenAI, version 2024-04-09) was used to draft the first version of the Methods section, which the authors then reviewed, edited, and finalized. The authors take full responsibility for the content of the manuscript."

**Text editing, LLM**

> "The authors thank [Tool Name] for language editing assistance. The tool was used to identify and correct grammatical errors and to suggest alternative phrasings. All edits were reviewed and approved by the authors."

**Code generation, LLM**

> "GPT-4 (OpenAI) was used to assist in writing the Python code for the single-cell analysis. The authors reviewed, tested, and validated all generated code. The full code is available at [GitHub URL]."

**Image annotation, LLM**

> "Cellpose (version 2.2) was used for cell segmentation. The model was trained on the authors' own annotated images; no pre-trained model weights were used. The segmentation masks were manually reviewed by [author name] before downstream analysis."

**Translation, LLM**

> "The authors thank DeepL Write for assistance in preparing the English version of the manuscript. The authors are native [language] speakers and reviewed all translations."

**Figure generation (most journals prohibit)**

> "No figure in this manuscript was generated or modified by an AI tool. All figures were created using [software: e.g., GraphPad Prism, Adobe Illustrator, BioRender]."

**Figure with AI-assisted image analysis (permitted in Methods, not in the figure itself)**

> "The histopathology images in Figure 3 were quantified using a custom-trained U-Net segmentation model. The model architecture and training data are described in the Methods. The segmentation masks were manually reviewed by [author name]."

### Methods-section language for AI use

When AI use is part of the methodology (e.g., image segmentation, protein structure prediction, single-cell annotation), the Methods section should read like a methods citation, not like a disclosure:

> "Single-cell RNA-sequencing data were annotated using the CellTypist model (version 1.0.0) with the default lung atlas reference. Cell labels were reviewed by [author name] using canonical marker gene expression. Annotations with low confidence scores (<0.5) were excluded from downstream analysis."

> "Protein structures were predicted using AlphaFold 3 (DeepMind, version 2024) and the predicted local-distance difference test (pLDDT) was used to assess confidence. Structures with pLDDT <70 were excluded from analysis."

The Methods citation approach is preferred over the Acknowledgments approach when the AI tool is genuinely part of the analysis pipeline.

### Acknowledgments-section language for AI use

When the AI use is editing or translation (not a methods component), the Acknowledgments section is the right place:

> "Acknowledgments: We thank the authors of [Tool Name] for the language-editing tool used in the preparation of this manuscript. The authors take full responsibility for the content."

> "Acknowledgments: GPT-4 (OpenAI) was used to draft the first version of the Discussion section. The authors subsequently revised and finalized the section. We thank the editor and reviewers for their thoughtful comments."

### Disclosure for the cover letter (transparency)

The cover letter can include a brief AI-disclosure line if the journal requests it:

> "We confirm that the manuscript was prepared in accordance with [Journal name]'s AI policy. GPT-4 was used to draft the first version of the Methods section, which the authors reviewed and finalized. All authors take responsibility for the content."

### Disclosure for image-AI use (most journals prohibit)

When an image-AI tool has been used to generate or substantially modify a figure, the disclosure must be specific and prominent. Most top-tier journals prohibit this; for the journals that permit it, the disclosure goes in the Methods and the figure legend.

> "Figure 4 was generated using DALL-E 3 (OpenAI) with the prompt '[prompt text]'. The image was reviewed by [author name] and modified in Adobe Illustrator. The use of AI-generated imagery is consistent with the journal's image policy."

> "No figure in this manuscript was generated or modified by an AI tool. All images are derived from the authors' own experimental data or from public datasets cited in the legend."

### Code-sharing language for AI-assisted code

When AI-assisted code is part of the analysis, the methods should describe the level of human review and provide a public link to the code:

> "All code used in this study is available at [GitHub URL]. The code was written in collaboration with GPT-4 (OpenAI) and reviewed and tested by [author name]. The repository includes the version of the model used and the date of generation."

### Authorship statement (universal, all journals)

The author list must include only human authors. Even when an AI tool contributed substantively to the manuscript, the byline must read:

> Authors: [List of human authors]
> Author contributions: [per CRediT taxonomy, with each contribution attributable to a named human author]
> AI use: [disclosed in Methods or Acknowledgments]

### Decision tree: where does the AI use go?

```
Did the AI tool generate or modify a figure?
├── Yes → Most top-tier journals prohibit. Revise the figure
│         to be human-generated, or note prominently in the
│         Methods + figure legend if the journal permits.
│
Did the AI tool write or substantially edit manuscript text?
├── Yes → Disclose in Acknowledgments with tool name,
│         version, and extent of use.
│
Did the AI tool write or debug analysis code?
├── Yes → Disclose in Methods with tool name, version, and
│         code review process. Link to public repository.
│
Did the AI tool annotate or segment images?
├── Yes → Disclose in Methods as a methods component
│         (model name, version, training data, review process).
│
Did the AI tool translate text?
├── Yes → Disclose in Acknowledgments; native-speaker review
│         of the translation.
│
Did the AI tool search the literature?
└── No standard disclosure required, but the authors must
  verify the search results before citing.
```

### Decision tree: which journal-specific policy applies?

```
Target journal
├── Nature, Science, Cell, Lancet, NEJM, JAMA
│   └── Strictest policies. AI cannot be an author. AI use
│       must be disclosed. Image-AI is generally prohibited.
│
├── PLOS, eLife, BMJ Open, F1000Research
│   └── Aligned with ICMJE. AI cannot be an author. AI use
│       must be disclosed. Image-AI is generally prohibited.
│
├── Specialty society journals (JBC, Blood, JCI, etc.)
│   └── Check the journal's policy page. Most follow the
│       ICMJE/COPE position.
│
└── Preprint servers (bioRxiv, medRxiv, arXiv)
    └── No formal AI policy; transparency is the norm.
        Disclose AI use in the manuscript.
```

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| "We used AI to improve the manuscript" | Vague; does not identify the tool or the extent | Name the tool, the version, the section, and the extent of use |
| Listing the AI in the author byline | All major journals reject this | List only human authors; disclose AI in Acknowledgments or Methods |
| LLM wrote the literature review and the authors did not verify the citations | LLM may hallucinate references; the manuscript will be flagged | Verify every reference the LLM produced |
| AI generated a figure and the manuscript does not disclose it | Editorial return; possible rejection | Disclose all AI use; consider revising the figure to be human-generated |
| LLM-assisted code was not reviewed or tested | Code bugs invalidate the analysis | State explicitly that the code was reviewed and tested; link to the public repository |
| LLM translated text and the authors are not native English speakers, but the translation was not reviewed | The translation may contain errors | State explicitly that a native English speaker reviewed the translation |
| LLM-edited text with a style the journal prohibits (e.g., LLM added a list of bullet points where the journal requires prose) | The journal will ask for a rewrite | Match the journal's style; manual revision after LLM editing |
| Disclosure in the wrong section | Some journals require Methods, others require Acknowledgments | Read the journal's policy page; place the disclosure in the section they specify |
| No version or date for the AI tool | The reviewer cannot reproduce the use | State the model name, the version, and the date of use |
| The same disclosure is copy-pasted from another manuscript | The disclosure is not specific to the present manuscript | Write a disclosure that is specific to the manuscript's actual use |
| "No AI was used" when the manuscript has clearly been LLM-polished | Reviewer can detect the writing style; the claim damages trust | Disclose the AI use; honest disclosure is a positive signal |
| AI used for statistical analysis without disclosure | The reviewer may flag the lack of methods | Disclose the AI-assisted analysis in the Methods section |
| LLM generated an image for the graphical abstract and the journal prohibits it | Editorial return | Avoid AI-generated images; commission a human-designed graphical abstract |

## Image-AI specific rules

Image-AI is the most regulated AI use case. The current state of the policies (as of 2026):

| Use case | Most journals' position |
|----------|------------------------|
| AI generated the figure from scratch (DALL-E, Midjourney, Stable Diffusion) | Generally prohibited in top-tier journals (Nature, Science, Cell, Lancet, NEJM, JAMA) |
| AI modified a real experimental image (added a panel, filled in a region) | Generally prohibited in top-tier journals |
| AI annotated a real image (cell segmentation, lesion detection) | Permitted with disclosure in Methods (Cellpose, StarDist, etc.) |
| AI helped design a graphical abstract (BioRender + AI suggestions) | Permitted; check the journal's specific guidance |
| AI predicted a protein structure (AlphaFold 3, Boltz-1) | Permitted with citation; the predicted structure is a result, not an image |
| AI synthesized a microscopy image (e.g., denoising, deconvolution) | Permitted with disclosure; cite the software and parameters |

The general rule: image-AI that creates or modifies content is treated as a falsification risk and is prohibited; image-AI that analyzes or annotates real content is treated as a methods tool and is permitted with disclosure.

## ICMJE and COPE positions

The ICMJE Recommendations state that AI tools cannot be authors. The four-criterion authorship standard (substantial contributions to conception or design; drafting or critical revision; final approval; accountability) requires human capacity; AI cannot meet the standard. The disclosure requirement is mirrored in the Methods or Acknowledgments.

The COPE position on AI authorship is consistent: AI tools cannot be authors, and their use must be disclosed. The position was published in 2023 and updated in 2024 and 2025 to address image-AI specifically.

The WAME (World Association of Medical Editors) position is consistent with ICMJE and COPE, with additional guidance on AI use in peer review (which is a separate, journal-controlled process).

## Validation

An AI disclosure passes validation when:

- The disclosure is specific (tool name, version, date, section, extent).
- The disclosure is in the section the journal requires (Methods, Acknowledgments, or both).
- The author byline does not include any AI tool.
- The disclosure is consistent with the journal's current AI policy.
- The code-sharing link (if applicable) is public and works.
- The figure legends disclose any AI-assisted image analysis.
- No figure was generated or modified by an AI tool (or the journal permits it and the disclosure is prominent).
- The corresponding author has signed off on the disclosure.
- The co-authors are aware of the AI use and the disclosure.

## Open alternatives

The AI tools themselves are commercial or open-weight. The disclosure workflow does not require any specific tool; the disclosure is text.

| Commercial / closed-weight | Open-weight / open-source alternative |
|----------------------------|---------------------------------------|
| GPT-4 (OpenAI) | Llama 3, Mistral,  |
| Claude (Anthropic) | Llama 3, Mistral |
| Gemini (Google) | Gemma |
| DALL-E 3 (image) | Stable Diffusion, FLUX |
| Midjourney (image) | Stable Diffusion, FLUX |

For open peer-review platforms (eLife, F1000Research, OpenReview), the AI disclosure is part of the public review history. The disclosure text is the same as for non-open platforms.

## References

- Nature editorial policies on AI. nature.com/nature-portfolio/editorial-policies/ai
- Science AI use policy. science.org/policies/ai-use
- Cell Press AI policy. cell.com/press-room/ai
- ICMJE Recommendations. icmje.org/icmje-recommendations.pdf
- COPE position on AI authorship. publicationethics.org/cope-position-position-authorship
- WAME recommendations on AI. wame.org
- NIH policy on AI use in peer review. nih.gov
- Elsevier AI policy. elsevier.com/about/policies-and-standards/publishing-ethics
- eLife peer-review AI section. elifesciences.org/peer-review
- PLOS AI policy. plos.org/ai-policy
- JAMA Network instructions for authors. jamanetwork.com/journals/jama/pages/instructions-for-authors

## Related Skills

- ors-scientific-writing-manuscript-structure — for the manuscript that the disclosure is part of.
- ors-scientific-writing-cover-letter — for the cover letter that may include a brief AI-disclosure line.
- ors-scientific-writing-rebuttal-letter — for the rebuttal if a reviewer flags an AI-use concern.
- ors-ethics-compliance-authorship-disputes — for the ICMJE authorship criteria applied to the human author list.
- ors-scientific-writing-response-to-reviewers — for the format of the response if the AI disclosure is the subject of a reviewer comment.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Consolidated public AI-disclosure guidance from ICMJE, COPE, WAME, Nature Portfolio, Science, Cell Press, PLOS, eLife, Elsevier, JAMA Network, and NIH. Included the consensus framework (AI cannot be author, but must be disclosed), disclosure snippets for common use cases (text drafting, code generation, image annotation, translation, image-AI generation), decision trees for placement and journal policy, and image-AI specific rules. No specific journal policies are quoted verbatim; all sources are publicly accessible via the URLs above.