# 軸⑤: Higher category / Fibration の応用論文サーベイ

調査日: 2026-05-14
担当: リサーチエージェント
対象: Grothendieck fibration / Higher category / Operad / Categorical Systems Theory の応用、および Yiyang Jia (圏論×折り紙×LLM) の論文全件

---

## A. Yiyang Jia (圏論×折り紙×LLM) の論文

> **注意**: Google Scholar に登録されている "Yiyang Jia" は Weizmann Institute の物理学者（SYK モデル・量子カオス専門）で **別人**。圏論×折り紙×LLM の Yiyang Jia は scholar 個別プロフィールが立っておらず、各論文の著者欄から辿る必要がある。共著者の三谷純（筑波大）から逆引きするのが安定。

### [Jia & Mitani 2022] Category of Strip Folding in Terms of a Boolean Matrix Representation
- venue: JP Journal of Algebra, Number Theory and Applications, Vol. 58 (2022)
- link: https://pphmjopenaccess.com/index.php/jpjana/article/view/949 （"Order Theory in Strip Folding" として再録/関連論文あり）
- 要旨: 短冊折り（strip folding）の状態をブール行列で表現し、それらを射とする圏を構成。折り操作の合成が圏の合成として整理される最初期の論文。
- 本プロジェクトとの接続: 「物理操作 = 射」「状態 = 対象」という抽象化テンプレ。インフラ整備を「国を対象、ファイナンス・工事介入を射」と置く発想と並行。
- 引っ掛かりポイント: ブール行列という具体表現を圏として扱う「実装可能な圏」のテンプレ。可視化・計算可能性が高い。

### [Jia & Mitani 2023] Making Strip Folding a Monoidal Category
- venue: JP Journal of Algebra, Number Theory and Applications, Vol. 61, No. 1 (2023)
- link: https://pphmjopenaccess.com/index.php/jpjana/
- 要旨: 上記2022を発展させ、strip folding に monoidal 構造（テンソル積）を入れる。短冊の並列接続が monoidal product に対応。
- 本プロジェクトとの接続: 並列実装（複数国で同時に同じプロジェクト）の構造化を monoidal で書けるのか、というヒント。リープフロッグの「並列射」と monoidal product の関係を検討する材料。
- 引っ掛かりポイント: 「順次合成 ≠ 並列合成」を圏論で明示的に分けたいときの標準パターン。

### [Jia & Mitani 2024] Heyting Algebra in Flat Origami
- venue: JP Journal of Algebra, Number Theory and Applications, Vol. 63, No. 5 (2024)
- link: https://pphmjopenaccess.com/index.php/jpjana/article/view/1938
- 要旨: フラット折り紙の状態圏を局所化し、Heyting 代数構造を入れる。(0,1)-topos にはなるが Grothendieck topos にはならないことを示す。「折りたためる/たためない」を論理的に扱う。
- 本プロジェクトとの接続: 「制度的に可能/不可能」を Heyting で扱えるかどうかの参考。ASEAN 各国の規制差分を「論理的可能性の格子」として表現する筋道がある。
- 引っ掛かりポイント: **(0,1)-topos だが Grothendieck topos ではない**という結論は、社会システムでも「直感的には topos 的だが厳密には違う」結論に至る可能性を予告している。

### [Jia 2024] Validity of Boundary Orders in Flat-Folding 1-Diagonal Grid Patterns
- venue: Advances and Applications in Discrete Mathematics (PPH)
- link: https://pphmjopenaccess.com/aadm/article/view/3537
- 要旨: 折り紙の境界順序の妥当性を判定する組合せ論的結果。圏論的視座は弱いが、上記圏論シリーズの数理的下支え。
- 本プロジェクトとの接続: ローカルな順序整合性が大域的折りたたみ可能性を決める、という観点は、ASEAN域内の国別ペース不整合が全体プロジェクトの実現可能性に効くロジックと対応。
- 引っ掛かりポイント: 「local validity → global feasibility」の組合せ条件。

### [Jia, Peng, Yang, Chen 2025] Category-Theoretical and Topos-Theoretical Frameworks in Machine Learning: A Survey
- venue: Axioms (MDPI), Vol. 14, Issue 3, Article 204 (March 2025) / arXiv:2408.14014
- link: https://www.mdpi.com/2075-1680/14/3/204 / https://arxiv.org/abs/2408.14014
- 要旨: ML を「勾配ベース」「確率ベース」「不変性ベース」「topos ベース」の4視点で圏論的に整理。topos 視点は本サーベイが初めて体系化。
- 本プロジェクトとの接続: 「複雑な実装を抽象構造で統一して整理する」というメタテンプレ。ASEAN を fibration で整理する論文を書く際、この survey と同じ「複数視点メタ整理」の型を踏襲できる。
- 引っ掛かりポイント: topos-based learning が初体系化。フィードバック付きの社会システム（実装→影響→次の実装）を topos で書く可能性。

