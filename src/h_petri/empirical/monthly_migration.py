# -*- coding: utf-8 -*-
# 大工事: 警報の月次全面移行 (設計 notes/40・実行前固定)
import csv, math, random, statistics, sys
from collections import defaultdict
from bisect import bisect_right
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months


def make_ecdf(v):
    s = sorted(v); n = len(s)
    return lambda x: bisect_right(s, x) / n


def fit_logit(X, Y, iters=2000, lr=0.5, lam=1e-4):
    k = len(X[0])
    w = [0.0] * k; b = 0.0
    n = len(X)
    for _ in range(iters):
        gw = [0.0] * k; gb = 0.0
        for xi, yi in zip(X, Y):
            z = b + sum(a * c for a, c in zip(w, xi))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            e = p - yi
            gb += e
            for j in range(k):
                gw[j] += e * xi[j]
        b -= lr * gb / n
        for j in range(k):
            w[j] -= lr * (gw[j] / n + lam * w[j])
    return w, b


def auc(sc, lb):
    pos = sum(lb); neg = len(lb) - pos
    if pos == 0 or neg == 0:
        return None
    order = sorted(range(len(sc)), key=lambda i: sc[i])
    ranks = [0.0] * len(sc)
    i = 0
    while i < len(order):
        j = i
        while j < len(order) and sc[order[j]] == sc[order[i]]:
            j += 1
        for m in range(i, j):
            ranks[order[m]] = (i + j - 1) / 2.0 + 1.0
        i = j
    sp = sum(ranks[x] for x in range(len(sc)) if lb[x] == 1)
    return (sp - pos * (pos + 1) / 2.0) / (pos * neg)


def main():
    fxm = load_fxm()
    crash_m = {iso: fx_crash_months(fxm[iso]) for iso in fxm}
    onset_idx = defaultdict(set)
    for iso, cr in crash_m.items():
        idxs = {y * 12 + m - 1 for (y, m) in cr}
        for (y, m) in sorted(cr):
            i = y * 12 + m - 1
            if not any((i - k) in idxs for k in range(1, 13)):
                onset_idx[iso].add(i)
    crash_idx = {iso: {y * 12 + m - 1 for (y, m) in cr} for iso, cr in crash_m.items()}

    meta = fp.load_real_countries(); real = set(meta)
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    res = defaultdict(dict)
    with open(ROOT / 'data_raw/il_reserves_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                res[row['iso3']][int(y) * 12 + int(m) - 1] = float(row['reserves_usd'])
            except (ValueError, KeyError):
                continue
    imports = defaultdict(lambda: defaultdict(float))
    trade = defaultdict(lambda: defaultdict(dict))
    with open(ROOT / 'data_raw/imts_trade_xm.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, xv, mv in r:
            try:
                y = int(yr); x = float(xv); mm = float(mv)
            except ValueError:
                continue
            imports[rep][y] += mm
            v = x + mm
            if v > 0:
                trade[rep][y][cp] = v

    # 前年重みの正規化(年ごと)
    wcache = {}

    def weights(c, y):
        key = (c, y)
        if key in wcache:
            return wcache[key]
        w = trade.get(c, {}).get(y - 1, {})
        if len(w) < 3:
            wcache[key] = None
        else:
            tot = sum(w.values())
            wcache[key] = {j: v / tot for j, v in w.items()} if tot > 0 else None
        return wcache[key]

    H = int(sys.argv[1]) if len(sys.argv) > 1 else 6  # 主予測地平(月)
    rows = []
    for c in sorted({c for (c, _) in gg}):
        fxd = fxm.get(c)
        if not fxd:
            continue
        for i in range(1978 * 12, 2025 * 12 + 6):
            y = i // 12; m = i % 12 + 1
            if i in crash_idx.get(c, set()):
                continue
            if (y, m) not in fxd:
                continue
            g = gg.get((c, y - 1))
            if g is None or not math.isfinite(g):
                continue
            W = weights(c, y)
            if W is None:
                continue
            tf_m = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
            # 鮮度停止版: 直前12月末(前年末)の火事状態
            dec = (y - 1) * 12 + 11
            tf_stale = sum(v for j, v in W.items() if dec in crash_idx.get(j, set()))
            r1 = res.get(c, {}).get(i)
            imp = imports.get(c, {}).get(y - 1)
            rm = (r1 / (imp / 12.0)) if (r1 and imp and imp > 0) else None
            if rm is not None and (not math.isfinite(rm) or rm > 120):
                rm = None
            lab = 1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
            rows.append((c, i, g, tf_m, tf_stale, rm, lab))
    print(f'panel: {len(rows)} country-months, positives={sum(r[6] for r in rows)}')

    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]

    def build(feats, data_tr):
        ecs = [make_ecdf([r[f] for r in data_tr]) for f in feats]
        pos = [r for r in data_tr if r[6] == 1]
        neg = [r for r in data_tr if r[6] == 0]
        rng = random.Random(41)
        sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
        X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub]
        Y = [r[6] for r in sub]
        w, b = fit_logit(X, Y)

        def score(r):
            return b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))
        return score, w

    y_te = [r[6] for r in test]
    sc_fresh, w1 = build([2, 3], train)
    sc_stale, w2 = build([2, 4], train)
    a_fresh = auc([sc_fresh(r) for r in test], y_te)
    a_stale = auc([sc_stale(r) for r in test], y_te)

    byc = defaultdict(list)
    for r in test:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(42); ds = []
    for b in range(300):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        yv = [r[6] for r in s]
        v1 = auc([sc_fresh(r) for r in s], yv)
        v2 = auc([sc_stale(r) for r in s], yv)
        if v1 is not None and v2 is not None:
            ds.append(v1 - v2)
    ds.sort(); n = len(ds)
    L = ['', f'MONTHLY-MIGRATION 2026-07-20 (大工事: 月次警報。h={H}ヶ月, panel={len(rows)}国月, 設計notes/40)',
         f'主検定: 月次鮮度(GG+TF_m)={a_fresh:.4f} vs 鮮度停止(GG+TF_前年末凍結)={a_stale:.4f}',
         f'  ΔAUC={a_fresh-a_stale:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] -> {"PASS: 月次の鮮度は買う価値がある" if ds[int(.025*n)] > 0 else "FAIL: 年次で飽和"}']

    # 副次: +RM(月次), +両方
    sub_rm = [r for r in rows if r[5] is not None]
    tr_rm = [r for r in sub_rm if r[1] < 2000 * 12]
    te_rm = [r for r in sub_rm if r[1] >= 2000 * 12]
    y_rm = [r[6] for r in te_rm]
    rows_rm = [(r[0], r[1], r[2], r[3], -r[5], 0, r[6]) for r in sub_rm]
    trr = [r for r in rows_rm if r[1] < 2000 * 12]
    ter = [r for r in rows_rm if r[1] >= 2000 * 12]
    s2, _ = build([2, 3], trr)
    s3, _ = build([2, 3, 4], trr)
    a2 = auc([s2(r) for r in ter], [r[6] for r in ter])
    a3 = auc([s3(r) for r in ter], [r[6] for r in ter])
    L.append(f'副次(+月次RM, 同一サンプルn={len(sub_rm)}): GG+TF_m={a2:.4f} -> +RM={a3:.4f} (Δ{a3-a2:+.4f})')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
