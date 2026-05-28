# 律速逆転サーベイ — ⊗ max / ▷ meet 仮説の新規性検証

調査日: 2026-05-24
検索回数: 15 (WebSearch 13 / WebFetch 5)

---

## 判定: **部分的に既出** (中核アイデアは複数領域に先行例あり、ただし「Petri net 圏論的合成における律速逆転」という特定の枠組みでの言明は未踏)

## 取得件数: 約65本 (有効に内容確認できたもの 12本)

---

## 直接競合する論文 (Top 3)

### 1. **Liebeherr (2017)** — *Duality of the Max-Plus and Min-Plus Network Calculus* (Foundations and Trends in Networking)
- **何を言ってる**: 同一の通信ネットワークに対し、min-plus algebra (容量・サービスを時間関数として扱う) と max-plus algebra (到着・出発時刻を扱う) という **2つの dual な代数構造** が存在し、それぞれで convolution / concatenation 演算が異なる挙動を示すことを体系化。両者は「underlying algebras は isomorphic だが network calculus 自体は isomorphic ではない」。
- **一致点**: **「同じシステムを2つの合成法で見ると、min と max が対称的に入れ替わる」**という観察は本仮説と本質的に同じ構造。律速の方向が代数の選択で決まる点も一致。
- **異なる点**: (a) 圏論的 (categorical) な定式化ではなく純粋に semiring/algebra ベース、(b) Petri net や cospan-pushout は扱わない、(c) network calculus (通信工学) の文脈に限定。本仮説の「圏論的観察」としての新規余地はここに残る。

### 2. **Krishnan (2014)** — *Flow-Cut Dualities for Sheaves on Graphs* (arXiv:1409.6712)
- **何を言ってる**: Max-Flow Min-Cut 定理を「半環値の sheaves」に一般化。directed (co)homology で flow と cut の双対を定式化。partial semimodule / quantale 上で議論。
- **一致点**: 「ネットワーク上で max と min が双対に振る舞う」現象を sheaf 理論 (=圏論的) に formalize した最も近い先行研究。半環選択で min/max が入れ替わる点も近い。
- **異なる点**: Petri net 合成 (cospan-pushout vs disjoint-union tensor) の対比という形ではなく、単一ネットワーク上の flow vs cut の双対。「合成方向で律速が反転」という言明はない。

### 3. **Ghrist, Gould & Lopez (2024)** — *Lattice-Valued Bottleneck Duality* (arXiv:2410.00315)
- **何を言ってる**: 古典的 bottleneck duality (max-min path = min-max cut) を **distributive lattice** 値容量に一般化。Theorem 3: ⋁_{P∈𝒫} ⋀_{e∈P} c(e) = ⋀_{C∈𝒞} ⋁_{e∈C} c(e)。pentagon/diamond lattice では成立しないことも証明。
- **一致点**: 「path (直列) では meet (∧) で律速、cut (並列) では join (∨) で律速」という構造そのもの。本仮説と数学的核心が完全に同型。
- **異なる点**: (a) Petri net や open systems の合成方向 (⊗ vs ▷) の議論ではなく古典的 flow network 内の path/cut, (b) 「bottleneck reversal」「asymmetric compositionality」という用語は使わず "lattice bottleneck duality" と呼ぶ, (c) cospan/monoidal product の対比は扱わない。

---

## 部分的に重なる論文 (Top 5)

### 4. **Baez & Master (2018, 2020)** — *Open Petri Nets* (arXiv:1808.05415, MSCS 2020) / Baez-Pollard *Reaction Networks*
- 開 Petri net を cospan で morphism として表現し、composition (pushout) と tensor (disjoint union) の2つの合成を symmetric monoidal double category で定式化。**ここでは律速の差は議論されていない** ― rate equation の挙動の compositional 保存が主題で、本仮説が指摘する「合成方向で律速演算が反転」という観察は明示されていない。**直接の余地。**

### 5. **Aguiar–Mahajan の duoidal category 系** (nLab; Garner-López Franco 2016 ほか) / Shapiro-Spivak (2022) *Duoidal Structures for Compositional Dependence*
- 2つの monoidal structure (★ と ◇) を持ち、lax interchange (A★B)◇(C★D) → (A◇C)★(B★D) で結ばれる構造。**parallel と sequential を別の monoidal とする** という本仮説の枠組みは duoidal の文脈で既に標準化。ただし「片方が max 律速、片方が meet 律速になる」という量的・順序的解釈は duoidal の主流テーマではない。**順序豊穣 (order-enriched) duoidal の特殊例として位置付ければ余地あり。**

