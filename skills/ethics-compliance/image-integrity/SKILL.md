---
name: image-integrity
description: "Use when preparing, reviewing, or auditing research images (Western\
  \ blots, gels, microscopy, EM, multi-panel figures) for submission — covers\
  \ manipulation detection by proofreader tools and human review, figure assembly\
  \ best practices, raw data retention, journal image-checking policies (e.g., Nature's\
  \ screening), RRIDs, and concrete examples of what gets flagged.
license: MIT
---

<!-- metadata:
category: ethics-compliance
version: 1.0.0
author: Pradyumna Jayaram
tags:
- image-integrity
- western-blot
- figure-prep
- research-integrity
- rrid
- microscopy
difficulty: intermediate
prerequisites:
  tools: []
  skills:
  - ors-scientific-visualization-multipanel-figures
sources: 'Original: Nature Editorial ''What constitutes image manipulation?'' and
  the Nature Portfolio image-screening policy; Adapted: screening policy and image-policy
  checklist; Original: Rossner & Yamada, ''What''s in a picture? The temptation of
  image manipulation'' (Journal of Cell Biology, 2004); Adapted: manipulation rules
  and figure-prep discipline; Original: ORI Guidelines for Scientific Images; Adapted:
  ''no specific feature may be enhanced, obscured, moved, removed, or introduced'';
  Original: SciForums / PubPeer image-screening reports; Adapted: case-pattern library
  of what gets flagged; Improvisions: toolchain (Proofreader, ImageJ, image-validator),
  RRID section, raw-data retention policy, worked example of an unflagged figure'
-->

# Research Image Integrity

