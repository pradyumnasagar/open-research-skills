---

name: cellprofiler-pipelines
description: "Use CellProfiler 5.x to build reproducible pipelines for cell/nuclei segmentation, illumination correction, feature extraction, and high-content screening assays including CellPainting."
license: MIT
---




<!-- metadata:
category: image-analysis-microscopy
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - image-analysis-microscopy
  - research
difficulty: intermediate
-->

# CellProfiler Pipelines for High-Content Image Analysis

> CellProfiler is the de-facto open-source standard for building modular,
> reproducible image-analysis pipelines at scale. The 5.x line introduced
> a redesigned module browser, a Java-less native distribution, and tighter
> integration with the Open Microscopy Environment (OME) formats. This skill
> walks through building a high-content pipeline end-to-end: ingest →
> illumination correction → primary/secondary object identification →
> measurement → export. Use it whenever you have a multi-well plate, a
> tissue microarray, or a CellPainting screen and need an auditable,
> GUI-friendly workflow that a non-programmer biologist can review and run.

## When to use

- Building a segmentation + measurement pipeline for fluorescence or
  brightfield high-content screening (HCS) data.
- CellPainting (or any multi-channel morphological profiling) assays
  where the same pipeline runs across thousands of wells.
- Quality control of an image set before downstream analysis
  (focus, saturation, illumination flatness).
- Producing per-cell feature tables for downstream clustering,
  classification, or hit selection.
- Standardizing an analysis that collaborators will reproduce across
  instruments or sites.

## When NOT to use

- Single images, exploratory analysis, or a one-off measurement — use
  ImageJ/Fiji or QuPath interactively.
- Whole-slide histopathology with gigapixel images — use QuPath
  (see `ors-image-analysis-microscopy-qupath-pathology`) which
  streams tiles rather than loading whole slides.
- Deep-learning segmentation only — use Cellpose / StarDist / nnU-Net
  directly and consume the masks downstream in Python. CellProfiler can
  call these as plugins but the modeling lives elsewhere.
- Tracking cells across time-lapse frames — CellProfiler's tracking
  modules exist but a dedicated tracker (TrackMate) is usually better.
- 3D volumetric segmentation — possible in CellProfiler but heavy; the
  napari + cellpose workflow is typically preferred.

## Prerequisites

- **CellProfiler ≥ 5.0** (native installer from cellprofiler.org, no
  Java required on 5.x). Linux, macOS, and Windows are all supported.
- **Java 11+** (only if you run plugins that ship as `.jar` files —
  most current plugins are Python-based).
- A folder of images in a vendor format CellProfiler can read
  (`.tif`, `.tiff`, `.png`, `.czi`, `.lif`, `.nd2`, `.oib`, `.ome.tif`,"
  `.ome.btf`) — see the CellProfiler "Input modules" docs for the
  current supported list.
- A consistent pixel-size calibration (microns per pixel) for every
  image in the batch. Embed this in metadata when possible (OME-TIFF,
  OME-XML); otherwise set it in the pipeline's `Metadata` module.
- (Optional) **CellProfiler Analyst ≥ 2.0** for downstream hit
  classification, clustering, and visualization of the per-object
  measurement table.

## Core workflow

A canonical CellProfiler pipeline follows a fixed ordering convention
that the Broad community has converged on. Deviating from it confuses
collaborators and reviewers.

1. **Input modules** — load images by file, by regular expression, or
   from a metadata-indexed CSV. Always set pixel size in the `Metadata`
   module so downstream measurements are in physical units (µm, µm²).
2. **NamesAndTypes** — assign each image's role (`DNA`, `CellMask`,
   `Brightfield`, `IlluminationFunction`, etc.). A common mistake is
   to skip this and let downstream modules guess.
3. **Groups** (optional) — define replicate groupings when running
   multi-batch screens.
4. **Image preprocessing** — `CorrectIlluminationCalculate` followed by
   `CorrectIlluminationApply`, or `EnhanceOrSuppressFeatures` for
   background subtraction. Order matters: correction before segmentation.
5. **Object identification** — at minimum, nuclei via
   `IdentifyPrimaryObjects` and cells/cytoplasm via
   `IdentifySecondaryObjects` (which uses the primary as a seed).
   Tissue regions use `IdentifyTissue` and similar modules — refer to
   the CellProfiler module index for the exact current name.
