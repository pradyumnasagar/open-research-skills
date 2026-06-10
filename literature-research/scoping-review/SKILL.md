---
name: ors-literature-research-scoping-review
display_name: "Scoping Review Methodology"
description: "Map evidence landscapes in emerging fields using Arksey-O'Malley and JBI scoping review frameworks. Includes charting, narrative synthesis, consultation exercise, and gap identification without formal quality assessment."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: literature-research
tags: [scoping-review, arksey-omalley, jbi, evidence-mapping, gap-analysis]
difficulty: intermediate
prerequisites:
  tools: [reference manager (Zotero), spreadsheet/Excel, NVivo/ATLAS.ti (optional for qualitative charting)]
  skills: [ors-literature-research-literature-search]
sources_consulted:
  - "Arksey & O'Malley 'Scoping studies: towards a methodological framework' (International Journal of Social Research Methodology); Adapted: Modern JBI methodology"
  - "JBI Manual for Evidence Synthesis, Chapter 11: Scoping Reviews (jbi-global); Adapted: PCC framework, evidence gap maps"
  - "Peters et al. PRISMA-ScR extension; Adapted: Reporting checklist"
  - "Levac, Colquhoun & O'Brien 'Scoping studies: advancing the methodology' (Implementation Science); Adapted: Consultation exercise guidance"
  - "Munn et al. 'Systematic review or scoping review?' (BMC Med Res Methodol); Adapted: Decision guidance"
last_updated: 2026-06-10
---

# Scoping Review Methodology

> A scoping review asks "what exists?" not "what works?" When the field is new, the question is broad, or the goal is to map concepts and identify gaps, a systematic review's emphasis on quantitative synthesis and risk-of-bias is the wrong tool. This skill covers the Arksey-O'Malley and JBI frameworks for scoping reviews: how to chart the literature narratively, synthesize conceptually, and engage stakeholders in the consultation exercise.

## When to use

- Mapping the breadth of literature in an emerging or rapidly evolving field
- Identifying key concepts, definitions, and terminology in a domain
- Exposing gaps in the evidence base to inform future research
- Determining whether a full systematic review is feasible or warranted
- Summarizing and disseminating research findings to practitioners/policymakers
- Exploring the extent, range, and nature of research on a topic
- When a broad question needs a broad answer (e.g., "what AI tools are used in clinical genomics?")

## When NOT to use

- Answering a focused clinical question with quantitative synthesis — use `ors-literature-research-systematic-review` instead
- When risk-of-bias assessment is required for decision-making (clinical guidelines, regulatory submissions)
- When the question can be narrowed to a specific PICO and enough RCTs exist for meta-analysis
- For qualitative meta-synthesis or realist synthesis (different methodologies)
- When formal quality grading (GRADE) is needed for each outcome
- For narrative reviews that don't follow a structured methodology

## Prerequisites

- A research question broad enough that systematic review would be inappropriate
- Stakeholder group identified for optional consultation exercise
- Reference manager with comprehensive search results (`ors-literature-research-literature-search`)
- A charting spreadsheet (Excel, Google Sheets, or Airtable) for data extraction
- Familiarity with the PCC framework (Population, Concept, Context) for scoping reviews
- Optional: Visualization tool (Tableau, R ggplot2) for evidence gap maps

## Core workflow

### 1. Define the scope using PCC

The PCC framework is the scoping review equivalent of PICO:

- **P (Population)**: Who is the focus? (e.g., older adults, patients with diabetes)
- **C (Concept)**: What is being examined? (e.g., AI tools, telehealth, shared decision-making)
- **C (Context)**: What is the setting? (e.g., primary care, low-income countries, hospital)

Write a brief protocol with:

1. **Title**: "Scoping review of [P] in relation to [C] in [C]"
2. **Objectives**: 2–3 specific objectives (e.g., map concepts, identify gaps, summarize evidence)
3. **Research question**: Broad question aligned with PCC
4. **Inclusion criteria**: Based on PCC + study type + language + date range

Example research question: "What artificial intelligence tools have been applied to genomic variant interpretation in clinical settings, and what evidence exists for their performance and implementation?"

### 2. Develop the search strategy

Build a comprehensive search:

- **Databases**: At least 3 relevant databases (e.g., PubMed, Embase, CINAHL for health)
- **Grey literature**: Conference proceedings, theses, reports, trial registries
- **Hand-searching**: Key journals in the field
- **Citation chasing**: Forward and backward snowballing
- **Search update**: Plan to re-run before submission

