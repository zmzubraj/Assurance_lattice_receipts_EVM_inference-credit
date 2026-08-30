# External Human and Scientific Gate Runbook

Case: `poi-alr-mpp-20260829T044029Z-b4e6442a-cd74f3`

Canonical case root: `/Users/rainbow/Documents/ZTech/Research/poi_alr_mpp_research_system`

Status at creation: `INTAKE`; the runbook is an execution plan, not evidence that any human or scientific gate has passed.

## 1. What the external humans must do

The case needs three accountable roles. They should be different people whenever practical.

1. **Registry administrator**
   - Creates the external trust root and registers reviewer public keys.
   - Confirms each real-world identity out of band, for example by institutional email, live meeting, or signed institutional statement.
   - Does not become a scientific reviewer merely by administering the registry.
2. **Independent scientific reviewer**
   - Has relevant blockchain/EVM/security-systems expertise.
   - Did not produce the artifact being reviewed and has no undisclosed conflict.
   - Reviews novelty, claim boundaries, protocol validity, technical interpretation, and manuscript claims.
3. **Independent methods/reproducibility reviewer**
   - Reviews design, leakage controls, estimands, uncertainty, analysis code, provenance, negative findings, and reproducibility.
4. **Accountable author/human approver**
   - Confirms authorship, disclosures, ethics/data authority, final rendered PDF, and the actual venue package.
   - Gives the final submission authorization. AI cannot perform this role.

The previous E3 evaluator is a fourth optional role with a narrow scope: the earlier E3/C3 external execution and attestation only. The evaluator's contact identity remains in the local confidential reuse ledger and is intentionally excluded from the GitHub repository. That prior authority does not establish ALR novelty, approve the new protocol, review the new manuscript, or authorize submission.

## 2. Non-negotiable independence and security rules

- A producer cannot independently verify the same scientific artifact.
- A registry administrator cannot silently self-appoint as a reviewer.
- Reviewer private keys stay outside the research case and are never sent to the author, AI, repository, or manuscript package.
- Only public keys are registered in the case.
- Every `VERIFIED` decision must follow substantive review; command execution alone is not review.
- If one person must cover two roles, record the overlap and conflict explicitly. It cannot be described as fully independent.
- The case remains fail-closed when a reviewer chooses `FAIL`, `PARTIAL`, `UNKNOWN`, or requests remediation.
- Previous E3 authorization may support only the historical E3 evidence to which it was bound.

## 3. One-time trust bootstrap

The registry administrator runs the following commands on a trusted machine. Replace every angle-bracket value before execution. Do not paste private-key contents into chat or the case.

```bash
CASE_ROOT=/Users/rainbow/Documents/ZTech/Research/poi_alr_mpp_research_system
ORCH_ROOT=/Users/rainbow/.codex/skills/orchestrate-top-journal-research
EXTERNAL_TRUST_ROOT=/Users/rainbow/Documents/POI_ALR_EXTERNAL_TRUST

mkdir -p "$EXTERNAL_TRUST_ROOT"
chmod 700 "$EXTERNAL_TRUST_ROOT"

ssh-keygen -t ed25519 -f "$EXTERNAL_TRUST_ROOT/registry-admin" -C "PoI ALR registry administrator"
ssh-keygen -t ed25519 -f "$EXTERNAL_TRUST_ROOT/scientific-reviewer" -C "PoI ALR independent scientific reviewer"
ssh-keygen -t ed25519 -f "$EXTERNAL_TRUST_ROOT/methods-reviewer" -C "PoI ALR methods and reproducibility reviewer"
ssh-keygen -t ed25519 -f "$EXTERNAL_TRUST_ROOT/accountable-author" -C "PoI ALR accountable author"

chmod 600 \
  "$EXTERNAL_TRUST_ROOT/registry-admin" \
  "$EXTERNAL_TRUST_ROOT/scientific-reviewer" \
  "$EXTERNAL_TRUST_ROOT/methods-reviewer" \
  "$EXTERNAL_TRUST_ROOT/accountable-author"

ssh-keygen -lf "$EXTERNAL_TRUST_ROOT/registry-admin.pub"
ssh-keygen -lf "$EXTERNAL_TRUST_ROOT/scientific-reviewer.pub"
ssh-keygen -lf "$EXTERNAL_TRUST_ROOT/methods-reviewer.pub"
ssh-keygen -lf "$EXTERNAL_TRUST_ROOT/accountable-author.pub"
```

