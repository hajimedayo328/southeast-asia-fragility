"""ファンダメンタルズ層別 TDA — 圏論版の前兆化をTDAで試す。

圏論版(§P6-C): 市場可視H1は同時指標。短期外債/外貨準備(Guidotti-Greenspan比率,1997-06,RBA/BIS)
  脆弱 V(>1): KR 3.0 / ID 1.6 / TH 1.1 ,  健全 S(<1): MY 0.6 / PH 0.7 (SG 健全と仮定)
を入れると「名目0/実態調整6」で前兆化した。不整合は脆弱/健全の境界に乗る。

TDA版の問い: ファンダで国を V群/S群に層別すると、V群の persistent H1 が崩壊前に S群より動くか。
  さらに vol標準化しても V群の前兆が残るか(vol由来でないか)。
出力ASCII。値は実計算のみ。出なければ「出ない」と書く。
"""
import os
import numpy as np
import pandas as pd
from ripser import ripser

OUT = os.path.dirname(os.path.abspath(__file__))
CRISIS = pd.Timestamp("1997-07-02")
GROUPS = {"V_fragile(KR,ID,TH)": ["KR", "ID", "TH"],
          "S_sound(MY,PH,SG)":   ["MY", "PH", "SG"]}


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


px = pd.read_csv(os.path.join(OUT, "indices_close.csv"), index_col=0, parse_dates=True)

print("=== fundamental layering: fragile (debt/reserves>1) vs sound ===")
print("%-22s %-13s %8s %8s %7s %12s %6s" %
      ("group", "variant", "calm", "crisis", "ratio", "peak", "pre?"))
results = {}
for gname, cols in GROUPS.items():
    sub = px[cols].dropna()
    ret = np.log(sub / sub.shift(1)).dropna()
    variants = {"raw": ret, "vol_adj": (ret / ret.rolling(20).std()).dropna()}
    for vname, R in variants.items():
        dates = pd.to_datetime(R.index)
        centers, L2 = h1_L2(dates, R.values, 50)
        pre, cri = split(centers, L2)
        ratio = cri.mean() / pre.mean() if pre.mean() > 0 else float("nan")
        pk = centers[int(np.argmax(L2))]
        results[(gname, vname)] = (centers, L2, pre, cri)
        print("%-22s %-13s %8.4f %8.4f %7.2f %12s %6s" %
              (gname, vname, pre.mean(), cri.mean(), ratio, str(pk.date()),
               "YES" if pk < CRISIS else "NO"))

# 核心の問い: 崩壊前(1997上半期)に V群の L2 が S群より高いか(脆弱が先に構造ストレス)
print("\n=== key test: pre-crisis (1997 H1) V vs S, raw ===")
for vname in ["raw", "vol_adj"]:
    _, _, preV, _ = results[("V_fragile(KR,ID,TH)", vname)]
    _, _, preS, _ = results[("S_sound(MY,PH,SG)", vname)]
    rel = preV.mean() / preS.mean() if preS.mean() > 0 else float("nan")
    print("%-8s pre-crisis  V=%.4f  S=%.4f  V/S=%.2f  %s" %
          (vname, preV.mean(), preS.mean(), rel,
           "V higher (fragile shows earlier stress)" if rel > 1.1 else
           "no clear V>S separation"))

# change-point: V群 raw が平穏baselineを持続的に超える日 vs 崩壊
print("\n=== change-point: V group raw, sustained breakout (>=10d) vs 1997-07-02 ===")
centers, L2, preV, _ = results[("V_fragile(KR,ID,TH)", "raw")]
thr = preV.mean() + 2 * preV.std()
above = (L2 > thr).astype(int)
run = 0
start = None
for idx, (c, a) in enumerate(zip(centers, above)):
    run = run + 1 if a else 0
    if run >= 10 and start is None and c >= pd.Timestamp("1997-01-01"):
        start = centers[idx - 9]
        break
if start is not None:
    print("V sustained breakout = %s (%+d days vs crisis) -> %s" %
          (str(start.date()), -(CRISIS - start).days,
           "BEFORE crisis (precursor!)" if start < CRISIS else "AT/AFTER onset (still no precursor)"))
else:
    print("no sustained breakout")
