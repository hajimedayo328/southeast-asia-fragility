# -*- coding: utf-8 -*-
# notes/51 TTB-HORIZON主検定: 投資ブーム後の反転最深年k*はTTB(Koeva Table1)と単調に並ぶか
# マッピングは実行前固定(SIC対応が明確な業種のみ・曖昧は除外)
import csv, json, math, random, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# French49 -> (Koeva TTBヶ月, BEA検索キーワード)  ※事前固定・変更しない
MAP = {
    'Food': (24, 'Food and beverage and tobacco'), 'Beer': (24, 'Food and beverage and tobacco'), 'Soda': (24, 'Food and beverage and tobacco'),
    'Txtls': (24, 'Textile'), 'Paper': (23, 'Paper products'), 'Chems': (23, 'Chemical products'),
    'Oil': (23, 'Petroleum and coal'), 'Rubbr': (13, 'Plastics and rubber'),
    'Steel': (37, 'Primary metals'), 'FabPr': (14, 'Fabricated metal'),
    'Mach': (18, 'Machinery'), 'ElcEq': (24, 'Electrical equipment'),
    'Autos': (28, 'Motor vehicles'), 'Aero': (28, 'Other transportation equipment'),
    'LabEq': (25, 'Miscellaneous manufacturing'), 'Telcm': (24, 'Broadcasting and telecom'),
    'Util': (86, 'Utilities'), 'Whlsl': (37, 'Wholesale trade'),
    'Trans': (23, 'Truck transportation'), 'BldMt': (18, 'Nonmetallic mineral'),
}


def main():
    # French 49 月次 -> 年次リターン
    rows = open(ROOT / 'data_raw/ff49/49_Industry_Portfolios.csv', encoding='latin-1').read().splitlines()
    start = next(i for i, l in enumerate(rows) if 'Average Value Weighted Returns -- Monthly' in l)
    hdr = [h.strip() for h in rows[start + 1].split(',')][1:]
    monthly = defaultdict(dict)
    for l in rows[start + 2:]:
        p = l.split(',')
        if len(p) < 40 or not p[0].strip().isdigit() or len(p[0].strip()) != 6:
            break
        ym = p[0].strip(); y, m = int(ym[:4]), int(ym[4:])
        for nm, v in zip(hdr, p[1:]):
            try:
                v = float(v)
            except ValueError:
                continue
            if v > -99:
                monthly[nm][(y, m)] = v / 100
    annual = defaultdict(dict)
    for nm, d in monthly.items():
        for y in range(1927, 2026):
            ms = [d[(y, m)] for m in range(1, 13) if (y, m) in d]
            if len(ms) == 12:
                r = 1.0
                for x in ms:
                    r *= (1 + x)
                annual[nm][y] = r - 1

    # BEA投資 -> 業種年次系列
    bea = json.load(open(ROOT / 'data_raw/bea_FAAt307ESI.json', encoding='utf-8'))
    inv = defaultdict(dict)
    for x in bea:
        try:
            v = float(x['DataValue'].replace(',', ''))
        except ValueError:
            continue
        inv[x['LineDescription']][int(x['TimePeriod'])] = v
    lines = list(inv)

    def find_line(kw):
        c = [l for l in lines if kw.lower() in l.lower()]
        return min(c, key=len) if c else None

    results = []
    matched_log = []
    for fnm, (ttb, kw) in MAP.items():
        if fnm not in annual:
            continue
        bl = find_line(kw)
        if bl is None:
            matched_log.append(f'{fnm}: BEA該当なし({kw})')
            continue
        matched_log.append(f'{fnm} -> {bl[:40]} (TTB {ttb}m)')
        g = {y: inv[bl][y] / inv[bl][y - 1] - 1 for y in inv[bl] if y - 1 in inv[bl] and inv[bl][y - 1] > 0}
        # ブーム: 自分史の上位1/4(その年までの拡大窓・最低20年)
        booms = []
        ys = sorted(g)
        for j, y in enumerate(ys):
            hist = [g[x] for x in ys[:j + 1]]
            if len(hist) < 20:
                continue
            if g[y] >= sorted(hist)[int(0.75 * len(hist))]:
                booms.append(y)
        # 超過リターン: 全49業種平均との差
        mkty = {y: statistics.mean([annual[n][y] for n in annual if y in annual[n]])
                for y in range(1948, 2026)}
        path = {}
        for k in range(1, 6):
            vals = [annual[fnm][b + k] - mkty[b + k] for b in booms
                    if b + k in annual[fnm] and b + k in mkty]
            if len(vals) >= 8:
                path[k] = statistics.mean(vals)
        if len(path) == 5:
            kstar = min(path, key=path.get)
            results.append((fnm, ttb, kstar, len(booms), {k: round(v, 3) for k, v in path.items()}))
    # 主検定
    def spearman(a, b):
        def rk(v):
            s = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v)
            for j, i in enumerate(s):
                r[i] = j
            return r
        ra, rb = rk(a), rk(b)
        ma, mb = statistics.mean(ra), statistics.mean(rb)
        num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        da = math.sqrt(sum((x - ma) ** 2 for x in ra)); db = math.sqrt(sum((y - mb) ** 2 for y in rb))
        return num / (da * db) if da * db > 0 else 0.0
    ttbs = [r[1] for r in results]; ks = [r[2] for r in results]
    rho = spearman(ttbs, ks)
    rng = random.Random(211); cnt = 0; B = 5000
    for _ in range(B):
        sh = ttbs[:]; rng.shuffle(sh)
        if spearman(sh, ks) >= rho:
            cnt += 1
    p = cnt / B
    L = ['', f'TTB-HORIZON 2026-07-22 (notes/51主検定。n={len(results)}業種, French49×BEA3.7ESI×Koeva Table1)',
         '  ' + ' / '.join(f'{r[0]}(TTB{r[1]}m,k*={r[2]})' for r in results),
         f'  主検定: Spearman rho(TTB, k*)={rho:+.3f} 並べ替えp={p:.3f}',
         f'  -> {"PASS: 反転の遅れは建設時間に比例(株式でもラグ法則成立)" if rho > 0 and p < 0.05 else "FAIL: 株式には翻訳されない(株価の先回り織り込みと整合)"}']
    for r in results:
        L.append(f'    {r[0]:6s} TTB={r[1]:3d}m booms={r[3]:3d} path(k=1..5)={r[4]}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(matched_log))
    print('\n'.join(L))


if __name__ == '__main__':
    main()