The administrator records the four fingerprints and identity-binding method in a dated, signed offline note. Then bootstrap the case registry:

```bash
python3 "$ORCH_ROOT/scripts/manage_verifier_identity.py" bootstrap-trust \
  "$CASE_ROOT" \
  --registry-admin-key-id poi-alr-registry-admin-001 \
  --registry-admin-public-key "$EXTERNAL_TRUST_ROOT/registry-admin.pub" \
  --registry-signing-key "$EXTERNAL_TRUST_ROOT/registry-admin"
```

Register the three accountable identities. The identity strings must be real, stable, and already verified out of band.

```bash
SCIENTIFIC_ID='<REAL_NAME_AND_VERIFIED_INSTITUTIONAL_ID>'
METHODS_ID='<REAL_NAME_AND_VERIFIED_INSTITUTIONAL_ID>'
AUTHOR_ID='<REAL_ACCOUNTABLE_AUTHOR_NAME_AND_ID>'

python3 "$ORCH_ROOT/scripts/manage_verifier_identity.py" register \
  "$CASE_ROOT" \
  --registry-id poi-alr-scientific-reviewer-001 \
  --verifier-identity "$SCIENTIFIC_ID" \
  --verifier-type INDEPENDENT_REVIEWER \
  --signing-key-id poi-alr-scientific-key-001 \
  --authority-tier SCIENTIFIC_DOMAIN_REVIEW \
  --public-key "$EXTERNAL_TRUST_ROOT/scientific-reviewer.pub" \
  --registry-signing-key "$EXTERNAL_TRUST_ROOT/registry-admin"

python3 "$ORCH_ROOT/scripts/manage_verifier_identity.py" register \
  "$CASE_ROOT" \
  --registry-id poi-alr-methods-reviewer-001 \
  --verifier-identity "$METHODS_ID" \
  --verifier-type INDEPENDENT_REVIEWER \
  --signing-key-id poi-alr-methods-key-001 \
  --authority-tier METHODS_REPRODUCIBILITY_REVIEW \
  --public-key "$EXTERNAL_TRUST_ROOT/methods-reviewer.pub" \
  --registry-signing-key "$EXTERNAL_TRUST_ROOT/registry-admin"

python3 "$ORCH_ROOT/scripts/manage_verifier_identity.py" register \
  "$CASE_ROOT" \
  --registry-id poi-alr-accountable-author-001 \
  --verifier-identity "$AUTHOR_ID" \
  --verifier-type ACCOUNTABLE_HUMAN \
  --signing-key-id poi-alr-author-key-001 \
  --authority-tier ACCOUNTABLE_AUTHOR_AND_SUBMISSION_AUTHORITY \
  --public-key "$EXTERNAL_TRUST_ROOT/accountable-author.pub" \
  --registry-signing-key "$EXTERNAL_TRUST_ROOT/registry-admin"

python3 "$ORCH_ROOT/scripts/manage_verifier_identity.py" list "$CASE_ROOT"
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
```

Stop if identity binding is uncertain, a key fingerprint differs, the registry signature fails, or strict validation fails.

## 4. Review packet and review method

For every gate, the producer gives the reviewer:

- the canonical case path and run ID;
- the exact artifact revisions and SHA-256 values from `artifact-registry.csv`;
- the upstream evidence files named in each artifact's `consumes` field;
- the reviewer checklist for that phase;
- a blank findings record containing `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, or justified `N/A` per question;
- conflicts, access limits, and requested remediation;
- the exact signing command only after the reviewer has completed the review.

The reviewer must inspect content, not merely check file existence or hashes. A hash proves which revision was reviewed; it does not prove scientific validity.

For the reproducibility slice, the reviewer first verifies the transferred minimum
bundle, extracts it into a newly created reviewer-controlled directory, and runs the
frozen candidate from that extracted copy. The fixed timestamp is part of the frozen
hash contract:

```bash
BUNDLE=/ABSOLUTE/PATH/poi-alr-mpp-minimum-artifact-bundle-v1.tar.gz
VERIFY=/ABSOLUTE/PATH/verify_minimum_artifact_bundle.py
REVIEW_ROOT=/ABSOLUTE/REVIEWER_CONTROLLED/poi-alr-review
REPRO_OUTPUT=/ABSOLUTE/REVIEWER_CONTROLLED/poi-alr-reproduction

