#!/usr/bin/env python3
"""Validate all SKILL.md files against the ORS specification (v0.4.0).

v0.4.0 additions (over v0.3.0):
  * Requires the `oversight` field in the <!-- metadata: ... --> block.
  * Requires `## Hard rules` section with the three base rule titles.
  * Requires `## Cross-references` section with slug-resolved links.
  * Adds `--backfill` mode to add `oversight: medium` to existing skills.
  * Adds `--meta` flag for cross-cutting `meta/` folder.
"""

import argparse
import pathlib
import re
import sys
import yaml

# SPDX license list (partial)
SPDX_LICENSES = {
    "MIT", "GPL-2.0", "GPL-3.0", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause",
    "AGPL-3.0", "LGPL-2.1", "LGPL-3.0", "MPL-2.0", "CC-BY-4.0", "CC-BY-SA-4.0"
}

VALID_OVERSIGHT = {"very-high", "high", "medium", "low"}

# Three base hard rules — every skill must include these.
BASE_HARD_RULES = [
    "no fabricated citations",
    "no claim without provenance",
    "no silent failure",
]

# Required body sub-section headings (case-insensitive substring match).
REQUIRED_SECTIONS = [
    "when to use",
    "hard rules",
    "cross-references",
    "changelog",
]


def validate_name(name: str, path: pathlib.Path, seen_names: dict) -> list[str]:
    errors = []
    if name in seen_names:
        errors.append(f"name is not unique (already used at {seen_names[name]})")
    seen_names[name] = path
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', name) and name != 'a':
        if name.startswith('-') or name.endswith('-'):
            errors.append("name must not start or end with hyphens")
        if re.search(r'[^a-z0-9-]', name):
            errors.append("name must be lowercase ASCII letters, digits, and hyphens only")
        if len(name) > 64 or len(name) < 1:
            errors.append("name must be 1-64 characters")
    expected = path.parent.name
    if name != expected:
        errors.append(f"name '{name}' does not match folder name '{expected}'")
    return errors


def validate_description(desc: str) -> list[str]:
    errors = []
    if not desc:
        errors.append("description is required")
    if len(desc) > 1024:
        errors.append("description must be ≤1024 characters")
    return errors


def validate_license(license: str) -> list[str]:
    if license not in SPDX_LICENSES:
        return [f"license '{license}' is not a valid SPDX identifier"]
    return []


def extract_metadata(content: str) -> tuple[dict | None, str | None]:
    """Return (parsed metadata dict, raw yaml text) or (None, None)."""
    m = re.search(r'<!-- metadata:\s*\n(.*?)-->', content, re.DOTALL)
    if not m:
        return None, None
    try:
        return yaml.safe_load(m.group(1)) or {}, m.group(1)
    except yaml.YAMLError:
        return None, m.group(1)


def validate_metadata_block(metadata: dict | None, raw: str | None,
                            path: pathlib.Path,
                            known_categories: set[str],
                            known_meta_slugs: set[str]) -> list[str]:
    errors = []
    if metadata is None:
        errors.append("missing <!-- metadata: ... --> block (required in v0.4.0)")
        return errors
    # category
    category = metadata.get('category')
    if category and category not in known_categories:
        # Allow meta/ folder to have no category, but if set it must be valid.
        errors.append(f"category '{category}' is not in spec/category-taxonomy.md")
    # oversight (required since v0.4.0)
    oversight = metadata.get('oversight')
    if oversight is None:
        errors.append("oversight is required in <!-- metadata: ... --> (v0.4.0); use very-high | high | medium | low")
    elif oversight not in VALID_OVERSIGHT:
        errors.append(
            f"oversight '{oversight}' must be one of very-high | high | medium | low"
        )
    # difficulty
    difficulty = metadata.get('difficulty')
    if difficulty and difficulty not in {'beginner', 'intermediate', 'advanced'}:
        errors.append(f"difficulty must be beginner | intermediate | advanced (got '{difficulty}')")
    # tags
    tags = metadata.get('tags', [])
    if tags is None:
        tags = []
    if not isinstance(tags, list) or len(tags) < 1 or len(tags) > 6:
        errors.append("tags must be a list of 1-6 strings")
    else:
        for tag in tags:
            if not re.match(r'^[a-z0-9-]+$', tag):
                errors.append(f"tag '{tag}' must be lowercase kebab-case")
            if tag.startswith('ors-'):
                errors.append("tags should not include 'ors-' prefix (it's implied)")
    return errors


