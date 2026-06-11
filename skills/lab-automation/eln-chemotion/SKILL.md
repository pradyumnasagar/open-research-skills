---
name: eln-chemotion
description: "Chemotion open electronic lab notebook for chemists via REST API. Molecule"
license: MIT
---



<!-- metadata:
category: ''
version: 1.0.0
author: Pradyumna Jayaram
tags: []
difficulty: beginner
sources: SciAgent-Skills-main/skills/lab-automation/benchling-integration/SKILL.md
-->

# Chemotion Electronic Lab Notebook

## Overview

Chemotion is a free, open-source electronic lab notebook built for synthetic and analytical chemistry. It provides a built-in molecule editor (Ketcher), reaction handling (with atom-mapping and stoichiometry), sample and inventory tracking, and direct import of NMR, IR, and MS spectra (JCAMP-DX, nmrML, mzML, Bruker/Agilent vendor formats). The Chemotion API exposes every UI action — sample creation, reaction drafting, spectra upload, inventory updates — so the entire synthetic workflow is scriptable from Python. Chemotion is the standard open alternative to commercial chemistry ELNs (ChemAxon, Accelrys, MestReLab).

Author: Pradyumna Jayaram.

## When to Use

- Recording synthetic procedures with structures, reagents, conditions, and yields in an open ELN
- Tracking a compound library with structures, batch data, and analytical spectra
- Importing NMR, IR, or MS spectra from vendor files (Bruker, Agilent, JCAMP-DX) and linking to the matching sample
- Storing reaction schemes with stoichiometry, atom mapping, and SMILES for each component
- Building a structure-searchable inventory (substructure, similarity, exact match) for a chemistry group
- Bulk-importing compounds from a CSV with SMILES into the sample database
- Sharing reproducible procedures with a chemistry collaboration via a self-hosted Chemotion instance
- For **biology-focused** workflows (plasmids, cell lines, antibodies, NGS samples), use `eln-elabftw` instead
- For **high-throughput LIMS** (assay plates, screens, facility-scale sample tracking), use `eln-openbis` instead

## Prerequisites

- **Chemotion instance**: self-hosted (Docker recommended) or a shared instance. See https://www.chemotion.net
- **API token**: obtained from user profile (click avatar → API Token). Token is per-user and inherits permissions.
- **Python packages**: `requests`, `pandas`, `rdkit` (for structure handling)
- **Network**: HTTPS to the Chemotion host
- **Optional**: `pychemotion` — community Python wrapper

```bash
pip install requests pandas rdkit
```

## Quick Start

```python
import os
import requests
"
API = "https://chemotion.example.org/api/v1"
headers = {"Content-Type": "application/json",
           "Authorization": f"Bearer {os.environ['CHEMOTION_TOKEN']}"}

# Create a sample (a compound in the inventory)
r = requests.post(f"{API}/samples", headers=headers, json={
    "name": "Aspirin",
    "smiles": "CC(=O)Oc1ccccc1C(=O)O",
    "molecule_name": "Acetylsalicylic acid",
    "external_label": "ASP-001",
    "density": 1.4,
    "molfile": "",   # Chemotion will generate from SMILES
    "stereo": 0,     # 0 = no stereo; 1 = absolute; 2 = relative
})
sample = r.json()
print(f"Created sample id={sample['id']} label={sample['external_label']}")
```

## Authentication

Chemotion uses a single bearer token per user. Generate one in the user profile. The token grants the same permissions as the user (read, write, delete, share).

```python
import os
import requests

API = "https://chemotion.example.org/api/v1"
def auth_headers():
    return {"Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {os.environ['CHEMOTION_TOKEN']}"}
```

For service-account-style use, create a dedicated user with limited scopes (e.g., read-only or samples-only). Rotate the token at least annually and immediately when a collaborator leaves.

## Core API

### Module 1: Molecules and samples

A *sample* in Chemotion is a physical or virtual specimen (a compound, a fraction, a synthesized material). Every sample has a structure (SMILES or molfile), a name, purity, hazards, and storage info. The molecule is rendered via Ketcher (JS) in the UI; the API accepts SMILES, InChI, or molfile.

