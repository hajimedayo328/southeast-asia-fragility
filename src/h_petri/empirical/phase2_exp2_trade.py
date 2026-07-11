# Phase 2 EXP2: 貿易ネットワークの隣人炎上指数はG-Gの穴を埋めるか(事前登録: notes/34)
# 特徴量: TF(c,t) = Σ_j w_ij(t-1)·crisis_j(t) / Σ_j w_ij(t-1)
#   w = 輸出FOB+輸入CIF(USD, IMF IMTS), crisis_j(t) = 相手国jがt年に危機状態(crashルールLV)
#   条件: Σw>0 かつ 相手国3カ国以上
# 主検定(事前固定): GG単独 vs GG+TF。train<2000 ECDFロジスティック→test>=2000 AUC。
#   成功基準 = delta >= +0.03 かつ 国ブロックbootstrap CIが0を除外
# 副検定(事前宣言): GG+TF+CF(BIS債権者炎上, EXP1)の3特徴版(BIS被覆との共通サンプル)
# サニティ: GG単独ロジスティックが生GGのAUCを再現すること
import sys, csv, math, random
from collections import defaultdict
from bisect import bisect_right
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from phase2_exp1_bis import load_bis, auc, make_ecdf, fit_logistic, MIN_STOCK, WINSOR


