# Solution Viability Case

Status: `DRAFT`; solution viability remains `ASSERTED_ONLY` until independently reviewed evidence exists.

## Claim boundary

The proposed solution is a local computational prototype that implements one bounded property:

> Protocol credit is activated if and only if every required typed assurance dimension passes and all receipt bindings are exact.

The prototype may support claims about deterministic local behavior, adversarial mutation rejection, Python/Solidity semantic agreement, and local Foundry gas/state measurements. It cannot support claims about mainnet deployment, consensus safety, general LLM correctness, TEE or ZK security, production economics, real-world adoption, or field impact.

## Thresholds

1. **Safety:** zero credit activations among every prespecified ineligible assurance state.
2. **Completeness:** every prespecified eligible state activates credit.
3. **Binding integrity:** zero successful prespecified replay, substitution, downgrade, stale-authority, scope-mismatch, synthetic-origin laundering, or type-confusion mutations.
4. **Semantic agreement:** exact Python/Solidity agreement for eligibility and reason code over the frozen matrix.
5. **Determinism:** repeated local replay from identical canonical inputs yields identical decisions and artifact hashes where deterministic output is required.
6. **Boundedness:** no unbounded loop or state-dependent iteration in the on-chain decision path; a numeric gas threshold will be set only after a simple baseline contract and measurement protocol are frozen.
7. **Scientific:** the independently challenged novelty matrix retains a material enforced difference from the strongest predecessor.

The first four thresholds are non-compensating. A failure on one cannot be offset by performance elsewhere.

## Failure envelope

The solution is not viable for the central claim if any ineligible state activates credit, any required mutation bypasses the gate, Python and Solidity disagree, the on-chain path is not bounded, or independent prior-art review finds no material mechanism-level difference.

An inconclusive result occurs when the finite state vocabulary is shown to be incomplete, when reason-code equivalence is ambiguous, when provenance authorization cannot be established, or when gas comparison lacks a fair baseline. Inconclusive results do not count as pass.

The historical E3 negative case remains context only unless its authority-chain drift is reconciled. Excluding E3 does not invalidate the synthetic state-machine test, but it removes the real negative-case demonstration.

## Falsification sequence

1. Independent feature-level prior-art comparison before implementation expansion.
2. Python reference-model enumeration over six three-state assurance dimensions (`PASS`, `FAIL`, `UNKNOWN`): `3^6 = 729` base states.
3. Prespecified binding and authority mutation tests over representative eligible and ineligible states.
4. Solidity implementation and differential testing against the reference model.
5. Local Foundry gas/state measurement against a frozen simple baseline.
6. Reproducibility replay in a clean environment.
7. Independent methods and scientific review.

The cheapest decisive failure stops or reframes later work.

