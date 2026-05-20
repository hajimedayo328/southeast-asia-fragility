# 軸① 圏論 × インフラ・社会システム ― 文献サーベイ

作成: 2026-05-14 / リサーチエージェント（Sonnet）
対象: 「機能圏 𝓕 / 国の圏 𝓒 / 実装圏 𝓘」三層 + Grothendieck fibration `p: 𝓘 → 𝓒` 構想の理論的バックボーンを支える論文・著作。

検索範囲: arxiv, Theory and Applications of Categories (TAC), EPTCS (ACT proceedings), Brendan Fong / John Baez / David Spivak / Evan Patterson / Jules Hedges らの公開資料。

---

## A. ACT コミュニティ基盤文献（Spivak, Fong, Coecke 系）

### [Fong & Spivak 2018] Seven Sketches in Compositionality: An Invitation to Applied Category Theory
- venue: arxiv 1803.05316 / Cambridge University Press (2019)
- link: https://arxiv.org/abs/1803.05316
- 要旨: ACT の標準入門書。順序集合・データベース・回路・Petri net・収益関数・論理を圏論的に統一する7つのスケッチ。
- 本プロジェクトとの接続: 𝓒（国の圏）に poset/preorder 構造を入れる足場、𝓘 を hypergraph category として扱う言語を提供。Heyting代数の章は軸②の Heyting層分析にも直結。
- 引っ掛かりポイント: 入門書ゆえ各章のモデルが浅い。「国×インフラ」のような階層化スキーマは扱われていない（fibration は登場するが応用例なし）。

### [Spivak 2013] The Operad of Wiring Diagrams
- venue: arxiv 1305.0297 / 関連: TAC Vol.30, No.51（dynamical systems algebra）
- link: https://arxiv.org/abs/1305.0297 ; http://www.tac.mta.ca/tac/volumes/30/51/30-51.pdf
- 要旨: 入出力を持つ「箱」を配線して合成するための operad を定式化。データベース、回路、recursion を統一的に表現。
- 本プロジェクトとの接続: 𝓘（実装圏）でインフラのモジュール（発電所・送電線・水処理プラント）を箱として並べ、国ごとに wiring を変えて構成するメタファに直結。Catlab.jl で実装可能。
- 引っ掛かりポイント: 静的な配線が中心で、時間発展（拡張・劣化）の扱いが弱い。Spivakらは temporal wiring diagram を別途定義しているが応用論文が少ない。

### [Vagner, Spivak, Lerman 2014] Algebras of Open Dynamical Systems on the Operad of Wiring Diagrams
- venue: TAC Vol.30, No.51
- link: http://www.tac.mta.ca/tac/volumes/30/51/30-51.pdf
- 要旨: 連続時間ダイナミクスを wiring diagram の上のオペラド代数として記述。open system を合成すると open system になる性質を厳密化。
- 本プロジェクトとの接続: 国インフラの動的シミュレーション（電力需給、人口移動）を圏論的に扱うときの直接的な土台。
- 引っ掛かりポイント: 純粋連続系のみ。離散イベント（停電、政策変更）と混在する hybrid system の扱いに弱い。

### [Spivak 2012] Functorial Data Migration
- venue: arxiv 1009.1166 / Information and Computation
- link: https://arxiv.org/abs/1009.1166
- 要旨: スキーマを圏として定義し、スキーマ間の関手によって 3 種類のデータ移行（Σ, Δ, Π）を導く。CQL の理論基盤。
- 本プロジェクトとの接続: 「タイ電力スキーマ」「ベトナム電力スキーマ」を別圏として定義し、関手で比較・統合 = 国比較研究の道具立てそのもの。
- 引っ掛かりポイント: スキーマ間のミスマッチ（電圧規格・データ粒度の違い）への対応は未整備。olog（[Spivak & Kent 2012]）と併読する必要。

### [Patterson, Lynch, Fairbanks 2021] Categorical Data Structures for Technical Computing (Catlab.jl)
- venue: arxiv 2106.04703 / Compositionality 4, 5 (2022)
- link: https://arxiv.org/abs/2106.04703
- 要旨: Julia 実装 Catlab.jl の基盤論文。symmetric monoidal category, wiring diagram, ACSets を計算機上で扱う枠組み。
- 本プロジェクトとの接続: 構想を「動くデモ」にする最短経路。卒論で実装パートを作るならここを足場にする。
- 引っ掛かりポイント: Julia エコシステム依存度が高く、Python 中心の研究室との橋渡し設計が必要。

---

## B. ACT 会議録（最新動向のスキャン用）

