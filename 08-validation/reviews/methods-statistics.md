# Producer-owned methods and statistics review

Status: `DRAFT — NOT INDEPENDENT`

## Scope

Reviewed the protocol, analysis plan, 729-state Cartesian design, seven exact-binding mutations, Python oracle/kernel separation, Solidity generated-vector checks, raw outputs, and same-owner replay.

## Findings

- **PASS — finite-population accounting.** All `3^6 = 729` base states and seven named mutations are accounted for; no p-value, sampling interval, exclusion, or imputation is used.
- **PASS — reported arithmetic.** `0/728`, `1/1`, `729/729`, `7/7`, and `736/736` reconcile with the preserved result tables.
- **PARTIAL — oracle independence.** The oracle is separately transcribed but remains producer-owned and may share specification errors with the kernel and generated Solidity expectations.
- **PARTIAL — mutation adequacy.** Seven single-defect bindings are useful mechanism-isolation tests but are not an exhaustive adversarial model; compound, malformed-type, ABI, replay-window, authority-transition, and integration failures remain incompletely tested.
- **FAIL — prospective protocol independence.** The protocol was not independently reviewed before the development run. A prospective unchanged rerun is required after external review.
- **FAIL — comparator and cost claim.** No fair baseline or numeric gas protocol was frozen, so no efficiency or bounded-gas advantage may be claimed.

## Statistical disposition

Inferential statistics are inapplicable to the enumerated finite model. Uncertainty concerns model completeness, implementation common-mode error, environmental transport, and adversarial coverage rather than sampling error. The paper appropriately reports exact denominators; it should not add conventional confidence intervals to imply external generality.

## Smallest adequate action

Freeze a comparator and gas measurement protocol; obtain independent methods sign-off; run the unchanged prospective evaluation; then have a different environment reproduce the central tables and hashes.
