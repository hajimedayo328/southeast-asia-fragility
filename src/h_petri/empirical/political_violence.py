# -*- coding: utf-8 -*-
# notes/47: 政治暴力(クーデター+武力紛争)×警報
# (i) 記述: 見逃しは政治暴力国に集中するか (ii) 主検定: GG+TF+COUP12+WAR1 従来バー
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

ALIAS = {
    'ivory coast': 'CIV', "cote d'ivoire": 'CIV', 'burkina faso': 'BFA',
    'burkina faso (upper volta)': 'BFA', 'guinea bissau': 'GNB', 'guinea-bissau': 'GNB',
    'congo': 'COG', 'congo-brazzaville': 'COG', 'congo, republic of': 'COG',
    'congo, democratic republic of': 'COD', 'congo, democratic republic of (zaire)': 'COD',
    'dr congo (zaire)': 'COD', 'zaire': 'COD', 'cambodia': 'KHM',
    'cambodia (kampuchea)': 'KHM', 'kampuchea': 'KHM', 'laos': 'LAO',
    'vietnam': 'VNM', 'south vietnam': None, 'vietnam, south': None,
    'vietnam (north vietnam)': 'VNM', 'yemen': 'YEM', 'yemen arab republic': 'YEM',
    'yemen (north yemen)': 'YEM', "yemen pdr (south yemen)": None,
    'yemen, north': 'YEM', 'yemen, south': None, 'south yemen': None,
    'north yemen': 'YEM', 'tanzania': 'TZA', 'trinidad and tobago': 'TTO',
    'trinidad': 'TTO', 'myanmar': 'MMR', 'myanmar (burma)': 'MMR', 'burma': 'MMR',
    'burma/myanmar': 'MMR', 'russia': 'RUS', 'russia (soviet union)': 'RUS',
    'ussr': None, 'soviet union': None, 'turkey': 'TUR', 'turkiye': 'TUR',
    'egypt': 'EGY', 'iran': 'IRN', 'syria': 'SYR', 'venezuela': 'VEN',
    'bolivia': 'BOL', 'gambia': 'GMB', 'the gambia': 'GMB', 'bahamas': 'BHS',
    'south korea': 'KOR', 'korea, south': 'KOR', 'korea south': 'KOR',
    'north korea': None, 'korea, north': None, 'czechoslovakia': None,
    'yugoslavia': None, 'serbia (yugoslavia)': 'SRB', 'macedonia': 'MKD',
    'madagascar (malagasy)': 'MDG', 'sri lanka': 'LKA', 'sri lanka (ceylon)': 'LKA',
    'ceylon': 'LKA', 'zimbabwe': 'ZWE', 'zimbabwe (rhodesia)': 'ZWE',
    'rhodesia': 'ZWE', 'suriname': 'SUR', 'surinam': 'SUR', 'kyrgyzstan': 'KGZ',
    'central african republic': 'CAF', 'united arab emirates': 'ARE',
    'equatorial guinea': 'GNQ', 'sao tome and principe': 'STP',
    'sao tome': 'STP', 'comoros': 'COM', 'cape verde': 'CPV', 'cabo verde': 'CPV',
    'slovakia': 'SVK', 'czech republic': 'CZE', 'east timor': 'TLS',
    'timor-leste': 'TLS', 'timor leste (east timor)': 'TLS', 'brunei': 'BRN',
    'philippines': 'PHL', 'dominican republic': 'DOM', 'haiti': 'HTI',
    'moldova': 'MDA', 'belarus': 'BLR', 'ecuador': 'ECU',
    'democratic republic of the congo': 'COD', 'bosnia-herzegovina': 'BIH',
    'swaziland': 'SWZ', 'somalia': 'SOM', 'eswatini': 'SWZ',
    'united states of america': 'USA', 'yemen arab republic; n. yemen': 'YEM',
    "yemen people's republic; s. yemen": None, 'republic of vietnam': None,
    'hyderabad': None, 'taiwan': None,
}


def build_name_map(meta):
    m = {v['name'].strip().lower(): k for k, v in meta.items()}
    m.update({k: v for k, v in ALIAS.items()})
    return m


