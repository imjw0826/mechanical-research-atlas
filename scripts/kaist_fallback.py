#!/usr/bin/env python3
"""Build an unofficial KAIST ME roster from OpenAlex affiliation strings, because me.kaist.ac.kr is down."""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ["x"]
import openalex_fetch as oa  # noqa: E402

ROR = "05apxxy63"
MIN_PAPERS = 5


def is_kaist_me(authorship):
    for s in authorship.get("raw_affiliation_strings") or []:
        low = s.lower()
        if "mechanical" in low and ("kaist" in low or "korea advanced institute" in low):
            return True
    return False


def main():
    flt = f'raw_affiliation_strings.search:"Mechanical Engineering",authorships.institutions.ror:{ROR},from_publication_date:2023-01-01'
    counts, names, cursor, total = collections.Counter(), {}, "*", 0
    while cursor:
        data = oa.get("works", {"filter": flt, "per-page": 200, "cursor": cursor, "select": "id,authorships"})
        rows = data.get("results", [])
        total += len(rows)
        for w in rows:
            auths = w.get("authorships") or []
            senior = [a for a in auths if a.get("is_corresponding")] or auths[-1:]
            for a in senior:
                if is_kaist_me(a) and (a.get("author") or {}).get("id"):
                    aid = a["author"]["id"].rsplit("/", 1)[1]
                    counts[aid] += 1
                    names[aid] = a["author"].get("display_name")
        cursor = data.get("meta", {}).get("next_cursor")
        if not rows:
            break
    labs = [{
        "pi": names[a], "pi_en": names[a], "name": None, "url": None, "labs": [], "topics": [],
        "openalex_ids": [a], "openalex_name": names[a], "match_status": "unofficial",
        "match_candidates": 1, "kaist_me_senior_papers": n,
    } for a, n in counts.most_common() if n >= MIN_PAPERS]
    ids = [l["openalex_ids"][0] for l in labs]
    by_author = {i: [] for i in ids}
    for start in range(0, len(ids), 50):
        chunk = ids[start:start + 50]
        keep = set(chunk)
        for w in oa.works_for(chunk):
            s = oa.slim(w)
            for a in w.get("authorships") or []:
                aid = ((a.get("author") or {}).get("id") or "").rsplit("/", 1)[-1]
                if aid in keep:
                    by_author[aid].append(s)
    for l in labs:
        l["publications"] = sorted(by_author[l["openalex_ids"][0]], key=lambda s: -(s["year"] or 0))
    out = {
        "university": "KAIST", "department": "Department of Mechanical Engineering",
        "department_url": "https://me.kaist.ac.kr/", "labs_list_url": None, "collected_at": "2026-11-09",
        "stage": "openalex", "official_roster": False,
        "roster_note": "me.kaist.ac.kr 접속 불가로 OpenAlex 소속 표기에서 추정한 명단",
        "labs": labs,
    }
    json.dump(out, open(os.path.join(oa.ROOT, "data", "oa-kaist.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"works_scanned": total, "authors": len(labs), "cost": round(oa.spent, 4),
                      "top": [(l["pi"], l["kaist_me_senior_papers"], len(l["publications"])) for l in labs[:8]]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
