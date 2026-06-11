---
name: citation-management
description: "Set up and use reference managers (Zotero, Mendeley, EndNote) with citation
  styles, group libraries, PDF annotation, DOI/PMID workflows, and BibTeX export for
  reproducible research.
license: MIT
---

<!-- metadata:
category: literature-research
version: 1.0.0
author: Pradyumna Jayaram
tags:
- zotero
- mendeley
- bibtex
- citation-style
- doi
- reference-manager
difficulty: beginner
prerequisites:
  tools:
  - Zotero 6+
  - ZotFile/Zotero PDF Translate
  - Better BibTeX
  - RStudio/VSCode (optional)
  skills: []
sources: 'Zotero documentation and community guides (zotero.org/support); Adapted:
  Integration with literature research workflow; Citation Style Language specification
  (citationstyles.org); Adapted: Format examples and CSL editing; Better BibTeX for
  Zotero (retorque.re/zotero-better-bibtex); Adapted: Modern export patterns; DOI
  resolution via doi.org and Crossref (crossref.org); Adapted: Programmatic DOI workflows;
  APA 7th Edition Style Guide, Vancouver Style guidelines; Adapted: Modern format
  examples'
-->

# Citation and Reference Management

> Reference management is the scaffolding of reproducible research. A well-organized library saves hundreds of hours across a career, enables collaboration through group libraries, and ensures that citations are accurate in any document. This skill covers the full reference manager stack: from initial setup through export formats, citation styles, and PDF organization for modern research workflows.

## When to use

- Starting a new research project and need to organize references systematically
- Collaborating with co-authors on a manuscript, grant, or systematic review
- Migrating from one reference manager to another (e.g., EndNote to Zotero)
- Setting up automated workflows: cite-while-you-write, version control integration
- Managing PDFs and annotations across hundreds or thousands of papers
- Generating bibliographies in specific citation styles (APA, Vancouver, Nature, etc.)
- Preparing data exports for systematic reviews, meta-analyses, or PRISMA diagrams
- Creating backup and version control of your reference library

## When NOT to use

- Looking up a single paper by DOI — use `ors-literature-research-paper-lookup` instead
- Conducting a systematic review's screening process — use `ors-literature-research-systematic-review` instead
- Writing a manuscript in LaTeX/Word — this skill is about *managing* references, not the manuscript itself
- Managing code repositories — use Git, not a reference manager
- Cloud document management — use Dropbox, Google Drive, etc., not a reference manager

## Prerequisites

- A working directory structure: `library/` for the main Zotero library, `pdfs/` for PDF storage
- Cloud storage account (optional but recommended): 5–10 GB free cloud storage (Google Drive, OneDrive, iCloud)
- Backup strategy: Zotero library is a SQLite database + files, needs regular backup
- Basic understanding of citation formats (APA, MLA, Chicago, Vancouver)
- LaTeX installation (optional, for BibTeX workflows)

## Core workflow

### 1. Choose your reference manager

Three major options, each with strengths:

| Tool | License | Cost | Strengths | Limitations |
|------|---------|------|-----------|-------------|
| Zotero | Open source (AGPL) | Free (300 MB cloud) | Extensible, open, group libraries, 9000+ citation styles, PDF reader, OCR | Cloud storage limited (can buy more) |
| Mendeley | Proprietary | Free (2 GB) | Elsevier integration, PDF reader, mobile app | Owned by Elsevier, limited export formats, 2 GB limit |
| EndNote | Proprietary | $250+ (institutional licenses common) | Mature, institutional adoption, publisher integrations | Expensive, not open, platform lock-in |

**Recommendation**: Zotero for academic research due to open-source nature, extensibility, and cost. Migrate from other managers if possible.

### 2. Set up Zotero

Download Zotero 6+ from zotero.org. Configure:

1. **File → Preferences → General**:
   - Set data directory to a location with backup
   - Enable automatic file renaming

2. **Install recommended plugins**:
   - **Better BibTeX**: Auto-generate citation keys, prevent duplicates
   - **ZotFile** or **Zotero PDF Translate**: PDF management, translation
   - **Zotero PDF Reader**: Built-in reader with OCR and annotations

