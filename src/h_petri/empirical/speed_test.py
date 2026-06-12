"""
SPEED test — the v×C trade-off (notes/20 §4), finally tested directly.

Three times we wrote "the speed version (v×C) remains untested". This closes
that gap. Adoption VELOCITY is computed from two Findex waves:

    v = (mobile_money_2021 − mobile_money_2017) / 4   [pp per year]

DATA PROVENANCE — both waves from the WB API (mobileaccount.t.d, source=28),
fetched 2026-06-12; the 2021 wave is additionally triple-verified (=OWID,
=A_findex.json). LA excluded (2017 null), VN excluded (2021 null), BN never
surveyed → n=7.

TWO different readings of the hypothesis, tested separately:
  (1) CORRELATION reading: "faster adopters are more concentrated"
      → test: Spearman(v, C).
  (2) INEQUALITY reading (the honest form of a trade-off): "you cannot be fast
      AND decentralized" → predicts an EMPTY corner (high v, low C) in the
      scatter, NOT a line. A bound is not a correlation.
A trade-off bound can hold exactly while correlation is zero — conflating the
two is a common error, and the distinction is structural (excluded region),
which fits this project better than a scalar slope anyway.
"""

from __future__ import annotations
import json
import statistics as st
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Findex mobile money account % (age 15+). WB API mobileaccount.t.d, source=28.
MM_2017 = {"ID": 3.12, "KH": 5.66, "MM": 0.69, "MY": 10.88,
           "PH": 4.52, "SG": 9.55, "TH": 8.26}          # LA null in 2017
MM_2021 = {"ID": 9.29, "KH": 6.60, "MM": 29.03, "MY": 27.98,
           "PH": 21.74, "SG": 30.60, "TH": 59.99}


def load_concentration() -> dict:
    p = Path(__file__).resolve().parents[3] / "docs" / "data" / "B_concentration.json"
    d = json.load(open(p, encoding="utf-8"))["data"]
    return {k: float(v["top_share_pct"]) for k, v in d.items()}


def main():
    conc = load_concentration()
    rows = []
    for c in MM_2017:
        if c in MM_2021 and c in conc:
            v = (MM_2021[c] - MM_2017[c]) / 4.0
            rows.append((c, round(v, 2), conc[c]))

    xs = [r[1] for r in rows]   # velocity pp/yr
    ys = [r[2] for r in rows]   # concentration
    pearson = st.correlation(xs, ys)
    spearman = st.correlation(xs, ys, method="ranked")

    print("=" * 72)
    print("SPEED test — adoption velocity (Findex 2017→2021) vs concentration")
    print("=" * 72)
    print(f"\n{'国':4s} {'2017%':>7s} {'2021%':>7s} {'v pp/yr':>9s} {'conc%':>7s}")
    for c, v, cc in sorted(rows, key=lambda r: -r[1]):
        print(f"{c:4s} {MM_2017[c]:7.1f} {MM_2021[c]:7.1f} {v:9.2f} {cc:7.0f}")

    print(f"\nn = {len(rows)}  Pearson r = {pearson:+.3f}   Spearman ρ = {spearman:+.3f}")
    weak = abs(spearman) < 0.4
    print(f"→ (1) 相関読み: {'やはり弱い — 「速い国ほど集中」という線形版は不成立' if weak else '相関あり'}")

    # (2) inequality reading: is the (high v, low C) corner empty?
    fast = [r for r in rows if r[1] >= 4.0]           # ≥4pp/yr = clearly fast
    decentral = [r for r in rows if r[2] < 50]        # <50% top share = decentralized
    fast_and_decentral = [r for r in rows if r[1] >= 4.0 and r[2] < 50]
    print(f"\n→ (2) 不等式読み(排除領域): 速い国 (v≥4pp/yr) = {[r[0] for r in fast]}")
    print(f"   分散国 (conc<50%) = {[r[0] for r in decentral]}")
    print(f"   「速い AND 分散」 = {[r[0] for r in fast_and_decentral] or 'なし(排除領域は空)'}")
    corner_empty = not fast_and_decentral

    print("\n" + "-" * 72)
    print("VERDICT (two readings, kept separate):")
    print("  相関版  : 不成立 (3つ目のスカラーテストも null — 発見5 がさらに頑健に)")
    if corner_empty:
        print("  不等式版: データと整合 — 速い国は全て conc≥60%、分散国 (ID 25%) は遅い。")
        print("  ⚠ ただし分散国が ID 1国しかないので、空の角は偶然でも説明できる。")
        print("    n=7・分散国1つでは『仮説と整合』止まり。検証には域外データが要る。")

    bundle = {
        "description": (
            "Direct test of the v×C trade-off (notes/20 §4). Velocity from two "
            "Findex waves (2017→2021, WB API both), concentration as before. "
            "Tests BOTH readings: correlation (a line) and inequality (an excluded "
            "high-v/low-C corner) — a trade-off is a bound, not a slope."
        ),
        "rows": [{"country": c, "mm_2017": MM_2017[c], "mm_2021": MM_2021[c],
                  "velocity_pp_per_yr": v, "concentration_pct": cc}
                 for c, v, cc in rows],
        "n": len(rows),
        "excluded": {"LA": "2017 null", "VN": "2021 null", "BN": "never surveyed"},
        "correlation_reading": {
            "pearson_r": round(pearson, 3), "spearman_rho": round(spearman, 3),
            "verdict": "null — the linear 'faster⇒more concentrated' fails, like both level proxies",
        },
        "inequality_reading": {
            "fast_countries_v_ge_4": [r[0] for r in fast],
            "decentralized_countries_conc_lt_50": [r[0] for r in decentral],
            "fast_AND_decentralized": [r[0] for r in fast_and_decentral],
            "excluded_corner_empty": corner_empty,
            "verdict": (
                "Consistent with the bound: every fast adopter (v≥4pp/yr: TH, MM, SG, "
                "PH, MY) has top-share ≥60%; the only decentralized market (ID, 25%) "
                "is slow (1.5pp/yr). BUT with one decentralized country in n=7 the "
                "empty corner is weak evidence — hypothesis-consistent, not confirmed."
            ),
        },
        "structural_note": (
            "A trade-off is an inequality (excluded region), not a correlation. The "
            "three null correlations (account, mobile-money level, velocity) all "
            "reinforce Finding 5; the surviving candidate form of notes/20 §4 is the "
            "BOUND 'fast ⇒ concentrated', which the data does not contradict."
        ),
        "honest_limits": (
            "n=7; one decentralized observation; concentration medium-confidence; "
            "thresholds (v≥4, conc<50) are author-chosen. Out-of-region data "
            "(e.g. India UPI, Brazil Pix, Kenya) needed to really test the corner."
        ),
    }
    out = Path(__file__).resolve().parents[3] / "docs" / "data" / "speed_empirical.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
