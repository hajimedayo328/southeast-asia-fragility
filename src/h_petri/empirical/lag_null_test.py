"""
Lag-shrinkage null-model test — attacking our own §T8 claim.

§T8 claims: prediction lags shrink (11→13→12→6→4→3 years), i.e. "the developed
world is catching SEA's fragility faster" (4x acceleration). Two self-critiques
must be tested before that claim is allowed to stand:

  (A) TRUNCATION (right-censoring): a Dev event can only be OBSERVED if it has
      already happened by the horizon (2026). An EA event from 2021 can show a
      lag of at most 5 years; one from 1997 up to 29. So even if true lags were
      IID (no acceleration at all), the observed completed pairs would
      mechanically show "shorter lags for newer events".
  (B) SELECTION: the 6 pairs were chosen post-hoc by the author.

(B) cannot be fixed statistically — it is recorded as a standing limitation.
(A) CAN be tested: simulate the null "lags are IID, independent of EA year",
apply the same truncation (lag ≤ 2026 − ea_year), and ask whether the observed
negative trend is any stronger than what truncation alone produces.

Also computed: the window-utilization diagnostic lag/(2026−ea_year). Under the
acceleration story this ratio should FALL for newer events; under pure
truncation it stays flat-ish; if it RISES, the data actively contradicts
acceleration once the window is accounted for.

Verdict logic is pre-registered here BEFORE running:
  - if observed Spearman is within the central 90% of the null → the shrinkage
    claim is NOT supported beyond truncation → §T8 must be weakened on Pages.
"""

from __future__ import annotations
import json
import random
import statistics as st
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HORIZON = 2026
# (ea_year, observed_lag) from docs/data/trust_timeline.json lag_trend
PAIRS = [(1997, 11), (1997, 13), (2010, 12), (2019, 6), (2020, 4), (2021, 3)]
N_SIM = 20000
SEED = 42


def spearman(xs, ys):
    return st.correlation(xs, ys, method="ranked")


def simulate(null_kind: str, rng: random.Random) -> list[float]:
    """Monte Carlo distribution of Spearman(year, lag) under IID lags + truncation."""
    years = [y for y, _ in PAIRS]
    caps = [HORIZON - y for y in years]
    observed_lags = [l for _, l in PAIRS]
    stats = []
    for _ in range(N_SIM):
        lags = []
        for cap in caps:
            while True:
                if null_kind == "uniform":
                    l = rng.randint(1, 29)
                else:  # "empirical": resample observed lags
                    l = rng.choice(observed_lags)
                if l <= cap:          # truncation: only completed pairs observable
                    lags.append(l)
                    break
        try:
            stats.append(spearman(years, lags))
        except st.StatisticsError:    # constant vector edge case
            continue
    return stats


def main():
    rng = random.Random(SEED)
    years = [y for y, _ in PAIRS]
    lags = [l for _, l in PAIRS]
    obs = spearman(years, lags)

    print("=" * 76)
    print("Lag-shrinkage null test — is §T8 anything beyond truncation?")
    print("=" * 76)
    print(f"\nobserved pairs (year, lag): {PAIRS}")
    print(f"observed Spearman(year, lag) = {obs:+.3f}  (強い負 = 見かけの縮小)")

    # window-utilization diagnostic
    ratios = [l / (HORIZON - y) for y, l in PAIRS]
    rho_ratio = spearman(years, ratios)
    print(f"\n窓利用率 lag/(2026−year): {[round(r,2) for r in ratios]}")
    print(f"Spearman(year, 窓利用率) = {rho_ratio:+.3f}")
    print("→ 正 = 新しい事象ほど『観測可能な窓の上限近く』を使っている")
    print("  (加速ストーリーなら負になるはず)")

    results = {}
    for kind in ("uniform", "empirical"):
        sims = simulate(kind, rng)
        sims_sorted = sorted(sims)
        q05 = sims_sorted[int(0.05 * len(sims))]
        q50 = sims_sorted[len(sims) // 2]
        frac_below = sum(1 for s in sims if s <= obs) / len(sims)
        results[kind] = {
            "null_median_spearman": round(q50, 3),
            "null_5th_percentile": round(q05, 3),
            "fraction_of_null_runs_leq_observed": round(frac_below, 3),
            "observed_within_central_90pct": bool(obs > q05),
        }
        print(f"\n[null = IID {kind} lags + truncation]  ({len(sims)} runs)")
        print(f"  null median Spearman = {q50:+.3f}   (truncation だけで負のトレンドが出る)")
        print(f"  null 5%点            = {q05:+.3f}")
        print(f"  P(null ≤ observed)    = {frac_below:.3f}")

    beyond = all(not r["observed_within_central_90pct"] for r in results.values())
    print("\n" + "-" * 76)
    print("VERDICT (pre-registered):")
    if not beyond:
        print("  観測された負のトレンドは、IID ラグ + 打ち切りの null が生む範囲内。")
        print("  → §T8 の「予言の到達が加速」は **このデータからは主張できない**。")
        print("  → 見かけの縮小の主因は観測窓の打ち切り(+事後選択)。Pages を弱める。")
    else:
        print("  観測トレンドは null の 5%点より極端 → 打ち切りを超えるシグナルの可能性。")
    print(f"  窓利用率は年とともに上昇 (ρ={rho_ratio:+.2f}) — 加速ストーリーと逆向き。")

    bundle = {
        "description": (
            "Null-model test of the §T8 lag-shrinkage claim. Simulates IID lags "
            "with right-truncation at the 2026 observation horizon and compares the "
            "observed Spearman(year, lag) against the null distribution. Also "
            "reports the window-utilization diagnostic lag/(horizon-year)."
        ),
        "observed": {"pairs": PAIRS, "spearman_year_lag": round(obs, 3),
                     "window_utilization": [round(r, 2) for r in ratios],
                     "spearman_year_utilization": round(rho_ratio, 3)},
        "null_models": results,
        "verdict": (
            "NOT SUPPORTED beyond truncation: the observed negative lag trend lies "
            "inside what IID lags + the observation-window cutoff mechanically "
            "produce; and window utilization RISES for newer events (opposite of "
            "acceleration). §T8's '4x faster' framing must be withdrawn/weakened."
            if not beyond else
            "Observed trend exceeds the truncation null at the 5% level."
        ),
        "standing_limitations": (
            "Selection bias (pairs chosen post-hoc) is untestable statistically and "
            "remains; n=6; horizon fixed at 2026; lag definitions depend on which "
            "Dev event is paired."
        ),
        "seed": SEED, "n_sim": N_SIM,
    }
    out = Path(__file__).resolve().parents[3] / "docs" / "data" / "lag_null_test.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