python3 "$VERIFY" "$BUNDLE"
mkdir -p "$REVIEW_ROOT" "$REPRO_OUTPUT"
tar -xzf "$BUNDLE" -C "$REVIEW_ROOT"

python3 "$REVIEW_ROOT/implementation/python/external_reproduction_candidate.py" \
  --case-root "$REVIEW_ROOT" \
  --output-dir "$REPRO_OUTPUT" \
  --generated-at 2026-08-29T05:00:00Z
```

The emitted report is candidate evidence only. The reviewer must hash it, document
the environment and deviations, inspect the Python and Foundry logs, and sign a
substantive reproducibility finding before it can support an external gate. A
stronger exact container replay additionally requires the content-addressed runtime
image or a reviewer-controlled rebuild from the included Dockerfile and lock; the
current derived image is local-only, so this dependency must not be silently waived.

After the exact image is available, execute the bundle-contained driver:

```bash
HERMETIC_OUTPUT=/ABSOLUTE/REVIEWER_CONTROLLED/poi-alr-hermetic-output

python3 "$REVIEW_ROOT/09-submission/hermetic-runtime/run_external_hermetic_replay.py" \
  --case-root "$REVIEW_ROOT" \
  --output-dir "$HERMETIC_OUTPUT"
```

Stop if any frozen input hash, image identity, command return code, Foundry count,
figure status, or PDF hash fails. Preserve `external-hermetic-replay-report.json`
and all command logs. A passing report remains candidate evidence until the methods
reviewer signs the exact report hash and substantive finding.

## 5. Reusable signing command

Use this template only after the named reviewer has approved the exact current revision. The reviewer must control and invoke their own private key.

```bash
python3 "$ORCH_ROOT/scripts/record_artifact.py" "$CASE_ROOT" \
  --path '<CASE_RELATIVE_ARTIFACT_PATH>' \
  --status VERIFIED \
  --owner '<ARTIFACT_OWNER_FROM_REGISTRY>' \
  --produced-by '<PRODUCER_ID_FROM_REGISTRY>' \
  --evidence-ids '<EVIDENCE_IDS_FROM_REGISTRY>' \
  --verified-by '<REGISTERED_REVIEWER_ID>' \
  --verification-id '<UNIQUE_PHASE_AND_ARTIFACT_REVIEW_ID>' \
  --verifier-identity '<EXACT_REGISTERED_IDENTITY_STRING>' \
  --verifier-type INDEPENDENT_REVIEWER \
  --verification-method '<WHAT_WAS_CHECKED_AND_WHICH_CHECKLIST_WAS_USED>' \
  --independence-mode INDEPENDENT \
  --independence-basis '<NO_PRODUCTION_ROLE; CONFLICTS DISCLOSED; IDENTITY BINDING METHOD>' \
  --notes '<PASS BOUNDARY, QUALIFICATIONS, AND RESIDUAL RISKS>' \
  --signing-key '<REVIEWER_PRIVATE_KEY_PATH_OUTSIDE_CASE>'