### [Floridi, Jia, Tohmé 2025] A Categorical Analysis of Large Language Models and Why LLMs Circumvent the Symbol Grounding Problem
- venue: arXiv:2512.09117 / SSRN 5894082 (Dec 2025)
- link: https://arxiv.org/abs/2512.09117
- 要旨: 圏 Rel において、人間ルート H→C→Pred(W) と LLM ルート H→C'→G×C'→O→Pred(W) を並べ、訓練パイプライン C→C'→D(C')→G を関手として書く。LLM はシンボル接地問題を「解く」のではなく「迂回」していると主張。
- 本プロジェクトとの接続: **これがユーザーのASEAN論文と同型の発想**。「文脈→国」の置換でほぼそのまま使える型。Floridi（哲学者）がエンドースしているため、ASEAN論文の権威付け参照として最有力。
- 引っ掛かりポイント: 関手 D: C → C' を「データ生成過程」と読んでいる箇所が、ASEAN論文でいう fibration の cleavage（持ち上げ）と相似。

### [Jia, Wei, Yang, Peng 2025] Modeling GRNs with a Probabilistic Categorical Framework
- venue: arXiv (Aug 2025)、Molecular Networks / ML / Category Theory
- link: arxiv.org 2025-08 リストに掲載（具体IDは未確認）
- 要旨: 遺伝子制御ネットワーク（GRN）を確率的な圏論的フレームで定式化。
- 本プロジェクトとの接続: 「ネットワーク × 確率 × 圏論」の応用ケース。ASEAN のインフラ依存ネットを確率的圏で書くアプローチの先例として参照。
- 引っ掛かりポイント: Jia先生が「LLM以外の社会的・生物的ネットワーク」にも圏論を応用していることの証拠。研究方向としての汎用性。

---

## B. Grothendieck Fibration / Indexed Category の応用

### [Shulman 2008→継続] Framed bicategories and monoidal fibrations / [Moeller & Vasilakopoulou 2020] Monoidal Grothendieck Construction
- venue: Theory and Applications of Categories, Vol. 35, No. 31 (2020) / arXiv:1809.00727
- link: http://www.tac.mta.ca/tac/volumes/35/31/35-31abs.html / https://arxiv.org/abs/1809.00727
- 要旨: 古典的な fibration ↔ indexed category 同値を monoidal 設定に拡張。network model や open systems への応用例を提示。
- 本プロジェクトとの接続: 「ネットワークモデルを monoidal fibration で書く」フォーマルな根拠。ASEAN 連結インフラを束ねるメタ構造の数学的バックボーン。
- 引っ掛かりポイント: monoidal にしたとたん applied 寄りの例（network model, systems）が一気に出るのが特徴。

### [Diaconescu 2002→継続] Grothendieck Institutions
- venue: Applied Categorical Structures (2002)
- link: https://www.researchgate.net/publication/226106039_Grothendieck_Institutions
- 要旨: 異なる論理体系を「institution」として束ねるとき、Grothendieck構成で異種論理を統合できることを示す。
- 本プロジェクトとの接続: **異種ドメイン（国・規制・通貨）を一つの圏に束ねる**という発想の決定的先例。ASEAN 各国の制度を異種 institution と見て Grothendieck で統合できるかどうかが論点になる。
- 引っ掛かりポイント: 「異種を一つに束ねる正準パターン = Grothendieck」が institution 理論で40年確立済み。再発明にならないように丁寧に位置づけたい。

### [Goguen & Burstall 1992] Institutions: Abstract Model Theory for Specification and Programming
- venue: Journal of the ACM (1992)
- link: https://dl.acm.org/doi/10.1145/147508.147524
- 要旨: 論理体系を抽象化する institution の元論文。fibration / indexed category を使って論理を整理。OBJ / CafeOBJ / Maude / CASL の理論基盤。
- 本プロジェクトとの接続: 「ドメインを fibration で統一する」という思想の祖。ASEAN 論文の background section で引用必須クラス。
- 引っ掛かりポイント: 「異論理間の翻訳をどう保つか」が institution morphism として書かれている。国別制度間翻訳と直接相似。

---

## C. David Spivak 系: Operad / Wiring Diagram / Polynomial Functors

