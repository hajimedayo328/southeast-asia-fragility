# V3: 仮説検証 — リープフロッグ国は信頼集中度が高くハブ依存・脆弱

## 検証する仮説

**「リープフロッグ国（特にモバイルマネー普及国）は、信頼が単一ノード（電話会社・中央銀行・プラットフォーム）に集中しているため、ハブ依存・脆弱性が高い」**

具体例: M-Pesa (Safaricom)、Bakong (NBC)、WeChat Pay/Alipay (Tencent/Alibaba)、GCash/GoPay/MoMo、Aadhaar/UPI。

---

## 最終判定: **部分一致（強い間接エビデンスあり、しかし定量的・ネットワーク科学的研究は空白）**

- **政策論文・現場記事**: M-Pesa集中とSafaricom障害がKenyaのシステミックリスクであることを明確に指摘する公的文書・報道は豊富 (CBK, IMF, BIS, GSMA, 業界紙)。
- **学術論文（経済・規制）**: 「dominant provider」「concentration」「systemic」などの用語で議論あり。ただしHHI等の指標で定量化したマルチ国比較研究は希薄。
- **ネットワーク科学的定量化 (centrality, ハブ依存度指数を金融トラスト構造に適用)**: ほぼ空白。「信頼の集中度」をグラフ理論で測った先行研究は見当たらない。
- → 仮説の **存在主張は既存。新規性は「定量化・グラフ理論化」「複数国横断」**。

---

## ヒット一覧

### ★★★★★ [Kenyan Treasury / CBK 2016〜2025] M-Pesaの「systemic risk」分類
- venue: Kenya Budget Policy Statement / CBK reports, Business Daily等
- link: https://techcabal.com/2026/01/28/kenya-central-bank-m-pesa-failure-economy-collapse/
- マッチ度: 完全一致（実装側）
- 主張: Kenya政府が **2016年から公式にM-Pesaをsystemic riskに分類**。CBKは「failure would significantly impair the real economy」と明言。M-Pesaは2025年にKES 83.7兆 (≈GDPの4倍) を処理、Safaricomは小売決済の95%、月間アクティブ32M+。
- 引用すべき: ★5。仮説の「実証例」として中核。

### ★★★★★ [IMF 2021] E-Money issuers and systemic risk (Soupe et al., e-money paper)
- venue: IMF Departmental Paper, MCM/LEG 2021 (DP/2021/002)
- link: https://www.imf.org/-/media/files/publications/dp/2021/english/empsoupea.pdf
- マッチ度: 完全一致（政策論文）
- 主張: 「rapid adoption of e-money and its **market concentration** in some jurisdictions may make e-money issuers **potentially systemic** from a macro-financial perspective」。Safaricom M-Pesaのシェア約90%を具体例として挙げる。
- 引用すべき: ★5。仮説の総論として最上位の出典。

### ★★★★★ [IMF Soupe et al. 2021 続] Interoperabilityによる集中緩和
- 主張: 「powerful network effects in mobile money markets may result in **de facto monopolies**」→ Brazil等が相互接続義務化。
- 仮説とのズレ: 解決策側を論じている。集中度の定量比較ではない。
- 引用すべき: ★4。

### ★★★★ [BIS Working Papers / BIS Bulletin] BigTech・プラットフォーム集中
- venue: BIS WP No. 1129 / BIS Bulletin 45 / BIS Annual Report 2019 Ch.III
- link: https://www.bis.org/publ/work1129.pdf , https://www.bis.org/publ/bisbull45.pdf
- マッチ度: 部分一致
- 主張: 「retail payments is a particularly stark example of the potential for **rapid concentration** involving big techs」「operational and concentration risks ... systemic vulnerabilities if big techs experience significant disruptions」。中国、東南アジア、東アフリカが具体例。
- 引用すべき: ★4。仮説の上位フレーム（BigTech全般→モバイルマネーへの内包）として使える。

