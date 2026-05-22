# 05. Petri net 理論ノート — 5つの主張と厳密化方針

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: 既存の `02_framework.md` (随伴 L ⊣ R) を Petri net 上に具体化するための理論詰め

## なぜ Petri net か

「決済システム/インフラを圏論で扱う」と言ったとき、抽象的な対象・射のままだと
「で、具体的に計算は?」になる。Petri net は:

1. **並行性の数学** — 並列発火を厳密に扱える
2. **モノイダル圏の生成元** — 自由対称モノイダル圏を構文で書ける
3. **計算可能** — 到達可能性、不変量、ホットスポット抽出が algorithmic に決まる
4. **Baez-Master 系で圏論的整理が完了** — ACT コミュニティの中心軸

つまり 02_framework で立てた「随伴 L ⊣ R」を Petri net で書き直すと:
- 抽象的だった「便利と不可視コストのペア」が **具体的なグラフ + トークン流** に降りる
- 計算可能 (= 賈先生に「動く」と見せられる)
- 既存研究 (Baez-Master) の上に乗れる

---

## §1 Petri net の基礎 (30秒整理)

### 構成要素
- **場所 (places)** `P = {p_1, p_2, ...}` 〇 で描く
- **遷移 (transitions)** `T = {t_1, t_2, ...}` □ で描く
- **フロー関係** `F ⊆ (P × T) ∪ (T × P)`
- **マーキング (marking)** `M: P → ℕ` (各場所のトークン数)

### 発火規則 (firing rule)
遷移 `t` は、`t` の前置場所すべてに十分なトークンがあるとき **発火可能 (enabled)**。
発火すると:
- 前置場所からトークンを取る
- 後置場所にトークンを入れる

### 派生概念
- **到達可能性 (reachability)**: 初期マーキング `M_0` から `M` に到達できるか
- **P-invariant**: 重み付き合計が遷移で不変な場所集合 → 保存量
- **T-invariant**: 発火列が初期状態に戻る → サイクル
- **デッドロック**: 全遷移が発火不能
- **活性 (liveness)**: 任意マーキングから任意遷移が発火可能に戻れる

### 拡張版
- **Colored Petri Net (CPN)**: トークンに型を持たせる
- **Stochastic Petri Net (SPN)**: 発火に確率分布を割り当てる
- **Open Petri Net**: 入出力ポートで他のPNと合成可能
- **Hyper Petri Net**: フロー関係を超グラフ化

---

## §2 Petri net の圏論的位置づけ

### Meseguer-Montanari 1990 "Petri Nets are Monoids"
- Petri net = **自由可換モノイドの上のグラフ**
- マーキング = モノイド元 (場所の自由可換モノイド)
- 発火 = モノイド演算 (+) と関連

### Joyal-Street 1991 / Sassone系
- Petri net の **実行は string diagram** として描ける
- これがモノイダル圏との明示的接続

### Baez & Master 2018 "Open Petri Nets" (arXiv 1808.05415)
- Petri net を **cospan** で構成 → 組み合わせ可能 (composable)
- 入力ポート + 内部 + 出力ポートの3要素
- ASEAN 各国の決済システムをポート経由で **合成可能なシステム** として扱う根拠
- **本プロジェクトの直接の出発点**

### AlgebraicPetri.jl (Catlab.jl の Petri net 拡張)
- Patterson, Halter らによる実装
- ACSets (Attributed C-Sets) 上に Petri net を実装
- 直接動かして実験可能

---

## §3 本プロジェクトでの主張 5つ

### 主張1: リープフロッグ可能性 = Petri net の reachability

**主張**:
> 機能 `X` がリープフロッグ可能 ⇔ Petri net `(P, T, F)` において、
> 「先進国経路ノード集合 `R_adv ⊂ P` のトークンを使わずに、
> 初期マーキング `M_0` から `送金完了` マーキング `M_done` に到達する遷移列が存在する」

**形式化候補**:
- 部分マーキング `M|_{P ∖ R_adv}` 上の reachability
- `R_adv` の場所を「使うと違反」とラベル付けし、違反なしで到達可能か判定

**計算可能性**:
- 一般の Petri net reachability は EXPSPACE
- でも本プロジェクトで使うのは bounded Petri net 想定 → PSPACE / 実用的に多項式

**直接的な利点**:
- 02_framework の「平行射の2-cell」が **具体的な遷移列の存在問題** に降りる
- アルゴリズムで自動判定可能 (高校生にも見せられる)
- ASEAN10 各国の Petri net で実例計算

### 主張2: 不可視コスト = 補助場所 (auxiliary places)

**主張**:
> 各「便利な遷移」`t` の発火時、可視層 (L) のトークン流に加え、
> **不可視層 (R) の補助場所** `p_aux^t` にトークンが +1 加算される。
> この補助場所群が随伴 L ⊣ R の R 側 (右随伴) の具体的位置に対応する。

