#!/usr/bin/env python3
"""Turn captured page text into data/direct-publications/<lab-id>.json records.

usage: save_captures.py CAPTURE.json [CAPTURE.json ...] [--blocked LAB_ID=reason ...] [--force] [--strict]

--strict keeps only strongly citation-like entries (for profile/home pages that mix in CV or news text).

CAPTURE.json maps a lab id (e.g. "eth-15") to a list of {url, requested?, text} page captures
taken from the lab's official publication pages. Pages of the same lab across files are merged.
Existing records that already hold papers are kept unless --force is given.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_visible_text import best_entries, VENUE_HINT, looks_like_authors  # noqa: E402

JUNK = re.compile(r"present\b|lecturer|congratulat|we released|min read|\bguide\b|obtained his|obtained her|joined|award|fellow\b|"
                  r"impact factor|quartile|committee|\bchair\b|editor|visiting|professor|ph\.?d\.? in|b\.?s\.? in", re.I)


def strong(citation):
    """Citation-like (venue hint, author list or quoted title) and free of CV/news wording."""
    return bool(VENUE_HINT.search(citation) or looks_like_authors(citation[:250]) or "“" in citation) \
        and not JUNK.search(citation)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "direct-publications"
UNIVERSITY = {"mit": "MIT", "stanford": "Stanford University", "nus": "National University of Singapore",
              "cambridge": "University of Cambridge", "ntu": "Nanyang Technological University", "eth": "ETH Zurich",
              "harvard": "Harvard University", "oxford": "University of Oxford", "delft": "Delft University of Technology",
              "imperial": "Imperial College London", "snu": "Seoul National University", "kaist": "KAIST", "postech": "POSTECH"}


def roster(uni):
    path = OUT / "kaist-official-roster.json" if uni == "kaist" else DATA / f"roster-{uni}.json"
    return json.loads(path.read_text(encoding="utf-8"))["labs"]


def main(argv):
    force = "--force" in argv
    strict = "--strict" in argv
    blocked = {}
    files = []
    args = iter(a for a in argv if a not in ("--force", "--strict"))
    for a in args:
        if a == "--blocked":
            k, _, v = next(args).partition("=")
            blocked[k] = v
        else:
            files.append(a)
    captures = {}
    for f in files:
        for lab_id, pages in json.loads(Path(f).read_text(encoding="utf-8")).items():
            lab_id = re.sub(r"[a-z]$", "", lab_id)  # allow eth-35a style partial keys
            captures.setdefault(lab_id, []).extend(pages)
    now = datetime.now(timezone.utc).isoformat()
    rosters = {}
    for lab_id, pages in sorted(captures.items()):
        uni, idx = lab_id.rsplit("-", 1)
        idx = int(idx)
        path = OUT / f"{lab_id}.json"
        old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        if old.get("papers") and not force:
            print("keep existing", lab_id, len(old["papers"]))
            continue
        person = rosters.setdefault(uni, roster(uni))[idx - 1]
        ok = [p for p in pages if p.get("text") and not str(p.get("url", "")).startswith("chrome-error")]
        papers, seen = [], set()
        for page in ok:
            for e in best_entries(page["text"]):
                key = re.sub(r"\W+", "", e["citation_raw"].casefold())
                if key in seen or (strict and not strong(e["citation_raw"])):
                    continue
                seen.add(key)
                row = {"title": e.get("title"), "year": e.get("year"), "citation_raw": e["citation_raw"],
                       "source_url": page["url"]}
                if e.get("year_type"):
                    row["year_type"] = e["year_type"]
                papers.append(row)
        if lab_id in blocked and not papers:
            status, note = "blocked", blocked[lab_id]
        elif not papers:
            status, note = "partial", "공식 사이트에서 논문 목록을 찾지 못함(프로필·연구실 홈만 확인)."
        else:
            status = "partial"
            note = (f"공식 연구실 논문 페이지 {len(ok)}개(페이지네이션 포함)를 Aside 브라우저로 열어 화면 텍스트를 저장하고 "
                    "parse_visible_text.py로 인용 항목을 자동 분리함. 제목·연도는 자동 추출값이며 원문 인용(citation_raw)을 보존. "
                    "항목별 사람 검수 전이므로 partial.")
        record = {k: v for k, v in old.items() if k not in ("papers", "status", "coverage_notes", "accessed_at")}
        record.update({
            "university": old.get("university") or UNIVERSITY.get(uni, uni), "university_key": uni,
            "pi": old.get("pi") or person.get("pi") or person.get("name"),
            "lab_name": old.get("lab_name") or ", ".join(person.get("labs") or []) or None,
            "lab_url": old.get("lab_url") or person.get("url"),
            "publication_urls": list(dict.fromkeys(p.get("requested") or p["url"] for p in pages)),
            "accessed_at": now, "coverage_notes": note, "status": status,
            "investigation_stage": "full_site_attempted", "extraction": "auto_heuristic_v1", "papers": papers,
        })
        if old.get("coverage_notes") and old.get("coverage_notes") != note:
            record["previous_coverage_notes"] = old["coverage_notes"]
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if ok:
            (OUT / f"{lab_id}.visible.txt").write_text(
                "\n\n".join(f"=== {p['url']}\n{p['text']}" for p in ok), encoding="utf-8")
        print(lab_id, status, len(papers))


if __name__ == "__main__":
    main(sys.argv[1:])
