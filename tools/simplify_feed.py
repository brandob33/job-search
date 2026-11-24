"""Pull security roles from SimplifyJobs' GitHub lists (New-Grad-Positions + Summer2027-Internships).

Usage: python3 tools/simplify_feed.py [--days N] [--out inbox/simplify-YYYY-MM-DD.json]

Reads the repos' structured listings.json (raw.githubusercontent.com), keeps active, visible
roles whose title looks security-related, located in SoCal or remote (US), posted/updated in the
last N days (default 3), and not already in data/seen.json (matched by URL). Prints a summary and
writes the candidates as JSON for the daily run to verify and score.
"""
import argparse, datetime, json, os, re, urllib.request

FEEDS = {
    "New-Grad-Positions": "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/.github/scripts/listings.json",
    "Summer2027-Internships": "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/.github/scripts/listings.json",
}
SEC = re.compile(r"secur|cyber|\bsoc\b|threat|vulnerab|penetration|pentest|red team|blue team|incident response|"
                 r"detection|forensic|\bgrc\b|infosec|appsec|identity|\biam\b|privacy engineer|trust ?& ?safety|fraud", re.I)
NOT_SEC = re.compile(r"physical security officer|security guard|securities|social security|\bsoc\b[^|]*(physical|design|firmware|architect|performance|validation|verification|memory)|"
                     r"(physical|design|firmware|architect|performance|validation|verification|memory)[^|]*\bsoc\b|object detection|regulatory data", re.I)
SOCAL = re.compile(r"irvine|costa mesa|santa ana|anaheim|orange|tustin|newport|huntington|fullerton|brea|lake forest|"
                   r"mission viejo|aliso viejo|laguna|san clemente|long beach|torrance|el segundo|hawthorne|los angeles|"
                   r"santa monica|culver|playa vista|redondo|manhattan beach|carson|gardena|downey|cerritos|pasadena|"
                   r"burbank|glendale|corona|ontario|riverside|chino|pomona|carlsbad|oceanside|san marcos|vista|"
                   r"seal beach|cypress|buena park|westminster|garden grove|yorba linda|placentia|signal hill|"
                   r"inglewood|beverly hills|el monte|irwindale|city of industry|sherman oaks|van nuys|"
                   r"camarillo|thousand oaks|westlake village", re.I)
REMOTE = re.compile(r"remote", re.I)
NON_US = re.compile(r"\b(UK|Canada|India|Germany|Ireland|Poland|Netherlands|France|Spain|Israel|Singapore|Japan|"
                    r"Australia|Mexico|Brazil|Romania|Portugal|Philippines|London|Toronto|Bangalore|Bengaluru|"
                    r"Dublin|Berlin|Paris|Amsterdam|Tel Aviv)\b|, ON\b|, BC\b", re.I)


def loc_ok(locs):
    for l in locs or []:
        if SOCAL.search(l) and not NON_US.search(l):
            return "socal"
    for l in locs or []:
        if REMOTE.search(l) and not NON_US.search(l):
            return "remote"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3)
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    seen = json.load(open(os.path.join(root, "data/seen.json")))
    seen_urls = {v.get("url", "").rstrip("/") for v in seen.values()}
    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=a.days)).timestamp()
    out = []
    for feed, url in FEEDS.items():
        data = json.load(urllib.request.urlopen(url, timeout=60))
        for j in data:
            if not (j.get("active") and j.get("is_visible", True)):
                continue
            t = j.get("title", "")
            if not SEC.search(t) or NOT_SEC.search(t):
                continue
            if feed == "Summer2027-Internships" and j.get("terms") and not any("2027" in x for x in j["terms"]):
                continue
            where = loc_ok(j.get("locations"))
            if not where:
                continue
            ts = max(j.get("date_posted") or 0, j.get("date_updated") or 0)
            if ts < cutoff:
                continue
            if j.get("url", "").rstrip("/") in seen_urls:
                continue
            out.append({
                "feed": feed, "company": j.get("company_name"), "title": t, "locations": j.get("locations"),
                "where": where, "terms": j.get("terms"), "url": j.get("url"),
                "sponsorship": j.get("sponsorship"),
                "date_posted": datetime.datetime.fromtimestamp(j.get("date_posted") or 0, datetime.timezone.utc).date().isoformat(),
            })
    out.sort(key=lambda x: (x["where"] != "socal", x["date_posted"]), reverse=False)
    for x in out:
        print(f'{x["feed"][:9]:9} | {x["date_posted"]} | {x["company"]} | {x["title"]} | {"; ".join(x["locations"])[:60]}')
    print(len(out), "candidates")
    if a.out:
        json.dump({"date": datetime.date.today().isoformat(), "source": "SimplifyJobs GitHub lists", "postings": out,
                   "processed": False}, open(a.out, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
