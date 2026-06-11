---
name: qupath-pathology
description: "Use QuPath 0.5.x for whole-slide image import, annotation, cell detection,"
license: MIT
---



<!-- metadata:
category: image-analysis-microscopy
version: 1.0.0
author: Pradyumna Jayaram
tags:
- qupath
- digital-pathology
- whole-slide
- cell-detection
- pixel-classification
- stardist
- cellpose
difficulty: intermediate
prerequisites:
  tools:
  - qupath>=0.5
  - java>=17
  - jdk>=17
  skills: []
sources: 'Original: QuPath documentation (qupath.readthedocs.io); Adapted: 2026 QuPath
  0.5.x features, modernized StarDist/Cellpose extension install notes.; Improvisions:
  added TMA workflow pointers, multiplexed analysis notes (e.g. OME-TIFF multi-channel),
  and JUPYTER-via-QuPath section.'
-->

# QuPath for Digital Pathology and Whole-Slide Image Analysis

> QuPath is the leading open-source platform for whole-slide image
> (WSI) analysis in digital pathology. The 0.5.x line introduced a
> revamped extension manager, improved GPU support for deep-learning
> extensions (StarDist, Cellpose, InstanSeg), and a more performant
> tile-streaming data model. Use QuPath when you have gigapixel H&E or
> fluorescence slides, need a graphical annotator that a pathologist
> can review, and want pixel- or cell-level quantification that scales
> to hundreds of slides. The same project file can drive downstream"
> bioimage analysis in Python via QuPath's "Run script" and command-line
> automation interfaces.

## When to use

- Importing, annotating, and quantifying whole-slide images (H&E,
  IHC, fluorescence) from `.svs`, `.ndpi`, `.czi`, `.lif`, `.qptiff`,
  `.bif`, `.scn`, `.mrxs`, `.tiff`, etc. — see the QuPath docs for
  the current full list.
- Manual or semi-automated annotation of regions of interest
  (tumor, stroma, necrosis, lymph follicles) for downstream
  classification or quantification.
- Cell detection on H&E or fluorescence using built-in
  "Cell detection" (hematoxylin-based watershed) or via the StarDist
  or Cellpose extensions.
- Pixel classification to learn tissue types (tumor vs stroma vs
  lumen) from a few hand-drawn regions, then apply to the whole slide
  and the whole project.
- Training or applying deep-learning models on QuPath objects
  (pixel classifier, cell classifier, object classifier).
- Tissue Microarray (TMA) workflows: dearraying cores, scoring IHC
  by core, exporting per-core measurements.
- Multiplexed fluorescence / mIHC workflows with multi-channel
  OME-TIFF input and per-marker cell phenotyping.

## When NOT to use

- Plate-based high-content screening (HCS) — use CellProfiler
  (`ors-image-analysis-microscopy-cellprofiler-pipelines`), which has
  first-class plate-metadata handling.
- 2D or 3D time-lapse tracking of live cells — use
  ImageJ/Fiji's TrackMate or napari + trackpy
  (`ors-image-analysis-microscopy-imagej-fiji-macro`).
- Pure segmentation modeling (training a new U-Net / StarDist model
  from scratch) — QuPath consumes models; build them with
  cellpose, starDist, or nnU-Net and import the weights.
- One-off fluorescence quantification on a few images — ImageJ/Fiji
  is faster to set up.
- Server-side, fully unsupervised batch processing of millions of
  slides — QuPath is best when a human is in the loop; for a pure
  pipeline, use the `qupath` command-line script runner or a
  dedicated WSI tool like HistomicsTK / WSInfer.

## Prerequisites

- **QuPath ≥ 0.5** (the current major release). Download a
  self-contained installer from <https://qupath.github.io>. QuPath
  bundles a JRE in the standard installer, but for command-line use
  you should install **JDK 17** or newer.
- **Memory:** for very large slides (≥ 100k × 100k pixels) allocate
  16-32 GB of RAM. QuPath is friendly to tile-streaming but big
  classifications will not fit if your machine is tight.
- **GPU (optional but recommended):** a CUDA-capable NVIDIA GPU
  greatly accelerates StarDist, Cellpose, and the deep-learning
  pixel classifier. Check the QuPath docs for the supported
  PyTorch / CUDA versions.
- **Extensions:** install via QuPath's *Extensions* menu —
  StarDist, Cellpose, InstanSeg, and any domain-specific extension
  you need.

## Core workflow

A typical QuPath project follows the same shape regardless of
downstream analysis:

1. **Create a project** and set up folder structure. QuPath projects
   hold an `Images` folder of source slides, an `Exports` folder, and
   the `.qpproj` file that points at them. Version-control the
   `.qpproj` and store slides on shared storage, not in the project
   itself.
