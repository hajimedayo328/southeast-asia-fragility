# LLM プロバイダー 実データ調査

**調査日**: 2026-05-25
**目的**: 東南アジア・モバイル金融脆弱性研究の枠組み（Heyting値・カテゴリ論的脆弱性）を、LLMプロバイダーに同型適用するための実データ収集。
**手法**: WebSearch ×10 による status page／業界レポート／規制文書のクロス参照。

---

## 1. 障害履歴サマリ（主要10本）

| 日時 | プロバイダー | 障害時間 | 影響範囲 | 原因 |
|------|-------------|---------|---------|------|
| 2023-03-20 | OpenAI / ChatGPT | 約4時間 | 全世界、Plus加入者の1.2%の決済情報漏洩 | redis-pyライブラリのバグ（他人のチャット履歴・支払情報が露出） |
| 2023-11-08 | OpenAI / ChatGPT・API | 約2日（断続） | 全世界 | L7 DDoS攻撃（SkyNet botnet） |
| 2024-06-04 | OpenAI / ChatGPT | 数時間（史上最長級） | Web/Mobile/Desktop全停止 | 内部システム障害 |
| 2024-12-11 | OpenAI / 全API | 4.5時間 | 全製品 | 設定エラー（new telemetry serviceのkubernetes APIサーバー過負荷） |
| 2024-12-26 | OpenAI / ChatGPT・Sora・API | 9時間 | エラー率>90% | Azureクラウドデータセンター電源障害 |
| 2025-06-10 | OpenAI / ChatGPT・Sora・API | 15時間以上 | グローバル | 公式詳細未公表 |
| 2025-10-20 | AWS us-east-1（Anthropic直撃） | 15時間以上 | Claude完全停止、Perplexity、一部OpenAI Kubernetes、Slack、Snapchat等 | DynamoDB DNS解決失敗 → カスケード |
| 2025-11-18 | Cloudflare（ChatGPT/Claude/Perplexity同時直撃） | 4時間10分 | インターネットの約20%、AI3社同時停止 | Bot Management機能ファイルのDB権限変更でduplicate行 → サイズ倍化 → ルーティング失敗 |
| 2026-02-18 | Google Gemini | 数時間 | Web/Mobile、チャット履歴非表示 | バックグラウンドプロセス障害 |
| 2026-05-21〜22 | Anthropic / Claude.ai・Opus 4.7・Haiku 4.5 | 数時間 | API成功率低下 | 内部fix適用、公式詳細未公表 |

**Key Finding**: 2025年に「単一インフラ層（Cloudflare／AWS）が複数AIプロバイダーを同時にダウンさせる」事象が2回発生。プロバイダーが3社あっても**バックボーン層は1〜2社に収束**しており、フェイルオーバーは構造的に効かない。

---

## 2. 集中度（2025年中盤〜2026年初頭）

### エンタープライズLLM支出シェア（Menlo Ventures 2025）
- **Anthropic**: 40%（2024: 24%、2023: 12% → 急上昇）
- **OpenAI**: 27%（2023: 50% → 半減）
- **Google (Gemini)**: 約20%
- **Meta (Llama)**: 9%
- **その他オープンソース**: 残り

### コーディング用途（Claude Code効果）
- Anthropic: 54% （6ヶ月前は42%）
- OpenAI: 21%

### コンシューマー市場（ChatGPT支配）
- ChatGPT 週次アクティブ: 約9億人〜10億人（2026年5月）
- ChatGPT AI検索市場シェア: 76.85%（2026年4月）
- ただしWeb traffic シェア: 86.7%（2025年1月）→ 56.7%（2026年3月）に大幅低下

### 市場規模
- Foundation model API市場: 125億ドル
- Generative AI全体: 400億ドル超（2025年）

---

## 3. 背景構造（単一企業依存・インフラ依存・規制）

### OpenAI
- **資本依存**: Microsoft 130億ドル投資、AGI到達まではAPI排他権を保持
- **インフラ依存**: 2019〜2025年初頭まで Azure 排他。2025年1月以降は Right of First Refusal モデルへ移行。2025年9月、Oracle と 3000億ドル/5年のクラウド契約。**事実上 Azure 一強状態は崩壊**
- **法的位置**: Section 230 の AI generative 出力への適用は不明確（2025年 Walters v. OpenAI 進行中）

