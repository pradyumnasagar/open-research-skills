# Open Research Skills — Taxonomy

Every `ors-*` skill belongs to exactly one top-level category. The category appears in the skill's frontmatter as `category:` and determines the folder it lives in.

## 1. **bioinformatics-sequence**
   Sequence manipulation, I/O, alignment, QC, variant calling, genome assembly/annotation, long-read, primer design, restriction analysis.

## 2. **bioinformatics-omics**
   RNA-seq (bulk + single-cell + spatial), ChIP-seq, ATAC-seq, CLIP-seq, methylomics, Hi-C, ribo-seq, m6A, proteomics, metabolomics, lipidomics, single-cell multi-omics.

## 3. **bioinformatics-functional**
   Pathway analysis, GSEA, GO/KEGG enrichment, gene regulatory networks, motif analysis, drug-target prioritization, immunoinformatics, neoantigen, TCR/BCR.

## 4. **bioinformatics-population**
   Population genetics, GWAS, eQTL, fine-mapping, Mendelian randomization, polygenic risk, ancestry, selection, linkage disequilibrium, phasing/imputation.

## 5. **bioinformatics-metagenomics**
   Shotgun metagenomics, 16S amplicon, viral discovery, AMR detection, functional profiling, microbiome diversity, eDNA.

## 6. **bioinformatics-clinical**
   ClinVar, gnomAD, COSMIC, pharmacogenomics, tumor mutation burden, MSI, HLA typing, ACMG classification, liquid biopsy, clinical reporting.

## 7. **bioinformatics-phylogenetics**
   Distance methods, ML/Bayesian tree inference, dating, reconciliation, HGT detection, pangenomes, synteny, orthology, selection scans.

## 8. **structural-biology**
   AlphaFold, Boltz, Chai, PDB, structure I/O, alignment, geometric analysis, modification, docking (Vina, DiffDock), MD (OpenMM, MDAnalysis, MDTraj).

## 9. **chemoinformatics**
   RDKit, molecular descriptors, similarity, substructure, virtual screening, ADMET, retrosynthesis, scaffold analysis, generative design, covalent design, PROTACs.

## 10. **scientific-computing**
   NumPy, SciPy, pandas, Polars, Dask, Vaex, Zarr, Xarray, parallel patterns, GPU compute, symbolic math, reproducibility, benchmarking.

## 11. **scientific-visualization**
   matplotlib, seaborn, plotly, ggplot2, scientific figure guides, multipanel, heatmaps, UMAP, Manhattan/QQ, circos, network, statistical annotation, color-blind palettes.

## 12. **scientific-writing**
   Manuscript drafting, IMRAD, abstracts (bilingual), peer review (journal-specific), R&R responses, citation management, AI-usage disclosure, plain-language summary, figure guides.

## 13. **literature-research**
   PubMed, bioRxiv, OpenAlex, Semantic Scholar, Google Scholar, citation graphs, hypothesis generation, critical reading, systematic reviews, meta-analysis.

## 14. **clinical-decision**
   Clinical reports, decision support, IRB/ethics, regulatory (FDA, EMA, ICMJE), CDISC, adaptive trial design, biostatistics for trials.

## 15. **lab-automation**
   Benchling, LabArchives, electronic lab notebooks, Opentrons/PyLabRobot, protocols.io, lab inventory, LIMS integration, robot calibration.

## 16. **data-engineering**
   SQL, DuckDB, Parquet, HDF5, Zarr, BioContainers, nf-core, Snakemake, Nextflow, CWL, WDL, workflow QC, data lakes, FAIR principles.

## 17. **machine-learning-bio**
   PyTorch, scikit-learn, scVI, BioNTech models, GNNs (torch-geometric), transformers for bio (ESM, ProtBERT), survival analysis, biomarker discovery, model interpretability (SHAP), Atlas mapping.

## 18. **omics-statistics**
   DESeq2, edgeR, limma, mixed models, batch correction, multiple testing, power analysis, survival (KM, Cox), longitudinal, Bayesian (PyMC, Stan), spatial statistics.

## 19. **medical-imaging**
   DICOM, pydicom, cellpose, napari, scikit-image, OpenCV, imageJ/Fiji (pyimagej), trackpy, IMC, spatial proteomics, segmentation, phenotyping.

## 20. **scientific-communication**
   Conference talks, posters, slides, grant writing, science Twitter, press releases, podcast prep, elevator pitch.

## 21. **open-science**
   Preprints, ORCID, data sharing (Zenodo, ENA, GEO), code sharing (GitHub, Zenodo), licensing, reproducibility, registered reports, preregistration.

## 22. **research-grants**
   NIH (R01, K, F), NSF, ERC, Wellcome, DARPA, foundation grants, specific aims, biographical sketch, letters of support, budget justification, resubmission strategy.

## 23. **mentorship-teaching**
   Lab notebook onboarding, reading groups, course design, syllabus writing, TA training, conflict resolution, mentee goal setting, inclusive mentoring.

## 24. **ethics-compliance**
   IRB protocols, informed consent, data privacy (HIPAA, GDPR), authorship disputes, conflicts of interest, image manipulation, AI in research (COPE, ICMJE).

## 25. **career-navigation**
   CV, tenure dossier, academic job market, industry transition, fellowship applications, mock interviews, negotiation, networking, science policy.

## 26. **systems-biology**
   COBRA, flux balance analysis, metabolic reconstruction, gene essentiality, GEMs, context-specific models, multi-omics integration (MOFA, mixOmics), model curation.

## 27. **comparative-genomics**
   Whole-genome alignment, synteny, orthology, pangenomes, gene family evolution, ancestral reconstruction, HGT detection, introgression, WGD, species delimitation.

## 28. **ecological-genomics**
   eDNA metabarcoding, biodiversity metrics, conservation genetics, landscape genomics, community ecology, population viability, species delimitation.

## 29. **epidemiological-genomics**
   Pathogen typing, variant surveillance, phylodynamics, transmission inference, AMR surveillance, outbreak pipelines, public health genomics.

## 30. **specialized-topics**
   Liquid biopsy, alternative splicing, epitranscriptomics, ribo-seq, small RNA, TCR/BCR, restriction enzyme, flow cytometry, IMC, eDNA, synthetic biology, biosensor design.

---

## Naming convention

`ors-<category-kebab>-<skill-slug>`

Examples:
- `ors-bioinformatics-sequence-pysam-genomics` (the pysam skill from sequence-io)
- `ors-bioinformatics-omics-scanpy-preprocessing` (single-cell preprocessing)
- `ors-scientific-writing-imrad-drafting` (research article drafting)
- `ors-omics-statistics-pymc-bayesian` (Bayesian stats for omics)

All folder names are lowercase, kebab-case, ASCII only. Folder name MUST match the frontmatter `name:` field exactly.

## Authoring rules

1. **No verbatim copying.** Every skill is rewritten in Pradyumna's voice. Code examples are kept structurally similar where the canonical pattern is well-established (e.g. `bwa mem | samtools sort`); prose and examples must be original or substantially transformed.
2. **Cite sources.** The `sources_consulted:` block lists every original source and what was changed.
3. **No hallucination.** Every tool, parameter, API, and reference must be something that exists in the public literature. When in doubt, link to the official docs rather than asserting behavior.
4. **Update for 2026.** Replace deprecated flags, point to current versions, mention modern alternatives (e.g. nf-core, BioContainers, scvi-tools 1.x, AlphaFold 3, Boltz-1, ChatGPT-5-era tools).
5. **Open alternatives required.** Any commercial tool must have an open-source substitute listed.
6. **Validation matters.** Every workflow skill must have a "How to know it worked" section.