### 6. **Katis-Sabadini-Walters + Sobocinski (2009)** — *Cospans and spans of graphs: a categorical algebra for the sequential and parallel composition of discrete systems* (arXiv:0909.4136)
- **sequential = cospan composition, parallel = span composition** と明示的に区別した先駆。本仮説の "⊗ = disjoint union, ▷ = cospan-pushout" の categorical 基礎はここに既出。ただし律速・bottleneck の量的解釈はなし。

### 7. **Cousot-Cousot 系 concurrent monoid** (Hoare ら) / 検索でヒットした *Concurrent monads for shared state* (ACM 2024)
- 「sequential と parallel の2つの monoid 構造 + inequational interchange law」を扱う。「parallel が weak、sequential が strong」のような構造的非対称性は議論される。本仮説の min/max 構造の特殊化として読める。

### 8. **化学反応における rate-determining step** (古典) + Curry-Montes (2026) *Categorical Perspectives on Chemical Reaction Networks* (arXiv:2604.04919)
- 「直列反応では最も遅いステップが律速」(meet 律速) は化学の常識。Curry-Montes は CRN を arrow category で扱うが、本仮説のような「並列合成では max が支配」との対比は明示していない。

---

## 関連語彙の探索結果

| 検索語 | 直接ヒット | 評価 |
|--------|-----------|------|
| "bottleneck reversal" (圏論文脈) | **0件** | この用語は未踏 |
| "asymmetric compositionality" (Petri net 文脈) | **0件** | この用語は未踏 |
| "meet vs join under different composition" | 0件 (Lattice-Valued Bottleneck Duality が最も近い) | 構造は既出だがこの言い方では未踏 |
| max-plus / min-plus network calculus duality | **多数** (Liebeherr monograph 中心) | **領域として確立済み** |
| duoidal category (parallel/sequential) | 多数 | 枠組みは標準化済み |
| cospan vs span (sequential/parallel) | 多数 (Katis-Sabadini-Walters 系) | 圏論的基礎は既出 |
| Petri net composition + bottleneck (categorical) | ほぼ 0 | **この交差点は空白** |

---

## 結論

### 本プロジェクトの仮説の新規性

**「⊗ で max 律速 / ▷ で meet 律速」という対比そのものは数学的に新規ではない。** 以下3つの先行領域にすでに本質的に同じ構造がある:

1. **Network calculus** (Liebeherr): min-plus と max-plus の合成演算の双対
2. **Sheaf-theoretic flow-cut duality** (Krishnan; Ghrist-Gould-Lopez): path で meet, cut で join という lattice bottleneck duality
3. **Duoidal categories**: 2つの monoidal structure を備えた標準的枠組み

### ただし、以下の **特定の組み合わせは未踏** と判定できる:

- **「open Petri net (Baez-Master) の cospan-pushout ▷ と disjoint-union ⊗ という *2つの categorical composition* で、律速演算が max ↔ meet に反転する」** という言明そのものは、検索範囲内では先行研究に見当たらない。
- "bottleneck reversal" / "asymmetric compositionality" という用語自体は未使用 (= naming の余地あり)。
- AlgebraicPetri / AlgebraicJulia の compositional framework 上での **定量的律速の compositional law** は議論されていない (rate constant の積としての保存は Baez-Pollard にあるが、律速の代数が合成方向で変わるとは言われていない)。

### プロジェクトの戦略的位置付け

本仮説を「完全新規」と主張するのは **不適切** (Liebeherr 2017 / Ghrist-Gould-Lopez 2024 と数学的に同型である事実は隠せない)。

正しい新規性主張は:
> "lattice bottleneck duality (既知) を open Petri net の categorical composition (▷ = cospan-pushout, ⊗ = disjoint union) の文脈に **持ち込み**、Baez-Master 圏論的枠組みで明示的に演算非対称性を述べる初の試み"

これなら **incremental だが正当な貢献** として位置付け可能。「カテゴリ理論×ボトルネック反転」を Petri net 合成に翻訳する貢献は確かに残されている。

ただし完全な新規性 (= no precedent in any field) は否定された。先行研究を必ず3本 (Liebeherr / Krishnan / Ghrist-Gould-Lopez) 引用したうえで「Petri net compositional bottleneck への翻訳」という限定された新規性として書くべき。