### ★★★★ [FSB 2019/2022] BigTech in Finance: market developments and risks
- venue: FSB report
- link: https://www.fsb.org/uploads/P091219-1.pdf
- マッチ度: 部分一致
- 主張: BigTech依存先の集中、operational risk、systemic threat。
- 引用すべき: ★4。

### ★★★★ [World Bank / IFC 2017] Risk Management in Mobile Money toolkit
- venue: World Bank/IFC Working Paper
- link: https://openknowledge.worldbank.org/entities/publication/b7f28659-a090-5749-8a52-d92f21a97576
- マッチ度: 部分一致（実装側のオペレーショナルリスク）
- 主張: モバイルマネー事業者のリスクカテゴリ網羅。フロート集中、ベンダー依存、エージェント管理等。
- 仮説とのズレ: 「provider内部リスク」中心。国家全体のハブ依存ではない。
- 引用すべき: ★3。

### ★★★★ [CGAP blogs / Focus Notes] 単一事業者ドミナンスと相互接続性
- venue: CGAP (World Bank系)
- link: https://www.cgap.org/blog/addressing-competition-bottlenecks-in-digital-financial-services
- 主張: 「mobile financial systems in developing countries being **dominated by a few large players** ... reduces incentives to lower prices or innovate」「given the early dominance of M-PESA in Kenya, regulatory intervention would be unlikely to produce interoperability without intervention」。
- 引用すべき: ★4。

### ★★★ [Kenya M-Pesa障害事例集]
- 2019年: 5時間障害で経済に「数十億ksh」損失（Treasury推計）
- 2023年7月: bank-to-M-Pesa transfers停止
- 2024年1月: 月内2回障害
- 2025年9月: SMS通知遅延が「fragility of mobile money systems」を露呈
- link: https://techtrendske.co.ke/2025/09/11/m-pesa-sms-delays-in-kenya/ , https://techcabal.com/2023/07/27/m-pesa-downtime-in-kenya/
- 引用すべき: ★4（実証ケースとして）。

### ★★★ [Caixin / SCMP 2021〜] Alipay-WeChat Pay デュオポリー
- 主張: 中国オンライン決済の **94%** をAlipay+WeChat Payが占める（duopoly）。中国当局がデジタル人民元で意図的に集中破壊を狙う。
- link: https://www.scmp.com/tech/policy/article/3118724/
- 仮説とのズレ: 「集中→脆弱」より「集中→規制」議論が主軸。systemicな障害事例の議論は弱い。
- 引用すべき: ★3。

