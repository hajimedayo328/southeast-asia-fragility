# -*- coding: utf-8 -*-
# 火事の動力学 (notes/41・事前固定): EXP-A 減衰プロファイル / EXP-B 2ホップ火事
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit, auc

I0, I1 = 1977 * 12, 2025 * 12 + 6  # fire計算はパネルより1年早くから(ラグ窓用)


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

    # fire_j(i) を全国・全月について前計算 (crash集合を持つ国のみ寄与)
    print('precomputing fire table...')
    fire = defaultdict(dict)  # fire[c][i]
    all_c = sorted({c for (c, _) in gg} | set(crash_idx))
    for c in all_c:
        for i in range(I0, I1):
            W = weights(c, i // 12)
            if W is None:
                continue
            f = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
            if f > 0:
                fire[c][i] = f
    print(f'fire table: {sum(len(v) for v in fire.values())} nonzero entries')

    H = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    WINDOWS ={'W0': [0], 'W1': [1, 2, 3], 'W2': [4, 5, 6], 'W3': list(range(7, 13)),
               'W03': [0, 1, 2, 3]}
    rows = []
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
            fw = {nm: sum(fire[c].get(i - k, 0.0) for k in ks) / len(ks)
                  for nm, ks in WINDOWS.items()}
            tf2 = sum(v * fire[j].get(i, 0.0) for j, v in W.items() if j in fire)
            lab = 1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
            rows.append((c, i, g, fw['W0'], fw['W1'], fw['W2'], fw['W3'], fw['W03'], tf2, lab))
    print(f'panel: {len(rows)} rows, positives={sum(r[9] for r in rows)}')
    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]
    LAB = 9

    def build(feats):
        ecs = [make_ecdf([r[f] for r in train]) for f in feats]
        pos = [r for r in train if r[LAB] == 1]
        neg = [r for r in train if r[LAB] == 0]
        rng = random.Random(71)
        sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
        X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub]
        w, b = fit_logit(X, [r[LAB] for r in sub])
        return (lambda r: b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))), w

    def block_ci(sA, sB, seed):
        byc = defaultdict(list)
        for r in test:
            byc[r[0]].append(r)
        cl = sorted(byc); rng = random.Random(seed); ds = []
        for b in range(300):
            s = []
            for _ in range(len(cl)):
                s.extend(byc[rng.choice(cl)])
            yv = [r[LAB] for r in s]
            v1 = auc([sA(r) for r in s], yv); v2 = auc([sB(r) for r in s], yv)
            if v1 is not None and v2 is not None:
                ds.append(v1 - v2)
        ds.sort()
        return ds[int(.025 * len(ds))], ds[int(.975 * len(ds))]

    y_te = [r[LAB] for r in test]
    L = ['', f'FIRE-DYNAMICS 2026-07-20 (notes/41事前固定。h={H}, panel={len(rows)})']
    # EXP-A: 窓別プロファイル
    scores = {}
    for nm, f in [('W0(当月)', 3), ('W1(1-3月前)', 4), ('W2(4-6月前)', 5), ('W3(7-12月前)', 6), ('W03(0-3月前)', 7)]:
        sc, _ = build([2, f])
        scores[nm] = sc
        L.append(f'  GG+{nm}: AUC={auc([sc(r) for r in test], y_te):.4f}')
    lo, hi = block_ci(scores['W03(0-3月前)'], scores['W3(7-12月前)'], 72)
    a_new = auc([scores['W03(0-3月前)'](r) for r in test], y_te)
    a_old = auc([scores['W3(7-12月前)'](r) for r in test], y_te)
    L.append(f'EXP-A主検定: 新しい火(0-3月)={a_new:.4f} vs 古い火(7-12月)={a_old:.4f} Δ={a_new-a_old:+.4f} CI[{lo:+.4f},{hi:+.4f}] -> {"PASS: 火は数ヶ月で減衰する" if lo > 0 else "FAIL: 12ヶ月ほぼ均一に残る"}')
    # EXP-B: 2ホップの限界寄与
    s1, _ = build([2, 3])
    s2, w2 = build([2, 3, 8])
    a1 = auc([s1(r) for r in test], y_te)
    a2 = auc([s2(r) for r in test], y_te)
    lo2, hi2 = block_ci(s2, s1, 73)
    L.append(f'EXP-B主検定: GG+TF={a1:.4f} vs +TF2(2ホップ)={a2:.4f} delta={a2-a1:+.4f} CI[{lo2:+.4f},{hi2:+.4f}] 係数={["%.2f" % x for x in w2]}')
    L.append(f'  -> {"PASS" if lo2 > 0 and a2 - a1 >= 0.03 else "FAIL: 伝染は実質1ホップ"}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
