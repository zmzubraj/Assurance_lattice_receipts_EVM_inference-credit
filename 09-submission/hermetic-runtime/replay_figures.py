#!/usr/bin/env python3
"""Clean-build the three declared TikZ figures into an isolated output directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess


SOURCES = (
    "figure1-architecture.tex",
    "figure2-workflow.tex",
    "figure3-reason-distribution.tex",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-date-epoch", required=True)
    args = parser.parse_args()

    case_root = args.case_root.resolve()
    source_root = case_root / "09-submission/frontiers-in-blockchain-technology-code/figures"
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update({
        "SOURCE_DATE_EPOCH": args.source_date_epoch,
        "FORCE_SOURCE_DATE": "1",
        "TZ": "UTC",
        "LC_ALL": "C",
        "LANG": "C",
    })
    records: list[dict[str, object]] = []
    for source_name in SOURCES:
        command = [
            "pdflatex",
            "-no-shell-escape",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-output-directory={output}",
            source_name,
        ]
        completed = subprocess.run(
            command,
            cwd=source_root,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        log_path = output / f"{Path(source_name).stem}.replay.log"
        log_path.write_text(completed.stdout + "\n" + completed.stderr, encoding="utf-8")
        pdf_path = output / f"{Path(source_name).stem}.pdf"
        records.append({
            "source": source_name,
            "argv": command,
            "returncode": completed.returncode,
            "pdf_sha256": digest(pdf_path) if pdf_path.is_file() else "",
            "log_sha256": digest(log_path),
        })
        if completed.returncode != 0:
            break

    status = "PASS" if len(records) == len(SOURCES) and all(row["returncode"] == 0 for row in records) else "FAIL"
    report = {
        "schema_version": "POI_ALR_HERMETIC_FIGURE_REPLAY_V1",
        "status": status,
        "records": records,
        "source_date_epoch": args.source_date_epoch,
        "network_required": False,
        "phase_promotion": "NOT_PERFORMED",
    }
    (output / "figure-replay-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