Document the search following PRISMA-S (from `ors-literature-research-literature-search`).

### 3. Select evidence (screening)

Apply inclusion/exclusion criteria iteratively:

- **Level 1 screening**: Title and abstract review
  - Liberal inclusion: include anything potentially relevant
  - Document reasons for exclusion
- **Level 2 screening**: Full-text review
  - Apply PCC criteria strictly
  - Document reasons for exclusion (use a coding scheme)

For scoping reviews, **dual screening is recommended** but **not always required**. Document your approach.

### 4. Chart the data

Extract key information from each included study. Unlike systematic reviews, "charting" is broader than "data extraction" and includes:

| Field | Example |
|-------|---------|
| Author(s), year | Smith et al., 2023 |
| Country/setting | United States, academic medical center |
| Population | Adults with type 2 diabetes (n=150) |
| Concept/phenomenon | AI-based glucose prediction |
| Methods | Prospective cohort, machine learning |
| Key findings | 85% accuracy in glucose prediction |
| Limitations | Single-site, limited demographics |
| Funding source | NIH R01DK123456 |
| Conflicts of interest | None reported |

Use NVivo, ATLAS.ti, or Excel for charting. Excel is most common and accessible.

### 5. Collate, summarize, and report results

Three synthesis approaches:

1. **Numerical summary**: Counts of studies by year, country, method, etc.
2. **Narrative summary**: Themes, patterns, and gaps described textually
3. **Tabular presentation**: Descriptive tables summarizing characteristics

#### Numerical analysis example
- 45 included studies
- Years: 2015–2026 (60% published 2022–2026)
- Countries: USA (40%), Europe (30%), Asia (20%), other (10%)
- Methods: 60% observational, 30% experimental, 10% qualitative
- Populations: 5 distinct groups identified

#### Narrative themes
- Theme 1: Most studies focus on prediction rather than causal inference
- Theme 2: Limited long-term follow-up (< 12 months)
- Theme 3: Few studies in low- and middle-income countries
- Gap 1: No validation studies in pediatric populations
- Gap 2: Limited integration with electronic health records

### 6. Consultation exercise (optional but recommended)

The Arksey-O'Malley framework includes a **consultation exercise** as a key stage:

- **Purpose**: Validate findings, identify missing literature, gain practitioner insights
- **Method**: Semi-structured interviews or focus groups with 5–20 stakeholders
- **Analysis**: Qualitative thematic analysis of consultation data
- **Integration**: Add consultation findings to the narrative synthesis

Levac et al. refined this to be more rigorous:

- Use purposive sampling to select stakeholders
- Develop interview guide from preliminary findings
- Use member checking to validate interpretations
- Integrate consultation findings with charted data

### 7. Identify gaps and implications

A core output of scoping reviews is the **evidence gap map** (EGM):

```
Evidence Gap Map Structure:
1. Research gaps: Topics understudied or not studied
2. Knowledge gaps: Inconsistencies or contradictions in findings
3. Methodological gaps: Weak designs, lack of rigor
4. Population gaps: Underrepresented groups
5. Setting gaps: Geographic or contextual limitations
```

#### Evidence Gap Map visualization

```
| Study Design | Strong Evidence | Moderate Evidence | Weak Evidence | No Evidence |
|--------------|-----------------|-------------------|---------------|-------------|
| RCT          | XXXX            | XX                | X             | 0           |
| Cohort       | XX              | XXXXXX            | XXX           | X           |
| Qualitative  | X               | X                 | XXXX          | XX          |
| Mixed        | 0               | X                 | XX            | XXX         |
```

### 8. Report using PRISMA-ScR

The PRISMA Extension for Scoping Reviews (PRISMA-ScR) checklist has 22 essential reporting items:

#### Title and Abstract
1. Title: identifies as scoping review
2. Structured summary: objectives, eligibility criteria, methods, results, conclusions

#### Introduction
3. Rationale: why a scoping review is needed
4. Objectives: specific research questions

#### Methods
5. Protocol and registration
6. Eligibility criteria (PCC)
7. Information sources (databases, grey literature)
8. Search strategy (full strings in appendix)
9. Selection of sources of evidence
10. Data charting process
11. Data items (charting form)
12. Critical appraisal (optional, often not done)
13. Synthesis of results

