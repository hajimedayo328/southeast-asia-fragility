# 09. Heyting × Petri net 再徹底サーベイ

検証目的: 「Heyting代数を coefficient とする Petri net」の研究が既存に存在するかを、前回 (06) で「ゼロ」と判定した結論を 8 つの「逃げ場」を全て潰すことで再検証する。

検索ツール使用回数: WebSearch 12回 + WebFetch 3回 = 15回

## 最終判定: **空白 (Heyting coefficient Petri net は存在しない)**

ただし「Heyting に隣接する代数 (lineale / quantale / Petri algebra / residuated lattice / MV-algebra)」を coefficient とする研究は豊富。Heyting **そのもの** を coefficient に据えて token game を定義した論文は発見できなかった。

---

## 各「逃げ場」の確認結果

| # | 逃げ場 | 結果 | 根拠 |
|---|--------|------|------|
| 1 | intuitionistic logic ベースの Petri net | ✗ Heyting でない | Engberg-Winskel (1990, 1993) は intuitionistic **linear** logic で、semantics は Quantale。Heyting ではない。 |
| 2 | complete lattice valued Petri net | △ Petri algebra として存在するが Heyting に限定されない | Badouel-Chenou-Guillou (ICALP 2005) "Petri Algebras" = lattice-ordered commutative group の positive cone。Heyting は含まれない (Heyting は群でない) |
| 3 | fuzzy Petri net (Heyting 互換?) | ✗ | Atanassov の Intuitionistic Fuzzy Petri Net (IFPN; Meng-Lei 等) は名前に "intuitionistic" を含むが、Atanassov の "intuitionistic" は誤称で Heyting と数学的に異なる (Dubois et al. 2005 が terminological critique を明示)。Heyting Brouwer 否定を満たさない |
| 4 | topos-theoretic Petri net | ✗ 空白 | Baez "Open Petri Nets", Master-Patterson 系の categorical Petri net 群、Topos Institute (multimodal Petri net) は double category / monoidal category 路線。**topos の internal Heyting algebra を coefficient に据えた研究は発見できず** |
| 5 | Petri net + presheaf | △ presheaf 表現はあるが Heyting 視点なし | Bruni et al. の coalgebraic semantics, "Whole-grain Petri nets" は presheaf category への faithful embedding を提示するが、presheaf topos の Heyting 構造を coefficient として陽に使う研究なし |
| 6 | 古典論文 (Engberg-Winskel, Brown-Gurr) の前提 | ✗ | Brown-Gurr (1990s) は dialectica で {0,1} = Boolean。de Paiva 等の拡張も lineale = symmetric monoidal closed poset。Heyting は lineale の **特殊例 (Example 2.8 で 2 値 case が登場)** にとどまり、一般の Heyting 代数を coefficient とした構成は無い |
| 7 | applied category theory 最新 (2024-2026) | ✗ | Lavore-Leal-de Paiva "Dialectica Petri Nets" (arXiv 2105.12801, 2025 published) は lineale 路線を更に拡張するが、Heyting は明示的に区別され「lineale の internal-hom は Heyting implication と異なる (a⊸b ≠ ¬(b→a))」と注記。Petri Nets 2025 (Paris) proceedings にも Heyting Petri net 系発表なし |
| 8 | Origami × Petri net (Jia 2024 路線) | ✗ 完全に空白 | Jia-Mitani 2024 "Heyting Algebra in Flat Origami" は origami の partial folding state が Heyting algebra になることを示すが、Petri net との交差は皆無。Origami × Petri net 自体も非常に少数 |

---

## 最重要発見 Top 3

### 1. **Badouel-Chenou-Guillou (2005) "Petri Algebras"** (ICALP, LNCS 3580)
- URL: https://www.irisa.fr/s4/download/papers/Badouel-et-al-ICALP05.pdf
- 「Petri algebra = residuated commutative monoid」を定義し、これは正確には「lattice-ordered commutative group の positive cone」に一致 (= 自由可換モノイドの一般化)。
- **Heyting algebra は群ではない (差し戻し不能性) ため Petri algebra ではない**。
- ただし bounded Petri algebra は MV-algebra で reformulate でき、Gödel MV-algebra (= 線形順序 Heyting) との距離は近い。**「Heyting に最も近い既存 Petri net 一般化」**。
- 違い: Petri algebra は「資源の量」を表現する linear/additive な構造。Heyting は「真偽の度合 (順序+蘊含)」を表す idempotent 構造。**両者は等冪性で本質的に分かれる**。

### 2. **de Paiva-Lavore-Leal (2025) "Dialectica Petri Nets"** (arXiv 2105.12801)
- URL: https://arxiv.org/html/2105.12801v5
- Petri net の transitions を **lineale** で重み付け。lineale の例として ℕ, ℤ, [0,1], 3-valued Kleene などを列挙。
- **Heyting algebra は lineale の特殊ケースとして「触れている」が、coefficient として中心的には扱っていない**。むしろ「Heyting implication と lineale の internal-hom は別物」と明示的に区別 (Example 2.8 周辺)。
- 関連: de Paiva-Syropoulos (2020) "Dialectica Fuzzy Petri Nets" (arXiv 2003.04712) は [0,1] を lineale 化。これも Heyting でなく Łukasiewicz/MV 系。

