---
name: image-analysis-best-practices
description: "Apply best practices for microscopy image analysis: pixel-size calibration, channel bleed-through, exposure and dynamic range, controls, publication figures, color-blind safe palettes, and proper statistical handling of n=cells vs n=images vs n=animals."
license: MIT
---



<!-- metadata:
category: image-analysis-microscopy
version: 1.0.0
author: Pradyumna Jayaram
tags:
- image-analysis
- best-practices
- controls
- publication
- statistics
- color-blind
difficulty: intermediate
prerequisites:
  tools:
  - python>=3.10
  - imageio
  - numpy
  - scipy
  - matplotlib
  skills: []
sources: 'Original: Rossner & Yamada 2004 JCB editorial ''What''s in a picture?'';
  Adapted: 2026 image-ethics framing, modernized to current ARRIVE 2.0 and NIH figure
  guidelines.; Improvisions: consolidated exposure, scale-bar, and color-blind guidance;
  added hierarchical-statistics section referencing the n=cells vs n=images vs n=animals
  debate.'
-->

# Image Analysis Best Practices: Acquisition, Controls, and Publication
"
> This skill is the "do no harm" companion to the tool-specific
> image-analysis skills. It covers what to do *before* you open a
> single image in CellProfiler, QuPath, or Fiji: how to plan controls,
> how to acquire with enough dynamic range and a real scale bar, how
> to keep channels from contaminating each other, how to make figures
> that survive peer review, and — most importantly — how to handle
> statistics correctly when the unit of analysis is not what the
> spreadsheet says it is. Pair this with
> `ors-image-analysis-microscopy-cellprofiler-pipelines`,
> `ors-image-analysis-microscopy-qupath-pathology`, or
> `ors-image-analysis-microscopy-imagej-fiji-macro`.

## When to use

- Designing a microscopy experiment whose quantitative results will
  appear in a paper, preprint, or grant.
- Reviewing a manuscript or thesis chapter that contains
  microscopy-based quantitative claims.
- Building a figure for a journal, with correct resolution, scale
  bars, color-blind safe palettes, and minimal-necessary processing.
- Deciding what counts as "n" in an image-derived dataset
  (cells vs images vs animals vs fields-of-view).
- Diagnosing a red flag in someone else's figure or your own
  (saturation, mismatch in channel intensities, scaled-up
  background, "western-blot" tweaks to gels).
- Implementing positive/negative/isotype controls for an
  immunofluorescence experiment.

## When NOT to use

- Tool-specific "how do I run CellProfiler / QuPath / Fiji" — use
  the corresponding tool skill in this category.
- Pure flow-cytometry (no spatial information) — see the
  `bio-flow-cytometry-*` skills.
- Statistical testing per se (t-tests, GLMMs) — see the
  statistical-analysis skills; this skill covers *which* test to
  pick, not the mechanics.
- Acquisition-side correction (illumination, chromatic
  aberration) — the tool skills cover that; this skill covers
  *experimental* best practices.

## Prerequisites

- Familiarity with the chosen microscope and acquisition software
  (µManager, NIS-Elements, ZEN, LAS X, slide-scanner software).
- A figure-creation tool (matplotlib, ggplot2, Illustrator,
  Inkscape) with at least one that supports CMYK / 300+ DPI export.
- A small statistics toolset (R, Python statsmodels / scipy) for
  hierarchical models and effect-size calculations.
- Awareness of the target journal's figure requirements (most
  biomedical journals require 300 DPI for color, 600 DPI for
  halftone, vector format for line art — verify with the journal's
  *Instructions for Authors*).

## Core workflow

The order below matters. Skipping step 1 cannot be patched in
step 5.

