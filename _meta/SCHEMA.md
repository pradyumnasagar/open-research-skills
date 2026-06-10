# Frontmatter Schema (canonical)

Every `SKILL.md` MUST begin with the following YAML frontmatter. Fields marked *required* must be present. Fields marked *recommended* should be present unless genuinely not applicable. Fields marked *optional* may be omitted.

```yaml
---
# Required
name: ors-<category-kebab>-<skill-slug>          # lowercase, kebab, matches folder name
display_name: "Human-Readable Title"             # Title-cased
description: "One sentence (max 200 chars) — what & when."
version: 1.0.0                                  # semver
author: Pradyumna Jayaram
license: MIT
category: <one of the categories in TAXONOMY.md>

# Recommended
tags: [list, of, 3-6, lowercase, tags]
difficulty: beginner | intermediate | advanced
last_updated: YYYY-MM-DD
sources_consulted:
  - "Original: <name> (<source-repo>); Adapted: <list of major changes>"
  - "Improvisions: <list of Pradyumna's additions/modernizations>"

# Optional
prerequisites:
  tools: [list, of, CLI, tools, or, libraries]
  skills: [list, of, ors-* names, this depends on]
```

## Body structure (recommended)

```markdown
# <Display Name>

> One-paragraph framing.

## When to use
## When NOT to use
## Prerequisites
## Core workflow
## Code patterns
## Common pitfalls
## Validation
## Open alternatives
## References
## Changelog
```

All sections are optional except the title and framing paragraph. Use what fits the skill.
