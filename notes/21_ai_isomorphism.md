# 21. AI 依存 H-Petri Net — 異分野同型の実証

**作成日**: 2026-05-23
**ステータス**: draft v1
**位置づけ**: notes/18 §4 で立てた「AI依存と モバイル金融 が同型構造」を実装で検証する。
本プロジェクトの方法論の **汎用性** を AI ドメインで示す。

## §1 動機 — 異分野同型を実コードで

notes/18 で informal に主張した「ChatGPT = GCash、Claude = GCash、Llama = PayNow、政府AI = Bakong」を、
**実コードで動かして数値で確認** する。

これが動けば:
- 本プロジェクトのフレームワーク (H-Petri Net + Heyting値) が AI ドメインに転用可能
- 律速逆転 (Ghrist-Gould-Lopez) が multi-agent LLM chain でも成立
- 「東南アジアは先進国の予言」の **AI版** が出る

---

## §2 AI ドメインの H-Petri Net

### 2.1 共通 CPN 規約への対応 (notes/07)

モバイル金融:
```
UserWallet → PendingTx → Backbone → SettledTx → RecipientWallet
                          (NBCBackbone / GlobeBackbone / etc.)
```

AI ドメイン:
```
User → PromptInQueue → LLMBackbone → ResponseReady → UserOutput
                       (OpenAI / Anthropic / Meta / 政府AI)
```

→ **完全同型**。場所5個、遷移5個、不可視場所2個。

### 2.2 各 LLM の Heyting値割当

| LLM | type | TrustInLLM 上限 | AtrophyOfThinking 上限 |
|---|---|---|---|
| **ChatGPT (OpenAI)** | 民間プラットフォーム | `⊤_priv` | `⊤_priv` (個人責任) |
| **Claude (Anthropic)** | 民間 + 安全性重視 | `⊤_priv` (構造的にChatGPTと同等) | `⊤_priv` |
| **Llama (Meta オープン)** | 銀行コンソーシアム的 | `⊤_bank` (オープン化で分散) | `⊤_bank` |
| **政府AI** (UK BritishAI, 仮想) | 中央銀行型 | `⊤_pub` (国家保証) | `⊤_pub` (公的責任) |

### 2.3 モバイル金融との完全な対応関係

```
ChatGPT      ⟷  GCash          (両方 ⊤_priv 民間集中)
Claude       ⟷  GCash          (同じ Heyting rank)
Llama        ⟷  PayNow         (両方 ⊤_bank 分散構造)
Government AI ⟷  Bakong         (両方 ⊤_pub 公的保証)
```

これは categorical な **完全同型**。Heyting値の階数が完全に一致。

---

## §3 律速逆転 (Ghrist-Gould-Lopez) の AI版

### 3.1 並列利用 (⊗) vs Multi-agent chain (▷)

**⊗ (並列利用)**: ユーザーが複数 LLM を **選んで使う** 状況
- ChatGPT、Claude、Llama、政府AI から best を選ぶ
- TrustInLLM 上限 = `max(⊤_priv, ⊤_priv, ⊤_bank, ⊤_pub) = ⊤_pub`
- → **強い backbone があれば全体強い**

**▷ (Multi-agent chain)**: LangChain / LangGraph で **複数 LLM を chain で繋ぐ**
- Agent_1 (Claude) → Agent_2 (ChatGPT) → Agent_3 (Llama) のような chain
- TrustInLLM 上限 = `meet(⊤_priv, ⊤_priv, ⊤_bank) = ⊤_priv`
- → **最弱の LLM で全 chain が律速**

### 3.2 含意

「**multi-agent LLM システムは構造的に脆い**」が Ghrist-Gould-Lopez 2024 から自動的に出る。

これは AI alignment 議論への直接含意:
- AutoGPT, BabyAGI のような multi-agent system は最弱 LLM に律速される
- 1つの LLM がハルシネーションすれば、chain 全体が壊れる
- 「複数 LLM を組み合わせれば安全」は **構造的に成立しない**

### 3.3 数値実証

```python
# src/h_petri/domains/ai_dependency.py の出力
[Government AI]  TrustInLLM 最終: ⊤_pub
[Llama]          TrustInLLM 最終: ⊤_bank
[Claude]         TrustInLLM 最終: ⊤_priv
[ChatGPT]        TrustInLLM 最終: ⊤_priv

⊗ (4並列):  ⊤_pub  (政府AI想定)
▷ (chain):  ⊤_priv (ChatGPT/Claude律速)
Heyting階数差: 2
```

これは Bakong vs GCash の比較と **完全に同じ構造の数値**。
- 階数差 2 (notes/15 の ASEAN5 と同じ)
- 同じ規約・同じ遷移・同じ並列構造

→ **異分野同型が数値レベルで成立**。

---

## §4 障害履歴との照合

### 4.1 ChatGPT 障害 vs GCash 障害

ChatGPT 主要障害 (literature/raw/12_llm_provider_data.md 参照):
- 2022/11: launch 後 1ヶ月で初の major outage
- 2023/3: ChatGPT data leak incident
- 2023/12: 6時間停止 (世界規模)
- 2024/8: 4時間停止
- 2024/12: 1日断続停止

GCash 障害:
- 2017-2020: 複数回 1〜8時間停止
- 2023/5, 2024/11: 大規模 reconciliation エラー

