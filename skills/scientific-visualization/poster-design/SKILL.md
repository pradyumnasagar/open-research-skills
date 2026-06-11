---
name: poster-design
description: "Design academic posters for conferences. Covers A0 portrait/landscape,"
license: MIT
---



<!-- metadata:
category: scientific-visualization
version: 1.0.0
author: Pradyumna Jayaram
tags:
- poster
- a0
- latex
- beamerposter
- tikzposter
- baposter
- iposters
- accessibility
- conference
difficulty: intermediate
prerequisites:
  tools:
  - inkscape>=1.0 OR powerpoint/keynote OR texlive-with-beamerposter-tikzposter-baposter
    OR quarto
  skills:
  - ors-scientific-visualization-figure-design
  - ors-scientific-visualization-schematics-diagrams
  - ors-scientific-visualization-color-and-accessibility
sources: 'Original: latex-research-posters (scientific-agent-skills, K-Dense Inc.);
  Adapted: narrowed to a single skill, added PowerPoint/Inkscape paths alongside LaTeX,
  added online poster-session and iPosters patterns; Improvisions: added a QR-code
  workflow, accessibility audit (CVD, contrast, font legibility), a 6-foot test, and
  a print-vs-digital checklist'
-->

# Academic Poster Design

> This skill turns a research paper into a poster that an attendee can read in 2–3 minutes while standing 3–6 feet away. A poster is a *medium*: a long, narrow conversation, not a paper pasted to a wall. The deliverable is a single-page document, typically A0 portrait or landscape, that a passer-by can read top-to-bottom or left-to-right in a logical order.

## When to use

Trigger this skill when any of the following apply:

- A conference requires a poster instead of, or in addition to, a talk.
- A departmental symposium, journal club, or thesis defense is in poster form.
- You want a one-page summary of a project for a recruitment fair, open day, or lab visit.
- The conference is online or hybrid, and the platform is iPosters, Gather, or a custom virtual venue.

## When NOT to use

- Slide decks — use `ors-scientific-visualization-slides-design`.
- Print figures for a paper — use `ors-scientific-visualization-figure-design`.
- Workflow / study-design cartoon embedded in a paper — use `ors-scientific-visualization-schematics-diagrams`.
- A pre-print (PDF) on a personal website — use `ors-scientific-writing`.

## Prerequisites
"
- The conference's poster specification: physical size (A0, 36"×48", 4'×3'), orientation (portrait or landscape), mounting method (push-pin, velcro, frame), and online-platform template if applicable.
- A list of the 3–5 main takeaways. The poster argues for these in the order a passer-by will read.
- High-resolution figures (PDF, 300+ DPI PNG) that survive scaling up to 100% A0.
- A QR code generator (e.g., `qrencode` CLI, or any reputable web tool) for linking to the paper, code, and contact details.
- A second person to read the poster at the back of a room before printing.

## Core workflow

1. **Anchor on the one-sentence takeaway.** Write the conclusion a passer-by should remember after 30 seconds at the poster.
2. **Confirm the spec.** A0 portrait (841 × 1189 mm) is the most common. A0 landscape (1189 × 841 mm) works for content that flows left-to-right. US conferences sometimes specify 36"×48" (914 × 1219 mm) or 4'×3' (1219 × 914 mm).
3. **Apply the 6-foot test.** At 6 feet (≈ 2 m), the title, the figure captions, and the take-home message should be legible. At 3 feet (≈ 1 m), the body text and the figure details should be legible. If not, increase the font size or reduce the content.
4. **Choose a grid.** 2-column, 3-column, or 4-column layout, with a wide top banner for title/author and a bottom strip for QR codes, acknowledgments, and contact.
5. **Set the typography.** One sans-serif family. Title 80–120 pt, section headers 40–60 pt, body 24–32 pt, figure captions 18–24 pt, references 14–18 pt. No body text under 24 pt at A0.
6. **Establish hierarchy.** Title at the top (largest), sections in a consistent order (Background → Method → Results → Conclusion), figures at 50–70% of the column width, take-home in a colored box.
7. **Add a QR code.** One for the paper, one for the code/data, one for the contact card (LinkedIn, ORCID, email). Test that each QR code resolves to a real URL before printing.
8. **Provide a handout.** A US-letter or A4 printout of the poster (1-up or 4-up) is the highest-leverage networking tool. Include the QR codes on the handout.
9. **Accessibility audit.** Run a CVD simulator over an export, check contrast at 4.5:1 minimum, and provide alt text for the digital version.
10. **Print or upload.** For physical posters, print on a single sheet (no tiling) at the venue's print shop or via an online service (sizes and shipping times vary). For online sessions, upload to the platform's template and verify on a phone.