3. **Set up sync** (optional but recommended):
   - Zotero cloud: 300 MB free, $20/year for 2 GB
   - Alternative: Sync via WebDAV (Nextcloud) or Git
   - Or: Manual backup of Zotero data directory

### 3. Import and organize references

Import references from:

- **DOI**: Drag a DOI into Zotero, or right-click → Add Item by Identifier
- **PubMed**: Use the magic wand icon in browser connector
- **Web pages**: Use browser connector to save web pages
- **PDF files**: Drag PDFs into Zotero — metadata auto-extracted
- **Manual entry**: Add Item button for book chapters, reports, etc.

Organize with **Collections** (folders):

```
Library/
├── by-project/
│   ├── systematic-review-diabetes/
│   ├── grant-application-2026/
│   └── manuscript-xyz/
├── by-topic/
│   ├── machine-learning/
│   ├── genomics/
│   └── clinical-trials/
├── by-status/
│   ├── to-read/
│   ├── reading/
│   ├── cited/
│   └── background/
└── shared/
    └── lab-group-library/
```

### 4. Manage PDFs and annotations

Configure PDF management:

1. **Set up linked attachments** (recommended for large libraries):"
   - Settings → Files and Folders → Custom "Linked Attachment Base Directory"
   - Store PDFs in `pdfs/` folder, version controlled

2. **Enable Zotero PDF Reader** (Zotero 6+):
   - Built-in reader with highlighting, annotations, image extraction
   - OCR for scanned PDFs
   - Sync annotations across devices

3. **Annotation workflows**:
   - Highlight key findings, methodology, limitations
   - Tag annotations by type (methods, results, limitations)
   - Export annotations for literature review summaries

### 5. Configure citation styles

Zotero ships with 9,000+ citation styles. To use a specific style:

1. **Install new style**:
   - Settings → Cite → Styles → Get additional styles
   - Search by name (e.g., "American Psychological Association 7th")
   - Or paste CSL URL: `https://citationstyles.org/`

2. **Common biomedical styles**:
   - Vancouver: `nlm-citation-style`
   - APA 7: `apa-7th-edition`
   - Nature: `nature`
   - Cell: `cell`
   - Science: `science`
   - Chicago: `chicago-author-date`

3. **Customize styles** (advanced):
   - Edit CSL files directly (XML format)
   - Use Visual CSL Editor: `https://editor.citationstyles.org/`
   - Fork existing styles to create custom variants

### 6. Cite-while-you-write integration

#### Word Integration
- Zotero toolbar in Word: Add/Edit Citation, Edit Bibliography, Refresh
- Add in-text citations: Type citation key or search by author/title
- Generate bibliography at end of document
- Update citations when library changes

#### LaTeX integration (with Better BibTeX)
- Generate unique citation keys automatically
- Export to `.bib` file
- Use `\cite{key}` in LaTeX

```latex
\documentclass{article}
\usepackage[backend=biber, style=nature]{biblatex}
\addbibresource{references.bib}

\begin{document}
Recent work by \cite{smith2023diabetes} shows...
\printbibliography
\end{document}
```

#### Quarto/Markdown integration
- Use `bibliography:` field in YAML header
- Zotero exports to `.bib` or `.yaml` (CSL-JSON) format

```yaml
---
title: "My Analysis"
bibliography: references.bib
format: html
---
```

### 7. Export and sharing

#### Export formats
- **BibTeX (.bib)**: LaTeX, R Markdown, Quarto
- **CSL JSON (.json)**: Pandoc, academic tools
- **RIS (.ris)**: Legacy format, some tools
- **EndNote XML**: EndNote compatibility
- **CSV**: Custom scripts, meta-analysis tools

Configure Better BibTeX auto-export:

1. Right-click collection → "Export Collection"
2. Format: "Better BibLaTeX" or "Better BibTeX"
3. Check "Export Notes" and "Export Files"
4. Set "On Change" to keep `.bib` file updated

#### Group libraries for collaboration
- Create group library (zotero.org/groups)
- Add co-authors with read/write permissions
- Share via link for read-only access
- Useful for lab groups, systematic reviews, manuscript co-authors