**形式化候補**:
- Petri net `(P, T, F)` を **2層拡張**: `P = P_visible ⊔ P_invisible`
- 各 `t ∈ T` に対し、`F(t, p_aux) > 0` for some `p_aux ∈ P_invisible`
- 補助場所はトークンが **減らない** (monotone)

**具体例**:
- 「Bakong送金完了」遷移発火のたびに、「NBC信頼依存」場所に +1
- 「GCash送金完了」遷移発火のたびに、「Globe Telecom信頼依存」場所に +1
- 送金回数 = 信頼依存トークン累積 (累積負債が可視化される)

**理論的含意**:
- 不可視コストが Petri net の **構造として明示される**
- グラフを見るだけで「どの遷移が何にコストを払うか」がわかる

### 主張3: backbone タイプ = 構造的不変量 (P/T-invariant)

**主張**:
> ASEAN10各国の決済 Petri net は、**P-invariant と T-invariant の組み合わせ** で
> 4 backbone タイプに分類できる:
> - 中央銀行型 (TH/KH): すべての遷移が中銀場所を経由する強い P-invariant
> - 民間型 (VN/ID/PH/MY): 特定プラットフォーム場所の単一ホットスポット
> - 銀行型 (SG/LA/MM/BN): 多数の銀行場所への分散
> - 電話会社型 (絶滅): telco場所中心の単一依存

**形式化候補**:
- 各国の Petri net を構築
- P-invariant `x: P → ℤ` を計算 (`x^T C = 0` where C はインシデンス行列)
- T-invariant も同様
- 不変量の構造的特徴 (rank, support) でタイプを区別

**根拠**:
- 既存研究 (前の Chart.js 4タイプ分類) は **業界レポートからの主観分類**
- これを **構造的不変量** で正当化すれば、数学的根拠を持つ分類になる

### 主張4: 集中度 = Petri net のホットスポット (場所中心性)

**主張**:
> 「すべての遷移列が経由する場所」を **ホットスポット** と定義。
> Petri net の構造から自動抽出可能。
> 民間型 (GCash, MoMo) ではホットスポットが少数の場所に集中、
> 中銀型 (Bakong, PromptPay) では分散。

**形式化候補**:
- 場所の **betweenness centrality** (Petri net 版): 全遷移列のうち、その場所を経由するものの比率
- 場所の **eigenvector centrality** (フロー行列の主固有ベクトル)
- 場所の **bottleneck index**: その場所がデッドロックを引き起こす確率

**HHI との接続**:
- 前のChart.js でやった HHI (集中度) を Petri net 上で再定義
- 業界統計から推定するのではなく、**システム構造から計算** できる

### 主張5: 域内決済合成 = Open Petri Net の合成

**主張**:
> ASEAN5 (TH/SG/MY/ID/PH) の決済システムは、各国 Petri net を
> **Open Petri Net** (Baez-Master 2018) のcospan合成で接続することで、
> ASEAN 域内決済システム全体を構築できる。

**形式化候補**:
- 各国の決済 Petri net を Open Petri Net として書く (入出力ポート付き)
- 越境決済プロトコル (PromptPay-PayNow, QRIS-DuitNow 等) をポート間の射として
- 合成は cospan の pushout で計算

**新規性**:
- Baez-Master 2018 は理論論文。**ASEAN実例で構築した研究はおそらくない** (要検証 → サーベイ中)
- 賈先生研究 (モノイダル圏) との直接接続点

---

## §4 各主張の数学的厳密化方針

### 主張1 厳密化
- **問1**: 部分マーキング reachability の判定アルゴリズムを実装する
- **問2**: ASEAN3カ国 (VN/PH/TH) で実例計算
- **問3**: NP完全性 or 多項式可解性 の議論
- **方針**: AlgebraicPetri.jl で 5-10 場所規模の Petri net を構築 → reachability 計算

### 主張2 厳密化
- **問1**: 2層Petri net (P_visible + P_invisible) は通常Petri netに還元可能か?
- **問2**: 補助場所がmonotoneである場合の不変量
- **問3**: 補助場所のトークン累積を「コスト指標」として定量化
- **方針**: 標準 Petri net の拡張として定式化 → 理論性質を導く

### 主張3 厳密化
- **問1**: 各 backbone タイプの P/T-invariant を計算
- **問2**: 不変量の構造的特徴 (rank, support) で型分類
- **問3**: 業界統計分類 (前のChart.js) との一致度
- **方針**: 各国 Petri net を構築 → invariant を計算 → タイプ識別

### 主張4 厳密化
- **問1**: 場所中心性指標 (betweenness, eigenvector) を Petri net 上で定義
- **問2**: 既存ネットワーク中心性との関係
- **問3**: HHI との数値比較
- **方針**: 場所中心性アルゴリズム実装 → ASEAN10 で計算 → HHI と比較

### 主張5 厳密化
- **問1**: 各国 Petri net を Open Petri Net として書き直す
- **問2**: 越境決済をポート射として定式化
- **問3**: cospan-pushout 合成の数値計算
- **方針**: Baez-Master 2018 を読み込み、AlgebraicPetri.jl の open net 機能を使う

