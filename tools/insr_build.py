#!/usr/bin/env python3
"""Optional local multi-target builder for INSR documents."""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
from pathlib import Path

from insr_registry import load_registry, targets_from_registry
from overleaf_doctor import ROOT, check_source, check_target

CONFIG_HASH_PATHS = (ROOT / "config", ROOT / "main.tex")


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", name).strip("-") or "default"


def compile_root(combination: str) -> Path:
    return ROOT / "build" / "compile" / _safe_name(combination)


def driver_path_for(combination: str) -> Path:
    return compile_root(combination) / "driver.tex"


def output_dir_for(combination: str) -> Path:
    return compile_root(combination) / "out"


def log_path_for(combination: str) -> Path:
    return output_dir_for(combination) / "driver.log"


def build_log_path_for(combination: str) -> Path:
    return compile_root(combination) / "build.log"


def _tracked_config_files() -> list[Path]:
    paths: list[Path] = []
    try:
        proc = subprocess.run(
            ["git", "ls-files", "config", "main.tex"],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        paths = [ROOT / line.strip() for line in proc.stdout.splitlines() if line.strip()]
    except (OSError, subprocess.CalledProcessError):
        for root in CONFIG_HASH_PATHS:
            if root.is_file():
                paths.append(root)
            elif root.is_dir():
                paths.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(set(paths))


def versioned_config_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in _tracked_config_files():
        if not path.exists():
            hashes[str(path.relative_to(ROOT))] = "<missing>"
            continue
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def assert_versioned_config_unchanged(before: dict[str, str]) -> None:
    after = versioned_config_hashes()
    if before != after:
        changed = sorted(set(before) | set(after))
        delta = [name for name in changed if before.get(name) != after.get(name)]
        raise RuntimeError("versioned configuration mutated during build: " + ", ".join(delta))


def write_driver(combination: str) -> Path:
    if combination not in targets_from_registry():
        raise KeyError(combination)
    root = compile_root(combination)
    root.mkdir(parents=True, exist_ok=True)
    driver = driver_path_for(combination)
    driver.write_text(
        "% Generated, ignored INSR build driver. Do not edit or commit.\n"
        f"\\documentclass[config/load-project=false,build/preset={combination}]{{insr}}\n"
        "\\begin{document}\n"
        "\\INSRMakeTitle\n"
        "\\INSRRenderDocument\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    return driver


def run_latexmk(combination: str) -> int:
    root = compile_root(combination)
    outdir = output_dir_for(combination)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    driver = write_driver(combination)
    if shutil.which("latexmk") is None:
        build_log_path_for(combination).write_text("latexmk not found; build not executed\n", encoding="utf-8")
        print("latexmk not found")
        return 127
    cmd = [
        "latexmk",
        "-lualatex",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-halt-on-error",
        f"-outdir={outdir}",
        str(driver),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    build_log_path_for(combination).write_text(proc.stdout, encoding="utf-8")
    return proc.returncode


def build(combination: str) -> int:
    targets = targets_from_registry()
    if combination not in targets:
        print(f"unknown registered combination: {combination}")
        return 1
    before = versioned_config_hashes()
    try:
        return run_latexmk(combination)
    finally:
        assert_versioned_config_unchanged(before)


def validate(combination: str | None = None) -> int:
    targets = targets_from_registry()
    names = [combination] if combination else sorted(targets)
    rc = 0
    for name in names:
        if name not in targets:
            print(f"unknown registered combination: {name}")
            rc = 1
            continue
        rc = check_target(argparse.Namespace(target=name)) or rc
    for source in sorted({info.get("source", "insr-position-paper") for info in targets.values()}):
        rc = check_source(argparse.Namespace(source=source)) or rc
    return rc


def list_document_types() -> None:
    registry = load_registry()
    for name in sorted(registry["document_types"]):
        print(name)


def list_output_targets() -> None:
    registry = load_registry()
    for name in sorted(registry["output_targets"]):
        print(name)


def list_combinations() -> None:
    for name, info in sorted(targets_from_registry().items()):
        print(
            f"{name}: document/type={info['type']} output/target={info['target']} "
            f"base={info['base']} adapter={info['adapter']} "
            f"profile={info['profile']} source={info['source']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build")
    build_parser.add_argument("combination")
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("combination", nargs="?")
    sub.add_parser("build-all")
    sub.add_parser("list-targets")
    sub.add_parser("list-document-types")
    sub.add_parser("list-output-targets")
    sub.add_parser("list-combinations")
    args = parser.parse_args()

    if args.command == "list-targets":
        print("\n".join(sorted(targets_from_registry())))
        return 0
    if args.command == "validate":
        return validate(args.combination)
    if args.command == "build":
        return build(args.combination)
    if args.command == "build-all":
        rc = 0
        for combination in sorted(targets_from_registry()):
            rc = build(combination) or rc
        return rc
    if args.command == "list-document-types":
        list_document_types()
        return 0
    if args.command == "list-output-targets":
        list_output_targets()
        return 0
    if args.command == "list-combinations":
        list_combinations()
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
