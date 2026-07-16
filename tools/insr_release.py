#!/usr/bin/env python3
"""Prepare a local, non-publishing INSR release bundle."""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_SUFFIXES = {".aux", ".log", ".toc", ".bcf", ".run.xml", ".fdb_latexmk", ".fls", ".synctex.gz"}

def sha256(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dest)

def prepare(version: str) -> int:
    out = ROOT / "dist" / f"insr-{version}"
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    subprocess.run(["python3", "tools/insr_metadata.py", "export-all", "--outdir", str(out / "metadata")], cwd=ROOT, check=True)
    for rel in ["README.md", "LICENSE", "references.bib", "main.tex", "latexmkrc"]:
        path = ROOT / rel
        if path.exists(): copy_file(path, out / rel)
    for tree in ["config", "content", "examples/reference-publication", "tex/latex/insr"]:
        src = ROOT / tree
        if src.exists():
            for path in src.rglob("*"):
                if path.is_file() and path.suffix not in EXCLUDE_SUFFIXES and "__pycache__" not in path.parts:
                    copy_file(path, out / path.relative_to(ROOT))
    manifest = {"version": version, "created_utc": datetime.now(timezone.utc).isoformat(), "files": []}
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        manifest["files"].append({"path": str(path.relative_to(out)), "sha256": sha256(path), "bytes": path.stat().st_size})
    (out / "release-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare"); p.add_argument("--version", required=True)
    args = parser.parse_args()
    if args.command == "prepare": return prepare(args.version)
    return 1
if __name__ == "__main__": raise SystemExit(main())
