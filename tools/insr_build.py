#!/usr/bin/env python3
"""Optional local multi-target builder for INSR documents."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from insr_registry import load_registry, targets_from_registry
from overleaf_doctor import ROOT, check_source, check_target

ACTIVE = ROOT / "config" / "active-target.tex"


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp_name, path)


def write_active(combination: str) -> str | None:
    targets = targets_from_registry()
    if combination not in targets:
        raise KeyError(combination)
    info = targets[combination]
    old = ACTIVE.read_text(encoding="utf-8") if ACTIVE.exists() else None
    text = (
        "% Temporary document/output selection written by tools/insr_build.py\n"
        "\\INSRBootstrap{\n"
        f"  document/type = {info['type']},\n"
        f"  output/target = {info['target']}\n"
        "}\n"
    )
    _atomic_write(ACTIVE, text)
    return old


def restore_active(old: str | None) -> None:
    if old is None:
        ACTIVE.unlink(missing_ok=True)
    else:
        _atomic_write(ACTIVE, old)


def _clean_root_aux() -> None:
    for suffix in [
        "aux", "toc", "out", "bcf", "bbl", "blg", "run.xml", "fdb_latexmk",
        "fls", "log", "nav", "snm", "synctex.gz", "vrb",
    ]:
        (ROOT / f"main.{suffix}").unlink(missing_ok=True)


def run_latexmk(combination: str) -> int:
    _clean_root_aux()
    outdir = ROOT / "build" / combination
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    if shutil.which("latexmk") is None:
        (outdir / "build.log").write_text("latexmk not found; build not executed\n", encoding="utf-8")
        print("latexmk not found")
        return 127
    cmd = [
        "latexmk",
        "-lualatex",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-halt-on-error",
        f"-outdir={outdir}",
        "main.tex",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (outdir / "build.log").write_text(proc.stdout, encoding="utf-8")
    return proc.returncode


def build(combination: str) -> int:
    targets = targets_from_registry()
    if combination not in targets:
        print(f"unknown registered combination: {combination}")
        return 1
    old = write_active(combination)
    try:
        return run_latexmk(combination)
    finally:
        restore_active(old)


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
