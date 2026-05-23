# 主張別 新規性マッピング

**作成日**: 2026-05-24
**目的**: 本プロジェクトの15主張 (A〜O) を既存研究と1対1で照合し、真の新規性が残る箇所を絞り込む。
**方針**: 「新規かもしれない」と楽観しない。文献ヒットがあれば原則 "部分既出" 以下に降格する。
**検索手段**: 既得サーベイ (literature/raw/01〜07) + literature/validation/V1〜V3 + WebSearch 15回

---

## 主張別 新規性マッピング

### A. 「便利と不可視コストの随伴 L⊣R」(notes/02, 08)

- 判定: **部分既出 (比喩レベルでは大量、圏論的厳密化はゼロ)**
- 既存研究:
  - [Zuboff 2019] Surveillance Capitalism: 「便利の対価としての監視」を社会学的に主張。形式化なし。
  - [Hinze 2010] Generic Programming with Adjunctions: 「観測と構成の随伴」一般論。社会的「便利/コスト」への適用なし。
  - [Sallach 2017] Topos Modeling of Social Conflict: トポス × 社会対立。`¬¬` 構造の言及はあるが随伴 L⊣R として具体化していない。
- 残る新規性 (1文): 「便利 (可視層拡張) と不可視コスト累積を free-forgetful 随伴 L⊣R として具体的に書く」構成は未見。ただし §5 自体が notes/08 で「雰囲気レベル」と自認しており、unit/counit を厳密に書ききるまでは新規性主張は弱い。
- 強度: **★★☆☆☆** (比喩は陳腐、厳密化に踏み込めば ★★★)

---

### B. 「機能圏 𝓕 + 国の圏 𝓒 + 実装圏 𝓘 の3層フレーム」(notes/01)

- 判定: **部分既出 (3層フレーム自体は陳腐、Grothendieck fibration での記述が新規候補)**
- 既存研究:
  - [Lawfare 2024] Three-Layer AI Governance Framework: 国×実装×機能の3層は政策論で常套句。
  - [Moeller & Vasilakopoulou 2020] Monoidal Grothendieck Construction: `p: 𝓘→𝓒` の monoidal fibration を網理論で使用。インフラ・国比較には未適用。
  - [Specker et al. 2020] Compositional Power Systems: DER を symmetric monoidal category で記述するが、単一国モデル。Grothendieck構造なし。
- 残る新規性: 「国 × インフラ (実装) × 機能」の三層を monoidal Grothendieck construction で記述し、ASEAN/モバイル金融の比較研究に適用」する組合せは未見。フレーム自体ではなく **適用ドメイン** に新規性。
- 強度: **★★★☆☆**

---

### C. 「リープフロッグ = 平行射の 2-cell」(notes/03)

- 判定: **真に新規 (ただし弱い)**
- 既存研究:
  - [Mutiso 2025] Five rules for technology leapfrogging: 経験則の列挙。形式化なし。
  - [Lee & Lim 2001] Economics of Technological Leapfrogging: stage-skipping/path-creating の二分。形式化なし。
  - [Binz et al. 2022] Transformative leapfrogging: 4類型分類のみ。圏論なし。
  - 圏論側で「parallel morphism × 2-cell」自体は nLab に標準項目あり (普通の道具)。
- 残る新規性 (1文): 「リープフロッグ = 同一機能対象への 2 つの平行射と、それらを結ぶ 2-cell (= 両立可能性)」という具体的圏論定式化を leapfrog 文献で行った例は皆無。
- 強度: **★★★☆☆** (定式化自体は容易だが、まだ誰も書いていない隙間)

---

### D. 「共通 CPN 規約 (4 backbone 比較フォーマット)」(notes/07)

- 判定: **真に新規 (応用論文として)**
- 既存研究:
  - [Ouyang & Billington 2008] CPN による電子決済 atomicity 検証: 単一プロトコル。比較規約なし。
  - [Pinna & Tonelli 2017] Bitcoin Petri net: 単体。
  - [Ganiyu 2019] Bank Cash Deposit HCPN: 単体。
  - サーベイ 07 結論: 「同一 CPN 枠組みで複数アーキテクチャを並べた先行研究は1本も検出できなかった」。
