# -*- coding: utf-8 -*-
# TF2の裁き (notes/42 EXP-A): 分割年1995/2005でh=3のTF2限界寄与を再検定
# 昇格 = 両分割で delta>=+0.03 かつ 国ブロックCIが0を除外
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit, auc


def build_panel(H=3):
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

    fire = defaultdict(dict)
    all_c = sorted({c for (c, _) in gg} | set(crash_idx))
    for c in all_c:
        for i in range(1977 * 12, 2025 * 12 + 6):
            W = weights(c, i // 12)
            if W is None:
                continue
            f = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
            if f > 0:
                fire[c][i] = f
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
            tf = fire[c].get(i, 0.0)
            tf2 = sum(v * fire[j].get(i, 0.0) for j, v in W.items() if j in fire)
            lab = 1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
            rows.append((c, i, g, tf, tf2, lab))
    return rows


def run_split(rows, split_year, seed):
    train = [r for r in rows if r[1] < split_year * 12]
    test = [r for r in rows if r[1] >= split_year * 12]

    def build(feats):
        ecs = [make_ecdf([r[f] for r in train]) for f in feats]
        pos = [r for r in train if r[5] == 1]
        neg = [r for r in train if r[5] == 0]
        rng = random.Random(seed)
        sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
        X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub]
        w, b = fit_logit(X, [r[5] for r in sub])
        return lambda r: b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))
    s1 = build([2, 3]); s2 = build([2, 3, 4])
    y_te = [r[5] for r in test]
    a1 = auc([s1(r) for r in test], y_te)
    a2 = auc([s2(r) for r in test], y_te)
    byc = defaultdict(list)
    for r in test:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(seed + 1); ds = []
    for b in range(300):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        yv = [r[5] for r in s]
        v1 = auc([s1(r) for r in s], yv); v2 = auc([s2(r) for r in s], yv)
        if v1 is not None and v2 is not None:
            ds.append(v2 - v1)
    ds.sort(); n = len(ds)
    return a1, a2, ds[int(.025 * n)], ds[int(.975 * n)]


def main():
    rows = build_panel(H=3)
    print(f'panel: {len(rows)} rows')
    L = ['', 'TF2-VERDICT 2026-07-20 (notes/42 EXP-A: h=3のTF2を分割年1995/2005で裁く。昇格=両方でdelta>=+0.03かつCI0除外)']
    ok = 0
    for sy, seed in ((1995, 81), (2005, 83)):
        a1, a2, lo, hi = run_split(rows, sy, seed)
        d = a2 - a1
        hit = lo > 0 and d >= 0.03
        ok += hit
        L.append(f'  分割{sy}: GG+TF={a1:.4f} +TF2={a2:.4f} delta={d:+.4f} CI[{lo:+.4f},{hi:+.4f}] -> {"通過" if hit else "不通過"}')
    L.append(f'裁定: {"昇格(両分割通過)" if ok == 2 else "示唆どまりで確定・この問いは閉じる"} ({ok}/2)')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