def parse_frontmatter(content: str) -> tuple[dict | None, str, str | None]:
    """Return (frontmatter dict, body, raw metadata yaml). Metadata is None if absent."""
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, "", None
    try:
        frontmatter = yaml.safe_load(parts[1].strip()) or {}
    except yaml.YAMLError:
        return None, parts[2].strip() if len(parts) > 2 else "", None
    body = parts[2].strip() if len(parts) > 2 else ""
    metadata, _ = extract_metadata(content)
    return frontmatter, body, metadata


def extract_section(body: str, heading: str) -> str | None:
    """Return the body text under `## <heading>` up to the next `## `, or None."""
    pattern = re.compile(
        rf'^##\s+{re.escape(heading)}\s*?\n(.*?)(?=^##\s|\Z)',
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(body)
    return m.group(1).strip() if m else None


def validate_required_sections(body: str) -> list[str]:
    errors = []
    body_lower = body.lower()
    for heading in REQUIRED_SECTIONS:
        if not extract_section(body, heading):
            errors.append(f"missing required body section '## {heading.title().replace('And', 'and')}' (v0.4.0)")
    return errors


def validate_hard_rules(body: str) -> list[str]:
    errors = []
    section = extract_section(body, "hard rules")
    if section is None:
        return errors  # already reported by required-sections check
    section_lower = section.lower()
    for rule in BASE_HARD_RULES:
        if rule not in section_lower:
            errors.append(f"## Hard rules section missing base rule '{rule}'")

    # Heuristic: a hard rule is "truncated" if it is a single line consisting
    # of just the bolded title (no body). E.g. "1. **No fabricated citations.**"
    # with no continuation on subsequent lines.
    lines = section.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\s*\d+\.\s+\*\*([^*]+?)\*\*\s*$", line)
        if not m:
            continue
        title = m.group(1).strip()
        # Is this one of the base rules? (Otherwise, domain-specific rules
        # legitimately can be short.)
        if not any(rule.split('.')[0] in title.lower() for rule in BASE_HARD_RULES):
            continue
        # The line is the title only (no body on the same line). Look at the
        # next non-blank line: if it is another numbered item, the body is
        # missing and the rule is truncated.
        next_non_blank = ""
        for j in range(i + 1, len(lines)):
            if lines[j].strip():
                next_non_blank = lines[j].strip()
                break
        if re.match(r"^\d+\.\s+\*\*", next_non_blank):
            errors.append(
                f"## Hard rules base rule '{title}' has no body (truncated)"
            )
            break
    return errors


def extract_cross_references(body: str) -> list[str]:
    """Parse `## Cross-references` section for bullet slugs."""
    section = extract_section(body, "cross-references")
    if section is None:
        return []
    slugs = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        # Strip leading bullet, optional checkbox, then take first token (the slug).
        rest = line[2:].strip()
        if rest.startswith("["):
            # Markdown task list: "- [ ] slug — desc"
            rest = rest.split("]", 1)[-1].strip()
        if "—" in rest:
            slug = rest.split("—", 1)[0].strip()
        elif "—" not in rest and " - " in rest:
            slug = rest.split(" - ", 1)[0].strip()
        elif " -" in rest:
            slug = rest.split(" -", 1)[0].strip()
        else:
            slug = rest.split()[0] if rest.split() else ""
        # Strip backticks and trailing punctuation.
        slug = slug.strip("`").rstrip(",;:")
        slugs.append(slug)
    return [s for s in slugs if s]


def validate_cross_references(slugs: list[str],
                              known_skill_slugs: set[str],
                              known_meta_slugs: set[str]) -> list[str]:
    errors = []
    for slug in slugs:
        # Accept both bare slugs and `meta/<slug>` for meta skills.
        bare = slug
        if slug.startswith("meta/"):
            bare = slug[len("meta/"):]
        if (slug in known_skill_slugs or slug in known_meta_slugs
                or bare in known_skill_slugs or bare in known_meta_slugs):
            continue
        errors.append(
            f"cross-reference slug '{slug}' does not resolve to any skill under skills/ or meta/"
        )
    return errors


def validate_skill(path: pathlib.Path,
                   seen_names: dict,
                   known_categories: set[str],
                   known_skill_slugs: set[str],
                   known_meta_slugs: set[str],
                   skip_cross_refs: bool = False) -> list[str]:
    errors = []
    content = path.read_text()
    frontmatter, body, metadata = parse_frontmatter(content)

    if frontmatter is None:
        return ["frontmatter YAML is invalid or missing"]

    name = frontmatter.get('name')
    description = frontmatter.get('description')

    if not name:
        errors.append("name is required")
    else:
        errors.extend(validate_name(name, path, seen_names))

    if not description:
        errors.append("description is required")
    else:
        errors.extend(validate_description(description))

    license = frontmatter.get('license')
    if license:
        errors.extend(validate_license(license))

    errors.extend(validate_metadata_block(metadata, None, path,
                                          known_categories, known_meta_slugs))
    errors.extend(validate_required_sections(body))
    errors.extend(validate_hard_rules(body))

    if not skip_cross_refs:
        slugs = extract_cross_references(body)
        errors.extend(validate_cross_references(slugs, known_skill_slugs, known_meta_slugs))

    if not body:
        errors.append("skill body is empty")

    return errors


def load_categories(spec_file: pathlib.Path) -> set[str]:
    """Read spec/category-taxonomy.md and extract the 18 category names."""
    text = spec_file.read_text()
    cats = set()
    # Match the table rows like `| \`bioinformatics-sequence\` | 23 | ...`
    for m in re.finditer(r'`([a-z][a-z0-9-]+)`\s*\|\s*\d+', text):
        cats.add(m.group(1))
    return cats


def collect_known_slugs(root: pathlib.Path, skills_dir: pathlib.Path,
                        meta_dir: pathlib.Path | None) -> tuple[set[str], set[str]]:
    """First pass: discover all skill names so cross-references can resolve."""
    skill_slugs = set()
    for p in skills_dir.rglob('SKILL.md'):
        skill_slugs.add(p.parent.name)
    meta_slugs = set()
    if meta_dir and meta_dir.exists():
        for p in meta_dir.rglob('SKILL.md'):
            meta_slugs.add(p.parent.name)
    return skill_slugs, meta_slugs


def backfill_oversight(path: pathlib.Path) -> bool:
    """Insert `oversight: medium` into the metadata block if absent. Returns True if changed."""
    content = path.read_text()
    metadata, raw = extract_metadata(content)
    if metadata is None:
        return False
    if 'oversight' in metadata:
        return False
    # Insert oversight line into the metadata YAML, right after the opening line.
    lines = raw.splitlines()
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and line.strip() and not line.strip().startswith("#"):
            new_lines.append("  oversight: medium")
            inserted = True
    new_block = "\n".join(new_lines)
    new_content = content.replace(
        f"<!-- metadata:\n{raw}-->",
        f"<!-- metadata:\n{new_block}-->",
        1,
    )
    if new_content == content:
        return False
    path.write_text(new_content)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('skills_dir', type=pathlib.Path, help='Directory with skills/')
    parser.add_argument('--meta', type=pathlib.Path, default=None,
                        help='Path to the meta/ directory (optional).')
    parser.add_argument('--spec', type=pathlib.Path,
                        default=pathlib.Path('spec/category-taxonomy.md'),
                        help='Path to category taxonomy.')
    parser.add_argument('--backfill', action='store_true',
                        help='Insert oversight: medium into skills that lack it, then exit.')
    parser.add_argument('--skip-cross-refs', action='store_true',
                        help='Skip cross-reference resolution (useful during partial migrations).')
    args = parser.parse_args()

    if not args.skills_dir.exists() or not args.skills_dir.is_dir():
        print(f"Error: {args.skills_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    skill_files = list(args.skills_dir.rglob('SKILL.md'))
    if args.meta and args.meta.exists():
        skill_files += list(args.meta.rglob('SKILL.md'))
    print(f"Found {len(skill_files)} SKILL.md files to process...")

    categories = load_categories(args.spec) if args.spec.exists() else set()
    skill_slugs, meta_slugs = collect_known_slugs(
        args.skills_dir.parent, args.skills_dir, args.meta
    )

    if args.backfill:
        changed = 0
        for sf in skill_files:
            if backfill_oversight(sf):
                changed += 1
        print(f"✅ Backfilled `oversight: medium` into {changed} skills")
        sys.exit(0)

    all_errors = []
    seen_names = {}

    for skill_file in skill_files:
        errors = validate_skill(skill_file, seen_names, categories,
                                skill_slugs, meta_slugs,
                                skip_cross_refs=args.skip_cross_refs)
        if errors:
            prefix = f"❌ {skill_file}"
            print(f"{prefix}:")
            for error in errors:
                print(f"  - {error}")
            all_errors.extend([f"{skill_file}: {error}" for error in errors])

    if all_errors:
        print(f"\n❌ Found {len(all_errors)} errors across {len(set(e.split(':', 1)[0] for e in all_errors))} files")
        sys.exit(1)
    else:
        print(f"✅ All {len(skill_files)} skills are valid")
        sys.exit(0)


if __name__ == '__main__':
    main()
