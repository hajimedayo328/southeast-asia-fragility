# 軸② リープフロッグ × ネットワーク科学・経済地理 — 文献サーベイ

作成日: 2026-05-14
担当軸: 途上国インフラのリープフロッグ現象を、ネットワーク科学・経済地理・拡散理論の側面から押さえる。
ゴール: 「同じ機能への平行射」として圏論で定式化する仮説の実証側の足場づくり。

---

## 1. リープフロッグ概念の整理（中核理論）

### [Mutiso 2025] Five rules for technology leapfrogging in Africa
- venue: Science, vol.389, eadz9028 (2025)
- link: https://www.science.org/doi/10.1126/science.adz9028
- 要旨: アフリカのリープフロッグ議論は曖昧な概念のまま使われ続けてきたが、政策・投資判断を誤らせる原因になる。本ペーパーは「リープフロッグを評価するための5つのルール」を提示。(1) leapfrog を明確に定義・評価する、(2) どの問題にリープフロッグが当てはまるかを限定する、(3) 予期せぬ使われ方を想定する、（残り2つは本文要確認）。携帯電話は典型成功例だが、それを他セクターに安易に一般化するなと警告。
- 本プロジェクトとの接続: **軸②の中心論文**。リープフロッグの「定義の曖昧さ」を圏論的に整理し直す研究意義の根拠になる。Mutisoが5ルールを「事例の経験則」レベルで止めているのに対し、こちらは射の合成・自然変換で形式化することで一段抽象化できる。
- 引っ掛かりポイント: 5ルールの中身が「対象（object）」「射（morphism）」「合成則」のどれに対応するかをマッピングできるか。例えば「予期せぬ使われ方」は射の domain/codomain が事後的に変わる現象と読み替えられる。

### [Lee & Lim 2001 系] Economics of Technological Leapfrogging
- venue: Oxford Handbook of Technology and Economic Catch-up in Emerging Economies (book chapter, 2021版あり)
- link: https://academic.oup.com/book/40028/chapter/340396988
- 要旨: 後発国は単に先発国の道を辿るのではなく、ステージをスキップしたり別の道を作る (path-creating)。「windows of opportunity」（新技術パラダイムの登場）が leapfrog のトリガー。先発国は sunk cost で旧技術にロックインされる一方、後発国は身軽。
- 本プロジェクトとの接続: stage-skipping と path-creating の区別が、圏論で言う「同一射 vs 別の射への置換」の区別と相似。本プロジェクトの「平行射」仮説は stage-skipping 側の定式化に当たる。
- 引っ掛かりポイント: path-creating は射の codomain（到達対象）自体が違う = 関手の像が違う、と読み替えられそう。

### [Binz et al. 2022] Towards transformative leapfrogging
- venue: Environmental Innovation and Societal Transitions, ScienceDirect
- link: https://www.sciencedirect.com/science/article/pii/S2210422422000740
- 要旨: 従来の leapfrog 論は「知識の獲得」に偏ってきたが、技術正統性・市場形成・金融フローといった「valuation 戦略」も重要。後発国向け4類型を提示し、社会技術トランジション論・経済地理論を統合。
- 本プロジェクトとの接続: ネットワーク科学的な「ノードのリンクの組み替え」よりも、「ノード自体の意味付け（valuation）が変わる」というレイヤーを示している。圏論で言えば「対象に付随する構造（例: 富化圏のhom対象）」が変わる現象。
- 引っ掛かりポイント: 卒論で「圏論×ネットワーク科学」を統合するとき、Binzの4類型を圏論の関手で対応付けると新規性が出る可能性。

---

## 2. モバイルマネー・M-Pesa の伝播ネットワーク研究

### [Suri & Jack 2016] The long-run poverty and gender impacts of mobile money
- venue: Science, vol.354, pp.1288-1292
- link: https://www.science.org/doi/10.1126/science.aah5309 / PDFミラー: https://www.jefftk.com/suri2016.pdf
- 要旨: ケニアM-Pesaへのアクセス増が一人当たり消費を引き上げ、194,000世帯（全世帯の2%）を貧困から押し上げた。効果は女性世帯主世帯でより顕著。鍵となる変数は「世帯近辺のエージェント密度」で、地理的近接性が金融行動・労働市場の変化を生んだ。
- 本プロジェクトとの接続: **軸②で必ず引く基準論文**。エージェント網は二部グラフ（ユーザー×エージェント）として記述でき、その密度が因果効果を媒介する。「リープフロッグ＝物理的銀行支店ノードのスキップ＋エージェントノードの局所密度生成」という構造を可視化できる。
- 引っ掛かりポイント: エージェント密度＝局所的なdegree centralityの近似値であり、Banerjee系（後述）の eigenvector centrality 議論と接続可能。本サーベイ全体でcentrality概念がリンクのキー。

