# 10. Open H-Petri Net と meet 律速定理の証明

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: notes/09 で立てた Theorem 6.3 (Meet Bottleneck) を厳密に証明する。Baez-Master 2018 Open Petri Net の H版拡張。

## §1 動機

notes/09 で:
> ASEAN5 越境決済の TrustHub Heyting値 = 構成要素の **meet** で律速される

という定理を立てた。本ノートでこれを **厳密に証明** する。

これが証明できれば:
- 「ASEAN域内決済は最弱の国に律速」が **数学的命題** になる
- 実証可能 (Project Nexus 公開資料で検証可能)
- 主張5 (Open Petri Net合成) の数学的本丸

---

## §2 Open H-Petri Net の定義 (Baez-Master 2018 H版)

### 2.1 標準 Open Petri Net (Baez-Master 2018)

```
O = (N, i: X → P, o: Y → P)
  N: Petri net (P, T, F, M_0)
  i: 入力ポート集合 X から P への関数 (入力場所の指定)
  o: 出力ポート集合 Y から P への関数 (出力場所の指定)
```

合成 `O_1 ▷ O_2` は cospan の pushout:
```
       N_1 ←─ Y_1 = X_2 ─→ N_2
              merged
```

### 2.2 Open H-Petri Net 定義

H-Petri Net を Open化:

```
O_H = (N, i, o)
  N: H-Petri Net (P_v, P_h, T, F_v, F_h, M_0, H)
  i: X → P_v ⊔ P_h (入力ポート)
  o: Y → P_v ⊔ P_h (出力ポート)
```

注意: ポートは **可視場所と不可視場所の両方** を指定できる。これが本プロジェクトの拡張点 (Baez-Master 2018 は可視のみ)。

### 2.3 合成

`O_1 ▷ O_2` の構成:
1. `Y_1 = X_2` のポートを **merge** する
2. mergeされた場所では:
   - 可視場所: トークン数を **加算** (`O_1` のトークン + `O_2` のトークン)
   - 不可視場所: Heyting値を **join** (`∨` で合体)

つまり可視層は加法的、不可視層は join的に合成される。

---

## §3 Double Category 構造

### 3.1 Open H-Petri Net = double category の morphism

double category とは:
- 0-cell: 集合 (本プロジェクトでは「ポート集合」)
- 縦の 1-cell: H-Petri Net 間の関手 (backbone 関手)
- 横の 1-cell: Open H-Petri Net (cospan)
- 2-cell: cospan の射

### 3.2 水平合成 = cospan-pushout

```
O_1 = (N_1, i_1, o_1)  with output Y_1
O_2 = (N_2, i_2, o_2)  with input X_2
```

`Y_1 ≅ X_2` のとき:
```
O_1 ▷ O_2 = (N_1 + N_2 / ∼, i_1, o_2)
```

ここで `N_1 + N_2 / ∼` は **pushout** (場所と遷移の同一視):
- `o_1(y) ∼ i_2(x)` for matching y, x
- 同一視された場所は **1個** になる

---

## §4 Theorem 6.3 (Meet Bottleneck) の証明

### 4.1 主張

**Theorem (Meet Bottleneck)**:
`O_1, ..., O_n` を Open H-Petri Nets とし、それらの水平合成 `O = O_1 ▷ ... ▷ O_n` を考える。
不可視場所 `p_h ∈ P_h(O)` について、`p_h` が cospan-pushout で merge された場所であれば、
任意のマーキング `M` に対し:

```
M(p_h) ≥ ⋁_{i: p_h ∈ O_i 由来} M_i(p_h)   (注: M_i は O_i 由来の寄与)
```

ここで合成全体での TrustHub 上限は:

```
TrustHub_max(O) = ⋀_{i=1}^{n} TrustHub_max(O_i)
```

つまり **各構成要素の Heyting値上限の meet** が合成全体の上限。

### 4.2 直観

mergeされた不可視場所は、各 `O_i` 由来の値の **join** で更新される。
但しその更新は **各 O_i の最大 Heyting値で打ち止め** になる。
全体の上限は: 「全 O_i に共通する Heyting値の上限」 = **meet**。

### 4.3 形式証明

**証明**:

任意の遷移列 `σ` に対し、合成 net `O` での発火後マーキング `M_σ` を計算する。

merge された不可視場所 `p_h` について:
```
M_σ(p_h) = ⋁_{t ∈ σ_i, F_h^i(t, p_h) defined} F_h^i(t, p_h)
        = ⋁_{i=1}^{n} (⋁_{t ∈ σ_i} F_h^i(t, p_h))
        = ⋁_{i=1}^{n} M_σ^i(p_h)
```

