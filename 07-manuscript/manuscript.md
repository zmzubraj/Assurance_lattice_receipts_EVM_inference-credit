# Title

**Assurance-Lattice Receipts for Fail-Closed EVM Inference Credit: A Reproducible Development Study**

Status: `DEVELOPMENT DRAFT — NOT SUBMISSION READY`

Authorship, author order, affiliations, declarations, venue, and accountable approval
remain unresolved human-controlled fields.

# Abstract

Blockchain-mediated AI inference needs more than evidence that computation occurred:
credit activation can also depend on semantic disposition, authority, provenance,
freshness, evidence origin, claim scope, and exact request-response bindings. We
study a typed assurance-lattice receipt (ALR) whose EVM credit gate uses a
non-compensating meet rule: every required condition must pass, while failure or
unknown status rejects activation with a deterministic reason code. The development
prototype comprises an independent Python oracle, a Python reference kernel, and a
Solidity 0.8.24 gate. We exhaustively executed all 729 states in a six-factor,
three-level model and seven prespecified binding mutations. The local development
run observed 0/728 false activations, 1/1 activation of the all-pass state, 729/729
base decision-and-reason matches, 7/7 mutation rejections, and 736/736
Python-generated-vector versus Solidity matches. A second same-owner local process
reproduced byte-identical core result artifacts. These findings establish only
development-level conformance to the frozen finite model. Novelty remains unresolved,
the protocol was not independently verified before execution, the attack set is not
exhaustive, no gas comparator was frozen, and no external or field validation was
performed. [claim:C003] [evidence:EV-ALR-BASE-001,EV-ALR-MUT-001,EV-ALR-PARITY-001,EV-ALR-REPLAY-001]

**Keywords:** blockchain assurance; EVM; verifiable AI inference; fail-closed
authorization; provenance; reproducible software evaluation

# Introduction

Optimistic and deterministic approaches already provide important mechanisms for
verifiable blockchain-based machine-learning inference, including fraud-proof-style
verification and public re-execution. [claim:C001] [evidence:PA006,PA008] Recent
work also shows that signed tool receipts can distinguish direct evidence from
inference, while attestation studies demonstrate that missing freshness checks can
permit replay despite otherwise valid evidence. [claim:C001]
[evidence:PA002,PA003] Governance-first architectures further show that deterministic
execution gates, evidence chains, and explicit assurance assumptions can be evaluated
as systems properties. [claim:C001] [evidence:PA001]

These predecessors defeat any claim that receipts, deterministic gates, optimistic
inference verification, provenance, or freshness are individually new. The narrower
hypothesis examined here is whether their decision-relevant dispositions can be kept
typed and independently failing through an EVM receipt-to-credit transition, rather
than collapsed into a compensating confidence score. This remains a novelty
hypothesis pending an independently owned search challenge and feature-level
reconciliation with the strongest prior art. [claim:C001]
[evidence:PA001,PA002,PA003,PA006,PA008]

The paper contributes a formal fail-closed rule, a minimal Python/Solidity artifact,
an exhaustive finite-state development evaluation, and a provenance-preserving
bundle of positive, negative, and inconclusive evidence. It does not claim a new
inference-proof primitive, semantic truth, production consensus safety, field impact,
or publication readiness. [claim:C003]
[evidence:EV-ALR-BASE-001,EV-ALR-MUT-001,EV-ALR-PARITY-001]

# Methods

## System and receipt rule

The ALR contains six assurance dimensions: execution, semantic, authority,
provenance, freshness, and origin/scope. Each takes `PASS`, `FAIL`, or `UNKNOWN`.
Seven exact predicates cover unused-receipt status, request and response hash
bindings, authority-epoch liveness, allowed evidence origin, claim-scope agreement,
and type-tag validity. Eligibility is the conjunction of all conditions. Figure 1
shows the architecture. [claim:C003] [evidence:EV-ALR-BASE-001]

## Algorithm

Algorithm 1 scans the six dimensions in a frozen order. The first non-pass state
returns its typed reason; exact bindings are then checked in a second frozen order.
Only the absence of any defect yields `ELIGIBLE`. This ordering makes diagnostics
deterministic but means reason-frequency counts reflect precedence rather than
dimension importance.

## Design and analysis

The base design is the complete Cartesian product `3^6 = 729`; it is a finite
population, not a statistical sample. The all-pass tuple is the only eligible base
state. Seven additional fixtures introduce one exact-binding defect at a time. An
oracle transcription generates expected vectors separately from the reference
kernel. Those vectors are compiled into the Solidity test, which checks every
decision and reason code. Missing or malformed rows count as failures; no rows are
excluded or imputed. P-values and observed power are inapplicable. [claim:C003]
[evidence:EV-ALR-BASE-001,EV-ALR-MUT-001]

## Implementation and reproducibility

