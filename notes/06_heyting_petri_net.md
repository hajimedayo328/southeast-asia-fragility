# 06. Heyting値 Petri net の数学的厳密化

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: `05_petri_net_theory.md` の主張2-v2 の中核を厳密に書ききるノート

## §1 動機 — なぜ Heyting値か

### 標準 Petri net の限界

標準 Petri net (P/T Net) は場所のトークンを `ℕ` (自然数) で扱う。これは:
- 「あるか、ないか」「何個か」の **離散・二値・量的** な思考
- 「決済が完了した、未完了」のような **on/off** 状態には適してる

しかし、本プロジェクトで扱う「不可視コスト」=「信頼累積」「証拠の蓄積」は:
- **連続的** (徐々に積もる)
- **累積的** (一度生まれた証拠は消えない)
- **質的多様性** (信頼の証拠は1種類じゃない、相互独立な証拠が複数)

これは `ℕ` の足し算より、**Heyting代数の ∨ (証拠の合体)** が自然に対応する。

### 既存研究 (06サーベイで確認)

- **線形論理 × Petri net** (Engberg-Winskel quantale, Brown-Gurr dialectica) は確立
- **直観主義論理 (Heyting代数) × Petri net** は文献ゼロ
- Jia (2024) "Heyting Algebra in Flat Origami" — 折り紙の数学に Heyting代数を導入する論文
- → これを Petri net に持ち込むのが本ノートの目標

---

## §2 数学的準備

### 2.1 Heyting代数

**定義**: Heyting代数 `H` は、束 (lattice) であって、各 `a, b ∈ H` に対して

```
a ∧ x ≤ b  ⟺  x ≤ (a → b)
```

を満たす **含意演算 `→`** が存在するもの。

**演算**:
- `∧` (meet, AND, 共通)
- `∨` (join, OR, 合体)
- `→` (implication, 含意)
- `⊥` (bottom, 偽, 証拠なし)
- `⊤` (top, 真, 完全な証拠)

**完備 Heyting代数 (cHa)**: 任意の部分集合に対する meet/join が存在 (= complete lattice + Heyting structure)。

### 2.2 例 (本プロジェクトで使う候補)

| 例 | H | 解釈 |
|---|---|---|
| 命題真偽 | `{⊥, ⊤}` | 二値 (Boolean) |
| 単位区間 | `[0, 1]` | 連続的な信頼度 |
| 開集合の束 | `O(X)` | 空間 X 上の証拠領域 |
| 関数空間 | `H^X` | X 上の関数として証拠 |
| 集合束 | `2^S` for S = 証拠集合 | どの証拠を持つかの集合 |

最も実用的なのは **`[0, 1]`** または **`2^S` (有限集合の冪集合)**。

### 2.3 直観主義論理との対応 (BHK解釈)

- `⊤` = 完全な証拠 (provable)
- `⊥` = 証拠なし (no proof)
- `a ∨ b` = a の証拠 ∪ b の証拠
- `a ∧ b` = a の証拠 ∩ b の証拠
- `a → b` = a を b に変換する関数
- `¬a := a → ⊥` = a があるなら矛盾、の意

**重要**: 二重否定除去 `¬¬a → a` は **成立しない** (古典論理との違い)。
これは「証拠がないことの証拠 ≠ 偽の証拠」を表す。

---

## §3 標準 Petri net の形式定義 (確認)

**定義**: P/T Petri net は四つ組 `N = (P, T, F, M_0)`:
- `P`: 場所の有限集合
- `T`: 遷移の有限集合 (P ∩ T = ∅)
- `F: (P × T) ∪ (T × P) → ℕ`: フロー関数
- `M_0: P → ℕ`: 初期マーキング

**発火規則**:
- `t ∈ T` が `M` で発火可能: `∀p ∈ P. M(p) ≥ F(p, t)`
- 発火後: `M'(p) = M(p) - F(p, t) + F(t, p)`

---

## §4 Heyting値 Petri net (H-Petri Net) の定義 ★中核

### 4.1 形式定義

**定義 (H-Petri Net)**: 完備Heyting代数 `H` をパラメータとして、H-Petri Net は

```
N = (P_v, P_h, T, F_v, F_h, M_0, H)
```

- `P_v`: 可視層の場所 (ℕ値、標準 Petri net と同じ)
- `P_h`: 不可視層の場所 (Heyting値)
- `T`: 遷移
- `F_v: (P_v × T) ∪ (T × P_v) → ℕ`: 可視層フロー
- `F_h: T × P_h → H`: 遷移発火による不可視場所への Heyting値増分
- `M_0`: 初期マーキング
  - `M_0|_{P_v}: P_v → ℕ`
  - `M_0|_{P_h}: P_h → H`
- `H`: 完備 Heyting代数

### 4.2 発火規則

遷移 `t ∈ T` が `M` で **発火可能** (enabled):
```
∀p ∈ P_v. M(p) ≥ F_v(p, t)
```

(発火可能性は可視層だけで決まる。不可視層はトリガーされる側、消費されない)

