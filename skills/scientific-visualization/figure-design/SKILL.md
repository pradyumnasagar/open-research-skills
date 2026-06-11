---
name: figure-design
description: "Design publication-quality scientific figures in Python (matplotlib,
  seaborn, plotly) and R (ggplot2). Covers DPI, vector vs raster, color-blind safe
  palettes, fonts, multi-panel layout, legends, scale bars, and axis labels with units.
license: MIT
---

<!-- metadata:
category: scientific-visualization
version: 1.0.0
author: Pradyumna Jayaram
tags:
- figures
- matplotlib
- seaborn
- plotly
- ggplot2
- publication
- dpi
- vector-graphics
- colorblind
difficulty: intermediate
prerequisites:
  tools:
  - python>=3.9
  - R>=4.0 (optional)
  - matplotlib>=3.5
  - seaborn>=0.12
  - plotly>=5.0
  - ggplot2 (R)
  skills: []
sources: 'Original: scientific-visualization (scientific-agent-skills, K-Dense Inc.);
  Adapted: dropped bundled scripts, removed AI image-generation workflow, restructured
  around reusable pattern library; Improvisions: added ggplot2 R patterns, journal-column-width
  reference table, scale-bar/scale-label conventions, vector vs raster decision matrix,
  journal DPI rules consolidated'
-->

# Publication-Quality Figure Design

> This skill turns raw analytical output into figures ready for peer review. It is a self-contained workflow covering resolution, color, typography, layout, and export. Use it whenever the deliverable is a figure that will appear in a manuscript, supplement, thesis, or report — not when you are still exploring data.

## When to use

Trigger this skill when any of the following apply:

- Producing a figure for a journal article, preprint, thesis chapter, or grant.
- Preparing supplementary figures.
- A reviewer or co-author has flagged a figure for legibility, resolution, or color issues.
- You need a multi-panel composite and want consistent style across panels.
- You are finalizing exploratory plots for a public talk, poster, or web page.

## When NOT to use

- Pure exploratory data analysis — use seaborn defaults or `plotly.express` directly.
- Slide-only graphics — see `ors-scientific-visualization-slides-design`.
- Poster-only graphics — see `ors-scientific-visualization-poster-design`.
- Schematic / cartoon figures — see `ors-scientific-visualization-schematics-diagrams`.
- Color and accessibility audits of an existing figure — see `ors-scientific-visualization-color-and-accessibility`.

## Prerequisites

- Python 3.9+ with `matplotlib`, `numpy`, `pandas`, and ideally `seaborn` and `plotly`.
- For R users: a current `ggplot2` and (optionally) `patchwork` / `cowplot` for composition.
- One journal's author guidelines in hand (column widths, accepted formats).
- A working directory layout: `figures/`, `data/`, `src/` (recommended).

## Core workflow

1. **Decide the target.** Identify the destination (journal name, screen vs. print) before drawing anything. This fixes width, font size, and DPI.
2. **Pick the chart family.** Match the question to the chart: distribution, comparison, relationship, composition, change over time. See the decision table below.
3. **Set global style once.** Apply a publication rcParams block (or `theme_set` in R) so every panel in the manuscript shares font, color cycle, and DPI. Do not restyle per-panel.
4. **Encode data, not chartjunk.** Remove top/right spines, gridlines on bar charts, 3D effects, shadows, and decorative backgrounds. Direct-label whenever feasible.
5. **Label with units.** Every axis gets a name plus a unit in parentheses, e.g. `Time (min)`, `Concentration (µM)`. Use sentence case, not ALL CAPS.
6. **Use redundant encoding.** Pair color with shape, line style, or marker — never rely on hue alone. See the color-and-accessibility skill.
7. **Compose panels with gridspec / patchwork.** A 2×2 layout with shared legends, consistent margins, and bold panel labels (A, B, C, D).
8. **Export in the right format.** Vector (PDF, SVG, EPS) for plots; raster (TIFF, PNG) at 300+ DPI for photos and microscopy. Never export plots as JPEG.
9. **Verify at final size.** Open the file at 100% intended print size and read every label. If you cannot, shrink your screen to ~25% and read.

## Code patterns

### A. Publication rcParams (apply once, project-wide)