### [Spivak 2013] The Operad of Wiring Diagrams: Formalizing a Graphical Language for Databases, Recursion, and Plug-and-Play Circuits
- venue: arXiv:1305.0297
- link: https://arxiv.org/abs/1305.0297
- 要旨: 配線図（wiring diagram）が operad の射をなすことを示し、データベースクエリ・回路・recursion を統一フレームで扱う。
- 本プロジェクトとの接続: 「複合システムを差し込み式（plug-and-play）に合成する」テンプレ。インフラのモジュール合成・国境越え接続を operad で書く準備。
- 引っ掛かりポイント: 「自己相似性」を operad で表現できる点。ASEAN内ハブ＆スポークの再帰構造との相性。

### [Niu & Spivak 2023] Polynomial Functors: A Mathematical Theory of Interaction
- venue: arXiv:2312.00990 / Cambridge LMS Lecture Notes 498 (Topos Institute 出版)
- link: https://arxiv.org/abs/2312.00990 / https://toposinstitute.github.io/poly/poly-book.pdf
- 要旨: 多項式関手の圏 Poly を「相互作用」の数学的基盤として整備。動的システム・データベース・型理論・意思決定をカバー。
- 本プロジェクトとの接続: 「ポジション × 方向」というシンプルな抽象が、政策プラットフォーム（複数選択肢の中での実装方向選定）と相似。
- 引っ掛かりポイント: Niu は NASA の Advanced Air Mobility Architecture に応用中。**インフラへの実応用例**として最先端。

### [Spivak & Vicary 2021] Double Categories of Open Dynamical Systems
- venue: arXiv:2005.05956 / EPTCS (ACT2020)
- link: https://arxiv.org/abs/2005.05956
- 要旨: 行動型（behavior type）を区間上の sheaf として導入し、open dynamical system を double category として扱う。Willems 流の「変数共有」を indexed double category で表現。
- 本プロジェクトとの接続: 「変数共有 = 国境越え依存」と読み替えれば、ASEAN 各国システムの相互依存を double category で書ける。
- 引っ掛かりポイント: **indexed double category** という構造が、ユーザーの fibration p:𝓘→𝓒 を「二層に拡張」する自然な道筋。

### [Spivak 2016] Dynamical Systems and Sheaves
- venue: Applied Categorical Structures (Springer) / arXiv:1609.08086
- link: https://arxiv.org/abs/1609.08086
- 要旨: 動的システムを sheaf として扱う。時間軸上のローカル情報の貼り合わせとして系を構成。
- 本プロジェクトとの接続: 「ローカル整合性 → 大域整合性」のテンプレ。各国の局所政策が時間軸で一致するかどうかを sheaf で書ける。
- 引っ掛かりポイント: Heyting algebra in flat origami (Jia 2024) の論理構造と sheaf 的視点の接続。

---

## D. Categorical Systems Theory / Compositional Models

### [Myers 2022→継続] Categorical Systems Theory（書籍ドラフト）
- venue: 書籍ドラフト（公開中、Topos Institute）
- link: https://www.davidjaz.com/Papers/DynamicalBook.pdf
- 要旨: 一般システム理論を圏論で再構築。決定論的・微分的・確率的システムを double category と lens / wiring diagram で統一。
- 本プロジェクトとの接続: 「システムの内的定義を避け、相互作用と合成性で系を定義する」という方針が、内発性のない多国システム（押し付けられた援助案件）の記述に向く。
- 引っ掛かりポイント: 一般 compositionality 定理がコアにあり、ASEAN 論文の「合成可能性」セクションで引用できる。

### [Fong & Spivak 2018] Seven Sketches in Compositionality: An Invitation to Applied Category Theory
- venue: arXiv:1803.05316 / MIT Press
- link: https://arxiv.org/abs/1803.05316
- 要旨: 応用圏論の標準教科書。順序集合・データベース・signal flow・hypergraph・operad・topos を7章で。
- 本プロジェクトとの接続: 「応用圏論で何ができるか」の地図。先生・査読者がここからの距離で実応用論文を評価する基準点。
- 引っ掛かりポイント: 章6（hypergraph categories）に decorated cospan の説明あり。インフラネットワーク表現の代替候補。

### [Ghani, Hedges, Winschel, Zahn 2018] Compositional Game Theory
- venue: LICS 2018 / arXiv:1603.04641
- link: https://arxiv.org/abs/1603.04641
- 要旨: ゲーム理論を symmetric monoidal category で書く「open game」フレーム。隣接ゲームの合成・並列が categorical 合成と monoidal product。
- 本プロジェクトとの接続: ASEAN の国家間ゲーム（援助・誘致・規制競争）を open game の合成として書ける可能性。Bayesian open games（後続論文）で確率版もある。
- 引っ掛かりポイント: 経済学への圏論応用で最も発展中の領域。社会システムへの本格応用先例として強い。

