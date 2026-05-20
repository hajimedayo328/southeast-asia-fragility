# 軸④: ASEAN/東南アジア × インフラ・ネットワーク分析 — 文献サーベイ

最終更新: 2026-05-14
担当軸: 東南アジア地域 × インフラ × グラフ理論／ネットワーク分析

---

## 1. ASEAN Power Grid（APG）／越境電力ネットワーク

### [Lyu et al. 2026] GraphGrid: A graph-theoretic framework for energy pricing and supply network analysis using power grid data
- venue: Sustainable Energy, Grids and Networks (Elsevier)
- link: https://www.sciencedirect.com/science/article/abs/pii/S2352467726000718
- 要旨: 実電力データ×グラフ理論×グラフDBを統合したスケーラブル解析フレームワーク。Dijkstra・媒介中心性・コミュニティ検出を「価格形成」と「供給網健全性」両方に適用する設計。
- 本プロジェクトとの接続: APGのような多国間電力統合に、価格と物理供給を同時に扱うグラフ層を載せる前例。圏論ベースの「物理 → 取引」関手のヒントになる。
- 引っ掛かりポイント: ASEAN事例ではないが、APGに移植する余地は大きい。「越境取引のpricing」と「物理潮流」を別カテゴリとして扱える設計に注目。

### [Tongsopit et al. / IEA 2025] Driving global and regional collaboration to realise the ASEAN Power Grid vision
- venue: IEA Commentary (2025)
- link: https://www.iea.org/commentaries/driving-global-and-regional-collaboration-to-realise-the-asean-power-grid-vision
- 要旨: APGは1999年構想開始、現在の課題は政治・規制・制度であり技術ではない、と指摘。LTMS-PIP（Lao→Thai→Mal→Sing）など多国間取引が進む。
- 本プロジェクトとの接続: 「ノード＝国、エッジ＝双方向／多者協定」という二部グラフ的構造の典型。多者ネットワーク（trilateral, ministerial WG）の存在は、ハイパーグラフ的記述を要求する。
- 引っ掛かりポイント: 制度ネットワークと物理ネットワークの「ズレ」が観測可能。グラフ理論的に未だ正面分析されていない領域。

### [TransitionZero 2024] Modelling ASEAN Cross-Border Transmission with TZ-APG
- venue: TransitionZero technical report
- link: https://www.transitionzero.org/insights/modelling-asean-cross-border-transmission-with-tz-apg
- 要旨: ASEAN10カ国の越境送電線をオープンモデルで再現。脱炭素シナリオ下での投資必要量・潮流をシミュレート。
- 本プロジェクトとの接続: APGのグラフ表現を実装データで持っている数少ない公開モデル。これに圏論的層構造（電源 / 線路 / 政策 / 価格）を被せられるか検討余地。
- 引っ掛かりポイント: モデル自体はOR系の最適化で、グラフ理論的不変量（連結度・脆弱性）は副次的にしか扱われていない → 穴。

### [Ember Energy 2025] Wired for profit: Grid is the key to unlock ASEAN energy investment
- venue: Ember Energy Report (May 2025)
- link: https://ember-energy.org/app/uploads/2025/05/Report-Wired-for-profit-ASEAN-PDF.pdf
- 要旨: APG実現に必要な送電投資・国家間連系を試算。再エネ統合がボトルネック。
- 本プロジェクトとの接続: APGネットワークの「現状トポロジー」と「2030想定トポロジー」の差分を取れる素材。エッジ追加に対する地政学リスク評価の入力になる。
- 引っ掛かりポイント: トポロジー変化を時系列で扱う発想（dynamic graph / persistent topology）が未適用。

---

## 2. メコン河流域：水・電力・食料の三層ネットワーク

### [Zhang et al. 2024] Dams in the Mekong: a comprehensive database, spatiotemporal distribution, and hydropower potentials
- venue: Earth System Science Data (Copernicus), 16, 1209
- link: https://essd.copernicus.org/articles/16/1209/2024/
- 要旨: メコン1055ダムの公開DB。10年単位の時空間分布、グリッドベースのhydropower potential評価。
- 本プロジェクトとの接続: 「メコン川ダム配置最適化（Science掲載）」のさらに上流の基盤データ。ラオス中心のpost-2020s拡張をネットワーク変化として追える。
- 引っ掛かりポイント: 1055ノードもあるのに、現状は地理データであってグラフ分析が主目的ではない → 圏論的・トポロジー的解析の余白。

