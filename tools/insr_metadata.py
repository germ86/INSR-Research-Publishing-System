#!/usr/bin/env python3
"""Export lightweight publication metadata from INSR TeX configuration files."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILES = [ROOT / "config" / name for name in ["metadata-config.tex", "publication-config.tex", "authors-config.tex"]]

def read_all() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in CONFIG_FILES if p.exists())

def braced_value(text: str, key: str) -> str:
    m = re.search(rf"{re.escape(key)}\s*=\s*\{{([^{{}}]*)\}}", text)
    return m.group(1).strip() if m else ""

def parse_authors(text: str) -> list[dict[str, str]]:
    authors = []
    for block in re.findall(r"\\INSRAddAuthor\s*\{(.*?)\}\s*(?=\\INSRAddAuthor|\\INSRAddInstitution|$)", text, re.S):
        authors.append({
            "name": braced_value(block, "name"),
            "orcid": braced_value(block, "orcid"),
            "short_name": braced_value(block, "short-name"),
            "roles": braced_value(block, "roles"),
        })
    if not authors:
        name = braced_value(text, "metadata/author")
        if name:
            authors.append({"name": name, "orcid": "", "short_name": "", "roles": ""})
    return authors

def metadata() -> dict[str, object]:
    text = read_all()
    doi = braced_value(text, "publication/doi")
    if doi.lower() in {"pending", "to be assigned"}:
        doi = ""
    data = {
        "title": braced_value(text, "metadata/title"),
        "subtitle": braced_value(text, "metadata/subtitle"),
        "version": braced_value(text, "publication/version"),
        "status": braced_value(text, "publication/status"),
        "date": braced_value(text, "publication/date"),
        "year": braced_value(text, "publication/year"),
        "doi": doi,
        "repository": braced_value(text, "publication/repository"),
        "license": braced_value(text, "publication/license"),
        "publisher": braced_value(text, "publication/publisher") or braced_value(text, "metadata/institution"),
        "authors": parse_authors(text),
    }
    if not data["year"] and data["date"]:
        m = re.search(r"(\d{4})", str(data["date"]))
        data["year"] = m.group(1) if m else ""
    return data

def validate(data: dict[str, object]) -> list[str]:
    problems = []
    for field in ["title", "version", "date", "year", "license", "repository"]:
        if not data.get(field):
            problems.append(f"missing required metadata field: {field}")
    if not data.get("authors"):
        problems.append("missing required metadata field: authors")
    for author in data.get("authors", []):
        if not author.get("name"):
            problems.append("author entry is missing name")
    return problems

def cff(data: dict[str, object]) -> str:
    lines = ["cff-version: 1.2.0", f"title: {data['title']}", f"version: {data['version']}", f"date-released: {data['date']}", f"license: {data['license']}", "authors:"]
    for author in data["authors"]:
        lines.append(f"  - name: {author['name']}")
        if author.get("orcid"):
            lines.append(f"    orcid: https://orcid.org/{author['orcid']}")
    if data.get("doi"):
        lines.append(f"doi: {data['doi']}")
    if data.get("repository"):
        lines.append(f"repository-code: {data['repository']}")
    return "\n".join(lines) + "\n"

def datacite(data: dict[str, object]) -> str:
    out = {
        "types": {"resourceTypeGeneral": "Text", "resourceType": "Preprint"},
        "titles": [{"title": data["title"]}],
        "creators": [{"name": a["name"], **({"nameIdentifiers": [{"nameIdentifier": f"https://orcid.org/{a['orcid']}", "nameIdentifierScheme": "ORCID"}]} if a.get("orcid") else {})} for a in data["authors"]],
        "publisher": data.get("publisher"), "publicationYear": data.get("year"),
        "version": data.get("version"), "rightsList": [{"rights": data.get("license")}],
    }
    if data.get("doi"):
        out["doi"] = data["doi"]
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"

def codemeta(data: dict[str, object]) -> str:
    out = {"@context": "https://doi.org/10.5063/schema/codemeta-2.0", "@type": "SoftwareSourceCode", "name": data["title"], "version": data["version"], "datePublished": data["date"], "license": data["license"], "codeRepository": data["repository"], "author": [{"@type": "Person", "name": a["name"], **({"identifier": f"https://orcid.org/{a['orcid']}"} if a.get("orcid") else {})} for a in data["authors"]]}
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"

def export_all(outdir: Path) -> int:
    data = metadata(); problems = validate(data)
    if problems:
        print("\n".join(problems), file=sys.stderr); return 1
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "CITATION.cff").write_text(cff(data), encoding="utf-8")
    (outdir / "datacite.json").write_text(datacite(data), encoding="utf-8")
    (outdir / "codemeta.json").write_text(codemeta(data), encoding="utf-8")
    (outdir / "zenodo-preview.json").write_text(datacite(data), encoding="utf-8")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    for name in ["export-cff", "export-datacite", "export-codemeta", "export-all"]:
        sp = sub.add_parser(name); sp.add_argument("--outdir", default="build/metadata")
    args = parser.parse_args(); data = metadata()
    if args.command == "validate":
        problems = validate(data)
        if problems:
            print("\n".join(problems), file=sys.stderr); return 1
        print("metadata validation passed"); return 0
    outdir = ROOT / args.outdir
    if args.command == "export-all": return export_all(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    target = {"export-cff": ("CITATION.cff", cff), "export-datacite": ("datacite.json", datacite), "export-codemeta": ("codemeta.json", codemeta)}[args.command]
    (outdir / target[0]).write_text(target[1](data), encoding="utf-8")
    return 0
if __name__ == "__main__": raise SystemExit(main())
