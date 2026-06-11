---
name: text-humanizing-editorial
description: "Use when editing AI-assisted or AI-generated text so that it reads as written by a knowledgeable human — workflow from AI draft to authorial voice, what to keep, what to rewrite, and the line that humanizing must not cross."
license: MIT
---



<!-- metadata:
category: humanizer-skills
version: 1.0.0
author: Pradyumna Jayaram
tags:
- editing
- voice
- ai-tells
- rewriting
- scientific-writing
- integrity
difficulty: intermediate
prerequisites:
  tools: []
  skills:
  - ors-humanizer-skills-scientific-voice-style
  - ors-humanizer-skills-ai-detection-awareness"
sources: "Original: Pinker, S. The Sense of Style — Adapted: reader-experience\
  \ and unit-of-thought passes paraphrased for AI-assisted editing; Original: Sword,\
  \ H. Stylish Academic Writing — Adapted: 'rewrite from understanding' rule\
  \ applied to AI drafts; Original: Gopen, G. D. & Swan, J. A. The Science of Scientific\
  \ Writing — Adapted: structural pass is the final edit, not the first; Improvisions:\
  \ AI-tell -> rewrite playbook, 'what to keep / what to rewrite / what not to do'\
  \ rule set, paraphrasing-tool failure mode explained structurally"
-->

# Text Humanizing (Editorial)

> Humanizing is the editorial work of turning text that reads as machine-generated into text that reads as written by someone who knows the field. It is a craft skill, not a synonym for "paraphrase until undetectable." Done well, it recovers the author's voice without changing the underlying claims; done badly, it smuggles fabrication, removes caveats, or substitutes vocabulary churn for understanding. This skill describes the workflow, the AI tells to rewrite, the rewrite playbook, and the integrity boundary that the work must not cross.

## When to use

- You have an AI-assisted draft (your own prompt, an LLM suggestion, a copyediting pass) and want to convert it into prose that reads as yours.
- You are reviewing a mentee's AI-assisted draft and want to give actionable edits, not vibes.
- You are auditing your own prose for AI tells before submission.
- You are building a lab workflow for AI-assisted writing that preserves voice and accuracy.
- You are responding to a reviewer or editor who flagged the prose as AI-flavored.

## When NOT to use

- You are trying to evade AI detection. Paraphrase-only passes do not reliably do this (see `ai-detection-awareness`), and treating humanizing as evasion is a misuse of the skill.
- The underlying claims are wrong. Humanizing fixes voice, not facts. If the draft is incorrect, fix the science first.
- The text is for a tightly regulated format (structured abstracts, regulatory submissions) where voice is not the goal. Use a copyediting skill.
- The draft is someone else's work (a collaborator's, a mentee's) and they did not ask for an AI-style overhaul. Editing someone else's prose without permission changes the authorship signal.
- You are looking for synonyms. Synonym substitution is the most superficial form of humanizing and is detectable. Do not start there.

## Prerequisites

- An AI-assisted (or AI-flavored) draft. The skill is for editing existing text.
- A clear sense of what *you* would have written. If you cannot articulate that, the draft is doing work you do not yet understand; do not humanize it — go back to the source material.
- Familiarity with the conventions and cadence of the target register. Voice work without register-awareness produces generic prose in a different key.
- A read-aloud habit. The fastest way to find AI residue is to listen to the prose.

## Core workflow

### 1. Separate the voice problem from the truth problem

Before any rewrite, ask: is the passage *wrong*, *unclear*, or *flat*? Each gets a different fix.

- Wrong -> fix the claim, not the voice. Cite the source.
- Unclear -> restructure. Use the Gopen-Swan unit-of-thought pass; stress the new information.
- Flat -> humanize. This is what the rest of the skill addresses.

Do not blend the three. The fastest way to introduce an error is to "fix" a flat passage by adding confident-sounding detail that the AI inferred but the source does not support.

### 2. Identify the AI tells in the draft