- 残る新規性: 「7必須場所 + 5標準遷移」のような厳密な共通規約を立て、中銀型/銀行型/民間型/電話会社型を同枠で記述する規約は皆無。
- 強度: **★★★★☆** (応用論文として独立価値)

---

### E. 「H-Petri Net (Heyting値補助場所付き)」(notes/06)

- 判定: **部分既出 (要警戒) — 名前と動機は新しいが、技術的構成要素は既出の可能性大**
- 既存研究:
  - [Engberg-Winskel 1990] Petri Nets as Models of Linear Logic: quantale を採用。Heyting algebra は **quantale の特例** として包含される。
  - [Lavore-Leal-de Paiva 2021/2025] Dialectica Petri Nets: 「lineale = Boolean と Heyting algebra に対応」と明示。複数 lineale の積も論じる。**Heyting版を直接扱う一般構造を提供しており、本プロジェクトの H-Petri Net は事実上この特殊例とみなされうる**。
  - [Meng-Lei ほか] Intuitionistic Fuzzy Petri Nets (IFPN): Atanassov型 IFS を採用。**Atanassov "intuitionistic" は標準 Heyting/Brouwer intuitionism とは異なる** (Dubois-Prade 2005 が用語論争を整理)。よって名称上の競合はあるが、意味論的には別物。
  - [Genovese-Loregian-Palombi 2021] Bounded Petri nets, comonad: 容量制約の categorical 化。
- 残る新規性 (1文): 「**可視層 (ℕ値, P/T) と不可視層 (Heyting値) を二層構造として明示し、不可視層の発火を ∨ で冪等更新する**」という二層分離は Dialectica 系 でも明示されておらず、ここに弱い新規性が残る。ただし Dialectica Petri Nets の "lineale product" を Heyting単独に specialize して二層化したと見ることもでき、純数学的には微差。
- 強度: **★★☆☆☆** (再警戒: Dialectica Petri Nets を熟読して差別化を明文化しないと「派生研究」扱いされる)

---

### F. 「Heyting値 unfading monotonicity」(notes/06 §5)

- 判定: **完全既出**
- 既存研究:
  - 標準 P/T Petri net の **monotonicity** (larger state → enabled transitions remain) は古典 (Desel-Reisig)。
  - **Monotonic extensions of Petri nets** (Abdulla et al., well-structured transition systems) は forward/backward search で扱われる。
  - **Persistent Petri nets** (Landweber-Robertson 1978, Best et al.): 「発火が他遷移を無効化しない」が古典概念。
  - [Oliver & Kuure 2026] Modelling Trust: 「lack of evidence does not imply not trusted」 (= 二重否定除去不成立) を Heyting で明示。本プロジェクトと同じ哲学。
- 残る新規性: 「Heyting値の `∨` の冪等性から monotonicity が自動的に出る」のは Heyting代数の代数的事実そのもの。
- 強度: **★☆☆☆☆** (これ自体は新規性ではなく、Heyting代数の `∨` 冪等性の繰り返し)

---

### G. 「R-restricted reachability = リープフロッグ可能性」(notes/12)

- 判定: **部分既出 (R-restricted という名称は新しいが、構造は既出)**
- 既存研究:
  - 「restricted reachability」「place-environment restriction」(Tredup-Erofeev 2021 arXiv:2112.03608): 場所の preset/postset 制約での reachability synthesis。
  - Reachability with **inhibitor arcs** (Reinhardt 2008): 特定場所に token が無いことを条件化 → 「Rを経由しない」と類似。
  - Petri net reachability decidability (Mayr 1981, Czerwinski 2019): 古典。
- 残る新規性 (1文): 「`R ⊂ P_v` を経由しない発火列の存在判定 = リープフロッグ可能性」という **応用解釈** は新規。技術的には inhibitor arc / restricted synthesis の特殊例で書ける。
- 強度: **★★☆☆☆** (技術的に新しくはないが、leapfrog文脈への応用がオリジナル)

