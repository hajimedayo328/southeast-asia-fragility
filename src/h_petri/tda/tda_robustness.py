"""1997 TDA結果の頑健性チェック。
主張する前に: 危機/平穏 比(点推定1.90) と「前兆でない(ピークが崩壊後)」が
window長・指標・国セットに安定か、ブロックbootstrap CIが1を超えるかを確認する。
出力はASCII(Bashの文字化け回避)。値は実計算のみ。"""
import os
import numpy as np
import pandas as pd
from ripser import ripser

OUT = os.path.dirname(os.path.abspath(__file__))
CRISIS_START = pd.Timestamp("1997-07-02")  # タイ変動相場制移行


def load(countries):
    px = pd.read_csv(os.path.join(OUT, "indices_close.csv"), index_col=0, parse_dates=True)
    px = px[countries].dropna()
    ret = np.log(px / px.shift(1)).dropna()
    return pd.to_datetime(ret.index), ret.values


def h1_metrics(dates, X, w):
    centers, L2, maxlife, nloop = [], [], [], []
    for i in range(len(X) - w + 1):
        h1 = ripser(X[i:i + w], maxdim=1)["dgms"][1]
        if len(h1) == 0:
            L2.append(0.0); maxlife.append(0.0); nloop.append(0)
        else:
            life = h1[:, 1] - h1[:, 0]
            life = life[np.isfinite(life)]
            L2.append(float(np.sqrt((life ** 2).sum())))
            maxlife.append(float(life.max()) if len(life) else 0.0)
            nloop.append(int(len(life)))
        centers.append(dates[i + w - 1])
    return pd.to_datetime(centers), np.array(L2), np.array(maxlife), np.array(nloop)


def split(centers, v):
    pre = v[(centers >= pd.Timestamp("1997-01-01")) & (centers < CRISIS_START)]
    cri = v[(centers >= CRISIS_START) & (centers < pd.Timestamp("1998-03-01"))]
    return pre, cri


C7 = ["TH", "ID", "KR", "MY", "PH", "SG", "HK"]

dates, X = load(C7)
print("data: 7 countries  N=%d  %s..%s" % (len(X), dates.min().date(), dates.max().date()))

print("\n=== window sweep (7 countries, metric = L2 of lifespans) ===")
print("%4s %9s %9s %7s %12s %14s" % ("w", "calm", "crisis", "ratio", "peak_date", "peak_before_Jul2?"))
for w in [30, 40, 50, 70, 100]:
    centers, L2, ml, nl = h1_metrics(dates, X, w)
    pre, cri = split(centers, L2)
    ratio = cri.mean() / pre.mean() if pre.mean() > 0 else float("nan")
    pk = centers[int(np.argmax(L2))]
    before = pk < CRISIS_START
    print("%4d %9.4f %9.4f %7.2f %12s %14s" %
          (w, pre.mean(), cri.mean(), ratio, str(pk.date()), "YES" if before else "NO"))

print("\n=== metric sweep (w=50) ===")
centers, L2, ml, nl = h1_metrics(dates, X, 50)
for nm, v in [("L2_lifespan", L2), ("max_lifespan", ml), ("loop_count", nl.astype(float))]:
    pre, cri = split(centers, v)
    ratio = cri.mean() / pre.mean() if pre.mean() > 0 else float("nan")
    pk = centers[int(np.argmax(v))]
    print("%-13s calm=%.4f crisis=%.4f ratio=%.2f peak=%s before_Jul2=%s" %
          (nm, pre.mean(), cri.mean(), ratio, str(pk.date()), "YES" if pk < CRISIS_START else "NO"))

print("\n=== block bootstrap CI for ratio (w=50, L2, B=2000, block=10) ===")
pre, cri = split(centers, L2)
rng = np.random.default_rng(42)


def block_resample(a, bl=10):
    out = []
    while len(out) < len(a):
        s = rng.integers(0, len(a))
        out.extend(a[s:s + bl])
    return np.array(out[:len(a)])


ratios = np.array([block_resample(cri).mean() / block_resample(pre).mean() for _ in range(2000)])
lo, hi = np.percentile(ratios, [2.5, 97.5])
print("ratio point=%.2f  95%%CI=[%.2f, %.2f]  excludes_1=%s" %
      (cri.mean() / pre.mean(), lo, hi, "YES" if lo > 1 else "NO"))

print("\n=== country-set check: 5 countries with long 1995 baseline (TH,KR excluded) ===")
print("(needs 1995 data; uses same cache if present, else skip)")
try:
    dates5, X5 = load(["ID", "MY", "PH", "SG", "HK"])
    if dates5.min() <= pd.Timestamp("1996-06-01"):
        centers5, L25, _, _ = h1_metrics(dates5, X5, 50)
        pre5, cri5 = split(centers5, L25)
        pk5 = centers5[int(np.argmax(L25))]
        print("5-country: calm=%.4f crisis=%.4f ratio=%.2f peak=%s before_Jul2=%s  baseline_from=%s" %
              (pre5.mean(), cri5.mean(), cri5.mean() / pre5.mean(), str(pk5.date()),
               "YES" if pk5 < CRISIS_START else "NO", dates5.min().date()))
    else:
        print("cache starts %s (no pre-1996 data) -> skip long-baseline test" % dates5.min().date())
except Exception as e:
    print("skip:", type(e).__name__, str(e)[:50])