### [Master & Lin eds. 2024] Proceedings of the Seventh International Conference on Applied Category Theory 2024
- venue: arxiv 2509.18357 / EPTCS
- link: https://arxiv.org/abs/2509.18357
- 要旨: ACT2024（Oxford）の proceedings。古典力学・確率・言語学・疫学・熱力学・工学への ACT 応用が幅広く収録。
- 本プロジェクトとの接続: 直近の「圏論×応用」のトレンドを掴むカタログ。インフラ近接の論文（疫学・工学）をここから拾える。
- 引っ掛かりポイント: 多くが extended abstract で短く、深掘りは元論文必須。

### [Master eds. 2023] Proceedings of the Sixth International Conference on Applied Category Theory 2023
- venue: arxiv 2312.08138 / EPTCS
- link: https://arxiv.org/abs/2312.08138
- 要旨: ACT2023（Maryland）の proceedings。
- 本プロジェクトとの接続: 上に同じく定点観測。
- 引っ掛かりポイント: 同上。

---

## C. インフラ・電力網への直接応用

### [Specker, Anand, Bristow, Fairbanks 2020] Compositional Models for Power Systems
- venue: arxiv 2009.06833 / NIST 公開版
- link: https://arxiv.org/abs/2009.06833
- 要旨: 分散エネルギー資源 (DER) を symmetric monoidal category と categorical database で記述。汎用問題仕様と数値ソルバを関手で接続。
- 本プロジェクトとの接続: **最重要候補**。本プロジェクトのアイデア（インフラを圏で並べ、国ごとに具体化）にもっとも近い既存実装。Catlab.jl ベース。
- 引っ掛かりポイント: 米国向けの DER 単一国モデル。**国比較は不在**で、Grothendieck fibration による「国×実装」二軸の階層化も未実装。← ここに穴がある。

### [Baez & Fong 2018] A Compositional Framework for Passive Linear Networks
- venue: arxiv 1504.05625 / TAC Vol.33, No.38
- link: https://arxiv.org/abs/1504.05625
- 要旨: 抵抗・インダクタ・キャパシタからなる受動線形回路を decorated cospan の圏として定式化。合成性が成り立つことを証明。
- 本プロジェクトとの接続: 「電力網は decorated cospan で記述できる」というロールモデル。インフラを「境界（端子）+ 中身（回路）」と分けて扱う発想の原典。
- 引っ掛かりポイント: passive かつ linear に限定。実インフラの非線形性（変圧器、制御）を取り込むには拡張が必要。

### [Min, Anderson, et al. 2025] Compositional and Equilibrium-Free Conditions for Power System Stability — Part I: Theory
- venue: arxiv 2506.11406
- link: https://arxiv.org/abs/2506.11406
- 要旨: 不均一非線形デバイスを含む電力系統の安定性を、平衡点に依らないローカル条件で合成的に保証する枠組み。
- 本プロジェクトとの接続: 上記 Baez-Fong の「passive/linear」制約を破る新しい方向。実インフラの動的安定性を圏論ベースで扱う最新成果。
- 引っ掛かりポイント: 「compositional」を強調するが厳密な圏論構成は限定的（symmetric monoidal までは行かない）。圏論側との接続を深める余地。

---

## D. 一般システム理論・Petri net・Cospan

### [Baez, Genovese, Master, Shulman 2021] Categories of Nets
- venue: arxiv 2101.04238 / LICS 2021
- link: https://arxiv.org/abs/2101.04238
- 要旨: Petri net / pre-net / whole-grain Petri net / Σ-net を統一的に扱い、それぞれが生成する monoidal category の違いを左随伴で整理。
- 本プロジェクトとの接続: インフラの「資源・トークン」の流れを Petri net で表すなら、本論文がメタ理論の決定版。
- 引っ掛かりポイント: 純粋数学寄り。実応用（インフラ・サプライチェーン）の事例は最小限。

### [Baez, Courser 2020] Structured Cospans
- venue: arxiv 1911.04630 / TAC Vol.35
- link: https://arxiv.org/abs/1911.04630
- 要旨: 「内部に構造を持つ open system」を関手 L: A → X で生成する cospan として定式化。decorated cospan の代替・拡張。
- 本プロジェクトとの接続: 「タイの電力網（オブジェクト）」と「ベトナムの電力網」を同じ A に持ち上げて比較するスキーマに使える。
- 引っ掛かりポイント: structured と decorated の使い分けが本プロジェクト用途では非自明。Patterson 2023（下）を併読すべき。