```python
import os
import requests

API = "https://chemotion.example.org/api/v1"
headers = auth_headers()

# Create a sample from SMILES
payload = {
    "name": "Benzyl alcohol",
    "smiles": "OCc1ccccc1",
    "external_label": "BA-2026-001",
    "location": "Cabinet A · Shelf 2",
    "amount": 25.0,
    "amount_unit": "mL",
    "purity": 0.998,
    "stereo": 0,
    "is_partial": False,
    "inventory_label": "BA-2026-001",
    "xref_inchikey": "",  # leave blank to auto-compute
    "decoupled": False,
    "deprecated": False,
}
r = requests.post(f"{API}/samples", headers=headers, json=payload)
sample = r.json()
print(f"id={sample['id']} inchikey={sample.get('xref_inchikey', '?')}")
```

```python
# List samples with a name/SMILES filter
r = requests.get(f"{API}/samples", headers=headers, params={"search": "benzyl"})
for s in r.json()[:5]:
    print(f"  {s['id']}: {s['name']} ({s.get('smiles', '')[:40]})")

# Get a single sample with full details
r = requests.get(f"{API}/samples/{sample['id']}", headers=headers)
print(r.json().get("molecule_name"), r.json().get("xref_inchikey"))
```

```python
# Update sample metadata (e.g., log an NMR result)
requests.patch(f"{API}/samples/{sample['id']}", headers=headers, json={
    "purity": 0.999,
    "description": "Re-purified by column; new NMR confirms structure.",
})
```

### Module 2: Reactions

A *reaction* groups reactants, products, solvents, and conditions into a single entity. Chemotion extracts atom mapping automatically when the SMILES contain the same atom indices on both sides.

```python
# Create a reaction: aspirin synthesis
r = requests.post(f"{API}/reactions", headers=headers, json={
    "name": "Acetylation of salicylic acid",
    "description": "Standard Fischer esterification; acetic anhydride, H2SO4 cat.",
    "temperature": {"value": 85, "unit": "°C"},
    "duration": {"value": 30, "unit": "min"},
    "solvent": "acetic anhydride",
    "reactants": [
        {"smiles": "OC(=O)c1ccccc1O", "equivalent": 1.0, "reference": True},
    ],
    "products": [
        {"smiles": "CC(=O)Oc1ccccc1C(=O)O", "equivalent": 1.0, "reference": False},
    ],
    "conditions": "H2SO4 catalytic, 85 °C, 30 min",
    "yield": 0.78,
})
rxn = r.json()
print(f"Reaction id={rxn['id']} yield={rxn.get('yield')}")
```

```python
# Add an analytical sample to the reaction
requests.post(f"{API}/reactions/{rxn['id']}/samples", headers=headers, json={
    "sample_id": sample["id"],   # the benzyl alcohol sample from Module 1
    "role": "reactant",
    "equivalent": 1.0,
})

# List all reactions in a date range
r = requests.get(f"{API}/reactions", headers=headers,
                 params={"updated_after": "2026-01-01"})
print(f"Reactions updated since 2026-01-01: {len(r.json())}")
```

### Module 3: Spectra (NMR, IR, MS, HPLC)

Chemotion stores analytical spectra as files linked to samples or reactions. Accepted formats include JCAMP-DX (`.jdx`, `.dx`), Bruker (`.zip`, top-level `1r`, `2rr`), Agilent (`.d` directories), and mzML for MS.

```python
# Upload a JCAMP-DX NMR spectrum to a sample
with open("benzyl_alcohol_1H.jdx", "rb") as f:
    r = requests.post(
        f"{API}/samples/{sample['id']}/analyses",
        headers={"Authorization": headers["Authorization"]},
        files={"file[]": ("benzyl_alcohol_1H.jdx", f, "chemical/x-jcamp-dx")},
        data={"analysis_type": "NMR", "name": "1H NMR CDCl3 400 MHz"},
    )
print("NMR upload:", r.status_code, r.text[:120])
```

```python
# Upload an HPLC chromatogram
with open("purity_trace.csv", "rb") as f:
    r = requests.post(
        f"{API}/samples/{sample['id']}/analyses",
        headers={"Authorization": headers["Authorization"]},
        files={"file[]": ("purity.csv", f, "text/csv")},
        data={"analysis_type": "HPLC", "name": "Purity check 2026-06-10"},
    )
print("HPLC upload:", r.status_code)
```

### Module 4: Inventory, locations, and barcodes

