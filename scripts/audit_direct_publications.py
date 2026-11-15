#!/usr/bin/env python3
"""Check extracted bibliography fields against saved browser-visible source text."""
import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "direct-publications"


def content_warnings(paper):
    """Flag obvious section-boundary errors without altering research evidence."""
    title = str(paper.get("title") or "")
    authors = str(paper.get("authors_raw") or "").strip().casefold()
    flags = []
    if len(title) > 600:
        flags.append("title_too_long_review_section_boundary")
    if re.search(r"Onderwijs.*(?:Media|Contact)|Back to top|Links voor studenten|Contactgegevens", title, re.S):
        flags.append("title_contains_navigation_sections")
    if authors in {"prizes", "zoeken", "onderwijs", "media", "contact", "read more", "lees meer", "publications"}:
        flags.append("authors_are_navigation_text")
    return flags


def normalized(value):
    return re.sub(r"\s+", " ", unicodedata.normalize(
        "NFKC", html.unescape(str(value or "")).replace("\\n", "\n")
    )).strip().casefold()


def audit():
    records = []
    for path in sorted(SOURCE.glob("*.json")):
        if not re.fullmatch(r"[a-z]+-[1-9]\d*\.json", path.name):
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue  # An active collection job may still be writing this file.
        if not isinstance(data, dict) or not data.get("papers"):
            continue
        evidence_paths = [path.with_suffix(suffix) for suffix in
                          (".txt", ".visible.txt", ".sources.txt", ".source.txt")]
        evidence_paths = [candidate for candidate in evidence_paths if candidate.exists()]
        evidence = normalized("\n".join(candidate.read_text() for candidate in evidence_paths))
        issues = []
        for number, paper in enumerate(data["papers"], 1):
            title = normalized(paper.get("title"))
            citation = normalized(paper.get("citation_raw"))
            flags = content_warnings(paper)
            if not evidence:
                flags.append("missing_saved_visible_text")
            elif title and title not in evidence:
                flags.append("title_not_found_verbatim_in_saved_text")
            if not citation:
                flags.append("missing_original_citation")
            if not paper.get("source_url"):
                flags.append("missing_source_url")
            if not title:
                flags.append("title_unparsed_original_citation_preserved")
            if flags:
                issues.append({"record_number": number, "title": paper.get("title"), "flags": flags})
        records.append({
            "file": str(path.relative_to(ROOT)), "pi": data.get("pi"),
            "posted_entries": len(data["papers"]), "coverage_status": data.get("status"),
            "evidence_files": [str(candidate.relative_to(ROOT)) for candidate in evidence_paths], "issues": issues,
        })
    result = {
        "method": "Local consistency checks against saved Aside Browser text; not an independent website audit.",
        "records_with_entries": len(records),
        "posted_entries": sum(item["posted_entries"] for item in records),
        "flagged_entries": sum(len(item["issues"]) for item in records),
        "entries_with_unparsed_title": sum(
            "title_unparsed_original_citation_preserved" in issue["flags"]
            for item in records for issue in item["issues"]),
        "entries_with_evidence_issue": sum(
            any(flag != "title_unparsed_original_citation_preserved" for flag in issue["flags"])
            for item in records for issue in item["issues"]),
        "records": records,
    }
    (ROOT / "data" / "direct-publications-audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print({key: result[key] for key in ("records_with_entries", "posted_entries", "flagged_entries")})


if __name__ == "__main__":
    audit()