### [Patterson 2024] Structured and Decorated Cospans from the Viewpoint of Double Category Theory
- venue: arxiv 2304.00447
- link: https://arxiv.org/abs/2304.00447
- 要旨: structured/decorated cospan を double category の言語で整理し、open system 合成の選択肢を体系化。
- 本プロジェクトとの接続: 𝓘 を double category として組む際の現代的な手引書。Grothendieck fibration との接続も double 構造で見るとクリア。
- 引っ掛かりポイント: 抽象度が高く、応用文脈での具体例が少ない。「途上国インフラ」みたいな現場概念とのギャップが大きい。

### [Baez, Weisbart, Yassine 2025/forthcoming] Double Categories of Open Systems: the Cospan Approach
- venue: arxiv 2509.22584
- link: https://arxiv.org/abs/2509.22584
- 要旨: open Petri net / open dynamical system / open Petri net with rates を double category の cospan アプローチで統一展開。
- 本プロジェクトとの接続: 「機能圏 𝓕 / 実装圏 𝓘」を double category にまとめる雛形。
- 引っ掛かりポイント: 最新で参照論文がまだ少ない。逆に言えば乗っかれる先端。

### [Lanese, Sassone et al. 2025] Towards a Double Operadic Theory of Systems
- venue: arxiv 2505.18329
- link: https://arxiv.org/abs/2505.18329
- 要旨: 「systems theory」を symmetric monoidal loose right module（systems）× symmetric monoidal double category（interfaces and interactions）として組む統一枠。Petri net, Moore machine などを例として収納。
- 本プロジェクトとの接続: 𝓘 の合成則を最も汎用的に扱う枠組み。本プロジェクトの「機能/国/実装」三層を operadic に書き下す参考。
- 引っ掛かりポイント: 抽象的すぎて、エネルギー・水・通信などの個別ドメイン例なし。

### [Fong 2016] The Algebra of Open and Interconnected Systems（PhD thesis）
- venue: Oxford PhD thesis
- link: https://math.ucr.edu/home/baez/thesis_fong.pdf
- 要旨: decorated cospan を導入し、open system のさまざまな例（回路、signal-flow、Markov 過程）を構築。
- 本プロジェクトとの接続: open system 圏論派の出発点。「インフラを境界付きシステムとして合成する」発想の原典。
- 引っ掛かりポイント: 単一国・単一ドメインの設定。多国比較や fibration の応用は射程外。

---

## E. Heyting代数・直観主義論理 × 社会システム

### [Sallach 2017] Topos Modeling of Social Conflict: Theory and Methods
- venue: Advances in Computational Social Science (Springer)
- link: https://link.springer.com/chapter/10.1007/978-4-431-55236-9_4
- 要旨: 社会的対立をトポス圏で表現し、subobject classifier が誘導する Heyting 代数構造を「ローカル直観主義論理」として活用する社会学的枠組み。
- 本プロジェクトとの接続: **直観主義論理 → 社会システム** の数少ない実例。本プロジェクトで「ある国では送電が満たされない」を Heyting 代数の `¬¬` 構造で扱う構想と整合。
- 引っ掛かりポイント: 形式モデルが思弁的で、計算可能な実装まで届いていない。実証データへの接続が弱い。

### [Patel 2024 ほか] A New Universe for Causality: How Topos Theory Rewrites the Rules of Causal Inference
- venue: 解説記事（Deep Paper）+ 元論文 arxiv（Universal Causal Inference）
- link: https://deep-paper.org/en/paper/17909_universal_causal_inferen-1195/
- 要旨: 因果介入 `do(X=x)` がトポス上の subobject を生成し、その論理関係が Heyting 代数になるという主張。
- 本プロジェクトとの接続: 「政策介入」を Heyting 構造で扱う動機付け。インフラ整備プロジェクト = 介入の合成として読める。
- 引っ掛かりポイント: 概念実証段階。Pearl 流の DAG ベース因果推論との比較・優位性が未整理。

### [Spivak & Kent 2012] Ologs: A Categorical Framework for Knowledge Representation
- venue: PLoS ONE 7(1)
- link: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3265496/
- 要旨: 自然言語的なオントロジーを圏として記述する olog。Spivak の categorical database 路線の知識表現サイド。
- 本プロジェクトとの接続: 「国の概念体系」を olog で書き、関手で他国と接続する素朴な道具。Heyting 構造（subobject）も扱える。
- 引っ掛かりポイント: 学術コミュニティでの普及が限定的。実プロジェクトでの大規模事例が乏しい。

---

## F. Grothendieck Fibration（本プロジェクトの中核道具）

