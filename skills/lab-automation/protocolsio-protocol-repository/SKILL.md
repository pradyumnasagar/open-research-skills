---
name: protocolsio-protocol-repository
description: "Search and download published wet-lab protocols from protocols.io REST API. Find 90,000+ community protocols by keyword, DOI, or filter; extract steps, reagents, materials, timing, equipment. Free for public protocols. Use to build automation with opentrons-protocol-api or record runs in an ELN."
license: MIT
---



<!-- metadata:
category: ''
version: 1.0.0
author: Pradyumna Jayaram
tags: []
difficulty: beginner
sources: SciAgent-Skills-main/skills/lab-automation/protocolsio-integration/SKILL.md
-->

# protocols.io Protocol Repository

## Overview

protocols.io is the world's largest open repository of experimental protocols with 90,000+ submissions across molecular biology, biochemistry, cell biology, bioinformatics, clinical research, lab automation, and microfluidics. The REST API enables programmatic access to search the database, retrieve complete protocol details (steps, reagents, materials, timing), browse version history, and discover community-adapted protocols. Public protocols are freely accessible without authentication; OAuth2 tokens are needed for private protocols or creating new protocols. API responses return structured data that can be integrated directly into automation scripts, ELN entries, or protocol editors.

Author: Pradyumna Jayaram.

## When to Use

- Finding peer-reviewed, field-tested protocols by technique, reagent, or paper DOI
- Extracting detailed reagent lists, timing steps, and equipment lists for protocol implementation
- Building lab automation workflows by adapting community-validated methods
- Getting real-world tips and error notes that are not in vendor manuals
- Citing the specific version DOI in methods sections for reproducibility
- Discovering open alternatives to commercial kits or proprietary methods
- Using alongside `opentrons-protocol-api` to convert published protocols into Python scripts
- For writing and publishing your own protocols, use the protocols.io web interface

## Prerequisites

- **Python packages**: `requests`, `pandas`
- **Data requirements**: protocol keywords, DOIs, or protocol IDs for retrieval
- **Environment**: Internet connection
- **Rate limits**: 10 requests/second for public API; unauthenticated requests allowed for public protocols
- **Authentication**: None needed for public protocols; OAuth2 token for private content (optional)

```bash
pip install requests pandas
```

## Quick Start

```python
import requests
import pandas as pd
"
BASE = "https://www.protocols.io/api/v4"
HEADERS = {"Authorization": "YOUR_TOKEN_HERE"}  # Optional for public

# Search CRISPR protocols with filters
r = requests.get(
    f"{BASE}/protocols",
    params={"q": "CRISPR guide RNA design", "order_field": "views", "page_size": 10},
    headers=HEADERS,
)
r.raise_for_status()
data = r.json()
print(f"Total protocols: {data['pagination']['total_results']}")
for p in data["items"][:3]:
    print(f"  {p['title']} (DOI: {p.get('doi')} | Views: {p.get('stats', {}).get('number_of_views', 0)})")
```

## Core API

### Module 1: Protocol Search and Discovery

Search the public protocol library by keyword, technique, or full text. Use filters to narrow by category, author, or performance metrics.

```python
def search_protocols(query, page_size=20, order_field="relevance", category_id=None):
    params = {"q": query, "page_size": page_size, "order_field": order_field}
    if category_id:
        params["filter[categories_ids][]"] = category_id
    r = requests.get(f"{BASE}/protocols", params=params)
    r.raise_for_status()
    return r.json()

# Search by keyword
data = search_protocols("RNA extraction tissue", order_field="views", page_size=15)
total = data["pagination"]["total_results"]
print(f"RNA extraction protocols found: {total}")

# Extract structured info
rows = []
for p in data["items"][:10]:
    stats = p.get("stats", {})
    rows.append({
        "id": p.get("id"),
        "title": p.get("title"),
        "doi": p.get("doi"),
        "views": stats.get("number_of_views", 0),
        "forks": stats.get("number_of_forks", 0),
        "steps": p.get("number_of_steps", 0),
        "created": p.get("created_on")[:10],
        "category": p.get("categories", [{}])[0].get("name", "n/a"),
        "authors": [a["name"] for a in p.get("creators", [])[:2]],
    })
df = pd.DataFrame(rows).sort_values("views", ascending=False)
print("\nTop protocols:")
print(df[["title", "views", "forks", "steps"]].head(5).to_string(index=False))
```