**発火後のマーキング `M'`**:
```
可視層:  M'(p_v) = M(p_v) - F_v(p_v, t) + F_v(t, p_v)   for p_v ∈ P_v
不可視層: M'(p_h) = M(p_h) ∨ F_h(t, p_h)                  for p_h ∈ P_h
```

### 4.3 核心ポイント

1. **不可視層は ∨ で更新** (足し算じゃなく合流) → 証拠の累積を表す
2. **不可視層のトークンは減らない** (monotone): `M'(p_h) ≥ M(p_h)` 常に成立
3. **可視層は標準 Petri net と同じ**: 互換性確保

---

## §5 主要性質

### 5.1 Monotonicity (証拠は減らない)

**命題**: 任意の発火列 `σ = t_1 t_2 ... t_n` について、結果のマーキング `M_n` は

```
∀p_h ∈ P_h. M_n(p_h) ≥ M_{n-1}(p_h) ≥ ... ≥ M_0(p_h)
```

**証明**: `∨` は Heyting代数の上の順序保存演算なので、各ステップで `M_{i+1}(p_h) = M_i(p_h) ∨ F_h(t_{i+1}, p_h) ≥ M_i(p_h)`。直接従う。 ∎

**意味**: 「信頼の累積」「証拠の蓄積」が **構造的に保証**される。標準 Petri net では発火で消費があるので証拠が「消える」可能性があったが、H-Petri net では絶対に消えない。

### 5.2 Reachability (到達可能性)

**問**: 与えられた `M_target` に到達する発火列 `σ` が存在するか?

- **可視層成分**: 標準 Petri net の reachability 問題 (EXPSPACE)
- **不可視層成分**: monotonicity から、任意の `M_h ≤ ⋁_{t ∈ σ} F_h(t, p_h)` が到達可能 (上限さえ越えれば良い)

**系**: 可視層の到達可能性が決まれば、不可視層の到達可能性は計算容易。
不可視層は「証拠の累積上限」を見るだけで判定できる。

### 5.3 リープフロッグ可能性 (主張1-応用)

**定義 (R-restricted reachability)**:
場所部分集合 `R ⊂ P_v` (「先進国経路」のノード) について、`R` のトークンを使わずに `M_0` から `M_target` に到達する発火列が存在するか。

```
σ = t_1 ... t_n   such that
∀i. ∀p_v ∈ R. M_{i-1}(p_v) ≥ F_v(p_v, t_i) は使わない条件
```

形式的には、`R` の場所に十分なトークンが既にあっても、発火列 `σ` が `R` を経由しない (= `pre(t_i) ∩ R = ∅` for all i) ようなものが存在するか。

**含意**: リープフロッグ可能性 = R-restricted reachability の存在判定 = 構成的アルゴリズム化可能。

---

## §6 標準 Petri net への還元性

H-Petri net は標準 Petri net に還元可能か? これは独自貢献の強度を決める論点。

### 6.1 ケース1: 有限 Heyting代数

`|H| < ∞` の場合:
- `H = {h_1, ..., h_n}` と列挙
- 各 `p_h ∈ P_h` を `n` 個の標準場所 `{p_h^{h_1}, ..., p_h^{h_n}}` に置換 (binary encoding)
- 発火規則を変換:
  - `F_h(t, p_h) = h_k` のとき、対応する `p_h^{h_k}` 場所にトークン +1
  - `∨` 演算は事前計算した変換テーブルで処理

→ **理論的に還元可能**、ただし場所数が `|H| × |P_h|` 倍にブローアップ。
実用的には扱える (オーダー数百〜数千場所まで)。

### 6.2 ケース2: 無限 Heyting代数

`|H| = ∞` の場合 (例: `H = O(X)` 開集合の束、`H = [0, 1]`):
- 場所数を有限にできない (連続的)
- 一般に標準 Petri net への還元 **不可能**

→ **新規拡張として独立した数学的価値**。
これが Jia (2024) Flat Origami の本来の使い方 (連続的な折り) に対応。

### 6.3 結論

- **有限 H**: 実用上 OK、ただし「単なる encoding 改善」のレベル
- **無限 H**: 新規拡張として独立価値、本プロジェクトの数学的中核

実装は有限 H で始め、理論議論は無限 H を視野に入れる、という両刀持ち。

---

## §7 最小例: Bakong (中銀型) vs GCash (民間型)

### 7.1 共通フォーマット (5場所5遷移、共通CPN規約)

両方とも以下の場所:
- `p1: UserWallet` (ℕ値、初期 100)
- `p2: SettlementLayer` (ℕ値、初期 0)
- `p3: RecipientWallet` (ℕ値、初期 0)
- `p_inv1: TrustHub` (Heyting値、初期 ⊥)
- `p_inv2: SystemicLoad` (Heyting値、初期 ⊥)

遷移:
- `t1: InitiateSend`
- `t2: BackboneClear`
- `t3: Settle`
- `t4: Reconciliation`
- `t5: AcknowledgeReceipt`

### 7.2 Bakong (中央銀行型)

`F_h(t, p_inv1) = ⊤` for all `t` (NBC backbone への信頼累積)
`F_h(t, p_inv2) = {nbc_load}` (NBC負荷の累積)

