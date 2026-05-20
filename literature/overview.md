# 06. 文献サーベイ統合レポート — 既存研究地図と「穴」

**作成日**: 2026-05-14
**収集件数**: 計 76本（軸① 19 / 軸② 13 / 軸③ 14 / 軸④ 15 / 軸⑤ 15）
**詳細ファイル**: `literature/01_*.md` 〜 `literature/05_*.md`

## 全体地図

5軸を直交配置し、本プロジェクトが立つ交差点を可視化:

```
                      [軸①] 圏論×システム
                    Specker 2020 (power)
                    Moeller-Vasilakopoulou 2020 (monoidal fibration)
                              │
[軸③] 多層ネットワーク ─── ★本プロジェクト ─── [軸⑤] Higher Cat 応用
Buldyrev 2010 / Bashan 2013         Jia 2025 (LLM fibration)
Danziger 2022                       Spivak Wiring Diagram系
                              │
                      [軸②] リープフロッグ拡散
                      Mutiso 2025 (5 rules)
                      Suri-Jack 2016 (M-Pesa)
                              │
                      [軸④] ASEAN事例
                      Bui 2023 Nat Comm (Dengue×infra×mobility)
                      Zhang 2024 (1055 dam DB)
                      Wang 2020 (航空網)
```

中心の★（本プロジェクト）は **5軸の交差点が無人地帯** であることが今回のサーベイで確認できた。

## 各軸の最重要論文 TOP 3 ずつ

### 軸① 圏論×システム
1. **Specker et al. 2020 "Compositional Models for Power Systems"** (arxiv 2009.06833)
   — Catlab.jl で電力系統に symmetric monoidal category 適用。**単一国・国比較なし・fibration なし**。本プロジェクトの差別化ポイントが明確。
2. **Moeller & Vasilakopoulou 2020 "Monoidal Grothendieck Construction"** (TAC 35-31)
   — `p: 𝓘 → 𝓒` を monoidal fibration として書く理論基盤。応用が network model 止まり。
3. **Sallach 2017 "Topos Modeling of Social Conflict"** (Springer)
   — Heyting代数で社会システム。賈先生研究と直結、実装が思弁段階で止まっている。

### 軸② リープフロッグ拡散
1. **Mutiso et al. 2025 "Five rules for technology leapfrogging in Africa"** (Science)
   — リープフロッグの5ルール、**形式化はしていない**。本プロジェクトの存在根拠論文。
2. **Suri & Jack 2016 "Long-run M-Pesa impact"** (Science)
   — エージェント密度の因果効果。ユーザー×エージェント二部グラフとして読み替え可能。
3. **Banerjee, Chandrasekhar, Duflo, Jackson 2013 "Diffusion of Microfinance"** (Science)
   — diffusion centrality 提案、コード公開。M-Pesa/ASEAN への移植が穴。

### 軸③ 多層・相互依存
1. **Danziger & Barabási 2022 "Recovery coupling"** (Nature Comm)
   — 米国電力数百万件の実データから新概念抽出。**「治る側」を扱う唯一級**。
2. **Tang et al. 2025 "I³ Model"** (arxiv 2503.02890)
   — 電力・道路・通信・建物の4層異種グラフ予測、AUC+31.94%。**北米限定、ASEAN空白**。
3. **Bashan-Berezin-Buldyrev-Havlin 2013** (Nature Phys)
   — 中間距離の依存リンクが最脆弱。**リープフロッグと正面衝突する仮説**。

### 軸④ ASEAN事例
1. **Bui et al. 2023** (Nature Comm) — ベトナムdengue×インフラ×人流の3層解析。**ベトナム派遣の出発点に最適**。
2. **Zhang 2024** — メコン1055ダムDB。Lancang-Mekong の最適化研究。
3. **IEA 2025 ASEAN Power Grid Report** — APGの政治的ボトルネック分析。

### 軸⑤ Higher Category 応用
1. **Jia & Floridi (& Tohmé) 2025 "Categorical Analysis of LLMs"** (arxiv 2512.09117)
   — **賈先生本人の論文。「人間ルート関手」vs「LLMルート関手」の並列構造がリープフロッグ=2-cellと直接同型**。
2. **Moeller-Vasilakopoulou 2020 Monoidal Grothendieck** (軸①と重複)
3. **Niu & Spivak 2023 "Polynomial Functors"** — 現代ACTの技術背景、open dynamical systems。

