# -*- coding: utf-8 -*-
# notes/50 A+B: 月次移行のFR_25_10頑健性 + 検知層(速い燃焼)の運用計測
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm
from monthly_migration import make_ecdf, fit_logit, auc

H = 6
Q = 0.10


def crash_months_rule(d, DEP, ACC):
    c = set()
    for (y, m) in sorted(d):
        def back(k):
            i = y * 12 + m - 1 - k
            return d.get((i // 12, i % 12 + 1))
        cur = d[(y, m)]; p1 = back(12); p2 = back(24)
        if p1 and p1 > 0 and p2 and p2 > 0:
            dep = cur / p1 - 1; dp = p1 / p2 - 1
            if dep >= DEP and dep - dp >= ACC:
                c.add((y, m))
    return c


def build(fxm, gg, weights, crash_idx, onset_idx):
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
            dec = (y - 1) * 12 + 11
            tf_st = sum(v for j, v in W.items() if dec in crash_idx.get(j, set()))
            lab = 1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
            rows.append((c, i, g, tf, tf_st, lab))
    return rows


def main():
    fxm = load_fxm()
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

    L = ['', 'HARDENING-BATCH 2026-07-22 (notes/50 A+B)']
    # ---- A: FR_25_10頑健性 ----
    crash_fr = {iso: crash_months_rule(fxm[iso], 0.25, 0.10) for iso in fxm}
    crash_idx = {iso: {y * 12 + m - 1 for (y, m) in cr} for iso, cr in crash_fr.items()}
    onset_idx = defaultdict(set)
    for iso, cr in crash_fr.items():
        idxs = {y * 12 + m - 1 for (y, m) in cr}
        for (y, m) in sorted(cr):
            i = y * 12 + m - 1
            if not any((i - k) in idxs for k in range(1, 13)):
                onset_idx[iso].add(i)
    rows = build(fxm, gg, weights, crash_idx, onset_idx)
    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]

    def fit2(feats, seed):
        ecs = [make_ecdf([r[f] for r in train]) for f in feats]
        p2 = [r for r in train if r[5] == 1]; n2 = [r for r in train if r[5] == 0]
        rng = random.Random(seed)
        sub = p2 + rng.sample(n2, min(len(n2), 5 * len(p2)))
        X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub]
        w, b = fit_logit(X, [r[5] for r in sub])
        return lambda r: b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))
    s_fr = fit2([2, 3], 161); s_st = fit2([2, 4], 161)
    y_te = [r[5] for r in test]
    a_fr = auc([s_fr(r) for r in test], y_te)
    a_st = auc([s_st(r) for r in test], y_te)
    byc = defaultdict(list)
    for r in test:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(162); ds = []
    for bb in range(300):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        yv = [r[5] for r in s]
        v1 = auc([s_fr(r) for r in s], yv); v2 = auc([s_st(r) for r in s], yv)
        if v1 is not None and v2 is not None:
            ds.append(v1 - v2)
    ds.sort(); n = len(ds)
    L.append(f'A(FR_25_10頑健性): panel={len(rows)} positives={sum(y_te)} 鮮度={a_fr:.4f} vs 凍結={a_st:.4f} Δ={a_fr-a_st:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] -> {"PASS: 月次化の利得はルール非依存" if ds[int(.025*n)] > 0 else "FAIL: ルール特異的"}')

    # ---- B: 検知層の運用計測 (LV_30_10の既定ルールで) ----
    from attack_anatomy import fx_crash_months
    crash_lv = {iso: fx_crash_months(fxm[iso]) for iso in fxm}
    crash_idx2 = {iso: {y * 12 + m - 1 for (y, m) in cr} for iso, cr in crash_lv.items()}
    onset2 = defaultdict(set)
    for iso, cr in crash_lv.items():
        idxs = {y * 12 + m - 1 for (y, m) in cr}
        for (y, m) in sorted(cr):
            i = y * 12 + m - 1
            if not any((i - k) in idxs for k in range(1, 13)):
                onset2[iso].add(i)
    rows2 = build(fxm, gg, weights, crash_idx2, onset2)
    tr2 = [r for r in rows2 if r[1] < 2000 * 12]
    te2 = [r for r in rows2 if r[1] >= 2000 * 12]
    e_g = make_ecdf([r[2] for r in tr2]); e_t = make_ecdf([r[3] for r in tr2])
    p2 = [r for r in tr2 if r[5] == 1]; n2_ = [r for r in tr2 if r[5] == 0]
    rng2 = random.Random(163)
    sub = p2 + rng2.sample(n2_, min(len(n2_), 5 * len(p2)))
    w0, b0 = fit_logit([[e_g(r[2]), e_t(r[3])] for r in sub], [r[5] for r in sub])
    bym = defaultdict(list)
    for r in te2:
        bym[r[1]].append((b0 + w0[0] * e_g(r[2]) + w0[1] * e_t(r[3]), r[0]))
    slow = set()
    for i, lst in bym.items():
        lst.sort(reverse=True)
        nn = len(lst)
        for k, (s, c) in enumerate(lst):
            if k / nn <= Q:
                slow.add((c, i))
    fxi = {c: {y * 12 + m - 1: v for (y, m), v in d.items()} for c, d in fxm.items()}

    def mom3(c, i):
        d = fxi.get(c, {})
        a = d.get(i); b = d.get(i - 3)
        if a is None or b is None or b <= 0:
            return None
        return a / b - 1.0
    onsets_te = [(c, i0) for c, s in onset2.items() for i0 in s
                 if 2000 * 12 <= i0 < 2025 * 12]
    for THR in (0.05, 0.10):
        det = 0; leads = []; n_ons = 0
        for c, i0 in onsets_te:
            ms = [(j, mom3(c, i0 - j)) for j in range(1, 13)]
            ms = [(lead, v) for lead, v in ms if v is not None]
            if not ms:
                continue
            n_ons += 1
            fired = [lead for lead, v in ms if v > THR]
            if fired:
                det += 1
                leads.append(max(fired))
        leads.sort()
        med = leads[len(leads) // 2] if leads else None
        # 負担と的中(panel国月ベース, 非危機月のみ=rows2がそう)
        fires = [r for r in te2 if (mom3(r[0], r[1]) or 0) > THR]
        prec = sum(r[5] for r in fires) / max(1, len(fires))
        L.append(f'B(検知層 MOM3>{int(THR*100)}%): 検知率={det}/{n_ons}={det/max(1,n_ons):.0%} 初点灯リード中央値={med}ヶ月 点灯率={len(fires)/len(te2):.1%} 的中率={prec:.1%}')
    # 二層合算 (>5%)
    det2 = 0; n_ons2 = 0
    for c, i0 in onsets_te:
        pre_slow = any((c, j) in slow for j in range(i0 - H, i0))
        ms = [mom3(c, i0 - j) for j in range(1, 13)]
        pre_fast = any(v is not None and v > 0.05 for v in ms)
        if not any((c, j) in bym and True for j in range(i0 - H, i0)):
            pass
        pcts_exist = any((c, j) in slow or any(x[1] == c for x in bym.get(j, [])) for j in range(i0 - H, i0))
        if not pcts_exist and not any(v is not None for v in ms):
            continue
        n_ons2 += 1
        if pre_slow or pre_fast:
            det2 += 1
    burden = len({k for k in slow} | {(r[0], r[1]) for r in te2 if (mom3(r[0], r[1]) or 0) > 0.05})
    L.append(f'B(二層合算 遅q10 OR 速>5%): 検知率={det2}/{n_ons2}={det2/max(1,n_ons2):.0%} 合算点灯国月={burden}({burden/len(te2):.1%})')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