Run the draft against the AI-tell checklist (see `scientific-voice-style/SKILL.md` for the canonical list and a regex scanner). Mark every match. Categorise each mark as *rewrite*, *restructure*, or *delete*. Do not rewrite yet.

The most common tells in 2024-2026 LLM output:

- **Em-dash overuse** (more than four per 1000 words is suspicious).
- **Three-part lists** ("fast, accurate, and reliable"; "robust, scalable, and interpretable"). The triad is the single most common AI rhythm.
- **Travel metaphors** ("delve into", "dive into", "navigate the complexities", "explore the landscape", "unpack").
- **Hedging that is true but empty** ("It is important to note that...", "It is worth mentioning that...").
- **Generic intensifiers** ("crucially", "importantly", "key", "essential").
- **Polite filler** ("I hope this is helpful", "let me know if you have questions", "I will now discuss...").
- **False balance** ("on the one hand... on the other hand...") used where the evidence does not support it.
- **Summary openers** ("In this study, we have shown that...") used to launch a summary paragraph.
- **Bolded conclusions** that restate the previous sentence.
- **Vague attribution** ("studies have shown that...") without a citation, or with a hallucinated citation.
- **Lengthy restatement of the prompt** at the top of a section ("The user asked me to discuss X. In this section, we will...").
- **Padded transitions** ("With this in mind, it becomes clear that...", "Having established X, we now turn to Y...").

### 3. For each marked passage, decide: keep, rewrite, or delete

The default is not "rewrite everything." The fastest and safest humanizing pass is often a *targeted* edit.

- **Keep** if the passage is technically correct, well-structured, and the AI tell is cosmetic (e.g. one em-dash). Move on.
- **Rewrite** if the passage is technically correct but flat. Rewrite from your own understanding; do not paraphrase the AI text. If you cannot rewrite it from understanding, leave a comment and revisit later.
- **Delete** if the passage is a polite filler, a vague attribution, or a restated prompt. None of these are doing work. Cut them and check whether the surrounding text still makes sense.

### 4. Rewrite using the playbook, not the thesaurus

For each rewrite, use one of these moves. Do not stack them — pick the one that fits.

- **Replace the metaphor with a literal claim.** "Delve into the complexities of" -> "examine" or, better, a specific verb that names the action. "We tested whether X mediates the relationship between Y and Z" is shorter and clearer than "We delved into the question of whether X mediates the complex relationship between Y and Z."
- **Trade the triad for a list of unequal weight.** "Fast, accurate, and reliable" -> name the dominant property and the trade-off. "Fast at the cost of some accuracy" or "accurate within ~5% but slow on long sequences." Triads imply symmetry; science rarely is symmetrical.
- **Cut the empty hedge.** "It is important to note that the sample size was small" -> "The sample size was small." The hedge was redundant; the claim is the same.
- **Replace vague attribution with a citation or a name.** "Studies have shown that..." -> "Smith et al. showed that..." or, if the claim is generic textbook knowledge, "It is well established that...". Vague attribution is the closest an LLM gets to a hallucination in academic prose and is the most damaging.
- **Move the stress.** A sentence whose stress word is "however" or "therefore" or "this" is structurally weak. Move the new information to the end. "We measured gene expression, however, in three tissues" -> "We measured gene expression in three tissues." (Now the stress is on the tissues.)
- **Add the specific detail the AI could not infer.** A sentence like "The model performed well on a variety of benchmarks" is AI-flavored *because* it is generic. "The model reached a top-1 accuracy of 67% on ImageNet, comparable to the 2024 state of the art within 3 points" is harder to write and harder to fake.

### 5. Vary sentence rhythm deliberately

AI prose is metronomic. The fastest single fix: count the words in your last ten sentences. If the standard deviation is low, vary the length deliberately.

- A long sentence followed by a short sentence is a breath mark. Use it where a point lands.
- Three sentences of similar length in a row is a tell. Break the run.
- A single-word sentence ("Surprising.") or a two-word sentence ("It was not.") is a strong voice move and is hard for an LLM to produce.