6. **Object processing** — `FilterObjects`, `SplitOrMergeObjects`,
   `RelateObjects` (to nest cytoplasm inside nuclei, etc.).
7. **Measurement modules** — `MeasureObjectIntensity`,
   `MeasureObjectSizeShape`, `MeasureObjectNeighbors`,
   `MeasureTexture`, `MeasureColocalization` (when applicable). Add
   `MeasureImageQuality` for QC.
8. **QC outputs** — `FlagImage`, `DisplayDataOnImage`, and
   `GroupsToIgnore`/`ImageSet` filtering for failed wells.
9. **Export** — `ExportToSpreadsheet` for CSV/`MySQL`/`SQLite`, or
   `ExportToDatabase` for a SQLite/Postgres backend consumed by
   CellProfiler Analyst.

### Typical CellPainting pipeline (sketch)

The published CellPainting protocol (Bray et al., 2016, *Nature Protocols*)
and its v5 update define five imaging channels: Hoechst (nuclei),
Concanavalin A / WGA (ER/membrane), phalloidin (actin), MitoTracker
(mitochondria), and a property-discovering stain (e.g. wheat-germ
agglutinin in some variants). A CellProfiler 5.x CellPainting pipeline
ingests a 5-channel `.ome.tiff` per well, runs the steps above, and
exports per-cell features for downstream `pycytominer` aggregation
into the morphological profiles that feed into hit selection.

### Batch processing with CellProfiler Analyst

After exporting per-cell measurements to a SQLite database, open
CellProfiler Analyst, point it at the database, define treatments vs
controls via the `input.csv` from the pipeline, and:

- **Classifier** — train a random forest to separate positive and
  negative controls (e.g. known toxic vs DMSO wells), then score all
  wells to triage hits.
- **Clustering** — visualize the per-well feature vector with t-SNE /
  UMAP and color by treatment to find phenotype clusters.
- **Image gallery** — browse the actual image tiles corresponding to
  any cell or well, directly linked from the measurement table.

Always pin the random-seed, the CellProfiler version, and the pipeline
file (`.cppipe`) in your methods — pipelines are versioned like code.

## Code patterns

> Note: CellProfiler pipelines are typically constructed in the GUI
> and saved as `.cppipe` (JSON in 5.x) or `.cpproj`. The following
> snippets show how to drive CellProfiler from the command line and
> how to inspect or generate pipelines programmatically. They are
> intentionally framework-level — confirm exact module names and
> parameter keys against the current CellProfiler module index at
> cellprofiler.org before deploying.

### Headless batch run (Linux/macOS CLI)

```bash
# CellProfiler 5.x on Linux
cellprofiler \
  --run-headless \
  --pipeline ./pipelines/cellpainting_v5.cppipe \
  --data-in ./plate_images/ \
  --output-directory ./output/2026-06-10_run/ \
  --image-set-output ./output/2026-06-10_run/image_set.csv \
  --log-level INFO \
  --plugins-directory ./plugins/
```

For Docker-based reproducible runs, see the `cellprofiler/cellprofiler`
images on Docker Hub. Pin the image tag (e.g. `:5.0.0`) to lock the
analysis environment.

### Programmatic pipeline construction (Python)

Useful when you need to generate many near-identical pipelines that
vary in channel order or thresholds.

```python
# Pseudo-code — verify the current Python API in the CellProfiler docs
# before relying on a specific import path.
from cellprofiler_core.pipeline import Pipeline
from cellprofiler_core.setting import JSONFolder

pipeline = Pipeline()
# Add modules by name; consult the module list for valid identifiers.
# pipeline.add_module("Metadata")
# pipeline.add_module("NamesAndTypes")
# pipeline.add_module("IdentifyPrimaryObjects")
# ...
pipeline.save("./pipelines/auto_generated.cppipe")
```

### Loading per-cell features into Python (post-pipeline)

```python
import pandas as pd

# CellProfiler exports one CSV per object type
nuclei = pd.read_csv("./output/MyExpt_Nuclei.csv")
cells  = pd.read_csv("./output/MyExpt_Cells.csv")
images = pd.read_csv("./output/MyExpt_Image.csv")

# ParentObject relationship is encoded by a numeric ImageNumber /
# ObjectNumber pair plus the parent link
merged = nuclei.merge(
    cells,
    on=["ImageNumber", "Parent_Cells"],
    suffixes=("_nuc", "_cell"),
)
print(merged.shape)
```

## Common pitfalls

