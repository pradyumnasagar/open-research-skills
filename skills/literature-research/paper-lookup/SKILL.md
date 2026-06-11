---
name: paper-lookup
description: "Look up and resolve academic papers by DOI, PMID, arXiv ID, or title"
license: MIT
---



<!-- metadata:
category: literature-research
version: 1.0.0
author: Pradyumna Jayaram
tags:
- doi
- pmid
- crossref
- pubmed
- retraction-watch
- openalex
difficulty: beginner
prerequisites:
  tools:
  - python
  - requests
  - biopython (optional)
  skills: []
sources: 'Crossref API documentation (api.crossref.org); Adapted: DOI resolution and
  metadata; NCBI E-utilities (eutils.ncbi.nlm.nih.gov); Adapted: PMID and PMC ID handling;
  OpenAlex API (docs.openalex.org); Adapted: Open scholarly metadata; Semantic Scholar
  API (api.semanticscholar.org); Adapted: Citation graph and recommendations; Retraction
  Watch database (retractionwatch.com); Adapted: Retraction status checking; arXiv
  API (arxiv.org/help/api); Adapted: Preprint lookup; ORCID (orcid.org); Adapted:
  Author disambiguation'
-->

# Paper Lookup and Resolution

> Finding a specific paper is the most common task in literature research, but it's harder than it should be. A DOI might be broken, a PMID might map to a retracted paper, an arXiv preprint might have evolved into a journal article, and authors with common names create ambiguity. This skill provides the tools and APIs to resolve papers reliably, check their status, and trace their citation relationships.

## When to use

- Resolving a DOI, PMID, PMC ID, or arXiv ID to full metadata
- Finding the latest version of a paper that has evolved from preprint to published
- Checking if a paper has been retracted or has an expression of concern
- Looking up forward citations (papers that cite X)
- Disambiguating authors with common names using ORCID
- Finding open access (OA) versions of paywalled papers
- Resolving incomplete citations to complete bibliographic entries
- Finding related papers by topic similarity or citation graph

## When NOT to use

- Conducting a comprehensive literature search — use `ors-literature-research-literature-search` instead
- Managing your reference library — use `ors-literature-research-citation-management` instead
- Performing systematic review screening — use `ors-literature-research-systematic-review` instead
- Reading and annotating PDFs — use a PDF reader or Zotero
- Evaluating paper quality or peer review status — different from paper lookup

## Prerequisites

- Python 3.8+ with `requests` library (or equivalent HTTP client)
- Internet connection to query APIs
- A text file or spreadsheet with identifiers to look up
- Optional: NCBI API key for higher rate limits (3 req/s with key, 3 req/s without)
- Optional: OpenAlex polite pool email for higher rate limits
- Optional: Semantic Scholar API key for higher rate limits (100 req/s with key)

## Core workflow

### 1. Identify the identifier type

Common academic paper identifiers:

- **DOI** (Digital Object Identifier): `10.1038/nature12373` — publisher-assigned, persistent
- **PMID** (PubMed ID): `23842501` — NLM-assigned, biomedical focus
- **PMCID** (PubMed Central ID): `PMC3746950` — NLM full-text archive
- **arXiv ID**: `2301.12345` or `cs.LG/0301001` — preprint server
- **bioRxiv DOI**: `10.1101/2023.01.01.123456` — preprint DOI
- **OpenAlex ID**: `W2741809807` — OpenAlex internal ID
- **Semantic Scholar ID**: `DOI:10.1038/nature12373` or custom hash
- **ORCID** (for authors): `0000-0002-1825-0097`

### 2. Choose the right API

| Need | API | Notes |
|------|-----|-------|
| DOI → metadata | Crossref | Comprehensive, open, no key needed |
| DOI → OA PDF | Unpaywall | Open API, OA detection |
| PMID → metadata | NCBI E-utilities | PubMed, no key needed (3 req/s) |
| Broad metadata | OpenAlex | Open, comprehensive, no key needed |
| Citations, recommendations | Semantic Scholar | Open, good for citation graph |
| Preprint → journal version | OpenAlex, Crossref | Use `is-referenced-by` chain |
| Retraction status | Retraction Watch | API or database download |
| Author disambiguation | ORCID, OpenAlex | ORCID for canonical IDs |
| arXiv preprint | arXiv API | Direct query |