```python
import matplotlib as mpl

mpl.rcParams.update({"
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.linewidth": 0.8,
    "lines.linewidth": 1.2,
    "lines.markersize": 4,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "figure.dpi": 100,        # screen preview
    "savefig.dpi": 300,       # raster export
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,       # embed real fonts, not Type 3
    "ps.fonttype": 42,
})
```

### B. Vector vs raster decision matrix

| Content | Recommended format | Reason |
|---|---|---|
| Line plot, bar, box, violin, heatmap, contour | PDF or SVG (vector) | Scales to any size; no aliasing |
| Microscopy, photograph, gel, blot | TIFF or PNG, 300–600 DPI | Fixed-pixel source; vectorization is impossible |
| Composite that mixes both | PDF with embedded raster at 300+ DPI | Single artifact for LaTeX |
| Web-only figure | SVG or PNG at 144 DPI | Smaller file, screen-tuned |

> **Rule of thumb**: plots go vector, images go raster. Never export a vector plot as JPEG.

### C. DPI / size reference table (common journals)

Approximate final-figure widths. Always confirm in the journal's "Information for Authors".

| Journal family | Single column | Double column | Min DPI (photo) | Min DPI (line) |
|---|---|---|---|---|
| Nature / Nature methods | 89 mm (3.5") | 183 mm (7.2") | 300 | 600 or vector |
| Science | 55 mm (2.17") | 175 mm (6.9") | 300 | 600 or vector |
| Cell / Cell Reports | 85 mm (3.35") | 174 mm (6.85") | 300 | vector preferred |
| PLOS | 83 mm (3.27") | 169 mm (6.65") | 300 | vector preferred |
| IEEE | 3.5" | 7.16" | 300 | vector preferred |
| eLife | 110 mm (4.33") | 225 mm (8.86") | 300 | vector preferred |
| Generic thesis | 130 mm | 260 mm | 300 | vector |

Convert to matplotlib with `figsize=(width_in, height_in)`. Height is yours to choose; 0.6–0.75 of width is a safe starting point for single-panel plots.

### D. Single-panel line plot with error bars

```python
import matplotlib.pyplot as plt
import numpy as np

# data: mean ± SEM per timepoint per group
t = np.array([0, 1, 2, 4, 8, 24])
ctrl_mean = np.array([1.00, 0.98, 1.01, 1.02, 0.99, 0.97])
ctrl_sem   = np.array([0.04, 0.05, 0.04, 0.06, 0.05, 0.05])
treat_mean = np.array([1.00, 1.10, 1.25, 1.40, 1.32, 1.18])
treat_sem   = np.array([0.05, 0.06, 0.07, 0.08, 0.07, 0.06])

fig, ax = plt.subplots(figsize=(3.5, 2.5))   # Nature single column
ax.errorbar(t, ctrl_mean,  yerr=ctrl_sem,  fmt="o-",
            label="Control", color="#0072B2", capsize=2, lw=1.0, ms=3.5)
ax.errorbar(t, treat_mean, yerr=treat_sem, fmt="s-",
            label="Treatment", color="#D55E00", capsize=2, lw=1.0, ms=3.5)

ax.set_xlabel("Time (h)")
ax.set_ylabel("Relative expression (AU)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, loc="best")
fig.tight_layout()
fig.savefig("figure1.pdf")            # vector
fig.savefig("figure1.png", dpi=300)   # raster fallback
```

### E. Multi-panel with gridspec (matplotlib)

```python
from string import ascii_uppercase
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(7.2, 4.0))  # Nature double column
gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.45,
                      left=0.08, right=0.98, top=0.92, bottom=0.10)

axes = [fig.add_subplot(gs[i // 2, i % 2]) for i in range(4)]

# axes[0].plot(...), axes[0].bar(...), etc.
# axes[0].set_xlabel("..."); axes[0].set_ylabel("...")

for ax, letter in zip(axes, ascii_uppercase):
    ax.text(-0.18, 1.06, letter, transform=ax.transAxes,
            fontsize=10, fontweight="bold", va="top", ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# Optional: shared legend at the figure level
# fig.legend(handles, labels, loc="lower center", ncol=4, frameon=False)
# fig.subplots_adjust(bottom=0.18)
```

