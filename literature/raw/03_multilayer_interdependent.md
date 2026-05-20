# 軸③ 多層・相互依存ネットワーク サーベイ

途上国インフラの依存構造をグラフ理論・圏論で分析する研究のための文献メモ。Buldyrev 2010 起点、2024〜2026 を中心に。

---

## 起点・古典（背景把握用）

### [Buldyrev et al. 2010] Catastrophic cascade of failures in interdependent networks
- venue: Nature 464, 1025–1028
- link: https://www.nature.com/articles/nature08932 / https://arxiv.org/abs/0907.1182
- 要旨: 2つの相互依存ネットワーク（電力・通信を想定）で片方のノード故障が他方の依存ノード故障を誘発し、無限カスケードに至るモデル。単一網と異なり、相互依存系は **広い次数分布ほど壊れやすい** ことを示した。パーコレーション転移が **第一次（不連続）** になる。
- 本プロジェクトとの接続: 軸③の出発点。途上国の電力⇄通信⇄水のように **薄い結合だが鋭く崩れる** 系統の数理的根拠を提供。
- 引っ掛かりポイント: モデルは「ノード x が動くには相手側ノード x' が動いている必要」というシンプルな one-to-one 依存。これは圏論の **pullback / fibered product** の関手的記述と整合する可能性がある。各国の依存型を **functor F: D → Net** として定式化できれば、Buldyrev モデルの一般化系として位置付けられる。

### [Boccaletti et al. 2014] The structure and dynamics of multilayer networks
- venue: Physics Reports 544, 1–122
- link: https://arxiv.org/abs/1407.0742
- 要旨: 多層ネットワークの構造・ダイナミクス・応用の包括的レビュー。layer/multiplex/network of networks/interdependent などの **用語整理** と数学的形式化。
- 本プロジェクトとの接続: 用語の正典。論文で "layer" を使うとき必ず参照される。
- 引っ掛かりポイント: 多層構造のテンソル表現は **圏論の indexed family / fibration** に対応する。境氏は明示しないが、layer = 関手の値域となる対象、と読み替えると圏論的書き換えが可能。

### [Gao et al. 2012] Networks formed from interdependent networks
- venue: Nature Physics 8, 40–48
- link: https://www.nature.com/articles/nphys2180
- 要旨: 2層→ n 層への拡張。Network-of-Networks 形式化。ツリー状の依存構造で解析解、ループあり依存はより脆い。
- 本プロジェクトとの接続: ASEAN 域内の **電力・水・通信・物流の 4 層以上** を扱う際の理論的足場。
- 引っ掛かりポイント: 「依存グラフのグラフ」という入れ子は圏論の **2-category** 的構造。途上国では先進国と違って「電力 → 通信」だけでなく「燃料輸送 → 電力 → 通信 → 電力監視」という長い周回が出る。Network-of-Networks の **トポロジー自体** を解析対象にできる余地。

---

## 中核論文（2017〜2022）

### [Liu, Eisenberg, Seager, Lai 2018] The "weak" interdependence of infrastructure systems produces mixed percolation transitions in multilayer networks
- venue: Scientific Reports 8, 2111
- link: https://www.nature.com/articles/s41598-018-20019-7 / https://arxiv.org/abs/1710.00940
- 要旨: 完全依存ではなく **tolerance α** を導入し「相手が落ちても確率 1-α で生き残る」モデルへ。スーパー次数が高い層は不連続、低い層は連続/不連続両方の **mixed percolation** を起こす。
- 本プロジェクトとの接続: 途上国インフラは「完全依存」ではなく **冗長な手段（自家発電・井戸・ラジオ）** が残るため、Buldyrev のハード依存より Liu の弱依存のほうが現実に近い。
- 引っ掛かりポイント: α パラメータは **層ごとに違う**。圏論的には「依存射 f: A → B に重み（あるいは部分関手）を付ける」ことに相当。途上国別に α を推定して比較する実証研究が手薄。

