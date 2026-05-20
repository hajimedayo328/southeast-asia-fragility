# 論文構造抽出: Nolan, Pollard, Breiner, Anand, Subrahmanian (2020)
"Compositional Models for Power Systems"
arXiv:2009.06833 / Compositionality誌掲載 / NIST + UMD + CMU共著

> 注: 著者は Specker ではなく Nolan ほか（NIST チーム）。Pollard は Baez 系統の応用圏論研究者。
> ユーザー側で「Specker論文」と呼んでいた本論文を以下では便宜的に「本論文 (Nolan2020)」と呼ぶ。

---

## 0. 論文の全体構造

| Section | 内容 | 圏論の使い方 |
|---|---|---|
| §1 Introduction | Smart Grid の多モデル問題 | モチベーション |
| §2 Power flow problems | 配電問題のスキーマ化 | **categorical database (CQL)** |
| §2.1 Connecting to a tool | MATPOWERへの接続 | schema = 有限提示圏、instance = Set値関手 |
| §2.2 Connecting tools | ツール間翻訳 | **Σ_F, Δ_F, Π_F (随伴三項)**, query, colimit |
| §3 Distributed Energy Resources | DERのモデル化 | **DER という圏**を定義 |
| §3.1 Aggregation | DERの集約 | **対称モノイダル構造 ⊗** (定理7) |
| §4 Conclusions | 将来課題 | open Petri net, hypergraph cat, 2-cat への拡張示唆 |

---

## 1. 論文の圏論構造マップ

### 1.1 使われている圏

#### (a) 電力フロースキーマ圏 (Power flow schema, §2)
- **対象**: エンティティ型 `Bus, Branch, PQ Bus, PV Bus, Generator, Int, Float`
- **射**: 属性関数 + 外部キー (例: `Branch --s--> Bus`, `PQ Bus --PD--> Float`)
- **意味**: MATPOWER の入力テーブル構造を有限提示圏として書き下したもの
- **path equation 制約**: `s . BUS_I = F_BUS`, `t . BUS_I = T_BUS` (CQL で書ける)

#### (b) インスタンス圏 `S-Inst = [S, Set]` (§2)
- **対象**: schema `S` から `Set` への関手 (= 具体的なデータベース内容)
- **射**: 自然変換

#### (c) **DER 圏 `DER`** (§3, 定義3, 定義4) ← **論文の中心圏**
- **対象**: DER `D = (S, T, s, t, a, d)`
  - `S`: 有限集合 (状態集合: On/Off/Charging/...)
  - `T`: 有限集合 (遷移集合)
  - `s, t: T → S`: source / target
  - `a: S → T`: 各状態の自己ループ (reflexive graph の reflexivity)
  - `d: S → 2^ℂ`: **各状態に複素電力 (P + iQ) の許容領域**を割り当てる関数
- **射** `φ: D → D'` = `(φ_S, φ_T)` (グラフ準同型) で:
  - 自己ループを保つ: `φ(1_σ) = 1_{φ(σ)}`
  - 需要領域は **包含**: `d(σ) ⊆ d'(φ(σ))`  ← 粗視化 (coarse-graining) を表す

#### (d) `Gph` (reflexive graphs と graph homomorphism の圏)
- 補助的に登場。`U: DER → Gph` が忠実関手として証明に効く。

---

### 1.2 関手 (Functor)

| 関手 | 型 | 役割 |
|---|---|---|
| **Database instance** | `S → Set` | スキーマ → 具体データ |
| **Schema map** `F: S → T` | `S → T` (圏間) | モデル間マッピング |
| **Δ_F (pullback)** | `T-Inst → S-Inst` | データを汎用→特化方向へ「忘れる」 |
| **Σ_F (left Kan)** | `S-Inst → T-Inst` | データを左Kan拡張で「埋め込む」 |
| **Π_F (right Kan)** | `S-Inst → T-Inst` | データを右Kan拡張で「埋め込む」 |
| **eval(Q)** | `S-Inst → T-Inst` | クエリ Q の評価 |
| **coeval(Q)** | `T-Inst → S-Inst` | クエリ Q の **双対評価** (functorial data model の特長) |
| **U: DER → Gph** | 忘却関手 | DER から需要 d を忘れて元のグラフだけ取り出す。忠実 |
| **⊗: DER × DER → DER** | 双関手 (bifunctor) | DER 集約 (§3.1, 定義6) |
| **( ̄): D → D̄** | DER 内の射 | **net demand quotient**: 同じ需要を持つ状態を同一視 |

