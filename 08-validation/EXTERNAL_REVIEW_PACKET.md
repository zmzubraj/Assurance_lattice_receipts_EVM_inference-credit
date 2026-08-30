# PoI ALR MPP external review packet

Run ID: `poi-alr-mpp-20260829T044029Z-b4e6442a-cd74f3`

Canonical case: `/Users/rainbow/Documents/ZTech/Research/poi_alr_mpp_research_system`

Current phase: `INTAKE`

Current scientific disposition: novelty `UNRESOLVED`; solution viability `ASSERTED_ONLY`; acceptance readiness `NOT_ASSESSABLE`.

This file is a mechanical handoff index. It is not a review, verification event, or submission authorization. Reviewers must use the role separation, identity registration, signing, stop rules, and phase-order commands in `00-governance/EXTERNAL_HUMAN_SCIENTIFIC_GATE_RUNBOOK.md`.

## Start here

1. Read the external-gate runbook completely.
2. Verify the canonical case before reviewing:

   ```bash
   CASE_ROOT=/Users/rainbow/Documents/ZTech/Research/poi_alr_mpp_research_system
   ORCH_ROOT=/Users/rainbow/.codex/skills/orchestrate-top-journal-research
   python3 "$ORCH_ROOT/scripts/check_research_case.py" "$CASE_ROOT" --strict
   ```

3. Inspect `artifact-registry.csv`; confirm that every path, revision, and hash under review matches the registry.
4. Record question-level findings as `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, or justified `N/A`. Do not convert an unresolved novelty, independence, protocol, or provenance issue into a prose-only qualification.
5. Sign an artifact as `VERIFIED` only after substantive review of that exact revision. A producer or AI may not perform the independent scientific review.

The immediate serial next step is the four-artifact `INTAKE` gate. Use the
prefilled review kit at `08-validation/external-gate-kit/`; its validator checks
return completeness and exact revision/hash binding but deliberately cannot certify
reviewer identity, independence, or scientific judgment.

## Exact current review anchors

| Artifact | Status | Revision | SHA-256 |
|---|---:|---:|---|
| `00-governance/intake-original.md` | DRAFT | 1 | `b4e6442ac64366c6f04fa610276bd7870d02dda76b447b5435c128be778273bb` |
| `00-governance/intake.json` | DRAFT | 1 | `dc2ddb1024f077a09024a6a6b2f8a9174cb7671f53b3b516bee296a866ca8ce2` |
| `00-governance/program-charter.md` | DRAFT | 2 | `801d4057b9badb49c0d92f7ce97c58671713a2c9aa4882b2251a47c37dc7f0b9` |
| `00-governance/study-profile.json` | DRAFT | 2 | `65653add0ca0b90b4569d257a387897214be170a5c715efac00f7a4b1bd9f5da` |
| `01-novelty/novelty-claim-specification.md` | DRAFT | 1 | `0dfe967470e1b1b857e4c3487517cc60d318a4ece96bcb5236a8c3ce487ccee3` |
| `01-novelty/evidence-ledger.csv` | DRAFT | 1 | `f88e351b0962f79c0f32dd610e7df9cbed491a8a250f53c404ec85e6f2d224eb` |
| `01-novelty/novelty-matrix.csv` | DRAFT | 1 | `6d73b5f22bd49f8baeca4d6723ea4b1a33eb88d5d73c527e0e8a93485f757144` |
| `02-feasibility/pilot-results.md` | DRAFT | 1 | `fae780b928783adec199f485ebecdbfd9ea6599d3996f9233fb8e4f8475f5cf6` |
| `03-design/protocol.md` | DRAFT | 1 | `753c330aef2f22e6848583f40ef4a458775d52d01c2978833665c21299246ccf` |
| `03-design/analysis-plan.md` | DRAFT | 1 | `614a149685504e2a6b7c75fc512763c2bcb22d529177bed06913a065a4ea1303` |
| `04-data/provenance-manifest.csv` | DRAFT | 2 | `0a2b81aafc0c5d797e837ceceeb6eea0915f91012fa1395ff58a7adb443f0b47` |
| `05-analysis/results/primary-results.csv` | DRAFT | 1 | `0052070625346859d59ff21b39aab4981a3e11fdb767be1aed4d22ec38e26bf2` |
| `05-analysis/results/negative-findings.csv` | DRAFT | 1 | `b8dc6d9bd56fe94807f12fe329d8eda109828ba2891f86c6d543910611fc1b52` |
| `05-analysis/reproducibility-report.md` | DRAFT | 1 | `b5fc605f72f809ae1b40def66f742e1cbba776a349198354fdbd6f2a17d7199e` |
| `06-visuals/visual-ledger.csv` | DRAFT | 1 | `82f94fbff267b3ba4f69c1d35c4409e73f92d68c3b570d0ecddd0d1f95ceef0a` |
| `06-visuals/figures/figure-manifest.csv` | DRAFT | 3 | `eba15c8619e4fc82ff6180e9ba62f3ffb346f8a279fa9555e647683408aa751a` |
| `07-manuscript/manuscript.md` | DRAFT | 4 | `74af4435533049a60823fac91efbf717c12c1d0b08a250636822be7bd2ef10ff` |
| `07-manuscript/claim-evidence-matrix.csv` | DRAFT | 1 | `3bbb3a6257cf60349e53693af58a26ced836bf9b5e71bb25b8eeb3efc709afec` |
| `07-manuscript/source-manifest.json` | DRAFT | 1 | `8aab86b28fad86e9b3fe550ecd3f1a6c682a0244381aa2dc271ff98938df755e` |
| `07-manuscript/latex/main.pdf` | noncanonical draft build | — | `6700c8ffb31889bb15576178fdf3232ec730532f73333d13eaf9daa6821f1ac5` |
| `09-submission/hermetic-output/manuscript.pdf` | producer hermetic draft | — | `a6364b8b865afdcfbd5a885d8156bb9bd1a61d1f7a78934e42432ac1bda37400` |
| `09-submission/frontiers-in-blockchain-technology-code/frontiers-manuscript.pdf` | producer venue draft | — | `8822a98bc298c156e4c7aa3bed662ef0020c0d07ebe8a02826469509e4ca9c57` |

## External reproduction candidate command

The methods/reproducibility reviewer must run this on their own controlled environment and preserve the emitted `reproduction-report.json`. The producer-side test passed the frozen hashes, but it remains candidate-only and does not establish reviewer independence.

```bash
CASE_ROOT=/Users/rainbow/Documents/ZTech/Research/poi_alr_mpp_research_system
REPRO_OUTPUT=/ABSOLUTE/REVIEWER_CONTROLLED/OUTPUT/DIRECTORY

