# 17. 時間軸 — 信頼の時間関手化 (Heyting値の時間積分)

**作成日**: 2026-05-23
**ステータス**: draft v1
**位置づけ**: これまで Heyting値を **静的** に扱ってきた。実際は時間で変化する。
「先進国は100年かけて信頼蓄積」「東南アジアは10年で同等を狙う」を categorical に書く。

## §1 動機 — 静的 Heyting値の限界

notes/06〜09 で扱った H-Petri Net は、Heyting値が **発火で単調増加** することは扱った (notes/06 §5.1 monotonicity)。
だが、それは「1取引内」の話。

実際の社会では:
- **信頼は何年もかけて積み上がる**: 銀行口座 = 数百年、モバイルマネー = 数年
- **危機で減衰する**: M-Pesa 5時間停止で「⊤_pub」が一時的に下がる
- **時間圧縮の代償**: 早く強くなるには、構造的に集中する必要がある

これを「時間軸を持つ Heyting値」として圏論で書く。

これが本ノートの目標。

---

## §2 時間関手 `Trust: Time → H`

### 2.1 Time の圏

**Time** = 時刻 `t ∈ ℝ_≥0` を対象とし、時間の進行を射とする圏:
- 対象: 時刻 `t`
- 射: `t → t'` (`t ≤ t'`)、つまり時間順序

これは **全順序集合 (totally ordered set)** = preorder の特殊例 = 圏の特殊例。

### 2.2 関手 Trust

完備 Heyting代数 `H` を target にして、時間関手:

```
Trust: Time → H
```

成分: `Trust(t) ∈ H` が時刻 `t` での信頼値。
関手性: `t ≤ t' ⟹ Trust(t) ≤ Trust(t')` (時間順序を Heyting順序に保つ)

→ **時間が進んでも信頼は減らない (monotone)** がデフォルト。

### 2.3 反例ケース (危機減衰)

monotone じゃないケースもある:
- M-Pesa 5時間停止 → `Trust(t_crisis) < Trust(t_crisis - δ)` (短期的に下がる)
- これは普通の関手じゃ書けない (関手性が崩れる)

対処:
- (a) **粒度を粗くする**: 月単位なら monotone (短期下げは見えない)
- (b) **lax 関手**: `t ≤ t' ⟹ Trust(t) ≤ Trust(t') ∨ ε` (誤差 ε 許容)
- (c) **stochastic Petri Net + Heyting**: 期待値での monotonicity

本ノートでは (a) 粗粒度を採用。月単位での Trust 時系列を扱う。

---

## §3 時間積分としての信頼蓄積

### 3.1 Heyting版時間積分

連続関数の積分 `∫_0^T Trust(t) dt` の Heyting版:

```
TrustAcc(T) = ⋁_{t ∈ [0,T]} Trust(t)
```

意味: 時刻 0 から T までの **最大到達 Heyting値**。
monotone ならこれは `Trust(T)` に等しい。

### 3.2 ASEAN各国の TrustAcc(2026)

| backbone | スタート年 | TrustAcc(2026) | 経過年数 | 速度 |
|---|---|---|---|---|
| KH Bakong | 2020 | ⊤_pub | 6年 | 1.5階段/年 ★最速 |
| TH PromptPay | 2016 | ⊤_pub | 10年 | 0.9階段/年 |
| VN MoMo | 2010 | ⊤_priv | 16年 | 0.1階段/年 ★遅い |
| PH GCash | 2004 | ⊤_priv | 22年 | 0.05階段/年 ★最遅 |

→ **bakcbone タイプで「Trust上昇速度」が劇的に違う**。
中銀型は爆速 (国家が直接保証付けるから)、民間型は遅い (時間で信頼を積むしかない)。

### 3.3 先進国との比較