2. **Import whole-slide images.** Drag-and-drop into the project, or
   use the command-line `--import` mode. For very large projects,
   populate the `Images/` folder and let QuPath read the directory
   list.
3. **Inspect and annotate.**
   - For H&E: use the *Brush*, *Wand*, or *Polygon* tools to draw
     regions, *Classify → Set class* to label them (Tumor, Stroma,
     Ignore).
   - For fluorescence: confirm channel order from the import
     dialog and re-arrange if needed; annotate the regions of
     interest (ROIs).
4. **Cell detection or deep-learning segmentation.**
   - *Built-in:* "Analyze → Cell detection → Cell detection"
     (hematoxylin-OD threshold + watershed) works for many H&E
     cases.
   - *StarDist extension:* preferred for dense nuclei. Train or
     pick a pretrained model, run on ROIs, review overlays.
   - *Cellpose extension:* preferred for unusual morphologies or
     fluorescence; pick a model (e.g. `cyto3`, `nuclei`) and
     run with appropriate diameter.
5. **Pixel classification (optional but powerful).** For "tumor vs
   stroma" or "PD-L1-positive vs negative" at the pixel level:
   - Annotate representative regions across many classes.
   - *Classify → Pixel classification → Train classifier.* QuPath
     trains a Random Forest in seconds on millions of pixels.
   - Apply to ROIs or whole slides; review the heatmap; refine the
     annotations and retrain.
6. **Object / cell classification.** Add a *Cell classification* or
   *Object classification* step. Use measurements (intensity,
   shape, neighbor counts) to identify phenotypes.
7. **Workflow / batch.** Build a *Workflow* (QuPath's reproduci-
   bility primitive) that chains the steps above. Workflows are
   stored alongside the project and can be run headless via the
   command line.
8. **Export.**
   - Per-object measurements to CSV/TSV from the "Show detections"
     table → *Export*.
   - Per-image summary metrics via a custom groovy script.
   - Annotation overlays as GeoJSON for downstream tools.
9. **TMA dearraying** (when applicable): use *TMA → Add TMA grid*
   then *TMA → TMA dearrayer* to map cores to labels. Score IHC
   per core and export a TMA grid + table.

### Multiplexed / mIHC workflow (sketch)

For multi-channel fluorescence (e.g. OPAL, CODEX, Hyperion):

- Import as a multi-channel OME-TIFF or the vendor's QPTIFF.
- In the Brightness/Contrast panel, assign each channel a color and
  confirm the panel (e.g. DAPI / CD3 / CD8 / PD-1 / pan-CK / FoxP3).
- Use *Cell detection* (fluorescence mode) on the nuclear marker,
  then *Set cell intensity classifications* to assign per-marker
  positive/negative thresholds.
- Use *Object classification* (or a script) to derive phenotype
  classes (e.g. CD8⁺ PD-1⁺ FoxP3⁻ effector T cell).
- Export per-cell phenotyping for downstream `scimap`/`squidpy`
  spatial analysis.

### Command-line / headless run

```bash
# Verify the current CLI flags in the QuPath docs
qupath \
  --project /data/myproj.qpproj \
  --script /scripts/run_tma_grid.groovy \
  --save
```

Use this when integrating QuPath into an nf-core / Snakemake
workflow; treat the `.qpproj` and the scripts as the versioned
artifacts, not the slides.

## Code patterns

> QuPath automation is typically written in **Groovy** (the script
> language embedded in QuPath) and run from the *Automate* menu or
> the CLI. The snippets below show the typical scaffolding; check
> the QuPath documentation for the exact current API (methods
> sometimes shift between minor releases).

### Headless workflow run

```groovy
// QuPath script: run a previously-defined workflow across all
// images in the project. Verify the current entry-point in the
// QuPath API docs before deploying.
def project = getProject()
project.getImageList().each { entry ->
    setImageData(entry.readImageData())
    // run a saved workflow by name
    runWorkflow("TMA-gridded analysis")
    entry.saveImageData(getImageData())
}
```

### TMA grid scoring (per-core IHC H-score)

```groovy
// Sketch: walk TMA cores, request the H-score per core, collect
// a per-core table. Verify the exact helper-class names in the
// current QuPath release.
def tmaData = getProject().getTmaData()
def rows = []
tmaData.getTmaCores().each { core ->
    rows << [
        "core": core.getName(),
        "n":   core.getDetectionCount(),
        "H_score": core.getMetadataValue("H-score")
    ]
}
new File("tma_h_scores.csv").text = "core,n,H_score\n"
rows.each { r ->
    new File("tma_h_scores.csv").append("${r.core},${r.n},${r.H_score}\n")
}
```

### Pixel classifier (interactive)

