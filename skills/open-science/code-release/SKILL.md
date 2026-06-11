---


name: code-release
description: "Use when releasing research code: Zenodo-GitHub integration for a citable DOI, Citation File Format (CFF), containerization with Docker/Apptainer, conda lockfiles, and reproducibility badges for end-to-end reproducibility."
license: MIT
---

<!-- metadata:
category: open-science
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - open-science
  - research
difficulty: intermediate
-->




# Code Release

> Releasing research code well means making it citable, reproducible, and easy to use. This skill covers the canonical pipeline: a public Git repository, a tagged release, a DOI minted on Zenodo (or a JOSS publication), a `CITATION.cff` for human readers, a container image (Docker/Apptainer) and/or a conda lockfile for environment reproducibility, a Software Heritage archive for long-term preservation, and a documented test that a stranger can run. Each step addresses a different failure mode of "we will release the code when the paper is accepted," which usually means: never, badly, or in a way no one can run.

## When to use

- Tagging and **archiving a release** of a research code repository.
- Minting a **DOI** for a specific version of a code repository.
- Writing a **CITATION.cff** so users get the right citation when they cite the code.
- Creating a **Docker container** or **Apptainer (formerly Singularity) image** for an analysis environment.
- Pinning dependencies with a **conda lockfile** (`conda-lock`, `pixi`, or `pyproject.toml`).
- Preparing a **JOSS (Journal of Open Source Software)** submission.
- Earning a **reproducibility badge** from a journal (e.g., PLOS, eLife) or a conference (e.g., ML Reproducibility Challenge).
- Building a **reproducibility report** (an artifact with the paper).

## When NOT to use

- For **data release** (the data behind the code) — see `ors-open-science-fair-data`.
- For **licensing the code** — see `ors-open-science-licensing` (this skill defers to it).
- For **preprinting the paper** — see `ors-open-science-preprints`.
- For **production-grade software** that is not a research output — the rules are different (semantic versioning, changelogs, deprecation policies).
- For **internal lab code** that you do not intend to release — the discipline still applies if you want to reuse it in 2 years.

## Prerequisites

- A working code repository (git, on GitHub, GitLab, or Bitbucket).
- A clear license (default: MIT or Apache-2.0; see `ors-open-science-licensing`).
- A README with install + run instructions.
- Tests that pass (the code must work in a fresh environment).
- An ORCID iD for the maintainer.
- (Optional) Docker installed; (optional) Apptainer installed; (optional) conda/mamba/pixi.

## Core workflow

1. **Pick a license.** MIT, Apache-2.0, GPL — see `ors-open-science-licensing`. Add `LICENSE` to the root.
2. **Write a `CITATION.cff`.** Use the CFF schema; commit it to the repo.
3. **Tag a release.** `git tag -a v1.0.0 -m "Release for the 2025 paper"`; push the tag.
4. **Mint a DOI on Zenodo.** Connect GitHub repo to Zenodo; each release gets a Zenodo DOI. Record it in the paper.
5. **Pin the environment.**
   - **Python**: `pyproject.toml` + `pixi.lock` or `conda-lock.yml`; or a `requirements.txt` with hashes.
   - **R**: `renv.lock`.
   - **Julia**: `Manifest.toml` + `Project.toml`.
   - **Containers**: build a Docker image and push to Docker Hub or GHCR; mirror as an Apptainer `.sif` for HPC.
6. **Document the test.** A `reproduce.sh` (or `Makefile`) that goes from a fresh clone to the figure/result. The test should be runnable on a clean container.
7. **Add badges.** CI passing, license, DOI, version, coverage, JOSS status.
8. **Submit to JOSS or apply for a reproducibility badge** (optional).
9. **Archive to Software Heritage** (automatic for GitHub via the SWH plugin).

## Code and document patterns

### Pattern 1: A code-release checklist