### [Middleton et al. 2019] Governance of the water-energy-food nexus: insights from four infrastructure projects in the Lower Mekong Basin
- venue: Sustainability Science, Springer
- link: https://link.springer.com/article/10.1007/s11625-019-00779-5
- 要旨: 下メコン4事例で WEF nexus governance を比較。SNAで「セクター×ステークホルダ」関係のdensity / centralityを評価。
- 本プロジェクトとの接続: 水・電力・食料を「別カテゴリ」と扱い、相互変換を関手で書くアプローチの叩き台。governance層は3つ目のカテゴリとして自然に追加できる。
- 引っ掛かりポイント: SNAは行ったが、「nexus間のtrade-off構造」を圏論的に扱う動きは未確認。

### [Yu et al. 2020] Exploring synergies in the water-food-energy nexus by using an integrated hydro-economic optimization model for the Lancang-Mekong River basin
- venue: Science of The Total Environment
- link: https://www.sciencedirect.com/science/article/abs/pii/S0048969720315096
- 要旨: 蘭蒼江-メコンを統合し、水・食・エネルギーの最適化モデルを構築。中国上流とLMB下流の取引構造を分析。
- 本プロジェクトとの接続: 「上流国 vs 下流国」の非対称性を定量化。圏論的には射の向きが非対称な小さなカテゴリの良い例。
- 引っ掛かりポイント: 最適化モデルだが、ネットワーク構造を変えたときのロバスト性比較が薄い。

### [ADB / WB 2019] Greater Mekong Subregion Power Market Development
- venue: World Bank technical report
- link: https://documents1.worldbank.org/curated/en/541551554971088114/pdf/Greater-Mekong-Subregion-Power-Market-Development-All-Business-Cases-including-the-Integrated-GMS-Case.pdf
- 要旨: GMS6カ国の電力市場統合のbusiness case。Lao→Vietnam, Lao→Cambodia, Lao→Thailand→Singaporeの3ルートを比較。
- 本プロジェクトとの接続: 既存接続のグラフトポロジーがほぼそのまま読める。地政学リスクが乗ったときのエッジ重みを差し替える素材。
- 引っ掛かりポイント: トポロジカルな脆弱性指標（algebraic connectivity, cut set）は計算されていない。

---

## 3. 都市インフラ・防災ネットワーク（ベトナム・インドネシア・フィリピン・タイ）

### [Putri & Esteban et al. 2023] Quantification of Loss of Access to Critical Services during Floods in Greater Jakarta
- venue: Remote Sensing, 15(21), 5250
- link: https://www.mdpi.com/2072-4292/15/21/5250
- 要旨: Jakarta圏で確率的洪水回帰140シナリオを実行し、社会・地理・ネットワーク3観点でcritical servicesへのアクセス損失を定量化。
- 本プロジェクトとの接続: 既知の「洪水時道路ネットワーク崩壊」研究の最新版。サービス層（病院・学校）と道路層を分離して扱う発想は、層付きグラフ（sheafに近い）への接続が自然。
- 引っ掛かりポイント: 「層間結合」の数学的扱いがアドホック。ここに圏論的な抽象化が効く余地大。

### [Sun et al. 2024] Resilience of transportation infrastructure networks to road failures
- venue: Chaos: An Interdisciplinary Journal of Nonlinear Science, 34(1), 013124
- link: https://pubs.aip.org/aip/cha/article/34/1/013124/3037471
- 要旨: 道路網のfailure modeをgraph topologyから評価。betweenness, k-coreで重要セグメントを抽出。
- 本プロジェクトとの接続: 既存研究「洪水時の道路ネットワーク崩壊（媒介中心性、5カ国）」の方法論的後ろ盾。
- 引っ掛かりポイント: ASEAN特化版はまだ少ない。ベトナム・フィリピン台風データへの応用は明確な穴。