The run used Python 3.14.6, Foundry 1.5.1-stable, and Solidity 0.8.24 on macOS 15.1
arm64. The runner captured argv, return codes, logs, and SHA-256 values without
requiring network access. A second same-owner process replayed the workflow with a
fixed protocol timestamp. [claim:C003]
[evidence:EV-ALR-PARITY-001,EV-ALR-REPLAY-001]

## Ethics and evidence boundary

The development evaluation used synthetic state fixtures and locally authorized
existing source material. It involved no participants, personal data, live networks,
or financial transactions. Institutional and venue-specific determinations remain
pending accountable-human review.

# Results

All 729 base states executed. The 728 ineligible states produced zero activations;
the all-pass state activated. Expected and observed base decisions and reasons agreed
for 729/729 states. All seven prespecified binding mutations rejected, and all 736
shared Python-generated vectors matched Solidity outputs. Three Python unit tests and
two Foundry tests passed. [claim:C003]
[evidence:EV-ALR-BASE-001,EV-ALR-MUT-001,EV-ALR-PARITY-001]

The same-owner replay reproduced identical SHA-256 values for the base CSV, mutation
CSV, and Python summary. Timing-bearing logs and run manifests differed as expected.
Figure 3 reports the first-reason distribution; its 486/162/54/18/6/2/1 pattern is a
consequence of the fixed precedence and must not be interpreted as empirical risk or
relative assurance importance. [claim:C003] [evidence:EV-ALR-REPLAY-001]

Several decisive outcomes remain negative or unresolved. The protocol was not
independently verified before execution; the numeric gas comparator is absent;
malformed-type parity is only partial; independent reproduction and field validation
were not performed; novelty remains unresolved; and the prior PoI semantic result
remains `NOT_SUPPORTED` with FAR 0.500 against a frozen 0.25 threshold. That prior
negative is retained as context and is not used as positive ALR evidence.

# Discussion

The development result supports a narrow software-conformance statement: within the
frozen six-dimension model and seven named binding mutations, the Python and Solidity
implementations obeyed the prespecified fail-closed rule. It does not establish that
the model captures every relevant assurance dimension or attack, that the semantic
input is correct, or that local conformance transports to production.

The strongest prior work makes novelty particularly uncertain. LATTICE overlaps
deterministic governance gates and auditable evidence chains; tool receipts overlap
typed evidence sources; freshness studies overlap replay-resistant evidence currency;
and opML/EigenAI overlap blockchain inference verification and enforcement.
[claim:C001] [evidence:PA001,PA002,PA003,PA006,PA008] The remaining candidate
difference is the specific typed, non-compensating EVM receipt-to-credit composition
and its exhaustive development contract. Whether that difference is material or
obvious is an external scientific question, not something the prototype can certify.

A prospective unchanged rerun after independent protocol review is the cheapest next
falsification step. A fair baseline must also be frozen before any bounded-gas claim.
External reproduction can then test whether the artifact and instructions are
sufficient outside the producer's environment.

# Conclusion

The ALR prototype provides exact development evidence for one deliberately narrow
claim: within the frozen finite model and seven named binding mutations, separately
implemented Python and Solidity decision paths conformed to the same fail-closed rule.
That result is useful as a falsifiable software contract, but it is not evidence of
semantic correctness, universal attack coverage, production safety, external
generality, or material novelty. The minimum responsible publication path is therefore
to preserve this claim ceiling while completing independent novelty and protocol
review, a prospective unchanged rerun, and external reproduction. [claim:C003]
[evidence:EV-ALR-BASE-001,EV-ALR-MUT-001,EV-ALR-PARITY-001,EV-ALR-REPLAY-001]

# Limitations

The protocol and analysis plan were reviewed only by the producing AI-assisted
workflow. The finite state model and mutation set may be incomplete. The same-owner
replay is not independent replication. Foundry test-call gas is not transaction or
production gas. The study did not evaluate semantic accuracy, decentralized
adversaries, mainnet conditions, privacy, TEEs, consensus safety, user outcomes, or
field impact. The literature search is bounded and awaits independent challenge,
patent/standard refresh, and full-text predecessor reconciliation. Authorship,
declarations, AI disclosure wording, venue rules, and final approval remain open.

# Data and code availability

The current development code, generated state tables, logs, manifests, figure source
data, Mermaid source, and manuscript source are preserved locally in the versioned
research-system folder. No public repository, archival DOI, license, or immutable
release has yet been approved; therefore public availability is `PENDING HUMAN
DECISION`, not promised.

# Declarations

- **Authorship and CRediT:** unresolved; accountable humans must determine eligibility,
  order, affiliations, and roles.
- **Funding:** unverified.
- **Competing interests:** unverified.
- **Ethics:** software-only development evaluation with no human participants or
  personal data; institutional applicability not independently determined.
- **AI use:** OpenAI Codex assisted with local code generation, execution, analysis,
  visual-source preparation, and drafting. Accountable human authors must verify all
  content and adapt disclosure to current venue policy.
- **Submission approval:** not granted.
