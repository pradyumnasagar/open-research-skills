---

name: eln-elabftw
description: "eLabFTW open-source electronic lab notebook via REST API. Self-hosted ELN/LIMS alternative to Benchling and LabArchives: experiments, database entries, inventory, equipment booking, experiments linking. Use for free, open lab notebook management. For chemistry-focused work use eln-chemotion; for assay/LIMS-heavy pipelines use eln-openbis."
license: MIT
---




<!-- metadata:
category: lab-automation
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - lab-automation
  - research
difficulty: intermediate
-->

# eLabFTW Electronic Lab Notebook

## Overview

eLabFTW is a free, self-hostable electronic lab notebook with a complete REST API. It is the standard open-source alternative to Benchling and LabArchives for academic and small-industry labs. eLabFTW stores experiments, database entries (reagents, plasmids, cells, antibodies, equipment), inventory with locations and barcodes, equipment bookings, and inter-experiment links — all in a single instance your group controls. Authentication is by API key or email/password; users can sign in with local accounts or institutional SSO via LDAP/OIDC. The API exposes every UI action, so the full lab-notebook workflow is scriptable from Python.

Author: Pradyumna Jayaram.

## When to Use

- Replacing or supplementing paper lab notebooks with a free, self-hosted ELN
- Tracking experiments with linked reagents, cells, and protocols without paying for Benchling or LabArchives seats
- Building a small group inventory system (boxes, locations, freezer maps) tied to experiments
- Booking shared equipment (qPCR machines, microscopes, FACS) with an open scheduler
- Scripting experiment creation from Opentrons runs, plate readers, or imaging pipelines
- Bulk-importing legacy experiments or reagents from spreadsheets
- Auditing a lab notebook's chain of custody (locked entries, signatures, timestamps)
- For **chemistry-specific** molecule and reaction handling, use `eln-chemotion` instead — eLabFTW has no built-in molecule editor
- For **large LIMS workflows** (sample tracking across a facility, multi-user permissions, integration with instruments), use `eln-openbis` instead

## Prerequisites

- **eLabFTW instance**: self-hosted (Docker recommended) or shared server. See https://www.elabftw.net
- **API key**: generated in user profile (`Profile → API keys`); or use email + password
- **Python packages**: `requests`, `pandas`
- **Network**: HTTPS access to the eLabFTW host
- **Optional**: `pyelabftw` — official community Python wrapper (currently thin; many workflows still use plain `requests`)

```bash
pip install requests pandas
# Optional community wrapper
# pip install pyelabftw
```

## Quick Start

```python
import os
import requests
from requests.auth import HTTPBasicAuth
"
API = "https://eln.example.org/api/v2"
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])
headers = {"Content-Type": "application/json", "Accept": "application/json"}

# Create a new experiment
r = requests.post(
    f"{API}/experiments",
    headers=headers,
    auth=auth,
    json={"title": "CRISPR screen — 2026-06-10 — replicate 1"},
)
r.raise_for_status()
exp = r.json()
print(f"Created experiment id={exp['id']} title={exp['title']}")
```

## Authentication

eLabFTW supports three authentication modes for the API. Choose based on your security posture.

```python
import os
import requests
from requests.auth import HTTPBasicAuth

API = "https://eln.example.org/api/v2"

# Option 1: API key (preferred for scripts)
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])

# Option 2: email + password (only for one-off scripts; do not commit creds)
auth = HTTPBasicAuth("jane@example.org", os.environ["ELN_PASSWORD"])

# Option 3: Bearer token (when SSO/OIDC is configured)
headers = {"Authorization": f"Bearer {os.environ['ELN_BEARER']}"}
# requests.get(API + "/experiments", headers=headers)
```

API keys inherit the user's permissions. Generate a separate key per script, and rotate when a student or postdoc leaves the lab.

## Core API

### Module 1: Experiments (the lab notebook)

Experiments are the core ELN entity. They have rich-text bodies, attached files, links to database items, and a lock-on-signature workflow.

