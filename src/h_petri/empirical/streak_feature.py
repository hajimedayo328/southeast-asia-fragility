# -*- coding: utf-8 -*-
# notes/45: streak(連続点灯月数)を第3の材料に昇格できるかの主検定
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit, auc

H = 6
Q = 0.10
CAP = 24


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
            tf = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
            lab = 1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
            rows.append([c, i, g, tf, 0.0, 0.0, lab])   # [4]=streak [5]=share12
    train0 = [r for r in rows if r[1] < 2000 * 12]
    e_g = make_ecdf([r[2] for r in train0])
    e_t = make_ecdf([r[3] for r in train0])
    pos = [r for r in train0 if r[6] == 1]
    neg = [r for r in train0 if r[6] == 0]
    rng = random.Random(101)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    wB, bB = fit_logit([[e_g(r[2]), e_t(r[3])] for r in sub], [r[6] for r in sub])

    # 全期間の点灯とstreak/share12
    bym = defaultdict(list)
    for r in rows:
        bym[r[1]].append((bB + wB[0] * e_g(r[2]) + wB[1] * e_t(r[3]), r[0]))
    lit = set()
    for i, lst in bym.items():
        lst.sort(reverse=True)
        n = len(lst)
        for p_, (s, c) in enumerate(lst):
            if p_ / n <= Q:
                lit.add((c, i))
    streak = {}
    for c, i in sorted(lit, key=lambda k: k[1]):
        streak[(c, i)] = min(CAP, streak.get((c, i - 1), 0) + 1)
    for r in rows:
        r[4] = float(streak.get((r[0], r[1]), 0))
        r[5] = sum(1 for k in range(12) if (r[0], r[1] - k) in lit) / 12.0

    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]

    def build(feats, seed):
        ecs = [make_ecdf([r[f] for r in train]) for f in feats]
        p2 = [r for r in train if r[6] == 1]
        n2 = [r for r in train if r[6] == 0]
        rng2 = random.Random(seed)
        sub2 = p2 + rng2.sample(n2, min(len(n2), 5 * len(p2)))
        X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub2]
        w, b = fit_logit(X, [r[6] for r in sub2])
        return (lambda r: b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))), w

    y_te = [r[6] for r in test]
    s1, _ = build([2, 3], 102)
    s2, w2 = build([2, 3, 4], 102)
    s3, w3 = build([2, 3, 5], 102)
    a1 = auc([s1(r) for r in test], y_te)
    a2 = auc([s2(r) for r in test], y_te)
    a3 = auc([s3(r) for r in test], y_te)
    byc = defaultdict(list)
    for r in test:
        byc[r[0]].append(r)
    cl = sorted(byc); rng3 = random.Random(103); ds = []; ds3 = []
    for bb in range(300):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng3.choice(cl)])
        yv = [r[6] for r in s]
        v1 = auc([s1(r) for r in s], yv)
        v2 = auc([s2(r) for r in s], yv)
        v3 = auc([s3(r) for r in s], yv)
        if v1 is not None and v2 is not None:
            ds.append(v2 - v1)
        if v1 is not None and v3 is not None:
            ds3.append(v3 - v1)
    ds.sort(); ds3.sort(); n = len(ds); m = len(ds3)
    d = a2 - a1
    L = ['', f'STREAK-FEATURE 2026-07-20 (notes/45。h={H}, panel={len(rows)}, q10点灯のstreakを第3材料に)',
         f'主検定: GG+TF={a1:.4f} +streak={a2:.4f} delta={d:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] 係数={["%.2f" % x for x in w2]}',
         f'  -> {"PASS: 警報の第3の材料(自己履歴)" if ds[int(.025*n)] > 0 and d >= 0.03 else "FAIL"}',
         f'副次(代替定義 12ヶ月点灯シェア): +share12={a3:.4f} delta={a3-a1:+.4f} CI[{ds3[int(.025*m)]:+.4f},{ds3[int(.975*m)]:+.4f}]']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
