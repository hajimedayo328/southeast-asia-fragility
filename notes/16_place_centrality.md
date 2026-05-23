# 16. 主張4 厳密化 — Petri net 上の場所中心性 (Place Centrality)

**作成日**: 2026-05-23
**ステータス**: draft v1
**位置づけ**: notes/05 §3 主張4 「集中度 = Petri net のホットスポット」を数学的に詰める。HHI (経済学の集中度指標) との対応も明示。

## §1 動機

主張4 (notes/05 §3) は俯瞰レベルで残ってた:

> 「すべての遷移が経由する場所 = ハブ」
> 「HHI を Petri net 上で再定義」

これを厳密化して、Bakong/GCash の場所中心性スコアを **数値で出せる** 状態にする。
これが詰まれば、HTML可視化で「どの場所がボトルネックか」のヒートマップを出せる。

---

## §2 グラフ理論的中心性のクイック復習

普通のグラフ `G = (V, E)` における主要中心性:

| 指標 | 定義 | 意味 |
|---|---|---|
| **Degree centrality** | `C_d(v) = deg(v) / (|V|-1)` | 直接の接続数 |
| **Betweenness centrality** | `C_b(v) = ∑ σ(s,t|v) / σ(s,t)` (s,t を結ぶ最短路のうち v を通る割合) | 「経由ノード」としての重要度 |
| **Eigenvector centrality** | 隣接行列 A の主固有ベクトル | 「重要なノードに繋がってる」度 |
| **PageRank** | random walk の定常分布 | フローの集中度 |
| **Closeness centrality** | `C_c(v) = (|V|-1) / ∑_u d(u,v)` | 距離の近さ |

Petri net は二部グラフ (場所と遷移)、フロー有り。これらを **「場所」を対象に適応** する必要がある。

---

## §3 Petri net 上の場所中心性 — 形式定義

### 3.1 基本フロー隣接行列

H-Petri Net `N = (P, T, F)` から:
- `B^- ∈ ℕ^{P × T}`: pre-incidence matrix (`B^-[p,t] = F(p,t)`)
- `B^+ ∈ ℕ^{P × T}`: post-incidence matrix (`B^+[t,p] = F(t,p)`)
- `C = B^+ - B^-`: incidence matrix
- `R = B^- (B^+)^T ∈ ℕ^{P × P}`: 場所間の「同一遷移で繋がる」関係

### 3.2 Petri net 場所中心性 — 5つの候補

#### (i) Transition Coverage Centrality (TCC)

> 「全遷移のうち、その場所を pre/post に含む割合」

```
TCC(p) = |{t ∈ T : F(p,t) > 0 ∨ F(t,p) > 0}| / |T|
```

直感: 場所がどれだけ多くの遷移に関与してるか。

#### (ii) Token Flow Centrality (TFC)

> 「ランダムな取引フローのうち、その場所を経由する期待値」

シミュレーション or `B^- (B^+)^T` の支配的固有ベクトルで近似。

```
TFC(p) = (left eigenvector of B^- (B^+)^T )_p
```

#### (iii) Bottleneck Index (BI)

> 「その場所を除いた net における到達可能性が、元の net より何%減るか」

```
BI(p) = 1 - |Reach(N \ {p}, M_0)| / |Reach(N, M_0)|
```

直感: 場所 p がデッドロックを引き起こす確率の指標。

#### (iv) Heyting Concentration Centrality (HCC) ★本プロジェクト独自

> 「その場所が不可視層 (Heyting値層) の TrustHub に与える影響の上限」

```
HCC(p) = ⋁_{t: p ∈ pre(t)} F_h(t, TrustHub)
```

直感: 場所 p を経由する遷移が、TrustHub に書き込む Heyting値の最大値。

#### (v) HHI-Analog Centrality (HHI-AC)

> 古典的 HHI = `∑_i s_i^2` (各 backbone のシェア二乗和) の Petri net 版

`s_p = TCC(p)` とすると:
```
HHI-AC(N) = ∑_{p ∈ P} TCC(p)^2
```

これは net 全体の **集中度スコア** (一個の場所が支配的なら大きい、分散してれば小さい)。

---

## §4 Bakong vs GCash での計算 (具体)

### 4.1 Bakong の場所中心性

5可視場所 + 2不可視場所:
| 場所 | TCC | TFC | BI | HCC | 解釈 |
|---|---|---|---|---|---|
| UserWallet | 1/5 | 中 | 中 | - | 入口、無くせない |
| PendingTx | 2/5 | 中 | 中 | - | バッファ |
| **NBCBackbone** | **2/5** | **高** | **最高** | - | **bottleneck** |
| SettledTx | 3/5 | 中 | 中 | - | 中継 |
| RecipientWallet | 1/5 | 中 | 低 | - | 出口 |
| TrustHub | 0/5 (post only) | - | - | `⊤_pub` | 不可視 |
| SystemicLoad | 0/5 (post only) | - | - | `⊤_bank` | 不可視 |

→ **NBCBackbone が Bakong の bottleneck**。
これを取り除くと全遷移が止まる (BI = 最高)。

### 4.2 GCash の場所中心性

