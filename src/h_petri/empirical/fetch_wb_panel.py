"""
Fetch + cache the World Bank WDI series needed for the §5.6 false-POSITIVE panel.

The existing §5.6 work (false_positive_test.py / notes 28) could measure a false
NEGATIVE (Malaysia) but NOT a true false-POSITIVE rate, because all 5 countries it
uses are crisis participants. A genuine false-positive rate — "ratio>1 (Guidotti–
Greenspan violation) yet NO crisis followed" — needs a panel that INCLUDES
non-crisis country/years. This script fetches the raw inputs for that panel from a
single reproducible source (World Bank WDI public API, no key) and caches them so the
analysis (false_positive_panel.py) is auditable and re-runnable without re-fetching.

SERIES (verified live against api.worldbank.org, 2026-06-15):
  DT.DOD.DSTC.IR.ZS  Short-term debt (% of total reserves)
                     = short-term external debt / total reserves x 100.
                     This IS the Guidotti–Greenspan ratio (>100% == ratio>1).
                     World Bank Debtor Reporting System (DRS); annual, year-end.
  PA.NUS.FCRF        Official exchange rate (LCU per US$, period average)
                     — used to compute a mechanical currency-crash chronology.

HONESTY NOTE baked in from the probe (2026-06-15):
  The WDI/DRS series is NOT the BIS-based RBA RDP 9805 end-June-1997 measure that
  §5.5 uses. Korea AND Malaysia are ABSENT from this WDI series (non-DRS reporters
  in that era), and where both exist the values differ (e.g. Philippines end-1996
  0.68 ~ RBA 0.7, but WDI year-end 1997 is post-onset and much higher). So this
  panel tests the G-G RULE on a consistent cross-country series; it does not extend
  §5.5's exact numbers. That discontinuity is a finding, not a bug, and is reported.
"""

from __future__ import annotations
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

API = "https://api.worldbank.org/v2"
SERIES = {
    "st_debt_reserves": "DT.DOD.DSTC.IR.ZS",
    "fx_lcu_per_usd": "PA.NUS.FCRF",
    "broad_money_reserves": "FM.LBL.BMNY.IR.ZS",
    "reserves_months_imports": "FI.RES.TOTL.MO",
}
DATE_RANGE = "1975:2022"
OUT = Path(__file__).resolve().parents[3] / "docs" / "data" / "panel_raw"


def _get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "sea-fragility-research"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def fetch_indicator(code: str) -> list[dict]:
    """Fetch ALL country/year observations for one WDI indicator (handles paging)."""
    rows: list[dict] = []
    page = 1
    while True:
        url = (f"{API}/country/all/indicator/{code}"
               f"?format=json&per_page=20000&date={DATE_RANGE}&page={page}")
        meta, batch = _get(url)
        if not batch:
            break
        rows.extend(batch)
        if page >= int(meta.get("pages", 1)):
            break
        page += 1
        time.sleep(0.2)
    return rows


def fetch_countries() -> list[dict]:
    """Country metadata so we can drop WB aggregates (region.value == 'Aggregates')."""
    _, batch = _get(f"{API}/country?format=json&per_page=400")
    return batch


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    countries = fetch_countries()
    real = {c["id"]: c for c in countries if c.get("region", {}).get("value") != "Aggregates"}
    json.dump(countries, open(OUT / "countries.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"countries: {len(countries)} total, {len(real)} real (non-aggregate)")

    for nice, code in SERIES.items():
        rows = fetch_indicator(code)
        json.dump(rows, open(OUT / f"{nice}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        # coverage diagnostics on REAL countries only
        have = [r for r in rows
                if r.get("value") is not None and r.get("countryiso3code") in real]
        ctry = sorted({r["countryiso3code"] for r in have})
        yrs = sorted({int(r["date"]) for r in have})
        print(f"\n{nice}  ({code})")
        print(f"  raw rows: {len(rows)}   non-null real-country obs: {len(have)}")
        if yrs:
            print(f"  countries with data: {len(ctry)}   years: {yrs[0]}-{yrs[-1]}")

    print(f"\ncached -> {OUT}")


if __name__ == "__main__":
    main()
