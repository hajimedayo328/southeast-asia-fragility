# H-Petri Net シミュレータ

`notes/06_heyting_petri_net.md` と `notes/07_common_cpn_spec.md` に従って、
ASEAN モバイル金融 backbone を Heyting値 Petri net で記述・比較する Python 実装。

## 構成

```
src/
├── h_petri/
│   ├── core.py          # H-Petri Net, Heyting algebra, firing rule
│   ├── backbones/
│   │   ├── bakong.py    # 中央銀行型 (Cambodia)
│   │   └── gcash.py     # 民間プラットフォーム型 (Philippines)
│   └── compare.py       # Bakong vs GCash 比較スクリプト
└── README.md
```

## 動かし方

```bash
cd src/
python -m h_petri.compare
```

または:

```bash
cd src/h_petri/
python compare.py
```

出力:
- 標準出力: 各 backbone の TrustHub 到達履歴 + 解釈
- JSON ファイル: `docs/data/petri_comparison.json` (HTML 可視化用)

## 期待される結果

Bakong (中央銀行型):
- 1回目の `t2_BakongClear` 発火で `TrustHub` が `⊤_pub` 到達
- 国家保証の構造的表現

GCash (民間型):
- `TrustHub` は何回送金しても `⊤_priv` で頭打ち
- 民間企業の保証上限の構造的表現

これが「同じ場所数・同じ遷移数」でも「不可視層 Heyting値の上限が違う」
ことの **構造的** な表現。

## 依存

- Python 3.10+ (型ヒント、match 構文使用)
- 標準ライブラリのみ (numpy 等不要)

## 次の実装予定

- [ ] PayNow (銀行コンソーシアム型)
- [ ] KBZPay (銀行型、ミャンマー)
- [ ] P-invariant / T-invariant 自動計算
- [ ] Open H-Petri Net 合成 (ASEAN5 合成)
- [ ] HTML 可視化への接続
