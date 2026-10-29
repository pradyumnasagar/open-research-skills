---
name: thesis-defense-viva
description: "Use when preparing for the viva voce / oral thesis defense — building the examiner's question set, rehearsing the presentation, and the pre-defense polish (slides, summary, the 'what if I'm stuck' responses) for a life-science or bioinformatics PhD."
license: MIT
---
<!-- metadata:
  category: thesis-writing
  oversight: medium
  version: 1.0.0
  author: Pradyumna Jayaram
  tags: [thesis-writing, viva, defense, presentation]
  difficulty: intermediate
-->

# Thesis Defense & Viva Voce (Life Sciences / Bioinformatics)

The viva is not a fact recitation; it is an examiner's structured interview
about **whether the work is yours, whether it is sound, and whether you know
its edges.** Preparation is question-driven: you rehearse the specific probes
an examiner will actually ask, not a generic "good luck." This skill builds the
question set from your own thesis, scripts the presentation, and defines how to
answer when you are genuinely stuck.

## Hard rules

1. **No fabricated citations.** Anything you cite under questioning (a prior
   result, a protocol, a benchmark) must resolve to a record you can defend.
   Do not bluff a reference number; an examiner will catch a wrong citation
   faster than any other slip, and it reads as integrity, not memory.
2. **No claim without provenance.** If you assert a number or a conclusion in
   the defense, be able to point to the figure/table/page that supports it.
   "The result is in Table 4.2" is the habit to train; "I think it was about
   30%" is the habit that sinks you.
3. **No silent failure.** If a probe touches a method or a control you have not
   fully run, do not gloss over it. Name the gap and its status ("I have not
   run X; here is what I would do and what I expect") — an admitted, bounded
   gap is scored far better than a confident dodge.
4. **Answer the question asked, not the one you wanted.** A 30-second direct
   answer, then elaboration only if invited. Rummaging through the thesis while
   you think is the single most common live mistake.

## When to use

- Rehearsing the oral defense / viva voce.
- Building the examiner question set a week or two before the defense.
- A final "what will I be probed on?" walk-through of your own chapters.

## When NOT to use

- Fixing the underlying reproducibility gaps the exam would expose — that is
  `thesis-methods-reproducibility`, run it first.
- The written thesis itself — `thesis-structure`.
- Rehearsing a *conference* talk or a *grant* talk (different stakes, different
  length) — use `comm-conference-talk` or `grant-proposal-craft`; a defense is
  10–20 min of talk + 1–3 h of questioning.

## Prerequisites

- The thesis draft is essentially frozen — you can answer "what's on page N?"
  quickly because you know your own document.
- Your supervisor or a mock examiner to run at least one full dry run.

## Build the question set from your thesis

Generate the probes your *own* document invites, in the examiner's order of
attack. This is the highest-leverage prep: it is the exact list they will
walk.

1. **The framing questions** (first, to place you):
   - What is the one contribution, in a sentence?
   - Why does this matter, and why was it hard before your work?
   - What did *you* do versus the group / the tool / the collaborators?
2. **The soundness questions** (the core):
   - For each major result: what was the control, and why does it support the
     claim?
   - What alternative explanation did you rule out, and how?
   - What is the weakest assumption in your method, and what would break it?
3. **The edge-of-work questions** (the stress test):
   - What if the sample size / the cutoff / the normalization were different?
   - Where does your result *not* hold? (Examiners reward a stated boundary.)
   - What would you do with 6 more months, and what would you do first?
4. **The provenance questions**:
   - Trace one number in your results to its source file / figure / parameter.
   - If a method "standard protocol" was used, name the version and the
     parameter.

Rehearse each until the direct answer is under 30 seconds; only then add depth.

## The presentation (10–20 min)

- It is the **thesis-scale** summary, not a chapter read: contribution → the
  one experiment / result that carries it → the boundary. Mirror `thesis-structure`
  in miniature.
- Slides are the visual aid, not the script: figure-forward, minimal text, every
  panel labeled. The defense slides are a *separate* deck from the written
  thesis figure set.
- Open with the contribution, not the background — the examiner knows the
  background; they need your result and your claim.

## When you are genuinely stuck

- **Don't bluff.** "I'm not certain; here is how I would find out" is the
  correct move and is scored above a confident wrong answer.
- **Buy time, don't freeze.** Repeat the question in your own words to confirm
  it; a 5-second rephrase is normal and reads as engagement, not delay.
- **Scope the answer.** If the question is broader than you can answer, answer
  the part you can and name the part you can't: "On X, my data says …; the
  Y aspect I did not measure."

## Pitfalls

- **Rummaging through the thesis** while composing an answer — pre-locate your
  key figures; know where every number lives.
- **Answering the question you hoped they'd ask** instead of the one they
  asked.
- **Bluffing a citation or a version** — caught fast, and it reads as an
  integrity problem, not a memory slip.
- **No stated boundary** — "my method is robust" with no "except when …" is
  the tell of someone who has not stress-tested their own work.
- **Treating the examiner as hostile** — they are checking your grasp; the
  tone you keep is part of the score.
- **Forgetting the "what would you do differently" question** — the classic
  final, and one you can prepare a clean, specific answer for.

## Validation

- A full mock defense run (at least one), with the question set answered cold
  for the framing and soundness categories.
- Every major result has a rehearsed control-justification in under 30 seconds.
- One live trace from a results number to its source figure/file, done aloud.
- A written "stuck" script: for each known-weak area, the bounded-answer line
  you will actually say.

## References

- `thesis-structure` — the miniature the defense slides must mirror.
- `thesis-methods-reproducibility` — the provenance habits behind every answer.
- Program-specific viva format (panel size, allowed items, time) lives in your
  department's PhD regulations — the authoritative local source.

## Cross-references

- thesis-structure — the architecture you present and defend.
- thesis-methods-reproducibility — the provenance discipline the exam probes.
- manuscript-structure — for polishing the defense's one-page contribution
  statement into words an examiner will reuse.

(Run the `meta/integrity-audit` skill on the final slides + question-set answers
before the defense. Content skills in this repo do not cross-reference `meta/`
slugs as bullets, so it is referenced in prose here.)

## Changelog

- **1.0.0** (2026-06-18) — Initial release. A question-set builder keyed to
  your own chapters, a 10–20 min presentation script, the "when you're stuck"
  responses, and the rehearsal validation, tuned for life-science /
  bioinformatics defenses.
