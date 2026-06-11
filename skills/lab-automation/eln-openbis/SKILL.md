---
name: eln-openbis
description: "openBIS open LIMS/ELN for life-sciences facilities via REST and Python API. Sample tracking across collections, spaces, datasets, vocabularies; integration with instruments and high-throughput pipelines. Open-source alternative to LabWare, Benchling LIMS. For notebook-style workflows use eln-elabftw; for chemistry use eln-chemotion."
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

# openBIS LIMS / ELN

## Overview

openBIS (open Biology Information System) is a free, open-source Laboratory Information Management System (LIMS) and Electronic Lab Notebook (ELN) developed at ETH Zurich and now maintained by the openBIS community. It is the standard open alternative to commercial LIMS (LabWare, Benchling LIMS, Thermo Watson) for core facilities, multi-user labs, and screening centers. openBIS models samples, experiments, datasets, materials, and instruments in a typed object model (Space → Project → Collection → Sample/Dataset). The Python API (`pyopenBIS`) and the REST API expose the full data model for scripted integration with high-throughput pipelines, plate readers, and sequencing instruments. Authentication is by session ID or personal access token; group permissions and ACLs control access.

Author: Pradyumna Jayaram.

## When to Use

- Tracking thousands of samples through a core facility (e.g., a genomics, proteomics, or screening core)
- Modeling a multi-step workflow: collection → sample → dataset → analysis with full provenance
- Capturing instrument output (HCS images, plate-reader reads, sequencing run folders) as registered datasets with metadata
- Building a high-throughput screening (HTS) campaign tracker with plates, wells, and library compounds
- Enforcing lab/team-level access control for shared facility resources
- Replacing a paid LIMS for an academic facility with a self-hosted open solution
- Capturing analysis outputs and linking them back to the originating samples and datasets
- For **notebook-style biology workflows** (free-form experiments with rich text, images, files), use `eln-elabftw` instead
- For **chemistry-specific** molecule and reaction handling, use `eln-chemotion` instead

## Prerequisites

- **openBIS instance**: self-hosted (Docker or VM) or shared. See https://openbis.ch
- **Credentials**: session-based; can be obtained via the login endpoint or via a personal access token
- **Python packages**: `pyopenBIS` (the official Python wrapper), `pandas`, `requests`
- **Network**: HTTPS to the openBIS host

```bash
pip install pyopenBIS pandas
```

## Quick Start

```python
import os
from pyopenBIS import openBIS
"
o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

# Find or create a space
default_space = o.get_space("/SCREEN") or o.create_space("SCREEN", "Screening campaigns")

# Create a new sample
sample = o.new_sample(
    type="COMPOUND",
    space="/SCREEN",
    project="MAY2026",
    collection="FRAGLIB",
    props={"name": "Fragment 1", "smiles": "c1ccccc1", "mw": 78.11},
)
sample.save()
print(f"Created sample permId={sample.permId}")
```

## Authentication and the data model

openBIS exposes a typed object hierarchy. Each entity has a permanent identifier (`permId`) and a type (an object type) that defines the schema. Understanding the model is the key to scripting openBIS.

```python
import os
from pyopenBIS import openBIS

o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

# Hierarchy:
#   Space (e.g., /SCREEN)
#     └── Project (e.g., /SCREEN/MAY2026)
#           └── Collection (e.g., /SCREEN/MAY2026/FRAGLIB)
#                 ├── Sample (a physical/virtual specimen)
#                 └── Dataset (raw or processed data file)
#
# Datasets are linked to Samples by parent-child relationships
# Every object has a permId, e.g., "202606100912345-1234"
```

Sample types: `COMPOUND`, `CELL_LINE`, `PLASMID`, `ANTIBODY`, `WELL`, `PLATE`, etc. (configurable per instance). Each type has a fixed set of properties (props) defined in the openBIS admin interface.

## Core API

### Module 1: Spaces, projects, and collections

```python
import os
from pyopenBIS import openBIS

o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

# List all spaces
for s in o.list_spaces():
    print(f"  /{s.code}: {s.description}")

# Get or create a project
if not o.get_project("/SCREEN/MAY2026"):
    o.create_project("MAY2026", "SCREEN", "May 2026 screening campaign")

# Get or create a collection
if not o.get_collection("/SCREEN/MAY2026/FRAGLIB"):
    o.create_collection("FRAGLIB", "MAY2026", "SCREEN", "Fragment library plates")
```

### Module 2: Samples

