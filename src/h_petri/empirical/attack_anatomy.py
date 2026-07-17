# -*- coding: utf-8 -*-
# ATTACK-ANATOMY (事前固定):
# (a) 嵐→攻撃: 四半期EMP攻撃件数×GSI(lag0-4全報告)。予測=正で有意
# (b) 攻撃→崩壊: EMP攻撃onset条件付きで「12ヶ月以内にFX崩壊」~ rank(GG)+rank(TF)。予測=両方正
import csv, math, statistics, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from phase2_exp1_bis import auc, make_ecdf, fit_logistic


def load_fxm():
    fxm = defaultdict(dict)
    with open(ROOT / 'data_raw/er_monthly.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for iso, per, v in r:
            try:
                y, m = per.split('-M')
                fxm[iso][(int(y), int(m))] = float(v)
            except ValueError:
                continue
    return fxm


def build_emp_attacks(fxm):
    res = defaultdict(dict)
    with open(ROOT / 'data_raw/il_reserves_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                res[row['iso3']][(int(y), int(m))] = float(row['reserves_usd'])
            except (ValueError, KeyError):
                continue
    rates = defaultdict(dict); pref = defaultdict(dict)
    with open(ROOT / 'data_raw/mfs_rates_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                k = (int(y), int(m)); v = float(row['rate'])
            except (ValueError, KeyError):
                continue
            (pref if row['kind'] == 'MMRT' else rates)[row['iso3']].setdefault(k, v)
    for iso in pref:
        rates[iso].update(pref[iso])

    def prev(d, y, m):
        i = y * 12 + m - 2
        return d.get((i // 12, i % 12 + 1))

    comps = {}
    for iso in fxm:
        for (y, m), e in fxm[iso].items():
            e0 = prev(fxm[iso], y, m)
            if not e0 or e0 <= 0:
                continue
            dE = e / e0 - 1
            if abs(dE) > 1:
                continue
            r0 = prev(res.get(iso, {}), y, m); r1 = res.get(iso, {}).get((y, m))
            if not r0 or not r1 or r0 <= 0:
                continue
            dR = r1 / r0 - 1
            if abs(dR) > 1:
                continue
            i0 = prev(rates.get(iso, {}), y, m); i1 = rates.get(iso, {}).get((y, m))
            dI = None
            if i0 is not None and i1 is not None:
                dI = i1 - i0
                if abs(dI) > 50:
                    dI = None
            comps[(iso, y, m)] = (dE, dR, dI)
    s_e = statistics.pstdev([c[0] for c in comps.values()])
    s_r = statistics.pstdev([c[1] for c in comps.values()])
    s_i = statistics.pstdev([c[2] for c in comps.values() if c[2] is not None])
    emp = {k: (dE / s_e + (-dR) / s_r + ((dI / s_i) if dI is not None else 0))
           for k, (dE, dR, dI) in comps.items()}
    mu = statistics.mean(emp.values()); sd = statistics.pstdev(emp.values())
    cr = {k for k, v in emp.items() if v > mu + 2 * sd}
    st = defaultdict(set)
    for (iso, y, m) in cr:
        st[iso].add((y, m))
    attacks = []
    for iso, s in st.items():
        idxs = {y * 12 + m - 1 for (y, m) in s}
        for (y, m) in sorted(s):
            if not any((y * 12 + m - 1 - k) in idxs for k in range(1, 13)):
                attacks.append((iso, y, m))
    return attacks


def fx_crash_months(d):
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


def monthly(path):
    acc = defaultdict(list)
    with open(ROOT / path, encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for row in r:
            try:
                acc[(int(row[0][:4]), int(row[0][5:7]))].append(float(row[1]))
            except (ValueError, IndexError):
                continue
    return {k: statistics.mean(v) for k, v in acc.items()}


def pearson(a, b):
    ma, mb = statistics.mean(a), statistics.mean(b)
    sa, sb = statistics.pstdev(a), statistics.pstdev(b)
    if sa == 0 or sb == 0:
        return 0.0
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / len(a) / (sa * sb)


def lag1f(xs):
    m = statistics.mean(xs)
    den = sum((x - m) ** 2 for x in xs)
    return sum((xs[i] - m) * (xs[i + 1] - m) for i in range(len(xs) - 1)) / den if den > 0 else 0


def main():
    fxm = load_fxm()
    attacks = build_emp_attacks(fxm)
    print(f'EMP攻撃onset: {len(attacks)}')
    crash_m = {iso: fx_crash_months(fxm[iso]) for iso in fxm}

    # (a) 嵐→攻撃
    byq = defaultdict(int)
    for iso, y, m in attacks:
        byq[(y, (m - 1) // 3 + 1)] += 1
    ff = monthly('data_raw/fred_FEDFUNDS.csv'); dx = monthly('data_raw/fred_TWEXM.csv')
    oil = monthly('data_raw/fred_WTISPLC.csv'); vix = monthly('data_raw/fred_VIXCLS.csv')
    QS = [(y, q) for y in range(1978, 2026) for q in (1, 2, 3, 4)]

    def qv(d, y, q, chg=False):
        vs = [d[m] for m in [(y, 3 * q - 2), (y, 3 * q - 1), (y, 3 * q)] if m in d]
        if not vs:
            return None
        cur = statistics.mean(vs)
        if not chg:
            return cur
        vs0 = [d[m] for m in [(y - 1, 3 * q - 2), (y - 1, 3 * q - 1), (y - 1, 3 * q)] if m in d]
        if not vs0 or statistics.mean(vs0) == 0:
            return None
        return cur / statistics.mean(vs0) - 1

    raw = {'dx': [qv(dx, y, q, True) for y, q in QS], 'oil': [qv(oil, y, q, True) for y, q in QS],
           'ff': [qv(ff, y, q) for y, q in QS], 'vix': [qv(vix, y, q) for y, q in QS]}

    def zmap(xs):
        v = [x for x in xs if x is not None]
        m, s = statistics.mean(v), statistics.pstdev(v)
        return [None if x is None else (x - m) / s for x in xs]

    Z = {k: zmap(v) for k, v in raw.items()}
    gsi = {}
    for i, (y, q) in enumerate(QS):
        c = [Z['dx'][i], Z['ff'][i], (None if Z['oil'][i] is None else -Z['oil'][i]), Z['vix'][i]]
        c = [x for x in c if x is not None]
        if len(c) >= 3:
            gsi[(y, q)] = statistics.mean(c)

    L = ['', 'ATTACK-ANATOMY 2026-07-17 (理論スケッチの検証可能予測2本; 事前固定)']
    cells = []
    for lag in range(0, 5):
        pairs = []
        for i, (y, q) in enumerate(QS):
            j = i - lag
            if j < 0:
                continue
            g = gsi.get(QS[j])
            if g is not None:
                pairs.append((byq.get((y, q), 0), g))
        a = [p[0] for p in pairs]; b = [p[1] for p in pairs]
        r_ = pearson(a, b); ra, rb = lag1f(a), lag1f(b)
        neff = len(pairs) * (1 - ra * rb) / (1 + ra * rb) if (1 + ra * rb) > 0 else len(pairs)
        sig = '**' if abs(r_) > 2 / math.sqrt(max(4, neff)) else ''
        cells.append(f'lag{lag}: r={r_:+.3f}{sig}')
    L.append('(a) 嵐→攻撃 (GSI×EMP攻撃件数, 予測=正): ' + ' | '.join(cells))

    # (b) 攻撃→崩壊
    meta = fp.load_real_countries(); real = set(meta)
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    fx_a = fp.load_series('fx_lcu_per_usd', real)
    D_, A_ = fp.CRASH_RULES[fp.PRIMARY_RULE]
    crash_ann = fp.crash_years(fp.changes(fx_a, real, 1), fp.changes(fx_a, real, 2), D_, A_)
    trade = defaultdict(lambda: defaultdict(dict))
    with open(ROOT / 'data_raw/imts_trade.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, v in r:
            try:
                trade[rep][int(yr)][cp] = float(v)
            except ValueError:
                continue
    rows = []
    for (iso, y, m) in attacks:
        g = gg.get((iso, y - 1))
        if g is None or not math.isfinite(g):
            continue
        w = trade.get(iso, {}).get(y - 1, {})
        if len(w) < 3:
            continue
        tot = sum(w.values())
        if tot <= 0:
            continue
        tf = sum(v for j, v in w.items() if (j, y - 1) in crash_ann) / tot
        a0 = y * 12 + m - 1
        fell = any((i // 12, i % 12 + 1) in crash_m.get(iso, set()) for i in range(a0, a0 + 13))
        rows.append((iso, y, g, tf, 0, 1 if fell else 0))
    n_fall = sum(r[5] for r in rows)
    L.append(f'(b) 攻撃→崩壊: 攻撃onset {len(rows)}件(GG/貿易あり), 12ヶ月以内崩壊 {n_fall} ({n_fall/len(rows):.0%})')
    e_g = make_ecdf([r[2] for r in rows]); e_t = make_ecdf([r[3] for r in rows])
    sc, wg = fit_logistic(rows, [2, 3], [e_g, e_t])
    a_gg = auc([r[2] for r in rows], [r[5] for r in rows])
    a_tf = auc([r[3] for r in rows], [r[5] for r in rows])
    a_m = auc([sc(r) for r in rows], [r[5] for r in rows])
    byc = defaultdict(list)
    for r in rows:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(5); aa = []
    for b in range(500):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        v = auc([sc(x) for x in s], [x[5] for x in s])
        if v is not None:
            aa.append(v)
    aa.sort(); n = len(aa)
    L.append(f'  AUC: GG(前年家計簿)={a_gg:.3f} TF(前年火事)={a_tf:.3f} 両方={a_m:.3f} CI[{aa[int(.025*n)]:.3f},{aa[int(.975*n)]:.3f}]')
    L.append(f'  係数(GG,TF)={["%.3f" % w for w in wg]} (予測=両方正: 貯金薄+侵食→倒れる)')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
