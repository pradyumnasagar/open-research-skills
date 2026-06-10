---
name: ors-literature-research-literature-search
display_name: "Literature Search Strategy"
description: "Design reproducible, multi-database literature searches for biomedical and scientific questions. Covers PubMed/Web of Science/Scopus/Embase/IEEE/ACM/AGRICOLA/ERIC/PsycINFO, open indexes (OpenAlex, Semantic Scholar, Google Scholar), MeSH, Boolean operators, snowballing, citation alerts, and PRISMA-S compliant reporting."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: literature-research
tags: [pubmed, web-of-science, scopus, openalex, mesh, prisma-s, boolean-search]
difficulty: intermediate
prerequisites:
  tools: [python, requests, biopython, requests-cache]
  skills: [ors-literature-research-paper-lookup, ors-literature-research-citation-management]
sources_consulted:
  - "PRISMA 2020 statement and PRISMA-S extension for search reporting (prisma-statement.org)"
  - "Cochrane Handbook for Systematic Reviews of Interventions, Chapter 4 (training.cochrane.org/handbook)"
  - "NCBI PubMed User Guide and MeSH Browser (ncbi.nlm.nih.gov/mesh, pubmed.ncbi.nlm.nih.gov/help)"
  - "OpenAlex API documentation (docs.openalex.org)"
  - "Semantic Scholar API documentation (api.semanticscholar.org)"
last_updated: 2026-06-10
---

# Literature Search Strategy

> A literature search is a small research project. The question drives the query, the query drives the database, and the database drives the syntax. This skill captures the questions worth asking before any string is sent to a server, the database-specific syntax that actually returns what you want, and the reporting format that satisfies PRISMA-S so the search is reproducible by a third party months later.

## When to use

- Beginning a systematic, scoping, or narrative review and needing a defensible multi-database search.
- Building a reproducible search for a grant aim, dissertation chapter, or regulatory submission.
- Designing a search-update protocol so the same query re-runs cleanly on a future date.
- Constructing a sensitive (high recall) versus a specific (high precision) search and needing to defend the choice.
- Setting up citation alerts or RSS feeds to keep a question current after the initial search.
- Resolving a question about which database covers a particular topic or study type (engineering, agriculture, education, psychology, biomedicine).

## When NOT to use

- Looking up a single known paper by DOI/PMID/title — use `ors-literature-research-paper-lookup` instead.
- Selecting a citation manager — use `ors-literature-research-citation-management`.
- Running the formal risk-of-bias and meta-analysis pipeline — that is `ors-literature-research-systematic-review`.
- Conducting a scoping review with a specific framework — use `ors-literature-research-scoping-review`.
- Screening, deduplication, and PRISMA flow counts — the next skill in the pipeline handles this.

## Prerequisites

- A research question written in a structured frame (PICO, PEO, PCC, SPIDER — see "Framing the question").
- An account on at least one open index (OpenAlex or Semantic Scholar) for the modern multi-database approach.
- A working directory layout: `sources/search_<date>_<topic>/` for raw exports, `references/` for in-progress screening.
- A citation manager library set up via `ors-literature-research-citation-management` so exports land in a single library.
- Familiarity with Boolean logic, controlled vocabularies, and the concept of precision vs. recall.

## Core workflow

### 1. Frame the question

Pick a frame. The frame dictates which concepts matter and which database will be most sensitive.

- **PICO** (Population, Intervention, Comparator, Outcome) — clinical trials, therapy questions.
- **PEO** (Population, Exposure, Outcome) — etiology, risk factors.
- **PCC** (Population, Concept, Context) — scoping reviews, JBI guidance.
- **SPIDER** (Sample, Phenomenon of Interest, Design, Evaluation, Research type) — qualitative and mixed-methods.

Write the frame as a single short sentence, then extract 2–4 concepts. Each concept becomes a Boolean block.

### 2. Choose the database set

A sensitive search for a clinical question needs biomedical-heavy databases; an engineering question is poorly served by the same set. A pragmatic 2026 baseline for most biomedical systematic reviews is:

| Domain emphasis | Primary databases | Coverage notes |
|---|---|---|
| Biomedical / clinical | PubMed, Embase, Web of Science Core Collection, Cochrane CENTRAL | Add CINAHL for nursing, PsycINFO for behavioural |
| Public health / global | PubMed, Embase, Web of Science, LILACS, WHO Global Index Medicus | LILACS critical for Latin American literature |
| Engineering / computing | IEEE Xplore, ACM Digital Library, Scopus, Compendex (Engineering Village) | arXiv and ACM for preprints |
| Agriculture / food | AGRICOLA, CAB Abstracts, Web of Science, Scopus | Add FSTA for food science |
| Education / pedagogy | ERIC, Education Source, Web of Science, Scopus | Add ProQuest Dissertations for theses |
| Psychology / behavioural | PsycINFO, PubMed, Web of Science, Embase | Add PsycTESTS for instruments |
| Multidisciplinary / modern | OpenAlex, Semantic Scholar, Scopus, Dimensions, Google Scholar | OpenAlex is open; use as the always-included fallback |

