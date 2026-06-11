---
name: data-privacy
description: "Use when designing or reviewing the privacy plan for a study that uses"
license: MIT
---



<!-- metadata:
category: ethics-compliance
version: 1.0.0
author: Pradyumna Jayaram
tags:
- hipaa
- gdpr
- de-identification
- privacy
- federated-learning
- datathon
- sirb
- certificate-of-confidentiality
difficulty: advanced
prerequisites:
  tools: []
  skills:
  - ors-ethics-compliance-irb-protocol
sources: 'Original: 45 CFR 164.514 (HIPAA de-identification); Adapted: Safe Harbor
  vs Expert Determination decision matrix; Original: GDPR Articles 4, 6, 9, 13, 14,
  89 (Regulation EU 2016/679); Adapted: research-specific lawful bases and safeguards;
  Original: NIH Genomic Data Sharing Policy; Adapted: data-use-agreement template
  language; Original: 42 USC 241(d) Certificate of Confidentiality authority (revised
  2017); Adapted: CoC applicability checklist; Improvisions: datathon-specific guidance
  (data enclave, synthetic data, output review), federated learning primer, differential-privacy
  intuition, IRB + DUA coordination'
-->

# Data Privacy for Research

> Data privacy for research is the joint project of a federal regulation (HIPAA in the U.S. for health data, GDPR in the EU for personal data more broadly), an institutional oversight body (the IRB), and a contract (the Data Use Agreement or DUA). A defensible research privacy plan names the regulation that applies, the legal basis for processing, the de-identification or pseudonymization method, the controls on access, the breach-notification plan, and the documents (DUA, IRB approval, Certificate of Confidentiality) that enforce the plan. This skill encodes the HIPAA Safe Harbor and Expert Determination methods, the research-relevant GDPR articles, the de-identification and pseudonymization techniques, the privacy-preserving-analysis alternatives (federated learning, differential privacy, data enclaves, synthetic data), the role of single-IRB (sIRB) and Certificates of Confidentiality, and the patterns that show up in datathons, registries, and secondary-data studies.

## When to use

- Drafting the data-management and privacy sections of an IRB protocol that handles identifiable or potentially identifiable data.
- Negotiating or reviewing a Data Use Agreement (DUA), Business Associate Agreement (BAA), or Data Access Agreement (DAA) with a data provider (NIH dbGaP, NCI Cancer Research Data Commons, Synapse, Vivli, partner health system, commercial vendor).
- Designing or participating in a data science competition (datathon) that uses protected health information (PHI) or personal data.
- Planning a federated or privacy-preserving analysis when the data cannot leave the originating institution.
- Preparing a study for the EU (any EU site, any EU subject) or for cross-border data transfer.
- Determining whether a Certificate of Confidentiality applies and how to invoke it.

## When NOT to use

- The study is animal or in vitro only — no human data, no privacy regime. Use `ors-ethics-compliance-irb-protocol` only if specimens are linked to identifiable human data.
- You are working with de-identified data that meets all 18 Safe Harbor identifiers are removed AND you have no actual knowledge of re-identifiability — HIPAA does not apply, and GDPR likely does not apply either. Document the determination, do not assume it.
- The question is IRB review level (exempt, expedited, full board). That is `ors-ethics-compliance-irb-protocol`.
- The question is FDA-regulated clinical trial privacy. FDA has separate rules on records and reporting (21 CFR 312) that interact with HIPAA. Use `ors-clinical-decision-regulatory` for FDA side.

## Prerequisites

- Understanding of the data you plan to use: what identifiers it carries, how it was collected, who the original data controller is, what the data subject's consent says.
- For U.S. health data: familiarity with HIPAA (45 CFR 160, 162, 164) — particularly 164.514 for de-identification.
- For EU data: familiarity with GDPR (Regulation EU 2016/679) — particularly Articles 4, 5, 6, 9, 13, 14, 28, 32, 44-49, 89.
- Knowledge of your institution's data-use-agreement template and your privacy officer / data protection officer (DPO).
- For NIH-funded genomic or broad-scale data: familiarity with the NIH Genomic Data Sharing Policy and the dbGaP data-access mechanism.

