# 19. 時間圏 Time と関手 Trust の universal property

**作成日**: 2026-05-23
**ステータス**: draft v1
**位置づけ**: notes/17 で informal に出した「時間関手 Trust: Time → H」を **categorical に厳密化**。
時間圏 Time の正式定義、関手の圏 [Time, H] の構造、Yoneda の時間軸応用。

## §1 動機 — 「時間」を categorical に扱う必要

これまでの notes/06-18 は **静的** だった (= 1時刻の状態を見る)。
notes/17 で「Trust: Time → H」を informal に書いたが、数学的厳密性がない。

ここでは:
- 時間圏 `Time` を正式に定義 (離散 / 連続 の選択)
- 関手 `Trust: Time → H` の universal property
- 関手の圏 `[Time, H]` の categorical 構造
- end / coend の意味

これが詰まれば、「時間を入れた研究」が圏論的に **しっかりとした足場** を持つ。

---

## §2 時間圏 Time の定義 — 3つの選択肢

### 2.1 離散時間 `Time_d = (ℕ, ≤)`

- 対象: 自然数 `n ∈ ℕ` (例: 月単位の時刻)
- 射: `n → m` ⟺ `n ≤ m`
- これは **全順序集合 (totally ordered set)** = thin category (各 hom-set は最大1個の射)

**実用性**: 計算機実装に直接対応 (タイムステップ単位)。

### 2.2 連続時間 `Time_c = (ℝ_≥0, ≤)`

- 対象: 非負実数 `t ∈ ℝ_≥0`
- 射: 同様に `t → t'` ⟺ `t ≤ t'`

**数学的優美**: 連続時間関手は微分可能性を持てる。ただし計算は重い。

### 2.3 サンプリング時間 `Time_s = ⟨t_0, t_1, t_2, ...⟩`

- 観測時刻の系列 (例: ASEAN各国の年次データ)
- 離散だが irregular (等間隔じゃない)

**実データ向け**: 「日本第一国立銀行 1873年」「Bakong 2020年」のような不規則時刻を扱う。

### 2.4 本プロジェクトでの選択

主軸: **Time_s (サンプリング時間)**。
理由: 実データ駆動、Heyting値の階段関数として自然。

連続時間 Time_c は理論検討のみ。

---

## §3 時間関手 Trust: Time → H

### 3.1 形式定義

完備 Heyting代数 `H` を target とする関手:

```
Trust: Time → H
```

成分:
- `Trust(t) ∈ H` for each `t ∈ Time`
- `Trust(t ≤ t') = (Trust(t) ≤ Trust(t'))` (関手性 = 順序保存)

→ Time が thin category なので、関手 Trust は **「順序保存写像 (monotone function)」** と等価。
これは半順序集合論の基本概念。

### 3.2 monotone Trust の universal property

`Mon(Time, H)` = monotone functor Trust: Time → H の全体。

**Theorem (Universal Property)**: `Mon(Time, H)` は完備 Heyting代数 H の **時間方向 cocompletion** で表せる。

```
Mon(Time, H) ≅ H^{Time^{op}}  (時間方向の関手空間)
```

H 自体が完備 Heyting代数なら、`H^{Time^{op}}` も pointwise に完備 Heyting代数になる。

これが意味すること:
- Trust 関手集合自体が Heyting代数構造を持つ
- 「Trust の和」「Trust の積」が自然に定義される
- これで複数 backbone の Trust 関手を **代数的に合成** できる

---

## §4 関手の圏 [Time, H] の構造

### 4.1 対象と射

- **対象**: 時間関手 `Trust: Time → H`
- **射**: 自然変換 `α: Trust_1 ⇒ Trust_2`

Time が thin だから、自然変換 α は **「各時刻で Trust_1(t) ≤ Trust_2(t)」** と等価。

### 4.2 limit / colimit

- **Limit**: `lim_i Trust_i (t) = ⋀_i Trust_i(t)` (時刻ごとの meet)
  - 意味: 「複数の Trust 時系列に共通する下限」