The open-index trio (OpenAlex, Semantic Scholar, Crossref) covers more than 250M works and is free. If the topic is broad and resources are limited, an OpenAlex + Semantic Scholar + one discipline-specific database combination is defensible.

### 3. Build the concept blocks

For each concept, list free-text synonyms (title/abstract) and any controlled vocabulary (MeSH, EMTREE, thesaurus terms). Mix with OR inside a block, then AND the blocks together.

```
# Block 1: population
("type 2 diabetes"[MeSH] OR "diabetes mellitus, type 2"[MeSH]
  OR "T2DM"[tiab] OR "type 2 diabetes"[tiab] OR "non-insulin-dependent diabetes"[tiab])

# Block 2: intervention
("GLP-1 receptor agonist"[MeSH] OR "glucagon-like peptide-1"[tiab]
  OR semaglutide[tiab] OR liraglutide[tiab] OR dulaglutide[tiab])

# Block 3: outcome
("weight loss"[MeSH] OR "weight loss"[tiab] OR "body weight"[tiab]
  OR "BMI"[tiab] OR "glycated hemoglobin"[MeSH] OR "HbA1c"[tiab])

# Combine
#1 AND #2 AND #3
```

Add field tags explicitly: `[tiab]` (title/abstract), `[Mesh]` (MeSH), `[pt]` (publication type), `[la]` (language). When a concept has no MeSH, rely on `[tiab]` and `[tw]` (text word) coverage.

### 4. Add limits deliberately

Limits are filters you accept because they buy precision; document every limit because each one excludes studies.

- **Date range** — state the inclusive start and end (e.g., 2014-01-01 to 2026-05-31). Update reviews often re-run with the same start and a rolling end.
- **Language** — restrict only with a justification; document the languages of searchers if you screen translations.
- **Publication type** — use `[pt]` to remove comments/editorials/news if appropriate.
- **Age** — animal-only, human-only, or age-bracket filters via MeSH (e.g., `"Adult"[Mesh]`).
- **Species** — `"Humans"[Mesh]` versus `"Animals"[Mesh]`.

Avoid "full text only" filters — they create a publisher-lock-in bias.

### 5. Translate across databases

Syntax differs. Build a translation table before searching.

| Concept | PubMed | Embase (Emtree) | Web of Science | Scopus | OpenAlex |
|---|---|---|---|---|---|
| Diabetes T2 | `"Diabetes Mellitus, Type 2"[MeSH]` | `'non insulin dependent diabetes mellitus'/exp` | `TS="Type 2 diabetes"` | `TITLE-ABS-KEY("type 2 diabetes")` | `title_and_abstract.search:"type 2 diabetes"` |
| GLP-1 RA | `"Glucagon-Like Peptide-1 Receptor Agonists"[MeSH]` | `'glucagon like peptide 1 receptor agonist'/exp` | `TS="GLP-1 receptor agonist*"` | `TITLE-ABS-KEY("GLP-1*")` | `title_and_abstract.search:"GLP-1"` |
| Weight loss | `"Weight Loss"[MeSH]` | `'weight reduction'/exp` | `TS="weight loss"` | `TITLE-ABS-KEY("weight loss")` | `title_and_abstract.search:"weight loss"` |

Field tags: PubMed uses brackets; Embase uses `/exp` for exploded terms; Web of Science uses `TS=`, `TI=`, `AB=`; Scopus uses `TITLE-ABS-KEY`; OpenAlex uses `title_and_abstract.search:`. Use a tool like the database's translation wizard when available, but always verify the translation by inspecting ~20 returned records.

### 6. Run, document, export

For each database, record in a single `search_log.md`:

- Database name, vendor/interface (e.g., PubMed via NLM, Embase via Elsevier), date searched (UTC), date range filter.
- Full search string as executed (copy/paste, not a paraphrase).
- Number of records retrieved, number after internal deduplication.
- Filters, language limits, and any export settings.

Export in a machine-readable format that survives a referee request: RIS, BibTeX, CSV, or JSON. Open indexes (OpenAlex, Semantic Scholar) give JSON directly.

### 7. Snowball and citation chasing

For each included study, perform forward and backward citation chasing.

- **Backward** — pull the reference list and re-screen titles.
- **Forward** — query "papers that cite X" in OpenAlex (`https://api.openalex.org/works?filter=cites:W<id>`), Semantic Scholar (`/paper/{id}/citations`), or Web of Science Cited References.
- **Related** — OpenAlex `related_to` and Semantic Scholar `/recommendations` find near-neighbours by embedding similarity.

