# 23. 予言ペアの Petri net 構造的同型 — 5ペアの圏論的等価性検証

**作成日**: 2026-05-25
**ステータス**: draft v1 — 5ペアそれぞれの Open Petri Net を書き、構造的同型を Petri net レベルで主張
**位置づけ**: temporal.html §T7 (予言ペア) と §T9 (2030予測) の **数学的裏付け**

## §1 動機

temporal.html §T7 で5つの「東南アジア → 先進国」予言ペアを並べた:

| # | EA事象 | → 先進国事象 | ラグ |
|---|---|---|---|
| 1 | 1997 AFC | 2008 リーマン / 2010 欧州 | 11/13年 |
| 2 | 2019 M-Pesa 5h | 2025 Cloudflare 約4h | 6年 |
| 3 | GCash 85%集中 | GAFA-AI集中 | 4年 |
| 4 | 中国メコンダム | ロシア天然ガス露呈 | 12年 |
| 5 | Wave Money 強制オーナーシップ転換 (※旧「崩壊」は誇張、§7訂正参照) | TikTok divestment 要求 | 3年 |

これらが **「構造的に同型」** と主張してきた。本ノートで Petri net レベルで **同型射** を具体構成する。

---

## §2 同型の意味 — what does "structural isomorphism" mean

2つの Open H-Petri Net `O_EA` と `O_dev` が **構造的に同型** とは:
- 場所集合に **全単射** φ_P: P(O_EA) → P(O_dev) が存在
- 遷移集合に **全単射** φ_T: T(O_EA) → T(O_dev) が存在
- フローを保つ: φ が前置/後置関係を保存
- 不可視層 Heyting値が **対応する** (上限・増分パターンが同じ階数)

これは notes/09 の 2-category 上の **isomorphism in `𝓚_HPN`** と同じ概念。

---

## §3 ペア1: 1997 AFC ↔ 2008 リーマンショック

### 共通 Petri net 構造
場所: `BorrowerCountry`, `ShortTermFXDebt`, `BrokerBank`, `ContagionPath`, `CollapseEvent`
遷移: `Borrow`, `Refinance`, `Withdraw`, `Cascade`, `Bailout`
不可視場所: `TrustHub` (Heyting値), `SystemicRisk` (Heyting値)

### EA側 (1997 AFC):
- `BorrowerCountry` = タイ
- `BrokerBank` = BIBF, finance company
- `ContagionPath` = 域内 cospan (タイ→KR→ID→MY)
- `Bailout` = IMF プログラム (TrustHub だけ ⊤_priv → ⊤_priv 維持)

### 先進国側 (2008 リーマン):
- `BorrowerCountry` = US シャドーバンク
- `BrokerBank` = Lehman, Bear Stearns
- `ContagionPath` = グローバル cospan (US→EU→世界)
- `Bailout` = TARP, QE (TrustHub ⊤_priv → ⊤_pub に格上げ)

### 同型射
φ: Thailand → US シャドーバンク
   BIBF → Lehman
   ContagionPath (域内) → ContagionPath (グローバル)
   IMF → TARP/QE

**両者の差**: Bailout で先進国は TrustHub を ⊤_pub に格上げできたが、東南アジアは ⊤_priv 維持。
→ 「先進国は事後的に介入余地が大きい」が Heyting値階数の到達範囲の差として出る。

---

## §4 ペア2: M-Pesa停止 ↔ Cloudflare停止

### 共通構造
場所: `User`, `Backbone`, `Service`, `Recipient`, `OutageWindow`
遷移: `Request`, `Process`, `Deliver`, `Fail`, `Recover`
不可視場所: `SystemicLoad` (Heyting値で表現される影響規模)

### EA側 (2019 M-Pesa):
- `Backbone` = Safaricom 1社
- `Service` = ケニア国民の決済 (GDP 59% 経由)
- `OutageWindow` = 5時間
- 影響: Heyting値で `⊤_priv` (民間1社停止の規模)

### 先進国側 (2025 Cloudflare):
- `Backbone` = Cloudflare 1社
- `Service` = ChatGPT/Claude/Sora 等の全AI市場
- `OutageWindow` = 約4時間
- 影響: Heyting値で `⊤_priv` (民間1社停止)

### 同型射
φ: Safaricom → Cloudflare
   ケニア決済 → 世界AI市場
   5時間 → 約4時間 (どちらも数時間規模の単一民間backbone障害)

**観察**: どちらも数時間規模の単一民間backbone障害 (M-Pesa ~5h / Cloudflare ~4h) であり、
Heyting値階数 (⊤_priv vs ⊤_priv) も同じ。構造的同型として比較的強い証拠。

---