```

For final accountable-author actions, change `--verifier-type` to `ACCOUNTABLE_HUMAN`, use the registered author identity, and describe the accountability basis. Do not label that action as independent scientific review.

## 6. Phase-by-phase human work and command plan

### Gate A — INTAKE

Scientific reviewer actions:

Use the prefilled hash-bound kit at
`08-validation/external-gate-kit/`. Copy it to a reviewer-controlled writable
directory, complete the declaration and all four findings, and run
`validate_intake_review.py` as described in its `README.md`. A validator `PASS`
establishes mechanical completeness only; it does not replace the substantive
review or registered-key signatures below.

1. Compare `intake-original.md` with the user-confirmed intake.
2. Confirm `intake.json` is lossless normalization.
3. Check that `program-charter.md` narrows claims to an evidence-bound computational prototype.
4. Check `study-profile.json`, including study type, ethics category, jurisdiction basis, evidence standard, and reporting route.
5. Confirm the ambiguous admission/loan phrase is quarantined and does not create a lending or eligibility claim.
6. Sign the four required INTAKE artifacts separately with unique verification IDs.

After all four are independently `VERIFIED`:

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict

python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision PROCEED \
  --owner root-integration-owner \
  --evidence 00-governance/intake-original.md \
  --evidence 00-governance/intake.json \
  --evidence 00-governance/program-charter.md \
  --evidence 00-governance/study-profile.json
```

### Gate B — NOVELTY_AUDIT

External human actions:

1. Scientific reviewer checks the frozen novelty claim specification and causal bottleneck.
2. A differently owned challenger reruns high-yield paper/preprint/patent/standard/dataset/benchmark searches, known-item recovery, and citation chaining.
3. The challenger writes `independent-search-challenge.md`; the producer reconciles it into `novelty-matrix.csv` without hiding defeating evidence.
4. Scientific reviewer verifies the final search coverage, evidence ledger, challenge, novelty matrix, citation audit, and claim boundary.
5. If novelty is defeated or unresolved, select `REFRAME`, `NOVELTY_UNRESOLVED`, or `STOP`; do not sign `NOVELTY_SURVIVES` for schedule convenience.

After every required novelty artifact is independently verified:

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision NOVELTY_SURVIVES \
  --owner root-integration-owner \
  --evidence 01-novelty/novelty-matrix.csv \
  --evidence 01-novelty/independent-search-challenge.md \
  --evidence 01-novelty/citation-audit.md
```

### Gate C — FEASIBILITY_GATE

Methods reviewer actions:

1. Check that the minimum experiment can answer the narrowed question with existing authorized data.
2. Verify the V0-V5 maturity ceiling, failure envelope, data/resource constraints, progression criteria, and stop rules.
3. Ensure prior E3 results remain negative evidence and are not relabeled as ALR validation.
4. Choose only `GO`, `PILOT_FIRST`, `REDESIGN`, `BLOCKED`, `RESUME`, or `STOP`.
5. If `PILOT_FIRST`, independently verify both `pilot-plan.md` and `pilot-results.md` before a later `GO`.

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision GO \
  --owner root-integration-owner \
  --evidence 02-feasibility/solution-viability-case.md \
  --evidence 02-feasibility/feasibility-report.md \
  --evidence 02-feasibility/risk-register.csv \
  --evidence 02-feasibility/progression-criteria.csv
```

### Gate D — STUDY_DESIGN

Methods reviewer actions:

1. Review the frozen protocol before confirmatory interpretation.
2. Verify endpoints, baselines, controls, leakage prevention, sample-size or precision rationale, exclusions, stopping rules, multiplicity, sensitivity analyses, and negative-result handling.
3. Confirm exploratory and confirmatory analyses are separated.
4. Sign `protocol.md`, `analysis-plan.md`, `power-or-precision.md`, and `preregistration-and-deviations.md` only if adequate.

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision DESIGN_APPROVED \
  --owner root-integration-owner \
  --evidence 03-design/protocol.md \
  --evidence 03-design/analysis-plan.md \
  --evidence 03-design/power-or-precision.md \
  --evidence 03-design/preregistration-and-deviations.md
```

### Gate E — AUTHORIZED_EXECUTION

Accountable author and methods reviewer actions:

1. Accountable author confirms legal/ethical authority to use every dataset and artifact listed in `provenance-manifest.csv`.
2. Methods reviewer checks evidence-origin, scope, maturity, hash, no-reuse/leakage controls, and deviations.
3. Exclude or quarantine any item whose authorization or provenance is uncertain.
4. Sign `provenance-manifest.csv` and `evidence-status.csv` with the appropriate accountable and independent events.
5. Execute only the frozen, authorized protocol.

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision EXECUTION_COMPLETE \
  --owner root-integration-owner \
  --evidence 04-data/provenance-manifest.csv \
  --evidence 04-data/evidence-status.csv
```