Stop snowballing when one full iteration returns no new included studies (i.e., theoretical saturation on the citation graph).

### 8. Set up a citation alert

For a living search:

- **Google Scholar** — use the follow link on a search result page.
- **PubMed** — create an email/RSS alert from a saved search via the "Create RSS" icon.
- **OpenAlex** — poll a saved filter URL and diff the response; store the result in version control.
- **Semantic Scholar** — use the paper's `influentialCitationCount` field and a daily poll.
- **Web of Science** — use "Saved Searches and Alerts" with weekly cadence.

### 9. Report with PRISMA-S

PRISMA-S (the search extension to PRISMA 2020) defines 16 reporting items for the search. The minimum items to populate:

- Information sources (databases, registries, grey literature, citation chasing) with platform and date range.
- Full search strategies for every database, including any limits.
- Search filters (e.g., a validated filter for RCTs such as the Cochrane HSSS or InterTASC ISSG filters), with a citation.
- Peer review of the search strategy (PRESS 2015 checklist) by an information specialist.
- Update statement — date of the most recent search, planned update cadence.

Include a search log appendix and the raw search strings verbatim. A third party should be able to reproduce the count to within 5%.

## Code patterns

### PubMed via NCBI E-utilities

```python
from Bio import Entrez
import os, time, json

Entrez.email = os.environ["ENTREZ_EMAIL"]   # required by NCBI ToS
if "NCBI_API_KEY" in os.environ:
    Entrez.api_key = os.environ["NCBI_API_KEY"]

def pubmed_search(query: str, retmax: int = 10000) -> list[dict]:
    """Run a PubMed search; return list of {pmid, title, year, journal}."""
    with Entrez.esearch(db="pubmed", term=query, retmax=retmax, retmode="json") as r:
        ids = json.load(r)["esearchresult"]["idlist"]
    if not ids:
        return []
    time.sleep(0.34)  # ≤3 req/s without key, 0.1 with key
    with Entrez.esummary(db="pubmed", id=",".join(ids), retmode="json") as r:
        s = json.load(r)
    return [
        {
            "pmid": pmid,
            "title": s["result"][pmid]["title"],
            "year": s["result"][pmid]["pubdate"][:4],
            "journal": s["result"][pmid]["source"],
        }
        for pmid in ids
    ]

records = pubmed_search(
    '("Diabetes Mellitus, Type 2"[MeSH] OR "type 2 diabetes"[tiab]) '
    'AND ("Weight Loss"[MeSH] OR "weight loss"[tiab]) '
    'AND 2014:2026[dp]'
)
print(f"retrieved: {len(records)}")
```

### OpenAlex (open, no key required; polite pool with email)

```python
import requests, time

def openalex_search(query: str, per_page: int = 200, mailto: str | None = None) -> list[dict]:
    url = "https://api.openalex.org/works"
    params = {"search": query, "per_page": per_page}
    if mailto:
        params["mailto"] = mailto  # polite pool: higher rate limits
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()["results"]

def openalex_citing(openalex_id: str, mailto: str | None = None) -> list[str]:
    """Return OpenAlex IDs of works that cite the given work."""
    url = f"https://api.openalex.org/works"
    r = requests.get(url, params={"filter": f"cites:{openalex_id}",
                                  "per_page": 200, "mailto": mailto}, timeout=30)
    r.raise_for_status()
    return [w["id"] for w in r.json()["results"]]

# PubMed ↔ OpenAlex ID helper (PMIDs map to OpenAlex via the ids.openalex.org converter)
```

### Semantic Scholar (paper and citation graph)

```python
def s2_paper(paper_id: str, fields: str = "title,year,citationCount,references,citations") -> dict:
    """paper_id may be a DOI, PMID (with PMID: prefix), or arXiv ID (ARXIV: prefix)."""
    r = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}",
                     params={"fields": fields}, timeout=30)
    r.raise_for_status()
    return r.json()

def s2_citing(paper_id: str, limit: int = 500) -> list[str]:
    r = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations",
                     params={"fields": "paperId,title,year", "limit": limit}, timeout=30)
    r.raise_for_status()
    return [c["citingPaper"]["paperId"] for c in r.json()["data"]]
```

### Search log writer

```python
import json, datetime, pathlib

def append_search_log(outdir: pathlib.Path, db: str, query: str, n: int, filters: dict):
    log = outdir / "search_log.jsonl"
    with log.open("a") as f:
        f.write(json.dumps({
            "ts_utc": datetime.datetime.utcnow().isoformat(timespec="seconds"),
            "database": db,
            "query": query,
            "filters": filters,
            "n_results": n,
        }) + "\n")
```