```python
# Search with category filter
category_id = 22  # Molecular Biology category
data = search_protocols("qPCR primer design", category_id=category_id, order_field="views")
for p in data["items"][:3]:
    print(f"  {p['title'][:60]} (DOI: {p.get('doi', 'n/a')})")
```

### Module 2: Retrieve Full Protocol Details

Fetch the complete protocol with structured data for steps, materials, and equipment.

```python
def get_protocol(protocol_id):
    r = requests.get(f"{BASE}/protocols/{protocol_id}")
    r.raise_for_status()
    return r.json()

# Retrieve protocol by ID (from search results or DOI)
protocol_id = 45979  # Example: a publicly published protocol
data = get_protocol(protocol_id)
protocol = data.get("payload", data)  # Handle response structure

print(f"Title: {protocol.get('title')}")
print(f"DOI: {protocol.get('doi')}")
print(f"Authors: {', '.join(a['name'] for a in protocol.get('creators', []))}")
print(f"Steps: {len(protocol.get('steps', []))}")
print(f"Materials: {len(protocol.get('materials', []))}")
print(f"Abstract: {protocol.get('description', '')[:200]}...")
```

```python
# Extract structured steps
steps_df = []
for i, step in enumerate(protocol.get("steps", []), 1):
    duration = step.get("duration", {})
    steps_df.append({
        "step_number": i,
        "description": step.get("description", ""),
        "duration_value": duration.get("duration"),
        "duration_unit": duration.get("unit_label", ""),
        "temperature": step.get("temperature", {}).get("value"),
        "temp_unit": step.get("temperature", {}).get("unit_label", ""),
        "equipment": [eq.get("name") for eq in step.get("equipment", [])],
    })
steps_df = pd.DataFrame(steps_df)
print(f"\nFirst 5 steps:")
print(steps_df[["step_number", "description", "duration_value", "duration_unit"]].head().to_string(index=False))
```

```python
# Extract materials and equipment
materials = protocol.get("materials", [])
equipment_list = []

for material in materials[:10]:
    equipment_list.append({
        "name": material.get("name"),
        "quantity": material.get("quantity"),
        "unit": material.get("unit", {}).get("name", ""),
        "supplier": material.get("supplier", {}).get("name", ""),
        "catalog": material.get("sku"),
    })

print(f"\nSample materials:")
pd.DataFrame(equipment_list[:5])
```

### Module 3: Retrieve Protocol by DOI

Fetch a protocol using its exact DOI for precise citation-based retrieval.

```python
def get_protocol_by_doi(doi):
    r = requests.get(f"{BASE}/protocols",
                     params={"q": doi, "page_size": 5})
    r.raise_for_status()
    items = r.json()["items"]
    for item in items:
        if item.get("doi") == doi:
            return item
    return None

doi = "10.17504/protocols.io.bvb3n2qn"  # protocols.io DOI format
protocol = get_protocol_by_doi(doi)
if protocol:
    print(f"Found: {protocol['title']}")
    print(f"  ID: {protocol['id']}")
    print(f"  Version: {protocol.get('version_id')}")
```

### Module 4: Browse Protocol Categories

Find available categories for targeted searches, useful for building filter interfaces.

```python
def get_categories():
    r = requests.get(f"{BASE}/categories")
    r.raise_for_status()
    return r.json().get("items", [])

cats = get_categories()
print("Available protocol categories:")
for cat in cats[:10]:
    print(f"  {cat['id']}: {cat['name']} (protocols: {cat.get('protocol_count', 0)})")
```

### Module 5: Protocol Versioning and History

