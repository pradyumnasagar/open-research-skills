#!/usr/bin/env python3
"""Bulk-migrate existing ORS skills from v0.3.0 to v0.4.0.

For each skills/*/SKILL.md:
  1. Repair the <!-- metadata: ... --> block to canonical YAML
     (category derived from path, oversight derived from category table,
      version / author / tags / difficulty preserved from frontmatter).
  2. Insert ## Hard rules section with the 3 base rules (if absent).
  3. Insert ## Cross-references section listing sibling skills in the
     same category (if absent).

Idempotent: re-running on an already-migrated file is a no-op.

Run from repo root:
    python scripts/bulk-migrate-v0.4.0.py skills/         # migrate
    python scripts/bulk-migrate-v0.4.0.py skills/ --check # dry-run
"""

import argparse
import pathlib
import re
import sys

# Oversight defaults per category. Conservative (medium) for most, low for
# purely mechanical/algorithmic skills, very-high for generative ones.
OVERSIGHT_BY_CATEGORY = {
    # Generative / synthesis (require fact verification)
    "scientific-writing":        "very-high",
    "scientific-communication":  "very-high",
    "scientific-thinking":       "very-high",
    "literature-research":       "high",
    "peer-review":               "high",
    "research-grants":           "high",
    "career-navigation":         "high",
    "mentorship-teaching":       "medium",
    "open-science":              "medium",
    "ethics-compliance":         "medium",
    "humanizer-skills":          "very-high",
    "scientific-visualization":  "medium",
    "image-analysis-microscopy": "low",
    "chemoinformatics":          "low",
    "machine-learning-bio":      "low",
    "bioinformatics-sequence":   "low",
    "lab-automation":            "low",
    "data-engineering":          "low",
}

# The 3 base rules that every skill must declare (per spec/skill-format.md).
HARD_RULES = """## Hard rules

These are mandatory for every ORS skill — failure to follow them is a schema
violation, not a style preference.

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
"""

# When-to-use and Changelog stubs that the v0.4.0 spec requires but many
# existing skills lack. These are honest placeholders — the author should
# replace them with real content before publishing.
WHEN_TO_USE_STUB = """## When to use

Load this skill when the user asks a question that matches its declared
trigger conditions (see the frontmatter `description` for the most common
ones). Do not load it for questions outside its scope — defer to the
appropriate ORS skill instead.

## When NOT to use

Do not load this skill if the question is in a sibling skill's domain
(see `## Cross-references`), if the user explicitly asks for a different
tool, or if the task is outside the skill's declared category.
"""

CHANGELOG_STUB = """## Changelog

- **1.1.0** (migration) — Bulk-migrated to v0.4.0 schema: canonical
  metadata block, base Hard rules, Cross-references. Body content
  unchanged; author should review and fill in any domain-specific
  extensions to the Hard rules.
- **1.0.0** — Initial release.
"""


def derive_category(skill_path: pathlib.Path, skills_root: pathlib.Path) -> str:
    """Category is the top-level directory under skills/."""
    rel = skill_path.relative_to(skills_root)
    return rel.parts[0]


def build_metadata_block(frontmatter: dict, category: str) -> str:
    """Construct a canonical, well-formed <!-- metadata: ... --> block."""
    oversight = OVERSIGHT_BY_CATEGORY.get(category, "medium")
    lines = ["<!-- metadata:"]
    lines.append(f"  category: {category}")
    lines.append(f"  oversight: {oversight}")
    # Carry over from frontmatter if present
    for key in ("version", "author", "tags", "difficulty"):
        v = frontmatter.get(key)
        if v is None:
            continue
        if isinstance(v, list):
            # Render as inline yaml list
            items = ", ".join(str(x) for x in v)
            lines.append(f"  {key}: [{items}]")
        else:
            lines.append(f"  {key}: {v}")
    lines.append("-->")
    return "\n".join(lines)