Samples are the central entity. Each sample has a type, a permId, and a set of typed properties.

```python
# Create a compound sample
compound = o.new_sample(
    type="COMPOUND",
    space="/SCREEN",
    project="MAY2026",
    collection="FRAGLIB",
    props={
        "name": "Fragment 1",
        "smiles": "c1ccccc1",
        "mw": 78.11,
        "vendor": "Enamine",
        "vendor_id": "Z12345",
    },
)
compound.save()
print(f"Compound permId={compound.permId} barcode={compound.code}")
```

```python
# Search samples by property value
hits = o.search_samples({
    "type": "COMPOUND",
    "props.mw": {"operator": ">=", "value": 200},
})
print(f"Compounds with MW >= 200: {len(hits)}")
for s in hits[:5]:
    print(f"  {s.permId} {s.props.get('name')} MW={s.props.get('mw')}")
```

```python
# Update sample properties (e.g., add a qc result)
sample = o.get_sample(compound.permId)
sample.props["qc_purity"] = 0.98
sample.props["qc_method"] = "LCMS"
sample.save()
```

### Module 3: Datasets (file registration)

Datasets in openBIS are not just files — they are registered objects with metadata, file paths, and provenance. Registering a dataset is how openBIS captures instrument output: a sequencing run folder, an HCS image stack, a plate-reader CSV.

```python
# Register a dataset (an HCS image stack)
import os
ds = o.new_dataset(
    type="HCS_IMAGE",
    sample=compound.permId,           # link to the parent sample
    files=["/data/hcs/run_001/A01.tif", "/data/hcs/run_001/A02.tif"],
    props={"instrument": "ImageXpress", "magnification": 20, "channel": "DAPI"},
)
ds.save()
print(f"Dataset permId={ds.permId} files={len(ds.file_list)}")
```

```python
# Register a plate-reader dataset
ds = o.new_dataset(
    type="PLATE_READER",
    sample=plate_permId,
    files=["/data/platereader/2026-06-10/run_47.csv"],
    props={"instrument": "EnVision", "wavelength_nm": 450, "protocol": "CellTiter-Glo"},
)
ds.save()
```

### Module 4: Plate and well hierarchies

A common pattern in screening: register a plate as a sample, then wells as child samples with their own metadata (concentration, compound, replicate).

```python
# Create a 96-well plate
plate = o.new_sample(
    type="PLATE_96",
    space="/SCREEN",
    project="MAY2026",
    collection="FRAGLIB",
    props={"name": "Plate P-001", "format": "Greiner 655090"},
)
plate.save()

# Add wells as child samples
for row in "ABCDEFGH":
    for col in range(1, 13):
        well = o.new_sample(
            type="WELL",
            space="/SCREEN",
            project="MAY2026",
            collection="FRAGLIB",
            parent=plate.permId,                  # parent-child link
            props={"position": f"{row}{col:02d}", "concentration_um": 10.0},
        )
        well.save()
```

### Module 5: Vocabularies and controlled terms

Vocabularies restrict property values to a fixed list — useful for status fields, organ lists, treatment codes.

```python
# Add a controlled vocabulary term
o.add_vocabulary_term("TREATMENT", "rapamycin_10nm")
o.add_vocabulary_term("TREATMENT", "torin1_100nm")

# Set a vocabulary-bound property on a sample
sample = o.get_sample(plate_permId)
sample.props["treatment"] = "rapamycin_10nm"   # must be in TREATMENT vocab
sample.save()
```

### Module 6: Experiment types and the analysis graph

Experiments capture the *process* (e.g., a screen, a sequencing run, a microscope session). They link inputs (samples) to outputs (datasets) to analysis steps.

```python
# Create an experiment
exp = o.new_experiment(
    type="HCS_SCREEN",
    space="/SCREEN",
    project="MAY2026",
    props={"objective": "10x10 fragment library hit identification",
           "instrument": "ImageXpress", "date": "2026-06-10"},
)
exp.save()

# Link samples (inputs) and datasets (outputs) to the experiment
exp.add_samples([s.permId for s in hits])
exp.add_datasets([ds.permId])
exp.save()
```

## Key Concepts

### permId vs code

Every object in openBIS has both a `permId` (permanent ID, like `202606100912345-1234`) and a `code` (human-readable, like `PLATE-P-001`). The `permId` never changes; the `code` can be edited. Always store `permId` in external systems and use `code` for human-facing labels.

### Sample type schemas

