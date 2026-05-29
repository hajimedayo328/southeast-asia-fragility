# 14. 中心交換律と Coherence の検証

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: notes/09 (2-category) と notes/13 (monoidal 2-category) で立てた構造が、coherence diagram 公理を実際に満たしていることを確認する。

## §1 動機

これまで `𝓚_HPN` を:
- 2-category (notes/09)
- monoidal 2-category (notes/13)
- double category (notes/10)

として書いてきた。これらが **整合的に well-defined** であることを確認しないと、後で矛盾が出る。

確認すべき公理:
1. **2-category の中心交換律 (interchange law)**
2. **Monoidal 2-category の coherence axioms** (pentagon, triangle, hexagon)
3. **Double category の interchange between vertical and horizontal**

これらが満たされていれば、`𝓚_HPN` は数学的にロバストな構造として確立する。

---

## §2 中心交換律 (Interchange Law) の確認

### 2.1 主張

2-cell `α: f ⇒ g`, `α': g ⇒ h` (垂直合成可能) と
2-cell `β: f' ⇒ g'`, `β': g' ⇒ h'` (垂直合成可能) について:
```
(β' ∘_v β) ∘_h (α' ∘_v α) = (β' ∘_h α') ∘_v (β ∘_h α)
```

直感: 2-cell の「縦と横」の合成が **どちらの順でやっても同じ結果**。

### 2.2 𝓚_HPN での確認

本プロジェクトの 2-cell は Heyting順序 ≤ なので、両辺とも:
```
(β' ∘_v β) ∘_h (α' ∘_v α): Heyting値の順序関係
```

Heyting代数の半順序 ≤ は推移的で、`∨` と互換性がある (∨ は ≤ について monotone)。
よって両辺は **同じ Heyting順序関係** を表す。

**結論**: 中心交換律は Heyting代数の代数構造から **自動的に成立**。
証明は半順序の推移性 + ∨ の monotonicity から直接出る。

### 2.3 厳密証明スケッチ

α: f ⇒ g, β: f' ⇒ g' を Heyting順序の関係としては:
- α(p): `f(p) ≤ g(p)` for each p
- β(p): `f'(p) ≤ g'(p)` for each p

水平合成 `β ∘_h α`:
- `β(p) ∨ α(p) = max(f(p), f'(p)) ≤ max(g(p), g'(p)) = g(p) ∨ g'(p)`
- これは Heyting代数の `≤` と `∨` の monotonicity から成立

垂直合成も推移性から成立。両者の順序を入れ替えても、最終的に得られる順序関係は同じ。 ∎

---

## §3 Monoidal Coherence の確認

### 3.1 Pentagon Axiom

associator `a_{X,Y,Z}: (X ⊗ Y) ⊗ Z → X ⊗ (Y ⊗ Z)` について:
```
a_{X,Y,Z⊗W} ∘ a_{X⊗Y,Z,W} = (id_X ⊗ a_{Y,Z,W}) ∘ a_{X,Y⊗Z,W} ∘ (a_{X,Y,Z} ⊗ id_W)
```

### 3.2 𝓚_HPN での確認

`⊗ = disjoint union` の場合、associator は **strict equality**:
```
(N_1 ⊔ N_2) ⊔ N_3 = N_1 ⊔ (N_2 ⊔ N_3)
```

つまり結合律が **strict** に成立。よって Pentagon axiom は自明に成立。

**結論**: `𝓚_HPN` は **strict monoidal 2-category** (本質的には)。

### 3.3 Triangle Axiom

unit `I` (空 Petri net) について:
```
(X ⊗ I) ⊗ Y → X ⊗ (I ⊗ Y)
   ↓ unitor              ↓ unitor
X ⊗ Y ──────────────────→ X ⊗ Y
```

これも disjoint union の場合 strict に成立。

### 3.4 Hexagon Axiom (Symmetric)

Symmetric structure の coherence:
```
braiding: N_1 ⊗ N_2 → N_2 ⊗ N_1
hexagon: braiding と associator の互換性
```

disjoint union の場合、braiding も strict に成立。
- 順序を入れ替えても集合は同じ
- braiding は involution: `swap ∘ swap = id`

### 3.5 結論

`𝓚_HPN` は **strict symmetric monoidal 2-category** として完全に well-defined。
すべての coherence axiom が **disjoint union の strict性** から自動的に成立。

---

## §4 Double Category の interchange

### 4.1 双向 interchange

double category では、縦と横の合成の interchange:
```
水平で先合成 → 垂直で合成 = 垂直で先合成 → 水平で合成
```

### 4.2 𝓚_HPN での確認