### 3. Resolve DOI via Crossref

```python
import requests

def resolve_doi(doi):"
    """Resolve DOI to metadata via Crossref API."""
    url = f"https://api.crossref.org/works/{doi}"
    headers = {"User-Agent": "OpenResearchSkill/1.0 (mailto:user@example.com)"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()["message"]
    
    return {
        "doi": doi,
        "title": data.get("title", [""])[0],
        "authors": [
            f"{a.get('family', '')}, {a.get('given', '')}"
            for a in data.get("author", [])
        ],
        "year": data.get("published", {}).get("date-parts", [[None]])[0][0],
        "journal": data.get("container-title", [""])[0],
        "volume": data.get("volume"),
        "issue": data.get("issue"),
        "pages": data.get("page"),
        "type": data.get("type"),
        "url": data.get("URL"),
        "is_referenced_by_count": data.get("is-referenced-by-count", 0)
    }
```

### 4. Resolve PMID via NCBI E-utilities

```python
from Bio import Entrez
import os

Entrez.email = os.environ.get("ENTREZ_EMAIL", "user@example.com")
if "NCBI_API_KEY" in os.environ:
    Entrez.api_key = os.environ["NCBI_API_KEY"]

def resolve_pmid(pmid):
    """Resolve PMID to metadata via PubMed."""
    with Entrez.efetch(db="pubmed", id=pmid, retmode="xml") as r:
        record = Entrez.read(r)
    article = record["PubmedArticle"][0]["MedlineCitation"]
    
    return {
        "pmid": pmid,
        "title": str(article["Article"]["ArticleTitle"]),
        "authors": [
            f"{a.get('LastName', '')} {a.get('ForeName', '')}"
            for a in article["Article"].get("AuthorList", [])
        ],
        "year": article["Article"]["Journal"]["JournalIssue"]["PubDate"].get("Year"),
        "journal": str(article["Article"]["Journal"]["Title"]),
        "volume": article["Article"]["Journal"]["JournalIssue"].get("Volume"),
        "issue": article["Article"]["Journal"]["JournalIssue"].get("Issue"),
        "pages": article["Article"].get("Pagination", {}).get("MedlinePgn"),
        "mesh_terms": [str(t["DescriptorName"]) 
                      for t in article.get("MeshHeadingList", [])]
    }
```

### 5. Query OpenAlex for comprehensive metadata

```python
import requests

def openalex_lookup(doi_or_pmid, mailto="user@example.com"):
    """Lookup paper in OpenAlex by DOI or PMID."""
    if doi_or_pmid.startswith("10."):
        # DOI lookup
        url = f"https://api.openalex.org/works/doi:{doi_or_pmid}"
    else:
        # PMID lookup
        url = f"https://api.openalex.org/works/pmid:{doi_or_pmid}"
    
    response = requests.get(url, 
                          params={"mailto": mailto}, 
                          timeout=30)
    response.raise_for_status()
    data = response.json()
    
    return {
        "openalex_id": data["id"],
        "doi": data.get("doi"),
        "pmid": data.get("ids", {}).get("pmid"),
        "title": data.get("title"),
        "authors": [
            a["author"]["display_name"] 
            for a in data.get("authorships", [])
        ],
        "year": data.get("publication_year"),
        "venue": data.get("primary_location", {}).get("source", {}).get("display_name"),
        "cited_by_count": data.get("cited_by_count", 0),
        "is_oa": data.get("open_access", {}).get("is_oa", False),
        "oa_url": data.get("open_access", {}).get("oa_url"),
        "type": data.get("type")
    }
```

### 6. Find forward citations (papers that cite X)

