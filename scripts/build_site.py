#!/usr/bin/env python3
"""Merge official-website bibliographies into the site and write site/index.html.

Reads site/data.json (OpenAlex aggregate from aggregate.py) and data/direct-publications/*.json.
Writes:
  site/index.html            template + embedded summary data
  site/pubs/<lab-id>.json    full official-site bibliography per lab, loaded on demand
"""
import json
import re
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_direct_publications import content_warnings  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SRC = DATA / "direct-publications"
SITE = ROOT / "site"
RECENT = 8
OTHER_TYPE_RE = re.compile(
    r"patent|award|invited.talk|thes[ei]s|theses|book|exhibition|software|"
    r"technology.transfer|art.competition|technical.report|white.paper",
    re.I,
)
BAD_LAB_NAME_RE = re.compile(r"^(homepage|home|index)$|404|page not found", re.I)

PI_FIXES = {
    "mit-97": ("Evelyn N. Wang", None),
    "stanford-17": ("Steve Jones", None),
    "oxford-8": ("Robert Baines", None),
    "delft-26": ("V.A. (Vera) Popovich", None),
    "imperial-44": ("Ferdinando Rodriguez y Baena", None),
    "postech-22": ("장진아", "Jinah Jang"),
}

VERIFIED_LAB_ENRICHMENTS = {
    "kaist-0": {
        "lab": "Machine Intelligence & Novel sensor Technology Laboratory (MINT)",
        "url": "http://mint.kaist.ac.kr/",
        "topics": ["마이크로·나노 가공과 첨단 제조", "초저전력·집적 전자코", "로봇·인간 증강용 웨어러블 센서", "바이오메디컬 센서·임상 시스템"],
    },
    "kaist-1": {
        "lab": "AiM⁴ Lab | Laboratory for AI-powered Modeling in Mechanics, Materials, and Manufacturing",
        "url": "https://sites.google.com/site/seunghwalab/",
        "topics": ["물리 기반 AI·대리모델", "생성형·역설계", "멀티스케일 역학·재료 모델링", "공학 최적화"],
    },
    "kaist-9": {
        "lab": "Biorobotics Laboratory",
        "url": "https://biorobotics.kaist.ac.kr/",
        "topics": ["생체신호 기반 인간–로봇 상호작용", "햅틱·로봇 지각·촉각 학습", "건강·생체역학용 웨어러블 센서", "소프트 로보틱스"],
    },
    "kaist-30": {
        "lab": "Dynamic Robot Control & Design Lab (DRCD)",
        "url": "https://www.dynamicrobot.kaist.ac.kr/",
        "topics": ["다족 보행 로봇", "구동기·메커니즘 설계", "동적 제어 및 학습 기반 보행"],
    },
    "snu-3": {
        "lab": "AI주도 시뮬레이션 및 설계 연구실 (AISDL)",
        "url": "https://aisdl.snu.ac.kr/",
        "topics": ["DNA/RNA 구조 나노기술", "전산역학·과학적 머신러닝", "산업 인공지능", "기계적 메타물질"],
    },
    "snu-22": {
        "lab": "인터랙티브/네트워크 로보틱스 연구실 (INRoL)",
        "url": "https://www.inrol.snu.ac.kr/",
        "topics": ["로봇 역학·제어", "공중 로봇·조작", "햅틱·증강현실·가상현실", "자율 로봇·센서 융합"],
    },
    "snu-28": {
        "lab": "바이오로보틱스 연구실 (Bioinspired Embodied Intelligence Robotics Lab)",
        "url": "https://www.biorobotics.snu.ac.kr/",
        "topics": ["소프트·생체모방 로보틱스", "웨어러블 보조 로봇", "로봇 의수·전개형 로봇"],
    },
    "postech-20": {
        "lab": "Extreme Mechanics 연구실 (Extreme Mechanics Lab)",
        "url": "https://www.xml-postech.com/",
        "topics": ["얇은 구조물의 대변형·불안정성·셸 좌굴", "형상변형 구조·스마트 재료", "소프트 액추에이터·센서", "유체–고체 상호작용"],
    },
    "postech-24": {
        "lab": "열 및 에너지시스템 연구실 (Thermal Engineering & Energy Conversion Lab)",
        "url": "https://www.telab-postech.com/",
        "topics": ["열화학적 수소·연료 생산", "고체상 냉각·극저온 냉동", "스핀 칼로리트로닉스", "열전 변환·열수송·열관리"],
    },
    "nus-1": {
        "lab": "Baek Research Group (The Baek Lab)",
        "url": "https://thebaeklab.com/",
        "topics": ["에너지 전환용 전기촉매·전극", "AI 기반 소재 발견·시스템 최적화", "오페란도 반응 분석", "핵심 금속의 전기화학적 회수"],
    },
    "nus-2": {
        "lab": "Soft Robotics Lab",
        "url": "https://www.softroboticslab.info/",
        "topics": ["생체모방 연성 로봇·센서·구동기", "연성 로봇 모델링·적응제어·AI", "해양 관측용 수중 로봇", "의료·돌봄 보조 로봇팔"],
    },
    "ntu-32": {
        "lab": "Miniature Soft Robotics Lab",
        "url": "https://sites.google.com/site/ntuminiaturesoftroboticslab/",
        "topics": ["미세 물체 조작용 소형 소프트 로봇", "자기 구동·형상 프로그래밍", "유연 메커니즘·정밀 위치 제어", "약물전달·최소침습 수술 로봇"],
    },
    "ntu-74": {
        "lab": "Multimodal Embodied AI and Robotic Systems (MARS Lab)",
        "url": "https://marslab.tech/",
        "topics": ["신뢰성 높은 로봇 학습·정밀 조작", "휴머노이드 보행·조작 통합", "멀티모달 지각·월드모델·계획", "인간 의도·시선·언어 기반 상호작용"],
    },
    "eth-14": {
        "lab": "Robotic Systems Lab (RSL)",
        "url": "https://rsl.ethz.ch/",
        "topics": ["팔·다리 로봇 설계·동적 구동", "이동·조작 제어와 학습", "자율 항법용 지각", "험지·위험 환경의 자율성"],
    },
    "eth-17": {
        "lab": "Soft Robotics Lab (SRL)",
        "url": "https://srl.ethz.ch/",
        "topics": ["생체하이브리드 로봇", "연성 구동기·설계·제작", "유체·전기 구동과 모델 기반·모델프리 제어", "머신러닝을 통한 로봇 기술 학습"],
    },
    "mit-1": {
        "lab": "Design Computation and Digital Engineering (DeCoDE) Lab",
        "url": "https://decode.mit.edu/",
        "topics": ["AI 기반 공학 설계·생성 모델", "설계 최적화", "멀티모달 표현 및 인간–AI 협업 설계"],
    },
    "mit-97": {
        "lab": "Device Research Lab (DRL)",
        "url": "https://drl.mit.edu/",
        "topics": ["열·물질 전달 및 열관리", "태양열 시스템", "물 수확 및 담수화"],
    },
    "stanford-20": {
        "lab": "Living Matter Lab",
        "url": "https://livingmatter.stanford.edu/",
        "topics": ["전산 생체역학", "물리 기반 모델링 및 구성 신경망", "생체 시스템 머신러닝"],
    },
    "stanford-22": {
        "lab": "Mani Research Lab",
        "url": "https://manigroup.stanford.edu/",
        "topics": ["난류 수송 및 유체 역학", "고정밀 수치 시뮬레이션", "예측 모델링"],
    },
}