---

### 1.3 Symmetric monoidal category として何が表現されるか (定理7)

**主定理 (Theorem 7)**: `(DER, ⊗, I)` は対称モノイダル圏である。

#### ⊗ の意味
- **物理的には「並列接続による集約 (aggregation)」**
  - 2つの DER `D, D'` の積 `D ⊗ D'` は、両デバイスを **同時に独立して動かす** 仕組みを表す
  - 状態空間: `S × S'` (両方の状態のペア)
  - 遷移: 片方だけ動く遷移 `(τ, 1_{σ'})` が許される ← **並列性**
  - 需要: **ミンコフスキー和** `d(σ) + d'(σ') = {x + y : x ∈ d(σ), y ∈ d'(σ')}`
    - これは「総需要 = 各機器の需要の和（ベクトル領域として）」を表す
- **シリーズ接続(直列)ではない**。配電網レイヤーでは「同じバスにぶら下がる複数機器」の合算が本質。

#### 単位対象 `I`
- 1状態 σ、1自己ループ `1_σ`、需要 `d(σ) = {0} ⊆ ℂ` をもつ DER
- **「何も接続されていない仮想機器」「ゼロ需要」**を表す
- ミンコフスキー和の単位 `{0}` が monoidal unit に対応

#### 証明戦略
- `Gph` が有限積を持つので `×` で SMC
- `U: DER → Gph` が忠実 → `Gph` で可換な図式は `DER` でも可換
- associator/braiding/unitor はミンコフスキー和の結合・可換・単位律から自然に伸びる

---

### 1.4 Categorical database / acset の使い方

論文では Catlab.jl ではなく **CQL (Categorical Query Language)** を使っているが、構造は同じ:

#### スキーマ例 (Figure 2 を元に再構成)
```
Bus(BUS_I: Int, BUS_TYPE: Int)
Branch(F_BUS: Int, T_BUS: Int, s: Bus, t: Bus)
PQ Bus(BUS: Int, PD: Float, QD: Float)
PV Bus(BUS: Int, PD: Float, VM: Float)
Generator(BUS: Int, PG: Float, VM: Float)

path equations:
  s . BUS_I = F_BUS
  t . BUS_I = T_BUS
```
- これは AlgebraicJulia 流に書くと `@present SchPowerFlow(FreeSchema)` に直接対応する。

#### スキーマの 3 階層 (§2.1 - §2.2)
1. **Generic schema `G`** — 抽象的な power flow 仕様
2. **Specific solver schemas `S, S'`** — MATPOWER / GridLAB-D / Newton-Raphson などツール固有
3. **Auxiliary schema `A`** — generic に出てこないが保存したい属性 (実行時間、ソルバー設定など)

#### ツール間翻訳 (§2.2 の核心アルゴリズム)
```
S-Inst ─── eval(Q) ───> G-Inst ─── coeval(Q') ───> S'-Inst   (generic data path)
S-Inst ─── Δ_F ────> A-Inst ─── Σ_F' ─────> S'-Inst          (auxiliary data path)
       ↓ colimit (S'-Inst 内で結合)
   final S'-Inst
```
→ **CQL がコリミット計算機能を持っていることが kernel**

---

### 1.5 Wiring Diagram / Operad の使われ方

- **明示的な operad は登場しない**
- しかし対称モノイダル圏 `DER` 上では **string diagram (Joyal-Street [14], Selinger [21] 参照)** で集約を視覚化できる、と§3.1で述べられている
- 将来課題として §4 で「open Petri nets [Baez-Master]」「hypergraph categories [Fong]」「2-category 化 [Courser]」が示唆されている
- **本論文の wiring diagram は SMC の string diagram レベルで止まっている** (operad/decorated cospan までは行っていない)

---

### 1.6 中心構成 / 中心定理

