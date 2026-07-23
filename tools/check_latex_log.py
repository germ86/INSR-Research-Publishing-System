#!/usr/bin/env python3
"""Fail CI on INSR-specific LaTeX warnings that indicate a real regression."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FORBIDDEN = {
    "generic LaTeX package error": re.compile(
        r"(?:^|\n)! Package [^\n]+ Error:"
    ),
    "generic LaTeX error": re.compile(
        r"(?:^|\n)! LaTeX Error:"
    ),
    "undefined control sequence": re.compile(
        r"(?:^|\n)! Undefined control sequence\."
    ),
    "emergency stop": re.compile(
        r"(?:^|\n)! Emergency stop\."
    ),
    "fatal TeX error": re.compile(
        r"Fatal error occurred"
    ),
    "missing output PDF": re.compile(
        r"No output PDF file produced"
    ),
    "missing glyphs in selected font": re.compile(
        r"Missing character: There is no "
    ),
    "INSR package requested through a repository path": re.compile(
        r"You have requested package [`'](?:\./)?tex/latex/insr/insr-[^`']+"
    ),
    "INSR class requested through a repository path": re.compile(
        r"You have requested document class [`'](?:\./)?tex/latex/insr/insr[^`']*"
    ),
    "microtype/kernel showhyphens incompatibility": re.compile(
        r"Command \\showhyphens\s+has changed"
    ),
    "duplicate PDF author metadata": re.compile(
        r"Package hyperref Warning: Option [`']pdfauthor[`'] has already been used"
    ),
    "missing German biblatex localisation": re.compile(
        r"Package biblatex Warning: No localisation for language [`']ngerman[`'] loaded"
    ),
    "unknown INSR document type": re.compile(
        r"Package insr Warning: Unknown document/type"
    ),
    "unknown INSR output target": re.compile(
        r"Package insr Warning: Unknown output/target"
    ),
}


def check(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing LaTeX log: {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    problems: list[str] = []
    for label, pattern in FORBIDDEN.items():
        match = pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            problems.append(f"{path}:{line}: {label}: {match.group(0)}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("logs", nargs="+", type=Path)
    args = parser.parse_args()

    problems: list[str] = []
    for log in args.logs:
        problems.extend(check(log))
    if problems:
        print("INSR LaTeX log validation failed")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("INSR LaTeX log validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