### [Moeller & Vasilakopoulou 2020] Monoidal Grothendieck Construction
- venue: arxiv 1809.00727 / TAC Vol.35, No.31
- link: https://arxiv.org/abs/1809.00727
- 要旨: monoidal fibration と monoidal indexed category の同値（標準 Grothendieck 構成の monoidal 版）。fibration が ACT で使われる場面（network models, systems）を整理。
- 本プロジェクトとの接続: **直撃**。`p: 𝓘 → 𝓒` を monoidal fibration として組み、各国 c∈𝓒 のファイバ 𝓘_c で資源合成を行う、という構想の数学的バックボーン。
- 引っ掛かりポイント: 例が network model 中心で、社会システム・インフラへの応用は未着手。本プロジェクトはこの空白を埋めうる。

### [Hermida & co. ほか] Categorical Notions of Fibration（解説）
- venue: arxiv 1806.06129
- link: https://arxiv.org/abs/1806.06129
- 要旨: cloven / split / discrete / Cartesian fibration の関係を整理したサーベイ。
- 本プロジェクトとの接続: 𝓘→𝓒 をどのタイプの fibration として組むか選ぶ際の地図。
- 引っ掛かりポイント: 純粋圏論側で、応用との橋渡しは別途必要。

---

## G. 関連：合成ゲーム理論（インセンティブ層の参考）

### [Ghani, Hedges, Winschel, Zahn 2018] Compositional Game Theory
- venue: arxiv 1603.04641 / LICS 2018
- link: https://arxiv.org/abs/1603.04641
- 要旨: 経済ゲームを symmetric monoidal category の morphism として合成可能に再構築（open game）。
- 本プロジェクトとの接続: インフラ整備は複数アクター（政府・企業・住民）のゲーム。compositional game theory を「インフラ意思決定層」として 𝓒 や 𝓕 に重ねる発想に使える。
- 引っ掛かりポイント: 計算実装（フレームワーク）の成熟度が中途。実証データへの接続は別物。

---

## 穴の仮説（既存研究の隙間）

1. **「国×インフラ」を二重に階層化する fibration の応用例が事実上ゼロ**。Monoidal Grothendieck Construction（Moeller–Vasilakopoulou 2020）は理論を整えたが、応用は network model に留まり、政策・地理・制度差を国単位ファイバとして扱う研究は見当たらない。**ここが本プロジェクトの最大の白地**。

2. **電力系統の compositional モデル（Specker et al. 2020 / Min et al. 2025）はあるが、いずれも単一国・単一ドメイン**。クロスドメイン（電力 × 水 × 通信）も、クロスカントリー（タイ vs. ベトナム vs. ラオス）も扱われていない。`p: 𝓘 → 𝓒` の `𝓒` を「国 + ドメイン」のテンソル積として構成できれば新規性が立つ。

3. **Heyting代数の社会システム応用（Sallach 2017 ほか）は思弁段階に留まり、実データ／計算実装と結びついていない**。途上国インフラの「未充足ニーズ」を `¬φ`（古典否定）ではなく `¬¬φ`（直観主義二重否定）で扱う設計は、開発経済学のデータと組み合わせれば実証可能で、賈先生の Heyting 代数研究と直結する。

4. **ACT 主流の open system 圏論（Baez–Fong–Patterson 系）は工学的システムに偏り、開発経済・国際協力・ODA の文脈にほぼ持ち込まれていない**。例えば「ODA プロジェクトの合成」を structured cospan で記述する研究は皆無。世銀・JICA のプロジェクトデータと接続できれば差別化できる。

5. **時間発展（拡張・劣化・廃止）を扱う温度差**。temporal wiring diagram は提案されているが、インフラのライフサイクル（建設→保守→廃止）を fibration の射として扱う研究は見当たらない。歴史的ダイナミクスを含めると国比較研究としても深みが出る。

---

## 次のアクション候補

- **必読 5 本に絞る場合**: Spivak 2013（operad）, Fong–Spivak 2018（Seven Sketches）, Specker et al. 2020（power systems）, Moeller–Vasilakopoulou 2020（monoidal Grothendieck）, Sallach 2017（topos × 社会）。
- **手を動かす場合**: Catlab.jl で Specker et al. を再現 → 国インデックスを Grothendieck fibration として追加するプロトタイプ。
- **賈先生面談用**: 上記「穴の仮説」5 点を、それぞれ「先生の専門（モノイダル圏・Heyting・LLM圏論分析）との交差」とセットで A4 一枚にまとめると会話が走る。