### [Sudibyo et al. 2024] Spatial identification of critical logistics infrastructure as national vital objects: a network resilience approach to megathrust contingencies
- venue: Jurnal Pertahanan dan Bela Negara (Indonesia)
- link: https://jurnal.idu.ac.id/index.php/JPBH/article/view/20167
- 要旨: インドネシアの物流網について、media中心性とNetwork robustness simulationを用い、メガスラスト地震時の重要拠点を抽出。
- 本プロジェクトとの接続: インドネシア国軍／防衛系が出している実応用例。1万島嶼の海上＋陸上の異種ネットワーク統合は、複層カテゴリの典型題材。
- 引っ掛かりポイント: 軍・防災視点で「閉じた国家ネットワーク」として扱う。ASEAN横断にしたときの整合性は未検討。

### [Bui et al. 2023 / Climate-Mobility-Dengue] Interactions between climate change, urban infrastructure and mobility are driving dengue emergence in Vietnam
- venue: Nature Communications, 14
- link: https://www.nature.com/articles/s41467-023-43954-0
- 要旨: ベトナムでデング熱の発生を、気候・都市インフラ（衛生・上水）・人流（モビリティネットワーク）の3層相互作用として説明。
- 本プロジェクトとの接続: 既知「デング熱伝播クラスタ（ベトナム・タイ）」を更新する重要文献。「インフラの欠落」と「人の動き」をネットワーク的に結びつけた良い前例。
- 引っ掛かりポイント: 3層モデルだがネットワーク層間の関手的扱いはない → 圏論で書き直す価値がある。

### [Zhang et al. 2025 / mSWE-GNN ほか] Multi-scale hydraulic graph neural networks for flood modelling
- venue: Natural Hazards and Earth System Sciences, 25, 335
- link: https://nhess.copernicus.org/articles/25/335/2025/
- 要旨: 都市河川ネットワークをGNNで学習し、未知地形・時変境界条件にも汎化、数値モデル比700倍高速化。
- 本プロジェクトとの接続: 既知「都市洪水×GNN（2024）」の進化版。ASEANの都市（ホーチミン・マニラ・ジャカルタ）に転用するアーキテクチャ候補。
- 引っ掛かりポイント: ASEAN都市データでの学習例は未確認 → ベトナム派遣中の応用テーマになり得る。

---

## 4. モバイル金融・デジタル普及ネットワーク（GoPay / GCash / MoMo / Bakong）

### [McKinsey 2024] Mobile wallets: Southeast Asia's new digital life hack
- venue: McKinsey & Company (industry report)
- link: https://www.mckinsey.com/industries/financial-services/our-insights/mobile-wallets-southeast-asias-new-digital-life-hack
- 要旨: GoPay（インドネシア）、GCash（フィリピン）、MoMo（ベトナム）の支配的シェア構造を整理。フィリピン89%・ベトナム63%・タイ66%と各国寡占。
- 本プロジェクトとの接続: 「決済ネットワーク」を国×サービスの二部グラフで描いたときのトポロジーがほぼ確定している良データ。Bakong（カンボジア）は中央銀行主導のbackbone型で構造が異質。
- 引っ掛かりポイント: 学術論文ではなく業界レポート。ここをアカデミックに精密化する余地。

### [PIDS 2023] Financial Inclusion, Financial Technology, and the COVID-19 (Philippines)
- venue: Philippine Institute for Development Studies, DP 2023-45
- link: https://pidswebs.pids.gov.ph/CDN/document/pidsdps2345.pdf
- 要旨: COVID下でフィリピンの金融包摂が一気にデジタル化。GCash等のagent network拡大が農村部の口座普及を加速。
- 本プロジェクトとの接続: agent networkは「ハブ＝都市部、葉＝農村」の非対称グラフ。普及をネットワーク上の伝播現象として扱える。
- 引っ掛かりポイント: グラフ／ネットワーク分析として書かれてはいない。空間データから再構築する余地。

