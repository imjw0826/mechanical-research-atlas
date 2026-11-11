#!/usr/bin/env python3
"""Turn raw directory captures into roster-<school>.json files."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
SKIP = re.compile(r"emerit|honorary|lecturer|educator|adjunct|visiting|teaching|retired|in memoriam", re.I)
TAIL = re.compile(r"\s+(Professor.*|Associate Professor.*|Assistant Professor.*|Lecturer.*|Senior.*|Principal.*|Reader.*|Research.*|Institute.*|Chair.*|Dean.*)$")


def raw(name):
    return json.load(open(os.path.join(RAW, f"dir-{name}.json")))


def lab(pi, url=None, name=None, topics=None, **extra):
    return {"pi": pi, "pi_en": pi, "name": name, "url": url, "labs": [name] if name else [], "topics": topics or [], **extra}


def dedupe(labs):
    seen, out = set(), []
    for l in labs:
        key = re.sub(r"[^a-z]", "", (l.get("pi_en") or l["pi"] or "").lower())
        if key and key not in seen:
            seen.add(key)
            out.append(l)
    return out


def mit():
    out = []
    for text, url in raw("mit")["all"]:
        if "/people/faculty/" not in url or SKIP.search(text) or "," not in text:
            continue
        last, rest = text.split(",", 1)
        first = TAIL.sub("", rest.strip())
        out.append(lab(f"{first} {last.strip()}", url))
    return out


def stanford():
    out, current = [], None
    for text, url in raw("stanford")["all"]:
        if re.search(r"me\.stanford\.edu/(people?|person)/", url):
            out.append(lab(text, current[1] if current else url, current[0] if current else None))
        elif "stanford.edu" in url and "me.stanford.edu" not in url or "github.io" in url:
            current = (text, url)
        elif not url.startswith("https://me.stanford.edu"):
            current = (text, url)
    return out


def nus():
    out = []
    for page in json.load(open(os.path.join(RAW, "dir-nus-pages.json"))):
        lines = [s.strip() for s in page["fullText"].split("\n") if s.strip()]
        websites = {}
        people = {}
        for text, url in page["all"]:
            if "/me/staff/" in url and url not in people:
                people[url] = text
            if text.strip() == "Website" and people:
                websites[list(people)[-1]] = url
        for url, name in people.items():
            i = lines.index(name) if name in lines else -1
            block = " ".join(lines[i + 1:i + 5]) if i >= 0 else ""
            if SKIP.search(block):
                continue
            area = next((s for s in lines[i + 1:i + 5] if s in (
                "Manufacturing", "Materials", "Control & Mechatronics", "Fluid Mechanics", "Thermal Systems",
                "Mechanics", "Biomechanics", "Robotics")), None) if i >= 0 else None
            out.append(lab(name.title() if name.isupper() else name, websites.get(url) or url, topics=[area] if area else []))
    return out


def ntu():
    d = raw("ntu")
    lines = [s.strip() for s in d["fullText"].split("\n") if s.strip()]
    out = []
    for text, url in d["all"]:
        if "dr.ntu.edu.sg" not in url:
            continue
        i = lines.index(text) if text in lines else -1
        if i >= 0 and SKIP.search(" ".join(lines[i + 1:i + 3])):
            continue
        out.append(lab(text, url))
    return out


def eth():
    d = raw("eth")
    text = d["fullText"]
    sites = [u for t, u in d["all"] if t == "Website"]
    entries = list(re.finditer(r"^(.+?), (.+?), Prof\.[^\n]*$", text, re.M))
    out = []
    for i, m in enumerate(entries):
        chunk = text[m.end(): entries[i + 1].start() if i + 1 < len(entries) else len(text)]
        lines = [s.strip() for s in chunk.split("\n") if s.strip()]
        topics = [s for s in lines if s not in ("Contact", "Website", "Download") and not s.startswith(("Short", "Download"))]
        topic_text = topics[0] if topics else ""
        out.append(lab(f"{m.group(2)} {m.group(1)}", sites[i] if i < len(sites) else None,
                       topics=[t.strip() for t in topic_text.split(",") if t.strip()][:8]))
    return out


def harvard():
    return [lab(t, u) for t, u in raw("harvard")["all"] if "/person/" in u and len(t.split()) >= 2]


def delft():
    out = []
    for text, url in raw("delft")["all"]:
        m = re.match(r"Prof\.\s*(?:dr\.?\s*)?(?:ir\.?\s*)?(?:dr\.?\s*)?((?:[A-Z]\.)+\s*[^A-Z]*[A-Z][\w'-]+(?:-[A-Z][\w'-]+)?(?:\s\([A-Za-z]+\))?)\s*(.*)$", text)
        if "/staff/" not in url or not m:
            continue
        name = re.sub(r"\s*\(.*\)", "", m.group(1)).strip()
        out.append(lab(name, url, topics=[m.group(2)] if m.group(2) else []))
    return out


def imperial():
    out = []
    for text, url in raw("imperial")["all"]:
        if "profiles.imperial.ac.uk" not in url:
            continue
        m = re.match(r"(?:Professor|Dr|Prof\.?)\s+(.+?)\s+(?:Chair|Professor|Reader|Associate|Assistant|Senior|Principal|Lecturer|Director|Head)\b(.*)$", text)
        name = m.group(1) if m else re.sub(r"^(Professor|Dr)\s+", "", text)
        out.append(lab(re.sub(r"\s*\(.*?\)", "", name), url))
    return out


def postech():
    d = raw("postech-faculty")
    out = []
    for text, url in d["all"]:
        m = re.match(r"View more \+ (\S+) (?:\(JA\))?([A-Z][\w-]+(?: [A-Z][\w-]+)*)\s*(.*)$", text)
        if "/page/professor" not in url or not m:
            continue
        ex = lab(m.group(1), url, topics=[])
        ex["pi_en"] = re.sub(r"\s+Ph\w*$", "", m.group(2))
        ex["joint"] = "(JA)" in text
        out.append(ex)
    return out


def cambridge():
    out = []
    data = json.load(open(os.path.join(RAW, "dir-cam-divisions.json")))
    for division, people in data.items():
        for text, url in people:
            if not re.match(r"Prof", text):
                continue
            name = re.sub(r"^(Professor|Prof\.?)\s+", "", re.sub(r"\s*\(.*?\)", "", text)).strip()
            out.append(lab(name, url, topics=[division]))
    return out


def oxford():
    out = []
    for text, url in raw("oxp")["all"]:
        if "/people/" not in url or "," not in text or not re.search(r"Professor|Reader", text):
            continue
        last, rest = text.split(",", 1)
        first = re.split(r"\s+(?:Professor|Dr|Mr|Ms|Mrs|Sir)\b", rest.strip())[0]
        out.append(lab(f"{first.strip()} {last.strip()}", url))
    return out


SCHOOLS = {
    "cambridge": ("University of Cambridge", "Department of Engineering (Divisions A, C, E)", "https://www.eng.cam.ac.uk/", "https://www.eng.cam.ac.uk/people", cambridge),
    "oxford": ("University of Oxford", "Department of Engineering Science", "https://eng.ox.ac.uk/", "https://eng.ox.ac.uk/people?c=ac", oxford),
    "mit": ("MIT", "Department of Mechanical Engineering", "https://meche.mit.edu/", "https://meche.mit.edu/people?", mit),
    "stanford": ("Stanford University", "Department of Mechanical Engineering", "https://me.stanford.edu/", "https://me.stanford.edu/research-impact/labs", stanford),
    "nus": ("National University of Singapore", "Department of Mechanical Engineering", "https://cde.nus.edu.sg/me/", "https://cde.nus.edu.sg/me/about-us/people/academic-staff/", nus),
    "ntu": ("Nanyang Technological University", "School of Mechanical and Aerospace Engineering", "https://www.ntu.edu.sg/mae", "https://www.ntu.edu.sg/mae/about-us/our-people/administrative-staff", ntu),
    "eth": ("ETH Zurich", "Department of Mechanical and Process Engineering", "https://mavt.ethz.ch/", "https://mavt.ethz.ch/people/faculty/professors.html", eth),
    "harvard": ("Harvard University", "Materials Science & Mechanical Engineering", "https://seas.harvard.edu/materials-science-mechanical-engineering", "https://seas.harvard.edu/materials-science-mechanical-engineering/faculty-research", harvard),
    "delft": ("Delft University of Technology", "Faculty of Mechanical Engineering", "https://www.tudelft.nl/en/me", "https://www.tudelft.nl/en/about-tu-delft/organisation/professors/professors-mechanical-engineering", delft),
    "imperial": ("Imperial College London", "Department of Mechanical Engineering", "https://www.imperial.ac.uk/mechanical-engineering/", "https://www.imperial.ac.uk/mechanical-engineering/people/academic-staff/", imperial),
    "postech": ("POSTECH", "Department of Mechanical Engineering", "https://me.postech.ac.kr/", "https://me.postech.ac.kr/page/member01", postech),
}

if __name__ == "__main__":
    for key, (uni, dep, dep_url, list_url, fn) in SCHOOLS.items():
        labs = dedupe(fn())
        json.dump({"university": uni, "department": dep, "department_url": dep_url, "labs_list_url": list_url,
                   "collected_at": "2026-11-09", "stage": "roster_only", "labs": labs},
                  open(os.path.join(ROOT, "data", f"roster-{key}.json"), "w"), ensure_ascii=False, indent=1)
        print(key, len(labs), [l["pi_en"] for l in labs[:3]], [l["pi_en"] for l in labs[-2:]])