```python
import os
import requests
from requests.auth import HTTPBasicAuth

API = "https://eln.example.org/api/v2"
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])
headers = {"Content-Type": "application/json"}

# Create an experiment
body = """<h2>Goal</h2><p>Test three gRNA designs for BRCA1 knockout.</p>
<h2>Protocol</h2><p>Lipofect Cas9 RNP into HEK293T; harvest at 72h.</p>"""
r = requests.post(f"{API}/experiments", headers=headers, auth=auth,
                  json={"title": "BRCA1 gRNA screen 2026-06-10", "body": body})
exp = r.json()
print(f"Created: id={exp['id']} url=https://eln.example.org/experiments.php?mode=view&id={exp['id']}")

# Append to an experiment body
r = requests.post(f"{API}/experiments/{exp['id']}", headers=headers, auth=auth,
                  json={"bodyappend": "<h2>2026-06-11</h2><p>Transfected; cells look healthy.</p>"})

# Add a comment (visible to all users with read access)
requests.post(f"{API}/experiments/{exp['id']}/comments", headers=headers, auth=auth,
              json={"comment": "Lysis buffer ran out — reordered NEB B7203."})

# Lock the experiment (prevents further edits; recorded in the audit log)
requests.post(f"{API}/experiments/{exp['id']}", headers=headers, auth=auth,
              json={"action": "lock"})
```

```python
# Read experiment with linked items
r = requests.get(f"{API}/experiments/{exp_id}", auth=auth)
data = r.json()
print(f"Title: {data['title']}")
print(f"Status: {data['category_title']} | Date: {data['date']}")
print(f"Linked items: {len(data.get('items_links', []))}")
print(f"Tags: {data.get('tags', [])}")
```

### Module 2: Database items (reagents, plasmids, cells, antibodies)

Database items are typed records (your lab can define custom types) that get linked into experiments. Use them for everything reusable: plasmid stocks, antibody lots, cell lines, primers.

```python
# Create a plasmid database item
payload = {
    "category_id": 4,  # find via GET /items_types
    "title": "pX330-BRCA1-g1",
    "body": "<p>Cas9 + BRCA1 gRNA #1 from Addgene #XXXXX.</p>",
    "metadata": {"resistance": "AmpR", "insert": "BRCA1 gRNA #1", "promoter": "U6"},
    "tags": ["crispr", "brca1"],
}
r = requests.post(f"{API}/items", headers=headers, auth=auth, json=payload)
item = r.json()
print(f"Plasmid id={item['id']} title={item['title']}")

# Link a database item to an experiment
requests.post(f"{API}/experiments/{exp_id}/links", headers=headers, auth=auth,
              json={"item_id": item["id"]})

# Search database items
r = requests.get(f"{API}/items", auth=auth,
                 params={"q": "BRCA1", "limit": 20})
hits = r.json()
print(f"Found {len(hits)} items matching 'BRCA1'")
for h in hits[:5]:
    print(f"  id={h['id']} {h['title']}")
```

```python
# Update metadata (e.g., add a qc result to a plasmid item)
r = requests.patch(f"{API}/items/{item['id']}", headers=headers, auth=auth,
                   json={"metadata": {"resistance": "AmpR", "qc_sanger": "passed 2026-06-12"}})
```

### Module 3: Inventory (storage locations and containers)

eLabFTW tracks physical locations (freezers, shelves, rooms) and the containers (boxes, plates, tubes) inside them. Every container has a barcode string and a parent location.

```python
# List storage locations
r = requests.get(f"{API}/storage", auth=auth)
locations = r.json()
for loc in locations[:5]:
    print(f"  {loc['id']}: {loc['name']} ({loc['location_type']})")
```

```python
# Create a container (e.g., a 96-well plate in a freezer box)
container_payload = {
    "title": "Plate 2026-06-10 BRCA1 screen",
    "location_id": 3,                # parent storage location
    "container_type": "96-well plate",
    "barcode": "PLT-2026-06-10-A",
    "metadata": {"assay": "BRCA1 CRISPR screen", "date": "2026-06-10"},
}
r = requests.post(f"{API}/containers", headers=headers, auth=auth, json=container_payload)
c = r.json()
print(f"Container id={c['id']} barcode={c['barcode']}")

# Add stored items (e.g., each well = a sample database item)
requests.post(f"{API}/containers/{c['id']}/items", headers=headers, auth=auth,
              json={"item_id": item["id"], "position": "A1"})
```

### Module 4: Equipment and bookings

eLabFTW has a built-in scheduler for shared equipment with conflict detection.

