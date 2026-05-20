# Gibb et al. 2023 Nature Communications — 構造抽出メモ

## 重要訂正

**ユーザー指定の「Bui et al. 2023」は誤り**。正しくは **Gibb et al. 2023, Nature Communications**。
著者リスト22名中に「Bui」姓は存在しない。ベトナム人共著者は Phan, Vu, Do, Nguyen, Vien, Ly, Tran 姓のみ。
ただし論文の内容（ベトナム dengue × インフラ × 人流 × 気候の3-4層解析）は完全に一致するため、
本書ではこの論文を抽出対象として確定する。

- **正式タイトル**: Interactions between climate change, urban infrastructure and mobility are driving dengue emergence in Vietnam
- **DOI**: 10.1038/s41467-023-43954-0
- **発表**: 2023年12月12日 Nature Communications 14:8179
- **URL**: https://www.nature.com/articles/s41467-023-43954-0
- **PMC**: https://pmc.ncbi.nlm.nih.gov/articles/PMC10713571/
- **GitHub**: https://github.com/rorygibb/dengue_vietnam_ms (R 98.6%)
- **コード DOI**: 10.5281/zenodo.10159288

---

## 論文構造マップ

### 多層的データ層の構成（注: 著者は「multilayer network」とは呼んでいない）

論文は厳密には **多層ネットワーク解析ではなく Bayesian 階層回帰**である。
ただしカテゴリ理論的視点で見れば、以下の4ファイバーを共有ベース（district × month）上に貼った
**fiber bundle 構造**として再解釈可能。

| 層 | ノード単位 | 内容（covariates） | データソース | 期間/解像度 |
|----|-----------|------------------|--------------|------------|
| L1: 疫学 (response) | district × month | dengue 月次症例数 Yi,t ~ NegBinom(μ, n) | ベトナム保健省 GDPM (Phan Trong Lan 経由) | 1998–2020 月次 |
| L2: 気候 | district × month | Tmean, Tmin, Tmax, 月降水量, SPEI-1/SPEI-6（干ばつ指数）, lag 0–6ヶ月 | ERA5-Land, WFDE5 v2.1, SPEI R package | 1981–2020（参考期間込み） |
| L3: 都市インフラ | district × year | piped/borehole 水道カバー率, 屋内/屋外水洗トイレ率, 建築地被覆率, 10年間都市拡大率 | ベトナム国勢調査 2009, 2019（線形補間/外挿） | 2009 & 2019, 補間 |
| L4: 人流 (mobility) | district & district-pair | road traffic km/人/年, 重力モデル人口フロー, radiation model フロー | 統計局省レベル年次 + parameter-free gravity/radiation | 年次, 計算ベース |

**重要**: 実測 mobility データは省レベル交通量のみ。district 間ペアごとの人流は重力/放射モデルで「予測」している（Facebook Data for Good 等の真の OD データは未使用）。

### 層間結合
- L1 (response) ← L2, L3, L4 (全 covariates が同じ Negative Binomial 回帰に入る形で結合)
- L2 (気候) と L3 (インフラ) の **interaction term** が明示的に検証されている: 「水道カバー率が高い地区では干ばつ→デング感染増の効果が緩和される」（中心知見の一つ）
- L4 (人流) と L2 (気候) も interaction: 北部亜熱帯では人流が dengue 拡散の主要ドライバー、南部熱帯では気候が支配的

### 解析手法
- **Bayesian hierarchical model** (INLA を想定)
- **Random effects**: province-specific monthly seasonality + dengue-year-specific district-level Besag-York-Mollié (BYM) spatially structured + unstructured 効果
- **Block cross-validation** で予測力を評価
- **ネットワーク科学手法は未使用**: centrality, community detection, percolation, GNN いずれも論文中に登場しない
- mobility は「ネットワーク」というより回帰の covariate として扱われる

### データソース（公開状況）
- **疫学**: 4省（Ha Noi, Dak Lak, Khanh Hoa, Dong Nai）のみ部分公開。全国データは Phan Trong Lan (phantronglan@gmail.com) 経由でリクエスト
- **気候**: 完全公開（ERA5-Land, WFDE5）
- **国勢調査**: 公開（GSO Vietnam）
- **交通**: GSO Vietnam 省レベル年次統計

### 中心知見（数値ベース）
1. **気温が支配的要因**: 1950年以降の温暖化で dengue 感染リスクが特に Ha Noi・南中部沿岸で拡大
2. **「都市病」仮説の否定**: 罹患率はインフラ整備が中間レベルの transitional landscape で最大化（フル都市化地区では低下）
3. **水供給インフラの mitigation 効果**: 改良水道カバー率が高い地区では長期干ばつ → dengue 増効果が緩和される（ただし極端条件下では不十分）
4. **mobility の地域依存性**: 北部亜熱帯では人流ドライバー、南部エンデミック地域では気候ドライバー

### 空間スケール・期間
- **行政単位**: district (huyện) レベル、ベトナム全国
- **district 数**: 論文中の明示数値は WebFetch では取得不可（要 PDF 直接確認）。ベトナム全国 district は概ね 700前後
- **期間**: 1998年1月〜2020年12月（23年、276ヶ月）
- **政府協力**: General Department of Preventive Medicine, MOH（Phan Trong Lan）が共著として参画

---

## 転用マップ（→ ASEAN Infra Category への対応）