```python
def get_citing_papers(openalex_id, mailto="user@example.com", limit=100):
    """Get papers that cite a given paper."""
    url = "https://api.openalex.org/works"
    params = {
        "filter": f"cites:{openalex_id}",
        "per_page": limit,
        "mailto": mailto
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()["results"]

# Via Semantic Scholar
def s2_citations(paper_id, limit=500):
    """Get citations via Semantic Scholar."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations"
    params = {"fields": "title,year,authors,citationCount", "limit": limit}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return [c["citingPaper"] for c in response.json()["data"]]
```

### 7. Find related papers

```python
def get_related_papers(openalex_id, mailto="user@example.com", limit=10):
    """Get papers related to a given paper (via OpenAlex)."""
    url = f"https://api.openalex.org/works/{openalex_id}"
    response = requests.get(url, params={"mailto": mailto}, timeout=30)
    response.raise_for_status()
    work = response.json()
    
    related_ids = work.get("related_works", [])[:limit]
    if not related_ids:
        return []
    
    # Fetch related papers in batch
    pipe_ids = "|".join(related_ids)
    url2 = "https://api.openalex.org/works"
    params = {
        "filter": f"openalex_id:{pipe_ids}",
        "per_page": limit,
        "mailto": mailto
    }
    response = requests.get(url2, params=params, timeout=30)
    response.raise_for_status()
    return response.json()["results"]

# Via Semantic Scholar recommendations
def s2_recommendations(paper_id, limit=10):
    """Get paper recommendations via Semantic Scholar."""
    url = f"https://api.semanticscholar.org/recommendations/v1/papers/"
    params = {"fields": "title,year,authors,abstract", "limit": limit}
    # POST request with positive paper IDs
    payload = {"positivePaperIds": [paper_id]}
    response = requests.post(url, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["recommendedPapers"]
```

### 8. Check retraction status

Always verify a paper's status before citing it, especially for clinical or policy work.

```python
import requests

def check_retraction(doi=None, pmid=None, title=None):
    """
    Check if a paper has been retracted using Crossref or 
    Retraction Watch data.
    """
    if doi:
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()["message"]
            # Check for retraction update
            for update in data.get("update-to", []):
                if update.get("type") == "retraction":
                    return {
                        "retracted": True,
                        "reason": update.get("reason"),
                        "update_date": update.get("updated", {}).get("date-parts")
                    }
    
    # Cross-publisher retraction checking via Retraction Watch
    # Note: Retraction Watch API requires registration
    # Alternative: Use Crossref's retraction status or check publishers
    return {"retracted": False}

# For Retraction Watch database (requires API key):
# def check_retraction_watch(doi, api_key):
#     url = f"https://api.retractionwatch.org/v1/doi/{doi}"
#     headers = {"Authorization": f"Bearer {api_key}"}
#     response = requests.get(url, headers=headers, timeout=30)
#     return response.json() if response.status_code == 200 else None
```

### 9. Find preprint versions

```python
def find_preprint_version(doi, mailto="user@example.com"):
    """
    Find if a published paper has a preprint version.
    Uses OpenAlex's work relationships.
    """
    url = f"https://api.openalex.org/works/doi:{doi}"
    response = requests.get(url, params={"mailto": mailto}, timeout=30)
    response.raise_for_status()
    work = response.json()
    
    # Check for related works that might be preprints
    related = work.get("related_works", [])
    preprint_versions = []
    
    for rel_id in related:
        rel_url = f"https://api.openalex.org/works/{rel_id}"
        rel_response = requests.get(rel_url, 
                                   params={"mailto": mailto}, 
                                   timeout=30)
        if rel_response.status_code == 200:
            rel_work = rel_response.json()
            if rel_work.get("type") in ["preprint", "article"]:
                preprint_versions.append({
                    "doi": rel_work.get("doi"),
                    "type": rel_work.get("type"),
                    "year": rel_work.get("publication_year"),
                    "title": rel_work.get("title")
                })
    
    return preprint_versions

# arXiv-specific lookup
def arxiv_lookup(arxiv_id):
    """Look up arXiv preprint."""
    url = "http://export.arxiv.org/api/query"
    params = {"id_list": arxiv_id, "max_results": 1}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    # Parse Atom XML response
    return response.text
```

