# 07. 共通 CPN 規約 — ASEAN10 backbone を比較するための統一フォーマット

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: 05_petri_net_theory.md の主張3 (backbone型 = 不変量) と 主張5 (Open Petri Net 合成) の具体実装基盤

## §1 なぜ規約が要るか

07サーベイで強調された通り、論文化の鍵は:

> 「4類型 (中銀/民間/銀行/電話会社) を比較するための **共通 CPN 規約** (色・階層・タイミングの統一)」

理由:
1. 規約なしで Bakong を書き、GCash を書き、PayNow を書くと、3つが **構造的に直接比較できない** (場所数も遷移数も違う)
2. 比較不能なら「4類型の差は何か」が言えない
3. 一度規約を決めれば、ASEAN10全てに展開可能
4. 後で実装するとき書き直しコストが激減
5. 論文として「ASEAN を統一フォーマットで比較した最初の研究」が立つ (応用面の新規性)

つまり **規約 = 比較可能性の保証** であり、**論文化の必要条件**。

---

## §2 既存規約の参照

### 標準 P/T Net (Petri 1962)
- 場所・遷移・フロー (整数値)
- 最小規約、表現力は限定的

### Colored Petri Net (CPN, Jensen 1981)
- トークンに **型 (color)** を持たせる
- 例: トークン = `(user, amount, currency)` のタプル
- 表現力大幅に向上
- CPN Tools で実装

### Hierarchical CPN (HCPN, Jensen-Christensen 1991)
- **下位 Petri net** を「置換遷移」として上位に埋め込み
- スケール跨ぎ表現に必須

### Timed Petri Net (Merlin 1974, Ramchandani 1973)
- 各遷移に **発火時間** を割り当て
- 取引速度・タイムアウトを扱える

### Open Petri Net (Baez & Master 2018)
- **入出力ポート** で他のPNと合成可能
- ASEAN 国家間決済 (Project Nexus等) に必要

### AlgebraicPetri.jl
- Catlab.jl 上の Petri net 実装
- ACSets を内部表現に使う

→ 本プロジェクトの規約は **CPN + Hierarchical + Open + Heyting値拡張** を統合する。

---

## §3 本プロジェクト統一規約 (v1)

### 3.1 色集合 (Color Sets)

```
USER       = string             // ユーザー識別子
RECIPIENT  = string             // 受取人識別子
AMOUNT     = ℕ                  // 送金額 (最小通貨単位、例: 1 USD = 100 cents)
CURRENCY   = {USD, PHP, VND, THB, MYR, SGD, IDR, KHR, LAK, MMK, BND}
PROVIDER   = string             // 各 backbone プロバイダー名
TIMESTAMP  = ℕ                  // 単純時刻 (秒)
TRUST_LEVEL = H                 // Heyting代数値 (詳細後述)

TRANSACTION = USER × RECIPIENT × AMOUNT × CURRENCY × TIMESTAMP × PROVIDER
              (送金トークンの完全な型)
```

### 3.2 共通場所構造 (5 + 2 = 7 場所モデル)

すべての backbone Petri net で **必須の7場所**:

| 場所 ID | 名前 | 型 | 役割 |
|---|---|---|---|
| `p1` | `UserWallet` | `USER × CURRENCY × AMOUNT` | 送金者残高 |
| `p2` | `PendingTx` | `TRANSACTION` | 処理中取引 |
| `p3` | `Backbone` | `PROVIDER × TIMESTAMP` | backbone 内部状態 |
| `p4` | `SettledTx` | `TRANSACTION` | 確定取引 |
| `p5` | `RecipientWallet` | `RECIPIENT × CURRENCY × AMOUNT` | 受取人残高 |
| `p_inv1` | `TrustHub` | `TRUST_LEVEL` (Heyting値) | backbone信頼累積 |
| `p_inv2` | `SystemicLoad` | `TRUST_LEVEL` (Heyting値) | システム負荷累積 |

