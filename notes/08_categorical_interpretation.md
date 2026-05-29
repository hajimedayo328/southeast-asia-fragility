# 08. 圏論的解釈 — H-Petri Net の本当の姿

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: notes/06 (数学的定義) と notes/07 (規約) を踏まえ、本実装が**圏論的に何をしているか**を明示するノート

## §1 動機

src/ の実装で Bakong vs GCash が動いた。具体例としては「同じ場所・遷移数なのに Heyting値上限が違う」という結果が出た。

ただこれは **現象** であって **構造** じゃない。圏論で書き直すと、本プロジェクトの主張がもっと厳密に立つ。

「圏論的には何が起きているのか」を5層に分けて整理する。

---

## §2 H-Petri Net の圏論的構造

### 2.1 マーキング空間の対象

マーキング空間 `M` は2つの可換モノイドの直積:

```
M = ℕ^{P_v} × H^{P_h}
```

ただし:
- `ℕ^{P_v}` は **自由可換モノイド** (加法、Meseguer-Montanari 1990の流儀)
- `H^{P_h}` は **完備 join 半束** (∨ で可換モノイド、∨ は冪等)

両方とも **可換モノイド**。よってマーキング空間 `M` も可換モノイド。

### 2.2 発火 = マーキング圏の射

マーキング圏 `Mark(N)` を定義:
- **対象** = マーキング `m ∈ M`
- **射** `m → m'` = 「`m` から `m'` に発火列で到達できる」関係

発火列の合成 = 射の合成。これは Meseguer-Montanari 1990 "Petri Nets are Monoids" の流儀そのまま。

H-Petri Net では:
- 可視層の発火 = `ℕ^{P_v}` 上の加減 (非対称な作用)
- 不可視層の発火 = `H^{P_h}` 上の ∨ (**冪等な作用** ← ここが本質)

→ **不可視層は何度発火させても上限を超えない** (∨ の冪等性が monotonicity を生む)。
これが src/ で観察した「TrustHub の Heyting値が頭打ち」の **圏論的根拠**。

---

## §3 不可視層 = Heyting値の関手

不可視層の発火関数 `F_h: T → H^{P_h}` を見ると、これは:

```
F_h: T → H^{P_h}
```

`T` を **離散圏** とみなせば、`F_h` は普通の関数。
だが `T` を **発火列のなす圏** (= 自由モノイド `T*`) と見ると:

```
F_h^*: T* → H^{P_h}
```

これは **モノイド準同型** になる(∨ で可換モノイドだから)。

つまり **不可視層は遷移列の関手的拡張**:
- 遷移列 `σ = t_1 t_2 ... t_n` に対し
- `F_h^*(σ) = F_h(t_1) ∨ F_h(t_2) ∨ ... ∨ F_h(t_n)`

この関手性が **「証拠の累積」を圏論的に保証する**。

---

## §4 Bakong vs GCash = 共通圏上の2つの関手 + その間の自然変換 ★中核

### 4.1 共通圏 `𝓒_CPN` の定義

`notes/07_common_cpn_spec.md` で定めた **共通 CPN 規約** を圏として書く:

```
𝓒_CPN:
  対象: {UserWallet, PendingTx, Backbone, SettledTx, RecipientWallet,
         TrustHub, SystemicLoad}  (7必須場所)
  射:   {t1_InitiateSend, t2_BackboneClear, t3_Settle,
         t4_Reconciliation, t5_AcknowledgeReceipt}  (5標準遷移)
       + 合成 (発火列)
```

これは **規約だけ持つ抽象圏**。具体的な Heyting値増分は決まってない。

### 4.2 Bakong と GCash を 2つの関手として書く

```
F_Bakong: 𝓒_CPN → H-Petri Net 圏
F_GCash : 𝓒_CPN → H-Petri Net 圏
```

各関手は:
- 場所 → 実装場所 (`Backbone → NBCBackbone` vs `GlobeBackbone`)
- 遷移 → 実装遷移
- **特に**: `F_h(t) ∈ H` を割り当てる

これで「ASEAN モバイル金融の各 backbone = 共通圏から H-Petri Net 圏への関手」になる。

### 4.3 違いは自然変換 η

Bakong と GCash の構造的違いは、**自然変換**:

```
η: F_GCash ⇒ F_Bakong
```

η の成分は (Heyting順序の包含):
- η_{TrustHub}: `⊤_priv → ⊤_pub`  (GCash の TrustHub 上限 ≤ Bakong の TrustHub 上限)
- η_{SystemicLoad}: `⊤_priv → ⊤_bank`

**つまり**:
> **Bakong と GCash の構造的違い = 2つの関手の間の自然変換の成分**

これは 02_framework.md で言った「両立可能性 2-cell」の **具体的な実装**。

### 4.4 src/ 実装での確認

src/h_petri/backbones/bakong.py と gcash.py を見ると、**flow_in と flow_out は完全に同じ構造** で、**flow_heyting だけ違う**。

これはまさに「**共通圏 𝓒_CPN は同じ、関手の Heyting成分だけ違う**」の物理的実体化。
コードが直接、圏論的構造を表してる。

### 4.5 Jia-Floridi 2025 との直接同型

Jia-Floridi 2025 の構造:
- 圏 𝒞 ⊆ Rel
- 人間ルート関手 `g ∘ c: H → Pred(W)`
- LLM ルート関手 `r ∘ e ∘ i ∘ p: H → Pred(W)`
- 2-cell = 包含 ⊆

本プロジェクトの構造:
- 圏 `𝓒_CPN`
- F_Bakong 関手
- F_GCash 関手
- 自然変換 η = Heyting順序 ≤

→ **構造的に同型** (Jia 2025 の数学を別ドメインに転用)

---

## §5 便利と不可視コストの随伴 L⊣R の具体化

### 5.1 関手 L (便利を入れる)

```
L: 𝓒_visible → 𝓒_full
   (可視層のみのPN) → (可視+不可視のPN)
```

`L` は「可視Petri net に補助場所を追加して、各遷移を Heyting値増分付きにする」関手。
これが **「便利な遷移を発火する」操作の構造化**。

### 5.2 関手 R (不可視層を抽出)

```
R: 𝓒_full → 𝓒_invisible_record
   (可視+不可視のPN) → (不可視層の Heyting記録)
```

`R(N)` は H-Petri Net `N` から **不可視場所の Heyting値の最終状態だけ取り出す** 関手。
これが **「結果として累積したコストを観測する」操作**。

### 5.3 随伴関係

```
Hom(L(visible_PN), full_PN) ≅ Hom(visible_PN, R(full_PN))
```

意味:
- 左辺: 「可視 PN を full PN に持ち上げる写像」
- 右辺: 「可視 PN を full PN の不可視層に対応させる写像」

→ **「便利を入れる」と「コストを観測する」は数学的に同値な操作**。
これが 02_framework.md の **「便利と不可視コストは必ずペアで現れる」** の圏論的根拠。

### 5.4 まだ厳密に書ききれてない部分

- L と R の正確な定義 (今は雰囲気レベル)
- Unit/Counit の明示
- 随伴であることの証明

これは詰める価値あるが、本ノートは「全体像」を出すまでにとどめる。

---

## §6 ASEAN5 合成 = Open Petri Net の cospan-pushout

### 6.1 各国を Open H-Petri Net として書く

```
O_TH = (N_TH, i_TH: User → p1, o_TH: p5 → Recipient)
O_SG = (N_SG, i_SG, o_SG)
...
```

各国の N_i は §4 の関手 F_country の出力。

### 6.2 越境決済プロトコル = cospan の射

PromptPay × QRIS × DuitNow × InstaPay × PayNow の越境統合は、各 Open Petri Net の **入出力ポートを cospan で接続**:

```
O_TH ∘ O_SG ∘ O_MY ∘ O_ID ∘ O_PH
```

合成は cospan の **pushout**。これは Baez-Master 2018 の枠組みそのまま。

### 6.3 合成後の Heyting値律速

合成後の TrustHub の Heyting値は、**5国の TrustHub の meet** で計算される:

```
TrustHub(O_合成) = TrustHub(O_TH) ∧ TrustHub(O_SG) ∧ ... ∧ TrustHub(O_PH)
```

`∧` は Heyting代数の meet。

→ **域内決済全体の信頼 = 最弱の国に律速** (Heyting代数の半順序から自動的に出る)

