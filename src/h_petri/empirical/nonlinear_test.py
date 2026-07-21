# -*- coding: utf-8 -*-
# notes/48: 関数形の検定 — GBM/RF/2Dビン表/交互作用ロジット vs ECDFロジット
# 情報集合は同一(GG-ECDF, TF-ECDF)。ハイパラは事前固定・チューニング禁止
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, auc

H = 6


def main():
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
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
            rows.append((c, i, g, tf, lab))
    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]
    e_g = make_ecdf([r[2] for r in train])
    e_t = make_ecdf([r[3] for r in train])
    Xtr = [[e_g(r[2]), e_t(r[3])] for r in train]
    Ytr = [r[4] for r in train]
    Xte = [[e_g(r[2]), e_t(r[3])] for r in test]
    Yte = [r[4] for r in test]

    models = {}
    lg = LogisticRegression(max_iter=1000).fit(Xtr, Ytr)
    models['logit'] = lambda X: lg.predict_proba(X)[:, 1]
    gbm = GradientBoostingClassifier(n_estimators=200, max_depth=3, learning_rate=0.05,
                                     subsample=0.8, random_state=42).fit(Xtr, Ytr)
    models['gbm'] = lambda X: gbm.predict_proba(X)[:, 1]
    rf = RandomForestClassifier(n_estimators=500, max_depth=6, min_samples_leaf=50,
                                random_state=42, n_jobs=-1).fit(Xtr, Ytr)
    models['rf'] = lambda X: rf.predict_proba(X)[:, 1]
    lgx = LogisticRegression(max_iter=1000).fit(
        [[a, b, a * b] for a, b in Xtr], Ytr)
    models['logit_x'] = lambda X: lgx.predict_proba([[a, b, a * b] for a, b in X])[:, 1]

    # 2Dビン表(10x10, 経験ベイズ縮約: セル率を全体率へ n/(n+50) で縮める)
    NB = 10
    cnt = [[0] * NB for _ in range(NB)]
    hit = [[0] * NB for _ in range(NB)]
    for (a, b_), yv in zip(Xtr, Ytr):
        ia = min(NB - 1, int(a * NB)); ib = min(NB - 1, int(b_ * NB))
        cnt[ia][ib] += 1; hit[ia][ib] += yv
    p0 = sum(Ytr) / len(Ytr)

    def grid_pred(X):
        out = []
        for a, b_ in X:
            ia = min(NB - 1, int(a * NB)); ib = min(NB - 1, int(b_ * NB))
            n = cnt[ia][ib]; h = hit[ia][ib]
            out.append((h + 50 * p0) / (n + 50))
        return out
    models['grid'] = grid_pred

    scores = {k: list(f(Xte)) for k, f in models.items()}
    aucs = {k: auc(v, Yte) for k, v in scores.items()}
    # 国ブロックCI: GBM - logit
    idx_byc = defaultdict(list)
    for j, r in enumerate(test):
        idx_byc[r[0]].append(j)
    cl = sorted(idx_byc); rng = random.Random(141); ds = []
    for bb in range(300):
        js = []
        for _ in range(len(cl)):
            js.extend(idx_byc[rng.choice(cl)])
        yv = [Yte[j] for j in js]
        v1 = auc([scores['gbm'][j] for j in js], yv)
        v2 = auc([scores['logit'][j] for j in js], yv)
        if v1 is not None and v2 is not None:
            ds.append(v1 - v2)
    ds.sort(); n = len(ds)
    d = aucs['gbm'] - aucs['logit']
    L = ['', f'NONLINEAR-TEST 2026-07-20 (notes/48。同一情報集合(GG,TF)で関数形だけ変える。h={H}, train={len(train)}/test={len(test)})',
         f'  logit={aucs["logit"]:.4f} / GBM={aucs["gbm"]:.4f} / RF={aucs["rf"]:.4f} / 交互作用logit={aucs["logit_x"]:.4f} / 2Dビン表={aucs["grid"]:.4f}',
         f'  主検定 GBM-logit={d:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}]',
         f'  -> {"PASS: 天井はモデルの限界だった" if ds[int(.025*n)] > 0 and d >= 0.03 else "FAIL: 天井は情報の限界(線形ランクで使い切っている, Beutel et al.と整合)"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