### F. Seaborn for statistical comparison

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(context="paper", style="ticks", font_scale=1.0,
              rc={"axes.spines.top": False, "axes.spines.right": False})

fig, ax = plt.subplots(figsize=(3.5, 2.8))
sns.boxplot(data=df, x="treatment", y="response",
            order=["Control", "Low", "High"], palette="colorblind",
            fliersize=0, ax=ax)        # hide outliers
sns.stripplot(data=df, x="treatment", y="response",
              order=["Control", "Low", "High"], color="black",
              alpha=0.4, size=2.5, ax=ax)
ax.set_xlabel("Treatment")
ax.set_ylabel("Response (µM)")
```

### G. Plotly → static export

```python
import plotly.io as pio

# Make Plotly use the same paper-style fonts
pio.kaleido.scope.default_format = "png"
pio.kaleido.scope.default_scale = 3   # ~300 DPI for 96 DPI default

fig.update_layout(
    font=dict(family="Arial, sans-serif", size=10, color="black"),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=60, r=20, t=40, b=50),
)
fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=False)

fig.write_image("figure_interactive.html")           # for the web
fig.write_image("figure_static.png", scale=3)         # for the paper
```

### H. ggplot2 equivalent (R)

```r
library(ggplot2)
library(patchwork)   # for multi-panel composition

p1 <- ggplot(df, aes(t, mean, color = group)) +
  geom_line(linewidth = 0.4) +
  geom_errorbar(aes(ymin = mean - sem, ymax = mean + sem), width = 0.15) +
  scale_color_manual(values = c(Control = "#0072B2", Treatment = "#D55E00")) +
  labs(x = "Time (h)", y = "Relative expression (AU)", color = NULL) +
  theme_classic(base_size = 8, base_family = "Arial") +
  theme(legend.position = "top",
        plot.margin = margin(5, 5, 5, 5, "pt"))

p1 + p1 + plot_layout(ncol = 1)         # compose with patchwork
ggsave("figure1.pdf", width = 3.5, height = 2.5, units = "in")
```

### I. R / ggplot2 — paper theme

```r
theme_paper <- function(base_size = 8, base_family = "Arial") {
  theme_classic(base_size = base_size, base_family = base_family) %+replace%
    theme(
      axis.line = element_line(linewidth = 0.4, colour = "black"),
      axis.ticks = element_line(linewidth = 0.4, colour = "black"),
      legend.key = element_blank(),
      strip.background = element_blank(),
      plot.margin = margin(4, 4, 4, 4, "pt")
    )
}
```

## Color choice (quick reference; full audit in `color-and-accessibility`)

- Sequential continuous data: `viridis`, `cividis`, `plasma`, `magma`.
- Diverging with a meaningful center (e.g., correlation, log fold-change): `RdBu_r`, `BrBG`, `PuOr`.
- Categorical up to ~6 groups: Okabe-Ito (`#E69F00, #56B4E9, #009E73, #F0E442, #0072B2, #D55E00, #CC79A7, #000000`).
- Always test in grayscale (`plt.imshow(..., cmap="Greys")` after a color transform) and with a CVD simulator.

## Typography and legibility

- Sans-serif throughout. Arial / Helvetica for print, DejaVu Sans as the matplotlib fallback.
- Sentence case for axis labels: `Time (min)`, not `TIME (MIN)`.
- Always include units in parentheses — never leave bare axis labels.
- Use `µ`, not `u`. Use the minus sign (U+2212), not a hyphen. Use `×` for multiplication in legends.
- Bold sparingly: only for the one element the reader should anchor on.

## Multi-panel conventions

- Panels labeled with bold uppercase `A`, `B`, `C`, `D` (Nature uses lowercase `a`, `b`, `c` — match the journal).
- Place labels in the top-left of each panel, just outside the axes, not inside the data.
- Share x or y axes when the scales are identical, to make side-by-side comparison honest.
- Align the baselines of bar charts and the y-axes of like units.

## Scale bars and inset axes

- For microscopy, prefer a scale bar over a stated magnification in the caption.
- Draw the scale bar in the lower-right of the panel, in white if the background is dark, black otherwise.
- For geographic or spatial figures, include a north arrow AND a scale bar (or scale text).

