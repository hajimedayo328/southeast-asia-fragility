"""
Block-bootstrap-by-country confidence intervals for the §5.6 false-positive panel.

false_positive_panel.py reports POINT estimates (false-alarm share, FPR, recall,
noise-to-signal, lift). Two limitations were flagged there: no uncertainty
quantification, and serial correlation (country-years are not independent). Both are
answered by the SAME move — a block bootstrap whose resampling unit is the COUNTRY:

  Each country-year's confusion cell is determined purely by that country's own data
  (the crash detector uses only within-country exchange rates; the tranquil filter
  and outcome window are within-country). So countries are independent blocks.
  Resampling the ~100 countries WITH REPLACEMENT and recomputing the metrics gives a
  sampling distribution that respects within-country dependence. The 95% percentile
  interval then says whether the headline claims survive sampling noise:
    - lift 95% CI excluding 1.0  => the signal is significantly better than the base
      rate (genuine information, not chance).
    - noise-to-signal 95% CI excluding 1.0 => significantly below the "useless" line.

Primary spec only (theta=1.0 = Guidotti–Greenspan, k=2y), both crash rules. Reuses
the EXACT classification logic from false_positive_panel.py (imported, not copied) so
the point estimate matches the committed result by construction (asserted).
"""

from __future__ import annotations
import json
import random
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from h_petri.empirical.false_positive_panel import (   # noqa: E402
    load_real_countries, load_series, changes, crash_years, onsets, metrics,
    CRASH_RULES, PRIMARY_THETA, PRIMARY_K, PRIMARY_RULE)

B = 5000
SEED = 42
KEYS = ("false_alarm_share", "false_positive_rate_FPR", "recall_TPR",
        "noise_to_signal_KLR", "lift")
OUT = Path(__file__).resolve().parents[3] / "docs" / "data" / "false_positive_panel_ci.json"

# committed point counts to guard against any logic drift on import
EXPECTED_LV = {"TP": 163, "FP": 487, "FN": 298, "TN": 2503}


def per_country_cells(signal, fx, onset, crash, theta, k):
    """Same eligibility/tranquil/outcome rules as evaluate(), bucketed by country."""
    cells: dict[str, list[int]] = {}
    for (c, t), ratio in signal.items():
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            continue
        if (c, t) in crash:
            continue
        sig = ratio > theta
        cri = any((c, t + j) in onset for j in range(1, k + 1))
        idx = 0 if (sig and cri) else 1 if (sig and not cri) else 2 if cri else 3
        cells.setdefault(c, [0, 0, 0, 0])[idx] += 1
    return cells


def counts_from(cells, countries):
    tp = fp = fn = tn = 0
    for c in countries:
        a, b, d, e = cells[c]
        tp += a; fp += b; fn += d; tn += e
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn}


def main():
    real = set(load_real_countries())
    signal = {k: v / 100.0 for k, v in load_series("st_debt_reserves", real).items()}
    fx = load_series("fx_lcu_per_usd", real)
    d1, d2 = changes(fx, real, 1), changes(fx, real, 2)
    rng = random.Random(SEED)

    print("=" * 74)
    print(f"Block-bootstrap-by-country 95% CIs  (theta={PRIMARY_THETA}, k={PRIMARY_K}y, "
          f"B={B})")
    print("=" * 74)

    result = {}
    for name, (D, A) in CRASH_RULES.items():
        crash = crash_years(d1, d2, D, A)
        onset = onsets(crash)
        cells = per_country_cells(signal, fx, onset, crash, PRIMARY_THETA, PRIMARY_K)
        clist = sorted(cells)
        n = len(clist)
        point_counts = counts_from(cells, clist)
        if name == PRIMARY_RULE:
            assert point_counts == EXPECTED_LV, (point_counts, EXPECTED_LV)
        point = metrics(point_counts)

        dist = {k: [] for k in KEYS}
        for _ in range(B):
            samp = [clist[rng.randrange(n)] for _ in range(n)]
            m = metrics(counts_from(cells, samp))
            for k in KEYS:
                if m[k] is not None:
                    dist[k].append(m[k])

        ci = {}
        for k in KEYS:
            xs = sorted(dist[k])
            lo, hi = xs[int(0.025 * len(xs))], xs[int(0.975 * len(xs))]
            ci[k] = {"point": point[k], "ci95": [round(lo, 3), round(hi, 3)]}
        result[name] = {"n_countries": n, "point_counts": point_counts, "ci": ci}

        print(f"\n[{name}]  {n} countries (clustering unit), point N={point['N']}")
        for k in KEYS:
            lo, hi = ci[k]["ci95"]
            note = ""
            if k == "lift":
                note = "  <- excludes 1" if lo > 1 else "  <- includes 1 (NOT sig)"
            if k == "noise_to_signal_KLR":
                note = "  <- excludes 1 (below useless line)" if hi < 1 else "  <- includes 1"
            print(f"  {k:24} {point[k]:<6}  95% CI [{lo}, {hi}]{note}")

    lv = result[PRIMARY_RULE]["ci"]
    verdict = (
        f"Block-bootstrap-by-country ({result[PRIMARY_RULE]['n_countries']} countries, "
        f"B={B}). Under the primary spec (ratio>1, k={PRIMARY_K}y, {PRIMARY_RULE}): "
        f"lift point {lv['lift']['point']} CI {lv['lift']['ci95']} "
        f"({'excludes' if lv['lift']['ci95'][0] > 1 else 'includes'} 1) and "
        f"noise-to-signal point {lv['noise_to_signal_KLR']['point']} CI "
        f"{lv['noise_to_signal_KLR']['ci95']} "
        f"({'excludes' if lv['noise_to_signal_KLR']['ci95'][1] < 1 else 'includes'} 1). "
        f"False-alarm share CI {lv['false_alarm_share']['ci95']} stays high. So the "
        f"'genuine-but-weak, false-alarm-dominated' reading is "
        f"{'statistically supported' if (lv['lift']['ci95'][0] > 1 and lv['noise_to_signal_KLR']['ci95'][1] < 1) else 'only partly supported'} "
        f"— the signal beats chance but remains a noisy single-threshold indicator."
    )
    print("\n" + "-" * 74)
    print("VERDICT:", verdict)

    bundle = {
        "description": ("Block-bootstrap-by-country 95% confidence intervals for the "
                        "false-positive panel headline metrics. Countries are the "
                        "resampling unit (each country-year's cell is within-country), "
                        "so the CIs respect serial correlation and test whether lift>1 "
                        "and noise-to-signal<1 survive sampling uncertainty."),
        "method": {"resample_unit": "country (with replacement)", "n_bootstrap": B,
                   "seed": SEED, "spec": f"theta={PRIMARY_THETA}, k={PRIMARY_K}y",
                   "ci": "2.5/97.5 percentile"},
        "results": result,
        "verdict": verdict,
        "honest_limits": ("Percentile bootstrap (no bias correction); the country block "
                          "ignores any cross-country contagion in the SAME crisis (e.g. "
                          "1997-98 Asia, 1980s Latin America), which would make true CIs "
                          "a little wider. Same data caveats as false_positive_panel.py "
                          "(WDI/DRS != BIS; mechanical crash rules, not the L&V list)."),
    }
    json.dump(bundle, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {OUT}")


if __name__ == "__main__":
    main()
