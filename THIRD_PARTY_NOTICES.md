# Third-Party Notices

This document lists attribution notices for third-party software and content that informed the open-research-skills (ORS) project.

## License of this project

The open-research-skills project (this repository, all `SKILL.md` files, all docs, all scripts) is licensed under the MIT License. See `LICENSE` in the repo root.

The following upstream sources were studied, referenced, or adapted when authoring the skills in this repo. **No content was copied verbatim from any source.** All prose is original; all code patterns that appear standard (e.g. `bwa mem | samtools sort`) are documented as canonical workflows in the upstream tools' official documentation.

---

## Upstream skill sources (in rough order of contribution)

### 1. bioSkills (https://github.com/GPTomics/bioSkills)

- **License:** MIT
- **Contribution to ORS:** The structure and naming of the `bioinformatics-sequence/` category (23 skills covering sequence I/O, alignment, QC, statistics) was adapted from bioSkills' `sequence-io`, `sequence-alignment`, and `sequence-qc` subdirectories. Code patterns for samtools, bcftools, and pysam workflows were cross-referenced with bioSkills' implementation. All prose is rewritten.
- **Skills derived in part:** All 23 `bioinformatics-sequence` skills.

### 2. SciAgent-Skills (https://github.com/Prof-Luis-Casanova/SciAgent-Skills)

- **License:** Apache 2.0
- **Contribution to ORS:** Inspired the agent-friendly structure (frontmatter + body, validation steps, "When to use" sections) used throughout ORS. Some skill structure (e.g. `research-grants` organization) follows the SciAgent pattern of breaking a complex workflow into multiple narrow skills rather than one wide skill.
- **Skills derived in part:** Most categories, but lightly.

### 3. academic-research-skills (https://github.com/jlgingold/academic-research-skills)

- **License:** CC BY-NC 4.0
- **Contribution to ORS:** The `scientific-writing/`, `peer-review/`, and `career-navigation/` categories were inspired by the topical scope of this source. No prose was adapted (different license, NC clause).
- **Skills derived in part:** None directly. Topical coverage only.

### 4. scientific-agent-skills (https://github.com/K-Dense-AI/scientific-agent-skills)

- **License:** Apache 2.0
- **Contribution to ORS:** The categories `scientific-thinking/`, `scientific-visualization/`, `humanizer-skills/`, and `literature-research/` were directly inspired by this source. Some prompts and workflow patterns were cross-referenced; all prose is rewritten.
- **Skills derived in part:** The 4 skills in `scientific-thinking/`, 5 in `scientific-visualization/`, 4 in `humanizer-skills/`, 5 in `literature-research/`.

### 5. academic-research-skills-codex (https://github.com/microsoft/academic-research-skills-codex)

- **License:** MIT
- **Contribution to ORS:** The structure of the `ethics-compliance/` and `open-science/` categories was informed by this source. Some coverage overlaps with `scientific-writing/ai-disclosure-writing`.
- **Skills derived in part:** Light topical coverage.

---

## Public frameworks referenced in skills

The following public frameworks and standards are referenced in the body of ORS skills. ORS links to their official documentation and summarizes the standard in its own words. No content is copied verbatim from any of these.

| Framework / Standard | Skills that reference it | URL |
|---|---|---|
| FAIR Principles (Wilkinson et al., 2016) | `open-science/fair-data-principles` | https://www.go-fair.org/fair-principles/ |
| PRISMA 2020 Statement | `literature-research/systematic-review` | https://www.prisma-statement.org/ |
| ICMJE Recommendations | `scientific-writing/manuscript-structure` | https://www.icmje.org/ |
| ARRIVE 2.0 Guidelines | `ethics-compliance/animal-research-protocol` | https://arriveguidelines.org/ |
| CONSORT 2010 Statement | `ethics-compliance/clinical-trial-protocol` | http://www.consort-statement.org/ |
| NIH Grants Policy Statement | `research-grants/nih-r01-specific-aims` | https://grants.nih.gov/policy/ |
| NSF Proposal & Award Policies & Procedures Guide (PAPPG) | `research-grants/nsf-standard-grant` | https://www.nsf.gov/publications/pub_summ.jsp?ods_key=pappg |
| ERC Work Programme | `research-grants/erc-advanced-grant` | https://erc.europa.eu/ |
| ICH-GCP E6(R2) | `ethics-compliance/clinical-trial-protocol` | https://database.ich.org/ |
| HARKing, p-hacking discussions | `scientific-thinking/hypothesis-generation` | Various primary sources |
| BLAST suite documentation | `bioinformatics-sequence/blast-search` | https://blast.ncbi.nlm.nih.gov/ |
| samtools documentation | `bioinformatics-sequence/sam-bam-basics` | http://www.htslib.org/ |
| BWA manual | `bioinformatics-sequence/bwa-alignment` | http://bio-bwa.sourceforge.net/ |
| RDKit documentation | `chemoinformatics/*` | https://www.rdkit.org/docs/ |
| NIH BIRCBI Bioinformatics training | `bioinformatics-sequence/*` | https://bioinformatics.niaid.nih.gov/ |

---

## Fonts and other visual assets

ORS is text-only. No fonts, images, or other binary assets are bundled.

---

## Acknowledgments

Thanks to the open-source bioinformatics, chemistry, and open-science communities whose primary documentation makes skills like these possible. The ORS author is a beneficiary of the FAIR principle: Findable, Accessible, Interoperable, Reusable.

If you believe an ORS skill infringes your copyright or attribution, please open an issue. We will respond within 7 days.
