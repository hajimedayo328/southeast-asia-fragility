# 00. ノート全体地図 (Index)

**作成日**: 2026-05-25
**目的**: 30本のノートを1ページで見渡す。次セッション or 提出時の「ナビ」。

---

## 注意

- **ノートは裏側のストック**。Pages (`docs/`) の方が中心。
- 「必要性わからん」と感じたら、それは正常。Pages を中心に見れば OK。
- このINDEXは「俺 (Claude) が次セッションで迷子にならないため」と「提出用の地図」用。

---

## ランク表記
- ★★★: 本プロジェクトの核 (Pages の主張を支える)
- ★★: 補助 (理論的な裏付け、必要なら参照)
- ★: 試行錯誤の記録 (捨てても困らない、ただし削除はしない)

---

## ノート一覧 (依存関係付き)

### Phase 1: 概念立ち上げ (随伴 L⊣R)

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 01 | pitch.md | ★★ | 1ページピッチ (提出用に書いたが、Pages の index.html Hero と重複) |
| 02 | framework.md | ★★★ | **随伴 L⊣R** の全体フレーム。Pages 全体の理論的支柱 |
| 03 | cases/ | ★★ | モバイル金融 / 災害都市 の最初のスケッチ |
| 04 | directions.md | ★ | 探索期の方向案メモ |

### Phase 2: Petri net 主張群

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 05 | petri_net_theory.md | ★★★ | **Petri net 主張5つの俯瞰**。Pages の petri タブの根拠 |
| 06 | heyting_petri_net.md | ★★★ | **H-Petri Net の数学的定義**。Heyting値拡張の中核 |
| 07 | common_cpn_spec.md | ★★★ | **共通CPN規約**。4 backbone 比較の前提 |

### Phase 3: 圏論的格上げ (1-cat → 2-cat → coherence)

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 08 | categorical_interpretation.md | ★★ | 関手 + 自然変換による解釈 (1-cat 視点) |
| 09 | 2category_structure.md | ★★ | 2-category 構造 (関手間の自然変換) |
| 10 | open_h_petri_net.md | ★★ | Open Petri Net 拡張 (Baez-Master 2018) |
| 11 | universal_property.md | ★ | Lawvere theory base (実用上ほぼ使わない) |
| 12 | leapfroggability.md | ★★ | R-restricted reachability でのリープフロッグ定義 |
| 13 | monoidal_2category.md | ★ | Strip Folding (Jia 2022-23) 対応の理論側 |
| 14 | coherence.md | ★ | coherence axiom 検証 (技術的) |

### Phase 4: 律速逆転 (中心命題)

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 15 | bottleneck_reversal.md | ★★★ | **律速逆転定理** (⊗ max / ▷ meet)。Ghrist-Gould-Lopez 2024 の応用 |
| 16 | place_centrality.md | ★★ | 場所中心性 = ホットスポット (主張4の厳密化) |

### Phase 5: 普遍性主張 (時間軸 + 異分野)

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 17 | time_functor.md | ★★★ | **時間軸の導入**。Trust: Time → H 関手 |
| 18 | universal_isomorphism.md | ★★★ | **異分野同型** (9ドメインで便利と不可視コストが同型) |
| 19 | temporal_category.md | ★★ | 時間圏 Time の categorical 定義 |
| 20 | time_compression.md | ★★ | 速度-集中度トレードオフ |

### Phase 6: AI実例 + 検証

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 21 | ai_isomorphism.md | ★★ | AI同型の詳細 (Cloudflare 2025-11 等) |
| 22 | counterexample_analysis.md | ★★ | 反例検証 (太陽光 / OSS / 空気 等10候補) |

### Phase 7: 予言ペア (核実証)

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 23 | prediction_pair_isomorphism.md | ★★★ | **5ペアの同型射構成** (informal版) |

### Phase 8: 圏論を本気で当てる3層 (ユーザー方針後)

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 24 | monad_side_effects.md | ★★ | **モナド (Writer H)** で副作用累積を厳密化 |
| 25 | sheaf_local_global.md | ★★★ | **層 (sheaf)** で局所→大域の伝染、1997とCloudflareの同じ H¹ 振る舞い |
| 26 | translation_functor.md | ★★★ | **翻訳関手 F + Kan拡張**、5ペアを strict/lax で分類 (informal) |
| 27 | enriched_prediction_category.md | ★★★ | **予言圏を Heyting-enriched category として厳密化** (Lawvere 1973)。射を H 値で定義し循環論法を断つ。F を strict/lax/broken で**計算分類** |

### Phase 9: 自己批判・実証検証 (提出前の頑健化)

