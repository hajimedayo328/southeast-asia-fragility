"""
crisis_synchrony.py — 通貨危機の「同時発生(伝染の痕跡)」を測り、単一スカラー(G-G)の
取りこぼし(FN)が"同時多発危機"に偏るかを検証する。

賭けの仮説: 単一国のスカラー指標は、複数国が同時に落ちる伝染性成分を原理的に捉えにくい。
→ 取りこぼした危機(FN)は、孤発危機より同時多発年の危機に偏るのでは。もし偏れば
「単一指標は伝染性危機を構造的に見逃す＝ネットワーク視点が要る」の実データ根拠になる。

既存 false_positive_panel を import(crash/onset/eligible/label を流用、混同行列一致を assert)。
"""
from __future__ import annotations
import sys
from collections import Counter, defaultdict
from pathlib import Path
import statistics

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import false_positive_panel as fp  # noqa: E402


def main():
    meta = fp.load_real_countries()
    real = set(meta)
    gg = {k: v / 100.0 for k, v in fp.load_series("st_debt_reserves", real).items()}
    fx = fp.load_series("fx_lcu_per_usd", real)
    D, A = fp.CRASH_RULES[fp.PRIMARY_RULE]
    crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D, A)
    onset = fp.onsets(crash)
    theta, k = fp.PRIMARY_THETA, fp.PRIMARY_K

    # ---- (1) 危機の時間的クラスタリング(伝染の痕跡) ----
    onset_years = [y for (_, y) in onset]
    by_year = Counter(onset_years)
    ymin, ymax = min(onset_years), max(onset_years)
    counts = [by_year.get(y, 0) for y in range(ymin, ymax + 1)]
    mean = statistics.mean(counts)
    var = statistics.pvariance(counts)
    disp = var / mean if mean else None
    print("=== (1) 危機onsetの時間的クラスタリング ===")
    print(f"  対象年 {ymin}–{ymax}, 総onset {len(onset)} 件")
    print(f"  年あたり危機国数: mean={mean:.2f}  var={var:.2f}  分散指数(var/mean)={disp:.2f}")
    print(f"  → 1.0=ランダム(ポアソン)。>>1 なら過分散=特定年に集中=伝染/共通ショックの痕跡")
    top = sorted(by_year.items(), key=lambda kv: -kv[1])[:8]
    print("  危機集中年 top8: " + ", ".join(f"{y}({n})" for y, n in top))

    # ---- (2) TP/FN を、その危機の「同時多発度」で層別 ----
    # eligible tranquil (c,t) で 2y以内に onset があるものが「危機ケース」。
    # その危機の代表年 t* = 窓内で最初に当たった onset の年。同時多発度 = by_year[t*](その年の全危機国数)。
    counts_cell = Counter()
    tp_sync, fn_sync = [], []
    for (c, t), ratio in gg.items():
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            continue
        if (c, t) in crash:
            continue
        sig = ratio > theta
        hit_years = [t + j for j in range(1, k + 1) if (c, t + j) in onset]
        crisis = bool(hit_years)
        cell = ("TP" if sig and crisis else "FP" if sig and not crisis
                else "FN" if crisis else "TN")
        counts_cell[cell] += 1
        if crisis:
            tstar = hit_years[0]
            sync = by_year[tstar]              # その危機年に同時に危機だった国数
            (tp_sync if sig else fn_sync).append(sync)

    assert (counts_cell["TP"], counts_cell["FP"], counts_cell["FN"], counts_cell["TN"]) \
        == (163, 487, 298, 2503), f"混同行列不一致 {dict(counts_cell)}"
    print("\n✓ 混同行列を再現(163/487/298/2503)")

    print("\n=== (2) 的中(TP)危機 vs 取りこぼし(FN)危機：同時多発度の比較 ===")
    print(f"  的中TP   n={len(tp_sync):3d}  同時危機数 median={statistics.median(tp_sync):.1f} "
          f"mean={statistics.mean(tp_sync):.2f}")
    print(f"  見逃しFN n={len(fn_sync):3d}  同時危機数 median={statistics.median(fn_sync):.1f} "
          f"mean={statistics.mean(fn_sync):.2f}")

    # 高同時発生(その年に危機国数>=中央値の2倍など)で FN率が上がるか
    thr = statistics.median(counts) if False else 6  # その年6カ国以上同時=高伝染年(閾値は明示)
    def frac_high(xs):
        return sum(1 for s in xs if s >= thr) / len(xs) if xs else 0.0
    print(f"\n  「高同時発生年(同年に{thr}カ国以上)」の危機の割合:")
    print(f"    的中TP  : {frac_high(tp_sync):.2f}")
    print(f"    見逃しFN: {frac_high(fn_sync):.2f}")
    print("  → FN>TP なら『伝染性(同時多発)の危機ほど単一指標が取りこぼす』＝仮説を支持")

    # ---- 賭けの判定材料 ----
    diff = statistics.mean(fn_sync) - statistics.mean(tp_sync)
    print("\n--- 判定の材料 ---")
    print(f"FN同時度 − TP同時度 = {diff:+.2f}(正=取りこぼしほど同時多発＝仮説支持 / 0近辺・負=不支持)")
    print("※ これは相関の材料。有意性(並べ替え検定)と robustness は research-verification で。")


if __name__ == "__main__":
    main()
