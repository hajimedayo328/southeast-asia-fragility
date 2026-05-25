# 15. ⊗ vs ▷ 律速逆転 (Bottleneck Reversal) の深掘り

**作成日**: 2026-05-23
**ステータス**: draft v2 — サーベイ08で既存研究3本判明、新規性主張を修正済み
**位置づけ**: notes/13 §6 の仮説を厳密化したが、サーベイ結果で **既存の lattice bottleneck duality** に該当することが判明。本プロジェクトの貢献は「Open Petri Net + Heyting + ASEAN応用」への翻訳。

## §0 サーベイ08 (literature/raw/08) からの修正

当初は「本プロジェクトの唯一の真新規候補」と主張したが、徹底サーベイで以下が判明:

### 致命的な先行研究3本

1. **Liebeherr (2017) "Duality of the Max-Plus and Min-Plus Network Calculus"**
   - 200ページ級 monograph
   - 同一ネットワークに対し min-plus / max-plus の2代数が双対に振る舞うことを体系化
   - 「同じ対象に異なる合成で律速逆転」の構造そのもの
2. **Krishnan (2014) "Flow-Cut Dualities for Sheaves on Graphs"** (arXiv 1409.6712)
   - Max-Flow Min-Cut の半環値 sheaf 一般化
   - flow と cut で min/max が双対化する categorical 定式化
3. **Ghrist, Gould & Lopez (2024) "Lattice-Valued Bottleneck Duality"** (arXiv 2410.00315)
   - **Theorem 3**: `⋁_P ⋀_e c(e) = ⋀_C ⋁_e c(e)` を分配束で証明
   - path (直列, ▷的) で meet 律速、cut (並列, ⊗的) で join 律速
   - **本プロジェクトの定理と数学的に同型**

→ 「Bottleneck Reversal Theorem」は**既出**。

### 残る新規性 (未踏領域)

サーベイで以下は確認:
- 用語 "bottleneck reversal" "asymmetric compositionality" は圏論文献に **0件**
- Baez-Master Open Petri Net の cospan-pushout (▷) と disjoint union (⊗) を **律速演算の非対称性で対比した研究はゼロ**
- Duoidal category (Aguiar-Mahajan, Shapiro-Spivak) で order-enriched 解釈はない
- **Heyting代数値** (分配束より強い) での bottleneck duality 翻訳は未確認

→ 本プロジェクトの貢献は **「既知の lattice bottleneck duality を、Open Petri Net (Baez-Master 2018) の文脈に翻訳する初の試み」** という incremental contribution。

### 修正された主張

> 「Ghrist-Gould-Lopez 2024 の Lattice-Valued Bottleneck Duality を、
> Open H-Petri Net (Baez-Master 2018 の Heyting版) に翻訳し、
> ASEAN モバイル金融の越境決済システムに具体応用する。
> これにより『域内決済統合は最弱国に律速』という政策的予言が
> 圏論的構造から自動的に出る。」

「世界初の定理」じゃなく「**既知の数学を新しい応用ドメインに翻訳**」のスタンス。
これでも価値はあるが、当初の主張より控えめ。

引用必須: Liebeherr 2017, Krishnan 2014, **Ghrist-Gould-Lopez 2024 (最重要)**。

---

## §1 本プロジェクトの中で位置づけ

サーベイ06, 07, V1-V3 を踏まえて、本プロジェクトの主張のうち **真に新規** と認められそうなのは事実上1個:

> **「同じ Petri net 集合に対し、合成方向 (⊗ vs ▷) で律速が逆転する」**

他の主張 (随伴 L⊣R、Heyting値拡張、Bakong vs GCash 構造比較等) は **既存の組み合わせ・別ドメイン応用** のレベル。
本ノートはこの仮説を **「世界初」を狙えるレベルまで** 詰める。

---

## §2 ⊗ (monoidal product) の振る舞いの厳密化

### 2.1 定義

`𝓚_HPN` の monoidal product `⊗` は **disjoint union of Petri nets**:

```
N_1 ⊗ N_2 = (P_1 ⊔ P_2, T_1 ⊔ T_2, F_1 ⊔ F_2, M_0^1 ⊔ M_0^2)
```

- 場所、遷移、フローを互いに **独立** に並べる
- 不可視場所も独立 (`P_h^1 ⊔ P_h^2`)
- merge なし

### 2.2 Heyting値の振る舞い

⊗ で合成された net `N_1 ⊗ N_2` における不可視場所 `p_h^i ∈ P_h^i` の Heyting値:

- `p_h^1` は `N_2` の遷移発火の影響を受けない (独立)
- 各 `p_h^i` の上限は `TrustHub_max(N_i)` で決まる

→ **合成後の Heyting値集合の "全体最大"** は:
```
max_{i} TrustHub_max(N_i)   = TrustHub_max(⊗_i N_i)
```

つまり **「⊗ は最強の構成要素で律速」** (=max bound)。
ASEAN10 で言えば、`F_Bakong ⊗ F_GCash ⊗ ... = ⊤_pub` (最強の中銀型の上限が全体を示す)。

