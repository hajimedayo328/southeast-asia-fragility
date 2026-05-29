# 09. 2-Category としての H-Petri Net — 関手+自然変換から2-cellへ

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: notes/08 (圏論的解釈) で出した「関手 + 自然変換」を **2-category として完成** させる

## §1 動機 — なぜ 2-category か

notes/08 で:
- F_Bakong, F_GCash : 𝓒_CPN → H-PetriNet  (関手)
- η: F_GCash ⇒ F_Bakong  (自然変換)

まで来た。**自然変換が出てきた時点で、世界は実は 2-category** になっている。

2-category にすると何が嬉しいか:

1. **関手間の関係そのもの (η) を1級市民として扱える**
   - 「Bakong は GCash より強い」を 1-cell として書ける
2. **2-cell の合成則 (垂直 / 水平)** が使える
   - 複数の backbone を変換する2-cellをチェイン可能
3. **Floridi-Jia-Tohmé 2025 LLM論文の流儀と完全一致**
   - Jia-Floridi 2025 は 2-category そのもの
   - Strip Folding (Jia 2022-23) は monoidal 2-category
4. **Open Petri Net の Baez-Master 2018 が double category**
   - 双方向 (水平/垂直) の合成が必要
5. **主張1〜5を統一的に書き直せる**

つまり 2-category は **本プロジェクトの最終的な構造的言語**。

---

## §2 2-Category の数学的準備

### 2.1 定義 (Strict 2-Category)

`𝓚` が 2-category とは:
- **0-cell** (対象): 集合 `Ob(𝓚)`
- **1-cell** (1-morphism): 各 `a, b ∈ Ob(𝓚)` に対し集合 `𝓚(a, b)`
- **2-cell** (2-morphism): 各 1-cell `f, g ∈ 𝓚(a, b)` に対し集合 `𝓚(a, b)(f, g)`

合成:
- **1-cell の合成**: `𝓚(a, b) × 𝓚(b, c) → 𝓚(a, c)` (普通の射の合成)
- **2-cell の垂直合成** (`∘_v`): `α: f ⇒ g`, `β: g ⇒ h` ⇒ `β ∘_v α: f ⇒ h`
- **2-cell の水平合成** (`∘_h`): `α: f ⇒ g` in `𝓚(a, b)`, `β: f' ⇒ g'` in `𝓚(b, c)` ⇒ `β ∘_h α: f' ∘ f ⇒ g' ∘ g`

公理:
- 結合律 (1-cell 合成、2-cell 垂直 / 水平合成)
- 単位則
- **中心交換律 (interchange law)**: `(β ∘_v β') ∘_h (α ∘_v α') = (β ∘_h α) ∘_v (β' ∘_h α')`

### 2.2 例

| 2-category | 0-cell | 1-cell | 2-cell |
|---|---|---|---|
| **Cat** | 小圏 | 関手 | 自然変換 |
| **Rel** | 集合 | 二項関係 | 関係の包含 ⊆ |
| **Span(C)** | C の対象 | C の span | C の射 |
| **Cospan(C)** | C の対象 | C の cospan | C の射 |

特に **Cat (圏の2-category)** が本プロジェクトの母体。

---

## §3 H-Petri Net の 2-Category 構造

### 3.1 0-cell, 1-cell, 2-cell の同定

本プロジェクトの 2-category `𝓚_HPN` を以下で定義:

| | 内容 |
|---|---|
| **0-cell** | 共通CPN規約 `𝓒_CPN` (notes/07) |
| **1-cell** | 関手 `F: 𝓒_CPN → Cat_HPN`、つまり個別の backbone 実装 (F_Bakong, F_GCash, ...) |
| **2-cell** | 自然変換 `η: F ⇒ G`、backbone 間の Heyting順序による関係 |

注: 普通の Cat の流儀だと 0-cell が圏で 1-cell が関手だが、本プロジェクトでは「共通規約は1つ」なので、0-cell を `𝓒_CPN` 1つに固定して、1-cell を「`𝓒_CPN` から `Cat_HPN` への関手」と読み替える。これで実質的に Cat の subcategory として `𝓚_HPN` が定義できる。

### 3.2 backbone たちの位置取り

`𝓚_HPN` の中で各 backbone は:

```
F_Bakong : 𝓒_CPN → Cat_HPN  (中央銀行型、TrustHub上限 ⊤_pub)
F_PayNow : 𝓒_CPN → Cat_HPN  (銀行型、TrustHub上限 ⊤_bank)
F_GCash  : 𝓒_CPN → Cat_HPN  (民間型、TrustHub上限 ⊤_priv)
F_M-Pesa : 𝓒_CPN → Cat_HPN  (電話会社型、TrustHub上限 ⊤_telco)
```

### 3.3 2-cell (自然変換) の構造

任意の2つの backbone 間に自然変換が存在:

