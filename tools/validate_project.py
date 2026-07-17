#!/usr/bin/env python3
"""Repository-wide structural validation for the INSR publishing platform."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from insr_registry import load_registry, targets_from_registry, validate_registry

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(message)


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8") if not isinstance(path, Path) else path.read_text(encoding="utf-8")


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

required_packages = [
    "insr-core", "insr-config", "insr-metadata", "insr-content", "insr-adapters",
    "insr-bibliography", "insr-localization", "insr-typography", "insr-colors",
    "insr-layout", "insr-page-style", "insr-boxes", "insr-accessibility",
    "insr-neuro", "insr-utils",
]
for package in required_packages:
    path = ROOT / f"tex/latex/insr/{package}.sty"
    if not path.is_file():
        fail(f"Missing modular package: {path.relative_to(ROOT)}")
    if f"\\ProvidesPackage{{{package}}}" not in path.read_text(encoding="utf-8"):
        fail(f"Package name does not match request name in {path.relative_to(ROOT)}")

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
    if any(marker in text for marker in ("<<<<<<<", "=======", ">>>>>>>")):
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
