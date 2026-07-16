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
        "examples/publication-minimal/main.tex",
        "examples/publication-journal-article/main.tex",
        "examples/publication-position-paper/main.tex",
        "examples/publication-blind-review/main.tex",
        "examples/publication-zenodo-preprint/main.tex",
        "examples/publication-multi-author/main.tex",
        "examples/publication-funded-research/main.tex",
        "examples/reference-publication/paper.tex",
    ],
    "slides": [
        "examples/minimal-slides/main.tex",
        "examples/beamer-demo.tex",
        "examples/german-scientific-presentation.tex",
        "examples/hebrew-rtl-slides.tex",
        "examples/reference-publication/slides.tex",
        "examples/reference-publication/handout.tex",
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
    "poster": ["examples/conference-poster/main.tex", "examples/reference-publication/poster.tex"],
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
    "insr-layout", "insr-page-style", "insr-boxes", "insr-accessibility", "insr-neuro", "insr-utils",
]
GENERATED_SUFFIXES = {
    ".aux", ".bcf", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out",
    ".run.xml", ".synctex.gz", ".toc", ".nav", ".snm", ".vrb", ".glo", ".gls",
    ".glg", ".acn", ".acr", ".alg",
}

TARGETS = {
    "position-paper": {"base": "scrartcl", "adapter": "paper", "profile": "position-paper", "source": "insr-position-paper"},
    "paper": {"base": "scrartcl", "adapter": "paper", "profile": "paper", "source": "insr-position-paper"},
    "journal-paper": {"base": "scrartcl", "adapter": "paper", "profile": "paper", "source": "insr-position-paper"},
    "slides": {"base": "beamer", "adapter": "slides", "profile": "slides", "source": "insr-position-paper"},
    "handout": {"base": "beamer", "adapter": "slides", "profile": "handout", "source": "insr-position-paper"},
    "poster": {"base": "beamer", "adapter": "poster", "profile": "poster", "source": "insr-position-paper"},
    "clinical-manual": {"base": "scrreprt", "adapter": "manual", "profile": "manual", "source": "insr-position-paper"},
    "technical-report": {"base": "scrreprt", "adapter": "report", "profile": "report", "source": "insr-position-paper"},
    "executive-brief": {"base": "scrartcl", "adapter": "paper", "profile": "paper", "source": "insr-position-paper"},
    "book": {"base": "scrbook", "adapter": "book", "profile": "book", "source": "insr-position-paper"},
    "thesis": {"base": "scrbook", "adapter": "thesis", "profile": "thesis", "source": "insr-position-paper"},
}

SUPPORTED_DOCUMENT_TYPES = {
    "article", "paper", "position-paper", "whitepaper", "report", "book", "monograph",
    "thesis", "slides", "handout", "poster", "letter", "grant", "protocol",
    "clinical-trial-protocol", "rct", "systematic-review", "narrative-review",
    "technical-documentation", "developer-documentation", "manual",
} | set(TARGETS)
VALID_THEMES = {p.stem for p in (ROOT / "themes").glob("*.tex")}
VALID_PALETTES = {p.stem for p in (ROOT / "palettes").glob("*.tex") if p.parent.name == "palettes"}
VALID_FONTS = {p.stem for p in (ROOT / "typography").glob("*.tex")}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def flattened_entrypoints() -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for files in ENTRYPOINTS.values():
        for item in files:
            if item not in seen:
                out.append(item)
                seen.add(item)
    return out


def parse_class_options(text: str) -> tuple[str | None, str]:
    match = re.search(r"\\documentclass(?:\[([^]]*)\])?\{([^}]+)\}", text, re.S)
    if not match:
        return None, ""
    return match.group(2), match.group(1) or ""


def option_value(options: str, key: str) -> str | None:
    match = re.search(rf"{re.escape(key)}\s*=\s*(\{{[^}}]*\}}|[^,\]]+)", options)
    if not match:
        return None
    return match.group(1).strip().strip("{}")


def palette_exists(name: str) -> bool:
    return name in VALID_PALETTES or (ROOT / f"palettes/{name}.tex").is_file()


def canonical_main_ok() -> bool:
    return read(ROOT / "main.tex").strip() == """\\documentclass{insr}

\\begin{document}

\\INSRMakeTitle
\\INSRRenderDocument

\\end{document}"""


