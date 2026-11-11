#!/usr/bin/env python3
"""Classify works into mechanical-engineering areas, rank venues, and write site/data.json."""
import collections
import glob
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
UNIS = ["mit", "stanford", "nus", "cambridge", "ntu", "eth", "harvard", "oxford", "delft", "imperial", "snu", "kaist", "postech"]
QS = {"mit": "1", "stanford": "2", "nus": "3", "cambridge": "4", "ntu": "5", "eth": "6", "harvard": "=7", "oxford": "=7", "delft": "=9", "imperial": "=9"}
SHORT = {"mit": "MIT", "stanford": "Stanford", "nus": "NUS", "cambridge": "Cambridge", "ntu": "NTU", "eth": "ETH Zurich", "harvard": "Harvard",
         "oxford": "Oxford", "delft": "TU Delft", "imperial": "Imperial", "snu": "서울대", "kaist": "KAIST", "postech": "POSTECH"}
AREAS = [
    ("robotics", "로보틱스·자율시스템", r"robot|manipulat|teleoperat|haptic|exoskeleton|prosthe|locomotion|autonomous vehicle|drone|unmanned|uav|human-robot|gait|motion planning|localization and mapping|sensor-based localization"),
    ("bio", "바이오·의공학", r"biomechan|biomedical|tissue|cell|cancer|bone|orthop|cardi|blood|surgery|surgical|microfluidic|drug|medical imaging|neural|brain|muscle|protein|dna|rna|microscopy|hydrogel|photoacoustic|ultrasound imag"),
    ("manufacturing", "설계·제조", r"manufactur|additive|3d print|machining|welding|forming|tool|design optimization|topology optimization|supply chain|product design|engineering design|industry 4|fault diagnosis|maintenance|quality"),
    ("fluids", "유체역학·항공", r"fluid|turbulen|flow|aerodynamic|aeroelastic|boundary layer|wake|bubble|droplet|drop |wetting|hydrodynamic|turbomachin|gas turbine|compressor|ocean|wave energy|hypersonic|aircraft|aerospace|spacecraft"),
    ("thermal", "열·에너지", r"heat|thermal|thermoelectric|refrigerat|combustion|flame|engine|fuel cell|battery|batteries|lithium|solar|photovoltaic|hydrogen|electrocatal|energy|co2 capture|carbon capture|nuclear|phonon|perovskite"),
    ("solids", "고체역학·구조", r"fracture|fatigue|crack|solid mechanics|elastic|plastic|composite|structural|structure|contact mechanics|tribolog|lubric|mechanics of|metamaterial|finite element|computational mechanics|phase-field|numerical methods|shell|buckling|origami"),
    ("dynamics", "동역학·제어·음향", r"control|dynamics of|vibration|acoustic|noise|sonar|mems|sensors and actuators|vehicle dynamics|automotive|nonlinear dynamics|stability|estimation|system identification|oscillat"),
    ("materials", "재료·나노공학", r"material|nano|alloy|graphene|2d |thin film|polymer|metal|ceramic|semiconductor|crystal|microstructure|coating|surface|optical|photonic|plasmon|flexible|stretchable|wearable|electronic"),
    ("ai", "AI·계산과학", r"machine learning|deep learning|neural network|reinforcement|computer vision|vision|image|optimization algorithm|generative|data-driven|bayesian|language|natural language|ai "),
]
SUBFIELD = {
    "Mechanical Engineering": "solids", "Mechanics of Materials": "solids", "Civil and Structural Engineering": "solids", "Computational Mechanics": "solids",
    "Aerospace Engineering": "fluids", "Fluid Flow and Transfer Processes": "fluids", "Ocean Engineering": "fluids", "Automotive Engineering": "dynamics",
    "Control and Systems Engineering": "dynamics", "Acoustics and Ultrasonics": "dynamics", "Industrial and Manufacturing Engineering": "manufacturing",
    "Biomedical Engineering": "bio", "Biomaterials": "bio", "Artificial Intelligence": "ai", "Computer Vision and Pattern Recognition": "ai",
    "Materials Chemistry": "materials", "Polymers and Plastics": "materials", "Metals and Alloys": "materials", "Electronic, Optical and Magnetic Materials": "materials",
    "Renewable Energy, Sustainability and the Environment": "thermal", "Energy Engineering and Power Technology": "thermal", "Fuel Technology": "thermal", "Nuclear Energy and Engineering": "thermal",
}
AREA_RE = [(a, re.compile(p, re.I)) for a, _, p in AREAS]
OUT_OF_SCOPE_SUBFIELD = re.compile(r"Sociology|Political|Education|Economics|Finance|Marketing|Law|Philosophy|Literature|History|Archaeology|Pharmacology|Oncology|Epidemiology|Psychiatry|Public Health", re.I)
CANON = {
    "proceedings - ieee international conference on robotics and automation": "IEEE International Conference on Robotics and Automation (ICRA)",
    "ieee computer society conference on computer vision and pattern recognition": "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
    "neural information processing systems": "Conference on Neural Information Processing Systems (NeurIPS)",
    "proceedings of the ... american control conference": "American Control Conference (ACC)",
    "proceedings of the aaai conference on artificial intelligence": "AAAI Conference on Artificial Intelligence",
}
ELIGIBLE = {"article", "review", "conference-paper"}
RELIABLE = {"matched", "matched_by_field", "unofficial"}
BAD_VENUE = re.compile(r"abstract|arxiv|ssrn|zenodo|figshare|repository|biorxiv|research square|publons|chemrxiv|osti|dataset", re.I)


