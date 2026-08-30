# Novelty Claim Specification

Status: `DRAFT`; current novelty disposition is `UNRESOLVED`.

## Claim

The candidate contribution is a **typed, hash-bound, freshness-aware EVM inference receipt whose credit activation is the meet of independently failing assurance dimensions**, evaluated by exhaustive state enumeration and adversarial mutation against a deterministic Python reference model and a Solidity implementation.

The claim is a composition-and-enforcement hypothesis. It is not a claim that any component primitive is new.

## Novelty axes

1. **Receipt semantics:** one receipt carries execution, semantic, authority, provenance, freshness, evidence-origin/scope, and exact-binding dispositions without collapsing them into a single confidence score.
2. **Non-compensating activation:** every required dimension must pass; a stronger dimension cannot offset a failed or unknown dimension.
3. **Lifecycle enforcement:** the same typed decision controls an explicit EVM `receipt -> credit` state transition rather than only producing an audit report.
4. **Evidence-laundering resistance:** synthetic, historical, unauthorized, stale, mismatched, or out-of-scope evidence remains distinguishable and fail-closed.
5. **Evaluation contract:** a prospectively frozen cross-product of assurance states and adversarial mutations is checked for Python/Solidity semantic agreement and bounded local settlement cost.

## Materiality threshold

The novelty hypothesis survives only if the strongest predecessor comparison finds all of the following:

- no predecessor recovered within the documented scope implements all required dimensions in one receipt;
- no predecessor recovered uses the same non-compensating eligibility rule for an EVM credit transition;
- the differentiator is executable and tested, not terminology alone;
- exhaustive and adversarial tests demonstrate at least one decision-relevant capability not already established by the strongest predecessor;
- an independently owned search challenge reaches the same bounded conclusion or narrows it further.

If only implementation packaging differs, the correct disposition is `REFRAME` or `STOP`, not `NOVELTY_SURVIVES`.

## Defeating evidence

- LATTICE already combines signed policy bundles, deterministic governance, fail-safe behavior, confidence capping, and auditable evidence chains for authorized autonomous AI operations.
- NabaOS uses signed tool receipts and epistemic source classes to prevent unsupported AI-agent claims.
- Action Evidence Packages under RATS bind an action, authorizing principal, and outcome to attestation evidence; recent work demonstrates that nonce freshness is a real replay boundary.
- Freshness-constrained audit authorization work treats stale evidence as a reason to keep automation under review.
- opML, CommitLLM, EigenAI, zkGPT, and related systems defeat any primitive-level claim over verifiable or optimistic AI inference.
- Smart-contract provenance systems and AI-audit provenance systems overlap artifact binding and audit-chain functions.

These sources force the claim to the narrower EVM receipt-to-credit composition. They may still defeat that claim after full-text comparison and independent challenge.

## Scope

- System: local Python reference kernel plus Solidity/EVM prototype.
- Input evidence: authorized existing PoI artifacts, prospectively generated synthetic assurance states, and bounded local execution measurements.
- Setting: local deterministic replay and Foundry; no mainnet, production, TEE, frontier-model, consensus-safety, or field-impact claim.
- Evidence maturity ceiling before execution: `V0 ASSERTED` to `V1 ANALYTIC`.
- Search cutoff: 2026-08-29, Asia/Dhaka.
- Novelty language: `NOVELTY_UNRESOLVED` until independent challenge, citation chaining, patent/standard refresh, and predecessor reconciliation are complete.