## 共通する「穴」の集約

5軸のサーベイで共通して指摘された穴を整理:

### 穴A: 「国×インフラ」を fibration で扱った応用例が存在しない
- 軸①（Specker等）と軸⑤（Moeller-Vasilakopoulou等）の両方から指摘。
- 理論はある、単一国応用もある、**両者を繋ぐ研究がない**。
- → 本プロジェクトの **最大の新規性候補**。

### 穴B: リープフロッグの圏論的（形式的）定義が存在しない
- 軸②（Mutiso 5ルール、Binz類型）も軸⑤も「列挙止まり」「形式化なし」と指摘。
- 「stage-skipping = 射の合成スキップ」「path-creating = 関手による圏の置換」という形式化は無人地帯。
- → **本プロジェクトの中心仮説 03_leapfrog_2cell.md が直接刺さる**。

### 穴C: 賈先生のLLM論文構造を別ドメインに移植した研究がない
- 軸⑤の最も強い発見。Jia & Floridi 2025 の「並列関手構造」を「途上国経路 vs 先進国経路」に置換すれば、ほぼそのままASEANインフラ論文の骨格になる。
- → **賈先生研究室内研究としての正当性が最も高い線**。

### 穴D: 多層インフラ研究の途上国データへの応用がほぼゼロ
- 軸③（Buldyrev以来15年）、軸④（ASEAN10多機能統合）の両方から。
- インドネシア電力の単層解析が1本あるだけ。
- → **実証パートとして手堅い**。

### 穴E: 「中間距離依存」とリープフロッグの衝突仮説が未検証
- Bashan 2013（中間距離脆弱）vs リープフロッグ実態（携帯基地局+ミニグリッドが中間距離をつなぐ）。
- **反直観仮説**: リープフロッグは脆弱性を増やす可能性。
- → 実証する価値が極めて高い。卒論〜修論サイズ。

### 穴F: モバイル金融の学術的ネットワーク分析がほぼない
- 軸②、軸④共通。GCash/MoMo/Bakong のグラフ構造研究が皆無。
- TAMモデル（質的アンケート）止まり。
- → **最も低コストで論文化できる線**（業界レポートはあるのでデータ二次利用可能）。

### 穴G: モバイル金融のBakong型 vs Super-app型のトポロジー比較
- 軸④で指摘。中銀backbone型（Bakong）vs プラットフォーム型（GoPay/GCash）の異種トポロジー比較は短編1本書ける匂い。

## ユーザーの draft 仮説の位置づけ

`01〜04` で書いた draft 仮説を、サーベイ後の地図に当てはめ直すと:

| draft仮説 | 既存研究との位置 | 評価 |
|------|------|------|
| 機能圏 𝓕 + 国の圏 𝓒 + 実装圏 𝓘 | Specker 2020（電力単独）+ Moeller-Vasilakopoulou 2020（fibration理論）の延長 | **正統な位置**。穴Aを埋める |
| Grothendieck fibration `p: 𝓘 → 𝓒` | 賈先生 Jia-Floridi 2025 と同型 | **穴Cを直接埋める** |
| リープフロッグ = 平行射の2-cell | Mutiso 2025 の5ルールを形式化 | **穴Bを直接埋める** |
| Heyting代数で「証拠ベースのインフラ存在」 | Sallach 2017 の延長、賈先生Heyting研究と直結 | 補助線として有効 |

→ **draft仮説は穴A, B, C を同時にカバーする**。これは想定以上に強いポジション。

## 注意点・リスク

1. **Mutiso 2025 (Science) の本文未取得**。WebFetch 403。大学経由で入手必要。
2. **賈先生Yiyang Jia の Google Scholar プロフィール未登録**。共著者経由で逆引きする必要。
3. **モバイル金融データは業界レポート中心** — 学術データセットが少ないため実証パートは慎重に。
4. **ASEAN多層データの公開は限定的** — Bui 2023 がベトナム3層を出したのは例外的、他国は手作業で構築要。

## 関連メモ参照

- `.agent/memory/MEMORY.md` のインフラグラフ探索（2026/4/17）と思考プロセス記録
- `.agent/memory/paper_thought_categorical_llm_2025-05-05.md`（賈先生LLM論文の深掘り、Jia-Floridi 2025の扱い）
- `.agent/memory/research_themes_2026-04-30.md`（研究テーマ全体整理）
