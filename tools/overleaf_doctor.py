#!/usr/bin/env python3
"""Overleaf/local/CI diagnostics for the INSR publishing platform."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from insr_registry import load_registry, targets_from_registry, validate_registry

ROOT = Path(__file__).resolve().parents[1]
_REGISTRY = load_registry()
TARGETS = targets_from_registry()
SUPPORTED_DOCUMENT_TYPES = set(_REGISTRY["document_types"]) | set(_REGISTRY["aliases"])

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
    "poster": [
        "examples/conference-poster/main.tex",
        "examples/reference-publication/poster.tex",
    ],
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def flattened_entrypoints() -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for files in ENTRYPOINTS.values():
        for item in files:
            if item not in seen:
                result.append(item)
                seen.add(item)
    return result


def parse_class_options(text: str) -> tuple[str, list[str]]:
    match = re.search(r"\\documentclass(?:\[([^]]*)\])?\{([^}]+)\}", text)
    if not match:
        return "", []
    options = [item.strip() for item in (match.group(1) or "").split(",") if item.strip()]
    return match.group(2).strip(), options


def canonical_main_ok() -> bool:
    text = re.sub(r"%.*", "", read(ROOT / "main.tex"))
    tokens = re.findall(
        r"\\documentclass(?:\[[^]]*\])?\{insr\}|\\begin\{document\}|"
        r"\\INSRMakeTitle|\\INSRRenderDocument|\\end\{document\}",
        text,
    )
    return tokens == [
        "\\documentclass{insr}",
        "\\begin{document}",
        "\\INSRMakeTitle",
        "\\INSRRenderDocument",
        "\\end{document}",
    ]


def bootstrap_values() -> dict[str, str]:
    active = ROOT / "config/active-target.tex"
    if not active.is_file():
        return {}
    match = re.search(r"\\INSRBootstrap\s*\{(.*?)\}", read(active), re.S)
    if not match:
        return {}
    values: dict[str, str] = {}
    for part in match.group(1).split(","):
        key, separator, value = part.partition("=")
        if separator:
            values[key.strip()] = value.strip()
    return values



def active_selection(values: dict[str, str]) -> tuple[str, str, str]:
    preset = values.get("build/preset", "")
    if preset and preset in TARGETS:
        info = TARGETS[preset]
        return preset, info["type"], info["target"]
    return preset, values.get("document/type", ""), values.get("output/target", "")

def config_value(name: str) -> str:
    for relative in (
        "config/project-config.tex",
        "config/metadata-config.tex",
        "config/publication-config.tex",
        "config/layout-config.tex",
    ):
        path = ROOT / relative
        if not path.is_file():
            continue
        match = re.search(rf"{re.escape(name)}\s*=\s*(?:\{{([^}}]*)\}}|([^,\n]+))", read(path))
        if match:
            return (match.group(1) or match.group(2) or "").strip()
    return ""


def check_entry(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing entrypoint: {rel(path)}"]
    document_class, _ = parse_class_options(read(path))
    if not document_class:
        return [f"entrypoint has no document class: {rel(path)}"]
    return []


def collect_problems() -> list[str]:
    problems: list[str] = list(validate_registry())
    if not canonical_main_ok():
        problems.append("main.tex is not the canonical minimal INSR root document")

    active = bootstrap_values()
    preset, doc_type, output_target = active_selection(active)
    if "build/preset" not in active:
        problems.append("config/active-target.tex must set canonical build/preset")
    if "document/target" in active:
        problems.append("config/active-target.tex uses deprecated document/target")
    if "document/type" in active or "output/target" in active:
        problems.append("config/active-target.tex should use build/preset instead of document/type plus output/target")
    if preset and preset not in TARGETS:
        problems.append(f"unknown active build preset: {preset}")
    if doc_type and doc_type not in SUPPORTED_DOCUMENT_TYPES:
        problems.append(f"unknown active document type: {doc_type}")
    if output_target and output_target not in _REGISTRY["output_targets"]:
        problems.append(f"unknown active output target: {output_target}")

    for item in flattened_entrypoints():
        problems.extend(check_entry(ROOT / item))

    for name, info in _REGISTRY["document_types"].items():
        profile = ROOT / f"profiles/documents/{info['profile']}.profile.tex"
        manifest = ROOT / "content" / info["source"] / "manifest.tex"
        if not profile.is_file():
            problems.append(f"missing profile for {name}: {rel(profile)}")
        elif not read(profile).strip():
            problems.append(f"empty profile for {name}: {rel(profile)}")
        if not manifest.is_file():
            problems.append(f"missing source manifest for {name}: {rel(manifest)}")
        elif not read(manifest).strip():
            problems.append(f"empty source manifest for {name}: {rel(manifest)}")

    for name, info in _REGISTRY["output_targets"].items():
        adapter = ROOT / f"framework/adapters/{info['adapter']}.tex"
        if not adapter.is_file():
            problems.append(f"missing adapter for {name}: {rel(adapter)}")

    for manifest in (ROOT / "content").glob("*/manifest.tex"):
        for match in re.finditer(r"\\input\{([^}]+)\}", read(manifest)):
            target = ROOT / match.group(1)
            if target.suffix == "":
                target = target.with_suffix(".tex")
            if not target.is_file():
                problems.append(f"manifest references missing file: {rel(target)}")
            elif not read(target).strip():
                problems.append(f"manifest references empty file: {rel(target)}")

    full_path_request = re.compile(
        r"\\(?:RequirePackage|usepackage)\s*(?:\[[^]]*\])?\{(?:\./)?tex/latex/insr/"
    )
    for path in [ROOT / "insr.cls", *sorted((ROOT / "tex/latex/insr").glob("*.sty"))]:
        if path.is_file() and full_path_request.search(read(path)):
            problems.append(f"full-path package request causes package-name warnings: {rel(path)}")

    publication = ROOT / "config/publication-config.tex"
    if publication.is_file():
        text = read(publication)
        if "publication/date = {\\today}" not in text:
            problems.append("publication/date must default to \\today")
        if "publication/year = {\\number\\year}" not in text:
            problems.append("publication/year must default to \\number\\year")

    return sorted(set(problems))


def check_target(args: argparse.Namespace) -> int:
    name = args.target
    if name not in TARGETS:
        print(f"target {name}: invalid")
        print("- combination is not registered in config/target-registry.tex")
        return 1
    info = TARGETS[name]
    problems: list[str] = []
    profile = ROOT / f"profiles/documents/{info['profile']}.profile.tex"
    adapter = ROOT / f"framework/adapters/{info['adapter']}.tex"
    manifest = ROOT / "content" / info["source"] / "manifest.tex"
    for label, path in (("profile", profile), ("adapter", adapter), ("manifest", manifest)):
        if not path.is_file():
            problems.append(f"missing {label}: {rel(path)}")
    if problems:
        print(f"target {name}: invalid")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(
        f"target {name}: valid; document/type={info['type']} output/target={info['target']} "
        f"base={info['base']} adapter={info['adapter']} source={info['source']}"
    )
    return 0


def check_source(args: argparse.Namespace) -> int:
    directory = ROOT / "content" / args.source
    manifest = directory / "manifest.tex"
    problems: list[str] = []
    if not directory.is_dir():
        problems.append(f"missing content source: {args.source}")
    elif not manifest.is_file():
        problems.append(f"missing source manifest: {rel(manifest)}")
    elif not read(manifest).strip():
        problems.append(f"empty source manifest: {rel(manifest)}")
    if problems:
        print(f"source {args.source}: invalid")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"source {args.source}: valid")
    return 0


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
    problems = check_entry(path)
    if problems:
        for problem in problems:
            print(problem)
        return 1
    document_class, options = parse_class_options(read(path))
    print(f"file: {rel(path)}")
    print(f"class: {document_class}")
    print(f"options: {', '.join(options) if options else '(none)'}")
    return 0


def report(_: argparse.Namespace) -> int:
    out = ROOT / "build/overleaf-report.md"
    out.parent.mkdir(exist_ok=True)
    active = bootstrap_values()
    preset, doc_type, output_target = active_selection(active)
    problems = collect_problems()
    lines = [
        "# INSR Overleaf Report",
        "",
        "- Recommended main document: `main.tex`",
        "- Compiler: LuaLaTeX",
        f"- Current build preset: `{preset}`",
        f"- Current document type: `{doc_type}`",
        f"- Current output target: `{output_target}`",
        f"- Theme: `{config_value('design/theme')}`",
        f"- Palette: `{config_value('design/palette')}`",
        f"- Typography: `{config_value('design/font')}`",
        "",
        "## Registered combinations",
        "",
    ]
    for name, info in sorted(TARGETS.items()):
        lines.append(f"- `{name}`: `{info['type']}` -> `{info['target']}`")
    lines.extend(["", "## Detected problems", ""])
    lines.extend(f"- {problem}" for problem in problems) if problems else lines.append("- none")
    lines.extend(
        [
            "",
            "## Recommended Overleaf steps",
            "",
            "1. Set Main document to `main.tex`.",
            "2. Set compiler to LuaLaTeX.",
            "3. Change `build/preset` in `config/active-target.tex`; keep detail keys for advanced compatibility builds.",
            "4. Use Recompile from scratch after changing the base class or target.",
        ]
    )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(rel(out))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    target_parser = sub.add_parser("check-target")
    target_parser.add_argument("target")
    source_parser = sub.add_parser("check-source")
    source_parser.add_argument("source")
    list_parser = sub.add_parser("list-entrypoints")
    list_parser.add_argument("--plain", action="store_true")
    entry_parser = sub.add_parser("check-entrypoint")
    entry_parser.add_argument("path")
    sub.add_parser("report")
    args = parser.parse_args()

    if args.command == "check":
        problems = collect_problems()
        if problems:
            print("INSR project check failed")
            for problem in problems:
                print(f"- {problem}")
            return 1
        print("INSR project check passed")
        return 0
    if args.command == "check-target":
        return check_target(args)
    if args.command == "check-source":
        return check_source(args)
    if args.command == "list-entrypoints":
        return list_entrypoints(args)
    if args.command == "check-entrypoint":
        return check_entrypoint(args)
    if args.command == "report":
        return report(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