**規則**: 必須7場所に加えて、各backboneタイプは固有場所を追加してOK。
ただし固有場所は **必須7場所のいずれかから派生** すること (主場所の sub-type)。

### 3.3 共通遷移構造 (5遷移モデル)

| 遷移 ID | 名前 | pre | post | 役割 |
|---|---|---|---|---|
| `t1` | `InitiateSend` | `p1` | `p2`, `p_inv2 += δ1` | 送金開始、残高チェック |
| `t2` | `BackboneClear` | `p2`, `p3` | `p3'`, `p_inv1 += δ2` | backbone内処理 |
| `t3` | `Settle` | `p3'` | `p4`, `p_inv1 += δ3` | 取引確定 |
| `t4` | `Reconciliation` | `p4` | `p4`, `p_inv2 += δ4` | 帳簿整合 |
| `t5` | `AcknowledgeReceipt` | `p4` | `p5` | 受取確認 |

**Heyting値増分** `δ1, δ2, δ3, δ4 ∈ H` は backbone タイプで異なる:
- 中銀型: `δ2, δ3` で `TrustHub` の値が `⊤_{public}` 方向へ
- 民間型: `δ2, δ3` で `TrustHub` の値が `⊤_{private}` 方向へ
- 各タイプの δ 定義は §4 で具体化

### 3.4 階層構造

3階層:

```
[Layer A: ASEAN 域内合成] (Open Petri Net)
   ┃
   ┃ ポート: クロスボーダー入出力
   ▼
[Layer B: 国内決済システム] (この規約の主対象)
   ┃
   ┃ 各backboneタイプの違いを表現
   ▼
[Layer C: 個別取引] (Substitution Transition)
   ┃
   ┃ t2/t3 内部の詳細実装
   ▼
[Layer D: 暗号・コンセンサス層] (実装詳細、省略可)
```

Layer A は §5 で詳述。Layer B が本規約の中心。
Layer C/D は実装するときに展開する。

### 3.5 タイミング (Timed Extension)

各遷移に発火時間 `τ_i` を割り当て:

| 遷移 | 中銀型 | 民間型 | 銀行型 |
|---|---|---|---|
| `t1` InitiateSend | 1 sec | 1 sec | 2 sec |
| `t2` BackboneClear | 5 sec | 2 sec | 30 sec |
| `t3` Settle | 10 sec | 3 sec | 60 sec |
| `t4` Reconciliation | リアルタイム | バッチ (1日) | バッチ (1日) |
| `t5` AcknowledgeReceipt | 1 sec | 1 sec | 5 sec |

これは概算値。実データ (各国中銀統計、業界レポート) で補正。

### 3.6 backboneタイプ別 差分仕様

#### 中央銀行型 (TH PromptPay, KH Bakong)
- `TrustHub` の Heyting値: `⊤_{public}` (国家保証)
- 障害時の救済: 中央銀行責任 (国家責任)
- 相互運用性: 政府レベル (Project Nexus 等)
- **特性**: `δ2, δ3` が `⊤_{public}` に直接到達

#### 民間プラットフォーム型 (VN MoMo, ID GoPay/OVO/DANA, PH GCash, MY TNG)
- `TrustHub` の Heyting値: `⊤_{private}` (企業保証)
- 障害時の救済: 民法/破産処理
- 相互運用性: 中銀仕様への準拠 (QRIS, DuitNow QR)
- **特性**: `δ2, δ3` が `⊤_{private}` に向かう、ただし `⊤_{private} < ⊤_{public}` の半順序

#### 銀行コンソーシアム型 (SG PayNow, MY DuitNow, LA BCEL, MM KBZ, BN BIBD)
- `TrustHub` の Heyting値: `⊤_{bank}` (銀行保証 + 預金保険)
- 障害時の救済: 銀行規制 + 預金保険
- 相互運用性: 銀行間プロトコル (SWIFT, RTGS)
- **特性**: `⊤_{public} ≥ ⊤_{bank} ≥ ⊤_{private}` の半順序

