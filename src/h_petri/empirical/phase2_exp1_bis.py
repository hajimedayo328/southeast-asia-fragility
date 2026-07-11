# Phase 2 EXP1: BIS LBSネットワーク特徴はG-Gの穴を埋めるか(事前登録: notes/34)
# 特徴量: SS = -為替調整済み年間フロー/前年末残高(winsor±1, 最小残高$50mn)
#         CF = 債権者加重の危機指数(前年末与信シェア×債権者国の危機)
# 検定: train<2000でECDF+ロジスティック学習 -> test>=2000のAUCをGG単独と比較
# 成功基準(事前固定): delta >= +0.03 かつ 国ブロックbootstrap CIが0を除外
# 入力: data_raw/lbs_claims_extract.csv, data_raw/lbs_flows_extract.csv
#   (data_raw/lbs_flat.zip = BIS WS_LBS_D_PUB csv_flat からの1パス抽出。抽出条件:
#    S/F計測, C:総与信, A:全商品, TO1:全通貨, A:全通貨種, 5J:全親国, A:全報告機関,
#    A:全セクター, N:クロスボーダー)
import sys, csv, math, random, statistics
from collections import defaultdict
from bisect import bisect_right
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp

MIN_STOCK = 50.0   # USD millions
WINSOR = 1.0


def load_bis():
    stock = defaultdict(dict)
    bil = defaultdict(lambda: defaultdict(dict))
    with open(ROOT / 'data_raw/lbs_claims_extract.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, per, val in r:
            if not val or '-Q4' not in per:
                continue
            try:
                v = float(val)
            except ValueError:
                continue
            if not math.isfinite(v):
                continue
            y = int(per[:4])
            if rep == '5A':
                stock[cp][y] = v
            elif rep.isalpha():
                bil[cp][y][rep] = v
    flow = defaultdict(lambda: defaultdict(float))
    with open(ROOT / 'data_raw/lbs_flows_extract.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, per, val in r:
            if not val:
                continue
            try:
                v = float(val)
            except ValueError:
                continue
            if math.isfinite(v):
                flow[cp][int(per[:4])] += v
    return stock, bil, flow


def auc(sc, lb):
    pos = sum(lb); neg = len(lb) - pos
    if pos == 0 or neg == 0:
        return None
    order = sorted(range(len(sc)), key=lambda i: sc[i])
    ranks = [0.0] * len(sc)
    i = 0
    while i < len(order):
        j = i
        while j < len(order) and sc[order[j]] == sc[order[i]]:
            j += 1
        for m in range(i, j):
            ranks[order[m]] = (i + j - 1) / 2.0 + 1.0
        i = j
    sp = sum(ranks[x] for x in range(len(sc)) if lb[x] == 1)
    return (sp - pos * (pos + 1) / 2.0) / (pos * neg)


def make_ecdf(vals):
    s = sorted(vals); n = len(s)
    return lambda x: bisect_right(s, x) / n


def fit_logistic(data, feats, ecdfs, iters=6000, lr=0.5, lam=1e-4):
    X = [[ecdfs[j](d[f]) for j, f in enumerate(feats)] for d in data]
    y = [d[5] for d in data]
    wgt = [0.0] * len(feats); b = 0.0
    for _ in range(iters):
        gw = [0.0] * len(feats); gb = 0.0
        for xi, yi in zip(X, y):
            z = b + sum(w * x for w, x in zip(wgt, xi))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            e = p - yi
            gb += e
            for j in range(len(feats)):
                gw[j] += e * xi[j]
        n = len(X)
        b -= lr * gb / n
        for j in range(len(feats)):
            wgt[j] -= lr * (gw[j] / n + lam * wgt[j])

    def score(d):
        return b + sum(w * ecdfs[j](d[f]) for j, (w, f) in enumerate(zip(wgt, feats)))
    return score, wgt


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

    stock, bil, flow = load_bis()
    rows = []
    for (c, t) in gg:
        if not elig(c, t):
            continue
        g = gg[(c, t)]
        if not math.isfinite(g):
            continue
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
        fire = sum(w for rj, w in cred.items()
                   if rj in iso2to3 and (iso2to3[rj], t) in crash) / tot
        if not (math.isfinite(ss) and math.isfinite(fire)):
            continue
        rows.append((c, t, g, ss, fire, lab(c, t)))

    train = [r for r in rows if r[1] < 2000]
    test = [r for r in rows if r[1] >= 2000]
    y_te = [r[5] for r in test]
    aucA = auc([r[2] for r in test], y_te)

    e_g = make_ecdf([r[2] for r in train])
    sc_g, _ = fit_logistic(train, [2], [e_g])
    sanity = auc([sc_g(r) for r in test], y_te)

    e_s = make_ecdf([r[3] for r in train])
    e_c = make_ecdf([r[4] for r in train])
    scB, wB = fit_logistic(train, [2, 3, 4], [e_g, e_s, e_c])
    aucB = auc([scB(r) for r in test], y_te)

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

    print(f'sample n={len(rows)} train={len(train)} test={len(test)}')
    print(f'sanity GG-only logistic={sanity:.4f} vs raw GG={aucA:.4f}')
    print(f'main: GG={aucA:.4f} model={aucB:.4f} delta={aucB - aucA:+.4f}')
    print(f'weights GG,SS,CF={[f"{w:.3f}" for w in wB]}')
    print(f'bootstrap B={n}: CI[{diffs[int(.025 * n)]:+.4f},{diffs[int(.975 * n)]:+.4f}] p={p:.4f}')


if __name__ == '__main__':
    main()
