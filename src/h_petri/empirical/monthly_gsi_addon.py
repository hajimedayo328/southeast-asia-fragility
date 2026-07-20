# -*- coding: utf-8 -*-
# 月次移行の副次(2/2): +GSI (notes/40の事前登録項目)
# GG+TF_m vs GG+TF_m+GSI。GSIは直前の完結四半期(先読み防止)、zはtrain期間統計のみ。
# 合格基準(従来): delta>=+0.03 かつ 国ブロックCIが0を除外
import csv, math, random, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit, auc


def monthly(path):
    acc = defaultdict(list)
    with open(ROOT / path, encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for row in r:
            try:
                acc[(int(row[0][:4]), int(row[0][5:7]))].append(float(row[1]))
            except (ValueError, IndexError):
                continue
    return {k: statistics.mean(v) for k, v in acc.items()}


def build_gsi():
    ff = monthly('data_raw/fred_FEDFUNDS.csv')
    dx1 = monthly('data_raw/fred_TWEXM.csv')
    dx2 = monthly('data_raw/fred_DTWEXBGS.csv')
    dx = dict(dx2); dx.update({k: v for k, v in dx1.items() if k not in dx2})
    oil = monthly('data_raw/fred_WTISPLC.csv'); vix = monthly('data_raw/fred_VIXCLS.csv')
    QS = [(y, q) for y in range(1978, 2027) for q in (1, 2, 3, 4)]

    def qv(d, y, q, chg=False):
        vs = [d[m] for m in [(y, 3*q-2), (y, 3*q-1), (y, 3*q)] if m in d]
        if not vs:
            return None
        cur = statistics.mean(vs)
        if not chg:
            return cur
        vs0 = [d[m] for m in [(y-1, 3*q-2), (y-1, 3*q-1), (y-1, 3*q)] if m in d]
        if not vs0 or statistics.mean(vs0) == 0:
            return None
        return cur / statistics.mean(vs0) - 1
    raw = {'dx': [qv(dx, y, q, True) for y, q in QS], 'oil': [qv(oil, y, q, True) for y, q in QS],
           'ff': [qv(ff, y, q) for y, q in QS], 'vix': [qv(vix, y, q) for y, q in QS]}

    # z統計はtrain期間(<2000)のみから計算(OOSの正直さ)
    def zmap(xs):
        v = [x for x, (y, _) in zip(xs, QS) if x is not None and y < 2000]
        m, s = statistics.mean(v), statistics.pstdev(v)
        return [None if x is None else (x - m) / s for x in xs]
    Z = {k: zmap(v) for k, v in raw.items()}
    gsi = {}
    for i, (y, q) in enumerate(QS):
        c = [Z['dx'][i], Z['ff'][i], (None if Z['oil'][i] is None else -Z['oil'][i]), Z['vix'][i]]
        c = [x for x in c if x is not None]
        if len(c) >= 3:
            gsi[(y, q)] = statistics.mean(c)
    return gsi


def main():
    gsi = build_gsi()
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

    def prev_q_gsi(i):
        y = i // 12; m = i % 12 + 1
        q = (m - 1) // 3 + 1
        py, pq = (y, q - 1) if q > 1 else (y - 1, 4)
        return gsi.get((py, pq))

    H = 6
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
            gv = prev_q_gsi(i)
            if gv is None:
                continue
            lab = 1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
            rows.append((c, i, g, tf, gv, lab))
    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]

    def build(feats):
        ecs = [make_ecdf([r[f] for r in train]) for f in feats]
        pos = [r for r in train if r[5] == 1]
        neg = [r for r in train if r[5] == 0]
        rng = random.Random(61)
        sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
        X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub]
        w, b = fit_logit(X, [r[5] for r in sub])
        return (lambda r: b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))), w

    y_te = [r[5] for r in test]
    s2, _ = build([2, 3])
    s3, w3 = build([2, 3, 4])
    a2 = auc([s2(r) for r in test], y_te)
    a3 = auc([s3(r) for r in test], y_te)
    byc = defaultdict(list)
    for r in test:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(62); ds = []
    for b in range(300):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        yv = [r[5] for r in s]
        v1 = auc([s2(r) for r in s], yv); v2 = auc([s3(r) for r in s], yv)
        if v1 is not None and v2 is not None:
            ds.append(v2 - v1)
    ds.sort(); n = len(ds)
    L = ['', f'MONTHLY-GSI-ADDON 2026-07-20 (副次2/2: +GSI(直前完結四半期, z=train統計)。h={H}, n={len(rows)})',
         f'GG+TF_m={a2:.4f} vs +GSI={a3:.4f} delta={a3-a2:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] 係数={["%.2f" % x for x in w3]}',
         f'-> {"PASS" if ds[int(.025*n)] > 0 and a3 - a2 >= 0.03 else "FAIL"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