Every physical sample lives in a *location* (cabinet, shelf, fridge) and has a *container* (vial, well, bottle). Chemotion uses string-based barcode labels that can be generated and printed.

```python
# List locations
r = requests.get(f"{API}/locations", headers=headers)
for loc in r.json()[:5]:
    print(f"  {loc['id']}: {loc['name']} (barcodes-on: {loc.get('label', '?')})")
```

```python
# Move a sample to a new location
requests.patch(f"{API}/samples/{sample['id']}", headers=headers, json={
    "location": "Fridge B · Shelf 1",
})

# Generate a printable barcode label
import urllib.parse
label_text = urllib.parse.quote(sample["external_label"])
print(f"Print label: https://chemotion.example.org/labels/{label_text}.png")
```

### Module 5: Structure search

Chemotion supports substructure, similarity, and exact-match search by SMILES or molfile. Substructure search uses the included SSM (Small Substructure Matcher) or the optional Bingo cartridge for performance.

```python
# Substructure search: all samples containing a benzene ring
r = requests.post(f"{API}/search/substructure", headers=headers, json={
    "smiles": "c1ccccc1",
    "limit": 50,
})
for hit in r.json().get("samples", []):
    print(f"  {hit['id']}: {hit['name']}")
```

```python
# Similarity search: Tanimoto ≥ 0.7 vs aspirin
r = requests.post(f"{API}/search/similarity", headers=headers, json={
    "smiles": "CC(=O)Oc1ccccc1C(=O)O",
    "threshold": 0.7,
    "limit": 25,
})
print(f"Similar compounds: {len(r.json().get('samples', []))}")
```

### Module 6: Collections and sharing

Collections group samples/reactions for sharing with collaborators or for export.

```python
# Create a collection
r = requests.post(f"{API}/collections", headers=headers, json={
    "name": "Fragment library 2026-Q2",
    "description": "80 fragments selected for the May screening campaign",
    "shared": False,
})
coll = r.json()

# Add a sample to the collection
requests.post(f"{API}/collections/{coll['id']}/samples", headers=headers,
              json={"sample_id": sample["id"]})

# Export collection as SDFile (programmatically)
r = requests.get(f"{API}/collections/{coll['id']}/export", headers=headers,
                 params={"format": "sdf"})
with open("fragment_library.sdf", "wb") as f:
    f.write(r.content)
print(f"Exported SDFile: {len(r.content)} bytes")
```

## Key Concepts

### SMILES, InChI, and molfile

- **SMILES** is the recommended input. Chemotion canonicalizes SMILES and computes the InChIKey automatically. Use canonical SMILES from RDKit to avoid perception drift.
- **InChIKey** is the cross-database key; if you upload compounds from a vendor catalog, set `xref_inchikey` so future joins are exact.
- **Molfile (V2000/V3000)** is accepted for stereo-precise structures. Use it for tet stereo or charged species that SMILES round-trips awkwardly.

### Sample vs molecule

A *molecule* is the abstract chemical identity (defined by InChIKey or canonical SMILES). A *sample* is a physical specimen — it has a location, amount, lot, purity, and is the unit chemists actually weigh. The same molecule may have dozens of samples from different bottles, batches, and suppliers.

### Stereo flag

`stereo` in the sample payload encodes stereochemistry handling: `0` = no stereo, `1` = absolute, `2` = relative, `3` = racemic. Pick correctly — racemic mixtures should be `3`, not `0`, so structure searches distinguish "pure enantiomer" from "the racemate".

## Common Workflows

### Workflow 1: Bulk import a fragment library

```python
import csv
import os
import time
import requests

API = "https://chemotion.example.org/api/v1"
headers = auth_headers()

def create_sample(smiles, name, label):
    r = requests.post(f"{API}/samples", headers=headers, json={
        "name": name, "smiles": smiles, "external_label": label,
        "stereo": 0, "is_partial": False,
    })
    r.raise_for_status()
    return r.json()

created = []
with open("fragments.csv") as f:
    for row in csv.DictReader(f):
        try:
            s = create_sample(row["smiles"], row["name"], row["label"])
            created.append(s["id"])
        except Exception as e:
            print(f"  failed {row['label']}: {e}")
        time.sleep(0.1)  # rate-limit cushion
print(f"Imported {len(created)} fragments")
```

