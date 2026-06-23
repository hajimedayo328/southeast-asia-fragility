"""1997 TDA結果の中身を分解する。
(1) vol標準化: 各国リターンをローリングvol(20日)で割ってからTDA。
    1.90倍が消えれば「単なるボラ増」、残れば「co-movement構造の変化」。
(2) change-point: L2ノルムが平穏baseline(平均+2sd)を最初に超えた日 vs 崩壊(1997-07-02)。
出力ASCII。値は実計算のみ。"""
import os
import numpy as np
import pandas as pd
from ripser import ripser

OUT = os.path.dirname(os.path.abspath(__file__))
CRISIS = pd.Timestamp("1997-07-02")
C7 = ["TH", "ID", "KR", "MY", "PH", "SG", "HK"]


def h1_L2(dates, X, w=50):
    centers, L2 = [], []
    for i in range(len(X) - w + 1):
        h1 = ripser(X[i:i + w], maxdim=1)["dgms"][1]
        if len(h1) == 0:
            L2.append(0.0)
        else:
            life = h1[:, 1] - h1[:, 0]
            life = life[np.isfinite(life)]
            L2.append(float(np.sqrt((life ** 2).sum())))
        centers.append(dates[i + w - 1])
    return pd.to_datetime(centers), np.array(L2)


def split(centers, v):
    pre = v[(centers >= pd.Timestamp("1997-01-01")) & (centers < CRISIS)]
    cri = v[(centers >= CRISIS) & (centers < pd.Timestamp("1998-03-01"))]
    return pre, cri


px = pd.read_csv(os.path.join(OUT, "indices_close.csv"), index_col=0, parse_dates=True)[C7].dropna()
ret = np.log(px / px.shift(1)).dropna()

# ---- (1) raw vs vol-adjusted ----
print("=== (1) raw vs vol-standardized returns (w=50) ===")
variants = {
    "raw": ret,
    "vol_adj(20d)": (ret / ret.rolling(20).std()).dropna(),
}
for name, R in variants.items():
    dates = pd.to_datetime(R.index)
    centers, L2 = h1_L2(dates, R.values, 50)
    pre, cri = split(centers, L2)
    ratio = cri.mean() / pre.mean() if pre.mean() > 0 else float("nan")
    pk = centers[int(np.argmax(L2))]
    print("%-14s calm=%.4f crisis=%.4f ratio=%.2f peak=%s before_Jul2=%s" %
          (name, pre.mean(), cri.mean(), ratio, str(pk.date()), "YES" if pk < CRISIS else "NO"))

# ---- (2) change-point on raw L2 ----
print("\n=== (2) change-point: first day L2 exceeds calm baseline (mean+2sd) ===")
dates = pd.to_datetime(ret.index)
centers, L2 = h1_L2(dates, ret.values, 50)
pre, cri = split(centers, L2)
thr = pre.mean() + 2 * pre.std()
after_jan = centers >= pd.Timestamp("1997-01-01")
exceed = (L2 > thr) & after_jan
if exceed.any():
    first = centers[np.argmax(exceed)]
    lead = (CRISIS - first).days
    print("calm baseline mean=%.4f sd=%.4f  threshold(mean+2sd)=%.4f" % (pre.mean(), pre.std(), thr))
    print("first exceedance = %s   (Thai float 1997-07-02; %+d days vs crisis)" %
          (str(first.date()), -lead))
    print("=> %s" % ("BEFORE crisis (weak precursor)" if first < CRISIS else "AT/AFTER crisis onset (no precursor)"))
else:
    print("never exceeds threshold")

# sustained: first day where L2 stays above thr for >=10 consecutive days
print("\n=== sustained breakout (>=10 consecutive days above threshold) ===")
above = (L2 > thr).astype(int)
run = 0
sustained = None
for c, a in zip(centers, above):
    run = run + 1 if a else 0
    if run >= 10 and sustained is None and c >= pd.Timestamp("1997-01-01"):
        sustained = centers[list(centers).index(c) - 9]  # start of the run
        break
if sustained is not None:
    print("sustained breakout starts = %s  (%+d days vs 1997-07-02)" %
          (str(sustained.date()), -(CRISIS - sustained).days))
    print("=> %s" % ("BEFORE crisis" if sustained < CRISIS else "AT/AFTER crisis onset"))
else:
    print("no sustained breakout found")