## Core workflow

1. **Inventory the data.** What fields are in the dataset? Which are direct identifiers, which are indirect identifiers, which are sensitive-but-not-identifying (e.g., diagnosis code, age, sex)? Build a field-by-field table; the de-identification method depends on this table.

2. **Identify the applicable regulation(s).** Common cases:
   - PHI from a U.S. covered entity (hospital, health plan, clearinghouse) or business associate → HIPAA.
   - Personal data of an EU resident → GDPR (regardless of where the researcher sits)."
   - Identifiable biospecimens with a code linking them to the donor → may be PHI or "identifiable private information" under the Common Rule, regardless of HIPAA.
   - Data from a federal funder (NIH, NSF) with a Genomic Data Sharing plan → GDS Policy.
   - Two or more of the above → multiple regimes; the strictest governs.

3. **Pick a de-identification method** if your goal is to remove data from the regulatory perimeter:
   - **HIPAA Safe Harbor (45 CFR 164.514(b)(2))**: remove 18 categories of identifiers plus no actual knowledge of re-identifiability.
   - **HIPAA Expert Determination (45 CFR 164.514(b)(1))**: a qualified statistician applies generally accepted methods and certifies that the risk of re-identification by an "anticipated recipient" is very small.
   - **GDPR pseudonymization (Article 4(5))**: removal of identifiers plus a separately secured key. Pseudonymized data is still personal data under GDPR; only fully anonymous data is out of scope.
   - **Common Rule "identifiable" vs "de-identified"**: 45 CFR 46.102(e) defines both. The Common Rule applies to "identifiable private information" or "identifiable biospecimens."

4. **For data you cannot de-identify**, layer controls:
   - **Data Use Agreement** (HIPAA 164.504(e)) for limited data sets.
   - **Business Associate Agreement** (HIPAA 164.504(e)) when the recipient acts on behalf of a covered entity.
   - **Data Access Agreement** (NIH model) for controlled-access repositories (dbGaP, NHGRI AnVIL, Kids First, NCI CRDC).
   - **IRB approval** for the receiving protocol.
   - **Certificate of Confidentiality** (42 USC 241(d), as amended 2017) for NIH-funded or NIH-conducted sensitive research — protects researchers from being compelled to disclose identifiable data in legal proceedings.

5. **Coordinate IRB and DUA.** A common failure mode: the IRB approves a study without specifying the DUA, or the DUA is signed without IRB review. Both must reference each other; the DUA typically prohibits release until IRB approval is in hand, and the IRB approval typically references the DUA number.

6. **For multi-site studies, set up sIRB and a master DUA.** The 2018 Common Rule (45 CFR 46.114) requires U.S. federally funded multi-site studies to use a single IRB. The sIRB has authority over the privacy plan; the DUA may still be site-specific or, in some cases, master-negotiated.

7. **For datathons**, plan for an enclave, synthetic data, or output review. The most common pattern: the data provider hosts the data in a secure enclave; participants query the data inside the enclave; only aggregate or model outputs leave the enclave after a review (often automated for disclosure risk). Open data enclaves include the NIH NCBI SAFE, the NCI Cancer Research Data Commons, the All of Us Researcher Workbench, and Synapse. Open synthetic-data tools include SDV and the synthcity package.

8. **For federated analysis**, decide between model-centric and data-centric patterns. Model-centric: train a model at each site, share model updates, aggregate centrally. Data-centric: keep data local, send the analytic code. Both still need a DUA; both benefit from differential-privacy noise added to model updates.

9. **For EU data, document the lawful basis and the safeguards.** GDPR Article 6 (general lawful basis) and Article 9 (special categories) both apply in research; Article 89 permits derogations from data-subject rights when "appropriate safeguards" are in place. Common research lawful bases: explicit consent (Art 6(1)(a) + Art 9(2)(a)), public interest (Art 6(1)(e)), scientific research (Art 9(2)(j) via Art 89). Document the basis, the safeguards (pseudonymization, access controls, breach plan), and the data-subject-rights procedure (right of access, rectification, erasure — with the research-specific derogations).

