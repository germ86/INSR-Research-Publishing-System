#!/usr/bin/env python3
"""Optional local multi-target builder for INSR documents."""
from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from overleaf_doctor import TARGETS, ROOT, check_source, check_target
from insr_registry import load_registry

ACTIVE = ROOT / "config" / "active-target.tex"

def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp_name, path)

def write_active(target: str) -> str | None:
    old = ACTIVE.read_text(encoding="utf-8") if ACTIVE.exists() else None
    info = TARGETS[target]
    document_type = info.get("type", target)
    output_target = info.get("target", "paper")
    _atomic_write(
        ACTIVE,
        "% Temporary target selected by tools/insr_build.py\n"
        f"\\INSRBootstrap{{document/type={document_type}, output/target={output_target}}}\n",
    )
    return old

def restore_active(old: str | None) -> None:
    if old is None:
        ACTIVE.unlink(missing_ok=True)
    else:
        _atomic_write(ACTIVE, old)

def run_latexmk(target: str) -> int:
    outdir = ROOT / "build" / target
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    if shutil.which("latexmk") is None:
        (outdir / "build.log").write_text("latexmk not found; build not executed\n", encoding="utf-8")
        print("latexmk not found")
        return 127
    cmd = ["latexmk", "-lualatex", "-bibtex-", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={outdir}", "main.tex"]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (outdir / "build.log").write_text(proc.stdout, encoding="utf-8")
    return proc.returncode

def build(target: str) -> int:
    if target not in TARGETS:
        print(f"unknown target: {target}")
        return 1
    old = write_active(target)
    try:
        return run_latexmk(target)
    finally:
        restore_active(old)

def validate(target: str | None = None) -> int:
    rc = 0
    names = [target] if target else list(TARGETS)
    for name in names:
        ns = argparse.Namespace(target=name)
        rc = check_target(ns) or rc
    rc = check_source(argparse.Namespace(source="insr-position-paper")) or rc
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
    for name, info in TARGETS.items():
        print(f"{name}: document/type={info['type']} output/target={info['target']} base={info['base']} adapter={info['adapter']} profile={info['profile']} source={info['source']}")

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build"); b.add_argument("target")
    v = sub.add_parser("validate"); v.add_argument("target", nargs="?")
    sub.add_parser("build-all")
    sub.add_parser("list-targets")
    sub.add_parser("list-document-types")
    sub.add_parser("list-output-targets")
    sub.add_parser("list-combinations")
    args = parser.parse_args()
    if args.command == "list-targets":
        print("\n".join(TARGETS))
        return 0
    if args.command == "validate":
        return validate(args.target)
    if args.command == "build":
        return build(args.target)
    if args.command == "build-all":
        rc = 0
        for target in TARGETS:
            rc = build(target) or rc
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