```
η_GP : F_GCash  ⇒ F_PayNow   (民間 → 銀行への変換、Heyting順序)
η_PB : F_PayNow ⇒ F_Bakong   (銀行 → 中央銀行への変換)
η_GB : F_GCash  ⇒ F_Bakong   (民間 → 中央銀行、これは合成 η_PB ∘_v η_GP)
```

各 η の成分:
- η_GP(TrustHub): `⊤_priv → ⊤_bank` (Heyting値の包含)
- η_PB(TrustHub): `⊤_bank → ⊤_pub`
- η_GB(TrustHub): `⊤_priv → ⊤_pub` (垂直合成で出る)

### 3.4 垂直合成と Heyting順序

η の垂直合成は **Heyting順序の推移性** をそのまま表現:

```
(η_PB ∘_v η_GP)(TrustHub)
  = η_PB(TrustHub) ∘ η_GP(TrustHub)
  = (⊤_bank → ⊤_pub) ∘ (⊤_priv → ⊤_bank)
  = ⊤_priv → ⊤_pub
  = η_GB(TrustHub)
```

→ **2-cell の垂直合成 = Heyting順序の半順序的推移性**。
これは Heyting代数が **poset (preorder圏)** であることの2-categorical表現。

### 3.5 まとめ

```
        F_GCash ──────── η_GP ────────► F_PayNow
            │                              │
            │                              │
        η_GB │                         η_PB │
            │                              │
            ▼                              ▼
        (skipped)                      F_Bakong
                       (η_GB = η_PB ∘_v η_GP)
```

→ ASEAN10 の backbone 全体が 2-category の中で **半順序構造** を成す。

---

## §4 主張1〜5を 2-Category 上で統一

ノート05で立てた5つの主張を 2-category の言葉で書き直す:

### 4.1 主張1 (リープフロッグ = reachability) の 2-categorical形

- リープフロッグ可能性 = 部分マーキング reachability
- 2-categoricalには: **2-cell `η: F_legacy ⇒ F_leapfrog` が存在 ⇔ 同じ機能を達成する2つの関手間に自然変換が引ける**

つまり主張1 = `𝓚_HPN` の中での **homset の非空性**:
```
リープフロッグ可能 ⇔ 𝓚_HPN(𝓒_CPN, Cat_HPN)(F_legacy, F_leapfrog) ≠ ∅
```

### 4.2 主張2 (Heyting値) の 2-categorical形

- Heyting代数 `H` 自体が 0-cellだけの 2-category (= poset)
- Heyting値の不可視層 = `H` への **2-functor**
- F_h*: T* → H = monoid (= 1-object 圏) としての 2-functor

`H`-値づけは「`Cat_HPN` から `H` への 2-functor の存在」として書ける。

### 4.3 主張3 (P/T-invariant) の 2-categorical形

P-invariant は **2-natural transformation の特別な場合**:
- 標準: `x: P → ℤ` such that `x^T C = 0`
- 2-categorical形: `x: F ⇒ const_ℤ` のような自然変換 (各遷移で値が不変)

これで主張3 = **「特定形の 2-natural transformation の存在判定」**。

### 4.4 主張4 (集中度 = ホットスポット) の 2-categorical形

- 場所 = 1-cellの domain
- ホットスポット = **すべての 2-cell が因子化される 1-cell**
- 圏論的中心性 = 「factorization が多い 1-cell」

これは技術的に詰める要。但し直感的には「2-cell の経由率」として書ける。

### 4.5 主張5 (Open Petri Net 合成) の 2-categorical形

- Open Petri Net = **double category** の morphism (Baez-Master 2018)
- double category = 2つの 2-category の合成
- 合成 = 水平合成 (cospan の pushout)

ASEAN5 合成は double category 上の **水平合成連鎖**:
```
O_TH ▷ O_SG ▷ O_MY ▷ O_ID ▷ O_PH
```

→ **本プロジェクト全体が double category の特定形** として一気に書ける。

---

## §5 先行研究 (Jia-Mitani / Floridi-Jia-Tohmé 系) との対応 (2-categorical version)

### 5.1 Jia 2022-23 Strip Folding as Monoidal Category

折り紙の操作合成 = monoidal圏の射の合成。
monoidal圏 = **対称モノイダル 2-category の特定 object 1個の場合の hom-圏**。

本プロジェクトの `𝓚_HPN` も symmetric monoidal にできる:
- ⊗: 並列発火 (= disjoint union of Petri nets)
- I: 空 Petri net
- 対称性: 場所の交換

→ **同じ monoidal 2-category 流儀**。

### 5.2 Jia 2024 Heyting Algebra in Flat Origami

Heyting代数 = poset = **0-cellだけの2-category** (= preorder圏)。
Flat Origami での Heyting代数の使い方を Petri net に持ち込むのが notes/06 の本意。

→ **Heyting代数を H-Petri Net の coefficient として使う** = 2-functor `Cat_HPN → 𝓚(H)`。