```python
# List bookable equipment
r = requests.get(f"{API}/team_events/resources", auth=auth)
for r_ in r.json():
    print(f"  {r_['id']}: {r_['name']} (category {r_['category_id']})")

# Book a 2-hour window on the qPCR machine
from datetime import datetime, timedelta
start = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
end   = (datetime.utcnow() + timedelta(hours=2)).isoformat() + "Z"

r = requests.post(f"{API}/team_events", headers=headers, auth=auth,
                  json={
                      "item_id": 7,           # the equipment database item id
                      "title": "qPCR — BRCA1 screen validation",
                      "start": start,
                      "end": end,
                      "book_is_full": False,
                  })
print("Booking response:", r.status_code, r.text[:120])
```

### Module 5: Files (uploads to experiments and items)

Attach images, PDFs, plate-reader output, gel images, and sequence files. eLabFTW handles long-term storage and offers per-file access control.

```python
# Upload a file to an experiment
with open("gel_image.jpg", "rb") as f:
    r = requests.post(
        f"{API}/experiments/{exp_id}/uploads",
        auth=auth,
        files={"file": ("gel_image.jpg", f, "image/jpeg")},
        data={"comment": "Agarose gel — BRCA1 PCR products"},
    )
print("Upload status:", r.status_code, r.json().get("real_name", ""))

# Long-term storage: eLabFTW supports archive mode where files are checksummed
# and signed; verify via GET /experiments/{id}/uploads
r = requests.get(f"{API}/experiments/{exp_id}/uploads", auth=auth)
for u in r.json():
    print(f"  {u['real_name']} sha256={u.get('hash', 'n/a')[:16]}…")
```

### Module 6: Search, tags, and audit log

```python
# Full-text search across experiments and items
r = requests.get(f"{API}/experiments", auth=auth,
                 params={"q": "BRCA1", "limit": 20})
for e in r.json():
    print(f"  exp {e['id']}: {e['title']} (tags: {e.get('tags', [])})")

# Audit log (who did what, when) — for compliance
r = requests.get(f"{API}/experiments/{exp_id}/revisions", auth=auth)
for rev in r.json():
    print(f"  {rev['created_at']} by user {rev['userid']}: {rev['body_diff'][:80]}")
```

## Key Concepts

### Permission tiers

| Role | Can read | Can write | Can lock | Can administer |
|------|---------|-----------|---------|----------------|
| Anonymous (if enabled) | yes | no | no | no |
| User | yes | yes | own experiments | no |
| Admin | yes | yes | any | yes |

API keys inherit the role of the user that issued them. For shared automations, create a service account with the minimum role needed.

### Locking and signing

Once an experiment is locked, its body cannot be edited. A timestamp and a SHA-256 hash of the body are recorded. Use this to anchor an experiment to a point in time, satisfying electronic-signature requirements (FDA 21 CFR Part 11 in regulated contexts). The `lock` and `timestamp` actions are exposed via the API.

### Tags vs categories

- **Category** (status): one of the lab-defined statuses — e.g., "Running", "Completed", "Abandoned". Drives workflow reporting.
- **Tags**: free-form labels for search and grouping — e.g., "crispr", "screen-2026".

```python
# Set category and tags
requests.patch(f"{API}/experiments/{exp_id}", headers=headers, auth=auth,
               json={"category_id": 5, "tags": ["crispr", "screen-2026", "priority-high"]})
```

## Common Workflows

### Workflow 1: Record an Opentrons run

```python
import os
import requests
from requests.auth import HTTPBasicAuth

API = "https://eln.example.org/api/v2"
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])
headers = {"Content-Type": "application/json"}

# Create the experiment
r = requests.post(f"{API}/experiments", headers=headers, auth=auth,
                  json={
                      "title": "Opentrons OT-2 run — 2026-06-10 — plate reformat",
                      "body": "<h2>Run</h2><p>96->96 plate stamp, fresh tips.</p>",
                      "tags": ["opentrons", "plate-reformat"],
                  })
exp = r.json()

# Link the source and destination plate database items
for item_id in (12, 13):
    requests.post(f"{API}/experiments/{exp['id']}/links", headers=headers,
                  auth=auth, json={"item_id": item_id})

# Append the run log
log_path = "opentrons_run_log.txt"
with open(log_path) as f:
    log = f.read()
requests.post(f"{API}/experiments/{exp['id']}", headers=headers, auth=auth,
              json={"bodyappend": f"<h2>Run log</h2><pre>{log}</pre>"})

# Upload the run log file
with open(log_path, "rb") as f:
    requests.post(f"{API}/experiments/{exp['id']}/uploads", auth=auth,
                  files={"file": (log_path, f, "text/plain")})

print(f"Run recorded: https://eln.example.org/experiments.php?mode=view&id={exp['id']}")
```

