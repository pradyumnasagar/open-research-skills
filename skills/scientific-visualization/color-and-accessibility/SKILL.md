---

name: color-and-accessibility
description: "Choose and audit color palettes for scientific figures. Covers ColorBrewer, viridis, color-blindness simulators (Coblis, Sim Daltonism), texture/pattern encoding, WCAG 2.1 contrast, and alt text."
license: MIT
---




<!-- metadata:
category: scientific-visualization
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - scientific-visualization
  - research
difficulty: intermediate
-->

# Color and Accessibility in Scientific Figures

> This skill is the audit and palette layer for everything else in the visualization category. It is the answer to: "Will every reader of my figure — including the ~8% of men and ~0.5% of women with color vision deficiency (CVD), the low-vision reader, the screen-reader user, the projector-on-yellow-tint reader — extract the same message?" Use it whenever a figure is destined for publication, a talk, a poster, or a public web page.

## When to use

Trigger this skill when any of the following apply:

- You are picking a palette for a new figure.
- A figure uses color as the only encoding for groups, categories, or values.
- A reviewer or co-author has flagged a figure as hard to read.
- You are publishing a figure to a journal that requires alt text and contrast guarantees.
- You are presenting at a venue with a projector of unknown color profile.
- You are designing a figure for a public-facing web page (blog, GitHub README, lab website) that screen readers and CVD readers will encounter.

## When NOT to use

- Pure data exploration with seaborn defaults — use `ors-scientific-visualization-figure-design` and pick a default palette.
- A schematic / workflow figure where most elements are not data — use `ors-scientific-visualization-schematics-diagrams` and apply accessibility at the end.
- A slide deck or poster — use `ors-scientific-visualization-slides-design` or `ors-scientific-visualization-poster-design` (which link back here for the color audit).

## Prerequisites

- A draft of the figure (matplotlib, seaborn, ggplot2, plotly, or a saved PNG/PDF).
- A simulator: a CVD simulator (Coblis, Sim Daltonism, or the `colorblind` Python package), a greyscale conversion (`gs` or ImageMagick), and a contrast checker (WebAIM).
- A target contrast standard: WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large) is the minimum; AAA (7:1) is the recommended target for body text in scientific figures.
- Knowledge of the data type: ordinal (low/medium/high), categorical (mutually exclusive groups), sequential (continuous, one direction), or diverging (continuous, with a meaningful center).

## Core workflow

1. **Identify the data type.** Ordinal, categorical, sequential, or diverging. The data type picks the palette family.
2. **Pick a perceptually uniform palette** by default. For sequential and diverging data, start with `viridis`, `cividis`, `plasma`, or `magma`. These are CVD-friendly by design.
3. **For categorical data, start with Okabe-Ito** (8 CVD-safe colors) or a ColorBrewer qualitative palette. Do not exceed 6–8 groups per figure; split if you must.
4. **Audit with a CVD simulator.** Render the figure under deuteranopia, protanopia, and tritanopia simulations. Any pair of groups that becomes indistinguishable needs a redundant encoding (shape, line style, label).
5. **Test in greyscale.** Convert the figure to greyscale and confirm the data is still readable. If it is not, your encoding is too color-dependent.
6. **Check contrast.** Text and important graphical elements must meet WCAG 2.1 AA at minimum. Body text → 4.5:1; large text (≥ 18 pt or ≥ 14 pt bold) → 3:1; graphical elements → 3:1.
7. **Add redundant encoding.** Pair color with shape, line style, marker, fill pattern, or direct label. The combination is the message; the color alone is decoration.
8. **Write alt text.** 1–3 sentences that name the figure type, the main message, and the key elements. Alt text is for screen readers and for the journal's accessibility metadata.
9. **Audit under projector conditions.** A 4.5:1 contrast on a laptop may wash out to 3:1 on a projector with a yellow tint. Verify on the actual projector or a calibrated sRGB → projector profile.
10. **Document the palette.** Note the palette name and source in the figure caption or methods. This makes the figure reproducible.

## Code patterns

### A. Data type → palette family decision tree

```
What does the color encode?
│
├── A categorical group (e.g., cell type, treatment)
│     → Okabe-Ito or ColorBrewer qualitative
│     → Max 6–8 groups per figure
│
├── A continuous variable, low → high
│     → viridis, cividis, plasma, magma, inferno
│     → Sequential, perceptually uniform
│
├── A continuous variable with a meaningful center (e.g., log2FC, correlation)
│     → RdBu_r, BrBG, PuOr, Spectral (with caveats), coolwarm
│     → Diverging
│
├── A binary on/off
│     → Two Okabe-Ito colors with strong contrast (e.g., #0072B2 vs. #D55E00)
│
└── A heatmap with no natural center
      → viridis (default), then cividis, then magma
      → Avoid jet, rainbow, and "Spectral" for heatmaps
```