---

### H. 「Backbone型 = Heyting半順序による分類」(notes/05, 09)

- 判定: **真に新規 (ただし応用論文レベル)**
- 既存研究:
  - 標準 Petri net の P-invariant / T-invariant 解析 (Murata 1989) で構造分類は古典。
  - [Specker et al. 2020] DER の categorical 分類: 国比較なし。
  - サーベイ 07: 「4 backbone を Petri net で並べた先行研究はゼロ」。
- 残る新規性: 「公的 ⊤_pub > 銀行 ⊤_bank > 民間 ⊤_priv」のような Heyting半順序での backbone 型分類は未見。
- 強度: **★★★☆☆** (主張Dと一体で評価すれば ★★★★)

---

### I. 「場所中心性 = ホットスポット (主張4)」(notes/05 §3, 未厳密化)

- 判定: **完全既出**
- 既存研究:
  - [Banerjee et al. 2013] Diffusion centrality: ネットワーク科学側で完成。
  - [Genovese-Loregian-Palombi 2021] Bounded Petri nets + coverability (Lipton 1976 EXPSPACE): 「特定場所への集中 = 詰まり」の formal 化は完了。
  - 通常の **Place Invariant** 解析 (Murata 1989): 集中度の構造解析は標準ツール。
- 残る新規性: 本プロジェクトの notes 自身が「未厳密化」と自認。現状では新規性ゼロ。厳密化しても既存ツールの再発見にしかならない可能性が高い。
- 強度: **★☆☆☆☆**

---

### J. 「Open H-Petri Net = Baez-Master 2018 の H拡張」(notes/10)

- 判定: **真に新規 (ただし派生)**
- 既存研究:
  - [Baez & Master 2018-2022] Open Petri Nets (arXiv:1808.05415): cospan-pushout で open net を symmetric monoidal double category として構築。
  - [Baez & Courser 2020] Structured Cospans
  - [Baez, Weisbart 系 2025] Double Categories of Open Systems (arXiv:2509.22584): open Petri net with rates の double category 拡張。**ここで rates が値 (実数等) を取る拡張は既出**。
  - [Baldan-Corradini-Montanari 2008] Open Petri Nets: 古い系譜。
- 残る新規性 (1文): 「open化された Petri net の入出力ポートを **不可視 (Heyting値) 場所にも許す**」拡張は Baez-Master 系列で扱われていない。ただし Baez-Weisbart 2025 が "with rates" として既に値付き拡張を進めているため、その rates を Heyting値に specialize したと位置づければ「派生」扱い。
- 強度: **★★★☆☆** (Baez-Weisbart 2025 との差別化を明示しないと弱い)

---

### K. 「Meet Bottleneck Theorem (越境決済は最弱国に律速)」(notes/10 §4) ★

- 判定: **真に新規 (本プロジェクト最強候補)**
- 既存研究:
  - [Baez & Master 2018] cospan-pushout 合成の universal property: 構造定理は既出だが「meet 律速」という命名・解釈はない。
  - [Master 2021] **Additive Invariants of Open Petri Nets** (Compositionality journal): 不変量の合成則を扱うが、Heyting値の meet ではなく加法的不変量。本プロジェクトと **直接競合する可能性あり** — 必読・差別化必須。
  - ASEAN+3 政策論 (AMRO/IMF 2025): 「最弱規制国でリスク」は政策的通念。形式化なし。
- 残る新規性 (1文): 「cospan-pushout で merge された Heyting値場所の上限が、各構成要素の **Heyting meet** で律速される」という定理を、ASEAN5 越境決済に実証可能な数学的命題として提出した例は皆無。
- 強度: **★★★★★** (本プロジェクト最大の独自貢献候補。ただし Master "Additive Invariants" を必読し差別化要)

---

### L. 「⊗ max 律速 vs ▷ meet 律速の逆転」(notes/13 §6) ★

