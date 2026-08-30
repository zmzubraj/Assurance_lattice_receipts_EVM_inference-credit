# ALR Development Pilot Results

Status: `DRAFT — DEVELOPMENT_EXPLORATORY`; no phase promotion performed.

## Protocol adherence

The development run enumerated all 729 prespecified base states and all seven
single-fault binding mutations. A separate oracle transcription generated expected
reason codes, which were embedded into the Solidity test. Python unit tests,
Python evaluation, and Foundry tests all returned zero. The protocol and analysis
plan had not been independently verified before execution, so this is not a
confirmatory run.

## Results

- Base false activations: 0/728.
- Eligible base activations: 1/1.
- Base eligibility and reason-code agreement: 729/729.
- Prespecified mutation rejection: 7/7.
- Python-generated vector versus Solidity agreement: 736/736.
- Python unit tests: 3 passed, 0 failed.
- Foundry tests: 2 passed, 0 failed.
- Independent replay: core base CSV, mutation CSV, and Python summary SHA-256
  values were byte-identical.

## Progression decision

`PILOT_FIRST REMAINS OPEN`. The technical development evidence meets the internal
functional thresholds but cannot yield `GO` until independent protocol/methods
verification, novelty challenge, authorization/provenance review, and an unchanged
prospective rerun are complete. The gas criterion is not assessable because the
baseline and threshold were not frozen.

## Deviations

- `DEV-000`: execution preceded independent protocol and methods verification.
- `DEV-001`: no prespecified numeric gas comparator or threshold existed.
- Foundry test gas is retained only as diagnostic execution metadata.

## Residual uncertainty

The finite model may omit assurance states or attack families; the mutation set is
not exhaustive; the prototype is local and synthetic; no field, production,
semantic-truth, decentralization, or novelty inference is supported. Independent
scientific review remains absent.

