# -*- coding: utf-8 -*-
# 月次見逃し解剖 (notes/42 EXP-B・記述): test期のonsetを警報が捕まえていたか、
# 見逃しは「静かな死」だったのかを分解する
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit


def main():
    fxm = load_fxm()
    crash_m = {iso: fx_crash_months(fxm[iso]) for iso in fxm}
    crash_idx = {iso: {y * 12 + m - 1 for (y, m) in cr} for iso, cr in crash_m.items()}
    onset_idx = defaultdict(set)
    for iso, cr in crash_m.items():
        idxs = {y * 12 + m - 1 for (y, m) in cr}
        for (y, m) in sorted(cr):
            i = y * 12 + m - 1
            if not any((i - k) in idxs for k in range(1, 13)):
                onset_idx[iso].add(i)
    meta = fp.load_real_countries(); real = set(meta)
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    trade = defaultdict(lambda: defaultdict(dict))
    with open(ROOT / 'data_raw/imts_trade_xm.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, xv, mv in r:
            try:
                y = int(yr); v = float(xv) + float(mv)
            except ValueError:
                continue
            if v > 0:
                trade[rep][y][cp] = v
    wcache = {}

    def weights(c, y):
        key = (c, y)
        if key not in wcache:
            w = trade.get(c, {}).get(y - 1, {})
            tot = sum(w.values())
            wcache[key] = {j: v / tot for j, v in w.items()} if len(w) >= 3 and tot > 0 else None
        return wcache[key]

    # 特徴量(スコア対象は「危機状態でない国月」= 運用パネルと同一)
    feat = {}   # (c,i) -> (g, tf)
    for c in sorted({c for (c, _) in gg}):
        fxd = fxm.get(c)
        if not fxd:
            continue
        for i in range(1978 * 12, 2025 * 12 + 6):
            y = i // 12; m = i % 12 + 1
            if i in crash_idx.get(c, set()) or (y, m) not in fxd:
                continue
            g = gg.get((c, y - 1))
            if g is None or not math.isfinite(g):
                continue
            W = weights(c, y)
            if W is None:
                continue
            tf = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
            feat[(c, i)] = (g, tf)

    H = 6
    train = [(c, i, g, tf) for (c, i), (g, tf) in feat.items() if i < 2000 * 12]
    lab_tr = [1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
              for (c, i, g, tf) in train]
    e_g = make_ecdf([r[2] for r in train])
    e_t = make_ecdf([r[3] for r in train])
    pos = [(r, l) for r, l in zip(train, lab_tr) if l == 1]
    neg = [(r, l) for r, l in zip(train, lab_tr) if l == 0]
    rng = random.Random(91)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    X = [[e_g(r[2]), e_t(r[3])] for r, _ in sub]
    w, b = fit_logit(X, [l for _, l in sub])

    def score(g, tf):
        return b + w[0] * e_g(g) + w[1] * e_t(tf)

    # 月ごとの国横断ランキング(test期)
    bym = defaultdict(list)
    for (c, i), (g, tf) in feat.items():
        if i >= 2000 * 12:
            bym[i].append((score(g, tf), c, g, tf))
    rank_pct = {}   # (c,i) -> 上位パーセンタイル(0=最上位)
    med_g = {}
    for i, lst in bym.items():
        lst.sort(reverse=True)
        n = len(lst)
        gs = sorted(x[2] for x in lst)
        med_g[i] = gs[n // 2]
        for pos_, (s, c, g, tf) in enumerate(lst):
            rank_pct[(c, i)] = pos_ / n

    # test期のonsetを判定
    onsets_te = [(c, i0) for c, s in onset_idx.items() for i0 in s
                 if i0 >= 2000 * 12 and i0 < 2025 * 12]
    caught10 = caught20 = nofeat = 0
    quiet = outranked = 0
    for c, i0 in onsets_te:
        pre = [(c, j) for j in range(i0 - H, i0)]
        pcts = [rank_pct[k] for k in pre if k in rank_pct]
        if not pcts:
            nofeat += 1
            continue
        best = min(pcts)
        if best <= 0.10:
            caught10 += 1
        if best <= 0.20:
            caught20 += 1
        if best > 0.10:
            # 見逃し(q10)の内訳
            had_fire = any(feat[k][1] > 0 for k in pre if k in feat)
            g_hi = any(feat[k][0] >= med_g.get(k[1], math.inf) for k in pre if k in feat)
            if not had_fire and not g_hi:
                quiet += 1
            else:
                outranked += 1
    n_all = len(onsets_te)
    n_sc = n_all - nofeat
    miss10 = n_sc - caught10
    L = ['', f'MISS-ANATOMY-M 2026-07-20 (notes/42 EXP-B・記述: test>=2000のonset{n_all}件, 警報=前{H}ヶ月にq10/q20点灯)',
         f'  スコア不能(データ欠落): {nofeat}件 / 判定対象 {n_sc}件',
         f'  捕捉率: q10={caught10}/{n_sc}={caught10/n_sc:.1%}  q20={caught20}/{n_sc}={caught20/n_sc:.1%}',
         f'  見逃し(q10)={miss10}件の内訳: 静かな死(火ゼロかつGG中央値未満)={quiet}件({quiet/max(1,miss10):.0%}) / 信号ありだが順位負け={outranked}件({outranked/max(1,miss10):.0%})']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
