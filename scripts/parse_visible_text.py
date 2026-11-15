#!/usr/bin/env python3
"""Heuristically split browser-visible publication-page text into citation records.

Input: {lab_id: [{url, text}, ...]} captured from official lab pages (see collect_lab_pages.js).
Each record keeps the verbatim text block as citation_raw; titles are best-effort.
"""
import re

YEAR = re.compile(r"(?<![\d/.-])(19[89]\d|20[0-3]\d)(?![\d/-])")
NOISE = re.compile(
    r"^(paper|papers|supp|supplementary|code|github|arxiv|pdf|link|links|citation|bibtex|doi|project page|video|"
    r"slides?|poster|abstract|online|html|view|more|read more|download|\[?pdf\]?|\[?link\]?|website|demo|dataset|"
    r"home|people|members?|research|publications?|news|contact|gallery|login|search|menu|top|journal|journals|"
    r"conference|conferences|international|domestic|patents?|all|back|share|copyright.*|©.*|\W+)$", re.I)
NUMBER_ONLY = re.compile(r"^[\[(]?\d{1,4}[\]).]?$")
HEADER_YEAR = re.compile(r"^(19|20)\d\d(\s*[-–~]\s*(19|20)\d\d)?(년)?$")
NEWS = re.compile(r"^\[?(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+20\d\d\]|accepted to|won the|award|수상|선정|게재|합격|졸업|입학|seminar|세미나", re.I)
VENUE_HINT = re.compile(
    r"journal|transactions|letters|proceedings|conference|symposium|workshop|review|nature|science|advanced|"
    r"vol\.?|volume|pp\.|\bp\.\s?\d|\d+\s*\(\d+\)|doi|ieee|asme|acs|elsevier|springer|phys\.|chem|mater|"
    r"j\.|int\.|appl|energy|fluid|robot|cvpr|iccv|eccv|neurips|icra|iros|aaai|rss|corl|icml|iclr|학회|학술|논문집|저널", re.I)
AUTHORS = re.compile(r"^([A-Z][\w'’.-]*\.?\s?){1,4}([,;&]|\band\b)", re.U)


def clean(s):
    s = re.sub(r"[ \u00a0\u200b]+", " ", s)
    return re.sub(r" *\t *", "\t", s).strip()


def is_noise(line):
    return (not line or NOISE.match(line) or NUMBER_ONLY.match(line) or HEADER_YEAR.match(line)
            or len(line) < 4)


def looks_like_authors(line):
    commas = line.count(",") + line.count(";") + len(re.findall(r"\band\b|&", line))
    initials = len(re.findall(r"\b[A-Z]\.(?:\s?-?[A-Z]\.)*", line))
    korean_names = len(re.findall(r"[가-힣]{2,4}\s*[,·]", line))
    return (commas >= 1 and (initials >= 2 or korean_names >= 1) and len(line) < 400) or \
           (commas >= 2 and len(line.split()) <= 3 * (commas + 1) and not VENUE_HINT.search(line))


NAME_TOKEN = re.compile(r"^(\*|†|#|\^)?((?:[A-Z]\.-?){1,3}[A-Z][a-zA-Z'’-]+|[A-Z][a-zA-Z'’-]*\.?|[A-Z]{1,3}|[A-Z]\.-?[A-Z]\.?|[가-힣]{2,4}|et|al\.?|and|&)(\*|†|#|\^|\+)?$")


def is_name_segment(seg):
    seg = re.sub(r"^(and|&)\s+", "", seg.strip(" .;*"))
    toks = seg.split()
    return 0 < len(toks) <= 5 and all(NAME_TOKEN.match(t) for t in toks)


def title_from_line(line):
    if "\t" in line:
        segs = [x.strip(" .") for x in line.split("\t")]
        segs = [x for x in segs if len(x.split()) >= 4 and not looks_like_authors(x) and not is_name_segment(x)]
        return max(segs, key=lambda x: (sum(w[:1].islower() for w in x.split()) - x.count(","), len(x))) if segs else None
    line = re.sub(r"^\s*[\[(]?[A-Z]?\d{0,4}[\]).]\s*", "", line)
    m = re.search(r"[“\"]([^”\"]{12,400})[”\"]", line)
    if m:
        return m.group(1).strip(" ,.")
    line = re.sub(r"^.*?\((19|20)\d\d[a-z]?\)\.?\s*", "", line) if re.match(r"^[^()]{3,300}\((19|20)\d\d[a-z]?\)\.", line) else line
    segs = re.split(r",\s+|(?<=[a-z\)\]])\.\s+|;\s+|\.\s+(?=[A-Z][a-z])", line)
    i = 0
    while i < len(segs) and (is_name_segment(segs[i]) or not segs[i].strip() or re.fullmatch(r"\(?(19|20)\d\d[a-z]?\)?\.?", segs[i].strip())):
        i += 1
    title = []
    for seg in segs[i:]:
        if title and (YEAR.search(seg) or VENUE_HINT.search(seg) or re.search(r"\d", seg)):
            break
        title.append(seg)
        if len(" ".join(title).split()) >= 4 and seg.rstrip().endswith((".", "?", "!")):
            break
    t = ", ".join(title).strip(" ,.")
    return t if len(t.split()) >= 3 or re.search(r"[가-힣]{6,}", t) else None


def extract_title(lines):
    joined = " ".join(lines)
    m = re.search(r"[“\"]([^”\"]{12,400})[”\"]", joined)
    if m:
        return m.group(1).strip(" ,.")
    if len(lines) > 1:
        body = [re.sub(r"^[\[(]?[A-Z]?\d{1,4}[\]).]\s*", "", l) for l in lines]
        cands = [l for l in body if not looks_like_authors(l) and (len(l.split()) >= 3 or re.search(r"[가-힣]{6,}", l))]
        noyear = [l for l in cands if not YEAR.search(l)]
        if noyear:
            return noyear[0].strip(" ,.")
        for l in body:
            t = title_from_line(l)
            if t:
                return t
        return None
    return title_from_line(lines[0])


