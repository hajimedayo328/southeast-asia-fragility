# -*- coding: utf-8 -*-
# notes/52: 忘却サイクル — 再発間隔 G と GG再建時間 τ の相関(通貨危機の豚サイクル)
import math, random, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp


def main():
    meta = fp.load_real_countries(); real = set(meta)
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    fx = fp.load_series('fx_lcu_per_usd', real)
    D_, A_ = fp.CRASH_RULES[fp.PRIMARY_RULE]
    crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D_, A_)
    onset = fp.onsets(crash)
    byc = defaultdict(list)
    for (c, t) in onset:
        byc[c].append(t)
    episodes = []
    for c, ts in byc.items():
        ts.sort()
        for i, t0 in enumerate(ts):
            pre = [gg[(c, y)] for y in range(t0 - 3, t0) if (c, y) in gg and math.isfinite(gg[(c, y)])]
            if len(pre) < 2:
                continue
            pre_lv = statistics.median(pre)
            path = [(y, gg[(c, y)]) for y in range(t0, t0 + 16) if (c, y) in gg and math.isfinite(gg[(c, y)])]
            if len(path) < 4:
                continue
            trough_y = min(path[:6], key=lambda p: p[1])[0]
            tau = None
            for y, v in path:
                if y > trough_y and v >= pre_lv:
                    tau = y - t0
                    break
            nxt = ts[i + 1] if i + 1 < len(ts) else None
            G = (nxt - t0) if nxt else None
            episodes.append((c, t0, pre_lv, trough_y - t0, tau, G))
    # 主検定サンプル: τとGが両方あるもの(τはG以内で再建したもののみ=打切り除外)
    S = [(c, tau, G) for (c, t0, pl, tr, tau, G) in episodes
         if tau is not None and G is not None and tau <= G]
    taus = [x[1] for x in S]; Gs = [x[2] for x in S]

    def spearman(a, b):
        def rk(v):
            s = sorted(range(len(v)), key=lambda i: v[i])
            r = [0.0] * len(v)
            for j, i in enumerate(s):
                r[i] = j
            return r
        ra, rb = rk(a), rk(b)
        ma, mb = statistics.mean(ra), statistics.mean(rb)
        num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        da = math.sqrt(sum((x - ma) ** 2 for x in ra))
        db = math.sqrt(sum((y - mb) ** 2 for y in rb))
        return num / (da * db) if da * db > 0 else 0.0
    rho = spearman(taus, Gs)
    # 国単位並べ替え: 国ごとのτ列を国間でシャッフル
    byc2 = defaultdict(list)
    for c, tau, G in S:
        byc2[c].append((tau, G))
    cl = sorted(byc2); rng = random.Random(191)
    cnt = 0; B = 2000
    for _ in range(B):
        perm = cl[:]; rng.shuffle(perm)
        a = []; b = []
        for c_orig, c_perm in zip(cl, perm):
            gs = [g for _, g in byc2[c_orig]]
            ts_ = [t for t, _ in byc2[c_perm]]
            n = min(len(gs), len(ts_))
            a.extend(ts_[:n]); b.extend(gs[:n])
        if spearman(a, b) >= rho:
            cnt += 1
    p = cnt / B
    # 記述: V字軌道
    rel = defaultdict(list)
    for (c, t0, pl, tr, tau, G) in episodes:
        for dy in range(-3, 11):
            v = gg.get((c, t0 + dy))
            if v is not None and math.isfinite(v) and v < 10:
                rel[dy].append(v)
    prof = {dy: round(statistics.median(v), 2) for dy, v in sorted(rel.items()) if len(v) >= 10}
    med_tau = statistics.median(taus) if taus else None
    med_G = statistics.median(Gs) if Gs else None
    cens = sum(1 for e in episodes if e[4] is None and e[5] is not None)
    L = ['', f'FORGETTING-CYCLE 2026-07-22 (notes/52。episodes={len(episodes)}, 主検定対象n={len(S)}({len(byc2)}カ国), 打切り(G内未再建)={cens}件は除外)',
         f'  記述: GG中央値軌道(onset相対年): {prof}',
         f'  τ(再建時間)中央値={med_tau}年 / G(再発間隔)中央値={med_G}年',
         f'  主検定: Spearman rho(tau,G)={rho:+.3f} 国単位並べ替えp={p:.3f}',
         f'  -> {"PASS: 再発は在庫の再建にペースを合わせる(豚サイクル成立)" if rho > 0 and p < 0.05 else "FAIL: 再発ペースは在庫再建では決まらない(嵐主導・豚サイクルの適用限界)"}']
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
