#!/usr/bin/env python3
"""Repository-wide structural validation for the INSR publishing platform."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from insr_registry import load_registry, targets_from_registry, validate_registry

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAMES = [
    "insr-core",
    "insr-config",
    "insr-metadata",
    "insr-utils",
    "insr-localization",
    "insr-bibliography",
    "insr-typography",
    "insr-colors",
    "insr-layout",
    "insr-frontmatter",
    "insr-page-style",
    "insr-boxes",
    "insr-accessibility",
    "insr-neuro",
    "insr-content",
    "insr-adapters",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8") if not isinstance(path, Path) else path.read_text(encoding="utf-8")


def expected_shim(package: str) -> str:
    return (
        "% INSR source-tree compatibility shim for Overleaf and local builds.\n"
        f"\\input{{tex/latex/insr/{package}.sty}}\n"
        "\\endinput\n"
    )


required = [
    ".github/workflows/latex.yml",
    "insr.cls",
    "main.tex",
    "config/active-target.tex",
    "config/project-config.tex",
    "config/target-registry.tex",
    "config/metadata-config.tex",
    "config/publication-config.tex",
    "config/layout-config.tex",
    "config/authors-config.tex",
    "references.bib",
    "content/manifest.tex",
    "themes/manifest.tex",
    "plugins/README.md",
    "tools/insr_registry.py",
    "tools/insr_build.py",
    "tools/overleaf_doctor.py",
    "tools/check_latex_log.py",
]
missing = [path for path in required if not (ROOT / path).is_file()]
if missing:
    fail(f"Missing required files: {missing}")

class_copies = [str(path.relative_to(ROOT)) for path in ROOT.rglob("insr.cls") if ".git" not in path.parts]
if class_copies != ["insr.cls"]:
    fail(f"Expected exactly one authoritative insr.cls, found: {class_copies}")

expected_main = "\\documentclass{insr}\n\n\\begin{document}\n\n\\INSRMakeTitle\n\\INSRRenderDocument\n\n\\end{document}\n"
if read("main.tex") != expected_main:
    fail("main.tex must remain the stable minimal INSR entry document")

active = read("config/active-target.tex")
for token in ("\\INSRBootstrap", "document/type", "output/target"):
    if token not in active:
        fail(f"Missing active target bootstrap token: {token}")
if "document/target" in active:
    fail("config/active-target.tex must not use deprecated document/target")

project = read("config/project-config.tex")
for token in (
    "\\INSRConfigure",
    "document/build-profile",
    "design/theme",
    "design/palette",
    "design/font",
    "content/source = auto",
):
    if token not in project:
        fail(f"Missing project configuration token: {token}")
if "document/target=position-paper" in project:
    fail("project fallback must use separate document/type and output/target keys")

publication = read("config/publication-config.tex")
if "publication/date = {\\today}" not in publication:
    fail("publication/date must default to \\today")
if "publication/year = {\\number\\year}" not in publication:
    fail("publication/year must default to \\number\\year")
if re.search(r"publication/date\s*=\s*\{\d{1,2}\s+[A-Za-z]+\s+\d{4}\}", publication):
    fail("publication/date must not be hard-coded")

registry_problems = validate_registry()
if registry_problems:
    fail("Invalid target registry: " + "; ".join(registry_problems))
registry = load_registry()
targets = targets_from_registry()

config_pkg = read("tex/latex/insr/insr-config.sty")
for token in (
    "\\INSRRegisterDocumentType",
    "\\INSRRegisterDocumentAlias",
    "\\INSRRegisterOutputTarget",
    "\\INSRRegisterCombination",
    "config/target-registry.tex",
    "unknown-output-target",
    "__insr_resolve_document_profile:",
    "__insr_resolve_output_target:",
):
    if token not in config_pkg:
        fail(f"insr-config.sty is missing registry/resolver token: {token}")
if "tl_gset_eq:NN \\g_insr_document_type_tl \\g_insr_output_target_tl" in config_pkg:
    fail("output/target must never be copied blindly into document/type")

for package in PACKAGE_NAMES:
    implementation = ROOT / f"tex/latex/insr/{package}.sty"
    shim = ROOT / f"{package}.sty"
    if not implementation.is_file():
        fail(f"Missing modular package: {implementation.relative_to(ROOT)}")
    if f"\\ProvidesPackage{{{package}}}" not in implementation.read_text(encoding="utf-8"):
        fail(f"Package name does not match request name in {implementation.relative_to(ROOT)}")
    if not shim.is_file():
        fail(f"Missing root compatibility shim: {shim.relative_to(ROOT)}")
    if shim.read_text(encoding="utf-8") != expected_shim(package):
        fail(f"Root compatibility shim is not canonical: {shim.relative_to(ROOT)}")

cls = read("insr.cls")
order = [
    "\\RequirePackage{expl3}",
    "\\RequirePackage{insr-core}",
    "\\RequirePackage{insr-config}",
    "\\RequirePackage{insr-metadata}",
    "config/project-config.tex",
    "\\ProcessOptions",
    "\\insr_resolve_document_type:",
    "\\LoadClass",
    "\\RequirePackage{insr-adapters}",
]
positions = [cls.find(token) for token in order]
if any(position < 0 for position in positions) or positions != sorted(positions):
    fail("insr.cls bootstrap order does not match the v4 architecture")
if len(cls.splitlines()) > 250:
    fail("insr.cls must remain a thin bootstrap class")
if "\\input@path" in cls:
    fail("insr.cls must not modify \\input@path; root shims provide deterministic source-tree package resolution")
if "local package path:" in cls:
    fail("insr.cls diagnostics must report the resolved short package name only")

full_path_request = re.compile(r"\\(?:RequirePackage|usepackage)\s*(?:\[[^]]*\])?\{(?:\./)?tex/latex/insr/")
for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if full_path_request.search(text):
        fail(f"Full-path package request would produce package-name warnings: {path.relative_to(ROOT)}")
    if re.search(r"(?m)^(<<<<<<<|=======|>>>>>>>)", text):
        fail(f"Merge conflict marker left in {path.relative_to(ROOT)}")

for name, info in registry["document_types"].items():
    profile = ROOT / f"profiles/documents/{info['profile']}.profile.tex"
    manifest = ROOT / f"content/{info['source']}/manifest.tex"
    if not profile.is_file():
        fail(f"Missing profile for {name}: {profile.relative_to(ROOT)}")
    if not profile.read_text(encoding="utf-8").strip():
        fail(f"Empty profile for {name}: {profile.relative_to(ROOT)}")
    if not manifest.is_file():
        fail(f"Missing content manifest for {name}: {manifest.relative_to(ROOT)}")
    if not manifest.read_text(encoding="utf-8").strip():
        fail(f"Empty content manifest for {name}: {manifest.relative_to(ROOT)}")

for name, info in registry["output_targets"].items():
    adapter = ROOT / f"framework/adapters/{info['adapter']}.tex"
    if not adapter.is_file():
        fail(f"Missing adapter for {name}: {adapter.relative_to(ROOT)}")
    adapter_text = adapter.read_text(encoding="utf-8")
    if "__insr_adapter_make_title" not in adapter_text and "input{framework/adapters/" not in adapter_text:
        fail(f"Adapter does not provide or delegate title rendering: {adapter.relative_to(ROOT)}")

content_raw_bibliographies = []
for search_root in (ROOT / "content", ROOT / "examples"):
    for content_root in search_root.rglob("*.tex"):
        if "content" not in content_root.parts:
            continue
        if "\\printbibliography" in content_root.read_text(encoding="utf-8"):
            content_raw_bibliographies.append(str(content_root.relative_to(ROOT)))
if content_raw_bibliographies:
    fail(r"Content files must use \INSRPrintBibliography, not raw \printbibliography: " + ", ".join(content_raw_bibliographies))

adapters_pkg = read("tex/latex/insr/insr-adapters.sty")
if "\\NewDocumentCommand \\INSRPrintBibliography { O{} } { \\__insr_adapter_bibliography:n {#1} }" not in adapters_pkg:
    fail(r"\INSRPrintBibliography must route through the public adapter bibliography path")
common_adapter = read("framework/adapters/common-document.tex")
for token in ("__insr_adapter_part:n", "__insr_adapter_section:n", "__insr_adapter_subsection:n", "__insr_adapter_subsubsection:n", "__insr_adapter_render_content_unit:", "__insr_adapter_bibliography:n", "__insr_print_bibliography:n"):
    if token not in common_adapter:
        fail(f"Common document adapter must provide {token}")
for adapter_name in ("paper", "article", "book", "report", "thesis", "manual"):
    adapter = ROOT / f"framework/adapters/{adapter_name}.tex"
    adapter_text = adapter.read_text(encoding="utf-8")
    if "input{framework/adapters/common-document.tex}" not in adapter_text:
        fail(f"Adapter must load common document adapter defaults: {adapter.relative_to(ROOT)}")
    if "__insr_adapter_bibliography:n" in adapter_text or "__insr_adapter_render_content_unit:" in adapter_text:
        fail(f"Adapter must not duplicate common bibliography/content rendering: {adapter.relative_to(ROOT)}")
poster_adapter = read("framework/adapters/poster.tex")
if "__insr_adapter_bibliography:n" not in poster_adapter or "Poster~References" not in poster_adapter or "__insr_adapter_render_content_unit:" not in poster_adapter:
    fail("Poster adapter must provide poster-specific bibliography and content frames")
slides_adapter = read("framework/adapters/slides.tex")
if "\\begin{frame}[allowframebreaks]{References}" not in slides_adapter or "\\__insr_print_bibliography:n {#1}" not in slides_adapter or "\\end{frame}" not in slides_adapter:
    fail("Slides bibliography adapter must render a clean allowframebreaks References frame")

for name, info in targets.items():
    if info["type"] not in registry["document_types"]:
        fail(f"Combination {name} has unknown document type")
    if info["target"] not in registry["output_targets"]:
        fail(f"Combination {name} has unknown output target")

metadata = read("tex/latex/insr/insr-metadata.sty")
if "{2026}" in metadata:
    fail("Suggested citation contains a hard-coded year")
if "\\number\\year" not in metadata:
    fail("Suggested citation must derive its fallback year dynamically")

layout = read("tex/latex/insr/insr-layout.sty")
if "typography_microtype" not in layout or "RequirePackage{microtype}" not in layout:
    fail("microtype must remain explicitly configurable to avoid kernel warning regressions")
if "RequirePackage{bookmark}" not in layout:
    fail("bookmark must load after hyperref")

localization = read("tex/latex/insr/insr-localization.sty")
if "babelprovide[import,main]{ngerman}" not in localization:
    fail("ngerman must be selected before biblatex is loaded")

subprocess.run(["python3", "tools/insr_registry.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
subprocess.run(["python3", "tools/overleaf_doctor.py", "check"], cwd=ROOT, check=True)

print("project validation passed")