---

## §5 関連研究との接続

### Jia (2022-23) Strip Folding as Monoidal Category
- 折る操作 = モノイダル圏の射
- Petri net の遷移 = モノイダル圏の射
- → **遷移合成 ≡ 折り操作合成** という構造的同型
- 折り紙の「折り順」と Petri net の「発火列」が対応

### Jia (2024) Heyting Algebra in Flat Origami
- **Heyting値 Petri net** という拡張があるか? (サーベイ中)
- 場所のトークン値を Heyting代数値にすると、「証拠ベースのインフラ存在」を Petri net で扱える
- 普通の Petri net (ℕ値) vs Heyting値 Petri net (証拠強度値)
- これがゼロなら独自貢献候補

### Jia, Floridi, Tohmé (2025) Categorical Analysis of LLMs
- 人間ルート関手 vs LLM ルート関手 (Rel 上の射の並列)
- Petri net 化: 2つの並列発火経路として書ける
- 右Kan拡張 = ホットスポット場所の特性関数
- → LLM論文の構造を **動く Petri net** にできる

### Baez & Master (2018) Open Petri Nets
- 本プロジェクトの直接の出発点
- cospan による合成
- ASEAN域内決済の数学的基盤

---

## §6 自分で詰める論点 (未解決)

提出するわけじゃない、自分で答えを出すべき問い:

1. **2層 Petri net (可視層+不可視層) は標準Petri netに還元可能か?**
   - 還元可能なら理論的に新規性なし、ただ実用的に便利
   - 還元不可なら新規拡張として独立価値
2. **Heyting値 Petri net は文献にあるか?**
   - 6本目のサーベイ結果待ち
   - ゼロなら独自貢献候補 (Jia 2024 直接接続)
3. **リープフロッグの「経路disjoint」を Petri net でどう書くか?**
   - 単純に「経由しない」だけだと弱い
   - 「経路の本質的に異なる」を圏論的に定義したい
4. **ASEAN3カ国の Petri net を実装する規模感**
   - 5-10場所、10-20遷移で十分か
   - もっと細かくしないと現実が反映されないか
5. **AlgebraicPetri.jl の学習コスト**
   - Julia は触ったことがない (MEMORYでC++/Python中心)
   - Catlab.jl の習得時間 → ROI判断要
6. **市場時系列 (Tick Recorder) と Petri net は接続不能か?**
   - 連続時系列にトークン離散モデルを乗せるのは無理
   - でも「市場体制 (Bull/Bear/Range) の遷移」なら Petri net で書けるかも
   - 別研究テーマとして検討

---

## §7 当面のアクションリスト

### 短期 (今週)
1. サーベイ06_petri_net_categorical.md と 07_petri_net_payment_apps.md の結果統合
2. Heyting値 Petri net の存否確認 → 独自貢献の有無を決定
3. 主張1〜5 のうち最も筋がいいものを選定 (たぶん主張1か主張5)

### 中期 (今月)
4. 主張1: ASEAN3カ国 (VN/PH/TH) の決済 Petri net を 5-10場所スケールで構築
5. 主張1: AlgebraicPetri.jl or 自作Python で reachability 計算
6. 主張3: P-invariant を実例計算

### 長期 (3ヶ月)
7. 主張5: Baez-Master 2018 を読み込み、Open Petri Net を ASEAN5に実装
8. 主張4: 場所中心性アルゴリズムを実装、HHIと数値比較
9. 既存の southeast-asia-fragility の HTML に Petri net セクション追加 (理論固まったあと)

---

## §8 既存研究の借用関係 (整理)

| 借用元 | 何を借りるか |
|---|---|
| Petri 1962 | 基本定義 |
| Meseguer-Montanari 1990 | モノイド構造 |
| Baez-Master 2018 | Open Petri Net, cospan合成 |
| AlgebraicPetri.jl | 実装フレームワーク |
| Jia 2022-23 | モノイダル圏での操作合成 |
| Jia 2024 | Heyting値拡張の発想 |
| Jia-Floridi 2025 | 並列ルート関手の構造 |

借用する研究を明示することで、「単なる移植」じゃなく「先行研究の組合せ + 独自拡張」のスタンスを取る。

---

## §9 リスク評価

- **R1**: 主張1〜5 が全て既存研究にあって新規性ゼロ → サーベイ次第。穴を埋めるならOK
- **R2**: Julia (Catlab.jl) 学習コスト高くて手が止まる → Python自作で代替 (NetworkXベース)
- **R3**: ASEAN実例構築でデータ不足 → 既存の docs/data/ + 業界レポートで補完
- **R4**: Heyting値 Petri net が既出 → 直接の独自貢献は減るが、ASEAN応用で残せる

---

## §10 ノートの位置づけ

これは draft v1。確定じゃない。
今後の検証で:
- 主張のうち成立しないものを削除
- 新しい主張を追加
- 数式の厳密化を進める

論文書く気は今はない。これは「自分が後で迷わないための地図」。
