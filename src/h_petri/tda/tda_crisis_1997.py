"""1997アジア通貨危機を persistent homology (TDA) で実データ検証する。

目的: temporal タブで「手置き」した Cech H1 のタイムライン(0->4->6, 1996/12->97/7->97/12)が、
      実データ由来の persistent H1 でも「危機前に立ち上がる」という現象として再現するか。

重要な但し書き(捏造防止・過大主張防止):
  - 圏論版 H1 = 各国 Trust 値の sheaf 上の Cech コホモロジー(手置き値・ネットワーク上の穴)。
  - 本スクリプトの H1 = 各国日次リターンを点とした Vietoris-Rips 複体の persistent H1(幾何的な穴)。
  -> 「同じ H1」だが構成は別物。主張するのは "両方とも崩壊前に上がるか" という現象の一致だけ。
  - 値はすべて実データから計算したものだけを出力する。前兆が出なければ「出なかった」と書く。

手法: Gidea-Katz (arXiv:1703.04385) に倣う。
  各日 = d 指数の対数リターンのベクトル(R^d の点)。長さ w 日のスライディング窓で w 点の点群。
  ripser で H1 を計算し、寿命(death-birth)の L2 ノルムを「その日の H1 強度」とする。
"""
import os, json
import numpy as np
import pandas as pd
import yfinance as yf
from ripser import ripser
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import japanize_matplotlib  # noqa: F401

OUT = os.path.dirname(os.path.abspath(__file__))

# 1997当事国: 圏論版の6カ国(TH,ID,KR,MY,PH,SG) + 香港(HK)。
TICKERS = {"TH": "^SET.BK", "ID": "^JKSE", "KR": "^KS11",
           "MY": "^KLSE", "PH": "PSEI.PS", "SG": "^STI", "HK": "^HSI"}
START, END = "1996-01-01", "1999-12-31"
WINDOW = 50  # 取引日

# 参照イベント(史実・チャートの目印。計算結果ではない)
EVENTS = [("1997-07-02", "タイ変動相場制移行"),
          ("1997-10-23", "香港株急落"),
          ("1997-12-03", "韓国IMF合意")]


def load_prices():
    cache = os.path.join(OUT, "indices_close.csv")
    if os.path.exists(cache):
        return pd.read_csv(cache, index_col=0, parse_dates=True)
    series = {}
    for k, tk in TICKERS.items():
        df = yf.download(tk, start=START, end=END, progress=False, auto_adjust=True)
        s = df["Close"]
        if isinstance(s, pd.DataFrame):   # yfinance が MultiIndex 列で返す場合に対応
            s = s.iloc[:, 0]
        series[k] = pd.Series(s.values.ravel(), index=s.index, name=k)
    px = pd.DataFrame(series)
    px.to_csv(cache)
    return px


def main():
    px = load_prices()
    px = px[list(TICKERS.keys())].dropna()  # 全国そろった日だけ(共通期間)
    print(f"共通期間: {px.index.min().date()} 〜 {px.index.max().date()}  N={len(px)} 日")
    print(f"指数: {list(px.columns)}")

    ret = np.log(px / px.shift(1)).dropna()
    dates = pd.to_datetime(ret.index)
    X = ret.values
    n, d = X.shape

    centers, norms, n_loops = [], [], []
    for i in range(n - WINDOW + 1):
        cloud = X[i:i + WINDOW]                 # (w, d)
        h1 = ripser(cloud, maxdim=1)["dgms"][1]
        if len(h1) == 0:
            L2 = 0.0
        else:
            life = h1[:, 1] - h1[:, 0]
            life = life[np.isfinite(life)]
            L2 = float(np.sqrt((life ** 2).sum()))
        centers.append(dates[i + WINDOW - 1])   # 窓の末日に対応づけ
        norms.append(L2)
        n_loops.append(int(len(h1)))

    centers = pd.to_datetime(centers)
    norms = np.array(norms)

    # JSON出力(実測値のみ)
    out = [{"date": str(c.date()), "h1_l2": round(v, 6), "n_loops": k}
           for c, v, k in zip(centers, norms, n_loops)]
    json.dump({"window": WINDOW, "countries": list(px.columns),
               "method": "Gidea-Katz sliding-window Vietoris-Rips H1 L2",
               "series": out},
              open(os.path.join(OUT, "tda_1997_h1.json"), "w"), indent=1)

    # 平穏 vs 危機 の比較(前兆が立つか)
    def window_mean(a, b):
        m = (centers >= pd.Timestamp(a)) & (centers < pd.Timestamp(b))
        return float(norms[m].mean()) if m.any() else float("nan"), int(m.sum())

    pre, npre = window_mean("1997-01-01", "1997-07-01")    # 崩壊前(平穏)
    cri, ncri = window_mean("1997-07-01", "1998-03-01")    # 危機本体
    peak_i = int(np.argmax(norms))
    print("-" * 60)
    print(f"1997上半期(崩壊前) H1-L2 平均 = {pre:.4f}  (n={npre})")
    print(f"危機期 97/7-98/2    H1-L2 平均 = {cri:.4f}  (n={ncri})")
    if pre and not np.isnan(pre) and pre > 0:
        print(f"  -> 危機/平穏 比 = {cri / pre:.2f}x")
    print(f"H1-L2 のピーク: {centers[peak_i].date()}  値={norms[peak_i]:.4f}")

    # プロット
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(centers, norms, lw=1.3, color="#dc2626")
    ax.fill_between(centers, 0, norms, color="#dc2626", alpha=0.08)
    ymax = norms.max() * 1.05
    for ev, lab in EVENTS:
        t = pd.Timestamp(ev)
        ax.axvline(t, ls="--", lw=0.9, color="#555")
        ax.text(t, ymax * 0.97, lab, rotation=90, va="top", ha="right", fontsize=8, color="#333")
    ax.set_title(f"1997アジア危機 — persistent H1 の L2ノルム (窓{WINDOW}取引日 · {d}指数の対数リターン)")
    ax.set_ylabel("persistent H1  L2(寿命)")
    ax.set_xlabel("日付（窓の末日）")
    ax.set_ylim(0, ymax)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "tda_1997_h1.png"), dpi=120)
    print(f"saved: tda_1997_h1.json / tda_1997_h1.png")


if __name__ == "__main__":
    main()
