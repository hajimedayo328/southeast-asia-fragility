"""
combine_indicators.py — 弱い2指標(G-G と broad money/準備)の「独立性」を測り、
合成(和・差・max・min)が単独 AUC を超えるか検証する。

狙い: 単独はどちらも AUC≈0.6 で弱い。だが2つが独立(別々の危機を捉える)なら、
標準化して合成するとシグナルが加算されノイズが平均化され、単独を超えうる。
超えれば「弱い借り物指標×2 を独立性で合成した新指標」＝オリジナルな貢献の芽。

AUC は順位ベース(単調変換不変)なので、標準化しても単独指標の AUC は変わらない。
効くのは合成(和/差)のときのスケール整合。共通サンプルで in-sample 標準化(探索段階の注記)。
"""
from __future__ import annotations
import sys
import statistics
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import false_positive_panel as fp  # noqa: E402


def auc(scores, labels):
    pos = sum(labels)
    neg = len(labels) - pos
    if pos == 0 or neg == 0:
        return None
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
    sp = sum(ranks[i] for i in range(len(scores)) if labels[i] == 1)
    return (sp - pos * (pos + 1) / 2.0) / (pos * neg)


def pearson(xs, ys):
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    sx, sy = statistics.pstdev(xs), statistics.pstdev(ys)
    return cov / (sx * sy) if sx and sy else None


def main():
    meta = fp.load_real_countries()
    real = set(meta)
    gg = {k: v / 100.0 for k, v in fp.load_series("st_debt_reserves", real).items()}
    bm = fp.load_series("broad_money_reserves", real)
    fx = fp.load_series("fx_lcu_per_usd", real)
    D, A = fp.CRASH_RULES[fp.PRIMARY_RULE]
    crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D, A)
    onset = fp.onsets(crash)
    k = fp.PRIMARY_K

    def eligible(c, t):
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            return False
        return (c, t) not in crash

    def label(c, t):
        return 1 if any((c, t + j) in onset for j in range(1, k + 1)) else 0

    common = [(c, t) for (c, t) in gg if (c, t) in bm and eligible(c, t)]
    y = [label(c, t) for (c, t) in common]
    print(f"共通サンプル {len(common)} 国年 / 危機 {sum(y)}\n")

    # 危険方向に符号統一(gg 高=危険, bm 高=危険) → z 標準化
    def z(series):
        vals = [series[k] for k in common]
        m, s = statistics.mean(vals), statistics.pstdev(vals)
        return {k: (series[k] - m) / s for k in common}

    zg, zb = z(gg), z(bm)

    corr = pearson([zg[k] for k in common], [zb[k] for k in common])
    print(f"独立性: corr(G-G, broad money) = {corr:+.3f}  "
          f"(0近辺=独立=相補の可能性 / 高い=同じ情報)\n")

    cand = {
        "G-G 単独": {k: zg[k] for k in common},
        "broad money 単独": {k: zb[k] for k in common},
        "和  z(GG)+z(BM)": {k: zg[k] + zb[k] for k in common},
        "差  z(GG)-z(BM)": {k: zg[k] - zb[k] for k in common},
        "max(両方の高い方)": {k: max(zg[k], zb[k]) for k in common},
        "min(両方高い時のみ)": {k: min(zg[k], zb[k]) for k in common},
    }
    print("=== AUC 比較(共通サンプル・閾値フリー) ===")
    base = {}
    for name, sc in cand.items():
        a = auc([sc[k] for k in common], y)
        base[name] = a
        print(f"  {name:22s} AUC = {a:.3f}")

    best_single = max(base["G-G 単独"], base["broad money 単独"])
    print("\n--- 判定 ---")
    print(f"単独ベスト = {best_single:.3f}")
    for name in ["和  z(GG)+z(BM)", "差  z(GG)-z(BM)", "max(両方の高い方)", "min(両方高い時のみ)"]:
        d = base[name] - best_single
        flag = "★単独超え" if d > 0.005 else ("横ばい" if abs(d) <= 0.005 else "下回る")
        print(f"  {name:22s} Δ={d:+.3f}  {flag}")
    print("※ 相関が低い(独立)ほど合成の伸びしろが大きい理論。伸びれば新規性の芽、"
          "横ばいなら『合成しても情報増えず』。有意性は並べ替え検定で別途。")


if __name__ == "__main__":
    main()
