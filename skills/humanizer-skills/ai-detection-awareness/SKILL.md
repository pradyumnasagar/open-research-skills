---

name: ai-detection-awareness
description: "Use when you or your institution are using, evaluating, or responding to AI-detection tools (GPTZero, Turnitin, Copyleaks, Originality.ai, Pangram) — how detectors work, their failure modes, the limits of paraphrasing tools, and the move toward process-based assessment."
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

# AI Detection Awareness

> AI detection tools are now embedded in learning management systems, journal submission pipelines, and institutional review processes. They are also unreliable, particularly against non-native English writers, neurodivergent writers, and formal scientific prose. This skill is a working understanding of how detectors work, what they miss, who they harm when they are wrong, and why the institutional response is moving toward *process-based* assessment (draft history, oral defense, replication) rather than reliance on a single classifier's score.

## When to use

- You are evaluating an AI-detection tool for use in a classroom, lab, journal, or institutional workflow.
- You have been flagged by a detector and need to understand what the flag means — and what it does not.
- You are advising a student, mentee, or colleague whose work has been questioned on the basis of a detector score.
- You are designing a course or lab policy on AI use and want to ground the policy in a realistic understanding of the tools.
- You are deciding whether to use a paraphrase tool ("humanizer") to evade detection, and want a structural explanation of why this usually fails.
- You are writing a journal or institutional policy and want to understand the integrity argument for *process-based* assessment.

## When NOT to use

- You are looking for a tool that definitively proves whether a text was AI-generated. No such tool exists. Treat any vendor claim to the contrary with caution and look for independent, peer-reviewed validation in the current literature.
- You are using a detector's score as the sole basis for an academic-integrity accusation. The false-positive rate is too high and the populations harmed are too specific. A score is a *prompt to investigate*, not a conclusion.
- You are trying to choose between detectors to evade detection. This skill does not recommend specific tools for that purpose; the integrity argument runs in the other direction.
- You need a current benchmark of detector accuracy. Vendor-reported metrics change frequently and are not interchangeable; verify in the most recent peer-reviewed and third-party evaluations.

## Prerequisites

- A working understanding of how language models generate text (probabilistic next-token prediction with sampling). If this is unfamiliar, see the `ors-*` resources on transformer models.
- Access to the policies of the relevant institution or venue. Detection is policy-bound: a flag that matters at one institution may be informational at another.
- A willingness to update beliefs as detectors and policies change. The field is moving quickly; anything specific written here may be out of date within months.

## Core workflow

### 1. Understand the basic signals detectors use

Most current AI detectors combine several signals. The two most discussed in public materials are *perplexity* and *burstiness*.

- **Perplexity** measures how "surprising" a passage is to a language model. A passage that looks highly probable to the model (low perplexity) gets a higher AI-likelihood score on the assumption that an LLM would have generated the most-probable continuation. Human writing is, on average, higher-perplexity — humans are not next-token optimisers.
- **Burstiness** measures the variance of perplexity *within* a passage. Human writing tends to have bursts of low- and high-perplexity stretches (a complex sentence, a simple one, a list, a long clause). LLM output is more uniform. Detectors use burstiness as a secondary signal: a passage whose perplexity is uniformly low is more likely to be flagged.
- **Other signals.** Vendor-specific detectors add features: stylometric features (sentence length variance, vocabulary distribution), repetition patterns, paragraph-level parallelism, structural regularity, n-gram entropy, and trained classifiers on labelled corpora. The exact combination is vendor-specific and not always disclosed.

These signals are *probabilistic*. They produce scores, not verdicts, and the thresholds for flagging vary by vendor and by the population the detector was trained on.

### 2. Understand the documented failure modes

Detectors fail in well-characterised directions. The most important failure modes, in approximate order of harm:

- **False positives on non-native English writers.** Multiple independent analyses have shown that prose written by fluent non-native English writers is flagged at higher rates than prose written by native speakers. The structural reason: non-native writing has its own statistical regularities, and detectors trained predominantly on LLM-vs-native-English contrast learn to associate "non-native" features with "AI". If you use a detector, calibrate for this population.
- **False positives on neurodivergent writers.** Writers whose prose reflects autism-spectrum, ADHD, or dyslexic patterns (some structural repetition, lower hedging, more direct claims) have been reported in independent commentary and university teaching-and-learning centre guidance as over-flagged by detectors. Treat individual scores with caution and refer to accommodations processes where they exist.
- **False positives on formal scientific writing.** Scientific prose is itself stylistically constrained: low hedging in methods, regular paragraph structure, technical vocabulary, and a particular cadence. Detectors trained on general prose can flag scientific writing at higher rates. The signal is not that the text is AI; it is that the text is *formal*.
- **False negatives on edited or paraphrased LLM output.** The converse problem: LLM output that has been edited, even lightly, can drop below the flagging threshold. This is the failure mode that drives the arms-race concern.
- **False negatives on lightly prompted human writing.** A human who writes in a "neutral" register (uniform sentence length, generic intensifiers, low idiom) is closer to the LLM centroid than a human who writes distinctively. Distinctive writing is *less* likely to be flagged — the inverse of the naive expectation.
- **Domain drift.** Detectors trained on one model family (e.g. GPT-3.5-era) lose accuracy as new model families (e.g. Claude, Gemini, smaller specialised models) become dominant. Vendor updates try to keep up; the lag is real.

### 3. Understand paraphrase-tool failure modes

Tools marketed as "humanizers" (QuillBot's paraphrase modes, Grammarly's "humanize" feature, and various commercial services) operate on the surface of the text: they swap words, reorder clauses, sometimes change voice. The structural reasons they usually fail to evade detection:

- They do not change the *discourse-level* structure of the text. If an LLM produced a paragraph that begins with a topic sentence, lists three supporting claims, and ends with a summary, the paraphrase tool changes the words but keeps the structure. Current detectors and trained readers see through the structure.
- They often introduce meaning changes. A hedge like "this is a limitation" can become "this is a minor issue" in a paraphrase; that is a fabrication of confidence. A specific number can be approximated into a different number. These are not voice changes; they are claim changes.
- They are themselves an AI-driven transformation. Adding a second AI pass to a first AI pass does not produce human writing; it produces a doubly-processed artefact. The detector sees the artefact.
- The "arms race" framing is wrong for academic work. The integrity argument is not about defeating detectors; it is about writing truthfully. A manuscript that has been processed to evade detection is, by definition, less honest about its own origin.

The right response to a flat AI draft is not to paraphrase it; it is to rewrite it from your own understanding, with the source material in front of you. See `text-humanizing-editorial`.

### 4. Understand process-based assessment

The institutional response to detector unreliability is to shift the *evidence base* away from detector scores and toward process. Common process-based mechanisms:

- **Draft history.** Requiring access to the document's revision history (Google Docs, Overleaf track-changes, version control) so that the work can be examined as a process rather than as a final artefact.
- **Submission of intermediate artefacts.** Notes, outlines, query letters, data, code, and intermediate drafts, so that the provenance of claims is auditable.
- **Oral defense.** A viva, presentation, or Q&A in which the author explains the work in their own words. The strongest single signal of authorship, but expensive and not always available.
- **Replication and reproducibility.** Independent replication of the result; for code, independent re-implementation. The strongest signal of methodological authorship, but slow and not always practical.
- **Disclosure-based assessment.** A policy that requires honest AI disclosure (see `ai-disclosure-statement`) and treats undisclosed AI use as a separate integrity issue, independent of detection.
- **Authorship discussion.** Asking the author to describe the contribution of each co-author, including which sections were drafted by whom and with what tools. Combined with disclosure, this is a more reliable signal than a detector score.