## Code patterns

### A. Tool selection matrix

| Need | Recommended tool | Why |
|---|---|---|
| LaTeX-native, reproducible, version-controllable | **Beamerposter** or **tikzposter** or **baposter** | PDF output, journal-style typography, code-driven |
| Quick layout with drag-and-drop | **PowerPoint** (custom slide size = poster size) | Easy for non-LaTeX users; exports PDF or PNG |
| Vector polish for high-end venues | **Inkscape** | Free, full control, exact mm units, SVG → PDF |
| Mac-only, polished typography | **Keynote** (custom slide size) | Excellent default fonts; exports PDF |
| Quarto / R Markdown report-style | **Quarto** (PDF output, large geometry) | Reproducible; integrates code chunks |
| Online session, virtual venue | **iPosters** (template), Gather, Underline | Platform-specific template; usually PDF upload |
| University-branded template | Provided by your institution or conference | Already meets branding; small adjustments only |

### B. Beamerposter — minimal A0 portrait skeleton

```latex
\documentclass[a0paper,portrait]{baposter}

\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{xcolor}

\definecolor{accent}{HTML}{1F4E79}

\begin{document}

\begin{poster}{
    grid=false,
    columns=3,
    background=plain,
    bgColorOne=white,
    borderColor=accent,
    headerColorOne=accent,
    headerFontColor=white,
    boxColorOne=white,
    headershape=rectangle,
    headerfont=\Large\bf\sffamily,
    textborder=rectangle,
    background=plain
}
{\includegraphics[width=0.07\linewidth]{logo.png}}
{\bf\sffamily\Huge One-sentence takeaway the audience should remember}
{\sf\Large Pradyumna Jayaram \quad \textbar \quad Institution \quad
 \textbar \quad Conference, 2026}
{}
% Logo | Title | Authors

\headerbox{Background}{name=b,column=0,row=0}{
    \small 1--2 short paragraphs of context. The audience needs to know
    \emph{why} this matters.
}

\headerbox{Methods}{name=m,column=0,below=b}{
    \small Cohort, assay, model. Keep it schematic.
    \includegraphics[width=\linewidth]{workflow.png}
}

\headerbox{Result 1}{name=r1,column=1,row=0}{
    \small Headline finding as a complete sentence.
    \includegraphics[width=\linewidth]{fig1.png}
}

\headerbox{Result 2}{name=r2,column=1,below=r1}{
    \small Next figure, with the take-home in bold.
    \includegraphics[width=\linewidth]{fig2.png}
}

\headerbox{Take-home}{name=th,column=2,row=0}{
    \colorbox{accent!20}{\parbox{0.95\linewidth}{\large
        \textbf{One sentence: the answer to the question asked in
        Background.}
    }}
    \vspace{0.5em}
    \small Implications, next steps, contact.
}

\headerbox{QR codes}{name=qr,column=2,below=th}{
    \includegraphics[width=0.3\linewidth]{qr_paper.png}\quad
    \includegraphics[width=0.3\linewidth]{qr_code.png}\quad
    \includegraphics[width=0.3\linewidth]{qr_contact.png}\\
    {\footnotesize Paper \quad\quad Code/data \quad\quad Contact}
}

\end{poster}
\end{document}
```

Compile with `pdflatex poster.tex` (run twice for placement).

### C. tikzposter — alternative LaTeX class

