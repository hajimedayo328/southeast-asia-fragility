# 27. 予言圏を Heyting-enriched category として厳密に閉じる

**作成日**: 2026-06-06
**ステータス**: draft v1 — 定義フェーズ(実装検証は §8 以降、別途)
**位置づけ**: notes/23 (予言ペア同型) と notes/26 (翻訳関手 F) には共通の穴がある:
**「圏の射 (morphism) が未定義」**。本ノートはこの穴を埋め、予言圏を
**4段階 Heyting 代数で enrich された圏** (Lawvere 1973 流) として厳密に閉じる。

---

## §0 なぜこのノートが必要か — 2つの穴

### 穴1: 射が未定義 (notes/26 §7 で自分が挙げた未確定論点)

notes/26 は「関手 F: 𝓒_EA → 𝓒_Dev」と書いたが、**対象 (backbone) はあっても射 (関係) が未定義**。
射が無ければ「関手」も「自然変換」も「Kan拡張」も**飾りの言葉**で、計算できない。

### 穴2: 循環論法のリスク (notes/23)

notes/23 は各ペアで「EA と Dev に**同じ Petri net テンプレート**を流し込んで同型」と書いた。
これだと φ は恒等に近く、**「同じ箱に入れたから同じ形」= 循環論法**。
意味ある主張には、EA と Dev を**独立に** hom 構造として組み、それでも F が通ることを
**発見**しないといけない。

→ 両方の穴は「**射を H 値として定義する**」ことで同時に塞がる。

---

## §1 enrich の土台: 4段階 Heyting 代数は可換 quantale

H = {⊥ < ⊤_priv < ⊤_bank < ⊤_pub} (notes/06)。

これが **可換 quantale** であることを確認する:
- 完備束 (finite なので自明に完備)
- 二項演算 `∧` (meet) は結合的・可換的
- 単位元 = ⊤_pub (`x ∧ ⊤_pub = x`)
- `∧` は `∨` 上に分配する (Heyting 代数 = frame の有限版): `a ∧ (b∨c) = (a∧b)∨(a∧c)`

→ `(H, ∨, ∧, ⊤_pub)` は **可換 unital quantale**。
これを Lawvere 1973 の `V = ([0,∞], ≥, +, 0)` の代わりに使う。

| | Lawvere の距離 V | 本ノートの H |
|---|---|---|
| 台 | [0,∞] | {⊥, ⊤_priv, ⊤_bank, ⊤_pub} |
| 順序 | ≥ (小さいほど近い) | ≤ (大きいほど強い影響) |
| テンソル ⊗ | + | ∧ (meet) |
| 単位 | 0 | ⊤_pub |

---

## §2 予言圏 = H-enriched category

### 2.1 定義

**H-enriched category 𝓒** とは:
- 対象の集合 `Ob(𝓒)` = backbone / 事象ノード
- 各対象ペアに **hom-object** `𝓒(A,B) ∈ H` を割り当てる
  - 解釈: 「A から B への**影響の強度**」(どの法的・構造的レベルで A が B に効くか)
- 2つの公理を満たす:
  - **恒等**: `⊤_pub ≤ 𝓒(A,A)`  すなわち `𝓒(A,A) = ⊤_pub` (自己影響は最大)
  - **合成**: `𝓒(A,B) ∧ 𝓒(B,C) ≤ 𝓒(A,C)`
    (A→B と B→C の影響の**弱い方 (meet)** が、A→C の影響の**下界**になる)

これは「H 値の前順序 (H-valued preorder)」と呼ばれる標準的構造。
(quantale-enriched category の特別な場合; Stubbe 2005 等で整備済み)

### 2.2 合成公理 = 律速の圏論化

合成公理 `𝓒(A,B) ∧ 𝓒(B,C) ≤ 𝓒(A,C)` は:
> 「影響の連鎖は、各リンクの**最弱 (meet)** で下から押さえられる」

これは notes/15 の **meet 律速**そのもの。
本プロジェクトの中心概念が、enriched category の合成公理として**自動的に**出る。
(Lawvere の三角不等式 `d(A,C) ≤ d(A,B)+d(B,C)` の Heyting 版)

### 2.3 これで穴1が塞がる

射 = hom の H 値。合成 = meet。恒等 = ⊤_pub。
→ 圏が**完全に閉じた**。関手・自然変換・Kan拡張が**定義可能**になった。

---

## §3 翻訳関手 = H-enriched functor (V-functor)

### 3.1 定義

**H-functor `F: 𝓒_EA → 𝓒_Dev`** とは:
- 対象の写像 `F: Ob(𝓒_EA) → Ob(𝓒_Dev)`
- **enriched 関手性 (lax)**: 任意の A,B で
  ```
  𝓒_EA(A,B) ≤ 𝓒_Dev(FA, FB)
  ```
  「EA で A→B に影響があれば、Dev でも FA→FB に**少なくとも同じ強度**の影響がある」

### 3.2 strict / lax の厳密な意味 (notes/26 を格上げ)

