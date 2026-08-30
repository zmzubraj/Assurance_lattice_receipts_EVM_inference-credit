#!/usr/bin/env python3
"""Generate a deterministic SPDX 2.3 package inventory for the pinned runtime image."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


CREATED = "2026-08-30T00:00:00Z"


def run(argv: list[str]) -> str:
    completed = subprocess.run(argv, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(f"command failed ({completed.returncode}): {argv!r}\n{completed.stderr}")
    return completed.stdout


def spdx_id(name: str, index: int) -> str:
    normalized = re.sub(r"[^A-Za-z0-9.-]", "-", name)
    return f"SPDXRef-Package-{index:05d}-{normalized}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    inspect = json.loads(run(["docker", "image", "inspect", args.image]))[0]
    image_id = inspect["Id"]
    architecture = inspect.get("Architecture", "unknown")
    inventory = run([
        "docker",
        "run",
        "--rm",
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--pids-limit=64",
        args.image,
        "dpkg-query",
        "-W",
        "-f=${binary:Package}\\t${Version}\\t${Architecture}\\n",
    ])
    rows = sorted(
        tuple(line.split("\t"))
        for line in inventory.splitlines()
        if line.strip()
    )
    packages = []
    relationships = []
    image_spdx_id = "SPDXRef-RuntimeImage"
    packages.append({
        "SPDXID": image_spdx_id,
        "name": "poi-alr-texlive-foundry-solc-poppler-runtime",
        "versionInfo": image_id,
        "downloadLocation": "NOASSERTION",
        "filesAnalyzed": False,
        "licenseConcluded": "NOASSERTION",
        "licenseDeclared": "NOASSERTION",
        "supplier": "NOASSERTION",
        "externalRefs": [{
            "referenceCategory": "PACKAGE-MANAGER",
            "referenceType": "purl",
            "referenceLocator": f"pkg:oci/poi-alr-texlive-foundry-solc-poppler@{image_id.removeprefix('sha256:')}?arch={architecture}",
        }],
    })
    for index, row in enumerate(rows, start=1):
        if len(row) != 3:
            raise SystemExit(f"unexpected dpkg-query row: {row!r}")
        name, version, architecture = row
        package_id = spdx_id(name, index)
        packages.append({
            "SPDXID": package_id,
            "name": name,
            "versionInfo": version,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "supplier": "NOASSERTION",
            "externalRefs": [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:deb/debian/{name}@{version}?arch={architecture}",
            }],
        })
        relationships.append({
            "spdxElementId": image_spdx_id,
            "relationshipType": "CONTAINS",
            "relatedSpdxElement": package_id,
        })

    binary_inventory = run([
        "docker", "run", "--rm", "--network=none", "--read-only",
        "--cap-drop=ALL", "--security-opt=no-new-privileges", "--pids-limit=64",
        args.image, "sha256sum", "/usr/local/bin/forge", "/usr/local/bin/solc",
    ])
    binary_hashes = {
        Path(path).name: checksum
        for checksum, path in (line.split(maxsplit=1) for line in binary_inventory.splitlines())
    }
    binary_packages = (
        (
            "foundry-forge", "1.5.1", binary_hashes.get("forge"),
            "pkg:github/foundry-rs/foundry@v1.5.1?arch=amd64",
            "https://ghcr.io/foundry-rs/foundry@sha256:7ec8952cc5322dce65091768e9efab8641ea9b54105f21fd71d4ae3dc3da05a8",
        ),
        (
            "solidity-compiler", "0.8.24+commit.e11b9ed9", binary_hashes.get("solc"),
            "pkg:generic/solc@0.8.24?arch=amd64",
            "https://ghcr.io/argotorg/solc@sha256:e56ef5e376ae846f06b919d7ca4ed0c271f7fb0900daa6c660d53451f5bfd9db",
        ),
    )
    for offset, (name, version, checksum, purl, location) in enumerate(binary_packages, start=len(rows) + 1):
        package_id = spdx_id(name, offset)
        package = {
            "SPDXID": package_id,
            "name": name,
            "versionInfo": version,
            "downloadLocation": location,
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "supplier": "NOASSERTION",
            "externalRefs": [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": purl,
            }],
        }
        if checksum:
            package["checksums"] = [{"algorithm": "SHA256", "checksumValue": checksum}]
        packages.append(package)
        relationships.append({
            "spdxElementId": image_spdx_id,
            "relationshipType": "CONTAINS",
            "relatedSpdxElement": package_id,
        })

    image_digest = image_id.removeprefix("sha256:")
    document = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "PoI ALR hermetic runtime SBOM",
        "documentNamespace": f"https://ztech.local/spdx/poi-alr-runtime/{image_digest}",
        "creationInfo": {
            "created": CREATED,
            "creators": ["Tool: poi-alr-generate-runtime-sbom-v1"],
            "licenseListVersion": "3.26",
        },
        "documentDescribes": [image_spdx_id],
        "packages": packages,
        "relationships": relationships,
        "annotations": [{
            "annotationDate": CREATED,
            "annotationType": "OTHER",
            "annotator": "Tool: poi-alr-generate-runtime-sbom-v1",
            "comment": "Deterministic dpkg package inventory plus SHA-256 identities for the copied Forge and Solidity binaries from a network-disabled, read-only run of the digest-pinned local image; licenses and file-level analysis were not inferred.",
        }],
    }
    payload = json.dumps(document, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "image_id": image_id,
        "package_count": len(rows) + len(binary_packages),
        "architecture": architecture,
        "binary_hashes": binary_hashes,
        "output_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
