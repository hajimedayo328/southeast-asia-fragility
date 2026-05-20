# Southeast Asia as a Predictive Mirror

**東南アジアの脆弱性は先進国の予言である**
— 圏論×グラフ理論によるリスク構造の可視化

賈伊陽研究室（東京都市大学）持ち込み用プロジェクト

公開デモ: https://hajimedayo328.github.io/southeast-asia-fragility/

---

## 1行ピッチ

東南アジアのインフラ・社会システムは「便利な経路」を急速に作り上げている。
しかしその裏には**見えない依存コスト**（信頼集中、冗長性削除、義理の借り）が必ず貼り付く。
本プロジェクトは、この**「便利と不可視コストの随伴 L ⊣ R」**を圏論的に定式化し、
ASEAN10カ国の実データで可視化する。

最終的に **「東南アジアの脆弱性パターンは先進国の将来リスクの予言である」** という洞察に繋げる。

## 中心の問い

1. 東南アジアの機能ネットワークで、**見えない依存コスト**はどこに貼り付いているか?
2. 東南アジアの脆弱性パターンは、**先進国の将来リスク**として転用可能か?

## 圏論的コア道具

- **随伴 (adjunction) `L ⊣ R`**: 便利 (左随伴) と不可視コスト (右随伴) のペア
- **Heyting代数 / 直観主義論理**: 「証拠ベースで存在する」状態を扱う（漏れの許容）
- 補助: Grothendieck fibration (国ファイバー), 2-cell (リープフロッグ)

## 実証する事例

- **モバイル金融** (Bakong / GCash / MoMo / PromptPay) — 国〜地域スケール
- **災害時の都市インフラ** (ジャカルタ / ハノイ / マニラ) — 街〜国スケール

## このリポジトリの構成

```
southeast-asia-fragility/
├── README.md                ← この1ページ
├── docs/                    ← GitHub Pages公開
│   ├── index.html          ← スクロール型可視化
│   ├── style.css
│   ├── js/viz.js
│   └── data/                ← 公開データ取得結果
│       ├── A_findex.json    ← World Bank Findex
│       ├── B_concentration.json ← モバイル決済集中度
│       ├── C_disasters.json ← EM-DAT災害データ
│       ├── D_remittance.json ← World Bank送金
│       ├── E_comparison.json ← ASEAN比較指標
│       └── seed.csv         ← 80セル機能スケルトン
├── notes/                   ← 理論ノート
│   ├── 01_pitch.md         ← 賈先生向けピッチ
│   ├── 02_framework.md     ← 圏論的枠組み
│   ├── 03_cases/           ← 事例詳細
│   └── 04_directions.md    ← 深掘り方向
└── literature/              ← 文献サーベイ (76本)
```

## 現在の進捗

- [x] 圏論的枠組み draft v1
- [x] 文献サーベイ 76本
- [x] ASEAN10×8機能 スケルトンデータ
- [x] 5軸の公開データ取得
- [x] スクロール型可視化 HTML
- [ ] 賈先生フィードバック反映
- [ ] 実証深掘り

## 既存研究との位置づけ

詳細は `literature/validation/` を参照:
- **Jia, Floridi, Tohmé 2025** (Categorical Analysis of LLMs, arXiv:2512.09117)
  → 同じ枠組みを別ドメインに転用（向きを反転）
- **Oliver & Kuure 2026** (Category Theoretic Trust) → 信頼の Heyting 扱いを借りる
- **Buldyrev 2010** (Interdependent Networks) → 物理層の数学を借りる
- **Mutiso et al. 2025 Science** (Leapfrog 5 rules) → 列挙レベルの先行を形式化

## なぜ「東南アジア」か

- スケール跨ぎ (個人〜国〜地域) の動的変化が観察可能
- 多様性 (仏教/イスラム/キリスト教/社会主義) が同じ地域内に同居
- リープフロッグ実例が世界最密度
- 自然災害・気候変動の最前線
- **先進国の未来を先に経験している** 実験場

## 著者

東京都市大学 情報工学系 学部3年生
賈伊陽研究室 配属見込み (2026年5月時点)
