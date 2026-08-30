# PoI ALR external INTAKE gate kit

Status: `BLANK REVIEW KIT — NOT REVIEWED — NO PHASE PROMOTION`

This is the smallest external-human action needed next. It covers only the four
required `INTAKE` artifacts. It does not review novelty, methods, results, the
manuscript, or submission readiness.

## Reviewer sequence

1. Verify and extract the minimum artifact bundle using
   `08-validation/EXTERNAL_REVIEW_PACKET.md`.
2. Read `00-governance/EXTERNAL_HUMAN_SCIENTIFIC_GATE_RUNBOOK.md`, including the
   independence and trust-bootstrap rules.
3. Copy this directory to a reviewer-controlled writable location:

   ```bash
   REVIEW_ROOT=/ABSOLUTE/PATH/TO/EXTRACTED/CASE
   INTAKE_REVIEW_DIR=/ABSOLUTE/REVIEWER_CONTROLLED/poi-alr-intake-review

   cp -R "$REVIEW_ROOT/08-validation/external-gate-kit" "$INTAKE_REVIEW_DIR"
   ```

4. Complete `reviewer-declaration.md` with a real identity, binding method,
   qualifications, conflicts, access limits, date, and signature reference.
5. Review each exact revision in `intake-findings.csv`. Use only `PASS`,
   `PARTIAL`, `FAIL`, or `UNKNOWN`; all four artifacts are required, so `N/A` is
   not accepted. Give direct evidence, the consequence, and the smallest required
   action for every row.
6. Run the mechanical completeness validator:

   ```bash
   python3 "$REVIEW_ROOT/08-validation/external-gate-kit/validate_intake_review.py" \
     --case-root "$REVIEW_ROOT" \
     --review-dir "$INTAKE_REVIEW_DIR"
   ```

7. A validator `PASS` means only that the return is complete and hash-bound. It
   does not certify that the human judgment is correct or independent.
8. If and only if the reviewer substantively approves an artifact, use the
   registered-key signing command in the runbook for that exact path, revision,
   and hash. `PARTIAL`, `FAIL`, or `UNKNOWN` keeps the gate open.
9. Run the strict case checker and advance `INTAKE` only after all four required
   artifacts have valid independently signed `VERIFIED` events.

Never put reviewer private keys in this directory, the case, chat, or transfer
bundle.
