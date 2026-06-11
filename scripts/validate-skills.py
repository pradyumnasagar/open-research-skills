#!/usr/bin/env python3
"""Validate all SKILL.md files against the ORS specification."""

import argparse
import pathlib
import re
import sys
import yaml
from collections import defaultdict

# SPDX license list (partial)
SPDX_LICENSES = {
    "MIT", "GPL-2.0", "GPL-3.0", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause",
    "AGPL-3.0", "LGPL-2.1", "LGPL-3.0", "MPL-2.0", "CC-BY-4.0", "CC-BY-SA-4.0"
}

def validate_name(name: str, path: pathlib.Path, seen_names: set) -> list[str]:
    """Validate the name field."""
    errors = []

    # Check uniqueness
    if name in seen_names:
        errors.append(f"name is not unique (already used at {seen_names[name]})")
    seen_names[name] = path

    # Check format
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', name) and name != 'a':
        if name.startswith('-') or name.endswith('-'):
            errors.append("name must not start or end with hyphens")
        if re.search(r'[^a-z0-9-]', name):
            errors.append("name must be lowercase ASCII letters, digits, and hyphens only")
        if len(name) > 64 or len(name) < 1:
            errors.append("name must be 1-64 characters")

    # Check matches folder
    expected = path.parent.name
    if name != expected:
        errors.append(f"name '{name}' does not match folder name '{expected}'")

    return errors

def validate_description(desc: str) -> list[str]:
    """Validate the description field."""
    errors = []
    if not desc:
        errors.append("description is required")
    if len(desc) > 1024:
        errors.append("description must be ≤1024 characters")
    if len(desc) < 1:
        errors.append("description is required")
    return errors

def validate_license(license: str) -> list[str]:
    """Validate the optional license field."""
    errors = []
    if license not in SPDX_LICENSES:
        errors.append(f"license '{license}' is not a valid SPDX identifier")
    return errors

def validate_metadata_block(content: str, path: pathlib.Path) -> list[str]:
    """Validate the optional <!-- metadata: ... --> block."""
    errors = []

    # Extract metadata block
    metadata_match = re.search(r'<!-- metadata:\s*\n(.*?)-->', content, re.DOTALL)
    if metadata_match:
        metadata_yaml = metadata_match.group(1)
        try:
            metadata = yaml.safe_load(metadata_yaml)

            # Validate category
            category = metadata.get('category')
            if category:
                categories_file = path.parent.parent.parent / 'spec' / 'category-taxonomy.md'
                if categories_file.exists():
                    categories_text = categories_file.read_text()
                    if category not in categories_text.split('Category')[1].split('\n')[0].split('|')[1:-1]:
                        errors.append(f"category '{category}' is not in spec/category-taxonomy.md")

            # Validate difficulty
            difficulty = metadata.get('difficulty')
            if difficulty and difficulty not in ['beginner', 'intermediate', 'advanced']:
                errors.append(f"difficulty must be one of beginner, intermediate, advanced (got '{difficulty}')")

            # Validate tags
            tags = metadata.get('tags', [])
            if not isinstance(tags, list) or len(tags) < 1 or len(tags) > 6:
                errors.append("tags must be a list of 1-6 strings")
            else:
                for tag in tags:
                    if not re.match(r'^[a-z0-9-]+$', tag):
                        errors.append(f"tag '{tag}' must be lowercase kebab-case")
                    if tag.startswith('ors-'):
                        errors.append("tags should not include 'ors-' prefix (it's implied)")

        except yaml.YAMLError as e:
            errors.append(f"metadata YAML is invalid: {e}")
    return errors

def validate_skill(path: pathlib.Path) -> list[str]:
    """Validate a single SKILL.md file."""
    errors = []
    content = path.read_text()

    # Split frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        errors.append("missing frontmatter (YAML between --- markers)")
        return errors

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        errors.append(f"frontmatter YAML is invalid: {e}")
        return errors

    # Check required fields
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

    # Check optional license
    license = frontmatter.get('license')
    if license:
        errors.extend(validate_license(license))

    # Check metadata block
    errors.extend(validate_metadata_block(content, path))

    # Check body is not empty
    if not body:
        errors.append("skill body is empty")

    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('skills_dir', type=pathlib.Path, help='Directory with skills/')
    args = parser.parse_args()

    if not args.skills_dir.exists() or not args.skills_dir.is_dir():
        print(f"Error: {args.skills_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    skill_files = list(args.skills_dir.rglob('SKILL.md'))
    print(f"Found {len(skill_files)} SKILL.md files to validate...")

    all_errors = []
    seen_names = {}

    for skill_file in skill_files:
        errors = validate_skill(skill_file)
        if errors:
            prefix = f"❌ {skill_file.relative_to(args.skills_dir)}"
            print(f"{prefix}:")
            for error in errors:
                print(f"  - {error}")
            all_errors.extend([f"{skill_file.relative_to(args.skills_dir)}: {error}" for error in errors])

    if all_errors:
        print(f"\n❌ Found {len(all_errors)} errors across {len(all_errors) // len(skill_files)} files")
        sys.exit(1)
    else:
        print(f"✅ All {len(skill_files)} skills are valid")
        sys.exit(0)

if __name__ == '__main__':
    main()