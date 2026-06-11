---

name: ai-disclosure-statement
description: "Use when drafting or auditing an AI/LLM disclosure statement for a manuscript, preprint, grant, or venue — what to include, where to put it, and how to meet major journal and conference policies."
license: MIT
---




<!-- metadata:
category: humanizer-skills
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - humanizer-skills
  - research
difficulty: intermediate
-->

# AI Disclosure Statement

> A disclosure statement is a small paragraph that does outsized work: it is the record by which editors, reviewers, funders, and future readers judge whether you used AI responsibly. Get it wrong in either direction — under-disclosing, or padding it with performative detail — and you create risk that has nothing to do with the science. This skill is a drafting and audit guide for that paragraph, covering what to include, where to put it, and how to align with major journal and venue policies as of 2024-2026.

## When to use

- You used any LLM-based tool (ChatGPT, Claude, Gemini, Copilot, in-house models, domain-specific tools like Elicit, scite, or coding assistants) for any stage of the work and the paper is going to a venue with a stated AI policy.
- You are unsure which section the disclosure belongs in (Methods vs. Acknowledgments vs. a dedicated section vs. cover letter).
- You are writing a disclosure for a specific venue and want a working template, not a generic checklist.
- You are auditing a manuscript or mentee's draft for missing or over-broad AI disclosure.
- You are submitting a preprint, registered report, or grant application with AI involvement.

## When NOT to use

- No AI tool was used at any stage. Most venues do not require a statement in this case, though some ask you to affirm "no AI was used." Verify in the target venue's policy.
- You are describing the *scientific use* of an AI/ML method that is part of the methodology (e.g. AlphaFold for structure prediction, a neural network model as a benchmark). That belongs in Methods, not in an AI disclosure, and uses a different framing. See your methods-writing skill.
- The question is about *authorship* of an LLM (whether an LLM can be a co-author). That is a policy question, not a drafting question; consult the venue's authorship criteria (ICMJE for biomedicine, venue-specific for others).
- You are writing for a venue without a stated AI policy and have no institutional requirement. A short, accurate disclosure is still good practice, but the templates below are not load-bearing.

## Prerequisites

- A record of which AI tools you used, at which stages (ideation, literature triage, drafting, copyediting, code generation, figure production, data analysis), and on which sections.
- Access to the current AI policy of the target venue. **Policies update frequently** — verify in the journal's or conference's author guidelines page before submission. Treat the venue-specific guidance in this skill as a structural map, not a verbatim quote of current policy text.
- A working draft of the paper or submission, so the disclosure can be located correctly.

## Core workflow

### 1. Determine whether a disclosure is required

Start from the venue's policy, not from the absence of a rule. As of 2024-2026:

- Most major biomedical and life-sciences journals (Nature, Science, Cell, PNAS, PLOS, eLife, JAMA, Lancet, BMJ, NEJM) require disclosure of AI assistance at the time of writing. Verify the current wording in the target journal's author guidelines.
- Major ML and NLP conferences (ICML, NeurIPS, AAAI, ACL and its workshops) have explicit policies. Conference policies have evolved quickly; check the current year's author guidelines and any specific instructions on LLM use.
- Many funders (NIH, Wellcome, ERC, UKRI, major private foundations) have released guidance covering grant writing and the research record. Fundees' institutional policies may apply even when the venue is silent.
- A growing number of journals require disclosure for *any* AI-assisted step — including grammar, copyediting, reference formatting, and figure production. Read the policy carefully: "AI assistance" is often defined broadly.

If the venue is silent and your institution has a policy, follow the institutional policy and disclose.

### 2. Decide where the statement goes

The placement depends on the venue and on the *role* the AI played. There are four common placements:

- **Methods.** If AI was used as a *method* (e.g. LLM-assisted coding, AI-based image analysis, an LLM used to score or classify data, model-assisted data extraction), describe the tool, version, and how it was used. This is the most rigorous placement and is required by venues that treat AI as a methodological tool.
- **Acknowledgments.** If AI was used only for language polishing, copyediting, or drafting assistance without methodological role, most venues accept disclosure in Acknowledgments. This is the most common placement for "used ChatGPT to improve phrasing" cases.
- **A dedicated section** (e.g. "AI use", "Use of AI tools", or a numbered section in Methods). Some venues require or encourage this; check the policy.
- **Cover letter / submission form.** Some venues ask for the disclosure in the submission form *in addition to* the manuscript. Putting it only in the cover letter is rarely sufficient.

A safe default: if the AI did methodological work, describe it in Methods *and* acknowledge it in the cover letter. If the AI did only writing/editorial work, a single acknowledgment is usually enough.

### 3. Draft the statement

A disclosure statement should answer five questions in plain language. The exact phrasing will vary; the structure should be consistent.