#### Results
14. Selection of sources of evidence (PRISMA flow)
15. Characteristics of sources of evidence (table)
16. Synthesis of results (narrative + tabulation)

#### Discussion
17. Summary of evidence
18. Limitations
19. Conclusions

#### Funding
20. Funding sources
21. Conflicts of interest

#### Optional
22. Supplementary materials

### 9. Outputs of a scoping review

Common deliverables:

- **Descriptive table**: Characteristics of all included studies
- **Conceptual framework**: Map of key concepts and their relationships
- **Evidence gap map**: Visual representation of what is and isn't known
- **Narrative summary**: Synthesis of themes, patterns, gaps
- **Recommendations**: For practice, policy, and future research
- **Consultation report**: Stakeholder perspectives and validation

## Code patterns

### Building a charting database

```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Create charting spreadsheet template
def create_charting_template(output_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Charting"
    
    # Define columns
    columns = [
        "study_id", "first_author", "year", "title", "journal",
        "country", "setting", "population", "sample_size",
        "concept", "methodology", "study_design",
        "key_findings", "limitations", "funding_source",
        "notes", "reviewer_1", "reviewer_2"
    ]
    
    # Header row
    header_fill = PatternFill(start_color="366092", 
                              end_color="366092", 
                              fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    for col_idx, col_name in enumerate(columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
    
    # Set column widths
    column_widths = {
        "study_id": 10, "first_author": 20, "year": 8, "title": 40,
        "journal": 25, "country": 15, "setting": 20, "population": 30,
        "sample_size": 12, "concept": 30, "methodology": 25,
        "study_design": 20, "key_findings": 50, "limitations": 30,
        "funding_source": 25, "notes": 30, "reviewer_1": 15, "reviewer_2": 15
    }
    
    for col_idx, col_name in enumerate(columns, start=1):
        ws.column_dimensions[chr(64 + col_idx)].width = column_widths.get(col_name, 15)
    
    wb.save(output_path)
```

### Extracting data into charting table

```python
import requests
import json

def extract_from_papers(papers_metadata, output_csv):
    """
    Extract charting data from a list of paper metadata.
    """
    rows = []
    for paper in papers_metadata:
        # Extract relevant fields
        first_author = paper.get("authors", [{}])[0].get("name", "")
        year = paper.get("year", "")
        
        # Extract country/setting from affiliation data
        country = extract_country(paper.get("affiliations", []))
        setting = extract_setting(paper.get("affiliations", []))
        
        row = {
            "first_author": first_author,
            "year": year,
            "title": paper.get("title", ""),
            "journal": paper.get("venue", ""),
            "country": country,
            "doi": paper.get("doi", ""),
            "pmid": paper.get("pmid", ""),
        }
        rows.append(row)
    
    # Save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
```

### Numerical summary statistics

```python
import pandas as pd

def generate_numerical_summary(charting_csv):
    """
    Generate numerical summary of scoping review charting data.
    """
    df = pd.read_csv(charting_csv)
    
    summary = {
        "total_studies": len(df),
        "year_range": f"{df['year'].min()}-{df['year'].max()}",
        "recent_5_years": len(df[df['year'] >= 2021]),
        "top_journals": df['journal'].value_counts().head(5).to_dict(),
        "country_distribution": df['country'].value_counts().head(10).to_dict(),
        "methodology_distribution": df['methodology'].value_counts().to_dict(),
        "study_design_distribution": df['study_design'].value_counts().to_dict(),
    }
    
    return summary
```

