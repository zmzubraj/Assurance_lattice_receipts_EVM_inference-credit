#!/usr/bin/env python3
"""Build a deterministic local-review bundle for the PoI ALR MPP case."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path


INCLUDE_ROOTS = (
    "00-governance",
    "01-novelty",
    "02-feasibility",
    "03-design",
    "04-data",
    "05-analysis",
    "06-visuals",
    "07-manuscript",
    "08-validation",
    "09-submission/frontiers-in-blockchain-technology-code",
    "09-submission/hermetic-runtime",
    "09-submission/hermetic-output",
    "implementation",
)

INCLUDE_FILES = (
    "INDEX.md",
    ".latexmkrc",
    "program-state.json",
    "artifact-registry.csv",
    "agent-registry.csv",
    "09-submission/acceptance-readiness.md",
    "09-submission/analysis-replay-report.md",
    "09-submission/build-manifest.json",
    "09-submission/environment-capture.json",
    "09-submission/novelty-refresh.md",
    "09-submission/package-manifest.json",
    "09-submission/pdf-qa.json",
    "09-submission/reporting-checklist.md",
    "09-submission/submission-audit.md",
    "09-submission/submission-gate-ledger.csv",
    "09-submission/venue-portfolio.csv",
    "09-submission/venue-rules.md",
    "09-submission/build_minimum_artifact_bundle.py",
    "09-submission/verify_minimum_artifact_bundle.py",
)

EXCLUDED_NAMES = {
    ".DS_Store",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

EXCLUDED_SUFFIXES = {
    ".aux",
    ".blg",
    ".bbl",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".toc",
    ".synctex.gz",
    ".pyc",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def excluded(path: Path) -> bool:
    if any(part in EXCLUDED_NAMES for part in path.parts):
        return True
    name = path.name
    return any(name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)


def source_files(case: Path) -> list[Path]:
    files: set[Path] = set()
    for root_name in INCLUDE_ROOTS:
        root = case / root_name
        if not root.is_dir():
            raise SystemExit(f"required bundle root missing: {root_name}")
        for path in root.rglob("*"):
            if path.is_symlink():
                raise SystemExit(f"symlink not allowed in bundle: {path.relative_to(case)}")
            if path.is_file() and not excluded(path.relative_to(case)):
                files.add(path)
    for file_name in INCLUDE_FILES:
        path = case / file_name
        if not path.is_file():
            raise SystemExit(f"required bundle file missing: {file_name}")
        files.add(path)
    return sorted(files, key=lambda p: p.relative_to(case).as_posix())


def manifest_bytes(case: Path, files: list[Path]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["path", "size_bytes", "sha256"])
    for path in files:
        data = path.read_bytes()
        writer.writerow([path.relative_to(case).as_posix(), len(data), sha256(data)])
    return stream.getvalue().encode("utf-8")


def readme_bytes() -> bytes:
    return """# PoI ALR MPP minimum artifact bundle

Status: DEVELOPMENT DRAFT — NOT SUBMISSION READY and not authorized for public release.

This local-review bundle preserves the narrowed prototype, frozen development data,
negative and unresolved findings, analysis outputs, manuscript sources, compiled
draft PDFs, official-venue adaptation, reproducibility harness, and external human
and scientific gate instructions. File hashes are listed in BUNDLE_MANIFEST.csv.

Start with INDEX.md, 00-governance/EXTERNAL_HUMAN_SCIENTIFIC_GATE_RUNBOOK.md,
08-validation/EXTERNAL_REVIEW_PACKET.md,
08-validation/external-gate-kit/README.md, and artifact-registry.csv. The canonical
case remains at phase INTAKE. A clean build or matching hash does not establish
novelty, scientific validity, independent reproduction, authorship, licensing,
publication readiness, or submission authorization.

Frontiers draft build:
  cd 09-submission/frontiers-in-blockchain-technology-code
  ./build_frontiers_draft.sh

Fresh-directory reproduction candidate:
  python3 implementation/python/external_reproduction_candidate.py \
    --case-root . --output-dir /ABSOLUTE/REVIEWER_CONTROLLED/OUTPUT

Exact hermetic replay after the content-addressed runtime image is available:
  python3 09-submission/hermetic-runtime/run_external_hermetic_replay.py \
    --case-root /ABSOLUTE/PATH/TO/EXTRACTED/CASE \
    --output-dir /ABSOLUTE/REVIEWER_CONTROLLED/HERMETIC_OUTPUT
""".encode("utf-8")


def add_bytes(tar: tarfile.TarFile, name: str, data: bytes, mode: int = 0o644) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mode = mode
    tar.addfile(info, io.BytesIO(data))


def build(case: Path, output: Path) -> dict[str, object]:
    files = source_files(case)
    manifest = manifest_bytes(case, files)
    readme = readme_bytes()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as tar:
                add_bytes(tar, "BUNDLE_README.md", readme)
                add_bytes(tar, "BUNDLE_MANIFEST.csv", manifest)
                for path in files:
                    rel = path.relative_to(case).as_posix()
                    mode = 0o755 if path.stat().st_mode & 0o111 else 0o644
                    add_bytes(tar, rel, path.read_bytes(), mode)
    archive = output.read_bytes()
    return {
        "status": "DEVELOPMENT_DRAFT_NOT_SUBMISSION_READY",
        "archive": output.name,
        "archive_sha256": sha256(archive),
        "archive_size_bytes": len(archive),
        "source_file_count": len(files),
        "internal_manifest_sha256": sha256(manifest),
        "deterministic_epoch": 0,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "independent_verification": False,
        "public_release_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", default=".")
    parser.add_argument(
        "--output",
        default="09-submission/packages/poi-alr-mpp-minimum-artifact-bundle-v1.tar.gz",
    )
    parser.add_argument(
        "--report",
        default="09-submission/packages/poi-alr-mpp-minimum-artifact-bundle-v1.report.json",
    )
    args = parser.parse_args()
    case = Path(args.case_root).resolve()
    output = (case / args.output).resolve()
    report_path = (case / args.report).resolve()
    report = build(case, output)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
