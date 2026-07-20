# -*- coding: utf-8 -*-
# notes/46: 自己相対ランキング第2スクリーンで中位圏の見逃しを拾えるか
import csv, math, random, sys
from collections import defaultdict
from bisect import bisect_right, insort
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit

H = 6
Q = 0.10
LOOK = 120
MINH = 36


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
            rows.append((c, i, g, tf, lab))
    train = [r for r in rows if r[1] < 2000 * 12]
    e_g = make_ecdf([r[2] for r in train])
    e_t = make_ecdf([r[3] for r in train])
    pos = [r for r in train if r[4] == 1]
    neg = [r for r in train if r[4] == 0]
    rng = random.Random(121)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    w, b = fit_logit([[e_g(r[2]), e_t(r[3])] for r in sub], [r[4] for r in sub])
    score = {(r[0], r[1]): b + w[0] * e_g(r[2]) + w[1] * e_t(r[3]) for r in rows}
    lab_map = {(r[0], r[1]): r[4] for r in rows}

    # self_pct: 自国の過去120ヶ月内の百分位
    byc_series = defaultdict(dict)
    for (c, i), s in score.items():
        byc_series[c][i] = s
    self_pct = {}
    for c, ser in byc_series.items():
        for i, s in ser.items():
            hist = [ser[j] for j in range(i - LOOK, i) if j in ser]
            if len(hist) < MINH:
                continue
            hist.sort()
            self_pct[(c, i)] = bisect_right(hist, s) / len(hist)

    # 月ごとのスクリーン(test期)
    bym = defaultdict(list)
    for (c, i) in score:
        if i >= 2000 * 12:
            bym[i].append(c)
    glob_pct = {}
    selfrank_pct = {}
    for i, cs in bym.items():
        ranked = sorted(cs, key=lambda c: -score[(c, i)])
        n = len(ranked)
        for k, c in enumerate(ranked):
            glob_pct[(c, i)] = k / n
        avail = [c for c in cs if (c, i) in self_pct]
        ranked2 = sorted(avail, key=lambda c: -self_pct[(c, i)])
        n2 = max(1, len(ranked2))
        for k, c in enumerate(ranked2):
            selfrank_pct[(c, i)] = k / n2

    g10 = {k for k, v in glob_pct.items() if v <= Q}
    s10 = {k for k, v in selfrank_pct.items() if v <= Q}
    union = g10 | s10
    # 同予算の世界単独: 点灯数がunion以上になる最小q(0.01刻み)
    qE = None
    for qq in [x / 100 for x in range(10, 51)]:
        gq = {k for k, v in glob_pct.items() if v <= qq}
        if len(gq) >= len(union):
            qE = qq; gEq = gq
            break
    if qE is None:
        qE = 0.50; gEq = {k for k, v in glob_pct.items() if v <= qE}

    onsets_te = [(c, i0) for c, s in onset_idx.items() for i0 in s
                 if 2000 * 12 <= i0 < 2025 * 12]

    def caught(S, c, i0):
        return any((c, j) in S for j in range(i0 - H, i0))

    ev = []
    for c, i0 in onsets_te:
        if not any((c, j) in glob_pct for j in range(i0 - H, i0)):
            continue
        ev.append((c, caught(g10, c, i0), caught(s10, c, i0),
                   caught(union, c, i0), caught(gEq, c, i0),
                   min((glob_pct.get((c, j), 1) for j in range(i0 - H, i0)), default=1)))
    n_ev = len(ev)
    cg = sum(e[1] for e in ev); csf = sum(e[2] for e in ev)
    cu = sum(e[3] for e in ev); ce = sum(e[4] for e in ev)
    rescued = sum(1 for e in ev if not e[1] and e[2])
    # 記述: 見逃し(世界q10)の順位分布
    dist = {'10-20': 0, '20-30': 0, '30-50': 0, '50-100': 0}
    for e in ev:
        if e[1]:
            continue
        p = e[5]
        k = '10-20' if p <= .2 else '20-30' if p <= .3 else '30-50' if p <= .5 else '50-100'
        dist[k] += 1
    # 的中率
    def prec(S):
        f = [k for k in S if k in lab_map]
        return sum(lab_map[k] for k in f) / max(1, len(f)), len(f)
    p_g, n_g = prec(g10); p_s, n_s = prec(s10); p_u, n_u = prec(union); p_e, n_e = prec(gEq)
    # 国ブロックCI: 差(union - globalEq)
    byc_ev = defaultdict(list)
    for e in ev:
        byc_ev[e[0]].append(e)
    cl = sorted(byc_ev); rng2 = random.Random(122); ds = []
    for bb in range(1000):
        s = []
        for _ in range(len(cl)):
            s.extend(byc_ev[rng2.choice(cl)])
        if s:
            ds.append(sum(e[3] for e in s) / len(s) - sum(e[4] for e in s) / len(s))
    ds.sort(); n = len(ds)
    lo, hi = ds[int(.025 * n)], ds[int(.975 * n)]
    L = ['', f'SELFRANK-RESCUE 2026-07-20 (notes/46。自己相対120ヶ月百分位の第2スクリーン, onset{n_ev}件)',
         f'  記述: 世界q10見逃しの順位分布 10-20%={dist["10-20"]} / 20-30%={dist["20-30"]} / 30-50%={dist["30-50"]} / 50-100%={dist["50-100"]}',
         f'  捕捉率: 世界q10={cg/n_ev:.1%} / 自己q10={csf/n_ev:.1%} / 合体={cu/n_ev:.1%}(点灯{n_u}) / 世界q{int(qE*100)}(同予算{n_e})={ce/n_ev:.1%}',
         f'  自己スクリーンの救済: 世界q10が逃した{n_ev-cg}件のうち{rescued}件を拾う',
         f'  的中率: 世界q10={p_g:.1%} / 自己q10={p_s:.1%} / 合体={p_u:.1%} / 世界q{int(qE*100)}={p_e:.1%}',
         f'  主検定 差(合体-同予算世界)={cu/n_ev-ce/n_ev:+.3f} CI[{lo:+.3f},{hi:+.3f}]',
         f'  -> {"PASS: 自己相対は別軸として機能する" if lo > 0 else "FAIL: 中位圏は自己相対でも救えない(現行情報集合では救済不能として問いを閉じる)"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