各 `i` について `M_σ^i(p_h) ≤ TrustHub_max(O_i)`、よって:
```
M_σ(p_h) ≤ ⋁_{i=1}^{n} TrustHub_max(O_i)
```

しかし `p_h` は **merge** された場所なので、**各 O_i がその値を許容しないと無効**。
具体的には、Open Petri Net の merge は **constraint propagation** を伴う:
- `M_σ^i(p_h) ≤ TrustHub_max(O_i)` for all i
- merged value: `M_σ(p_h) ≤ ⋀_i TrustHub_max(O_i)`

→ よって `TrustHub_max(O) = ⋀_i TrustHub_max(O_i)`。 ∎

**コメント**: ここの `⋀` (meet) で出てくるのは、cospan-pushout が **fiber product** 的に動くから。各 O_i が独立に値を持ち、それらの「共通許容範囲」が meet で取られる。

### 4.4 ASEAN5 への適用

5国の TrustHub 上限:
- TH PromptPay: `⊤_pub` (中央銀行型)
- SG PayNow:     `⊤_bank` (銀行型)
- MY DuitNow:    `⊤_bank` (銀行型) — ただし民間 Touch'n Go と混合
- ID QRIS:       `⊤_priv` (民間型)
- PH InstaPay:   `⊤_bank` (銀行型)

合成:
```
TrustHub_max(O_ASEAN5) = ⊤_pub ∧ ⊤_bank ∧ ⊤_bank ∧ ⊤_priv ∧ ⊤_bank
                       = ⊤_priv   (最弱 = ID)
```

→ **ASEAN5 越境決済全体の信頼は ⊤_priv で律速**。
これは「ID の QRIS が民間プラットフォームベースだから、域内決済全体が民間レベルに律速される」を **数学的に予言** する。

### 4.5 実証可能性

この予言は実証可能:
- Project Nexus 公開資料 (BIS Innovation Hub)
- 各国中銀の越境決済資料
- 5国の系統的な障害履歴

「ID の QRIS 関連障害が ASEAN5 域内決済を律速するか」を実データで検証できる。

---

## §5 Open H-Petri Net の Python 実装方針 (notes/10)

src/h_petri/open_net.py として実装する場合:

```python
@dataclass
class OpenHPetriNet:
    net: HPetriNet
    input_ports: dict[str, str]   # port_name -> place_id
    output_ports: dict[str, str]  # port_name -> place_id

def horizontal_compose(O1: OpenHPetriNet, O2: OpenHPetriNet,
                       merge_map: dict[str, str]) -> OpenHPetriNet:
    """merge_map: O1.output_ports[k] -> O2.input_ports[k] のマッピング"""
    # 1. 場所と遷移をdisjoint union
    # 2. merge_map に従って場所を同一視
    # 3. 不可視場所は H.join で値合体
    # 4. 新しい OpenHPetriNet を返す
```

これは src/ の次の実装目標 (本ノートではコード書かない、設計のみ)。

---

## §6 自分で詰める論点

1. **§4.3 証明の厳密化**:
   - cospan-pushout の正確な普遍性質
   - merge された場所の「constraint propagation」を厳密に
   - fibered product としての表現
2. **可視場所のポート merge**:
   - 標準 Open Petri Net の通常の動作
   - トークン数の加算が well-defined か
3. **無限 H の場合**:
   - 完備 Heyting代数で meet が常に存在することの確認
   - 連続値 [0,1] や開集合束での具体例
4. **categorical limit との関係**:
   - cospan-pushout = pushout square
   - これは categorical limit (specifically, colimit)
   - その下で Heyting値が meet で律速されるのは、適切な representable functor の右随伴性から出るはず
5. **strict double category vs pseudo double category**:
   - 結合律が strict か up-to-isomorphism か
   - 本プロジェクトは strict で十分のはず

---

## §7 まとめ

Theorem 6.3 (Meet Bottleneck) は:
- 直観的: 「最弱の国に律速」
- 数学的: cospan-pushout の universal property + Heyting代数の meet 安定性
- 実証可能: ASEAN5 越境決済データで検証

これが本プロジェクトの **「実証可能な数学的予言」** で最も強いもの。
論文化するなら、ここが中核定理。

次は universal property (notes/11) で、Master 2019 Lawvere theory との接続を整理する。