### Workflow 2: Attach NMR spectra to a batch of samples

```python
import os
import requests

API = "https://chemotion.example.org/api/v1"
headers = auth_headers()

samples = [
    (4711, "spectra/BA-001_1H.jdx"),
    (4712, "spectra/BA-002_1H.jdx"),
    (4713, "spectra/BA-003_1H.jdx"),
]
for sample_id, path in samples:
    with open(path, "rb") as f:
        r = requests.post(
            f"{API}/samples/{sample_id}/analyses",
            headers={"Authorization": headers["Authorization"]},
            files={"file[]": (os.path.basename(path), f, "chemical/x-jcamp-dx")},
            data={"analysis_type": "NMR", "name": f"1H NMR {sample_id}"},
        )
    print(f"  {sample_id}: HTTP {r.status_code}")
```

### Workflow 3: Synthesize-and-record from a procedural script

```python
import os
import requests

API = "https://chemotion.example.org/api/v1"
headers = auth_headers()

# 1. Create product sample
prod = requests.post(f"{API}/samples", headers=headers, json={
    "name": "Methyl ester of BA-001",
    "smiles": "COC(=O)Cc1ccccc1",
    "external_label": "BA-001-Me",
    "stereo": 0,
}).json()

# 2. Create reaction linking reactant and product
requests.post(f"{API}/reactions", headers=headers, json={
    "name": "Fischer esterification of BA-001",
    "reactants": [{"smiles": "OCc1ccccc1", "equivalent": 1.0, "reference": True}],
    "products":  [{"smiles": "COC(=O)Cc1ccccc1", "equivalent": 1.0, "reference": False}],
    "solvent": "MeOH",
    "temperature": {"value": 65, "unit": "°C"},
    "duration": {"value": 240, "unit": "min"},
    "conditions": "H2SO4 cat., reflux 4 h",
    "yield": 0.82,
})

# 3. Log the run via the in-Chemotion description
requests.patch(f"{API}/samples/{prod['id']}", headers=headers, json={
    "description": "Scaled up 5x from BA-001 batch. Purity 96% by 1H NMR.",
})

print(f"Reaction and product recorded; product id={prod['id']}")
```

## Key Parameters

| Parameter | Endpoint | Default | Range / Options | Effect |
|-----------|----------|---------|-----------------|--------|
| `smiles` | samples, reactions | — | string | Structure; canonicalize with RDKit before upload |
| `stereo` | samples | `0` | `0`–`3` | `0` none, `1` absolute, `2` relative, `3` racemic |
| `amount` | samples | `0` | float | Quantity in `amount_unit` |
| `amount_unit` | samples | `"g"` | `"g"`, `"mg"`, `"mL"`, `"µL"`, `"mol"` | Unit for the amount field |
| `purity` | samples | `0` | `0`–`1` | Fraction (e.g., `0.998`) |
| `external_label` | samples | auto | string | Visible label / barcode text |
| `temperature.value` / `.unit` | reactions | — | float + `"°C"` or `"K"` | Reaction temperature |
| `duration.value` / `.unit` | reactions | — | float + `"s"`, `"min"`, `"h"` | Reaction time |
| `yield` | reactions | `0` | `0`–`1` | Fractional yield (0.78 = 78%) |
| `analysis_type` | spectra upload | required | `"NMR"`, `"IR"`, `"MS"`, `"HPLC"`, `"GC"`, `"UV"` | Type of spectrum uploaded |

## Best Practices

1. **Canonicalize SMILES before upload.** Round-trip through RDKit to avoid perception drift: `Chem.MolToSmiles(Chem.MolFromSmiles(s))`. This is the single most common cause of "duplicate" compounds in chemistry databases.

2. **Set `xref_inchikey` for vendor compounds.** When you buy a compound from Enamine, MolPort, or Sigma, store the vendor InChIKey in `xref_inchikey` so future joins are exact, not perceptual.

3. **Use stereo flag 3 for racemates.** Stereo `0` means "no stereo information"; use `3` to mean "racemic mixture" so the database distinguishes "this compound is the racemate" from "this compound is the pure enantiomer".

4. **Upload raw spectra, not just images.** The `.jdx`, `.mzML`, or vendor format preserves the data; a JPEG of a spectrum does not. Chemotion can render the spectrum on demand if the raw data is stored.