def text(v):
    return re.sub(r"\s+", " ", str(v or "")).strip()


def name_key(name):
    """'KIM, Dae Gyoum' / 'Daegyoum Kim' / '김대겸 KIM, Dae Gyoum' -> 'kim|daegyoum' (initials dropped)."""
    name = re.sub(r"[-‐‑–.]", " ", name or "")
    name = re.sub(r"[^A-Za-z\s,]", " ", name).strip()
    if "," in name:
        sur, given = name.split(",", 1)
    else:
        parts = name.split()
        sur, given = (parts[-1], " ".join(parts[:-1])) if parts else ("", "")
    given = "".join(t for t in given.lower().split() if len(t) > 1)
    return f"{sur.strip().lower()}|{given}"


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def paper_row(p):
    row = {"t": text(p.get("title")) or None, "y": p.get("year"), "c": text(p.get("citation_raw"))[:900]}
    link = text(p.get("doi_or_url"))
    if re.match(r"https?://", link):
        row["d"] = link
    if p.get("year_type") == "page_section":
        row["ys"] = 1
    return row


def clean_lab_name(name):
    s = text(name)
    s = re.sub(r":\s*Homepage$", "", s, flags=re.I).strip()
    if not s or BAD_LAB_NAME_RE.search(s):
        return None
    return s


def summarize(rec, rec_id):
    raw_papers = rec.get("papers") or []
    seen = set()
    papers = []
    other_count = 0
    for p in raw_papers:
        if not isinstance(p, dict) or not text(p.get("citation_raw")):
            continue
        if content_warnings(p):
            continue
        key = text(p["citation_raw"]).casefold()
        if key in seen:
            continue
        seen.add(key)
        output_type = text(p.get("publication_type")).casefold()
        if OTHER_TYPE_RE.search(output_type):
            other_count += 1
        else:
            papers.append(p)
    rows = [paper_row(p) for p in papers]
    rows_sorted = sorted(rows, key=lambda r: -(r["y"] or 0))
    years = [r["y"] for r in rows if isinstance(r["y"], int)]
    urls = [u for u in (rec.get("publication_urls") or [rec.get("publication_url")]) if u and re.match(r"https?://", u)]
    out = {
        "rid": rec_id,
        "status": rec.get("status"),
        "n": len(rows),
        "auto": rec.get("extraction", "").startswith("auto"),
        "src": urls[:4],
        "acc": text(rec.get("accessed_at"))[:10] or None,
        "note": text(rec.get("coverage_notes"))[:400] if isinstance(rec.get("coverage_notes"), str) else None,
        "span": [min(years), max(years)] if years else None,
        "recent": rows_sorted[:RECENT],
    }
    if other_count:
        out["other"] = other_count
    return out, rows_sorted