def main():
    meta = fp.load_real_countries(); real = set(meta)
    iso2to3 = {v['iso2Code']: k for k, v in meta.items()}
    gg = {k: v / 100 for k, v in fp.load_series('st_debt_reserves', real).items()}
    fx = fp.load_series('fx_lcu_per_usd', real)
    D, A = fp.CRASH_RULES[fp.PRIMARY_RULE]
    crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D, A)
    onset = fp.onsets(crash); k = fp.PRIMARY_K

    def elig(c, t):
        if any((c, t + j) not in fx for j in range(-1, k + 1)):
            return False
        return (c, t) not in crash

    def lab(c, t):
        return 1 if any((c, t + j) in onset for j in range(1, k + 1)) else 0

    # 貿易行列: trade[reporter][year] = {partner: X+M}
    trade = defaultdict(lambda: defaultdict(dict))
    with open(ROOT / 'data_raw/imts_trade.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, v in r:
            try:
                trade[rep][int(yr)][cp] = float(v)
            except ValueError:
                continue

    def trade_fire(c, t):
        w = trade.get(c, {}).get(t - 1, {})
        if len(w) < 3:
            return None
        tot = sum(w.values())
        if tot <= 0:
            return None
        return sum(v for j, v in w.items() if (j, t) in crash) / tot

    rows = []
    for (c, t) in gg:
        if not elig(c, t):
            continue
        g = gg[(c, t)]
        if not math.isfinite(g):
            continue
        tf = trade_fire(c, t)
        if tf is None or not math.isfinite(tf):
            continue
        rows.append((c, t, g, tf, 0.0, lab(c, t)))

    train = [r for r in rows if r[1] < 2000]
    test = [r for r in rows if r[1] >= 2000]
    y_te = [r[5] for r in test]
    aucA = auc([r[2] for r in test], y_te)

    e_g = make_ecdf([r[2] for r in train])
    sc_g, _ = fit_logistic(train, [2], [e_g])
    sanity = auc([sc_g(r) for r in test], y_te)

    e_t = make_ecdf([r[3] for r in train])
    scB, wB = fit_logistic(train, [2, 3], [e_g, e_t])
    aucB = auc([scB(r) for r in test], y_te)
    a_tf = auc([r[3] for r in rows], [r[5] for r in rows])
    sub = [r for r in test if r[2] <= 1.0]
    a_tf_sub = auc([r[3] for r in sub], [r[5] for r in sub])

    by_c = defaultdict(list)
    for r in test:
        by_c[r[0]].append(r)
    cl = sorted(by_c); rng = random.Random(12345); diffs = []
    for _ in range(800):
        s = []
        for _ in range(len(cl)):
            s.extend(by_c[rng.choice(cl)])
        x = auc([r[2] for r in s], [r[5] for r in s])
        yv = auc([scB(r) for r in s], [r[5] for r in s])
        if x is not None and yv is not None:
            diffs.append(yv - x)
    diffs.sort(); n = len(diffs)
    p = 2 * min(sum(1 for d in diffs if d <= 0), sum(1 for d in diffs if d >= 0)) / n

    # 副検定: BIS特徴(SS,CF)との3+1特徴版(共通サンプル)
    stock, bil, flow = load_bis()
    rows3 = []
    for (c, t, g, tf, _, y) in rows:
        i2 = meta[c]['iso2Code']
        s0 = stock.get(i2, {}).get(t - 1)
        fl = flow.get(i2, {}).get(t)
        if s0 is None or s0 < MIN_STOCK or fl is None:
            continue
        ss = max(-WINSOR, min(WINSOR, -fl / s0))
        cred = bil.get(i2, {}).get(t - 1, {})
        tot = sum(cred.values())
        if tot <= 0:
            continue
        cf = sum(w for rj, w in cred.items()
                 if rj in iso2to3 and (iso2to3[rj], t) in crash) / tot
        if not (math.isfinite(ss) and math.isfinite(cf)):
            continue
        rows3.append((c, t, g, tf, ss, cf, y))
    tr3 = [r for r in rows3 if r[1] < 2000]
    te3 = [r for r in rows3 if r[1] >= 2000]
    sec = None
    if len(tr3) > 200 and len(te3) > 200:
        ecs = [make_ecdf([r[f] for r in tr3]) for f in (2, 3, 4, 5)]

        def fitsec(data, feats, ecdfs):
            d6 = [(r[0], r[1], r[2], r[3], r[4], r[6]) for r in data]
            return None
        # 3+1特徴ロジスティック(ラベルはindex6)
        X = [[ecs[j]([r[2], r[3], r[4], r[5]][j]) for j in range(4)] for r in tr3]
        yv = [r[6] for r in tr3]
        wgt = [0.0] * 4; b = 0.0; lr = 0.5; lam = 1e-4
        for _ in range(6000):
            gw = [0.0] * 4; gb = 0.0
            for xi, yi in zip(X, yv):
                z = b + sum(w * x for w, x in zip(wgt, xi))
                pp = 1 / (1 + math.exp(-max(-30, min(30, z))))
                e = pp - yi
                gb += e
                for j in range(4):
                    gw[j] += e * xi[j]
            nn = len(X)
            b -= lr * gb / nn
            for j in range(4):
                wgt[j] -= lr * (gw[j] / nn + lam * wgt[j])

        def sc3(r):
            return b + sum(w * ecs[j]([r[2], r[3], r[4], r[5]][j]) for j, w in enumerate(wgt))
        aucA3 = auc([r[2] for r in te3], [r[6] for r in te3])
        aucB3 = auc([sc3(r) for r in te3], [r[6] for r in te3])
        sec = (len(rows3), len(tr3), len(te3), aucA3, aucB3, wgt)

    L = ['', 'PHASE2 EXP2 2026-07-11 (IMTS trade_fire=partner-trade-weighted crisis state; LV_30_10 k=2)',
         f'sample n={len(rows)} (train<2000 n={len(train)} crises={sum(r[5] for r in train)} / test>=2000 n={len(test)} crises={sum(r[5] for r in test)})',
         f'sanity: GG-only logistic test AUC={sanity:.4f} vs raw GG={aucA:.4f}',
         f'solo AUC full-sample: trade_fire={a_tf:.4f}; blind region(test&GG<=1, n={len(sub)} crises={sum(r[5] for r in sub)}): TF AUC={a_tf_sub:.4f}',
         f'main: GG alone test={aucA:.4f} | GG+TF test={aucB:.4f} delta={aucB - aucA:+.4f}; weights GG,TF={[f"{w:.3f}" for w in wB]}',
         f'      bootstrap B={n}: CI[{diffs[int(.025 * n)]:+.4f},{diffs[int(.975 * n)]:+.4f}] p={p:.4f}']
    if sec:
        n3, ntr3, nte3, aA3, aB3, w3 = sec
        L.append(f'secondary(declared) GG+TF+SS+CF on BIS∩trade sample n={n3}: GG test={aA3:.4f} model test={aB3:.4f} delta={aB3 - aA3:+.4f}; weights={[f"{w:.3f}" for w in w3]}')
    L.append('pre-registered success = delta>=+0.03 AND CI excludes 0')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