#### 電話会社型 (ASEAN絶滅、M-Pesa 参考)
- `TrustHub` の Heyting値: `⊤_{telco}`
- 障害時の救済: 通信規制 (限定的)
- **特性**: `⊤_{telco} ≈ ⊤_{private}`

→ 4タイプは **Heyting代数の半順序の上で位置が違う** ことが、共通規約で明確化される。

---

## §4 各backboneタイプの Petri net テンプレート (具体)

### 4.1 Bakong (中央銀行型) — Layer B

```
場所:
  p1: UserWallet      初期: {(user_A, USD, 1000)}
  p2: PendingTx       初期: ∅
  p3: NBCBackbone     初期: {(NBC, t=0)}
  p4: SettledTx       初期: ∅
  p5: RecipientWallet 初期: {(user_B, USD, 0)}
  p_inv1: NBC_Trust   初期: ⊥
  p_inv2: NBC_Load    初期: ⊥

遷移:
  t1: InitiateSend
    pre: p1[(u, c, a)] s.t. a ≥ X
    post: p1[(u, c, a-X)], p2[tx], p_inv2[+= {tx_id}]
  t2: BakongClear
    pre: p2[tx], p3[(NBC, t)]
    post: p3[(NBC, t+5)], p_inv1[+= ⊤_{public}]
  t3: Settle
    pre: p3'[(NBC, t)]
    post: p4[tx_settled], p_inv1[+= ⊤_{public}]
  t4: Reconciliation
    pre: p4[tx]
    post: p4, p_inv2[+= reconciled]
  t5: AcknowledgeReceipt
    pre: p4
    post: p5[(r, c, a+X)]

Heyting値増分:
  δ2 = ⊤_{public}  // 中銀直接保証
  δ3 = ⊤_{public}
  → TrustHub は短時間で ⊤_{public} に到達
```

### 4.2 GCash (民間プラットフォーム型) — Layer B

```
場所:
  p1 〜 p5: 同じ
  p3: GlobeBackbone   初期: {(GlobeGroup, t=0)}
  p_inv1: Globe_Trust 初期: ⊥
  p_inv2: GCash_Load  初期: ⊥

遷移:
  t1, t2, t3, t4, t5: 構造は同じ

Heyting値増分:
  δ2 = ⊤_{private}  // 民間企業1社の保証
  δ3 = ⊤_{private}
  → TrustHub は ⊤_{private} に向かう
  
  但し ⊤_{private} < ⊤_{public} (Heyting代数の半順序)
```

### 4.3 PayNow (銀行コンソーシアム型) — Layer B

```
場所:
  p3: BankConsortium  初期: {bank1, bank2, ..., bankN}
  p_inv1: BankConsortium_Trust  初期: ⊥

特徴:
  - p3 がコンソーシアム = 複数銀行のmultiset
  - t2 発火に複数銀行の同意要 (BFT風)
  - δ2 = ⊤_{bank}  // 銀行 + 預金保険
```

### 4.4 KBZPay (銀行型、ミャンマー)

```
特徴:
  - 銀行型だが KBZ Bank 1社支配
  - p3 = {KBZ}  (single member consortium)
  - 構造的には銀行型、機能的には民間型に近い
  - これが「分類の grey zone」例
```

### 4.5 比較表

| 観点 | Bakong (中銀) | GCash (民間) | PayNow (銀行) | KBZPay (銀行→民間境界) |
|---|---|---|---|---|
| `p3` 構造 | 単一中銀 | 単一企業 | 複数銀行 | 単一銀行 |
| `δ2, δ3` | `⊤_{public}` | `⊤_{private}` | `⊤_{bank}` | `⊤_{bank}` |
| 法的保護 | 中央銀行法 | 私法契約 | 銀行法 + 預金保険 | 銀行法 |
| 障害時責任 | 国家 | 企業 | 銀行 + 預金保険 | 銀行 (限定的) |
| TrustHub順序 | 最強 (`⊤_{pub}`) | 弱 (`⊤_{priv}`) | 中 (`⊤_{bank}`) | 中 |

