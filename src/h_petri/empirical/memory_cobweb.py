# -*- coding: utf-8 -*-
# notes/54 MEMORY-COBWEB: 半導体PPI(1967-)でブーム2年後の谷を検定(相対成長・事前固定)
import csv, math, random, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main():
    ann = defaultdict(list)
    with open(ROOT / 'data_raw/fred_PCU334413334413.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for d, v in r:
            try:
                ann[int(d[:4])].append(float(v))
            except ValueError:
                continue
    lvl = {y: statistics.mean(v) for y, v in ann.items() if len(v) >= 10}
    g = {y: lvl[y] / lvl[y - 1] - 1 for y in sorted(lvl) if y - 1 in lvl}
    ys = sorted(g)
    # 相対成長: 拡大窓中央値(最低8年)を控除
    rel = {}
    for j, y in enumerate(ys):
        hist = [g[x] for x in ys[:j + 1]]
        if len(hist) >= 8:
            rel[y] = g[y] - statistics.median(hist)
    rys = sorted(rel)
    booms = []
    for j, y in enumerate(rys):
        hist = [rel[x] for x in rys[:j + 1]]
        if len(hist) < 8 or y > max(rys) - 4:
            continue
        if rel[y] >= sorted(hist)[int(0.75 * len(hist))]:
            booms.append(y)
    paths = {k: [rel[b + k] for b in booms if b + k in rel] for k in range(1, 5)}
    mean_path = {k: statistics.mean(v) for k, v in paths.items() if v}
    # 谷ラグ分布
    trough = []
    for b in booms:
        cand = {k: rel[b + k] for k in range(1, 5) if b + k in rel}
        if len(cand) == 4:
            trough.append(min(cand, key=cand.get))
    # 主検定: (i) k=2平均<0 (ii) 符号検定
    k2 = paths.get(2, [])
    neg = sum(1 for x in k2 if x < 0)
    n = len(k2)
    # 二項片側p (p0=0.5)
    from math import comb
    p_sign = sum(comb(n, i) for i in range(neg, n + 1)) / 2 ** n if n else 1.0
    ok = mean_path.get(2, 1) < 0 and p_sign < 0.05
    tdist = {k: trough.count(k) for k in range(1, 5)}
    L = ['', f'MEMORY-COBWEB 2026-09-04 (notes/54。半導体PPI 1967-2025年次・相対成長。booms={len(booms)})',
         f'  ブーム後の平均相対成長: ' + ' '.join(f'k={k}:{mean_path[k]:+.3f}' for k in sorted(mean_path)),
         f'  谷ラグ分布(k=1..4): {[tdist.get(k,0) for k in range(1,5)]} (TTB予測はk=2)',
         f'  主検定: k=2平均={mean_path.get(2):+.3f}, 負の割合={neg}/{n}, 符号検定p={p_sign:.3f}',
         f'  -> {"PASS: 単一財ではブーム約2年後に潰れる(コブウェブ成立)" if ok else "FAIL"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('booms:', booms)
    print('\n'.join(L))


if __name__ == '__main__':
    main()