Track updates and cite the correct version in publications.

```python
def get_protocol_versions(protocol_id):
    r = requests.get(f"{BASE}/protocols/{protocol_id}")
    r.raise_for_status()
    protocol = r.json().get("payload", r.json())
    return {
        "title": protocol.get("title"),
        "version": protocol.get("version_id"),
        "published": protocol.get("published_on"),
        "doi": protocol.get("doi"),
        "parent_doi": protocol.get("parent_publication", {}).get("doi"),
        "current_version": protocol.get("is_current_version", False),
    }

versions = get_protocol_versions
print("\nVersion info:")
for k, v in versions.items():
    print(f"  {k}: {v}")
```

## Key Concepts

### Protocol DOIs and Versioning

- Each published protocol has a citable DOI: `10.17504/protocols.io.XXXXX`
- When a protocol is updated, it creates a new version with a new DOI
- The original DOI remains valid and points to the first version
- **Always cite the specific version DOI** for reproducibility

### API Authentication and Rate Limits

- **Public protocols**: Accessible without authentication, but tokens get higher rate limits (20 requests/second vs 10)
- **Private protocols**: Require an OAuth2 token from `https://www.protocols.io/developers`
- **Rate limiting**: 10 requests/second for public; include `time.sleep(0.15)` between requests to avoid hitting limits

### Protocol Structure

A protocol contains:
- **Steps**: Ordered list of operations with timing, temperature, equipment, and safety notes
- **Materials**: Reagents, consumables, equipment with suppliers and catalog numbers
- **Equipment**: Hardware requirements per step
- **Metadata**: Authors, tags, publication status, community metrics

## Common Workflows

### Workflow 1: Protocol Discovery and Quality Scoring

Find protocols with the most community validation (high forks = widely adapted).

```python
def search_and_rank(query, top_n=20):
    """Search and rank protocols by views + forks (community adaptation)."""
    r = requests.get(f"{BASE}/protocols",
                     params={"q": query, "page_size": top_n, "order_field": "views"})
    r.raise_for_status()
    data = r.json()

    rows = []
    for p in data["items"]:
        stats = p.get("stats", {})
        rows.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "doi": p.get("doi"),
            "views": stats.get("number_of_views", 0),
            "forks": stats.get("number_of_forks", 0),
            "steps": p.get("number_of_steps"),
            "created": p.get("created_on")[:10] if p.get("created_on") else "n/a",
            "category": p.get("categories", [{}])[0]. for c in p.get("creators", [])[:3],
        })

    df = pd.DataFrame(rows)
    df["popularity_score"] = df["views"] * 0.7 + df["forks"] * 0.3
    return df.sort_values("popularity_score", ascending=False)

# Find high-quality western blot protocols
df = search_and_rank("western blot protein detection", top_n=15)
df.to_csv("western_blot_protocols.csv", index=False)
print("\nTop western blot protocols:")
print(df[["title", "views", "forks", "steps"]].head(5).to_string(index=False))
```

### Workflow 2: Extract Protocol Data for Automation

Parse steps, reagents, and timing to build scripts or ELN entries.

```python
def extract_protocol_for_protocol_id(protocol_id):
    """Extract structured data for protocol automation."""
    r = requests.get(f"{BASE}/protocols/{protocol_id}")
    r.raise_for_status()
    protocol = r.json().get("payload", r.json())

    # Steps with timing
    steps = [{
        "step_number": i,
        "description": step.get("description", ""),
        "duration_value": step.get("duration", {}).get("duration"),
        "duration_unit": step.get("duration", {}).get("unit_label", ""),
        "temperature": step.get("temperature", {}).get("value"),
        "equipment": [eq.get("name") for eq in step.get("equipment", [])],
    } for i, step in enumerate(protocol.get("steps", []), 1)]

    # Materials with suppliers
    materials = [{
        "name": m.get("name"),
        "quantity": m.get("quantity"),
        "unit": m.get("unit", {}).get("name", ""),
        "supplier": m.get("supplier", {}).get("name", ""),
        "catalog": m.get("sku"),
    } for m in protocol.get("materials", [])]

    return {
        "title": protocol.get("title"),
        "doi": protocol.get("doi"),
        "steps": pd.DataFrame(steps),
        "materials": pd.DataFrame(materials),
    }

# Extract a protocol for automation
result = extract_protocol_for_protocol_id
print(f"\nProtocol: {result['title']} (DOi: {result['doi']})")
print(f"\nSteps summary:")
print(result["steps"].head())
print(f"\nMaterials summary:")
print(result["materials"].head())

# Export for integration
result["steps"].to_csv("protocol_steps.csv", index=False)
result["materials"].to_csv("protocol_materials.csv", index=False)
print("\nExported: protocol_steps.csv, protocol_materials.csv")
```

