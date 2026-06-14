"""
False-positive / false-negative check for the H¹ leading-indicator claim (§5.5).

§5.5 and sheaf/h1_leading.py feed short-term external debt / FX reserves
(end-June 1997, RBA RDP 9805 Table 9, verified against the primary source) through
the Guidotti–Greenspan rule (ratio>1 → effective ⊤_priv) and report adjusted H¹=6
sitting on the "vulnerable vs sound" boundary. The honest_limits there flagged the
single biggest hole: NO false-positive analysis. This script is the
literature-grounded version of that analysis. It has two parts.

(A) WHERE THIS INDICATOR STANDS IN THE EARLY-WARNING LITERATURE
    (all verified 2026-06-14 against primary / authoritative sources):

    - Frankel & Saravelos (2012, J. Int. Econ. 87(2):216–231; NBER w16047):
      reviewing 80+ EWS papers, RESERVES and the real exchange rate are the two
      most useful leading indicators; among reserve measures, reserves relative to
      short-term debt performs best (4 of 5 reserve measures significant at 5% in
      ≥half of crisis-intensity measures). → the §5.5 indicator is the
      literature's single favourite reserve measure. GOOD for §5.5.

    - BUT Kaminsky–Lizondo–Reinhart (1998, IMF Staff Papers 45(1)): the canonical
      "signals approach" 15 indicators do NOT include short-term-debt/reserves.
      Reserves enter only as (i) reserve growth and (ii) M2/reserves. KLR note that
      measuring reserves "in terms of short-term or external debt" sharply cuts the
      number of data points and loses significance. → there is NO established
      noise-to-signal ratio for the §5.5 indicator. It is a regression-era,
      post-Asia favourite (Rodrik–Velasco 1999), not a signals-approach calibrated
      one. So we CANNOT quote a standard false-positive rate for it — that absence
      is itself a finding.

    - Berg–Borensztein–Pattillo (2005, IMF Staff Papers 52(3), "Assessing Early
      Warning Systems"): EWS out-of-sample performance is mixed; only one
      long-horizon model beat pure guesswork. False alarms are the rule, not the
      exception, for ANY single-threshold EWS. → a single-threshold rule like G-G
      should be expected to misfire out of sample.

(B) AN IN-EPISODE CONFUSION-MATRIX CHECK on the very 5 countries §5.5 uses.
    Signal  = ratio > 1 (Guidotti–Greenspan violation).
    Outcome = severity of the 1997–98 hit (1998 real per-capita GDP fall).
    The §5.5 narrative is "ratio>1 (KR/ID/TH) severe, ratio<1 (MY/PH) mild, and the
    H¹ boundary lines up with that severity gradient." This part tests that claim
    on the data and finds Malaysia is a FALSE NEGATIVE: ratio 0.6 (a "sound"
    signal) yet a 1998 contraction (~−10%) deeper than Korea's (~−8%, ratio 3.0).

    The honest reading is NOT "the indicator is wrong" but "the indicator measures
    ONE channel (external short-term liquidity). Malaysia was genuinely sound on
    that channel (0.6 → no IMF programme needed) but was hit hard through a
    DIFFERENT channel (asset-price bubble / capital flight). §5.5's boundary holds
    for the liquidity channel; it does not capture total crisis damage."

DATA PROVENANCE
  ratios   : RBA RDP 9805 Table 9 (end-June 1997) — verified verbatim.
  gdp98    : 1998 real per-capita GDP change, representative cross-country values
             widely reported for the Asian crisis (ID −16 / TH −12 / MY −10 /
             KR −8 / PH −3). Aggregate-GDP figures differ slightly (e.g. Malaysia
             −7.4% headline) and exact values vary ±a few points by source/vintage,
             so the confusion matrix is driven by the ROBUST ORDERING
             (ID > TH > MY ≈ KR ≫ PH), not by any single decimal. Sensitivity to
             the severity threshold is reported below.
  fx_drop  : approximate peak depreciation vs USD, 1997–98 (context only).
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Short-term external debt / reserves, end-June 1997 (RBA RDP 9805 Table 9).
RATIOS_JUN97 = {"KR": 3.0, "ID": 1.6, "TH": 1.1, "MY": 0.6, "PH": 0.7}
GG_THRESHOLD = 1.0  # Guidotti–Greenspan rule

# 1998 real per-capita GDP change (%), representative cross-country values.
GDP98 = {"ID": -16, "TH": -12, "MY": -10, "KR": -8, "PH": -3}
# Approx peak depreciation vs USD, 1997–98 (context only, not used in the matrix).
FX_DROP = {"ID": -80, "KR": -50, "TH": -50, "MY": -40, "PH": -40}

# Severity thresholds to test (a country is "severely hit" if GDP fall ≤ threshold).
SEVERITY_THRESHOLDS = (-5, -7, -9)
PRIMARY_THRESHOLD = -7


def classify(ratios, gdp, sev_threshold):
    """Return per-country (signal, severe, cell) and the confusion counts."""
    rows = {}
    counts = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    for c in ratios:
        signal = ratios[c] > GG_THRESHOLD
        severe = gdp[c] <= sev_threshold
        if signal and severe:
            cell = "TP"
        elif signal and not severe:
            cell = "FP"
        elif (not signal) and severe:
            cell = "FN"
        else:
            cell = "TN"
        counts[cell] += 1
        rows[c] = {"ratio": ratios[c], "signal": signal, "gdp98": gdp[c],
                   "severe": severe, "cell": cell}
    return rows, counts


def main():
    print("=" * 76)
    print("False-positive / false-negative check — H¹ leading indicator (§5.5)")
    print("=" * 76)

    rows, counts = classify(RATIOS_JUN97, GDP98, PRIMARY_THRESHOLD)

    print(f"\nSignal = short-term-debt/reserves > {GG_THRESHOLD} (Guidotti–Greenspan).")
    print(f"Severe = 1998 real per-capita GDP fall ≤ {PRIMARY_THRESHOLD}%.\n")
    print(f"  {'ctry':4} {'ratio':>5} {'signal':>7} {'gdp98':>6} {'severe':>7}  cell")
    for c in sorted(rows, key=lambda x: -RATIOS_JUN97[x]):
        r = rows[c]
        print(f"  {c:4} {r['ratio']:5.1f} {str(r['signal']):>7} "
              f"{r['gdp98']:5d}% {str(r['severe']):>7}  {r['cell']}")

    tp, fp, fn, tn = counts["TP"], counts["FP"], counts["FN"], counts["TN"]
    fnr = fn / (tp + fn) if (tp + fn) else float("nan")
    print(f"\n  confusion: TP={tp}  FP={fp}  FN={fn}  TN={tn}")
    print(f"  false-negative rate FN/(TP+FN) = {fn}/{tp + fn} = {fnr:.2f}")
    false_negatives = [c for c in rows if rows[c]["cell"] == "FN"]
    print(f"  FALSE NEGATIVE(S): {false_negatives}  "
          f"(sound signal, ratio≤1, but severely hit)")

    # Robustness: does the Malaysia FN survive across severity thresholds?
    print("\nRobustness of the Malaysia false-negative across severity thresholds:")
    robust_rows = {}
    for th in SEVERITY_THRESHOLDS:
        _, cnt = classify(RATIOS_JUN97, GDP98, th)
        rr, _ = classify(RATIOS_JUN97, GDP98, th)
        my_cell = rr["MY"]["cell"]
        kr_cell = rr["KR"]["cell"]
        robust_rows[th] = {"counts": cnt, "MY": my_cell, "KR": kr_cell}
        print(f"  GDP fall ≤ {th:>3}% :  MY={my_cell}  KR={kr_cell}  "
              f"(TP={cnt['TP']} FP={cnt['FP']} FN={cnt['FN']} TN={cnt['TN']})")
    print("  → MY is a false negative at every plausible threshold (−5 to −9).")
    print("    Only at the extreme −9% does KR (ratio 3.0) flip to FP, showing the")
    print("    matrix is sensitive to a too-strict cutoff, not to the MY conclusion.")

    print("\n" + "-" * 76)
    print("VERDICT")
    print("  (A) Literature: short-term-debt/reserves is the FAVOURITE reserve")
    print("      measure in regression EWS reviews (Frankel–Saravelos 2012), yet is")
    print("      ABSENT from the KLR signals-approach 15 (data-coverage loss), so it")
    print("      has NO calibrated noise-to-signal ratio. Single-threshold EWS")
    print("      misfire out of sample as a rule (Berg–Borensztein–Pattillo 2005).")
    print("  (B) In-episode: on §5.5's own 5 countries the rule scores TP=3 (KR/ID/")
    print("      TH), TN=1 (PH), and ONE FALSE NEGATIVE — Malaysia (ratio 0.6 'sound'")
    print("      but 1998 GDP ≈ −10%, deeper than Korea's). The §5.5 boundary tracks")
    print("      the EXTERNAL-LIQUIDITY channel, not total crisis damage.")
    print("  → §5.5 should be DOWNGRADED further: not just retrodiction + one")
    print("    episode, but a single-channel indicator with an in-sample false")
    print("    negative. True false-POSITIVE analysis (ratio>1 yet NO crisis) is NOT")
    print("    possible in this 5-country sample (all crisis participants); it is now")
    print("    done in false_positive_panel.py (113-country WDI panel, notes 30):")
    print("    75% false-alarm share, FPR 16%, noise-to-signal 0.46, lift 1.88.")

    bundle = {
        "description": (
            "Literature-grounded false-positive / false-negative check for the §5.5 "
            "H¹ leading-indicator claim. (A) places the short-term-debt/reserves "
            "indicator in the EWS literature; (B) runs an in-episode confusion matrix "
            "on §5.5's own 5 countries and finds Malaysia is a false negative."
        ),
        "part_A_literature": {
            "frankel_saravelos_2012": (
                "Reviewing 80+ EWS papers, reserves + real exchange rate are the two "
                "most useful leading indicators; reserves relative to short-term debt "
                "is the best reserve measure (4/5 reserve measures significant at 5% "
                "in >=half of crisis-intensity measures). J.Int.Econ 87(2):216-231 / "
                "NBER w16047. Verified 2026-06-14 (RePEc/CEPR)."
            ),
            "kaminsky_lizondo_reinhart_1998": (
                "Canonical signals-approach 15 indicators do NOT include short-term-"
                "debt/reserves; reserves enter only as growth and M2/reserves. KLR: "
                "measuring reserves 'in terms of short-term or external debt' cuts data "
                "points and loses significance. => no calibrated noise-to-signal ratio "
                "exists for the §5.5 indicator. IMF Staff Papers 45(1). Verified."
            ),
            "berg_borensztein_pattillo_2005": (
                "EWS out-of-sample performance is mixed; only one long-horizon model "
                "beat guesswork. Single-threshold rules misfire out of sample as a "
                "rule. IMF Staff Papers 52(3). Verified."
            ),
            "implication": (
                "The §5.5 indicator is the literature's FAVOURITE reserve measure "
                "(supports 'useful') but has NO established false-positive rate "
                "(signals approach drops it), so §5.5 cannot borrow a low-FP number; "
                "and generic EWS evidence says expect false alarms out of sample."
            ),
        },
        "part_B_in_episode": {
            "ratios_jun97": RATIOS_JUN97,
            "ratios_source": "RBA RDP 9805 Table 9 (end-June 1997), verified verbatim",
            "gdp98_per_capita_pct": GDP98,
            "gdp98_source": (
                "Representative cross-country 1998 real per-capita GDP changes for the "
                "Asian crisis; ordering ID>TH>MY≈KR>>PH is robust, exact decimals vary "
                "by source/vintage (headline aggregate Malaysia ≈ -7.4%)."
            ),
            "signal_rule": "short-term-debt/reserves > 1 (Guidotti-Greenspan)",
            "severity_rule_primary": f"1998 per-capita GDP fall <= {PRIMARY_THRESHOLD}%",
            "confusion_primary": counts,
            "false_negative_rate": round(fnr, 2),
            "false_negatives": false_negatives,
            "robustness": {str(th): robust_rows[th] for th in SEVERITY_THRESHOLDS},
            "fx_drop_context_pct": FX_DROP,
        },
        "verdict": (
            "On §5.5's own 5 countries the G-G rule scores TP=3 (KR/ID/TH), TN=1 (PH) "
            "and ONE FALSE NEGATIVE: Malaysia (ratio 0.6 'sound' yet 1998 GDP ~-10%, "
            "deeper than Korea). Robust across -5..-9% severity cutoffs. The §5.5 "
            "boundary tracks the external-liquidity channel, not total crisis damage. "
            "Combined with (A) -- favourite reserve measure but no calibrated FP rate, "
            "and generic EWS false-alarm evidence -- §5.5 should be downgraded further: "
            "a single-channel indicator with an in-sample false negative, on top of "
            "the existing retrodiction + one-episode caveats."
        ),
        "honest_limits": (
            "This sample (5 crisis-participant countries) can show a false NEGATIVE "
            "(Malaysia) but CANNOT measure the false-POSITIVE rate (ratio>1 yet no "
            "crisis), because there are no non-crisis country/years in it -- that panel "
            "is now BUILT in false_positive_panel.py (113-country WDI panel, notes 30: "
            "75% false-alarm share, FPR 16%, noise-to-signal 0.46, lift 1.88). GDP-fall figures are "
            "secondary representative values (±a few points by source); the matrix is "
            "driven by the robust ordering, not single decimals. The Malaysia reading "
            "('sound on liquidity, hit via another channel') is an interpretation "
            "consistent with Malaysia avoiding an IMF programme, not a decomposition of "
            "its 1998 contraction. G-G rule itself postdates the crisis (1999)."
        ),
    }
    out = Path(__file__).resolve().parents[3] / "docs" / "data" / "false_positive_test.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
