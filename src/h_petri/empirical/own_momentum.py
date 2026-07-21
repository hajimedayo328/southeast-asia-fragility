# -*- coding: utf-8 -*-
# notes/49: 自国モメンタム(3ヶ月減価率) — 見逃しは「速い燃焼」かの定量化
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit, auc

Q = 0.10


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

    fxi = {c: {y * 12 + m - 1: v for (y, m), v in d.items()} for c, d in fxm.items()}

    def mom3(c, i):
        d = fxi.get(c, {})
        a = d.get(i); b = d.get(i - 3)
        if a is None or b is None or b <= 0:
            return None
        x = a / b - 1.0
        return max(-1.0, min(1.0, x))

    def build_rows(H):
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
                mo = mom3(c, i)
                if mo is None:
                    continue
                tf = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
                lab = 1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
                rows.append((c, i, g, tf, mo, lab))
        return rows

    L = ['', 'OWN-MOMENTUM 2026-07-20 (notes/49。自国3ヶ月減価率=速い燃焼の定量化。解釈警告つき: ナウキャストであり早期警報ではない)']
    rows = build_rows(6)
    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]

    # (i) 記述: onset前月のMOM3
    e_g = make_ecdf([r[2] for r in train]); e_t = make_ecdf([r[3] for r in train])
    pos = [r for r in train if r[5] == 1]; neg = [r for r in train if r[5] == 0]
    rng = random.Random(151)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    w0, b0 = fit_logit([[e_g(r[2]), e_t(r[3])] for r in sub], [r[5] for r in sub])
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
    H = 6
    for c, i0 in onsets_te:
        pcts = [gp[(c, j)] for j in range(i0 - H, i0) if (c, j) in gp]
        mo = mom3(c, i0 - 1)
        if not pcts or mo is None:
            continue
        best = min(pcts)
        key = 'caught' if best <= Q else ('miss_hi' if best <= 0.5 else 'miss_lo')
        grp[key].append(mo)
    base = [r[4] for r in test if r[5] == 0]
    base.sort()
    L.append(f'  (i) onset前月の自国3ヶ月減価率 (非onset月の基礎: 中央値{base[len(base)//2]:+.1%}, >5%率{sum(1 for x in base if x > .05)/len(base):.1%}, >10%率{sum(1 for x in base if x > .10)/len(base):.1%}):')
    for k, nm in (('caught', '捕捉(q10)'), ('miss_hi', '見逃し·順位10-50%'), ('miss_lo', '見逃し·順位下半分')):
        g = sorted(grp[k])
        if g:
            L.append(f'    {nm}: n={len(g)} 中央値{g[len(g)//2]:+.1%} >5%={sum(1 for x in g if x > .05)/len(g):.0%} >10%={sum(1 for x in g if x > .10)/len(g):.0%}')

    # (ii) AUC検定 h=6, h=3
    for H2 in (6, 3):
        rows2 = build_rows(H2)
        tr = [r for r in rows2 if r[1] < 2000 * 12]
        te = [r for r in rows2 if r[1] >= 2000 * 12]

        def build(feats, seed):
            ecs = [make_ecdf([r[f] for r in tr]) for f in feats]
            p2 = [r for r in tr if r[5] == 1]; n2 = [r for r in tr if r[5] == 0]
            rng2 = random.Random(seed)
            sub2 = p2 + rng2.sample(n2, min(len(n2), 5 * len(p2)))
            X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub2]
            w, b = fit_logit(X, [r[5] for r in sub2])
            return (lambda r: b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))), w
        s1, _ = build([2, 3], 152)
        s2, w2 = build([2, 3, 4], 152)
        y_te = [r[5] for r in te]
        a1 = auc([s1(r) for r in te], y_te)
        a2 = auc([s2(r) for r in te], y_te)
        byc = defaultdict(list)
        for r in te:
            byc[r[0]].append(r)
        cl = sorted(byc); rng3 = random.Random(153); ds = []
        for bb in range(300):
            s = []
            for _ in range(len(cl)):
                s.extend(byc[rng3.choice(cl)])
            yv = [r[5] for r in s]
            v1 = auc([s1(r) for r in s], yv); v2 = auc([s2(r) for r in s], yv)
            if v1 is not None and v2 is not None:
                ds.append(v2 - v1)
        ds.sort(); n = len(ds)
        d = a2 - a1
        L.append(f'  (ii) h={H2}: GG+TF={a1:.4f} +MOM3={a2:.4f} delta={d:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] 係数={["%.2f" % x for x in w2]}{" (バー通過だが解釈警告どおりナウキャスト)" if ds[int(.025*n)] > 0 and d >= 0.03 else ""}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