```
- [ ] Public repository (GitHub, GitLab, Bitbucket, SourceHut, Codeberg)
- [ ] LICENSE file in root
- [ ] README with: title, description, install, usage, citation
- [ ] CITATION.cff (Citation File Format)
- [ ] Tag v1.0.0 (semantic version)
- [ ] GitHub release / Zenodo DOI minted
- [ ] Tests passing (CI green)
- [ ] Dependencies pinned (lockfile or hashes)
- [ ] Dockerfile OR Apptainer def file
- [ ] reproduce.sh or Makefile that runs the analysis end-to-end
- [ ] Badges in README
- [ ] Software Heritage archived
- [ ] DOI included in manuscript
- [ ] (Optional) JOSS submission
```

### Pattern 2: `CITATION.cff` example

```yaml
# This file is in the Citation File Format (CFF).
# See https://citation-file-format.github.io/
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
type: software
title: "scvi-batch-correction"
version: 1.0.0
date-released: 2026-03-15
license: MIT
url: "https://github.com/yourname/scvi-batch-correction"
repository-code: "https://github.com/yourname/scvi-batch-correction"
doi: 10.5281/zenodo.1234567
authors:
  - family-names: Jayaram
    given-names: Pradyumna
    orcid: https://orcid.org/0000-0000-0000-0000
  - family-names: Doe
    given-names: Jane
    orcid: https://orcid.org/0000-0000-0000-0001
keywords:
  - single-cell
  - batch-correction
  - variational-inference
  - scvi-tools
preferred-citation:
  type: article
  title: "A scvi-tools workflow for batch correction in single-cell RNA-seq"
  authors:
    - family-names: Jayaram
      given-names: Pradyumna
    - family-names: Doe
      given-names: Jane
  - family-names: Smith
    given-names: Bob
  journal: "Nature Methods"
  year: 2026
  volume: 23
  start: 100  # first page
  end: 115
  doi: 10.1038/s41592-026-00000-0
```

### Pattern 3: Dockerfile (lightweight Python analysis)

```dockerfile
FROM mambaorg/micromamba:1.5-jammy

# Set the working directory
WORKDIR /app

# Copy the lockfile and environment file FIRST (for cache efficiency)
COPY environment.yml /app/environment.yml
COPY pixi.lock /app/pixi.lock 2>/dev/null || true

# Install the conda environment
RUN micromamba env create -f /app/environment.yml && \
    micromamba clean --all --yes

# Activate the environment for subsequent commands
SHELL ["bash", "-lc"]
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Copy the source code
COPY . /app

# Make the reproduce script executable
RUN chmod +x /app/reproduce.sh

# Default command: run the reproduction
CMD ["/app/reproduce.sh"]
```

### Pattern 4: Apptainer definition (for HPC)

```apptainer
Bootstrap: docker
From: mambaorg/micromamba:1.5-jammy

%files
    environment.yml /opt/environment.yml
    . /app

%post
    micromamba env create -f /opt/environment.yml
    micromamba clean --all --yes
    chmod +x /app/reproduce.sh

%environment
    export MAMBA_DOCKERFILE_ACTIVATE=1
    export PATH="/opt/conda/envs/myenv/bin:$PATH"

%runscript
    exec /app/reproduce.sh "$@"

%labels
    Author Pradyumna Jayaram
    Version 1.0.0
```

Build with `apptainer build my-tool_v1.0.0.sif my-tool.def`.

### Pattern 5: `environment.yml` (with lockfile comment)

```yaml
name: scvi-batch
channels:
  - conda-forge
  - bioconda
  - pytorch
dependencies:
  - python=3.11
  - numpy=1.26
  - pandas=2.2
  - scikit-learn=1.4
  - pytorch::pytorch=2.2
  - scvi-tools=1.1
  - muon=0.1.5
  - jupyterlab=4.1
  - pip
  - pip:
    - "git+https://github.com/Yale-Sandbox/scvi-tools.git@main#egg=scvi-tools"
```

To pin: `conda-lock lock -f environment.yml -p linux-64 -p osx-64 -p osx-arm64`. This produces `conda-lock.yml` that downstream users can install from: `conda-lock install -n myenv conda-lock.yml`.

### Pattern 6: `reproduce.sh` (end-to-end test)

