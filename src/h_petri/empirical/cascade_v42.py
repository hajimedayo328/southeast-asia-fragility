# -*- coding: utf-8 -*-
# CASCADE v4.2: 分散の内生化 σ_i,t = σ0 · x^g (危険な国ほど高ボラ)
# 事前固定: g は pre-2000 の残差から log|ε| ~ log x のOLS(傾きは不偏)。検証は v4.1 と同じ4項目
import sys, csv, math, random, statistics
from collections import defaultdict
from bisect import bisect_right
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp

meta = fp.load_real_countries(); real = set(meta)
gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
fx = fp.load_series('fx_lcu_per_usd', real)
D_, A_ = fp.CRASH_RULES[fp.PRIMARY_RULE]
crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D_, A_)
onset = fp.onsets(crash)

trade = defaultdict(lambda: defaultdict(dict))
with open(ROOT / 'data_raw/imts_trade.csv', encoding='utf-8') as f:
    r = csv.reader(f); next(r)
    for rep, cp, yr, v in r:
        try:
            trade[rep][int(yr)][cp] = float(v)
        except ValueError:
            continue
_p = {}
def prow(c, t):
    if (c, t) in _p:
        return _p[(c, t)]
    w = trade.get(c, {}).get(t - 1, {})
    if len(w) < 3:
        _p[(c, t)] = None
    else:
        tot = sum(w.values())
        _p[(c, t)] = {j: v / tot for j, v in w.items()} if tot > 0 else None
    return _p[(c, t)]

YRS = list(range(1977, 2023))
cs_all = sorted({c for (c, _) in gg})
wc = {}
for t in YRS:
    have = [c for c in {c for (c, _) in fx} if (c, t) in fx]
    wc[t] = sum(1 for c in have if (c, t) in onset) / max(1, len(have))