def classify(p):
    topic = p.get("topic") or ""
    sub = p.get("subfield") or ""
    if OUT_OF_SCOPE_SUBFIELD.search(sub):
        return "other"
    for area, rx in AREA_RE:
        if rx.search(topic):
            return area
    return SUBFIELD.get(sub, "other")


def clean_venue(name):
    if not name:
        return None
    base = re.split(r"/(?=Proceedings|IEEE Computer Society)", name)[0].strip()
    return CANON.get(base.lower(), base)


def eligible(p):
    return p.get("work_type") in ELIGIBLE and p.get("venue") and p.get("venue_type") in ("journal", "conference") and not BAD_VENUE.search(p["venue"])


def key_of(p):
    return p.get("doi") or (p.get("title") or "").lower()


def source_stats(ids):
    key = next(l.split("=", 1)[1].strip() for l in open(os.path.join(ROOT, ".env")))
    stats = {}
    ids = sorted(ids)
    for i in range(0, len(ids), 50):
        chunk = "|".join(ids[i:i + 50])
        q = urllib.parse.urlencode({"filter": f"openalex:{chunk}", "per-page": 50, "select": "id,summary_stats,host_organization_name", "api_key": key})
        with urllib.request.urlopen(f"https://api.openalex.org/sources?{q}", timeout=60) as r:
            for s in json.load(r)["results"]:
                sid = s["id"].rsplit("/", 1)[1]
                ss = s.get("summary_stats") or {}
                stats[sid] = {"h": ss.get("h_index"), "if2": round(ss.get("2yr_mean_citedness") or 0, 1), "host": s.get("host_organization_name")}
    return stats


