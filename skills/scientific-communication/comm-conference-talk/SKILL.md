---

name: comm-conference-talk
description: "Designs, scripts, and rehearses a 10-20 minute scientific conference talk (job talk, contributed talk, plenary, lightning) for a technical but non-specialist audience. Enforces a single-take-home-message structure (motivation-gap-evidence-claim-implication), prescribes slide-budget allocation by time, and codifies the Loui & Smith audience-engagement rubric. Use when preparing a contributed conference talk, defending a thesis chapter, writing a job-talk job talk, or rewriting a sprawling results-heavy talk into a 12-minute contribution."
license: MIT
---




<!-- metadata:
category: scientific-communication
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - scientific-communication
  - research
difficulty: intermediate
-->

## Version Compatibility

Reference framework authored 2026-06 from a synthesis of public sources. No code dependencies. Update when:
- The conference introduces a new talk format (e.g., 3-minute thesis) and the time budget changes
- The audience profile shifts (e.g., from specialists to generalist sessions) and the framing changes
- A peer-reviewed update to the Loui & Smith rubric (or its successor) is published

If audience-size, time, or venue constraints differ from the defaults below, scale slide count and rehearsal cadence linearly; do not change the message hierarchy.

# Conference Talk

A conference talk is not a paper read aloud. It is a single take-home message, carried on a structure your audience can follow without reading the slide, and delivered at a pace that gives them time to think. The default failure mode of a research talk is the speaker trying to transmit every result; the actual job is to transmit one message and let the audience remember one sentence when they leave the room.

This skill encodes the structural and rhetorical choices that distinguish a talk the audience remembers from a talk the audience sits through. The default is a 12-minute contributed talk; the same framework extends to 5-minute lightning and 45-minute job talks by scaling time and slide count, not structure.

## The Take-Home Message Test

Before writing a single slide, write the take-home message in a single sentence a non-specialist could repeat to a colleague. Test it against three rules:

1. **It is a claim, not a topic.** "We studied mRNA methylation in glioblastoma" is a topic. "N6-methyladenosine on MYC mRNA drives treatment resistance in glioblastoma, and targeting the methyltransferase reverses it in xenografts" is a claim.
2. **It has a verb that asserts.** "Show," "demonstrate," "cause," "predict," "explain" — never "discuss," "explore," or "look at."
3. **It can be falsified.** If a reviewer could read the paper and disagree with the message, the message is sharp enough to defend.

If the take-home message fails any test, the talk will be a tour of figures. The talk is the argument that the message is true.

## The Five-Act Structure

Loui & Smith's audience-engagement work, building on classical rhetoric, identifies five rhetorical moves the audience must register for a talk to land. Gopen & Swan's reader-expectation principles apply these moves to the spoken register: stress positions in sentences (the ends) and visual positions on slides (top, bottom-left, and bottom-right of the visual field) carry the meaning; the speaker's job is to design both.

| Act | Function | Default time | Default slide count (12-min) | Fails when |
|-----|----------|--------------|------------------------------|------------|
| 1. Motivation | Why this matters now | 1.5 min | 1-2 | Jargon-only framing; audience can't answer "why should I care?" |
| 2. Gap | What is unknown | 1 min | 1 | The work looks like an incremental replication of a known result |
| 3. Evidence | The data, in one or two figures | 6 min | 4-5 | Slides reproduce the paper figure-by-figure; no zoom into the deciding experiment |
| 4. Claim | Restate the take-home message | 1.5 min | 1 | Audience cannot summarize the talk in one sentence |
| 5. Implication | What this changes for the field | 2 min | 1-2 | Talk ends on "future work" without a defensible implication |

Acts 3 and 4 together carry the load. If the talk is short on time, cut from Acts 1, 2, and 5 — never from 4. The take-home message is the contract with the audience; if you cannot deliver it, you have not given a talk.

## Slide Budget Per Act

For a 12-minute talk, the speaker's pace should be approximately 90 seconds per slide for setup slides and 2-3 minutes per slide for figure slides. The following budget is the working default; adjust ±1 slide for audience familiarity.

| Act | Slide budget | Slide kind |
|-----|--------------|------------|
| 1. Motivation | 1-2 | Title + one setup figure or schematic |
| 2. Gap | 1 | A single contrast slide: "known / unknown" |
| 3. Evidence | 4-5 | Two zoom-in figures, two summary figures, one methods-in-one-slide |
| 4. Claim | 1 | A one-line slide restating the take-home message |
| 5. Implication + acknowledgments | 1-2 | Implication + acknowledgments + contact |

Total: 9-12 slides for 12 minutes. The temptation to bring 30 slides is the temptation to confuse coverage with communication; resist it. A talk that covers 30 figures covers none of them.

## The Loui & Smith Audience-Engagement Rubric

Loui & Smith (peer-reviewed paper on scientific talks) operationalize audience engagement into seven measurable behaviors. A talk should be rehearsed against this rubric; a talk should not be given that fails more than two of the seven.