```latex
\documentclass[25pt, a0paper, portrait, margin=0mm,
              innermargin=15mm, blockverticalspace=15mm,
              colspacing=15mm, subcolspacing=8mm]{tikzposter}

\usepackage{graphicx}
\usepackage{booktabs}

\usetheme{Simple}
\usecolorstyle{Default}
\colorlet{blocktitlebgcolor}{blue!70!black}
\colorlet{titlebgcolor}{blue!70!black}

\title{\parbox{0.95\linewidth}{\centering One-sentence takeaway}}
\author{Pradyumna Jayaram}
\institute{Institution}
\titlegraphic{\includegraphics[width=0.05\linewidth]{logo.png}}

\begin{document}

\maketitle

\begin{columns}

\column{0.33}
\block{Background}{
    1--2 short paragraphs. Keep the literature review to a minimum.
}
\block{Methods}{
    \includegraphics[width=\linewidth]{workflow.png}
}

\column{0.33}
\block{Result 1 -- main figure}{
    \includegraphics[width=\linewidth]{fig1.png}\\
    \textbf{One-sentence headline: the main result.}
}
\block{Result 2 -- supporting figure}{
    \includegraphics[width=\linewidth]{fig2.png}\\
    \textbf{Second headline.}
}

\column{0.33}
\block{Take-home}{
    \large \textbf{One sentence the audience should walk away remembering.}
    \normalsize
    \vspace{1em}
    Implications and next steps.
}
\block{Contact and code}{
    \includegraphics[width=0.25\linewidth]{qr_paper.png}\quad
    \includegraphics[width=0.25\linewidth]{qr_code.png}\quad
    \includegraphics[width=0.25\linewidth]{qr_contact.png}\\
    \footnotesize Paper \quad Code \quad Contact
}

\end{columns}

\end{document}
```

Compile with `pdflatex poster.tex` (run twice).

### D. PowerPoint — custom slide size for A0 portrait

```
File → Page Setup → Custom Slide Size
  Width:  84.1 cm   (A0 short side)
  Height: 118.9 cm  (A0 long side)
  Orientation: Portrait
```

Lay out a 3-column grid with built-in guides (`View → Guides`). Insert figures as PNG ≥ 200 DPI (for A0, 200 DPI at column width gives sharp output; 300 DPI is better). Export to PDF (`File → Save As → PDF`) for printing.

### E. QR codes (one-line CLI)

```bash
# Install once: `apt install qrencode` or `brew install qrencode`

# Paper
qrencode -o qr_paper.png  -s 10 -m 4 "https://doi.org/10.1234/abc.2024.001"
# Code
qrencode -o qr_code.png   -s 10 -m 4 "https://github.com/yourname/project"
# Contact card
qrencode -o qr_contact.png -s 10 -m 4 "https://yourdomain.com/cv"
```

The `-s` flag is the dot size in pixels; `-m` is the quiet-zone margin in modules. For poster print, `-s 10 -m 4` gives a QR code that is about 1–2 cm wide and remains scannable from ~30 cm with a phone camera.

### F. Handout — 4-up on US Letter or A4

```bash
# Use pdfjam or a poster service
pdfjam --nup 2x2 poster.pdf --out handout.pdf --landscape
```

Many print shops also offer a 4-up or 6-up handout as a service.

### G. Quarto poster (PDF output, large geometry)

```yaml
---
title: "One-sentence takeaway"
author: "Pradyumna Jayaram"
format:
  pdf:
    geometry:
      - paperwidth=84.1cm
      - paperheight=118.9cm
      - margin=1.5cm
    fig-width: 6
    fig-height: 4
---
```

Quarto is not a poster-specific framework, but its `pdf` output with custom geometry works well for posters whose content is mostly prose and figures in a 2- or 3-column grid (use fenced divs or `multicol`).

## Layout principles

### Column count

| Column count | Best for |
|---|---|
| 2 columns | Short posters, dense figures, equations-heavy content |
| 3 columns | The default for A0 portrait; balances figure and text |
| 4 columns | A0 landscape with a wide figure spread across columns 2–3 |

### Reading order

Use a numbered or arrowed reading order across the columns. The two common patterns are:

- **Linear (Z-pattern)**: Title → Background (col 1) → Method (col 1) → Result 1 (col 2) → Result 2 (col 2) → Take-home (col 3) → QR codes (col 3).
- **Center-out**: Title → central figure (col 2) → supporting details on both sides.