### [Bashan, Berezin, Buldyrev, Havlin 2013] The extreme vulnerability of interdependent spatially embedded networks
- venue: Nature Physics 9, 667–672
- link: https://www.nature.com/articles/nphys2727 / https://arxiv.org/abs/1206.2062
- 要旨: 格子（空間埋め込み）の相互依存系は **臨界依存率が存在せず、どれだけ弱い依存でも abrupt collapse する**。「中間距離の依存リンク」が最も脆弱化する。
- 本プロジェクトとの接続: 途上国インフラは地理に強く拘束された **空間ネットワーク**。Buldyrev の非空間モデルより、この空間版のほうが ASEAN 文脈で重要。
- 引っ掛かりポイント: 「中間距離が最脆弱」は **リープフロッグ戦略** に深い含意。携帯基地局や太陽光ミニグリッドが「中間距離（地方都市〜村）」に依存リンクを作ると、むしろ脆弱化する可能性。圏論的には **メトリック付き圏** で扱う必要が出てくる。

### [Duan, Lv, Si, Wang, Li, Gao, Havlin, Stanley, Boccaletti 2019] Universal behavior of cascading failures in interdependent networks
- venue: PNAS 116(45), 22452–22457
- link: https://www.pnas.org/doi/10.1073/pnas.1904421116
- 要旨: 自己無撞着理論で、伝染病・出生死亡・生化学制御など **広範な動的系** に拡張。ノードに動力学を入れると **常にカスケード加速**。一次/二次転移の条件を統一表現。
- 本プロジェクトとの接続: 軸③を「構造の話」から「**構造×動力学** の話」に拡張する橋渡し論文。需給バランス・遅延が支配的な発展途上国電力系統に向く。
- 引っ掛かりポイント: 動力学を載せた相互依存系は **dynamical system 圏 + interdependence functor** という二段構成で書ける。「動力学 D を載せた多層構造 M の collapse 条件」を圏論的不変量で書ければ、論文ネタになる。

### [Danziger, Barabási 2022] Recovery coupling in multilayer networks
- venue: Nature Communications 13, 1–8
- link: https://www.nature.com/articles/s41467-022-28379-5 / https://barabasi.com/media/Danziger_et_al-2022-Nature_Communications.pdf
- 要旨: 米国電力網の **実データ（数百万件の停電復旧記録）** から、復旧速度が他層の状態に依存することを示し、recovery coupling という新概念を導入。大攪乱後の **非線形・普遍的な復旧曲線**。カスケードと別の数学的指紋を持つ。
- 本プロジェクトとの接続: 軸③で **「壊れる側」だけでなく「治る側」** を扱う Mochi の論文。途上国はそもそも復旧が遅い／復旧資源が他層に依存する度合が強い → recovery coupling が支配的なはず。
- 引っ掛かりポイント: failure coupling は co-monad、recovery coupling は monad 的に書ける可能性（推測）。「壊す・治す」の双対性を圏論的に対称化できれば、軸③の根本構造を新しい言葉で説明できる。

---

## 最新（2024〜2026）

### [Tang, Piao, Wang, Shaw, Li 2025] Predicting Cascade Failures in Interdependent Urban Infrastructure Networks (I³ model)
- venue: arXiv 2503.02890（清華大・慶應大連名、WWW/SIGIR 系投稿）
- link: https://arxiv.org/html/2503.02890v1
- 要旨: 電力・道路・通信・建物の 4 層を異種グラフで結合し、Dual Graph Autoencoder + RGCN デコーダで **相転移を含むカスケードを予測**。既存 GNN ベースラインに対し AUC で +31.94%。
- 本プロジェクトとの接続: 軸③の現在の最先端実装。ただし北米データのみ。**途上国データで同モデルを動かす研究が空白**。
- 引っ掛かりポイント: 異種グラフ = 圏論的に **profunctor / multi-sorted hypergraph**。I³ モデルを「異種関手の合成」として書き直すと、現状ブラックボックスのアーキテクチャに数理的解釈が与えられる。

