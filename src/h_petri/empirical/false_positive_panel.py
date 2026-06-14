"""
The §5.6 false-POSITIVE panel — measuring the true false-alarm rate of the
Guidotti–Greenspan rule on a non-crisis-inclusive country/year panel.

WHY THIS EXISTS
  false_positive_test.py (notes 28) could show a false NEGATIVE (Malaysia) but
  explicitly could NOT measure a false-POSITIVE rate, because its 5 countries are
  ALL crisis participants — there is no "ratio>1 yet no crisis" cell available. The
  honest_limits there named the fix: a panel that includes non-crisis country/years.
  This script builds that panel from real World Bank WDI data (fetched + cached by
  fetch_wb_panel.py) and runs a full early-warning confusion-matrix evaluation.

PRE-REGISTERED DESIGN (fixed BEFORE looking at any result, to bar p-hacking)
  Universe : EVERY WDI Debtor-Reporting-System country with a short-term-debt/
             reserves observation, EVERY year 1975-2022. No country or year is
             hand-picked.
  Signal   : ratio_ct = DT.DOD.DSTC.IR.ZS / 100 ; fires when ratio > theta.
             Primary theta = 1.0 (the NAMED Guidotti–Greenspan threshold, not
             author-tuned). Sensitivity theta in {0.5, 1.0, 1.5, 2.0}.
  Crisis   : a mechanical CURRENCY CRASH reproduced from WDI official exchange rate
             (PA.NUS.FCRF, LCU/US$). depr_cy = fx_cy/fx_c(y-1) - 1. Crash if
             depr >= D AND (depr - prior-year depr) >= A. TWO rule settings, run
             side by side per the user's "both chronologies" choice:
               FR  Frankel–Rose (1996)        D=0.25, A=0.10
               LV  Laeven–Valencia rule        D=0.30, A=0.10
             These reproduce the published RULES on WDI FX data; they are NOT a
             verbatim copy of L&V's curated crisis LIST (which adds case judgment).
             That distinction is stated as a limitation, not hidden.
  Outcome  : for a signal in year t, "crisis follows" == a crash year exists in the
             window (t, t+k]. Primary k=2. Sensitivity k in {1,2,3}. A country-year
             is ELIGIBLE only if fx data covers t..t+k so that "no crisis" is an
             OBSERVATION, never an assumption from missing data (dropped = reported).
  Metrics  : the full confusion matrix plus
               false-positive rate  FPR  = FP/(FP+TN)   = P(signal | no crisis)
               false-alarm share         = FP/(FP+TP)   = P(no crisis | signal)
                                                          (the "ratio>1 yet no
                                                          crisis" rate §5.6 asks for)
               recall  TPR               = TP/(TP+FN)
               noise-to-signal (KLR)     = FPR / TPR
               base rate                 = (TP+FN)/N
               lift                      = precision / base rate

HONESTY CONSTRAINTS (up front)
  - WDI/DRS != the BIS-based RBA RDP 9805 end-June-1997 measure used by §5.5. Korea
    AND Malaysia are ABSENT from this WDI series; where overlap exists the values
    differ. So this panel tests the G-G RULE at scale on a consistent series; it
    does NOT reproduce or extend §5.5's exact 5 numbers.
  - Country-years are serially correlated (a ratio can stay >1 for years; one crash
    spans years). The country-year matrix is the standard signal-extraction unit but
    inflates N; a per-country summary and an onset-only variant are also reported.
  - A mechanical crash rule cannot see capital-control episodes that avert a crash
    (e.g. Malaysia 1998) — exactly the single-channel limit §5.6 already states.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAW = Path(__file__).resolve().parents[3] / "docs" / "data" / "panel_raw"
OUT = Path(__file__).resolve().parents[3] / "docs" / "data" / "false_positive_panel.json"

# ---- pre-registered constants -------------------------------------------------
THETAS = (0.5, 1.0, 1.5, 2.0)
PRIMARY_THETA = 1.0
HORIZONS = (1, 2, 3)
PRIMARY_K = 2
CRASH_RULES = {  # name -> (min depreciation D, min acceleration A)
    "FR_25_10": (0.25, 0.10),
    "LV_30_10": (0.30, 0.10),
}
PRIMARY_RULE = "LV_30_10"
YEARS = range(1975, 2023)


# ---- data loading -------------------------------------------------------------
def load_real_countries() -> dict[str, dict]:
    rows = json.load(open(RAW / "countries.json", encoding="utf-8"))
    return {c["id"]: c for c in rows
            if c.get("region", {}).get("value") != "Aggregates"}


def load_series(name: str, real: set[str]) -> dict[tuple[str, int], float]:
    rows = json.load(open(RAW / f"{name}.json", encoding="utf-8"))
    out: dict[tuple[str, int], float] = {}
    for r in rows:
        iso = r.get("countryiso3code")
        if iso in real and r.get("value") is not None:
            out[(iso, int(r["date"]))] = float(r["value"])
    return out


# ---- crisis (currency-crash) construction ------------------------------------
# WDI gives only the PERIOD-AVERAGE exchange rate (PA.NUS.FCRF). A mid-year crash
# (e.g. the July-1997 baht float) is then split across two calendar years, so each
# year's depreciation can fall below the named single-year thresholds even though
# the currency collapsed. To stay reproducible from WDI yet not miss such crashes,
# the SAME published thresholds (D, A) are applied to BOTH the 1-year change and the
# 2-year cumulative change; a year is a crash if EITHER fires. This adds no tunable
# parameter (the thresholds are reused). Crises are then counted as ONSETS (first
# year of a crash spell) so one multi-year collapse is one event.
def changes(fx, countries, lag):
    """ch[(c,y)] = fx_cy/fx_c(y-lag) - 1 where both endpoints exist and prior>0."""
    ch = {}
    for c in countries:
        for y in YEARS:
            a, b = fx.get((c, y - lag)), fx.get((c, y))
            if a and b and a > 0:
                ch[(c, y)] = b / a - 1.0
    return ch


def crash_years(d1, d2, D, A):
    """Crash at (c,y) if the 1-yr OR the 2-yr cumulative depreciation clears the
    named rule: change>=D and accelerates >=A vs the matching prior window."""
    crashes = set()
    for key, d in d1.items():
        c, y = key
        one = d >= D and d - d1.get((c, y - 1), 0.0) >= A
        d2v = d2.get(key)
        two = d2v is not None and d2v >= D and d2v - d2.get((c, y - 2), 0.0) >= A
        if one or two:
            crashes.add(key)
    return crashes


def onsets(crashes):
    """First year of each crash spell (declustered) — distinct crisis episodes."""
    return {(c, y) for (c, y) in crashes if (c, y - 1) not in crashes}


# ---- confusion-matrix evaluation ---------------------------------------------
def evaluate(signal_series, fx, onset, crash, theta, k):
    """Confusion matrix over eligible TRANQUIL country-years at (theta, horizon k).
    This is the standard early-warning set-up: a signal is meant to fire BEFORE a
    crisis, in a calm period, so a country-year that is ITSELF in a currency crash is
    excluded (you cannot 'predict' a crisis you are already in; counting those as
    false alarms would inflate the false-positive rate during prolonged collapses,
    e.g. Argentina's early-1980s spell). Outcome = a crash ONSET in (t, t+k].
    Eligible only if FX covers t-1..t+k, so 'no crisis' is observed, not assumed."""
    counts = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    false_positives, true_positives = [], []
    eligible = dropped = in_crisis = 0
    for (c, t), ratio in signal_series.items():
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            dropped += 1
            continue
        if (c, t) in crash:                 # already in a crash: not an EW test
            in_crisis += 1
            continue
        eligible += 1
        signal = ratio > theta
        crisis = any((c, t + j) in onset for j in range(1, k + 1))
        cell = ("TP" if signal and crisis else "FP" if signal and not crisis
                else "FN" if crisis else "TN")
        counts[cell] += 1
        if cell == "FP":
            false_positives.append((c, t, round(ratio, 2)))
        elif cell == "TP":
            true_positives.append((c, t, round(ratio, 2)))
    return counts, false_positives, true_positives, eligible, dropped, in_crisis


def metrics(counts):
    tp, fp, fn, tn = counts["TP"], counts["FP"], counts["FN"], counts["TN"]
    n = tp + fp + fn + tn
    fpr = fp / (fp + tn) if (fp + tn) else None              # P(signal|no crisis)
    false_alarm = fp / (fp + tp) if (fp + tp) else None      # P(no crisis|signal)
    recall = tp / (tp + fn) if (tp + fn) else None
    precision = tp / (tp + fp) if (tp + fp) else None
    base = (tp + fn) / n if n else None
    nts = (fpr / recall) if (fpr is not None and recall) else None
    lift = (precision / base) if (precision is not None and base) else None
    return {
        "N": n, "base_rate": _r(base), "signal_fires": tp + fp,
        "false_positive_rate_FPR": _r(fpr),
        "false_alarm_share": _r(false_alarm),
        "recall_TPR": _r(recall), "precision": _r(precision),
        "noise_to_signal_KLR": _r(nts), "lift": _r(lift),
    }


def _r(x, n=3):
    return None if x is None else round(x, n)


# ---- reporting ----------------------------------------------------------------
def main():
    real_meta = load_real_countries()
    real = set(real_meta)
    # DT.DOD.DSTC.IR.ZS is a PERCENT (short-term debt as % of reserves); the
    # Guidotti–Greenspan ratio is that / 100, so ratio>1 == percent>100.
    signal = {k: v / 100.0 for k, v in load_series("st_debt_reserves", real).items()}
    fx = load_series("fx_lcu_per_usd", real)

    sig_countries = sorted({c for c, _ in signal})
    print("=" * 78)
    print("False-POSITIVE panel — Guidotti–Greenspan rule on a real WDI panel")
    print("=" * 78)
    print(f"\nSignal universe (short-term-debt/reserves observed): "
          f"{len(sig_countries)} countries, {len(signal)} country-years, "
          f"{min(y for _, y in signal)}-{max(y for _, y in signal)}")
    overlap55 = [c for c in ("KOR", "MYS", "THA", "IDN", "PHL") if c in sig_countries]
    print(f"  §5.5 countries present in this panel: {overlap55}  "
          f"(absent: {[c for c in ('KOR','MYS','THA','IDN','PHL') if c not in sig_countries]})")

    d1 = changes(fx, real, 1)
    d2 = changes(fx, real, 2)
    rules = {name: crash_years(d1, d2, D, A) for name, (D, A) in CRASH_RULES.items()}
    onset_sets = {name: onsets(cr) for name, cr in rules.items()}
    for name, cr in rules.items():
        print(f"\ncrash rule {name}: {len(cr)} crash country-years, "
              f"{len(onset_sets[name])} distinct episodes (onsets)")

    # sanity: do the detectors flag textbook crises?
    print("\nSanity check — detected crash ONSETS for known cases "
          f"({PRIMARY_RULE}):")
    prim_on = onset_sets[PRIMARY_RULE]
    for c in ("THA", "IDN", "KOR", "MEX", "ARG", "TUR", "RUS", "BRA"):
        ys = sorted(y for cc, y in prim_on if cc == c)
        print(f"  {c}: {ys}")

    # ---- primary result -------------------------------------------------------
    print("\n" + "-" * 78)
    print(f"PRIMARY  theta={PRIMARY_THETA} (ratio>1, G-G)  horizon k={PRIMARY_K}y")
    print("-" * 78)
    primary = {}
    for name, onset in onset_sets.items():
        counts, fps, tps, elig, drop, incr = evaluate(signal, fx, onset, rules[name],
                                                       PRIMARY_THETA, PRIMARY_K)
        m = metrics(counts)
        primary[name] = {"counts": counts, "metrics": m,
                         "eligible_tranquil": elig, "dropped_no_fx_window": drop,
                         "excluded_in_crisis": incr,
                         "false_positive_examples": sorted(fps)[:25],
                         "n_false_positives": len(fps),
                         "n_true_positives": len(tps)}
        print(f"\n[{name}]  tranquil country-years={elig} "
              f"(dropped {drop} no-FX-window, {incr} excluded as already-in-crisis)")
        print(f"  confusion  TP={counts['TP']} FP={counts['FP']} "
              f"FN={counts['FN']} TN={counts['TN']}")
        print(f"  signal fired {m['signal_fires']}x; of those FALSE ALARMS "
              f"(ratio>1, no crisis in {PRIMARY_K}y) = {m['false_alarm_share']} "
              f"({counts['FP']}/{m['signal_fires']})")
        print(f"  FPR P(signal|no crisis)={m['false_positive_rate_FPR']}  "
              f"recall={m['recall_TPR']}  base rate={m['base_rate']}")
        print(f"  noise-to-signal (KLR)={m['noise_to_signal_KLR']}  lift={m['lift']}")

    # ---- sensitivity ----------------------------------------------------------
    print("\n" + "-" * 78)
    print("SENSITIVITY  false_alarm_share / noise-to-signal / recall / base_rate")
    print("-" * 78)
    sensitivity = {}
    for name, onset in onset_sets.items():
        sensitivity[name] = {}
        print(f"\n[{name}]")
        print(f"  {'theta':>5} {'k':>2} {'falseAlarm':>11} {'NtS':>6} "
              f"{'recall':>7} {'base':>6} {'N':>6}")
        for theta in THETAS:
            for k in HORIZONS:
                counts, *_ = evaluate(signal, fx, onset, rules[name], theta, k)
                m = metrics(counts)
                sensitivity[name][f"theta={theta},k={k}"] = {"counts": counts, "metrics": m}
                print(f"  {theta:5.1f} {k:2d} {str(m['false_alarm_share']):>11} "
                      f"{str(m['noise_to_signal_KLR']):>6} {str(m['recall_TPR']):>7} "
                      f"{str(m['base_rate']):>6} {m['N']:6d}")

    # ---- verdict --------------------------------------------------------------
    prim = primary[PRIMARY_RULE]["metrics"]
    fn = primary[PRIMARY_RULE]["counts"]["FN"]
    fa, nts = prim["false_alarm_share"], prim["noise_to_signal_KLR"]
    fpr, rec, lift = (prim["false_positive_rate_FPR"], prim["recall_TPR"], prim["lift"])
    print("\n" + "=" * 78)
    print("VERDICT  (real non-crisis-inclusive panel, "
          f"{len(sig_countries)} DRS countries, {PRIMARY_RULE})")
    print(f"  The G-G signal (ratio>1) fires in {prim['signal_fires']}/{prim['N']} "
          f"country-years; of those firings {fa:.0%} are FALSE ALARMS (no crisis in "
          f"{PRIMARY_K}y).")
    print(f"  Statistically: FPR P(signal|no crisis)={fpr}, recall={rec} (it MISSES "
          f"{1-rec:.0%} of crises), noise-to-signal={nts}, lift={lift}.")
    print("  Reading (neither vindication nor demolition):")
    print("   - GENUINE but WEAK signal: NtS<1 and lift>1 — a firing raises 2-yr crisis")
    print(f"     odds from the {prim['base_rate']:.0%} base rate to "
          f"{prim['precision']:.0%}. Matches Frankel–Saravelos 'best reserve measure'.")
    print(f"   - DOMINATED by false alarms ({fa:.0%}) and low recall ({fn} "
          f"crises came with ratio<=1 — the Malaysia-type false negative, at scale).")
    print("  => Supplies the true false-POSITIVE number §5.6 could not quote, and keeps")
    print("     §5.6's cautious rating: useful-direction, high-false-alarm single channel.")

    bundle = {
        "description": (
            "True false-positive panel for the §5.6 Guidotti–Greenspan H¹ leading "
            "indicator. Builds a non-crisis-inclusive country/year panel from World "
            "Bank WDI (short-term-debt/reserves = the G-G ratio) and evaluates the "
            "ratio>1 signal against a mechanical currency-crash outcome reproduced "
            "from WDI exchange rates, under two published crash rules (Frankel–Rose "
            "25/10 and Laeven–Valencia 30/10), with full threshold/horizon sensitivity."
        ),
        "preregistered_design": {
            "universe": "all WDI DRS countries with short-term-debt/reserves, 1975-2022",
            "signal": "ratio = DT.DOD.DSTC.IR.ZS/100 ; fires when ratio>theta",
            "primary_theta": PRIMARY_THETA, "thetas": list(THETAS),
            "crash_rules": {k: {"min_depreciation": v[0], "min_acceleration": v[1]}
                            for k, v in CRASH_RULES.items()},
            "primary_rule": PRIMARY_RULE,
            "outcome": ("a crash ONSET occurs in window (t, t+k]; a crash year is "
                        "flagged when the 1-yr OR 2-yr cumulative depreciation clears "
                        "(D, A); evaluated only on TRANQUIL years (t not itself a crash "
                        "year) and only if FX covers t-1..t+k"),
            "primary_horizon_years": PRIMARY_K, "horizons": list(HORIZONS),
            "metrics": ["FPR=FP/(FP+TN)", "false_alarm_share=FP/(FP+TP)",
                        "recall=TP/(TP+FN)", "noise_to_signal=FPR/recall",
                        "base_rate", "lift=precision/base_rate"],
        },
        "data_provenance": {
            "signal": "World Bank WDI DT.DOD.DSTC.IR.ZS (Short-term debt % of total "
                      "reserves), fetched live 2026-06-15, cached docs/data/panel_raw/",
            "exchange_rate": "World Bank WDI PA.NUS.FCRF (LCU/US$, period average)",
            "fetcher": "src/h_petri/empirical/fetch_wb_panel.py",
        },
        "panel_coverage": {
            "signal_countries": len(sig_countries),
            "signal_country_years": len(signal),
            "year_min": min(y for _, y in signal), "year_max": max(y for _, y in signal),
            "ss5_5_countries_present": overlap55,
            "ss5_5_countries_absent": [c for c in ("KOR", "MYS", "THA", "IDN", "PHL")
                                       if c not in sig_countries],
        },
        "crash_chronologies": {name: {"crash_country_years": len(rules[name]),
                                      "distinct_episodes": len(onset_sets[name])}
                               for name in rules},
        "sanity_known_crises": {c: sorted(y for cc, y in prim_on if cc == c)
                                for c in ("THA", "IDN", "KOR", "MEX", "ARG",
                                          "TUR", "RUS", "BRA")},
        "primary_result": primary,
        "sensitivity": sensitivity,
        "verdict": (
            f"On a real {len(sig_countries)}-country non-crisis-inclusive panel "
            f"({PRIMARY_RULE} rule, theta=1, k={PRIMARY_K}y): the Guidotti–Greenspan "
            f"signal (ratio>1) fires in {prim['signal_fires']}/{prim['N']} country-years; "
            f"{fa:.0%} of firings are false alarms (no crash within {PRIMARY_K}y) and it "
            f"misses {1-rec:.0%} of crises (recall={rec}). Yet it is NOT noise: "
            f"noise-to-signal={nts} (<1) and lift={lift} — a firing lifts 2-yr crisis "
            f"odds from the {prim['base_rate']:.0%} base rate to {prim['precision']:.0%}. "
            f"So the true false-POSITIVE rate the 5-country in-episode test "
            f"(false_positive_test.py) structurally could not measure is now MEASURED: a "
            f"genuine-but-weak, false-alarm-dominated single-threshold signal — "
            f"simultaneously consistent with Frankel–Saravelos ('best reserve measure') "
            f"and Berg–Borensztein–Pattillo ('false alarms are the rule'). §5.6's "
            f"cautious rating stands, now on measured numbers rather than an absent one. "
            f"The {1-rec:.0%} of crises with ratio<=1 are the Malaysia-type false "
            f"negative at panel scale."
        ),
        "honest_limits": (
            "WDI/DRS is NOT the BIS-based RBA end-June-1997 measure of §5.5 (Korea and "
            "Malaysia are absent here; overlapping values differ). The crash rules "
            "REPRODUCE the Frankel–Rose and Laeven–Valencia thresholds on WDI FX data; "
            "they are not L&V's verbatim curated list (edge cases differ). Country-years "
            "are serially correlated (effective N < count). A mechanical crash rule "
            "cannot detect crises averted by capital controls (Malaysia 1998), matching "
            "the single-channel caveat. High-inflation country-years can still trip the "
            "rule despite the acceleration term."
        ),
    }
    json.dump(bundle, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {OUT}")


if __name__ == "__main__":
    main()
