# -*- coding: utf-8 -*-
# REFINE-BATCH (事前固定・全結果報告):
# (a) TF_sev = 相手の減価率で重み付けた火事(0/1でなく強度)。GG+TF_sev vs GG+TF の
#     対決(同一サンプル・OOS)。合格 = 差のCIが0を除外
# (b) 崩壊車線に準備月数RMを追加: GG+TF+RM vs GG+TF。合格 = delta>=+0.03 かつ CI 0除外
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from phase2_exp1_bis import auc, make_ecdf, fit_logistic


def main():
    meta = fp.load_real_countries(); real = set(meta)
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    rm_ann = fp.load_series('reserves_months_imports', real)
    fx = fp.load_series('fx_lcu_per_usd', real)
    D_, A_ = fp.CRASH_RULES[fp.PRIMARY_RULE]
    d1 = fp.changes(fx, real, 1)
    crash = fp.crash_years(d1, fp.changes(fx, real, 2), D_, A_)
    onset = fp.onsets(crash); k = fp.PRIMARY_K

    def elig(c, t):
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            return False
        return (c, t) not in crash

    def lab(c, t):
        return 1 if any((c, t + j) in onset for j in range(1, k + 1)) else 0

    trade = defaultdict(lambda: defaultdict(dict))
    with open(ROOT / 'data_raw/imts_trade.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, v in r:
            try:
                trade[rep][int(yr)][cp] = float(v)
            except ValueError:
                continue

    def sev(j, t):
        # 相手の当年減価率(危機状態の相手のみ・0.3-3.0にクリップ=データ掃除)
        if (j, t) not in crash:
            return 0.0
        d = d1.get((j, t))
        if d is None or not math.isfinite(d):
            return 0.30
        return max(0.30, min(3.0, d))

    rows = []
    for (c, t) in gg:
        if not elig(c, t):
            continue
        g = gg[(c, t)]
        if not math.isfinite(g):
            continue
        w = trade.get(c, {}).get(t - 1, {})
        if len(w) < 3:
            continue
        tot = sum(w.values())
        if tot <= 0:
            continue
        tf = sum(v for j, v in w.items() if (j, t) in crash) / tot
        tfs = sum(v * sev(j, t) for j, v in w.items()) / tot
        rm = rm_ann.get((c, t))
        if not all(map(math.isfinite, (tf, tfs))):
            continue
        rows.append((c, t, g, tf, tfs, rm, lab(c, t)))

    train = [x for x in rows if x[1] < 2000]
    test = [x for x in rows if x[1] >= 2000]
    y_te = [x[6] for x in test]

    def fitN(feats, data_tr):
        ecs = [make_ecdf([r[f] for r in data_tr]) for f in feats]

        def pad(r):
            vals = [r[0], r[1]] + [r[f] for f in feats]
            return tuple(vals + [0] * (5 - len(vals) + 1) + [r[6]]) if len(vals) < 6 else tuple(vals[:5] + [r[6]])
        # 汎用pad: (c,t,f1..fn,0埋め,label) 長さ6
        def pad2(r):
            vals = [r[0], r[1]] + [r[f] for f in feats]
            while len(vals) < 5:
                vals.append(0)
            return tuple(vals + [r[6]])
        data = [pad2(r) for r in data_tr]
        sc, wg = fit_logistic(data, list(range(2, 2 + len(feats))), ecs)

        def score(r):
            return sc(pad2(r))
        return score, wg

    L = ['', 'REFINE-BATCH 2026-07-18 (事前固定・全報告: (a)強度重み火事 (b)崩壊車線+RM)']
    # (a) TF vs TF_sev
    sc_tf, _ = fitN([2, 3], train)
    sc_sev, _ = fitN([2, 4], train)
    a_tf = auc([sc_tf(x) for x in test], y_te)
    a_sev = auc([sc_sev(x) for x in test], y_te)
    byc = defaultdict(list)
    for x in test:
        byc[x[0]].append(x)
    cl = sorted(byc); rng = random.Random(21); ds = []
    for b in range(500):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        yv = [x[6] for x in s]
        v1 = auc([sc_tf(x) for x in s], yv); v2 = auc([sc_sev(x) for x in s], yv)
        if v1 is not None and v2 is not None:
            ds.append(v2 - v1)
    ds.sort(); n = len(ds)
    L.append(f'(a) GG+TF={a_tf:.4f} vs GG+TF_sev(強度重み)={a_sev:.4f} 差={a_sev-a_tf:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] -> {"PASS" if ds[int(.025*n)] > 0 else "FAIL/同等"}')
    # (b) GG+TF+RM (RMのある行のみ・同一サンプル比較)
    rows_rm = [r for r in rows if r[5] is not None and math.isfinite(r[5])]
    tr2 = [x for x in rows_rm if x[1] < 2000]; te2 = [x for x in rows_rm if x[1] >= 2000]
    y2 = [x[6] for x in te2]
    # RMは少=危険なので符号反転した列を作る
    rows_rm2 = [(r[0], r[1], r[2], r[3], -r[5], 0, r[6]) for r in rows_rm]
    tr3 = [x for x in rows_rm2 if x[1] < 2000]; te3 = [x for x in rows_rm2 if x[1] >= 2000]
    sc2, _ = fitN([2, 3], tr3)
    sc3, wg3 = fitN([2, 3, 4], tr3)
    a2 = auc([sc2(x) for x in te3], [x[6] for x in te3])
    a3 = auc([sc3(x) for x in te3], [x[6] for x in te3])
    byc2 = defaultdict(list)
    for x in te3:
        byc2[x[0]].append(x)
    cl2 = sorted(byc2); rng2 = random.Random(22); ds2 = []
    for b in range(500):
        s = []
        for _ in range(len(cl2)):
            s.extend(byc2[rng2.choice(cl2)])
        yv = [x[6] for x in s]
        v1 = auc([sc2(x) for x in s], yv); v2 = auc([sc3(x) for x in s], yv)
        if v1 is not None and v2 is not None:
            ds2.append(v2 - v1)
    ds2.sort(); m = len(ds2)
    L.append(f'(b) 同一サンプル(n={len(rows_rm)}): GG+TF={a2:.4f} vs GG+TF+RM={a3:.4f} delta={a3-a2:+.4f} CI[{ds2[int(.025*m)]:+.4f},{ds2[int(.975*m)]:+.4f}] 係数={["%.3f" % w for w in wg3]} -> {"PASS" if ds2[int(.025*m)] > 0 and a3 - a2 >= 0.03 else "FAIL"}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