### Workflow 3: Reorder Protocol Steps by Equipment

Group steps by the equipment used, useful for batch operations.

```python
def group_steps_by_equipment(protocol_id):
    """Group steps by required equipment for workflow planning."""
    r = requests.get(f"{BASE}/protocols/{protocol_id}")
    r.raise_for_status()
    protocol = r.json().get("payload", r.json())

    equipment_groups = {}
    for i, step in enumerate(protocol.get("steps", []), 1):
        equipment = [eq.get("name") for eq in step.get("equipment", [])]
        if not equipment:
            equipment = ["manual"]
        for eq_name in equipment:
            if eq_name not in equipment_groups:
                equipment_groups[eq_name] = []
            equipment_groups[eq_name].append({
                "step": i,
                "desc": step.get("description", "")[:80],
                "duration": step.get("duration", {}),
            })

    return equipment_groups

# Group a protocol by equipment
groups = group_steps_by_equipment
print("\nSteps grouped by equipment:")
for eq, steps in groups.items():
    print(f"\nEquipment: {eq}")
    for step in steps[:3]:
        dur = step["duration"]
        dur_str = f" {dur.get('duration')}{dur.get('unit_label', '')}" if dur else ""
        print(f"  Step {step['step']}: {step['desc']}{dur_str}")
```

## Key Parameters

| Parameter | Function | Default | Range / Options | Effect |
|-----------|----------|---------|-----------------|--------|
| `q` | Search | — | string | Full-text search query |
| `order_field` | Search | `"relevance"` | `"relevance"`, `"views"`, `"date"`, `"activity"` | Result sort order |
| `page_size` | Search | `10` | `1`–`50` | Items per page |
| `filter[categories_ids][]` | Search | — | category ID | Filter by category |
| `protocol_id` | Get protocol | required | integer | Specific protocol to fetch |
| `DOI` | Search by DOI | — | string | Exact DOI match for retrieval |

## Best Practices

1. **Sort by views first for quality protocols**: `order_field=views` gives protocols that have been tested by many users, increasing the chance of catching hidden pitfalls early.

2. **Always cite the specific version DOI**: When including a protocol in methods, cite `doi:10.17504/protocols.io.XXXXX` with the version number. protocols.io DOIs are versioned; the DOI in the `payload` is always the latest.

3. **Cross-check vendor info**: The materials list often has supplier and catalog numbers — use this for reordering, but double-check that it's current with the vendor before placing orders.

4. **Extract safety notes**: Some steps include safety warnings or special precautions that aren't in the original vendor manual. Import these into your automated protocol.

5. **Cache high-quality protocols**: After finding a good protocol, store the steps and materials locally in case the protocol is removed or changes.

6. **Use the `forks` metric for adaptation**: A protocol with many forks has been adapted by many labs — check the forks for common workarounds.

7. **Check license before use**: All public protocols.io protocols are CC-BY 4.0 by default. Check the license field for commercial use restrictions.

## Common Recipes

### Recipe: Find and rank reagent-specific protocols