- 判定: **真に新規**
- 既存研究:
  - Baez-Master 2018: ⊗ (disjoint union) と ▷ (cospan-pushout) は別物として扱う標準的構造だが、**両者の律速方向が逆転する** という観察は明示されていない。
  - Dialectica Petri Nets (Lavore-Leal 2021/2025): lineale の積を扱うが、合成方向での律速逆転は議論なし。
- 残る新規性 (1文): 「並列合成 ⊗ は max 律速 (最強の backbone)、水平合成 ▷ は meet 律速 (最弱の国)」という **構造的双対性** を Petri net 上で示した例は未見。これは数学的にも応用的にも面白い。
- 強度: **★★★★☆** (Kと並ぶ独自貢献候補)

---

### M. 「𝓚_HPN = strict symmetric monoidal double 2-category」(notes/14)

- 判定: **部分既出 (構造は標準、特定構築が新規)**
- 既存研究:
  - [Baez-Courser 2020] structured cospans: symmetric monoidal double category の系統的構築。
  - [Baez 2025 等] Double Categories of Open Systems: open Petri net をこの形にする。
  - [Hansen-Shulman 2019] symmetric monoidal double categories: 一般理論。
- 残る新規性: H拡張版の特定実装。coherence axioms は Heyting代数の `∨` 冪等性から自動成立、という点で「構造自体は新規ではないが、Heyting版での well-defined 性確認」が貢献。
- 強度: **★★☆☆☆**

---

### N. 「Universal Property (Master 2019 Q-Petri Net 拡張)」(notes/11)

- 判定: **完全既出**
- 既存研究:
  - [Master 2019] Petri Nets Based on Lawvere Theories (arXiv:1904.09091): 任意の Lawvere theory Q について Q-Petri Net の free 構成 = 左随伴。**H-Petri Net = (Th(CommMon) × Th(HeytAlg))-Petri Net** とすれば自動的に universal property を継承するだけで、新規構成ではない。
  - [Meseguer & Montanari 1990] Petri Nets are Monoids: 元祖 free-forgetful 随伴。
- 残る新規性: ゼロ。本プロジェクト notes/11 §3.2 自身が「Master 2019 の枠組みそのまま継承」と認めている。
- 強度: **★☆☆☆☆** (引用元として有用だが、独自の universal property ではない)

---

### O. 「Jia-Floridi 2025 LLM論文と F_Bakong/F_GCash の構造的同型」(notes/08, 09)

- 判定: **真に新規 (ただし類比論)**
- 既存研究:
  - [Jia, Floridi, Tohmé 2025] arXiv:2512.09117: LLM を Rel 内の関手 + entailment 2-cell で記述。本プロジェクトに直接転用可。**外部から見ると独立ドメイン同士の類比**。
  - 圏論的類比論文は多数あるが (例: SIR モデル × 化学反応 = open Petri net 双方を Baez が論じる)、Jia-Floridi 2025 自体が極めて新しく、それを別ドメインに最初に転用するのは本プロジェクトが初。
- 残る新規性 (1文): 「LLM の Floridi-Jia 構造 (Rel + 並列ルート + entailment 2-cell) と、モバイル金融 backbone 比較の構造が同型」という主張は他に存在しない。
- 強度: **★★★☆☆** (新規だが類比は弱い貢献。本論文の本筋は別 (KとL) にする方が強い)

---

## 総括

### 真に新規と認められる主張 (★★★★以上)

| 主張 | 強度 | 性質 |
|---|---|---|
| **K. Meet Bottleneck Theorem** | ★★★★★ | 数学的命題 + 実証可能 |
| **L. ⊗ max vs ▷ meet 律速逆転** | ★★★★☆ | 構造的双対性の新発見 |
| **D. 共通 CPN 規約 (4 backbone)** | ★★★★☆ | 応用論文として独立価値 |

### 部分既出 (★★★、要差別化)

- B. 3層フレーム (ドメイン応用のみ新規)
- C. リープフロッグ = 2-cell (形式化が未踏)
- H. Backbone型 = Heyting半順序分類
- J. Open H-Petri Net (Baez-Weisbart 2025 と要差別化)
- O. Jia-Floridi 2025 との構造同型

