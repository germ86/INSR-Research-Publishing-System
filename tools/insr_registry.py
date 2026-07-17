#!/usr/bin/env python3
"""Shared parser for the checked-in INSR LaTeX target registry."""
from __future__ import annotations
import re
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "target-registry.tex"

_CALL_RE = re.compile(r"\\INSRRegister(DocumentType|OutputTarget|Combination|DocumentAlias)\{([^}]*)\}(?:\{([^}]*)\})?")

def _split_top_level_commas(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    for char in text:
        if char == "{":
            depth += 1
        elif char == "}" and depth:
            depth -= 1
        if char == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(char)
    parts.append("".join(buf))
    return parts

def _parse_kv(text: str | None) -> dict[str, str]:
    if not text:
        return {}
    out: dict[str, str] = {}
    for part in _split_top_level_commas(text):
        if not part.strip():
            continue
        key, sep, value = part.partition('=')
        if sep:
            out[key.strip()] = value.strip().strip('{}')
    return out

def load_registry(path: Path = REGISTRY) -> dict[str, Dict[str, dict[str, str] | str]]:
    text = path.read_text(encoding="utf-8")
    document_types: dict[str, dict[str, str]] = {}
    output_targets: dict[str, dict[str, str]] = {}
    combinations: dict[str, dict[str, str]] = {}
    aliases: dict[str, str] = {}
    for kind, name, body in _CALL_RE.findall(text):
        if kind == "DocumentType":
            document_types[name] = _parse_kv(body)
        elif kind == "OutputTarget":
            output_targets[name] = _parse_kv(body)
        elif kind == "Combination":
            combinations[name] = _parse_kv(body)
        elif kind == "DocumentAlias":
            aliases[name] = body or ""
    return {
        "document_types": document_types,
        "output_targets": output_targets,
        "combinations": combinations,
        "aliases": aliases,
    }

def targets_from_registry() -> dict[str, dict[str, str]]:
    registry = load_registry()
    docs = registry["document_types"]
    outputs = registry["output_targets"]
    combos = registry["combinations"]
    targets: dict[str, dict[str, str]] = {}
    for name, combo in combos.items():
        doc_type = combo["type"]
        output_target = combo["target"]
        if doc_type not in docs:
            raise ValueError(f"combination {name} references unknown document type {doc_type}")
        if output_target not in outputs:
            raise ValueError(f"combination {name} references unknown output target {output_target}")
        doc = docs[doc_type]
        output = outputs[output_target]
        targets[name] = {
            "type": doc_type,
            "target": output_target,
            "base": output["base"],
            "adapter": output["adapter"],
            "profile": doc["profile"],
            "source": doc["source"],
            "template": doc.get("template", doc_type),
            "class_options": output.get("class-options", ""),
        }
    return targets

if __name__ == "__main__":
    for name, info in targets_from_registry().items():
        print(f"{name}: type={info['type']} target={info['target']} base={info['base']} adapter={info['adapter']} profile={info['profile']} source={info['source']}")
