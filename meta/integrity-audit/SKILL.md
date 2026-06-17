---
name: integrity-audit
description: "7-mode AI failure-mode checklist applied before publishing any ORS artifact (skill, manuscript section, dataset card, agent output). Catches: fabricated citations, silent failures, scope creep, missing provenance, unsupervised writes, version drift, hallucinated APIs. Use as the final pass before any 'publish', 'release', 'merge', or 'finalize' action."
license: MIT
---
<!-- metadata:
  oversight: low
  version: 1.0.0
  author: ORS maintainers
  tags: [meta, integrity, validation, failure-modes, pre-publish]
  difficulty: intermediate
-->

# Integrity Audit

A 7-mode checklist that catches the failure patterns AI agents most commonly
produce in research artifacts. Run this *immediately before* any publish,
release, merge, or "I'm done" assertion.

## When to use

- About to commit a SKILL.md to the ORS repository.
- About to publish a manuscript section, dataset, or figure caption
  generated with AI assistance.
- Reviewing someone else's AI-assisted work before sign-off.
- Anytime an agent says "done" or "ready to publish" — pause and run this.

## When NOT to use

- Mid-task. This is a *final* pass, not a continuous monitor.
- For quick smoke checks of well-understood files (use the language-specific
  linter instead).
- For security audits (use a dedicated security tool).

## Hard rules

1. **No fabricated citations.** Every cited work must resolve to a verifiable
   record (DOI, PMID, arXiv ID, ISBN, URL with retrieval date, or stable
   identifier). If a source cannot be resolved, the skill must say so
   explicitly rather than presenting the claim as established.
2. **No claim without provenance.** Every quantitative or factual claim
   must point to a file, line, table, figure, dataset, or external source
   the agent can show. "Trust me" is not provenance.
3. **No silent failure.** Every script invocation, API call, or tool use
   must declare its exit status and what to do on non-zero. A skill that
   silently swallows errors is a violation.

## The 7 modes

Run all 7 modes. Each produces either PASS, FLAG (needs human review), or
FAIL (must fix before publish).

### Mode 1 — Fabricated citations

**What it catches:** Citations to papers, DOIs, datasets, or authors that
do not exist. The single most common AI failure mode in research artifacts.

**How to audit:**
- For every cited work, resolve the DOI/PMID/arXiv ID via a real lookup
  (doi.org, PubMed, arXiv). Do not trust the agent's claim of existence.
- For every URL, fetch it. 404 is FAIL.
- For "et al." citations without full author list, verify the lead author.
- For inline numeric claims (sample sizes, p-values, fold-changes), verify
  the cited source actually contains that number.

**Verdict:**
- PASS — every cited work resolves and the cited claim matches the source.
- FLAG — citation resolves but the cited claim is missing or distorted.
- FAIL — citation does not resolve, or no citation was given for a
  non-trivial claim.

### Mode 2 — Silent failures

**What it catches:** Code that runs but does not do what it claims. Errors
that are swallowed. Exit codes that are ignored.

**How to audit:**
- Every `subprocess.run(...)` / `os.system(...)` / `! ...` cell must check
  the return code or capture and surface stderr.
- Every API call must check the HTTP status code.
- Every file write must check that the file exists after writing and is
  non-empty (unless empty is the intended outcome).
- Every exception handler must either re-raise, log loudly, or have a
  justified reason for swallowing.

**Verdict:**
- PASS — every external call has explicit error handling.
- FLAG — some calls have handling but it's inconsistent.
- FAIL — code assumes success without checking, or catches exceptions
  silently.

### Mode 3 — Scope creep

**What it catches:** Output that goes beyond the requested scope. Sections
that the user did not ask for. Files created that no one asked for.

**How to audit:**
- For every section of the output, ask: "Did the user ask for this?"
- For every file created/modified, ask: "Did the user ask me to touch
  this file?"
- For every recommendation, ask: "Is this within the skill's declared
  domain?"

**Verdict:**
- PASS — output matches the request, no extras.
- FLAG — minor extras (helpful tangents, useful notes).
- FAIL — output includes substantive material the user did not request.

### Mode 4 — Missing provenance

**What it catches:** Claims without sources. Numbers without backing.
Conclusions without reasoning shown.

**How to audit:**
- Every quantitative claim has either (a) a file/line reference or (b) a
  citation.
- Every qualitative claim has either a citation or a clearly-labeled
  inference.
- Every "based on X" must point to the specific X being used.

**Verdict:**
- PASS — every claim is traceable.
- FLAG — most claims are traceable, a few are inferential but plausible.
- FAIL — key claims have no source.

### Mode 5 — Unsupervised writes

**What it catches:** Destructive operations performed without confirmation.
Files overwritten. Databases mutated. Emails sent. PRs opened.

**How to audit:**
- For every file write, check: did the user ask me to write this specific
  content? Did I ask for confirmation on the overwrite?
- For every git push / git commit --amend / git reset --hard / rm -rf:
  was this explicitly authorized?
- For every API call with side effects: was the side effect confirmed?

**Verdict:**
- PASS — all writes were authorized, content matches the request.
- FLAG — writes were made but were in scope and reversible.
- FAIL — destructive operations were performed without authorization.

### Mode 6 — Version drift

**What it catches:** Stale version numbers. Skills with version 1.0.0
that have been edited 50 times. Frontmatter `description` that no longer
matches the body. Metadata block out of sync with reality.

**How to audit:**
- The metadata `version` field matches the latest entry in `## Changelog`.
- The frontmatter `description` reflects the current behavior, not the
  v1.0 behavior.
- All cross-reference slugs in `## Cross-references` resolve to existing
  files.
- The skill still passes `scripts/validate-skills.py`.

**Verdict:**
- PASS — version metadata matches reality.
- FLAG — minor drift, easily fixed.
- FAIL — version, description, or xrefs are stale.

### Mode 7 — Hallucinated APIs

**What it catches:** Method names, function arguments, CLI flags, or
library modules that do not exist.

**How to audit:**
- Every API call in code (function name, argument name, return value) must
  exist in the documented library at the cited version.
- Every CLI flag must exist in the tool at the cited version.
- Every config-file key must be valid for the cited schema.

**Verdict:**
- PASS — every API reference is real.
- FLAG — minor name misspellings or version-unstable features.
- FAIL — methods/flags that don't exist at all.

## Output format

After running all 7 modes, produce a summary table:

| Mode | Verdict | Notes |
|------|---------|-------|
| 1. Fabricated citations | PASS / FLAG / FAIL | ... |
| 2. Silent failures | ... | ... |
| ... | ... | ... |

The artifact is **publishable** only if every row is PASS or FLAG. Any
FAIL blocks publish until fixed.

## Cross-references

- meta/roadmap-author — use this audit as the final step of authoring.
- meta/release-management — version bumps should trigger a re-audit.
- meta/cross-reference-mapper — find related audit skills.

## Changelog

- **1.0.0** (2026-06-17) — Initial release. 7 modes distilled from common
  failure patterns observed in AI-assisted research outputs.