| backbone | スタート年 | TrustAcc(2026) | 経過年数 | 速度 |
|---|---|---|---|---|
| US Federal Reserve | 1913 | ⊤_pub | 113年 | 0.027階段/年 |
| JP 第一国立銀行 | 1873 | ⊤_pub | 153年 | 0.020階段/年 |
| EU SEPA | 2008 | ⊤_bank | 18年 | 0.11階段/年 |
| Bitcoin | 2009 | ⊤_priv (推測) | 17年 | 0.06階段/年 |

→ **先進国は数十倍の時間をかけて信頼を積み上げてる**。
東南アジアは **時間圧縮** で同等水準に到達しようとしている。

---

## §4 時間圧縮の代償 — 速度と集中度のトレードオフ

### 4.1 観察

東南アジアの中で「速い backbone」と「遅い backbone」を比較:

| backbone | 速度 (階段/年) | 集中度 (HHI推定) | 律速対称性 |
|---|---|---|---|
| KH Bakong | 1.5 | 中 (NBC1点だが BFT) | 速い+集中 |
| TH PromptPay | 0.9 | 高 (BOT mandate) | 速い+集中 |
| PH GCash | 0.05 | 極高 (85%独占) | 遅い+極集中 |
| EU SEPA | 0.11 | 低 (多銀行分散) | 中速+分散 |

### 4.2 仮説 (速度-集中トレードオフ)

**Hypothesis (Time-Concentration Trade-off)**:
```
Trust 上昇速度 v_T と 集中度 C の積は、構造的に有界:
v_T × C ≥ K_const  (Kは定数)
```

つまり:
- **速く強くなりたい → 集中するしかない**
- **分散したい → ゆっくりにしかなれない**

これは「時間と集中のトレードオフ」を数学的に書いたもの。

### 4.3 EU SEPAの位置

EU SEPA は「分散構造で時間をかけて ⊤_bank に到達」を選んだ。
東南アジアの Bakong は「集中で速く ⊤_pub に到達」を選んだ。

両者は **同じ Heyting値ゴール** に **逆のルート** で到達しようとしている。
これは政策設計の根本的な選択。

### 4.4 検証可能性

ASEAN10 + 先進国を縦軸 v_T、横軸 C でプロット。
反比例曲線 `v_T × C = K` が見えれば仮説支持。

これは実データで検証可能 (世銀統計 + IMF統計 + 業界レポート)。

---

## §5 危機減衰の categorical 扱い

### 5.1 monotone 関手の破綻

M-Pesa が 2019年(約5時間)停止した時、Trust 時系列は:
```
Trust(障害前) = ⊤_priv
Trust(障害中) = ⊥ (信頼崩壊)
Trust(復旧後) = ⊤_priv (回復)
```

これは monotone じゃない。関手 `Time → H` として書けない。

### 5.2 解決策 (3案)

**案A (粒度粗化)**: 月単位なら平均化されて見えない。
- メリット: 圏論的に簡潔
- デメリット: 短期ショックが消える、研究価値が落ちる

**案B (lax 関手)**: 関手性を弱める。
- `Trust(t) ≤ Trust(t') ∨ ε` (ε = 一時的減衰許容)
- monoidal 2-category の lax 構造で書ける
- 完備 Heyting代数の closure operator として表現可能

**案C (Trust の双方向化)**: Trust と Recovery の2関手ペア:
```
Trust:    Time → H   (monotone な「上限」)
Recovery: Time → H   (危機後の「再構築速度」)
```
両者の協働で動的振る舞いを書く。

→ 本プロジェクトでは **案A (粗粒度) を主軸**、案Bを補助、案Cは future work。

---

## §6 ASEAN各国の Trust 時系列を Petri net で書く

### 6.1 Time-indexed H-Petri Net

H-Petri Net `N` を時刻 `t` でindex化:
```
N(t) = N with M(p_h)(t) = Trust(t)
```

つまり、不可視場所のマーキングが時刻関数。
発火規則は同じ (∨ で更新)、ただし更新の **頻度** が時刻で変わる。

### 6.2 ASEAN5 の動的 Petri net

- TH PromptPay: 2016に1取引/月 → 2026に1000取引/秒
- KH Bakong: 2020に 0 → 2024に 75M tx/H1 2024
- VN MoMo: 2010に小規模 → 2026に 31M active users

