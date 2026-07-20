# -*- coding: utf-8 -*-
# 月次警報の現在リスト (MONTHLY-MIGRATION合格を受けて。最新月の特徴量→向こう6ヶ月の警戒順位)
import csv, math, random, sys
from collections import defaultdict
from bisect import bisect_right
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit


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
    gg_latest = {}
    import json
    rows_j = json.load(open(ROOT / 'docs/data/panel_raw/st_debt_reserves_latest.json', encoding='utf-8'))
    gg = {}
    for r in rows_j:
        iso = r.get('countryiso3code')
        if iso in real and r.get('value') is not None:
            gg[(iso, int(r['date']))] = float(r['value']) / 100
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

    def weights(c, y):
        for yy in (y - 1, y - 2):
            w = trade.get(c, {}).get(yy, {})
            if len(w) >= 3 and sum(w.values()) > 0:
                tot = sum(w.values())
                return {j: v / tot for j, v in w.items()}
        return None

    # 学習(全履歴, h=6, 月次TF) — migrationスクリプトと同一構成の簡略再現
    H = 6
    rows = []
    for c in sorted({c for (c, _) in gg}):
        fxd = fxm.get(c)
        if not fxd:
            continue
        for i in range(1978 * 12, 2025 * 12):
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
    e_g = make_ecdf([r[2] for r in rows])
    e_t = make_ecdf([r[3] for r in rows])
    pos = [r for r in rows if r[4] == 1]
    neg = [r for r in rows if r[4] == 0]
    rng = random.Random(51)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    X = [[e_g(r[2]), e_t(r[3])] for r in sub]
    Y = [r[4] for r in sub]
    w, b = fit_logit(X, Y)
    print(f'fit on {len(rows)} rows (weights {w[0]:.2f},{w[1]:.2f})')

    # 現在(データのある最新月)のスコア
    cand = []
    for c in sorted({c for (c, y_) in gg if y_ >= 2023}):
        fxd = fxm.get(c)
        if not fxd:
            continue
        months = sorted(fxd)
        latest = months[-1]
        i = latest[0] * 12 + latest[1] - 1
        if i < 2026 * 12 - 12 or i in crash_idx.get(c, set()):
            continue
        y = i // 12
        g = gg.get((c, y - 1)) or gg.get((c, y - 2))
        W = weights(c, y)
        if g is None or W is None or not math.isfinite(g):
            continue
        tf = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
        s = b + w[0] * e_g(g) + w[1] * e_t(tf)
        burning = sorted([(v, j) for j, v in W.items() if i in crash_idx.get(j, set())], reverse=True)[:2]
        cand.append((s, c, g, tf, latest, [j for _, j in burning]))
    cand.sort(reverse=True)
    L = ['', 'MONTHLY-NOWCAST 2026-07-20 (月次警報の初回リスト: 最新月データ→向こう6ヶ月の警戒順位)',
         f'対象 {len(cand)}カ国 上位12:']
    for i, (s, c, g, tf, latest, burn) in enumerate(cand[:12]):
        nm = meta[c]['name'][:18]
        bs = '+'.join(burn) if burn else '-'
        L.append(f'  {i+1:2d} {nm:18s} GG={g:5.2f} 火事={tf*100:5.1f}% (主火元:{bs}) 時点{latest[0]}-{latest[1]:02d}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
