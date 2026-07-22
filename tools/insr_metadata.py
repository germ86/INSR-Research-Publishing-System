#!/usr/bin/env python3
"""Export publication metadata from INSR TeX configuration files."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILES = [
    ROOT / "config" / name
    for name in ("metadata-config.tex", "publication-config.tex", "authors-config.tex")
]


def read_all() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in CONFIG_FILES if path.exists())


def braced_value(text: str, key: str) -> str:
    match = re.search(rf"{re.escape(key)}\s*=\s*\{{([^{{}}]*)\}}", text)
    return match.group(1).strip() if match else ""


def resolve_dynamic_tex_value(value: str, *, iso_date: bool = False) -> str:
    """Resolve the small dynamic TeX vocabulary supported by metadata exports."""
    stripped = value.strip()
    today = date.today()
    if stripped == r"\today":
        return today.isoformat() if iso_date else today.isoformat()
    if stripped == r"\number\year":
        return str(today.year)
    return stripped


def parse_authors(text: str) -> list[dict[str, str]]:
    authors: list[dict[str, str]] = []
    pattern = r"\\INSRAddAuthor\s*\{(.*?)\}\s*(?=\\INSRAddAuthor|\\INSRAddInstitution|$)"
    for block in re.findall(pattern, text, re.S):
        authors.append(
            {
                "name": braced_value(block, "name"),
                "orcid": braced_value(block, "orcid"),
                "short_name": braced_value(block, "short-name"),
                "roles": braced_value(block, "roles"),
            }
        )
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

    publication_date = resolve_dynamic_tex_value(
        braced_value(text, "publication/date"),
        iso_date=True,
    )
    publication_year = resolve_dynamic_tex_value(braced_value(text, "publication/year"))
    if not publication_year and publication_date:
        match = re.search(r"(\d{4})", publication_date)
        publication_year = match.group(1) if match else ""

    return {
        "title": braced_value(text, "metadata/title"),
        "subtitle": braced_value(text, "metadata/subtitle"),
        "version": braced_value(text, "publication/version"),
        "status": braced_value(text, "publication/status"),
        "date": publication_date,
        "year": publication_year,
        "doi": doi,
        "repository": braced_value(text, "publication/repository"),
        "license": braced_value(text, "publication/license"),
        "publisher": braced_value(text, "publication/publisher")
        or braced_value(text, "metadata/institution"),
        "authors": parse_authors(text),
    }


def validate(data: dict[str, object]) -> list[str]:
    problems: list[str] = []
    for field in ("title", "version", "date", "year", "license", "repository"):
        if not data.get(field):
            problems.append(f"missing required metadata field: {field}")
    authors = data.get("authors", [])
    if not authors:
        problems.append("missing required metadata field: authors")
    for author in authors:
        if not author.get("name"):
            problems.append("author entry is missing name")
    if data.get("date") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(data["date"])):
        problems.append("publication date export must resolve to ISO YYYY-MM-DD")
    if data.get("year") and not re.fullmatch(r"\d{4}", str(data["year"])):
        problems.append("publication year export must resolve to YYYY")
    return problems


def cff(data: dict[str, object]) -> str:
    lines = [
        "cff-version: 1.2.0",
        f"title: {data['title']}",
        f"version: {data['version']}",
        f"date-released: {data['date']}",
        f"license: {data['license']}",
        "authors:",
    ]
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
        "creators": [
            {
                "name": author["name"],
                **(
                    {
                        "nameIdentifiers": [
                            {
                                "nameIdentifier": f"https://orcid.org/{author['orcid']}",
                                "nameIdentifierScheme": "ORCID",
                            }
                        ]
                    }
                    if author.get("orcid")
                    else {}
                ),
            }
            for author in data["authors"]
        ],
        "publisher": data.get("publisher"),
        "publicationYear": data.get("year"),
        "version": data.get("version"),
        "rightsList": [{"rights": data.get("license")}],
    }
    if data.get("doi"):
        out["doi"] = data["doi"]
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def codemeta(data: dict[str, object]) -> str:
    out = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode",
        "name": data["title"],
        "version": data["version"],
        "datePublished": data["date"],
        "license": data["license"],
        "codeRepository": data["repository"],
        "author": [
            {
                "@type": "Person",
                "name": author["name"],
                **(
                    {"identifier": f"https://orcid.org/{author['orcid']}"}
                    if author.get("orcid")
                    else {}
                ),
            }
            for author in data["authors"]
        ],
    }
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def export_all(outdir: Path) -> int:
    data = metadata()
    problems = validate(data)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
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
    for name in ("export-cff", "export-datacite", "export-codemeta", "export-all"):
        command = sub.add_parser(name)
        command.add_argument("--outdir", default="build/metadata")
    args = parser.parse_args()
    data = metadata()

    if args.command == "validate":
        problems = validate(data)
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print("metadata validation passed")
        return 0

    outdir = ROOT / args.outdir
    if args.command == "export-all":
        return export_all(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    target = {
        "export-cff": ("CITATION.cff", cff),
        "export-datacite": ("datacite.json", datacite),
        "export-codemeta": ("codemeta.json", codemeta),
    }[args.command]
    (outdir / target[0]).write_text(target[1](data), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