## §5 ペア3: GCash独占 ↔ GAFA-AI独占

### 共通構造
場所: `User`, `Service1`, `Service2`, `MarketShare`, `LockIn`
遷移: `Use`, `Compete`, `Acquire`, `Dominate`
不可視場所: `MonopolyCost` (Heyting値で「選択肢喪失」)

### EA側 (GCash):
- `Service1` = GCash (85%), `Service2` = Maya (13%)
- フィリピン決済市場 100%
- `LockIn` = ユーザーが他に行けない (二人乗りでGCash払い前提)
- `MonopolyCost` = `⊤_priv` (民間独占リスク)

### 先進国側 (GAFA-AI):
- `Service1` = OpenAI/Anthropic/Google (≒90%)
- 生成AI市場 100%
- `LockIn` = API ロックイン (各社固有 prompt 文化)
- `MonopolyCost` = `⊤_priv` (民間独占リスク)

### 同型射
φ: GCash → OpenAI (or 3社グループ)
   フィリピン国民 → AI ユーザー世界
   モバイル送金 → 生成AI使用

**継続中**: どちらも進行形。本プロジェクトのリアルタイム監視対象。

---

## §6 ペア4: メコン上流ダム ↔ ロシア天然ガス

### 共通構造
場所: `UpstreamSource`, `Pipeline`, `Downstream`, `PoliticalLever`
遷移: `Produce`, `Transmit`, `Cutoff`, `Diversify`
不可視場所: `DependencyHidden` (Heyting値で「気づいてない依存」)

### EA側 (メコン):
- `UpstreamSource` = 中国上流ダム 11基
- `Downstream` = タイ・ラオス・カンボジア・ベトナム・ミャンマー
- `PoliticalLever` = 中国の水管理権 (公式には否認)
- `DependencyHidden` = `⊤_priv` (政治的)→ 実際には ⊤_pub レベルの戦略依存

### 先進国側 (露ガス):
- `UpstreamSource` = ロシア天然ガス
- `Downstream` = EU (ドイツ・イタリア中心)
- `PoliticalLever` = 2022年ウクライナ戦争で発動
- `DependencyHidden` = 開戦前は `⊤_priv` (商業契約) として扱ってた → 戦時に `⊤_pub` (戦略依存) として暴露

### 同型射
φ: 中国上流ダム → ロシアガス田
   メコン下流5国 → EU 諸国
   水管理 → ガス供給

**観察粒度補題そのもの**: `⊤_priv` と見えてた依存が、危機で `⊤_pub` (戦略的) と暴露される構造。

---

## §7 ペア5: Wave Money 強制オーナーシップ転換 ↔ TikTok divestment 要求

⚠️ **訂正 (2026-06-12)**: 当初の記述「Wave Money 崩壊 → ユーザーは KBZPay に移行」は
**誇張だった**(捏造パターン: 実在の事件に劇的な結末を盛った)。出典付きの実像:
- クーデターで Ant Group の出資 ($73.5M) が**破談**、Telenor が51%を**$53Mの投げ売りで
  Yoma に売却**、アプリMAUは**半減**(2M+→1M、kr-asia)
- **Wave Money は崩壊しておらず Yoma 傘下で存続**(2023/9 Yoma資料: エージェント6.1万・
  国土90%カバー)。KBZPay はアプリウォレット部門で成長(別セグメント)
- 構造的事実 = 「**政治ショックが外資を強制退出させ、backbone のオーナーシップを転換**」

→ 訂正後の方が TikTok とのペアは**むしろ綺麗**: 両方とも「政治圧力による backbone の
強制的オーナーシップ転換」(EA は完了 Telenor→Yoma、Dev は未解決 ByteDance→米資本)。

### 共通構造
場所: `Backbone`, `ForeignOwner`, `NewOwner`, `Users`, `Regulator`
遷移: `Use`, `PoliticalShock`, `ForcedTransfer`, `ContinueService`
不可視場所: `BackboneTrust` (Heyting値、変動する)

### EA側 (Wave Money、訂正版):
- `Backbone` = Wave Money (telco系 MFS)
- 2021年クーデター → `PoliticalShock`
- `ForeignOwner` = Telenor (51%) + Ant (出資予定) → **両方退出**
- `NewOwner` = Yoma (地場コングロマリット) — `ForcedTransfer` **完了** ($53M 投げ売り)
- `BackboneTrust`: `⊤_priv` → 一時降下 (MAU半減) → 地場所有で部分回復

### 先進国側 (TikTok):
- `Backbone` = TikTok (ByteDance、中国資本)
- 2024 divestment 法 → `PoliticalShock` (国家安全保障)
- `NewOwner` = 米国所有候補 (Oracle 等) — `ForcedTransfer` **未解決**
- `BackboneTrust`: `⊤_priv` → 宙吊り (国家承認待ち)