10. **Plan the breach response.** A breach that affects 500 or more individuals in the U.S. (HIPAA Breach Notification Rule, 45 CFR 164.404, 164.406, 164.408) triggers specific notification duties to individuals, HHS, and (sometimes) media. In the EU, GDPR Article 33 requires notification to the supervisory authority within 72 hours of awareness. The protocol's data-management section should name the responsible party, the timeline, and the template.

11. **Train the team.** A privacy plan that lives only in the protocol is not enforced. Brief every team member on the de-identification method, the access controls, the DUA terms, the breach-reporting line, and the consequence of unauthorized disclosure.

## Code patterns

This skill is documentation-heavy; the patterns below are the canonical text structures for each privacy plan section, plus a small Python pattern for Safe Harbor de-identification.

### Pattern 1 — Privacy plan table

```
Field class                       | Example            | Treatment
----------------------------------|--------------------|-----------------------------------------
Direct identifiers                | Name, MRN, SSN     | Removed (Safe Harbor #1, #8)
Indirect identifiers (geo)        | ZIP, city          | ZIP truncated to first 3 digits if pop >= 20,000 (Safe Harbor #2)
Indirect identifiers (date)       | DOB, admission     | Year only; ages > 89 aggregated to "90+" (Safe Harbor #3)
Contact identifiers               | Phone, email       | Removed (Safe Harbor #4, #6)
Biometric identifiers             | Fingerprint        | Removed (Safe Harbor #16)
Free-text notes                   | Pathology reports  | Redacted of all identifiers by NLP pipeline; residual review by expert
```

### Pattern 2 — DUA / DAA review checklist

Before signing any DUA, confirm: (1) the data provider is authorized to release the data; (2) the receiving institution's IRB will approve the use; (3) the data-use period is defined; (4) the use is limited to the named protocol; (5) the data will not be re-disclosed except as aggregated; (6) the data will be destroyed or returned at the end of the period; (7) breach notification is mutual; (8) the recipient's cloud or server environment meets the provider's security requirements.

### Pattern 3 — IRB and DUA coordination clause

A standard cross-reference reads: "Release of the limited data set under this DUA is contingent on IRB approval of protocol [number]. Any change to the protocol's data fields or analysis plan requires an amendment to both the IRB protocol and this DUA."

### Pattern 4 — Safe Harbor implementation in Python

```python
import hashlib
import re

SAFE_HARBOR_AGE_CAP = 90  # ages over 89 must be aggregated to "90+"

def safe_harbor_record(rec, phi_to_drop=("name", "ssn", "mrn", "email",
                                          "phone", "fax", "address",
                                          "license_plate", "device_id",
                                          "url", "ip", "biometric_id",
                                          "photo", "account", "cert_id",
                                          "vehicle_id", "health_plan_id")):
    """Remove Safe Harbor direct identifiers (164.514(b)(2)(i)(A)-(R)).

    The caller is responsible for date and ZIP truncation per the rule.
    """
    out = {k: v for k, v in rec.items() if k not in phi_to_drop}
    # age cap
    if "age" in out and out["age"] is not None and out["age"] > SAFE_HARBOR_AGE_CAP:
        out["age"] = "90+"
    return out

def truncate_zip(zip_code, pop_in_first_3):
    """164.514(b)(2)(i)(B): ZIP truncated to first 3 digits if pop >= 20,000;
       000 is permitted. Otherwise ZIP must be removed entirely."""
    if pop_in_first_3 >= 20_000:
        return zip_code[:3] + "00"
    return "000"

def truncate_date(date_value):
    """164.514(b)(2)(i)(C): dates reduced to year for events related to an individual."""
    return date_value[:4] if date_value else None
```

This is a starting point. Expert Determination (164.514(b)(1)) cannot be reduced to a 30-line script — it requires documented methodology and a qualified expert.

