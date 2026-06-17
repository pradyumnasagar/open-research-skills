#!/usr/bin/env python3
"""Validate Material Passport JSON files against spec/material-passport.schema.json.

Usage:
    python scripts/validate-passport.py examples/*.passport.json
    python scripts/validate-passport.py --all   # validate every *.passport.json in examples/

Exits 0 if every file is valid, 1 otherwise.
"""

import argparse
import json
import pathlib
import sys

try:
    import jsonschema
except ImportError:
    print("error: jsonschema package is required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


SCHEMA_PATH = pathlib.Path(__file__).parent.parent / "spec" / "material-passport.schema.json"
EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / "examples"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def validate_file(path: pathlib.Path, schema: dict) -> list[str]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"invalid JSON: {e}"]

    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for err in validator.iter_errors(data):
        # Format: "<path>: <message>"
        loc = ".".join(str(p) for p in err.absolute_path) if err.absolute_path else "<root>"
        errors.append(f"{loc}: {err.message}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("paths", nargs="*", type=pathlib.Path, help="Passport JSON files to validate.")
    ap.add_argument("--all", action="store_true", help=f"Validate every *.passport.json in {EXAMPLES_DIR}/")
    args = ap.parse_args()

    if not SCHEMA_PATH.exists():
        print(f"error: schema not found at {SCHEMA_PATH}", file=sys.stderr)
        return 2

    schema = load_schema()

    if args.all:
        paths = sorted(EXAMPLES_DIR.glob("*.passport.json"))
    else:
        paths = args.paths

    if not paths:
        print("no passports to validate", file=sys.stderr)
        return 1

    failed = 0
    for p in paths:
        if not p.exists():
            print(f"❌ {p}: file not found")
            failed += 1
            continue
        errors = validate_file(p, schema)
        if errors:
            print(f"❌ {p}:")
            for e in errors:
                print(f"   - {e}")
            failed += 1
        else:
            print(f"✅ {p}")

    if failed:
        print(f"\n{failed}/{len(paths)} passport(s) failed.")
        return 1
    print(f"\nAll {len(paths)} passport(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