**特徴**:
- TrustHub: NBC 単一ノード
- 全遷移が NBC を経由
- 但し Hyperledger Iroha で BFT コンセンサスにより、技術的には分散
- → Bakong の Heyting値補助場所はすべて **NBC1点に集約**

### 7.3 GCash (民間プラットフォーム型)

`F_h(t, p_inv1) = ⊤` for all `t` (Globe Telecom Group への信頼累積)
`F_h(t, p_inv2) = {gcash_load, globe_load}` (二重ハブ負荷)

**特徴**:
- TrustHub: Globe Telecom Group + Ant Group + Mynt
- 単一企業 (Globe Telecom) が backbone
- → GCash の Heyting値補助場所は **Globe Telecom1点に集約**、しかも民間1社

### 7.4 構造的比較

| 観点 | Bakong | GCash |
|---|---|---|
| TrustHub の本性 | 公的機関 (NBC = 国家) | 民間企業 (Globe Telecom) |
| 法的保護 | 中央銀行法 | 私法契約 |
| 障害時の救済 | 国家責任 | 企業破産処理 |
| Heyting値の上限 | `⊤_{public}` (政府保証) | `⊤_{private}` (民間保証) |

→ 同じ Petri net 構造 (5場所5遷移) でも、Heyting値補助場所の **意味的内容** が完全に異なる。
これが「4 backbone 比較」の理論的基盤。

---

## §8 Jia (2024) Flat Origami との対応

### 8.1 Flat Origami の Heyting構造

Jia (2024) の Flat Origami:
- 折り紙の各折り目を Heyting代数の元として扱う
- 折る操作 = `∧, ∨, →` の組合せ
- 折り順の整合性 = Heyting代数の公理 (特に `(a → b) ∧ a ≤ b` 等)

### 8.2 H-Petri Net との対応

| Flat Origami (Jia 2024) | H-Petri Net (本プロジェクト) |
|---|---|
| 折り紙の現状態 | 不可視マーキング `M(P_h) ∈ H^{P_h}` |
| 折り操作 | 遷移発火 |
| 折り操作の合成 | 遷移列の合成 |
| 折り目の積み重ね | `∨` による証拠累積 |
| 折りの整合性 | 発火後のマーキングの well-defined |

→ **構造的同型**: 折り紙の数学と、モバイル金融信頼の数学は同じ Heyting代数枠組み。

これが本プロジェクトの数学的アクト: **「折り紙」と「金融」が同じ圏論的枠組みで記述できる**。

### 8.3 含意

- Jia (2024) の Flat Origami での結果が、Petri net 経由で金融に転用される
- 逆に、本プロジェクトの結果 (集中度の Heyting的測度) が折り紙に転用される可能性
- これは賈先生研究室との **理論的双方向の橋** を作る

---

## §9 自分で詰める論点

1. **H-Petri Net の universal property**: 圏論的にどう characterize するか
   - 標準 Petri net = 自由可換モノイドの上のグラフ (Meseguer-Montanari 1990)
   - H-Petri Net = ?? (Heyting代数の何かの上のグラフ)
2. **Open H-Petri Net**: Baez-Master 2018 流の cospan 構造を H版でも構築する
3. **不変量 (P-invariant, T-invariant) の H版**
   - 標準: `x: P → ℤ` such that `x^T C = 0`
   - H版: `x: P → H` の何らかの不変条件
4. **「証拠の累積」の数量化**
   - Heyting値を実数に射影する方法 (例: `H = [0, 1]` 直接 or 確率測度)
   - これで「集中度スコア」を実数値として出せる
5. **stochastic H-Petri Net**
   - 発火確率と Heyting値を組み合わせる
   - 確率Petri net (SPN) との関係
6. **計算可能性 (decidability)**
   - H-Petri Net の reachability は decidable か?
   - 有限 H なら標準 Petri net への還元で yes、無限 H では別議論
7. **linear logic vs intuitionistic logic の Petri net 上での違い**
   - quantale × Petri net (既存) と Heyting代数 × Petri net (本プロジェクト) の比較
   - どちらが何を表現できないか

---

## §10 次のアクション

理論ノートとしてはここまで。次に詰めるなら:

### 短期
- §4 形式定義を厳密に書き直す (universal property を含む)
- §6 還元性の証明を完成 (有限 H 版)
- §7 最小例を Python or 紙で動かしてみる

### 中期
- Open H-Petri Net を定式化 (§9-2)
- H-Petri Net の不変量を計算する例を作る (§9-3)
- ASEAN5 全展開 (TH/SG/MY/ID/PH)

### 長期
- 主張1-5 全てを H-Petri Net で書ききる
- 賈先生研究との数学的等価性を厳密化
- 国内研究会 or arXiv プレプリント

---

## §11 ノートの位置づけ

これは 05_petri_net_theory.md の **主張2-v2 の数学的厳密化** ノート。
05 は俯瞰 (5主張 + サーベイ統合 + アクションリスト)、06 はこの中の「数学の中核」を詰める。

書ききれてない論点:
- §9 の各論
- §10 中・長期項目

これらは別ノート (07, 08, ...) で順次詰める。