### Gate F — ANALYSIS

Methods/reproducibility reviewer actions:

1. Replay the authorized analysis from the frozen provenance manifest.
2. Check denominators, seeds, exclusions, effect sizes, uncertainty, assumptions, robustness, boundary conditions, and all negative findings.
3. Verify no post-hoc analysis is presented as confirmatory.
4. Review the external-validation disposition: evidence if generality is claimed, otherwise a justified signed `N/A` and narrowed claims.
5. Sign required results, reproducibility, and editable table artifacts only after successful review.

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision EVIDENCE_READY \
  --owner root-integration-owner \
  --evidence 05-analysis/results/primary-results.csv \
  --evidence 05-analysis/results/robustness-and-boundaries.csv \
  --evidence 05-analysis/results/negative-findings.csv \
  --evidence 05-analysis/reproducibility-report.md
```

### Gate G — MANUSCRIPT

Scientific and methods reviewer actions:

1. Trace every central sentence-level claim through `claim-evidence-matrix.csv` and `claim-graph.json`.
2. Ensure claims do not exceed the weakest authorized evidence maturity.
3. Verify citations against sources; inspect diagrams, figures, editable tables, captions, units, uncertainty, and accessibility.
4. Check that the title and abstract disclose the actual evidence scope and negative outcomes.
5. Sign the manuscript, claim-evidence matrix, source manifest, and required visual artifacts.

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision MANUSCRIPT_READY \
  --owner root-integration-owner \
  --evidence 07-manuscript/manuscript.md \
  --evidence 07-manuscript/claim-evidence-matrix.csv \
  --evidence 07-manuscript/source-manifest.json \
  --evidence 06-visuals/visual-ledger.csv
```

### Gate H — ADVERSARIAL_QA

At least one qualified reviewer who did not write the manuscript performs a hostile but fair review. Prefer separate novelty/domain and methods reviewers.

1. Complete all review files under `08-validation/reviews/`.
2. Complete the postdoctoral-standard audit and every killer-question ledger row.
3. Record every remediation and rerun only the affected gate after material changes.
4. Any critical `FAIL` or `UNKNOWN` blocks advancement. Critical `PARTIAL` limits the readiness stage.

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision CRITICAL_GATES_PASS \
  --owner root-integration-owner \
  --evidence 08-validation/postdoctoral-standards-audit.md \
  --evidence 08-validation/killer-question-ledger.csv \
  --evidence 08-validation/remediation-log.csv
```

### Gate I — SUBMISSION_QA

Scientific reviewer and accountable author actions:

1. Verify the target venue and official rules again on the recorded date.
2. Refresh novelty through the submission cutoff.
3. Inspect the hermetic-build manifest, logs, PDF metadata, embedded fonts, references, anonymity, tables/figures, page limits, and rendered pages.
4. Verify the reporting checklist with manuscript locations.
5. Complete the submission-gate ledger and acceptance-readiness record. Use `NOT ESTIMABLE` for acceptance probability unless calibrated target-matched data exist.

```bash
python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
python3 "$ORCH_ROOT/scripts/advance_research_case.py" "$CASE_ROOT" \
  --decision SUBMISSION_PACKAGE_READY \
  --owner root-integration-owner \
  --evidence 09-submission/submission-audit.md \
  --evidence 09-submission/submission-gate-ledger.csv \
  --evidence 09-submission/novelty-refresh.md \
  --evidence 09-submission/acceptance-readiness.md \
  --evidence 09-submission/pdf-qa.json \
  --evidence 09-submission/package-manifest.json