### 2.3 直感的解釈

⊗ = 「並存」。ASEANの各国がそれぞれ独自の決済システムを運用してる状況。
ユーザーは backbone を「選ぶ」ことができ、最強のものを選べる。

例: フィリピン国民が GCash の代わりに InstaPay (BSP中銀型) を選べば、`⊤_priv` ではなく `⊤_bank` の Heyting値を享受できる。

---

## §3 ▷ (cospan-pushout) の振る舞いの厳密化

### 3.1 定義

`▷` は **Open Petri Net** の水平合成 (Baez-Master 2018):

```
O_1 ▷ O_2 = (N_1 + N_2 / ∼, i_1, o_2)
```

ここで `∼` は cospan に基づく **場所の merge** 関係:
- `o_1(y) ∼ i_2(x)` for matching ports
- merge された場所は **1個** になる

### 3.2 Heyting値の振る舞い

merge された不可視場所 `p_h^{merged}` における Heyting値:

両方の net から発火による Heyting値増分を受ける。両方の上限が **両方とも許容する** 必要がある (cospan の constraint propagation):

```
M(p_h^{merged}) ≤ TrustHub_max(N_1)
M(p_h^{merged}) ≤ TrustHub_max(N_2)
   ↓
M(p_h^{merged}) ≤ min(TrustHub_max(N_1), TrustHub_max(N_2)) = ⋀_i TrustHub_max(N_i)
```

→ **「▷ は最弱の構成要素で律速」** (=meet bound)。
ASEAN5 越境決済では:
```
F_TH(⊤_pub) ▷ F_SG(⊤_bank) ▷ F_MY(⊤_bank) ▷ F_ID(⊤_priv) ▷ F_PH(⊤_bank)
   ↓
合成後の TrustHub_max = ⊤_priv (ID の QRIS が律速)
```

### 3.3 直感的解釈

▷ = 「統合」。ASEAN域内で越境決済できるように **ポートを繋ぐ** 操作。
すべての国を経由する取引が出てくるので、1番弱い国の保証レベルでしか「全取引」を保証できない。

「越境統合は便利だが、信頼レベルが最弱国に落ちる」=これが直感の論理化。

---

## §4 律速逆転定理 (Bottleneck Reversal Theorem)

### 4.1 主張

**Theorem (Bottleneck Reversal)**:
H-Petri Net の有限集合 `{N_1, ..., N_n}` (各 `N_i` の TrustHub_max = `t_i ∈ H`) について、
合成方法によって全体の TrustHub_max が以下のように決まる:

```
TrustHub_max(⊗_i N_i) = ⋁_i t_i       (max bound, 最強で律速)
TrustHub_max(▷_i N_i) = ⋀_i t_i       (meet bound, 最弱で律速)
```

仮に `t_i` 達が **均一でない** (= `⋁ ≠ ⋀`) なら、
```
TrustHub_max(⊗_i N_i) > TrustHub_max(▷_i N_i)
```
が成立し、**合成方向の選択が結果を逆転させる**。

### 4.2 証明スケッチ

(`⊗` 側): §2.2 から、disjoint union では各 net が独立に Heyting値を保持。全体での最大値は各構成要素の最大値の `⋁`。

(`▷` 側): §3.2 から、cospan-pushout で merge された不可視場所は **constraint propagation** により、両方の net の上限の `⋀` で律速。

両者を比べると、`⋁_i t_i ≥ ⋀_i t_i` が Heyting代数の基本性質 (半順序の上限と下限の関係) から成立。等号は全 `t_i` が等しい時のみ。

詳細証明は §7 で完成予定。

### 4.3 ASEAN5 への具体的予言

- `⊗` 合成 (5国の並存): `⋁ = ⊤_pub` (TH PromptPay が最強)
- `▷` 合成 (5国の越境統合): `⋀ = ⊤_priv` (ID QRIS が最弱、足を引っ張る)

