# -*- coding: utf-8 -*-
# notes/53 PROFIT-LAG: 投資ブーム後の利益の谷 k* は TTB に比例するか (結果変数=業種利益成長)
import json, math, random, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# French名 -> (TTB, BEA投資キーワード, 利益6.16Dキーワード)。事前固定
MAP = {
    'Food': (24, 'Food and beverage and tobacco', 'Food and beverage and tobacco'),
    'Oil': (23, 'Petroleum and coal', 'Petroleum and coal'),
    'Chems': (23, 'Chemical products', 'Chemical products'),
    'FabPr': (14, 'Fabricated metal', 'Fabricated metal'),
    'Mach': (18, 'Machinery', 'Machinery'),
    'ElcEq': (24, 'Electrical equipment', 'Electrical equipment'),
    'Autos': (28, 'Motor vehicles', 'Motor vehicles'),
    'Util': (86, 'Utilities', 'Utilities'),
    'Whlsl': (37, 'Wholesale trade', 'Wholesale trade'),
    'Trans': (23, 'Truck transportation', 'Transportation and warehousing'),
}
MIN_BOOMS = 4


def load(fn):
    d = json.load(open(ROOT / fn, encoding='utf-8'))
    out = defaultdict(dict)
    for x in d:
        try:
            out[x['LineDescription']][int(x['TimePeriod'])] = float(x['DataValue'].replace(',', ''))
        except ValueError:
            continue
    return out


def main():
    inv = load('data_raw/bea_FAAt307ESI.json')
    prof = load('data_raw/bea_profits_616.json')

    def find(dic, kw):
        c = [l for l in dic if kw.lower() in l.lower()]
        return min(c, key=len) if c else None

    results = []
    for fnm, (ttb, ikw, pkw) in MAP.items():
        il = find(inv, ikw); pl = find(prof, pkw)
        if not il or not pl:
            print(f'{fnm}: match fail inv={il} prof={pl}')
            continue
        g = {y: inv[il][y] / inv[il][y - 1] - 1 for y in inv[il] if y - 1 in inv[il] and inv[il][y - 1] > 0}
        ys = sorted(g)
        booms = []
        for j, y in enumerate(ys):
            hist = [g[x] for x in ys[:j + 1]]
            if len(hist) < 20 or y < 1998 or y > 2020:
                continue
            if g[y] >= sorted(hist)[int(0.75 * len(hist))]:
                booms.append(y)
        pg = {y: prof[pl][y] / abs(prof[pl][y - 1]) - 1 for y in prof[pl]
              if y - 1 in prof[pl] and prof[pl][y - 1] != 0}
        path = {}
        for k in range(1, 6):
            vals = [pg[b + k] for b in booms if b + k in pg]
            if len(vals) >= MIN_BOOMS:
                path[k] = statistics.mean(vals)
        if len(path) == 5:
            kstar = min(path, key=path.get)
            results.append((fnm, ttb, kstar, len(booms)))
    ttbs = [r[1] for r in results]; ks = [r[2] for r in results]

    def spearman(a, b):
        def rk(v):
            s = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v)
            for j, i in enumerate(s):
                r[i] = j
            return r
        ra, rb = rk(a), rk(b)
        ma, mb = statistics.mean(ra), statistics.mean(rb)
        n_ = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        da = math.sqrt(sum((x - ma) ** 2 for x in ra)); db = math.sqrt(sum((y - mb) ** 2 for y in rb))
        return n_ / (da * db) if da * db > 0 else 0.0
    rho = spearman(ttbs, ks)
    rng = random.Random(221); cnt = 0
    for _ in range(5000):
        sh = ttbs[:]; rng.shuffle(sh)
        if spearman(sh, ks) >= rho:
            cnt += 1
    p = cnt / 5000
    L = ['', f'PROFIT-LAG 2026-07-22 (notes/53。利益6.16D(1998-2025)×ブーム3.7ESI×Koeva。n={len(results)}業種・短サンプル注意)',
         '  ' + ' / '.join(f'{r[0]}(TTB{r[1]}m,k*={r[2]},booms{r[3]})' for r in results),
         f'  主検定: Spearman rho(TTB, k*_profit)={rho:+.3f} 並べ替えp={p:.3f}',
         f'  -> {"PASS: 実物(利益)はラグ法則に従う=株価だけが先回りの完全な鎖" if rho > 0 and p < 0.05 else "FAIL: 集計業種レベルでは利益でもラグは観測不能"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