A sample *type* (e.g., `COMPOUND`, `WELL`, `CELL_LINE`) defines which properties exist and their types (string, integer, float, date, controlled vocabulary, sample link). Types are configured in the openBIS admin UI. You cannot create a sample without a type. Ask the facility admin for the type names in use.

### Object hierarchies and parent links

Samples can have parent samples (e.g., a `WELL` belongs to a `PLATE`). Datasets can have parent samples (e.g., a `PLATE_READER` dataset belongs to the plate sample) and can have parent datasets (e.g., a processed dataset derives from a raw dataset). These links are what make openBIS a *graph* rather than a flat table.

### ACL and access control

openBIS enforces group-based access at the Space, Project, and Collection level. The `permId` of an object is meaningless without the right ACL. A user with no access to `/SCREEN/MAY2026` cannot read samples there even if they know the `permId`. Always check that your user has the right group membership.

## Common Workflows

### Workflow 1: Register a high-throughput screen

```python
import os
from pyopenBIS import openBIS
import pandas as pd

o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

# 1. Create the campaign
campaign = o.new_experiment(
    type="HCS_SCREEN",
    space="/SCREEN",
    project="MAY2026",
    props={"objective": "BRCA1 modulator screen", "date": "2026-06-10"},
)
campaign.save()

# 2. Register plates from a CSV
plates = pd.read_csv("plates.csv")
for _, row in plates.iterrows():
    plate = o.new_sample(
        type="PLATE_96",
        space="/SCREEN",
        project="MAY2026",
        collection=row["collection"],
        props={"name": row["name"], "cell_line": row["cell_line"]},
    )
    plate.save()
    campaign.add_samples([plate.permId])

campaign.save()
print(f"Registered {len(plates)} plates in campaign {campaign.permId}")
```

### Workflow 2: Ingest a sequencing run

```python
import os
from pyopenBIS import openBIS

o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

run_dir = "/data/sequencing/2026-06-10_run42"
sample_permId = "202606100912345-1234"   # the library sample

ds = o.new_dataset(
    type="ILLUMINA_SEQUENCING",
    sample=sample_permId,
    files=[f"{run_dir}/R1.fastq.gz", f"{run_dir}/R2.fastq.gz"],
    props={"instrument": "NovaSeq 6000", "read_length": 150, "kit": "v3"},
)
ds.save()
print(f"Registered sequencing run as {ds.permId}")
```

### Workflow 3: Search and report

```python
import os
import pandas as pd
from pyopenBIS import openBIS

o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

# Find all compounds with a vendor qc result
hits = o.search_samples({
    "type": "COMPOUND",
    "props.vendor_qc": "PASS",
})

rows = [{k: v for k, v in s.props.items()} for s in hits]
df = pd.DataFrame(rows)
df.to_csv("qc_passed_compounds.csv", index=False)
print(f"Wrote {len(df)} qc-passed compounds")
```

## Key Parameters

| Parameter | Function/Endpoint | Default | Range / Options | Effect |
|-----------|-------------------|---------|-----------------|--------|
| `type` | `new_sample` | required | string (object type) | Schema of the sample; determines allowed properties |
| `space` / `project` / `collection` | `new_sample` | required | paths | Hierarchical placement |
| `parent` | `new_sample` | optional | permId | Parent sample (e.g., well → plate) |
| `props` | `new_sample` | `{}` | dict | Property values; keys must be valid for the type |
| `files` | `new_dataset` | required | list of paths | Files included in the dataset (paths must be visible to the openBIS server) |
| `props.instrument` | datasets | — | string | Free-text or vocab-bound |
| `vocab` | `add_vocabulary_term` | required | vocabulary code | The vocabulary the term belongs to |
| `operator` / `value` | search filters | required | comparison | `==`, `>=`, `<=`, `>`, `<`, `LIKE` |

## Best Practices

1. **Use `permId`, not `code`, in scripts.** `code` can be renamed; `permId` is permanent. If you build a downstream analysis that references a sample, store its `permId`.

2. **Configure your sample types up front.** Type-driven schemas are openBIS's superpower and its biggest upfront cost. Define the props, vocabularies, and controlled terms in the admin UI before you start scripting.

3. **Register datasets, not just files.** A raw file path is not enough — registering a dataset creates the link from the file to the sample, the experiment, and the analysis. This is what makes the openBIS graph queryable.

4. **Use parent-child links for hierarchy.** Plate → well, library → aliquot, screen → plate. Parent links make traversal queries (`get all wells of a plate`) trivial.