- **Channel order mismatch.** A pipeline built on DAPI/FITC/Cy3/Cy5
  silently produces garbage if the acquisition swaps to DAPI/Cy3/FITC.
  Always read channel names from the file's OME metadata rather than
  trusting filename order. Set up `NamesAndTypes` with explicit
  channel-pattern regex.
- **Wrong pixel size.** If two instruments record at 0.325 µm/px and
  the other at 0.65 µm/px, the same segmentation threshold yields
  wildly different object counts. Embed microns/px in the acquisition
  metadata; assert equality in a pipeline-test step.
- **Saturated pixels.** A bright nucleus can exceed 16-bit range and
  the segmentation module will treat it as one giant object. Add
  `MeasureImageSaturation` and gate out saturated wells.
- **Illumination bias left uncorrected.** Vignetting and lamp droop
  bias texture and intensity features. `CorrectIlluminationCalculate`
  per-plate (per "group") with the "Background" method almost always
  helps. Validate by eye on a flat-field well.
- **Treating the same cell as a "n" in statistics.** If your biological
  replicate is the animal, the per-cell rows are subsamples — see
  `ors-image-analysis-microscopy-image-analysis-best-practices` for
  the proper hierarchical model.
- **Segmentation parameter "fit and forget".** A threshold tuned on
  one well can fail across the plate. Use the per-image `Otsu` or
  `MoG` adaptive thresholding strategies and validate visually
  with `DisplayDataOnImage` on at least 20 random wells per batch.
- **Filename-based grouping** (e.g. grouping by `BATCH_01`, `BATCH_02`)
  breaks silently when a new batch changes the prefix. Use the
  built-in `Metadata` module's CSV/regular-expression grouping.

## Validation

- **Visual:** open 20-30 random per-image `DisplayDataOnImage` overlays
  per batch and confirm the segmentation outlines nuclei/cells. QuPath
  can also load CellProfiler's exported object outlines.
- **Numerical:** compare positive vs negative control per-feature
  distributions (Z'-factor ≥ 0.5 indicates a robust screening assay
  per Zhang et al., 1999). Compute via `scipy.stats` or pycytominer's
  `z_prime` helper.
- **Reproducibility:** a re-run of the same `.cppipe` over the same
  input folder must produce byte-identical SQLite output when the
  random seed and module order are pinned. Hash the pipeline file
  alongside the run.
- **QC metrics:** `MeasureImageQuality` (focus score, saturation,
  illumination uniformity) per well; fail and exclude any well outside
  the acceptable range before any downstream hit calling.

## Open alternatives

- **QuPath** (`ors-image-analysis-microscopy-qupath-pathology`) — much
  stronger for whole-slide pathology and pixel classification;
  weaker than CellProfiler for plate-based HCS.
- **ImageJ/Fiji macros** (`ors-image-analysis-microscopy-imagej-fiji-macro`)
  — better for one-off measurements and rapid iteration; weaker for
  reproducible batch pipelines.
- **Cellpose / StarDist / nnU-Net** — for segmentation-only workflows
  that feed into a Python-based feature pipeline (e.g. with `squidpy`,
  `scimap`, or `napari`). These are often *combined* with CellProfiler
  via the CellProfiler "RunCellpose" plugin in current versions.
- **napari** — for 3D volumetric data and interactive parameter
  exploration.
- **Commercial:** Columbus (PerkinElmer), Harmony (Revvity/Opera),
  IN Cell Analyzer Workstation (GE/Cytiva), MetaXpress (Molecular
  Devices). All use proprietary, locked pipelines; CellProfiler is the
  only fully open, modifiable equivalent.

## References

- CellProfiler home: <https://cellprofiler.org/>
- CellProfiler manual (latest): <https://cellprofiler.org/manual>
- CellProfiler GitHub: <https://github.com/CellProfiler/CellProfiler>
- CellProfiler Analyst: <https://cellprofileranalyst.org/>
- Bray et al. 2016, *Nature Protocols* — CellPainting protocol
  (PubMed: 27560178). The published v5 update is referenced on the
  cellprofiler.org CellPainting page.
- Cimini et al. 2023, *Nature Protocols* — Optimized CellPainting
  workflow (PubMed: 36914892).
- pycytominer (for downstream aggregation of CellProfiler output):
  <https://github.com/cytomining/pycytominer>

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from
  the Broad Institute CellProfiler documentation set; consolidated
  CellPainting notes and CellProfiler Analyst pointers.