| Gibb 2023 | ASEAN Infra Category (圏論的 fibration 視点) |
|-----------|---------------------------------------------|
| L1 dengue 症例 (district × month) | **観測ファイバー Obs**: ベース圏 Region × Time 上の値層 |
| L2 気候 (ERA5-Land) | **環境ファイバー Env**: 気温・降水を section とする |
| L3 都市インフラ (水道・衛生) | **物理インフラ層 Phy**: ASEAN カテゴリの中核（電力/通信/水/交通）の一部 (水セクター) |
| L4 mobility (重力モデル + 交通量) | **移動機能層 Move**: 関手 Move: Region × Region → Flux |
| BYM spatial random effect | **空間隣接圏**: ベース Region のトポロジー（隣接グラフ）を符号化 |
| 月次 seasonality random | **時間ファイバー Time**: 季節周期を section とする |
| Climate × Infra 交互作用項 | **層間 natural transformation**: η: Env ⇒ Phy⊗Env（水道が干ばつ→感染を mediate） |
| Block cross-validation | **層分解の妥当性検証**: ファイバーごとに残差を評価 |

---

## 転用ギャップ（重要、5個）

1. **「multilayer network」と明言していない**
   著者は重力モデル・回帰の covariate として人流を扱うのみで、layer-coupling tensor や interconnected adjacency matrix を構築していない。
   → ユーザーが圏論的 fibration として転用する際は「**我々がポスト処理で多層ネットワーク化する**」という再解釈レイヤーが必要。

2. **mobility が実測でなくモデル予測値**
   district 間人流は重力/放射モデルから「計算」しており、真の OD 行列ではない。Facebook Data for Good や Grab / Be データを統合できれば精度が大幅向上する。
   → ベトナム派遣時に「実測 mobility 入手の交渉」が研究貢献として大きい。

3. **物理インフラが水道・衛生のみ**
   ASEAN Infra Category で想定する電力・通信・交通・物流の網羅性に対し、本論文は dengue 関連の水セクターに特化。電力・通信網との結合は未検証。
   → 別データソース (World Bank, Vietnam EVN, MIC) を追加で組む必要あり。

4. **空間解像度が district 単位（≈ 700ノード）**
   commune (xã, ≈11,000) や grid 1km レベルではない。ASEAN 全体に拡張する際、隣国（Lao, Cambodia, Thailand）と district 定義が揃わない問題。
   → fibration として ASEAN 共通ベース圏を定義するなら GADM や HDX の admin level を揃える必要あり。

5. **ネットワーク科学指標が未計算**
   centrality, modularity, persistent homology 等はゼロ。著者の関心は疫学であり、トポロジカル不変量への興味は薄い。
   → 既存データに対しネットワーク解析を後付けする「**圏論的補完研究**」として位置付けられる。卒論ネタとして高い独自性。

---

## ベトナム派遣準備メモ（2027年夏に向けて）

### 再現に必要なデータ・申請
| データ | 取得方法 | 難易度 |
|-------|---------|--------|
| 全国 district 月次 dengue 症例 | MOH Phan Trong Lan (phantronglan@gmail.com) にメール申請 | 中（共著者経由で紹介可能性） |
| 気候 ERA5-Land | Copernicus CDS（無料） | 低 |
| 国勢調査 (2009, 2019, 2024) | Vietnam GSO 公開データ | 低 |
| 真の mobility (Grab/Facebook) | Data for Good 申請 or 現地企業折衝 | 高 |
| 電力・通信網トポロジー | EVN, VNPT への研究協力打診 | 高 |

### 著者コンタクト戦略
- **Rachel Lowe (last author)**: BSC-CNS（バルセロナスーパーコンピューティングセンター, ICREA Research Professor）→ ヨーロッパ気候/疫学コミュニティの中心人物。grant 規模大、博士課程候補としても有望
- **Rory Gibb (first/corresponding)**: London School of Hygiene & Tropical Medicine → メール `rory.gibb.14@ucl.ac.uk`（PMC論文記載）
- **Oliver J Brady (senior)**: LSHTM、dengue 疫学の世界的権威
- **Phan Trong Lan**: ベトナム MOH General Department of Preventive Medicine 副局長クラス、現地データの window

### 派遣前に準備すべきこと
1. R + INLA でこの論文の4省サンプルコード（GitHub `rorygibb/dengue_vietnam_ms`）を再現実行
2. 重力モデル・放射モデルを自前で Python 実装し、Gibb の結果と一致させる
3. ベトナム語の行政区分名（tỉnh, huyện, xã）と GADM コードの対応表を作る
4. Rory Gibb / Rachel Lowe にメールでアプローチ（卒論テーマと派遣計画を簡潔に）

### 圏論的 fibration への発展アイデア
- Gibb のデータをベース圏 (District × Month) 上の **複数 sheaf** として再構成
- 気候・インフラ・人流の3 sheaf 間に **natural transformation** （干渉項）を定義
- ASEAN 6カ国に拡張する際、共通ベース圏として **GADM admin-1 (province) レベル**を採用
- persistent homology で「インフラ不在の穴」の時間発展を追跡

---

## 主要参考URL
- 論文本体: https://www.nature.com/articles/s41467-023-43954-0
- PMC（フルテキスト無料）: https://pmc.ncbi.nlm.nih.gov/articles/PMC10713571/
- preprint: https://www.medrxiv.org/content/10.1101/2023.07.25.23293110v2
- コード: https://github.com/rorygibb/dengue_vietnam_ms
- LSHTM DataCompass: https://datacompass.lshtm.ac.uk/id/eprint/3730/
- ICREA highlights: https://www.icrea.cat/impact/outreach/scientific-highlights/11/

抽出日: 2026-05-14