### Pattern 5 — Datathon enclave workflow

```
1. Apply to data provider -> data access committee (DAC) reviews protocol.
2. On approval, receive enclave credentials (NIH SAFE, Synapse, CRDC, All of Us).
3. Work inside the enclave: query data, train models, write code.
4. Export only approved artifacts: aggregate statistics, model coefficients,
   code, figures. Output review (often automated + human-in-the-loop) checks
   for disclosure risk (e.g., does the figure leak an outlier that re-identifies?).
5. Sign DUA at submission; abide by the destruction date.
```

### Pattern 6 — Federated analysis conceptual frame

```
Central server                    Sites (3 to N)
--------------                    --------------
broadcast model                   train on local data
aggregate updates  <-----         send updates (or model)
update model ------>             receive new model
                                 (loops until convergence)
```

For privacy, the model updates should be clipped, noised (differential privacy), or aggregated with secure multi-party computation. The DUA typically authorizes the model exchange but not the raw data exchange.

### Pattern 7 — Differential-privacy intuition (research-grade, not production)

The Laplace mechanism adds noise scaled to the *sensitivity* of the query divided by epsilon, the privacy budget. Smaller epsilon = stronger privacy = more noise. Reusing the same dataset across many queries compounds the privacy loss (composition). For research reporting, state the epsilon used and the noise distribution; for cross-site analyses, budget across sites and queries.

### Pattern 8 — Certificate of Confidentiality language

CoC applies automatically to NIH-funded or NIH-conducted research that collects identifiable sensitive information (the 2017 revision made it automatic; researchers do not need to apply for the certificate itself but must understand the protections and the disclosure rules). The CoC protects researchers from compelled disclosure (subpoena, court order) of identifiable data, with statutory exceptions (e.g., mandatory reporting of child abuse, voluntary participant consent to release).

### Pattern 9 — GDPR Article 89 safeguards checklist

For research relying on Article 89 derogations from data-subject rights, document: pseudonymization as the default; technical and organizational access controls; no decision-making based on the data that affects the data subject; data minimization; purpose limitation; and a data-protection-impact assessment (DPIA) for high-risk processing.

## Common pitfalls

- **"De-identified" used loosely.** "De-identified" is a defined term in HIPAA and a contested term in GDPR. A dataset with a study ID, a birth year, a 3-digit ZIP, and a diagnosis code may be HIPAA-Safe-Harbor-compliant but is not GDPR-anonymous; it is pseudonymized.
- **Free-text notes treated as de-identified.** Pathology reports, clinical notes, and radiology reports are the most common source of residual identifiers. NLP redaction tools (e.g., Philter, scrubadub) help, but expert review is still required for Expert Determination.
- **Dates not truncated.** Safe Harbor requires year only for dates related to an individual. The protocol frequently misses this for "date of consent," "date of enrollment," and "date of last follow-up."
- **ZIP retained at full resolution.** Safe Harbor permits ZIP only if the population of the geographic unit is at least 20,000. ZIP codes in low-population areas must be truncated to "000" or removed.
- **Ages over 89 reported individually.** Safe Harbor requires ages 90 and over to be aggregated to "90+."
- **DUA signed without IRB.** The IRB must approve the use before data is released. A DUA that lacks an IRB cross-reference is incomplete.
- **DUA absent re-disclosure clause.** A weak DUA allows the recipient to share the data with collaborators or downstream users. Re-disclosure must be prohibited or constrained.
- **Certificate of Confidentiality not invoked.** CoC is automatic for NIH-funded sensitive research as of 2017, but the IRB consent form must include the CoC disclosure language. The protection is only as strong as the consent-form language.
- **EU study with no lawful basis.** "It's research" is not a lawful basis. GDPR requires Article 6 + (if special categories) Article 9. Document the basis in the protocol.
- **EU-US transfer without an adequacy decision or SCCs.** Post-Schrems II, transfers to the U.S. require either an adequacy decision (currently limited), Standard Contractual Clauses (SCCs) plus a transfer impact assessment, or Binding Corporate Rules. A DUA that ships EU data to a U.S. server without these is non-compliant.
- **Federated learning treated as automatically private.** Sending model updates leaks information (gradient attacks can reconstruct training data). Federated learning without differential privacy, secure aggregation, or trusted execution environments is *not* a privacy mechanism — it is a deployment pattern.
- **Differential privacy applied without composition accounting.** Reusing a dataset across many queries compounds the privacy loss. A paper that reports epsilon=0.1 per query across 100 queries has actually spent epsilon=10 in the worst case; this must be reported.
- **Synthetic data assumed safe.** Synthetic data can leak training records, especially for outliers. A defensible synthetic-data plan includes a disclosure-risk evaluation, not just utility metrics.
- **Breach plan that names a "responsible person" who is on leave.** The protocol should name a function, not a person; a privacy officer or designee is more robust than a single individual.
- **No data destruction date.** Most DUAs require destruction or return at a defined date. A protocol that does not specify a destruction date risks indefinite retention.

