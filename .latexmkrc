# Submission-build safety contract: the canonical hermetic entrypoint must not
# permit either full or restricted shell escape.
$pdflatex = 'pdflatex -no-shell-escape %O %S';
