---
name: ors-scientific-visualization-slides-design
display_name: "Scientific Slide Design"
description: "Design scientific conference and lecture slides. Covers the 6x6 rule, results-first structure, the 5-second test, build progression, citation format, dark-mode contrast, and accessibility."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: scientific-visualization
tags: [slides, presentation, keynote, powerpoint, beamer, revealjs, marp, quarto, dark-mode, accessibility]
difficulty: intermediate
prerequisites:
  tools: [powerpoint or keynote or google-slides, latex-beamer (optional), marp-cli (optional), quarto (optional), reveal.js (optional)]
  skills: [ors-scientific-visualization-figure-design, ors-scientific-visualization-schematics-diagrams, ors-scientific-visualization-color-and-accessibility]
sources_consulted:
  - "Original: scientific-slides (scientific-agent-skills, K-Dense Inc.); Adapted: removed demo deck scripts, restructured around the 6x6 / 5-second-test / results-first triad, added Beamer and Marp/Quarto code patterns"
  - "Improvisions: added dark-mode guidance for projector venues, citation-on-slide conventions, animation-restrained build patterns, and an accessibility checklist for screen-readers"
last_updated: 2026-06-10
---

# Scientific Slide Design

> This skill turns a research story into a deck that an audience can read in real time. The goal is comprehension at speaking pace: every slide communicates one idea in the time it takes to say one sentence. It complements `ors-scientific-visualization-figure-design` (data plots for the slides) and `ors-scientific-visualization-schematics-diagrams` (workflow / study-design cartoons).

## When to use

Trigger this skill when any of the following apply:

- You are preparing a conference talk, departmental seminar, journal club, or thesis defense.
- You are pitching a grant or paper to a non-specialist audience.
- You are recording an asynchronous talk for a webinar, MOOC, or YouTube.
- A co-author or mentor has flagged a slide as "too busy" or "I couldn't read the bottom row".
- You are converting a paper into a 10–15 minute talk.

## When NOT to use

- Posters — see `ors-scientific-visualization-poster-design`.
- Print figures for a paper — see `ors-scientific-visualization-figure-design`.
- Schematics, workflows, study design — see `ors-scientific-visualization-schematics-diagrams`.
- Slide-decks that are pure text (manuscript, README) — use `ors-scientific-writing` instead.

## Prerequisites

- A defined audience and venue (specialist conference? departmental seminar? high-school outreach?). This decides depth, jargon, and visual style.
- A target talk length in minutes, and a rule of thumb: ~1 slide per minute for a fast conference talk, 1 slide per 2 minutes for a lecture.
- A list of 3–5 main messages. The whole deck exists to deliver these.
- The figures from the paper (PDF, PNG) or the data and code to regenerate them.
- A backup plan: a printed handout, a PDF copy on a USB stick, and a version that does not depend on network access at the venue.

## Core workflow

1. **Anchor on the one-sentence takeaway.** Write the conclusion the audience should walk out remembering. The whole deck argues for that sentence.
2. **Results-first structure.** Use a problem → approach → key result → implication arc, not a chronological "we did X, then Y". Most slides should be results; the introduction and methods should be short.
3. **Apply the 6×6 rule.** No more than 6 lines per slide, no more than 6 words per line. If a slide is busier than this, split it.
4. **Apply the 5-second test.** Show a slide to a colleague for 5 seconds, then hide it. If they cannot state the main idea, simplify or rewrite the headline.
5. **Use one main idea per slide.** A slide is a single claim, supported by one figure, one table, or one bulleted list. Two claims = two slides.
6. **Use the headline-as-conclusion pattern.** Replace "Methods" with "Single-cell RNA-seq of 50,000 cells across 12 patients". The slide title is the message, not the topic.
7. **Build progression for complex figures.** Use 2–4 sequential reveals (one panel at a time, one arrow at a time). The audience reads at the pace you build, not all at once.
8. **Restrain animation.** Use animation for build progression only. No spinning logos, no fly-ins, no random slide transitions. Build once, then leave the final state on screen while you speak.
9. **Cite on the slide, not just at the end.** A small citation footer (`Smith et al., Nature 2024`) lets the audience follow up without breaking the talk.
10. **Audit for the venue.** Projector contrast, color profile, and aspect ratio differ by room. Test the deck on the actual projector or a similar one the day before.

