# Coverage and Precision Rationale

Status: `DRAFT — NOT A POWER ANALYSIS`

## Target

The target is complete coverage of the frozen finite state model and exact
conformance, not detection of a stochastic effect.

## Assumptions

The central experiment enumerates the entire prespecified finite base state space:
six three-level assurance dimensions produce exactly 729 cases. Consequently, a
sample-size or statistical-power calculation is neither needed nor appropriate for
the base conformance claim. Coverage is complete only at 729/729 unique states.

## Calculation

The complete base count is `3^6 = 729`: one all-PASS eligible state and 728
ineligible states. Seven additional prespecified single-fault binding mutations are
evaluated separately.

## Decision

The decisive safety threshold is zero observed false activations across all 728
ineligible states. This establishes conformance only for the frozen state model and
implementation; it does not estimate an unknown field failure probability. The one
eligible state checks completeness of the activation rule but is not a population
estimate.

Seven adversarial mutations are mechanism tests selected from the frozen threat
model. They are not claimed to exhaust all attacks. Their result will be stated as
`x/7 prespecified mutation families rejected`, with residual attack classes listed
as limitations.

## Sensitivity

The development sensitivity checks are byte-identical replay of core artifacts,
reason-code stratification, and the seven mechanism-specific mutations. They do not
produce inferential confidence intervals.

Any future randomized fuzzing or live workload study requires a separate precision
or power rationale, a new protocol revision, and independent approval. Observed
power will not be computed after seeing results.
