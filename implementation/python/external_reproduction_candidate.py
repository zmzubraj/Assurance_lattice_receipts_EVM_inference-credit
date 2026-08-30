#!/usr/bin/env python3
"""Create and test a clean-copy ALR reproduction candidate.

This harness verifies deterministic execution in a fresh temporary directory. It
does not establish reviewer independence; the operator and environment must be
recorded separately by an accountable external reproducer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


FROZEN_SOURCE_HASHES = {
    "03-design/analysis-plan.md": "614a149685504e2a6b7c75fc512763c2bcb22d529177bed06913a065a4ea1303",
    "03-design/protocol.md": "753c330aef2f22e6848583f40ef4a458775d52d01c2978833665c21299246ccf",
    "implementation/python/alr_mpp.py": "9023486cff28870f4acbbc04f7c81ee72ceebf9c912955bac65e925aff974fac",
    "implementation/python/run_evaluation.py": "7bf5d8dcfe69ef45d58d30196880f8ff10c3c11562b4cfa969d6ab08ac425e48",
    "implementation/solidity/src/ALRReceiptGate.sol": "563f32e9e810177d8dd34311762913f940c75f068e3dc055952ace028247c162",
}

FROZEN_RESULT_HASHES = {
    "base-results.csv": "44affd48e439b0ea8669ca9767d951a9a96e46cdde1b2416cea439447bf7f250",
    "mutation-results.csv": "f1ef61762a83096f68486b07e9db4948429d452fa2a7ca9af1de6d03bb4fb160",
    "python-summary.json": "b5048255525d7751f817fd3d5be510f1ee609bce06bfcd4c39e4c3d02a31178d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_case_slice(source: Path, destination: Path) -> None:
    ignore = shutil.ignore_patterns("__pycache__", "cache", "out", ".git", ".DS_Store")
    shutil.copytree(source / "implementation", destination / "implementation", ignore=ignore)
    shutil.copytree(source / "03-design", destination / "03-design", ignore=ignore)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--generated-at", default="2026-08-29T05:00:00Z")
    args = parser.parse_args()

    source = args.case_root.expanduser().resolve()
    output = args.output_dir.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)

    source_checks = {
        relative: {
            "expected": expected,
            "observed": sha256(source / relative) if (source / relative).is_file() else None,
        }
        for relative, expected in FROZEN_SOURCE_HASHES.items()
    }
    source_match = all(item["expected"] == item["observed"] for item in source_checks.values())
    if not source_match:
        report = {
            "schema_version": "ALR_EXTERNAL_REPRODUCTION_CANDIDATE_V1",
            "status": "SOURCE_HASH_MISMATCH",
            "candidate_only": True,
            "independence_established": False,
            "source_checks": source_checks,
        }
        (output / "reproduction-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return 2

    with tempfile.TemporaryDirectory(prefix="poi-alr-external-candidate-") as temporary:
        clean_root = Path(temporary) / "case"
        copy_case_slice(source, clean_root)
        argv = [
            sys.executable,
            "implementation/python/run_full_evaluation.py",
            "--case-root",
            str(clean_root),
            "--run-id",
            "external-candidate",
            "--generated-at",
            args.generated_at,
        ]
        completed = subprocess.run(
            argv,
            cwd=clean_root,
            text=True,
            capture_output=True,
            check=False,
        )
        run_dir = clean_root / "04-data/development/external-candidate"
        result_checks = {
            name: {
                "expected": expected,
                "observed": sha256(run_dir / name) if (run_dir / name).is_file() else None,
            }
            for name, expected in FROZEN_RESULT_HASHES.items()
        }
        result_match = all(item["expected"] == item["observed"] for item in result_checks.values())

        if run_dir.is_dir():
            shutil.copytree(run_dir, output / "run", dirs_exist_ok=True)
        vectors = clean_root / "implementation/solidity/test/GeneratedVectors.t.sol"
        if vectors.is_file():
            shutil.copy2(vectors, output / "GeneratedVectors.t.sol")

        report = {
            "schema_version": "ALR_EXTERNAL_REPRODUCTION_CANDIDATE_V1",
            "status": "PASS" if completed.returncode == 0 and result_match else "FAIL",
            "candidate_only": True,
            "independence_established": False,
            "independence_note": (
                "A qualified external operator must run this harness in an independently controlled "
                "environment and record identity, conflicts, toolchain, and direct evidence."
            ),
            "network_required": False,
            "command": argv,
            "returncode": completed.returncode,
            "source_checks": source_checks,
            "result_checks": result_checks,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "phase_promotion": "NOT_PERFORMED",
        }
        (output / "reproduction-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
