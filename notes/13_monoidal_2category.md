# 13. Monoidal 2-Category 拡張 — 並列発火と Strip Folding 対応

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: notes/09 の 2-category 構造に **monoidal product ⊗** を入れる。Jia 2022-23 Strip Folding as Monoidal Category と直接対応する。

## §1 動機

notes/09 で `𝓚_HPN` を 2-category として構築した。
ここに **monoidal 積 ⊗** を入れると:
- 並列発火 (= 2つの取引が同時に起きる) を ⊗ で書ける
- 並列 backbone の合成 (例: Bakong と GCash が並列に存在する地域) を ⊗ で書ける
- Jia 2022-23 Strip Folding as Monoidal Category の流儀と完全一致

これでこの研究系統の **3層** (Strip Folding 2022-23 → Heyting 2024 → LLM 2025) が本プロジェクトに全て接続される。

---

## §2 Monoidal 2-Category の定義 (簡略)

### 2.1 定義

`(𝓚, ⊗, I)` が **monoidal 2-category** とは:
- `𝓚` が 2-category
- `⊗: 𝓚 × 𝓚 → 𝓚` が 2-functor (monoidal product)
- `I ∈ Ob(𝓚)` が unit
- associator, unitor が 1-cell isomorphism として存在
- coherence diagrams を満たす (pentagon, triangle)

**Symmetric** だと `⊗` が swap up to natural isomorphism.

### 2.2 例

- **Cat** (圏の 2-category): `⊗ = ×` (direct product)
- **Span(C)**: ⊗ = product in C  
- **Cospan(C)**: ⊗ = coproduct in C

H-Petri Net 圏 `Cat_HPN` は **どちらの構造でも持てる**:
- 並列発火 → coproduct (disjoint union of nets)
- 場所の組合せ → product (タプル空間)

本プロジェクトでは **並列発火 = coproduct を ⊗** として採用 (Baez-Master 2018 流)。

---

## §3 𝓚_HPN の Monoidal 構造

### 3.1 並列発火を ⊗ で書く

2つの取引 (例: `tx_1, tx_2`) が独立に同時発生する状況:
- 場所: `P(tx_1) ⊔ P(tx_2)`
- 遷移: `T(tx_1) ⊔ T(tx_2)`
- 不可視層: `H^{P(tx_1) ⊔ P(tx_2)}`

これは Petri net の **disjoint union** で書ける。
disjoint union を `⊗` と書くと、**並列取引は ⊗ で合成可能**。

### 3.2 Unit `I`

`I` = 空 Petri net (場所 0, 遷移 0):
```
N ⊗ I ≅ N
I ⊗ N ≅ N
```

### 3.3 Associativity

```
(N_1 ⊗ N_2) ⊗ N_3 ≅ N_1 ⊗ (N_2 ⊗ N_3)
```

これは disjoint union の自明な性質。

### 3.4 Symmetric structure

並列発火に順序はない (自然な対称性):
```
N_1 ⊗ N_2 ≅ N_2 ⊗ N_1   (swap)
```

→ `𝓚_HPN` は **symmetric monoidal 2-category**。

---

## §4 並列 backbone の合成

### 4.1 同じ国で複数の backbone が共存する状況

実例: フィリピンには GCash, Maya, InstaPay が共存。
これらは並列に動く独立 Petri net:

```
F_PH = F_GCash ⊗ F_Maya ⊗ F_InstaPay
```

各 backbone は独立な 1-cell、`⊗` で並列合成。

### 4.2 Heyting値の振る舞い

並列 backbone のとき、不可視場所 (TrustHub) は **各 backbone ごとに別** (disjoint なので merge されない):

```
TrustHub_GCash:    ⊤_priv  (民間)
TrustHub_Maya:     ⊤_priv  (民間)
TrustHub_InstaPay: ⊤_bank  (銀行型、中央銀行backbone)
```

ユーザーは backbone を選ぶ → どの TrustHub を「使う」かが変わる。

これは **既存の Chart.js でやった4 backbone 比較** の数学的母体。

---

## §5 Jia 2022-23 Strip Folding との対応

### 5.1 Strip Folding の構造

Jia & Mitani 2022/2023 の Strip Folding:
- 紙の strip を折る操作系を monoidal category として扱う
- 折る操作の合成 = `⊗`
- 操作の順序付き合成 = `∘`

```
M_Strip = (operations, ⊗, I, composition)
```

### 5.2 本プロジェクトとの対応

