#!/usr/bin/env python3
"""Deterministically estimate Frontiers main-body words from the local LaTeX source."""

from __future__ import annotations

import re
import sys
from pathlib import Path


START = r"\section{Introduction}"
END = r"\section*{Conflict of Interest Statement}"


def main() -> int:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "frontiers-manuscript.tex")
    text = source.read_text(encoding="utf-8")
    try:
        body = text[text.index(START) : text.index(END)]
    except ValueError as exc:
        raise SystemExit(f"required section boundary missing: {exc}") from exc

    body = re.sub(r"(?m)(?<!\\)%.*$", " ", body)
    body = re.sub(r"\\cite[pt]?\{[^{}]*\}", " ", body)
    body = re.sub(r"\\(?:ref|pageref|label)\{[^{}]*\}", " ", body)
    body = re.sub(r"\\(?:begin|end)\{[^{}]*\}", " ", body)
    body = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", body)
    body = body.replace("{", " ").replace("}", " ").replace("~", " ")
    body = re.sub(r"\$[^$]*\$", " ", body)
    words = re.findall(r"\b[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*\b", body)
    print(len(words))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