これは notes/07 §5.3 で立てた仮説の **数学的証明**。

---

## §7 先行研究 (Jia-Mitani / Floridi-Jia-Tohmé 系) との接続点まとめ

| 先行研究 | 本プロジェクトでの圏論的対応 |
|---|---|
| **Strip Folding as Monoidal Category** (Jia 2022-23) | 発火列 = モノイダル圏の射の合成 |
| **Heyting Algebra in Flat Origami** (Jia 2024) | 不可視層 = Heyting値の関手 `F_h^*: T* → H^{P_h}` |
| **Categorical Analysis of LLMs** (Jia-Floridi 2025) | F_Bakong vs F_GCash の自然変換 |

特に Jia 2024 と Jia-Floridi 2025 は **本プロジェクトの数学的バックボーン**:
- Jia 2024 から **Heyting値の構造** を借用
- Jia-Floridi 2025 から **並列関手 + 自然変換** の構造を借用

→ 本プロジェクトは **「この圏論研究系統の方法論をモバイル金融という別ドメインに転用する応用研究」** という位置づけが最も明確。

---

## §8 圏論的に見えること (まとめ)

src/ の実装で見た「Bakong vs GCash の不可視層 Heyting値の差」は、圏論で書き直すと:

1. **共通圏 `𝓒_CPN` 上の2つの関手 `F_Bakong, F_GCash`** が存在
2. 両関手は可視層では同型、**Heyting成分だけ違う**
3. 自然変換 `η: F_GCash ⇒ F_Bakong` が Heyting順序の包含を表現
4. これは Jia-Floridi 2025 の「並列ルート関手 + 2-cell」と同型
5. ASEAN5合成は Open Petri Net の cospan-pushout
6. 域内信頼は **meet 律速** (Heyting代数の構造から自動)

つまり src/ で動かしたシミュレーションは、**圏論的構造の数値実体化** であり、
結果として現れた「Heyting値の永久差」は **自然変換の成分** として圏論的に厳密に解釈できる。

---

## §9 自分で詰める論点

1. **L ⊣ R の厳密定義** (§5)
   - Unit η: id ⇒ R∘L の明示
   - Counit ε: L∘R ⇒ id の明示
   - 随伴の証明 (三角恒等式)
2. **自然変換 η の universality** (§4.3)
   - η が **terminal** な自然変換か? (= 一番強い差分)
   - もし terminal なら「Bakong は GCash の理想化」と言える
3. **F_h^* の関手性の証明** (§3)
   - `T*` から `H^{P_h}` への準同型性を厳密に
4. **𝓒_CPN の正確な定義** (§4.1)
   - 圏として well-defined か (合成可能性、結合律)
   - 場所と遷移をどう object/morphism に分けるか
5. **ASEAN5 合成の存在性** (§6)
   - cospan の pushout は常に存在するか (一般には yes、本プロジェクトで具体的に構成)
   - 越境プロトコルがそれぞれ cospan の射として well-defined か
6. **meet 律速定理の証明** (§6.3)
   - 完備 Heyting代数の meet が cospan-pushout で保たれるか

これらを詰めると論文1本書ける規模。

---

## §10 次のアクション

### 短期
- §4.3 自然変換 η を src/ コードで明示的に書く (例: `compare.py` に η の表示追加)
- §6.3 meet 律速の計算例を Python で実装
- ノートを通読し、矛盾や不明点を洗う

### 中期
- L ⊣ R の厳密化 (§5)
- F_h^* の関手性証明 (§3)
- ASEAN5合成の Python 実装 (Open Petri Net)

### 長期
- 論文骨格としての再整理
- 当該先行研究の借用関係を厳密に明示
- arXiv プレプリント候補

---

## §11 ノートの位置づけ

これは notes/06 (定義) と notes/07 (規約) を踏まえて、**「圏論で書くと何が見える」** を整理したノート。

src/ の実装は **このノートの圏論構造の物理実体化**。
- コードを読むと圏論的構造が見え
- 圏論構造を読むとコードが書ける

これが本プロジェクトの最大の整合性。
理論 (notes/06, 07, 08) と実装 (src/) が**同じ圏論構造の2つの表現**になっている。
