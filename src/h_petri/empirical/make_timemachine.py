# -*- coding: utf-8 -*-
# タイムマシン用データ前計算 -> docs/data/timemachine.json
# 警報モデルは1999年末で凍結(それ以前はin-sample・UIに明記)。各月は当月データのみ参照
import csv, json, math, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, fx_crash_months
from monthly_migration import make_ecdf, fit_logit
from monthly_gsi_addon import build_gsi

JP = {'ARG': 'アルゼンチン', 'BRA': 'ブラジル', 'MEX': 'メキシコ', 'TUR': 'トルコ',
      'RUS': 'ロシア', 'IDN': 'インドネシア', 'IND': 'インド', 'CHN': '中国',
      'EGY': 'エジプト', 'NGA': 'ナイジェリア', 'ZAF': '南アフリカ', 'LKA': 'スリランカ',
      'PAK': 'パキスタン', 'BGD': 'バングラデシュ', 'VEN': 'ベネズエラ', 'BOL': 'ボリビア',
      'BLR': 'ベラルーシ', 'UKR': 'ウクライナ', 'KAZ': 'カザフスタン', 'DJI': 'ジブチ',
      'ETH': 'エチオピア', 'GHA': 'ガーナ', 'ZWE': 'ジンバブエ', 'LBN': 'レバノン',
      'COL': 'コロンビア', 'CHL': 'チリ', 'PER': 'ペルー', 'ECU': 'エクアドル',
      'MYS': 'マレーシア', 'PHL': 'フィリピン', 'VNM': 'ベトナム', 'MMR': 'ミャンマー'}


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
    for r in json.load(open(ROOT / 'docs/data/panel_raw/st_debt_reserves_latest.json', encoding='utf-8')):
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
    wcache = {}

    def weights(c, y):
        key = (c, y)
        if key not in wcache:
            for yy in (y - 1, y - 2):
                w = trade.get(c, {}).get(yy, {})
                tot = sum(w.values())
                if len(w) >= 3 and tot > 0:
                    wcache[key] = {j: v / tot for j, v in w.items()}
                    break
            else:
                wcache[key] = None
        return wcache[key]

    # 特徴量とラベル(学習用)
    feat = {}
    for c in sorted({c for (c, _) in gg}):
        fxd = fxm.get(c)
        if not fxd:
            continue
        for i in range(1978 * 12, 2026 * 12 + 6):
            y = i // 12; m = i % 12 + 1
            if (y, m) not in fxd:
                continue
            g = gg.get((c, y - 1)) or gg.get((c, y - 2))
            if g is None or not math.isfinite(g):
                continue
            W = weights(c, y)
            if W is None:
                continue
            tf = sum(v for j, v in W.items() if i in crash_idx.get(j, set()))
            burn = sorted(((v, j) for j, v in W.items() if i in crash_idx.get(j, set())), reverse=True)
            feat[(c, i)] = (g, tf, burn[0][1] if burn else None)
    train = [(c, i, g, tf) for (c, i), (g, tf, _) in feat.items()
             if i < 2000 * 12 and i not in crash_idx.get(c, set())]
    lab = [1 if any((i + k) in onset_idx.get(c, set()) for k in range(1, 7)) else 0
           for (c, i, g, tf) in train]
    e_g = make_ecdf([r[2] for r in train]); e_t = make_ecdf([r[3] for r in train])
    pos = [(r, l) for r, l in zip(train, lab) if l == 1]
    neg = [(r, l) for r, l in zip(train, lab) if l == 0]
    rng = random.Random(171)
    sub = pos + rng.sample(neg, min(len(neg), 5 * len(pos)))
    w, b = fit_logit([[e_g(r[2]), e_t(r[3])] for r, _ in sub], [l for _, l in sub])

    gsi = build_gsi()
    months = []
    i0, i1 = 1978 * 12, max(i for (_, i) in feat) + 1
    isos = sorted({c for (c, _) in feat} | {c for c in crash_idx if any(i0 <= i < i1 for i in crash_idx[c])})
    iso_ix = {c: k for k, c in enumerate(isos)}
    states = []; top = {}; gsi_out = []
    for i in range(i0, i1):
        y = i // 12; m = i % 12 + 1
        key = f'{y}-{m:02d}'
        months.append(key)
        q = (m - 1) // 3 + 1
        pq = (y, q - 1) if q > 1 else (y - 1, 4)
        gsi_out.append(round(gsi.get(pq, 0), 2) if gsi.get(pq) is not None else None)
        scored = []
        row = ['.'] * len(isos)
        for c in isos:
            if i in crash_idx.get(c, set()):
                row[iso_ix[c]] = 'X'
            elif (c, i) in feat:
                g, tf, bp = feat[(c, i)]
                s = b + w[0] * e_g(g) + w[1] * e_t(tf)
                scored.append((s, c, g, tf, bp))
        scored.sort(reverse=True)
        n = len(scored)
        tops = []
        for k, (s, c, g, tf, bp) in enumerate(scored):
            d = min(9, int(10 * k / max(1, n)))
            row[iso_ix[c]] = str(d)
            if d == 0:
                tops.append([c, round(g, 2), round(tf * 100, 1), bp])
        states.append(''.join(row))
        top[key] = tops
    out = {
        'note': '警報モデル(帳簿GG+貿易火事TF)は1999年末までのデータで学習し凍結。2000年以降は真の未知。各月の色はその月に入手可能な情報のみで計算。灰色=データ不足で採点不能(タイ・韓国など短期債務データの無い国を含む)',
        'months': months, 'isos': isos,
        'names': {c: meta.get(c, {}).get('name', c) for c in isos},
        'jp': {c: JP[c] for c in isos if c in JP},
        'region': {c: meta.get(c, {}).get('region', {}).get('value', '?') for c in isos},
        'states': states,
        'onsets': {c: [f'{i//12}-{i%12+1:02d}' for i in sorted(onset_idx.get(c, set())) if i0 <= i < i1]
                   for c in isos if onset_idx.get(c)},
        'gsi': gsi_out, 'top': top,
    }
    p = ROOT / 'docs/data/timemachine.json'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'{p} written: {p.stat().st_size//1024} KB, {len(months)} months, {len(isos)} countries')


if __name__ == '__main__':
    main()
