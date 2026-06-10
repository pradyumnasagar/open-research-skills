---
name: ors-data-engineering-snakemake-workflow-engine
display_name: "Snakemake Workflow Engine"
description: "Python-based workflow manager for reproducible, scalable pipelines. Define rules with file-based dependencies; Snakemake resolves execution order and parallelism. Runs local, SLURM, LSF, AWS, GCP via profiles; per-rule conda/Singularity envs. For NGS pipelines, ML training, and multi-step file processing. Use Nextflow for Groovy dataflow or nf-core integration."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: data-engineering
tags: [snakemake, workflow, pipeline, hpc, reproducibility]
difficulty: intermediate
prerequisites:
  tools: [snakemake>=8, graphviz, conda]
  skills: []
sources_consulted:
  - "Original: snakemake-workflow-engine (SciAgent-Skills-main/scientific-computing/snakemake-workflow-engine); Adapted: trimmed verbose examples, added 2026 SLURM profile guidance, added nf-core / Nextflow disambiguation, added modern container options (Apptainer vs Singularity, pixi support)."
  - "Improvisions: rewrote for data-engineering category audience — emphasised data pipeline patterns (Parquet/Zarr/HDF5 outputs), DVC integration, FAIR output handling, added `module` workflow composition."
last_updated: 2026-06-10
---

# Snakemake Workflow Engine

> Snakemake treats pipeline steps as **rules with file-based dependencies** and resolves the execution DAG backward from your requested outputs. The same Snakefile runs on a laptop, an HPC cluster, or a cloud VM — you only swap a profile. This is the workhorse for reproducible data-engineering pipelines in research computing, especially when every step needs to be re-runnable, citable, and tied to a specific tool version.

## When to use

- Building reproducible multi-step data pipelines (FASTQ → BAM → variants → annotation).
- Scaling the same workflow from local development to a SLURM cluster without code changes.
- Processing many samples identically using wildcard-based rules (`{sample}`).
- Managing dependencies automatically — only re-run steps whose inputs changed.
- Pinning tool versions per rule (Conda, pixi, or container) for full reproducibility.
- Producing DAG visualisations and dry-run previews before committing compute.
- Reusing validated community modules via `Snakemake Wrappers` and `snakemake-workflow-catalog`.

## When NOT to use

- The task graph is **dynamic** (fan-out from a database) or **time-scheduled** → use **Airflow** or **Prefect**.
- The pipeline is **single tool, single output** → a shell script is simpler.
- You need **containerised, cloud-native, Groovy dataflow** → use **Nextflow** (and `nf-core`).
- You need **CWL/WDL** standards compliance (clinical genomics, GA4GH) → use **cwltool** or **Cromwell/WDL**.

## Prerequisites

- Python ≥ 3.11
- `snakemake ≥ 8.x` (check `command -v snakemake` first)
- `graphviz` (for `--dag` visualisation)
- Conda/mamba, **pixi**, or Apptainer for per-rule environments
- SLURM/LSF/PBS for HPC execution

```bash
conda install -c conda-forge -c bioconda snakemake
# or: pip install snakemake
snakemake --version          # 8.x.x
```

## Core workflow

1. **Declare a target `rule all`** with the final outputs you want to produce.
2. **Write rules** mapping input files → output files via a `shell:`, `run:`, or `script:` block.
3. **Use wildcards** (`{sample}`) for sample-agnostic rules and `expand()` to materialise the target list.
4. **Add resources** (`mem_mb`, `runtime`, `threads`) to compute-heavy rules.
5. **Pin environments** with `conda:`, `container:`, or `pixi:` per rule.
6. **Dry-run** with `snakemake -n` to confirm the DAG.
7. **Execute** with a profile (`--profile profiles/slurm`) for HPC/cloud.

## Code patterns

### Minimal two-rule pipeline