### Anthropic
- **資本依存**: Amazon 80億ドル + 追加最大250億ドル = 計約330億ドル相当
- **インフラ依存**: AWS Trainium 5GW 容量確保、10年で1000億ドル AWS 支出をコミット → **AWSロックイン構造**
- **2025-10-20 AWS us-east-1 障害で Claude が全停止** → 実証された単一障害点

### Google Gemini
- **インフラ依存**: 自社 GCP（TPU + Cloud）で完結。垂直統合度が最も高い
- **障害頻度**: 11ヶ月で143件以上の outage（Google AI Studio / Gemini API）

### Meta Llama
- **オープンソース戦略**: ライセンス上は分散だが、最強モデル（405B）は Meta が訓練。実質的に Meta + AWS Bedrock 経由が大半
- **規制セクター採用**: 銀行・通信・公的機関でオンプレ展開 → 「データ主権」需要を満たす
- **エンタープライズシェア9%** = 「分散しているが主流ではない」段階

### 規制環境
- **EU AI Act**: 2025年8月から GPAI（汎用AI）に transparency / documentation / rights 義務発効。違反は行政罰 + 加盟国によっては民事・刑事責任
- **AI Liability Directive**: 2025年2月に欧州委員会が**撤回**（コンセンサス欠如）→ LLM出力の責任所在は法的空白
- **米Section 230**: AI生成コンテンツへの適用は不確定。Hawley「No Section 230 Immunity for AI Act」は Cruz の異議で停滞
- **中国**: 2023年7月「生成AI管理暫定弁法」。ERNIE / DeepSeek / 全国産LLMは党中央の検閲ガイドラインに従う → **国家統制型**

---

## 4. Heyting値マッピング（本プロジェクト枠組み）

| LLM | type | TrustInLLM上限 | 法的保護 | 障害頻度 | 構造的類推 |
|-----|------|---------------|---------|---------|-----------|
| ChatGPT (OpenAI) | 民間プラットフォーム型 | ⊤_priv | Section 230適用不明、責任空白 | 中〜高（年5〜10件major） | GCash（85%集中、単一民間） |
| Claude (Anthropic) | 民間プラットフォーム型＋AWSロックイン | ⊤_priv（AWS従属） | 同上 | 中（AWS連鎖時に高） | GoPay（民間集中、決済層が外部依存） |
| Gemini (Google) | 民間プラットフォーム型・垂直統合 | ⊤_priv | 同上 | 高（年140件超の小規模outage） | TrueMoney系（自社インフラ完結だが寡占） |
| Llama (Meta) | 半オープン・分散展開可能 | ⊤_mid（用途による） | デプロイ主が責任を持つ → 分散 | 個別デプロイ依存 | **PayNow（銀行コンソーシアム）に近い**：仕様は共有、運用は分散 |
| ERNIE / DeepSeek (China) | 国家統制型 | ⊤_pub（党中央） | 国家責任で検閲・運用 | 不明（透明性低） | 中銀型／PromptPay（国家インフラ） |
| UK Project Mercury / UK-LLM | 国家後援＋私企業 | ⊤_pub に接近 | 政府ファンド支援、英国データ主権 | 立ち上げ段階 | PayNow初期段階に類似 |

**重要な発見**: OpenAI / Anthropic / Gemini は「3社あって分散している」ように見えるが、**全てが米国民間企業 + Azure/AWS/GCP の3クラウド + Cloudflare 1社** に依存。2025-11-18のCloudflare障害で実証されたとおり、**真の分散度はHeyting格子では同じ ⊤_priv に潰れる**。

---

## 5. モバイル金融との同型構造

### 具体的対応

| モバイル金融（東南アジア） | LLM（グローバル） | 同型のポイント |
|-------------------------|------------------|--------------|
| GCash 85%集中（フィリピン） | ChatGPT 76.85% AI検索シェア | 単一民間プラットフォームの寡占 |
| GCash → AWS依存 | ChatGPT → Azure依存（〜2025初） | 民間が単一クラウドに従属 |
| GoPay (Indonesia) | Claude (Anthropic) | 民間集中 + クラウド層単一依存 |
| PayNow (Singapore) 銀行コンソーシアム | Llama (Meta) 半オープン展開 | 仕様共有・運用分散モデル |
| PromptPay (Thailand) 中銀運営 | ERNIE / DeepSeek (中国国家統制) | 国家直接運営・統制型 |
| UPI (India) 公的IDインフラ | UK Project Mercury / UK-LLM | 国家戦略としての主権インフラ |