1. **What tool was used?** Name the model or product (e.g. "GPT-4", "Claude 3.5", "ChatGPT", "GitHub Copilot", "an in-house LLM"). Include the version where the venue requires it; otherwise a model family name is acceptable.
2. **What was the scope of use?** Specify the sections or stages. Examples: "assistance in drafting the Introduction", "literature triage for the Related Work section", "code generation for the analysis pipeline in Methods 4.2", "language polishing of the Discussion".
3. **What was the prompt or workflow?** This is the most-debated element. Most current policies do *not* require you to publish every prompt. Some require a representative example or a summary of the workflow. Do not paste a multi-page transcript unless the venue asks.
4. **How was the output verified?** State that a human author reviewed, edited, and takes responsibility for the content. Be specific: "All AI-generated text was reviewed, edited, and approved by the authors."
5. **What is excluded?** If the AI was *not* used for a category the venue is likely to ask about (e.g. "AI was not used for data collection, statistical analysis, or figure generation"), say so.

### 4. Avoid the common failure modes

Both over-disclosure and under-disclosure create problems.

Under-disclosure failure modes:

- Stating "no AI was used" when any tool was used, even for trivial edits. If a tool was used, the statement must be honest. Reviewers and editors can often tell.
- Omitting the tool name or version when the venue asks for it.
- Putting the disclosure in the cover letter only and leaving the manuscript silent.
- Failing to disclose AI-assisted *image* or *figure* generation. Several journals have specific rules here; treat image work as a separate, prominent disclosure.

Over-disclosure failure modes:

- Pasting a full chat transcript into the manuscript. This is rarely required and reads as evasion. Summarise the workflow; offer the transcript on request.
- Listing every prompt. This is noise, and many venues will not read it.
- Hiding methodological work behind "AI-assisted writing". If AI did real work, name it as a method.
- Adding false confidence: "AI-generated text was verified for accuracy" when no such verification was performed. Verification is a process; describe the process.

### 5. Cross-check venue-specific rules

A few high-frequency checks:

- **Image / figure generation.** Many venues explicitly forbid or restrict AI-generated images. Verify before including.
- **Reference / citation generation.** Several venues forbid LLM-generated citations or require author verification of every citation. Disclose even if you verified.
- **Authorship.** No major venue accepts an LLM as an author as of 2026. If your co-author list includes a non-human entity, that is almost certainly a desk-rejectable error.
- **Data and privacy.** Some venues forbid uploading unpublished data or identifiable patient data to commercial AI services. If you used a cloud LLM, you may have to say so.
- **Conflicts of interest.** AI tool providers may, in some interpretations, represent a conflict (e.g. if the tool's vendor funded the work). This is a gray area; check with the target venue.

### 6. Audit the final statement

Before submission, read the statement aloud and ask:

- Could a reviewer unfamiliar with my workflow understand what I did?
- Does the placement match the venue's policy?
- Did I claim verification I did not perform?
- Did I omit any tool I actually used?
- Does the statement match the AI-tell *content* of the manuscript? A paper whose prose is heavily AI-flavored and whose disclosure is one sentence is a mismatch a reviewer will notice.

## Code patterns

### Template: Methods placement (AI used as a method)

```
LLM use (Methods, e.g. section 4.2 — or as the venue requires)

We used [model name, version] via [interface: API / web UI / in-house deployment]
to [specific methodological step]. Prompts were [summarise workflow in one sentence
or list representative prompts; do not paste full transcripts]. All model outputs
were reviewed by [author initials] and verified against [ground truth / source data /
manual inspection]. The model was not used for [explicit exclusions, e.g. data
collection, statistical inference, figure generation].
```

### Template: Acknowledgments placement (writing / language only)

```
Acknowledgments (add as a new paragraph)

During the preparation of this work, the authors used [model name] to
[scope: e.g. "improve the clarity and grammar of the Introduction and
Discussion"]. After using this tool, the authors reviewed and edited the
content as needed and take(s) full responsibility for the content of
the publication.
```

This template is structurally common; the exact wording required varies by venue. Verify against the journal's current policy and adapt accordingly.

### Template: Dedicated AI-use section (where the venue requires it)

```
Use of AI tools

Models and versions. [List, with versions and access dates if the venue requires.]
Sections of involvement. [Bullet list mapping tool -> section -> role.]
Workflow. [One paragraph: how prompts were constructed, how outputs were selected,
how they were integrated.]
Human oversight. [Who reviewed, what they checked, what was rejected or rewritten.]
Exclusions. [List of steps where AI was not used.]
Data and privacy. [Whether unpublished or identifiable data was provided to the
model, and if so, the safeguards used.]
```

### Venue-specific structural map (verify in current policy)

This table is a *structural* map, not a verbatim quote of any current policy. Use it as a starting point, then verify.

| Venue family | Typical placement | Common requirements | Verify at |
| --- | --- | --- | --- |
| Nature portfolio | Methods + cover letter | Tool, version, role, human verification | Nature author guidelines (current) |
| Science | Methods or Acknowledgments | Tool, scope, verification | Science author guidelines (current) |
| Cell | Methods or dedicated section | Tool, version, scope | Cell author guidelines (current) |
| PNAS | Methods | Tool, version, role in study | PNAS author guidelines (current) |
| PLOS | Methods or submission form | Tool, version, scope, verification | PLOS AI policy (current) |
| eLife | Methods or dedicated section | Tool, version, scope; image rules | eLife AI policy (current) |
| ICML / NeurIPS | Acknowledgments or paper section | Tool, scope, full responsibility claim | Conference call papers (current year) |
| AAAI | Acknowledgments | Tool, scope; author responsibility | AAAI author instructions (current) |
| ACL / EMNLP | Acknowledgments or Limitations | Tool, scope, limitations | ACL policy (current year) |
| JAMA | Methods or Acknowledgments | Tool, version, scope; ICMJE-aligned | JAMA Instructions for Authors (current) |
| Lancet | Methods or Acknowledgments | Tool, version, scope | Lancet author guidelines (current) |
| BMJ | Methods | Tool, version, scope; data privacy | BMJ AI policy (current) |
| NEJM | Methods or Acknowledgments | Tool, version, scope; ICMJE-aligned | NEJM Author Center (current) |

If the venue does not appear above, default to: Methods for any methodological role; Acknowledgments for editorial use; check the submission form for an AI-use field.

### Decision tree (textual)

1. Did AI play a methodological role? -> Methods, with the model treated as a method.
2. Was AI used only for writing/editorial work? -> Acknowledgments.
3. Does the venue require a dedicated section? -> Add it, with cross-references to Methods if relevant.
4. Does the submission form ask for AI use? -> Answer it, even if the manuscript also discloses.
5. Did AI generate or alter images? -> Prominent disclosure in figure caption or Methods, per venue rules.
6. Are you unsure? -> Disclose in both Methods and Acknowledgments, and offer to provide prompt logs on request.

## Common pitfalls

- **Treating the venue's policy as a recommendation.** For most major journals, the policy is a requirement. Failure to disclose is a corrigenda-class error, not a stylistic one.
- **Confusing "AI-assisted writing" with "AI as a method".** Spelling and grammar checks do not require Methods placement; data analysis with an LLM does. The placement should reflect the role.
- **Using the same generic disclosure for every venue.** Different venues ask different questions. Read each policy and adapt.
- **Pasting chat logs as a substitute for clear writing.** A 30-page transcript is not a disclosure; it is a deflection. Summarise, point, offer on request.
- **Forgetting to disclose AI-assisted *figure* generation or *code* generation.** These are common oversight cases and are usually treated more strictly than writing assistance.
- **Letting the AI write its own disclosure.** This is circular and is exactly the kind of mismatch a reviewer will catch. The disclosure is a high-stakes paragraph; write it yourself.
- **Disclosing only in the cover letter.** Most venues treat the cover letter as confidential to the editor; reviewers and readers will not see it. The disclosure must be in the manuscript too.
- **Ignoring data-privacy implications.** Submitting identifiable human data or unpublished results to a commercial LLM can violate the venue's data-sharing policy and, in some jurisdictions, the law. Disclose the route.
- **Forgetting grant and preprint versions.** If you put a preprint on arXiv or bioRxiv and later revise for a journal, the preprint disclosure and the journal disclosure should match.
- **Letting the disclosure drift from the manuscript.** A statement that says "AI was used only for grammar" while the prose is heavily AI-flavored is a red flag. Make the disclosure match the artefact.

## Validation

A disclosure statement is well-formed if:

- A reviewer can identify the tool, the section, and the verification step from the disclosure alone.
- The placement matches the venue's policy and the role AI played.
- The disclosure is consistent with the manuscript's actual prose and figures.
- The statement names a specific human author who takes responsibility.
- The statement has been cross-checked against the current venue policy (not a 2023 blog post).
- The manuscript's reference list has been verified by a human, even if AI helped format it.
- The data-privacy story is consistent with what was uploaded to any external LLM.

## Open alternatives

- For drafting a disclosure from scratch, write the first sentence yourself and let the model complete a structured template. Do not let the model invent the tool name, version, or scope.
- For institutional policy cross-checks, your institution's research-integrity office will have a current list of accepted phrasings. Prefer these over generic templates.
- For maintaining consistency across a lab's outputs, draft a short lab-level "AI use policy" that all members cite. This is faster and more coherent than per-paper disclosures.

## References

- ICMJE Recommendations. *Defining the Role of Authors and Contributors.* Verify current version at icmje.org.
- COPE position statement on AI authorship. Verify current wording at publicationethics.org.
- Nature, Science, Cell, PNAS, PLOS, eLife, ICML, NeurIPS, AAAI, ACL, JAMA, Lancet, BMJ, NEJM — author guidelines and AI policies. **Policies update frequently; verify in the current author guidelines before submission.**
- NIH, Wellcome, ERC, UKRI guidance on AI in research. Verify current versions on each funder's site.
- Related `ors-*` skills: `ors-humanizer-skills-ai-detection-awareness`, `ors-humanizer-skills-text-humanizing-editorial`, `ors-scientific-writing-manuscript-structure`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Sources: ICMJE Recommendations; COPE position on AI authorship; current public AI policies of Nature, Science, Cell, PNAS, PLOS, eLife, ICML, NeurIPS, AAAI, ACL, JAMA, Lancet, BMJ, NEJM (verified structurally; specific text varies by venue and updates frequently). Added: venue placement decision tree, common under- and over-disclosure failure modes, Methods vs. Acknowledgments template variants.