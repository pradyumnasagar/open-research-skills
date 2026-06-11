---
name: licensing
description: "Use when choosing a Creative Commons license (CC0, CC-BY, CC-BY-SA) for data, picking a software license (MIT, Apache-2.0, GPL), handling EU database sui generis rights, or planning dual-licensing for a research project."
license: MIT
---



<!-- metadata:
category: open-science
version: 1.0.0
author: Pradyumna Jayaram
tags:
- licensing
- creative-commons
- mit
- apache
- gpl
- open-source
- database-rights
- dual-licensing
difficulty: intermediate
prerequisites:
  tools:
  - web-browser
  - knowledge of project IP situation
  skills: []"
sources: "Original: Creative Commons license chooser and license deeds (https://creativecommons.org/licenses/).;\
  \ Original: Open Source Initiative (OSI) approved licenses (https://opensource.org/licenses).;\
  \ Original: Software Package Data Exchange (SPDX) license list (https://spdx.org/licenses/).;\
  \ Original: GNU General Public License v3 (https://www.gnu.org/licenses/gpl-3.0.html).;\
  \ Original: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0).; Original:\
  \ MIT license (https://opensource.org/licenses/MIT).; Original: EU Directive 96/9/EC\
  \ on the legal protection of databases (database sui generis right).; Original:\
  \ Wellcome Trust open access policy 2024+.; Original: Plan S rights retention strategy.;\
  \ Improvisions: Pradyumna Jayaram — license decision trees (data, code, mixed,\
  \ databases), the 'what does open mean here' table, dual-licensing flowchart, common-failure\
  \ table."
-->

# Licensing

> A license is the legal frame around an open output: it says what others may do with your code, data, or text. Choosing the wrong license is the single most common cause of "I made it open but no one can use it" — a CC-BY-NC clause forbids commercial use and disqualifies most industrial users; a GPL copyleft clause surprises users who expected permissiveness; a missing license is "all rights reserved" by default, even if the file is on GitHub. This skill gives a decision tree for data, code, and databases, and explains the "what does open mean in different contexts" question that confuses researchers and policymakers alike.

## When to use

- Picking a **Creative Commons license** for a dataset, figure, or supplementary file.
- Picking a **software license** (MIT, Apache-2.0, BSD, GPL, AGPL) for a research code release.
- Deciding between **CC0, CC-BY-4.0, CC-BY-SA-4.0** for data.
- Handling **EU database rights** (the sui generis right) when releasing a database.
- Setting up **dual licensing** for a project that has both academic and commercial users.
- Responding to funder mandates (Plan S, Wellcome, NIH) that specify CC-BY-4.0.
- Choosing the right license for a **mixed output** (code + data + manuscript + figures).
- Auditing a project for **license compatibility** with its dependencies.
- Resolving disputes: "Can I use this figure in a textbook?" "Can I use this code in a commercial product?"

## When NOT to use

- For **authorship / copyright transfer** to a journal — that is a separate (and complex) matter, handled by the journal's author agreement.
- For **trademark** protection of a project name — the Apache-2.0 license includes a trademark grant; MIT and BSD do not.
- For **patent** issues — Apache-2.0 has an explicit patent grant; MIT does not.
- For **privacy** of human-subject data — see `ors-ethics-compliance-` skills (HIPAA, GDPR).
- For **export-control** of dual-use research — separate from licensing.

## Prerequisites

- An understanding of **what is being licensed** (code, data, manuscript text, figure, database).
- An understanding of **who will use it** (academics, industry, general public, government).
- An understanding of **what restrictions apply** (funder mandates, institutional IP policies, journal policies, third-party content embedded in your work).

## Core workflow

1. **Identify the asset type.** Code, data, text/figure, database, mixed.
2. **Identify the audience.** Academic only, academic + industry, public, government.
3. **Identify external constraints.** Funder mandate, journal policy, third-party content.
4. **Pick the license family** (see decision trees).
5. **Apply the license text** (not a one-liner — use the canonical full text or a recognised SPDX identifier).
6. **State the license clearly in the README and in the LICENSE file.**
7. **Audit dependencies** for license compatibility.
8. **Document the choice** in the data availability statement or the methods section.