Process-based assessment does not eliminate the problem. It shifts the work from "run a detector" to "design a process", and the latter requires institutional investment. It is, however, the direction most universities and journals are moving as of 2024-2026, precisely because detector-only assessment is not defensible.

### 5. When you are flagged

If you or your work is flagged:

- Ask for the *score*, not just the verdict. Most vendors produce a percentage or a band; the band matters.
- Ask which *detector* produced the flag, and on which *version*. Different detectors disagree; the same detector can disagree across versions.
- Do not panic-resign the paper. Most venues have an appeal or explanation process. Use it.
- Prepare a *process record*: draft history, intermediate artefacts, disclosure statement, notes. This is the most useful counter-evidence.
- If the flag was for a section you did not write (e.g. a co-author's contribution, a methods section auto-generated by a tool), say so. Specify the section.
- If the venue or institution has a known policy on this detector, follow it. If not, request a process-based review.

### 6. When you are advising a flagged student

A few rules of thumb:

- The score is evidence of a *classifier's output*, not of an action. Reframe the conversation in those terms.
- Specific populations are at higher false-positive risk. If the student is a non-native English writer, neurodivergent, or in a formal scientific field, mention this explicitly.
- The institution's accommodations and academic-integrity processes exist for a reason. Refer to them.
- Encourage the student to keep their *process* artefacts: revision history, notes, search logs. These are the strongest evidence in a process-based review.

### 7. Designing an institutional or course policy

If you are responsible for a policy:

- Do not adopt a detector as a *primary* signal. If you use one at all, treat the output as a prompt to investigate, not a conclusion.
- State the populations known to be at higher false-positive risk and document the mitigation. This is increasingly a legal-requirement as well as an ethical one.
- Combine any detector use with a process-based mechanism: disclosure requirement, draft history, viva, replication.
- Be explicit that "no AI was used" claims are an integrity claim, not a detector output, and that a flagged declaration is itself a violation.
- Update the policy annually. The field is moving quickly; a 2024 policy is not a 2026 policy.

## Code patterns

### Detector signal: a structural overview (pseudocode)

```python
# Pseudocode of a typical detector pipeline. Vendor implementations vary
# and most add features beyond this sketch. The point is structural.

def detector_score(text: str) -> float:
    # 1. Tokenize and compute per-token log-probabilities under one
    #    or more reference language models.
    per_token_logprob = reference_lm.score(text)

    # 2. Aggregate to a perplexity-like scalar.
    perplexity = exp(-mean(per_token_logprob))

    # 3. Compute burstiness: variance of per-sentence or per-window
    #    perplexity within the passage.
    burstiness = std(perplexity_per_window(text))

    # 4. Extract stylometric features (sentence length variance,
    #    vocabulary distribution, n-gram entropy, ...).
    stylometry = stylometric_features(text)

    # 5. Apply a trained classifier on (perplexity, burstiness, stylometry).
    score = classifier.predict_proba(perplexity, burstiness, stylometry)

    return score  # higher = more "AI-like" per the classifier
```

The same sketch explains why each failure mode happens: the perplexity and burstiness signals are correlated with style, not with authorship; the stylometric features are sensitive to register; the classifier is only as good as the labelled data it was trained on.

### A simple diagnostic for your own writing (Python)

```python
# Compare your prose's sentence-length variance and n-gram entropy to
# a few LLM baselines. This is a coarse, structural diagnostic, not a
# detector. It will not tell you whether you used AI. It will tell you
# whether your prose has the kind of structure that detectors flag.

import re
import math
from collections import Counter

def sentence_lengths(text: str) -> list[int]:
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    return [len(s.split()) for s in sents if s]

def ngram_entropy(text: str, n: int = 2) -> float:
    toks = re.findall(r"\w+", text.lower())
    grams = [tuple(toks[i:i+n]) for i in range(len(toks) - n + 1)]
    if not grams:
        return 0.0
    counts = Counter(grams)
    total = sum(counts.values())
    probs = [c / total for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def diagnose(text: str) -> None:
    lens = sentence_lengths(text)
    mean = sum(lens) / len(lens) if lens else 0
    var = sum((x - mean) ** 2 for x in lens) / len(lens) if lens else 0
    sd = var ** 0.5
    cv = sd / mean if mean else 0
    ent = ngram_entropy(text)
    print(f"sentences={len(lens)}  mean_len={mean:.1f}  cv={cv:.2f}  bigram_entropy={ent:.2f}")

    # CV < 0.35 across a passage is metronomic; this is a *structural*
    # diagnostic. It is consistent with AI output but does not prove it.
```

This is a writing-helper, not a detector. Use it to find metronomic passages and edit them; do not use it as evidence in an integrity case.

## Common pitfalls

- **Treating a detector score as evidence of misconduct.** It is not. It is a classifier output. The integrity question requires process, not a percentage.
- **Assuming a single detector is authoritative.** Detectors disagree, both across vendors and across versions. A single tool's output is not a basis for an accusation.
- **Assuming paraphrasing tools defeat detectors.** They usually do not, and they introduce integrity issues of their own. See Section 3 above.
- **Assuming non-native English writing is "less rigorous" because it is flagged.** The flag is a property of the detector, not of the writer.
- **Using detectors as the only assessment mechanism.** Process-based mechanisms (draft history, oral defense, replication) carry more weight and are fairer.
- **Writing a policy that is brittle to model updates.** A policy that depends on the current generation of detectors will be obsolete within a year. Write the policy around process and disclosure, not around the current tool.
- **Punishing students or authors without an appeal path.** Most institutions require one. The detector score alone does not satisfy the requirement.
- **Equating "passed the detector" with "written by a human".** A low score does not mean human authorship; it means the classifier did not flag.
- **Conflating detection with disclosure.** A detector score and a disclosure statement are different evidence. The disclosure statement is a more reliable signal of honesty; the detector score is a signal of textual features.

## Validation

You understand the state of detection well enough to act when:

- You can explain, in structural terms, what perplexity and burstiness measure and why they fail on specific populations.
- You can describe the failure modes of paraphrase tools without reaching for the "arms race" framing.
- You can name at least three process-based assessment mechanisms and explain when each is appropriate.
- You can advise a flagged student or author in terms of *process evidence*, not detector scores.
- You can write or review a course or journal AI policy that does not depend on a single detector.
- You can identify the populations at higher false-positive risk and design mitigations.

## Open alternatives

- For detection: there is no open-source detector that matches the best commercial tools, and the best commercial tools are not independently validated at the level required for high-stakes decisions. Process-based mechanisms are the open alternative.
- For "humanizing": there is no open-source "humanizer" that is integrity-safe. The right alternative is a rewrite-from-understanding workflow, supported by read-aloud review and the AI-tell scanner in `scientific-voice-style/SKILL.md`.
- For policy: open-licensed course and journal AI policies are available from several institutions; the structural features (process evidence, disclosure requirement, appeal path) are converging across them.

## References

- Public product and policy pages of GPTZero, Turnitin, Copyleaks, Originality.ai, Pangram. Vendor accuracy claims change frequently; verify in current documentation and in third-party peer-reviewed evaluations.
- University teaching-and-learning center guidance on AI detection and academic integrity. Verify in current institutional guidance for your context.
- ICMJE, COPE, and major journal guidance on AI in submissions. See `ai-disclosure-statement/SKILL.md`.
- Related `ors-*` skills: `ors-humanizer-skills-text-humanizing-editorial`, `ors-humanizer-skills-ai-disclosure-statement`, `ors-humanizer-skills-scientific-voice-style`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Sources: public statements and product pages of GPTZero, Turnitin, Copyleaks, Originality.ai, Pangram (structural summary; specific accuracy claims not repeated); representative university teaching-and-learning center guidance. Added: false-positive analysis by population, paraphrase-tool failure mode explained structurally, process-based assessment as the institutional direction.