| ラベル | 主張 |
|---|---|
| **Definition 1** | power flow graph: `R ←─g/b── E ─s/t→ N` |
| **Definition 2** | power balance equations (2\|N\|本の非線形方程式) |
| **Definition 3** | DER `D = (S, T, s, t, a, d)` |
| **Definition 4** | DER morphism: グラフ準同型 + 需要領域の包含 |
| **Definition 5** | ミンコフスキー和 `X + Y` (`2^ℂ` を可換モノイドにする) |
| **Definition 6** | テンソル積 `⊗: DER × DER → DER` (状態は積、需要はミンコフスキー和) |
| **Theorem 7** ★ | `(DER, ⊗, I)` は対称モノイダル圏 |
| **Definition 8** | **Net Demand Quotient `D̄`** — `d(σ) = d(σ')` で状態を同一視した商 |

#### Net Demand Quotient の正確な定義 (Def. 8)
- `S` 上に同値関係: `σ ∼ σ'  iff  d(σ) = d(σ')`
- `T` 上に誘導同値関係: `τ ≈ τ'  iff  s(τ) ∼ s(τ') ∧ t(τ) ∼ t(τ')`
- `D̄ := (S/∼, T/≈, s̄, t̄, ā, d̄)`
- 自然な射 `( ̄): D → D̄` を生む
- **配電レイヤーでは詳細状態は不要、純需要だけが本質** という観察を圏論的にエンコード

#### NDQ + 最短経路探索 (§3.1 末尾)
- `D̄` 上で BFS / Dijkstra を回して **「目的の純需要を達成する最小コスト遷移列」**を見つける
- これは Smart Grid の dynamic dispatching に直結

---

## 2. ASEAN Infra への転用マップ

ユーザーの「途上国インフラを圏論で扱う」プロジェクトに本論文の枠組みをマッピング:

| 本論文 (Nolan2020) | ASEAN多層インフラ (転用) |
|---|---|
| **DER = (状態S, 遷移T, 需要d)** | **インフラ機能ノード** = (運転状態, 状態遷移, 提供サービス量領域) |
| 状態 `σ` (On/Off/Charging) | 運用モード (通常運転 / 部分停止 / 災害時バックアップ / 計画停電) |
| 遷移 `T` | モード切替 (例: 雨季→ディーゼル発電に切替) |
| 需要領域 `d(σ) ⊆ ℂ` (P + iQ) | 多次元サービス量領域 (例: `(電力kWh, 給水L, 通信bps)` ⊆ ℝ^n) |
| **⊗ (集約・並列接続)** | 機能の並列提供 (電力 ⊗ 通信 ⊗ 給水 = 統合インフラパッケージ) |
| ミンコフスキー和 `d + d'` | **総供給能力 = 各機能の供給領域の和** (容量計画の合成) |
| 単位対象 `I` (ゼロ需要) | 「インフラ未整備地区」「ベースライン」 |
| DER射 `φ: D → D'` (粗視化) | 詳細モデル → 政策レベル要約 (例: 各村の発電実態 → 県レベル統計) |
| **Net Demand Quotient `D̄`** | 「同じサービス水準を提供する地区は同一視」= **政策単位への抽象化** |
| schema (CQL) | ASEAN各国・各機関のデータベース (PLN, EVN, EGAT等の異なるフォーマット) |
| Σ_F, Δ_F, Π_F | **国ごと/機関ごとのデータ変換** (タイGISフォーマット → ベトナム電力会社フォーマット) |
| generic schema `G` | **共通インフラ仕様** (ASEAN/ADB 標準) |
| specific schema `S` | 各国固有スキーマ (タイPEA, インドネシアPLN, ベトナムEVN ...) |
| auxiliary schema `A` | **国別保存属性** (補助金制度、料金体系、燃料種別) |
| colimit-based merge | 多国データを統合した汎ASEANビュー |

---

## 3. 転用ギャップ (本プロジェクトに足りないもの Top 3 + 2)

### Gap 1: **単一国/単一機能 → 多国多機能 → fibration / Grothendieck 構成が必要**
- 本論文: 単一の電力グリッド、単一国
- ASEAN: 複数国 × 複数機能 (電力・通信・給水・交通・金融包摂)
- **対策**: `Country → Cat` の Grothendieck fibration で「国ごとに異なる圏」を全体圏に貼り合わせる
- 関連文献: Spivak の polynomial functor / Patterson の "Algebra of database queries"