## Validation

- A field-level data inventory lists every direct and indirect identifier and the treatment of each.
- The de-identification method is named (Safe Harbor or Expert Determination) and justified for the dataset.
- The DUA references the IRB protocol, and the IRB protocol references the DUA.
- The IRB consent form includes the Certificate of Confidentiality language (if applicable).
- For EU data, the lawful basis under GDPR is documented, and (for U.S. recipients) the transfer mechanism is named.
- For datathons, the enclave and the output-review process are named.
- For federated or privacy-preserving analyses, the privacy guarantee is named (differential privacy with epsilon, secure aggregation, trusted execution environment) and the composition is reported.
- The breach-notification plan names the timeline, the responsible function, the authorities to be notified, and the template.
- The team has been briefed; training is documented.

## Open alternatives

- **HIPAA de-identification tooling**: Philter (open-source NLP redaction), scrubadub (open-source PII detection), ARX (open-source de-identification and risk analysis), sdcMicro (R package for statistical disclosure control).
- **Differential privacy libraries**: Google's differential-privacy library, IBM diffprivlib, TensorFlow Privacy, Opacus (PyTorch).
- **Federated learning frameworks**: Flower (open-source, framework-agnostic), OpenFL (Intel, focused on healthcare), FedML, PySyft.
- **Synthetic data tools**: SDV (Synthetic Data Vault), synthcity, Gretel (commercial with open tier).
- **Data enclaves**: NIH SAFE, NCI Cancer Research Data Commons, All of Us Researcher Workbench, Synapse, Vivli.
- **Reliance agreements**: SMART IRB (open, NIH-supported).
- **Consent templates**: OPENeX consent template; PRISMA-compliant consent templates.

## References

- 45 CFR 164.514 — HIPAA de-identification (Safe Harbor and Expert Determination).
- 45 CFR 46.102(e) — Common Rule definitions of "human subject" and "identifiable."
- Regulation (EU) 2016/679 (GDPR) — Articles 4, 5, 6, 9, 13, 14, 28, 32, 44-49, 89.
- 42 USC 241(d) — Certificate of Confidentiality authority (Public Health Service Act, amended 2017).
- NIH Genomic Data Sharing Policy (2014, updated 2023) and dbGaP Data Use Agreement template.
- HIPAA Breach Notification Rule — 45 CFR 164.400-414.
- 2018 Common Rule — 45 CFR 46.114 (single-IRB requirement).
- Related skills: `ors-ethics-compliance-irb-protocol` (IRB process and review levels), `ors-clinical-decision-regulatory` (FDA-regulated research), `ors-omics-statistics-differential-expression` (analysis after access is granted).

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesized from 45 CFR 164.514 (HIPAA de-identification), GDPR (Regulation EU 2016/679), the NIH Genomic Data Sharing Policy, and 42 USC 241(d) (Certificate of Confidentiality). Datathon and federated-learning sections are original synthesis.