### PRESS 2015 peer-review checklist (essentials)

Use the PRESS 2015 Evidence-Based Checklist to peer-review the search strategy before locking it. Items 1–6 cover the query structure; items 7–13 cover the operators and limits; items 14–16 cover the project fit. The checklist is freely available and a completed form is acceptable supplementary material for most journals.

## Common pitfalls

- **Searching only PubMed** — coverage is biomedical-heavy. Engineering, agriculture, and education are poorly served; use the domain table above.
- **Forgetting to translate MeSH to EMTREE** — Embase requires Emtree terms, not MeSH. PubMed auto-explodes MeSH; Embase does not auto-translate.
- **Reliance on a single synonym** — name variants, abbreviations, and trade names all need to be in the OR block.
- **Field tag over-restriction** — `[ti]` (title only) loses recall; `[tiab]` or `[tw]` is usually safer.
- **Limit by "full text"** — creates publisher lock-in; rely on `ors-literature-research-paper-lookup` to find an OA copy per record instead.
- **No PRESS review** — a non-specialist peer reviewing the strategy catches syntax errors and missed synonyms.
- **Snowballing once and stopping** — a single backward pass is not enough; iterate until saturation.
- **No date-stamped search log** — referees will ask; the search is not reproducible without one.
- **Mixing topic-specific filters with the strategy** — Cochrane HSSS, ISSG, and validated hedges should be quoted as named blocks, not edited into the topic query.
- **Ignoring grey literature and trial registries** — clinical questions need ClinicalTrials.gov, ICTRP, and the relevant regulator; grant questions need OAIster and base-search.net.

## Validation

- **Search log present** — `search_log.jsonl` (or `.md`) with one row per database, full query, result count, and date.
- **Reproducibility check** — re-run the most important database search on a different day and within a 5% delta.
- **PRESS review** — a second information specialist has signed off on the strategy using the PRESS 2015 checklist.
- **Coverage check** — known seed studies (5–10 papers the team agrees must be in the result) all appear in at least one database's output.
- **Recall sanity** — for a sensitive search, the number of records per database should be in the hundreds to low thousands; a search returning 12 records has over-filtered.
- **PRISMA-S items complete** — all 16 items answered, with appendix of raw strings.

## Open alternatives

| Commercial / paid | Open alternative | Trade-off |
|---|---|---|
| Web of Science | OpenAlex + Crossref + Semantic Scholar | OpenAlex has wider coverage but slightly noisier metadata |
| Scopus | OpenAlex | OpenAlex has near-complete coverage; Scopus has stronger affiliation data |
| Embase | PubMed + OpenAlex for pre-2026 work | Embase has unique drug/device indexing; supplement with clinical trial registries |
| Google Scholar (UI scraping) | OpenAlex (API), Semantic Scholar (API) | Open APIs rate-limit cleanly; Scholar scraping is brittle |
| Covidence (screening) | Rayyan (free tier) | Rayyan is free for academic use; ASReview is the open ML-assisted option |
| EndNote / Mendeley (manager) | Zotero | Zotero is free, open, has group libraries and 9k+ citation styles |
| CINAHL (paywalled) | PubMed + OpenAlex for allied health; CINAHL Complete via institutional access | No fully open equivalent; negotiate institutional access |

## References

Internal skills:
- `ors-literature-research-paper-lookup` — resolve DOIs/PMIDs/arXiv IDs to metadata, find OA copies.
- `ors-literature-research-citation-management` — Zotero / BibTeX pipeline, citation styles.
- `ors-literature-research-systematic-review` — PRISMA 2020 flow, screening, risk of bias, meta-analysis.
- `ors-literature-research-scoping-review` — JBI / Arksey-O'Malley framework.
- `ors-open-science-preprints` — bioRxiv / arXiv / medRxiv deposition after a search is run.

External sources:
- PRISMA 2020 statement and PRISMA-S search extension — prisma-statement.org
- Cochrane Handbook for Systematic Reviews of Interventions — training.cochrane.org/handbook
- PRESS 2015 Evidence-Based Checklist — cadth.ca/resources/finding-evidence/press
- PubMed Help and MeSH Browser — ncbi.nlm.nih.gov, meshb.nlm.nih.gov
- OpenAlex API — docs.openalex.org
- Semantic Scholar API — api.semanticscholar.org
- ISSG Search Filters Resource — ISSG.york.ac.uk
- JBI Manual for Evidence Synthesis — jbi-global

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Rewritten from the Bioinfoskill `literature-review` SKILL with a focus on the search (vs. synthesis) step, an open-index-first database table, PRISMA-S reporting, and code patterns using E-utilities, OpenAlex, and Semantic Scholar.
