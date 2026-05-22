# Petri net 圏論研究 サーベイ

調査日: 2026-05-22
調査者: Claude (Opus 4.7) — Research subagent
調査範囲: Petri net の圏論的扱い、Open Petri Net、Heyting / 直観主義論理との接続、Stochastic、AlgebraicPetri.jl、東南アジアモバイル金融との既存研究確認

## 取得件数: 25本以上 (詳細は本文参照)

## コア論文 Top 5 (賈先生研究との接続強度で順序づけ)

### [Meseguer & Montanari, 1990] Petri Nets are Monoids
- venue: Information and Computation 88(2), 105-155 (SRI Tech Report 1988初出)
- link: https://www.semanticscholar.org/paper/Petri-Nets-Are-Monoids-Meseguer-Montanari/382a8fbe1be96c0651cc9c553b09cb8dcb80c091
- 中心定理: P/T-Petri net = "commutative monoidal category" (対称が恒等の対称strict monoidal category) の表示 (presentation) として見ることができる。Petri net と commutative monoidal category の間に随伴 (adjunction) が成立する。
- 本プロジェクトとの接続: **主張3 (backbone型 = P/T-invariant)** と直結。Petri net をモナド/モノイドで定式化したオリジナル論文。賈先生の "Strip Folding as Monoidal Category" (2022) と同じく「具体的構造を monoidal category として扱う」枠組みで、形式上の親和性が極めて高い。
- 引っ掛かりポイント: 30年以上前の論文で、「commutative monoidal category」は対称 strict monoidal category の "unusually strict" な変種である点が後続研究で繰り返し議論されている (collective-token vs individual-token philosophy)。

### [Baez & Master, 2018-2022] Open Petri Nets
- venue: arXiv:1808.05415 (v6: 2022/7/25), Mathematical Structures in Computer Science
- link: https://arxiv.org/abs/1808.05415
- 中心構成: 入出力 place を cospan で指定した "open" Petri net を定義し、それを対称 monoidal double category Open(Petri) の morphism として扱う。2種類の意味論 (operational / reachability) を symmetric monoidal double functor として与える。
- 本プロジェクトとの接続: **主張5 (域内決済合成 = Open Petri Net)** の本丸。Bakong/GCash/MoMo を「域内ノードを入出力 place として開いた Petri net」と捉え、cospan 合成で組み合わせる、というのはまさにこの論文の応用例として位置づけられる。
- 引っ掛かりポイント: composition が同型を除いてしか定まらないので double category が必要、という技術的詳細あり。学部3年生に説明する場合はこの "up-to-iso" の部分を慎重に扱う必要がある。

### [Master, 2019/2020] Petri Nets Based on Lawvere Theories
- venue: arXiv:1904.09091, Mathematical Structures in Computer Science 30 (2020), 833-864
- link: https://arxiv.org/abs/1904.09091
- 中心定理: Lawvere theory Q をパラメータとした Q-net を定義し、通常の Petri net, pre-net, integer net, elementary net をすべて特殊例として包含する。Q ごとに operational semantics の随伴を構成。
- 本プロジェクトとの接続: **主張2 (不可視コスト = 補助場所)** を「特殊化された Lawvere theory による Q-net」として記述できる可能性。手数料・FX スプレッドなどを Lawvere theory のオペレーションとして扱える。
- 引っ掛かりポイント: 一般化が強すぎて学部論文には重い。だが「Petri net は変種多数あるがすべて同じ枠組みで扱える」という基礎事実の引用に最適。

### [Genovese, Loregian, Palombi, 2021] A Categorical Semantics for Bounded Petri Nets
- venue: arXiv:2101.09100
- link: https://arxiv.org/abs/2101.09100
- 中心定理: 容量制約 (bounded) 付き Petri net を comonad / lax-monoidal-lax functor で内部化する。collective- と individual-token 両方の philosophy をカバー。
- 本プロジェクトとの接続: **主張4 (集中度 = ホットスポット)** に対応。「特定 place に token が集中すると詰まる」という挙動を bounded net として扱う基礎理論。モバイル金融の流動性プールの上限制約と相性が良い。
- 引っ掛かりポイント: comonad の話題は学部生には重め。"non-local" な外部意味論が議論されているのは応用上強力。

