# Minimal showcase: synthetic RNA-seq -> volcano plot
#
# This Makefile implements the recipe in showcase-rnaseq-mini.md.
# Run:    make -f examples/Makefile showcase
# Clean:  make -f examples/Makefile clean
#
# Requires: fastp, minimap2, samtools, subread (featureCounts), wgsim,
#           python3, curl, gunzip, samtools, ORS source tree on PYTHONPATH.

WORK ?= showcase
REF ?= $(WORK)/data/chr22.fa
NREADS ?= 10000

.PHONY: showcase clean validate chain

showcase: $(WORK)/results/volcano.png $(WORK)/CHAIN.txt
	@echo ""
	@echo "Showcase complete. Open $(WORK)/results/volcano.png"

clean:
	rm -rf $(WORK)

# --- Steps ----------------------------------------------------------------

$(WORK)/data/chr22.fa:
	@mkdir -p $(WORK)/data
	curl -sSL https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr22.fa.gz \
	  | gunzip > $(WORK)/data/chr22.fa

$(WORK)/data/sample_R1.fastq.gz: $(WORK)/data/chr22.fa
	wgsim -N $(NREADS) -1 100 -2 100 -r 0.001 $(WORK)/data/chr22.fa \
	    $(WORK)/data/sample_R1.fastq $(WORK)/data/sample_R2.fastq
	gzip $(WORK)/data/sample_R*.fastq

$(WORK)/data/sample_R1.trim.fastq.gz: $(WORK)/data/sample_R1.fastq.gz
	fastp -i $(WORK)/data/sample_R1.fastq.gz -I $(WORK)/data/sample_R2.fastq.gz \
	      -o $(WORK)/data/sample_R1.trim.fastq.gz \
	      -O $(WORK)/data/sample_R2.trim.fastq.gz \
	      -j $(WORK)/results/fastp.json -h $(WORK)/results/fastp.html \
	      --thread 4

$(WORK)/results/sample.sorted.bam: $(WORK)/data/sample_R1.trim.fastq.gz
	minimap2 -d $(WORK)/data/chr22.mmi $(WORK)/data/chr22.fa
	minimap2 -ax sr -t 4 $(WORK)/data/chr22.mmi \
	         $(WORK)/data/sample_R1.trim.fastq.gz \
	         $(WORK)/data/sample_R2.trim.fastq.gz \
	  | samtools sort -@ 4 -o $(WORK)/results/sample.sorted.bam -
	samtools index $(WORK)/results/sample.sorted.bam

$(WORK)/results/sample.counts.tsv: $(WORK)/results/sample.sorted.bam
	curl -sSL https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/hg38.knownGene.gtf.gz \
	  | gunzip > $(WORK)/data/hg38.knownGene.gtf
	featureCounts -a $(WORK)/data/hg38.knownGene.gtf \
	              -o $(WORK)/results/sample.counts.tsv \
	              -t exon -g gene_id $(WORK)/results/sample.sorted.bam

$(WORK)/results/volcano.png: $(WORK)/results/sample.counts.tsv
	# Stub: replace with the real volcano-plot skill implementation.
	# The skill produces a publication-quality figure and a passport.
	python -c "import matplotlib.pyplot as plt; \
	           import pandas as pd; \
	           df = pd.read_csv('$(WORK)/results/sample.counts.tsv', sep='\t', comment='#'); \
	           plt.scatter(df.iloc[:, -1], df.iloc[:, -2]); \
	           plt.savefig('$(WORK)/results/volcano.png', dpi=200); \
	           plt.close()"
	touch $(WORK)/sample.fig.passport.json

$(WORK)/CHAIN.txt: $(WORK)/results/volcano.png
	@echo "trim -> align -> counts -> fig" > $(WORK)/CHAIN.txt

# --- Validation -----------------------------------------------------------

validate:
	python scripts/validate-passport.py --all
	python scripts/validate-skills.py skills/ --meta meta/

chain:
	@echo "Passport chain:"
	@for f in showcase/*.passport.json; do \
	  echo "  $$f"; \
	done
