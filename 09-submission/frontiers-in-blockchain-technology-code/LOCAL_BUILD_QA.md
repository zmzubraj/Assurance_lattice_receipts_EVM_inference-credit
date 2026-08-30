# Frontiers local draft build QA

Status: `PRODUCER-SIDE LOCAL DRAFT — NOT HERMETIC — NOT HUMAN APPROVED`

Checked: 2026-08-30.

## Build

- Source: `frontiers-manuscript.tex`
- Official publisher class: `FrontiersinHarvard.cls`, preserved byte-for-byte.
- Official publisher bibliography style: `Frontiers-Harvard.bst`, preserved byte-for-byte.
- Build command: `./build_frontiers_draft.sh`
- Engine: pdfLaTeX through latexmk; shell escape was not enabled.
- Main-text word-count estimate: 1,268 from `count_main_text.py`.
- PDF: 9 A4 pages; 213,786 bytes.
- PDF SHA-256: `39b988e75e00d691f7df9996c20c8b16ba62a345512eab0d9deecea1eba1fdcd`.

## Mechanical checks

- Six cited and six listed references; zero unresolved, missing, unused, duplicate, or DOI-validation warnings in the citation audit.
- No unresolved LaTeX citations, references, labels, or missing glyph messages in the final log.
- All PDF fonts are embedded and subset.
- Tables are editable LaTeX and positioned at the manuscript end.
- Three vector PDF figures are included at the manuscript end and retained as individual files.
- Single spacing and line numbers are enabled.

## Warning disposition

The official class emits an obsolete `xcolor` option warning, a microtype footnote-patch warning, a first-page header box warning, and recurring 2.0245-point vertical-box warnings. Rendered pages show no clipping or unreadable content. Two float-position suggestions and expected underfull vertical space occur on figure-only pages. These warnings are producer-reviewed but not waived by an accountable author or publisher.

## Rendered-page inspection

All nine pages were rendered at 110 dpi and visually inspected locally. The title, draft banner, line numbers, body text, Harvard references, two tables, three figures, captions, and page boundaries were legible. Figure 2's caption remains on its page. This is AI-assisted producer QA only; the required accountable-human final-size, accessibility, plagiarism, source-license, and portal-preview reviews remain open.

## Open blockers

This is not the canonical digest-pinned offline container build. Authors, affiliations, project URL, archival DOI/URI, license, exact AI model/version disclosure, conflicts, funding, ethics applicability, APC route, novelty, independent protocol review, external reproduction, and human submission approval remain unresolved.