### [Genovese & Spivak, 2020] A Categorical Semantics for Guarded Petri Nets
- venue: arXiv:2002.02762
- link: https://arxiv.org/abs/2002.02762
- 中心定理: guard (条件付き発火) を持つ Petri net の意味論を、deterministic 版と side-effect 付き版の2 flavor で与える。Grothendieck 構成で guard を net 内部に内在化。
- 本プロジェクトとの接続: KYC / 規制チェック / 残高ガードなど「条件付き取引」を内部化する自然な枠組み。**主張2** にも接続 (ガード条件としての規制コスト)。
- 引っ掛かりポイント: Spivak は AlgebraicJulia の中心人物の一人なので、AlgebraicPetri.jl への接続経路としても重要。

---

## 各主張に対する既存研究マッピング

| 本プロジェクト主張 | 既存研究 | カバー度 |
|---|---|---|
| **主張1**: リープフロッグ = reachability | Mayr 1981 (decidability), Czerwinski et al. 2019/2021 (non-elementary lower bound, Ackermann完全), Esparza decidability survey | **高** — 古典中の古典。reachability そのものは完全に確立。ただし「経済発展段階のスキップ」を reachability で形式化した先行例は見当たらず、応用面では新規性あり |
| **主張2**: 不可視コスト = 補助場所 | Abdulla et al. "Petri Nets with Time and Cost" (arXiv:1302.3291), Priced Timed Petri Nets, Master 2019 (Q-net) | **中** — 「cost place」概念自体は priced/timed Petri net で確立。「観測されない隠しコスト」という社会経済的解釈は独自性あり |
| **主張3**: backbone型 = P/T-invariant | Meseguer-Montanari 1990, 標準的 invariant 解析理論 (Murata 1989, Schmidt et al.) | **高** — P-invariant / T-invariant は構造解析の標準ツール。"backbone" としての解釈は応用側の貢献 |
| **主張4**: 集中度 = ホットスポット | Genovese-Loregian-Palombi 2021 (bounded), Coverability analysis (Lipton 1976, EXPSPACE-complete) | **中** — bounded net と coverability で形式化済み。「決済システムの集中度」という具体応用は薄い |
| **主張5**: 域内決済合成 = Open Petri Net | Baez-Master 2018, Patterson-Halter (epidemiological structured cospans 2020), AlgebraicPetri.jl | **高** — 理論側は完全装備。Bakong/GCash/MoMo への直接適用例はゼロ |

---

## 穴の仮説 (本プロジェクトの新規性候補)

### 仮説H1: Heyting algebra × Petri net は実質的に空白
- 既存研究の主流は **linear logic × Petri net** (Engberg-Winskel quantale, Brown-Gurr dialectica, de Paiva)
- Heyting algebra (直観主義論理) と Petri net を直接結ぶ論文は本サーベイ内に見当たらない
- 関連は2段階を介す: (a) quantale = 線形直観主義論理の代数, (b) complete Heyting algebra = 直観主義論理の代数
- Dialectica Petri Nets (Lavore-Leal, Fundamenta Informaticae 2025) でも Heyting への明示的接続は薄い (lineale としての言及程度)
- **賈先生 "Heyting Algebra in Flat Origami" (2024) と接続するなら、ここが最大の新規性候補**

### 仮説H2: モバイル金融 (Bakong/GCash/MoMo) の Petri net 形式化はゼロ
- M-Pesa, GCash, MoMo 等を colored / 形式 Petri net で記述した論文は本サーベイで発見されず
- 既存の「Petri net × 銀行」は通常の振込・ATM (Moldavian 2017, 中国系 CPN ベース論文) に限定
- **応用論文としてのオリジナリティは確保しやすい**

### 仮説H3: "Leapfrog 発展 = reachability problem" という解釈の数理化
- ICT4D 分野で leapfrog は標準語彙だが、Petri net reachability で形式化した先行研究は見当たらない
- 形式化により「どの発展段階はスキップ可能か = reachable か」を明示的に議論できる
- 経済学・開発学側へのリーチを持つ独自貢献

### 仮説H4: AlgebraicPetri.jl での東南アジア金融モデリングは未開拓
- AlgebraicPetri.jl は epidemiology (SIR等) に集中しており、金融応用例は薄い
- structured cospan で「国境を跨ぐ決済の合成」を実装する例として新規性あり

### 仮説H5: Heyting × Open Petri Net の二重新規性
- "open" な Petri net (Baez-Master) に直観主義論理的「未確定/possibility」を組み込んだ研究はゼロ
- 賈先生研究室との接続性が最も高い

---

## 賈先生研究との接続マップ

