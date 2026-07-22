#!/usr/bin/env python3
"""Canonical version metadata for INSR tooling and release validation."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "insr-version.json"

def load_version(path: Path = VERSION_FILE) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))

def l3build_version() -> str:
    data = load_version()
    return f"{data['version']} {data['date']}"

if __name__ == "__main__":
    data = load_version()
    for key in sorted(data):
        print(f"{key}={data[key]}")