### 完全既出または弱い (★★以下)

- A. L⊣R 随伴 (比喩レベル、厳密化が薄い)
- E. **H-Petri Net 自体** (Dialectica Petri Nets と要差別化、警戒度大)
- F. unfading monotonicity (Heyting代数の代数的事実)
- I. 場所中心性 = ホットスポット (未厳密化、Banerjee/Genovese で既出)
- M. 𝓚_HPN の構造 (Baez系列で標準)
- N. Universal property (Master 2019 そのまま)

### 最も強い新規性候補

**Theorem (Meet Bottleneck) + ⊗ vs ▷ 律速逆転 (主張 K + L)**

この2つを軸に論文を組めば、

1. 数学的に新規 (Heyting代数の meet/join が cospan-pushout vs disjoint union で逆転する構造定理)
2. 実証可能 (ASEAN5 越境決済データで検証可能、Project Nexus 公開資料)
3. 応用ドメイン未開拓 (モバイル金融に Petri net を当てた研究はゼロ)

の3点が揃う。これが本プロジェクトの **数学的本丸**。

### 学部レベルでの位置

「Baez-Master open Petri net + Lawvere theory の枠組みを継承し、Heyting値拡張を施し、ASEAN モバイル金融という未開拓応用ドメインで Meet Bottleneck Theorem を提出する」というプロジェクトは、**学部卒論として十分に成立する独自性**を持つ。

特にDが「比較規約」、Kが「中核定理」、Lが「構造的洞察」として三角形を作る構成が強い。

### 論文化可能なレベルでの位置

論文化を狙う場合の最大の警戒事項:

1. **Dialectica Petri Nets (Lavore-Leal-de Paiva 2021/2025)** との差別化を明示しないと「派生研究」扱いされる (主張Eへの直撃)
2. **Master "Additive Invariants of Open Petri Nets" (Compositionality 2021)** と K の関係を整理しないと「Heyting版の自明な特殊化」扱いされる
3. **Baez-Weisbart 2025 "Double Categories of Open Systems"** との関係 (open Petri net with rates の Heyting特殊化として位置づけられる可能性) を整理する
4. **Oliver-Kuure 2026** が Kan拡張・2-category への拡張を future work に挙げており、先取されるリスクあり (validation V2 で既に指摘済み)

これらに対する明示的な差別化説明を入れれば、**応用領域論文 (応用圏論 ACT proceedings レベル) として論文化可能**。トップ数学誌は厳しい (構成は派生、独自定理はK・Lに限定されるため)。

### 推奨される論文骨格

```
1. Introduction: モバイル金融の集中リスク (Suri-Jack, GSMA), Petri net 既存研究の空白
2. Common CPN spec (主張D): 7場所5遷移の比較規約
3. Open H-Petri Net (主張J): Baez-Master の H拡張、Dialectica との関係明示
4. Theorem (Meet Bottleneck) (主張K): 中核定理、ASEAN5 への適用
5. ⊗ vs ▷ duality (主張L): 構造的洞察
6. Empirical validation: Project Nexus 公開資料
7. Related work: Baez-Master, Master, Dialectica, Oliver-Kuure, Jia-Floridi の差別化
```

主張 A, F, I, N は本文から削るか、補遺に回すのが論理的。

---

## 引用必須リスト (新規性主張に直結するもの)

