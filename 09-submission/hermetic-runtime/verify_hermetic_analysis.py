#!/usr/bin/env python3
"""Verify hermetic Python and Foundry replay outputs against frozen invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_HASHES = {
    "base-results.csv": "44affd48e439b0ea8669ca9767d951a9a96e46cdde1b2416cea439447bf7f250",
    "mutation-results.csv": "f1ef61762a83096f68486b07e9db4948429d452fa2a7ca9af1de6d03bb4fb160",
}

EXPECTED_VECTOR_SHA256 = "6fc0cec1f7e6f1b855aafa92932fca764a7745d60c7ffe20c6a5b2180ab506f4"

EXPECTED_SUMMARY = {
    "analysis_status": "DEVELOPMENT_EXPLORATORY",
    "evidence_origin": "SYNTHETIC_NON_EVIDENCE",
    "base_case_count": 729,
    "ineligible_case_count": 728,
    "eligible_case_count": 1,
    "false_activations": 0,
    "eligible_activations": 1,
    "base_reason_matches": 729,
    "mutation_count": 7,
    "mutation_rejections": 7,
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    case_root = args.case_root.resolve()
    output = args.output_dir.resolve()
    errors: list[str] = []
    observed_hashes: dict[str, str] = {}
    for name, expected in EXPECTED_HASHES.items():
        path = output / name
        if not path.is_file():
            errors.append(f"missing {name}")
            continue
        observed = digest(path)
        observed_hashes[name] = observed
        if observed != expected:
            errors.append(f"hash mismatch for {name}")

    summary_path = output / "python-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.is_file() else {}
    if not summary:
        errors.append("missing python-summary.json")
    for key, expected in EXPECTED_SUMMARY.items():
        if summary.get(key) != expected:
            errors.append(f"summary mismatch for {key}")

    vector_path = output / "GeneratedVectors.t.sol"
    vector_hash = digest(vector_path) if vector_path.is_file() else None
    if vector_hash != EXPECTED_VECTOR_SHA256:
        errors.append("generated Solidity vector hash mismatch")

    foundry_path = output / "hermetic-foundry-report.json"
    foundry = json.loads(foundry_path.read_text(encoding="utf-8")) if foundry_path.is_file() else {}
    if not foundry:
        errors.append("missing hermetic-foundry-report.json")
    else:
        if foundry.get("status") != "PASS":
            errors.append("hermetic Foundry replay did not pass")
        if foundry.get("returncode") != 0:
            errors.append("hermetic Foundry return code was not zero")
        if foundry.get("test_count") != 2 or foundry.get("failed_count") != 0:
            errors.append("hermetic Foundry suite totals mismatch")
        if foundry.get("generated_vector_sha256") != EXPECTED_VECTOR_SHA256:
            errors.append("hermetic Foundry vector hash mismatch")

    canonical = case_root / "04-data/development/alr-pilot-v1-run-001"
    canonical_hashes = {
        name: digest(canonical / name)
        for name in EXPECTED_HASHES
        if (canonical / name).is_file()
    }
    if canonical_hashes != EXPECTED_HASHES:
        errors.append("canonical frozen result hashes no longer match the verifier contract")

    report = {
        "schema_version": "POI_ALR_HERMETIC_ANALYSIS_VERIFICATION_V2",
        "status": "PASS" if not errors else "FAIL",
        "evidence_origin": "SYNTHETIC_NON_EVIDENCE",
        "analysis_status": "DEVELOPMENT_EXPLORATORY",
        "observed_hashes": observed_hashes,
        "expected_hashes": EXPECTED_HASHES,
        "summary_invariants": EXPECTED_SUMMARY,
        "generated_vector_sha256": vector_hash,
        "foundry_report_sha256": digest(foundry_path) if foundry_path.is_file() else None,
        "foundry_parity": {
            "status": foundry.get("status"),
            "test_count": foundry.get("test_count"),
            "failed_count": foundry.get("failed_count"),
            "forge_version": foundry.get("forge_version"),
            "solc_version": foundry.get("solc_version"),
        },
        "errors": errors,
        "phase_promotion": "NOT_PERFORMED",
        "independence_established": False,
    }
    (output / "hermetic-analysis-verification.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