### 8. DOI and PMID management

#### Adding by DOI
```
Right-click → Add Item by Identifier → paste DOI
```

#### Programmatic DOI resolution
```python
import requests
import re

def doi_to_metadata(doi):
    """Fetch metadata from Crossref API."""
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()["message"]
    
    return {
        "title": data.get("title", [""])[0],
        "authors": [f"{a.get('family', '')}, {a.get('given', '')}" 
                    for a in data.get("author", [])],
        "year": data.get("published", {}).get("date-parts", [[None]])[0][0],
        "journal": data.get("container-title", [""])[0],
        "doi": doi
    }
```

#### Importing from PubMed
- Install Zotero browser connector
- On PubMed search results, click Zotero connector icon
- Select references to import

#### Finding PDFs
- Right-click item → "Find Available PDF" (uses DOI, Unpaywall)
- Configure proxy for institutional access
- Manual: right-click → "Attach Linked File" or "Attach Stored Copy"

### 9. Backups and version control

#### Zotero library backup
- Library = SQLite database + files in data directory
- Back up entire data directory regularly
- Use Time Machine (macOS), File History (Windows), or rsync (Linux)
- Cloud sync (Zotero or WebDAV) is automatic backup

#### Version control for `.bib` files
- Export collection to `.bib` in Git-tracked directory
- Commit changes with descriptive messages
- Review diff to see added/removed/modified citations

```bash
git add references.bib
git commit -m "Add 15 new citations from systematic review search"
```

### 10. Migration between managers

#### From EndNote to Zotero
1. EndNote: File → Export → EndNote XML
2. Zotero: File → Import
3. Verify all references transferred correctly
4. Check for missing attachments

#### From Mendeley to Zotero
1. Mendeley: Tools → Options → Mendeley Web Importer
2. Zotero: File → Import → "Mendeley Database" or RIS
3. Use Zotero's Mendeley importer (built-in)

#### Preserving citation keys
- Better BibTeX maintains stable citation keys across sessions
- Export from old manager with keys, import to Zotero
- Verify keys match before deleting old library

## Code patterns

### Better BibTeX export configuration

```javascript
// Better BibTeX settings (JSON config in Zotero)
{
  "citeKeyFormat": "auth+year",
  "citeKeyFormatAuthor": "LastName",
  "citeKeyFormatYear": "4-digit-year",
  "citeKeyTitle": 0,  // 0 = no title
  "citeKeyLowercase": "lower",
  "citeKeyReplace": "_",  // Replace spaces with underscores
  "citeKeyRemoveDiacritics": true,
  "autoPin": false  // Auto-pin citation keys
}
```

### Programmatic import to Zotero via pyzotero

```python
from pyzotero import zotero

# Connect to personal library
zot = zotero.Zotero(library_id, 'user', api_key)

# Add an item by DOI
zot.add_items([{
    "itemType": "journalArticle",
    "DOI": "10.1038/s41586-2020-1234",
    "url": "https://doi.org/10.1038/s41586-2020-1234"
}])

# Get all items in a collection
items = zot.collection_items("ABCD1234")
for item in items:
    print(item["data"]["title"])
```

### CSL style snippet (APA 7th, simplified)

```xml
<style xmlns="http://purl.org/net/xbiblio/csl" 
       class="in-text" 
       version="1.0">
  <info>
    <title>American Psychological Association 7th edition</title>
    <id>http://www.zotero.org/styles/apa-7th-edition</id>
    <link href="http://www.zotero.org/styles/apa-7th-edition" 
          rel="self"/>
  </info>
  <citation>
    <layout prefix="(" suffix=")" delimiter="; ">
      <group delimiter=", ">
        <names variable="author">
          <name form="short" and="text" 
                initialize-with=". " 
                delimiter=", "/>
        </names>
        <date variable="issued">
          <date-part name="year"/>
        </date>
      </group>
    </layout>
  </citation>
  <bibliography>
    <layout suffix=".">
      <names variable="author" delimiter=", "/>
      <date variable="issued" prefix=" (" suffix=")">
        <date-part name="year"/>
      </date>
    </layout>
  </bibliography>
</style>
```

