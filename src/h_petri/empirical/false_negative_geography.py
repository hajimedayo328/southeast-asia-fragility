"""
false_negative_geography.py — 取りこぼし(偽陰性 FN=298: 危機なのにG-G警告が出なかった国年)が
地域・時期・国に偏るかを見る。目的②「最良スカラーの失敗は国家間の構造に落ちる」の最初の実データ。

方針: 既存 false_positive_panel のロジックを import してそのまま使い、混同行列カウントが
元(TP163/FP487/FN298/TN2503)と一致することを assert で保証してから FN を分解する
(再実装での取り違えを防ぐ=過去の「自前再構築で誤判定」教訓の回避)。新規データ収集なし。
"""
from __future__ import annotations
import sys, statistics
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import false_positive_panel as fp  # noqa: E402  ← 既存ロジックをそのまま使う


def decade(y: int) -> str:
    return f"{(y // 10) * 10}s"


def main():
    meta = fp.load_real_countries()
    real = set(meta)
    signal = {k: v / 100.0 for k, v in fp.load_series("st_debt_reserves", real).items()}
    fx = fp.load_series("fx_lcu_per_usd", real)
    D, A = fp.CRASH_RULES[fp.PRIMARY_RULE]
    d1 = fp.changes(fx, real, 1)
    d2 = fp.changes(fx, real, 2)
    crash = fp.crash_years(d1, d2, D, A)
    onset = fp.onsets(crash)
    theta, k = fp.PRIMARY_THETA, fp.PRIMARY_K

    counts: Counter = Counter()
    FN, TP = [], []
    for (c, t), ratio in signal.items():
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            continue
        if (c, t) in crash:
            continue
        sig = ratio > theta
        crisis = any((c, t + j) in onset for j in range(1, k + 1))
        cell = ("TP" if sig and crisis else "FP" if sig and not crisis
                else "FN" if crisis else "TN")
        counts[cell] += 1
        if cell == "FN":
            FN.append((c, t, ratio))
        elif cell == "TP":
            TP.append((c, t, ratio))

    # ---- ロジック再現の検証(合わなければ止める) ----
    assert (counts["FN"], counts["TP"], counts["FP"], counts["TN"]) == (298, 163, 487, 2503), \
        f"混同行列が既存パネルと不一致: {dict(counts)} — 分解を信用しない"
    print("✓ 混同行列を再現: FN=298 / TP=163 / FP=487 / TN=2503 = 既存パネルと一致\n")

    def region(c):
        return (meta[c].get("region") or {}).get("value", "?")

    def cname(c):
        return meta[c].get("name", c)

    # ---- 地域分布: FN と TP を並べ、取りこぼし率を見る ----
    print("=== 取りこぼし(FN)の地域分布 vs 的中(TP) — FN率が高い地域=構造的に見えていない ===")
    regions = sorted({region(c) for c, _, _ in FN} | {region(c) for c, _, _ in TP})
    fn_reg = Counter(region(c) for c, _, _ in FN)
    tp_reg = Counter(region(c) for c, _, _ in TP)
    print(f"  {'region':34s} {'FN':>4} {'TP':>4} {'FN率':>6}")
    for r in sorted(regions, key=lambda r: -(fn_reg[r] + tp_reg[r])):
        fnv, tpv = fn_reg[r], tp_reg[r]
        rate = fnv / (fnv + tpv) if (fnv + tpv) else 0.0
        print(f"  {r:34s} {fnv:4d} {tpv:4d} {rate:6.2f}")

    # ---- 年代分布 ----
    print("\n=== 取りこぼしの年代分布 vs 的中 ===")
    fn_dec = Counter(decade(t) for _, t, _ in FN)
    tp_dec = Counter(decade(t) for _, t, _ in TP)
    for d in sorted(set(fn_dec) | set(tp_dec)):
        fnv, tpv = fn_dec.get(d, 0), tp_dec.get(d, 0)
        rate = fnv / (fnv + tpv) if (fnv + tpv) else 0.0
        print(f"  {d:8s} FN={fnv:4d} TP={tpv:4d} FN率={rate:.2f}")

    # ---- 国別 top ----
    print("\n=== 取りこぼしが多い国 top12 ===")
    for name, cnt in Counter(cname(c) for c, _, _ in FN).most_common(12):
        print(f"  {name:30s} {cnt}")

    # ---- 偽陰性のG-G比の分布: 「惜しい見逃し」か「指標が全く見えてない」か ----
    fn_ratios = [r for _, _, r in FN]
    print("\n=== 取りこぼし時のG-G比(短期外債/準備) — 指標が構造的に見えていないかの判定 ===")
    print(f"  median={statistics.median(fn_ratios):.2f}  mean={statistics.mean(fn_ratios):.2f}")
    print(f"  G-G比>1.0(警告水準)の割合 = {sum(1 for r in fn_ratios if r > 1) / len(fn_ratios):.2f}")
    print(f"  G-G比>0.5 の割合         = {sum(1 for r in fn_ratios if r > 0.5) / len(fn_ratios):.2f}")
    print(f"  G-G比<0.3(全く低い)の割合 = {sum(1 for r in fn_ratios if r < 0.3) / len(fn_ratios):.2f}")

    # ---- 読み(データが出す判定、盛らない) ----
    top_reg, top_n = fn_reg.most_common(1)[0]
    share = top_n / counts["FN"]
    print("\n--- 判定の材料 ---")
    print(f"最も取りこぼしが多い地域 = {top_reg} が FN の {share:.0%} を占める。")
    print("FN率が地域で大きく割れる & 見逃し時のG-G比が低い(<1)なら、"
          "「指標が構造的に見えない危機がある」= 目的②の芽。均等なら§4は弱い(正直に)。")


if __name__ == "__main__":
    main()