→ **両者とも単一企業に依存、月単位で類似の障害頻度**。同型構造が時間的にも対応。

### 4.2 政府AI vs Bakong の比較

政府AI (仮想):
- 障害履歴: ない (まだ存在しないため)
- 推定: 国家ITインフラの安定性に依存 → 中央銀行の安定性と同等

Bakong:
- 5年で障害公開報告ゼロ
- ただし開示バイアスの可能性

→ 両方とも「公開報告ゼロ」、構造的に堅牢だが、開示の信頼性に課題。

### 4.3 Llama vs PayNow の比較

Llama (オープン):
- 障害なし (Meta が止めても重みは流通済み)
- 個別 hosting で動く

PayNow:
- バンクコンソーシアム障害は個別銀行で起きる
- 全停止は稀

→ 両方とも分散構造の強みを持つ。

---

## §5 政策的含意

### 5.1 AI 依存 vs モバイル金融 — 同じ問題が先進国に来る

東南アジアでは:
- GCash 1社集中 → 政府が懸念 (BSP/Bangko Sentral の規制)
- M-Pesa Kenya が GDP 59% を経由 → CBK が systemic risk と認定

先進国で同じ構造:
- ChatGPT が世界の AI 利用の大半 → 各国 AI ガバナンス議論
- GAFA AI 集中 → EU AI Act、米国 Executive Order

→ **東南アジアの規制議論の経験が、先進国 AI ガバナンスへの予言になる**。

### 5.2 multi-agent システムの構造的脆弱性

「multi-agent system は安全」という業界 narrative は構造的に弱い:
- 並列 (⊗) で使う限り強い
- chain (▷) で使うと最弱に律速
- → **agent chain を組む時は最弱 LLM の Heyting値を確認しろ**

これは practical な開発ガイドラインに直接使える。

### 5.3 政府AI の構造的優位 (仮想ケース)

もし政府がAIを直接提供 (例: UK BritishAI、Japan 国家AI) すれば:
- TrustInLLM ⊤_pub (国家保証)
- 民間 LLM (⊤_priv) より構造的に強い
- ただし民間の速度・イノベーションを犠牲にする (Time-concentration trade-off)

→ 「政府AI vs 民間AI」の選択は、Bakong vs GCash と同じ構造的選択。

---

## §6 反例の検証

### 6.1 「ChatGPT = GCash」は本当に同型か?

潜在的な差:
- ChatGPT は **国境を越える** (ASEAN GCash は国内)
- ChatGPT は **prompt engineering で動作変わる** (GCash は決まった金額)
- ChatGPT は **embedding を返す** (GCash はトークンを返す)

→ これらは categorical には **付帯情報** (annotation) で扱える。本質的同型は崩れない。

### 6.2 「Claude が ChatGPT より安全」は Heyting値に出るか?

Claude の Constitutional AI、ChatGPT より厳格 → 直感的には ⊤_priv より上 (例: ⊤_priv+0.5)。
しかし4段階の Heyting代数では区別できない (`⊤_priv` か `⊤_bank` のどちらか)。

→ **Heyting代数の細粒度化** (8段階や [0,1] 連続) が必要。
これは future work。

### 6.3 Llama = PayNow 同型は本当か?

Llama の利点: オープン化で「Meta が止めても重みが流通する」=分散。
PayNow の利点: バンクコンソーシアムで「1銀行が倒れても他が支える」=分散。

→ **両方とも「単一障害点を回避するための分散」** で同型。

ただしメカニズムは違う:
- Llama: 重みのオープン化 (情報の冗長性)
- PayNow: 多銀行連携 (主体の冗長性)

→ Categorical には同型、メカニズムには違いあり。

---

## §7 残る論点

1. **§6.2 Heyting代数の細粒度化**
   - 4段階を [0,1] 連続値にする
   - これで Claude vs ChatGPT の微妙な差を表現
2. **Multi-agent system の Petri net 実装**
   - LangChain の workflow を H-Petri Net で書く
   - 律速逆転を実コードで再現
3. **動的な信頼変化**
   - LLM が更新されると Heyting値が変化 (例: GPT-4 → GPT-4.5)
   - これは時間関手 Trust: Time → H (notes/19) で扱える
4. **AI 障害カスケード**
   - ChatGPT が止まると LangChain が止まる、agent system が止まる、ユーザーが止まる
   - cascade 解析を Petri net で
5. **「世界初」の主張範囲**
   - 「AI Petri net 形式化」は既存サーベイ (literature/raw/13) で空白か?
   - もし空白なら本ノートが独自貢献

---

## §8 まとめ

実コードで確認したこと:
- ChatGPT/Claude/Llama/政府AI を 同じ H-Petri Net 規約で書ける
- Heyting値の階数が モバイル金融 backbone と完全一致
- 律速逆転 (Ghrist-Gould-Lopez) が AI ドメインでも数値で再現
- multi-agent chain は構造的に脆い (最弱 LLM 律速)

これで本プロジェクトの方法論が **AI alignment 議論にも転用可能** と示せた。

「東南アジアは先進国の予言」の **AI版**:
> モバイル金融で起きている (1社集中、規制議論) ことは、AI でもこれから起きる。
> ChatGPT 集中の AI 規制議論は、GCash 規制議論と同じ構造で進む。

これが本プロジェクトの **応用範囲の広さ** の証明。