### [Sowon et al. 2023] The Role of User-Agent Interactions on Mobile Money Practices in Kenya and Tanzania
- venue: arXiv:2309.00226
- link: https://arxiv.org/abs/2309.00226
- 要旨: ケニア・タンザニア計72件のインタビューから、ユーザーとエージェントが「制度の穴」を埋めるための workaround を共同設計している実態を抽出。エージェント融資、身分証代替の関係構築、利便性向上のための取引改変など。
- 本プロジェクトとの接続: 公式システム（射 f）と非公式 workaround（射 g）が同じ機能（codomain）を実現している = まさに「平行射」事例。圏論的にはequalizer/coequalizerで形式化できる構造。
- 引っ掛かりポイント: 「非公式回避策が公式システムに吸収される」現象 = pushout/colimit と類比できそう。卒論の具体例に最適。

### [Mbiti & Weil 2011/2012] Mobile Banking: The Impact of M-Pesa in Kenya / Documenting the birth of a financial economy
- venue: NBER WP 17129 / PNAS (2012)
- link: https://www.pnas.org/doi/10.1073/pnas.1115843109
- 要旨: M-Pesa導入前後のケニア家計の取引データから、現金経済から電子経済への移行を「金融経済の誕生」として記述。ネットワーク効果と臨界質量の議論あり。
- 本プロジェクトとの接続: 「誕生」を圏論的にはinitial object（始対象）からの射の発生として記述可能。リープフロッグの起点問題（なぜ2007年だったのか）への示唆。
- 引っ掛かりポイント: PNAS 2012版が無料公開。

### [Tanzania interoperability研究 2023] Interoperability Between Mobile Money Agents and Choice of Network Operators
- venue: Review of Network Economics (de Gruyter), 2023
- link: https://www.degruyterbrill.com/document/doi/10.1515/rne-2023-0024/html
- 要旨: タンザニアは2014年にアフリカ初のモバイルマネー相互運用を導入。ノンエクスクルーシブなエージェント契約がオペレーター選好にどう影響するかを定量分析。
- 本プロジェクトとの接続: 「単一のエージェントノードが複数のオペレーター射を担う」現象 = 関手の合成・モナド的構造。プラットフォーム間相互運用は圏論で fibration/cofibration として扱える。
- 引っ掛かりポイント: 国際比較で interoperability の有無が leapfrog 経路を変える事例。

### [GSMA 2025] State of the Industry Report on Mobile Money 2025
- venue: GSMA Mobile for Development (industry report, 2025)
- link: https://www.gsma.com/sotir/
- 要旨: 2024年時点でモバイルマネー登録口座は20億超、月次アクティブユーザー5億超。取引額1.68兆ドル/年。最初の10億口座到達に18年かかったが、その後5年で倍増。サブサハラアフリカが最活発、東南アジアが第2成長地域。GSMA自身が「leapfrog to DFS」という表現を使用。
- 本プロジェクトとの接続: マクロ統計の裏付け。サブサハラ vs ASEAN vs 南アジアの増加率比較は、リープフロッグ「経路」の地域差を示す。卒論の図表素材として直接使える。
- 引っ掛かりポイント: industry report は査読論文ではないが、生データが豊富で図表に使える。

---

## 3. 拡散理論 × ネットワーク科学

### [Banerjee, Chandrasekhar, Duflo, Jackson 2013] The Diffusion of Microfinance
- venue: Science, vol.341, no.6144 (2013)
- link: https://web.stanford.edu/~jacksonm/Banerjee-Chandrasekhar-Duflo-Jackson-DiffusionOfMicrofinance-Science-2013.pdf
- 要旨: 南インド43村でマイクロファイナンス導入前にネットワークデータを収集し、その後の参加状況を追跡。最初に情報を伝える「leader」のeigenvector centralityが拡散の成否を決める。新提案の「diffusion centrality」指標が予測力で従来指標を上回る。
- 本プロジェクトとの接続: **本軸のもう一つの基準論文**。Aadhaar/M-Pesa等のリープフロッグ事例にも diffusion centrality を計算できれば、Mutiso 5ルールの「unexpected uptake」を定量化できる。
- 引っ掛かりポイント: コード・データが Jackson のサイトで公開。卒論の実装段階で再利用可能。

### [Langrené, Liu, Wu, Zhi 2026] The dynamics of innovation diffusion: A survey of Bass-type models
- venue: arXiv:2602.19488 (2026)
- link: https://arxiv.org/abs/2602.19488
- 要旨: Rogers (1962)–Bass (1969) 系の拡散モデル群を体系的にレビュー。counting/diffusion/uncertain processes、ベイジアン推定、エージェントベース代替モデルまで網羅。
- 本プロジェクトとの接続: 拡散ダイナミクスの「現状の標準ツール一覧」。圏論的構造をBass系モデルの上に乗せる試みの基盤になる。
- 引っ掛かりポイント: 2026年の最新サーベイ。本プロジェクトの「related work」セクションでこれ1本を引けば数式系の出自を一通りカバーできる。