## Code patterns

### A. Tool selection matrix

| Need | Recommended tool | Why |
|---|---|---|
| Collaborative editing, easy review | **Google Slides** | Multi-author, comment threads, version history, no install |
| Mac-only, polished typography | **Keynote** | Best default fonts and motion presets; export to PowerPoint or PDF |
| Windows-dominant institution, advanced builds | **PowerPoint** | Universal, Morph transition for clean reveals, good presenter view |
| LaTeX-native, equations, citations | **Beamer** (`latex-beamer`) | Reproducible, journal-style, version-controllable, excellent math |
| Markdown to slides, code-heavy | **Marp** | Write slides in Markdown, export to HTML/PDF, version-controllable |
| Reproducible reports with embedded slides | **Quarto** (`revealjs` format) | Markdown + code chunks + citations in one pipeline |
| Web-deployed, math, code, audio/video | **reveal.js** | Full HTML/CSS/JS control; great for recorded talks |
| Long-form lecture with notes | **org-reveal** (Emacs) or **Jupyter Slides** | Code + prose + slides from one source |

### B. Beamer — minimal conference talk skeleton

```latex
\documentclass[10pt,aspectratio=169]{beamer}
\usetheme{metropolis}              % clean, modern, sans-serif
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}

\title{One-Sentence Takeaway}
\author{Pradyumna Jayaram}
\institute{Institution}
\date{Conference Name, 2026}

\begin{document}
\maketitle

\section{Introduction}
\begin{frame}{The problem}
    % Headline is the message, not the topic
    Single-cell assays are noisy; bulk averages hide the cells that matter.
    \begin{itemize}
        \item ~50{,}000 cells, 12 patients
        \item Goal: find a rare population driving outcome
    \end{itemize}
\end{frame}

\section{Approach}
\begin{frame}{Cohort and assay}
    \begin{columns}
        \begin{column}{0.5\textwidth}
            \begin{itemize}
                \item 10x Genomics 3' v3
                \item 12 patients, 4 conditions
                \item QC with `cellranger` and `scrublet`
            \end{itemize}
        \end{column}
        \begin{column}{0.5\textwidth}
            \includegraphics[width=\textwidth]{workflow.png}
        \end{column}
    \end{columns}
\end{frame}

\section{Results}
\begin{frame}{A rare population predicts outcome}
    \begin{figure}
        \centering
        \includegraphics[width=0.8\textwidth]{umap_rare.pdf}
        \caption{\textbf{Rare cluster (cyan) is 1.2\% of cells} but
                 explains 38\% of outcome variance (OR 4.7, 95\% CI 2.1--10.5).}
    \end{figure}
\end{frame}

\section{Conclusion}
\begin{frame}{Take-home}
    \begin{alertblock}{}
        A rare, transcriptionally distinct cell population
        drives patient outcome and is a candidate therapeutic target.
    \end{alertblock}
    \begin{itemize}
        \item Validation in an independent cohort is ongoing
        \item Code: \texttt{github.com/yourname/project}
    \end{itemize}
\end{frame}

\begin{frame}{References}
    \footnotesize
    \bibliographystyle{plain}
    \bibliography{refs}
\end{frame}
\end{document}
```

Compile with `pdflatex talk.tex` (twice for the table of contents) or `latexmk -pdf talk.tex`.

### C. Marp — Markdown to slides (code-heavy talks)