```bash
#!/usr/bin/env bash
# Reproduce all results for the manuscript.
# Tested on: Linux x86_64, macOS arm64, Apptainer 1.3
set -euo pipefail

echo "==> Downloading data"
python -m my_tool.download \
    --accession PRJNA123456 \
    --output data/raw/

echo "==> Preprocessing"
python -m my_tool.preprocess \
    --input data/raw/ \
    --output data/processed/

echo "==> Running the model"
python -m my_tool.train \
    --config configs/main.yaml \
    --output results/

echo "==> Generating figures"
python -m my_tool.plot \
    --results results/ \
    --output figures/

echo "==> Comparing to expected results"
python tests/check_results.py --tolerance 0.01

echo "Done. Figures in figures/, results in results/."
```

The corresponding `tests/check_results.py` is what proves end-to-end reproducibility. If the output of `reproduce.sh` matches the figures in the paper, the code is reproducible.

### Pattern 7: `reproduce-apptainer.sh` (HPC version)

```bash
#!/usr/bin/env bash
# Run the analysis inside an Apptainer container.
set -euo pipefail
APPTAINER_IMG="docker://ghcr.io/yourname/my-tool:v1.0.0"
apptainer run \
    --bind "$PWD:/work" \
    "$APPTAINER_IMG" \
    /work/reproduce.sh
```

