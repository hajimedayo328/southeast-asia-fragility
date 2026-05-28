# 24. モナド (Monad) で「便利の副作用」を圏論的に書く

**作成日**: 2026-05-25
**ステータス**: draft v1
**位置づけ**: 「便利と不可視コストの随伴 L⊣R」を **モナド** として書き直す。
これは notes/02, 08 の adjunction より一段強い構造。
プログラミング言語の effect system (Haskell IO, State monad) と **完全に同型**。

## §0 これが既存notesに書いてない理由

notes/02-23 は随伴 L⊣R までは書いた。だがモナドまで降りてない。
モナドは「随伴から自然に出る」けど、本プロジェクトでは:
- adjunction = ペアの存在
- monad = 副作用の **連鎖と合成** が構造的に保証される

この一歩を書くと、「便利の暴走 = モナド合成の暴走」が categorical に出る。
これは本プロジェクトに **真に新規な視点**。

---

## §1 モナドの定義 (最小)

圏 𝓒 上のモナドは三つ組 `(T, η, μ)`:
- `T: 𝓒 → 𝓒` 関手 (= 副作用付き計算をくるむもの)
- `η: id ⇒ T` 自然変換 (= 副作用なしで値を入れる: unit)
- `μ: T ∘ T ⇒ T` 自然変換 (= 副作用を平坦化する: multiplication)

3つの法則:
- 結合律: `μ ∘ Tμ = μ ∘ μT`
- 単位則: `μ ∘ Tη = μ ∘ ηT = id`

直感: モナドは「**副作用を持つ計算を関数として書くための型変換**」。

### 代表例

| モナド T | 何をくるむか |
|---|---|
| `Maybe` | 失敗の可能性 |
| `List` | 複数候補 |
| `IO` | 外界との入出力 |
| `State s` | 隠れた状態の読み書き |
| `Writer w` | ログ累積 |
| `Reader r` | 環境への依存 |

特に **Writer モナド** が本プロジェクトの「不可視コスト累積」と同型構造を持つ (詳細 §3)。

---

## §2 随伴 → モナド の関係

任意の随伴 `L ⊣ R: 𝓓 ⇄ 𝓒` から、モナド `T = R ∘ L` が自然に出る:
- `η: id_𝓒 ⇒ R∘L` = adjunction の unit
- `μ: R∘L∘R∘L ⇒ R∘L` = `R·ε·L` (counit を挟む)

→ **本プロジェクトの随伴 L⊣R (notes/02, 08) からは、自動的にモナド T が出る**。
この T が「便利の副作用」を表すモナド。

---

## §3 H-Petri Net のモナド版

### 3.1 Writer モナドとの同型

本プロジェクトの不可視場所 (TrustHub, SystemicLoad) は、各遷移発火時に Heyting値が **累積** する。
これは Haskell の `Writer w` モナドと **完全に同型**:

```haskell
-- Haskell Writer モナド
newtype Writer w a = Writer { runWriter :: (a, w) }

-- a = 計算結果, w = ログ (Monoid 構造)
```

本プロジェクト:
```
H-Petri Net の発火 = Writer H (Visible Marking)
  visible value (a) = 可視層のマーキング
  log (w)            = 不可視層の Heyting値累積
```

`w` の Monoid 構造は Heyting代数の `∨` で成立する。

### 3.2 Kleisli 圏

Writer モナドの Kleisli 圏 `Kleisli(Writer H)`:
- 対象: 通常の対象
- 射: `f: a → (b, h)` (h は副作用 Heyting値)

合成:
- `(f >>= g)(a) = (b', h_f ∨ h_g)` where (b, h_f) = f(a), (c, h_g) = g(b)

→ **2つの便利な操作を合成すると、副作用が自動的に ∨ で合体する**。
これは Petri net 発火列の不可視場所更新規則 (notes/06 §4.2) と **完全一致**。

### 3.3 副作用累積の順序非依存性 (既知の半束性質)

**命題 (新規定理ではない — Heyting代数の ∨ が有界半束であることの直接の帰結)**:
任意の Kleisli 射の合成 `f_n ∘ ... ∘ f_1` の副作用は:
```
total_effect = h_1 ∨ h_2 ∨ ... ∨ h_n
```
であり、これは `∨` の **結合性・可換性・冪等性**から **計算順序に依存しない**。

→ 「便利な計算を何回繋いでも、副作用は monotone に累積する」が **構造的に保証**される。
逃げ場なし。