### B. Okabe-Ito palette (the categorical default)

The Okabe-Ito 8-color palette was designed to be distinguishable under the three main forms of CVD.

```python
okabe_ito = {
    "black":      "#000000",
    "orange":     "#E69F00",
    "sky_blue":   "#56B4E9",
    "bluish_grn": "#009E73",
    "yellow":     "#F0E442",
    "blue":       "#0072B2",
    "vermilion":  "#D55E00",
    "r_purple":   "#CC79A7",
}
# In matplotlib
import matplotlib.pyplot as plt
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=list(okabe_ito.values()))
# In seaborn
import seaborn as sns
sns.set_palette(list(okabe_ito.values()))
```

R / ggplot2:

```r
okabe_ito <- c("#000000","#E69F00","#56B4E9","#009E73",
               "#F0E442","#0072B2","#D55E00","#CC79A7")
scale_color_manual(values = okabe_ito)
```

### C. viridis and friends (sequential, CVD-friendly by design)

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 4, figsize=(10, 2.2))
for ax, cmap in zip(axes, ["viridis", "cividis", "plasma", "magma"]):
    img = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(img, cmap=cmap, aspect="auto")
    ax.set_title(cmap, fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
```

These four palettes are perceptually uniform, CVD-friendly, and print legibly in greyscale.

### D. CVD simulation (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Simulate deuteranopia / protanopia / tritanopia
# by transforming the RGB image through a CVD matrix.
def simulate_cvd(rgb, cvd_type="deuteranopia"):
    """
    Apply a color-vision-deficiency simulation matrix to an RGB image.
    cvd_type in {'deuteranopia','protanopia','tritanopia','achromatopsia'}.
    """
    # Brettel/Vienot/Mollon CVD matrices — loadable from a library
    # (e.g., `colorblind` package) or from a published lookup table.
    # For brevity, use the `colorblind` package:
    from colorblind import simulate as cb
    return cb.colorblindness(rgb, cvd_type=cvd_type)

img = plt.imread("figure.png")
plt.imsave("figure_deuteranopia.png", simulate_cvd(img, "deuteranopia"))
plt.imsave("figure_protanopia.png",   simulate_cvd(img, "protanopia"))
plt.imsave("figure_tritanopia.png",   simulate_cvd(img, "tritanopia"))
plt.imsave("figure_greyscale.png",    simulate_cvd(img, "achromatopsia"))
```

The `colorblind` package, the `viscm` library, and the `colorspacious` library all expose CVD matrices; the Brettel-Vienot-Mollon transform is the standard reference.

### E. WCAG 2.1 contrast — programmatic check

```python
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    """WCAG 2.1 relative luminance from sRGB 0–255."""
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(fg_hex, bg_hex):
    L1 = relative_luminance(hex_to_rgb(fg_hex))
    L2 = relative_luminance(hex_to_rgb(bg_hex))
    lighter, darker = max(L1, L2), min(L1, L2)
    return (lighter + 0.05) / (darker + 0.05)

# Example
ratio = contrast_ratio("#000000", "#FFFFFF")
print(f"Black on white: {ratio:.2f}:1")
# Black on white: 21.00:1   (passes AAA)
```

WCAG 2.1 targets:

| Element | AA | AAA |
|---|---|---|
| Normal text (< 18 pt, < 14 pt bold) | 4.5:1 | 7:1 |
| Large text (≥ 18 pt, ≥ 14 pt bold) | 3:1 | 4.5:1 |
| Graphical elements (icons, charts) | 3:1 | (n/a) |

For axis labels, legends, and figure captions, target **AA at minimum, AAA when feasible**. For a graphical line on a white background, target 3:1 minimum (line) and 4.5:1 for the legend text.

### F. Greyscale conversion (for the greyscale test)

```bash
# Ghostscript
gs -sDEVICE=pngalpha -sColorConversionStrategy=Gray \
   -o figure_greyscale.png figure.pdf

# ImageMagick
convert figure.png -colorspace Gray figure_greyscale.png
```

If the figure tells its story in greyscale, the encoding is robust. If not, add redundant encoding.

### G. Texture and pattern as redundant encoding

When color alone is not enough, pair it with a pattern, marker shape, or line style. This is critical for figures that may be printed in greyscale.

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(4, 3))
x = np.arange(5)
ax.bar(x - 0.2, [1, 2, 3, 4, 5], width=0.4,
       color="#0072B2", hatch="///",  label="Control")
