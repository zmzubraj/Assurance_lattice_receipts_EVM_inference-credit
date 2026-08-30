# Protocol Freeze and Deviation Ledger

Status: `DRAFT — PRE-FREEZE`

## Preregistered decisions

- Protocol ID: `ALR-MPP-PILOT-V1`
- Base design: complete `PASS/FAIL/UNKNOWN` Cartesian product for six dimensions
- Base case count: 729
- Binding-mutation count: 7
- Eligibility rule: conjunction/meet of all assurance and binding predicates
- Reason precedence: defined in `03-design/protocol.md`
- Primary endpoints and green thresholds: defined in
  `03-design/analysis-plan.md`
- Stop rule: first unsafe activation stops development pending diagnosis

## Timestamp

Candidate protocol timestamp: `2026-08-29T05:00:00Z`. This timestamp identifies the
development fixture revision; it is not an independent preregistration receipt.

## Current freeze status

`NOT FROZEN`. The producer may execute a development run, but only an independently
verified protocol revision can authorize a prospective confirmatory rerun. No
development result can self-freeze this plan.

## Deviations

| Deviation ID | Date | Status | Description | Impact | Required action |
|---|---|---|---|---|---|
| DEV-000 | 2026-08-29 | OPEN | Independent protocol and methods verification has not occurred. | All current runs remain development/exploratory. | Obtain signed independent review and rerun unchanged fixtures. |
| DEV-001 | 2026-08-29 | OPEN | Numeric gas comparator and threshold are not frozen. | Gas may be descriptive only and cannot satisfy the gas progression gate. | Freeze a fair baseline before confirmatory gas execution. |

## Impact

Because DEV-000 and DEV-001 remain open, the development run may inform redesign and
manuscript drafting but cannot promote the case, satisfy independent review, or
support a confirmatory gas claim.

New deviations must be appended; prior rows must not be deleted or rewritten.
