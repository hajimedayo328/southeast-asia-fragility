# -*- coding: utf-8 -*-
# 市場グラフ×通貨危機の接続 (設計: notes/36、実行前に固定済み)
# 歴史的マーケットグラフ(1974-2025 月次)を FRED 長期系列から構築し、
# 構造指標(主=β1)が「嵐」を GSI 超えで説明するかを四半期190点で検定する。
import csv, math, statistics, random, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))

RAW = ROOT / 'data_raw'
# (id, kind, invert)  kind: 'rate'=差分, 'px'=対数リターン
NODES = [
    ('DGS10', 'rate', False), ('TB3MS', 'rate', False),
    ('BAA', 'rate', False), ('AAA', 'rate', False),
    ('WTISPLC', 'px', False), ('PPIACO', 'px', False), ('NASDAQCOM', 'px', False),
    ('DEXJPUS', 'px', True), ('DEXUSUK', 'px', False),
    ('DEXCAUS', 'px', True), ('DEXSZUS', 'px', True),
]
WIN = 36          # ローリング窓(月)
THR_MAIN = 0.5    # 主閾値(事前固定)
THR_ROBUST = [0.4, 0.6]


def monthly_series(fid):
    """FRED CSV -> {(y,m): value} 月平均"""
    acc = defaultdict(list)
    with open(RAW / f'fred_{fid}.csv', encoding='utf-8') as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            try:
                y, m = int(row[0][:4]), int(row[0][5:7])
                acc[(y, m)].append(float(row[1]))
            except (ValueError, IndexError):
                continue
    return {k: statistics.mean(v) for k, v in acc.items()}


def returns(series, kind, invert):
    """月次リターン(金利=差分, 価格=対数リターン)。invertで為替の向きを揃える"""
    ks = sorted(series)
    out = {}
    for i in range(1, len(ks)):
        a, b = series[ks[i - 1]], series[ks[i]]
        # 月の連続性チェック
        py, pm = ks[i - 1]
        cy, cm = ks[i]
        if (cy * 12 + cm) - (py * 12 + pm) != 1:
            continue
        if invert:
            if a <= 0 or b <= 0:
                continue
            a, b = 1.0 / a, 1.0 / b
        if kind == 'rate':
            out[ks[i]] = b - a
        else:
            if a <= 0 or b <= 0:
                continue
            out[ks[i]] = math.log(b / a)
    return out


def pearson(a, b):
    n = len(a)
    if n < 8:
        return None
    ma, mb = statistics.mean(a), statistics.mean(b)
    sa, sb = statistics.pstdev(a), statistics.pstdev(b)
    if sa == 0 or sb == 0:
        return None
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / n / (sa * sb)


def graph_stats(names, rets, months, thr):
    """相関>thr を辺とするグラフの構造指標。
    ノードはその窓で十分なデータ(>=24ヶ月)がある系列のみ(欠測ノードで指標が歪むのを防ぐ)"""
    live = [n for n in names if sum(1 for m in months if m in rets[n]) >= 24]
    V = len(live)
    if V < 6:
        return None
    edges = []
    for i in range(V):
        for j in range(i + 1, V):
            xs, ys = [], []
            for m in months:
                a, b = rets[live[i]].get(m), rets[live[j]].get(m)
                if a is not None and b is not None:
                    xs.append(a); ys.append(b)
            r = pearson(xs, ys)
            if r is not None and r > thr:
                edges.append((i, j))
    E = len(edges)
    # 連結成分
    par = list(range(V))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for i, j in edges:
        a, b = find(i), find(j)
        if a != b:
            par[a] = b
    C = len({find(i) for i in range(V)})
    beta1 = E - V + C          # 第一ベッチ数 = 独立サイクル数 = 構造の穴
    density = 2 * E / (V * (V - 1))
    # k-core (最大コア数)
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j); adj[j].add(i)
    deg = {v: len(adj[v]) for v in range(V)}
    alive = set(range(V)); k = 0; maxk = 0
    while alive:
        while True:
            rm = [v for v in alive if deg[v] <= k]
            if not rm:
                break
            for v in rm:
                alive.discard(v)
                for w in adj[v]:
                    if w in alive:
                        deg[w] -= 1
        if alive:
            maxk = k + 1
        k += 1
        if k > V:
            break
    isolated = sum(1 for v in range(V) if len(adj[v]) == 0)
    return dict(beta1=beta1, density=density, max_k_core=maxk, isolated=isolated,
                n_edges=E, n_nodes=V)


def build_market_graph():
    rets = {}
    for fid, kind, inv in NODES:
        s = monthly_series(fid)
        rets[fid] = returns(s, kind, inv)
    names = [n[0] for n in NODES]
    # 全ノードが出揃う1974年以降に限定(初期の欠測ノードで指標が歪むため)
    allm = sorted(m for m in set().union(*[set(rets[n]) for n in names]) if m[0] >= 1974)
    out = {}
    for idx in range(WIN, len(allm)):
        win_months = allm[idx - WIN:idx]
        m = allm[idx - 1]
        stats = {}
        ok = True
        for thr in [THR_MAIN] + THR_ROBUST:
            s = graph_stats(names, rets, win_months, thr)
            if s is None:
                ok = False; break
            stats[thr] = s
        if ok:
            out[m] = stats
    return out


def main():
    print('building historical market graph (1974-2025, monthly, 11 nodes)...', flush=True)
    G = build_market_graph()
    ms = sorted(G)
    print(f'graph months: {ms[0]} -> {ms[-1]} (n={len(ms)})')
    # サニティ: 主要ショック期のβ1
    for probe in [(1998, 9), (2008, 10), (2020, 3), (2015, 8)]:
        if probe in G:
            print(f'  sanity β1 at {probe}: {G[probe][THR_MAIN]["beta1"]} (density {G[probe][THR_MAIN]["density"]:.2f})')
    # 保存
    with open(ROOT / 'data_raw/market_graph_monthly.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['year','month','thr','beta1','density','max_k_core','isolated','n_edges','n_nodes'])
        for (y, m) in ms:
            for thr, s in G[(y, m)].items():
                w.writerow([y,m,thr,s['beta1'],f"{s['density']:.4f}",s['max_k_core'],s['isolated'],s['n_edges'],s['n_nodes']])
    print('saved -> data_raw/market_graph_monthly.csv')


if __name__ == '__main__':
    main()
