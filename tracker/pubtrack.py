"""Track research outputs (papers, posters, talks) through the publication review.

    python pubtrack.py check  submissions.csv          # find rows that break the process rules
    python pubtrack.py status submissions.csv          # what is at risk before its deadline
    python pubtrack.py status submissions.csv --today 2026-11-02

The stages and the working days each one needs come from ../process/publication-review.md.
"""
import argparse
import csv
import datetime as dt
import sys

STAGES = ["draft", "confidentiality", "technical", "approval", "approved", "submitted", "withdrawn"]
DAYS_NEEDED = {"draft": 5 + 10 + 3, "confidentiality": 5 + 10 + 3, "technical": 10 + 3, "approval": 3}
REQUIRED = ["id", "title", "lead_author", "type", "venue", "deadline", "stage", "stage_since"]


def parse_date(s):
    return dt.date.fromisoformat(s.strip())


def workdays_between(a, b):
    """Working days (Mon-Fri) from a to b, not counting a."""
    days, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        days += d.weekday() < 5
    return days


def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def problems(row):
    out = []
    for k in REQUIRED:
        if not row.get(k, "").strip():
            out.append(f"missing {k}")
    if row.get("stage") and row["stage"] not in STAGES:
        out.append(f"unknown stage '{row['stage']}'")
    for k in ("deadline", "stage_since"):
        try:
            if row.get(k):
                parse_date(row[k])
        except ValueError:
            out.append(f"{k} is not a YYYY-MM-DD date")
    stage = row.get("stage", "")
    if stage in ("technical", "approval", "approved", "submitted") and not row.get("reviewer", "").strip():
        out.append("no technical reviewer named")
    if row.get("customer_data", "").lower() == "yes" and row.get("customer_consent", "").lower() != "yes" \
            and stage in ("approval", "approved", "submitted"):
        out.append("uses customer data but consent is not recorded")
    return out


def cmd_check(rows):
    bad = 0
    for r in rows:
        p = problems(r)
        if p:
            bad += 1
            print(f"{r.get('id', '?'):8} {'; '.join(p)}")
    print(f"{len(rows)} rows, {bad} with problems")
    return 1 if bad else 0


def cmd_status(rows, today):
    open_rows = [r for r in rows if r["stage"] in DAYS_NEEDED and not problems(r)]
    print(f"Publication review status, {today.isoformat()}\n")
    print(f"{'id':8} {'stage':16} {'in stage':>8} {'deadline':>11} {'workdays left':>13}  flag")
    for r in sorted(open_rows, key=lambda r: r["deadline"]):
        left = workdays_between(today, parse_date(r["deadline"]))
        waited = workdays_between(parse_date(r["stage_since"]), today)
        need = DAYS_NEEDED[r["stage"]]
        flag = "LATE" if left < need else ("tight" if left < need + 5 else "")
        if r["stage"] in ("confidentiality", "technical") and waited > (5 if r["stage"] == "confidentiality" else 10):
            flag = (flag + " stuck").strip()
        print(f"{r['id']:8} {r['stage']:16} {waited:6}d {r['deadline']:>11} {left:13}  {flag}")
    skipped = [r.get("id", "?") for r in rows if problems(r)]
    if skipped:
        print(f"\nnot shown, fix first (run check): {', '.join(skipped)}")
    counts = {s: sum(r["stage"] == s for r in rows) for s in STAGES}
    print("\n" + ", ".join(f"{s}: {n}" for s, n in counts.items() if n))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["check", "status"])
    ap.add_argument("csv")
    ap.add_argument("--today", type=parse_date, default=dt.date.today())
    a = ap.parse_args(argv)
    rows = load(a.csv)
    return cmd_check(rows) if a.command == "check" else cmd_status(rows, a.today) or 0


if __name__ == "__main__":
    sys.exit(main())
