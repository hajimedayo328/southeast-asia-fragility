"""
MM sensitivity check — do the headline empirical conclusions survive the
contested Myanmar assignment?

The 2026-06-12 correction established that Myanmar's top provider / backbone
type is CONTESTED post-coup (KBZPay bank-wallet 60% in the app segment vs Wave
Money platform-MFS, GSMA ~80% figure possibly pre-coup). Since MM appears in
every country-level test, re-run the key statistics under BOTH assignments:

  A (current loader values): MM = bank,     concentration 60
  B (contested alternative): MM = platform, concentration 80

If a conclusion flips between A and B, it depended on an unverifiable point
and must be weakened on the Pages. If not, the conclusions are robust to the
MM ambiguity.
"""

from __future__ import annotations
import json
import statistics as st
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WB_ACCOUNT_2021 = {"PH": 51.37, "TH": 95.58, "ID": 51.76, "MY": 88.37,
                   "SG": 97.55, "KH": 33.39, "LA": 37.32, "MM": 47.79}
MM_LEVEL_2021 = {"ID": 9.29, "KH": 6.60, "LA": 5.48, "MM": 29.03,
                 "MY": 27.98, "PH": 21.74, "SG": 30.60, "TH": 59.99}
VELOCITY = {"ID": 1.54, "KH": 0.23, "MM": 7.08, "MY": 4.28,
            "PH": 4.30, "SG": 5.26, "TH": 12.93}

BASE_CONC = {"VN": 56, "ID": 25, "PH": 85, "TH": 65, "MY": 62,
             "SG": 60, "KH": 70, "LA": 55, "MM": 60, "BN": 75}
BASE_TYPE = {"VN": "platform", "ID": "platform", "PH": "platform", "MY": "platform",
             "TH": "central_bank", "KH": "central_bank",
             "SG": "bank", "LA": "bank", "MM": "bank", "BN": "bank"}

SCENARIOS = {
    "A_current (MM=bank, conc60)":      {"conc": 60, "type": "bank"},
    "B_contested (MM=platform, conc80)": {"conc": 80, "type": "platform"},
}


def eta_squared(groups):
    allv = [x for vs in groups.values() for x in vs]
    grand = st.fmean(allv)
    sst = sum((x - grand) ** 2 for x in allv)
    ssb = sum(len(vs) * (st.fmean(vs) - grand) ** 2 for vs in groups.values() if vs)
    return ssb / sst if sst else 0.0


def spearman(pairs):
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    return st.correlation(xs, ys, method="ranked")


def run(scn):
    conc = dict(BASE_CONC); conc["MM"] = scn["conc"]
    typ = dict(BASE_TYPE); typ["MM"] = scn["type"]

    rho_account = spearman([(WB_ACCOUNT_2021[c], conc[c]) for c in WB_ACCOUNT_2021])
    rho_mmlevel = spearman([(MM_LEVEL_2021[c], conc[c]) for c in MM_LEVEL_2021])
    rho_speed = spearman([(VELOCITY[c], conc[c]) for c in VELOCITY])

    groups = {}
    for c, a in WB_ACCOUNT_2021.items():
        groups.setdefault(typ[c], []).append(a)
    eta2 = eta_squared(groups)

    fast_decentral = [c for c in VELOCITY if VELOCITY[c] >= 4.0 and conc[c] < 50]
    return {
        "spearman_account_vs_conc": round(rho_account, 3),
        "spearman_mmlevel_vs_conc": round(rho_mmlevel, 3),
        "spearman_speed_vs_conc": round(rho_speed, 3),
        "eta2_type_vs_account": round(eta2, 3),
        "fast_AND_decentralized": fast_decentral,
    }


def main():
    print("=" * 72)
    print("MM sensitivity — do conclusions survive the contested Myanmar entry?")
    print("=" * 72)
    results = {}
    for name, scn in SCENARIOS.items():
        r = run(scn)
        results[name] = r
        print(f"\n[{name}]")
        for k, v in r.items():
            print(f"  {k:30s} = {v}")

    a, b = results.values()
    checks = {
        "all_three_correlations_stay_weak(|rho|<0.4)": all(
            abs(r[k]) < 0.4 for r in (a, b)
            for k in ("spearman_account_vs_conc", "spearman_mmlevel_vs_conc", "spearman_speed_vs_conc")),
        "type_orthogonal_to_inclusion(eta2<0.15)": all(
            r["eta2_type_vs_account"] < 0.15 for r in (a, b)),
        "corner_stays_empty(no fast&decentralized)": all(
            not r["fast_AND_decentralized"] for r in (a, b)),
    }
    print("\n" + "-" * 72)
    print("ROBUSTNESS CHECKS (must hold in BOTH scenarios):")
    all_ok = True
    for k, v in checks.items():
        all_ok = all_ok and v
        print(f"  {'✓' if v else '✗ FLIPS'} {k}")
    print(f"\n=> {'全ての主要結論は MM の contested な割り当てに依存しない。' if all_ok else '⚠ 一部の結論が MM 依存 — Pages を弱める必要あり!'}")

    bundle = {
        "description": (
            "Sensitivity of the headline empirical conclusions to the contested "
            "Myanmar assignment (bank/60 vs platform/80). All key statistics "
            "recomputed under both scenarios."
        ),
        "scenarios": results,
        "robustness_checks": checks,
        "all_conclusions_robust": all_ok,
    }
    out = Path(__file__).resolve().parents[3] / "docs" / "data" / "mm_sensitivity.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
