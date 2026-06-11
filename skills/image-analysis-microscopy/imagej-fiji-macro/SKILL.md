---

name: imagej-fiji-macro
description: "Record, write, and run ImageJ/Fiji macros for batch processing, ROI handling, intensity measurement, colocalization, time-lapse, FRET, and plugin installation in life-sciences microscopy."
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

# ImageJ / Fiji Macro Language for Bioimage Analysis

> ImageJ and its batteries-included distribution **Fiji** (Fiji Is Just
> ImageJ) have been the swiss-army knife of bioimage analysis for over
> 25 years. The macro language is a small, JavaScript-derived syntax
> that biologists can record by clicking through the GUI and then
> generalize into batch scripts. Use it for quick measurements on
> dozens to thousands of images, ROI handling, intensity and shape
> quantification, colocalization, time-lapse, and FRET — anything
> where a single workstation and a reproducible script are enough. For
> production pipelines, macros can be wrapped in a Java/Python bridge
> (e.g. `pyimagej`).

## When to use
"
- Recording an analysis by clicking through the GUI ("Plugins →
  Macros → Record") and then generalizing the macro to a folder of
  images.
- Batch processing: apply the same segmentation, measurement, or
  transformation to every `.tif` in a directory tree.
- ROI handling: drawing, importing, transferring, combining, and
  measuring regions of interest across images or stacks.
- Intensity measurement (mean, integrated, max) over ROIs or whole
  images; ratiometric FRET calculations; time-lapse intensity
  tracking.
- Colocalization (Pearson, Manders, ICQ, Li's approach) on
  two-channel images — see the coloc-2 plugin in Fiji.
- Stitching tile scans, Z-projecting stacks, 4D viewing and
  quantification.
- Installing community plugins (TrackMate, Stardist, BioVoxxel
  Toolbox, MorphoLibJ) via the Fiji Updater.

## When NOT to use

- High-content screening (HCS) of multi-well plates with plate
  metadata — use CellProfiler
  (`ors-image-analysis-microscopy-cellprofiler-pipelines`).
- Whole-slide histopathology — use QuPath
  (`ors-image-analysis-microscopy-qupath-pathology`).
- Pure deep-learning segmentation training — use cellpose,
  StarDist, or nnU-Net, then consume the masks in ImageJ/Fiji for
  measurement.
- Very large 3D / 4D volumes where the JVM memory model is
  limiting — use napari + Dask/zarr.
- Heavy numeric / statistical pipelines — ImageJ's built-in
  statistics are limited; for mixed-effects models, n = cells vs
  n = images vs n = animals, and other niceties, export to R or
  Python (see
  `ors-image-analysis-microscopy-image-analysis-best-practices`).

## Prerequisites

- **Fiji** (the easiest install) — a self-contained bundle of ImageJ
  with pre-installed plugins, from <https://fiji.sc>. Use the
  *ImageJ2* (Fiji 2.x) line for current macro syntax.
- For **headless** / scripted runs: **Java 11+** (Fiji ships its
  own JRE on most platforms; for server / Docker usage, ensure the
  same JVM is on the PATH).
- For Python bridges: `pyimagej` (the official Python wrapper).
- Some plugins require a particular Java version or a Caffe / TF /
  PyTorch runtime; check the plugin's installation page.

## Core workflow

1. **Install Fiji and any plugins.** Start Fiji, then *Help →
   Update…* to bring everything to the latest version. *Manage
   update sites* to add specialty sites (e.g. Stardist, BioVoxxel,
   MorphoLibJ, IJPB-plugins).
2. **Record a macro on a single image.** *Plugins → Macros →
   Record.* Click through the analysis you want to automate. Stop
   the recorder, copy the recorded commands into a new `.ijm` file.
3. **Refactor to a batch script.** Replace hard-coded file names
   with `getDirectory` + a list loop, replace magic numbers with
   `setOption` calls at the top, and add a `setBatchMode(true)` call
   to suppress image display for large jobs.
4. **Choose the run mode.**
   - *Interactive:* *Plugins → Macros → Run* on the `.ijm` file.
   - *Headless:* `ImageJ-linux64 --headless --run script.ijm
     "arg1,arg2"` (verify the exact binary name and `--run` syntax
     in the Fiji docs for your platform).
   - *From Python:* `pyimagej` initializes a JVM and dispatches
     macros / scripts.
5. **Validate on a small batch first.** Run on 3-5 images, open the
   results table, eyeball the segmentations / overlays, *then*
   point at the full directory.
6. **Version control the macro.** Save the `.ijm` in a git repo
   alongside the README, the test data, and the expected output
   table or image.

### Macro anatomy

- **Variables:** `n = 10;` (untyped, but `var n = 10;` is preferred
  in modern ImageJ2 macro syntax).
- **Strings:** use `d2s(value, decimals)` to convert numbers to
  strings; concatenate with `+`.
- **Arrays:** `list = newArray(10, 20, 30);`.
- **Loops:** `for (i = 0; i < n; i++) { ... }` and
  `list = getFileList(dir);`.
- **Built-in functions:** `getDirectory`, `listFiles`, `open`,
  `run`, `getNumber`, `setBatchMode`, `getTitle`, `selectWindow`,
  `close`, `roiManager`.
- **Plugins:** `run("Coloc 2", "channel1=1 channel2=2 ...")` — the
  string form depends on the plugin and is documented in each
  plugin's macro-recording output.

## Code patterns

> All code blocks below are written for the current Fiji / ImageJ2
> macro syntax. Verify the exact macro function names and plugin
  argument strings in the Fiji and ImageJ.net documentation before
  deploying — the macro language is stable but plugin-specific
  argument strings can shift between releases.

### Template: measure intensity in ROIs

```javascript
// Template: open a folder, draw ROIs, measure per-ROI intensity.
// Adjust getDirectory prompt to your platform conventions.
dir = getDirectory("Choose folder of images");
list = getFileList(dir);

setBatchMode(true);
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".tif")) {
        open(dir + list[i]);
        // expect the user to draw ROIs in the ROI Manager
        // ... or load ROIs from a directory:
        // roiManager("Open", dir + "RoiSet_" + list[i] + ".zip");
        n = roiManager("count");
        for (r = 0; r < n; r++) {
            roiManager("select", r);
            meanInt = getValue("Mean");
            area    = getValue("Area");
            print(list[i] + ",ROI" + r + "," + meanInt + "," + area);
        }
        close();
    }
}
setBatchMode(false);
```

### Colocalization (Coloc 2)

```javascript
run("Coloc 2",
    "channel_1=1 channel_2=2 " +
    "roi_or_mask=[<none>] " +
    "threshold_regression=Costes " +
    "show_save_diag=false " +
    "display_each_image=false " +
    "display_histogram_2d=false " +
    "display_scatterplot=false");
```

The output log contains Pearson's R, Manders M1/M2, and ICQ.
**Verify the exact argument names** in the current Coloc 2
documentation — they have evolved between versions.

### Z-projection

```javascript
run("Z Project...",
    "projection=[Average Intensity] " +
    "projection=[Max Intensity]");
```

### Time-lapse intensity tracking (single ROI)

```javascript
// After opening a hyperstack with T frames, draw one ROI in the
// ROI Manager, then:
n_frames = nSlices; // for a 2D time series
x = newArray(n_frames);
y = newArray(n_frames);
for (t = 0; t < n_frames; t++) {
    setSlice(t + 1);
    roiManager("select", 0);
    x[t] = t;
    y[t] = getValue("Mean");
}
Plot.create("Intensity vs Time", "Time", "Mean", x, y);
```

### FRET — ratiometric

```javascript
// For a standard sensitized-emission FRET setup with donor, FRET,
// and acceptor channels; verify the exact FRET calculator you use
// (e.g. the FRETratiometric plugin, or the BioVoxxel Toolbox).
run("FRET Ratiometric (FRETratio) ...");
```

### FRET — acceptor photobleaching

```javascript
// Sketch: average acceptor and donor intensity before/after
// bleaching in a stack. Verify the plugin and the exact argument
// string in the current Bio-Formats / FRET documentation.
```

### Headless run

```bash
# Linux / macOS
$FIJI_HOME/ImageJ-linux64 --headless --run /path/to/script.ijm
```

The `--run` argument passes any further text to the macro's
`getArgument()` function. Always read it with
`args = split(getArgument(), ",")` to handle multi-argument
dispatch.

### Python bridge (`pyimagej`)

```python
import imagej

ij = imagej.init("/opt/fiji")  # path to your Fiji install
macro = """
#@ String path
open(path);
print("Opened: " + getTitle());
"""
ij.py.run_macro(macro, {"path": "/data/sample.tif"})
```

## Common pitfalls

- **Macro recorded on a different plugin version.** Argument
  strings like `"channel_1=1 channel_2=2"` are not guaranteed
  stable across plugin updates. Re-record after upgrades or
  pin the plugin version.
- **Pixel size not set.** A macro that measures diameters in
  pixels will silently lie. *Image → Properties…* to set the
  calibration, or set it programmatically with
  `run("Properties...", ...)` at the top of the script.
- **Filenames with spaces / unicode.** Wrap paths in quotes and
  prefer cross-platform path conventions.
- **Forgetting `setBatchMode(true)` for big batches.** Without
  it, Fiji will open and redraw each image and be 10-100x
  slower.
- **Not closing windows.** Memory leaks accumulate. `close();`
  after every iteration, or use
  `run("Close All")` periodically.
- **Stack vs hyperstack confusion.** A 4D dataset can be a
  stack (XYT), a hyperstack (XYCZT), or a folder of files
  (`virtual stack`). Confirm with
  `getImageInfo()` / `getDimensions(...)` before looping.
- **Misinterpreting "Results" table.** ImageJ's "Results" table
  is process-global — multiple macros running in sequence can
  clobber each other. Use a *Custom* table or export to a
  CSV/TSV per run.
- **ROI coordinate space drift.** A ROI saved in one image will
  not apply correctly to a different-resolution image. Use
  ROIs in calibrated units or scale at load time.

## Validation

- **Visual:** `roiManager("Show All")` overlays every saved ROI
  on the source image. Confirm none went off-frame after a
  transformation (e.g. rotation, registration).
- **Numerical:** compare positive vs negative control means per
  measurement. For colocalization, Pearson R ≈ 0.95 on a
  perfect colocalization control and ≈ 0 on segregated
  channels. Reasonable positive-control values are required to
  trust the negatives.
- **Reproducibility:** a re-run of the macro on the same input
  must produce byte-identical output tables (modulo any
  random-number-using step — seed where possible).
- **Unit tests with synthetic data:** construct a small TIFF
  with known properties (e.g. 5 circles, intensity 200, area
  πr²) and assert the macro recovers them.

## Open alternatives

- **CellProfiler** — preferred for plate-based HCS with
  per-image metadata and a graphical pipeline.
- **QuPath** — preferred for whole-slide histopathology.
- **napari + scikit-image** — preferred for 3D / 4D interactive
  visualization and Python-native pipelines.
- **FIJI-as-a-Service / `pyimagej`** — if your team standardizes
  on Python, drive Fiji from a Jupyter notebook.
- **Commercial:** MetaMorph (Molecular Devices), NIS-Elements
  (Nikon), ZEN (Zeiss), LAS X (Leica). Powerful but vendor-
  locked; Fiji is the open benchmark.

## References

- Fiji home: <https://fiji.sc>
- ImageJ documentation: <https://imagej.net/docs>
- Macro reference: <https://imagej.net/developer/macro/functions.html>
- Headless / scripting FAQ: <https://imagej.net/scripting>
- Coloc 2: <https://imagej.net/plugins/coloc-2>
- TrackMate: <https://imagej.net/plugins/trackmate>
- pyimagej: <https://github.com/imagej/pyimagej>
- Stuurman, N. et al. 2005, "ImageJ and ImageJ2" — see
  <https://imagej.net/pubs>

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from
  the ImageJ.net and Fiji documentation sets; consolidated
  headless and pyimagej pointers; updated plugin-install path
  to the modern Fiji Updater.