→ **共通規約の上で、4タイプの差が Heyting値の半順序で明確化される**。

---

## §5 Open Petri Net 拡張 (Layer A: ASEAN 域内合成)

### 5.1 Open H-Petri Net の定義

Baez-Master 2018 の Open Petri Net を H-Petri Net に拡張:

```
O = (N, i, o)
  N: H-Petri Net (本規約の Layer B)
  i: X → P 入力ポート関数 (X = 入力インターフェース集合)
  o: Y → P 出力ポート関数 (Y = 出力インターフェース集合)
```

合成は cospan の pushout:
```
O_1 ∘ O_2 = (N_1 ∪ N_2 / merge(o_1, i_2), i_1, o_2)
```

### 5.2 ASEAN5 合成例

TH (PromptPay) ∘ SG (PayNow) ∘ MY (DuitNow) ∘ ID (QRIS) ∘ PH (InstaPay)

- 越境決済プロトコル (Project Nexus) = cospan の射
- 5国合成 = 連続 pushout
- 合成後の TrustHub は **5国の Heyting値の meet** で評価される (最弱の国に律速)

### 5.3 ASEAN域内決済の構造的性質 (仮説)

- 5国の TrustHub Heyting値の **meet** が「域内決済全体の信頼」
- 1国でも `⊤_{private}` だと、域内全体が `⊤_{private}` に律速 (Heyting代数 ∧ で)
- → **域内決済は最弱backboneに律速される**

これが「ASEAN内の Trust hub bottleneck」を理論的に説明する仮説。実証可能。

---

## §6 atomicity 要件 (Ouyang & Billington 2008 借用)

### 6.1 atomicity 性質

- **All-or-Nothing**: 取引は完全成立 or 完全失敗
- **Money Atomicity**: 金銭移動の二重発生なし
- **Goods Atomicity**: 商品移動と金銭移動が同期
- **Certified Delivery**: 受取の証明可能性

### 6.2 H-Petri Net での atomicity 表現

- atomicity = T-invariant の存在
  - 「取引完了」か「巻き戻し」の T-invariant が両方存在
- Goods Atomicity = `p5` (RecipientWallet) と `p1` (UserWallet) の **質量保存** (P-invariant)
- Certified Delivery = `p_inv1` (TrustHub) のトークン累積で記録

### 6.3 backbone別 atomicity

| backbone | All-or-Nothing | Money Atomicity | Goods Atomicity | Certified Delivery |
|---|---|---|---|---|
| Bakong | 強 (BFT) | 強 | 強 | 強 (chain記録) |
| GCash | 中 (中央集中) | 強 | 強 | 中 (企業ログ) |
| PayNow | 強 (銀行間清算) | 強 | 強 | 強 (銀行帳簿) |
| KBZPay | 中 | 強 | 強 | 弱 |

→ atomicity の4性質を比較可能な数値指標に変える方法は §7 で詰める。

---

## §7 比較指標 (定量化)

### 7.1 構造指標

| 指標 | 定義 | 意味 |
|---|---|---|
| **集中度** `C` | `TrustHub` の支配シングル要素度合い | 高いほど単一障害点リスク |
| **冗長度** `R` | `p3` (Backbone) の constituent multiset サイズ | 高いほど復元力 |
| **atomicity rate** `A` | T-invariant でカバーされる遷移の比率 | 完了保証性 |
| **legal coverage** `L` | TrustHub Heyting値の上限 (`⊤_{public}/⊤_{bank}/⊤_{private}`) | 法的保護強度 |

### 7.2 動的指標

| 指標 | 定義 | 意味 |
|---|---|---|
| **TrustHub到達速度** `v_T` | `⊤` に到達する発火回数 | 信頼累積の速さ |
| **障害復旧時間** `T_recovery` | `p3` 破壊後の reachability 回復時間 | 復元力の動的測度 |
| **systemic load 累積率** | `p_inv2` の Heyting値増分率 | システム負担 |

これらを ASEAN10 で計算 → 4タイプ別に値の分布を見る。

---

