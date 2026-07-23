#!/usr/bin/env python3
"""Registry-to-runtime integrity audit for the INSR publishing platform."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from insr_registry import load_registry, targets_from_registry, validate_registry
import check_latex_log
import insr_build

ROOT = Path(__file__).resolve().parents[1]
STATUS_ORDER = {"supported": 0, "experimental": 1, "incomplete": 2, "legacy": 3, "broken": 4}
RUNTIME_TEMPLATE_RE = re.compile(r"\\(?:NewDocumentCommand|DeclareDocumentCommand|cs_new|cs_set|input|file_input|begin\{INSRContentUnit\})")
CONTENT_FIELD_COMMANDS = {
    "full": "\\INSRFullText",
    "summary": "\\INSRSummary",
    "key": "\\INSRKeyMessage",
    "handout": "\\INSRHandoutText",
    "poster": "\\INSRPosterText",
    "executive": "\\INSRExecutiveSummary",
    "clinical": "\\INSRClinicalApplication",
    "safety": "\\INSRSafetyNote",
    "methods": "\\INSRMethodsSummary",
    "limitations": "\\INSRLimitationsSummary",
    "notes": "\\INSRSpeakerNotes",
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def file_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": rel(path), "exists": False, "nonempty": False, "runtime_function": False}
    text = path.read_text(encoding="utf-8")
    stripped_lines = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("%")]
    runtime_function = bool(stripped_lines and RUNTIME_TEMPLATE_RE.search("\n".join(stripped_lines)))
    return {"path": rel(path), "exists": True, "nonempty": bool(stripped_lines), "runtime_function": runtime_function}


def classify_document(name: str, info: dict[str, str], source_counts: Counter[str]) -> tuple[str, list[str], dict[str, Any]]:
    profile = ROOT / "profiles" / "documents" / f"{info.get('profile', '')}.profile.tex"
    manifest = ROOT / "content" / info.get("source", "") / "manifest.tex"
    template = ROOT / "framework" / "templates" / f"{info.get('template', '')}.tex"
    artifacts = {"profile": file_state(profile), "manifest": file_state(manifest), "template": file_state(template)}
    reasons: list[str] = []
    status = "supported"
    if not artifacts["profile"]["exists"] or not artifacts["manifest"]["exists"]:
        return "broken", ["missing profile or content manifest"], artifacts
    if info.get("source") == "insr-position-paper" and name not in {"position-paper", "paper", "journal-article", "article"}:
        status = "incomplete"
        reasons.append("uses shared insr-position-paper content source instead of a dedicated manifest")
    if source_counts[info.get("source", "")] > 4:
        reasons.append(f"content source {info.get('source')} is shared by {source_counts[info.get('source', '')]} document types")
    if artifacts["template"]["exists"] and not artifacts["template"]["runtime_function"]:
        status = max_status(status, "incomplete")
        reasons.append("registered template file is declarative only and has no detectable runtime implementation")
    elif not artifacts["template"]["exists"]:
        status = max_status(status, "incomplete")
        reasons.append("registered template file is absent; manifest drives rendering")
    return status, reasons, artifacts


def max_status(a: str, b: str) -> str:
    return a if STATUS_ORDER[a] >= STATUS_ORDER[b] else b


def _adapter_runtime_text(adapter_name: str, seen: set[str] | None = None) -> str:
    seen = seen or set()
    if adapter_name in seen:
        return ""
    seen.add(adapter_name)
    path = ROOT / "framework" / "adapters" / f"{adapter_name}.tex"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    chunks = [text]
    for included in re.findall(r"\\input\{framework/adapters/([^}]+)\.tex\}", text):
        chunks.append(_adapter_runtime_text(included, seen))
    return "\n".join(chunks)


def _adapter_declared_fallbacks(adapter_name: str) -> list[str]:
    path = ROOT / "framework" / "adapters" / f"{adapter_name}.tex"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?mi)^\s*%\s*fallbacks\s*:\s*([a-z0-9_,\-\s]+)$", text)
    if not match:
        return []
    return [field.strip() for field in match.group(1).split(",") if field.strip()]


def _clean_fields(fields: list[str], explicit_fields: list[str] | None = None) -> list[str]:
    explicit = set(explicit_fields or [])
    noise = {"notes", "internal_comments"}
    clean: list[str] = []
    for field in fields:
        if field in noise and field not in explicit:
            continue
        if field and field not in clean:
            clean.append(field)
    return clean


def adapter_fields(adapter_name: str, output_target: str | None = None) -> list[str]:
    # Specialized output targets can include generic adapters, but their runtime
    # field set is defined by the target-specific fallback chain. Keep these
    # checks ahead of adapter text scanning so inherited helpers (for example
    # slide speaker notes) do not leak into handout/integrity reports.
    target_fallbacks = {
        "handout": ["handout", "summary", "full", "key"],
        "poster": ["poster", "summary", "key", "full"],
        "executive-brief": ["executive", "summary", "full", "key"],
        "submission-package": ["full", "summary", "key"],
        "web": ["summary", "full", "key"],
    }
    if output_target in target_fallbacks:
        declared = _adapter_declared_fallbacks(adapter_name)
        fields = declared or target_fallbacks[output_target]
        return sorted(_clean_fields(fields, declared))

    runtime_text = _adapter_runtime_text(adapter_name)
    fields = []
    for field, command in CONTENT_FIELD_COMMANDS.items():
        tl_name = f"l_insr_unit_{field}_tl"
        if command in runtime_text or tl_name in runtime_text:
            fields.append(field)
            continue
        if re.search(rf"(?<![A-Za-z]){re.escape(field)}(?![A-Za-z])", runtime_text):
            fields.append(field)

    # Block adapters delegate the field decision to insr-content.sty. Report the
    # runtime fallback chain for the concrete output target instead of attributing
    # every content API field to every adapter.
    block_fallbacks = {
        "paper": ["full", "summary", "key"],
        "article": ["full", "summary", "key"],
        "report": ["full", "summary", "key"],
        "book": ["full", "summary", "key"],
        "thesis": ["full", "summary", "key"],
        "manual": ["clinical", "safety", "full", "summary", "key"],
        "executive-brief": ["executive", "summary", "full", "key"],
        "submission-package": ["full", "summary", "key"],
        "web": ["full", "summary", "key"],
        "letter": ["full", "summary", "key"],
    }
    if "__insr_render_content_unit_block" in runtime_text and output_target in block_fallbacks:
        fields.extend(block_fallbacks[output_target])
    return sorted(dict.fromkeys(fields))


def build_report() -> dict[str, Any]:
    registry_errors = validate_registry()
    registry = load_registry()
    targets = targets_from_registry() if not registry_errors else {}
    docs: dict[str, dict[str, Any]] = {}
    outputs: dict[str, dict[str, Any]] = {}
    combos: dict[str, dict[str, Any]] = {}
    source_counts = Counter(info.get("source", "") for info in registry["document_types"].values())

    for name, info in registry["document_types"].items():
        status, reasons, artifacts = classify_document(name, info, source_counts)
        docs[name] = {"status": status, "profile": info.get("profile"), "source": info.get("source"), "template": info.get("template"), "reasons": reasons, "artifacts": artifacts}

    for name, info in registry["output_targets"].items():
        adapter_path = ROOT / "framework" / "adapters" / f"{info.get('adapter', '')}.tex"
        status = "supported" if adapter_path.exists() and adapter_path.read_text(encoding="utf-8").strip() else "broken"
        reasons = [] if status == "supported" else ["missing or empty adapter"]
        if name in {"web", "submission-package", "executive-brief"}:
            status = "experimental"
            reasons.append("registered target is currently PDF/adapter compatibility output, not a full product")
        outputs[name] = {"status": status, "base": info.get("base"), "adapter": info.get("adapter"), "class-options": info.get("class-options", ""), "reasons": reasons, "adapter_file": rel(adapter_path)}

    for name, info in targets.items():
        status = max_status(docs[info["type"]]["status"], outputs[info["target"]]["status"])
        reasons = docs[info["type"]]["reasons"] + outputs[info["target"]]["reasons"]
        combos[name] = {**info, "status": status, "reasons": reasons}

    fields_by_adapter = {name: adapter_fields(info.get("adapter", ""), name) for name, info in registry["output_targets"].items()}
    return {
        "summary": {
            "document_type_count": len(registry["document_types"]),
            "output_target_count": len(registry["output_targets"]),
            "combination_count": len(registry["combinations"]),
            "shared_sources": dict(source_counts),
            "registry_errors": registry_errors,
        },
        "document_types": docs,
        "output_targets": outputs,
        "combinations": combos,
        "aliases": registry["aliases"],
        "content_fields_by_adapter": fields_by_adapter,
    }


def write_reports(report: dict[str, Any], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "insr-integrity.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# INSR Registry-to-Runtime Integrity Audit", "", "## Summary", ""]
    for key, value in report["summary"].items():
        lines.append(f"- **{key}**: `{value}`")
    lines += ["", "## Document types", "", "| Document type | Status | Source | Template | Reason |", "| --- | --- | --- | --- | --- |"]
    for name, info in sorted(report["document_types"].items()):
        lines.append(f"| `{name}` | `{info['status']}` | `{info['source']}` | `{info['template']}` | {'; '.join(info['reasons']) or 'runtime files present'} |")
    lines += ["", "## Output targets", "", "| Target | Status | Base | Adapter | Reason |", "| --- | --- | --- | --- | --- |"]
    for name, info in sorted(report["output_targets"].items()):
        lines.append(f"| `{name}` | `{info['status']}` | `{info['base']}` | `{info['adapter']}` | {'; '.join(info['reasons']) or 'adapter present'} |")
    lines += ["", "## Adapter content-field usage", "", "| Target | Fields read by runtime path |", "| --- | --- |"]
    for name, fields in sorted(report["content_fields_by_adapter"].items()):
        lines.append(f"| `{name}` | `{', '.join(fields)}` |")
    lines.append("")
    (outdir / "insr-integrity.md").write_text("\n".join(lines), encoding="utf-8")


def compile_combinations(report: dict[str, Any], names: list[str] | None) -> int:
    names = names or sorted(report["combinations"])
    rc = 0
    for name in names:
        build_rc = insr_build.build(name)
        rc = build_rc or rc
        if build_rc == 0:
            log = insr_build.log_path_for(name)
            problems = check_latex_log.check(log)
            if problems:
                print("INSR LaTeX log validation failed")
                for problem in problems:
                    print(f"- {problem}")
                rc = 1
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", default="build/integrity", help="directory for JSON and Markdown reports")
    parser.add_argument("--json", action="store_true", help="print JSON report to stdout")
    parser.add_argument("--compile", action="store_true", help="also compile registered combinations via tools/insr_build.py")
    parser.add_argument("--combination", action="append", help="limit --compile to a combination; may be repeated")
    args = parser.parse_args()

    report = build_report()
    write_reports(report, ROOT / args.outdir)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    broken = [name for name, info in report["document_types"].items() if info["status"] == "broken"]
    broken += [name for name, info in report["output_targets"].items() if info["status"] == "broken"]
    if report["summary"]["registry_errors"]:
        broken.extend(report["summary"]["registry_errors"])
    rc = 1 if broken else 0
    if args.compile:
        rc = compile_combinations(report, args.combination) or rc
    if broken:
        print("broken registry/runtime entries: " + ", ".join(broken), file=sys.stderr)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
