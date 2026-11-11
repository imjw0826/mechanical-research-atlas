#!/usr/bin/env python3
"""Resolve a university roster to OpenAlex authors and fetch their works since 2022.

Usage: openalex_fetch.py <roster.json> <institution_ror> <out.json>
"""
import json
import math
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.openalex.org"
SINCE = "2022-01-01"
FIELDS = "id,title,publication_year,doi,type,primary_location,authorships,primary_topic"
spent = 0.0


def api_key():
    with open(os.path.join(ROOT, ".env")) as f:
        for line in f:
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("OPENALEX_API_KEY missing")


KEY = api_key()


def get(path, params):
    global spent
    query = urllib.parse.urlencode({**params, "api_key": KEY})
    url = f"{API}/{path}?{query}"
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-directory/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r)
            spent += data.get("meta", {}).get("cost_usd") or 0
            time.sleep(0.12)
            return data
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 4:
                time.sleep(2 ** attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < 4:
                time.sleep(2 ** attempt)
                continue
            raise


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z ]", " ", s.replace("-", "").replace("‐", "")).split()


def to_query(name):
    if "," in name:
        last, first = [p.strip() for p in name.split(",", 1)]
        return f"{first} {last}"
    return name.strip()


def name_matches(target, candidate):
    """Accept same tokens in any order, or initials plus an identical family name."""
    t, c = norm(target), norm(candidate)
    if not t or not c:
        return False
    if sorted("".join(t)) == sorted("".join(c)) and set(t) & set(c):
        return True
    if t[-1] != c[-1]:
        return False
    if "".join(t[:-1]) == "".join(c[:-1]):
        return True
    given_t, given_c = t[:-1], c[:-1]
    if all(len(x) == 1 for x in given_t) and given_t and len(given_c) >= 1:
        return "".join(given_t) == "".join(x[0] for x in given_c)[:len(given_t)]
    return False


FIELD_WEIGHT = {
    "Engineering": 1.0, "Materials Science": 0.8, "Energy": 0.8, "Physics and Astronomy": 0.6,
    "Chemical Engineering": 0.6, "Computer Science": 0.5, "Mathematics": 0.3,
    "Biochemistry, Genetics and Molecular Biology": 0.1, "Chemistry": 0.2,
    "Medicine": -1.0, "Social Sciences": -1.0, "Arts and Humanities": -1.0,
    "Psychology": -0.8, "Business, Management and Accounting": -0.8, "Economics, Econometrics and Finance": -0.8,
    "Agricultural and Biological Sciences": -0.3, "Nursing": -1.0, "Health Professions": -0.8, "Dentistry": -1.0,
}
KO_HINTS = {
    "로봇": "robot robotic control manipulator", "컴퓨터비전": "vision image visual recognition",
    "비전": "vision image visual", "열": "heat thermal energy", "유체": "fluid flow turbulent",
    "바이오": "cell biological biomedical", "생체": "cell biological biomedical",
    "음향": "acoustic noise vibration", "설계": "design manufacturing", "생산": "manufacturing printing",
    "에너지": "energy battery fuel solar", "자동차": "engine vehicle combustion", "자율주행": "vehicle autonomous",
    "광학": "optical imaging microscopy", "이미징": "optical imaging microscopy", "전산역학": "computational mechanics dna",
    "나노": "nano thermal phonon", "연료전지": "fuel cell", "냉동": "refrigeration",
}


def hint_tokens(lab):
    text = " ".join([str(lab.get("major") or "")] + list(lab.get("labs") or []) + list(lab.get("topics") or []))
    extra = " ".join(v for k, v in KO_HINTS.items() if k in text)
    return {t for t in re.findall(r"[a-z]{4,}", (text + " " + extra).lower())}


def score(author, hints):
    topics = author.get("topics") or []
    total = sum(t.get("count") or 0 for t in topics) or 1
    field = sum(FIELD_WEIGHT.get((t.get("field") or {}).get("display_name"), 0) * (t.get("count") or 0) for t in topics) / total
    names = " ".join(t.get("display_name", "") for t in topics[:10]).lower()
    return field + sum(1.5 for h in hints if h in names)