### 3. **Meng-Lei "Intuitionistic Fuzzy Petri Nets" (IFPN)** (Atanassov 系)
- URL: semanticscholar.org/.../fc734a6defffb146e24cc8713d55c297ed1a25a5
- 名前は紛らわしいが Atanassov intuitionistic fuzzy set = (membership μ, non-membership ν) の pair で μ+ν ≤ 1 を要求。
- **Dubois et al. (Fuzzy Sets and Systems 2005) が "intuitionistic" の用語誤用を批判**。Atanassov 否定は Brouwer 否定の矛盾律を満たさず、強二重否定や De Morgan 一方を持つため、Heyting と本質的に別物。
- → IFPN は「Heyting Petri net」と誤解されやすいが、**数学的には完全に別物**。この混同は要注意で、論文を書くなら明示的に区別すること。

---

## Fuzzy Petri net との関係 (詳細整理)

| Fuzzy Petri net の variant | Coefficient 代数 | Heyting? |
|---|---|---|
| Cardoso 系 classical fuzzy PN | [0,1] with min/max (Gödel t-norm) | 部分的に Heyting 互換 (Gödel algebra は線形 Heyting) |
| Looney 系 | [0,1] with various t-norms | 大半は MV/Łukasiewicz で Heyting でない |
| Dialectica Fuzzy PN (Paiva-Syropoulos 2020) | [0,1] as lineale | Heyting でない (lineale internal-hom ≠ Heyting →) |
| Intuitionistic Fuzzy PN (Atanassov 系) | (μ, ν) pair | **Heyting でない** (誤称) |

→ **Gödel t-norm fuzzy PN** が最も Heyting に近いが、これも「Heyting algebra を陽に coefficient と宣言した研究」ではなく、結果的に Gödel = 線形 Heyting に乗っているだけ。「一般の (非線形な) Heyting algebra で markings を valued する Petri net」は存在しない。

---

## Topos-theoretic Petri net

### 既存ある? → **狭義では No (空白)**

- Baez "Open Petri Nets" (2018-2022): 圏 Petri を Sets 上で構成し double category で open化。**topos 内には移していない**。
- Master-Patterson 系 (UC Riverside / Topos Institute): symmetric monoidal double category 路線。topos の internal Petri net は提案されていない。
- "Whole-grain Petri nets" (Kock 2020, arXiv 2005.05108): polynomial functor で presheaf 表現するが、これは presheaf category を「使う」だけで「Petri net を topos 内に定義する」ものではない。

### 独立貢献候補

**「elementary topos E 内の Petri net」を定義する研究は発見できなかった**。具体的には:
- 場所 P, 遷移 T を E の object とする
- coefficient として subobject classifier Ω (= internal Heyting algebra) で重み付け
- marking を Ω-valued function P → Ω として定義
- firing rule を internal Heyting 構造 (∧, →) で書く

この方向性は **完全にオープン**。卒論・研究の独立貢献として成立する可能性が高い。

---

## まとめ: 独立貢献ポイント

1. **Petri algebra (Badouel 2005) は群ベースで Heyting を排除している** → 「等冪な (= 群でない) coefficient での Petri net」は理論的に未開拓
2. **Dialectica Petri net (Lavore-Leal-de Paiva 2025) は lineale で一般化したが Heyting を明示的に避けている** → 「lineale でなく Heyting frame を coefficient とする」ことの意味論的差異は未論述
3. **Atanassov 系 IFPN との混同を整理する論考** だけでも価値がある (用語整理 + 数学的差異の明示)
4. **Topos 内 internal Petri net + Ω-valued marking** は完全空白
5. Origami の Heyting (Jia 2024) と Petri net を繋ぐ研究は皆無 → Mitani 研究室との接点を活かせば希少な交差領域になる

→ **「Heyting Petri net」を正面から定式化する論文は存在しない**。前回 06 の結論を **強化** する形で再確認した。

---

## 参照 URL

- https://arxiv.org/html/2105.12801 (Dialectica Petri Nets)
- https://www.irisa.fr/s4/download/papers/Badouel-et-al-ICALP05.pdf (Petri Algebras)
- https://arxiv.org/abs/2003.04712 (Dialectica Fuzzy Petri Nets)
- https://www.semanticscholar.org/paper/Linear-Logic-on-Petri-Nets-Engberg-Winskel/7c53f5362fac876575a3bc75b6fc197a69203f32 (Engberg-Winskel)
- https://johncarlosbaez.wordpress.com/2019/10/06/quantales-from-petri-nets/ (Baez quantales)
- https://www.appliedcategorytheory.org/adjoint-school-act-2020/dialectica-categories-of-petri-nets/ (Brown-Gurr-de Paiva 系)
- https://arxiv.org/pdf/1808.05415 (Baez Open Petri Nets)
- https://pphmjopenaccess.com/index.php/jpjana/article/view/1938 (Jia-Mitani Heyting Origami)
- https://www.semanticscholar.org/paper/Intuitionistic-Fuzzy-Petri-Nets-for-Knowledge-and-Meng-Lei/fc734a6defffb146e24cc8713d55c297ed1a25a5 (Atanassov IFPN)
- https://www.irit.fr/publis/ADRIA/DPetal047.pdf (Dubois et al., Atanassov "intuitionistic" 誤称批判)
- https://petrinets25.github.io/web/ (Petri Nets 2025 Paris)
- https://arxiv.org/pdf/2005.05108 (Whole-grain Petri nets, Kock)