### LaTeX BibTeX entry example

```bibtex
@article{smith2023diabetes,
  author  = {Smith, John A. and Doe, Jane B.},
  title   = {Effects of GLP-1 agonists on type 2 diabetes outcomes},
  journal = {Nature Medicine},
  year    = {2023},
  volume  = {29},
  number  = {5},
  pages   = {1234--1245},
  doi     = {10.1038/s41591-2023-0123-4},
  pmid    = {37212345}
}
```

### R Markdown/Quarto bibliography setup

```yaml
---
title: "My Analysis"
output: html_document
bibliography: references.bib
csl: nature.csl
---
```

Download CSL files from `https://github.com/citation-style-language/styles`.

## Common pitfalls

- **Not backing up regularly**: Loss of library is catastrophic; set up automatic backups
- **Mixing multiple citation managers**: Creates duplicate citations and confusion
- **Ignoring metadata quality**: Missing fields lead to incomplete citations
- **Not using collections**: A flat library becomes unmanageable above 1000 references
- **Cloud sync not configured**: Limits device access and creates backup risk
- **Citation keys changing unexpectedly**: Use Better BibTeX's "pin" feature for stable keys
- **PDF organization in wrong place**: Don't let PDFs accumulate in Zotero storage if you need manual control
- **Not removing duplicates**: Duplicates from multiple imports cause citation errors
- **Ignoring version control for exports**: `.bib` files should be in Git for reproducibility
- **Manual citation editing**: Always use citation tools, never edit Word/LaTeX citations by hand
- **PDF annotations lost on re-import**: Sync annotations to avoid losing them

## Validation

- **Backup present**: Regular backups of Zotero data directory
- **Cloud sync working**: Library accessible from multiple devices
- **All references have DOIs/PMIDs**: Easy to verify and re-find
- **Citation style configured**: Bibliography generates in target format
- **Cite-while-you-write working**: Citations insert in Word/LaTeX without errors
- **Duplicate check passed**: No duplicate references in library
- **Group library permissions verified**: Co-authors have appropriate access
- **PDFs attached and accessible**: No missing files or broken links
- **Citation keys stable**: Keys don't change unexpectedly (with Better BibTeX)
- **Exports work correctly**: `.bib`, RIS, CSL JSON files generate without errors

## Open alternatives

| Commercial / paid | Open alternative | Trade-off |
|---|---|---|
| EndNote | Zotero | Zotero is free, open, has 9000+ styles; EndNote has institutional adoption |
| Mendeley (Elsevier) | Zotero | Zotero is not owned by publisher; Mendeley has mobile app but limited exports |
| Paperpile (Google Docs) | Zotero + Google Docs integration | Paperpile is paid; Zotero has limited Google Docs integration |
| ReadCube Papers | Zotero with PDF reader | ReadCube has better mobile app; Zotero has better library organization |
| RefWorks (ProQuest) | Zotero with group libraries | RefWorks is institutional; Zotero groups are free for any size |

## References

Internal skills:
- `ors-literature-research-literature-search` — search strategies to feed into library
- `ors-literature-research-paper-lookup` — find specific papers to add to library
- `ors-literature-research-systematic-review` — uses exported library for screening
- `ors-open-science-preprints` — tracks preprints added to library
- `ors-scientific-writing` — uses Zotero for manuscript citations

External sources:
- Zotero documentation — zotero.org/support
- Better BibTeX documentation — retorque.re/zotero-better-bibtex
- Citation Style Language — citationstyles.org
- Crossref API — api.crossref.org
- pyzotero documentation — pyzotero.readthedocs.io
- DOI resolution — doi.org
- Unpaywall API — unpaywall.org
- APA Style — apastyle.apa.org
- Vancouver Style — nlm.nih.gov/bsd/uniform_requirements.html
- Nature citation style — nature.com/nature-portfolio/editorial-policies/citation-style

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Updated from Bioinfoskill `reference-management` with focus on Zotero as primary tool, modern PDF annotation workflows, Better BibTeX integration for version control, DOI/PMID management with programmatic examples, and CSL style customization.