- **Colimit**: `colim_i Trust_i (t) = ⋁_i Trust_i(t)` (時刻ごとの join)
  - 意味: 「複数の Trust 時系列の上限」

### 4.3 monoidal structure

時間関手の monoidal product 候補:
- **(⊗_∨)**: `(Trust_1 ⊗_∨ Trust_2)(t) = Trust_1(t) ∨ Trust_2(t)` (時刻ごとに join)
- **(⊗_∧)**: `(Trust_1 ⊗_∧ Trust_2)(t) = Trust_1(t) ∧ Trust_2(t)` (時刻ごとに meet)

両方とも well-defined。
本プロジェクトでは:
- **⊗_∨ = 並列 backbone (個別並存)** ↔ notes/15 の ⊗ に対応
- **⊗_∧ = 越境統合 (constraint propagation)** ↔ notes/15 の ▷ に対応

→ notes/15 の Bottleneck Reversal Theorem が **時間軸でも成立** することがここから自動的に出る。

---

## §5 End / Coend — 時間軸の不変量

### 5.1 End (左端、infimum)

```
∫_t Trust(t) = lim_{t ∈ Time} Trust(t) = ⋀_{t ∈ Time} Trust(t)
```

意味: 「全期間で **絶対に守られる最低保証**」。

ASEAN各国の例:
- KH Bakong: `end = ⊥` (2020年以前は存在しない、最低 = 0)
- TH PromptPay: `end = ⊥` (2016年以前)
- US Fed: `end = ⊥` (1913年以前) ← 但し設立直後から ⊤_pub なら end = ⊤_pub (歴史継続)

→ end は「歴史の始まり」を反映する。

### 5.2 Coend (右端、supremum)

```
∫^t Trust(t) = colim_{t ∈ Time} Trust(t) = ⋁_{t ∈ Time} Trust(t)
```

意味: 「**いつかは到達する上限**」= TrustAcc(∞)。

ASEAN各国の例:
- KH Bakong: `coend = ⊤_pub` (2024 までに到達済み)
- PH GCash: `coend = ⊤_priv` (22年で頭打ち、上昇予兆なし)
- US Fed: `coend = ⊤_pub` (1913 以降ずっと)

→ coend は「将来の天井」を反映する。

### 5.3 End / Coend の意味

- end = 過去の最低 = backbone が誕生する **前** の値
- coend = 将来の最高 = backbone の **究極的なポテンシャル**

両者の差 `coend - end` = 「その backbone が時間で達成した変化量」。

例: Bakong の coend - end = ⊤_pub - ⊥ = 3階段 (最大変化)
GCash の coend - end = ⊤_priv - ⊥ = 1階段 (低い)

→ **end/coend を計算するだけで、backbone の「歴史的達成度」が出る**。

---

## §6 Yoneda lemma の時間軸への応用

### 6.1 Yoneda の基本

```
Hom_{[Time, H]}(よ(t), Trust) ≅ Trust(t)
```

ここで `よ(t) = Time(-, t)` は **時刻 t の表現可能関手** (Yoneda embedding)。

意味: 「時刻 t での Trust 値は、Yoneda embedding 経由で完全に決まる」。

### 6.2 本プロジェクトでの含意

これは「時刻 t での Trust」が時刻 t という対象の **prefab な representative** で完全表現できることを意味する。

実用的には:
- 「2026年の Bakong の Trust」を聞かれた → Yoneda で答え直接得られる
- 時間軸全体を知らなくても、特定時刻だけで Trust を計算可能

これは categorical 美学だが、応用的には「**部分情報からの推論**」の根拠になる。

---

## §7 monoidal structure と「並列 vs 統合」の時間版

### 7.1 並列 backbone (⊗_∨)

複数 backbone の並列合成:
```
(F_Bakong ⊗_∨ F_GCash)(t) = F_Bakong(t) ∨ F_GCash(t)
```