Numbered circles (1, 2, 3) at the start of each block help a passer-by follow the order without backtracking.

### Whitespace

- 10–15 mm of margin around the whole poster.
- 10–15 mm of padding inside each block.
- 15–25 mm between blocks.
- A poster that fills every millimeter looks crowded and is hard to read at 6 feet.

### Figures at the right size

A figure that takes 50–70% of a column width is the sweet spot. Smaller figures feel like afterthoughts; larger figures are illegible from 6 feet. The take-home message of each figure should be readable as the figure caption (in 18–24 pt, not 8).

## Typography at A0

- **Title**: 80–120 pt, bold, sans-serif. White text on the colored banner, or black on white.
- **Authors and affiliation**: 30–40 pt. Less prominent than the title but still readable from 6 feet.
- **Section headers**: 40–60 pt, bold. Same color as the title banner.
- **Body text**: 24–32 pt, regular weight. Never below 24 pt.
- **Figure captions**: 18–24 pt, italic or regular.
- **References**: 14–18 pt (the smallest text on the poster).
- **Take-home message**: 40–60 pt, bold, in a colored box.

Rule of thumb: if you have to lean in to read a block, the text is too small.

## The 6-foot test (and the 3-foot test)

- **At 6 feet (2 m)**: the title, the section headers, the figures, and the take-home box should all be readable.
- **At 3 feet (1 m)**: the body text, the figure captions, and the axis labels should be readable.
- **At 1 foot (0.3 m)**: the references, the equations, and the small print should be readable.

Test by taping A4 printouts of each block to a wall at the same relative size, then walking back 2 m and 1 m. If the smallest text is illegible from 1 m, increase the font size; do not shrink the poster.

## QR codes: what to put on them

A poster can carry 2–3 QR codes without crowding:

1. **Paper**: a DOI URL or a direct link to the published paper.
2. **Code / data**: a GitHub, Zenodo, or figshare URL.
3. **Contact**: a LinkedIn profile, ORCID page, or a vCard.

Keep the QR codes at least 1.5 × 1.5 cm on the printed poster, with a quiet zone (white margin) of 4 modules. Test each code with a phone camera before printing; a high error-correction level (M or H) makes the codes more robust to the small print artifacts of poster printing.

## Accessibility for posters

- **Color + shape**. Pair color with shape or pattern for the most important categories. A poster with only red/green coding excludes ~8% of male readers.
- **Contrast**. Body text ≥ 4.5:1 against its background (WCAG 2.1 AA). Title text ≥ 7:1 is recommended.
- **Font size for low vision**. If the body text is 24 pt, a low-vision reader can still use a magnifier; below 18 pt, the poster is inaccessible.
- **Alt text for the digital version**. If the poster is also uploaded to an iPosters-style platform, write 1–3 sentences of alt text describing the layout, the main figures, and the take-home.
- **No information conveyed by color alone**. Use line style, marker shape, or direct labels.
- **Plain language in the take-home**. The take-home is the single block a non-specialist will read. Avoid jargon in that block.

## Online poster sessions and iPosters

For virtual or hybrid conferences:

- **iPosters** uses a fixed template (PDF upload) and a sidebar for the abstract, video, and chat. The poster should be exported at the platform's specified size (often a custom aspect ratio, not A0).
- **Gather** and similar platforms use a static image plus a video or live-chat window. The poster is the "room" the audience walks into.
- **Tips for online sessions**:
    - Export the poster as a single PDF or a high-DPI PNG. The platform usually does the rendering.
    - Add a 30-second narrated video walking through the poster; upload it to the platform or YouTube and link via a QR code.
    - Pin a chat window or Zoom link for live Q&A.
    - Provide a downloadable PDF of the poster (the digital equivalent of a handout).

## Common pitfalls