1. **Plan the experiment *before* imaging.** Specify the biological
   replicate (animal, donor, biological sample), the technical
   replicate (fields-of-view, slides, sections), the *a priori*
   power calculation, and which statistical test will be applied
   later. The MIAME/MIAPE-style checklists (e.g. the CellProfiler
   example pipelines' "metadata") are useful templates.
2. **Set the acquisition parameters once, write them down.**
   - Exposure / gain for every channel chosen to place the
     dimmest expected signal *well above* the noise floor
     (typically with peak pixel 500-3000 of a 12-bit / 16-bit
     dynamic range — see "Dynamic range" below).
   - Pixel size at Nyquist or finer (≈ 2.3× oversampling of the
     optical resolution; for a 1.4 NA objective at 488 nm
     excitation, the Abbe limit is ≈ 200 nm, so 90-100 nm/px
     sampling is good practice).
   - Laser power, integration time, and detector gain recorded in
     a per-channel table.
   - No contrast / brightness / gamma applied at acquisition
     (linear data, no LUT stretching).
3. **Capture the controls.** For fluorescence:
   - **Negative control (no primary / isotype).** Establishes
     autofluorescence and non-specific binding baseline.
   - **Positive control (known-positive sample).** Confirms the
     antibody / probe works and the acquisition range is right.
   - **Single-stain controls (one per channel).** Required for
     unmixing, channel bleed-through correction, and spectral
     unmixing.
   - **DAPI / nuclear channel on its own.** Confirms the nuclear
     segmentation.
4. **Process and quantify on raw data.** Always keep a copy of the
   original `.czi`, `.lif`, `.nd2`, or 16-bit `.tif` in a
   write-once archive. Apply the same processing chain to every
   image in the batch. The image is the data; the figure is the
   visualization.
5. **Document the processing chain.** A short methods paragraph
   listing: software, version, exact modules / commands, any
   thresholds, any color balance changes. Best practice: deposit
   the full pipeline / script (e.g. `.cppipe`, `.qpproj`, `.ijm`,
   Python notebook) in a public or supplementary archive
   (Zenodo, GitHub tag).
6. **Build the figure to journal specs.** Resolution, color space,
   file format, scale bar, channel colors, and any linear
   contrast adjustment must be applied *identically* to all
   panels in a comparison (no "normalized" or "this one is
   brighter to see the structure").
7. **Run the statistics on the right unit of analysis.** See the
   "Common pitfalls — n = cells vs n = images vs n = animals"
   below. Report effect sizes and CIs, not only p-values.
8. **Self-audit before submission.** Run the figure through the
   "Common pitfalls — Image manipulation" checklist. Use the
   CellProfiler example data or test images as a sanity check
   for the whole pipeline.

## Code patterns

### Pixel-size / scale bar verification

```python
import tifffile
import json

# Load a multi-resolution slide and check the embedded XML
# metadata (OME / vendor-specific). Verify the exact metadata
# keys for your file format in the Bio-Formats or vendor docs.
img = tifffile.TiffFile("slide.tif")
# The physical-pixel-size key is format-dependent; the exact
# name and units must be confirmed in the metadata specification.
# print(img.pages[0].tags.get("XResolution"))
```

In the figure, set the scale bar in absolute units — e.g. "10 µm"
in white on a 10-pixel wide line — and never in pixel count
("250 pixels = ? µm, depends on the figure size").

### Check for channel bleed-through

```python
import numpy as np
import tifffile
import matplotlib.pyplot as plt

# Single-stain control: image of only the donor (no acceptor).
donor_only = tifffile.imread("control_donor_only.tif")
# Acceptor-detection channel from that same field:
acceptor_leak = tifffile.imread("control_donor_only_acceptor_ch.tif")

# Plot a 2-D intensity histogram to look for cross-talk
H, xedges, yedges = np.histogram2d(
    donor_only.ravel(), acceptor_leak.ravel(), bins=128
)
plt.imshow(np.log1p(H.T), origin="lower", aspect="auto",
           extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
plt.xlabel("Donor intensity")
plt.ylabel("Acceptor-leak intensity")
plt.title("Single-stain control — check for cross-talk")
plt.colorbar(label="log(1 + count)")
plt.show()
```

A non-zero slope in the high-intensity donor tail means
bleed-through; correct by unmixing (linear spectral unmixing,
linear subtraction with a measured coefficient) or by selecting
narrower emission filters.

### Saturation / dynamic-range audit

```python
import numpy as np
import tifffile

img = tifffile.imread("dapi.tif")
bit_depth = img.dtype  # e.g. uint16

# Percentage of pixels at the max value
sat = np.mean(img == np.iinfo(bit_depth).max) * 100
print(f"Saturated pixels: {sat:.3f}%")

# Median intensity — should be well above the camera's
# dark / readout floor
print(f"Median intensity: {np.median(img):.1f}")
```

Both CellProfiler's `MeasureImageSaturation` and a custom Python
check like this are reasonable. Re-image at lower exposure if
saturation > ~0.5%; re-image at higher exposure if median ≪
0.1% of dynamic range.

### Color-blind safe palette (Wong / Okabe-Ito)

```python
import matplotlib.pyplot as plt
import numpy as np

# Okabe-Ito 8-color palette — distinguishable by all common
# forms of color-vision deficiency. Originally published
# by Okabe & Ito and popularized in Wong 2011 (Nature
# Methods). Always cite the palette you use.
okabe_ito = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
}

fig, ax = plt.subplots()
for (name, color) in okabe_ito.items():
    ax.plot(np.arange(10), np.random.rand(10), color=color, label=name)
ax.legend()
plt.show()
```

### Hierarchical / mixed-effects model (n = cells, n = images, n = animals)

```python
# Pseudo-code: a hierarchical model where per-cell measurements
# are subsamples of per-image measurements, which are subsamples
# of per-animal measurements. Use a linear mixed-effects model
# in statsmodels or R's lme4 — the exact test and link function
# depend on the data type. Verify the model in the statsmodels
# / lme4 documentation.
#
# import statsmodels.formula.api as smf
# model = smf.mixedlm(
#     "intensity ~ treatment",
#     data=per_cell_df,
#     groups=per_cell_df["animal_id"],
#     vc_formula={"image_id": "0 + C(image_id)"}
# )
# result = model.fit()
# print(result.summary())
```

A simpler but *acceptable* alternative when the experimental
design permits is to **average within animal first**, then run
the test on the per-animal table (one number per animal). This
discards the per-cell information but produces a defensible
n = number-of-animals statistical test.

## Common pitfalls

### Image manipulation (Rossner & Yamada 2004, *Journal of Cell Biology*)

- **Adjusting brightness/contrast differently across panels** —
  a frequent reason for editorial rejection. Apply the *same*
  linear adjustment to every image in a comparison.
- **Erasing background speckle / dust / saturated pixels** —
  must be done in a way that is also applied to controls and
  documented. ImageJ's *Cloning* tool used to "clean up" a panel
  is a hard no for a publication figure.
- **Splicing lanes / regions from different gels or fields** —
  must be visibly indicated with a separator line and explained
  in the legend. A "representative" image must be representative
  of the quantified data, not a cherry-picked field.
- **Re-scaling a Western blot's contrast** to hide or enhance a
  band. Always provide the full original.
- **Publication of an image with no scale bar / wrong scale
  bar** — the original Rossner & Yamada editorial gives many
  examples.

### Exposure and dynamic range

- **Pixel intensities pinned at 65535 (or 4095).** Saturated
  pixels cannot be quantified; the relative amount of
  signal across samples is destroyed. Lower the exposure.
- **Median intensity << 1% of the dynamic range.** The signal is
  being thrown away; raise the exposure or use a brighter probe.
- **16-bit data saved as 8-bit JPEG.** All quantitative
  information is lost; the dynamic range is permanently
  compressed.

### Channel bleed-through

- **Using the "yellow" look (green + red colocalization) on
  un-corrected channels.** Strong cross-talk can mimic
  colocalization. Run single-stain controls; compute
  bleed-through coefficients; consider spectral unmixing.
- **Photobleaching during acquisition.** The donor bleaches
  faster than the acceptor, biasing ratiometric measurements
  (FRET) over time. Reduce laser power; minimize exposure
  time; do the FRET calculation on the same frame order.

### Controls

- **No negative control / no isotype.** Every fluorescence
  experiment must have one. For a multi-color panel, include
  single-color controls and a "no primary" or "isotype"
  control per primary.
- **No positive control.** A failed experiment looks identical
  to a successful one with no positive control. Always include
  a known-positive sample.
- **Wrong "isotype" concentration.** Isotype control should be
  at the same concentration (mass, fluorophore-to-protein
  ratio) as the test antibody, not at a generic "matching"
  concentration.

### Publication figures

- **Insufficient resolution.** Most journals require ≥ 300 DPI
  for color, ≥ 600 DPI for halftone, vector format (PDF, SVG,
  EPS) for line art. A "pretty" 72-DPI figure is not
  publication-quality.
- **Using red/green to encode information.** Deuteranopia
  (red-green color-blindness) affects ~6% of male readers;
  use a color-blind safe palette (Wong / Okabe-Ito) and pair
  with shape/label redundancy.
- **No scale bar.** Reviewers will (rightly) reject the
  figure.
- **Inconsistent figure styles within a paper.** Define a
  style once (font, line widths, color, marker sizes,
  annotations) and apply it everywhere.
- **Log-scale axes without a warning.** Log scales hide
  small-magnitude differences; use them with care, and
  label them clearly.

### n = cells vs n = images vs n = animals

This is the single most common statistical error in image
analysis papers (and reviewers are increasingly trained to
catch it). Three scenarios:

- **n = cells, treatment-vs-control.** If 50 cells from one
  animal per condition are measured, the unit of analysis
  is the cell, but the *biological replicate* is still the
  animal. The cell-level test is wrong if it ignores the
  animal-level clustering.
- **n = images (fields-of-view).** Often 5-10 fields per
  condition per animal. The FOV is a *technical* replicate
  nested in animal; analyze as a hierarchical model or
  average within animal first.
- **n = animals.** If you have 6 animals per condition, the
  per-animal mean is the right unit. Doing a t-test on
  per-cell values with n = 1000 is statistically invalid
  because the cells are not independent.

Use a **linear mixed-effects model** (R `lme4`, Python
`statsmodels` mixedlm) with the appropriate random-effect
structure: cells nested in FOVs nested in animals. Or, when
the design is simple, average within animal, plot per-animal
points, and run a t-test on the per-animal means. *Always
report both n = animals and a total cell count in the
legend.*

### Other gotchas

- **Comparing images acquired with different objectives /
  cameras / bit depths.** Calibrate the pixel size and the
  intensity units first; otherwise the comparison is
  meaningless.
- **Comparing control and treated without checking the
  baseline imaging conditions.** Day-to-day, instrument-to-
  instrument variation in lamp output and detector gain can
  exceed biological effects. Block by day, run a control in
  the *same* session, or use a ratiometric measurement.
- **Ignoring 3D context.** A 2-D maximum projection of a Z
  stack is *not* the same data as a single 2-D plane; the
  projection can introduce apparent co-localization
  artifacts.

## Validation

- **Pipeline test on synthetic data:** generate an artificial
  image stack (e.g. 100 circles of known diameter and
  intensity) and verify the pipeline recovers the ground truth
  within tolerance.
- **Spike-and-recovery / dilution series:** where possible,
  spike in a known amount of fluorescent standard and verify
  the measurement is linear in the expected range.
- **Inter-rater agreement:** when annotations are involved
  (pathology, ROIs), compute Cohen's κ or ICC between two
  annotators; report it.
- **Re-analysis by an independent analyst:** if results are
  central to a paper claim, have a second person re-run the
  analysis from raw data using only the methods paragraph.
- **Journals' figure QC:** Cell, Nature, JCB, eLife, and PLOS
  all run published figures through image-manipulation
  screening tools (e.g. the Office of Research Integrity's
  forensic kit). Run your own audit with the
  `bioimage-forensics` or similar tool before submission.

## Open alternatives

- **Forensic image-audit tools:** the *Bioimage Forensics*
  community maintains open tools for detecting cloning and
  splicing. Commercial equivalents exist (e.g. ImageJ-based
  "Analyze → Tools → ...) but are not standard.
- **Acquisition standards:** the *Quality Assessment and
  Reproducibility for Instruments in Optical Microscopy*
  (QUAREP-LiMi) initiative publishes per-modality
  checklists.
- **Reporting standards:** ARRIVE 2.0 (animal research),
  MIAME (microarray — analogously applied to imaging),
  REMARK (tumor marker), and the *CellProfiler* and
  *QuPath* project templates all have methods-section
  templates you can copy.

## References

- Rossner, M. & Yamada, K. M. 2004, "What's in a picture?
  The temptation of image manipulation," *Journal of Cell
  Biology* 166(1):11-15. The foundational editorial on
  image-manipulation ethics.
- Cromey, D. W. 2010, "Avoiding twisted pixels: ethical
  guidelines for the appropriate use and manipulation of
  scientific digital images," *Science and Engineering
  Ethics* 16(4):639-667. Comprehensive practical guide.
- Okabe, M. & Ito, K. 2008, "Color universal design" — the
  origin of the Okabe-Ito palette.
- Wong, B. 2011, "Points of view: Color blindness," *Nature
  Methods* 8:441. Popularized Okabe-Ito for biology.
- QUAREP-LiMi: <https://quarep.org/> — community
  microscopy-quality standards.
- ARRIVE 2.0: <https://arriveguidelines.org/>
- NIH figure guidelines and the *ImageJ for
  Scientists* book (Miura & Nørrelykke, 2021) for
  further practical reading.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram
  from the Rossner & Yamada 2004 JCB editorial and the
  QUAREP-LiMi reporting standards; consolidated the
  n = cells vs n = images vs n = animals guidance and the
  color-blind palette reference.