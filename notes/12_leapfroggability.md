# 12. Leapfroggability の厳密化 — R-Restricted Reachability

**作成日**: 2026-05-21
**ステータス**: draft v1
**位置づけ**: notes/05 主張1 (リープフロッグ = reachability) の数学的厳密化。アルゴリズム化と計算可能性。

## §1 動機

これまで「リープフロッグ可能性」を雰囲気で扱ってきた:
- notes/02: 平行射の2-cell
- notes/06 §5.3: R-restricted reachability
- notes/08, 09: 関手 + 自然変換

本ノートで **形式定義 + 計算可能性 + アルゴリズム** を完成させる。
これで「Bakong reachability」を Python で計算できる状態になる。

---

## §2 形式定義

### 2.1 標準 Reachability

P/T Petri net `N = (P, T, F, M_0)` の reachability:
```
R(N, M_0) = { M | ∃ σ ∈ T*. M_0 →σ M }
```

これは古典的に EXPSPACE-complete (Mayr 1981, Czerwinski 2019)。

### 2.2 R-Restricted Reachability (本プロジェクト独自)

部分マーキング `R ⊂ P` (例: 「先進国経路」の場所) について:

```
R^{≠}-reach(N, M_0, M_target) = ∃ σ = t_1...t_n s.t.
  - M_0 →σ M_target  (普通の到達可能性)
  - ∀i. pre(t_i) ∩ R = ∅   (σ が R を経由しない)
```

つまり「`R` の場所を一切使わずに `M_0` から `M_target` に達する遷移列」が存在するか。

### 2.3 リープフロッグ可能性の定義

機能 `X` (`M_target` で表現) について:
```
リープフロッグ可能(X) ⇔ R^{≠}-reach(N, M_0, M_target) is True
```

ここで `R` = 「先進国経路の場所集合」(例: BankAccount, ATM, Wire)。

### 2.4 例: Pay (送金)

- `M_target` = (RecipientWallet has tokens)
- `R = {BankAccount, ATM, Wire}` (先進国経路)
- 求める: `R` を一度も経由せずに RecipientWallet にトークンを入れる発火列

これに「SIM → MobileMoney → Recipient」経路があれば、リープフロッグ可能。

### 2.5 例: Light (照明)

- `M_target` = (LightOn token)
- `R = {Grid, WiredDistribution}` (先進国経路)
- 求める: `R` を経由せずに LightOn に達する発火列

ただし「Solar → Microgrid → LightOn」経路でも **Power のような中間ノードを共有** する場合、`R` から `Power` を除外したかどうかで結果が変わる。

→ **何を `R` に入れるか** が定義の鍵。

---

## §3 計算可能性

### 3.1 Naive Algorithm

```
def is_leapfrog_possible(net, M_0, M_target, R):
    queue = [(M_0, [])]  # (marking, transition_history)
    visited = set([tuple(M_0.visible.items())])
    while queue:
        M, hist = queue.pop(0)
        if M_target_satisfied(M, M_target):
            return True, hist
        for t in net.transitions:
            if t.pre_set & R: continue  # R を経由する遷移はスキップ
            if not enabled(net, M, t): continue
            M_new = fire(net, M, t)
            key = tuple(M_new.visible.items())
            if key not in visited:
                visited.add(key)
                queue.append((M_new, hist + [t]))
    return False, None
```

複雑度:
- 一般 Petri net: EXPSPACE
- bounded Petri net (容量制限): PSPACE
- 本プロジェクト想定: 5-10 場所、10-20 遷移、bounded → 多項式時間で十分

### 3.2 性質

**Proposition 3.1**: R-restricted reachability は通常の reachability の **special case**:
```
R^{≠}-reach(N, M_0, M_target) ≡ reach(N|_{T \ T_R}, M_0, M_target)
```
ここで `T_R = {t ∈ T | pre(t) ∩ R ≠ ∅}` (R を経由する遷移を全部除いたサブネット).

つまり R-restricted reachability は **「R 経由遷移を削除した部分 Petri net 上の通常 reachability」** と同値。

**Corollary 3.2**: R-restricted reachability は、通常の reachability と **同じ計算複雑度**。
標準アルゴリズム (Mayr 1981 等) をそのまま転用可能。

### 3.3 H-Petri Net の場合

H-Petri Net (可視層 + 不可視層) でも:
- 発火可能性は可視層だけで決まる (notes/06 §4.2)
- 不可視層は monotone に変化するだけ
- → **R-restricted reachability は可視層だけで判定可能**

不可視層は「到達後の Heyting値の状態」を見るだけ。

---

