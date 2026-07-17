# -*- coding: utf-8 -*-
# REGIME-TEST (事前固定): 為替制度は危機の型を決めるか (IRR Coarse分類)
# 制度はイベント12ヶ月前の値(逆流防止)。コード1-2=固定側, 3-4=変動側。5(自由落下=結果汚染),6(二重)は除外
# 予測: 固定側の危機は攻撃型に偏る / 変動側は崩壊型に偏る
# 合格 = 攻撃型シェア差(固定-変動)の国ブロックbootstrap CIが0を除外
import math, statistics, random, sys
from collections import defaultdict
from pathlib import Path
import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, build_emp_attacks, fx_crash_months


def load_regimes():
    wb = openpyxl.load_workbook(ROOT / 'data_raw/irr_regime_monthly.xlsx', read_only=True, data_only=True)
    ws = wb['Coarse']
    rows = list(ws.iter_rows(values_only=True))
    # 国名 = 行5-6の結合(複数行に折り返す名がある)
    names = []
    for ci in range(2, len(rows[5])):
        parts = []
        for ri in (4, 5):
            v = rows[ri][ci]
            if v and str(v).strip() and str(v).strip() != 'Country':
                parts.append(str(v).strip())
        names.append(' '.join(parts).strip())
    reg = defaultdict(dict)
    for r in rows[7:]:
        d = r[1]
        if not d or 'M' not in str(d):
            continue
        try:
            y, m = str(d).split('M')
            y, m = int(y), int(m)
        except ValueError:
            continue
        for ci in range(2, len(r)):
            v = r[ci]
            if v is None:
                continue
            try:
                code = int(v)
            except (ValueError, TypeError):
                continue
            nm = names[ci - 2]
            if nm:
                reg[nm][(y, m)] = code
    return reg


def main():
    reg_by_name = load_regimes()
    meta = fp.load_real_countries()
    name2iso = {v['name'].strip().lower(): k for k, v in meta.items()}
    alias = {'korea': 'KOR', 'south korea': 'KOR', 'russia': 'RUS', 'egypt': 'EGY', 'iran': 'IRN',
             'venezuela': 'VEN', 'syria': 'SYR', 'turkey': 'TUR', 'ivory coast': 'CIV',
             "cote d'ivoire": 'CIV', 'cape verde': 'CPV', 'swaziland': 'SWZ', 'myanmar': 'MMR',
             'burma': 'MMR', 'vietnam': 'VNM', 'laos': 'LAO', 'kyrgyzstan': 'KGZ',
             'slovakia': 'SVK', 'macedonia': 'MKD', 'czech republic': 'CZE', 'yemen': 'YEM',
             'congo, dem. rep.': 'COD', 'democratic republic of the congo': 'COD', 'zaire': 'COD',
             'congo, rep.': 'COG', 'republic of congo': 'COG', 'congo': 'COG',
             'the bahamas': 'BHS', 'the gambia': 'GMB', 'gambia': 'GMB',
             'st. kitts and nevis': 'KNA', 'st. lucia': 'LCA', 'united states': 'USA',
             'united kingdom': 'GBR', 'bolivia': 'BOL', 'tanzania': 'TZA', 'moldova': 'MDA'}
    regimes = defaultdict(dict)
    unmatched = []
    for nm, d in reg_by_name.items():
        key = nm.lower()
        iso = name2iso.get(key) or alias.get(key)
        if not iso:
            cand = [k for n, k in name2iso.items() if key in n or n in key]
            iso = cand[0] if len(cand) == 1 else None
        if not iso:
            unmatched.append(nm)
            continue
        regimes[iso].update(d)
    print(f'制度データ: {len(regimes)}カ国にマップ, 未対応 {len(unmatched)}')

    # 危機イベント(taxonomyと同一構成)
    fxm = load_fxm()
    attacks = build_emp_attacks(fxm)
    fx_on = []
    for iso in fxm:
        cr = fx_crash_months(fxm[iso])
        idxs = {y * 12 + m - 1 for (y, m) in cr}
        for (y, m) in sorted(cr):
            if not any((y * 12 + m - 1 - k) in idxs for k in range(1, 13)):
                fx_on.append((iso, y, m))
    att_idx = defaultdict(set)
    for iso, y, m in attacks:
        att_idx[iso].add(y * 12 + m - 1)
    fx_idx = defaultdict(set)
    for iso, y, m in fx_on:
        fx_idx[iso].add(y * 12 + m - 1)

    def near(s, i, w=6):
        return any((i + k) in s for k in range(-w, w + 1))

    events = []
    for iso, y, m in fx_on:
        i = y * 12 + m - 1
        t = 'overlap' if near(att_idx.get(iso, set()), i) else 'collapse'
        events.append((iso, y, m, t))
    for iso, y, m in attacks:
        i = y * 12 + m - 1
        if not near(fx_idx.get(iso, set()), i):
            events.append((iso, y, m, 'attack'))

    rows = []
    for iso, y, m, t in events:
        pi = y * 12 + m - 1 - 12   # 12ヶ月前
        code = regimes.get(iso, {}).get((pi // 12, pi % 12 + 1))
        if code is None or code not in (1, 2, 3, 4):
            continue
        fixed = 1 if code <= 2 else 0
        rows.append((iso, fixed, t))
    n_fix = sum(1 for r in rows if r[1]); n_flex = len(rows) - n_fix

    def share(sel, typ):
        s = [r for r in rows if r[1] == sel]
        return sum(1 for r in s if r[2] == typ) / max(1, len(s))
    a_fix, a_flex = share(1, 'attack'), share(0, 'attack')
    c_fix, c_flex = share(1, 'collapse'), share(0, 'collapse')
    obs = a_fix - a_flex
    byc = defaultdict(list)
    for r in rows:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(3); ds = []
    for b in range(1000):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        f1 = [r for r in s if r[1] == 1]; f0 = [r for r in s if r[1] == 0]
        if not f1 or not f0:
            continue
        ds.append(sum(1 for r in f1 if r[2] == 'attack') / len(f1) - sum(1 for r in f0 if r[2] == 'attack') / len(f0))
    ds.sort(); n = len(ds)
    lo, hi = ds[int(.025 * n)], ds[int(.975 * n)]
    L = ['', 'REGIME-TEST 2026-07-18 (為替制度は危機の型を決めるか: IRR分類, 制度=イベント12ヶ月前, code5/6除外)',
         f'イベント(制度1-4のみ) {len(rows)} (固定側{n_fix}/変動側{n_flex})',
         f'攻撃型シェア: 固定側={a_fix:.3f} vs 変動側={a_flex:.3f} (差{obs:+.3f})',
         f'崩壊型シェア: 固定側={c_fix:.3f} vs 変動側={c_flex:.3f}',
         f'攻撃型シェア差(固定-変動) CI[{lo:+.3f},{hi:+.3f}] -> {"PASS: 制度が型を決める" if lo > 0 else "FAIL"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