def resolve(lab, ror):
    q = to_query(lab.get("pi_en") or lab["pi"])
    data = get("authors", {
        "search": q,
        "filter": f"affiliations.institution.ror:https://ror.org/{ror}",
        "per-page": 25,
        "select": "id,display_name,display_name_alternatives,works_count,cited_by_count,topics",
    })
    matched = []
    for a in data.get("results", []):
        names = [a.get("display_name")] + (a.get("display_name_alternatives") or [])
        if any(name_matches(q, n) for n in names if n):
            matched.append(a)
    if not matched:
        return [], "not_found", 0
    hints = hint_tokens(lab)
    # Field fit decides who this is; publication volume breaks ties so one-paper fragments never win.
    def key(a):
        return score(a, hints) * math.log1p(a.get("works_count") or 0)
    ranked = sorted(matched, key=key, reverse=True)
    best = ranked[0]
    if score(best, hints) <= 0:
        return [best], "low_confidence", len(matched)
    top = {t.get("display_name") for t in (best.get("topics") or [])[:5]}
    fragments = [a for a in ranked[1:] if top & {t.get("display_name") for t in (a.get("topics") or [])[:5]}]
    group = [best] + fragments
    if len(matched) == 1:
        return group, "matched", 1
    runner = next((a for a in ranked[1:] if a not in fragments), None)
    clear = runner is None or key(best) >= 2 * max(key(runner), 0.01)
    return group, "matched_by_field" if clear else "ambiguous", len(matched)


def works_for(author_ids):
    out, cursor = [], "*"
    flt = f"authorships.author.id:{'|'.join(author_ids)},from_publication_date:{SINCE}"
    while cursor:
        data = get("works", {"filter": flt, "per-page": 200, "cursor": cursor, "select": FIELDS})
        out.extend(data.get("results", []))
        cursor = data.get("meta", {}).get("next_cursor")
        if not data.get("results"):
            break
    return out


def slim(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    topic = w.get("primary_topic") or {}
    return {
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "doi": w.get("doi"),
        "work_type": w.get("type"),
        "venue": src.get("display_name"),
        "venue_type": src.get("type"),
        "venue_id": src.get("id"),
        "topic": topic.get("display_name"),
        "subfield": (topic.get("subfield") or {}).get("display_name"),
        "field": (topic.get("field") or {}).get("display_name"),
    }


def main():
    roster_path, ror, out_path = sys.argv[1:4]
    roster = json.load(open(roster_path))
    labs = roster["labs"]
    for lab in labs:
        group, status, n = resolve(lab, ror)
        lab["match_status"] = status
        lab["match_candidates"] = n
        if group:
            lab["openalex_ids"] = [a["id"].rsplit("/", 1)[1] for a in group]
            lab["openalex_name"] = group[0]["display_name"]
            lab["openalex_topics"] = [t["display_name"] for t in (group[0].get("topics") or [])[:5]]
    ids = sorted({i for lab in labs for i in lab.get("openalex_ids", [])})
    by_author = {i: [] for i in ids}
    for start in range(0, len(ids), 50):
        chunk = ids[start:start + 50]
        chunk_set = set(chunk)
        for w in works_for(chunk):
            s = slim(w)
            for a in w.get("authorships") or []:
                aid = ((a.get("author") or {}).get("id") or "").rsplit("/", 1)[-1]
                if aid in chunk_set:
                    by_author[aid].append(s)
    for lab in labs:
        seen, works = set(), []
        for i in lab.get("openalex_ids", []):
            for s in by_author.get(i, []):
                k = s["doi"] or s["title"]
                if k not in seen:
                    seen.add(k)
                    works.append(s)
        works.sort(key=lambda s: -(s["year"] or 0))
        lab["publications"] = works
    roster["stage"] = "openalex"
    roster["openalex_since"] = SINCE
    json.dump(roster, open(out_path, "w"), ensure_ascii=False, indent=1)
    counts = {}
    for lab in labs:
        counts[lab["match_status"]] = counts.get(lab["match_status"], 0) + 1
    print(json.dumps({
        "labs": len(labs), "match": counts,
        "works": sum(len(l["publications"]) for l in labs),
        "cost_usd": round(spent, 4),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
