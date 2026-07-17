# -*- coding: utf-8 -*-
# CRISIS-TAXONOMY (事前固定): 崩壊型(FX)と攻撃型(EMP)の解剖
# 分類: 両者が±6ヶ月以内=重複型 / FXのみ=じわ崩壊型 / EMPのみ=攻撃型
# 問い(事前固定): (i)時代ミックスの変化 (ii)所得階層の勾配 (iii)国の「型」の持続性
import csv, math, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, build_emp_attacks, fx_crash_months


def main():
    fxm = load_fxm()
    attacks = build_emp_attacks(fxm)
    fx_on = []
    for iso in fxm:
        cr = fx_crash_months(fxm[iso])
        idxs = {y * 12 + m - 1 for (y, m) in cr}
        for (y, m) in sorted(cr):
            if not any((y * 12 + m - 1 - k) in idxs for k in range(1, 13)):
                fx_on.append((iso, y, m))
    att_idx = defaultdict(set)
    for iso, y, m in attacks:
        att_idx[iso].add(y * 12 + m - 1)
    fx_idx = defaultdict(set)
    for iso, y, m in fx_on:
        fx_idx[iso].add(y * 12 + m - 1)

    def near(idxset, i, w=6):
        return any((i + k) in idxset for k in range(-w, w + 1))

    events = []   # (iso, year, type)
    for iso, y, m in fx_on:
        i = y * 12 + m - 1
        events.append((iso, y, 'overlap' if near(att_idx.get(iso, set()), i) else 'collapse'))
    for iso, y, m in attacks:
        i = y * 12 + m - 1
        if not near(fx_idx.get(iso, set()), i):
            events.append((iso, y, 'attack'))
    n_by = defaultdict(int)
    for _, _, t in events:
        n_by[t] += 1
    meta = fp.load_real_countries()

    L = ['', 'CRISIS-TAXONOMY 2026-07-17 (崩壊型/攻撃型/重複型の解剖; ±6ヶ月で重複判定)',
         f"イベント総数: じわ崩壊型(FXのみ)={n_by['collapse']} 攻撃型(EMPのみ)={n_by['attack']} 重複型={n_by['overlap']}"]

    # (i) 時代ミックス
    L.append('(i) 時代ミックス(行=年代, 列=型の構成比):')
    for lo, hi in [(1978, 1989), (1990, 1999), (2000, 2009), (2010, 2025)]:
        sub = [e for e in events if lo <= e[1] <= hi]
        n = len(sub)
        if n == 0:
            continue
        c = sum(1 for e in sub if e[2] == 'collapse') / n
        a = sum(1 for e in sub if e[2] == 'attack') / n
        o = sum(1 for e in sub if e[2] == 'overlap') / n
        L.append(f'  {lo}-{hi}: n={n:4d} 崩壊{c:.0%} 攻撃{a:.0%} 重複{o:.0%}')

    # (ii) 所得階層(WDI incomeLevel)
    L.append('(ii) 所得階層ミックス:')
    inc_order = ['LIC', 'LMC', 'UMC', 'HIC']
    inc_name = {'LIC': '低所得', 'LMC': '下位中所得', 'UMC': '上位中所得', 'HIC': '高所得'}
    for inc in inc_order:
        sub = [e for e in events if meta.get(e[0], {}).get('incomeLevel', {}).get('id') == inc]
        n = len(sub)
        if n < 10:
            continue
        c = sum(1 for e in sub if e[2] == 'collapse') / n
        a = sum(1 for e in sub if e[2] == 'attack') / n
        o = sum(1 for e in sub if e[2] == 'overlap') / n
        L.append(f'  {inc_name[inc]:6s}: n={n:4d} 崩壊{c:.0%} 攻撃{a:.0%} 重複{o:.0%}')

    # (iii) 国の型: 両方を経験した国の割合、型の偏り(2項検定的に)
    by_c = defaultdict(lambda: defaultdict(int))
    for iso, y, t in events:
        by_c[iso][t] += 1
    multi = [iso for iso, d in by_c.items() if sum(d.values()) >= 3]
    typed = 0
    for iso in multi:
        d = by_c[iso]
        tot = sum(d.values())
        mx = max(d.values())
        if mx / tot >= 0.75:
            typed += 1
    L.append(f'(iii) 3イベント以上の国 {len(multi)}カ国中、単一型が75%以上を占める国 = {typed} ({typed/len(multi):.0%})')
    # 型の例
    ex_c = sorted([iso for iso in multi if by_c[iso]['collapse'] / sum(by_c[iso].values()) >= 0.75],
                  key=lambda i: -sum(by_c[i].values()))[:5]
    ex_a = sorted([iso for iso in multi if by_c[iso]['attack'] / sum(by_c[iso].values()) >= 0.75],
                  key=lambda i: -sum(by_c[i].values()))[:5]
    L.append(f'  崩壊型の常連: {[meta.get(i, {}).get("name", i)[:12] for i in ex_c]}')
    L.append(f'  攻撃型の常連: {[meta.get(i, {}).get("name", i)[:12] for i in ex_a]}')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
