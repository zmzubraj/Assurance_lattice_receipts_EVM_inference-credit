#!/usr/bin/env python3
"""Run frozen Python-generated Solidity vectors with offline pinned Foundry."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


EXPECTED_VECTOR_SHA256 = "6fc0cec1f7e6f1b855aafa92932fca764a7745d60c7ffe20c6a5b2180ab506f4"
EXPECTED_CONTRACT_SHA256 = "563f32e9e810177d8dd34311762913f940c75f068e3dc055952ace028247c162"
EXPECTED_TESTS = (
    "testPythonGeneratedBaseVectors729",
    "testPythonGeneratedMutationVectors7",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    case_root = args.case_root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    work = output / "solidity-work"
    if work.exists():
        shutil.rmtree(work)
    (work / "src").mkdir(parents=True)
    (work / "test").mkdir(parents=True)

    shutil.copy2(case_root / "implementation/solidity/foundry.toml", work / "foundry.toml")
    shutil.copy2(
        case_root / "implementation/solidity/src/ALRReceiptGate.sol",
        work / "src/ALRReceiptGate.sol",
    )
    generated_vectors = output / "GeneratedVectors.t.sol"
    if generated_vectors.is_file():
        shutil.copy2(generated_vectors, work / "test/GeneratedVectors.t.sol")

    errors: list[str] = []
    vector_hash = digest(generated_vectors) if generated_vectors.is_file() else None
    contract_hash = digest(work / "src/ALRReceiptGate.sol")
    if vector_hash != EXPECTED_VECTOR_SHA256:
        errors.append("generated Solidity vector hash mismatch")
    if contract_hash != EXPECTED_CONTRACT_SHA256:
        errors.append("Solidity contract hash mismatch")

    forge_version = run(["/usr/local/bin/forge", "--version"])
    solc_version = run(["/usr/local/bin/solc", "--version"])
    test = run([
        "/usr/local/bin/forge",
        "test",
        "--offline",
        "--root",
        str(work),
        "--use",
        "/usr/local/bin/solc",
        "-vv",
    ])
    combined = test.stdout + test.stderr
    (output / "forge-test.log").write_text(combined, encoding="utf-8")
    if test.returncode != 0:
        errors.append(f"forge test returned {test.returncode}")
    for name in EXPECTED_TESTS:
        if f"[PASS] {name}()" not in combined:
            errors.append(f"missing passing test record: {name}")
    match = re.search(r"2 tests passed, 0 failed, 0 skipped", combined)
    if not match:
        errors.append("unexpected Foundry suite totals")

    report = {
        "schema_version": "POI_ALR_HERMETIC_FOUNDRY_REPLAY_V1",
        "status": "PASS" if not errors else "FAIL",
        "evidence_origin": "SYNTHETIC_NON_EVIDENCE",
        "analysis_status": "DEVELOPMENT_EXPLORATORY",
        "network_required": False,
        "offline_flag": True,
        "command": [
            "/usr/local/bin/forge", "test", "--offline", "--root",
            str(work), "--use", "/usr/local/bin/solc", "-vv",
        ],
        "returncode": test.returncode,
        "forge_version": forge_version.stdout.strip(),
        "solc_version": solc_version.stdout.strip(),
        "generated_vector_sha256": vector_hash,
        "contract_sha256": contract_hash,
        "expected_tests": list(EXPECTED_TESTS),
        "test_count": 2 if match else None,
        "failed_count": 0 if match else None,
        "errors": errors,
        "gas_boundary": "Foundry test-call gas is descriptive only; no transaction or production-gas claim is authorized.",
        "phase_promotion": "NOT_PERFORMED",
        "independence_established": False,
    }
    (output / "hermetic-foundry-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