## §4 ASEAN 実例: Bakong reachability

### 4.1 Bakong での R-restricted reachability

Bakong は中央銀行型なので、「先進国経路」は何か?
- 先進国経路 = `R = {NBCBackbone}`? とすると、Bakong 自体がリープフロッグ不可能になる
- 別の解釈: `R = {Bank の物理支店}` のような **古い物理ノード**

この場合:
- M_target = 受取人ウォレットへの送金完了
- R = 物理支店ノード
- 答え: 可能 (Bakong は支店なしで動く)

### 4.2 GCash で同じ計算

- 同じ M_target
- 同じ R = {物理支店}
- 答え: 可能 (GCash も支店なし)

### 4.3 比較

- **Bakong**: `R^{≠}-reach = True` (リープフロッグ可能)
- **GCash**: `R^{≠}-reach = True` (リープフロッグ可能)

両者ともリープフロッグ可能だが、**何をリープフロッグしてるかが違う**:
- Bakong: 物理支店 + 民間プラットフォーム 両方をスキップ
- GCash: 物理支店をスキップ、民間プラットフォームに依存

→ R を何に取るかで、リープフロッグの「深さ」を測れる。

---

## §5 Python 実装方針

src/h_petri/leapfrog.py として実装:

```python
from h_petri.core import HPetriNet, Marking, fire, enabled

def r_restricted_reachable(
    net: HPetriNet,
    M_start: Marking,
    M_target_predicate,
    forbidden_places: set[str],
    max_steps: int = 100,
) -> tuple[bool, list[str] | None]:
    """R-restricted reachability check via BFS."""
    visited = set()
    queue = [(M_start, [])]
    while queue:
        M, hist = queue.pop(0)
        if M_target_predicate(M):
            return True, hist
        if len(hist) >= max_steps:
            continue
        key = tuple(sorted(M.visible.items()))
        if key in visited:
            continue
        visited.add(key)
        for t in net.transitions:
            pre = net.pre_visible(t)
            if set(pre.keys()) & forbidden_places:
                continue
            if not enabled(net, M, t):
                continue
            queue.append((fire(net, M, t), hist + [t]))
    return False, None
```

これで Bakong / GCash の R-restricted reachability が即計算可能。

---

## §6 高度な議論 — Categorical Leapfroggability

### 6.1 R-restricted reachability の圏論的解釈

`R` を場所 subcategory として見ると:
- `Petri(N)`: N の遷移を射とする圏
- `Petri(N|_{¬R})`: R を除いた部分圏
- R-restricted reachability = `Petri(N|_{¬R})` での通常 reachability

これは **functor restriction** とも見える:
```
i*: Petri(N) → Petri(N|_{¬R})  (forgetful functor)
```

リープフロッグ可能性 = `i*` の image における reachability.

### 6.2 2-categorical formulation

notes/09 で見た 2-category の言葉で:
- F_legacy : 𝓒_CPN → Cat_HPN (先進国経路を含む)
- F_leapfrog : 𝓒_CPN → Cat_HPN (先進国経路を経由しない)
- リープフロッグ可能 ⇔ **自然変換 `F_legacy ⇒ F_leapfrog` が存在し、かつ F_leapfrog が `R = ∅` の制約を満たす**

→ リープフロッグ可能性 = 2-category の中での自然変換存在問題に帰着。

---

## §7 自分で詰める論点

1. **§4.1 R の選び方**:
   - 「先進国経路」を場所集合として明示する手法
   - 業界レポート + 歴史的経路から導出
2. **計算可能性のtight bound**:
   - 5場所5遷移なら多項式時間で済むことの確認
   - bounded Petri net の reachability の文献調査
3. **Heyting値層の reachability**:
   - 不可視層の Heyting値変化を含めた reachability
   - 「TrustHub が ⊤_pub に到達するか」というクエリ
4. **2-categorical leapfroggability の universal property**:
   - terminal な leapfrog 関手の存在
   - 「最も深いリープフロッグ」の特性化
5. **量的測度**:
   - 「リープフロッグの深さ」を数値化
   - 例: |R| / |P| で測る、または BFS の最短経路長で測る

---

## §8 まとめ

主張1 (リープフロッグ = reachability) は:
- 数学的に厳密に書ける (R-restricted reachability)
- 計算可能 (BFS で実装可能)
- ASEAN モバイル金融に直接適用可能
- 2-categorical にも自然変換存在問題として書ける

これで主張1の **理論 + アルゴリズム + 実装方針 + 圏論的解釈** が揃った。

次は monoidal 2-category 拡張 (notes/13)。