def to_iso(name, nmap, unmatched):
    n = name.strip().lower()
    if n in nmap:
        return nmap[n]
    unmatched.add(name)
    return None


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
    nmap = build_name_map(meta)
    unmatched = set()

    # クーデター(事件月)
    coup_months = defaultdict(set)
    with open(ROOT / 'data_raw/powell_thyne_coups.txt', encoding='utf-8', errors='replace') as f:
        r = csv.reader(f, delimiter='\t')
        hdr = next(r)
        idx = {h: i for i, h in enumerate(hdr)}
        n_coup = 0
        for row in r:
            try:
                nm = row[idx['country']].strip('"')
                y = int(row[idx['year']]); mo = int(row[idx['month']])
            except (ValueError, IndexError):
                continue
            iso = to_iso(nm, nmap, unmatched)
            if iso:
                coup_months[iso].add(y * 12 + mo - 1)
                n_coup += 1
    # 紛争(国年)
    war_years = defaultdict(set)
    with open(ROOT / 'data_raw/ucdp/UcdpPrioConflict_v25_1.csv', encoding='utf-8', errors='replace') as f:
        n_war = 0
        for row in csv.DictReader(f):
            try:
                y = int(row['year'])
            except (ValueError, KeyError):
                continue
            for nm in row['location'].split(','):
                iso = to_iso(nm, nmap, unmatched)
                if iso:
                    war_years[iso].add(y)
                    n_war += 1
    print(f'coup events mapped: {n_coup}, war country-years: {n_war}')
    print(f'unmatched sample: {sorted(unmatched)[:15]} (total {len(unmatched)})')

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

    def coup12(c, i):
        return 1.0 if any((i - k) in coup_months.get(c, set()) for k in range(0, 12)) else 0.0

    def war1(c, i):
        return 1.0 if (i // 12 - 1) in war_years.get(c, set()) else 0.0

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
            rows.append((c, i, g, tf, coup12(c, i), war1(c, i), lab))
    LAB = 6
    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]

    # ---- (i) 記述: 見逃しと政治暴力 ----
    e_g = make_ecdf([r[2] for r in train]); e_t = make_ecdf([r[3] for r in train])
    pos = [r for r in train if r[LAB] == 1]; neg = [r for r in train if r[LAB] == 0]
    rng = random.Random(131)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    w0, b0 = fit_logit([[e_g(r[2]), e_t(r[3])] for r in sub], [r[LAB] for r in sub])
    bym = defaultdict(list)
    for r in test:
        bym[r[1]].append((b0 + w0[0] * e_g(r[2]) + w0[1] * e_t(r[3]), r[0]))
    gp = {}
    for i, lst in bym.items():
        lst.sort(reverse=True)
        n = len(lst)
        for k, (s, c) in enumerate(lst):
            gp[(c, i)] = k / n
    onsets_te = [(c, i0) for c, s in onset_idx.items() for i0 in s
                 if 2000 * 12 <= i0 < 2025 * 12]
    grp = {'caught': [], 'miss_hi': [], 'miss_lo': []}
    for c, i0 in onsets_te:
        pcts = [gp[(c, j)] for j in range(i0 - H, i0) if (c, j) in gp]
        if not pcts:
            continue
        best = min(pcts)
        key = 'caught' if best <= Q else ('miss_hi' if best <= 0.5 else 'miss_lo')
        pol_c = 1 if any((i0 - k) in coup_months.get(c, set()) for k in range(0, 12)) else 0
        pol_w = 1 if (i0 // 12 - 1) in war_years.get(c, set()) else 0
        grp[key].append((pol_c, pol_w))
    base_c = sum(r[4] for r in test) / len(test)
    base_w = sum(r[5] for r in test) / len(test)
    L = ['', f'POLITICAL-VIOLENCE 2026-07-20 (notes/47。Powell-Thyne V2026.01.13 + UCDP/PRIO v25.1, h={H})',
         f'  (i) onset前12ヶ月クーデター率 / 前年紛争率 (test期基礎率: クーデター{base_c:.1%} / 紛争{base_w:.1%}):']
    for k, nm in (('caught', '捕捉(q10)'), ('miss_hi', '見逃し·順位10-50%'), ('miss_lo', '見逃し·順位下半分')):
        g = grp[k]
        if g:
            L.append(f'    {nm}: n={len(g)} クーデター{sum(x[0] for x in g)/len(g):.1%} 紛争{sum(x[1] for x in g)/len(g):.1%}')

    # ---- (ii) 主検定 ----
    def build(feats, seed):
        ecs = [make_ecdf([r[f] for r in train]) for f in feats]
        p2 = [r for r in train if r[LAB] == 1]; n2 = [r for r in train if r[LAB] == 0]
        rng2 = random.Random(seed)
        sub2 = p2 + rng2.sample(n2, min(len(n2), 5 * len(p2)))
        X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub2]
        w, b = fit_logit(X, [r[LAB] for r in sub2])
        return (lambda r: b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))), w

    y_te = [r[LAB] for r in test]
    s1, _ = build([2, 3], 132)
    s2, w2 = build([2, 3, 4, 5], 132)
    sc_c, _ = build([2, 3, 4], 133)
    sc_w, _ = build([2, 3, 5], 134)
    a1 = auc([s1(r) for r in test], y_te)
    a2 = auc([s2(r) for r in test], y_te)
    ac = auc([sc_c(r) for r in test], y_te)
    aw = auc([sc_w(r) for r in test], y_te)
    byc = defaultdict(list)
    for r in test:
        byc[r[0]].append(r)
    cl = sorted(byc); rng3 = random.Random(135); ds = []
    for bb in range(300):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng3.choice(cl)])
        yv = [r[LAB] for r in s]
        v1 = auc([s1(r) for r in s], yv); v2 = auc([s2(r) for r in s], yv)
        if v1 is not None and v2 is not None:
            ds.append(v2 - v1)
    ds.sort(); n = len(ds)
    d = a2 - a1
    L.append(f'  (ii) 主検定: GG+TF={a1:.4f} +COUP12+WAR1={a2:.4f} delta={d:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] 係数={["%.2f" % x for x in w2]}')
    L.append(f'      単独: +COUP12のみ={ac:.4f}({ac-a1:+.4f}) / +WAR1のみ={aw:.4f}({aw-a1:+.4f})')
    L.append(f'  -> {"PASS: 政治暴力は警報の材料になる" if ds[int(.025*n)] > 0 and d >= 0.03 else "FAIL"}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
