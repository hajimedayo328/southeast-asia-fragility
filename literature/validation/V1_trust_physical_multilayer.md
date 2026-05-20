# V1 検証: 信頼層 × 物理層の二層連動 = リープフロッグ国の真のリスク

**検証日**: 2026-05-16
**検証者**: Claude (Opus 4.7)
**検索回数**: WebSearch 15回 + WebFetch 3回

## 検証する仮説

> 「信頼層 × 物理層の二層連動が、リープフロッグ国の真のリスクである」
>
> - 物理インフラ層（電力、通信、金融）の脆弱性
> - 信頼インフラ層（評判、信用、制度信頼）の脆弱性
> - これらを interdependent / multilayer networks 枠組みで連動的に扱う

## 判定: **部分的に重なる論文がある（核心は空白）**

仮説の構成要素は個別には大量に研究されているが、**「信頼層と物理インフラ層を formal な multilayer / interdependent network として一体モデル化し、それをリープフロッグ国のリスク評価に適用した研究」は見つからなかった**。

### 既出の領域 (★既存研究で固められている)

1. **Interdependent infrastructure networks (電力×通信×交通)** — Buldyrev et al. 2010 Nature 以来、膨大な蓄積。物理層同士のカップリングは完全に成熟領域
2. **Multilayer financial networks (銀行間×市場×シャドーバンキング)** — Battiston系の DebtRank、systemic risk 文献群
3. **Cyber-Physical-Social Systems (CPSS) の trust management** — 工学側からの trust as a layer 概念は存在
4. **Information cascade × bank run** — Diamond-Dybvig 系のモデル、社会信頼の崩壊は研究されている
5. **Weaponized interdependence** — Farrell & Newman 2019 IS。発展途上国への影響まで議論あり

### 新規性が残る領域 (★私の仮説の核心)

- **「制度信頼／評判信頼」をネットワーク層として formal 化し、物理インフラ層と coupled percolation / cascade で連動させる定式化**
- **リープフロッグ国 (M-PESA型、UPI型、ASEAN後発組) の固有リスクとして二層連動を診断するフレームワーク**
- **「物理層の局所故障 → 制度信頼層の global collapse → 物理層への back-cascading」というフィードバック構造の形式モデル**

---

## ヒットした論文一覧

### [Ju et al. 2022] Exploring a Multi-Layer Coupled Network Propagation Model Based on Information Diffusion and Bounded Trust
- venue: PMC9339600 (MDPI Entropy系)
- link: https://pmc.ncbi.nlm.nih.gov/articles/PMC9339600/
- 仮説とのマッチ度: **周辺**
- 何を扱っているか: オンライン層・遷移層・オフライン層の3層でうわさ拡散と有界信頼を扱う
- 仮説と何がズレているか: 「物理層」とは対面コミュニケーションのことで、電力・通信・金融などのインフラではない。完全に社会内部の話
- 引用すべき度合い: ★★（「多層×信頼」の前例として枕詞用）

### [Sarkar et al. 2015] Multilayer network decoding versatility and trust
- venue: arXiv:1506.02066
- link: https://arxiv.org/abs/1506.02066
- 仮説とのマッチ度: **周辺**
- 何を扱っているか: ボリウッド俳優の協業ネットワークでの「trust=度数相関」分析
- 仮説と何がズレているか: 物理インフラと無関係、社会的trustも institutional ではない
- 引用すべき度合い: ★（タイトルが似ているだけ）

### [Ferraris et al. 2011] Trust based interdependency weighting for on-line risk monitoring in interdependent critical infrastructures
- venue: IEEE Xplore document 6061545
- link: https://ieeexplore.ieee.org/document/6061545/
- 仮説とのマッチ度: **部分一致 (要精読)**
- 何を扱っているか: タイトル上、相互依存する重要インフラ間で「trust」を重み付けに使う on-line risk monitoring。"trust"は社会的というより技術的reliabilityの可能性大
- 仮説と何がズレているか: trust が institutional trust か technical reliability か、本文で確認が必要 (WebFetch失敗)
- 引用すべき度合い: ★★★ (要精読、最重要候補)

### [Farrell & Newman 2019] Weaponized Interdependence
- venue: International Security 44(1), MIT Press
- link: https://direct.mit.edu/isec/article/44/1/42/12237/
- 仮説とのマッチ度: **部分一致**
- 何を扱っているか: グローバル経済ネットワークの hub を握る国が chokepoint / panopticon 効果で developing states を脅かす政治学的枠組み
- 仮説と何がズレているか: ネットワーク科学的 formal model ではなく IR 理論。trust は明示的にネットワーク層化されていない
- 引用すべき度合い: ★★★★ (リープフロッグ国脆弱性の上位概念として必須)

### [Aleta & Moreno 2019系] Multilayer Networks 系の総説
- venue: arXiv:1804.03488, Nature Physics 2023 (s41567-023-02132-1)
- 仮説とのマッチ度: 周辺
- 何を扱っているか: multilayer network science の方法論総説
- 仮説と何がズレているか: 信頼層×物理層の具体的応用は射程外
- 引用すべき度合い: ★★★ (方法論基盤として)