### 10. Disambiguate authors

```python
def lookup_orcid(orcid):
    """Fetch author profile from ORCID."""
    url = f"https://pub.orcid.org/v3.0/{orcid}/record"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    name = data.get("person", {}).get("name", {})
    given = name.get("given-names", {}).get("value", "")
    family = name.get("family-name", {}).get("value", "")
    
    # Get works
    works_url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    works_response = requests.get(works_url, 
                                 headers=headers, 
                                 timeout=30)
    works_data = works_response.json()
    
    return {
        "orcid": orcid,
        "name": f"{given} {family}",
        "works_count": len(works_data.get("group", [])),
        "url": f"https://orcid.org/{orcid}"
    }

# Find ORCID by author name (via OpenAlex)
def find_author_orcid(author_name, mailto="user@example.com"):
    """Search for author ORCID via OpenAlex."""
    url = "https://api.openalex.org/authors"
    params = {"search": author_name, "mailto": mailto, "per_page": 5}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    results = response.json()["results"]
    
    return [
        {
            "openalex_id": a["id"],
            "name": a["display_name"],
            "orcid": a.get("orcid"),
            "works_count": a.get("works_count", 0),
            "institution": a.get("last_known_institutions", [{}])[0].get("display_name")
        }
        for a in results
    ]
```

## Code patterns

### Batch lookup from a CSV file

```python
import csv
import time

def batch_lookup(input_csv, output_csv, id_column="doi"):
    """
    Look up metadata for all IDs in a CSV file.
    """
    results = []
    with open(input_csv, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    for i, row in enumerate(rows):
        identifier = row[id_column].strip()
        if not identifier:
            continue
        
        try:
            if identifier.startswith("10."):
                metadata = resolve_doi(identifier)
            elif identifier.isdigit():
                metadata = resolve_pmid(identifier)
            else:
                continue
            
            metadata.update({k: v for k, v in row.items() if k != id_column})
            results.append(metadata)
        except Exception as e:
            print(f"Error on row {i}: {identifier} - {e}")
        
        # Rate limiting: 0.34s for NCBI, 0.1s for OpenAlex
        time.sleep(0.1)
        
        # Progress reporting
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1}/{len(rows)}")
    
    # Write results
    with open(output_csv, "w", newline="") as f:
        if results:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
```

### Resolve DOI to BibTeX

```python
def doi_to_bibtex(doi):
    """Generate BibTeX entry from DOI via Crossref."""
    metadata = resolve_doi(doi)
    
    # Determine entry type
    type_map = {
        "journal-article": "article",
        "book": "book",
        "book-chapter": "incollection",
        "proceedings-article": "inproceedings",
        "report": "techreport"
    }
    entry_type = type_map.get(metadata["type"], "article")
    
    # Generate citation key
    first_author = metadata["authors"][0].split(",")[0] if metadata["authors"] else "Unknown"
    cite_key = f"{first_author.lower()}{metadata['year']}"
    
    # Format authors for BibTeX
    bib_authors = " and ".join(metadata["authors"])
    
    # Build BibTeX
    bibtex = f"@{entry_type}{{{cite_key},\n"
    bibtex += f"  author = {{{bib_authors}}},\n"
    bibtex += f"  title = {{{{{metadata['title']}}}}},\n"
    bibtex += f"  journal = {{{metadata['journal']}}},\n"
    bibtex += f"  year = {{{metadata['year']}}},\n"
    if metadata.get("volume"):
        bibtex += f"  volume = {{{metadata['volume']}}},\n"
    if metadata.get("issue"):
        bibtex += f"  number = {{{metadata['issue']}}},\n"
    if metadata.get("pages"):
        bibtex += f"  pages = {{{metadata['pages']}}},\n"
    bibtex += f"  doi = {{{metadata['doi']}}},\n"
    bibtex += "}"
    
    return bibtex
```

### Find open access PDF