```groovy
// Sketch: trigger the built-in pixel-classifier train & apply.
// The exact entry-points are in the QuPath Groovy API for 0.5.x —
// confirm the current method names before relying on this.
setPixelClassifier(pixelClass)
def classifier = getPixelClass()
classifier.trainClassifier()
classifier.applyClassifications(qupath.lib.objects.PathObject)
```

### StarDist extension from Groovy

```groovy
// Sketch: invoke the StarDist extension programmatically.
// Verify the exact builder class names in the current QuPath
// extension docs.
def stardist = StarDist2D.builder()
    .modelPath("/models/he_heavy_augment.pb")
    .threshold(0.5)
    .build()
stardist.detectObjects(imageData, pathObjects)
```

### Python integration

QuPath exposes a *Jupyter* / *QuPath Notebook* path (newer 0.5.x
releases) that lets you import a QuPath image into a Python
kernel, run cellpose or scimap on the cell masks, and write
results back to the QuPath project. Treat the notebook as a
reproducible record of the analysis.

## Common pitfalls

- **Annotation bias.** A pixel classifier learned on a single
  whole-slide-image (WSI) can generalize poorly to other scanners
  and staining batches. Train on at least 5-10 slides with the
  full range of variation; review the heatmap on held-out slides.
- **Color deconvolution mismatch.** "Estimate stain vectors" works
  on H&E only. For IHC (single DAB) or special stains, set the
  vectors manually — the wizard otherwise picks wrong ones.
- **Stardist model choice.** A model trained on H&E nuclei will
  fail on DAB IHC or fluorescence. Use the Cellpose extension
  with `cyto3`/`nuclei` for non-H&E; or train a custom StarDist
  on your own data with the QuPath StarDist command-line tools.
- **Channel confusion in mIHC.** Multi-channel imports sometimes
  load with the wrong colors. Always open the Brightness/Contrast
  panel and check that the DAPI channel is blue, etc.
- **TMAs: core mis-mapping.** If the dearrayer puts cores in the
  wrong well, the entire per-core table is wrong. Manually verify
  the grid alignment on a slide with a distinctive landmark.
- **Running out of RAM.** A full pixel classification on a 200k ×
  200k slide with fine features can take 32 GB+. Lower the
  resolution, mask to tissue, or run on a per-ROI basis.
- **QuPath vs QuPath-Extension version skew.** Extensions built
  for QuPath 0.4.x may not load on 0.5.x. Pin both QuPath and
  extension versions in your pipeline manifests.

## Validation

- **Visual review:** overlay the segmentation or pixel
  classification on the original slide at multiple locations
  and zoom levels. Always have a pathologist or domain expert
  sign off on the annotations.
- **Held-out slides:** keep at least one slide per batch
  *outside* the pixel-classifier training set. Report per-slide
  metrics (Dice, agreement, F1 against a small hand-labeled
  region set) — QuPath's pixel classifier can output a
  per-pixel probability map you can threshold and compare.
- **Object counts sanity:** cell counts per mm² should be in a
  biologically plausible range; if they double after a model
  change, you have a problem.
- **Re-run reproducibility:** re-applying the same workflow
  to the same `.qpproj` should produce identical (or
  numerically close, for stochastic classifiers) measurement
  tables. QuPath supports seeding where applicable.

## Open alternatives

- **CellProfiler** — better for plate-based screens; weaker for
  WSI; lacks the tile-streaming / region-aware model of QuPath.
- **ImageJ/Fiji** — best for exploratory, single-image
  fluorescence quantification; struggles at WSI scale.
- **HistomicsTK / WSInfer / PathML** — for purely Python pipeline
  integration and large-scale inference across slide libraries
  without a human-in-the-loop annotator.
- **QuPath + QuExtension ecosystem** — extensions for
  deep-learning cell typing (HistoQC, Stardist, Cellpose,
  InstanSeg), spatial omics (Pixie, Polaris), and IHC scoring
  (Positive Cell Detection).
- **Commercial:** Visiopharm, HALO (Indica Labs), Aperio
  ImageScope (Leica), Definiens (now part of Roche). All are
  powerful but proprietary and licensed per seat; QuPath is
  fully open (Apache 2.0) and unencumbered.

## References

- QuPath home: <https://qupath.github.io>
- QuPath documentation: <https://qupath.readthedocs.io>
- QuPath GitHub: <https://github.com/qupath/qupath>
- Bankhead et al. 2017, *Scientific Reports* — QuPath (DOI:
  10.1038/s41598-017-17204-5)
- StarDist extension: <https://github.com/qupath/qupath-extension-stardist>
- Cellpose extension:
  <https://github.com/yeexiangzhen/qupath-extension-cellpose>
- InstanSeg (deep-learning cell segmentation):
  <https://github.com/instanseg/instanseg>

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from
  the QuPath documentation set; consolidated 0.5.x extension
  install notes, TMA and multiplexed workflow pointers.