notes/26 では strict/lax を informal に使っていた。enriched で**正確に定義**できる:

| F の性質 | 条件 | 意味 |
|---|---|---|
| **strict (等長, isometric)** | 全 A,B で `𝓒_EA(A,B) = 𝓒_Dev(FA,FB)` | hom を完全保存 = 最強の予言 |
| **lax** | `𝓒_EA(A,B) ≤ 𝓒_Dev(FA,FB)` (一部で <) | Dev で影響が**増幅**される (例: bailout 余地) |
| **oplax** | `𝓒_EA(A,B) ≥ 𝓒_Dev(FA,FB)` (一部で >) | Dev で影響が**減衰**される |

→ 「予言の強度 = F が等長からどれだけズレるか」が、**hom 行列の差**として測れる。
これは notes/26 の主張を、**計算可能な量** (各 (A,B) での `𝓒_Dev(FA,FB) ⊖ 𝓒_EA(A,B)`) に変えた。

### 3.3 これで穴2 (循環論法) が塞がる

手順:
1. EA 側の hom 行列 `𝓒_EA(A,B)` を、**EA の現実の影響関係から独立に**埋める
2. Dev 側の hom 行列 `𝓒_Dev(X,Y)` を、**Dev の現実から独立に**埋める
3. 対象写像 F を固定し、`𝓒_EA(A,B) ≤ 𝓒_Dev(FA,FB)` が成り立つか**検証**する
   - 成り立てば F は (lax) functor として**実在** → 予言の構造的根拠
   - 一部で破れれば、そこが「予言が破れる境界」(notes/26 の lax 破れ箇所)

→ φ を押し付けるのでなく、独立に組んだ2つの hom 行列の間に F が**通るかを発見**する。
循環論法を断つ。

---

## §4 5ペアの再解釈 (hom 行列の比較として)

各ペアを「2つの小さな H-enriched category + その間の F」として書き直す。
**重要**: EA と Dev の hom 行列を独立に埋め、F の等長性を**測る**(押し付けない)。

例: ペア1 (1997 AFC ↔ 2008 Lehman)
- 𝓒_EA: 対象 {Thailand, BIBF, KR, IMF}、hom = 1997 の実際の影響強度
- 𝓒_Dev: 対象 {ShadowBank, Lehman, AIG, TARP}、hom = 2008 の実際の影響強度
- F(Thailand)=ShadowBank, F(BIBF)=Lehman, F(KR)=AIG, F(IMF)=TARP
- 検証: `𝓒_EA(BIBF, IMF) ≤ 𝓒_Dev(Lehman, TARP)` か?
  - EA: IMF 介入は ⊤_priv 維持 → `𝓒_EA(BIBF,IMF) = ⊤_priv`
  - Dev: TARP は ⊤_pub 格上げ → `𝓒_Dev(Lehman,TARP) = ⊤_pub`
  - `⊤_priv ≤ ⊤_pub` ✓ 成立 (Dev で影響が**増幅** = lax)
  → ペア1 は lax functor。「先進国の介入余地が大きい」が hom の不等号として出る。

これを5ペア全部、**コードで hom 行列を埋めて F の等長性を計算**する (§8)。

---

## §5 計算可能性 — 何が実際に計算できるか (まだ「できた」とは言わない)

有限 H-enriched category なので、以下は**原理的に**計算可能(実装して初めて主張する):

1. **F の等長性判定**: 全 (A,B) で `𝓒_EA(A,B)` と `𝓒_Dev(FA,FB)` を比較 → strict/lax/oplax/不成立 を分類
2. **等長からのズレの総量**: `Σ rank(𝓒_Dev(FA,FB)) − rank(𝓒_EA(A,B))` = 予言の歪みの定量化
3. **enriched Kan拡張 Ran_F**: quantale-enriched の右Kan拡張は **end 公式**
   ```
   (Ran_F G)(d) = ⋀_{a} [ 𝓒_Dev(d, Fa) ⇒ G(a) ]
   ```
   が **有限 meet と Heyting含意 ⇒ の組合せ**になり、計算可能
   (⇒ は Heyting 代数の相対擬補元; H が Heyting だからこそ end が書ける)
4. **逆翻訳 G の存在 (AFT)**: 有限なので Freyd の一般 AFT を待たず、
   **enriched Galois 接続**として G を直接構成・検証できる

⚠️ **現時点で「計算した」とは言わない**。§8 の実装で実際に回して、出た結果だけを主張する。
notes/25 (sheaf) で「数値で確認」と書きすぎた反省を踏まえる。

---

## §6 先行研究との接続 (実在確認済み)

- **Lawvere 1973** "Metric spaces, generalized logic, and closed categories"
  (Rendiconti Sem. Mat. Fis. Milano XLIII, 135–166; TAC Reprints No.1)
  → 距離空間 = [0,∞]-enriched category。本ノートはその **Heyting 版**。土台はこの古典。
- **Floridi-Jia-Tohmé 2025** (arXiv:2512.09117) の「2-cell as ⊆」
  → enriched の hom が H 値、その順序 ≤ が 2-cell。**同じ enriched 2-圏の発想**。