> Image integrity is the discipline of producing research figures (Western blots, gels, microscopy, electron microscopy, multi-panel composites) that accurately represent the underlying data, with all adjustments disclosed, all features preserved, and all source files available. The default mode of image manipulation is innocent: a contrast is pushed so a band is visible, a crop is tightened so a panel is tight, a lane is moved to make a story. The default mode of detection is forensic: editorial screeners and post-publication reviewers now apply automated tools and visual inspection to every figure, and a flag can trigger a multi-year investigation. This skill encodes the journal policies (Nature's screening, Science's requirements, Cell's standards, ORI guidelines), the manipulation rules that apply universally, the figure-assembly best practices, the proofreader tools (and their limits), the raw-data retention policy, the RRID convention, and the concrete patterns that get flagged in 2025-2026.

## When to use

- Preparing Western blots, gels, microscopy, EM, or multi-panel figures for a manuscript or thesis.
- Reviewing a manuscript for image integrity before submission (self-audit, lab-internal review).
- Responding to an editor or reviewer request for original, unprocessed images.
- Responding to a post-publication image concern (PubPeer comment, institutional inquiry, journal investigation).
- Setting up a lab's image-acquisition, image-storage, and image-processing standards.
- Adding RRIDs (Research Resource IDs) to a methods section for cell lines, antibodies, model organisms, plasmids, and software.

## When NOT to use

- The question is statistical (p-values, error bars, sample size). Use `ors-omics-statistics-statistical-analysis`.
- The question is figure layout, color, or readability. Use `ors-scientific-visualization-multipanel-figures`.
- The question is authorship or contribution. Use `ors-ethics-compliance-ai-disclosure` and related skills.
- The question is whether an image is fabricated from no data. That is fabrication, a different and more severe category of misconduct. This skill assumes the data exist and the question is how to represent them honestly.

## Prerequisites

- The original, unprocessed image files (TIFF or the camera vendor's native format) for every blot, gel, and micrograph in the manuscript.
- The acquisition metadata: microscope settings, exposure times, gain, bit depth, objective, fluorophore filter sets, antibody lot numbers.
- Access to a proofreader tool (Proofreader in ImageJ, the publisher's in-house screener where available) and a quantitative analysis tool (ImageJ, FIJI, or commercial alternatives).
- For antibodies and cell lines, the RRID lookup at [scicrunch.org](https://scicrunch.org) (or the equivalent registry).
- Familiarity with the ORI guidelines on scientific images and the Nature Portfolio image-policy page.

## Core workflow

1. **Acquire and store the raw image.** The raw image (TIFF or vendor native) is the legal record. Store it with metadata. Do not process in place; produce a working copy. Many journals (Nature, Cell, EMBO) require the unprocessed image on request, with the option to refuse only with a documented reason.

2. **Process in linear, reversible steps.** Brightness, contrast, color balance, and pseudocolor must be applied as linear, reproducible functions on the full image, recorded in the methods, and applied to the control and experimental images identically. Local adjustments (a brush that brightens one band, a crop that hides a tear) are the most-flagged category.

3. **Assemble the figure honestly.** Three rules from Rossner & Yamada (2004) and the ORI guidelines:
   - **No specific feature may be enhanced, obscured, moved, removed, or introduced.**
   - **Adjustments must apply to the entire image and be disclosed.**
   - **Original, unprocessed images must be retained and available on request.**

4. **For Western blots and gels, do not splice lanes without disclosure.** A clean white gap between non-adjacent lanes is a flag. Either run all relevant lanes adjacent in the same gel, or disclose the splice with a black line and a figure-caption note. Background-cleaning tools (e.g., the rubber-band tool in Photoshop) must apply to the entire lane, not to a region of interest.

5. **For microscopy, avoid over-processing.** Deconvolution, denoising, and background subtraction are standard but must be applied to all images identically. Sharpening that creates apparent structures (e.g., a band of speckle) is a flag. Channel bleed-through that suggests co-localization is a flag.
"
6. **For EM, retain the original negatives or the digital equivalent.** EM image processing has a long history of disputes over the line between "enhancement" and "fabrication." The rule: the original must be available, and any processing must be disclosed.

7. **Add RRIDs to the methods.** An RRID is a persistent identifier for a research resource (cell line, antibody, model organism, plasmid, software tool, database). Cell lines misidentified by mis-purchase are a common cause of retraction; the RRID links the manuscript to the authentic stock. Add RRIDs at first mention in the methods; the format is "RRID:AB_2532109" for antibodies, "RRID:CVCL_0022" for cell lines, and so on.

8. **Self-audit with a proofreader tool.** Run the figure through ImageJ's Proofreader plugin (or the in-house screener provided by the journal during submission) and visually inspect for: duplicated bands or regions, spliced lanes, asymmetric contrast, patches of cloned background, brightness/contrast differences between panels that were "treated the same way."

9. **Disclose adjustments in the methods or figure legend.** "Images were brightness/contrast-adjusted linearly and identically across the entire image in Adobe Photoshop; no regional adjustments were made." "Figure X lanes 3-5 are from the same gel as lanes 1-2; the lane rearrangement is disclosed with a black vertical line."

10. **On submission, expect a request for raw data.** Most publishers (Nature, Cell, eLife) will ask for original images at revision or at acceptance. Have the TIFFs and the metadata in a folder, not a deep drive.

11. **On post-publication concern, take it seriously.** A PubPeer comment or a reader email is not a complaint — it is a request for the underlying record. Respond with the original image, the metadata, and a description of the processing. Most concerns are clarified in one round; a small minority become investigations.

## Code patterns

This skill is documentation-heavy. The patterns below are the canonical figure-prep, image-audit, and disclosure structures, plus a small ImageJ / Python workflow for self-audit.

### Pattern 1 — Western blot processing and assembly (best practice)

```
Raw TIFF
  -> Linear brightness/contrast adjustment (recorded; same for all lanes)
  -> Crop to lanes of interest (no deletion of lanes without disclosure)
  -> Lane rearrangement (only if necessary; black vertical line + caption note)
  -> Background subtraction (applied to entire image, not region of interest)
  -> Annotation (molecular weight markers, sample labels)
  -> Export at 300 dpi for figure assembly

Never:
  - Use the rubber-band / dodge / burn tools to clean a band
  - Apply a Gaussian blur to "smooth" a noisy band
  - Increase contrast asymmetrically between control and experimental
  - Re-use a band from a previous experiment without disclosure
```

### Pattern 2 — Microscopy processing (best practice)

```
Raw TIFF (multi-channel if applicable)
  -> Background subtraction (rolling ball, identical radius for all images)
  -> Deconvolution (identical kernel, identical iterations)
  -> Linear brightness/contrast (identical for all images in the figure)
  -> Pseudocolor (channel assignments, look-up tables; do not change mid-figure)
  -> Cropping (identical orientation and zoom; disclosure if different fields are shown)
  -> Scale bar (added at this step; never re-scaled)
  -> Export at 300 dpi

Never:
  - Apply sharpening that creates speckle
  - Adjust channel intensities asymmetrically
  - Combine channels that are not from the same acquisition
```

### Pattern 3 — ImageJ self-audit (Proofreader plugin)

```
1. Open the original TIFF.
2. Plugins > Proofreader (from the BioVoxxel update site).
3. The plugin highlights potential duplications and inconsistencies.
4. Visual inspection: look for:
   - Repeating pixel patterns across distant regions
   - Asymmetric brightness/contrast between adjacent panels
   - Region-specific smoothing or sharpening
   - Duplicated bands in Western blots
5. Document the audit and the response in the lab notebook.
```

### Pattern 4 — Python forensic check (basic duplication)

The pattern below is a starting point for an automated duplication check; it is not a substitute for visual inspection.

```python
import hashlib
import numpy as np
from PIL import Image

def perceptual_hash(region, hash_size=8):
    """A simple average-hash for detecting near-duplicate regions."""
    g = region.convert("L").resize((hash_size, hash_size))
    arr = np.asarray(g, dtype=np.float32)
    avg = arr.mean()
    return (arr > avg).flatten()

def find_duplicate_patches(img_path, patch=64, stride=32, hamming_threshold=5):
    """Sliding-window patch comparison; flags near-duplicate regions."""
    img = Image.open(img_path).convert("L")
    w, h = img.size
    hashes = []
    coords = []
    for y in range(0, h - patch, stride):
        for x in range(0, w - patch, stride):
            box = (x, y, x + patch, y + patch)
            hashes.append(perceptual_hash(img.crop(box)))
            coords.append(box)
    flags = []
    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            # only flag patches that are not trivially adjacent
            if abs(coords[i][0] - coords[j][0]) < patch and abs(coords[i][1] - coords[j][1]) < patch:
                continue
            xor = np.bitwise_xor(hashes[i].astype(np.uint8),
                                  hashes[j].astype(np.uint8))
            if int(xor.sum()) <= hamming_threshold:
                flags.append((coords[i], coords[j]))
    return flags
```

A more rigorous audit uses a structural-similarity index (SSIM) over sliding windows, but the perceptual-hash pattern is enough to catch the common "I cloned a piece of background" error.

### Pattern 5 — Image disclosure text in Methods

> "Western blots were developed using ECL substrate (vendor, catalog) and imaged on a [system]. Raw TIFFs of all blots are available on request. Images were brightness- and contrast-adjusted linearly in [software, version] using the same settings for all lanes in a panel; no regional adjustments were made. Lanes 3 and 4 of Figure 2B are from the same gel as lanes 1 and 2; the non-adjacent lanes are indicated by a black vertical line. Loading controls (GAPDH, β-actin) are from the same membrane as the target protein."

### Pattern 6 — RRID block in Methods

> "Cell lines: HEK293T (RRID:CVCL_0063), HeLa (RRID:CVCL_0030). Authentication by STR profiling (date). Mycoplasma testing: negative (date).
> Antibodies: anti-METTL3 (vendor, catalog, RRID:AB_2853113), anti-GAPDH (vendor, catalog, RRID:AB_2533119)."

The RRID is obtained from the SciCrunch resolver at [scicrunch.org](https://scicrunch.org/resources). For software, the RRID points to a [SciCrunch software entry](https://scicrunch.org/resources/software) or the [bio.tools](https://bio.tools) registry.

### Pattern 7 — Raw data retention policy (lab)

```
- All raw images (TIFF / vendor native) stored on a lab NAS with
  daily offsite backup.
- Naming: YYYYMMDD_initials_experiment_blotNN.tif
- Subfolder: raw/ for acquisition, processed/ for working copies,
  figures/ for submission-ready.
- Retention: minimum 10 years after publication (funder requirement),
  with the option to extend for clinical or regulated studies.
- On publication, a copy of the raw data is deposited in a public
  repository (Zenodo, Figshare, or domain-specific) with a DOI.
```

## Common pitfalls

- **Spliced lanes without disclosure.** A black or white gap between non-adjacent lanes in a Western blot is the most-flagged image feature. Either run adjacent lanes in the same gel, or add a black line and disclose the splice.
- **Rubber-band / clone-stamp background cleaning.** The Photoshop "rubber-band" tool (or any "remove blemishes" function) on a band or a background is treated as manipulation. Background subtraction that applies to the entire image is fine; region-specific cleanup is not.
- **Asymmetric brightness/contrast.** A control panel and an experimental panel that have been processed with different settings to make the experimental band look "stronger" is the classic duplicate-publication figure. Apply identical settings to the entire panel.
- **Duplicated bands reused across figures.** A band from Figure 1 re-used in Figure 3 as if it were a different sample is a flag. Disclose when a band is re-used.
- **Pseudocolor choices that exaggerate.** A rainbow LUT on a low-dynamic-range image creates apparent structure that does not exist. Use a perceptually uniform LUT (viridis, magma) and disclose the LUT.
- **Spliced microscopy tiles stitched with different exposures.** A tiled microscopy image where each tile has been exposure-matched individually is acceptable if disclosed; if not disclosed, it is flagged.
- **Sharpen / denoise that creates speckle.** A denoising filter that creates apparent puncta is a flag. Use the same denoising settings for all images in a panel and disclose the kernel.
- **Scale bar wrong or missing.** A scale bar that does not match the pixel size is treated as scientific misconduct, not just sloppiness. Calibrate against a stage micrometer or a known reference.
- **Cell-line misidentification.** HeLa mis-labeled as HEK293, or vice versa, is a leading cause of retraction. Authenticate by STR profiling; add the RRID; report the date of authentication.
- **No RRID for an antibody or cell line.** Many journals now require RRIDs at first mention. Missing RRIDs are an easy desk-reject and a flag for post-publication screening.
- **Original images not available on request.** Refusing to provide original images, or providing cropped/processed versions, escalates a concern from editorial to misconduct.
- **Image used in two papers without disclosure.** A figure from a published paper re-used in a review or in a follow-up paper is a copyright and a publication-ethics issue. The standard remedy is disclosure and permission.
- **AI-edited images not disclosed.** Generative-AI editing of an image (background removal, denoising, sharpening) is treated as image manipulation if not disclosed. See `ors-ethics-compliance-ai-disclosure`.
- **Fabricated images.** Western blots with no underlying experiment are fabrication, the most severe category. The reviewer-tool landscape is improving at catching these.

## Validation

- The figure file (TIFF) at submission has a documented processing history in the lab notebook.
- All raw images are stored with metadata and are accessible to the journal on request.
- All band/region adjustments are applied to the full image, not a region of interest.
- All spliced lanes are disclosed with a black line and a caption note.
- All cell lines and antibodies have an RRID, and the cell line is authenticated.
- The figure passes the Proofreader plugin and a visual inspection by a second lab member.
- The methods section contains a disclosure paragraph describing the image processing.
- The raw data is deposited in a public repository with a DOI at publication.
- The image has not been published in a previous paper (or the re-use is disclosed with permission).

## Open alternatives

- **Proofreader plugin** (ImageJ / FIJI, open-source): BioVoxxel update site, free.
- **Forensic image analysis**: open tools are catching up to the proprietary screeners used by publishers; the journal's in-house screener is generally stricter.
- **Image storage**: institutional NAS with offsite backup; Zenodo or Figshare for public deposit.
- **STR profiling for cell-line authentication**: ATCC's STR profiling service is commercial; many institutional cores offer it for free.
- **RRID lookup**: [scicrunch.org](https://scicrunch.org/resources) and the [BioGRID RRID portal](https://scicrunch.org/resources).
- **Antibody validation**: [CiteAb](https://www.citeab.com) for citations per antibody, the [Antibodypedia](https://www.antibodypedia.com) registry, and the International Working Group for Antibody Validation (IWGAV) recommendations.

## References

- Rossner, M. & Yamada, K. M. "What's in a picture? The temptation of image manipulation." *Journal of Cell Biology* 166, 11-15 (2004).
- ORI Guidelines for Scientific Images — "no specific feature may be enhanced, obscured, moved, removed, or introduced."
- Nature Portfolio Image Policy and editorial "What constitutes image manipulation?" — screening and disclosure.
- Science / AAAS figure-prep and image-manipulation policy.
- Cell Press figure-prep guidelines.
- [SciCrunch RRID portal](https://scicrunch.org/resources) — RRID lookup.
- [BioGRID](https://thebiogrid.org) — RRID resolver and resource registry.
- Related skills: `ors-scientific-visualization-multipanel-figures` (figure layout and color), `ors-ethics-compliance-ai-disclosure` (AI-edited images), `ors-omics-statistics-statistical-analysis` (data behind the figure).

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesized from the ORI Guidelines for Scientific Images, the Nature Portfolio image-screening policy, the Rossner & Yamada (2004) manipulation rules, the SciCrunch RRID portal, and the standard proofreader-tool landscape. The Python forensic-check pattern and the worked example are original.