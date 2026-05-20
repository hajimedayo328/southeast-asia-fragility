# Jia, Floridi, Tohmé 2025 — 圏論構造抽出

**論文**: "A Categorical Analysis of Large Language Models and Why LLMs Circumvent the Symbol Grounding Problem"
**著者**: Luciano Floridi, Yiyang Jia, Fernando Tohmé
**arXiv**: 2512.09117
**取得経路**: arxiv.org/html/2512.09117v1 (HTML版から本文を取得。PDF版は本文非公開バイナリ)
**抽出日**: 2026-05-14

---

## 論文の圏論構造マップ

### 使われている圏

**唯一の主要圏: 𝒞 ⊆ Rel** (Relの部分圏)

- **圏名**: 𝒞 (Rel内の部分2-圏)
- **対象 (objects)**: 集合として以下を採用
  - H : human epistemic situations (人間の認識状況)
  - C : human-authored content (人間が書いたコンテンツ)
  - C′ : tokenised strings (トークン化された文字列)
  - D(C′) : datasets (データセット空間)
  - G : space of trained LLMs (訓練済みLLMの空間)
  - O : LLM outputs (LLMの出力)
  - W : possible worlds (可能世界の空間)
  - Pred(W) = 𝒫(W) : propositions = Wの冪集合 (包含⊆でposet)
- **射 (morphisms)**: 集合間の二項関係 (relations)
- **何を表しているか**: コンテンツ→トークン→モデル→出力→意味、という認識・生成プロセス全体を関係の合成として圏論化したもの

### 関手 F: C_i → C_j

**論文は単一圏 𝒞 内部の射を主役にしており、外部関手は明示されていない。** 代わりに以下の「ルート (合成射)」が中心:

- **F_human (人間ルート)**: `g ∘ c : H → Pred(W)`
  - 対象: 認識状況 h ↦ 命題集合 P_human(h)
  - 意味: 人間がコンテンツを参照して意味を確定するルート
- **F_LLM (LLMルート)**: `r ∘ e ∘ i_{g_0} ∘ p : H → Pred(W)`
  - 対象: 認識状況 h ↦ 命題集合 P_AI(h)
  - 意味: 人間のプロンプト生成→固定モデルとペア→評価→意味解釈
- **F_training (訓練パイプライン)**: `t ∘ D ∘ s : C → G`
  - 意味: コンテンツ→トークン化→データセット化→訓練、でモデルが生成される

個別の射:
```
x   : H → W           (experience: 認識状況の真の世界)
c   : H → C           (consult content)
g   : C → Pred(W)     (interpret content)
p   : H → C′          (generate prompt)
s   : C → C′          (tokenise)
D   : C′ → D(C′)      (construct dataset)
t   : D(C′) → G       (train)
i_{g_0}: C′ → G × C′  (pair with fixed model g_0)
e   : G × C′ → O      (evaluate)
r   : O → Pred(W)     (assign semantics)
ρ   : Pred(W) → W     (resolve reference)
```

### 自然変換 / 2-cell

**ここが論文の最大の工夫点**:

- 通常の可換図式 (equality) を採用せず、**Entailment-Commutativity (含意可換性)** を使う
- 2-cell の構成:
  - 0-cells: 集合 (H, C′, Pred(W) 等)
  - 1-cells: 関係 R ⊆ A × B
  - 2-cells: 包含 R ⇒ S iff R ⊆ S in A × B
- 中心 2-cell:
  ```
  ∀h ∈ H,  (r ∘ e ∘ i_{g_0} ∘ p)(h)  ⊆  (g ∘ c)(h)
  ```
  → LLMルートが人間ルートに「含意される」ことが健全性 (soundness) を意味する

### Fibration / 圏の構成