- **quantale-enriched category** (Stubbe 2005, Hofmann-Seal-Tholen 2014 "Monoidal Topology")
  → H 値前順序は既知の枠組み。本ノートは「既知の道具を予言ペアに当てる」応用。

→ **新規性の主張は最小限に**: 構成自体は Lawvere/quantale-enriched の既知物。
本プロジェクトの貢献は「backbone 予言ペアへの適用」と「meet 律速 = 合成公理という対応の明示」のみ。

---

## §7 このノートが**主張しないこと** (honest limits)

- ❌ 「enriched category を発明した」— Lawvere 1973 / quantale-enriched の既知物
- ❌ 「同型を証明した」— §3 は (lax) functor の存在検証であって同型ではない
- ❌ 「予言が当たることを証明した」— 構造的可能性 (hom 行列に F が通る) の主張に限る
- ❌ hom 行列の値自体の客観性 — 各 hom の H 値は**著者の割当て**(notes/25 と同じ留保)。
  ただし「割当てた行列の間に F が通るか」は割当てを固定すれば**客観的に計算可能**
- ⚠️ hom 行列の妥当性は別問題。実データで埋める方法 (§8 の次) は未着手

---

## §8 実装方針 (次フェーズ、ここから先は別作業)

`src/h_petri/category/` に:

```
src/h_petri/category/
├── enriched.py      # H-enriched category (hom 行列), V-functor, 合成公理検証
├── isometry.py      # F の strict/lax/oplax 判定 + ズレ総量
├── kan.py           # enriched 右Kan拡張 Ran_F の end 公式計算
└── pairs_enriched.py# 5ペアの hom 行列を埋めて F を検証
```

各段階で:
1. `EnrichedCategory` クラス: hom 辞書 + 合成公理 `𝓒(A,B)∧𝓒(B,C) ≤ 𝓒(A,C)` の**自動検証**
   (埋めた hom 行列が本当に圏の公理を満たすかをチェック → 満たさなければ行列が不正)
2. `VFunctor` クラス: 対象写像 + 等長性判定
3. 5ペアで F の strict/lax を**計算して分類** → notes/26 の表を**コード生成**に置換
4. Ran_F を1ペアで実際に計算して、「予言が破れる箇所」を数値で出す

→ これで notes/23, 26 の「informal な同型/翻訳」が
**「公理検証付きの enriched functor」** に格上げされる。
かつ §7 の留保を守り、計算で確認できたことだけを Pages に出す。

### §8.1 実行結果 (2026-06-06、実装済み)

`src/h_petri/category/enriched.py` + `pairs_enriched.py` を実装・実行。
EA/Dev を**独立に**生成子から閉包して F を分類した結果:

| ペア | F の判定 | distortion | 内容 |
|---|---|---|---|
| 2 (M-Pesa↔Cloudflare) | **strict** | 0 | 等長。最強の予言 |
| 3 (GCash↔GAFA-AI) | lax | +1 | 国内→グローバルで影響増幅 |
| 4 (メコン↔露ガス) | lax | +2 | 隠蔽(⊤_priv)→公然(⊤_pub)に増幅 |
| 1 (1997↔Lehman) | lax | +3 | 介入余地が IMF(⊤_priv)→TARP(⊤_pub) |
| 5 (Wave↔TikTok) | **broken** | −3 | Dev 側未完成で functoriality が3ペアで破れる |

- **全 EA/Dev 圏で公理 ✓**(閉包構成が identity + composition を保証、コードで検証)
- **狙ってない結果**: ペア1 で `hom(TH,IMF): ⊤_priv→⊤_bank` の増幅が、生成子に無いのに
  TH→BIBF→IMF の **meet 閉包から自動で出た**。フレームワークが入力してない帰結を計算した例。
- notes/26 の定性ランキング(ペア2最強・ペア5最弱)と一致。ただし今回は
  **独立に組んだ hom 行列から計算**された判定であって、押し付けではない。
- ⚠️ §7 の留保通り: hom 値は著者割当て。客観的なのは「公理が成立」「割当てを固定すれば
  F の判定が一意に決まる」の2点。割当て自体の妥当性(実データ化)は未着手。

出力: `docs/data/enriched_pairs.json`。

---

## §9 まとめ

- notes/23, 26 の穴 = **射が未定義 + 循環論法**
- 解決 = 予言圏を **H-enriched category** (Lawvere 1973 の Heyting 版) として閉じる
  - hom = 影響強度 ∈ H、合成 = meet (= 律速の圏論化)、恒等 = ⊤_pub
- 翻訳関手 = **H-functor**、strict/lax = **等長性のズレ** = 予言の歪みの定量
- 循環論法は「EA/Dev を独立に hom 行列化 → F が通るか検証」で断つ
- 土台は Lawvere 1973 / quantale-enriched (既知・実在)。貢献は適用に限定
- **計算は §8 の実装で回してから主張**(先走らない)

これが「理論を本気で詰める」第一歩。次は `src/h_petri/category/` の実装。
