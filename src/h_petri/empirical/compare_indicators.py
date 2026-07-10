"""
compare_indicators.py — G-G(短期外債/準備) vs broad money/準備 vs 準備の輸入月数 を、
同じ国年サンプル・閾値フリーの AUC で危機予測力を比較し、目的①(有用説 vs 失効説)を裁く。

Aydın–Tunç 2025「broad money/準備の方が効く」を自前パネルで検証。閾値で揃えると恣意が
入るので、閾値非依存の AUC (rank-based, 0.5=偶然) で公平に比べる。危機ラベル・eligible・
crash 判定は false_positive_panel と同一(import して使う)。危険方向に符号を統一:
G-G と broad money は「高い=危険」(+)、準備の輸入月数は「低い=危険」(−)。
"""
from __future__ import annotations
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import false_positive_panel as fp  # noqa: E402


def auc(scores, labels):
    """rank-based AUC = P(score[crisis] > score[no-crisis]). ties は平均順位。"""
    pos = sum(labels)
    neg = len(labels) - pos
    if pos == 0 or neg == 0:
        return None, pos, neg
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j < len(order) and scores[order[j]] == scores[order[i]]:
            j += 1
        avg = (i + j - 1) / 2.0 + 1.0
        for m in range(i, j):
            ranks[order[m]] = avg
        i = j
    sum_pos = sum(ranks[i] for i in range(len(scores)) if labels[i] == 1)
    return (sum_pos - pos * (pos + 1) / 2.0) / (pos * neg), pos, neg


def decade(y):
    return (y // 10) * 10


def main():
    meta = fp.load_real_countries()
    real = set(meta)
    gg = {k: v / 100.0 for k, v in fp.load_series("st_debt_reserves", real).items()}
    bm = fp.load_series("broad_money_reserves", real)     # %  高い=危険
    rm = fp.load_series("reserves_months_imports", real)  # 月数 低い=危険
    fx = fp.load_series("fx_lcu_per_usd", real)
    D, A = fp.CRASH_RULES[fp.PRIMARY_RULE]
    crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D, A)
    onset = fp.onsets(crash)
    k = fp.PRIMARY_K

    indicators = {
        "G-G (std/res)": (gg, +1),
        "broad money/res": (bm, +1),
        "reserves(mo.imp)": (rm, -1),
    }

    def eligible(c, t):
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            return False
        return (c, t) not in crash

    def label(c, t):
        return 1 if any((c, t + j) in onset for j in range(1, k + 1)) else 0

    # 共通サンプル = G-G と broad money 両方に値がある eligible tranquil 国年(公平比較の要)
    common = [(c, t) for (c, t) in gg if (c, t) in bm and eligible(c, t)]
    print(f"共通サンプル(G-G & broad money 両方あり・tranquil・fx cover): {len(common)} 国年")
    print(f"うち危機(2y以内 onset)= {sum(label(c, t) for c, t in common)}\n")

    def eval_auc(keys, series, sign):
        sc, lb = [], []
        for (c, t) in keys:
            if (c, t) in series:
                sc.append(sign * series[(c, t)])
                lb.append(label(c, t))
        return auc(sc, lb)

    print("=== 全期間 AUC（共通サンプル・閾値フリー・0.5=偶然） ===")
    for name, (ser, sign) in indicators.items():
        a, pos, neg = eval_auc(common, ser, sign)
        print(f"  {name:18s} AUC = {a:.3f}   (crisis {pos} / calm {neg})" if a is not None
              else f"  {name:18s} n/a")

    print("\n=== 年代別 AUC（共通サンプル） ===")
    bydec = defaultdict(list)
    for (c, t) in common:
        bydec[decade(t)].append((c, t))
    print("decade   " + "".join(f"{n:>18s}" for n in indicators))
    for d in sorted(bydec):
        row = f"{d}s    "
        for name, (ser, sign) in indicators.items():
            a, _, _ = eval_auc(bydec[d], ser, sign)
            row += f"{(f'{a:.3f}' if a is not None else '-'):>18s}"
        print(row + f"   n={len(bydec[d])}")

    print("\n--- 読み ---")
    print("AUC が高い指標ほど危機予測力が上。broad money が G-G を(特に2000s以降)明確に上回れば")
    print("Aydın–Tunç 失効説を自前で支持。G-G が勝てば有用説寄り。差が小さい/全部0.5近辺なら「どれも弱い」。")
    print("※ AUC は閾値フリーなので、前の lift 分析(閾値θ=1固定)と別角度。両方を突き合わせて判断する。")


if __name__ == "__main__":
    main()