### Gap 2: **連続値領域 `2^ℂ` の集約 → 不確実性・確率分布の集約**
- 本論文: ミンコフスキー和は決定論的領域の和
- ASEAN: 災害発生確率、季節変動、人口統計 → **確率モノイダル圏 (Markov category, Stochastic relation)** が要る
- **対策**: Fritz の Markov category, Cho-Jacobs の stochastic relation を需要モデルに組み込む

### Gap 3: **wiring diagram レベル止まり → operad / open system が必要**
- 本論文: §4 で「open Petri net, hypergraph cat, 2-cat 化」を将来課題として明示
- ASEAN: 国境を跨ぐインフラ (メコン河水資源、ASEANパワーグリッド) → **open system の合成**
- **対策**: Baez-Pollard の open reaction network、Fong の decorated cospan、Courser の bicategory of decorated cospans を導入。本論文の参考文献 [3,4,9,12] がそのまま転用元。

### Gap 4: **同期 (instant snapshot) → 時間発展・スケジューリング**
- 本論文: ある瞬間の power flow が中心。動的計画は BFS/Dijkstra 程度
- ASEAN: 長期計画 (5年/10年)、季節循環、災害対応の時間軸が必須
- **対策**: 時間付き圏 (operadic temporal logic, copresheaves over time poset)、機械学習との結合

### Gap 5: **CQL ベース → AlgebraicJulia (Catlab.jl) への移植**
- 本論文の実装は CQL (Java) で書かれている (Categorical Informatics 製)
- 現代の標準は AlgebraicJulia / Catlab.jl + ACSets。コミュニティが活発で論文事例も多い
- **対策**: schema を `@present` で書き直す、acset で instance を持つ、AlgebraicRewriting.jl で書き換え規則を入れる

---

## 4. 本プロジェクトへの即時アクション提案

1. **Catlab.jl で本論文の DER 圏を再実装**
   - `@present SchDER(FreeSchema)` で `S, T, s, t, a, d` を定義
   - acset で具体的 DER を構築、`⊗` (categorical product on reflexive graphs + Minkowski sum) を実装
   - 論文の Fig.4 (デバイス故障モデル) を再現

2. **ASEAN メコン圏で「インフラ機能 DER」プロトタイプ**
   - 国 = `Thailand, Vietnam, Laos, Cambodia, Myanmar`
   - 機能 = `Electricity, Telecom, Water, Road`
   - 需要領域 d を ℂ ではなく ℝ^4 (4次元) に拡張、ミンコフスキー和を実装

3. **Grothendieck 構成で多国を貼り合わせ**
   - `B = ASEAN 国の圏 (射 = 越境協定)`
   - 各国 → `DER^k` 圏 (k = 機能数)
   - fibration として全体を表現 → 卒論の中心構成にできる

---

## 5. 主要参考文献 (本論文の引用、ASEAN転用に直接効くもの)

- [2] Baez-Fong "Compositional framework for passive linear networks" — 電力網の open system 化
- [3] Baez-Master "Open Petri nets" — 状態遷移系の open 合成
- [4] Baez-Pollard "Compositional framework for reaction networks" — 化学反応の op-cat、インフラに転用可
- [9] Courser "A bicategory of decorated cospans" — 2-cat 化
- [12] Fong "Decorated cospans" — open system 合成の基盤
- [20] Schultz-Spivak-Vasilakopoulou-Wisnesky "Algebraic Databases" — categorical DB の決定版
- [22] Spivak "Functorial data migration" — Σ_F/Δ_F/Π_F の原典
- [23] Stay-Meredith "Enriched Lawvere theories" — DER の reflexive graph 表現の元ネタ

---

## 6. ピンポイント引用 (再利用しやすい原文)

- §3 末: *"a category of distributed energy resources (DERs) as reflexive graphs equipped with power demand data, where morphisms can be viewed as model transformations or inclusions. This category admits a natural symmetric monoidal structure with DER aggregation as tensor product."*
- §3.1: *"This aggregation procedure, based on the category theoretic product of reflexive graphs ... serves as a symmetric monoidal product on DER. As a result, string diagrams can be used to reason about DERs and aggregation."*
- Thm.7 証明: `U: DER → Gph` を faithful 忘却関手として使うのが鍵 → 多国対応でも同じ戦略が有効
