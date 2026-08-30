# ALR Technical Pilot Plan

Status: `DRAFT`; this is not an authorized execution record.

## Uncertainties

The pilot addresses four decision-relevant uncertainties:

1. whether the proposed non-compensating receipt semantics are internally coherent;
2. whether all ineligible states fail closed;
3. whether adversarial binding mutations remain rejected;
4. whether Python and Solidity can implement the same bounded semantics at locally measurable cost.

It does not estimate real-world effectiveness or publication acceptance.

## Protocol

1. Freeze six dimensions: execution, semantic, authority, provenance, freshness, and origin/scope.
2. Give each dimension exactly three base states: `PASS`, `FAIL`, and `UNKNOWN`.
3. Enumerate all `3^6 = 729` base states.
4. Define eligibility before execution: only the all-`PASS` state is eligible in the base matrix; exact binding checks are evaluated separately.
5. Record expected eligibility and canonical reason code for every state using a deterministic precedence rule that must itself be reviewed.
6. Apply prespecified mutation families: receipt replay, request/response hash substitution, authority-epoch staleness, evidence-origin relabeling, claim-scope mismatch, status downgrade/type confusion, and consumed-receipt reuse.
7. Execute the Python reference model as development evidence.
8. After design approval and authorized execution, run the same fixtures through Solidity/Foundry and compare decisions and reason codes.
9. Measure gas/state behavior against a frozen minimal baseline; do not set the numeric ceiling after seeing ALR measurements.
10. Preserve every failure and inconclusive outcome.

## Green criteria

- zero false activations across every ineligible state;
- all eligible states activate as specified;
- every prespecified mutation rejects;
- exact cross-runtime decision and reason-code agreement;
- bounded on-chain path and independently frozen gas criterion met;
- complete artifact and environment replay.

## Amber criteria

- state or mutation vocabulary is incomplete but no unsafe activation has been observed;
- only non-semantic serialization differences exist;
- bounded implementation exceeds the frozen gas criterion but can be simplified without changing the claim;
- E3 is excluded while the synthetic/local central result remains coherent.

Amber requires protocol amendment, invalidation of affected results, and a complete rerun. It is not a pass.

## Red criteria

- any ineligible state or adversarial mutation activates credit;
- Python and Solidity disagree semantically after one bounded repair cycle;
- the state space cannot represent the claimed assurance dimensions;
- on-chain logic is unbounded or the claim requires production assumptions outside scope;
- independent review finds no material differentiator.

Red triggers `REDESIGN` or `STOP` for the affected central claim.

## Stop rules

- Stop immediately on the first unsafe activation during development; diagnose before running more cases.
- Permit at most one design repair before refreezing the complete matrix; further semantic failures require redesign.
- Do not reuse pre-freeze pilot outcomes as confirmatory evidence without an explicit, independently approved reuse rule.
- Do not run live-network, mainnet, production, participant, or external-data tests under this plan.
- Do not advance from feasibility until the pilot plan and result are independently verified after a formal `PILOT_FIRST` disposition.