### ★★★ [Aadhaar / UPI 関連] India Stack の単一障害点議論
- venue: IACR ePrint 2022/481 (India's Aadhaar: Structure, Security, Vulnerabilities), Policy Circle, Biometric Update
- link: https://eprint.iacr.org/2022/481.pdf
- 主張: Aadhaar設計者自身が「single point of failure」リスクを認める。6.5%の認証失敗率→脆弱層の排除を生む。UPIへの統合で連鎖リスク拡大。
- 仮説とのズレ: 排除（exclusion）議論が中心。経済全体のシステミックリスクへの接続は弱い。
- 引用すべき: ★3。Aadhaar/UPIは「中銀でも電話会社でもなく**国家ID**による集中」という別パターンとして言及価値あり。

### ★★ [Bakong / NBC] Cambodia
- venue: WEF, Asian Banker, ORF, Central Banking
- link: https://www.weforum.org/stories/2022/01/cambodia-hybrid-digital-currency-blockchain-bakong/
- 主張: Bakongは **Hyperledger Iroha (BFTコンセンサス)** ベースで複数機関にレジャー複製。「resilient by design against hardware failures, tampering, cyberattacks」と公式主張。
- 仮説とのズレ: **反証側**。Bakongは設計上、単一障害点を避けようとしている。ただしレジャー運用主体はNBC一極 → トラスト集中は残る（運用主体≠技術冗長性）。
- 引用すべき: ★3。「集中度をどう測るか」の議論材料。

### ★★★ [GSMA SOTIR 2024/2025] 業界統計
- link: https://www.gsma.com/sotir/wp-content/uploads/2025/04/The-State-of-the-Industry-Report-2025_English.pdf
- 主張: 世界モバイルマネー登録口座20億超、SSA 11億、336サービス稼働（うちSSAで165）。ただし**国内シェア集中度**には触れない。
- 引用すべき: ★3。マクロ統計の基礎データとして必須。

### ★★ [Mbiti & Weil NBER 2011] Mobile Banking: Impact of M-Pesa
- link: https://www.nber.org/system/files/working_papers/w17129/w17129.pdf
- 主張: M-Pesaの経済影響を実証。集中リスクには触れない（普及効果中心）。
- 引用すべき: ★2（背景文献）。

### ★★ [arxiv] Network science × payment 一般
- Lightning Network topology (2512.20641): 「persistent and growing centralization in routing, small number of nodes handle majority of traffic」
- Supply chain rewiring (2504.12955): meso-scale構造のsystemic risk
- 仮説とのズレ: モバイルマネー特化ではない。**手法的に転用可能**な隣接研究。
- 引用すべき: ★3（手法論として）。

---

## 特に確認した4項目

### (a) M-Pesa障害事例 — **実在・複数記録あり**
2019/2023/2024/2025の障害が報道。Treasury推計で5時間障害=数十億ksh損失。CEOによる原因説明（Daily Nation等）あり。事例集としては仮説実証に十分。

### (b) Bakong / Aadhaar の集中リスク議論
- Bakong: 技術的にはBFT分散だが、運用ガバナンスはNBC集中。学術的議論は薄い (AEPR 2024 "Design of CBDC in Cambodia" 1本)。
- Aadhaar: 集中リスク議論は**豊富**だが、「ハブ脆弱性」ではなく「排除・監視」の文脈。

### (c) 「信頼の集中度」を**定量化**した研究 — **ほぼ空白**
- HHI×モバイルマネーの単体研究は見つからず。Safaricom 90%という数字は政策レポート（IMF, GSMA）に散発的に出るのみ。
- ネットワーク中心性 (betweenness, eigenvector) でトラスト構造を測った研究は payment system全般では存在するが、**リープフロッグ国の信頼集中**を主題にしたものは未発見。
- **→ ここが本研究の新規性ポイント**。

### (d) 政策論文 vs 学術論文の分布
| 観点 | 政策論文 | 学術論文 |
|------|---------|---------|
| systemic risk主張 | IMF, BIS, FSB, World Bank, CBK | 経済学・規制論で散発 |
| 定量化 | シェア数値の列挙のみ | HHI研究は銀行向け、モバイルマネー未適用 |
| ネットワーク科学 | ほぼ未参照 | Lightning Net等の隣接研究のみ |
| ケーススタディ | 豊富（M-Pesa, Bakong, India Stack） | M-Pesa中心、Bakong薄い |

---

## 仮説への含意

1. **「集中→脆弱」という主張自体は既存**。IMF/BIS/CBKレベルで認知済み。→ 本研究のオリジナリティは「ここを論じること」ではない。
2. **新規性は「圏論／グラフ理論で集中度を測り、複数国を比較し、リープフロッグ度との相関を出す」**部分。既存研究は単一国(Kenya中心)・記述的・分野横断弱。
3. **反論への備え**: Bakongのような「設計上分散」事例は仮説を弱めうる。→ 「技術的冗長性 vs 運用ガバナンス集中」を分けて測る必要がある。
4. **引用必須セット (Top 5)**:
   - IMF Soupe et al. 2021 (e-money systemic)
   - BIS WP1129 / Bulletin 45 (BigTech concentration)
   - CGAP "Addressing Competition Bottlenecks"
   - World Bank/IFC 2017 Risk Management in Mobile Money
   - Kenya CBK / Treasury Budget Policy Statement (M-Pesa systemic分類)