def main():
    labs_out, venues = [], {}
    global_seen = set()
    uni_summary = {}
    for uni in UNIS:
        d = json.load(open(os.path.join(DATA, f"oa-{uni}.json")))
        counters = collections.Counter()
        area_counts = collections.Counter()
        for i, lab in enumerate(d["labs"]):
            status = lab.get("match_status")
            reliable = status in RELIABLE
            works = [p for p in lab.get("publications", []) if eligible(p)] if reliable else []
            tags = collections.Counter(classify(p) for p in works)
            in_scope = sum(c for a, c in tags.items() if a != "other")
            share = round(in_scope / len(works), 2) if works else None
            scoped = bool(works) and share >= 0.3
            ranked = [a for a, _ in tags.most_common() if a != "other"]
            primary = ranked[0] if ranked else None
            venue_counts = collections.Counter(clean_venue(p["venue"]) for p in works)
            recent = sorted(works, key=lambda p: -(p.get("year") or 0))[:5]
            pi = lab.get("pi") or lab.get("pi_en")
            pi_en = lab.get("pi_en") if lab.get("pi_en") != pi else None
            name = lab.get("name") or (lab.get("labs") or [None])[0]
            official = [t for t in (lab.get("topics") or []) if t]
            labs_out.append({
                "id": f"{uni}-{i}", "u": uni, "pi": pi, "en": pi_en, "lab": name, "url": lab.get("url"),
                "area": primary, "second": ranked[1] if len(ranked) > 1 else None,
                "status": status if reliable else "unverified", "scope": scoped, "n": len(works),
                "topics": official[:5] or (lab.get("openalex_topics") or [])[:3],
                "topicSrc": "official" if official else "openalex",
                "venues": [v for v, _ in venue_counts.most_common(3)],
                "recent": [{"t": p["title"], "y": p["year"], "v": clean_venue(p["venue"]), "d": p.get("doi")} for p in recent],
            })
            counters["labs"] += 1
            counters["reliable"] += reliable
            counters["scoped"] += scoped
            if not scoped:
                continue
            for p in works:
                area = classify(p)
                if area == "other":
                    continue
                area_counts[area] += 1
                k = key_of(p)
                vname = clean_venue(p["venue"])
                v = venues.setdefault(vname, {"name": vname, "type": p["venue_type"], "sid": (p.get("venue_id") or "").rsplit("/", 1)[-1],
                                              "keys": set(), "unis": set(), "labs": set(), "areas": collections.Counter()})
                if k not in v["keys"]:
                    v["keys"].add(k)
                    v["areas"][area] += 1
                v["unis"].add(uni)
                v["labs"].add(f"{uni}-{i}")
                global_seen.add(k)
        uni_summary[uni] = {"key": uni, "name": SHORT[uni], "full": d["university"], "dept": d["department"], "url": d.get("department_url"), "list": d.get("labs_list_url"),
                            "qs": QS.get(uni), "official": d.get("official_roster", True), "labs": counters["labs"], "reliable": counters["reliable"], "scoped": counters["scoped"],
                            "areas": dict(area_counts)}
    top_ids = {v["sid"] for v in sorted(venues.values(), key=lambda v: -len(v["labs"]))[:1200] if v["sid"]}
    stats = source_stats(top_ids)
    rows = []
    for v in venues.values():
        n, u, l = len(v["keys"]), len(v["unis"]), len(v["labs"])
        tier = "core" if u >= 6 and l >= 10 else "major" if u >= 3 and l >= 5 else None
        s = stats.get(v["sid"], {})
        rows.append({"name": v["name"], "type": v["type"], "n": n, "unis": u, "labs": l, "uniList": sorted(v["unis"], key=UNIS.index),
                     "tier": tier, "h": s.get("h"), "if2": s.get("if2"), "host": s.get("host"), "areas": dict(v["areas"].most_common()),
                     "area": v["areas"].most_common(1)[0][0]})
    rows.sort(key=lambda r: (-r["labs"], -r["n"]))
    out = {"generated": "2026-11-09", "qsYear": 2026, "since": 2022, "areas": [{"id": a, "name": n} for a, n, _ in AREAS],
           "unis": [uni_summary[u] for u in UNIS], "labs": labs_out, "venues": [r for r in rows if r["labs"] >= 2],
           "totals": {"papers": len(global_seen), "labs": len(labs_out), "reliable": sum(1 for l in labs_out if l["status"] != "unverified"),
                      "scoped": sum(1 for l in labs_out if l["scope"]), "venues": len(rows)}}
    os.makedirs(os.path.join(ROOT, "site"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "site", "data.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(json.dumps(out["totals"], ensure_ascii=False))
    print({u["key"]: [u["labs"], u["reliable"], u["scoped"]] for u in out["unis"]})
    print(collections.Counter(l["area"] for l in labs_out if l["scope"]).most_common())
    for a, n, _ in AREAS:
        conf = [r for r in rows if r["area"] == a and r["type"] == "conference"][:5]
        jour = [r for r in rows if r["area"] == a and r["type"] == "journal"][:4]
        print(n, "CONF", [(r["name"][:45], r["labs"], r["unis"], r["n"], r["tier"]) for r in conf])
        print(n, "JOUR", [(r["name"][:40], r["labs"], r["unis"], r["n"], r["h"]) for r in jour])
    print("size", os.path.getsize(os.path.join(ROOT, "site", "data.json")), file=sys.stderr)


if __name__ == "__main__":
    main()