### 5.3 Jia-Floridi 2025 Categorical Analysis of LLMs

これが最も直接的に対応:

| Jia-Floridi 2025 | 本プロジェクト |
|---|---|
| 𝒞 ⊆ Rel (Relの部分2-圏) | `Cat_HPN` (Petri net の圏) |
| 人間ルート関手 g∘c | F_Bakong |
| LLM ルート関手 r∘e∘i∘p | F_GCash |
| 2-cell ⊆ (関係包含) | 自然変換 η (Heyting順序) |
| 右Kan拡張 Ran_p(g∘c) | ホットスポット場所 (主張4 候補) |

→ **完全な構造的同型**。Jia-Floridi 2025 の数学を別ドメイン (モバイル金融) に移植したのが本プロジェクト。

---

## §6 ASEAN5 合成と meet 律速の 2-categorical 定式化

### 6.1 Open Petri Net = double category

Baez-Master 2018 の Open Petri Net は **double category**:
- 縦の 1-cell: Petri net 間の射
- 横の 1-cell: cospan (入出力ポート)
- 2-cell: cospan の射

これを H-Petri Net に拡張すると:
- 縦の 1-cell: F_Bakong, F_GCash 等の backbone 関手
- 横の 1-cell: 国境を超える cospan
- 2-cell: 越境プロトコル

### 6.2 合成の Heyting値律速

水平合成 (= cospan pushout) の Heyting値は **meet で律速**:

```
TrustHub(O_TH ▷ O_SG ▷ ... ▷ O_PH) = TrustHub(O_TH) ∧ TrustHub(O_SG) ∧ ... ∧ TrustHub(O_PH)
```

これは double category の hom-object が **完備 Heyting代数値** であることから自動的に出る。

### 6.3 律速定理 (主張)

**Theorem (Meet Bottleneck)**:
Open H-Petri Net `O_1, ..., O_n` の水平合成 `O_1 ▷ ... ▷ O_n` について、
不可視場所 `p_h ∈ P_h` の Heyting値は

```
M(p_h) ≤ ∧_{i=1}^{n} TrustHub_max(O_i)
```

つまり**最弱の `O_i` に律速される**。

**証明スケッチ**: cospan-pushout の hom-object 構造 + Heyting代数の meet 安定性から。
詳細は別途。

---

## §7 自分で詰める論点

1. **𝓚_HPN が strict 2-category か bicategory か**
   - 関手の合成が strict associative であれば strict 2-category
   - そうでなければ bicategory (合成に同型しか保証されない)
   - 本プロジェクトでは strict で十分のはず
2. **中心交換律 (interchange law) の確認**
   - 2-cell の垂直と水平の合成が compatible か
   - Heyting順序の場合は自動的に成立 (poset内の半順序)
3. **主張4 (ホットスポット) の 2-categorical 厳密化**
   - 「factorization が多い 1-cell」を圏論で書く方法
   - 右Kan拡張との関係
4. **double category 拡張**
   - Open H-Petri Net を厳密に double category として書ききる
   - Baez-Master 2018 の H版を構築
5. **meet 律速定理の厳密証明** (§6.3)
   - cospan-pushout の hom-object 計算
   - Heyting代数の meet 安定性
6. **monoidal 2-category への拡張**
   - 並列発火を ⊗ で書く
   - Jia-Mitani 2023 Strip Folding との完全対応

---

## §8 ノート整理 — 理論基盤の完成度

| ノート | 何を扱う | 完成度 |
|---|---|---|
| 02 | 随伴 L⊣R 全体フレーム | 概念レベル |
| 05 | Petri net 主張5つ俯瞰 | 詰めた |
| 06 | Heyting値 Petri net 数学 | 詰めた |
| 07 | 共通CPN規約 | 詰めた |
| 08 | 関手+自然変換 (1-categorical) | 詰めた |
| **09** | **2-category 構造** | **本ノート** |

次に詰める候補:
- 10: Open H-Petri Net (double category 厳密) — meet律速定理の証明
- 11: Heyting値 Petri net の universal property — Master 2019 Lawvere theory との関係
- 12: 主張1 (leapfroggability) の厳密化 — R-restricted reachability の計算可能性

---

## §9 圏論的に「本プロジェクト」を1文で言うと

> **本プロジェクトは、共通CPN規約 `𝓒_CPN` を 0-cell に固定した 2-category `𝓚_HPN` の中で、ASEAN10各国の決済システムを 1-cell として配置し、その間の Heyting順序構造を 2-cell として記述する研究である。これは Jia-Floridi 2025 の LLM 圏論分析を別ドメインに移植したものであり、また Jia 2024 Heyting Origami の代数構造を Petri net の不可視層に持ち込んだものでもある。最終的な数学的構造は monoidal double category であり、ASEAN5 域内決済合成は cospan-pushout として定式化される。**

これが「圏論的にこのプロジェクトが何か」の完成形 1文 (v1)。
あとは詰めるだけ。