```python
def find_oa_pdf(doi, email="user@example.com"):
    """
    Find open access PDF via Unpaywall API.
    """
    url = f"https://api.unpaywall.org/v2/{doi}"
    params = {"email": email}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    if data.get("is_oa"):
        best_oa = data.get("best_oa_location", {})
        return {
            "is_oa": True,
            "pdf_url": best_oa.get("url_for_pdf"),
            "landing_page": best_oa.get("url"),
            "license": best_oa.get("license"),
            "host_type": best_oa.get("host_type"),
            "repository": best_oa.get("repository_institution")
        }
    return {"is_oa": False}
```

## Common pitfalls

- **Not checking retraction status**: Citing retracted papers undermines credibility
- **Confusing preprint and journal versions**: Always check if a preprint has been published
- **Ignoring author ambiguity**: Common names can refer to multiple researchers
- **Rate limit violations**: NCBI allows 3 req/s without key; OpenAlex similar
- **DOI resolution failures**: Some DOIs are broken or point to deleted papers
- **Incomplete metadata**: Some APIs return partial data; cross-check with multiple sources
- **Not handling errors**: APIs fail; need retry logic and graceful degradation
- **Assuming OA is unavailable**: Always check Unpaywall before giving up on a paywalled paper
- **Not storing identifiers**: Always save DOI/PMID even if other metadata is incomplete
- **Ignoring version differences**: arXiv versions matter; preprint → published may differ
- **Missing expressions of concern**: Papers with concerns may not be fully retracted
- **Copyright issues with PDFs**: OA ≠ free to redistribute; check licenses

## Validation

- **Metadata complete**: Title, authors, year, venue all present
- **DOI resolves correctly**: Both via Crossref and doi.org redirect
- **PMID present for biomedical papers**: Check PubMed for clinical/biomedical topics
- **OA version found**: For at least 30% of recent papers, OA version available
- **Retraction status checked**: Especially for clinical guidelines, policy work
- **Citation count reasonable**: New papers (< 1 year) should have lower counts
- **Author disambiguation verified**: ORCID confirms author identity
- **Preprint → journal version tracked**: Both versions cited appropriately
- **References and citations fetched**: Forward citation list is available
- **Related papers found**: At least 5–10 related papers for context

## Open alternatives

| Commercial / paid | Open alternative | Trade-off |
|---|---|---|
| Web of Science lookup | OpenAlex + Crossref | OpenAlex has broader coverage; WoS has curated data |
| Scopus lookup | OpenAlex | OpenAlex is free, no API limits for basic use |
| Dimensions | OpenAlex | OpenAlex is fully open; Dimensions has institutional features |
| Microsoft Academic (discontinued) | OpenAlex | OpenAlex picked up MA's coverage |
| Google Scholar (UI scraping) | OpenAlex API, Semantic Scholar API | APIs are stable; Scholar scraping breaks frequently |
| Lens.org (paid tier) | Lens.org (free tier), OpenAlex | Lens.org has patent data; OpenAlex is open |

## References

Internal skills:
- `ors-literature-research-literature-search` — uses DOI/PMID lookups for paper resolution
- `ors-literature-research-citation-management` — stores looked-up papers in library
- `ors-literature-research-systematic-review` — uses lookups for screening and inclusion
- `ors-open-science-preprints` — uses preprint lookups for tracking
- `ors-research-grants` — uses paper lookups for grant proposals

External sources:
- Crossref API — api.crossref.org
- DOI Foundation — doi.org
- NCBI E-utilities — eutils.ncbi.nlm.nih.gov
- PubMed — pubmed.ncbi.nlm.nih.gov
- OpenAlex — docs.openalex.org
- Semantic Scholar API — api.semanticscholar.org
- arXiv API — arxiv.org/help/api
- Unpaywall API — unpaywall.org/api/v2
- Retraction Watch — retractionwatch.com
- ORCID — info.orcid.org/documentation
- bioRxiv API — api.biorxiv.org

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Rewritten from Bioinfoskill `paper-lookup` with modern API examples (Crossref, OpenAlex, Semantic Scholar), retraction checking, preprint version tracking, ORCID-based author disambiguation, and batch lookup utilities.