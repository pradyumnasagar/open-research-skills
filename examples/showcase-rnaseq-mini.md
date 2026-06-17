# Showcase: End-to-End RNA-seq Mini Analysis

A complete, runnable walkthrough that uses 4 ORS skills in sequence,
writes Material Passports at each step, and produces a publication-quality
volcano plot from raw FASTQ. The pipeline runs in < 5 minutes on a laptop.

This is the worked example referenced in `docs/pipelines.md` (Pipeline 1,
shortened to 4 skills for the showcase).

## What you'll produce

```
showcase/
├── data/
│   └── sample.fastq.gz          # 10,000 synthetic reads
├── results/
│   ├── sample.sorted.bam        # aligned reads
│   ├── sample.counts.tsv        # gene-level counts
│   └── volcano.png              # publication figure
├── sample.trim.passport.json    # passport from step 2
├── sample.align.passport.json   # passport from step 3
├── sample.counts.passport.json  # passport from step 4
├── sample.fig.passport.json     # passport from step 5
└── CHAIN.txt                    # the passport DAG
```

## Skills used

| # | Skill | Role |
|---|---|---|
| 1 | `meta/roadmap-author` | (not used in the run, but the recipe is generated using its workflow) |
| 2 | `bioinformatics-sequence/fastp-quality-control` | adapter trim + QC |
| 3 | `bioinformatics-sequence/minimap2-alignment` | align to a tiny reference |
| 4 | `bioinformatics-sequence/featurecounts-quantification` | count reads per gene |
| 5 | `statistics/volcano-plot` | the DE volcano plot |

## Step 0: Setup

```bash
# Clone and install ORS
git clone https://github.com/pradyumnasagar/open-research-skills
cd open-research-skills
pip install -r requirements.txt   # fastp, minimap2, subread, pandas, matplotlib, seaborn

# Create the showcase workdir
mkdir -p showcase/{data,results}
cd showcase
```

## Step 1: Generate synthetic input

```bash
# Download a tiny reference (chr22 of GRCh38, ~50kb)
curl -L https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr22.fa.gz \
  | gunzip > data/chr22.fa
samtools faidx data/chr22.fa

# Generate 10,000 synthetic 100bp reads (use any simulator; wgsim is simplest)
wgsim -N 10000 -1 100 -2 100 -r 0.001 data/chr22.fa data/sample_R1.fastq data/sample_R2.fastq
gzip data/sample_R*.fastq
```

## Step 2: Quality control

```bash
# Load the fastp-quality-control skill, then run it on the data
fastp \
  -i data/sample_R1.fastq.gz -I data/sample_R2.fastq.gz \
  -o data/sample_R1.trim.fastq.gz -O data/sample_R2.trim.fastq.gz \
  -j results/fastp.json -h results/fastp.html \
  --thread 4
```

After fastp finishes, the skill writes `sample.trim.passport.json`:

```json
{
  "schema_version": "1.0.0",
  "passport_id": "<uuid>",
  "created_at": "2026-06-17T12:00:00Z",
  "produced_by": {"skill": "fastp-quality-control", "skill_version": "1.0.0"},
  "inputs": [{"type": "fastq", "path": "data/sample_R1.fastq.gz", "sha256": "..."}],
  "outputs": [{"type": "fastq", "path": "data/sample_R1.trim.fastq.gz", "sha256": "..."}],
  "decisions": [{"step": "trim", "choice": "fastp default", "rationale": "..."}],
  "errors": [{"step": "trim", "tool": "fastp", "exit_code": 0, "stderr_excerpt": ""}],
  "consumed_passports": [],
  "downstream_hints": {
    "next_skills": ["minimap2-alignment", "star-alignment"],
    "expected_inputs": ["fastq", "fastq"]
  }
}
```

## Step 3: Alignment

```bash
# Build a minimap2 index for chr22 (small enough to be quick)
minimap2 -d data/chr22.mmi data/chr22.fa

# Align
minimap2 -ax sr -t 4 data/chr22.mmi \
  data/sample_R1.trim.fastq.gz data/sample_R2.trim.fastq.gz \
  | samtools sort -@ 4 -o results/sample.sorted.bam -
samtools index results/sample.sorted.bam
```

Write `sample.align.passport.json` with `consumed_passports: ["<step 2 passport_id>"]`.

## Step 4: Quantification

```bash
# Get a tiny GTF (chr22 annotation, ~1000 genes)
curl -L https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/hg38.knownGene.gtf.gz \
  | gunzip > data/hg38.knownGene.gtf  # or use a pre-made tiny GTF

# Count
featureCounts -a data/hg38.knownGene.gtf -o results/sample.counts.tsv \
  -t exon -g gene_id results/sample.sorted.bam
```

Write `sample.counts.passport.json`.

## Step 5: Volcano plot

```bash
# Use the volcano-plot skill to make a publication-quality figure
python -m ors_skills.statistics.volcano_plot \
  --counts results/sample.counts.tsv \
  --output results/volcano.png \
  --title "Showcase: synthetic RNA-seq" \
  --width 5 --height 4
```

Write `sample.fig.passport.json`.

## Step 6: Write the chain

```bash
# Concatenate the consumed_passports edges to form the DAG
cat <<EOF > CHAIN.txt
sample.trim.passport.json
  → sample.align.passport.json
    → sample.counts.passport.json
      → sample.fig.passport.json
EOF

# Validate every passport
python ../scripts/validate-passport.py --all
```

Expected output:

```
✅ sample.trim.passport.json
✅ sample.align.passport.json
✅ sample.counts.passport.json
✅ sample.fig.passport.json

All 4 passport(s) valid.
```

## Step 7: Verify the chain

```bash
# Confirm that every consumed_passports ID actually points to an existing passport
python -c "
import json, glob, pathlib
known = {json.loads(p.read_text())['passport_id']: p for p in glob.glob('*.passport.json')}
for p in glob.glob('*.passport.json'):
    data = json.loads(p.read_text())
    for c in data.get('consumed_passports', []):
        if c not in known:
            print(f'❌ {p.name} references unknown passport {c}')
        else:
            print(f'✅ {p.name} → {known[c].name}')
"
```

## What this showcase demonstrates

- **Skill composition:** 4 skills + 1 meta skill load in sequence, each
  producing real output and a Material Passport.
- **Passport chaining:** every step's `consumed_passports[]` references
  the prior step's `passport_id`, forming a verifiable DAG.
- **Cross-category flow:** the pipeline spans `bioinformatics-sequence`
  (steps 2-4) and `statistics` (step 5), using the passport as the
  boundary object.
- **Schema validation:** `scripts/validate-passport.py` enforces the
  JSON Schema at every step.
- **Self-contained reproducibility:** the `CHAIN.txt` file documents the
  exact execution order; the passports document what each step actually
  did.

## Adapting this showcase

To run the showcase on real data:

- Replace synthetic reads with a real SRA accession (e.g. SRR12345678).
- Use the full GRCh38 instead of chr22.
- Use `star-alignment` instead of `minimap2` for spliced alignment.
- Add `deseq2-differential-expression` between step 4 and step 5 to get
  real DE results (you'll need a metadata file with sample conditions).
- Use `scientific-writing/figure-design` after step 5 to refine the figure.

Each adaptation requires a new passport — the showcase recipe is the
starting point, not the destination.

## Cross-references

- `docs/pipelines.md` — pipeline 1 (full RNA-seq with 7 stages).
- `spec/material-passport.md` — the passport schema.
- `meta/agent-handoff/SKILL.md` — the handoff discipline.
- `meta/roadmap-author/SKILL.md` — how to author a new skill like the
  ones used in this showcase.
