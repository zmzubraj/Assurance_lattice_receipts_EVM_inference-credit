# Hermetic runtime provenance and limits

Status: `PRODUCER-OWNED DRAFT — NOT INDEPENDENTLY VERIFIED`

## Runtime identity

- Platform: `linux/amd64` (executed under Docker Desktop emulation on the producer's arm64 host)
- Official base image: `texlive/texlive@sha256:bd551dda2195c6830bb714f731d74c4f71cda812178abae15a206fd68b5dbb7c`
- Base amd64 platform manifest: `texlive/texlive@sha256:51a1e21b72829eca6a195c37715505fc441585786ae52ebef0f20da334c2efa7`
- Official upstream project: <https://gitlab.com/islandoftex/images/texlive>
- Foundry image: `ghcr.io/foundry-rs/foundry@sha256:7ec8952cc5322dce65091768e9efab8641ea9b54105f21fd71d4ae3dc3da05a8`
- Foundry identity: `1.5.1-v1.5.1`, commit `b0a9dd9ceda36f63e2326ce530c10e6916f4b8a2`
- Solidity image: `ghcr.io/argotorg/solc@sha256:e56ef5e376ae846f06b919d7ca4ed0c271f7fb0900daa6c660d53451f5bfd9db`
- Solidity identity: `0.8.24+commit.e11b9ed9.Linux.g++`
- Derived local image: `poi-alr/texlive-foundry-poppler@sha256:b33763e92d1295e4d1fec00e613084624ce6b805c1fc882ee5a72778039c6ebc`
- Runtime lock SHA-256: `8a180399f5dd0f4ae662da2f1f7daf7599f457e8551d9563653c9b23890abcbb`
- SPDX SBOM SHA-256: `55cd06de5387e426aac6cd0df7fe51b6f19c24a28746e4fc245bd5a0d9c91a65`
- Deterministic epoch: `1787979600`

The derived image adds the version-locked Foundry, Solidity compiler, and Poppler
PDF inspection tools listed in `runtime.lock`. The Forge and solc binary SHA-256
identities are recorded there and in the generated SPDX inventory. It runs as
UID/GID `501:20`. The canonical builder invokes it with
network disabled, a read-only root filesystem and case mount, all capabilities
dropped, `no-new-privileges`, a PID limit, and only the output mount writable.
Manuscript and figure builds explicitly disable shell escape.

## Reproduction boundary

The derived image is content-addressed in the local Docker content store but is
not published to a public registry and is not included as a multi-gigabyte OCI
archive in the minimum transfer bundle. A new external environment must therefore
either receive the exact image through an authorized channel or rebuild it from
the included `Dockerfile` and `runtime.lock`. Rebuilding currently depends on the
pinned base manifest remaining retrievable and the exact Debian package versions
remaining available. Consequently, the present run proves repeatable producer-side
execution, not independent external reproduction.

Once the exact image is available, the bundle-contained fail-closed replay driver
requires a new or empty output directory outside the extracted case, verifies the
frozen source, lock, and SBOM hashes, runs all eight commands with the controls
above, and checks the exact manuscript PDF hash:

```bash
python3 09-submission/hermetic-runtime/run_external_hermetic_replay.py \
  --case-root /ABSOLUTE/PATH/TO/EXTRACTED/CASE \
  --output-dir /ABSOLUTE/PATH/TO/NEW/REVIEWER/OUTPUT
```

Its `PASS` is execution evidence only. The driver always records
`independence_established: false` and `phase_promotion: NOT_PERFORMED`; a qualified
reviewer must separately sign any external reproducibility disposition.

The hermetic analysis replay covers the Python unit tests, exhaustive finite-state
evaluation, frozen result-hash verification, offline compilation with exact Solidity
0.8.24, both Foundry vector-parity tests, figure generation, manuscript build, PDF
metadata, and font checks. Foundry test-call gas remains descriptive and cannot be
used as transaction, production, efficiency, or scalability evidence. Independent
external reproduction remains open even when this producer-controlled replay passes.

## SBOM note

Docker's bundled SBOM plugin could not run because its client API was older than
the daemon's supported minimum. No compatibility bypass was used. The included
`generate_runtime_sbom.py` instead queried installed Debian packages inside the
exact pinned, network-disabled, read-only image and emitted the deterministic
SPDX 2.3 document, including explicit Forge and solc binary identities. This is
producer-generated inventory evidence and requires
independent review before it can support a scientific or release gate.

The official Foundry image exposed attached SLSA and SBOM metadata through Docker
Buildx, but `gh attestation verify` returned HTTP 404 for both the platform and index
digests. Therefore this package records immutable digest, upstream source, commit,
labels, attached metadata inspection, and binary hashes, but does not claim that the
GitHub CLI independently verified the image signature or attestation.