```python
# Find protocols using a specific kit
r = requests.get(f"{BASE}/protocols",
                 params={"q": "RNeasy Mini Kit RNA extraction", "order_field": "views"},
                 headers=HEADERS)
data = r.json()
print(f"Protocols using RNeasy: {data['pagination']['total_results']}")
for p in data["items"][:3]:
    print(f"  {p['title'][:60]} (DOI: {p.get('doi', 'n/a')})")
```

### Recipe: Generate citation strings for methods

```python
def generate_citation(doi):
    """Generate a formatted citation string."""
    protocol = get_protocol_by_doi(doi)
    if not protocol:
        return "Not found"
    authors = "; ".join(a["name"] for a in protocol.get("creators", [])[:3])
    year = protocol.get("created_on", "")[:4] or "n.d."
    title = protocol.get("title") or "(untitled)"
    print(f"{authors} ({year}). {title}. protocols.io. https://doi.org/{protocol.get('doi')}")
    return f"{authors} ({year}). {title}. protocols.io. https://doi.org/{protocol.get('doi')}"

# Generate citation for a protocol
citation = generate_citation("10.17504/protocols.io.bvb3n2qn")
```

### Recipe: Build an equipment list for a lab

```python
def extract_equipment_from_category(category_id, sample_size=50):
    """Get unique equipment from a category of protocols."""
    r = requests.get(f"{BASE}/categories")
    cats = r.json().get("items", [])
    for cat in cats:
        if cat["id"] == category_id:
            category_name = cat["name"]
            break
    else:
        return "Category not found"

    equipment = set()
    page = 1
    total_gathered = 0

    while total_gathered < sample_size:
        r = requests.get(f"{BASE}/protocols",
                         params={"filter[categories_ids][]": category_id,
                                 "page_size": 50, "page_id": page})
        data = r.json()
        if not data["items"]:
            break

        for p in data["items"][:sample_size - total_gathered]:
            for step in p.get("steps", []):
                for eq in step.get("equipment", []):
                    equipment.add(eq.get("name", "Unknown"))

            total_gathered += 1
        page += 1

    print(f"Equipment from {category_name} protocols:")
    for eq in sorted(equipment):
        print(f"  - {eq}")
    return sorted(equipment)

# Get equipment from a category
equipment = extract_equipment_from_category(22, 20)  # Molecular Biology
```

## Expected Outputs

- CSV/Excel files with protocol metadata, steps, and materials
- DOI strings for citation in publications
- Structured JSON for protocol automation
- Equipment lists and reagent lists for ordering

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `401` error accessing a protocol | Private protocol without auth | Get an OAuth2 token from `https://www.protocols.io/developers` |
| Search returns empty results | Query too specific or no match | Broaden the query; try fewer keywords or related terms |
| Protocol steps are empty or HTML-formatted | Protocol uses rich text | Use BeautifulSoup or `re.sub(r'<[^>]+>', '', text)` to strip HTML |
| `materials` list is empty | Materials embedded in step text | Check `steps` for reagent names and quantities listed inline |
| DOI lookup returns wrong protocol | Similar title match | Compare DOI field exactly using `if item.get("doi") == expected_doi` |
| Rate limit errors (`429 Too Many Requests`) | Exceeding 10 requests/second | Add `time.sleep(0.15)` between requests or get a token for 20/second |

## References

- [protocols.io API documentation](https://www.protocols.io/developers) — official REST API reference
- [protocols.io platform](https://www.protocols.io/) — browse and submit protocols
- [protocols.io citation guide](https://www.protocols.io/researcher-tools/citing-protocols) — how to cite in publications
- [Teytelman et al. Nature Methods 13, 401](https://doi.org/10.1038/nmeth.3999) — platform description
- [CC-BY license](https://creativecommons.org/licenses/by/4.0/) — terms of use

## Related Skills

- `opentrons-ot2-protocols` — convert downloaded protocols into automated Python scripts
- `eln-elabftw`, `eln-chemotion`, `eln-openbis` — store protocols and run details in an ELN
- `pylabrobot-vendor-agnostic` — run protocols across Hamilton, Tecan, Opentrons robots
- `western-blot-quantification` — follow published protocols for WB analysis