5. **Limit direct file access; use the API.** When a tool wants to read a dataset file, it should use the openBIS download endpoint, not the underlying filesystem. This keeps the ACL enforced.

6. **Bulk-create with care.** `new_sample` followed by `save()` issues one HTTP call. For thousands of samples, batch them in a single transaction (use the underlying `etlserver` ETL framework or a `with transaction():` block in the Python API).

7. **Document your object types in the ELN.** The openBIS admin UI does not document types; maintain a `TYPES.md` in your project repo so future users know which types and properties to use.

8. **Test searches before relying on them.** `o.search_samples` does a server-side search; latency depends on indexing. For 1M+ samples, consider ELN-LIMS Hybris or a custom index.

## Common Recipes

### Recipe: Find all datasets for a sample

```python
import os
from pyopenBIS import openBIS

o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

sample = o.get_sample(sample_permId)
datasets = o.get_datasets_of_sample(sample)
for ds in datasets:
    print(f"  {ds.permId} type={ds.type} files={len(ds.file_list)}")
```

### Recipe: Add a vocabulary term

```python
import os
from pyopenBIS import openBIS

o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

o.add_vocabulary_term("TREATMENT", "compound_X_1um")
o.add_vocabulary_term("TREATMENT", "compound_X_10um")
```

### Recipe: Bulk sample creation from CSV

```python
import csv
import os
from pyopenBIS import openBIS

o = openBIS("https://openbis.example.org")
o.login(os.environ["OPENBIS_USER"], os.environ["OPENBIS_PASSWORD"])

with open("samples.csv") as f:
    for row in csv.DictReader(f):
        s = o.new_sample(
            type="COMPOUND",
            space="/SCREEN", project="MAY2026", collection="FRAGLIB",
            props={"name": row["name"], "smiles": row["smiles"],
                   "vendor": row["vendor"], "vendor_id": row["vendor_id"]},
        )
        s.save()
        print(f"  {row['name']} -> {s.permId}")
```

## Expected Outputs

- Permanent IDs (`permId`) for every object, returned from `save()` calls
- A web UI at `https://<host>/openbis/webapp/` where users browse the object graph
- A REST API at `https://<host>/openbis/openbis/rmi-lims` (v1) or `https://<host>/openbis/api/v3/` (v3)
- ELN-LIMS exports (CSV, JSON, mzML-linked bundles) for archival

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `401 Unauthorized` on login | Wrong credentials or expired session | Verify username/password; some instances use SSO and require a different login flow |
| `404 Not Found` on `get_sample(permId)` | Object does not exist or user has no ACL | Confirm the permId is correct; check that the user belongs to the right group |
| Sample save fails with "missing property" | Required prop not set for the type | Run `o.get_sample_type("COMPOUND")` to see required props; check your instance's type configuration |
| Dataset registration fails with "file not found" | openBIS server cannot see the file path | Files must be in a path the openBIS server can read; use dropbox folders, mount points, or the API upload endpoint |
| `pyopenBIS` attribute missing | Older API version | The Python wrapper has changed across openBIS versions; check `pyopenBIS.__version__` and consult the matching docs |
| `search_samples` is slow | Unindexed property or huge dataset | Index properties in the openBIS admin UI; for 1M+ objects consider a custom ELN-LIMS search infrastructure |
| Cannot edit a sample's props | Sample is in a "frozen" experiment | Once an experiment is finalized, samples inside are read-only; the admin must unfreeze the experiment |
| pyopenBIS version mismatch | API server is a different version | Match `pyopenBIS` version to the openBIS server (v16, v17, v20, v21) |

## References

- [openBIS official site](https://openbis.ch) — features, downloads, news
- [openBIS documentation](https://openbis.ch/documentation.html) — install, configure, admin
- [openBIS GitHub](https://github.com/qbicsoftware/openbis) — source, releases
- [pyopenBIS documentation](https://pypi.org/project/pyopenBIS/) — Python API wrapper
- [Bauch et al., *J. Cheminformatics* 3:33 (2011)](https://doi.org/10.1186/1758-2946-3-33) — openBIS architecture paper

## Related Skills

- `eln-elabftw` — open ELN for general biology workflows
- `eln-chemotion` — open ELN for chemistry with structure handling
- `protocolsio-protocol-repository` — search and import published protocols
- `plannotate-plasmid-annotation` — annotate plasmids before registering as samples
- `opentrons-ot2-protocols` — automated liquid handling, register output as openBIS datasets