### [Ehresmann & Vanbremeersch] Memory Evolutive Systems（古典）
- venue: Series in Advances in Mathematics for Applied Sciences (World Scientific, 2007 ほか)
- link: 検索: "Ehresmann Vanbremeersch Memory Evolutive Systems"
- 要旨: 多階層複雑系（生物・社会・認知）を colimit と higher category で記述。1990年代から続く長期プロジェクト。
- 本プロジェクトとの接続: **社会システムを higher category で書いた数少ない長期研究**。「先行例はある」と示すうえで重要。
- 引っ掛かりポイント: 数学的厳密性は時代相応で、現代 ACT 系の Spivak / Myers / Hedges 派と接続が薄い。逆に「再定式化」のニーズがある。

---

## E. 穴の仮説（重要）

このサーベイで浮かび上がった**研究空白**を3〜5個書く。ASEAN 論文の novelty 主張の根拠になる。

### 仮説1: ASEAN・東南アジアインフラを圏論で書いた論文は **存在しない**
- 検索結果: "applied category theory infrastructure ASEAN" 系のクエリでヒットゼロ。出てくるのは政策論文（ADB, JICA, Wiley の app5 等）で、すべて自然言語の比較分析。
- 含意: ユーザーの「ASEAN×fibration」論文は、応用圏論の地理的空白を埋める意義がある。**Spivak が wiring diagram でやったこと、Hedges が経済ゲームでやったこと、を ASEAN インフラでやる、という位置づけ**。

### 仮説2: 「社会システムを fibration で書いた論文」自体が極端に少ない
- ヒットしたのは: ① Grothendieck Institutions（Diaconescu）= 論理体系統合、② Goguen 流 institution = 仕様統合、③ Spivak の double category（変数共有）。
- いずれも **「人間社会の制度」を fibration で扱った例ではない**。生物（GRN, Memory Evolutive Systems）・物理（Spivak の dynamical systems）・論理（institution）は揃うが、社会制度の比較に fibration を直接当てた前例は確認できなかった。
- 含意: ASEAN 論文の唯一性が高い。先生に説明する際の「なぜ未踏か」の根拠。

### 仮説3: 「リープフロッグ = 2-cell」を明示的に書いた論文は確認できない
- 「リープフロッグ」は経済発展論の概念（Perez, Soete 系）で、これと圏論の 2-morphism を結びつけた論文は今回のサーベイで見つからなかった。
- 唯一近いのは Floridi-Jia-Tohmé 2025 で「人間ルートと LLM ルート」の 2 つの関手を並べるアプローチ。これを **2-natural transformation** として再定式化すれば、リープフロッグの厳密版になる可能性。
- 含意: 「Floridi-Jia-Tohmé 同型構造を社会発展に転用」というのが ASEAN 論文の理論的セールスポイントになる。

### 仮説4: Topos Institute / Spivak グループは「政策・国家システム」にまだ手をつけていない
- Polynomial Functor の応用例は: ① NASA Advanced Air Mobility（Niu）、② 動的システム、③ データベース、④ 型理論、⑤ 意思決定理論。
- **公共政策・開発経済への応用は空白**。ASEAN 論文を Compositionality 誌や ACT カンファレンスに投げる際、Topos 系の方法論を社会領域に持ち込む最初期の事例になり得る。

### 仮説5: 圏論×開発経済の中間言語が存在しない
- 開発経済側（ADB, World Bank, JICA）の論文に圏論的視座はゼロ。
- 圏論側（Spivak, Myers, Hedges, Jia）の論文に開発経済の引用はゼロ。
- 含意: **両側の語彙を翻訳する「橋」論文**が市場として完全に空いている。ユーザーの ASEAN 論文を「橋」として書き、長期的には方法論派生（リープフロッグ index, asymmetry index 等）に展開する余地が大きい。

---

## F. 次アクションの提案

1. **Floridi-Jia-Tohmé 2025（arXiv:2512.09117）を最優先で精読**: ASEAN 論文の構造テンプレートになる。
2. **Diaconescu の Grothendieck Institutions を読む**: 「異種を fibration で束ねる」古典的正当化を確保。
3. **Niu & Spivak の Poly 本 + Myers の Categorical Systems Theory ドラフト**を ASEAN 論文の technical background として位置づけ、Topos 系コミュニティとの距離を縮める。
4. **著者に直接コンタクト可能**: scholar プロフィールがないため、共著者経由（Floridi の Yale Digital Ethics Center 経由が一番堅い）でメール可能。同型構造に気付いた旨を伝える価値あり。
