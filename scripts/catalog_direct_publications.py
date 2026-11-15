#!/usr/bin/env python3
"""Catalog bibliographies captured from official websites through Aside Browser.

This script only reads direct-publications/*.json; it never reads OpenAlex files.
Run after a collection batch to refresh the JSON catalog and readable bibliography.
"""
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from audit_direct_publications import content_warnings

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "direct-publications"


def text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def web_url(value):
    value = text(value)
    return value if urlsplit(value).scheme in {"https", "http"} else None


def coverage_text(value):
    if isinstance(value, list):
        return " / ".join(coverage_text(item) for item in value)
    if isinstance(value, dict):
        parts = [text(value.get(key)) for key in ("method", "filters", "excluded")]
        for source in value.get("publication_sources", []):
            parts.append(f"{source.get('type')}: {source.get('record_count')}건, "
                         f"{len(source.get('pages_visited', []))}페이지 확인")
        return " / ".join(part for part in parts if part)
    return text(value)


def catalog():
    labs = []
    problems = []
    withheld = []
    for path in sorted(SOURCE.glob("*.json")):
        if not re.fullmatch(r"[a-z]+-[1-9]\d*\.json", path.name):
            continue
        try:
            lab = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(lab, dict) or "papers" not in lab:
                continue
            if not text(lab.get("pi")):
                raise ValueError("missing pi")
            if lab.get("status") not in {"complete", "partial", "blocked"}:
                raise ValueError("status must be complete, partial, or blocked")
            seen = set()
            papers = []
            other_outputs = []
            for index, paper in enumerate(lab["papers"], 1):
                if not isinstance(paper, dict):
                    raise ValueError(f"paper {index}: expected an object")
                source_url = web_url(paper.get("source_url"))
                if not source_url:
                    raise ValueError(f"paper {index}: missing source_url")
                if not text(paper.get("citation_raw")):
                    raise ValueError(f"paper {index}: missing citation_raw")
                warnings = content_warnings(paper)
                if warnings:
                    withheld.append({"record_file": str(path.relative_to(ROOT)),
                                     "record_number": index, "source_url": source_url,
                                     "reasons": warnings})
                    continue
                key = text(paper["citation_raw"]).casefold()
                if key in seen:
                    continue
                seen.add(key)
                output_type = text(paper.get("publication_type")).casefold()
                if re.search(r"patent|award|invited.talk|thes[ei]s|theses|book|exhibition|software|technology.transfer|art.competition|technical.report|white.paper", output_type):
                    other_outputs.append(paper)
                else:
                    papers.append(paper)
            labs.append({**lab, "papers": papers, "other_outputs": other_outputs,
                         "record_file": str(path.relative_to(ROOT))})
        except (ValueError, TypeError, KeyError) as error:
            problems.append(f"{path.name}: {error}")
    if problems:
        raise SystemExit("Invalid research records:\n" + "\n".join(problems))

    total = sum(len(lab["papers"]) for lab in labs)
    result = {
        "method": "Aside Browser: official professor/lab publication pages",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "research_records": len(labs),
        "labs_with_posted_entries": sum(bool(lab["papers"]) for lab in labs),
        "coverage_status_counts": dict(Counter(lab["status"] for lab in labs)),
        "paper_lab_records": total,
        "other_output_records": sum(len(lab["other_outputs"]) for lab in labs),
        "withheld_for_review": withheld,
        "count_note": "A paper appearing on multiple lab websites remains associated with each lab.",
        "labs": labs,
    }
    (ROOT / "data" / "direct-publications-index.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# 공식 교수·연구실 웹사이트 논문 조사",
        "",
        f"웹페이지 메뉴·다른 섹션이 섞인 것으로 의심되는 {len(withheld)}개 항목은 "
        "검수 전까지 이 목록에서 제외하고 원본 조사 파일에 보존했습니다.",
        "",
        f"연구실 조사 기록 {len(labs)}개 · 게시 항목을 확보한 연구실 "
        f"{result['labs_with_posted_entries']}개 · 연구실별 논문·원고 기록 {total:,}건",
        "",
        "**수집·검수 진행 중입니다.** 아래의 complete는 해당 사이트의 게시 목록 수집 상태이며, "
        "전체 대학 조사 완료나 교수의 평생 전체 논문을 보증하는 표시는 아닙니다.",
        "",
        "Aside 브라우저로 확인한 Publications/Papers 페이지의 게시 목록입니다. "
        "게시된 목록의 범위는 연구실별 메모에 표시합니다. "
        "같은 논문이 여러 연구실에 게시되면 각 연구실에 남깁니다.",
        "교수 프로필만 확인한 partial 기록은 논문 목록 수집 완료를 뜻하지 않습니다. "
        "공식 사이트의 논문 메뉴에 함께 게시된 원고·발표·기타 항목은 원문 표현과 유형을 확인하세요.",
        f"특허·수상·학위논문·도서·초청강연 등으로 유형이 명시된 "
        f"{result['other_output_records']:,}건은 이 논문 목록에서 분리했습니다. "
        "원본 조사 파일과 JSON 합본의 other_outputs에 보존되어 있습니다.",
        "",
    ]
    groups = defaultdict(list)
    grouped_lines = defaultdict(list)
    for lab in labs:
        groups[lab.get("university_key", "unknown")].append(lab)
    lines.extend(["[대학별 조사 진행 현황](direct-publications-progress.md)", ""])
    for key, university_labs in sorted(groups.items()):
        name = text(university_labs[0].get("university"))
        count = sum(len(lab["papers"]) for lab in university_labs)
        lines.append(f"- [{name}: {count:,}개 게시 기록](bibliographies/{key}.md)")
    lines.append("")
    for lab in labs:
        start = len(lines)
        lines.extend([
            f"## {text(lab.get('university'))} — {text(lab['pi'])}",
            "",
            f"{text(lab.get('lab_name'))} · 논문·원고 {len(lab['papers']):,}건 · "
            f"기타 성과 {len(lab['other_outputs']):,}건 · 상태: {lab['status']}",
            "",
            f"확인일: {text(lab.get('accessed_at'))}",
            "",
            f"수집 범위: {coverage_text(lab.get('coverage_notes'))}",
            "",
        ])
        urls = lab.get("publication_urls") or [lab.get("publication_url")]
        for url in urls:
            if web_url(url):
                lines.extend([f"출처: <{url}>", ""])
        for index, paper in enumerate(lab["papers"], 1):
            # Render the original citation so ambiguous punctuation in parsed fields
            # never removes part of a title or changes the website's bibliography.
            citation = text(paper["citation_raw"].replace("\\n", "\n"))
            # Repeated 1. markers let Markdown number long lists while keeping
            # continuation indentation correct after 9, 99, and 999 entries.
            lines.extend([f"1. {citation}", ""])
            status = paper.get("publication_status_raw") or paper.get("publication_status")
            if status:
                lines.append(f"    게시 상태: {text(status)}")
            if paper.get("year_type") == "page_section":
                lines.append("    연도는 사이트의 분류 제목 기준이며, 개별 게재연도는 미표기입니다.")
            link = web_url(paper.get("doi_or_url"))
            if link:
                lines.append(f"    논문: <{link}>")
            lines.extend([f"    게시 페이지: <{paper['source_url']}>", ""])
        grouped_lines[lab.get("university_key", "unknown")].extend(lines[start:])
    export_dir = ROOT / "data" / "bibliographies"
    export_dir.mkdir(exist_ok=True)
    for key, contents in grouped_lines.items():
        name = text(groups[key][0].get("university"))
        header = [f"# {name} — 공식 웹사이트 게시 목록", "",
                  "수집·검수 진행 중입니다. 연구실별 상태와 게시 범위를 확인하세요.", "",
                  "[전체 진행 현황](../direct-publications-progress.md) · [전체 목록](../direct-publications.md)", ""]
        (export_dir / f"{key}.md").write_text("\n".join(header + contents) + "\n", encoding="utf-8")
    (ROOT / "data" / "direct-publications.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(f"Cataloged {len(labs)} lab records and {total} paper/lab records.")


if __name__ == "__main__":
    catalog()