ax.bar(x + 0.2, [2, 3, 1, 5, 4], width=0.4,
       color="#D55E00", hatch="\\\\", label="Treatment")
ax.set_xticks(x); ax.set_xticklabels(["A", "B", "C", "D", "E"])
ax.legend(frameon=False)
```

Hatch patterns in matplotlib: `/`, `\\`, `|`, `-`, `+`, `x`, `.`, `o`, `O`, `*`. Use 2–3 patterns at most.

Line styles in matplotlib: `'-'` (solid), `'--'` (dashed), `'-.'` (dash-dot), `':'` (dotted). Pair each line style with a marker for maximum redundancy.

Marker shapes: `'o'`, `'s'`, `'^'`, `'D'`, `'v'`, `'P'`, `'*'`. Match marker shape to line style or color for clarity.

### H. Alt text (writing the figure description)

A figure's alt text should answer three questions: *what type of figure is this?*, *what is the main message?*, and *what are the key elements?* It should be 1–3 sentences for a simple figure, up to 5 for a multi-panel composite.

Examples:

- "Volcano plot. Differentially expressed genes (n = 1,243; padj < 0.05, |log2FC| > 1) are shown in red; non-significant genes in gray. The strongest induction is gene X (log2FC = 4.2, padj = 1e-30)."
- "Multi-panel figure with 4 UMAP plots. Panel A shows the full dataset (50,000 cells). Panel B highlights cluster 7 (cyan, 1.2% of cells). Panel C shows that cluster 7 is enriched in patients with outcome Y. Panel D shows the marker genes for cluster 7."
- "Schematic workflow. FASTQ files are QC-filtered with fastp, aligned with STAR, quantified with featureCounts, and tested for differential expression with DESeq2. The output is a results table feeding a volcano plot and a GO enrichment analysis."

Do not start with "Image of" or "Figure showing"; screen readers already announce that the element is a figure.

## CVD simulator matrix

| Simulator | Platform | URL / install | Notes |
|---|---|---|---|
| **Coblis** | Web | `www.color-blindness.com/coblis-color-blindness-simulator` | Drag-and-drop image; covers all 3 types; greyscale option |
| **Sim Daltonism** | macOS | `michelf.ca/projects/sim-daltonism` | Live window that overlays a CVD simulation on the screen |
| **Color Oracle** | Windows / macOS / Linux | `colororacle.org` | Free, applies a CVD filter to the whole screen in real time |
| **Stark** (Sketch / Figma plugin) | Plugin | (varies) | Live CVD preview inside the design tool |
| **`colorblind` (Python)** | Python | `pip install colorblind` | Brettel-Vienot-Mollon transform; scriptable |
| **`colorspacious` (Python)** | Python | `pip install colorspacious` | CVD + greyscale + contrast; uses the same matrices |
| **`viscm` (Python)** | Python | `pip install viscm` | Designed for testing colormap CVD-friendliness |
| **Chrome DevTools "Rendering → Emulate vision deficiencies"** | Browser | Built into Chrome | Live preview of any web page under CVD |
| **Firefox `layout.css.color-mix` + DevTools** | Browser | Built into Firefox | Sim Daltonism-style overlay |

Run every important figure through at least one of these before submission. If two groups become indistinguishable under deuteranopia (the most common CVD, ~6% of men), the figure is not safe for the global readership of a journal.

## Color choices to avoid

Some palettes are widely used in science but fail accessibility:

- **Jet / rainbow**: a 1970s MATLAB default that introduces false boundaries (perceptual non-uniformity) and is especially bad for greyscale and CVD. Use viridis or cividis.
- **Spectral**: a ColorBrewer diverging palette that is not perceptually uniform. Use RdBu_r or BrBG instead.
- **Red-green only**: distinguishes two groups by hue alone, and fails for ~8% of male readers. Use Okabe-Ito orange/blue or a CVD-safe pair.
- **Pure red on pure green, pure red on pure blue, or pure black on pure red**: low contrast for any reader. Use a CVD-safe pair with at least 3:1 contrast.
- **Saturated colors on saturated backgrounds**: the high-saturation + high-saturation combination vibrates and is hard to read on a projector. Use a tinted background (off-white) instead of pure white, and a desaturated foreground.
- **Traffic-light colors for non-traffic-light data**: the cultural association (red = bad, green = good) is not universal. For continuous data, do not encode "low = red, high = green" without explicit labels; use the full hue range so that the perceptual ordering is preserved.

## Common pitfalls

- **Color as the only encoding**: red dots for cases, blue dots for controls. Add markers, panels, or direct labels.
- **Six colors that look fine in sRGB and collapse in print**: pick a palette that survives the journal's color profile (usually CMYK). The Okabe-Ito and viridis palettes are print-safe.
- **Background mismatch**: a figure designed on a white background viewed on a black slide-deck. Audit the figure against the actual background it will be presented on.
- **A 4.5:1 ratio that drops to 3:1 under projector gamma**: re-test on the actual projector.
- **ColorBrewer output as raw hex without testing**: ColorBrewer is a starting point, not a guarantee. Always CVD-test.
- **Alt text that is just the filename**: "figure1.png" tells a screen reader nothing.
- **Inconsistent palette across the manuscript**: figure 1 uses viridis, figure 2 uses jet, figure 3 uses a custom palette. Pick a project-wide palette and use it.
- **Saturation over hierarchy**: every category is at 100% saturation, and nothing is the most important. Reduce saturation for non-emphasis, keep one or two elements at full saturation as the anchor.

## Validation

- **CVD simulation**: render the figure under deuteranopia, protanopia, tritanopia, and achromatopsia. Every group or value must remain distinguishable.
- **Greyscale test**: convert to greyscale (`gs -sColorConversionStrategy=Gray` or ImageMagick). The figure must still tell its story.
- **Contrast test**: every text and graphical element meets WCAG 2.1 AA at minimum. Body text → 4.5:1; graphical → 3:1.
- **Projector test**: view the figure on the actual projector or a similar one. The figure is not ready until it survives the venue.
- **Alt-text test**: paste the figure (no caption) into a document and read the alt text to a colleague. The colleague should be able to sketch the figure from the alt text alone.
- **Print test**: print a color figure on a black-and-white printer. Important information must not be lost.
- **Color-blind colleague test**: the most reliable test is to show the figure to a colleague with CVD. If they can read the figure without explanation, it passes.

## Open alternatives

| Commercial / proprietary | Open alternative | Trade-off |
|---|---|---|
| Adobe Color (palette picker) | coolors.co (web) | Free, fast, no account required |
| ColorSchemer / Pixie (color picker) | GIMP color picker / Inkscape color picker | Free, sufficient for most pickers |
| Tableau / Power BI built-in palettes | viridis, ColorBrewer, Okabe-Ito | CVD-friendly by design; project-wide consistency |
| Mathematica default palettes | viridis, cividis | Free, perceptually uniform, CVD-friendly |
| Colorgorical (Carnegie Mellon generator) | ColorBrewer / iwanthue | Free, less automated, but well-curated |
| Chroma.js color scales | matplotlib / ggplot2 native scales | Free, library-driven, fully scriptable |
| Adobe Illustrator re-color tool | Inkscape color randomization + manual pick | Free; slower |

## References

Internal cross-links to other `ors-*` skills:

- `ors-scientific-visualization-figure-design` — apply the chosen palette to a publication-ready figure.
- `ors-scientific-visualization-schematics-diagrams` — apply the palette to a schematic / workflow.
- `ors-scientific-visualization-slides-design` — apply the palette to a deck.
- `ors-scientific-visualization-poster-design` — apply the palette to a poster.

External resources (do not fabricate exact paths):

- ColorBrewer 2.0 (Cynthia Brewer) — `colorbrewer2.org`
- viridis colormap family — official documentation and motivation
- Okabe-Ito palette (Masataka Okabe and Kei Ito, 2008) — `jfly.uni-koeln.de/color`
- Coblis color-blindness simulator — `color-blindness.com/coblis-color-blindness-simulator`
- Sim Daltonism — `michelf.ca/projects/sim-daltonism`
- Color Oracle — `colororacle.org`
- WebAIM contrast checker — `webaim.org/resources/contrastchecker`
- WCAG 2.1 — `w3.org/TR/WCAG21/`
- `colorblind` Python package — `pypi.org/project/colorblind`
- `colorspacious` Python package — `pypi.org/project/colorspacious`
- Servier Medical Art (CC-BY biomedical icon library) — `smart.servier.com`
- National Eye Institute, color vision deficiency statistics (prevalence of red-green CVD in the population)

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `scientific-visualization` and `bio-data-visualization-color-palettes` (K-Dense Inc.). Merged the two source skills into a single color-and-accessibility skill, added a CVD simulator matrix, redundant-encoding patterns, WCAG 2.1 contrast code, an alt-text template, and a "colors to avoid" section with rationale.