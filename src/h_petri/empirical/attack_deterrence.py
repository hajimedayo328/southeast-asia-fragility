# -*- coding: utf-8 -*-
# ATTACK-DETERRENCE (事前固定): 貯金は「抑止力」か
# 全国月パネル(EMP危機状態でない国月)で、準備の輸入月数(少=危険)が
# 「3ヶ月以内のEMP攻撃onset」を予測するか。予測=する(低準備→攻撃されやすい)なら
# 選択効果の実証が完成: 貯金=抑止力(攻撃前) かつ 非防衛力(攻撃後)
import csv, math, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from phase2_exp1_bis import auc
from attack_anatomy import load_fxm, build_emp_attacks


def main():
    fxm = load_fxm()
    attacks = build_emp_attacks(fxm)
    att_idx = defaultdict(set)
    for iso, y, m in attacks:
        att_idx[iso].add(y * 12 + m - 1)

    res = defaultdict(dict)
    with open(ROOT / 'data_raw/il_reserves_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                res[row['iso3']][(int(y), int(m))] = float(row['reserves_usd'])
            except (ValueError, KeyError):
                continue
    imports = defaultdict(lambda: defaultdict(float))
    with open(ROOT / 'data_raw/imts_trade_xm.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, xv, mv in r:
            try:
                imports[rep][int(yr)] += float(mv)
            except ValueError:
                continue

    # EMP危機状態(攻撃中)の除外用: attacksのspan近似として onset月から6ヶ月を除外
    in_attack = defaultdict(set)
    for iso, y, m in attacks:
        a0 = y * 12 + m - 1
        for i in range(a0, a0 + 7):
            in_attack[iso].add(i)

    rows = []
    for iso in res:
        for (y, m), r1 in res[iso].items():
            if y < 1978 or y > 2024:
                continue
            idx = y * 12 + m - 1
            if idx in in_attack.get(iso, set()):
                continue
            imp = imports.get(iso, {}).get(y - 1)
            if not imp or imp <= 0:
                continue
            rm = r1 / (imp / 12.0)
            if not math.isfinite(rm) or rm > 120:
                continue
            hit = 1 if any((idx + k) in att_idx.get(iso, set()) for k in (1, 2, 3)) else 0
            rows.append((iso, -rm, hit))   # 少=危険 → 符号反転

    n_hit = sum(r[2] for r in rows)
    a_rm = auc([r[1] for r in rows], [r[2] for r in rows])
    # 国ブロックbootstrap CI
    import random
    byc = defaultdict(list)
    for r in rows:
        byc[r[0]].append(r)
    cl = sorted(byc); rng = random.Random(9); aa = []
    for b in range(300):
        s = []
        for _ in range(len(cl)):
            s.extend(byc[rng.choice(cl)])
        v = auc([x[1] for x in s], [x[2] for x in s])
        if v is not None:
            aa.append(v)
    aa.sort(); n = len(aa)
    L = ['', 'ATTACK-DETERRENCE 2026-07-17 (貯金は抑止力か: 非攻撃時の国月で、準備の輸入月数[少=危険]が3ヶ月以内の攻撃onsetを予測するか)',
         f'国月 {len(rows)} (うち3ヶ月以内に攻撃 {n_hit}): AUC={a_rm:.3f} CI[{aa[int(.025*n)]:.3f},{aa[int(.975*n)]:.3f}]',
         f'-> {"抑止力あり(低準備→攻撃されやすい)" if aa[int(.025*n)] > 0.5 else "抑止力も検出されず"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