### 同型射 (訂正版)
φ: クーデター → 米中対立
   Wave Money → TikTok
   Telenor/Ant (退出する外資) → ByteDance (退出を迫られる外資)
   Yoma (受け皿) → 米国所有候補 (受け皿)

**両者**: 「政治圧力で backbone の**所有権**が強制的に動く」構造。
切り替わるのは backbone 自体ではなく**その後ろに立つ者** — §10.5 の stalk 結論と同型。

---

## §8 まとめ表

| ペア | EA構造 | 先進国構造 | 同型射の存在 | Heyting値階数の対応 |
|---|---|---|---|---|
| 1 | meet律速崩壊 | meet律速崩壊 | ✓ | EA: ⊤_priv 維持, Dev: ⊤_pub格上げ |
| 2 | 単一民間backbone停止 | 単一民間backbone停止 | ✓ | 両方 ⊤_priv (どちらも数時間規模) |
| 3 | 民間プラットフォーム独占 | 民間プラットフォーム独占 | ✓ | 両方 ⊤_priv |
| 4 | 上流ノード戦略依存隠蔽 | 上流ノード戦略依存隠蔽 | ✓ | 両方: 平時 ⊤_priv, 危機時 ⊤_pub 暴露 |
| 5 | 政治圧力でオーナーシップ強制転換 (完了) | 同 (未解決) | ✓ | 両方: 転換後の Trust 再構築 |

→ **5ペアすべてが Open Petri Net レベルで同型** (φ_P, φ_T の構成可能性として)。

---

## §9 同型射の存在 ⇒ 何が言えるか

5ペアで同型射が構成できることは、本プロジェクトの中心命題:

> **「東南アジアで起きた構造的脆弱性は、先進国で同型構造として再発する」**

を **数学的にサポート** する。
ただし「同型 ⇒ 同じ振る舞い」は厳密には保証されない (写像はあっても、初期マーキングや発火順序が違えば挙動は違う)。

これは:
- 「**構造の同型は必要条件**」 (構造が違えば同じパターンは出ない)
- 「**初期条件 + 発火順序が一致すれば挙動も同型**」 (これは追加条件)

つまり本プロジェクトの予言は **「構造的可能性」** の主張。
**「同じ脆弱性が再発するために必要な構造的条件が揃っている」** という主張に絞れば数学的に正当化可能。

---

## §10 実装方針 (次フェーズ)

各ペアを Python で `src/h_petri/pairs/` 配下に実装:

```
src/h_petri/pairs/
├── pair_1_afc_lehman.py
├── pair_2_mpesa_cloudflare.py
├── pair_3_gcash_gafa.py
├── pair_4_mekong_russia_gas.py
└── pair_5_wave_tiktok.py
```

各ファイルが:
1. EA側と先進国側の Open H-Petri Net を構築
2. φ_P, φ_T の写像を明示的に書く
3. 同型射の検証関数 `verify_isomorphism(O_EA, O_dev, phi_P, phi_T)` を呼ぶ
4. シミュレーションで「同じ初期条件で同じ挙動」になることを実際に確認

これで予言ペアが「概念だけ」から「**動くコード + 同型射の検証**」へ昇格する。

---

## §11 残る論点

1. φ_P, φ_T を厳密に定義: 何が「同じ」を判定するか
2. 不可視場所 (Heyting値) の同型射の独自定義 (notes/06 §4.2 から拡張)
3. Open Petri Net の cospan 構造の同型 (ポート射の保存)
4. 初期マーキング `M_0` の対応関係
5. 5ペア以外の候補 (例: 「日本判子文化 → 米国紙小切手」? 「ベトナム送金 → 米国ギグエコノミー」?)

---

## §12 まとめ

5つの予言ペアは Open H-Petri Net レベルで同型射を構成できる:
- ペア1: meet律速崩壊 (両者の差は事後介入の余地)
- ペア2: 単一民間backbone停止 (どちらも数時間規模、M-Pesa ~5h / Cloudflare ~4h)
- ペア3: 民間独占 (継続中)
- ペア4: 上流戦略依存隠蔽 (観察粒度補題そのもの)
- ペア5: 政治圧力による backbone オーナーシップ強制転換 (訂正版、§7)

これで「東南アジアの脆弱性は先進国の予言」が、**圏論的同型としての構造的可能性** として根拠を持つ。

実装は別フェーズ (`src/h_petri/pairs/` 5ファイル) だが、概念整理はここで完成。
notes 23本目、本プロジェクトの理論側の現状最終ノート。
