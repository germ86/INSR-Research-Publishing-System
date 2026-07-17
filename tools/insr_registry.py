#!/usr/bin/env python3
"""Shared parser and validator for the checked-in INSR LaTeX target registry."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "target-registry.tex"

_CALL_RE = re.compile(
    r"\\INSRRegister(DocumentType|OutputTarget|Combination|DocumentAlias)"
    r"\{([^}]*)\}(?:\{([^}]*)\})?"
)


def _parse_kv(text: str | None) -> dict[str, str]:
    if not text:
        return {}
    out: dict[str, str] = {}
    for part in text.split(","):
        if not part.strip():
            continue
        key, sep, value = part.partition("=")
        if not sep:
            raise ValueError(f"registry item is not key=value: {part!r}")
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError(f"registry item has an empty key or value: {part!r}")
        out[key] = value
    return out


def load_registry(path: Path = REGISTRY) -> dict[str, Dict[str, dict[str, str] | str]]:
    text = path.read_text(encoding="utf-8")
    document_types: dict[str, dict[str, str]] = {}
    output_targets: dict[str, dict[str, str]] = {}
    combinations: dict[str, dict[str, str]] = {}
    aliases: dict[str, str] = {}
    for kind, raw_name, body in _CALL_RE.findall(text):
        name = raw_name.strip()
        if not name:
            raise ValueError("registry entry has an empty name")
        if kind == "DocumentType":
            if name in document_types:
                raise ValueError(f"duplicate document type: {name}")
            document_types[name] = _parse_kv(body)
        elif kind == "OutputTarget":
            if name in output_targets:
                raise ValueError(f"duplicate output target: {name}")
            output_targets[name] = _parse_kv(body)
        elif kind == "Combination":
            if name in combinations:
                raise ValueError(f"duplicate combination: {name}")
            combinations[name] = _parse_kv(body)
        elif kind == "DocumentAlias":
            if name in aliases:
                raise ValueError(f"duplicate document alias: {name}")
            aliases[name] = (body or "").strip()
    return {
        "document_types": document_types,
        "output_targets": output_targets,
        "combinations": combinations,
        "aliases": aliases,
    }


def validate_registry(path: Path = REGISTRY) -> list[str]:
    problems: list[str] = []
    try:
        registry = load_registry(path)
    except (OSError, ValueError) as exc:
        return [str(exc)]

    docs = registry["document_types"]
    outputs = registry["output_targets"]
    combinations = registry["combinations"]
    aliases = registry["aliases"]

    for name, info in docs.items():
        for key in ("profile", "source", "template"):
            if not info.get(key):
                problems.append(f"document type {name!r} is missing {key}")
    for name, info in outputs.items():
        for key in ("base", "adapter"):
            if not info.get(key):
                problems.append(f"output target {name!r} is missing {key}")
    for name, info in combinations.items():
        doc_type = info.get("type", "")
        target = info.get("target", "")
        if doc_type not in docs:
            problems.append(f"combination {name!r} references unknown document type {doc_type!r}")
        if target not in outputs:
            problems.append(f"combination {name!r} references unknown output target {target!r}")
    for alias, canonical in aliases.items():
        if canonical not in docs:
            problems.append(f"document alias {alias!r} references unknown type {canonical!r}")
    return problems


def targets_from_registry() -> dict[str, dict[str, str]]:
    problems = validate_registry()
    if problems:
        raise ValueError("invalid target registry: " + "; ".join(problems))
    registry = load_registry()
    docs = registry["document_types"]
    outputs = registry["output_targets"]
    combinations = registry["combinations"]
    targets: dict[str, dict[str, str]] = {}
    for name, combo in combinations.items():
        doc_type = combo["type"]
        output_target = combo["target"]
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
            "class-options": output.get("class-options", ""),
        }
    return targets


if __name__ == "__main__":
    issues = validate_registry()
    if issues:
        for issue in issues:
            print(issue)
        raise SystemExit(1)
    for name, info in sorted(targets_from_registry().items()):
        print(
            f"{name}: type={info['type']} target={info['target']} base={info['base']} "
            f"adapter={info['adapter']} profile={info['profile']} source={info['source']}"
        )