- **Grothendieck construction**: 明示的には**使われていない**
- **pullback / pushout / limit / colimit**: 明示的には**使われていない**
- 代わりに**右Kan拡張 (Right Kan Extension)** が中心ツール:
  ```
  Ran_p(g ∘ c) = ⋃ { R ⊆ C′ × Pred(W) | R ∘ p ⊆ g ∘ c }
  ```
  - Pointwise: `Ran_p(g ∘ c)(c′) = ⋂_{h ∈ p^{-1}(c′)} (g ∘ c)(h)`
  - 意味: 同じプロンプトを生む全ての h における人間命題の**共通部分**(最厳しい上界) = LLMが達成できる最良の健全出力

### Heyting 代数 / 直観主義論理の使われ方

- **明示的なHeyting代数・topos・presheaf・直観主義論理は使われていない**
- ただし Pred(W) = 𝒫(W) は完備Boolean代数 (したがってHeyting代数の特例) であり、`⊆` を含意とみなす構造は自然にそこにある
- 拡張可能性として Stoch / SRel (確率的圏)、sheaf over H が言及されるのみ

### 中心定理 / 中心構成

**Proposition 2.1 (Soundness ≡ Kan extension)**

```
1. If  P_AI(h) ⊆ Ran_p(g∘c)(p(h)),  then  h ∈ H*
2. If p is injective, then  h ∈ H*  ⟹  P_AI(h) ⊆ Ran_p(g∘c)(p(h))
```

ここで `H* := { h ∈ H | P_AI(h) ⊆ P_human(h) }` (健全な状況の集合)

**一文要約**: LLMの健全性は、人間ルート `g ∘ c` をプロンプト射 `p` に沿って右Kan拡張した普遍的上界 `Ran_p(g∘c)` に LLM出力が含まれることと(injective `p` の下で)同値。

補助命題:
- **Proposition 2.2 (Knowledge condition)**: 世界レベル一致集合 `H^! := {h | W_human(h) = W_AI(h) = {w}}` 上で、出力は知識として成立する

---

## ASEAN Infra Category への転用マップ

| Jia論文の概念 | ASEAN Infra Categoryでの対応 |
|---|---|
| H (human epistemic situations) | S (ASEAN各国のインフラ需要状況 / 国×時刻) |
| C (human-authored content) | T_adv (先進国の蓄積された技術・ノウハウ) |
| C′ (tokenised strings) | T_local (現地化・モジュール化された技術仕様) |
| D(C′) (datasets) | Proj_pool (実証実験プールやパイロットプロジェクト集合) |
| G (trained LLMs) | I_built (実装済みインフラの空間: 港湾・電力網・5G等) |
| O (outputs) | Ops (運用実績データ: スループット・稼働率) |
| W (possible worlds) | F (達成され得るインフラ未来状態の空間) |
| Pred(W) = 𝒫(W) | Goal(F) (SDG / 開発目標 = Fの部分集合) |
| 人間ルート F_human = g∘c | F_advanced : S → Goal(F) (先進国がフル仕様でカバーするルート) |
| LLMルート r∘e∘i_{g₀}∘p | F_leapfrog : S → Goal(F) (途上国がモバイル決済/分散太陽光等で跳躍するルート) |
| p: H → C′ (prompt生成) | π: S → T_local (需要状況→必要な現地化仕様) |
| s: C → C′ (tokenise) | σ: T_adv → T_local (先進国技術→現地適合仕様への圧縮/翻訳) |
| t: D(C′) → G (training) | τ: Proj_pool → I_built (実証→本実装) |
| g: C → Pred(W) | γ: T_adv → Goal(F) (理論上達成可能な開発目標) |
| r: O → Pred(W) | ρ: Ops → Goal(F) (運用実績→実達成された開発目標) |
| Entailment-commutativity: AIルート ⊆ humanルート | リープフロッグ健全性: F_leapfrog(s) ⊆ F_advanced(s) (= 跳躍が標準目標を逸脱しない) |
| Right Kan extension Ran_p(g∘c) | Ran_π(γ∘ι): 「同じ現地仕様 t_local を要する全ての s で達成可能な目標の共通部分」 = リープフロッグが守るべき普遍的上界 |
| Soundness set H* | S* := {s | F_leapfrog(s) ⊆ F_advanced(s)} (= 「跳躍が標準ルートに対し健全な国・時点」) |
| World-level agreement H^! | S^! := {s | 単一未来 f が両ルートで一致して実現} (= ハードな成功事例) |
| Hallucination (∃p ∈ P_AI \ P_human) | Infra-failure: ∃ goal ∈ F_leapfrog(s) \ F_advanced(s) (= リープフロッグ特有の副作用・標準逸脱) |
| 2-cell (R ⊆ S) | 「強い達成 → 弱い達成」の被覆関係 |