### [Kapronasia / Fintech Singapore 2024] APAC's mobile wallet landscape: local giants, government-backed systems, and super-apps
- venue: Industry analysis
- link: https://fintechnews.sg/111609/payments/apacs-mobile-wallet-landscape-local-giants-government-backed-systems-and-super-apps/
- 要旨: ASEANの決済を「民間super-app型（GrabPay, GoPay, MoMo, GCash）」「政府backbone型（Bakong, QRIS）」に類型化。
- 本プロジェクトとの接続: 圏論の「異なる構成原理を持つ二つのカテゴリ間の関手」として書ける枠組み。クロスボーダー接続（QR連携）が射の合成。
- 引っ掛かりポイント: 各国の規制（central bank policy）が層構造として効く。これも未整理。

---

## 5. ASEAN supply chain / production network のトポロジー

### [ERIA 2021] Robustness and Resilience of Supply Chains During the COVID-19 Pandemic: Findings from a Questionnaire Survey on the Supply Chain Links of Firms in ASEAN and India
- venue: ERIA Discussion Paper 2021-40
- link: https://ideas.repec.org/p/era/wpaper/dp-2021-40.html
- 要旨: ASEAN＋India約1400社調査。リンクの強さを「同質性（owner国＝供給先国）」と「地理的多様性」で説明。
- 本プロジェクトとの接続: 既知「農業サプライチェーン耐性（COVID-19）」を超え、製造業まで含めたエッジ強度のmicro-data。robust ↔ resilientの区別が圏論的に面白い（リンク維持 vs 代替射の存在）。
- 引っ掛かりポイント: ネットワーク図示までは行われていない。tensor的に統合する余地。

### [Choirun et al. 2024] Distribution of the ASEAN battery electric vehicle production network: Mapping the interplay of endowments, policies, and global integration
- venue: Asia Pacific Management Review (Elsevier)
- link: https://www.sciencedirect.com/science/article/abs/pii/S0973082624002758
- 要旨: ASEANのBEV生産ネットワークを国×部材×政策で立体マッピング。タイ・インドネシア・ベトナムの分業構造を明らかにする。
- 本プロジェクトとの接続: 「電気自動車 = 電力グリッド × 自動車サプライ × 鉱物資源（Ni, Co）」のクロスセクターネットワーク。複層グラフの良いケーススタディ。
- 引っ掛かりポイント: 多層性は明示するが、層間の数学的な合成則は未定式化。

### [Trinidad et al. 2025] Strengthening ASEAN's Electrical and Electronics Sector: Enhancing Regional Production Networks and Economic Resilience
- venue: Asian Journal of Economics and Banking (Elsevier系)
- link: https://www.sciencedirect.com/science/article/pii/S1925209925000518
- 要旨: ASEAN E&E産業を input-output で分析し、ペリフェラル／中間／先進の3クラスタに分類。Malaysia・Singaporeが調整ハブ。
- 本プロジェクトとの接続: 「ハブの非対称性」をinput-outputとネットワーク中心性の両方から見られる。
- 引っ掛かりポイント: 産業セクター間の依存とインフラ（電力・港湾）依存が別々に議論され、統合されていない。

### [Yu et al. 2024] The effects of the COVID-19 pandemic on connectivity, operational efficiency, and resilience of major container ports in Southeast Asia
- venue: Journal of Transport Geography
- link: https://www.sciencedirect.com/science/article/abs/pii/S0966692324000449
- 要旨: 東南アジア主要港の接続性・効率・レジリエンスをCOVID前後で比較。Singapore・Port Klangが構造的優位。
- 本プロジェクトとの接続: 港湾ネットワークは「海運（外向き）と陸運（内向き）」の界面。圏論的には2つのカテゴリの貼り合わせ。
- 引っ掛かりポイント: 内陸ネットワーク（タイ-ラオス国境、ジャカルタ後背地）との結合分析がない。

### [Lordan & Lordan 2024] Pattern-detection in the global automotive industry: A manufacturer-supplier-product network analysis
- venue: Chaos, Solitons & Fractals
- link: https://www.sciencedirect.com/science/article/pii/S0960077924001814
- 要旨: 自動車産業の世界三部グラフ（メーカー×サプライヤー×製品）を分析。地域クラスタを抽出。
- 本プロジェクトとの接続: タイ（Detroit of Asia）・ベトナム・インドネシアの相対位置を世界網内で測れる。
- 引っ掛かりポイント: 世界全体の話で、ASEAN内の内部構造はぼやけている。

---

## 6. 横断的（複層・category-theoretic）