### 6. Run the Gopen-Swan structural pass last

Voice work is not a substitute for reader-experience work. After you have rewritten the AI-flavored passages, do a final pass on sentence-level structure. Each sentence should have one unit of thought, and that unit should land in the position of greatest stress (usually the end). Read each sentence aloud; if the stress word is a connective, restructure.

This is the same pass described in `scientific-voice-style`; do it after the voice work, not before.

### 7. Audit for the integrity boundary

Before considering the humanizing pass complete, audit the changes against the rule "humanizing must not change the meaning." Specifically:

- Did any rewrite add a claim the source does not support? Revert or cite.
- Did any rewrite remove a caveat the source includes? Restore it.
- Did any rewrite introduce false confidence? Hedge it back.
- Did any rewrite change a number, a unit, a name, or a citation? Verify against the source.
- Did any rewrite swap a specific term for a more general one? That is a meaning change, not a voice change. Revert.

### 8. Disclose, if the venue requires

Humanizing does not change the disclosure requirement. If AI assistance was used at any stage, the manuscript should disclose it (see `ai-disclosure-statement`). Humanizing for voice and disclosing honestly are not in tension; both are parts of the same integrity posture.

## Code patterns

### AI-tell -> rewrite playbook (compact table)

| Tell | Don't do this | Do this |
| --- | --- | --- |
| Em-dash overuse | "We tested X — a key factor — and found..." | "We tested X, a key factor, and found..." (or restructure so the parenthetical is gone) |
| Triadic construction | "fast, accurate, and reliable" | Name the dominant property; describe the trade-off |
| Travel metaphor | "delve into" | "examine" / "test" / "measure" |
| Empty hedge | "It is important to note that..." | Cut; or replace with the claim itself |
| Generic intensifier | "crucially", "importantly" | Cut; or replace with the reason it matters |
| Polite filler | "I hope this is helpful" | Cut |
| Vague attribution | "Studies have shown that..." | Cite; or delete if the claim is filler |
| Bolded conclusion | "**This matters because...**" | Cut the bold; cut the sentence if it restates the previous one |
| Summary opener | "In this study, we have shown that..." | Cut or replace with the actual result |
| Padded transition | "Having established X, we now turn to Y" | Just turn to Y |

### Sentence-rhythm diagnostic (Python)

```python
# Apply the length-variance diagnostic to a passage.
# CV < 0.35 across ten consecutive sentences is metronomic.

import re

def sentence_lengths(text: str) -> list[int]:
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    return [len(s.split()) for s in sents if s]

def length_variance_report(text: str, window: int = 10) -> None:
    lens = sentence_lengths(text)
    for i in range(0, len(lens), window):
        chunk = lens[i:i+window]
        if len(chunk) < 3:
            continue
        mean = sum(chunk) / len(chunk)
        var = sum((x - mean) ** 2 for x in chunk) / len(chunk)
        sd = var ** 0.5
        cv = sd / mean if mean else 0
        flag = "  <-- metronomic" if cv < 0.35 else ""
        print(f"sents {i:>3}-{i+len(chunk):<3}  mean={mean:>4.1f}  sd={sd:>4.1f}  cv={cv:.2f}{flag}")
```

### Paraphrase-tool failure mode (structural)