def ols(X, y):
    n = len(X); k = len(X[0]) + 1
    Xd = [[1.0] + r for r in X]
    A = [[sum(Xd[i][a] * Xd[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    bv = [sum(Xd[i][a] * y[i] for i in range(n)) for a in range(k)]
    M = [row[:] + [bv[i]] for i, row in enumerate(A)]
    for c_ in range(k):
        p = max(range(c_, k), key=lambda r: abs(M[r][c_])); M[c_], M[p] = M[p], M[c_]
        for r in range(k):
            if r != c_ and abs(M[c_][c_]) > 1e-12:
                f = M[r][c_] / M[c_][c_]
                for cc in range(c_, k + 1):
                    M[r][cc] -= f * M[c_][cc]
    beta = [M[i][k] / M[i][i] for i in range(k)]
    yh = [sum(b * x for b, x in zip(beta, Xd[i])) for i in range(n)]
    return beta, [a - b for a, b in zip(y, yh)]


rows = []
for c in cs_all:
    for t in range(1977, 2000):
        x0 = gg.get((c, t)); x1 = gg.get((c, t + 1))
        if not x0 or not x1 or x0 <= 0 or x1 <= 0:
            continue
        d = math.log(x1) - math.log(x0)
        if abs(d) > 3:
            continue
        rows.append((d, 1.0 if (c, t) in onset else 0.0, wc[t], math.log(x0)))

beta, resid = ols([[r[1], r[2], r[3]] for r in rows], [r[0] for r in rows])
a0, b_own, c_world, d_mr = -beta[0], -beta[1], -beta[2], -beta[3]
sig_flat = statistics.pstdev(resid)

vr = [(math.log(abs(e)), r[3]) for e, r in zip(resid, rows) if abs(e) > 1e-6]
bv, _ = ols([[p[1]] for p in vr], [p[0] for p in vr])
g_var = bv[1]
print(f'分散の x 依存: g={g_var:+.4f} (n={len(vr)})  → σ ∝ x^{g_var:.3f}')

# 裏取り: log x の五分位ごとの残差sd
pairs = sorted(zip(rows, resid), key=lambda z: z[0][3])
m = len(pairs) // 5
for i in range(5):
    grp = pairs[i * m:(i + 1) * m]
    print(f'  x五分位{i+1} (log x中央値 {statistics.median(z[0][3] for z in grp):+.2f}): '
          f'残差sd={statistics.pstdev([z[1] for z in grp]):.3f}')

mean_lx = statistics.mean(r[3] for r in rows)
sig0 = sig_flat / math.exp(g_var * mean_lx)


def make_ecdf(v):
    s = sorted(v); n = len(s)
    return lambda x: bisect_right(s, x) / n


def fit_logit(data, iters=3000, lr=0.5):
    X = [[d[0], d[1]] for d in data]; Y = [d[2] for d in data]
    w = [0.0, 0.0]; b = 0.0
    for _ in range(iters):
        gw = [0.0, 0.0]; gb = 0.0
        for xi, yi in zip(X, Y):
            z = b + w[0] * xi[0] + w[1] * xi[1]
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            e = p - yi; gb += e; gw[0] += e * xi[0]; gw[1] += e * xi[1]
        n = len(X); b -= lr * gb / n
        for j in range(2):
            w[j] -= lr * (gw[j] / n + 1e-4 * w[j])
    return w, b


fit = []
for t in range(1977, 2000):
    live = [c for c in cs_all if (c, t) in gg and prow(c, t)]
    if len(live) < 10:
        continue
    ex = make_ecdf([gg[(c, t)] for c in live])
    pf = {c: sum(w for j, w in prow(c, t).items() if (j, t) in crash) for c in live}
    ep = make_ecdf(list(pf.values()))
    for c in live:
        if (c, t) in crash:
            continue
        fit.append((ex(gg[(c, t)]), ep(pf[c]), 1 if (c, t + 1) in crash else 0))
wF, bF = fit_logit(fit)
rho = sum(1 if (c, t + 1) in crash else 0 for (c, t) in crash if t < 2000) / len([1 for (c, t) in crash if t < 2000])


def sg(z):
    return 1 / (1 + math.exp(-max(-30, min(30, z))))


def simulate(var_mode, seed):
    rng = random.Random(seed)
    x = {c: gg[(c, 1977)] for c in cs_all if (c, 1977) in gg}
    st = {c: ((c, 1977) in crash) for c in cs_all}
    med = {}; frac = {}; p75 = {}; ons = []
    for t in YRS:
        live = [c for c in x if x[c] > 0 and prow(c, t)]
        if len(live) < 10:
            break
        ex = make_ecdf([x[c] for c in live])
        pf = {c: sum(w for j, w in prow(c, t).items() if st.get(j, False)) for c in live}
        ep = make_ecdf(list(pf.values()))
        newst = {}; o = 0
        for c in live:
            if st.get(c, False):
                newst[c] = rng.random() < rho
            else:
                newst[c] = rng.random() < sg(bF + wF[0] * ex(x[c]) + wF[1] * ep(pf[c]))
                if newst[c]:
                    o += 1
        ons.append(o); wcr = o / len(live)
        for c in live:
            own = 1.0 if st.get(c, False) else 0.0
            lx = math.log(x[c])
            s = (sig0 * math.exp(g_var * lx)) if var_mode == 'endog' else sig_flat
            s = max(0.05, min(2.0, s))
            x[c] = math.exp(lx - (a0 + b_own * own + c_world * wcr + d_mr * lx) + rng.gauss(0, s))
            x[c] = max(1e-3, min(50.0, x[c]))
        st = newst
        v = sorted(x[c] for c in live)
        med[t] = statistics.median(v)
        frac[t] = sum(1 for q in v if q > 1) / len(v)
        p75[t] = v[int(.75 * len(v))]
    return med, frac, p75, ons


def obs_at(y_, f):
    v = sorted(gg[(c, y_)] for c in cs_all if (c, y_) in gg)
    return f(v)


obs_med = {y_: obs_at(y_, statistics.median) for y_ in (2007, 2022)}
obs_frac = {y_: obs_at(y_, lambda v: sum(1 for q in v if q > 1) / len(v)) for y_ in (2007, 2022)}
obs_p75 = {y_: obs_at(y_, lambda v: v[int(.75 * len(v))]) for y_ in (2007, 2022)}

L = ['', 'CASCADE v4.2 2026-07-15 (分散の内生化: sigma = sigma0 * x^g。危険な国ほど高ボラ→皆が積むと分散も縮むフィードバック)',
     f'推定: **分散のx依存 g={g_var:+.4f}** (sigma ∝ x^{g_var:.2f}, n={len(vr)}) | a={a0:+.4f} b_own={b_own:+.4f} c_world={c_world:+.4f} d_mr={d_mr:+.4f} sigma_flat={sig_flat:.3f}',
     f'観測(較正外): 中央値07={obs_med[2007]:.3f}/22={obs_med[2022]:.3f} | >1割合07={obs_frac[2007]:.3f}/22={obs_frac[2022]:.3f} | p75 07={obs_p75[2007]:.3f}/22={obs_p75[2022]:.3f}']
for mode, label in [('endog', 'v4.2 フル(分散も内生)'), ('flat', 'v4.1 対照(分散固定)')]:
    M = []; F = []; P = []; O = []
    for i in range(300):
        med, frac, p75, ons = simulate(mode, 3000 + i)
        if 2007 in med and 2022 in med:
            M.append((med[2007], med[2022])); F.append((frac[2007], frac[2022]))
            P.append((p75[2007], p75[2022])); O.append(statistics.mean(ons))
    if not M:
        continue
    def band(v, i):
        s = sorted(z[i] for z in v)
        return s[int(.05 * len(s))], s[int(.95 * len(s))]
    ok = lambda o, b: b[0] <= o <= b[1]
    m07, m22, f07, f22, p07, p22 = band(M, 0), band(M, 1), band(F, 0), band(F, 1), band(P, 0), band(P, 1)
    n_ok = sum([ok(obs_med[2007], m07), ok(obs_med[2022], m22), ok(obs_frac[2007], f07), ok(obs_frac[2022], f22)])
    L.append(f'  {label}: 主要4項目 {n_ok}/4 通過 (onset/年={statistics.mean(O):.1f})')
    L.append(f'    中央値07[{m07[0]:.3f},{m07[1]:.3f}]{"OK" if ok(obs_med[2007],m07) else "NG"} 22[{m22[0]:.3f},{m22[1]:.3f}]{"OK" if ok(obs_med[2022],m22) else "NG"}')
    L.append(f'    >1割合07[{f07[0]:.3f},{f07[1]:.3f}]{"OK" if ok(obs_frac[2007],f07) else "NG"} 22[{f22[0]:.3f},{f22[1]:.3f}]{"OK" if ok(obs_frac[2022],f22) else "NG"}')
    L.append(f'    [参考]p75 07[{p07[0]:.3f},{p07[1]:.3f}]{"OK" if ok(obs_p75[2007],p07) else "NG"} 22[{p22[0]:.3f},{p22[1]:.3f}]{"OK" if ok(obs_p75[2022],p22) else "NG"} ←分散縮小の直接指標')

with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')
print('\n'.join(L))