```

### Gate J — HUMAN_APPROVAL

The accountable author must personally:

1. Read the final PDF and supplements.
2. Confirm authorship and CRediT roles, conflicts, funding, ethics/data authority, AI-use disclosure, data/code availability, and all venue declarations.
3. Confirm that the portal preview matches the approved PDF and metadata.
4. Record the decision, venue, manuscript version, PDF hash, date/time, limitations, and explicit authorization in `09-submission/human-approval.md`.
5. Sign that artifact using the registered accountable-author key.
6. Perform the final portal submission personally or under an institutionally authorized process. A prepared package or clicked button is not proof of submission; retain the venue receipt.

Accountable-author signing template:

```bash
python3 "$ORCH_ROOT/scripts/record_artifact.py" "$CASE_ROOT" \
  --path 09-submission/human-approval.md \
  --status VERIFIED \
  --owner '<ACCOUNTABLE_AUTHOR_OWNER_ID>' \
  --produced-by '<ACCOUNTABLE_AUTHOR_OWNER_ID>' \
  --evidence-ids '<FINAL_SUBMISSION_EVIDENCE_IDS>' \
  --verified-by poi-alr-accountable-author-001 \
  --verification-id HUMAN-APPROVAL-001 \
  --verifier-identity "$AUTHOR_ID" \
  --verifier-type ACCOUNTABLE_HUMAN \
  --verification-method 'Personal review of final PDF, declarations, metadata, portal preview, and package hash' \
  --independence-mode ACCOUNTABLE_AUTHORITY \
  --independence-basis 'Named accountable author with verified identity and submission authority' \
  --notes 'Explicit approval applies only to the recorded venue, manuscript revision, and package hash' \
  --signing-key "$EXTERNAL_TRUST_ROOT/accountable-author"

python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
```

`HUMAN_APPROVAL` is terminal human authority. Automation must not fabricate a final advancement or submission receipt.

## 7. Previous E3 authority and data reuse

Permitted reuse:

- The earlier E3 raw/result bundle as historical external evidence, subject to exact manifest and hash validation.
- The signed E3 authority and result attestation as provenance for the E3-only evaluation scope.
- The reported negative outcome: E3/C3 support was not established under its stated threshold.

Prohibited reuse:

- Treating E3 authorization as authorization for the new ALR experiment.
- Treating the E3 evaluator as an ALR novelty, protocol, manuscript, or submission reviewer without a new registered role and a new substantive review.
- Reissuing a new document and describing it as the historical pre-execution authorization.
- Hiding the observed authority-record hash drift.

The currently observed E3 authority record does not match the historical declared hash in its verifier record. Before manuscript citation of that chain, the E3 evaluator must either:

1. restore and verify the exact historical signed inputs; or
2. issue a new, dated reconciliation statement that explicitly identifies the drift, the exact files reviewed, and the limited conclusion that remains supportable.

Until then, the E3 chain is usable as a disclosed, qualified provenance record, not as a cleanly reverified new scientific gate.

## 8. Fastest legitimate reviewer schedule

- **Day 0:** registry administrator verifies identities, creates keys, bootstraps trust, and registers roles.
- **Day 0-1:** scientific reviewer closes INTAKE and reviews the frozen novelty claim specification.
- **Day 1-2:** independent search challenger completes novelty challenge; scientific reviewer reconciles the novelty gate.
- **Day 2:** methods reviewer closes feasibility and design, or issues `PILOT_FIRST`/`REDESIGN`.
- **After authorized execution:** methods reviewer replays analysis and verifies results.
- **Manuscript day:** scientific and methods reviewers perform claim-trace and visual/citation review.
- **Final day:** independent adversarial QA, venue/PDF QA, then accountable-author approval and portal submission.

This is an optimistic critical path, not a guarantee. A failed scientific gate extends the schedule rather than lowering the threshold.

## 9. Gate completion evidence

A gate is complete only when all of the following are present:

- required artifacts have substantive content and current hashes;
- artifact-specific semantic checks pass;
- required artifacts are signed by registered, appropriately independent humans;
- `check_research_case.py --strict` passes;
- the phase-specific decision is recorded by `advance_research_case.py`;
- limitations, conflicts, and negative findings remain visible;
- no later upstream change has made the verification stale.

Anything less remains `DRAFT`, `PARTIAL`, `BLOCKED`, `UNKNOWN`, or `STALE` as appropriate.
