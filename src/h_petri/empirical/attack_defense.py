# -*- coding: utf-8 -*-
# ATTACK-DEFENSE (事前固定): 攻撃時点の月次準備(輸入月数)は生存を予測するか
# 「貯金無力」がデータの粗さか選択効果かの切り分け:
#   月次でも無力 → 選択効果(攻撃者が既に貯金を織り込んで標的選択)が濃厚
#   月次なら効く → 年次の粗さが原因だった
import csv, math, statistics, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from phase2_exp1_bis import auc, make_ecdf, fit_logistic
from attack_anatomy import load_fxm, build_emp_attacks, fx_crash_months


def main():
    fxm = load_fxm()
    attacks = build_emp_attacks(fxm)
    crash_m = {iso: fx_crash_months(fxm[iso]) for iso in fxm}

    res = defaultdict(dict)
    with open(ROOT / 'data_raw/il_reserves_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                res[row['iso3']][(int(y), int(m))] = float(row['reserves_usd'])
            except (ValueError, KeyError):
                continue
    # 年間輸入(imts_trade_xm: 相手別の輸入Mを合計)
    imports = defaultdict(lambda: defaultdict(float))
    with open(ROOT / 'data_raw/imts_trade_xm.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, xv, mv in r:
            try:
                imports[rep][int(yr)] += float(mv)
            except ValueError:
                continue
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
        # 攻撃直前月の準備(先読み防止: m-1)
        pi = y * 12 + m - 2
        r1 = res.get(iso, {}).get((pi // 12, pi % 12 + 1))
        imp = imports.get(iso, {}).get(y - 1)
        if not r1 or not imp or imp <= 0:
            continue
        rm = r1 / (imp / 12.0)   # 輸入月数
        if not math.isfinite(rm) or rm > 120:
            continue
        g = gg.get((iso, y - 1))
        w = trade.get(iso, {}).get(y - 1, {})
        tf = None
        if w and len(w) >= 3 and sum(w.values()) > 0:
            tf = sum(v for j, v in w.items() if (j, y - 1) in crash_ann) / sum(w.values())
        a0 = y * 12 + m - 1
        fell = 1 if any((i // 12, i % 12 + 1) in crash_m.get(iso, set()) for i in range(a0, a0 + 13)) else 0
        rows.append((iso, y, rm, g, tf, fell))

    n_fall = sum(r[5] for r in rows)
    L = ['', 'ATTACK-DEFENSE 2026-07-17 (攻撃直前月の準備[輸入月数]は生存を予測するか — 貯金無力の切り分け)',
         f'攻撃onset(月次準備+輸入あり) {len(rows)}件, 12ヶ月以内崩壊 {n_fall} ({n_fall/len(rows):.0%})']
    # RM単独(全サンプル)
    a_rm = auc([-r[2] for r in rows], [r[5] for r in rows])   # 月数少ない=危険 → 符号反転で「危険度」
    L.append(f'  準備の輸入月数(攻撃直前月, 少=危険): AUC={a_rm:.3f} (n={len(rows)})')
    # GG/TFが揃うサブサンプルで3つ巴
    sub = [r for r in rows if r[3] is not None and math.isfinite(r[3]) and r[4] is not None and math.isfinite(r[4])]
    if len(sub) > 100:
        a_rm2 = auc([-r[2] for r in sub], [r[5] for r in sub])
        a_gg = auc([r[3] for r in sub], [r[5] for r in sub])
        a_tf = auc([r[4] for r in sub], [r[5] for r in sub])
        data = [(r[0], r[1], -r[2], r[4], 0, r[5]) for r in sub]
        e_r = make_ecdf([d[2] for d in data]); e_t = make_ecdf([d[3] for d in data])
        sc, wg = fit_logistic(data, [2, 3], [e_r, e_t])
        a_j = auc([sc(d) for d in data], [d[5] for d in data])
        L.append(f'  同一サブサンプル(n={len(sub)}, 崩壊{sum(r[5] for r in sub)}): 月次準備={a_rm2:.3f} 年次GG={a_gg:.3f} TF={a_tf:.3f} | 準備+TF={a_j:.3f} 係数={["%.3f" % w for w in wg]}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
