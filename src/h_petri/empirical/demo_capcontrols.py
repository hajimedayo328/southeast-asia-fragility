# -*- coding: utf-8 -*-
# notes/55: EXP-A 人口動態 / EXP-B 資本規制(KAOPEN) — 年次パネル・従来バー
import csv, json, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from phase2_exp1_bis import auc, make_ecdf, fit_logistic
from attack_anatomy import load_fxm, build_emp_attacks


def wb_json(path):
    d = json.load(open(ROOT / path, encoding='utf-8'))
    out = {}
    for r in d[1]:
        iso = r.get('countryiso3code')
        if iso and r.get('value') is not None:
            out[(iso, int(r['date']))] = float(r['value'])
    return out


def main():
    meta = fp.load_real_countries(); real = set(meta)
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    fx = fp.load_series('fx_lcu_per_usd', real)
    D_, A_ = fp.CRASH_RULES[fp.PRIMARY_RULE]
    crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D_, A_)
    onset = fp.onsets(crash); k = fp.PRIMARY_K
    pop = wb_json('docs/data/panel_raw/pop_growth.json')
    fert = wb_json('docs/data/panel_raw/fertility.json')
    kao = {}
    with open(ROOT / 'data_raw/kaopen.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                kao[(row['ccode'], int(float(row['year'])))] = float(row['kaopen'])
            except ValueError:
                continue
    trade = defaultdict(lambda: defaultdict(dict))
    with open(ROOT / 'data_raw/imts_trade.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, v in r:
            try:
                trade[rep][int(yr)][cp] = float(v)
            except ValueError:
                continue

    def elig(c, t):
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            return False
        return (c, t) not in crash

    def lab(c, t):
        return 1 if any((c, t + j) in onset for j in range(1, k + 1)) else 0

    rows = []
    for (c, t) in gg:
        if not elig(c, t):
            continue
        g = gg[(c, t)]
        if not math.isfinite(g):
            continue
        w = trade.get(c, {}).get(t - 1, {})
        tot = sum(w.values())
        if len(w) < 3 or tot <= 0:
            continue
        tf = sum(v for j, v in w.items() if (j, t) in crash) / tot
        rows.append((c, t, g, tf, pop.get((c, t - 1)), fert.get((c, t - 1)), kao.get((c, t - 1)), lab(c, t)))

    L = ['', 'DEMO+CAPCONTROLS 2026-09-04 (notes/55。年次パネル・従来バー)']

    def run_add(feat_ix, name, seed):
        sub = [r for r in rows if r[feat_ix] is not None and math.isfinite(r[feat_ix])]
        train = [x for x in sub if x[1] < 2000]; test = [x for x in sub if x[1] >= 2000]
        y_te = [x[7] for x in test]

        def fitN(feats):
            ecs = [make_ecdf([r[f] for r in train]) for f in feats]

            def pad(r):
                vals = [r[0], r[1]] + [r[f] for f in feats]
                while len(vals) < 5:
                    vals.append(0)
                return tuple(vals + [r[7]])
            sc, wg = fit_logistic([pad(r) for r in train], list(range(2, 2 + len(feats))), ecs)
            return (lambda r: sc(pad(r))), wg
        s1, _ = fitN([2, 3])
        s2, wg = fitN([2, 3, feat_ix])
        a1 = auc([s1(x) for x in test], y_te)
        a2 = auc([s2(x) for x in test], y_te)
        byc = defaultdict(list)
        for x in test:
            byc[x[0]].append(x)
        cl = sorted(byc); rng = random.Random(seed); ds = []
        for b in range(500):
            s = []
            for _ in range(len(cl)):
                s.extend(byc[rng.choice(cl)])
            yv = [x[7] for x in s]
            v1 = auc([s1(x) for x in s], yv); v2 = auc([s2(x) for x in s], yv)
            if v1 is not None and v2 is not None:
                ds.append(v2 - v1)
        ds.sort(); n = len(ds)
        d = a2 - a1
        ok = ds[int(.025 * n)] > 0 and d >= 0.03
        L.append(f'  {name}: n={len(sub)} GG+TF={a1:.4f} +X={a2:.4f} delta={d:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] 係数={["%.2f" % x for x in wg]} -> {"PASS" if ok else "FAIL"}')

    run_add(4, 'EXP-A 人口成長', 241)
    run_add(5, 'EXP-A 出生率', 243)
    run_add(6, 'EXP-B KAOPEN', 245)

    # EXP-B(ii) 記述: 攻撃率を年内KAOPEN三分位別に
    fxm = load_fxm()
    attacks = build_emp_attacks(fxm)
    atk_years = defaultdict(set)
    for iso, y, m in attacks:
        atk_years[iso].add(y)
    byy = defaultdict(list)
    for (c, t) in {(r[0], r[1]) for r in rows}:
        v = kao.get((c, t - 1))
        if v is not None:
            byy[t].append((v, c))
    terc = defaultdict(lambda: [0, 0])
    for t, lst in byy.items():
        if len(lst) < 12:
            continue
        lst.sort()
        n3 = len(lst) // 3
        for i, (v, c) in enumerate(lst):
            g = 0 if i < n3 else (1 if i < 2 * n3 else 2)
            terc[g][0] += 1
            if t in atk_years.get(c, set()):
                terc[g][1] += 1
    lbl = ['閉鎖(規制強)', '中間', '開放']
    L.append('  EXP-B(ii) EMP攻撃率(年内KAOPEN三分位・前年値): ' + ' / '.join(
        f'{lbl[g]}={terc[g][1]}/{terc[g][0]}={terc[g][1]/max(1,terc[g][0]):.1%}' for g in (0, 1, 2)))
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