```python
# Snakefile
SAMPLES = ["sampleA", "sampleB"]

rule all:
    input:
        expand("results/{sample}.sorted.bam", sample=SAMPLES)

rule align:
    input:
        fastq="data/{sample}.fastq",
        ref="refs/genome.fa"
    output:
        bam="results/{sample}.sorted.bam"
    threads: 4
    shell:
        "bwa mem -t {threads} {input.ref} {input.fastq} "
        "| samtools sort -@ {threads} -o {output.bam}"
```

```bash
snakemake -n            # dry-run
snakemake --cores 8     # execute
```

### Wildcard constraints + multi-extension output

```python
rule process:
    input:
        "data/{sample}_{rep}.fastq"
    output:
        "results/{sample}_{rep}.txt"
    wildcard_constraints:
        sample="[A-Za-z]+",
        rep="\d+"

rule bwa_index:
    input:  "refs/genome.fa"
    output: multiext("refs/genome.fa", ".amb", ".ann", ".bwt", ".pac", ".sa")
    shell:  "bwa index {input}"
```

### Externalise configuration

```python
# config/config.yaml
# samples: [ctrl, treat]
# threads: {align: 8, sort: 4}
# min_mapq: 20

configfile: "config/config.yaml"
SAMPLES = config["samples"]

rule filter_reads:
    input:  "results/{sample}.bam"
    output: "results/{sample}.filtered.bam"
    params: mapq=config["min_mapq"]
    threads: config["threads"]["sort"]
    shell:  "samtools view -q {params.mapq} -b {input} > {output}"
```

### Per-rule resources (drives SLURM/LSF profiles)

```python
rule variant_calling:
    input:
        bam="results/{sample}.deduped.bam",
        ref="refs/genome.fa"
    output:
        vcf="variants/{sample}.vcf.gz"
    resources:
        mem_mb=16000,
        runtime=240,
        disk_mb=20000
    threads: 8
    shell:
        "bcftools mpileup -f {input.ref} {input.bam} "
        "| bcftools call -m -Oz -o {output.vcf}"
```

### Per-rule Conda environment

```python
rule star_align:
    input:
        reads="data/{sample}.fastq",
        genome_dir="refs/star_index/"
    output:
        bam="star_out/{sample}/Aligned.sortedByCoord.out.bam"
    conda:  "envs/star.yaml"
    threads: 8
    shell:
        "STAR --runThreadN {threads} --genomeDir {input.genome_dir} "
        "--readFilesIn {input.reads} --outSAMtype BAM SortedByCoordinate"
```

### Per-rule container (Docker/Apptainer)

```python
rule gatk_haplotypecaller:
    input:
        bam="results/{sample}.bam",
        ref="refs/genome.fa"
    output:
        gvcf="gvcfs/{sample}.g.vcf.gz"
    container: "docker://broadinstitute/gatk:4.4.0.0"
    shell:
        "gatk HaplotypeCaller -I {input.bam} -R {input.ref} "
        "-O {output.gvcf} -ERC GVCF"
```

### Reusable modules via `configfile` includes

```python
# Snakefile
module qc:
    snakefile: "modules/qc/Snakefile"
    config: config

use rule * from qc as qc_*
```

### Run as a module (publish to PyPI / share across projects)

```python
# workflow/Snakefile — exported as `my_pipeline`
configfile: "config.yaml"
SAMPLES = config["samples"]

rule all:
    input: expand("out/{sample}.bam", sample=SAMPLES)

rule align:
    input:  "in/{sample}.fastq"
    output: "out/{sample}.bam"
    shell:  "bwa mem refs/genome.fa {input} | samtools view -b > {output}"
```

```bash
snakemake --module workdir my_pipeline       # install
# In another Snakefile:
# module my_pipeline:
#     snakefile: "workflow/Snakefile"
```

### Special output types

