# Fresh bundle replay QA

Status: `PRODUCER-SIDE PASS — NOT INDEPENDENT — NO PHASE PROMOTION`

Checked: 2026-08-30.

## Transfer archive

- Archive: `poi-alr-mpp-minimum-artifact-bundle-v1.tar.gz`
- Archive SHA-256: `b54474ed37c0e9557051072b32c4f5ca4a8a8786a60a1a8dc423435d4df2c63e`
- Archive size: 2,787,884 bytes
- Manifested source files: 344
- Archive members: 346
- Archive verifier: `PASS`, zero errors
- Two consecutive archive builds were byte-identical.

## Fresh-directory evaluation replay

The final archive was extracted into a newly created producer-controlled temporary directory. `external_reproduction_candidate.py` copied the frozen inputs into its own fresh case, reran Python tests, the evaluation, and Foundry tests without network access, and compared the frozen result hashes.

- Candidate report: `producer-final-candidate-replay-v3/reproduction-report.json`
- Candidate report SHA-256: `f78bf96ef543f042f4864ba951c9af7075591baa4afb6e52cdc39578fd478076`
- Candidate status: `PASS`
- Return code: `0`
- Frozen result hashes matched: `base-results.csv`, `mutation-results.csv`, and `python-summary.json`
- Independence established: `false`
- Phase promotion: `NOT_PERFORMED`

An initial producer invocation supplied the wrong generated-at timestamp and was
correctly rejected by the frozen `python-summary.json` hash check despite a zero
process return from the underlying evaluation. The reported candidate is the clean
rerun with the prespecified `2026-08-29T05:00:00Z` timestamp. This operator deviation
and correction do not establish independence.

## Fresh-directory manuscript build

The Frontiers source was clean-built from the extracted final archive using the included build script.

- Rebuilt PDF SHA-256: `8822a98bc298c156e4c7aa3bed662ef0020c0d07ebe8a02826469509e4ca9c57`
- Canonical local PDF SHA-256: `8822a98bc298c156e4c7aa3bed662ef0020c0d07ebe8a02826469509e4ca9c57`
- Byte comparison: identical
- Build log: `producer-fresh-frontiers-build.log`
- Build-log SHA-256: `ad982fb5aeeaf9efbe3d45f2210e20b62b08e59729f42de5298e4bda6010bdb6`
- Controls: fixed source epoch, UTC timezone, C locale, and explicit no-shell-escape

## Fresh-directory hermetic replay

The extracted final archive was also passed to the canonical container builder in
a new producer-controlled temporary directory. The exact locally available
content-addressed runtime image was used with network disabled, read-only root and
case mounts, dropped capabilities, `no-new-privileges`, and a writable isolated
output mount.

- Declared container commands: 8
- Return codes: eight zeros
- Frozen Python base, mutation, summary, and Solidity-vector hashes: matched
- Exact Solidity 0.8.24 compilation: `PASS`
- Offline Foundry parity tests: 2 passed, 0 failed
- Figure replay: `PASS`
- PDF QA: compile `PASS`; fonts embedded; zero unresolved references; zero layout warnings
- Rebuilt venue-neutral PDF SHA-256: `a6364b8b865afdcfbd5a885d8156bb9bd1a61d1f7a78934e42432ac1bda37400`
- Canonical hermetic PDF byte comparison: identical
- Human rendered-page review: `REQUIRED`
- Independence established: `false`
- Phase promotion: `NOT_PERFORMED`

The final archive's bundled self-contained driver
`run_external_hermetic_replay.py` was also executed directly, without the
machine-global orchestration builder. It rejected an initial operator attempt when
the output directory was made non-empty by shell redirection, then passed from a
genuinely empty output directory.

- Driver report: `producer-final-hermetic-replay-v3/external-hermetic-replay-report.json`
- Driver-report SHA-256: `aa09339027a87610f3113579a8ce8d311f89435ef98b6ae0f0c344799c0db64d`
- Frozen source, runtime-lock, and SBOM hash checks: `PASS`
- Runtime image-ID check: `PASS`
- Driver commands: 8; return codes: eight zeros
- Driver Foundry parity: 2 passed, 0 failed
- Driver PDF compile and embedded-font checks: `PASS`
- Driver unresolved-reference and layout-warning counts: zero
- Driver PDF SHA-256: `a6364b8b865afdcfbd5a885d8156bb9bd1a61d1f7a78934e42432ac1bda37400`
- Driver independence established: `false`
- Driver phase promotion: `NOT_PERFORMED`

The derived image is not publicly distributed. This replay therefore establishes
archive-to-container repeatability on the producer's Docker content store, not an
independent clean-environment reproduction.

## External INTAKE kit QA

The final archive contains the four-artifact hash-bound kit under
`08-validation/external-gate-kit/`. From a fresh extraction, the blank template was
correctly rejected with return code 2. A mechanically completed test fixture then
returned `PASS` for four exact registry revisions and hashes while retaining
`independence_established: false`, `scientific_verification_established: false`, and
`phase_promotion: NOT_PERFORMED`. Test placeholder dispositions are not scientific
findings and were not copied into the canonical case.

## Assurance boundary

This establishes producer-side transfer integrity, same-toolchain PDF determinism,
archive-to-container repeatability, and reproducible development-output hashes. It
does not establish scientific validity, novelty, independent reproduction,
external validation, release authorization, accountable authorship, venue approval,
or submission authorization. Those gates remain fail-closed.
