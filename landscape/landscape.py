"""Who in India publishes hyperspectral remote-sensing research, and who already uses spaceborne
hyperspectral data? Pulls works from OpenAlex (free, no key) and writes landscape.md + CSV tables.

    python landscape.py            # fetch (cached in cache/) and write the report
    python landscape.py --refresh  # ignore the cache
"""
import collections
import csv
import json
import os
import pathlib
import sys
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "cache"
YEARS = "2021-2026"
MAILTO = os.environ.get("OPENALEX_MAILTO", "")   # optional contact address
API_KEY = os.environ.get("OPENALEX_API_KEY", "")  # optional; without it requests share a small free daily budget
# spaceborne / airborne hyperspectral sensors whose users are the natural first users of new data
SENSORS = ["PRISMA", "EnMAP", "AVIRIS-NG", "HySIS", "Hyperion", "DESIS", "EMIT", "Pixxel"]


def fetch_all(filt, refresh=False):
    """All works matching an OpenAlex filter (page-number paging, fine below 10 000 results), cached as JSON."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / (urllib.parse.quote(filt, safe="") + ".json")
    if path.exists() and not refresh:
        return json.loads(path.read_text())
    works, page = [], 1
    while True:
        url = (f"https://api.openalex.org/works?filter={urllib.parse.quote(filt, safe=':,|-')}&per_page=200&page={page}"
               + (f"&api_key={API_KEY}" if API_KEY else "") + (f"&mailto={MAILTO}" if MAILTO else ""))
        req = urllib.request.Request(url, headers={"User-Agent": "landscape.py"})   # the default urllib agent is refused
        with urllib.request.urlopen(req, timeout=60) as r:
            batch = json.load(r)["results"]
        works += batch
        if len(batch) < 200:
            break
        page += 1
        time.sleep(0.2)
    path.write_text(json.dumps(works))
    return works


def indian_affiliations(work):
    """(author name, institution name) pairs for authors with an Indian affiliation."""
    out = []
    for a in work["authorships"]:
        for inst in a["institutions"]:
            if inst.get("country_code") == "IN":
                name = "".join(ch for ch in a["author"]["display_name"] if ch.isprintable() and ch not in "\u202a\u202c")
                out.append((name.strip(), inst["display_name"]))
    return out


def words(work):
    """Title and abstract as a set of case-preserved words (OpenAlex stores abstracts as a word index)."""
    raw = (work.get("title") or "").split() + list((work.get("abstract_inverted_index") or {}).keys())
    return {w.strip(".,;:()[]'\"") for w in raw}


def sensors_in(work):
    """Sensor names matched as whole, case-sensitive words. PRISMA is also the name of a reporting
    guideline for systematic reviews, and EMIT is also a verb, so those need the stricter check."""
    w = words(work)
    text = " ".join(sorted(w)).lower()
    found = [s for s in SENSORS if s in w or (s not in ("PRISMA", "EMIT") and s.lower() in {x.lower() for x in w})]
    if "PRISMA" in found and ("systematic" in text or "meta-analysis" in text):
        found.remove("PRISMA")
    return found


def main():
    refresh = "--refresh" in sys.argv
    works = fetch_all(f"title_and_abstract.search:hyperspectral,authorships.countries:IN,publication_year:{YEARS}", refresh)
    by_inst = collections.defaultdict(lambda: {"works": 0, "cites": 0, "authors": collections.Counter(),
                                              "topics": collections.Counter(), "sensors": collections.Counter()})
    for w in works:
        affs = indian_affiliations(w)
        sens = sensors_in(w)
        topic = (w.get("primary_topic") or {}).get("display_name", "unknown")
        for inst in {i for _, i in affs}:
            b = by_inst[inst]
            b["works"] += 1
            b["cites"] += w.get("cited_by_count", 0)
            b["topics"][topic] += 1
            for s in sens:
                b["sensors"][s] += 1
        for author, inst in affs:
            by_inst[inst]["authors"][author] += 1

    rows = sorted(by_inst.items(), key=lambda kv: -kv[1]["works"])
    with open(HERE / "institutions.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["institution", "works", "citations", "most_active_authors", "main_topics", "sensors_mentioned"])
        for inst, b in rows:
            wr.writerow([inst, b["works"], b["cites"],
                         "; ".join(f"{a} ({n})" for a, n in b["authors"].most_common(3)),
                         "; ".join(t for t, _ in b["topics"].most_common(3)),
                         "; ".join(f"{s} ({n})" for s, n in b["sensors"].most_common())])

    sensor_users = collections.Counter()
    for w in works:
        for s in sensors_in(w):
            sensor_users[s] += 1
    spaceborne = [w for w in works if set(sensors_in(w)) & {"PRISMA", "EnMAP", "DESIS", "EMIT", "HySIS", "Pixxel"}]
    spaceborne.sort(key=lambda w: -w.get("cited_by_count", 0))

    md = [f"# Hyperspectral research in India, {YEARS}",
          "",
          f"Source: OpenAlex, works whose title or abstract mentions *hyperspectral* and that have at least one "
          f"author with an Indian affiliation. Fetched {time.strftime('%d %b %Y')}. Generated by `landscape.py`; "
          f"numbers are counts of OpenAlex records, so they inherit its coverage and affiliation errors.",
          "",
          f"**{len(works)} works** from **{len(by_inst)} institutions** (Indian and their co-authors' institutions abroad).",
          "",
          "## Most active Indian institutions",
          "",
          "| Institution | Works | Citations | Most active authors | Main topics |",
          "|---|---:|---:|---|---|"]
    shown = 0
    for inst, b in rows:
        if not any(i == inst for w in works for _, i in indian_affiliations(w)):
            continue
        md.append(f"| {inst} | {b['works']} | {b['cites']} | "
                  + ", ".join(a for a, _ in b["authors"].most_common(3)) + " | "
                  + "; ".join(t for t, _ in b["topics"].most_common(2)) + " |")
        shown += 1
        if shown == 20:
            break
    md += ["", "## Which sensors these papers name", "",
           "Mentions in title or abstract (a paper can name several).", "",
           "| Sensor | Papers |", "|---|---:|"]
    md += [f"| {s} | {sensor_users.get(s, 0)} |" for s in SENSORS]
    users = collections.Counter(i for w in spaceborne for i in {i for _, i in indian_affiliations(w)})
    md += ["", "## Indian institutions with the most spaceborne hyperspectral papers", "",
           "Counting papers that name PRISMA, EnMAP, DESIS, EMIT, HySIS or Pixxel. These groups already know how to "
           "work with satellite hyperspectral cubes.", "", "| Institution | Papers |", "|---|---:|"]
    md += [f"| {i} | {n} |" for i, n in users.most_common(12)]
    md += ["", "## Indian groups already working with spaceborne hyperspectral data", "",
           "Papers naming PRISMA, EnMAP, DESIS, EMIT, HySIS or Pixxel, most cited first.", "",
           "| Year | Title | Sensors | Indian institutions | Cited |", "|---|---|---|---|---:|"]
    for w in spaceborne[:25]:
        insts = sorted({i for _, i in indian_affiliations(w)})
        md.append(f"| {w['publication_year']} | [{(w['title'] or '').replace('|', '/')[:90]}]({w['id']}) | "
                  f"{', '.join(sensors_in(w))} | {'; '.join(insts)[:110]} | {w.get('cited_by_count', 0)} |")
    (HERE / "landscape.md").write_text("\n".join(md) + "\n")
    print(f"{len(works)} works, {len(by_inst)} institutions -> landscape.md, institutions.csv")


if __name__ == "__main__":
    main()