5. **Use collections to share, not to hide.** Collections are the unit of sharing in Chemotion — put a project, a publication, or a class in a collection and grant access by collection, not by individual sample.

6. **Treat atom mapping as informational, not mandatory.** Chemotion auto-maps reactions when atom indices match; for retrosynthesis analyses keep this in mind — atom-mapped SMILES are not the same as canonical SMILES.

7. **Backup before bulk operations.** `POST /samples/bulk` is fast; an accidental wipe is faster. Snapshot the database before any large migration.

8. **Use the import wizard for >100 samples.** The UI importer is faster than a one-by-one script for large libraries, and it gives a preview before commit.

## Common Recipes

### Recipe: Find all samples containing a substructure

```python
import os
import requests

API = "https://chemotion.example.org/api/v1"
headers = auth_headers()

r = requests.post(f"{API}/search/substructure", headers=headers, json={
    "smiles": "c1ccc2ncccc2c1",   # quinoline
    "limit": 100,
})
for s in r.json().get("samples", []):
    print(f"  {s['id']}: {s['name']}")
```

### Recipe: Generate a barcode label image

```python
import os
import requests

API = "https://chemotion.example.org/api/v1"
headers = auth_headers()

label = "BA-2026-001"
r = requests.get(f"{API}/labels/{label}", headers={"Accept": "image/png"},
                 params={"size": "small"}, auth=None)
# or use the URL with the bearer token in a query param
# (depends on deployment; some instances expose unauthenticated label endpoints)
with open(f"{label}.png", "wb") as f:
    f.write(r.content)
```

### Recipe: Tanimoto similarity search

```python
import os
import requests

API = "https://chemotion.example.org/api/v1"
headers = auth_headers()

r = requests.post(f"{API}/search/similarity", headers=headers, json={
    "smiles": "CC(=O)Oc1ccccc1C(=O)O",  # aspirin
    "threshold": 0.6,
    "limit": 25,
})
for hit in r.json().get("samples", []):
    print(f"  {hit['id']} ({hit.get('similarity', '?'):.2f}) {hit['name']}")
```

## Expected Outputs

- Sample URLs: `https://<host>/samples/<id>`
- Reaction URLs: `https://<host>/reactions/<id>`
- Spectra appear under the sample page (preview + raw file download)
- SDFile exports contain all samples in a collection with structures and metadata

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `401 Unauthorized` | Invalid or expired token | Regenerate the token in the user profile; check `CHEMOTION_TOKEN` env var |
| `403 Forbidden` | Token user lacks write permission | Confirm the user role (Admin, Member, Viewer) in Chemotion admin |
| `422 Unprocessable Entity` on sample create | Invalid SMILES or missing required field | Try the SMILES in the Ketcher editor; ensure `name` is non-empty |
| Structure renders blank in the UI | InChI computation failed | Recompute with `Chem.MolToInchiKey` (RDKit) and pass via `xref_inchikey`; some special salts are not handled |
| Spectra upload silently ignored | Wrong content-type header | Use the `files=` kwarg in `requests` (it sets multipart and content-type correctly); do not manually set `Content-Type: application/json` for uploads |
| Substructure search returns no hits | Chemistry-extension not installed | Chemotion ships with a default SSM matcher; the high-performance Bingo cartridge is optional and enabled per-instance |
| Stereo loss after import | SMILES string had unspecified stereo | Re-export with `@/@@` from RDKit: `Chem.MolToSmiles(mol, isomericSmiles=True)` |

## References

- [Chemotion official site](https://www.chemotion.net) — features, news, community
- [Chemotion GitHub](https://github.com/Chemotion/Chemotion) — source, releases, issue tracker
- [Chemotion API documentation](https://www.chemotion.net/docs/api) — endpoint reference
- [Chemotion ELN specification](https://www.chemotion.net/eln) — data model and exports
- [Tremouilhac et al., *J. Cheminformatics* 9:45](https://doi.org/10.1186/s13321-017-0226-2) — Chemotion architecture paper

## Related Skills

- `eln-elabftw` — open ELN for general biology workflows (no chemistry editor)
- `eln-openbis` — open LIMS for high-throughput assay and sample tracking
- `protocolsio-protocol-repository` — search and import published synthetic procedures