python3 "$CASE_ROOT/implementation/python/external_reproduction_candidate.py" \
  --case-root "$CASE_ROOT" \
  --output-dir "$REPRO_OUTPUT"
```

The reviewer must check that `status` is `PASS`, `candidate_only` is `true`, `independence_established` remains `false` until separately signed, and all three expected/observed result hashes match. The reviewer then records environment, identity, conflicts, deviations, and the exact report hash in the signed review. A local producer rerun cannot satisfy this gate.

## Required external return

The return must identify the reviewer, role, out-of-band identity-binding method, conflicts, exact reviewed revisions and hashes, checklist used, question-level findings, requested remediation, residual risks, and signed verification-event IDs. The independent novelty challenger must replace the producer-owned placeholder in `01-novelty/independent-search-challenge.md` with an independently produced search challenge before novelty can advance.

The accountable author must separately review authorship, affiliations, CRediT roles, funding, competing interests, ethics/data authority, AI-use disclosure, venue rules, rendered PDF, and portal preview. That final human approval cannot be inferred from scientific review or a successful build.

## Minimum artifact bundle for reviewer transfer

The producer-side transfer candidate is:

- archive: `09-submission/packages/poi-alr-mpp-minimum-artifact-bundle-v1.tar.gz`;
- expected contents: 344 manifested source files and 346 total archive members;
- authoritative local archive hash/report: `09-submission/packages/poi-alr-mpp-minimum-artifact-bundle-v1.report.json`;
- verifier: `09-submission/verify_minimum_artifact_bundle.py`;
- provisional venue PDF: `09-submission/frontiers-in-blockchain-technology-code/frontiers-manuscript.pdf`;
- venue source and local build limitations: `09-submission/frontiers-in-blockchain-technology-code/frontiers-manuscript.tex` and `LOCAL_BUILD_QA.md`.

After transferring the archive and report into a reviewer-controlled directory, run:

```bash
python3 /ABSOLUTE/PATH/verify_minimum_artifact_bundle.py \
  /ABSOLUTE/PATH/poi-alr-mpp-minimum-artifact-bundle-v1.tar.gz