各 backbone の「取引頻度」を時系列データから取得 → Petri net の発火頻度に反映 → Heyting値の時間進化を計算

これは **stochastic Petri Net + 時間関手** の組合せ。実装可能 (今は概念のみ)。

### 6.3 「先進国 = 古い Petri net」「東南アジア = 新しい Petri net」

時間関手で見ると:
- 先進国 backbone は **長期発火履歴** を持つ Petri net
- 東南アジア backbone は **短期発火履歴** だが **発火頻度が高い** Petri net

→ 「同じ Heyting値」に達するルートが構造的に違う。
東南アジアは Bakong式 (高速・集中) しか選べない。
EU は SEPA式 (低速・分散) を選べる (歴史的余裕がある)。

---

## §7 時間関手の universal property (試案)

時間関手 `Trust: Time → H` 全体のなす圏 `[Time, H]`:
- 対象: 時間関手
- 射: 自然変換 (時間ごとの Heyting順序の保持)

この圏には:
- **end (左端)**: `lim_{t} Trust(t) = ⋀_t Trust(t)` (常に下回る値)
- **coend (右端)**: `colim_{t} Trust(t) = ⋁_t Trust(t) = TrustAcc(∞)`

これらが Trust 時系列の **不変量** を与える。

例:
- end: 「絶対に上回らない下限」(全期間で守られる最低保証)
- coend: 「いつかは到達する上限」(将来到達する最大値)

これは informal な「時間積分」を categorical に書いた形。

---

## §8 先行研究 (Jia-Mitani / Floridi-Jia-Tohmé 系) との接続

### Jia 2022-23 Strip Folding as Monoidal Category
- 折り紙の状態は「折る順序」で決まる = 時間順序
- 折る操作の合成 = Trust 関手の時間合成
- → 同型構造

### Jia 2024 Heyting Algebra in Flat Origami
- 折り紙の状態を Heyting値で扱う = Trust の Heyting値
- 時間で折り操作が積み重なる = Trust の時間積分
- → 直接接続

### Jia-Floridi 2025 Categorical Analysis of LLMs
- LLM の「文脈で評価が変わる」は時間軸でも書ける
- 文脈 = 時刻、評価 = Trust
- → 時間関手化で LLM論文の拡張

---

## §9 残る論点

1. **速度-集中トレードオフ定理 (§4.2) の証明**
   - `v_T × C ≥ K_const` を構成的に証明する
   - 統計力学的 (Maxwell-Boltzmann) アプローチ?
2. **危機減衰の lax 関手版 (§5.2 案B)**
   - 完備 Heyting代数の closure operator で書く
   - lax 関手の categorical 性質
3. **時間圏 Time の正確な定義**
   - 連続? 離散?
   - 連続なら ℝ_≥0、離散なら ℕ
   - 本プロジェクトでは離散 (月単位) が実用的
4. **end/coend (§7) と実データの対応**
   - 「全期間最低保証」「将来最大値」を実データで計算
5. **dynamic Petri net** との関係
   - Stochastic Petri Net の文献調査
   - Timed Petri Net (Merlin 1974) との接続
6. **時間関手の monoidal product**
   - `Trust_1 ⊗ Trust_2 = (t ↦ Trust_1(t) ∨ Trust_2(t))?`
   - 並列 backbone の合成

---

## §10 まとめ

時間軸を入れると見えること:
- **速度-集中トレードオフ**: 速く強くなりたいなら集中するしかない (定理候補)
- **先進国 vs 東南アジア**: 同じ Heyting値ゴールに **逆のルート** で到達
- **時間関手 Trust** が `Time → H` の関手として書ける
- end/coend で「全期間最低保証」「将来最大値」を categorical に書ける
- 危機減衰は粗粒度 or lax 関手で扱う

これで「型分類の浅さ」を抜けて、**動的構造** が見える。
次は F (異分野同型) で **普遍構造** を見る (notes/18)。
