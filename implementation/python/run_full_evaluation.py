#!/usr/bin/env python3
"""Run and capture the complete ALR development evaluation without network access."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], cwd: Path, log_path: Path, env: dict[str, str]) -> int:
    completed = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    log_path.write_text(
        "$ " + " ".join(argv) + "\n\nSTDOUT\n" + completed.stdout + "\nSTDERR\n" + completed.stderr,
        encoding="utf-8",
    )
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--generated-at", required=True)
    args = parser.parse_args()

    root = args.case_root.resolve()
    output = root / "04-data" / "development" / args.run_id
    output.mkdir(parents=True, exist_ok=True)
    vectors = root / "implementation" / "solidity" / "test" / "GeneratedVectors.t.sol"
    env = dict(os.environ)
    env.update({"PYTHONHASHSEED": "0", "TZ": "UTC", "LC_ALL": "C", "LANG": "C"})

    commands = [
        ([sys.executable, "-m", "unittest", "discover", "-s", "implementation/tests", "-v"], output / "python-tests.log"),
        ([sys.executable, "implementation/python/run_evaluation.py", "--output-dir", str(output), "--solidity-vectors", str(vectors), "--generated-at", args.generated_at], output / "python-evaluation.log"),
        (["forge", "test", "--root", "implementation/solidity", "-vv"], output / "forge-test.log"),
    ]
    records = []
    overall = 0
    for argv, log_path in commands:
        returncode = run(argv, root, log_path, env)
        records.append({"argv": argv, "returncode": returncode, "log": str(log_path.relative_to(root))})
        if returncode != 0:
            overall = returncode
            break

    tracked = [
        output / "base-results.csv",
        output / "mutation-results.csv",
        output / "python-summary.json",
        output / "python-tests.log",
        output / "python-evaluation.log",
        output / "forge-test.log",
        vectors,
        root / "implementation/python/alr_mpp.py",
        root / "implementation/python/run_evaluation.py",
        root / "implementation/solidity/src/ALRReceiptGate.sol",
        root / "03-design/protocol.md",
        root / "03-design/analysis-plan.md",
    ]
    artifacts = {
        str(path.relative_to(root)): sha256(path)
        for path in tracked
        if path.is_file()
    }
    manifest = {
        "schema_version": "ALR_MPP_DEVELOPMENT_RUN_MANIFEST_V1",
        "run_id": args.run_id,
        "protocol_id": "ALR-MPP-PILOT-V1",
        "analysis_status": "DEVELOPMENT_EXPLORATORY",
        "evidence_origin": "SYNTHETIC_NON_EVIDENCE",
        "network_required": False,
        "generated_at": args.generated_at,
        "commands": records,
        "artifacts": artifacts,
        "overall_returncode": overall,
        "phase_promotion": "NOT_PERFORMED",
        "limitations": [
            "Protocol and methods review remain independently unverified.",
            "This run supports only development-level software conformance.",
            "Foundry gas figures are test-call measurements, not a frozen production comparator.",
        ],
    }
    (output / "run-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, sort_keys=True))
    return overall


if __name__ == "__main__":
    raise SystemExit(main())