### [Tsuiki & Honkawa 2013] Theory of Interface: Category Theory, Directed Networks and Evolution of Biological Networks
- venue: arXiv:1210.6166 / BioSystems
- link: https://arxiv.org/abs/1210.6166
- 要旨: 有向ネットワークの進化を圏論の「随伴」で記述。静的経路と動的（横断的）経路を双対関係として扱う。
- 本プロジェクトとの接続: インフラを「物理層」「制度層」とし、その間を関手・随伴で結ぶ叩き台。
- 引っ掛かりポイント: 生物応用だが、抽象構造はインフラに直接転用可能。ASEAN応用は未開拓。

### [Wang et al. 2020] The evolving structure of the Southeast Asian air transport network through the lens of complex networks, 1979–2012
- venue: Transportation Research Part A
- link: https://pmc.ncbi.nlm.nih.gov/articles/PMC7127681/
- 要旨: 東南アジアの航空網を30年単位で複雑ネットワーク解析。scale-free性とsmall-world性の進化を追跡。
- 本プロジェクトとの接続: 「動的ネットワーク（時系列）」のASEAN事例として希少。ハブ都市変遷（Bangkok→Singapore→KL→Jakarta）の定量化。
- 引っ掛かりポイント: 航空単独。これに鉄道・港湾を加えて多層化するのが次。

---

## 穴の仮説（gap hypotheses）

研究計画立案に直結する「まだ誰もやっていない／薄い」領域。

### 仮説1: 「ASEAN10カ国 × 複数機能インフラ（電力・水・交通・通信・金融）」を一つの数学的対象として統合した研究は事実上存在しない
- 個別には豊富（電力＝APG、水＝メコン、交通＝航空・港湾、金融＝モバイルウォレット）
- 統合する場合、関手 F: C_country → C_infra や、層付きグラフ（sheaf）として書く枠組みはまだ提示されていない
- 圏論を「ASEAN特有の制度的非対称性（中国・日本・韓国の影響、ASEAN+3）」と組み合わせると独自性が出る

### 仮説2: メコン下流のWEF nexusとAPGの電力越境取引を「同じグラフ」で扱った研究はない
- メコン研究はWEF nexus governance（SNA）に閉じ、APG研究は電力市場・送電投資に閉じている
- 両者は実際にはLao PDRが結節点（ダム発電→Thai/Vietnam輸出）
- 「ダム-送電-取引-下流影響」を一つのcompositional graphで書ければ新規

### 仮説3: ASEANのモバイル金融普及を「ネットワーク現象」として圏論／グラフ理論的に扱った学術研究は皆無
- 業界レポート（McKinsey, Kapronasia）止まり
- agent network（GCash 2.5M merchants, MoMo 5000 agents）の空間データはあるが、ネットワーク統計が未公表
- Bakong（カンボジア中央銀行）vs 民間super-app の異なるトポロジーを比較する論文は未確認 → 短中編論文1本ぶんの穴

### 仮説4: 災害ネットワーク研究は「単一国・単一機能」が主流。ASEAN横断（megathrust、メコン洪水、台風）で「複数国×複数機能」を同時に崩壊させたときの圏論的解析は未着手
- Sudibyo (Indonesia) は国内閉じ
- Mekong flood研究も流域内閉じ
- 「2026年型 multi-country compound disaster」のformal modelに穴

### 仮説5: ASEAN production network（BEV、E&E、自動車）と物理インフラ（電力・港湾・道路）の依存を、「セクター依存層 → 物理依存層」の関手として明示した文献はない
- 経済学側：input-output / GVC
- 工学側：infrastructure interdependency
- この2系統の橋渡しに、応用圏論（Fong & Spivakの compositional system 系）が刺さる可能性

---

## 次アクション候補
1. 仮説3（モバイル金融×ネットワーク）が一番低コストで論文1本書ける匂い。空間データ（agent location）の入手可否を要調査。
2. 仮説2（メコン × APG）は卒論〜修論級。Lao PDRをノードとする統合グラフのプロトタイプを年内に作る価値。
3. ベトナム派遣（2027夏）に向け、ホーチミン・ハノイの洪水×電力×通信の3層データを今から探し始める（仮説1の実証ケース）。
