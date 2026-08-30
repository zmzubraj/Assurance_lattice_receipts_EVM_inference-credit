#!/usr/bin/env python3
"""Fail-closed hash and path verifier for the PoI ALR MPP minimum bundle."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
import tarfile
from pathlib import Path, PurePosixPath


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_minimum_artifact_bundle.py ARCHIVE.tar.gz")
    archive = Path(sys.argv[1]).resolve()
    observed: dict[str, bytes] = {}
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar.getmembers():
            name = PurePosixPath(member.name)
            if name.is_absolute() or ".." in name.parts:
                raise SystemExit(f"unsafe archive path: {member.name}")
            if not member.isfile():
                raise SystemExit(f"non-file member is not allowed: {member.name}")
            if member.name in observed:
                raise SystemExit(f"duplicate archive member: {member.name}")
            handle = tar.extractfile(member)
            if handle is None:
                raise SystemExit(f"unreadable archive member: {member.name}")
            observed[member.name] = handle.read()

    manifest_data = observed.get("BUNDLE_MANIFEST.csv")
    if manifest_data is None:
        raise SystemExit("BUNDLE_MANIFEST.csv missing")
    expected: dict[str, tuple[int, str]] = {}
    for row in csv.DictReader(io.StringIO(manifest_data.decode("utf-8"))):
        path = row["path"]
        if path in expected:
            raise SystemExit(f"duplicate manifest path: {path}")
        expected[path] = (int(row["size_bytes"]), row["sha256"])

    errors: list[str] = []
    for path, (size, expected_hash) in expected.items():
        data = observed.get(path)
        if data is None:
            errors.append(f"missing: {path}")
            continue
        if len(data) != size:
            errors.append(f"size mismatch: {path}")
        if digest(data) != expected_hash:
            errors.append(f"hash mismatch: {path}")
    allowed_unlisted = {"BUNDLE_README.md", "BUNDLE_MANIFEST.csv"}
    unexpected = sorted(set(observed) - set(expected) - allowed_unlisted)
    errors.extend(f"unlisted member: {path}" for path in unexpected)
    report = {
        "status": "PASS" if not errors else "FAIL",
        "archive_sha256": digest(archive.read_bytes()),
        "manifest_file_count": len(expected),
        "archive_member_count": len(observed),
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
