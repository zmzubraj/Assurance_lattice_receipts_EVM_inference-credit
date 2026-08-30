#!/usr/bin/env python3
"""Mechanically validate a completed external INTAKE review return."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


EXPECTED_PATHS = {
    "00-governance/intake-original.md",
    "00-governance/intake.json",
    "00-governance/program-charter.md",
    "00-governance/study-profile.json",
}
ALLOWED_DISPOSITIONS = {"PASS", "PARTIAL", "FAIL", "UNKNOWN"}
REQUIRED_FINDING_FIELDS = {
    "direct_evidence",
    "consequence",
    "smallest_required_action",
    "residual_risk",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--review-dir", type=Path, required=True)
    args = parser.parse_args()

    case = args.case_root.expanduser().resolve()
    review = args.review_dir.expanduser().resolve()
    errors: list[str] = []

    registry_path = case / "artifact-registry.csv"
    findings_path = review / "intake-findings.csv"
    declaration_path = review / "reviewer-declaration.md"
    if not registry_path.is_file():
        errors.append("artifact-registry.csv missing")
        registry_rows = []
    else:
        with registry_path.open(newline="", encoding="utf-8") as handle:
            registry_rows = list(csv.DictReader(handle))

    registry = {row["path"]: row for row in registry_rows if row["path"] in EXPECTED_PATHS}
    if set(registry) != EXPECTED_PATHS:
        errors.append("registry does not contain exactly the four required INTAKE paths")

    if not findings_path.is_file():
        errors.append("intake-findings.csv missing")
        findings = []
    else:
        with findings_path.open(newline="", encoding="utf-8") as handle:
            findings = list(csv.DictReader(handle))

    finding_paths = [row.get("artifact_path", "") for row in findings]
    if len(findings) != 4 or set(finding_paths) != EXPECTED_PATHS or len(set(finding_paths)) != 4:
        errors.append("findings must contain each required INTAKE artifact exactly once")

    row_checks: list[dict[str, object]] = []
    for finding in findings:
        artifact_path = finding.get("artifact_path", "")
        registry_row = registry.get(artifact_path)
        artifact = case / artifact_path
        observed_hash = sha256(artifact) if artifact.is_file() else None
        disposition = finding.get("disposition", "").strip().upper()
        row_errors: list[str] = []
        if registry_row is None:
            row_errors.append("path absent from registry")
        else:
            if finding.get("revision", "") != registry_row.get("revision", ""):
                row_errors.append("revision does not match registry")
            if finding.get("sha256", "") != registry_row.get("sha256", ""):
                row_errors.append("finding hash does not match registry")
            if observed_hash != registry_row.get("sha256", ""):
                row_errors.append("current artifact hash does not match registry")
        if disposition not in ALLOWED_DISPOSITIONS:
            row_errors.append("disposition must be PASS PARTIAL FAIL or UNKNOWN")
        for field in REQUIRED_FINDING_FIELDS:
            if not finding.get(field, "").strip():
                row_errors.append(f"{field} is required")
        row_checks.append(
            {
                "artifact_path": artifact_path,
                "disposition": disposition,
                "observed_sha256": observed_hash,
                "errors": row_errors,
            }
        )
        errors.extend(f"{artifact_path}: {error}" for error in row_errors)

    declaration_complete = False
    if not declaration_path.is_file():
        errors.append("reviewer-declaration.md missing")
    else:
        declaration = declaration_path.read_text(encoding="utf-8")
        placeholders = ["<REQUIRED>", "<NONE_OR_EXPLAIN>"]
        declaration_complete = not any(item in declaration for item in placeholders)
        if not declaration_complete:
            errors.append("reviewer declaration still contains placeholders")
        if "I confirm that I reviewed the exact revisions" not in declaration:
            errors.append("reviewer declaration confirmation text missing")

    report = {
        "schema_version": "POI_ALR_EXTERNAL_INTAKE_RETURN_V1",
        "status": "PASS" if not errors else "INCOMPLETE_OR_INVALID",
        "mechanical_completeness_only": True,
        "independence_established": False,
        "scientific_verification_established": False,
        "phase_promotion": "NOT_PERFORMED",
        "declaration_complete": declaration_complete,
        "row_checks": row_checks,
        "errors": errors,
        "next_action": (
            "Registered reviewer signs each substantively approved exact artifact; strict case validation and serial phase advancement remain separate."
            if not errors
            else "Reviewer corrects the listed omissions or mismatches; do not sign or advance."
        ),
    }
    report_path = review / "intake-review-validation.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