```markdown
---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section.lead h1 { text-align: center; }
  section { font-size: 26px; }
---

# Single-cell RNA-seq identifies a rare outcome-driving population
### Pradyumna Jayaram — Conference 2026

---

## The problem

Single-cell assays are noisy; bulk averages hide the cells that matter.

- 50,000 cells, 12 patients
- Goal: rare population driving outcome

---

## A rare population predicts outcome

![width:800px](umap_rare.png)

**Rare cluster (cyan, 1.2% of cells) explains 38% of outcome variance** (OR 4.7, 95% CI 2.1–10.5).
```

Render with `marp talk.md --pdf` or `marp talk.md -o talk.html` for a web-friendly version.

### D. Quarto + reveal.js — reproducible report-as-talk

```yaml
---
title: "Single-cell RNA-seq identifies a rare outcome-driving population"
author: "Pradyumna Jayaram"
format:
  revealjs:
    theme: simple
    incremental: true
    slide-number: true
    chalkboard: true
bibliography: refs.bib
jupyter: python3
---
```

```python
# Code chunks render and execute; figures embed directly
import scanpy as sc
adata = sc.read_h5ad("data.h5ad")
sc.tl.umap(adata)
sc.pl.umap(adata, color="leiden", save="umap_leiden.png")
```

```markdown
## Results

![](umap_leiden.png){fig-align="center" width="70%"}

A rare cluster (cyan) explains 38% of outcome variance [@smith2024singlecell].
```

Build with `quarto render talk.qmd` → `talk.html`. The same source can be re-rendered as a PDF, a manuscript, or a poster.

### E. PowerPoint / Keynote — build progression (one panel at a time)

Pseudocode for a 4-panel reveal:

```
Slide "Approach"
  Build 1: panel A (cohort diagram)
  Build 2: + panel B (assay workflow)
  Build 3: + panel C (QC steps)
  Build 4: + panel D (statistical model)
  [leave the final state on screen while you speak]
```

In PowerPoint, set each panel to appear on click via the "Animations" pane; choose "Appear" or "Fade", not "Fly In" or "Spin". In Keynote, use "Build In" with "Fade".

### F. Citation footer (consistent across the deck)

PowerPoint / Keynote: insert a small text box anchored to the bottom-left of the slide master, font 9–10 pt, italic. Content: `Smith et al., Nature 2024` or `\cite{smith2024}` if generated by a Beamer bibliography.

Beamer: add to the footer template with `\setbeamertemplate{footline}{...}`.

Marp / Quarto: define a global footer in the frontmatter.

## The 6×6 rule, in practice

The 6×6 rule (no more than 6 lines, 6 words per line) is a heuristic, not a law. The deeper rule is **readability at glance**:

- Title slide: 1–2 lines of title, 1 line of name, 1 line of affiliation.
- Content slide: 1 title (the message), ≤ 6 bullet lines, ≤ 6 words per line, supporting figure.
- Methods slide: short prose (1–2 sentences) + 1 figure, not both a wall of text and a figure.
- "Q&A" slide: 1 line ("Questions?") + an email and a QR code to the paper.

If a slide needs 8 bullets, split it into 2. If a bullet needs 14 words, cut it.

## Results-first structure (a defensible default)

A common talk template for a 12-minute conference talk:

| Slide | Time | Content |
|---|---|---|
| 1. Title | 0:00 | Title, author, affiliation, one-sentence takeaway |
| 2. Hook | 0:30 | The surprising fact that earns the audience's attention |
| 3. Background | 1:30 | 1–2 slides of context the audience needs to follow |
| 4. Question | 3:00 | "We asked: does X drive Y?" |
| 5. Approach | 4:00 | Cohort, assay, model — schematic, not detail |
| 6. Result 1 | 6:00 | Main figure with the headline conclusion as the title |
| 7. Result 2 | 8:00 | Second key figure, building on Result 1 |
| 8. Result 3 | 9:30 | Third figure or validation |
| 9. Implication | 10:30 | Why this matters, who should care |
| 10. Caveats | 11:00 | One slide of limitations and next steps |
| 11. Take-home | 11:30 | One line the audience should remember |
| 12. Acknowledgments / Q&A | 12:00 | Funding, collaborators, contact |

