# ALR Development Reproducibility Report

Status: `DRAFT — SAME-OWNER LOCAL REPLAY ONLY`

## Data provenance

The base and mutation inputs are generated locally from `ALR-MPP-PILOT-V1` and are
labeled `SYNTHETIC_NON_EVIDENCE`. File-level provenance, authorization, processing,
ownership, and SHA-256 values are recorded in `04-data/provenance-manifest.csv`.
No live network, participant, personal, financial, or newly collected semantic data
were used.

## Code and environment

The reference kernel is `implementation/python/alr_mpp.py`; the EVM gate is
`implementation/solidity/src/ALRReceiptGate.sol`. The captured run used Python
3.14.6, Foundry 1.5.1-stable, and Solidity 0.8.24 on macOS 15.1 arm64. The runner
sets `PYTHONHASHSEED=0`, `TZ=UTC`, `LC_ALL=C`, and `LANG=C`; no network is required.
Exact argv and return codes are in each `run-manifest.json`.

## Replay

`alr-pilot-v1-run-001` and `alr-pilot-v1-replay-001` both completed three Python
tests and two Foundry tests without failure. Across the two processes, the base CSV
hash was `44affd48e...f7f250`, the mutation CSV hash was
`f1ef61762a...fb160`, and the Python summary hash was
`b504825552...1178d` in both runs. Timing-bearing logs and run manifests are not
expected to be byte-identical because paths and measured durations differ.

## Seeds

No pseudorandom generator is used. The base matrix follows deterministic Cartesian
product order, and mutation IDs and reason precedence are fixed by the protocol.

## Deviations

The run occurred before independent protocol/methods verification (`DEV-000`). A
numeric gas baseline and threshold were not frozen (`DEV-001`). Both deviations
remain open and prevent confirmatory or phase-promoting use.

## Limitations

This replay is same-owner and same-machine, not independent reproduction. The finite
model may omit states or attacks. The seven mutation families are not exhaustive.
Test-harness gas does not establish production cost. The results do not establish
novelty, semantic truth, field reliability, decentralized security, or publication
readiness.