- **Wall of text**: the poster is the paper pasted onto a wall. It is not. The body text should be a third of the paper's text at most.
- **Figures that are too small**: 4 tiny figures in a row, each illegible from 6 feet. Use 2 figures, each at 50–70% of column width.
- **Inconsistent typography**: different fonts in different blocks, different sizes for "Methods" and "Approach". Pick a theme (Beamerposter theme, tikzposter theme, PowerPoint master) and stick to it.
- **Missing the take-home**: the audience walks away and cannot state the conclusion. The take-home block is non-negotiable.
- **Broken QR codes**: a typo in the URL, a code that resolves to a 404. Test every QR code with two different phone cameras.
- **Wrong size**: A0 vs. A1, landscape vs. portrait. Re-check the conference's spec every year.
- **Title in a font that does not render in the venue's printer**: an unusual font that the venue's print service does not have. Use a common font (Helvetica, Arial, DejaVu) or convert text to paths in Inkscape (`Path → Object to Path`).
- **Low-resolution figures**: a 72 DPI screenshot from a paper that becomes blurry at A0. Always export figures at 200–300 DPI.
- **No contact info**: the audience wants to follow up but has no email. Add a contact block with email, ORCID, and a QR code.
- **Poster too busy for the venue**: a 30-block poster at a 5-minute poster session. Cut to the 6–8 blocks that deliver the main message.

## Validation

- **6-foot test**: tape the poster to a wall, walk 2 m back, and read the title, headers, and figures. If you cannot, the typography is too small.
- **3-foot test**: walk 1 m back, read the body text and figure captions.
- **Cold-read test**: ask a colleague to read the poster in 2 minutes and state the main conclusion. If they cannot, simplify.
- **QR-code test**: scan every QR code with a phone camera before printing. Test the resolved URL.
- **Color test**: convert a low-DPI export to greyscale and check that all figures remain distinguishable.
- **Print test**: print a US-letter / A4 version of the poster before sending the A0 file to the print shop. Catch layout issues at low cost.
- **Handout test**: print a 4-up handout and bring 50 copies. The handout is the highest-leverage networking tool at the session.

## Open alternatives

| Commercial / proprietary | Open alternative | Trade-off |
|---|---|---|
| Adobe Illustrator (poster polish) | Inkscape | Free, full vector control, mm units |
| PowerPoint Poster templates | LibreOffice Impress / custom PowerPoint master | Free, less curated |
| Keynote (macOS) | LibreOffice Impress | Cross-platform; less polished default typography |
| PosterPresentations.com / Makesigns.com | Local university print shop / `pdfjam` + `poster` service | Free for in-house; per-sheet cost for online services |
| BioRender poster (icon-heavy) | Inkscape + sci-icon set (e.g., Servier Medical Art) | Free; smaller icon library |
| iPosters Pro (paid) | iPosters free tier / custom Zoom + PDF | Free; less analytics |
| Mentimeter live polls | Wooclap / direct QR-to-Google-Form | Free tier; fewer features |
| Beautiful.ai / Tome (generative) | Hand-author in Beamerposter / Inkscape | Reliable, disclosable, accessible; slower |

## References

Internal cross-links to other `ors-*` skills:

- `ors-scientific-visualization-figure-design` — DPI, fonts, multi-panel layout that the poster figures use.
- `ors-scientific-visualization-schematics-diagrams` — workflow and study-design blocks.
- `ors-scientific-visualization-color-and-accessibility` — palette choice and contrast audit.
- `ors-scientific-visualization-slides-design` — when the same story is told as a talk instead of a poster.
- `ors-scientific-writing` — caption and take-home phrasing.

External resources (do not fabricate exact paths):

- Beamerposter documentation — `ctan.org/pkg/beamerposter`
- tikzposter documentation — `ctan.org/pkg/tikzposter`
- baposter documentation — `ctan.org/pkg/baposter`
- Quarto PDF format — `quarto.org/docs/output-formats/pdf`
- Inkscape documentation — `inkscape.org/doc`
- iPosters platform — `ipostersessions.com`
- WCAG 2.1 contrast guidelines — `w3.org/TR/WCAG21/`
- WebAIM contrast checker — `webaim.org/resources/contrastchecker`
- qrencode CLI — `fukuchi.org/works/qrencode`

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `latex-research-posters` (K-Dense Inc.). Consolidated the LaTeX-only workflow into a tool-selection matrix, added Beamerposter / tikzposter / PowerPoint / Inkscape paths, added a QR-code workflow, online-session and iPosters patterns, and an accessibility audit.