The exact slide count varies; the ratio does not. ~60% results, ~20% introduction + approach, ~20% conclusion + Q&A.

## Animation: when to use it, when not

- **Use it**: to reveal a multi-panel figure one panel at a time; to underline a key element with an arrow or box; to show progression (year 1 → year 5 of a cohort).
- **Avoid it**: spinning logos, random slide transitions, fly-ins, typewriter text, animated charts, "click here!" pointers, auto-advancing slides, embedded video without a backup screenshot.
- **The "leave it on screen" rule.** After a build sequence, the final state stays on screen while you speak about it. The audience should not have to remember the order of reveals.

## Dark mode for venues

Many conference rooms and lecture halls are dark. Choose slide background based on the venue:

- **Light background, dark text** is the safest default for mixed venues and printed handouts. Use a slight off-white (`#FAFAFA`) instead of pure white to reduce eye strain.
- **Dark background, light text** works for projector-only rooms where the lights are off. Use a near-black (`#1A1A1A`) and an off-white text (`#EAEAEA`) to avoid the glare of pure black/white.
- **Test contrast on the actual projector.** A 4.5:1 contrast ratio on a laptop may look fine but wash out on a projector with a yellow tint. Run the WCAG contrast check at projector gamma, not at laptop gamma.
- **Avoid mid-tones for text.** Mid-gray (`#888888`) text on a gray background is illegible under projector light. Use ≥ 7:1 contrast for body text and ≥ 4.5:1 for fine print.

## Citations on the slide

There is no universal style, but the conventions in major venues:

- **APA / Nature numeric**: small superscript number on the slide, full reference in a final slide or handout (`[1] Smith et al., Nature 2024`).
- **Author-year**: inline `Smith et al. (2024)` in the body of the bullet, full reference list at the end.
- **For data and code**: include the accession or repository on the slide (`GEO: GSE123456`, `github.com/yourname/repo`).
- **Avoid hyperlinks in the slide body.** Hyperlinks look fine on a laptop and become unreadable on a projector. Put the URL in the speaker notes or the handout.

## Accessibility for slides

- **Font size.** Body text ≥ 24 pt for the back row of a typical room; ≥ 28 pt for a large auditorium. Titles ≥ 32 pt.
- **Color + redundancy.** Encode groups by color + shape, never by color alone. Aim for ≥ 4.5:1 contrast (WCAG 2.1 AA) for body text.
- **Alt text.** Add alt text to every figure in the deck (PowerPoint: right-click → "Edit Alt Text"; Keynote: "Format → Advanced → Alternative Text"). The alt text should describe the figure in 1–2 sentences, not just its filename.
- **Reading order.** Use the slide outline, not visual stacking, as the reading order. Screen readers and `pdftotext` extract the outline first.
- **No flashing content.** Avoid strobing or rapid flashing; WCAG 2.1 caps flashing at 3 Hz.
- **Captions on embedded video.** If the talk has a video, caption it. Auto-captions are a starting point, not a final answer.
- **Speaker notes for live captioning.** Many venues run automated captioning. Speaker notes give the captioner context.

## Common pitfalls

- **The "manuscript on a slide" anti-pattern**: copying a figure caption or a paragraph of the paper onto a slide. The slide is a *medium*, not a *copy*; rewrite for spoken pace.
- **Title = topic, not message**: a slide titled "Results" tells the audience nothing. Rename to "A rare population predicts outcome".
- **Too many figures on one slide**: 4 small figures, each illegible. Show one big figure with 2 builds.
- **Body text 14 pt or smaller**: invisible from the back row. The minimum is 24 pt; default to 28.
- **Truncated axis without a break mark**: a bar chart that starts at 30% exaggerates the difference. Mark the break.
- **Inconsistent style across slides**: one slide in Times New Roman, the next in Calibri, the next in Arial. Set a master / theme and use it.
- **Embedded video that does not play in the venue**: a codec the projector laptop lacks, a YouTube link behind a firewall. Always have a still-frame screenshot as a backup.
- **Speaker notes that read the slide**: notes are a script, not a copy. If the slide and the notes say the same thing, the slide is too busy.
- **"Thank you / Questions?" without contact info**: an audience member wants to follow up but has no email. Add the email and a QR code to the paper.