差分: `⊤_pub` と `⊤_priv` の **2段階の差** = `Heyting階数で 2 ランク**。

---

## §5 政策的含意

これは **反直観的な政策的予言**:

### 5.1 常識的視点

「ASEAN域内決済統合 (Project Nexus 等) を進めると、各国民の決済利便性が上がる」 ← 業界の常識

### 5.2 本定理の予言

「ASEAN域内決済統合を進めるほど、全取引が **最弱国の保証レベルに律速** される。
個別国民が中銀型 backbone (PromptPay) を選んで享受していた `⊤_pub` レベルの保証が、
越境決済に巻き込まれる瞬間に `⊤_priv` まで落ちる。」

### 5.3 反直観性

- 統合 = 強化 (常識) ↔ 統合 = 弱体化 (本定理)
- 「ASEAN市民は越境決済の便利を取って、信頼レベルを失う」というトレードオフ
- これが「便利と不可視コストの随伴 L⊣R」の **具体的・数値的な表現**

### 5.4 検証可能性

Project Nexus (BIS Innovation Hub, 2022〜) の公開資料で:
- 越境決済システムの信頼レベルが、個別国レベルより **低い** ことを示せれば、本定理が支持される
- 例: 越境決済の Service Level Agreement (SLA) が各国国内決済の SLA より低い場合、構造的支持

---

## §6 反例の探索

「律速逆転」が常に成立するか? 反例があれば定理が壊れる。

### 反例候補1: 全 `t_i` が等しい場合
`t_1 = t_2 = ... = t_n` なら `⋁ = ⋀`、逆転なし。
→ これは **退化ケース**。定理の前提から除外される。

### 反例候補2: cospan-pushout で constraint propagation が起きない場合
不可視場所が merge されない (= 独立) なら、▷ でも max bound になる。
→ これは「合成じゃない」ケース。実質的な ▷ ではない。

### 反例候補3: 非完備 Heyting代数
完備性がないと `⋁, ⋀` が存在しない。
→ 本プロジェクトは完備 Heyting代数を仮定 (notes/06 §2.1)、回避。

### 反例候補4: 異なる種類の Heyting代数の混合
各 `t_i` が異なる Heyting代数の元なら、`⋁, ⋀` は定義不能。
→ 本プロジェクトは共通の Heyting代数を仮定、回避。

→ **退化ケースを除き、定理は成立**。

---

## §7 Universal property としての一般化

### 7.1 監察 — これは monoidal vs cospan の対比の一般現象?

⊗ (monoidal product) は **coproduct-like** (disjoint union)。
▷ (cospan-pushout) は **pushout** = colimit の特定形。

Heyting代数の completed Heyting algebra (cHa) を考えると:
- coproduct: `⋁`
- pushout: ?

実は Heyting代数の上で、coproduct と pushout は **両方とも colimit** であるはず。
これらが律速的に逆転するのは、本当に新発見か?

### 7.2 仮説 (一般化)

**Hypothesis (General)**:
任意の symmetric monoidal double category において、対象 `X_1, ..., X_n` に
"capacity" (= Heyting値) を割り当てた場合:
- monoidal product の capacity = `⋁` (sup)
- horizontal composition の capacity = `⋀` (inf)

→ これが本当なら、Petri net に限らず **categorical な普遍現象**。

### 7.3 既存研究での先例

サーベイ 08 (進行中) で確認:
- "asymmetric compositionality" "bottleneck reversal" でヒットするか
- monoidal vs cospan の compositionality 文献

もし未踏なら、本プロジェクトの定理は **「ある enriched monoidal double category における coproduct と pushout の振る舞いの普遍法則」** として一般化できる。

---

## §8 ASEAN10 全展開予言

ASEAN10 全 backbone (10種) を全部:
- 並列 ⊗: `⊤_pub` (Bakong/PromptPay 中銀型のおかげ)
- 統合 ▷: `⊤_priv` (ID QRIS, VN MoMo, PH GCash, MY TNG 等が引きずる)

**10国の Heyting値分布**:
```
中銀型 (⊤_pub): TH, KH = 2国
銀行型 (⊤_bank): SG, LA, MM, BN = 4国
民間型 (⊤_priv): VN, ID, PH, MY = 4国
```

⋁ = `⊤_pub` (4-2-4 のうち最強)
⋀ = `⊤_priv` (最弱)

差は **Heyting階数で 2 ランク**。これが「越境統合の代償」の数値。

---

## §9 残る論点

1. **§4.2 証明の厳密化**:
   - cospan-pushout の constraint propagation を universal property から導出
   - completed Heyting algebra での meet 安定性
2. **§7 一般化の確認**:
   - サーベイ 08 結果待ち
   - 「asymmetric compositionality」が既存にあるか
3. **§5 政策的含意の実証**:
   - Project Nexus の公開資料調査
   - 各国 SLA 比較
4. **enriched 一般化**:
   - 完備 Heyting代数を一般の `V`-enriched category に拡張
   - これは Lawvere の metric space 流の一般化
5. **「最弱で律速」を回避する方法はあるか?**
   - 例: redundant ports (多重 cospan)
   - これで `⋀` を `⋁` 寄りにシフトできるか?
6. **時間軸の含意**:
   - 短期 (個別 ⊗ 状態): 強い
   - 長期 (統合 ▷ 進む): 弱くなる
   - ASEAN の歴史的軌跡をこの線で説明できるか

---

## §10 まとめ — これが本プロジェクトの「世界初」候補

本ノートの定理が本当に新規 (サーベイ 08 で確認) なら、本プロジェクトの中核貢献は:

> **「同じ要素集合の合成方向 (⊗ vs ▷) で律速が逆転する」一般定理。**
> **この定理を ASEAN モバイル金融に当てると、「越境統合は最弱国に律速」という反直観的な政策的予言が出る。**

これが他の主張 (Heyting値拡張、4 backbone 分類、関手 + 自然変換) と違って、**借用じゃなく発見** の可能性が一番高い箇所。

ここを徹底的に詰めるべき。

次のアクション:
- サーベイ08 (asymmetric compositionality) 結果待ち
- もし未踏確認 → notes/15 を論文骨格に格上げ
- 実装: Open H-Petri Net の Python で律速逆転を数値検証