### Strip Folding (Jia-Mitani 2022/2023) × Petri net
- 共通枠組: 両者とも具体的構造 (折り紙の折り目 / Petri net の発火) を **monoidal category** として表示する
- Strip folding は単一の物理紙片の折り順序 = sequential composition、Petri net は並列発火 = parallel composition
- 折り目の Boolean matrix 表現は Petri net の incidence matrix と類似構造
- **接続点**: 「離散的状態遷移を boolean / non-negative integer matrix で表現し、monoidal category として抽象化する」共通アプローチ。論文導入の「先行研究」セクションで自然に接続可能

### Heyting Algebra in Flat Origami (Jia 2024) × Petri net
- **これは最重要かつ最も空白**。仮説H1の通り、Petri net と Heyting algebra を直接結ぶ既存研究は実質ない
- 折り紙の「折るか折らないか」の不確定性が Heyting algebra で記述されるなら、Petri net の「発火するかしないか」の possibility も同様の構造を持ちうる
- 提案: Petri net の reachability set を frame / locale として扱い、Heyting algebra 構造を抽出する研究
- 申先生研究室で進める場合、これが学部卒論〜修論の中核テーマになりうる

### Jia-Floridi "Categorical Analysis of LLMs" (arXiv:2512.09117, 2025) × Petri net
- LLM を categorical 視点で分析する手法と、Petri net の categorical semantics は共通の言語 (functor, monoidal category) を使う
- LLM の token 生成プロセス自体を一種の "stochastic Petri net" として扱う可能性 (Baez-Biamonte の stochastic mechanics と接続)
- 直接の応用は遠いが、賈先生研究室の「現実現象を圏で記述する」方法論に Petri net を加える正当化として機能する

---

## 補足: その他の重要文献

### Sassone系
- Vladimiro Sassone "On the Category of Petri Net Computations" (eprints.soton.ac.uk/261951)
- Sassone "An Axiomatization of the Category of Petri Net Computations"
- "strongly concatenable processes" を導入。Meseguer-Montanari の精密化

### Joyal-Street 1991 "Geometry of Tensor Calculus, I"
- venue: Advances in Mathematics 88(1), 55-112
- string diagram の数学的基礎。Petri net を string diagram として描く際の理論的根拠
- 本プロジェクトでの図示の正当化に必須引用

### Kock 2022 "Whole-grain Petri Nets and Processes" (Journal of the ACM)
- Σ-nets / digraphical species として Petri net を presheaf category に埋め込む
- Patterson-Halter の AlgebraicPetri.jl 実装の理論基盤

### Baldan-Corradini-Montanari-Ribeiro "Open Petri Nets: Non-deterministic Processes and Compositionality" (2008)
- Baez-Master 以前の "open net" 系譜。colimit ベースの合成

### Dialectica Petri Nets 系
- Brown-Gurr 1996, de Paiva 2005 (Categorical multirelations)
- Lavore-Leal "Dialectica Petri Nets" (Fundamenta Informaticae, 2025, arXiv:2105.12801)
- de Paiva-Syropoulos "Dialectica Fuzzy Petri Nets" (arXiv:2003.04712)

### 確率/連続時間
- Abdulla et al. "Petri Nets with Time and Cost" (arXiv:1302.3291)
- Baez-Biamonte "Quantum Techniques in Stochastic Mechanics" (World Scientific 2018) — stochastic Petri net の categorical 扱い

### Reachability complexity
- Czerwinski et al. "The Reachability Problem for Petri Nets is Not Elementary" (arXiv:1809.07115)
- Leroux-Schmitz "Reachability Problem for Petri Nets is Not Primitive Recursive" (arXiv:2104.12695)
- Lipton 1976 (EXPSPACE lower bound), Mayr 1981 (decidability)

### 実装
- AlgebraicJulia/AlgebraicPetri.jl: https://github.com/AlgebraicJulia/AlgebraicPetri.jl
- Catlab.jl: 同 organization, applied category theory framework
- Libkind 2022: stratification methods

---

## 結論

1. **理論基盤は完備**: Petri net の categorical 扱いは Meseguer-Montanari (1990) 〜 Baez-Master (2018) 〜 Master (2019) で十分整っており、本プロジェクトはこれを応用できる
2. **応用は空白**: 東南アジアモバイル金融 (Bakong/GCash/MoMo) を Petri net で記述した先行研究はゼロ。leapfrog = reachability の形式化も先行例なし
3. **賈先生研究との接続の鍵は Heyting algebra**: Petri net × Heyting algebra は実質空白で、賈先生の Flat Origami 論文と接続できれば二重に新規性が立つ
4. **実装パス**: AlgebraicPetri.jl を使えば structured cospan による合成が即実装可能。Julia + Catlab で東南アジア金融ネットワークのプロトタイプを作れる