### [Sun et al. 2024] Recovery of contour nodes in interdependent directed networks
- venue: arXiv 2410.13492
- link: https://arxiv.org/html/2410.13492
- 要旨: 有向相互依存網に **復旧戦略** を入れると、崩壊状態 ↔ 復旧状態の **abrupt transition（ヒステリシスあり）** が出る。境界ノード（contour）優先復旧が最適。
- 本プロジェクトとの接続: Danziger 2022 の理論側拡張。**「どこから治すか」を決める数理**。途上国でリソースが限られる現場に直結。
- 引っ掛かりポイント: 「境界ノード」は圏論的には **adjunction の単位/余単位** が刺さる場所に対応するはず。具体的に書ければ「圏論的復旧戦略」という新ジャンル候補。

### [Artime, Grassia, De Domenico, Gleeson, Makse, Mangioni, Perc, Radicchi 2024] Robustness and resilience of complex networks
- venue: Nature Reviews Physics 6(2), 114–131
- link: https://www.nature.com/articles/s42254-023-00676-y / https://hmakse.ccny.cuny.edu/wp-content/uploads/2024/05/s42254-023-00676-y-compressed.pdf.pdf
- 要旨: パーコレーション、ネットワーク dismantling、カスケード、systemic resilience を横断的にまとめた **最新総説**。多層・時系列・higher-order を統合的に整理。
- 本プロジェクトとの接続: 軸③現時点の **教科書代わり**。準備の参考文献として必読。
- 引っ掛かりポイント: 著者陣（De Domenico, Radicchi）は多層ネットワークの **テンソル表現** 推進派。テンソル = 多変数関手なので、圏論的接続は素直。

### [arXiv 2509.13808, 2025] Higher-order Network phenomena of cascading failures in resilient cities
- venue: arXiv 2509.13808（査読中）
- link: https://arxiv.org/html/2509.13808v1
- 要旨: 単純グラフではなく **simplicial complex** で都市インフラを表現。高次相互作用がカスケードを **40–60% 加速**、面的故障は局所故障の 1.6 倍のノードを巻き込む。
- 本プロジェクトとの接続: 軸③を **higher-order** へ拡張する流れ。途上国の災害（洪水・地震）は本質的に面的なので、こちらが正しい記述。
- 引っ掛かりポイント: simplicial complex は **圏論の nerve construction** で得られる。「依存圏 D の nerve = インフラ単体複体」と書けると、圏論経由で higher-order インフラ解析の理論基盤が組める。

### [Xue, Gao, Gallos, Levy, Gross, Di, Havlin 2024] Nucleation phenomena and extreme vulnerability of spatial k-core systems
- venue: Nature Communications 15, 6373
- link: https://pmc.ncbi.nlm.nih.gov/articles/PMC11239893/
- 要旨: 空間 k-core 系で **核生成的な崩壊**（小さな空洞が臨界サイズを超えると一気に拡大）を実証。長距離リンクは崩壊を加速。
- 本プロジェクトとの接続: 軸③の空間効果の最新版。Bashan 2013 の続編。
- 引っ掛かりポイント: 「核生成（局所→大域）」は **層論（sheaf theory）の non-trivial cohomology** と対応しうる。崩壊予兆 = 大域切断の不存在 = H¹ ≠ 0、というアナロジーが立てられる。

### [Wu, Guo, Wang, Zio 2025] Attack-defense game of interdependent infrastructure systems considering cascading failures
- venue: Proc. Inst. Mech. Eng. Part O / SAGE
- link: https://journals.sagepub.com/doi/10.1177/1748006X251336007
- 要旨: 相互依存系を攻撃者・防御者ゲームで分析。カスケードを含めると **最適防御戦略が層をまたぐ**。
- 本プロジェクトとの接続: 途上国の **意図的攻撃・テロ・反政府勢力**（フィリピン Mindanao の送電塔爆破等）を扱う際の理論枠。
- 引っ掛かりポイント: ゲーム理論的設定は圏論で **dialectica category** として知られる。攻防の双対性を圏論化する余地。

### [arXiv 2407.16796, 2024] Modeling and solving cascading failures across interdependent infrastructure systems
- venue: arXiv 2407.16796
- link: https://arxiv.org/html/2407.16796v1
- 要旨: 電力・水・通信の相互依存カスケードを **混合整数最適化** で表現し、復旧資源配分問題を解く。
- 本プロジェクトとの接続: 軸③を「数理最適化＋OR」側からアプローチした最近作。実装志向。
- 引っ掛かりポイント: 最適化定式化は圏論の **オペラド / 制約論理** と接続可能。論文では明示されないが、依存構造の代数的圧縮表現を考える余地。