| # | ノート | ランク | 一行サマリ |
|---|---|---|---|
| 28 | false_positive_analysis.md | ★★★ | §5.6 偽陽性=文献(A)+5カ国混同行列(B)。**マレーシア偽陰性**を検出 |
| 29 | edge_grounding_sensitivity.md | ★★★ | 予言ペア辺をグラウンディング。**判定 under-determined、頑健はペア2のみ** |
| 30 | false_positive_panel.md | ★★★ | **真の偽陽性パネル**(WDI実データ113カ国)。偽警報率75%/FPR16%/NtS0.46/lift1.88 |

---

## 「核」ノート 9本 (★★★)

これだけ読めば本プロジェクトの理論が分かる:

1. **02 framework** — 随伴 L⊣R
2. **05 petri_net_theory** — Petri net 主張俯瞰
3. **06 heyting_petri_net** — H-Petri Net 数学
4. **07 common_cpn_spec** — 4 backbone 比較規約
5. **15 bottleneck_reversal** — 律速逆転定理
6. **17 time_functor** — 時間軸の導入
7. **18 universal_isomorphism** — 異分野同型
8. **23 prediction_pair_isomorphism** — 予言ペア5本
9. **25 sheaf_local_global** + **26 translation_functor** — 圏論本気適用

これ以外は「補助 or 試行錯誤の記録」として置いてある。

---

## ノート間の依存グラフ (主要のみ)

```
02 framework (随伴)
   ↓
05 Petri主張俯瞰 ─→ 06 H-Petri 数学
                    ↓
                   07 共通CPN規約 ─→ Pages (petri.html)
                    ↓
                   15 律速逆転 (← Ghrist 2024)
                    ↓
17 時間軸 ─→ 18 異分野同型 ─→ 23 予言ペア ─→ Pages (temporal.html)
                                  ↓
                       24 モナド + 25 層 + 26 翻訳関手 (圏論本気適用3層)
```

---

## Pages との対応

| Pages タブ | 主要 notes |
|---|---|
| **index.html** (概観) | 02, 18, 23 |
| **finance.html** (金融) | 03, 07 |
| **petri.html** (Petri net) | 05, 06, 07, 09, 15, 26 |
| **temporal.html** (時間軸) | 17, 18, 19, 20, 23, 25 |

---

## 「捨てて困らない」候補 (将来整理する場合)

- 01 pitch.md (index.html と内容重複)
- 04 directions.md (探索期メモ)
- 11 universal_property.md (実用上未使用)
- 13 monoidal_2category.md (技術的、結論は他ノートに集約済)
- 14 coherence.md (technical verification only)

→ これらは保管価値が低い。ただし「整理コスト > 削除価値」なので放置でOK。

---

## サーベイ / 検証ノート (literature/)

- `literature/raw/01-11` 圏論サーベイ系統
- `literature/raw/16` 1997アジア通貨危機分析
- `literature/validation/V1-V3` 仮説検証

これらは notes と独立に「先行研究の整理」として機能。

---

## 実装との対応

| 実装 | 関連 notes | Pages |
|---|---|---|
| `src/h_petri/core.py` | 06 (H-Petri Net) | — |
| `src/h_petri/backbones/{bakong,gcash,paynow,kbzpay}.py` | 07 (共通CPN) | petri.html §P4 |
| `src/h_petri/domains/ai_dependency.py` | 18 (異分野同型), 26 (翻訳関手) | petri.html §P5 |
| `src/h_petri/monad/writer_h.py` | 24 (Writer H モナド) | petri.html §P7 |
| `src/h_petri/sheaf/cech.py` | 25 (層) | petri.html §P6 |
| `src/h_petri/centrality.py` | 16 (中心性) | (未統合) |
| `src/h_petri/trust_timeline.py` | 17, 20 (時間関手) | temporal.html §T1-T9 |
| `src/h_petri/compare.py` | 06, 07 (金融比較ランナー) | — |
| `src/h_petri/compare_ai.py` | 18 (AI比較ランナー + Cloudflare cascade) | — |

### 出力 JSON と Pages の対応

| JSON | 生成元 | 使用先 |
|---|---|---|
| `docs/data/petri_comparison.json` | `compare.py` | petri.html §P4 |
| `docs/data/ai_comparison.json` | `compare_ai.py` | petri.html §P5 |
| `docs/data/trust_timeline.json` | `trust_timeline.py` | temporal.html §T1-T9 |
| `docs/data/sheaf_h1.json` | `sheaf/cech.py` | petri.html §P6 |
| `docs/data/writer_h.json` | `monad/writer_h.py` | petri.html §P7 |

---

## このINDEXの位置づけ

**ユーザー本人**: 「必要性わからん」と感じてOK。ノートは裏のストック。
**俺 (Claude) **: 次セッションでの迷子防止。
**提出時**: 「9本の核ノート + Pages 4タブ + Python実装」のセットで全体像が伝わる。

ノートは積み上げたけど、本プロジェクトの **対外的な顔は Pages**。
ノートはあくまで「動くものと数式の裏付け」として置いてある。
