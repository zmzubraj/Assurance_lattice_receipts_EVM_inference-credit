# Candidate Portfolio

Status: `DRAFT`; candidate ranking is provisional and cannot establish novelty or feasibility.

## Candidate families

| Candidate | Causal family | Predicted advantage | Fatal assumption | Current status |
| --- | --- | --- | --- | --- |
| A. Assurance-lattice receipt | typed conjunctive/meet gate | preserves failure reasons and prevents cross-dimension compensation before credit | dimensions and thresholds are complete and materially different from prior art | SELECTED_FOR_FALSIFICATION |
| B. Weighted assurance score | compensating scalar optimization | compact and tunable | a high score can hide a failed authority, freshness, or semantic dimension | FAILS_HARD_GATE |
| C. Monolithic ZK/TEE proof receipt | cryptographic execution attestation | strong execution binding under stated assumptions | does not by itself establish semantic disposition or evidence authority; cost/trust exceeds MPP scope | DEFERRED_BASELINE |
| D. Optimistic challenge receipt | dispute-driven enforcement | low common-path cost | unchallenged invalid or semantically unsupported evidence may activate credit | BASELINE_ONLY |
| E. Human multisignature approval | accountable manual gate | strong contextual judgment | slow, non-scalable, and not deterministic enough for the central mechanism | GOVERNANCE_FALLBACK |

## Mechanisms

Candidate A uses separately typed finite assurance dimensions, exact hash/scope/epoch bindings, and an all-required-dimensions rule. Candidate B aggregates dimensions into a scalar. Candidate C attempts to strengthen execution validity through cryptographic or hardware evidence. Candidate D defers verification until challenge. Candidate E moves the decision to accountable humans.

The families are causally distinct because the decisive authorization link is respectively conjunction, scalar compensation, cryptographic attestation, dispute response, or human judgment.

## Hard gates

Candidate A must satisfy all of these:

1. no failed or unknown required state activates credit;
2. replay, substitution, downgrade, stale authority, scope mismatch, and type confusion fail closed;
3. Python and Solidity decisions agree for the complete prespecified matrix;
4. failure reasons remain inspectable rather than reduced to one score;
5. local gas/state cost remains within the frozen threshold;
6. strongest-prior-art and independent challenge preserve a material differentiator.

Candidate B is rejected because compensation violates the target safety property. Candidates C-E remain comparison families and may be combined only if their evidence type remains explicit.

## Uncertainty

- The strongest conceptual predecessors already cover several individual mechanisms.
- The exact state lattice and threshold policy are not frozen.
- Exhaustive state count and mutation set are not designed.
- Solidity storage/event design and gas ceiling are not measured.
- Historical E3 authority-chain drift may restrict the case study.
- Independent novelty, methods, and human gates remain open.

## Decisive tests

| Order | Test | Pass condition | Fail condition | Decision enabled |
| --- | --- | --- | --- | --- |
| 1 | Feature-level predecessor reconciliation | at least one material enforced mechanism remains after comparison | no material difference | continue or reframe before implementation |
| 2 | Reference-model exhaustive matrix | zero false credit activations and explicit reason preservation | any failed/unknown state passes | retain or kill Candidate A |
| 3 | Adversarial mutation suite | every prespecified replay/substitution/downgrade mutation rejected | any attack activates credit | security viability |
| 4 | Python/Solidity differential test | exact decision and reason-code agreement | any semantic divergence | implementation validity |
| 5 | Foundry boundedness measurement | gas/state growth within frozen local threshold | threshold exceeded or unbounded path | minimum prototype viability |
| 6 | Independent scientific challenge | reviewer verifies bounded differentiator and design | novelty defeated or methods invalid | gate disposition only; never acceptance guarantee |

