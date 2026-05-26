# Southeast Asia as a Predictive Mirror

**東南アジアの脆弱性は先進国の予言である**
— 圏論 × グラフ理論によるリスク構造の可視化

研究方向の整理・共有用プロジェクト (work in progress, draft)

公開デモ: https://hajimedayo328.github.io/southeast-asia-fragility/

---

## 1行ピッチ

東南アジアのインフラ・社会システムは「便利な経路」を急速に作り上げている。
しかしその裏には **見えない依存コスト** (信頼集中、冗長性削除、義理の借り) が必ず貼り付く。
本プロジェクトは、この **「便利と不可視コストの随伴 L ⊣ R」** を **Heyting値 Petri Net** で定式化し、
ASEAN モバイル金融 + AI 依存 + sheaf cohomology で可視化する。

最終的に **「東南アジアの脆弱性パターンは先進国の将来リスクの予言である」** という洞察に繋げる。

## 中心の問い

1. 東南アジアの機能ネットワークで、**見えない依存コスト**はどこに貼り付いているか?
2. 東南アジアの脆弱性パターンは、**先進国の将来リスク**として転用可能か?
3. それを **圏論的にどこまで厳密に書けるか** (関手 / 自然変換 / Kan 拡張 / モナド / 層)?

## 圏論的コア道具

- **随伴 (adjunction) `L ⊣ R`**: 便利 (左随伴) と不可視コスト (右随伴) のペア
- **Heyting 値 Petri Net (H-Petri Net)**: 4 段階 Heyting 代数 `⊥ < ⊤_priv < ⊤_bank < ⊤_pub`
- **Open Petri Net** (Baez-Master 2018) + **律速逆転** (Ghrist-Gould-Lopez 2024)
- **Writer H モナド**: 不可視コスト累積を Kleisli 圏で書く (notes/24)
- **Čech H¹ 層**: 局所→大域のリスク伝播 (notes/25)
- **翻訳関手 F: 𝓒_EA → 𝓒_Dev** + Kan 拡張: 5 予言ペアの自然性分類 (notes/26)

## 実証する事例

- **モバイル金融** (Bakong / PayNow / KBZPay / GCash) — 国〜地域スケール、4 backbone 比較
- **AI 依存** (ChatGPT / Claude / Llama / GovAI) — 同じ Heyting 階数が再現、Cloudflare 2025-11 cascade
- **1997 アジア通貨危機** — H¹ が 0 → 4 → 6 と階段上昇する sheaf-理論的指紋

## このリポジトリの構成

```
southeast-asia-fragility/
├── README.md                       ← この1ページ
├── docs/                           ← GitHub Pages 公開
│   ├── index.html                  ← 概観タブ (KEY FINDINGS 4 つ)
│   ├── finance.html                ← 金融タブ
│   ├── petri.html                  ← Petri net タブ (§P1-P8)
│   ├── temporal.html               ← 時間軸タブ (§T1-T11)
│   ├── style.css
│   ├── vendor/chart.umd.min.js    ← Chart.js v4.4.1 (ローカル, Tracking Prevention 回避)
│   ├── js/{viz,petri,temporal}.js
│   └── data/                       ← Python 実行結果の JSON
│       ├── petri_comparison.json   ← 金融 4 backbone (compare.py)
│       ├── ai_comparison.json      ← AI 4 backbone (compare_ai.py)
│       ├── trust_timeline.json     ← 時間関手 (trust_timeline.py)
│       ├── sheaf_h1.json           ← Čech H¹ (sheaf/cech.py)
│       └── writer_h.json           ← Writer H モナド (monad/writer_h.py)
├── src/h_petri/                    ← Python 実装
│   ├── core.py                     ← HPetriNet, Marking, FourLevelHA
│   ├── backbones/                  ← 金融 4 backbone (Bakong/PayNow/KBZPay/GCash)
│   ├── domains/ai_dependency.py    ← AI 4 backbone
│   ├── monad/writer_h.py           ← Writer H モナド
│   ├── sheaf/cech.py               ← Čech H¹
│   ├── centrality.py               ← 場所中心性 (TCC, BI, HCC, HHI-AC)
│   ├── trust_timeline.py           ← 時間関手 Trust: Time → H
│   ├── compare.py                  ← 金融比較ランナー
│   └── compare_ai.py               ← AI比較ランナー
├── notes/                          ← 理論ノート (26 本 + INDEX)
│   ├── 00_INDEX.md                 ← 全体地図
│   ├── 02_framework.md             ← ★★★ 随伴 L⊣R
│   ├── 05-07                       ← ★★★ Petri net 三本柱
│   ├── 15_bottleneck_reversal.md   ← ★★★ 律速逆転
│   ├── 17-23                       ← ★★★ 時間関手 / 異分野同型 / 予言ペア
│   └── 24-26                       ← ★★★ モナド / 層 / 翻訳関手 (圏論本気適用3層)
└── literature/                     ← 文献サーベイ
```

## 動かし方

```bash
# Python 3.14
cd src

# 金融 4 backbone 比較
python -m h_petri.compare

# AI 4 backbone + Cloudflare 2025-11 cascade
python -m h_petri.compare_ai

# Čech H¹ (1997 AFC + Cloudflare)
python -m h_petri.sheaf.cech

# Writer H モナド (Effect Accumulation Theorem)
python -m h_petri.monad.writer_h

# Pages ローカル確認
cd ../docs && python -m http.server 8767
# → http://localhost:8767/
```

## 現在の進捗

- [x] H-Petri Net 数学的定義 + Python 実装
- [x] 共通CPN 規約 (notes/07) + 4 金融 backbone 実装
- [x] 律速逆転定理 (notes/15, Ghrist-Gould-Lopez 2024 ベース)
- [x] 時間関手 Trust: Time → H + 予言ペア 5 本
- [x] AI 4 backbone (notes/18 異分野同型のコード検証)
- [x] Writer H モナド (notes/24 Effect Accumulation Theorem 構成的検証)
- [x] Čech H¹ sheaf (notes/25 1997-Cloudflare 同型)
- [x] 翻訳関手 F の strict/lax 分類 (notes/26)
- [x] Pages 4 タブ + 全結果可視化
- [ ] Open Petri Net 合成で ASEAN5 越境決済の数値検証 (notes/10)
- [ ] 場所中心性の Pages 可視化
- [ ] 外部レビュー反映

## 既存研究との位置づけ

- **Jia, Floridi, Tohmé 2025** (Categorical Analysis of LLMs, arXiv:2512.09117)
  → 同じ Kan 拡張ツールセットを別ドメインに転用
- **Baez & Master 2018** (Open Petri Nets, arXiv:1808.05415) → cospan-pushout 構造を借りる
- **Ghrist, Gould & Lopez 2024** (Lattice-Valued Bottleneck Duality, arXiv:2410.00315) → 律速逆転の数学的根拠
- **Oliver & Kuure 2026** (Category Theoretic Trust) → 信頼の Heyting 扱いを借りる
- **Buldyrev 2010** (Interdependent Networks) → 物理層の数学を借りる

## なぜ「東南アジア」か

- スケール跨ぎ (個人〜国〜地域) の動的変化が観察可能
- 多様性 (仏教/イスラム/キリスト教/社会主義) が同じ地域内に同居
- リープフロッグ実例が世界最密度
- 自然災害・気候変動の最前線
- **先進国の未来を先に経験している** 実験場

## 著者

学部 3 年生 (圏論 × グラフ理論を学習中)