1. **Eye contact with the audience, not the screen.** Glance at the slide only when pointing to a specific feature; otherwise address the back of the room.
2. **Naming the audience's next question.** After each figure, state the question the figure answers before showing it. "You may be asking whether this is a confound of batch — the next figure shows the batch-corrected effect is preserved."
3. **Signposting transitions.** At every act boundary, name the move: "That was motivation. Now the gap." Audiences do not penalize signposts; they penalize the loss of thread.
4. **One idea per slide.** If a slide has three ideas, it has zero ideas. Split it.
5. **Reading the figure, not the table.** If the deciding data is a table, convert it to a figure for the talk. Audiences do not read tables in real time.
6. **Restating the claim at the midpoint.** At the halfway mark, repeat the take-home message once. Audiences forget by minute six what they heard at minute one.
7. **Ending on the implication, not "thank you."** "Thank you" is the last slide, not the message. The message slide comes first in the closing sequence.

## The Deciding-Experiment Test

For each result slide in Act 3, ask: if a hostile reviewer could attack only this figure, would the figure survive? The slide that survives that attack is the deciding experiment of the talk. The deciding experiment gets 60-90 seconds of verbal time. Adjacent supporting figures get 20-30 seconds each. Everything else goes to the supplement or the poster.

A common failure: the speaker presents a screening result, a validation result, a mechanism result, a phenotype result, and a rescue — and gives each one 60 seconds. The audience cannot weight them, so they weight none. Pick the one figure that, if it failed, the paper fails. That figure is the spine of the talk.

## Gopen & Swan Applied to Spoken Prose

Gopen & Swan's "Science of Scientific Writing" argues that readers process prose by structural position, not linearly. The same is true of listeners, but more strongly: a listener cannot reread. Apply seven of their principles to the spoken register.

1. **Put the subject at the start of the sentence.** "The methyltransferase catalyzes the modification" beats "The modification is catalyzed by the methyltransferase."
2. **Put the verb early.** Subject-verb-object before any subordinate clause.
3. **End sentences on the new information.** The end of the sentence is the listener's stress position. "Treatment resistance is reversed by targeting the methyltransferase" — "methyltransferase" is the new information and belongs at the end.
4. **One idea per sentence.** Two-clause sentences that try to relate two ideas lose half the audience.
5. **Use topic sentences in transitions.** "Three lines of evidence support this. First, ..."
6. **Mark the stress position with a pause.** A 1-second pause before the stressed word is the spoken equivalent of italics.
7. **Avoid nominalizations.** "We performed an investigation of" → "We investigated."

These are defaults, not absolutes. The principle is that the listener's working memory is the bottleneck; the speaker's job is to manage the bottleneck.

## Slide Design Rules

The default failure mode of a scientific slide is to reproduce a paper figure with a 12-point caption in 8-point font. The audience cannot read it; the speaker cannot see it; the projector washes out the contrast. Apply the following rules.

1. **One figure, one slide.** No side-by-side comparisons unless the side-by-side is the point.
2. **Font size ≥ 24 pt** for body, ≥ 32 pt for labels, ≥ 40 pt for the title. Test by rendering at 1024x768 — if you cannot read it from 3 m, neither can the back of the room.
3. **Title is a sentence, not a label.** "Figure 3A" is a label. "Methylation of MYC mRNA increases under therapy" is a sentence. The audience should be able to read the title and learn the result without seeing the figure.
4. **No full sentences in the body.** Phrases only. The speaker says the sentences; the slide shows the structure.
5. **Color for meaning, not decoration.** Use a single accent color for the result of interest. Everything else is grayscale.
6. **Animation only for sequence.** Build a figure in two or three steps to control attention. Animation for decoration is a tax on the audience's working memory.
7. **Cite the figure number in the corner** for figures that will be discussed in Q&A. "Fig 3A" in 12 pt is enough.

## Rehearsal Cadence

A talk that has not been rehearsed out loud is not a talk; it is a slide deck. Rehearse in three passes.

**Pass 1: Alone, with a timer.** Run the talk in real time. If you run over by more than 10%, cut. If you run under by more than 20%, add. Aim for ±30 seconds of the time limit.

**Pass 2: With one labmate, recorded.** Record the talk. Watch the recording at 1.5x speed, the way the audience will mentally skim if bored. Note the moments you sped up (boredom) and the moments you slowed down (over-explanation). Cut the over-explanations; the bored audience is the right audience.

**Pass 3: With a non-specialist.** A friend from another field, an undergraduate, a relative. If they can repeat the take-home message in one sentence after a 5-minute talk, the talk is sharp. If they cannot, the message is buried.

A job talk rehearsed in this cadence takes three full days from first draft to delivery. A 12-minute contributed talk takes one full day. A 5-minute lightning talk takes half a day. Budget the rehearsal time at 4x the talk length.

## Q&A Preparation

Q&A is the second half of the talk. The audience will ask three kinds of questions; prepare for each.