⚠️ **注意**: これを当初「Effect Accumulation Theorem」と呼んでいたが、内容は半束(join-semilattice)の
標準的な性質そのものであり、新しい定理ではない。本プロジェクトの貢献は「副作用累積を Writer H モナドとして
**書ける**」という枠組み側であって、∨ の順序非依存性自体は既知。実装 (`src/h_petri/monad/writer_h.py`) は
この既知性質を 720 順列で確認するデモ。

---

## §4 「便利の暴走はモナド合成の暴走」

### 4.1 直感

各「便利な遷移」`t_i` は Writer モナド射:
```
t_i: State → (State', cost_i)
```

ユーザーが便利を **連鎖** すると:
```
result = (t_n ∘ ... ∘ t_1)(initial)
       = (final_state, cost_1 ∨ cost_2 ∨ ... ∨ cost_n)
```

→ 副作用 cost が **monotone に積み上がる**。
これは:
- 物理学の **エントロピー増加** (第二法則)
- プログラミングの **副作用ログ** (Writer monad)
- 経済学の **externality 累積** (環境破壊)

すべて同じ構造。

### 4.2 実例: Cloudflare 2025-11

```
ユーザー視点:
  t1: ChatGPT に質問 → Cloudflare 経由
  t2: Claude に質問 → Cloudflare 経由
  t3: Sora に動画生成 → Cloudflare 経由

各 t_i の副作用:
  cost_i = "Cloudflare依存度 +ε"

合成後:
  total_dependency = ε ∨ ε ∨ ε ... (累積)
```

そして Cloudflare 2025-11 障害発火:
```
recover: state → (state', large_negative_visibility)
```

= 「累積してた依存が一気に表面化」。Writer モナドのログが **暴露される瞬間**。

### 4.3 賈先生 LLM論文との直結

Jia-Floridi 2025 の中心ツール = Kan拡張 (= adjoint pair の特殊形)。
Kan拡張は **モナドを生成する** (Day convolution など)。

→ **本プロジェクトのモナド T は、賈先生のLLM圏論ツールセットの中で自然に位置する**。
これが「賈先生研究の流儀そのまま」と言える根拠。

---

## §5 effect system との橋渡し

プログラミング言語研究 (Plotkin-Power 2003 "Algebraic Operations and Generic Effects"):
- 計算効果 (副作用) を **代数演算** として扱う
- IO, State, Exception, Continuation 等
- これは monad の一般化 (effect handler)

本プロジェクトとの対応:

| Plotkin-Power 系 | 本プロジェクト |
|---|---|
| effect operation | 便利な遷移 |
| effect handler | backbone (中銀型/民間型...) |
| handler の合成 | Petri net 合成 (⊗ or ▷) |
| pure computation | 不可視コスト ⊥ の遷移 |
| effect propagation | Heyting値の monotone 累積 |

→ **「経済」と「プログラミング言語理論」が同じ構造**を持つ。
これは異分野同型 (notes/18) の新しい例。

---

## §6 マシン学習との接続 (おまけ)

ニューラルネットワークの **勾配累積** も Writer モナド構造:
- forward pass = 計算 (visible)
- gradient = 副作用 (invisible、累積)
- backward pass = Writer モナドの runWriter

→ **本プロジェクトのフレームワークは、AI研究にも転用可能** な強度。
これが notes/18 の異分野同型を更に強化する具体例。

---

## §7 自分で詰める論点

1. **§3.1 Writer モナドとの同型の厳密証明**
   - H-Petri Net の発火が `Writer H` の `>>=` と等価であることを構成的に
2. **§3.3 効果累積定理の証明**
   - Monoid 結合性からの直接導出
3. **§4 Cloudflare 2025-11 を Writer モナドで書ききる**
   - Python 実装 (`Writer H` 型を実装、各 t_i を Kleisli射として)
4. **algebraic effect handlers (Plotkin-Power) との関係**
   - Eff言語、Koka言語の handler構文との同型確認
5. **モナド変換子 (monad transformer)** で複数 backbone の合成を書く
   - `Writer H` + `State` + `Reader` の composition

---

## §8 まとめ

本プロジェクトの不可視コストは:
- **adjunction** (notes/02) では「ペアの存在」止まり
- **モナド** で書くと「**副作用の累積と合成則** が構造的に保証される」
- 具体的に `Writer H` モナド (H は Heyting代数)
- これはプログラミング言語の effect system と同じ枠組み

新しい主張:
> **「便利の暴走 = Kleisli圏での合成が制御不能になる現象」**

これは notes/02-23 のどこにも書いてない、本物の新規視点。

実装は `src/h_petri/monad/writer_h.py` として可能 (次フェーズ)。
理論は本ノートで一旦完成。
