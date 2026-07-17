# -*- coding: utf-8 -*-
# LANE-INTERACTION (事前固定): 二車線理論の核心検定
# (a) 攻撃率の2x2: 貯金(準備月数, 前四半期末)の下位1/3=薄 × GSIの上位1/3=嵐。
#     予測=掛け算構造: rate(薄,嵐) > rate(薄,凪)*rate(厚,嵐)/rate(厚,凪)
#     合格 = 交互作用比(ratio of ratios)の国ブロックbootstrap CIが1を除外
# (b) 抑止力の交絡チェック: 攻撃予測でRM(月次準備)はGG(年次家計簿)を超えるか
import csv, math, statistics, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from phase2_exp1_bis import auc, make_ecdf, fit_logistic
from attack_anatomy import load_fxm, build_emp_attacks


def main():
    fxm = load_fxm()
    attacks = build_emp_attacks(fxm)
    att_q = defaultdict(set)
    for iso, y, m in attacks:
        att_q[iso].add((y, (m - 1) // 3 + 1))

    res = defaultdict(dict)
    with open(ROOT / 'data_raw/il_reserves_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                res[row['iso3']][(int(y), int(m))] = float(row['reserves_usd'])
            except (ValueError, KeyError):
                continue
    imports = defaultdict(lambda: defaultdict(float))
    with open(ROOT / 'data_raw/imts_trade_xm.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, xv, mv in r:
            try:
                imports[rep][int(yr)] += float(mv)
            except ValueError:
                continue

    # GSI(四半期, TWEXM時代+DTWEXBGS延長: 1978-2025)
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
    ff = monthly('data_raw/fred_FEDFUNDS.csv')
    dx1 = monthly('data_raw/fred_TWEXM.csv')
    dx2 = monthly('data_raw/fred_DTWEXBGS.csv')
    dx = dict(dx2); dx.update({k: v for k, v in dx1.items() if k not in dx2})
    oil = monthly('data_raw/fred_WTISPLC.csv'); vix = monthly('data_raw/fred_VIXCLS.csv')
    QS = [(y, q) for y in range(1978, 2026) for q in (1, 2, 3, 4)]

    def qv(d, y, q, chg=False):
        vs = [d[m] for m in [(y, 3*q-2), (y, 3*q-1), (y, 3*q)] if m in d]
        if not vs:
            return None
        cur = statistics.mean(vs)
        if not chg:
            return cur
        vs0 = [d[m] for m in [(y-1, 3*q-2), (y-1, 3*q-1), (y-1, 3*q)] if m in d]
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
    gv = sorted(gsi.values())
    storm_thr = gv[int(2 / 3 * len(gv))]   # 上位1/3=嵐

    def rm_at_qstart(iso, y, q):
        # 前四半期末の月の準備 / 前年輸入
        pm = (y, 3 * (q - 1)) if q > 1 else (y - 1, 12)
        r1 = res.get(iso, {}).get(pm)
        imp = imports.get(iso, {}).get(y - 1)
        if not r1 or not imp or imp <= 0:
            return None
        v = r1 / (imp / 12.0)
        return v if math.isfinite(v) and v <= 120 else None

    meta = fp.load_real_countries(); real = set(meta)
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}

    # パネル構築(攻撃中の四半期は除外: onset四半期+次を除く簡易処置)
    in_att = defaultdict(set)
    for iso, y, m in attacks:
        q0 = (m - 1) // 3 + 1
        idx = (y * 4 + q0 - 1)
        for k in range(0, 3):
            in_att[iso].add(idx + k)
    panel = []
    for iso in res:
        for (y, q) in QS:
            if gsi.get((y, q)) is None:
                continue
            idx = y * 4 + q - 1
            rm = rm_at_qstart(iso, y, q)
            if rm is None:
                continue
            onset_here = (y, q) in att_q.get(iso, set())
            if not onset_here and idx in in_att.get(iso, set()):
                continue   # 攻撃継続中(onsetでない)は除外
            panel.append((iso, y, q, rm, gsi[(y, q)], 1 if onset_here else 0))

    # 四半期ごとの薄/厚(下位1/3=薄)
    byq = defaultdict(list)
    for p in panel:
        byq[(p[1], p[2])].append(p)
    cells = defaultdict(lambda: [0, 0])   # (thin,storm) -> [attacks, n]
    rows_b = []
    for (y, q), grp in byq.items():
        if len(grp) < 20:
            continue
        rms = sorted(p[3] for p in grp)
        thin_thr = rms[int(len(rms) / 3)]
        storm = gsi[(y, q)] > storm_thr
        for p in grp:
            thin = p[3] <= thin_thr
            cells[(thin, storm)][0] += p[5]
            cells[(thin, storm)][1] += 1
            rows_b.append((p[0], thin, storm, p[5], p[3], gg.get((p[0], y - 1))))

    def rate(k):
        a, n = cells[k]
        return a / n if n else 0.0
    r_ts = rate((True, True)); r_tc = rate((True, False))
    r_hs = rate((False, True)); r_hc = rate((False, False))
    ror = (r_ts / r_tc) / (r_hs / r_hc) if min(r_tc, r_hs, r_hc) > 0 else float('nan')

    # 国ブロックbootstrapでrorのCI
    byc = defaultdict(list)
    for r in rows_b:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(11); rors = []
    for b in range(500):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        c2 = defaultdict(lambda: [0, 0])
        for iso, thin, storm, hit, rm, g in s:
            c2[(thin, storm)][0] += hit
            c2[(thin, storm)][1] += 1
        try:
            rr = ((c2[(True, True)][0] / c2[(True, True)][1]) / (c2[(True, False)][0] / c2[(True, False)][1])) / \
                 ((c2[(False, True)][0] / c2[(False, True)][1]) / (c2[(False, False)][0] / c2[(False, False)][1]))
            if math.isfinite(rr):
                rors.append(rr)
        except ZeroDivisionError:
            continue
    rors.sort(); n = len(rors)
    lo, hi = rors[int(.025 * n)], rors[int(.975 * n)]

    L = ['', 'LANE-INTERACTION 2026-07-17 (二車線理論の核心: 攻撃率は「薄い貯金×嵐」で掛け算的に跳ねるか)',
         f'panel={len(panel)}国四半期, 攻撃onset={sum(p[5] for p in panel)}',
         f'攻撃率2x2: 薄×嵐={r_ts:.3f} 薄×凪={r_tc:.3f} 厚×嵐={r_hs:.3f} 厚×凪={r_hc:.3f}',
         f'交互作用比(RoR)={ror:.2f} CI[{lo:.2f},{hi:.2f}] -> {"PASS: 掛け算構造(相乗)" if lo > 1 else "FAIL: 相加どまり(車線は独立)" if hi < 1 or lo <= 1 <= hi else "?"}']

    # (b) 抑止力の交絡: RM vs GG
    sub = [r for r in rows_b if r[5] is not None and math.isfinite(r[5])]
    a_rm = auc([-r[4] for r in sub], [r[3] for r in sub])
    a_gg = auc([r[5] for r in sub], [r[3] for r in sub])
    data = [(r[0], 0, -r[4], r[5], 0, r[3]) for r in sub]
    e_r = make_ecdf([d[2] for d in data]); e_g = make_ecdf([d[3] for d in data])
    sc, wg = fit_logistic(data, [2, 3], [e_r, e_g])
    a_j = auc([sc(d) for d in data], [d[5] for d in data])
    L.append(f'(b) 抑止力の交絡チェック(n={len(sub)}): RM(月次準備)={a_rm:.3f} GG(年次家計簿)={a_gg:.3f} 両方={a_j:.3f} 係数(RM,GG)={["%.3f" % w for w in wg]}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