### Pattern 8: Badges in README

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/yourname/my-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/my-tool/actions)
[![Coverage](https://codecov.io/gh/yourname/my-tool/branch/main/graph/badge.svg)](https://codecov.io/gh/yourname/my-tool)
[![Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/yourname/my-tool/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/yourname/my-tool)
[![JOSS](https://joss.theoj.org/papers/10.21105/joss.01234/status.svg)](https://joss.theoj.org/papers/10.21105/joss.01234)
```

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| **No license** | Code is not legally reusable | Add `LICENSE` (MIT, Apache-2.0, etc.). |
| **No DOI** | Code is citable but not citation-tracked | Mint a Zenodo DOI for each release tag. |
| **Dependencies unpinned** | "Works on my machine" → broken elsewhere | Use `conda-lock`, `pixi.lock`, `requirements.txt` with hashes. |
| **Data path hard-coded** | `reproduce.sh` fails on someone else's machine | Use relative paths, environment variables, or config files. |
| **Random seeds not set** | Results differ run-to-run | Set `np.random.seed(42)`, `torch.manual_seed(42)`, etc. |
| **GPU-required code on a CPU machine** | Reviewer cannot reproduce | Test on both GPU and CPU; fall back to a small-data demo. |
| **GPU-specific PyTorch build on CPU** | `libcudart.so: cannot open` | Provide a CPU-only `requirements-cpu.txt` or a Docker build arg. |
| **Secrets in the repo (API keys, tokens)** | Security breach; revoked and broken immediately | Use environment variables; check `gitleaks` / `trufflehog`. |
| **Generated outputs checked in** | Git blame is contaminated; reviewer sees stale data | Add `results/`, `data/`, `*.pkl` to `.gitignore`. |
| **Huge data files in git** | Repo bloats; clone is slow | Use Git LFS or external data storage (Zenodo, S3, Open Science Framework). |
| **Container image with no entrypoint** | User has to guess how to run it | Provide a `Dockerfile` ENTRYPOINT or a `reproduce.sh` runscript. |
| **DOI version doesn't match code** | Reviewer tries to reproduce a different version | Tag the release BEFORE the paper is published; use the tag's DOI in the paper. |
| **No test for the analysis** | A bug slips into the published code | Add a smoke test (smoke runs in <1 min, verifies the pipeline runs). |
| **README says "data available upon request"** | The reviewer cannot reproduce | Put the data on Zenodo and link it in the README. |
| **License mismatch with dependencies** | If a dependency is GPL, your MIT code may need to re-license | Run `pip-licenses` to check; re-license or replace as needed. |

## Validation

A code release is "good" when:

- [ ] A stranger can `git clone` the repository.
- [ ] A stranger can `pip install` (or `conda env create`) and get a working environment.
- [ ] A stranger can run `reproduce.sh` and get the same numbers / figures as the paper.
- [ ] The README has a DOI badge linking to the Zenodo record.
- [ ] The CITATION.cff yields a valid BibTeX entry via `cffconvert` (https://citation-file-format.github.io/cff-converter-python/).
- [ ] The container image builds in CI and is published to a registry.
- [ ] The Software Heritage archive has the version (check the SWH badge).
- [ ] The version of the code matches the version cited in the paper.

A simple reproducibility test:

```bash
# In a clean environment:
git clone https://github.com/yourname/my-tool
cd my-tool
git checkout v1.0.0
docker build -t my-tool:v1.0.0 .
docker run --rm -v "$PWD:/work" my-tool:v1.0.0 /work/reproduce.sh
diff -r results/ expected_results/  # should be empty (or small tolerance)
```

## Open alternatives

| Commercial / restricted | Open alternative | Trade-off |
|--------------------------|------------------|-----------|
| Docker Hub (private repos) | GitHub Container Registry (GHCR) | GHCR is free for public; Docker Hub has rate limits. |
| Docker Desktop (proprietary build) | Podman, Apptainer | Podman is daemonless; Apptainer is built for HPC. |
| Anaconda (commercial default channel) | conda-forge, mamba, micromamba, pixi | conda-forge is community-driven; pixi is Rust-based, fast. |
| PyPI (full Python) | conda-forge, BioConda | BioConda is biology-specific. |
| Travis CI (now limited free) | GitHub Actions, GitLab CI | GitHub Actions is free for public repos. |
| CodeOcean (commercial reproducibility platform) | Repo2Docker (Jupyter), SingularityHub, Renku | All open source; CodeOcean has nicer UX. |
| GitHub (Microsoft-owned) | GitLab, Codeberg, SourceHut | GitLab is fully open-source (community edition); Codeberg is non-profit. |
| ReadTheDocs (hosted) | mkdocs + GitHub Pages, Quarto | All open source; ReadTheDocs has nicer versioning. |

## References

- Zenodo GitHub integration: https://docs.zenodo.org/docs/integrations/github
- Zenodo help: https://help.zenodo.org/
- Citation File Format (CFF): https://citation-file-format.github.io/
- CFF converter (cffconvert, cff-init): https://citation-file-format.github.io/cff-converter-python/
- Open Container Initiative (OCI): https://opencontainers.org/
- Docker docs: https://docs.docker.com/
- Apptainer (formerly Singularity) docs: https://apptainer.org/documentation/
- conda-forge: https://conda-forge.org/
- conda-lock: https://github.com/conda/conda-lock
- pixi (Astral): https://pixi.sh/
- BioConda: https://bioconda.github.io/
- Software Heritage Archive: https://www.softwareheritage.org/
- Software Heritage GitHub integration: https://docs.softwareheritage.org/
- JOSS (Journal of Open Source Software): https://joss.theoj.org/
- JOSS reviewer checklist: https://joss.readthedocs.io/en/latest/review_checklist.html
- OCI image spec: https://github.com/opencontainers/image-spec
- Singularity user guide: https://docs.sylabs.io/guides/latest/user_guide/

## Related skills

- `ors-open-science-fair-data` — releasing the data behind the code.
- `ors-open-science-licensing` — picking a license for the code.
- `ors-open-science-preprints` — posting the manuscript that uses this code.
- `ors-data-engineering-snakemake-workflow-engine` / `ors-data-engineering-nextflow-workflow-engine` — workflow managers for reproducible pipelines.
- `ors-data-engineering-docker-singularity-containers` — deeper dive on containerization.
- `ors-data-engineering-conda-pixi-environments` — deeper dive on environments.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesised Zenodo GitHub integration; Citation File Format (CFF) Initiative; Open Container Initiative; Apptainer docs; conda-forge lockfile spec; Software Heritage; JOSS reviewer checklist. Code-release checklist, CITATION.cff template, Dockerfile, Apptainer def file, environment.yml, reproduce.sh, and end-to-end test protocol are original compositions.
