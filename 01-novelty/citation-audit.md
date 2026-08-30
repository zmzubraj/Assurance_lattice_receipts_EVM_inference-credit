# Citation Audit

Status: `DRAFT`; the six-entry manuscript bibliography passes local structural and DOI-resolution checks, but novelty-search citation coverage and independent human verification remain incomplete.

## Metadata

- `PA001` was checked against the primary Frontiers article page and DOI `10.3389/frai.2026.1800407`.
- `PA002`, `PA003`, `PA004`, `PA005`, `PA006`, and `PA008` use primary arXiv identifiers.
- `PA009` and `PA010` were recovered from Crossref metadata with DOI identifiers; full-text verification remains pending.
- `PA007` uses the official repository identifier and must be pinned to a reviewed commit before citation.
- `PA012` uses public patent identifiers and is not a legal patentability opinion.
- `PA013` is a local external-result record, not a scholarly citation.

On 2026-08-30, the citation-management validator checked
`07-manuscript/latex/references.bib` against `07-manuscript/latex/main.tex`:

- six BibTeX entries and six unique manuscript citation keys;
- zero missing/unresolved keys;
- zero unused entries;
- zero duplicates;
- zero structural errors;
- the Frontiers DOI resolved successfully;
- the Frontiers article number `1800407` was added as the BibTeX `pages` value,
  after which the metadata-completeness warning was cleared.

This local validation checks metadata structure and linkage. It does not establish that
the six references are a sufficient novelty corpus or that every source interpretation
is correct.

The live metadata retrieval and response hashes are preserved in `prior-art-query-log.json` and `prior-art-raw-snapshots.json`. Metadata strings are treated as untrusted source content.

## Claim-source correspondence

| Evidence | Supported use | Prohibited broader use |
| --- | --- | --- |
| PA001 | deterministic governance, confidence cap, evidence-chain, fail-safe authorization overlap | proof that ALR is identical or defeated without feature-level review |
| PA002 | signed tool receipts and epistemic evidence classes | cryptographic inference correctness or blockchain settlement |
| PA003 | action/authority/outcome binding and nonce-freshness failure | production TPM guarantee; the reported attester is emulated |
| PA004 | evidence freshness as an automation authorization constraint | blockchain or inference implementation |
| PA006-PA010 | specific optimistic/verifiable/provenance overlap | full ALR composition equivalence without detailed comparison |
| PA013 | historical negative E3 result and scope boundary | positive semantic performance or clean current authority-chain closure |

## Corrections and retractions

The sole journal DOI in the six-entry manuscript bibliography resolved during the
2026-08-30 machine audit. The five arXiv records were checked against their primary
identifier pages during drafting, but a submission-time successor, correction,
withdrawal, and retraction refresh remains required. The broader novelty ledger still
contains records outside the six-entry manuscript bibliography that require full-text
and status verification. Any correction, withdrawal, or retraction reopens affected
claims.

## Access limits

- Several recent items are preprints and have not been independently peer reviewed.
- PA009 and PA010 currently rely on metadata-level recovery.
- Patent family/claims and standards full text remain incomplete.
- No proprietary citation database was accessed.
- Backward and forward citation edges remain unverified.
- The current BibTeX file is structurally validated, but it is not yet independently
  verified or venue-formatted.
