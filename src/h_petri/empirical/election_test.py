# -*- coding: utf-8 -*-
# ELECTION-TEST (事前固定): 選挙サイクルは崩壊警報に追加予測力を持つか
# 仮説(Stein-Streb系): 政権は選挙前に通貨を防衛し選挙後に切下げを解放する
#   → 行政選挙年 t の翌1-2年に onset が偏るはず。選挙日程は事前既知=正当な予測子
# (i) 記述: P(onset t+1..t+2 | exelec_t=1) vs P(|=0) + 国ブロックbootstrap CI
# (ii) 主検定: GG+TF+ELEC vs GG+TF。合格 = delta>=+0.03 かつ CI 0除外(従来基準)
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
    name2iso = {v['name'].strip().lower(): k for k, v in meta.items()}
    alias = {'turkiye': 'TUR', 'turkey': 'TUR', 'russia': 'RUS', 'egypt': 'EGY', 'iran': 'IRN',
             'venezuela': 'VEN', 'syria': 'SYR', 'yemen': 'YEM', 'vietnam': 'VNM',
             'south korea': 'KOR', 'korea, south': 'KOR', 'rok': 'KOR', 'prc': 'CHN',
             'ivory coast': 'CIV', "cote d'ivoire": 'CIV', 'cape verde': 'CPV',
             'congo (drc)': 'COD', 'dem. rep. congo': 'COD', 'congo, dem. rep.': 'COD',
             'congo': 'COG', 'congo, rep.': 'COG', 'roc': None, 'taiwan': None,
             'laos': 'LAO', 'kyrgyzstan': 'KGZ', 'slovakia': 'SVK', 'macedonia': 'MKD',
             'czech rep.': 'CZE', 'czech republic': 'CZE', 'gambia': 'GMB', 'bahamas': 'BHS',
             'myanmar': 'MMR', 'burma': 'MMR', 'brunei': 'BRN', 'uae': 'ARE',
             'st. lucia': 'LCA', 'st. kitts and nevis': 'KNA', 'st.vincent and grenadines': 'VCT',
             'trinidad-tobago': 'TTO', 'dominican rep.': 'DOM', 'eq. guinea': 'GNQ',
             'gdr': None, 'frg': 'DEU', 'yugoslavia': None, 'czechoslovakia': None,
             'soviet union': None, 'ussr': None, 'serbia and montenegro': None}
    elec = {}
    with open(ROOT / 'data_raw/dpi2023.csv', encoding='utf-8-sig', errors='replace') as f:
        r = csv.reader(f)
        hdr = next(r)
        idx = {h: i for i, h in enumerate(hdr)}
        unmatched = set()
        for row in r:
            try:
                y = int(row[idx['year']][:4])
                ex = row[idx['exelec']].strip()
                lg = row[idx['legelec']].strip()
            except (ValueError, IndexError):
                continue
            ifs = row[idx['ifs']].strip().upper()
            nm = row[idx['countryname']].strip().lower()
            iso = ifs if ifs in real else name2iso.get(nm) or alias.get(nm)
            if iso is None:
                unmatched.add(row[idx['countryname']])
                continue
            e = 1 if ex in ('1', '1.0') else 0
            l = 1 if lg in ('1', '1.0') else 0
            elec[(iso, y)] = (e, l)
    print(f'DPIマップ: {len({c for c, y in elec})}カ国, 未対応例 {sorted(unmatched)[:8]}')

    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    fx = fp.load_series('fx_lcu_per_usd', real)
    D_, A_ = fp.CRASH_RULES[fp.PRIMARY_RULE]
    crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D_, A_)
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
        el = elec.get((c, t))
        if el is None or not math.isfinite(tf):
            continue
        rows.append((c, t, g, tf, el[0], lab(c, t)))

    # (i) 記述: 選挙年の翌1-2年 onset率
    e1 = [r for r in rows if r[4] == 1]
    e0 = [r for r in rows if r[4] == 0]
    p1 = sum(r[5] for r in e1) / max(1, len(e1))
    p0 = sum(r[5] for r in e0) / max(1, len(e0))
    byc = defaultdict(list)
    for r in rows:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(31); ds = []
    for b in range(1000):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        a1 = [x for x in s if x[4] == 1]; a0 = [x for x in s if x[4] == 0]
        if not a1 or not a0:
            continue
        ds.append(sum(x[5] for x in a1) / len(a1) - sum(x[5] for x in a0) / len(a0))
    ds.sort(); n = len(ds)
    L = ['', 'ELECTION-TEST 2026-07-20 (選挙サイクル: DPI2023 exelec。事前固定=Stein-Streb仮説の警報文脈での検定)',
         f'サンプル n={len(rows)} (選挙年{len(e1)}/非選挙年{len(e0)})',
         f'(i) 選挙年の翌1-2年onset率 {p1:.3f} vs 非選挙年 {p0:.3f} 差{p1-p0:+.3f} CI[{ds[int(.025*n)]:+.3f},{ds[int(.975*n)]:+.3f}]']
    # (ii) 主検定
    train = [x for x in rows if x[1] < 2000]; test = [x for x in rows if x[1] >= 2000]
    y_te = [x[5] for x in test]

    def fitN(feats):
        ecs = [make_ecdf([r[f] for r in train]) for f in feats]

        def pad(r):
            vals = [r[0], r[1]] + [r[f] for f in feats]
            while len(vals) < 5:
                vals.append(0)
            return tuple(vals + [r[5]])
        sc, wg = fit_logistic([pad(r) for r in train], list(range(2, 2 + len(feats))), ecs)
        return (lambda r: sc(pad(r))), wg
    sc2, _ = fitN([2, 3])
    sc3, wg3 = fitN([2, 3, 4])
    a2 = auc([sc2(x) for x in test], y_te)
    a3 = auc([sc3(x) for x in test], y_te)
    byc2 = defaultdict(list)
    for x in test:
        byc2[x[0]].append(x)
    cl2 = sorted(byc2); rng2 = random.Random(32); ds2 = []
    for b in range(500):
        s = []
        for _ in range(len(cl2)):
            s.extend(byc2[rng2.choice(cl2)])
        yv = [x[5] for x in s]
        v1 = auc([sc2(x) for x in s], yv); v2 = auc([sc3(x) for x in s], yv)
        if v1 is not None and v2 is not None:
            ds2.append(v2 - v1)
    ds2.sort(); m = len(ds2)
    L.append(f'(ii) GG+TF={a2:.4f} vs GG+TF+選挙={a3:.4f} delta={a3-a2:+.4f} CI[{ds2[int(.025*m)]:+.4f},{ds2[int(.975*m)]:+.4f}] 係数={["%.3f" % w for w in wg3]}')
    L.append(f'-> {"PASS" if ds2[int(.025*m)] > 0 and a3 - a2 >= 0.03 else "FAIL"}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
