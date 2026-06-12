"""
Leapfrog-precise empirical test — mobile money adoption vs concentration.

This is the ROBUSTNESS test for KEY FINDING 5. The account-ownership version
(tradeoff_test.py) found ~zero correlation (ρ≈-0.08). But account ownership is
a BROAD inclusion proxy (includes ordinary bank accounts). The leapfrog story
is specifically about MOBILE MONEY. If mobile-money adoption DID correlate with
concentration, Finding 5 ("fragility is structural, not scalar") would need
revision. So this test can overturn our own published claim.

DATA PROVENANCE — mobile money account (% age 15+, Findex 2021), TRIPLE-VERIFIED
2026-06-12 with three independent routes agreeing:
  1. WB API  api.worldbank.org/v2/.../mobileaccount.t.d?source=28&date=2021
  2. OWID grapher 'mobile-money-account-usage' (Findex-sourced)
  3. repo docs/data/A_findex.json (matches both)
NOTE: an earlier audit wrongly flagged the PH value (21.74%) as disagreeing with
"~29%" — that was a news-summary figure; the primary sources agree on 21.74%.
The audit flag was a false positive, corrected 2026-06-12.

Concentration = docs/data/B_concentration.json (medium confidence, as before).
VN excluded (not in the Findex 2021 wave); BN excluded (never surveyed).
"""

from __future__ import annotations
import json
import statistics as st
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Mobile money account % (age 15+, Findex 2021) — triple-verified, see header.
MOBILE_MONEY_2021 = {
    "ID": 9.29, "KH": 6.60, "LA": 5.48, "MM": 29.03,
    "MY": 27.98, "PH": 21.74, "SG": 30.60, "TH": 59.99,
}


def load_concentration() -> dict:
    p = Path(__file__).resolve().parents[3] / "docs" / "data" / "B_concentration.json"
    d = json.load(open(p, encoding="utf-8"))["data"]
    return {k: (float(v["top_share_pct"]), v["backbone_type"]) for k, v in d.items()}


def eta_squared(groups: dict[str, list[float]]) -> float:
    allv = [x for vs in groups.values() for x in vs]
    grand = st.fmean(allv)
    ss_total = sum((x - grand) ** 2 for x in allv)
    ss_between = sum(len(vs) * (st.fmean(vs) - grand) ** 2 for vs in groups.values() if vs)
    return (ss_between / ss_total) if ss_total else 0.0


def main():
    conc = load_concentration()
    rows = [(c, mm, *conc[c]) for c, mm in MOBILE_MONEY_2021.items() if c in conc]

    xs = [r[1] for r in rows]  # mobile money %
    ys = [r[2] for r in rows]  # concentration %
    pearson = st.correlation(xs, ys)
    spearman = st.correlation(xs, ys, method="ranked")

    print("=" * 72)
    print("Leapfrog-precise test — mobile money % (triple-verified) vs concentration")
    print("=" * 72)
    print(f"\n{'国':4s} {'mobile money%':>14s} {'conc%':>7s}  backbone_type")
    for c, mm, share, btype in sorted(rows, key=lambda r: -r[1]):
        print(f"{c:4s} {mm:14.1f} {share:7.0f}  {btype}")

    print(f"\nn = {len(rows)}  Pearson r = {pearson:+.3f}   Spearman ρ = {spearman:+.3f}")

    # orthogonality: does backbone type explain mobile-money adoption?
    groups: dict[str, list[float]] = {}
    for c, mm, share, btype in rows:
        groups.setdefault(btype, []).append(mm)
    eta2 = eta_squared(groups)
    print(f"\ntype → mobile money の η² = {eta2:.3f}")
    for t, vs in sorted(groups.items()):
        print(f"  {t:13s} mobile money = {[round(v,1) for v in vs]}")
    print("  (同じ central_bank 型で TH 60.0 vs KH 6.6 — 型は adoption を決めない)")

    weak = abs(spearman) < 0.4
    print("\n" + "-" * 72)
    if weak:
        print("ROBUSTNESS VERDICT: mobile-money 版でも相関は弱い → 発見5 は両方の")
        print("包摂プロキシ (account / mobile money) に対して頑健。")
    else:
        print("⚠ ROBUSTNESS VERDICT: mobile-money 版で相関が出た → 発見5 は要修正!")
        print("  (このメッセージが出たら index.html 発見5 を書き直すこと)")

    bundle = {
        "description": (
            "Leapfrog-precise robustness test for KEY FINDING 5: mobile-money "
            "adoption (Findex 2021, triple-verified) vs provider concentration. "
            "Designed so it COULD overturn the published finding."
        ),
        "data_provenance": {
            "mobile_money": "Findex 2021 mobileaccount.t.d — triple-verified 2026-06-12 "
                            "(WB API = OWID = repo A_findex.json, all 21.74 for PH etc.)",
            "audit_correction": "earlier '21.74 vs official ~29' flag was a false positive "
                                "(news-summary figure); primary sources agree on 21.74.",
            "concentration": "B_concentration.json, medium confidence",
        },
        "rows": [{"country": c, "mobile_money_pct": mm, "concentration_pct": s,
                  "backbone_type": b} for c, mm, s, b in rows],
        "n": len(rows),
        "pearson_r": round(pearson, 3),
        "spearman_rho": round(spearman, 3),
        "eta2_type_vs_mobile_money": round(eta2, 3),
        "finding5_robust": weak,
        "verdict": (
            ("Weak/no correlation on the mobile-money proxy as well — Finding 5 "
             "(fragility is structural, not scalar) is robust across BOTH inclusion "
             "proxies.") if weak else
            ("Correlation appeared on the mobile-money proxy — Finding 5 needs "
             "revision.")
        ),
        "honest_limits": (
            "n=8 (VN not in the 2021 wave, BN never surveyed); concentration is "
            "medium-confidence; SPEED (v×C) remains untested — this is adoption "
            "LEVEL, not adoption velocity."
        ),
    }
    out = Path(__file__).resolve().parents[3] / "docs" / "data" / "leapfrog_empirical.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
