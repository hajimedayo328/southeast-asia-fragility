# -*- coding: utf-8 -*-
# notes/43: EXP-A 警報の運用解剖(記述) / EXP-B 余震仮説(事前登録)
import csv, math, random, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit, auc

REC_CAP = 240


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

    sorted_crash = {c: sorted(s) for c, s in crash_idx.items()}
    from bisect import bisect_left

    def recency(c, i):
        s = sorted_crash.get(c)
        if not s:
            return REC_CAP
        p = bisect_left(s, i)
        if p == 0:
            return REC_CAP
        return min(REC_CAP, i - s[p - 1])

    H = 6
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
            rec = recency(c, i)
            lab = 1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, H + 1)) else 0
            rows.append((c, i, g, tf, -rec, lab))   # RECは少=危険 -> 符号反転
    train = [r for r in rows if r[1] < 2000 * 12]
    test = [r for r in rows if r[1] >= 2000 * 12]

    def build(feats, seed):
        ecs = [make_ecdf([r[f] for r in train]) for f in feats]
        pos = [r for r in train if r[5] == 1]
        neg = [r for r in train if r[5] == 0]
        rng = random.Random(seed)
        sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
        X = [[ecs[j](r[f]) for j, f in enumerate(feats)] for r in sub]
        w, b = fit_logit(X, [r[5] for r in sub])
        return (lambda r: b + sum(wj * ecs[j](r[f]) for j, (wj, f) in enumerate(zip(w, feats)))), w

    L = ['', f'ALARM-OPS+RECENCY 2026-07-20 (notes/43。h={H}, panel={len(rows)})']

    # ---- EXP-A: 運用解剖 (基準モデル GG+TF) ----
    s_base, _ = build([2, 3], 95)
    bym = defaultdict(list)
    for r in test:
        bym[r[1]].append((s_base(r), r[0]))
    rank_pct = {}
    for i, lst in bym.items():
        lst.sort(reverse=True)
        n = len(lst)
        for p_, (s, c) in enumerate(lst):
            rank_pct[(c, i)] = p_ / n
    onsets_te = [(c, i0) for c, s in onset_idx.items() for i0 in s
                 if 2000 * 12 <= i0 < 2025 * 12]
    QS = (0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50)
    # 捕捉率
    L.append('EXP-A(1) 枠と捕捉のトレードオフ:')
    catch = {q: 0 for q in QS}
    n_sc = 0
    lead = []
    for c, i0 in onsets_te:
        pre = [(c, j) for j in range(i0 - H, i0)]
        pcts = [(rank_pct[k], i0 - k[1]) for k in pre if k in rank_pct]
        if not pcts:
            continue
        n_sc += 1
        best = min(p for p, _ in pcts)
        for q in QS:
            if best <= q:
                catch[q] += 1
        fires10 = [m for p, m in pcts if p <= 0.10]
        if fires10:
            lead.append(max(fires10))   # 最初の点灯(=最も早い月)
    # 誤警報コスト: 点灯国月のうちlabel=0だった率 + 常連集中度
    for q in QS:
        flagged = [r for r in test if rank_pct.get((r[0], r[1]), 1) <= q]
        fa = [r for r in flagged if r[5] == 0]
        prec = 1 - len(fa) / max(1, len(flagged))
        L.append(f'  q{int(q*100):2d}: 捕捉 {catch[q]}/{n_sc}={catch[q]/n_sc:.1%}  点灯国月={len(flagged)}  的中率={prec:.1%}')
    lead.sort()
    med = lead[len(lead) // 2] if lead else None
    dist = {m: sum(1 for x in lead if x == m) for m in range(1, H + 1)}
    L.append(f'EXP-A(2) リードタイム(q10捕捉{len(lead)}件): 中央値={med}ヶ月, 分布(1..6ヶ月前)={[dist.get(m,0) for m in range(1,H+1)]}')
    fa10 = [r for r in test if rank_pct.get((r[0], r[1]), 1) <= 0.10 and r[5] == 0]
    byc_fa = defaultdict(int)
    for r in fa10:
        byc_fa[r[0]] += 1
    top5 = sorted(byc_fa.items(), key=lambda x: -x[1])[:5]
    share = sum(v for _, v in top5) / max(1, len(fa10))
    L.append(f'EXP-A(3) 誤警報の常連集中(q10): 誤警報{len(fa10)}国月のうち上位5カ国={share:.0%} ({[(meta[c]["name"][:10], v) for c, v in top5]})')

    # ---- EXP-B: 余震仮説 ----
    s1, _ = build([2, 3], 96)
    s2, w2 = build([2, 3, 4], 96)
    y_te = [r[5] for r in test]
    a1 = auc([s1(r) for r in test], y_te)
    a2 = auc([s2(r) for r in test], y_te)
    byc = defaultdict(list)
    for r in test:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(97); ds = []
    for b in range(300):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        yv = [r[5] for r in s]
        v1 = auc([s1(r) for r in s], yv); v2 = auc([s2(r) for r in s], yv)
        if v1 is not None and v2 is not None:
            ds.append(v2 - v1)
    ds.sort(); n = len(ds)
    d = a2 - a1
    L.append(f'EXP-B主検定(余震=自国履歴REC): GG+TF={a1:.4f} +REC={a2:.4f} delta={d:+.4f} CI[{ds[int(.025*n)]:+.4f},{ds[int(.975*n)]:+.4f}] 係数={["%.2f" % x for x in w2]}')
    L.append(f'  -> {"PASS: 警報の第3の材料" if ds[int(.025*n)] > 0 and d >= 0.03 else "FAIL"}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