### Evidence gap map visualization

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_evidence_gap_map(gap_data, output_path):
    """
    Plot a bubble chart evidence gap map.
    
    gap_data: DataFrame with columns:
        - topic (research topic)
        - evidence_strength (1-4)
        - study_count (number of studies)
        - gap_type (Research, Knowledge, Methodological)
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Color by gap type
    colors = {
        "Research": "#1f77b4",
        "Knowledge": "#ff7f0e",
        "Methodological": "#2ca02c"
    }
    
    for gap_type, color in colors.items():
        subset = gap_data[gap_data["gap_type"] == gap_type]
        ax.scatter(subset["evidence_strength"], 
                  subset.index,
                  s=subset["study_count"] * 50,
                  c=color, 
                  alpha=0.6,
                  label=gap_type)
    
    ax.set_xlabel("Evidence Strength (1=Weak, 4=Strong)")
    ax.set_ylabel("Research Topics")
    ax.set_title("Evidence Gap Map")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```

### Concept mapping with VOSviewer export

```python
def export_for_vosviewer(charting_csv, output_csv):
    """
    Export data in VOSviewer-compatible format for concept mapping.
    VOSviewer creates bibliometric network visualizations.
    """
    df = pd.read_csv(charting_csv)
    
    # VOSviewer expects: id, label, weight, <dimension columns>
    network_data = []
    for idx, row in df.iterrows():
        # Extract keywords/concepts
        concepts = extract_concepts(row)
        for concept in concepts:
            network_data.append({
                "id": f"study_{idx}",
                "label": concept,
                "weight": 1
            })
    
    pd.DataFrame(network_data).to_csv(output_csv, index=False)
```

## Common pitfalls

- **Treating scoping review as systematic review**: Scoping reviews don't assess risk of bias or pool effects
- **Too narrow a question**: If you can form a PICO, consider systematic review instead
- **No conceptual synthesis**: Just listing studies without identifying themes
- **Missing the consultation stage**: Stakeholder input is a defining feature
- **Quality assessment not done**: Scoping reviews typically don't assess quality, but if you do, document your approach
- **Inadequate charting**: Surface-level extraction misses nuances
- **Confusing scoping with narrative review**: Scoping reviews follow a structured methodology
- **No gap identification**: A core output is identifying what we don't know
- **PRISMA-ScR not followed**: Reviewers expect adherence to reporting standards
- **No protocol registration**: Optional for scoping but improves rigor
- **Too much synthesis**: Don't force meta-analysis; the goal is breadth, not depth
- **Ignoring grey literature**: Limits scope and misses key sources

## Validation

- **PRISMA-ScR checklist complete**: All 22 items addressed
- **PCC framework clear**: Population, Concept, Context explicitly defined
- **Search strategy documented**: Multiple databases, grey literature, citation chasing
- **Charting table comprehensive**: All relevant fields extracted
- **Numerical summary provided**: Counts, distributions, year ranges
- **Narrative synthesis present**: Themes and patterns identified
- **Evidence gaps identified**: Specific gaps in research, knowledge, methodology
- **Consultation conducted**: Stakeholder perspectives integrated (if applicable)
- **Conceptual framework or gap map**: Visual output of findings
- **Future research directions**: Clear recommendations for next studies
- **Limitations acknowledged**: Search limitations, language, date ranges

## Open alternatives

| Commercial / paid | Open alternative | Trade-off |
|---|---|---|
| Covidence for screening | Rayyan (free tier), ASReview | Rayyan has free academic tier |
| NVivo for qualitative analysis | ATLAS.ti (paid), Taguette (free), RQDA (R) | NVivo is industry standard; Taguette is free and web-based |
| EndNote for reference management | Zotero | Zotero is free and open |
| Scoping review workshops (paid) | JBI Manual, Arksey & O'Malley paper, Tricco et al. methods papers | JBI manual is free; workshops provide hands-on training |
| MAXQDA for qualitative data | RQDA, Taguette, dedoose | RQDA is open-source R package |
| Tableau for gap maps | R (ggplot2), Python (matplotlib) | Tableau is paid; R/Python are open but require code |

## References

Internal skills:
- `ors-literature-research-literature-search` — comprehensive search strategies
- `ors-literature-research-citation-management` — reference management for screening
- `ors-literature-research-systematic-review` — for focused questions with synthesis
- `ors-open-science-preprints` — for protocol preprints
- `ors-research-grants` — for grant applications based on scoping review findings

External sources:
- Arksey & O'Malley (2005) original framework — doi.org/10.1080/1364557032000119616
- JBI Manual for Evidence Synthesis — jbi-global
- PRISMA-ScR Extension (Tricco et al. 2018) — annals.org/aim/fullarticle/2700389
- Levac, Colquhoun & O'Brien — implementationscience.biomedcentral.com/articles/10.1186/1748-5908-5-69
- Munn et al. "Systematic review or scoping review?" — bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-018-0611-x
- VOSviewer for bibliometric visualization — vosviewer.com
- Evidence Gap Maps (3ie) — 3ieimpact.org/evidence-hub/evidence-gap-maps

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Written from scratch following Arksey-O'Malley framework, JBI methodology, and PRISMA-ScR reporting guidelines. Includes PCC framework, charting workflows, consultation exercise guidance, evidence gap mapping, and code examples for data extraction and visualization.