def split_entries(text):
    raw = [clean(l) for l in text.replace("\r", "").split("\n")]
    lines = [l for l in raw if l]
    entries = []
    used = set()
    for i, line in enumerate(lines):
        if not YEAR.search(line) or is_noise(line) or NEWS.search(line):
            continue
        if len(line) > 2500:
            continue
        block = [line]
        if line.count("\t") >= 2:
            if re.search(r"\btitle\b.*\b(author|journal)|\bauthor\b.*\btitle\b", line, re.I):
                continue  # table header row
            cites = re.sub(r"\t+", " ", line)
            years = [int(y) for y in YEAR.findall(line)]
            entries.append({"lines": block, "citation_raw": cites, "year": max(years) if years else None})
            continue
        # A line carrying title, authors and venue is a citation on its own.
        self_contained = len(line) >= 90 and (looks_like_authors(line[:200]) or re.search(r"[“\"]", line)) and VENUE_HINT.search(line)
        if not self_contained:
            j = i - 1
            while j >= 0 and len(block) < 4 and j not in used:
                prev = lines[j]
                if is_noise(prev) or NEWS.search(prev):
                    if len(block) > 1 or not NUMBER_ONLY.match(prev):
                        break
                    j -= 1
                    continue
                if YEAR.search(prev) and VENUE_HINT.search(prev) and len(prev) < 300 and j + 1 == i - 0 and len(block) == 1 and len(prev) > 60:
                    break  # previous line is itself another citation
                block.insert(0, prev)
                j -= 1
                if len(block) >= 3:
                    break
            used.update(range(j + 1, i + 1))
        citation = re.sub(r"\t+", " ", " ".join(block))
        if len(citation) < 50 or len(citation.split()) < 7:
            continue
        if not (VENUE_HINT.search(citation) or looks_like_authors(citation) or re.search(r"[“\"]", citation)):
            continue
        years = [int(y) for y in YEAR.findall(block[-1])] or [int(y) for y in YEAR.findall(citation)]
        entries.append({"lines": block, "citation_raw": citation, "year": max(years) if years else None})
    # De-duplicate repeated blocks (pagination often repeats page 1).
    out, seen = [], set()
    for e in entries:
        key = re.sub(r"\W+", "", e["citation_raw"].casefold())
        if key in seen:
            continue
        seen.add(key)
        e["title"] = extract_title(e["lines"])
        out.append(e)
    return out


def split_grouped(text, blank_splits=True, year_joins=False, year_then_one=False):
    """Entries laid out as Title / Authors / Venue blocks separated by numbers, links or year headings."""
    lines = [clean(l) for l in text.replace("\r", "").split("\n")]
    groups, cur, year_header, cur_year, close_next = [], [], None, None, False
    for line in lines + [""]:
        if year_then_one:
            if not line:
                continue
            if close_next:
                cur.append(line)
                groups.append((cur, cur_year))
                cur, close_next = [], False
                continue
            if cur and HEADER_YEAR.match(line):
                cur.append(line)
                close_next = True
                continue
        header = HEADER_YEAR.match(line) if line else None
        if not line and not blank_splits:
            continue
        if year_joins and cur and line and HEADER_YEAR.match(line):
            cur.append(line)
            continue
        if not line or is_noise(line) or NEWS.search(line):
            if header:
                year_header = int(line[:4])
            if cur:
                groups.append((cur, cur_year))
                cur = []
            continue
        if not cur:
            cur_year = year_header
        cur.append(line)
    entries = []
    for block, header_year in groups:
        if not 2 <= len(block) <= 5:
            continue
        citation = re.sub(r"\t+", " ", " ".join(block))
        if len(citation) < 50 or len(citation.split()) < 7 or len(citation) > 2500:
            continue
        if re.search(r"skip to|건너뛰기|copyright|all rights|powered by", citation, re.I):
            continue
        if not any(looks_like_authors(l) for l in block) and not (
                any(is_name_segment(l) for l in block) and YEAR.search(citation)):
            continue
        years = [int(y) for y in YEAR.findall(citation)]
        year = max(years) if years else header_year
        entries.append({"lines": block, "citation_raw": citation, "year": year,
                        "year_type": None if years else ("page_section" if header_year else None)})
    out, seen = [], set()
    for e in entries:
        key = re.sub(r"\W+", "", e["citation_raw"].casefold())
        if key not in seen:
            seen.add(key)
            e["title"] = extract_title(e["lines"])
            out.append(e)
    return out


def strip_abstracts(text):
    """Drop the abstract paragraph that follows a bare 'Abstract' label (ETH publication widgets)."""
    out, skip = [], False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.lower() in ("abstract", "abstract:"):
            skip = True
            continue
        if skip:
            if stripped:
                skip = False
            continue
        out.append(line)
    return "\n".join(out)


def best_entries(text):
    text = strip_abstracts(text)
    def score(entries):
        good = 0
        for e in entries:
            t = e.get("title") or ""
            if len(t.split()) >= 4 and not YEAR.search(t) and not looks_like_authors(t) and \
                    not re.match(r"^[\[(]?\d", t) and not VENUE_HINT.match(t):
                good += 1
        return good
    variants = [split_entries(text), split_grouped(text), split_grouped(text, True, True),
                split_grouped(text, False), split_grouped(text, False, True),
                split_grouped(text, False, False, True)]
    scores = [score(v) for v in variants]
    best = max(range(len(variants)), key=lambda i: (scores[i] * (1.0 if i == 0 else 0.87), -i))
    return variants[best]
