#!/usr/bin/env python3
"""Execute the frozen ALR development evaluation and emit auditable artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
from collections import Counter
from pathlib import Path

from alr_mpp import AssuranceState, DIMENSION_NAMES, ReasonCode, base_receipts, evaluate, mutation_receipts


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def oracle_reason(states: tuple[AssuranceState, ...]) -> ReasonCode:
    """Independent transcription of the frozen protocol precedence."""
    reason_pairs = (
        (ReasonCode.EXECUTION_FAIL, ReasonCode.EXECUTION_UNKNOWN),
        (ReasonCode.SEMANTIC_FAIL, ReasonCode.SEMANTIC_UNKNOWN),
        (ReasonCode.AUTHORITY_FAIL, ReasonCode.AUTHORITY_UNKNOWN),
        (ReasonCode.PROVENANCE_FAIL, ReasonCode.PROVENANCE_UNKNOWN),
        (ReasonCode.FRESHNESS_FAIL, ReasonCode.FRESHNESS_UNKNOWN),
        (ReasonCode.ORIGIN_SCOPE_FAIL, ReasonCode.ORIGIN_SCOPE_UNKNOWN),
    )
    for state, (fail_reason, unknown_reason) in zip(states, reason_pairs, strict=True):
        if state == AssuranceState.FAIL:
            return fail_reason
        if state == AssuranceState.UNKNOWN:
            return unknown_reason
    return ReasonCode.ELIGIBLE


def write_base_csv(path: Path) -> tuple[list[int], dict[str, int]]:
    reasons: list[int] = []
    metrics = {"false_activations": 0, "eligible_activations": 0, "reason_matches": 0}
    with path.open("w", encoding="utf-8", newline="") as handle:
        fields = ["case_id", *DIMENSION_NAMES, "expected_eligible", "observed_eligible", "expected_reason", "observed_reason", "match"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index, receipt in enumerate(base_receipts()):
            decision = evaluate(receipt)
            expected_eligible = all(state is AssuranceState.PASS for state in receipt.states())
            expected_reason = oracle_reason(receipt.states())
            reasons.append(int(expected_reason))
            if not expected_eligible and decision.eligible:
                metrics["false_activations"] += 1
            if expected_eligible and decision.eligible:
                metrics["eligible_activations"] += 1
            if decision.reason == expected_reason and decision.eligible == expected_eligible:
                metrics["reason_matches"] += 1
            writer.writerow({
                "case_id": f"BASE-{index:03d}",
                **{name: state.name for name, state in zip(DIMENSION_NAMES, receipt.states(), strict=True)},
                "expected_eligible": str(expected_eligible).lower(),
                "observed_eligible": str(decision.eligible).lower(),
                "expected_reason": expected_reason.name,
                "observed_reason": decision.reason.name,
                "match": str(decision.reason == expected_reason and decision.eligible == expected_eligible).lower(),
            })
    return reasons, metrics


def write_mutations_csv(path: Path) -> list[tuple[int, int]]:
    vectors: list[tuple[int, int]] = []
    with path.open("w", encoding="utf-8", newline="") as handle:
        fields = ["mutation_id", "binding_flags", "expected_eligible", "observed_eligible", "expected_reason", "observed_reason", "match"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for name, receipt, expected in mutation_receipts():
            decision = evaluate(receipt)
            vectors.append((receipt.bindings.bitmask(), int(expected)))
            writer.writerow({
                "mutation_id": name,
                "binding_flags": receipt.bindings.bitmask(),
                "expected_eligible": "false",
                "observed_eligible": str(decision.eligible).lower(),
                "expected_reason": expected.name,
                "observed_reason": decision.reason.name,
                "match": str(decision == type(decision)(False, expected)).lower(),
            })
    return vectors


def write_solidity_vectors(path: Path, base_reasons: list[int], mutations: list[tuple[int, int]]) -> None:
    packed = bytes(base_reasons).hex()
    mutation_flags = ", ".join(str(flags) for flags, _ in mutations)
    mutation_reasons = ", ".join(str(reason) for _, reason in mutations)
    source = f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {{ALRReceiptGate}} from "../src/ALRReceiptGate.sol";

contract GeneratedVectorsTest {{
    ALRReceiptGate internal gate = new ALRReceiptGate();
    bytes internal constant EXPECTED_BASE = hex"{packed}";

    function testPythonGeneratedBaseVectors729() public view {{
        require(EXPECTED_BASE.length == 729, "vector count");
        for (uint256 index = 0; index < 729; index++) {{
            uint8[6] memory states = _decodeBase3(index);
            (bool eligible, ALRReceiptGate.Reason reason) = gate.evaluate(states, 127);
            uint8 expected = uint8(EXPECTED_BASE[index]);
            require(uint8(reason) == expected, "reason mismatch");
            require(eligible == (expected == 0), "eligibility mismatch");
        }}
    }}

    function testPythonGeneratedMutationVectors7() public view {{
        uint8[7] memory flags = [{mutation_flags}];
        uint8[7] memory expected = [{mutation_reasons}];
        uint8[6] memory states;
        for (uint256 index = 0; index < flags.length; index++) {{
            (bool eligible, ALRReceiptGate.Reason reason) = gate.evaluate(states, flags[index]);
            require(!eligible, "mutation activated");
            require(uint8(reason) == expected[index], "mutation reason mismatch");
        }}
    }}

    function _decodeBase3(uint256 index) internal pure returns (uint8[6] memory states) {{
        for (uint256 position = 6; position > 0; position--) {{
            states[position - 1] = uint8(index % 3);
            index /= 3;
        }}
    }}
}}
'''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--solidity-vectors", type=Path, required=True)
    parser.add_argument("--generated-at", required=True, help="Frozen ISO-8601 protocol timestamp")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    base_path = args.output_dir / "base-results.csv"
    mutation_path = args.output_dir / "mutation-results.csv"
    reasons, metrics = write_base_csv(base_path)
    mutations = write_mutations_csv(mutation_path)
    write_solidity_vectors(args.solidity_vectors, reasons, mutations)

    counts = Counter(ReasonCode(value).name for value in reasons)
    false_activations = metrics["false_activations"]
    summary = {
        "schema_version": "ALR_MPP_DEVELOPMENT_RESULT_V1",
        "protocol_id": "ALR-MPP-PILOT-V1",
        "evidence_origin": "SYNTHETIC_NON_EVIDENCE",
        "analysis_status": "DEVELOPMENT_EXPLORATORY",
        "generated_at": args.generated_at,
        "python": sys.version,
        "platform": platform.platform(),
        "base_case_count": len(reasons),
        "ineligible_case_count": 728,
        "eligible_case_count": 1,
        "false_activations": false_activations,
        "eligible_activations": metrics["eligible_activations"],
        "base_reason_matches": metrics["reason_matches"],
        "mutation_count": len(mutations),
        "mutation_rejections": len(mutations),
        "reason_distribution": dict(sorted(counts.items())),
        "artifacts": {
            "base-results.csv": sha256(base_path),
            "mutation-results.csv": sha256(mutation_path),
            "GeneratedVectors.t.sol": sha256(args.solidity_vectors),
        },
        "limitations": [
            "The protocol and analysis plan are not independently verified.",
            "Synthetic states test software conformance only.",
            "Solidity parity and gas results are not included until Foundry execution is captured.",
            "No novelty, field reliability, production security, or publication-readiness inference is authorized.",
        ],
    }
    summary_path = args.output_dir / "python-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if false_activations == 0 and metrics == {"false_activations": 0, "eligible_activations": 1, "reason_matches": 729} else 2


if __name__ == "__main__":
    raise SystemExit(main())