### [Boccaletti et al. 2014] / De Domenico 関連 multilayer review
- venue: Phys. Rep., Nat. Phys.
- 仮説とのマッチ度: 周辺
- 引用すべき度合い: ★★★ (方法論)

### [Buldyrev et al. 2010] Catastrophic cascade of failures in interdependent networks
- venue: Nature 464, 1025
- link: https://www.nature.com/articles/nature08932
- 仮説とのマッチ度: 周辺（物理層×物理層のみ）
- 引用すべき度合い: ★★★★★ (interdependent networks の出発点として必須引用)

### [Lemieux] Three-layer trust model of blockchain technology
- venue: 図のみヒット (RG fig 333659272)
- 仮説とのマッチ度: 部分一致
- 何を扱っているか: ブロックチェーンを social layer / records layer / technical layer の3層 trust model で論じる
- 仮説と何がズレているか: ブロックチェーン特化の設計論、cascade dynamics なし
- 引用すべき度合い: ★★ ("layered trust" 概念の前例)

### [Carnegie 2024] Security and Trust in Africa's Digital Financial Inclusion Landscape
- venue: Carnegie Endowment policy report
- link: https://carnegieendowment.org/2024/03/08/security-and-trust-in-africa-s-digital-financial-inclusion-landscape-pub-91932
- 仮説とのマッチ度: 周辺 (実証側)
- 何を扱っているか: アフリカのデジタル金融包摂における trust とセキュリティの政策論
- 仮説と何がズレているか: formal network model ではなく政策レポート
- 引用すべき度合い: ★★★ (リープフロッグ国実証材料として)

### [Ahmad et al. 2020 / Aron 2018系] Mobile money reviews
- venue: J. Economic Surveys, Oxford
- 仮説とのマッチ度: 周辺
- 何を扱っているか: M-PESA等の総説、trust factor 言及あり
- 引用すべき度合い: ★★★ (実証ベース)

### [BIS 2024 FSI Insights No.60] BigTech infrastructure dependency
- venue: BIS publication
- link: https://www.bis.org/fsi/publ/insights60.pdf
- 仮説とのマッチ度: 部分一致
- 何を扱っているか: 銀行のBigTechクラウド依存が systemic 影響を生む concentration risk
- 仮説と何がズレているか: 信頼層を明示的にモデル化していない
- 引用すべき度合い: ★★★ (物理層集中の実証として)

### [Modeling cascading trust failures in social networks] Procedia Computer Science (1877-7503)
- venue: ScienceDirect S1877750321001149
- 仮説とのマッチ度: 部分一致
- 何を扱っているか: ソーシャルネットワーク内のtrust→distrust遷移の cascade、multiplex 表現
- 仮説と何がズレているか: 物理インフラ層との連動なし、social内のみ
- 引用すべき度合い: ★★★ ("trust cascade" 概念の直接前例)

---

## 最終判定詳細

### なぜ「空白」と言えるか

3軸すべてを同時に満たす研究が見当たらない:

| 軸 | 既存研究 | 仮説 |
|---|---|---|
| 1. 物理インフラの相互依存 | ◎ (Buldyrev 系) | 含む |
| 2. 信頼層を formal network 化 | △ (CPSSや trust cascade in social) | 含む |
| 3. リープフロッグ国の固有性 | △ (政策論レベル) | 含む |
| **1+2 同時** | × (Ferraris 2011がぎりぎり要精読) | 含む |
| **1+2+3 同時** | **未発見** | 仮説の core |

### 隣接3本 (空白を裏付ける近傍)

1. **Buldyrev 2010 Nature** — 物理×物理の interdependent network の出発点。信頼層なし
2. **Procedia 2021 cascading trust failures** — multiplex 上の trust→distrust cascade、物理層なし
3. **Farrell & Newman 2019 IS** — developing state 脆弱性論、network formal modelなし

この3本がそれぞれ「物理側」「信頼側」「リープフロッグ側」を埋めるが、**3つを1つの multilayer formal model に統合した先行研究は確認できなかった**。

### 引用すべき度合い Top 3

1. ★★★★★ Buldyrev et al. 2010 Nature — 方法論ルーツ
2. ★★★★ Farrell & Newman 2019 — リープフロッグ国脆弱性の上位概念
3. ★★★ Procedia 2021 (cascading trust failures) + BIS 2024 (BigTech dependency) — trust側・物理側それぞれ

### 残る新規性 (差別化ポイント)

- **二層coupling の formal化** (Buldyrev型の percolation を trust ↔ infrastructure に拡張)
- **リープフロッグ国の構造的特異性** (旧インフラ層を skip した結果、trust 層のbufferが薄い)
- **back-cascading フィードバック** (信頼崩壊 → 取付騒ぎ → モバイル金融 traffic spike → 通信障害 → さらなる信頼崩壊)
- **ASEAN/アフリカの実データ適用** (M-PESA、UPI、GCash、PayMaya等)

---

## 次にやること

1. Ferraris 2011 IEEE Xplore 論文を大学経由でフルテキスト取得・精読 (trust が institutional か reliability か確定)
2. Battiston系 DebtRank の trust 拡張版が無いか別ルートで再検索
3. ASEAN central banks の operational risk report (BSP, BI, BOT) で実証データの所在確認
4. Manlio De Domenico (Padova) の最新論文を直接チェック (multilayer 重鎮)
