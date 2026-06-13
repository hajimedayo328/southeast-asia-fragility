# 29. 予言ペアの辺をグラウンディングする → 判定は under-determined

**日付**: 2026-06-14
**ステータス**: 完了（実装＋実行＋出典裏取り済み）
**コード**: `src/h_petri/category/pairs_enriched_grounded.py`
**出力**: `docs/data/enriched_pairs_grounded.json`
**前提**: notes/27 §7・§8.1・**§8.3**、`src/h_petri/data/backbone_facts.py`

---

## §0 動機 — §8.3 が残した最後の (b)

§8.3 の正直なスコープ宣言で、こう書いた:

> (c) 化できたのは金融 backbone の enriched 構造だけ。5予言ペアの事象間の辺
> (TH→IMF 等)は backbone Trust そのものではないので **(b) のまま**。

STORY §6 もこれを「予言ペアの辺のデータ化＝(b) の最後の大物」と呼んだ。本ノートは
これを埋める。`backbone_facts.py` が backbone **ノード**でやった規律——「出典付きの
法的バックストップ tier ＋ 単一ルール → Heyting レベル」——を、予言ペアの **26 本の
辺**に適用する。

問いは1つだけ: **strict / lax / broken の判定は、辺を一貫してグラウンディングしても
生き残るか?**

結論を先に: **生き残るのは5本中1本(ペア2)だけ**。残りは読み方依存で反転する
(ペア1・3・5)か、そもそもグラウンディング不能(ペア4)。予言強度スペクトルは
**著者の tier 判断のアーティファクト**であり、測定された性質ではない。

---

## §1 方法（意図的に minimal・監査可能）

1. **辺ルール**: どの影響辺もある**機関**に錨を下ろしている。その機関の法的バックストップ
   tier を出典付き事実から取り（backbone_facts と同じ5段階）、
   **`hom(A,B) = tier(A) ∨ tier(B)`**、`NONINST = ⊥`（市場・経済・利用者集団は金融機関
   ではない＝⊥）で辺値を決める。
2. **再グラウンディングは contested な機関に錨を下ろす辺だけ**（IMF・OpenAI・Maya・Yoma）。
   他の辺は著者の私的プラットフォーム値のまま。こうすると判定の変化は**1つの出典付き
   tier に帰属**でき、全面再チューニングではない。保守的に「この tier を直すだけで反転」を
   示す。
3. **2ノードは本質的に両義的**（それぞれ2通りの defensible な読み）。1つを選ばず**両読みで
   判定を列挙**する。
4. **ペア4（地政学レバレッジ）は金融バックストップ tier が存在しない**。ルールが意味論的に
   不適用 → 強制せず「グラウンディング不能」と報告。

ルール `∨`（強い方の機関が辺を裏打ちする）は、著者の **uncontested な辺**を最もよく再現する
選択。例: (Wave→Yoma)=⊤_bank は max(priv, bank)、(Lehman→TARP)=⊤_pub は max(priv, pub)。

---

## §2 出典付きノード tier（2026-06-14 Web 検索で裏取り）

| ノード | tier | 根拠 | 出典 |
|---|---|---|---|
| OpenAI | ⊤_priv | 非営利→2025-10-28 再編、営利は **OpenAI Group PBC**（公益法人、非銀行）。著者の ⊤_bank は**規模**格上げで法的 tier ではない | openai.com/our-structure ; aljazeera 2025-10-28 |
| Anthropic | ⊤_priv | Delaware PBC、AI 企業、銀行ではない | anthropic.com（LTBT）; time.com/6983420 |
| GCash | ⊤_priv | BSP 認可の**非銀行** EMI。親会社が2024に「免許は規制増で遅くなる」と digital bank 免許に消極的と明言＝意図的に非銀行 | wikipedia/GCash ; bworldonline 2024-08-15 |
| **Maya** | **両義** | ①消費者 e-wallet＝非銀行 EMI（⊤_priv） ②**Maya Bank** は BSP 認可デジタル銀行（2021-09〜、認可6行の1つ）（⊤_bank） | rappler（PayMaya digital bank license）; maya.ph |
| **Yoma** | **両義** | ①2022に Telenor の51%を取得したのは **Yoma Strategic Holdings** 子会社 Yoma MFS Holdings＝**非銀行**の SGX 上場複合企業（⊤_priv） ②同 Yoma/FMI グループに **Yoma Bank**（CBM 認可商業銀行）がある（⊤_bank） | globenewswire 2022-01-17 ; wikipedia/Yoma_Bank |
| IMF | ⊤_pub | 公的国際金融機関。1997タイ介入は主権規模の公的救済。著者はこの辺を ⊤_priv と過小評価 | imf.org/About |
| TARP | ⊤_pub | 米財務省の公的救済($700bn) | （著者値と一致、uncontested） |
| Safaricom / Cloudflare | ⊤_priv | 通信事業者 / Web インフラ企業（いずれも非銀行） | （uncontested） |

NONINST（⊥）: TH, KR, ShadowBank, KEpay, KEeconomy, AIsvc, AImarket, PHmarket, MMusers,
USusers, およびペア4 の全ノード。

---

## §3 結果（コードの出力。`pairs_enriched_grounded.py`）