### Workflow 2: Bulk import reagents from a CSV

```python
import csv
import os
import requests
from requests.auth import HTTPBasicAuth

API = "https://eln.example.org/api/v2"
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])
headers = {"Content-Type": "application/json"}

def get_or_create_item_type(name, color="#3366CC"):
    """Return id of an item type, creating it if it does not exist."""
    types = requests.get(f"{API}/items_types", auth=auth).json()
    for t in types:
        if t["title"] == name:
            return t["id"]
    r = requests.post(f"{API}/items_types", headers=headers, auth=auth,
                      json={"title": name, "color": color})
    return r.json()["id"]

reagent_type = get_or_create_item_type("Reagents")
created = []
with open("reagents.csv") as f:
    for row in csv.DictReader(f):
        r = requests.post(f"{API}/items", headers=headers, auth=auth, json={
            "category_id": reagent_type,
            "title": row["name"],
            "metadata": {"vendor": row["vendor"], "catalog": row["catalog"], "lot": row["lot"]},
            "tags": [t.strip() for t in row.get("tags", "").split(";") if t.strip()],
        })
        if r.ok:
            created.append(r.json()["id"])
print(f"Imported {len(created)} reagents")
```

### Workflow 3: Generate an experiment summary report

```python
import os
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

API = "https://eln.example.org/api/v2"
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])

r = requests.get(f"{API}/experiments", auth=auth, params={"limit": 200})
exps = r.json()
df = pd.DataFrame([{
    "id": e["id"],
    "title": e["title"],
    "status": e.get("category_title", ""),
    "date": e.get("date", ""),
    "tags": ";".join(e.get("tags", [])),
} for e in exps])
df.to_csv("experiment_summary.csv", index=False)
print(f"Wrote {len(df)} experiments to experiment_summary.csv")
```

## Key Parameters

| Parameter | Endpoint | Default | Range / Options | Effect |
|-----------|----------|---------|-----------------|--------|
| `category_id` | experiments, items | required | int | Status / item type id; use `GET /items_types` to list |
| `tags` | experiments, items | `[]` | list of strings | Free-form labels for search |
| `body` | experiments, items | `""` | HTML string | Long-form rich-text content |
| `bodyappend` | experiments | — | HTML string | Append HTML to existing body |
| `metadata` | items | `{}` | JSON object | Typed fields for the item type |
| `limit` | list endpoints | `50` | `1`–`100` | Page size |
| `offset` | list endpoints | `0` | int | Pagination offset |
| `q` | list endpoints | — | string | Full-text search query |
| `barcode` | containers | optional | string | Physical barcode; unique per container |

## Best Practices

1. **Treat the API key as a password.** Use environment variables, never commit. Rotate when a user leaves the lab.

2. **Lock experiments only when truly done.** Locking is irreversible without admin intervention. Use the lock as the boundary between "in progress" and "archived".

3. **Use database items, not free-text bodies, for reusable reagents.** A well-typed reagent item with metadata (vendor, lot, storage location) is searchable, linkable, and version-controlled across all your experiments.

4. **Tag with a project prefix.** A consistent tag scheme like `screen-2026`, `gfp-trap`, `screen-2026-q2` makes group-wide queries simple.

5. **Backup before bulk operations.** `POST /items/bulk` and `PATCH /experiments/{id}` are fast; an `items_types` table wipe is faster. Snapshot the database before any large migration.

6. **Prefer `PATCH` over repeated `POST`.** Some endpoints accept an `action` field (e.g., `lock`); others require `PATCH` for partial updates. Check the API docs for each resource.

7. **Link early.** Linking a database item to an experiment at creation time (not after) keeps your inventory map accurate.