### 共通する脆弱性

1. **バックボーン単一障害点**: モバイル金融が AWS/Azure を共有しているのと同様、LLM 3 大社は Cloudflare（CDN/Bot Mgmt）を共有 → 2025-11-18 で同時崩壊
2. **法的責任の空白**: モバイル金融の「決済失敗時の責任所在」とLLMの「Hallucination責任所在」が同型に未確立（Section 230 / AI Liability Directive撤回）
3. **国家統制 vs 民間集中のトレードオフ**: PromptPay型（中銀）は障害耐性が高いが言論統制リスク（ERNIE）、GCash型（民間）は革新速いが寡占リスク
4. **オープンソース／コンソーシアム型の中間項**: PayNow ≈ Llama は「分散しているが運用品質が分散先に依存」→ Heyting格子の中間値

---

## 6. 主要発見

1. **2025年は「AIインフラの単一障害点」が複数回露呈した分水嶺の年**: AWS us-east-1（10-20）、Cloudflare（11-18）の2件で、ChatGPT / Claude / Perplexity が**同時に**ダウン。プロバイダー多様化はバックボーン層で打ち消される。

2. **Heyting値 ⊤_priv は単一値ではなく「依存ベクトル」**: 3社あっても (Azure, AWS, GCP, Cloudflare) の4要素に集約。真の sub-Heyting分散度を測るには**インフラ層まで降りて格子を取り直す必要がある**。

3. **Llama は PayNow と同型の中間項として唯一の構造的代替**: ただしエンタープライズシェア9%にとどまり、運用品質はデプロイ主に依存。**「規制セクター（銀行・通信・公的機関）で先行採用」**というパターンも PayNow ローンチ初期と一致。

4. **国家AI（UK Project Mercury、中国ERNIE）は ⊤_pub への移行を試みているが、UKはまだ立ち上げ段階、中国は透明性ゼロ**: モバイル金融でいう PromptPay / UPI に相当する「成熟した公的LLM」は2026年5月時点で**存在しない**。

5. **法的責任構造はモバイル金融より未成熟**: モバイル金融は中銀規制・決済法が存在するが、LLMは AI Liability Directive 撤回（2025-02）で欧州ですら空白。Section 230 のAI適用も判例待ち。

6. **エンタープライズ vs コンシューマーで集中度が逆転**: コンシューマー = ChatGPT 76%、エンタープライズ = Anthropic 40% で OpenAI を逆転。同じ「LLM市場」でもセグメントによって寡占者が違う → モバイル金融の B2C（GCash）vs B2B（銀行間決済）の構造分離と同型。

---

## 参考URL（主要のみ）

- [Cloudflare Outage Nov 2025 (SiliconANGLE)](https://siliconangle.com/2025/11/18/cloudflare-outage-briefly-takes-chatgpt-claude-services-offline/)
- [AWS us-east-1 Outage Oct 2025 (ThousandEyes)](https://www.thousandeyes.com/blog/aws-outage-analysis-october-20-2025)
- [Menlo Ventures: 2025 State of GenAI Enterprise](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/)
- [Anthropic-Amazon $100B AWS deal (TechCrunch)](https://techcrunch.com/2026/04/20/anthropic-takes-5b-from-amazon-and-pledges-100b-in-cloud-spending-in-return/)
- [Microsoft-OpenAI partnership end of exclusivity (OpenAI blog)](https://openai.com/index/next-chapter-of-microsoft-openai-partnership/)
- [EU AI Act GPAI enforcement Aug 2025 (White & Case)](https://www.whitecase.com/insight-our-thinking/ai-watch-global-regulatory-tracker-european-union)
- [Section 230 AI applicability (Fortune)](https://fortune.com/2025/10/08/ai-chatbot-section-230-meta-social-media-legal-shield-no-protection/)
- [China AI Policy DeepSeek Era (Carnegie)](https://carnegieendowment.org/research/2025/07/chinas-ai-policy-in-the-deepseek-era)
- [UK Sovereign AI Fund](https://www.sovereignai.gov.uk/)
- [Storyboard18: Biggest AI Outages 2024-2025](https://www.storyboard18.com/how-it-works/biggest-ai-outages-since-2024-chatgpt-claude-and-cloudflare-disruptions-that-shook-the-industry-91169.htm)
