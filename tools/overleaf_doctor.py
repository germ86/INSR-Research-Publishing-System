#!/usr/bin/env python3
"""Overleaf/local/CI diagnostics for the INSR publishing platform."""
from __future__ import annotations
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = {
    "root": ["main.tex"],
    "paper": [
        "examples/minimal-paper/main.tex",
        "examples/paper-demo.tex",
        "examples/minimal-english-paper.tex",
        "examples/position-paper/main.tex",
        "examples/arabic-rtl-paper.tex",
        "examples/multi-institution-consortium-paper.tex",
    ],
    "slides": [
        "examples/minimal-slides/main.tex",
        "examples/beamer-demo.tex",
        "examples/german-scientific-presentation.tex",
        "examples/hebrew-rtl-slides.tex",
    ],
    "manual": [
        "examples/clinical-manual/main.tex",
        "examples/manual-demo.tex",
        "doc/latex/insr/insr-latex-manual.tex",
    ],
    "protocol": [
        "examples/clinical-protocol/main.tex",
        "examples/rct-protocol/main.tex",
        "examples/clinical-trial-protocol.tex",
    ],
    "review": ["examples/systematic-review/main.tex"],
    "poster": ["examples/conference-poster/main.tex"],
    "documentation": [
        "examples/technical-documentation/main.tex",
        "examples/theme-gallery/main.tex",
        "examples/custom-theme/main.tex",
        "examples/custom-palette/main.tex",
        "examples/custom-theme-palette.tex",
        "examples/mixed-german-arabic-report.tex",
        "examples/grant-proposal/main.tex",
        "examples/thesis/main.tex",
    ],
}
REQUIRED_STY = [
    "insr-core", "insr-config", "insr-metadata", "insr-content", "insr-adapters",
    "insr-bibliography", "insr-localization", "insr-typography", "insr-colors",
    "insr-layout", "insr-boxes", "insr-accessibility", "insr-neuro", "insr-utils",
]
GENERATED_SUFFIXES = {
    ".aux", ".bcf", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out",
    ".run.xml", ".synctex.gz", ".toc", ".nav", ".snm", ".vrb", ".glo", ".gls",
    ".glg", ".acn", ".acr", ".alg",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def canonical_main_ok() -> bool:
    return read(ROOT / "main.tex").strip() == """\\documentclass{insr}

\\begin{document}

\\INSRMakeTitle
\\INSRRenderDocument

\\end{document}"""


def check_entry(path: Path) -> list[str]:
    problems: list[str] = []
    text = read(path)
    m = re.search(r"\\documentclass(?:\[([^]]*)\])?\{([^}]+)\}", text)
    if not m:
        problems.append("missing documentclass")
    elif m.group(2) != "insr":
        problems.append(f"non-v4 document class: {m.group(2)}")
    if "\\begin{document}" not in text or "\\end{document}" not in text:
        problems.append("incomplete document environment")
    if re.search(r"insr-(paper|beamer|manual)|INSRTitlePage", text):
        problems.append("deprecated public API/class reference")
    if "../../../references.bib" in text:
        problems.append("fragile relative bibliography path")
    return problems


def collect_problems() -> list[str]:
    problems: list[str] = []
    classes = [p for p in ROOT.rglob("insr.cls") if ".git" not in p.parts]
    if classes != [ROOT / "insr.cls"]:
        problems.append(f"expected exactly one root insr.cls, found: {[rel(p) for p in classes]}")
    if not canonical_main_ok():
        problems.append("main.tex is not the canonical public INSR entrypoint")
    if not (ROOT / "config/project-config.tex").is_file():
        problems.append("missing config/project-config.tex")
    for name in REQUIRED_STY:
        if not (ROOT / f"tex/latex/insr/{name}.sty").is_file():
            problems.append(f"missing package tex/latex/insr/{name}.sty")
    conflict_markers = ("<" * 7, "=" * 7, ">" * 7)
    for pattern in conflict_markers:
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.parts and path.suffix not in {".pdf", ".png", ".jpg"}:
                if pattern in read(path):
                    problems.append(f"conflict marker {pattern} in {rel(path)}")
    for path in ROOT.rglob("*"):
        if any(part.endswith(" ") for part in path.relative_to(ROOT).parts):
            problems.append(f"path component has trailing space: {rel(path)}")
    for group, files in ENTRYPOINTS.items():
        for item in files:
            path = ROOT / item
            if not path.is_file():
                problems.append(f"missing documented {group} entrypoint: {item}")
            else:
                problems.extend(f"{item}: {p}" for p in check_entry(path))
    for adapter in ["article", "paper", "report", "book", "slides", "poster", "letter", "manual"]:
        if not (ROOT / f"framework/adapters/{adapter}.tex").is_file():
            problems.append(f"missing adapter: {adapter}")
    return sorted(set(problems))


def list_entrypoints(args: argparse.Namespace) -> int:
    for group, files in ENTRYPOINTS.items():
        if not args.plain:
            print(f"[{group}]")
        for item in files:
            print(item if args.plain else item)
    return 0


def check_entrypoint(args: argparse.Namespace) -> int:
    path = (ROOT / args.path).resolve() if not Path(args.path).is_absolute() else Path(args.path)
    text = read(path)
    m = re.search(r"\\documentclass(?:\[([^]]*)\])?\{([^}]+)\}", text)
    opts = (m.group(1) or "") if m else ""
    print(f"file: {rel(path)}")
    print(f"documentclass: {m.group(2) if m else 'missing'}")
    print(f"document type: {re.search(r'document/type\s*=\s*([^,\]]+)', opts).group(1).strip() if re.search(r'document/type\s*=\s*([^,\]]+)', opts) else 'config/default'}")
    print("required class path: insr.cls")
    print("bibliography path: config/project-config.tex or document-local configuration")
    print("compile from repository root: yes")
    print(f"complete document environment: {'yes' if '\\begin{document}' in text and '\\end{document}' in text else 'no'}")
    problems = check_entry(path)
    if problems:
        print("problems:")
        for p in problems:
            print(f"- {p}")
        return 1
    print("problems: none")
    return 0


def check(_: argparse.Namespace) -> int:
    problems = collect_problems()
    if problems:
        print("Overleaf doctor found problems:")
        for p in problems:
            print(f"- {p}")
        return 1
    print("Overleaf doctor check passed")
    return 0


def report(_: argparse.Namespace) -> int:
    problems = collect_problems()
    cfg = read(ROOT / "config/project-config.tex") if (ROOT / "config/project-config.tex").exists() else ""
    def key(name: str) -> str:
        m = re.search(rf"{re.escape(name)}\s*=\s*([^,\n]+)", cfg)
        return m.group(1).strip().strip("{}") if m else "unknown"
    out = ROOT / "build/overleaf-report.md"
    out.parent.mkdir(exist_ok=True)
    lines = [
        "# INSR Overleaf Report", "", "- Recommended main document: `main.tex`", "- Compiler: LuaLaTeX", f"- Current document type: `{key('document/type')}`", f"- Theme: `{key('design/theme')}`", f"- Palette: `{key('design/palette')}`", f"- Typography: `{key('design/font')}`", "", "## Official entrypoints", "",
    ]
    for group, files in ENTRYPOINTS.items():
        lines.append(f"### {group}")
        lines.extend(f"- `{item}`" for item in files)
        lines.append("")
    lines.append("## Detected problems")
    lines.extend(f"- {p}" for p in problems) if problems else lines.append("- none")
    lines.extend(["", "## Recommended Overleaf steps", "", "1. Set Main document to `main.tex`.", "2. Set compiler to LuaLaTeX.", "3. Change output type only in `config/project-config.tex`."])
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(rel(out))
    return 0


def clean(_: argparse.Namespace) -> int:
    removed = 0
    for path in ROOT.rglob("*"):
        if path.is_file() and (path.suffix in GENERATED_SUFFIXES or path.name.endswith(".synctex.gz") or path.name.endswith(".run.xml") or path.name.endswith(".fdb_latexmk")):
            path.unlink()
            removed += 1
    print(f"removed {removed} generated files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check").set_defaults(func=check)
    le = sub.add_parser("list-entrypoints"); le.add_argument("--plain", action="store_true", help="print only paths for scripts"); le.set_defaults(func=list_entrypoints)
    ce = sub.add_parser("check-entrypoint"); ce.add_argument("path"); ce.set_defaults(func=check_entrypoint)
    sub.add_parser("generate-overleaf-report").set_defaults(func=report)
    sub.add_parser("clean").set_defaults(func=clean)
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
