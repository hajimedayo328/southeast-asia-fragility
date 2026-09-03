# -*- coding: utf-8 -*-
# notes/53 v2: PROFIT-LAG — 営業余剰スプライス(1947-2024)で投資ブーム後の利益の谷 k* vs TTB
import json, math, random, statistics, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# French名 -> (TTB, 3.7ESI投資kw, SIC期PTIkwリスト, NAICS産業コード)
MAP = {
    'Food': (24, 'Food and beverage and tobacco', ['Food and kindred'], '311FT'),
    'Oil': (23, 'Petroleum and coal', ['Petroleum and coal'], '324'),
    'Chems': (23, 'Chemical products', ['Chemicals and allied'], '325'),
    'FabPr': (14, 'Fabricated metal', ['Fabricated metal'], '332'),
    'Mach': (18, 'Machinery', ['Industrial machinery', 'Machinery, except'], '333'),
    'ElcEq': (24, 'Electrical equipment', ['Electronic and other electric', 'Electric and electronic'], '335'),
    'Autos': (28, 'Motor vehicles', ['Motor vehicles'], '3361MV'),
    'Util': (86, 'Utilities', ['Electric, gas, and sanitary'], '22'),
    'Whlsl': (37, 'Wholesale trade', ['Wholesale trade'], '42'),
    'Trans': (23, 'Truck transportation', ['Trucking and warehousing'], '484'),
    'Txtls': (24, 'Textile', ['Textile mill'], '313TT'),
    'Paper': (23, 'Paper products', ['Paper and allied'], '322'),
    'Steel': (37, 'Primary metals', ['Primary metal'], '331'),
    'Telcm': (24, 'Broadcasting and telecom', ['Telephone and telegraph', 'Communications'], '513'),
}


def load_sic(sheet):
    import pandas as pd
    df = pd.read_excel(ROOT / 'data_raw/GDPbyInd_VA_SIC.xls', sheet_name=sheet, header=None)
    years = [int(x) for x in df.iloc[0, 2:] if str(x).strip().isdigit()]
    out = defaultdict(dict)
    for _, row in df.iterrows():
        if str(row[0]).strip() != 'GOS':
            continue
        nm = str(row[1]).strip()
        for j, y in enumerate(years):
            try:
                out[nm][y] = float(row[j + 2])
            except (ValueError, TypeError):
                continue
    return out


def growth(series):
    return {y: series[y] / abs(series[y - 1]) - 1 for y in series
            if y - 1 in series and series[y - 1] != 0}


def main():
    import pandas as pd  # noqa
    sic72 = load_sic('72SIC_Components of VA')
    sic87 = load_sic('87SIC_Components of VA')
    naics_rows = json.load(open(ROOT / 'data_raw/bea_vacomp.json', encoding='utf-8'))
    gos = defaultdict(dict)
    for x in naics_rows:
        if 'operating surplus' in x['IndustrYDescription'].lower():
            try:
                gos[x['Industry']][int(x['Year'])] = float(str(x['DataValue']).replace(',', ''))
            except ValueError:
                continue
    inv_raw = json.load(open(ROOT / 'data_raw/bea_FAAt307ESI.json', encoding='utf-8'))
    inv = defaultdict(dict)
    for x in inv_raw:
        try:
            inv[x['LineDescription']][int(x['TimePeriod'])] = float(x['DataValue'].replace(',', ''))
        except ValueError:
            continue

    def find(dic, kws):
        for kw in kws:
            c = [l for l in dic if kw.lower() in l.lower()]
            if c:
                return min(c, key=len)
        return None

    results = []
    for fnm, (ttb, ikw, skws, ncode) in MAP.items():
        il = find(inv, [ikw])
        s72 = find(sic72, skws); s87 = find(sic87, skws)
        gn = gos.get(ncode, {})
        if not il or not s72 or not s87 or not gn:
            print(f'{fnm}: match fail inv={bool(il)} 72={s72} 87={s87} naics={len(gn)}')
            continue
        print(f'{fnm}: 72SIC[{s72[:28]}] 87SIC[{s87[:28]}] NAICS[{ncode}:{len(gn)}yr] TTB={ttb}m')
        g72 = growth(sic72[s72]); g87 = growth(sic87[s87]); gN = growth(gn)
        pg = {}
        pg.update({y: v for y, v in g72.items() if y <= 1987})
        pg.update({y: v for y, v in g87.items() if 1988 <= y <= 1997})
        pg.update({y: v for y, v in gN.items() if y >= 1998})
        gi = growth(inv[il])
        ys = sorted(gi)
        booms = []
        for j, y in enumerate(ys):
            hist = [gi[x] for x in ys[:j + 1]]
            if len(hist) < 20 or not (1968 <= y <= 2019):
                continue
            if gi[y] >= sorted(hist)[int(0.75 * len(hist))]:
                booms.append(y)
        path = {}
        for k in range(1, 6):
            vals = [pg[b + k] for b in booms if b + k in pg]
            if len(vals) >= 8:
                path[k] = statistics.mean(vals)
        if len(path) == 5:
            kstar = min(path, key=path.get)
            results.append((fnm, ttb, kstar, len(booms)))
        else:
            print(f'  {fnm}: path不足 {sorted(path)}')

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
    ttbs = [r[1] for r in results]; ks = [r[2] for r in results]
    rho = spearman(ttbs, ks)
    rng = random.Random(231); cnt = 0
    for _ in range(5000):
        sh = ttbs[:]; rng.shuffle(sh)
        if spearman(sh, ks) >= rho:
            cnt += 1
    p = cnt / 5000
    L = ['', f'PROFIT-LAG-v2 2026-09-04 (notes/53 v2。営業余剰スプライス1947-2024。n={len(results)}業種)',
         '  ' + ' / '.join(f'{r[0]}(TTB{r[1]}m,k*={r[2]},booms{r[3]})' for r in results),
         f'  主検定: Spearman rho(TTB, k*_profit)={rho:+.3f} 並べ替えp={p:.3f}',
         f'  -> {"PASS: 実物(利益)はラグ法則に従う — 株価だけが先回りする鎖が完成" if rho > 0 and p < 0.05 else "FAIL: 集計業種レベルでは利益でもラグ不可読"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
