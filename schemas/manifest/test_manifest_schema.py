#!/usr/bin/env python3
"""
Test runner for AICF-002A Manifest JSON Schema.
Validates schemas/manifest/aicf-manifest.schema.json and the 12 validation fixtures.
"""

import json
import os
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

def run_tests():
    base_dir = Path(__file__).resolve().parent
    schema_path = base_dir / "aicf-manifest.schema.json"
    fixtures_dir = base_dir / "fixtures"

    print("=================================================================")
    print(" AICF-002A: Manifest JSON Schema Test Suite (Draft 2020-12)")
    print("=================================================================")

    # 1. Load and validate schema against Draft 2020-12 meta-schema
    print(f"\n[1/2] Checking Schema Definition: {schema_path.name}")
    if not schema_path.exists():
        print(f"FAIL: Schema not found at {schema_path}")
        return 1

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        Draft202012Validator.check_schema(schema)
        print(" PASS: Schema conforms to JSON Schema Draft 2020-12 meta-schema.")
    except Exception as e:
        print(f" FAIL: Schema meta-validation failed: {e}")
        return 1

    validator = Draft202012Validator(schema)

    # 2. Test Fixtures
    fixture_expectations = {
        "01-minimal-valid.json": {
            "valid": True,
            "description": "Minimal valid manifest"
        },
        "02-fully-populated-valid.json": {
            "valid": True,
            "description": "Fully populated valid manifest"
        },
        "03-missing-aicf-version.json": {
            "valid": False,
            "description": "Missing aicf.version"
        },
        "04-missing-project-id.json": {
            "valid": False,
            "description": "Missing project.id"
        },
        "05-missing-project-name.json": {
            "valid": False,
            "description": "Missing project.name"
        },
        "06-missing-profile-id.json": {
            "valid": False,
            "description": "Missing profile.id"
        },
        "07-invalid-field-types.json": {
            "valid": False,
            "description": "Invalid field types"
        },
        "08-unsafe-absolute-artifact-paths.json": {
            "valid": False,
            "description": "Unsafe absolute artifact paths"
        },
        "09-artifact-path-traversal.json": {
            "valid": False,
            "description": "Artifact path traversal"
        },
        "10-unknown-top-level-properties.json": {
            "valid": False,
            "description": "Unknown top-level/core properties"
        },
        "11-valid-extensions.json": {
            "valid": True,
            "description": "Valid extensions"
        },
        "12-vendor-config-at-core-rejected.json": {
            "valid": False,
            "description": "Vendor-specific configuration rejected at core level"
        }
    }

    print(f"\n[2/2] Validating Fixtures ({len(fixture_expectations)} total)")
    passed = 0
    failed = 0

    for filename, config in sorted(fixture_expectations.items()):
        fixture_path = fixtures_dir / filename
        if not fixture_path.exists():
            print(f" FAIL: Missing fixture file {filename}")
            failed += 1
            continue

        with open(fixture_path, "r", encoding="utf-8") as f:
            instance = json.load(f)

        errors = list(validator.iter_errors(instance))
        is_valid = len(errors) == 0
        expected_valid = config["valid"]
        desc = config["description"]

        if is_valid == expected_valid:
            status = "PASS"
            passed += 1
            if expected_valid:
                print(f"  [{status}] {filename} -> VALID (as expected: {desc})")
            else:
                sample_error = errors[0].message if errors else "unknown"
                print(f"  [{status}] {filename} -> REJECTED (as expected: {desc})")
                print(f"         Reason: {sample_error}")
        else:
            status = "FAIL"
            failed += 1
            print(f"  [{status}] {filename} -> Got valid={is_valid}, expected={expected_valid} ({desc})")
            if errors:
                for err in errors:
                    print(f"         Error: {err.message}")

    print("\n-----------------------------------------------------------------")
    print(f" Summary: {passed} passed, {failed} failed out of {len(fixture_expectations)} fixtures.")
    print("-----------------------------------------------------------------")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(run_tests())