| ペア | 著者判定 | グラウンディング後 | 頑健性 | 何が起きたか |
|---|---|---|---|---|
| 1 (1997↔Lehman) | lax | **strict** | FRAGILE | (BIBF→IMF) を ⊤_priv→**⊤_pub** に正すだけで、「Dev 増幅」非対称が消える。EA 側も pub に届き TARP=pub と等長 |
| 2 (M-Pesa↔Cloudflare) | strict | **strict** | **ROBUST** | 両ノードとも明白に非銀行→priv。contested 辺なし＝判定不変 |
| 3 (GCash↔GAFA-AI) | lax | **strict ↔ broken** | FRAGILE | Maya=priv 読み→strict（OpenAI を bank→priv に正す）。Maya=bank 読み→**broken**（EA に bank 辺が立ち、非銀行 AI 2社の Dev を上回る）。**全スペクトル横断** |
| 4 (メコン↔露ガス) | lax | **不能** | — | 辺は資源遮断/兵器化＝強圧レバレッジの意味論。金融バックストップ tier 不在 |
| 5 (Wave↔TikTok) | broken | **strict ↔ broken** | FRAGILE | Yoma=priv（取得主体=非銀行持株）読み→strict。Yoma=bank（グループに銀行）読み→broken（著者値と一致） |

**頑健な判定: 4本(グラウンディング可能)中 1本(ペア2)のみ。**

特筆すべき2点（裏取りで判明、引き継ぎ想定を訂正）:
- **ペア3**: 著者の lax は**どちらの一貫読みでも再現されない**。lax には OpenAI=⊤_bank（規模格上げ）
  と Maya=⊤_priv（その銀行免許を無視）を**同時に**置く必要があり、これは tier 付けとして
  **内部不整合**。一貫させると strict か broken に分かれる。
- **ペア5**: 著者の broken は「Yoma=銀行裏付けの地元オーナー」前提に全面依存。だが**実際の
  取得主体は Yoma Strategic Holdings（非銀行持株会社）**であって Yoma Bank ではない。
  取得主体読みでは broken は消えて strict になる。

---

## §4 解釈 — これは「著者が誤り」ではなく「under-determined」の証明

- backbone **ノード**の MM 感度（KBZPay の ⊤_bank↔⊤_priv、`mm_sensitivity.py`）は**全結論
  非依存＝頑健**だった（notes/27、STORY §5）。今回の予言ペア **辺**は逆で、**判定が読み依存で
  反転**する。同じ Heyting スケールでも、ノードのバックボーン構造は (c) 化に耐え、事象間の
  辺は耐えない。
- 反転の正体は「同一スケールに2つの非互換な意味論を載せていた」こと:
  **法的バックストップ tier**（backbone_facts の規律）と **システム的リーチ/規模**（OpenAI を
  bank に格上げ、Yoma をグループ単位で bank 扱い）。後者の意味論なら著者値も筋が通るが、
  プロジェクトの (c) 化が依拠する前者で一貫させると判定が動く。
- これは §4 系（H¹ 前兆化）で見た「⊤_priv が ⊤_bank を演じる」と**同型のメカニズム**であり、
  §5.6 のマレーシア偽陰性とも同型: **headline が未グラウンディングのモデリング選択に乗っている**。

§8.2 の Kan gap で「期待した綺麗な相関が出なかったが正直」と同じく、ここでも「辺を
グラウンディングすれば判定が確定する」という期待は**成り立たなかった**。これが正直な結果。

---

## §5 格付けへの含意

- 予言ペアの辺 hom は **(b) のまま**。さらに今回、**(b) の中でも『割当て次第で判定が反転する』
  弱い (b)** だと判明した（ペア1・3・5）。STORY §5 の (b) 行をこの含意で更新する。
- 予言強度スペクトル（「ペア2 が最強 isometric、ペア5 が broken」等）を**確定した発見として
  主張してはいけない**。確定的に主張できるのは:
  - **ペア2 の strict は頑健**（両ノードが明白に非銀行）。
  - 公理の成立・Kan 随伴・構造整合は値非依存で (c) 級（既出、不変）。
- ペア4 は enriched-圏の枠組みでは**事象を辺として (c) 化できない**ことが明確になった
  （地政学＝法的バックストップ不在）。これは枠組みの適用限界の正直な明示。

---

## §6 正直な限界

- 辺ルール `∨` も5段階 tier も**モデル選択**（backbone_facts から透明に継承）。別ルール
  （min＝ボトルネック、source-only 等）なら別の数字になりうる。
- 本ノートは著者判定が**間違い**だとは示していない。**under-determined（出典付きの等しく
  defensible な読みの間で判定が反転する）**ことを示した。どの読みを採るかはモデル外の判断。
- 再グラウンディングを contested 辺に限定したのは保守的選択。全辺を `∨` で再計算すれば
  （例ペア1 (BIBF→KR) も bank 化）さらに動くが、「1 tier 直すだけで反転」を見せる方が強い。
- Maya/Yoma の「両義」は実在の二重構造（消費者ウォレット vs 認可銀行、取得主体 vs グループ）に
  由来する**実際の**曖昧さで、人為的に作った両論併記ではない。

---

## 出典

- OpenAI 構造: https://openai.com/our-structure/ ; https://www.aljazeera.com/economy/2025/10/28/openai-restructures-into-public-benefit-firm-microsoft-takes-27-stake
- Anthropic PBC/LTBT: https://www.anthropic.com/news/the-long-term-benefit-trust ; https://time.com/6983420/anthropic-structure-openai-incentives/
- GCash 非銀行: https://en.wikipedia.org/wiki/GCash ; https://www.bworldonline.com/banking-finance/2024/08/15/613988/gcash-hesitant-on-digital-bank-license/
- Maya 銀行免許: https://www.rappler.com/business/paymaya-gets-digital-bank-license/ ; https://www.maya.ph/stories/maya-is-1-of-the-6-bsp-licensed-digital-banks-in-the-philippines-today
- Yoma 取得主体: https://www.globenewswire.com/en/news-release/2022/01/17/2367508/0/en/Telenor-Group-agrees-to-sell-its-stake-in-Wave-Money-to-Yoma-Strategic.html ; https://en.wikipedia.org/wiki/Yoma_Bank
- IMF: https://www.imf.org/en/About