### [Liu et al. 2025] Cascading failures in multiple-to-multiple interdependent networks considering interdependent failure threshold
- venue: Physica A / ScienceDirect
- link: https://www.sciencedirect.com/science/article/abs/pii/S0378437125003644
- 要旨: 1対1 依存ではなく **多対多依存** に拡張、閾値依存（k 個壊れたら自分も壊れる）を導入。
- 本プロジェクトとの接続: 途上国は「複数の発電所のどれかが動けばよい」式の多対多冗長を持つ。Buldyrev の単純化を緩めた最新版。
- 引っ掛かりポイント: 多対多 + 閾値 = **fuzzy categorical limit** の一種。圏論的にきれいに書く余地。

---

## 関連（境界領域）

### [Ghrist, Hiraoka] Applications of Sheaf Cohomology and Exact Sequences to Network Coding
- venue: 京大数理解析研究所講究録 1752 / preprint
- link: https://www2.math.upenn.edu/~ghrist/preprints/networkcodingshort.pdf
- 要旨: ネットワーク符号化問題を **層コホモロジー** で扱い、最大フローや拡張性を H⁰/H¹ で特徴付ける。
- 本プロジェクトとの接続: 軸③を圏論側から狙うとき、最も実績がある **Ghrist の sheaf approach**。インフラ依存をスタックの「データ」、整合性を「貼り合わせ」とみなせる。
- 引っ掛かりポイント: 既存研究が **通信網中心**。「電力・水・通信の異種貼り合わせ」を sheaf として書いた研究は未踏。途上国の異種混在インフラと相性が良い。

---

## 穴の仮説（このサーベイから見えた研究空白）

1. **途上国×多層ネットワークの実証空白**
   - 軸③の理論論文は Buldyrev 以来 15 年で大量。だが **データを使った実証はほぼ米中欧の先進国電力網**。ASEAN・サブサハラを多層形式で扱った査読論文は数えるほど（IEEE 2018 のインドネシアグリッド単層解析が代表で、多層化されてない）。
   - → **「途上国 N カ国の電力 × 通信 × 水 を多層ネットワーク化し、Liu 2018 の α パラメータ・Danziger 2022 の recovery coupling を実測」** で空白埋め一本書ける可能性。

2. **リープフロッグ概念の数理化が未着手**
   - 軸③論文群はインフラを「先進国型固定インフラ」と暗黙に仮定。携帯電話＋ソーラーミニグリッド＋モバイルマネーで **物理層を skip した依存構造** は数理モデル化されていない。
   - → 「リープフロッグした層構造は、Bashan 2013 の空間脆弱性を **回避** するか **強化** するか」が立論可能。中間距離が脆弱という結果に照らすと、リープフロッグは脆弱化する可能性が高い、という反直観的仮説が立つ。

3. **圏論的依存記述が空白**
   - 軸③の論文はすべて **テンソル代数 or 行列代数** の言葉。圏論（functor, sheaf, profunctor）で書き直した論文は Ghrist 系を除いて存在しない。
   - → 「Buldyrev モデルを **pullback による依存射** として書き直し、復旧（Danziger）を adjoint pair として双対化する」で純理論論文一本。

4. **failure coupling と recovery coupling の双対性**
   - Danziger 2022 が recovery coupling を提唱したが、failure 側との **対称構造** は議論されていない（独立な現象として扱われている）。
   - → 「両者は同じ圏論的構造の双対であり、システムの **ヒステリシス幅** がそのギャップを定量化する」という仮説。Sun 2024（contour 復旧）と組み合わせると検証可能。

5. **higher-order × spatial × developing の三点交差**
   - 2025 の higher-order 系（simplicial complex）は **空間** 拡張も **途上国** 適用も未着手。三つの方向の交差点がぽっかり空いている。
   - → ASEAN 都市の電力・水・道路を simplicial complex で組み、洪水・地震という面的攪乱でのカスケードを simulate する研究が成立しうる。