def parse_metadata_block(content: str) -> dict:
    """Best-effort extraction of fields from the existing (possibly broken)
    <!-- metadata: ... --> block. Used to preserve version/author/tags/etc.

    Strategy: walk the lines and apply a simple state machine that recognizes
    `key: scalar` and `key:` followed by indented `- item` lines. We don't try
    to round-trip the broken YAML — we just extract the fields we care about.
    """
    m = re.search(r'<!--\s*metadata:\s*\n(.*?)-->', content, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    out: dict = {}
    current_list_key: str | None = None
    for line in block.splitlines():
        # Strip trailing --> if glued to last line
        line = line.rstrip()
        if line.endswith('-->'):
            line = line[:-3].rstrip()
        if not line or line.lstrip().startswith('#'):
            continue
        stripped = line.lstrip()
        # List item: starts with `- ` (possibly indented)
        if stripped.startswith('- '):
            item = stripped[2:].strip()
            if current_list_key and isinstance(out.get(current_list_key), list):
                out[current_list_key].append(item)
            continue
        # Key: value line — find the first colon
        m2 = re.match(r'([A-Za-z_][\w-]*)\s*:\s*(.*)', stripped)
        if not m2:
            continue
        key, val = m2.group(1), m2.group(2).strip()
        if val == '':
            # Could be a list, or a key with a null value
            current_list_key = key
            out[key] = []
        else:
            current_list_key = key
            out[key] = val
    return out


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Pull the Anthropic-spec frontmatter (top of file, between --- lines)."""
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not m:
        return {}, ""
    try:
        import yaml
        return yaml.safe_load(m.group(1)) or {}, m.group(0)
    except Exception:
        return {}, m.group(0)


def remove_old_metadata_block(content: str) -> str:
    """Remove a possibly-broken <!-- metadata: ... --> block from the body."""
    # Match the metadata block: starts with `<!-- metadata:` and ends with `-->`
    # on its own line, or with the last line of the block (e.g., `key: value-->`).
    return re.sub(
        r'\n*<!--\s*metadata:\s*\n.*?-->\s*\n*',
        '\n',
        content,
        count=1,
        flags=re.DOTALL,
    )


def find_h1_position(content: str) -> int:
    """Find the position right before the first `# Title` heading."""
    m = re.search(r'^# .+\n', content, re.MULTILINE)
    if not m:
        return len(content)
    return m.start()


def insert_after_h1(content: str, insert: str) -> str:
    """Insert `insert` immediately after the first H1 heading + blank line."""
    m = re.search(r'^(# .+\n)\n*', content, re.MULTILINE)
    if not m:
        # No H1 — append to end
        return content.rstrip() + "\n\n" + insert + "\n"
    pos = m.end()
    return content[:pos] + insert + "\n" + content[pos:]


def insert_after_section(content: str, section_name: str, insert: str) -> str:
    """Insert `insert` immediately after the end of the `## section_name`
    block. If the section is not found, append to the end."""
    # Find the section header
    hdr = re.search(rf'^##\s+{re.escape(section_name)}\s*?\n',
                    content, re.MULTILINE | re.IGNORECASE)
    if not hdr:
        return content.rstrip() + "\n\n" + insert + "\n"
    # Find the next ## header after this one
    after = content[hdr.end():]
    next_hdr = re.search(r'^##\s+', after, re.MULTILINE)
    if next_hdr:
        # Insert before next section
        abs_pos = hdr.end() + next_hdr.start()
    else:
        # Append to end
        return content.rstrip() + "\n\n" + insert + "\n"
    return content[:abs_pos] + insert + "\n" + content[abs_pos:]


def has_section(body: str, header: str) -> bool:
    """True if body has `## Header` (case-insensitive)."""
    return bool(re.search(rf'^##\s+{re.escape(header)}\s*$', body, re.MULTILINE | re.IGNORECASE))


def build_cross_references(category: str, skills_root: pathlib.Path,
                           current_slug: str) -> str:
    """Build the ## Cross-references section.

    Lists sibling skills in the same category if any, otherwise emits an
    honest "no related skills yet" stub. The v0.4.0 spec requires the
    section to be present, even when empty.
    """
    siblings = []
    cat_dir = skills_root / category
    if cat_dir.exists():
        for p in sorted(cat_dir.rglob('SKILL.md')):
            slug = p.parent.name
            if slug == current_slug:
                continue
            siblings.append(slug)

    lines = ["## Cross-references", ""]
    if siblings:
        lines.append("Other skills in this category:")
        lines.append("")
        for s in siblings:
            lines.append(f"- {s}")
    else:
        lines.append("_No related skills in this category yet. ")
        lines.append("Add sibling skills as they are created in this category. ")
        lines.append("Universal research-workflow skills live under `meta/`._")
    return "\n".join(lines)


def migrate_skill(skill_md: pathlib.Path, skills_root: pathlib.Path,
                  check_only: bool = False) -> tuple[bool, str]:
    """Migrate a single SKILL.md. Returns (changed, message)."""
    content = skill_md.read_text()
    frontmatter, _ = parse_frontmatter(content)
    # Preserve fields from the existing (possibly broken) metadata block
    existing_meta = parse_metadata_block(content)
    # Merge: frontmatter wins for overlapping scalar fields we don't manage
    merged = {**existing_meta, **frontmatter}
    category = derive_category(skill_md, skills_root)

    # --- Step 1: rebuild the metadata block ---
    new_meta = build_metadata_block(merged, category)

    # Remove old metadata block (broken or intact)
    body = remove_old_metadata_block(content)
    # Re-attach frontmatter + new metadata
    fm_match = re.match(r'^---\s*\n.*?\n---\s*\n', body, re.DOTALL)
    if fm_match:
        body = body[fm_match.end():]
    # Construct canonical content
    new_content = fm_match.group(0) if fm_match else ""
    if not new_content:
        # No frontmatter — synthesize a minimal one
        slug = skill_md.parent.name
        desc = frontmatter.get('description', f'ORS skill: {slug}.')
        new_content = f"---\nname: {slug}\ndescription: {desc}\nlicense: MIT\n---\n\n"
    new_content += new_meta + "\n\n"

    # Body (everything after the metadata block, if any) — start from the old body
    # (already has frontmatter + metadata stripped above)
    # Now strip leading blank lines
    body = body.lstrip('\n')

    # --- Step 2: Hard rules ---
    if has_section(body, "Hard rules") or has_section(body, "Hard Rules"):
        # Section exists. Verify it has all 3 base rules. If "no silent failure"
        # is missing, replace the last rule with the correct one.
        # This is a one-time repair for the previous broken migration.
        hr_match = re.search(r'(## Hard [Rr]ules\s*\n)(.*?)(?=\n## |\Z)',
                             body, re.DOTALL)
        if hr_match and 'no silent failure' not in hr_match.group(2).lower():
            section = hr_match.group(0)
            # Find numbered list items
            new_section = re.sub(
                r'(?ms)(\d+\.\s+\*\*[^*]+\*\*[^\n]*\n)(?=\d+\.)',
                lambda _m: '', section, count=1
            )
            # If regex above didn't trim, do it manually: keep first 2 items
            # and replace the 3rd with "No silent failure"
            items = re.findall(r'(?ms)\d+\.\s+\*\*[^*]+\*\*[^\n]*\n?', section)
            if len(items) >= 2:
                new_section = hr_match.group(1) + ''.join(items[:2])
                new_section += "3. **No silent failure.** Every script invocation, API call, or tool use must declare its exit status and what to do on non-zero. A skill that silently swallows errors is a violation.\n"
                body = body[:hr_match.start()] + new_section + body[hr_match.end():]
    else:
        body = insert_after_h1(body, HARD_RULES)

    # --- Step 3: Cross-references ---
    if has_section(body, "Cross-references") or has_section(body, "Cross-References"):
        pass
    else:
        slug = skill_md.parent.name
        xrefs = build_cross_references(category, skills_root, slug)
        if xrefs:
            body = body.rstrip() + "\n\n" + xrefs + "\n"

    # --- Step 4: When to use / When NOT to use ---
    if not (has_section(body, "When to use") or has_section(body, "When To Use")):
        # Insert right after the H1 + Hard rules block (i.e. as the next
        # major section). Find end of Hard rules section.
        body = insert_after_section(body, "Hard rules", WHEN_TO_USE_STUB)

    # --- Step 5: Changelog ---
    if not has_section(body, "Changelog"):
        body = body.rstrip() + "\n\n" + CHANGELOG_STUB + "\n"

    new_content += body

    # Compare
    if new_content.strip() == content.strip():
        return False, "no change"

    if not check_only:
        skill_md.write_text(new_content)
    return True, "migrated"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills_dir", type=pathlib.Path)
    parser.add_argument("--check", action="store_true", help="dry-run")
    args = parser.parse_args()

    skills_root = args.skills_dir.resolve()
    if not skills_root.exists():
        sys.exit(f"Skills dir not found: {skills_root}")

    changed = 0
    total = 0
    for skill_md in sorted(skills_root.rglob('SKILL.md')):
        total += 1
        # Skip the reference skill — it's already v0.4.0
        if skill_md.parent.name == "systematic-review":
            continue
        did, msg = migrate_skill(skill_md, skills_root, check_only=args.check)
        if did:
            changed += 1
            print(f"  ✓ {skill_md.relative_to(skills_root.parent)}  ({msg})")
    print(f"\n{changed}/{total} skills {'would be ' if args.check else ''}migrated.")


if __name__ == "__main__":
    main()