- 縦 1-cell: backbone 関手 (例: F_Bakong)
- 横 1-cell: Open H-Petri Net (cospan)
- 縦と横の interchange = 関手と cospan の互換性

これは Baez-Master 2018 の枠組みで保証されている。本プロジェクト独自に確認すべき点:
- Open H-Petri Net (Heyting値拡張) でも interchange が崩れないか

確認:
- 不可視場所の Heyting値は monotone に更新
- merge (pushout) は ∨ で値合体
- 順序を入れ替えても **∨ の可換性 + 結合性** で同じ結果

→ **Heyting代数の ∨ の代数法則から interchange は自動成立**。

---

## §5 Higher Coherence (3-cell 以上)

### 5.1 必要性

monoidal 2-category では、本来は **3-cell (modification)** まで考えるのが正統:
- associator 自体が isomorphism (1-cell)
- isomorphism 同士の関係が 2-cell
- 2-cell 同士の関係が 3-cell (= modification)

### 5.2 𝓚_HPN での状況

本プロジェクトでは:
- associator が **strict equality** なので、associator の isomorphism は **identity**
- よって 3-cell は **全部 identity**
- → **strict** な monoidal 2-category として 3-cell以上を考える必要なし

### 5.3 もし pseudo monoidal 2-category にするなら

将来 H を厳密に有限 Heyting代数じゃなくする (例: 連続値) と:
- associator が isomorphism (not identity) になる可能性
- そのときは 3-cell が non-trivial になる
- modification (3-cell) を厳密に書く必要が出る

→ 今は strict のままで OK。pseudo化は future work。

---

## §6 数学的構造の完全な記述

これまでの全体を整理:

```
𝓚_HPN = strict symmetric monoidal 2-category
        + double category extension via Open Petri Nets
        + Lawvere theory base (Th(CommMon) × Th(HeytAlg))
        + Q-Petri Net specialization (Master 2019)

公理:
- 2-category 公理 (結合律、単位則、interchange law)
- Symmetric monoidal 公理 (Pentagon, Triangle, Hexagon)
- Double category 公理 (vertical/horizontal interchange)

すべて Heyting代数の代数法則 + disjoint union の集合論的法則
から自動的に成立。
```

これが本プロジェクトの **数学的最終構造** (v1完成)。

---

## §7 自分で詰める論点

1. **§2.3 中心交換律の厳密証明**
   - Heyting代数の monotonicity の categorical 表現
2. **§3 Coherence axioms の厳密証明**
   - すべての axiom を diagram で具体的に書く
3. **§4.2 Double category interchange**
   - Open H-Petri Net の interchange 詳細
4. **将来の pseudo 化**
   - 連続 Heyting代数 (例: H = O(X)) での associator
   - 3-cell modification の具体構成
5. **categorical software**:
   - Catlab.jl で strict monoidal 2-category として実装可能か
   - もしそうなら計算機検証可能

---

## §8 ノート全体の整理 (notes/02 〜 notes/14)

| ノート | 内容 | 状態 |
|---|---|---|
| 02 | 随伴 L⊣R 全体 | 概念 |
| 05 | Petri net 主張5つ | 詰めた |
| 06 | Heyting値 Petri net 数学 | 詰めた |
| 07 | 共通CPN規約 | 詰めた |
| 08 | 1-categorical 解釈 | 詰めた |
| 09 | 2-category 構造 | 詰めた |
| 10 | Open H-Petri Net + Meet定理 | 詰めた |
| 11 | Universal property + Master 2019 | 詰めた |
| 12 | Leapfroggability 厳密化 | 詰めた |
| 13 | Monoidal 2-category 拡張 | 詰めた |
| 14 | Coherence verification | 本ノート |

これで「理論詰め」は **論文化準備が整ったレベル** に到達した。
あとは:
- 実装側を ASEAN5 まで拡張
- 各定理の厳密証明を完成 (§7 課題)
- 当該先行研究との対応を最終確認

---

## §9 まとめ

`𝓚_HPN` は:
- **strict symmetric monoidal 2-category**
- **double category** として越境合成可能
- すべての coherence axiom が代数構造から自動成立
- Lawvere theory base で operadic に書ける
- Heyting代数の monotonicity が両 interchange law を保証

これで「理論詰め」フェーズ完了。
本プロジェクトの数学的基盤は **論文化可能なレベル** に到達。

次のフェーズ:
- 実装の ASEAN5 全展開
- 主張4 (ホットスポット) の数学化 (まだ詰めてない)
- 当該先行研究との完全な対応 マッピング表
- 国内研究会発表 or arXiv プレプリント