1. Baez & Master 2018 — Open Petri Nets (arXiv:1808.05415) ★★★★★
2. Master 2019 — Petri Nets Based on Lawvere Theories (arXiv:1904.09091) ★★★★★
3. Master 2021 — Additive Invariants of Open Petri Nets (Compositionality journal) ★★★★★ 必読・差別化必須
4. Lavore-Leal-de Paiva 2021/2025 — Dialectica Petri Nets (arXiv:2105.12801) ★★★★★ 必読・差別化必須
5. Meseguer & Montanari 1990 — Petri Nets are Monoids ★★★★★
6. Baez, Weisbart 2025 — Double Categories of Open Systems (arXiv:2509.22584) ★★★★ 差別化必須
7. Oliver & Kuure 2026 — Modelling Trust (arXiv:2602.11376) ★★★★★ (V2で既に判明)
8. Jia, Floridi, Tohmé 2025 — Categorical Analysis of LLMs (arXiv:2512.09117) ★★★★
9. Ouyang & Billington 2008 — CPN Electronic Payment ★★★★
10. Pinna & Tonelli 2017 — Petri Nets Model for Blockchain Analysis ★★★★
11. Moeller & Vasilakopoulou 2020 — Monoidal Grothendieck Construction ★★★
12. Engberg & Winskel 1990 — Petri Nets as Models of Linear Logic ★★★
13. Genovese-Loregian-Palombi 2021 — Categorical Semantics for Bounded Petri Nets ★★★
14. Mutiso 2025 — Five rules for technology leapfrogging (Science) ★★★
15. Suri & Jack 2016 — Long-run impacts of mobile money (Science) ★★★

---

## 検索ログ (新規性検証で実行した検索)

1. `"Heyting algebra" "Petri net" intuitionistic logic 2024 2025` → 主要hitなし、Dialecticaに集約
2. `"adjunction" convenience "hidden cost" technology categorical` → 数学・社会論ともhitなし
3. `"open Petri net" composition meet "fiber product" Heyting 2024 2025` → Baez-Master系のみ、Heyting特化なし
4. `"mobile money" OR "GCash" categorical "petri net" formal model` → ゼロ (07サーベイ確認)
5. `"leapfrog" "category theory" "functor" development economics formal` → ゼロ
6. `"R-restricted reachability" Petri net subset places` → 部分既出 (Tredup-Erofeev synthesis)
7. `"monotonicity" "Petri net" "unfading" persistent trust evidence` → 既出 (古典 monotonicity)
8. `"Dialectica Petri Nets" Lavore Leal lineale Heyting 2025` → 主張Eに直撃する既存研究
9. `"Place invariant" centrality concentration "Petri net" hotspot` → 既出 (古典 invariant 解析)
10. `"monoidal Grothendieck" "fibration" payment finance economics 2024 2025` → 金融応用ゼロ (本プロジェクトの隙間)
11. `"strict symmetric monoidal" "double" "2-category" Petri net Baez 2024 2025` → Baez-Weisbart 2025 確認
12. `"cross-border payment" weakest link OR fragility ASEAN` → 政策論あり、形式化ゼロ
13. `"Genovese" "Loregian" "Petri net" guarded bounded categorical` → bounded/guarded 既出
14. `"Master" "Lawvere theory" Petri net 2019 universal property "Q-net"` → Master 2019 確認
15. `"Heyting" valued OR "fuzzy Petri net" intuitionistic place semantics` → IFPN (Atanassov) 別物確認
16. `"Atanassov" intuitionistic fuzzy set difference Heyting algebra` → 用語論争確認 (Dubois-Prade 2005)
17. `"parallel arrow" "2-cell" leapfrog development category 2024 2025` → ゼロ (主張C生存)
18. `"Meseguer" "Montanari" "Petri nets are monoids" universal property` → 古典確認
19. `"open Petri net" "compositionality" "weakest" "bottleneck" "meet" theorem` → 命名で先行ゼロ、Additive Invariants は要差別化
20. `"Jia" "Floridi" LLM symbol grounding Kan extension 2025` → arXiv:2512.09117 確認

---

## 警戒事項 (最後にもう一度)

- **「新規かもしれない」と楽観しない**。本マッピングでは ★★★★ 以上の主張は3つ (K/L/D) のみに絞った
- 残りの12主張は派生・既出・未厳密化のいずれか
- 論文化するなら、本筋は K (Meet Bottleneck) + L (⊗ vs ▷ 双対性) + D (共通CPN規約 + ASEAN応用) で組み、他は補強材料に回す
- Dialectica Petri Nets, Master "Additive Invariants", Baez-Weisbart 2025 の3本は **本プロジェクトのほぼ全主張に直撃** するので、必ず読破してから論文を書く