意味: 「時刻 t においてユーザーが選べる最強の Heyting値」。
- 2026年: Bakong (⊤_pub) があるなら、PH民は Bakong に逃げれば ⊤_pub
- ただし政治的・技術的に Bakong を使えない場合は GCash の ⊤_priv のみ

### 7.2 越境統合 backbone (⊗_∧)

```
(F_Bakong ⊗_∧ F_GCash)(t) = F_Bakong(t) ∧ F_GCash(t)
```

意味: 「時刻 t において越境統合システム全体の Heyting値」。
- 2026年: ⊤_pub ∧ ⊤_priv = ⊤_priv (最弱に律速)
- これは notes/10 Meet Bottleneck Theorem の **時間関手版**

→ **時間軸を入れても、Ghrist-Gould-Lopez 2024 の bottleneck duality は同じく成立**。

### 7.3 時間進化での予測

```
2010: F_Bakong = ⊥ (まだない), F_GCash = ⊤_priv (新興)
       ⊗_∧ = ⊥  (Bakongがないなら越境統合できない)

2024: F_Bakong = ⊤_pub, F_GCash = ⊤_priv
       ⊗_∧ = ⊤_priv  (GCashが律速)

2030予測: F_Bakong = ⊤_pub, F_GCash = ⊤_priv or ⊤_bank?
       ⊗_∧ = 民間がbankに上がるかで変わる
```

これは時間軸を持つ Petri net で **将来予測** ができる根拠。

---

## §8 先行研究 (Jia-Mitani / Floridi-Jia-Tohmé 系) との接続

### Jia 2022-23 Strip Folding as Monoidal Category
- 折り紙の折り順 = 時間順序
- 折る操作の合成 = Trust 関手の時間合成
- → notes/19 の monoidal structure と直接対応

### Jia 2024 Heyting Algebra in Flat Origami
- 折り紙の状態を Heyting値で扱う = Trust の Heyting値
- 時間で折りが積み重なる = Trust の時間関手
- → notes/19 の formalization が Jia 2024 の Petri net 拡張に該当

### Jia-Floridi 2025 Categorical Analysis of LLMs
- LLM の文脈 = 時刻と読み替え可能
- 文脈で評価が変わる = Trust が時間で変わる
- → notes/19 で LLM 論文の時間軸拡張になる

---

## §9 自分で詰める論点

1. **§3.2 universal property の厳密証明**
   - `Mon(Time, H) ≅ H^{Time^{op}}` を関手の表現可能性経由で証明
2. **連続時間 `Time_c` での dynamics**
   - 時間微分 `dTrust/dt` の Heyting版
   - これは Yoneda lemma の連続版
3. **時間圏 Time の monoidal structure**
   - Time × Time → Time (時間の合成) の意味
   - 「過去と未来の合成」みたいな解釈
4. **危機減衰の lax 関手化** (notes/17 §5 案B)
   - lax monoidal 関手 + Heyting closure operator
5. **時間圏の universal property**
   - Time は何の universal なものか? (例: 「順序集合の自由構成」)
6. **monoidal product の選択**
   - `⊗_∨` と `⊗_∧` のどちらが「物理的に妥当」か
   - 物理的状況によって使い分ける

---

## §10 まとめ

時間圏 Time と時間関手 Trust の categorical 基盤:

```
Time         = thin category (全順序集合)
Trust        = monotone functor Time → H
[Time, H]   = 関手の圏、Heyting代数構造を継承
End          = ⋀_t Trust(t) = 全期間最低保証
Coend        = ⋁_t Trust(t) = 将来上限
Monoidal     = ⊗_∨ (並列) / ⊗_∧ (統合) の2種
Bottleneck Reversal は時間軸でも成立 (notes/10 拡張)
Yoneda       = 部分情報からの時刻 t での値推論
```

これが時間関手の categorical な完全な基盤。
notes/20 (時間圧縮の数学) と組み合わさって、「時間軸を持つ研究」が本格化する。
