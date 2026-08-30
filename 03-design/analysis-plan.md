# ALR MPP Prespecified Analysis Plan

Status: `DRAFT — NOT INDEPENDENTLY VERIFIED`

## Analysis populations

- `BASE_ALL`: all 729 Cartesian-product assurance states.
- `BASE_INELIGIBLE`: the 728 states containing at least one `FAIL` or `UNKNOWN`.
- `BASE_ELIGIBLE`: the single all-PASS state.
- `MUTATION_SINGLE_FAULT`: the seven prespecified mutations of the all-PASS state.

No row may be excluded. Parser, runtime, or serialization failures remain rows with
an explicit error disposition and make the corresponding endpoint fail.

## Estimands

| Estimand | Numerator | Denominator | Green criterion |
|---|---:|---:|---:|
| Base false-activation rate | activated rows in `BASE_INELIGIBLE` | 728 | 0/728 |
| Eligible activation | activated rows in `BASE_ELIGIBLE` | 1 | 1/1 |
| Base reason agreement | exact expected reason matches | 729 | 729/729 |
| Mutation rejection | rejected mutation rows | 7 | 7/7 |
| Cross-runtime parity | exact decision and reason matches | all shared vectors | 100% |

These are exhaustive finite-population quantities, not estimates from a random
sample. P-values and post-hoc power are inapplicable. Counts and exact proportions
will be reported without pretending that sampling uncertainty exists.

## Primary analysis

The evaluator compares every observed eligibility and reason code with the
prespecified oracle. Primary results are exact counts and proportions for the five
estimands above. All endpoints must meet their thresholds; results are not averaged
into a compensating score.

## Sensitivity

1. Stratify ineligible states by the first failing reason code.
2. Report the count of states by number of non-PASS dimensions.
3. Hash raw outputs and rerun the complete evaluator; compare hashes byte for byte.
4. Preserve all compiler/test warnings and every failed or inconclusive row.
5. If gas is measured, report the exact toolchain, optimization settings, calls,
   median/min/max across deterministic fixtures, and the unfrozen-comparator limit.

These checks assess deterministic replay and boundary behavior; they are not
sampling-based sensitivity intervals.

## Multiplicity

There is no inferential multiplicity correction because the primary endpoints are
deterministic conformance gates. Every endpoint is non-compensating: one failure
fails the pilot.

## Missing data

Missing rows, duplicate case IDs, malformed output, or an absent runtime are
failures, not imputed observations.

## Exploratory boundary

Any run before independent verification of the protocol and analysis plan is
`DEVELOPMENT_EXPLORATORY`. After a verified protocol freeze, the exact same code and
fixtures may be rerun prospectively as confirmatory evidence; pre-freeze results
must not be silently relabeled.