A note for anyone considering paraphrase tools (QuillBot, Grammarly's "humanize" feature, commercial "humanizer" services, or any tool that rephrases text without changing its claim content):

- These tools operate at the lexical and syntactic level — they swap words and reorder clauses.
- Current AI detectors and trained readers do not only look at the surface; they look at *discourse-level* patterns (paragraph-level parallelism, abstract-then-exemplify structure, the way claims are sequenced, the way hedges are deployed).
- A surface paraphrase of a paragraph that was *structured* by an LLM often retains enough discourse-level structure to be flagged.
- Worse: paraphrase tools can introduce meaning changes. A claim like "this is a limitation" can become "this is a minor issue" in a paraphrase; that is a fabrication of confidence.
- The right response to a flat AI draft is *not* to paraphrase it; it is to rewrite it from your understanding, with the source material in front of you.

## Common pitfalls

- **Synonym substitution as the main move.** This is detectable, often introduces meaning changes, and produces prose that is worse than the AI draft.
- **Removing caveats to make the prose sound more confident.** A caveat is a claim. Removing it changes the meaning.
- **Adding specific-looking details that you cannot verify.** "Crucially" + a specific number with no citation is a fabrication pattern.
- **Humanizing only the introduction.** Reviewers read the whole paper. The methods and discussion deserve the same pass.
- **Skipping the read-aloud.** Voice is partly sound. You cannot find metronomic prose by reading silently.
- **Treating humanizing as evasion.** If the goal is to make the prose look human, you are doing it wrong. The goal is to make the prose *be* yours.
- **Letting the model do the humanizing.** A model rewriting its own draft into a "more human" register is the most circular version of this skill. The voice has to come from you.
- **Confusing the integrity boundary with the voice boundary.** Voice work is about *how* you say what the source says. Integrity work is about *what* the source says. Keep them separate.
- **Believing a single pass is enough.** The first humanizing pass usually fixes the obvious tells. A second pass, after a night's rest, fixes the subtler ones. A third pass, ideally to a colleague, fixes the ones you cannot see.
- **Underestimating discipline-specific cadence.** A humanized sentence in the wrong subfield is still a tell. The cadence of clinical pharmacology is not the cadence of single-cell genomics.

## Validation

You know the humanizing pass worked when:

- A trusted colleague can identify a passage as yours without being told.
- A reviewer comment engages the *argument* rather than the *prose*.
- The AI-tell scanner flags few matches.
- The manuscript's voice survives a one-night delay and a cold re-read.
- The integrity audit (Section 7 above) passes — no claims added, no caveats removed, no numbers changed.
- The disclosure statement still matches the manuscript (and the venue's policy).

You know the pass is failing when:

- You find yourself reaching for the thesaurus.
- You cannot tell which paragraph in your manuscript you wrote.
- A reviewer comment on the prose is positive in a way that hedges the content ("nicely written, but...").
- The rewrite is shorter than the original in a way that loses caveats.
- A specific number, citation, or name changed in the rewrite and you did not catch it.

## Open alternatives

- For read-aloud review: text-to-speech (system voices on macOS / Linux / Windows, or the open `piper-tts`) lets you hear your own prose without the self-consciousness of reading aloud.
- For AI-tell scanning: the regex scanner in `scientific-voice-style/SKILL.md` is a simple open approach. There is no canonical open-source "humanizer"; commercial services in this space have not been independently validated and should not be relied on for integrity-relevant work.
- For sentence-rhythm diagnostics: the code pattern above is a starting point; more sophisticated analyses (e.g. n-gram entropy, sentence-initial word distribution) are research-grade and not necessary for a single manuscript.

## References

- Pinker, S.. *The Sense of Style: The Thinking Person's Guide to Writing in the 21st Century.* Viking.
- Sword, H.. *Stylish Academic Writing.* Harvard University Press.
- Gopen, G. D., & Swan, J. A.. "The Science of Scientific Writing." *American Scientist*, 78(6), 550-558.
- Williams, J. M.. *Style: Lessons in Clarity and Grace* (11th ed.). Pearson.
- Related `ors-*` skills: `ors-humanizer-skills-scientific-voice-style`, `ors-humanizer-skills-ai-detection-awareness`, `ors-humanizer-skills-ai-disclosure-statement`, `ors-scientific-writing-manuscript-structure`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Sources: Pinker 2014, Sword 2012, Gopen & Swan 1990. Added: AI-tell -> rewrite playbook, sentence-rhythm diagnostic, paraphrase-tool failure mode explained structurally, integrity-boundary audit step.