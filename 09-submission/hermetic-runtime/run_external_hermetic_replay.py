#!/usr/bin/env python3
"""Replay the frozen PoI ALR package in the exact content-addressed runtime.

This is a transfer/reproducibility driver, not an independence certificate. It
never changes the research-case phase and always reports independence as false;
an accountable external reviewer must separately document identity, environment,
conflicts, deviations, and scientific findings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import subprocess
import sys


RUNTIME_IMAGE = (
    "poi-alr/texlive-foundry-poppler@"
    "sha256:b33763e92d1295e4d1fec00e613084624ce6b805c1fc882ee5a72778039c6ebc"
)
SOURCE_DATE_EPOCH = "1787979600"
EXPECTED_INPUT_HASHES = {
    ".latexmkrc": "e2b60569765dd752fc60408e5f0dc4a43640d3fd13ae2a99a0a1c77236d502a2",
    "07-manuscript/manuscript.tex": "1cf14b0abc5f45673d2cebe6e0eeaf01575cb0458b0b01894055951ab2a20a25",
    "07-manuscript/latex/main.tex": "f197112acaa9af304553ba4f7ae17e995015898d6a1b39313a9805707679f05b",
    "07-manuscript/latex/references.bib": "b63dae78195e3b7903c3f36852f351be8870744d8578ea2e80af8990c7c8c0b4",
    "09-submission/hermetic-runtime/runtime.lock": (
        "8a180399f5dd0f4ae662da2f1f7daf7599f457e8551d9563653c9b23890abcbb"
    ),
    "09-submission/hermetic-runtime/runtime-sbom.spdx.json": (
        "55cd06de5387e426aac6cd0df7fe51b6f19c24a28746e4fc245bd5a0d9c91a65"
    ),
}
EXPECTED_PDF_SHA256 = "a6364b8b865afdcfbd5a885d8156bb9bd1a61d1f7a78934e42432ac1bda37400"

COMMANDS = (
    (
        "python",
        "-m",
        "unittest",
        "discover",
        "-s",
        "implementation/tests",
        "-v",
    ),
    (
        "python",
        "implementation/python/run_evaluation.py",
        "--output-dir",
        "/output/analysis",
        "--solidity-vectors",
        "/output/analysis/GeneratedVectors.t.sol",
        "--generated-at",
        "2026-08-29T05:00:00Z",
    ),
    (
        "python",
        "09-submission/hermetic-runtime/run_hermetic_foundry.py",
        "--case-root",
        "/workspace",
        "--output-dir",
        "/output/analysis",
    ),
    (
        "python",
        "09-submission/hermetic-runtime/verify_hermetic_analysis.py",
        "--case-root",
        "/workspace",
        "--output-dir",
        "/output/analysis",
    ),
    (
        "python",
        "09-submission/hermetic-runtime/replay_figures.py",
        "--case-root",
        "/workspace",
        "--output-dir",
        "/output/figures",
        "--source-date-epoch",
        SOURCE_DATE_EPOCH,
    ),
    (
        "latexmk",
        "-pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "-outdir=/output",
        "/workspace/07-manuscript/manuscript.tex",
    ),
    ("pdfinfo", "/output/manuscript.pdf"),
    ("pdffonts", "/output/manuscript.pdf"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_report(output: Path, report: dict[str, object]) -> None:
    (output / "external-hermetic-replay-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--docker", default="docker")
    args = parser.parse_args()

    case = args.case_root.expanduser().resolve()
    output = args.output_dir.expanduser().resolve()
    report: dict[str, object] = {
        "schema_version": "POI_ALR_EXTERNAL_HERMETIC_REPLAY_V1",
        "status": "FAIL",
        "generated_at": utc_now(),
        "runtime_image": RUNTIME_IMAGE,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "candidate_only": True,
        "independence_established": False,
        "phase_promotion": "NOT_PERFORMED",
        "evidence_origin": "SYNTHETIC_NON_EVIDENCE",
        "limitations": [
            "Execution and matching hashes do not establish scientific validity or novelty.",
            "Foundry test-call gas is descriptive only and supports no production-gas claim.",
            "A separately signed accountable external review is required for independence.",
        ],
        "errors": [],
        "commands": [],
    }

    if not case.is_dir():
        raise SystemExit(f"case root is not a directory: {case}")
    if output == case or output.is_relative_to(case):
        raise SystemExit("output directory must be outside the read-only case root")
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"output directory must be new or empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    docker = shutil.which(args.docker)
    if docker is None:
        report["errors"] = [f"container runtime not found: {args.docker}"]
        write_report(output, report)
        return 2

    input_checks: dict[str, dict[str, object]] = {}
    for relative, expected in EXPECTED_INPUT_HASHES.items():
        path = case / relative
        observed = sha256(path) if path.is_file() else None
        input_checks[relative] = {
            "expected": expected,
            "observed": observed,
            "match": observed == expected,
        }
    report["input_checks"] = input_checks
    if not all(item["match"] for item in input_checks.values()):
        report["errors"] = ["one or more frozen input hashes do not match"]
        write_report(output, report)
        return 2

    inspect = subprocess.run(
        [docker, "image", "inspect", RUNTIME_IMAGE, "--format", "{{.Id}}"],
        text=True,
        capture_output=True,
        check=False,
    )
    report["runtime_inspect"] = {
        "returncode": inspect.returncode,
        "image_id": inspect.stdout.strip(),
        "stderr": inspect.stderr,
    }
    if inspect.returncode != 0:
        report["errors"] = [
            "exact runtime image is unavailable; obtain it through an authorized channel or rebuild it from the pinned Dockerfile"
        ]
        write_report(output, report)
        return 2

    base = [
        docker,
        "run",
        "--rm",
        "--platform=linux/amd64",
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--pids-limit=256",
        "--tmpfs=/tmp:rw,nosuid,nodev,noexec,size=1g",
        "--mount",
        f"type=bind,src={case},dst=/workspace,readonly",
        "--mount",
        f"type=bind,src={output},dst=/output",
        "--workdir=/workspace",
        "--env",
        f"SOURCE_DATE_EPOCH={SOURCE_DATE_EPOCH}",
        RUNTIME_IMAGE,
    ]

    command_records: list[dict[str, object]] = []
    for index, declared in enumerate(COMMANDS, start=1):
        completed = subprocess.run(
            [*base, *declared], text=True, capture_output=True, check=False
        )
        stdout_path = output / f"command-{index:02d}.stdout.log"
        stderr_path = output / f"command-{index:02d}.stderr.log"
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        command_records.append(
            {
                "index": index,
                "declared_argv": list(declared),
                "returncode": completed.returncode,
                "stdout_path": stdout_path.name,
                "stdout_sha256": sha256(stdout_path),
                "stderr_path": stderr_path.name,
                "stderr_sha256": sha256(stderr_path),
            }
        )
        if completed.returncode != 0:
            report["errors"] = [f"command {index} returned {completed.returncode}"]
            break
    report["commands"] = command_records

    analysis_path = output / "analysis/hermetic-analysis-verification.json"
    figure_path = output / "figures/figure-replay-report.json"
    pdf_path = output / "manuscript.pdf"
    analysis = json.loads(analysis_path.read_text()) if analysis_path.is_file() else {}
    figures = json.loads(figure_path.read_text()) if figure_path.is_file() else {}
    observed_pdf = sha256(pdf_path) if pdf_path.is_file() else None
    final_log_path = output / "manuscript.log"
    final_log = (
        final_log_path.read_text(encoding="utf-8", errors="replace")
        if final_log_path.is_file()
        else ""
    )
    unresolved = sorted(
        set(
            re.findall(
                r"(?:undefined references|Citation .+ undefined|Reference .+ undefined)",
                final_log,
                flags=re.IGNORECASE,
            )
        )
    )
    layout_warnings = sorted(
        set(re.findall(r"(?:Overfull|Underfull) \\[hv]box[^\n]*", final_log))
    )
    fonts_log_path = output / "command-08.stdout.log"
    font_lines = (
        [
            line
            for line in fonts_log_path.read_text(encoding="utf-8", errors="replace")
            .splitlines()[2:]
            if line.strip()
        ]
        if fonts_log_path.is_file()
        else []
    )
    fonts_embedded = bool(font_lines) and all(
        " yes " in f" {line.lower()} " for line in font_lines
    )
    report["decisive_checks"] = {
        "all_eight_commands_zero": (
            len(command_records) == 8
            and all(item["returncode"] == 0 for item in command_records)
        ),
        "analysis_status": analysis.get("status"),
        "analysis_errors": analysis.get("errors"),
        "foundry_status": analysis.get("foundry_parity", {}).get("status"),
        "foundry_test_count": analysis.get("foundry_parity", {}).get("test_count"),
        "foundry_failed_count": analysis.get("foundry_parity", {}).get("failed_count"),
        "figure_status": figures.get("status"),
        "compile_passed": pdf_path.is_file()
        and len(command_records) >= 6
        and command_records[5]["returncode"] == 0,
        "fonts_embedded": fonts_embedded,
        "unresolved_references": unresolved,
        "layout_warnings": layout_warnings,
        "human_rendered_page_review": "REQUIRED",
        "expected_pdf_sha256": EXPECTED_PDF_SHA256,
        "observed_pdf_sha256": observed_pdf,
        "pdf_hash_match": observed_pdf == EXPECTED_PDF_SHA256,
    }
    decisive = report["decisive_checks"]
    passed = (
        not report["errors"]
        and decisive["all_eight_commands_zero"]
        and decisive["analysis_status"] == "PASS"
        and decisive["analysis_errors"] == []
        and decisive["foundry_status"] == "PASS"
        and decisive["foundry_test_count"] == 2
        and decisive["foundry_failed_count"] == 0
        and decisive["figure_status"] == "PASS"
        and decisive["compile_passed"]
        and decisive["fonts_embedded"]
        and decisive["unresolved_references"] == []
        and decisive["layout_warnings"] == []
        and decisive["pdf_hash_match"]
    )
    report["status"] = "PASS" if passed else "FAIL"
    if not passed and not report["errors"]:
        report["errors"] = ["one or more decisive replay checks failed"]
    write_report(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