1. **The comprehension question.** "Did you control for X?" The audience is trying to confirm a detail. Answer in one sentence, then offer to discuss offline.
2. **The attack question.** "How do you know this isn't just Y?" The audience is testing the deciding experiment. Your answer is the one sentence that defends the deciding experiment; prepare it in advance.
3. **The connection question.** "Have you thought about Z?" The audience is offering a collaboration. Acknowledge, point to the implication slide, and end the answer in 30 seconds.

The three worst Q&A answers are: (a) restating the question, (b) saying "that's a good question" before answering, (c) defending the work by attacking the questioner. The three best Q&A answers are: (a) one sentence that says yes/no, (b) one sentence that says what the result is, (c) one sentence that says what it would take to change your mind.

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| Paper-as-talk | 30+ slides reproducing the paper | Cut to 10-12 slides; pick the deciding experiment |
| Methods-heavy Act 1 | Talk opens on "we used scRNA-seq" | Open on the gap or the claim, not the technique |
| Figure-less claim | Talk asserts results without showing them | One figure per major claim; no exceptions |
| Citation dump | Slide 1 lists 12 prior papers | Cite one or two pivotal papers; full citation in the paper |
| Reading the slide | Speaker reads bullet points aloud | Bullet points are speaker prompts, not audience content |
| Defensive Q&A | Speaker says "we haven't done that yet" before answering | Lead with the answer; the limitation is one sentence later |
| Soft ending | "Thank you for your time" | End on the implication slide; the thank-you is the last slide |

## Plain-Language Discipline

NIH Plain Language guidelines apply to spoken science: the audience's comprehension is the speaker's responsibility. Two specific rules.

1. **Define a jargon term once, then use the plain version.** "Persistent RNA/DNA hybrids (R-loops) — from here on, R-loops." Do not alternate between technical and plain.
2. **Quantify before generalizing.** "About 30% of cases" beats "many cases" beats "a substantial fraction." Numbers anchor abstract claims.

The Alda Center adds a third rule: avoid the imperative of expertise. "We can see that..." is a hedge that signals the speaker is uncertain. State the result: "The effect size is 1.7-fold; the 95% CI excludes 1."

## A 12-Minute Worked Example

For a 12-minute talk on "N6-methyladenosine modification of MYC mRNA drives temozolomide resistance in glioblastoma":

- **Slide 1 (0:00-0:30):** Title, authors, one-sentence take-home: "METTL3-mediated m6A modification of MYC mRNA drives temozolomide resistance, and pharmacological METTL3 inhibition restores sensitivity in xenograft models."
- **Slide 2 (0:30-2:00):** Motivation. Glioblastoma has 15-month median survival despite temozolomide; resistance is the clinical bottleneck.
- **Slide 3 (2:00-3:00):** Gap. The mechanism of acquired resistance is unknown. Two competing hypotheses: drug efflux vs. epigenetic adaptation.
- **Slide 4 (3:00-4:30):** Evidence 1. Patient-derived xenografts that relapse show elevated MYC mRNA and elevated m6A.
- **Slide 5 (4:30-6:30):** Evidence 2 (the deciding experiment). METTL3 knockdown in resistant lines restores sensitivity; METTL3 overexpression in sensitive lines induces resistance. This is the only slide that gets 90 seconds.
- **Slide 6 (6:30-8:00):** Evidence 3. m6A-sequencing shows the modification site on MYC codon 235; mutation of the site abolishes the effect.
- **Slide 7 (8:00-9:00):** Evidence 4. A small-molecule METTL3 inhibitor (STM2457) restores temozolomide sensitivity in vivo.
- **Slide 8 (9:00-9:30):** Methods-in-one-slide. One figure or one sentence; not a workflow diagram.
- **Slide 9 (9:30-10:30):** Claim slide. Restate the take-home message. Repeat it.
- **Slide 10 (10:30-11:30):** Implication. METTL3 inhibition is a candidate combination strategy for temozolomide-resistant GBM.
- **Slide 11 (11:30-12:00):** Acknowledgments + contact. One slide; do not read names aloud.

This 11-slide, 12-minute structure is the working template. Adapt the slide count to the time; do not adapt the structure.

## References

- Loui & Smith, "Talk to the audience" — peer-reviewed paper on scientific talks, engagement rubric.
- Gopen & Swan, "The Science of Scientific Writing" — structure of scientific prose, applied here to spoken register.
- Nature Masterclasses: Scientific Presentation — slide design, audience analysis.
- AAAS Communication Toolkit — talk preparation worksheet, audience profiles.
- Alda Center for Communicating Science — improvisation, clarity, and avoiding the imperative of expertise.
- NIH Plain Language guidelines — jargon discipline, quantification.
- Anderson, *The Way We're Working Isn't Working* — TED talk principles applied to science: the talk as a one-idea transmission.

## Related Skills

- scientific-communication/poster — companion format for the deciding experiment and the supporting figures.
- scientific-communication/elevator-pitch — distilled version of the take-home message for hallway conversation.
- scientific-communication/press-release — the take-home message recast for a general audience.
- scientific-communication/podcast — long-form spoken version of the same take-home message.