| 場所 | TCC | TFC | BI | HCC | 解釈 |
|---|---|---|---|---|---|
| UserWallet | 1/5 | 中 | 中 | - | 入口 |
| PendingTx | 2/5 | 中 | 中 | - | バッファ |
| **GlobeBackbone** | **2/5** | **高** | **最高** | - | **bottleneck** |
| SettledTx | 3/5 | 中 | 中 | - | 中継 |
| RecipientWallet | 1/5 | 中 | 低 | - | 出口 |
| TrustHub | 0/5 (post only) | - | - | `⊤_priv` | 不可視 |
| SystemicLoad | 0/5 (post only) | - | - | `⊤_priv` | 不可視 |

→ **GlobeBackbone が GCash の bottleneck**。
構造的に同型だが、HCC (Heyting Concentration Centrality) で見ると **両者の上限が違う**。

### 4.3 HHI-Analog Centrality 比較

両 net 共に同じ TCC 分布:
```
HHI-AC = (1/5)^2 + (2/5)^2 + (2/5)^2 + (3/5)^2 + (1/5)^2 + 0 + 0
       = 0.04 + 0.16 + 0.16 + 0.36 + 0.04 = 0.76
```

→ HHI-AC では Bakong と GCash は **同じ**。
これは標準的な「構造的集中度」では両者が区別できないことを意味する。

→ **本プロジェクトの貢献**: HHI-AC ではなく **HCC で測ると差が出る**。
古典的集中度指標では捉えられない構造的差を、Heyting値で捉える。

---

## §5 圏論的解釈

### 5.1 中心性 = 関手の有界性

場所中心性は **関手 `Heyting Petri Net → ℝ_≥0` の universal property** として書ける。

具体的に:
```
TCC: HPN → [0, 1]   (functor preserving disjoint union as +)
HCC: HPN → H        (functor preserving disjoint union as ⋁)
```

これらは **monoidal 関手** として well-defined (notes/13 §4 から)。

### 5.2 Right Kan extension としての中心性

Jia-Floridi 2025 の右Kan拡張 `Ran_p(g∘c)` は「能力の上限」を表現。
本プロジェクトの場所中心性 (HCC) も同様に Kan拡張で書ける可能性:

```
HCC(p) = Ran_{inclusion: {p} → P} (F_h restricted to p)
```

これが正しければ、**主張4 が Jia-Floridi 2025 の道具を再利用する** 形になる (主張2 と並ぶ Kan拡張応用)。

---

## §6 実装方針 (src/h_petri/centrality.py)

```python
def transition_coverage_centrality(net: HPetriNet, place: str) -> float:
    """TCC: ratio of transitions involving the place"""
    count = sum(
        1 for t in net.transitions
        if place in net.pre_visible(t) or place in net.post_visible(t)
    )
    return count / len(net.transitions) if net.transitions else 0

def bottleneck_index(net: HPetriNet, place: str, M_0: Marking, max_steps: int = 50) -> float:
    """BI: 1 - |reach(N\\{p})| / |reach(N)|"""
    full_reach = reachable_markings(net, M_0, max_steps)
    if place in net.places_visible:
        # remove place and all transitions touching it
        net_minus = remove_place(net, place)
        partial_reach = reachable_markings(net_minus, M_0, max_steps)
    else:
        partial_reach = reachable_markings(net, M_0, max_steps)  # invisible places don't gate firing
    if not full_reach: return 0
    return 1 - len(partial_reach) / len(full_reach)

def heyting_concentration_centrality(net: HPetriNet, place: str) -> str:
    """HCC: max Heyting value written to place by any transition"""
    H = net.heyting
    value = H.bottom
    for (t, p), h_val in net.flow_heyting.items():
        if p == place:
            value = H.join(value, h_val)
    return value

def hhi_analog(net: HPetriNet) -> float:
    """HHI-AC: sum of TCC squared over all places"""
    return sum(
        transition_coverage_centrality(net, p) ** 2
        for p in net.places_visible
    )
```

これを src/h_petri/centrality.py として実装可能。次のセッションで。

---

## §7 残る論点

1. **TFC (eigenvector-based) の厳密定義**
   - フロー行列 `B^- (B^+)^T` の意味づけ
   - エルゴード性、収束性
2. **BI の計算複雑度**
   - 一般 Petri net で reachability は EXPSPACE
   - bounded net なら多項式
3. **HCC の意味的な深さ**
   - 「Heyting値の最大上限」と「実際に発火される頻度」の関係
   - dynamic vs static
4. **Kan拡張表現の厳密化** (§5.2)
   - 本当に右Kan拡張で書けるか
   - もし書けるなら Jia-Floridi 2025 の道具を完全に再利用
5. **HHI-AC と古典 HHI の対応**
   - 経済学の HHI は「市場シェア」の二乗和
   - Petri net の TCC は「遷移カバレッジ」、市場シェアと違う
   - 直接の数値比較ができるか?

---

## §8 まとめ

主張4 は5つの中心性指標で書ける:
- TCC (transition coverage)
- TFC (token flow)
- BI (bottleneck index)
- **HCC (Heyting concentration centrality) ★本プロジェクト独自**
- HHI-AC (HHI analog)

Bakong vs GCash の構造的中心性は **同じ** (TCC, BI 等)。
だが **HCC では永久に違う** (上限が Heyting半順序で異なる)。

→ **「古典的集中度指標では捉えられない差を、Heyting値で捉える」が本プロジェクトの貢献**。

これで主張4 を整理完了。次の実装は src/h_petri/centrality.py。