## Validation

- **5-second test**, per slide: a colleague who has never seen the deck should be able to state the main idea of each slide after 5 seconds of viewing.
- **6×6 audit**: open the deck on a single screen and count lines per slide and words per line. Anything over 6/6 needs cutting.
- **Back-row test**: open the deck at the size shown on the projector and read the bottom row of the smallest table from 6 meters away. If you cannot, the text is too small.
- **Greyscale test**: convert the deck to greyscale (PowerPoint: `View → Greyscale`; Keynote: print preview in greyscale) and confirm each slide still tells its story.
- **CVD test**: pass a few representative slides through a CVD simulator. Distinguishability holds.
- **Print test**: print the deck 6-up on letter/A4 and read it. If you cannot, the deck is not speaker-ready.
- **Cold-read rehearsal**: read the speaker notes aloud, slide by slide, at speaking pace, and time it. If the talk runs over by more than 10%, cut.

## Open alternatives

| Commercial / proprietary | Open alternative | Trade-off |
|---|---|---|
| PowerPoint | LibreOffice Impress | Free; opens and saves `.pptx`; some advanced transitions missing |
| Keynote (macOS) | LibreOffice Impress / Beamer | Cross-platform; less polished default typography |
| Google Slides | OnlyOffice / CryptPad presentations | Self-hostable; less polished collaboration UX |
| Beautiful.ai / Pitch | Marp / Quarto / reveal.js | Free, version-controllable, code-driven; less template-driven polish |
| Prezi (zooming canvas) | Beamer with `\\only` overlays / reveal.js fragments | Free; less dramatic, but more accessible to screen readers |
| Adobe Express templates | Inkscape + slide master in Impress | Free; manual layout |
| Mentimeter / Slido | Wooclap / direct QR-to-Google-Form | Free tier; fewer live-response visualizations |
| Slidebean | Marp / Quarto | Free, code-driven; less auto-layout AI |
| Beautiful.ai / Tome (generative) | Hand-author in Marp / Beamer | Reliable, disclosable, accessible; slower |

## References

Internal cross-links to other `ors-*` skills:

- `ors-scientific-visualization-figure-design` — DPI, fonts, and multi-panel layout that the slides will use.
- `ors-scientific-visualization-schematics-diagrams` — workflow and study-design slides.
- `ors-scientific-visualization-color-and-accessibility` — palette choice and contrast audits.
- `ors-scientific-visualization-poster-design` — when the same story is told as a poster instead of a talk.
- `ors-scientific-writing` — caption and headline-as-conclusion phrasing.

External resources (do not fabricate exact paths):

- Beamer user guide (in TeX Live; `texdoc beamer` or `ctan.org/pkg/beamer`)
- Marp documentation and themes — `marpit.org`
- Quarto reveal.js format — `quarto.org/docs/presentations/revealjs`
- reveal.js documentation — `revealjs.com`
- WCAG 2.1 contrast guidelines — `w3.org/TR/WCAG21/`
- WebAIM contrast checker — `webaim.org/resources/contrastchecker`
- Nature / Science / Cell author guidelines for talks (often in a separate "presentation" section)

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `scientific-slides` (K-Dense Inc.). Consolidated talk-demo scripts into a template, added Beamer / Marp / Quarto code patterns, added a results-first talk-time table, dark-mode contrast guidance, and an accessibility checklist.
