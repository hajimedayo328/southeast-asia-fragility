# -*- coding: utf-8 -*-
# notes/44: EXP-A リードタイム完全版(窓24ヶ月・記述) / EXP-B 新規点灯vs慢性点灯(事前登録)
import csv, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit

H = 6
Q = 0.10
WIN = 24


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
    rng = random.Random(95)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    w, b = fit_logit([[e_g(r[2]), e_t(r[3])] for r in sub], [r[4] for r in sub])

    # ランキングは1996年以降(streak/24ヶ月窓の履歴用にtest開始より前から)
    bym = defaultdict(list)
    for r in rows:
        if r[1] >= 1996 * 12:
            bym[r[1]].append((b + w[0] * e_g(r[2]) + w[1] * e_t(r[3]), r[0]))
    lit = set()
    for i, lst in bym.items():
        lst.sort(reverse=True)
        n = len(lst)
        for p_, (s, c) in enumerate(lst):
            if p_ / n <= Q:
                lit.add((c, i))

    # EXP-A: リード分布(窓24ヶ月)
    onsets_te = [(c, i0) for c, s in onset_idx.items() for i0 in s
                 if 2000 * 12 <= i0 < 2025 * 12]
    leads = []; full_chronic = 0; shares = []
    n_sc = 0
    for c, i0 in onsets_te:
        months = [(c, j) for j in range(i0 - WIN, i0)]
        obs = [k for k in months if k[1] in bym and any(x[1] == c for x in bym[k[1]])]
        if len(obs) < 12:
            continue
        n_sc += 1
        lits = [i0 - k[1] for k in months if k in lit]
        if not lits:
            continue
        leads.append(max(lits))
        shares.append(len(lits) / len(obs))
        if len(lits) >= len(obs):
            full_chronic += 1
    leads.sort()
    med = leads[len(leads) // 2] if leads else None
    hist = {'1-6': 0, '7-12': 0, '13-18': 0, '19-24': 0}
    for x in leads:
        hist['1-6' if x <= 6 else '7-12' if x <= 12 else '13-18' if x <= 18 else '19-24'] += 1
    shares.sort()
    med_share = shares[len(shares) // 2] if shares else None
    L = ['', f'LEADTIME+NOVELTY 2026-07-20 (notes/44。q10, 窓{WIN}ヶ月)',
         f'EXP-A: 判定対象onset {n_sc}件, 点灯あり{len(leads)}件(捕捉{len(leads)/n_sc:.0%})',
         f'  最初の点灯リード: 中央値={med}ヶ月, 分布(1-6/7-12/13-18/19-24)={list(hist.values())}, 24ヶ月全点灯={full_chronic}件',
         f'  点灯月数シェア中央値={med_share:.0%}']

    # EXP-B: 新規(streak<=3) vs 慢性(streak>=12)
    streak = {}
    for c, i in sorted(lit, key=lambda k: k[1]):
        streak[(c, i)] = streak.get((c, i - 1), 0) + 1
    lab_map = {(r[0], r[1]): r[4] for r in rows}
    groups = {'new': [], 'mid': [], 'chronic': []}
    for (c, i) in lit:
        if i < 2000 * 12 or (c, i) not in lab_map:
            continue
        s = streak[(c, i)]
        g = 'new' if s <= 3 else ('chronic' if s >= 12 else 'mid')
        groups[g].append((c, lab_map[(c, i)]))
    p_new = sum(l for _, l in groups['new']) / max(1, len(groups['new']))
    p_chr = sum(l for _, l in groups['chronic']) / max(1, len(groups['chronic']))
    p_mid = sum(l for _, l in groups['mid']) / max(1, len(groups['mid']))
    byc = defaultdict(lambda: {'new': [], 'chronic': []})
    for gname in ('new', 'chronic'):
        for c, l in groups[gname]:
            byc[c][gname].append(l)
    cl = sorted(byc); rng2 = random.Random(99); ds = []
    for bb in range(1000):
        aN = []; aC = []
        for _ in range(len(cl)):
            cc = rng2.choice(cl)
            aN.extend(byc[cc]['new']); aC.extend(byc[cc]['chronic'])
        if aN and aC:
            ds.append(sum(aN) / len(aN) - sum(aC) / len(aC))
    ds.sort(); n = len(ds)
    lo, hi = ds[int(.025 * n)], ds[int(.975 * n)]
    L.append(f'EXP-B: 新規点灯(streak<=3) n={len(groups["new"])} 的中率={p_new:.1%} / 中間(4-11) n={len(groups["mid"])} {p_mid:.1%} / 慢性(>=12) n={len(groups["chronic"])} {p_chr:.1%}')
    L.append(f'  主検定 差(新規-慢性)={p_new-p_chr:+.3f} CI[{lo:+.3f},{hi:+.3f}]')
    if lo > 0:
        L.append('  -> PASS: 新しい赤ほど危ない(点灯の変化を重視すべき)')
    elif hi < 0:
        L.append('  -> 逆符号で確定: 慢性ほど危ない(点きっぱなし=長い前兆であり止まった時計ではない)')
    else:
        L.append('  -> 差なし: 点灯の鮮度に情報なし')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