## §8 実装方針

### 8.1 言語選定

**Python が第一候補**:
- 既存スキル流用 (MEMORYで Python 中心)
- NetworkX で Petri net 基本構造
- Heyting値拡張は自作 (簡単)
- HTML可視化 (Chart.js) との接続が容易

**AlgebraicPetri.jl は第二候補**:
- Julia 学習コスト高
- 正統な実装基盤、ただし ROI 不明
- 後で必要になったら採用

決定: **Python で自作 H-Petri Net シミュレータを実装**。

### 8.2 ファイル構成 (実装時)

```
src/
├── petri/
│   ├── __init__.py
│   ├── core.py          # H-Petri Net クラス
│   ├── heyting.py       # Heyting代数の例 (Boolean, Powerset, [0,1])
│   ├── firing.py        # 発火規則
│   ├── invariants.py    # P/T-invariant 計算
│   └── open_net.py      # Open H-Petri Net 合成
├── backbones/
│   ├── bakong.py        # Bakong 規約準拠
│   ├── gcash.py         # GCash 規約準拠
│   ├── paynow.py
│   └── kbzpay.py
├── compare/
│   ├── metrics.py       # §7 比較指標
│   └── viz.py           # HTML 出力用
└── tests/
    └── test_*.py
```

### 8.3 出力先

- 最小実装: 各 backbone の H-Petri Net をシミュレートして指標出力
- 中間: ASEAN5 (TH/SG/MY/ID/PH) のOpen Petri Net 合成
- 最終: HTML可視化 (southeast-asia-fragility に Petri net セクション追加)

---

## §9 自分で詰める論点

1. **Heyting代数 H の具体形をどう選ぶか**
   - 開始は `H = {⊥, ⊤_{priv}, ⊤_{bank}, ⊤_{pub}, ⊤}` の4段階で十分か?
   - もっと細かい連続値 (`[0, 1]`) にする?
   - 商品ごとに独立な証拠集合 `2^S` にする?
2. **3.5 タイミング値の実データ補正**
   - 各国中銀統計から取引時間データを取得
   - 規約値と実データのキャリブレーション
3. **5.3 域内決済 bottleneck 仮説の検証方法**
   - 実際の越境送金データで律速関係を確認
   - Project Nexus 公開資料の活用
4. **6.3 atomicity 数値化の方法**
   - 「強・中・弱」を量的指標に変える
   - T-invariant の集合サイズで測る方法
5. **規約の拡張性**
   - 4 backbone 以外 (CBDC、暗号資産) に拡張可能か
   - cryptocurrency をどう書くか (Pinna-Tonelli 借用)
6. **規約の boundary** (どこまで詳細にすべきか)
   - Layer C (個別取引) を展開するか、抽象のまま放置するか

---

## §10 次のアクション

### 短期 (今週)
1. Python H-Petri Net シミュレータの core モジュール実装 (`petri/core.py`)
2. Heyting代数の例実装 (`petri/heyting.py`、Boolean と {⊥, ⊤_{priv}, ⊤_{bank}, ⊤_{pub}})
3. Bakong テンプレート実装 (`backbones/bakong.py`)
4. 発火シミュレータ動作確認

### 中期 (今月)
5. GCash, PayNow, KBZPay の4タイプ全実装
6. 比較指標計算 (`compare/metrics.py`)
7. P-invariant 計算
8. Bakong vs GCash の最初の数値比較レポート

### 長期 (3ヶ月)
9. Open Petri Net 合成 (`petri/open_net.py`)
10. ASEAN5 合成シミュレーション
11. HTML可視化に Petri net セクション追加
12. atomicity 数値化アルゴリズム実装

---

## §11 ノートの位置づけ

これは notes/05 (主張5つ俯瞰) と notes/06 (Heyting値Petri net 数学) を踏まえた **実装規約**。
06 が数学、07 がフォーマット。組み合わさることで「動かせる H-Petri Net」が立つ。

次のステップは **実装** (notes/08 or src/ ディレクトリ作成)。
