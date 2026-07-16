# -*- coding: utf-8 -*-
# EMP(市場圧力指数)による危機日付け直し + 主検定の再実行 (設計: notes/38・事前固定)
import csv, math, random, statistics, sys
from collections import defaultdict
from bisect import bisect_right
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from phase2_exp1_bis import auc, make_ecdf, fit_logistic


def load_monthly(path, valcol, keycols=('iso3', 'period')):
    out = defaultdict(dict)
    with open(ROOT / path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                per = row['period']
                y, m = per.split('-M')
                out[row['iso3']][(int(y), int(m))] = float(row[valcol])
            except (ValueError, KeyError):
                continue
    return out


def main():
    fxm = defaultdict(dict)
    with open(ROOT / 'data_raw/er_monthly.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for iso, per, v in r:
            try:
                y, m = per.split('-M')
                fxm[iso][(int(y), int(m))] = float(v)
            except ValueError:
                continue
    res = load_monthly('data_raw/il_reserves_monthly.csv', 'reserves_usd')
    # 金利: MMRT優先、無ければDISR
    rates = defaultdict(dict)
    pref = defaultdict(dict)
    with open(ROOT / 'data_raw/mfs_rates_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                k = (int(y), int(m))
                kind = row['kind']
                v = float(row['rate'])
            except (ValueError, KeyError):
                continue
            iso = row['iso3']
            if kind == 'MMRT':
                pref[iso][k] = v
            else:
                rates[iso].setdefault(k, v)
    for iso in pref:
        rates[iso].update(pref[iso])

    def prev(d, y, m):
        i = y * 12 + m - 2
        return d.get((i // 12, i % 12 + 1))

    # 成分計算(データ掃除: |dE|,|dR|<=1, |dI|<=50pp — 測定エラー除去、チューニングではない)
    comps = {}
    for iso in fxm:
        for (y, m), e in fxm[iso].items():
            e0 = prev(fxm[iso], y, m)
            if not e0 or e0 <= 0:
                continue
            dE = e / e0 - 1
            if abs(dE) > 1:
                continue
            r0 = prev(res.get(iso, {}), y, m)
            r1 = res.get(iso, {}).get((y, m))
            dR = None
            if r0 and r1 and r0 > 0:
                dR = r1 / r0 - 1
                if abs(dR) > 1:
                    dR = None
            i0 = prev(rates.get(iso, {}), y, m)
            i1 = rates.get(iso, {}).get((y, m))
            dI = None
            if i0 is not None and i1 is not None:
                dI = i1 - i0
                if abs(dI) > 50:
                    dI = None
            if dR is None:
                continue  # 準備なしは判定不能(事前固定)
            comps[(iso, y, m)] = (dE, dR, dI)

    s_e = statistics.pstdev([c[0] for c in comps.values()])
    s_r = statistics.pstdev([c[1] for c in comps.values()])
    s_i = statistics.pstdev([c[2] for c in comps.values() if c[2] is not None])
    print(f'components n={len(comps)}  pooled sd: e={s_e:.4f} r={s_r:.4f} i={s_i:.3f}')

    emp = {}
    for k, (dE, dR, dI) in comps.items():
        v = dE / s_e + (-dR) / s_r
        if dI is not None:
            v += dI / s_i
        emp[k] = v
    mu = statistics.mean(emp.values())
    sd = statistics.pstdev(emp.values())
    print(f'EMP: mean={mu:.3f} sd={sd:.3f}')

    def crisis_sets(k_sigma):
        thr = mu + k_sigma * sd
        cr = {k for k, v in emp.items() if v > thr}
        st = defaultdict(set)
        for (iso, y, m) in cr:
            st[iso].add((y, m))
        onsets = []
        for iso, s in st.items():
            idxs = {y * 12 + m - 1 for (y, m) in s}
            for (y, m) in sorted(s):
                if not any((y * 12 + m - 1 - k) in idxs for k in range(1, 13)):
                    onsets.append((iso, y, m))
        return cr, onsets

    L = ['', 'EMP-DATING 2026-07-16 (設計notes/38。為替+準備+金利の市場圧力指数。プールsd加重、閾値mean+kσ)',
         f'被覆: 成分計算可能 {len(comps)} 国月 (為替203/準備179/金利116カ国)']
    for ks in (1.5, 2.0, 2.5):
        cr, ons = crisis_sets(ks)
        L.append(f'  k={ks}: 危機国月={len(cr)} onset={len(ons)}')
    cr, ons = crisis_sets(2.0)

    # サニティ: 防衛成功事例
    probes = [('HKG', 1997, 1998, '香港ペッグ防衛'), ('BRA', 1997, 1999, 'ブラジル防衛→99陥落'),
              ('THA', 1996, 1997, 'タイ防衛→97陥落'), ('ARG', 1995, 1995, 'テキーラ余波(防衛成功)')]
    L.append('サニティ(防衛成功が点灯するか, k=2):')
    for iso, y0, y1, label in probes:
        hits = sorted((y, m) for (i2, y, m) in cr if i2 == iso and y0 <= y <= y1)
        L.append(f'  {label}: {[f"{y}-{m:02d}" for y, m in hits] if hits else "点灯なし"}')

    # FXのみ日付けとの重なり
    def fx_crashes(d):
        c = set()
        for (y, m) in sorted(d):
            def back(k):
                i = y * 12 + m - 1 - k
                return d.get((i // 12, i % 12 + 1))
            cur = d[(y, m)]; p1 = back(12); p2 = back(24)
            if p1 and p1 > 0 and p2 and p2 > 0:
                dep = cur / p1 - 1; dp = p1 / p2 - 1
                if dep >= 0.30 and dep - dp >= 0.10:
                    c.add((y, m))
        return c
    fx_cr = set()
    for iso in fxm:
        for k in fx_crashes(fxm[iso]):
            fx_cr.add((iso, k[0], k[1]))
    both = fx_cr & set(emp)  # 比較はEMP計算可能な国月に限定
    fx_in = {k for k in fx_cr if k in emp}
    cap = len(fx_in & cr) / max(1, len(fx_in))
    L.append(f'重なり: FX危機のうちEMP(k=2)でも点灯 {cap:.0%} / EMP危機のうちFXでも点灯 {len(fx_in & cr)/max(1,len(cr)):.0%}')
    L.append(f'  EMPのみ(=防衛・準備流出型) {len(cr - fx_cr)} 国月, FXのみ {len(fx_in - cr)} 国月')

    # 主検定再実行: EMP年次ラベル
    meta = fp.load_real_countries(); real = set(meta)
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    trade = defaultdict(lambda: defaultdict(dict))
    with open(ROOT / 'data_raw/imts_trade.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, v in r:
            try:
                trade[rep][int(yr)][cp] = float(v)
            except ValueError:
                continue
    ann_state = defaultdict(set)
    for (iso, y, m) in cr:
        ann_state[iso].add(y)
    ann_onset = set()
    for (iso, y, m) in ons:
        ann_onset.add((iso, y))

    rows = []
    for (c, t) in gg:
        if t > 2023 or t < 1978:
            continue
        if t in ann_state.get(c, set()):
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
        tf = sum(v for j, v in w.items() if t in ann_state.get(j, set())) / tot
        if not math.isfinite(tf):
            continue
        y_ = 1 if ((c, t + 1) in ann_onset or (c, t + 2) in ann_onset) else 0
        rows.append((c, t, g, tf, 0, y_))
    train = [x for x in rows if x[1] < 2000]
    test = [x for x in rows if x[1] >= 2000]
    y_te = [x[5] for x in test]
    aucA = auc([x[2] for x in test], y_te)
    e_g = make_ecdf([x[2] for x in train]); e_t = make_ecdf([x[3] for x in train])
    sc, wg = fit_logistic(train, [2, 3], [e_g, e_t])
    aucB = auc([sc(x) for x in test], y_te)
    byc = defaultdict(list)
    for x in test:
        byc[x[0]].append(x)
    cl = sorted(byc); rng = random.Random(12345); diffs = []
    for b in range(500):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        yv = [x[5] for x in s]
        a1 = auc([x[2] for x in s], yv); a2 = auc([sc(x) for x in s], yv)
        if a1 is not None and a2 is not None:
            diffs.append(a2 - a1)
    diffs.sort(); n = len(diffs)
    p = 2 * min(sum(1 for d in diffs if d <= 0), sum(1 for d in diffs if d >= 0)) / n
    L.append(f'主検定(EMPラベル, k=2): n={len(rows)} (train危機={sum(x[5] for x in train)}/test={sum(y_te)})')
    L.append(f'  GG={aucA:.4f} | GG+TF={aucB:.4f} delta={aucB - aucA:+.4f} CI[{diffs[int(.025*n)]:+.4f},{diffs[int(.975*n)]:+.4f}] p={p:.4f}')
    L.append(f'  -> {"PASS: 防衛込みラベルでも貿易火事は生存" if diffs[int(.025*n)] > 0 and aucB-aucA >= 0.03 else "判定は本文の読みで"}')

    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