| Strip Folding (Jia 2022-23) | H-Petri Net (本プロジェクト) |
|---|---|
| 紙の状態 | マーキング |
| 折る操作 | 遷移 |
| 折る操作の合成 | 遷移合成 (発火列) |
| 並列に折る | 並列発火 |
| Monoidal ⊗ | 並列発火の ⊗ |
| Unit (折ってない紙) | 空 Petri net I |

→ **構造的に同じ symmetric monoidal category**。
Jia 2022-23 の枠組みが本プロジェクトに **直接転用可能**。

### 5.3 2-cell 構造の対応

Jia 2022-23 では monoidal **category** (1-categorical) だが、
本プロジェクトでは monoidal **2-category** (2-cell が増えた)。

これは「Strip Folding の高次拡張」と見ることもできる:
- 1-cell: 折る操作 (= 遷移)
- 2-cell: 折る操作間の関係 (= 自然変換、本プロジェクトでは Heyting順序)

折り紙の世界で 2-cell が何を意味するかは未知だが、本プロジェクトでは「同じ操作の異なる実装」を表す。

---

## §6 ⊗ の bottleneck 性質 (新仮説)

### 6.1 主張

`N_1 ⊗ N_2` での Heyting値律速:
```
TrustHub_max(N_1 ⊗ N_2) = max(TrustHub_max(N_1), TrustHub_max(N_2))
```

ここは **meet ではなく max (= join)** になる。なぜなら disjoint union だから各 net の TrustHub は **独立** に存在する。

これは Theorem 6.3 (Meet Bottleneck) と対照的:
- **水平合成 (▷)**: meet 律速 (cospan-pushout の merge)
- **monoidal 合成 (⊗)**: max 律速 (disjoint union、merge なし)

### 6.2 ASEAN10 への応用

ASEAN10 のすべての backbone を **monoidal積** で合成:
```
F_ASEAN_TOTAL = F_Bakong ⊗ F_GCash ⊗ F_PayNow ⊗ ... ⊗ F_PromptPay
```

TrustHub_max:
- monoidal: `max(⊤_pub, ⊤_priv, ⊤_bank, ...) = ⊤_pub`
- (但しユーザーは選んだ backbone の Heyting値のみ享受)

一方、**越境決済 (cospan合成)** だと:
- `meet(⊤_pub, ⊤_priv, ⊤_bank, ...) = ⊤_priv` (notes/10 Theorem 6.3)

→ **同じ ASEAN10 でも、合成の方法 (⊗ vs ▷) で律速の方向が逆**:
- 個別並存 (⊗): 最強で律速
- 越境統合 (▷): 最弱で律速

これが本プロジェクトの新しい数学的洞察。

---

## §7 自分で詰める論点

1. **Coherence diagrams**
   - Pentagon axiom for associator
   - Triangle axiom for unitor
   - Hexagon axiom for symmetry
   - これらが H-Petri Net で自動的に成立することの確認
2. **monoidal functor としての backbone**
   - `F_Bakong : 𝓒_CPN → Cat_HPN` が monoidal functor か
   - つまり `F(P ⊗ Q) ≅ F(P) ⊗ F(Q)` を満たすか
3. **§6.1 max 律速の厳密証明**
   - disjoint union の Heyting値が max になることの確認
4. **higher coherence**:
   - 3-cell 構造の必要性
   - sylleptic / symmetric / braided など
5. **strict vs lax**:
   - strict monoidal 2-category か lax monoidal か
   - Petri net の場合は strict で十分のはず

---

## §8 ASEAN10 全体の数学的構造

これまでの蓄積を統合:

```
𝓚_HPN = symmetric monoidal double 2-category
  - 0-cells: ASEAN各国 (TH, SG, MY, ID, PH, VN, KH, LA, MM, BN)
  - 縦 1-cells: backbone関手 F_country
  - 横 1-cells: Open H-Petri Net (越境合成可能)
  - 2-cells: 自然変換 (Heyting順序)
  - ⊗: 並列合成 (max 律速)
  - ▷: 水平合成 (meet 律速)
```

これがプロジェクト全体の **最終的な数学的構造**。
あとはこの構造の中で具体的に何を計算するか、を詰める。

---

## §9 まとめ

monoidal 2-category 構造を入れることで:
- 並列発火が ⊗ で書ける
- 並列 backbone (1国内の複数決済) が ⊗ で記述可能
- Jia 2022-23 Strip Folding と直接同型
- 新しい数学的洞察: **⊗ は max 律速、▷ は meet 律速** (合成方向で律速逆転)

これでこの研究系統 3層 (Strip Folding / Heyting / LLM) すべてに本プロジェクトが接続された。

次は中心交換律の検証 (notes/14)。