def main():
    D = json.loads((SITE / "data.json").read_text(encoding="utf-8"))
    pubs_dir = SITE / "pubs"
    if pubs_dir.exists():
        shutil.rmtree(pubs_dir)
    pubs_dir.mkdir()

    for lab in D["labs"]:
        if lab["id"] in PI_FIXES:
            pi_fixed, en_fixed = PI_FIXES[lab["id"]]
            lab["pi"] = pi_fixed
            if en_fixed is not None:
                lab["en"] = en_fixed

    labs_by_id = {l["id"]: l for l in D["labs"]}
    kaist_site = {name_key(l.get("en") or l["pi"]): l for l in D["labs"] if l["u"] == "kaist"}
    eth_map = load(SRC / "progress" / "eth-official-lab-map.json") or {"labs": []}
    attached = 0
    added = 0
    for path in sorted(SRC.glob("*.json")):
        m = re.fullmatch(r"([a-z]+)-([1-9]\d*)\.json", path.name)
        if not m:
            continue
        rec = load(path)
        if not isinstance(rec, dict) or "papers" not in rec:
            continue
        uni, idx = m.group(1), int(m.group(2))
        rec_id = f"{uni}-{idx}"
        if uni == "kaist":
            pi = text(rec.get("pi"))
            ko = re.match(r"^([가-힣]+)\s+(.*)$", pi)
            lab = kaist_site.get(name_key(pi))
            if lab is None:
                # Official KAIST roster member missing from the earlier inferred roster.
                lab = {"id": f"kaist-o{idx}", "u": "kaist", "pi": ko.group(1) if ko else pi,
                       "en": ko.group(2) if ko else None, "lab": clean_lab_name(rec.get("lab_name")), "url": rec.get("lab_url"),
                       "area": None, "second": None, "status": "unverified", "scope": False, "n": 0,
                       "topics": [], "topicSrc": "openalex", "venues": [], "recent": [], "official": True}
                D["labs"].append(lab)
                labs_by_id[lab["id"]] = lab
                kaist_site[name_key(pi)] = lab
                added += 1
            else:
                if ko:
                    if not re.search(r"[가-힣]", lab.get("pi") or ""):
                        lab["en"] = lab.get("pi") or ko.group(2)
                        lab["pi"] = ko.group(1)
                lab["official"] = True
                if lab.get("status") == "unofficial":
                    lab["status"] = "matched"
        else:
            lab = labs_by_id.get(f"{uni}-{idx - 1}")
        if lab is None:
            continue
        summary, rows = summarize(rec, rec_id)
        if lab.get("dp") and lab["dp"]["n"] >= summary["n"]:
            continue
        lab["dp"] = summary
        if rec.get("lab_url") and re.match(r"https?://", rec["lab_url"]):
            lab["url"] = rec["lab_url"]
        cleaned_name = clean_lab_name(rec.get("lab_name"))
        if cleaned_name and not lab.get("lab"):
            lab["lab"] = cleaned_name
        (pubs_dir / f"{lab['id']}.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        attached += 1

    # The earlier ETH roster had lab URLs shifted by one row; use the official D-MAVT lab map instead.
    for lab in D["labs"]:
        if lab["u"] != "eth":
            continue
        last = (lab["pi"] or "").split()[-1].lower().replace("ü", "u")
        hits = [x["url"].split("#")[0] for x in eth_map["labs"] if x.get("url") and last in x["name"].lower().replace("ü", "u")]
        if hits:
            lab["url"] = hits[0]

    # Apply verified official lab names, direct URLs, and official research topics from manual/Aside audits.
    for lab_id, info in VERIFIED_LAB_ENRICHMENTS.items():
        lab = labs_by_id.get(lab_id)
        if not lab:
            continue
        if info.get("lab"):
            lab["lab"] = info["lab"]
        if info.get("url"):
            lab["url"] = info["url"]
        if info.get("topics"):
            lab["topics"] = info["topics"]
            lab["topicSrc"] = "official"

    progress = load(DATA / "direct-publications-progress.json") or {}
    D["dpProgress"] = {
        "generated": text(progress.get("generated_at"))[:10],
        "totals": progress.get("totals", {}),
        "unis": [{"key": u["key"], "targets": u["targets"], **u["counts"]} for u in progress.get("universities", [])],
    }
    D["totals"]["dpLabs"] = sum(1 for l in D["labs"] if l.get("dp", {}).get("n"))
    D["totals"]["dpPapers"] = sum(l.get("dp", {}).get("n", 0) for l in D["labs"])
    D["totals"]["dpOther"] = sum(l.get("dp", {}).get("other", 0) for l in D["labs"])

    template = (SITE / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(D, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (SITE / "index.html").write_text(template.replace("__DATA__", payload), encoding="utf-8")
    size = (SITE / "index.html").stat().st_size
    print(f"attached {attached} official bibliographies, added {added} KAIST official-roster labs, "
          f"{D['totals']['dpPapers']} papers (+{D['totals']['dpOther']} other outputs); index.html {size/1e6:.2f} MB")


if __name__ == "__main__":
    main()
