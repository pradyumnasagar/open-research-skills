# Repo automation scripts

These are utilities for maintaining the open-research-skills repo. Run them from the repo root.

| Script | Purpose |
|---|---|
| `validate-skills.py` | Check every SKILL.md in `skills/` against the frontmatter and naming rules in `spec/skill-format.md`. |
| `build-index.py` | Regenerate `INDEX.md` from the actual `SKILL.md` files in `skills/`. |

## `validate-skills.py`

```bash
python scripts/validate-skills.py skills/
```

Checks:

- `name` field matches the parent folder name
- `name` is unique repo-wide
- `name` is lowercase kebab-case ASCII, 1–64 chars
- `description` is present and 1–1024 chars
- `license` (if present) is a valid SPDX identifier
- The optional `<!-- metadata: ... -->` block, if present, has well-formed YAML

Exits 0 on success, 1 on any error. Used in CI.

## `build-index.py`

```bash
python scripts/build-index.py
```

Reads every `SKILL.md` in `skills/`, extracts the frontmatter and metadata block, and writes `INDEX.md` as a Markdown table. Use this whenever you add, remove, or rename a skill.

The script is idempotent — running it twice produces the same output.

## Why Python?

No dependencies. Both scripts use only the standard library (`pathlib`, `re`, `sys`, `json`, `argparse`). Python 3.10+ is required for `str | None` syntax in `validate-skills.py`. If you're on an older Python, see the `pyproject.toml` for the minimum version.
