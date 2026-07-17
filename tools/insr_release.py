#!/usr/bin/env python3
"""Prepare a local, non-publishing INSR release bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_SUFFIXES = {
    ".aux",
    ".log",
    ".toc",
    ".bcf",
    ".run.xml",
    ".fdb_latexmk",
    ".fls",
    ".synctex.gz",
}
ROOT_FILES = [
    "README.md",
    "LICENSE",
    "references.bib",
    "main.tex",
    "latexmkrc",
    "insr.cls",
]
RUNTIME_TREES = [
    "config",
    "content",
    "framework",
    "profiles",
    "themes",
    "palettes",
    "typography",
    "templates",
    "i18n",
    "locales",
    "assets",
    "tex/latex/insr",
    "examples/reference-publication",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def copy_tree(tree: str, out: Path) -> None:
    src = ROOT / tree
    if not src.exists():
        return
    for path in src.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if any(str(path).endswith(suffix) for suffix in EXCLUDE_SUFFIXES):
            continue
        copy_file(path, out / path.relative_to(ROOT))


def prepare(version: str) -> int:
    out = ROOT / "dist" / f"insr-{version}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    subprocess.run(
        ["python3", "tools/insr_metadata.py", "export-all", "--outdir", str(out / "metadata")],
        cwd=ROOT,
        check=True,
    )

    root_paths = [ROOT / relative for relative in ROOT_FILES]
    root_paths.extend(sorted(ROOT.glob("insr-*.sty")))
    root_paths.extend(sorted(ROOT.glob("insr-*.cls")))
    seen: set[Path] = set()
    for path in root_paths:
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        copy_file(path, out / path.relative_to(ROOT))

    for tree in RUNTIME_TREES:
        copy_tree(tree, out)

    required_runtime = [
        out / "main.tex",
        out / "insr.cls",
        out / "insr-core.sty",
        out / "tex/latex/insr/insr-core.sty",
        out / "config/target-registry.tex",
        out / "content/manifest.tex",
        out / "framework/adapters/paper.tex",
        out / "profiles/documents/position-paper.profile.tex",
        out / "themes/insr-default.tex",
        out / "palettes/neuroclinical.tex",
        out / "typography/libertinus.tex",
    ]
    missing = [str(path.relative_to(out)) for path in required_runtime if not path.is_file()]
    if missing:
        raise SystemExit(f"Release bundle is missing runtime files: {missing}")

    manifest = {
        "version": version,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "files": [],
    }
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        manifest["files"].append(
            {
                "path": str(path.relative_to(out)),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    (out / "release-manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    prepare_parser = sub.add_parser("prepare")
    prepare_parser.add_argument("--version", required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        return prepare(args.version)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