---

## 転用時の論理的ギャップ (Top 5)

1. **「真理」と「達成度」の質的違い**
   Jia論文では Pred(W) の元は命題 = 真偽が世界 w で決まる 0/1。インフラの開発目標は連続的 (例: 電化率70%) で、`⊆` を単純な集合包含で扱えない。**修正**: Goal(F) を二値命題ではなく [0,1]値関手 (= Lawvere計量空間 enriched cat) に置き換える必要がある。Stoch / SRel の拡張案が論文末尾にあるのはここに対応するヒント。

2. **「同じプロンプト→同じ出力」の射構造が崩れる**
   Jia論文では `p: H → C′` が(できれば)injective であることが Prop 2.1 (2) の前提。インフラでは「同じ現地仕様 t_local が全く違う国 s で違う結果を生む」(文化・政治・気候依存) のが普通で、π は injective でないどころか強い**fiber依存**を持つ。**修正**: ここで初めて Grothendieck construction (国ごとに fiber を切る) が必要になる — Jia論文より構造を**増やす**方向。

3. **Rel という対称的圏では資源の不可逆性が表現できない**
   Jia論文の射は関係 = 対称扱い可能。インフラ建設は不可逆 (一度作った石炭火力は10年単位で固定資産)・パスデペンデント。**修正**: Rel ではなく **PROP / monoidal category with non-invertible morphisms** にする必要。あるいは時間順序を fiber 化 (S = Country × ℕ_time)。

4. **Right Kan拡張の「intersection」がインフラでは空集合になりがち**
   Pointwise定義 `Ran_π(γ)(t_local) = ⋂_{s ∈ π^{-1}(t_local)} γ(s)` は、需要が国ごとに大きく異なる場合 (例: ASEAN10カ国) に共通部分が空になりやすい。**修正**: 厳しい上界 (intersection) ではなく「多数決」「加重平均」「robust core」など、enrichedな極限に置き換える必要。これは Jia論文の枠を出る。

5. **Entailment ⊆ の方向の妥当性**
   Jia論文では「LLM ⊆ human」(AI は人間より控えめが健全) は LLM の幻覚抑制という文脈に固有。**インフラでは逆**: リープフロッグの価値は「先進国ルートでは達成不可能なゴール (例: 銀行支店ゼロでのモバイル決済普及) を達成すること」にあり、`F_leapfrog ⊆ F_advanced` を要求すると**リープフロッグの本質を消す**。**修正**: 2-cell の向きを再考し、「LLM/leapfrog が human/advanced と**両立可能**(共通の coarsening が存在する)」程度に緩める必要。これは概念的に最も大きいギャップ。

---

## 補足: 取れなかったもの・推測ベースの部分

- PDF版は binary stream で取得失敗 (797KB, 本文非展開)
- HTML版から本文構造を取得 (Section 2 "Categorical Framework", Appendix A "Category Theory and Rel" のあることは確認済み)
- Heyting代数/topos/Grothendieck構成は HTML版抽出時点で「使われていない」と判断。これは Floridi系の哲学論文として一致する (Floridi はLevels of Abstractionが本業で、SGA級の構成は使わない傾向)
- Section 7 の内容は HTML 抽出で取りこぼした可能性あり。将来必要になったら src/2512.09117 (TeX) からの再取得を推奨
