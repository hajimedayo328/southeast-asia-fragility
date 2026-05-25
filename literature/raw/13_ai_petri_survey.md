# AI × Petri net サーベイ

調査日: 2026-05-25
調査手法: WebSearch 9回 + WebFetch 1回（403）

## 取得件数: 約45件 / 関連34件 / 直接該当 4〜5本

---

## 直接的研究 (LLM/AI agent を Petri net で形式化したもの, Top 5)

1. **TB-CSPN: Beyond Prompt Chaining — The TB-CSPN Architecture for Agentic AI** (Future Internet 17(8):363, MDPI, 2025年7月)
   - Topic-Based Communication Space Petri Net。Colored Petri Net セマンティクスで LLM エージェントを協調制御
   - Surface / Observation / Computation の3層、LLM は「コンサルタント層」のみに閉じ込め、業務ロジックはトークン通信で表現
   - LangGraph 比で LLM呼び出し66.7%削減、スループット167%向上を主張
   - **本プロジェクトに最も近い既存研究**

2. **An organizational theory for multi-agent interactions integrating human agents, LLMs, and specialized AI** (Discover Computing, Springer, 2025)
   - TB-CSPN と同著者系列。人間 + LLM + 専門AI をCPNで組織論的に統合
   - 「centauric supervision（人馬一体監督）」概念を提示

3. **Petri Net Structural Reduction for Temporal Epistemic Logic Verification in Multi-Agent Systems** (Computing and Informatics, 44(6), 2025)
   - LLM非依存だがマルチエージェント Petri net の検証手法
   - 状態爆発を構造削減で抑える

4. **Asynchronous Multi-Agent Systems with Petri nets** (arXiv:2504.00602, 2025)
   - 非同期エージェントの Petri net モデル化。LLM は念頭にないが基礎理論

5. **A Hybrid Petri Net–AI Architecture for Adaptive and ...** (IJISRT, 2025年10月)
   - Petri net と AI を組み合わせた適応制御。応用色強い

---

## 隣接研究 (Top 10)

1. **Quantifying Systemic Vulnerability in the Foundation Model Industry / AIIVI** (arXiv:2510.23421)
   - O-Ring 生産理論で AI 産業の集中脆弱性を定量化。AIIVI=0.82。**Petri netではない**が AI 集中リスクの formal model
2. **AI, Digital Platforms, and the New Systemic Risk** (arXiv:2509.17878) — AI+プラットフォームの hybrid systemic risk
3. **Identifying the Supply Chain of AI for Trustworthiness** (arXiv:2511.15763) — AIサプライチェーンのリスク分類
4. **AI Power, Global Risk: Quantitative Systemic Risk Modeling for AI-Dominated Civilizational Infrastructure** (2026 ed., ResearchGate)
5. **CPN4M: Testing Multi-Agent Systems under Moise+ Using Colored Petri Nets** (Applied Sciences 12(12):5857) — 古典MAS + CPN
6. **Petri (Anthropic alignment tool, 2025)** — 名前が紛らわしいが Petri net とは無関係（Parallel Exploration Tool for Risky Interactions）
7. **Petri net and rewriting logic based formal analysis of multi-agent safety-critical systems** (Boucherit et al., 2020)
8. **Categorical Semantics for Hierarchical Petri Nets** (arXiv:2102.00096) — Jia-Floridi 系の延長として圏論的扱い
9. **Dialectica Petri Nets** (arXiv:2105.12801) — Petri net の圏論的意味論
10. **BIS Papers No 154 The AI supply chain** (BIS, 2024) — 金融規制側からのAIサプライチェーン分析
11. **Cloud Concentration Risk: Agent Based Model for Systemic Risk Analysis** (2020) — ABM だが Petri net 親和性あり

---

## 判定

**AI 依存の Petri net 形式化: 部分既出（限定領域のみ）**

- **既出領域**: LLM マルチエージェントの「内部協調プロトコル」を CPN で形式化（TB-CSPN ファミリー、2025年に集中）
- **空白領域**:
  - **AIサプライチェーン全体（半導体→クラウド→LLM→ユーザー）の Petri net 形式化は完全空白**
  - **AI集中障害のカスケード故障モデル（GPT停止→下流AIアプリ連鎖崩壊）の Petri net 化も空白**
  - **GAFA AI / 政府AI（中国・EU）の対比を Petri net で表現した研究は皆無**
  - Floridi 系の AI ガバナンス論は哲学・倫理レイヤーに留まり、Petri net 等の operational model に落とし込んだ研究は見当たらない

---

## 本プロジェクトとの差分（新規余地）

TB-CSPN が押さえているのは「**1つのLLMエージェント群の内部協調**」であり、本プロジェクトが狙う「**AI 依存社会のマクロな脆弱性**」とはレイヤーが違う:

| 軸 | TB-CSPN等の既出研究 | 本プロジェクトの新規領域 |
|----|---|---|
| スコープ | 単一企業の LLM 多エージェント | 国家・地域のAI依存構造全体 |
| トークン意味 | 意味的トピック | 計算資源・モデルアクセス権・データフロー |
| 関心事 | 効率・正当性検証 | カスケード故障・集中リスク・地政学 |
| 評価指標 | LLM呼び出し回数・スループット | AIIVI類似の脆弱性指標 + 構造的到達可能性 |

**つまり「マクロAI依存×Petri net」は事実上の空白地**。AIIVI は formal だが Petri net ではなくスカラー指標。本プロジェクトは「AIIVI の動的版」「TB-CSPN のマクロ拡張」と位置付けられる。

---

## 推奨される取り扱い

- **独自貢献として書ける範囲**:
  - 「LLM API + 半導体 + 電力 + 規制」を場所(places)、ノード故障・規制発動・モデル更新をトランジションとする Petri net 構築
  - 中国・EU・米のAIガバナンスを別ネットとして並置し、合成積で相互作用を表現
  - 連鎖故障の到達可能性解析（OpenAI障害→金融AI→市場混乱の経路カウント）
- **限定すべき主張**:
  - 「LLMを Petri net 化したのは世界初」とは**書けない** → TB-CSPN がある
  - 「AI集中リスクの formal model 化は初」とも**書けない** → AIIVI がある
  - 書くべきは「**両者の交点（動的かつマクロな AI 依存 Petri net 形式化）が空白**」

### 引用すべき論文 Top 3

1. **TB-CSPN (Future Internet 2025)** — 直接の先行研究として必須引用。差分を明示する基準点
2. **AIIVI (arXiv:2510.23421)** — AI集中リスクの定量化先行例。スカラー vs グラフという差分を強調
3. **Petri Net Structural Reduction for Temporal Epistemic Logic Verification (Computing and Informatics 2025)** — 検証手法の方法論的引用