```python
rule sort_bam:
    input:  "results/{sample}.raw.bam"
    output: temp("results/{sample}.sorted_temp.bam")  # auto-deleted after consumers run
    shell:  "samtools sort {input} -o {output}"

rule final_report:
    input:  "results/{sample}.vcf.gz"
    output: protected("reports/{sample}.final.vcf.gz")  # write-protected
    shell:  "cp {input} {output}"

rule validate_bam:
    input:  "results/{sample}.bam"
    output: touch("checkpoints/{sample}.validated")  # empty flag
    shell:  "samtools quickcheck {input} && echo OK"
```

### Auto-discover samples from disk

```python
from pathlib import Path
SAMPLES = sorted(p.stem.replace(".fastq", "") for p in Path("data/").glob("*.fastq"))

rule all:
    input: expand("results/{sample}.bam", sample=SAMPLES)
```

### Aggregation rule across all samples

```python
rule multiqc:
    input:
        expand("qc/{sample}_fastqc.zip", sample=SAMPLES),
        expand("results/{sample}.flagstat.txt", sample=SAMPLES)
    output:
        "multiqc/multiqc_report.html"
    shell:  "multiqc qc/ results/ -o multiqc/"
```

## SLURM profile (the high-value step)

```bash
mkdir -p profiles/slurm
cat > profiles/slurm/config.yaml <<'EOF'
executor: slurm
jobs: 100
default-resources:
  mem_mb: 4000
  runtime: 60
use-conda: true
use-apptainer: true
latency-wait: 30
rerun-incomplete: true
EOF

snakemake --profile profiles/slurm --cores 256 -n        # dry-run
snakemake --profile profiles/slurm --cores 256         # submit
snakemake --profile profiles/slurm --report report.html # post-run HTML report
```

## Common pitfalls

- **No `rule all`** → Snakemake only runs the first rule. Always declare your final targets.
- **Ambiguous wildcards** (`AmbiguousRuleException`) → add `wildcard_constraints:` or use `ruleorder`.
- **Missing outputs** (`MissingOutputException`) → check the rule's `shell:` cwd and that all output paths are created.
- **Cluster jobs OOM or timeout** → increase `mem_mb` / `runtime`; check `benchmark:` to measure real use.
- **Conda env build fails** → add `conda-forge` before `bioconda`, pin versions.
- **Re-running unexpectedly** → output mtime older than input; `snakemake --touch` or delete and re-run.
- **Protected output can't be overwritten** → remove the file or drop `protected()`.

## Validation

- `snakemake -n` → dry-run shows the expected DAG; run before every production launch.
- `snakemake --dag | dot -Tpdf > workflow_dag.pdf` → visualise the DAG.
- `snakemake --report report.html` → post-run HTML with stats per rule.
- Per-rule `benchmark: "benchmarks/{rule}/{sample}.txt"` → real runtime and memory.

## Open alternatives

| Need | Tool |
|------|------|
| Groovy dataflow, container-native, cloud-first | **Nextflow** (DSL2, nf-core) |
| CWL/WDL standards (clinical, GA4GH) | **cwltool**, **Cromwell/WDL** |
| Dynamic fan-out from a database | **Airflow**, **Prefect**, **Dagster** |
| Self-contained tool version per step | **pixi** (`pixi:` directive in v8+) |
| Container engines | **Apptainer** (replaces Singularity on HPC) |

## References

- Snakemake docs: <https://snakemake.readthedocs.io/>
- Snakemake paper: Mölder et al. 2021, *F1000Research* 10:33, `10.12688/f1000research.29032.2`
- Snakemake workflow catalog: <https://snakemake.github.io/snakemake-workflow-catalog/>
- nf-core (parallel Nextflow ecosystem): <https://nf-co.re/>
- Companion skill: `ors-data-engineering-nextflow-workflow-engine`
- Companion skill: `ors-data-engineering-fair-data-principles` (DVC integration)

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `snakemake-workflow-engine` (SciAgent-Skills-main/scientific-computing/snakemake-workflow-engine).
