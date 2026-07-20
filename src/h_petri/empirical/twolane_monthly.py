# -*- coding: utf-8 -*-
# 二車線警報の月次統合リスト (2026-07固定・答え合わせプロトコル付き)
# 定義(実行前固定): 赤=車線内上位10% / 二重赤=両車線とも上位20%
# 崩壊車線 = GG+TF_m (monthly_nowcast同構成・全履歴学習) / 攻撃車線 = RM(準備の輸入月数)昇順
# 答え合わせ: 2027-07-31までに月次crashルールのonsetが出たかで機械判定(docs/data/nowcast_monthly_2026_07.json)
import csv, json, math, random, sys
from collections import defaultdict
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
    rows_j = json.load(open(ROOT / 'docs/data/panel_raw/st_debt_reserves_latest.json', encoding='utf-8'))
    gg = {}
    for r in rows_j:
        iso = r.get('countryiso3code')
        if iso in real and r.get('value') is not None:
            gg[(iso, int(r['date']))] = float(r['value']) / 100
    trade = defaultdict(lambda: defaultdict(dict))
    imports = defaultdict(lambda: defaultdict(float))
    with open(ROOT / 'data_raw/imts_trade_xm.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, xv, mv in r:
            try:
                y = int(yr); x = float(xv); mm = float(mv)
            except ValueError:
                continue
            imports[rep][y] += mm
            v = x + mm
            if v > 0:
                trade[rep][y][cp] = v
    res = defaultdict(dict)
    with open(ROOT / 'data_raw/il_reserves_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                res[row['iso3']][int(y) * 12 + int(m) - 1] = float(row['reserves_usd'])
            except (ValueError, KeyError):
                continue

    def weights(c, y):
        for yy in (y - 1, y - 2):
            w = trade.get(c, {}).get(yy, {})
            tot = sum(w.values())
            if len(w) >= 3 and tot > 0:
                return {j: v / tot for j, v in w.items()}
        return None

    # 崩壊車線モデル(全履歴学習・monthly_nowcastと同構成)
    H = 6
    hist = []
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
            hist.append((c, i, g, tf, lab))
    e_g = make_ecdf([r[2] for r in hist])
    e_t = make_ecdf([r[3] for r in hist])
    pos = [r for r in hist if r[4] == 1]
    neg = [r for r in hist if r[4] == 0]
    rng = random.Random(111)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    w, b = fit_logit([[e_g(r[2]), e_t(r[3])] for r in sub], [r[4] for r in sub])

    # 現在値(最新月・12ヶ月以内のデータのみ)
    cand = {}
    for c in sorted({c for (c, y_) in gg if y_ >= 2023}):
        fxd = fxm.get(c)
        if not fxd:
            continue
        latest = sorted(fxd)[-1]
        i = latest[0] * 12 + latest[1] - 1
        if i < 2026 * 12 - 12 or i in crash_idx.get(c, set()):
            continue
        y = i // 12
        g = gg.get((c, y - 1)) or gg.get((c, y - 2))
        W = weights(c, y)
        if g is None or W is None or not math.isfinite(g):
            continue
        tf = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
        col = b + w[0] * e_g(g) + w[1] * e_t(tf)
        # 攻撃車線: 最新の準備 / 前年輸入月平均
        rm = None
        rmon = res.get(c, {})
        if rmon:
            im = max(k for k in rmon if k <= i) if any(k <= i for k in rmon) else None
            imp = imports.get(c, {}).get(y - 1)
            if im is not None and im >= i - 12 and imp and imp > 0:
                rm = rmon[im] / (imp / 12.0)
        cand[c] = {'collapse_score': col, 'gg': g, 'tf': tf, 'rm_months': rm,
                   'asof': f'{latest[0]}-{latest[1]:02d}'}

    cs = sorted(cand, key=lambda c: -cand[c]['collapse_score'])
    for k, c in enumerate(cs):
        cand[c]['collapse_rank_pct'] = k / len(cs)
    rms = [c for c in cand if cand[c]['rm_months'] is not None]
    rms.sort(key=lambda c: cand[c]['rm_months'])
    for k, c in enumerate(rms):
        cand[c]['attack_rank_pct'] = k / len(rms)

    RED, DUAL = 0.10, 0.20
    col_red = [c for c in cs if cand[c]['collapse_rank_pct'] <= RED]
    atk_red = [c for c in rms if cand[c]['attack_rank_pct'] <= RED]
    dual = [c for c in cs if cand[c]['collapse_rank_pct'] <= DUAL
            and cand[c].get('attack_rank_pct', 1) <= DUAL]
    out = {
        'fixed_on': '2026-07-20',
        'definitions': {
            'collapse_lane': 'GG+TF_m ECDF logistic (trained on full 1978-2024 history), rank pct among candidates',
            'attack_lane': 'reserves months of prior-year imports (monthly IL), ascending rank pct',
            'red': 'lane rank pct <= 0.10', 'dual_red': 'both lanes rank pct <= 0.20',
            'judgment': 'For each listed country: crash onset (12m-30%+10pp monthly rule, established codebase) '
                        'occurring within 12 months of its asof month = HIT. Judge on/after 2027-08-01 with same code.',
        },
        'n_candidates': {'collapse': len(cs), 'attack': len(rms)},
        'collapse_red': [{'iso': c, 'name': meta[c]['name'], **{k: v for k, v in cand[c].items()}} for c in col_red],
        'attack_red': [{'iso': c, 'name': meta[c]['name'], **{k: v for k, v in cand[c].items()}} for c in atk_red],
        'dual_red': [{'iso': c, 'name': meta[c]['name'], **{k: v for k, v in cand[c].items()}} for c in dual],
    }
    path = ROOT / 'docs/data/nowcast_monthly_2026_07.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    L = ['', 'TWOLANE-MONTHLY 2026-07-20 (二車線の月次統合。赤=上位10%/二重赤=両車線20%。答え合わせはJSONのルールで2027-08以降に機械判定)',
         f'  対象: 崩壊{len(cs)}カ国 / 攻撃{len(rms)}カ国。正本: docs/data/nowcast_monthly_2026_07.json',
         f'  崩壊赤({len(col_red)}): ' + ', '.join(f"{meta[c]['name'][:12]}" for c in col_red),
         f'  攻撃赤({len(atk_red)}): ' + ', '.join(f"{meta[c]['name'][:12]}({cand[c]['rm_months']:.1f}ヶ月)" for c in atk_red),
         f'  二重赤({len(dual)}): ' + (', '.join(f"{meta[c]['name'][:12]}" for c in dual) if dual else 'なし')]
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