8. **Use the audit log for compliance.** eLabFTW records every edit; for regulated work, the `revisions` endpoint gives a tamper-evident timeline of who changed what.

## Common Recipes

### Recipe: Find all experiments using a specific reagent

```python
import os
import requests
from requests.auth import HTTPBasicAuth

API = "https://eln.example.org/api/v2"
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])

reagent_id = 4711
# eLabFTW stores link tables; query the link endpoint for the item
r = requests.get(f"{API}/items/{reagent_id}/experiments", auth=auth)
print(f"Reagent {reagent_id} used in {len(r.json())} experiments")
for e in r.json():
    print(f"  exp {e['id']} {e['title']}")
```

### Recipe: Lock and sign an experiment

```python
import os
import requests
from requests.auth import HTTPBasicAuth

API = "https://eln.example.org/api/v2"
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])
headers = {"Content-Type": "application/json"}

exp_id = 12345
# Lock creates a SHA-256 hash of the body, recorded with timestamp and user
r = requests.post(f"{API}/experiments/{exp_id}", headers=headers, auth=auth,
                  json={"action": "lock"})
print("Lock response:", r.status_code, r.json().get("locked_at", ""))
```

### Recipe: Book a microscope for a time block

```python
import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

API = "https://eln.example.org/api/v2"
auth = HTTPBasicAuth(os.environ["ELN_USERNAME"], os.environ["ELN_API_KEY"])
headers = {"Content-Type": "application/json"}

start = datetime.utcnow().replace(microsecond=0, second=0, minute=0)
end   = start + timedelta(hours=2)
r = requests.post(f"{API}/team_events", headers=headers, auth=auth, json={
    "item_id": 9,                          # microscope database item
    "title": "Confocal — BRCA1 screen imaging",
    "start": start.isoformat() + "Z",
    "end":   end.isoformat() + "Z",
})
print("Booking:", r.status_code, r.json().get("id", r.text))
```

## Expected Outputs

- A web URL for each created experiment: `https://<host>/experiments.php?mode=view&id=<id>`
- Database item URLs: `https://<host>/database.php?mode=view&id=<id>`
- File attachments stored on the eLabFTW instance filesystem; downloadable from the experiment page
- JSON responses from the API; the same data is visible in the eLabFTW web UI

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `401 Unauthorized` | Wrong credentials, expired API key | Regenerate the key in user profile; check `ELN_USERNAME` and `ELN_API_KEY` env vars |
| `403 Forbidden` | User lacks write access | Ask the lab admin to elevate the user role; or use a different API key |
| `404 Not Found` | Wrong id, or resource is in another team | Confirm the experiment/item id; eLabFTW scopes by team — check that the API key belongs to the right team |
| `400` on body content | Invalid HTML or oversized body | Strip `<script>` tags; eLabFTW sanitizes but rejects malformed HTML; check the body size limit in your config |
| Files fail to upload | Filesystem full, or wrong perms | Check the eLabFTW `ELABFTW_UPLOAD_DIR`; default `/var/elabftw/uploads/` |
| Search returns nothing | Index not built | Run `bin/console experimpent-types:update` (or the v5 equivalent) to rebuild the search index |
| Locked experiment edits fail | Locked state | Locked experiments are read-only by design. Re-open requires admin; the API does not expose a clean "unlock" for compliance reasons |

## References

- [eLabFTW official documentation](https://doc.elabftw.net/) — install, configure, API
- [eLabFTW API reference (v2)](https://doc.elabftw.net/api/) — full endpoint catalog
- [eLabFTW GitHub repository](https://github.com/elabftw/elabftw) — source code and releases
- [eLabFTW Docker image](https://hub.docker.com/r/elabftw/elabftw) — quick self-host
- [eLabFTW community forum](https://github.com/elabftw/elabftw/discussions) — Q&A and announcements

## Related Skills

- `eln-chemotion` — open chemistry ELN with built-in molecule editor and reaction handling
- `eln-openbis` — open LIMS/ELN designed for high-throughput assay and sample tracking
- `protocolsio-protocol-repository` — search and import published protocols
- `opentrons-ot2-protocols` — automated liquid-handling protocols; record runs in eLabFTW
- `plannotate-plasmid-annotation` — annotate plasmid database items before linking to experiments