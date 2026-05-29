# 11. H-Petri Net の Universal Property — Master 2019 Lawvere Theory との接続

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: notes/06, 08, 09, 10 で構築した H-Petri Net を、Master 2019 "Petri Nets Based on Lawvere Theories" (arXiv:1904.09091) の枠組みで捉え直し、universal property として characterize する。

## §1 動機

Master 2019 は、Petri net の変種を **Lawvere theory Q をパラメータ化** することで統一的に扱う研究。
本プロジェクトの H-Petri Net もこの枠組みで再解釈すると:
- **Heyting代数を Lawvere theory として与える特殊例** として位置づけ可能
- 「H-Petri Net とは何か」が categorical に1行で言える
- 既存の Q-net の universal property を継承

これは notes/06 §4 で雰囲気で書いた定義を、**categorical に厳密化** するノート。

---

## §2 Lawvere Theory のクイックレビュー

### 2.1 定義

Lawvere theory `Q` とは:
- 対象が自然数 (0, 1, 2, ...) 
- finite products を持つ small category
- 各対象 `n` が `1` の n-fold product として表される: `n = 1 × 1 × ... × 1`

直感的: Lawvere theory = **有限 arity の代数演算系**を圏論的に扱う道具。

### 2.2 代表例

| Lawvere theory | 何の代数 |
|---|---|
| `Th(Mon)` | モノイド |
| `Th(CommMon)` | 可換モノイド |
| `Th(Grp)` | 群 |
| `Th(Lat)` | 束 |
| `Th(SLat)` | 半束 (semilattice) |
| `Th(HeytAlg)` | Heyting代数 ★ |

### 2.3 Q-algebra

`Q`-代数 = `Q` からの直積保存関手 `A: Q → Set`。

- `Th(Mon)`-algebra = モノイド
- `Th(HeytAlg)`-algebra = Heyting代数

---

## §3 Master 2019 の Q-Petri Net

### 3.1 主構成

Master 2019 は **Q-Petri Net** という枠組みを提案:

```
Q-Petri Net = (P, T, F, M_0)
  but: 場所の集合 P は Q-algebra (集合じゃない)
```

つまり、場所のトークン数だけじゃなく、**Q の構造を持つ集合** に値を取る。

- `Q = Th(CommMon)` のとき: 普通の P/T Petri net (場所のトークン = 自然数)
- `Q = Th(Vec_k)` のとき: continuous Petri net (場所のトークン = ベクトル)
- `Q = Th(HeytAlg)` のとき: **本プロジェクトの不可視層**

### 3.2 H-Petri Net の Q-Petri Net としての位置づけ

本プロジェクトの H-Petri Net は **2層構造**:
- 可視層: 標準 P/T Petri net (`Q = Th(CommMon)`)
- 不可視層: `Q = Th(HeytAlg)` の Q-Petri Net

**2層を1つの Q-Petri Net にまとめる方法**:
直積 Lawvere theory `Q_total = Th(CommMon) × Th(HeytAlg)` を取れば、両方を同時に扱える。

実際:
```
H-Petri Net = (Th(CommMon) × Th(HeytAlg))-Petri Net
            = Q_total-Petri Net
```

→ Master 2019 の枠組みそのまま継承。

---

## §4 H-Petri Net の Universal Property

### 4.1 自由 H-Petri Net

集合 `P_v`, `P_h`, `T` を与えると、**自由 H-Petri Net** `F(P_v, P_h, T)` が構築可能:
- 可視層: 自由可換モノイド `ℕ^{P_v}` (Meseguer-Montanari 1990)
- 不可視層: 自由 Heyting代数 `Free_HeytAlg(P_h)`
- 遷移: `T` 上の自由射

### 4.2 Universal Property (主張)

**定義 (圏 HPN)**: H-Petri Net 全体の圏:
- 対象: H-Petri Net
- 射: 場所・遷移を保つ準同型

**定理 (Universal Property of Free Construction)**:
`F: Set × Set × Set → HPN` は **左随伴**: 忘却関手 `U: HPN → Set × Set × Set` (3つの底集合を取り出す) の左随伴。

```
F ⊣ U: Hom_HPN(F(P_v, P_h, T), N) ≅ Hom_Set(P_v, U(N)) × Hom_Set(P_h, U(N)) × Hom_Set(T, U(N))
```

これは Meseguer-Montanari 1990 "Petri Nets are Monoids" の H版。

### 4.3 系: 任意の場所を持つ H-Petri Net は自由 H-Petri Net の商

任意の H-Petri Net `N` は、適切な集合からの自由構成 `F(P_v(N), P_h(N), T(N))` の **適切な商** で書ける。

これにより:
- 「H-Petri Net とは何か」が universal property で characterize される
- 構成的に H-Petri Net を生成できる
- Catlab.jl 流の ACSets として実装可能

---

## §5 Jia-Mitani 2024 "Heyting Algebra in Flat Origami" との Lawvere Theory 対応

### 5.1 Jia 2024 の Heyting代数の使い方

Jia 2024 "Heyting Algebra in Flat Origami" では:
- 折り紙の操作系を Heyting代数として扱う
- 折り目の有無を `⊤, ⊥` で表現
- 折り操作の合成を `∧, ∨` で表現

これは **Heyting代数の inhabited structure** を直接利用する。

### 5.2 本プロジェクトとの対応

`Th(HeytAlg)` という Lawvere theory を共通の base に取ることで:
- Jia 2024 の Origami = `Th(HeytAlg)`-algebra の特定インスタンス
- 本プロジェクトの不可視層 = `Th(HeytAlg)`-Petri Net

**両方とも同じ Lawvere theory の上に乗っている**。これが「折り紙と金融が同じ枠組み」の Lawvere version。

---

## §6 Operad との関係

Lawvere theory は **operad の特殊例**:
- Lawvere theory = symmetric operad の特定形 (各 arity の operations が finite product を生成する)

operad の言葉では:
- H-Petri Net = (`Th(CommMon) × Th(HeytAlg)`)-operad の algebra
- 遷移 = operad operation
- 発火 = operation 適用

これは Spivak の operadic systems theory (notes/05 §8 参照) の流儀そのまま。

---

## §7 自分で詰める論点

1. **§4.2 Universal Property の厳密証明**
   - `F ⊣ U` の三角恒等式
   - 自由構成の具体的構成法 (Meseguer-Montanari の Heyting版)
2. **`Free_HeytAlg(X)` の構成**
   - 集合 X から自由 Heyting代数を生成する具体的手順
   - 連続束として実現される (Stone duality との関係)
3. **`Th(CommMon) × Th(HeytAlg)` の正確な定義**
   - 直積 Lawvere theory の構成
   - これが普通の Lawvere theory として well-defined か
4. **operad 表現**:
   - colored operad として書く方法
   - Spivak の polynomial functor との関係
5. **AlgebraicPetri.jl での実装**
   - ACSets 上での `Th(HeytAlg)`-Petri Net 実装
   - schema の定義

---

## §8 まとめ

H-Petri Net は:
- **Master 2019 の Q-Petri Net の特定例** (Q = `Th(CommMon) × Th(HeytAlg)`)
- **Universal Property** で characterize される (自由構成の左随伴)
- **operad の algebra** としても書ける (Spivak流)
- **Jia 2024 の Heyting Origami と同じ Lawvere theory base**

これで「H-Petri Net とは何か」が、5層 (notes/06=数学定義、07=規約、08=関手、09=2-category、10=double cat、11=Lawvere theory) で完全に捉えられた。

次の主張別厳密化 (notes/12〜) で、leapfroggability、monoidal 2-cat、coherence をそれぞれ詰める。
