# Draft PDF build report

Status: **mechanically passed; not a submission build and not human-approved**

- Built: 2026-08-30 (Asia/Dhaka)
- Source: `main.tex` with `references.bib` and local source-first TikZ assets
- Command: `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`
- Engine/toolchain: pdfTeX 1.40.29, Latexmk 4.88, BibTeX 0.99e, TeX Live 2026
- Output: `main.pdf`, seven A4 pages
- SHA-256: `6700c8ffb31889bb15576178fdf3232ec730532f73333d13eaf9daa6821f1ac5`
- Log audit: no unresolved citations, unresolved references, multiply-defined labels, missing glyphs, overfull boxes, underfull boxes, or package/LaTeX warnings were found in the final log.
- Font audit: every listed Latin Modern Type 1 font is embedded and subset; Unicode mappings are present.
- Content smoke test: the draft banner, result denominators, limitations, and references are extractable from the PDF.
- AI rendered-page review: all seven pages were rasterized at 120 dpi and inspected; no clipping, overflow, unreadable labels, or missing visual elements were observed. Figures 2 and 3 occupy dedicated pages before the Discussion; this is accepted for the venue-neutral draft and must be reconsidered after venue selection.

This report is not the canonical hermetic submission build, does not satisfy accountable-human rendered-page review, and does not authorize submission.