## Statistical annotation

- Always state the n in the figure or caption (`n = 3 biological replicates`).
- Mark significance with asterisks and report the test in the caption (`* p < 0.05, ** p < 0.01, two-sided t-test`).
- Show individual data points (jittered or strip) on top of summary bars/boxes; the dot cloud carries more information than the mean alone.
- Specify the dispersion measure (SD, SEM, 95% CI) — never let the reader guess.

## Legends, captions, and the reader

- A figure legend inside the panel is for symbol-to-series mapping. A figure caption is the standalone explanation.
- Direct-label small multiples; reserve the figure-level legend for series comparisons.
- Captions should answer: what is plotted, what are the n and the error measure, what does the test show, and what the reader should conclude.

## Common pitfalls

- **PDF font fallback to Type 3**: garbled text on the publisher's end. Set `pdf.fonttype=42`.
- **Raster at 72 DPI**: blurry when the figure is scaled up. Set `savefig.dpi=300` and verify with `pdfimages -list`.
- **Color-only encoding**: indistinguishable for ~8% of male readers. Add markers, line styles, or panels.
- **Junk axis**: top and right spines, double axes, broken axes without a break mark.
- **Truncated y-axis on a bar chart**: exaggerates differences. Start at zero unless scientifically justified, and mark the break.
- **Inconsistent styles across panels**: different fonts, sizes, or color cycles between figure A and figure B. Set rcParams once, at the top of the project.
- **"Preview" figure saved as the final**: the test version of `figure1.png` ships in the submission. Version-control your outputs.

## Validation

- Open the final PDF in Illustrator/Inkscape and confirm fonts are outlines-or-embedded, not substituted.
- Run `pdfimages -list figure.pdf` and check every embedded image is ≥ 300 DPI.
- Convert the PDF to grayscale (`gs -sDEVICE=pdfwrite -sColorConversionStrategy=Gray ...`) and check the figure still tells its story.
- Run a CVD simulator (Coblis, Sim Daltonism) over a PNG export and confirm series remain distinguishable.
- Compare panel-by-panel: same font size, same color cycle, same line weight, same axis style.
- Print a single panel at target size on paper. If the caption is illegible from 2 feet, the figure is not publication-ready.

## Open alternatives

| Commercial / proprietary | Open alternative | Trade-off |
|---|---|---|
| Adobe Illustrator polish | Inkscape | Same vector file, slightly different UX |
| Origin / GraphPad Prism | matplotlib + seaborn | Free, scriptable, less point-and-click |
| MATLAB plot editor | matplotlib / plotly | Free, slightly different defaults |
| STATA graph editor | ggplot2 | Free, better defaults for publication |
| BioRender figures | Inkscape + sci-schematics skill | Free; less icon library for biology |

## References

Internal cross-links to other `ors-*` skills:

- `ors-scientific-visualization-color-and-accessibility` — pick and audit palettes.
- `ors-scientific-visualization-schematics-diagrams` — non-data illustrative figures.
- `ors-scientific-visualization-slides-design` — adaptation for projection.
- `ors-scientific-visualization-poster-design` — adaptation for large format.
- `ors-bioinformatics-omics-*` — domain-specific plot families (volcano, MA, UMAP, circos, etc.).
- `ors-scientific-writing` — caption and figure-callout guidance.

External resources (do not fabricate exact paths):

- matplotlib official documentation — `matplotlib.org/stable/contents.html`
- matplotlib `rcParams` reference
- seaborn tutorial — `seaborn.pydata.org/tutorial.html`
- ggplot2 documentation — accessed via `?ggplot2` in R, or the official tidyverse site
- patchwork R package (multi-panel ggplot2)
- ColorBrewer 2.0 (Cynthia Brewer) — `colorbrewer2.org`
- viridis colormap family — documentation site
- WCAG 2.1 contrast guidelines — `w3.org/TR/WCAG21/`

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `scientific-visualization` (K-Dense Inc.). Removed AI image-generation scripts, restructured around the publication rcParams + gridspec pattern, added ggplot2 R patterns and a journal-width reference table.