## Document patterns

### Pattern 1: What does "open" mean in different contexts?

| Context | "Open" means | License convention | Caveat |
|---------|--------------|--------------------|--------|
| **Open source code** | Anyone can use, modify, redistribute (with attribution). | OSI-approved license: MIT, Apache-2.0, BSD, GPL, etc. | "Source-available" (you can see it but can't use it) is **not** open source. |
| **Open access publication** | The article is free to read, with reuse rights. | CC-BY-4.0 (most permissive) to CC-BY-NC-ND-4.0 (most restrictive). | "Free to read" is not enough; without reuse rights, it is "open access lite." |
| **Open data** | Anyone can use, modify, redistribute the data. | CC0 (no attribution required) or CC-BY-4.0 (attribution required). | "Available upon request" is not open data. |
| **FAIR data** | Findable, Accessible, Interoperable, Reusable. | Often CC-BY-4.0 or CC0. | FAIR does not require open; it requires well-described and accessible under a clear license. |
| **Open educational resources (OER)** | Free to use, adapt, share. | CC-BY-SA-4.0 (typical) or CC-BY-4.0. | "Non-commercial" clauses are usually problematic for OER. |
| **Open hardware** | Schematics, BOM, code are open. | CERN Open Hardware License (CERN-OHL), TAPR, or CC-BY-4.0 for documentation. | |
| **Open source AI model** | Anyone can use, fine-tune, redistribute. | OSI's "Open Source AI Definition" 2024. | "Open weights" (e.g., Llama 2) is not the same as "open source." |
| **Open peer review** | Reviews are public, signed or anonymous. | Reviewer identity: open identity, open interaction, open content. | "Open" here refers to the review process, not the license. |

### Pattern 2: Decision tree for data (Creative Commons)

```
What is the asset?
├── Raw or aggregated dataset (csv, tsv, fasta, fastq, mzML, etc.)
│   └── CC0 1.0 (most permissive, no attribution needed)
│       OR CC-BY-4.0 (attribution required; funders like Plan S prefer this)
│
├── Processed / curated database (PDB, UniProt, GenBank)
│   └── CC-BY-4.0 (use + attribution); some use CC0 for the raw data
│
├── A figure or plot
│   └── CC-BY-4.0 (in the paper) or reuse permission from publisher
│
├── Manuscript text
│   └── Journal-specific (most open-access journals use CC-BY-4.0;
│       some hybrid journals use CC-BY-NC-ND-4.0)
│
├── Educational material (slides, course notes)
│   └── CC-BY-SA-4.0 (forces derivative works to remain open)
│
└── Mixed / unsure
    └── Default to CC-BY-4.0
```

### Pattern 3: Decision tree for code (OSI-approved)

```
Will the code be used in commercial products?
├── YES → Avoid GPL family (forces derivatives to be GPL)
│        Use MIT or Apache-2.0
└── NO  → Does your org require copyleft (e.g., GNU, Linux kernel)?
         ├── YES → GPL-3.0
         └── NO  → Apache-2.0 (default; explicit patent grant)
                  OR MIT (shorter; no patent grant)
```

| License | Permissions | Conditions | Limitations | Patent grant? | Use when |
|---------|-------------|-----------|-------------|---------------|----------|
| **MIT** | Use, copy, modify, merge, publish, distribute, sublicense, sell | Preserve copyright + license notice | No liability, no warranty | No | Small libraries, scripts, academic code; permissive default. |
| **Apache-2.0** | Same as MIT | Copyright + license + NOTICE + state changes | Same | **Yes (explicit)** | Code that may be patent-encumbered; default for industry-facing. |
| **BSD-2 / BSD-3** | Same as MIT | Copyright + license | Same | No (BSD-3 has "no endorsement" clause) | Equivalent to MIT for most purposes. |
| **GPL-2.0 / GPL-3.0** | Use, copy, modify, distribute | **Copyleft**: derivatives must be GPL | Same | GPL-3: yes | Software that should remain open; GNU/Linux ecosystem. |
| **LGPL-2.1 / LGPL-3.0** | Use, modify (with conditions for linking) | Weak copyleft (only the library, not the whole program, must be LGPL) | Same | LGPL-3: yes | Libraries that should remain open but allow linking. |
| **AGPL-3.0** | Same as GPL + network use is distribution | Strong copyleft: even SaaS use requires source release | Same | Yes | Network services: ensures SaaS users get source. |
| **MPL-2.0** | Use, modify, distribute | File-level copyleft (only MPL-licensed files must be MPL) | Same | Yes | Mozilla: file-level copyleft, more permissive than GPL. |
| **Unlicense** | Public-domain-equivalent | None | No warranty | No | Equivalent to CC0 for code; rarely used. |
| **BSL (Business Source License)** | Delayed open source | After N years, converts to OSI license | Time-delayed | No | "Source-available" until conversion; not OSI-approved. |
| **SSPL (Server Side Public License)** | Use, modify, distribute | Service operators must release the entire stack as SSPL | Same | No | MongoDB's license; not OSI-approved. |

**Practical defaults:**

- For a research tool / analysis code: **MIT** or **Apache-2.0**.
- For a research framework others will build on: **Apache-2.0** (patent grant).
- For a foundational algorithm / "Linux of biology": **GPL-3.0** (copyleft).
- For a SaaS tool: **AGPL-3.0** if you want to prevent closed forks.

### Pattern 4: Decision tree for databases (EU database rights)

```
Is the database "substantial" (EU: 5,000+ records, or "substantial investment in obtaining, verifying, or presenting")?
├── YES → Two layers of rights apply:
│         1. Copyright (if the database is "the author's own intellectual creation")
│         2. **Database sui generis right** (EU Directive 96/9/EC):
│            - Prevents extraction/re-utilization of "the whole or a substantial
│              part" of the database contents
│            - 15-year term from publication; renewed if "substantial new investment"
│         Apply CC-BY-4.0 (or CC0) to waive both.
└── NO  → Database is just a file; treat it as data.
```

In the EU, a database has a **two-tier** protection:

1. **Copyright** in the selection/arrangement (if original).
2. **Sui generis right** (a property right, not copyright) for the maker who invested in obtaining, verifying, or presenting the database. This is what makes "scraping the whole GenBank" legally risky even when the data is public.

In the US, the sui generis right does not exist; only copyright applies (and Feist v. Rural Telephone Service 1991 held that mere facts are not copyrightable). A phone book has no copyright in the US; it has sui generis protection in the EU.

**Mitigation:** applying CC0 to the database waives the sui generis right (where the law permits). Applying CC-BY-4.0 retains attribution. Always consult legal counsel for high-stakes database releases.

### Pattern 5: Dual-licensing for academic + commercial

```
You are the copyright holder.
You want: (1) academic users get it free, (2) commercial users pay.

Approach A: Dual-license
  - Public repo with AGPL-3.0 (or GPL-3.0) for academic use
  - Separate commercial license (paid) for companies that want MIT-like terms
  - This is what MySQL, MongoDB (pre-SSPL), Qt, and others do.

Approach B: "Open core"
  - Public repo with permissive license (MIT, Apache-2.0)
  - Commercial features (e.g., enterprise support, cloud hosting) sold separately
  - The "core" stays open.

Approach C: BSL → conversion to OSS
  - Public repo with Business Source License (BSL) for N years
  - After N years, auto-converts to a permissive OSS license (e.g., Apache-2.0)
  - HashiCorp, MariaDB, CockroachDB use this.
```

### Pattern 6: The "LICENSE" file and the SPDX header

A `LICENSE` file in the root of a repo, with the full license text. The `README` should reference the SPDX identifier:

```markdown
## License

This project is licensed under the Apache License 2.0 — see [LICENSE](LICENSE).

`SPDX-License-Identifier: Apache-2.0`
```

For source files, the SPDX header convention:

```python
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pradyumna Jayaram
```

### Pattern 7: License audit script (Python)

```python
# pip-licenses CLI: https://pypi.org/project/pip-licenses/
# Lists all third-party licenses and flags incompatibility.

# pip install pip-licenses
# pip-licenses --format=markdown --with-urls > THIRD_PARTY_LICENSES.md

# Compatibility heuristic:
# - MIT, BSD-2, BSD-3, Apache-2.0, Unlicense: all compatible with each other
#   and with GPL-3.0.
# - GPL-2.0-only and Apache-2.0-only: sometimes incompatible (depending on
#   version of each). Use GPL-2.0-or-later.
# - AGPL-3.0: stronger than GPL; cannot be used in a closed SaaS without
#   releasing source.
# - SSPL, BSL, RPL: not OSI-approved; may not be combined with GPL.
```

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| **No license at all** | All rights reserved by default under copyright law; even "look but don't touch" is the legal default | Add a license file. `choosealicense.com` helps. |
| **CC-BY-NC on data** | "Non-commercial" excludes industry, clinical labs, government users; also ambiguous (is a research scientist at a for-profit company commercial?) | Use CC0 or CC-BY-4.0 for data. CC-BY-NC is acceptable for text where the journal mandates it. |
| **GPL on a research tool that industry wants to use** | Companies will not adopt a GPL tool; they fork or wait for an MIT-licensed alternative | Use MIT or Apache-2.0 by default. |
| **Mixing GPL-2.0-only and Apache-2.0-only** | Incompatible per the FSF | Use `-or-later` (`GPL-2.0-or-later`) or upgrade to GPL-3.0. |
| **Using a figure with CC-BY-NC-ND in a derivative work** | ND forbids derivatives; cannot use in a review article | Get permission or use a CC-BY-4.0 version. |
| **Code licensed "MIT" but the data licensed "all rights reserved"** | Inconsistent; confusing for users | Pick a license for each asset and state it. |
| **Reusing MIT-licensed code without preserving the copyright notice** | Violates the license; the user's code becomes legally exposed | Keep the copyright + license notice in source files. |
| **Putting a CC-BY-SA clause in a dataset** | "Copyleft" for data is unusual; downstream users may stop using it | Use CC-BY-4.0 for data; reserve CC-BY-SA for educational / collaborative works. |
| **Adding a license after the fact** | Code committed before the license was added is in a legal grey area | Add the license to the FIRST commit; add a `LICENSE` file in the initial commit. |
| **Assuming CC0 waives moral rights in France/Germany** | Moral rights cannot be waived in some EU jurisdictions | CC0 includes a fallback license; consult legal counsel for high-value releases. |
| **Database scraped from a CC-BY-NC source** | The CC-BY-NC forbids commercial use of the database contents; republishing as "open" is a license violation | Use only CC-BY-4.0 or CC0 sources; respect upstream licenses. |
| **Asking for a "no commercial use" license on a preprint** | Almost no one enforces it; funder policies forbid it; lawyers advise against it | Default to CC-BY-4.0 for preprints. |
| **Confusing SPDX with copyright** | SPDX is an identifier (e.g., `MIT`), not a license | Always include the full LICENSE text; SPDX is the machine-readable shorthand. |
| **EU sui generis right not waived** | Someone can sue for "substantial extraction" of your database, even if the data is public | Apply CC0 to the database. |
| **Using a figure from a CC-BY-NC source in a thesis chapter that is sold as a book** | The book is commercial; CC-BY-NC forbids it | Get explicit permission or use a CC-BY source. |
| **Not auditing third-party licenses** | A GPL dependency in an MIT project may force re-licensing | Run `pip-licenses` and `npm ls --license` regularly. |

## Validation

A licensing decision is "well-made" when:

- [ ] The license is recorded in a `LICENSE` file at the root of the repo / data deposit.
- [ ] The README cites the license by name and SPDX identifier.
- [ ] Each source file (for code) has a SPDX header.
- [ ] The license is compatible with all third-party dependencies (`pip-licenses`, `npm ls --license`).
- [ ] The license is appropriate for the audience (academic + industry → MIT/Apache; foundational copyleft → GPL).
- [ ] The license is consistent across all artifacts (code, data, manuscript, figures).
- [ ] The license is in the data-availability statement of the paper.
- [ ] For EU databases, the sui generis right is explicitly waived (via CC0) or the implications are understood.

A simple test:

```bash
# In a clean checkout:
ls LICENSE
grep -E "^# SPDX-License-Identifier:" *.py
# Check that no file in the repo has "all rights reserved" without an override.
```

## Open alternatives

| "Restricted" license | Open alternative | Trade-off |
|----------------------|------------------|-----------|
| CC-BY-NC (non-commercial) | CC-BY-4.0 | Loses the "non-commercial" restriction; gains industry reusers. |
| CC-BY-ND (no derivatives) | CC-BY-4.0 | Loses the no-derivatives clause; users can remix. |
| CC-BY-NC-ND (most restrictive) | CC-BY-4.0 (data) or CC-BY-SA-4.0 (educational) | Loses both restrictions. |
| Proprietary EULA | MIT, Apache-2.0 | Loses the proprietary lock-in; gains a community. |
| BSL / SSPL (delayed open) | AGPL-3.0 (immediate open) | BSL/SSPL are not OSI-approved; AGPL is OSI-approved and stronger. |
| AGPL-3.0 (network copyleft) | Apache-2.0 + CLA (contributor license agreement) | AGPL is open; the CLA is institutional, not the license. |
| "All rights reserved" + dual license | MIT + commercial addendum (e.g., MongoDB) | The dual-license model works for many companies. |
| Closed-access journal | Open-access journal with CC-BY-4.0 | Loses subscription revenue (a publisher concern, not a researcher's). |

## References

- Creative Commons license deeds: https://creativecommons.org/licenses/
- Creative Commons license chooser: https://creativecommons.org/choose/
- Creative Commons FAQ: https://creativecommons.org/faq/
- Open Source Initiative (OSI) approved licenses: https://opensource.org/licenses
- Choose a License: https://choosealicense.com/
- SPDX license list: https://spdx.org/licenses/
- GNU General Public License v3: https://www.gnu.org/licenses/gpl-3.0.html
- GNU licenses FAQ: https://www.gnu.org/licenses/gpl-faq.html
- Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
- MIT license: https://opensource.org/licenses/MIT
- BSD licenses: https://opensource.org/licenses/BSD-2-Clause
- Mozilla Public License 2.0: https://www.mozilla.org/en-US/MPL/2.0/
- EU Directive 96/9/EC (database legal protection): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:31996L0009
- Wellcome Trust open access policy: https://wellcome.org/grant-funding/guidance/open-access-guidance
- Plan S Rights Retention Strategy: https://www.coalition-s.org/plan-s-rights-retention-strategy-explained/
- Software Freedom Conservancy: https://sfconservancy.org/
- Free Software Foundation: https://www.fsf.org/
- Open Knowledge Foundation: https://okfn.org/
- pip-licenses: https://pypi.org/project/pip-licenses/

## Related skills

- `ors-open-science-fair-data` — for the data side of the licensing decision.
- `ors-open-science-code-release` — for the code side of the licensing decision.
- `ors-ethics-compliance-` (multiple skills) — for the legal and privacy side.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesised Creative Commons license deeds; Open Source Initiative license list; SPDX license list; GNU, Apache, MIT, MPL, BSD license texts; EU Directive 96/9/EC on database rights; Wellcome Trust open access policy; Plan S rights retention strategy. "What does open mean" matrix, code/data/database decision trees, dual-licensing flowchart, and license compatibility table are original compositions.