def check_entry(path: Path) -> list[str]:
    problems: list[str] = []
    text = read(path)
    docclass, options = parse_class_options(text)
    if docclass is None:
        problems.append("missing documentclass")
    elif docclass != "insr":
        problems.append(f"non-v4 document class: {docclass}")
    if path.name != "main.tex" or path.parent != ROOT:
        if "config/load-project=false" not in options:
            problems.append("official example should set config/load-project=false")
        for key in ["metadata/title", "metadata/author", "metadata/institution"]:
            if option_value(options, key) is None:
                problems.append(f"official example missing {key}")
    if "\\begin{document}" not in text or "\\end{document}" not in text:
        problems.append("incomplete document environment")
    if re.search(r"insr-(paper|beamer|manual)|INSRTitlePage|INSRSetup", text):
        problems.append("deprecated public API/class reference")
    if "../../../references.bib" in text:
        problems.append("fragile relative bibliography path")
    doc_type = option_value(options, "document/type")
    if doc_type and doc_type not in SUPPORTED_DOCUMENT_TYPES:
        problems.append(f"unsupported document/type: {doc_type}")
    theme = option_value(options, "design/theme")
    if theme and theme not in VALID_THEMES:
        problems.append(f"invalid theme: {theme}")
    palette = option_value(options, "design/palette")
    if palette and not palette_exists(palette):
        problems.append(f"invalid palette: {palette}")
    font = option_value(options, "design/font")
    if font and font not in VALID_FONTS:
        problems.append(f"invalid typography preset: {font}")
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
            if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts and path.suffix not in {".pdf", ".png", ".jpg", ".pyc"}:
                if pattern in read(path):
                    problems.append(f"conflict marker {pattern} in {rel(path)}")
    for path in ROOT.rglob("*"):
        if any(part.endswith(" ") for part in path.relative_to(ROOT).parts):
            problems.append(f"path component has trailing space: {rel(path)}")
    flat = flattened_entrypoints()
    duplicates = sorted({item for item in flat if flat.count(item) > 1})
    for item in duplicates:
        problems.append(f"duplicate entrypoint: {item}")
    for group, files in ENTRYPOINTS.items():
        for item in files:
            path = ROOT / item
            if not path.is_file():
                problems.append(f"missing documented {group} entrypoint: {item}")
            else:
                problems.extend(f"{item}: {p}" for p in check_entry(path))
    manifest = ROOT / "content/manifest.tex"
    if manifest.is_file():
        manifest_text = read(manifest)
        for match in re.finditer(r"\\input\{([^}]+)\}", manifest_text):
            target = ROOT / match.group(1)
            if target.suffix == "":
                target = target.with_suffix(".tex")
            if not target.is_file():
                problems.append(f"manifest references missing file: {rel(target)}")
            elif not read(target).strip():
                problems.append(f"manifest references empty file: {rel(target)}")
    for doc_type in SUPPORTED_DOCUMENT_TYPES:
        if not (ROOT / f"profiles/documents/{doc_type}.profile.tex").is_file():
            problems.append(f"missing profile: {doc_type}")
    for adapter in ["article", "paper", "report", "book", "slides", "poster", "letter", "manual", "thesis"]:
        if not (ROOT / f"framework/adapters/{adapter}.tex").is_file():
            problems.append(f"missing adapter: {adapter}")
    return sorted(set(problems))


def list_entrypoints(args: argparse.Namespace) -> int:
    if args.plain:
        for item in flattened_entrypoints():
            print(item)
        return 0
    for group, files in ENTRYPOINTS.items():
        print(f"[{group}]")
        for item in files:
            print(item)
    return 0


def check_entrypoint(args: argparse.Namespace) -> int:
    path = (ROOT / args.path).resolve() if not Path(args.path).is_absolute() else Path(args.path)
    text = read(path)
    docclass, opts = parse_class_options(text)
    print(f"file: {rel(path)}")
    print(f"documentclass: {docclass if docclass else 'missing'}")
    print(f"document type: {option_value(opts, 'document/type') or 'config/default'}")
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



def check_target(args: argparse.Namespace) -> int:
    target = args.target
    if target not in TARGETS:
        print(f"unknown target: {target}")
        return 1
    info = TARGETS[target]
    problems: list[str] = []
    if not (ROOT / f"framework/adapters/{info['adapter']}.tex").is_file():
        problems.append(f"missing adapter: {info['adapter']}")
    if not (ROOT / f"profiles/documents/{info['profile']}.profile.tex").is_file():
        problems.append(f"missing profile: {info['profile']}")
    if not (ROOT / f"content/{info['source']}").is_dir():
        problems.append(f"missing content source: {info['source']}")
    config_pkg = read(ROOT / "tex/latex/insr/insr-config.sty")
    if f"{{ {target} }}" not in config_pkg and f"{{{target}}}" not in config_pkg:
        problems.append("target not mapped in insr-config.sty")
    if problems:
        print(f"target {target}: invalid")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"target {target}: base={info['base']} adapter={info['adapter']} profile={info['profile']} source={info['source']}")
    return 0


def check_source(args: argparse.Namespace) -> int:
    source = args.source
    directory = ROOT / "content" / source
    manifest = ROOT / "content/manifest.tex"
    problems: list[str] = []
    if not directory.is_dir():
        problems.append(f"missing content source: {source}")
    if not manifest.is_file():
        problems.append("missing content/manifest.tex")
    else:
        text = read(manifest)
        if f"content/{source}/" not in text:
            problems.append(f"manifest does not reference content/{source}/")
    if problems:
        print(f"source {source}: invalid")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"source {source}: ok")
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
    ct = sub.add_parser("check-target"); ct.add_argument("target"); ct.set_defaults(func=check_target)
    cs = sub.add_parser("check-source"); cs.add_argument("source"); cs.set_defaults(func=check_source)
    le = sub.add_parser("list-entrypoints"); le.add_argument("--plain", action="store_true", help="print only paths for scripts"); le.set_defaults(func=list_entrypoints)
    ce = sub.add_parser("check-entrypoint"); ce.add_argument("path"); ce.set_defaults(func=check_entrypoint)
    sub.add_parser("generate-overleaf-report").set_defaults(func=report)
    sub.add_parser("clean").set_defaults(func=clean)
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