```

The archive hash is intentionally not embedded in this packet because this packet is
itself an archive member. The reviewer must independently compare the observed
archive SHA-256 with the separately transferred adjacent report, retain the verifier
output, and record the exact archive hash in their signed return. Passing this
verifier establishes package integrity only; it does not establish reviewer identity,
independence, scientific correctness, novelty, or authorization to submit.

After the verifier passes, extract into a new reviewer-controlled directory and run
the candidate from that copy, not from the producer's working tree:

```bash
REVIEW_ROOT=/ABSOLUTE/REVIEWER_CONTROLLED/poi-alr-review
REPRO_OUTPUT=/ABSOLUTE/REVIEWER_CONTROLLED/poi-alr-reproduction

mkdir -p "$REVIEW_ROOT" "$REPRO_OUTPUT"
tar -xzf /ABSOLUTE/PATH/poi-alr-mpp-minimum-artifact-bundle-v1.tar.gz \
  -C "$REVIEW_ROOT"

python3 "$REVIEW_ROOT/implementation/python/external_reproduction_candidate.py" \
  --case-root "$REVIEW_ROOT" \
  --output-dir "$REPRO_OUTPUT" \
  --generated-at 2026-08-29T05:00:00Z

python3 - <<'PY'
import json
from pathlib import Path
p = Path('/ABSOLUTE/REVIEWER_CONTROLLED/poi-alr-reproduction/reproduction-report.json')
r = json.loads(p.read_text(encoding='utf-8'))
assert r['status'] == 'PASS'
assert r['returncode'] == 0
assert r['candidate_only'] is True
assert r['independence_established'] is False
assert all(v['expected'] == v['observed'] for v in r['result_checks'].values())
print('candidate replay checks: PASS')
PY
```

For the stronger container replay, the reviewer must first obtain the exact derived
image through an authorized transfer channel or rebuild it from the included
`09-submission/hermetic-runtime/Dockerfile` and `runtime.lock`. The required image
identity is
`poi-alr/texlive-foundry-poppler@sha256:b33763e92d1295e4d1fec00e613084624ce6b805c1fc882ee5a72778039c6ebc`;
the runtime-lock SHA-256 is
`8a180399f5dd0f4ae662da2f1f7daf7599f457e8551d9563653c9b23890abcbb`,
and the SPDX SBOM SHA-256 is
`55cd06de5387e426aac6cd0df7fe51b6f19c24a28746e4fc245bd5a0d9c91a65`.
The image is not currently public, so this stronger replay remains externally open.
After the exact image is present in the reviewer's Docker content store, run:

```bash
HERMETIC_OUTPUT=/ABSOLUTE/REVIEWER_CONTROLLED/poi-alr-hermetic-output

python3 "$REVIEW_ROOT/09-submission/hermetic-runtime/run_external_hermetic_replay.py" \
  --case-root "$REVIEW_ROOT" \
  --output-dir "$HERMETIC_OUTPUT"
```

The reviewer retains `external-hermetic-replay-report.json` and all eight pairs of
command logs, verifies that the report is `PASS`, confirms that it still says
`independence_established: false` and `phase_promotion: NOT_PERFORMED`, records the
environment and any deviations, and then issues a separately signed substantive
methods/reproducibility finding. The script cannot self-certify its operator.
