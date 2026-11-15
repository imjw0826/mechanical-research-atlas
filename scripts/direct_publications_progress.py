#!/usr/bin/env python3
"""Report bibliography coverage against every roster, including missing records."""
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_direct_publications import content_warnings  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "direct-publications"
OTHER_TYPE_RE = re.compile(
    r"patent|award|invited.talk|thes[ei]s|theses|book|exhibition|software|"
    r"technology.transfer|art.competition|technical.report|white.paper",
    re.I,
)


def text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def count_outputs(result):
    if not result:
        return 0, 0
    seen = set()
    papers = 0
    other = 0
    for p in result.get("papers", []):
        if not isinstance(p, dict) or not text(p.get("citation_raw")):
            continue
        if content_warnings(p):
            continue
        key = text(p["citation_raw"]).casefold()
        if key in seen:
            continue
        seen.add(key)
        if OTHER_TYPE_RE.search(text(p.get("publication_type")).casefold()):
            other += 1
        else:
            papers += 1
    return papers, other


def load(path):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def main():
    roster_paths = sorted((ROOT / "data").glob("roster-*.json"))
    official_kaist = SOURCE / "kaist-official-roster.json"
    if official_kaist.exists():
        roster_paths.append(official_kaist)
    universities = []
    for roster_path in roster_paths:
        roster = load(roster_path)
        if not isinstance(roster, dict) or not isinstance(roster.get("labs"), list):
            raise SystemExit(f"Invalid roster: {roster_path}")
        key = "kaist" if roster_path == official_kaist else roster_path.stem.removeprefix("roster-")
        records = []
        counts = Counter()
        for index, person in enumerate(roster["labs"], 1):
            path = SOURCE / f"{key}-{index}.json"
            result = load(path)
            status = result.get("status", "pending") if result else "pending"
            if status not in {"complete", "partial", "blocked"}:
                status = "pending"
            counts[status] += 1
            entries, other_entries = count_outputs(result)
            counts["posted_entries"] += entries
            counts["other_outputs"] += other_entries
            counts["with_entries"] += bool(entries)
            stage = result.get("investigation_stage") if result else None
            counts["full_site_attempted"] += stage == "full_site_attempted" or status == "complete"
            records.append({
                "id": f"{key}-{index}", "pi": person.get("pi") or person.get("name"),
                "status": status, "posted_entries": entries,
                "other_outputs": other_entries,
                "investigation_stage": stage,
                "record_file": str(path.relative_to(ROOT)) if result else None,
            })
        universities.append({
            "key": key, "name": roster.get("university") or key,
            "targets": len(records), "counts": dict(counts), "labs": records,
        })
    totals = Counter()
    for university in universities:
        totals["targets"] += university["targets"]
        totals.update(university["counts"])
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "coverage_note": "complete means the researcher reported covering the website's posted list; partial includes profile-only discovery and unfinished extraction. blocked requires an access limitation. pending has no research record yet.",
        "totals": dict(totals), "universities": universities,
    }
    output = ROOT / "data" / "direct-publications-progress.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# 공식 웹사이트 논문 조사 진행 현황", "",
        "기존 13개 대학 전체 대상입니다. KAIST는 직접 확인한 최신 공식 명단을 사용합니다.", "",
        "전체 게시 목록 수집(complete), 후속 조사 필요(partial), 접근 제한(blocked), 미수집(pending)을 구분합니다. "
        "게시 기록에는 원고·발표·기타 항목이 포함될 수 있으며, 연구실 간 동일 논문은 별도 기록입니다.", "",
        "| 대학 | 대상 | 전체목록 조사 시도 | 전체 게시 목록 수집 | 후속 조사 필요 | 접근 제한 | 미수집 | 게시 기록 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for university in universities:
        c = university["counts"]
        lines.append(f"| {university['name']} | {university['targets']} | "
                     f"{c.get('full_site_attempted', 0)} | "
                     f"{c.get('complete', 0)} | {c.get('partial', 0)} | "
                     f"{c.get('blocked', 0)} | {c.get('pending', 0)} | {c.get('posted_entries', 0):,} |")
    lines.extend(["", "[수집한 논문 목록](direct-publications.md)", ""])
    (ROOT / "data" / "direct-publications-progress.md").write_text("\n".join(lines))
    print(dict(totals))


if __name__ == "__main__":
    main()