### [Bertotti et al. 2016] The Bass diffusion model on networks with correlations and inhomogeneous advertising
- venue: Chaos, Solitons & Fractals
- link: https://www.sciencedirect.com/science/article/abs/pii/S0960077916300686
- 要旨: スケールフリーネットワーク上でのBassモデル拡張。任意のpower-law指数、assortative correlationを扱う。ハブの少数のadoption曲線が全体adoptionを先取りすることを示す。
- 本プロジェクトとの接続: モバイルマネーのエージェント網が scale-free 性を持つと仮定すれば、ハブエージェントの動向から国全体のadoption予測ができる。リープフロッグ「速度差」をネットワーク構造で説明する道具。
- 引っ掛かりポイント: 数式が重め。実装するならネットワーク生成と数値積分が必要。

### [Bonabeau系 / Tandfonline 2024] The Bass diffusion model: agent-based implementation on arbitrary networks
- venue: Mathematical and Computer Modelling of Dynamical Systems (T&F)
- link: https://www.tandfonline.com/doi/full/10.1080/13873954.2024.2350244
- 要旨: 任意ネットワーク上でのBassモデルのエージェントベース実装の最新研究。
- 本プロジェクトとの接続: 卒論で「圏論的記述 → エージェントベース実装で検証」というパイプラインを組むときの実装側の参考。
- 引っ掛かりポイント: コード公開状況は要確認。

### [Conley & Udry 2010 系・Bandiera & Rasul 2006 系] Social networks and technology adoption in developing countries
- venue: AERピアエフェクト系（複数）
- link: https://www.sciencedirect.com/science/article/abs/pii/S0167268122003298 など
- 要旨: モザンビーク・ガーナ・ウガンダ等で農業・モバイルマネー等の採用が社会ネットワーク経由で広がることをRCTで実証。ピアの数だけでなく「誰がピアか」が効く。
- 本プロジェクトとの接続: 拡散の経路依存性 = 圏論で言う「射の composition の順序が結果を変える」現象の実証例。Aadhaar の州レベル普及差なども同枠で扱える。
- 引っ掛かりポイント: 個別RCTを束ねるメタ的な視点で本プロジェクトに引用すると説得力が増す。

---

## 4. デジタルID / プラットフォーム

### [Madon & Schoemaker 2021等] Realizing digital identity in government: Prioritizing design objectives for Aadhaar in India
- venue: Government Information Quarterly (ScienceDirect)
- link: https://www.sciencedirect.com/science/article/abs/pii/S0740624X19303557
- 要旨: Aadhaarの設計・実装を Design Theory と Critical Success Factor 理論で評価。専門家FGDで優先目標を抽出。uniqueness/security/privacyがトップ。
- 本プロジェクトとの接続: AadhaarをM-Pesaと並べる際の「設計目標の優先順位の違い」を圏論的に対比できる。Aadhaar=identity射（始対象→ID対象）、M-Pesa=value-transfer射（口座対象間の射）と分けて記述可能。
- 引っ掛かりポイント: Aadhaarの「societal digital platform」概念は、本プロジェクトの「インフラを圏として記述」の発想と非常に近い。

---

## 穴の仮説（このサーベイで埋まっていない箇所）

1. **「リープフロッグの圏論的形式化」を試みた論文が見当たらない**
   Mutiso 2025 はルールを列挙するに留まり、Binz et al. 2022 も類型化までしか進んでいない。「stage-skipping = 射の合成のスキップ」「path-creating = 関手による圏の置換」といった形式化は本プロジェクトの新規性として狙える穴。

2. **モバイルマネー研究と拡散ネットワーク研究の融合不足**
   Suri-Jack系（地理・密度ベース）と Banerjee-Jackson系（centrality・diffusion centrality）が別々に走っており、M-Pesaのエージェント網に diffusion centrality を実際に計算した論文が見当たらない。卒論の実証パートで埋められる可能性。

3. **ASEAN（GCash/MoMo）に diffusion centrality / network 分析を当てた研究の希薄さ**
   GCash・MoMoのアカデミック研究はTAMモデル（perceived usefulness等）のアンケート分析が大半で、ネットワーク科学的アプローチが極めて少ない。M-Pesaの方法論をASEANに移植するだけで一定の新規性。

4. **「複数の leapfrog 事例を比較する形式的フレームワーク」の欠如**
   M-Pesa・Aadhaar・GCash・MoMo・UPI を「同じ機能への異なる射」として並べて比較する論文がない。比較を可能にする圏（カテゴリ）の取り方そのものが研究貢献になり得る。

5. **「失敗した leapfrog」のネットワーク科学的説明の不在**
   成功事例の研究は多いが、なぜインドネシアのモバイルマネーがケニアほど離陸しなかったか、ナイジェリアでなぜ遅れたかをネットワーク構造（agent network density / centrality分布）で説明する研究は乏しい。「リープフロッグの不成立条件」を圏論的に「射が存在しない」「合成が定義されない」状況として記述する切り口は新しい。

---

## 次の調査タスク候補

- Suri & Jack 2016 の PDF（jefftk ミラー）と Banerjee et al. 2013 の PDF を実際に読み、network指標の定義を整理する
- Mutiso 2025 の Science 本文を IIBC or 大学アクセスで読み、5ルールの完全リスト化
- ASEAN系（GCash/MoMo）の登録ベース成長率の生データを GSMA 2025 から抽出
- Aadhaar の州別 enrolment rate と社会ネットワーク密度の相関データの探索
