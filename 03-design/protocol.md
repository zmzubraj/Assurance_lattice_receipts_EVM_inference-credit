# ALR MPP Computational Protocol

Status: `DRAFT — DEVELOPMENT EXECUTION ONLY`

Protocol ID: `ALR-MPP-PILOT-V1`

This protocol defines a finite, deterministic software experiment. It does not
authorize a confirmatory scientific claim, a live-chain deployment, new external
data collection, or phase promotion. Development execution may use only generated
test states and the already-authorized PoI source revision identified below.

## Research question

Can one typed receipt enforce a non-compensating credit-activation rule across six
independently failing assurance dimensions and seven exact-binding checks, with the
same eligibility decision and reason code in a Python reference kernel and a
Solidity implementation?

## Design

The experiment is an exhaustive three-level full factorial over six assurance
dimensions, followed by seven prespecified single-fault binding mutations. Run
order is irrelevant to the pure functions, but canonical enumeration order is
fixed for reproducible vector IDs and hashes.

## Population or system

The target system is the local Python ALR reference kernel and Solidity/EVM gate.
The finite target population for the base conformance test is all 729 states in the
frozen model; no people, natural populations, or production transactions are used.

## Frozen implementation source

- Source worktree: `/Users/rainbow/Documents/ZTech/Research/poi_mpp_workspace/.worktrees/poi-mpp-publication-artifacts`
- Source revision: `32ae7c8a18a37c163512d99cda78efe761e62638`
- Reuse rule: read-only conceptual and interface reuse; no unregistered runtime
  outputs are imported as evidence without a separate provenance row.
- New implementation location: this research system's `implementation/` tree.

## Experimental unit and factors

One base experimental unit is one complete assurance-state tuple. The six factors
are `execution`, `semantic`, `authority`, `provenance`, `freshness`, and
`origin_scope`. Each factor has three nominal levels: `PASS`, `FAIL`, and
`UNKNOWN`. The design is the complete Cartesian product, not a sample:

\[
N_{base}=3^6=729.
\]

The base matrix holds all seven exact-binding checks true and the receipt unused.
Seven additional single-fault mutation units are evaluated from the all-PASS base
state: consumed-receipt replay, request-hash substitution, response-hash
substitution, stale authority epoch, disallowed evidence origin, claim-scope
mismatch, and invalid type tag.

## Frozen decision rule

Credit activation is eligible if and only if every assurance dimension equals
`PASS`, the receipt is unused, and every exact-binding check succeeds. `FAIL` and
`UNKNOWN` are distinct recorded states but both fail closed.

When several defects coexist, the reason code is the first failing condition in
this fixed precedence:

1. assurance dimensions in the order listed above, with `FAIL` before `UNKNOWN`
   only as dictated by the observed state;
2. consumed receipt;
3. request hash mismatch;
4. response hash mismatch;
5. stale authority epoch;
6. disallowed evidence origin;
7. claim-scope mismatch;
8. invalid type tag;
9. `ELIGIBLE` when no defect exists.

## Controls

The positive control is the all-PASS state with all binding flags true. Negative
controls are all 728 non-all-PASS base states. The seven mutation fixtures isolate
one binding failure at a time while every assurance state remains PASS.

## Endpoints

Primary endpoints:

1. false activations among the 728 ineligible base states;
2. correct activation of the one eligible base state;
3. exact expected-versus-observed reason-code agreement for all 729 states;
4. rejection of all seven prespecified single-fault mutations;
5. exact Python-versus-Solidity decision and reason-code agreement under the same
   frozen rule.

Secondary endpoints:

- deterministic byte-identical replay hashes;
- Solidity compilation and exhaustive test status;
- descriptive gas measurements, if collected after the comparator is frozen.

## Bias and leakage

The expected vector is generated from a separate transcription of the frozen rule,
not by copying the reference kernel's observed decision. Python-generated expected
codes are then compiled into the Solidity test. Any code or protocol change makes
the result stale and requires complete regeneration and replay. Development results
cannot be relabeled as confirmatory after inspection.

## Stopping rules

Green requires 0/728 false activations, 1/1 true activation, 729/729 exact base
reason matches, 7/7 mutation rejections, and exact cross-runtime agreement. Any
unsafe activation is red and stops development immediately. A serialization-only
difference is amber, invalidates affected outputs, and permits one bounded repair
followed by a complete rerun. A second semantic repair requirement triggers
`REDESIGN` rather than repeated tuning.

## Ethics

This software-only protocol uses synthetic states and existing locally authorized
source material. It excludes human participants, personal data, live networks,
financial transactions, and external data transmission. Accountable authors must
still verify data rights, AI-use disclosure, conflicts, and venue requirements.

## Evidence labels and limits

Generated states are `SYNTHETIC_NON_EVIDENCE` inputs. Successful deterministic
execution may support only an internal software-correctness claim at up to
`V3 INTERNAL` after independent verification. It cannot establish novelty,
real-world reliability, decentralized security, production gas bounds, semantic
truthfulness, or publication readiness.
