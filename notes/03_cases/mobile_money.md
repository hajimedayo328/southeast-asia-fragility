# Case 1: 東南アジアのモバイル金融

**スケール**: 国〜地域
**期間**: 2010-2025

## ASEAN10の主要プレイヤー (backbone別)

### Platform型 (民間プラットフォーム主導)
- **VN**: MoMo, ZaloPay, ViettelPay
- **ID**: GoPay, OVO, DANA, ShopeePay
- **PH**: GCash (Globe), Maya
- **MY**: Touch'n Go eWallet, GrabPay, Boost

### Central Bank型 (国主導 backbone)
- **TH**: PromptPay (BOT主導)
- **ID**: QRIS (BI主導の統一規格)
- **KH**: Bakong (NBC主導)
- **PH**: InstaPay+PESONet (BSP主導)

### Bank型
- **SG**: PayNow
- **BN**: BIBD NEXGEN

### Telco型 (電話会社主導)
- **MM**: Wave Money (Yoma+Ant), KBZPay
- **LA**: U-Money (Unitel)

## 各タイプの「便利L」と「不可視コストR」

| タイプ | L (便利) | R (不可視コスト) |
|---|---|---|
| Platform | 高速イノベーション、UI洗練 | 単一プラットフォーム依存、規制困難 |
| Central Bank | 規制統制、財政連携 | 中央集権の単一障害、政治リスク |
| Bank | 既存信頼活用 | 取込スピード遅、legacy縛り |
| Telco | 既存契約者ベース | 電話会社倒産=金融全滅 |

## 仮説候補 (データ取得後に検証)

### H-Mobile-1: 便利度と集中度の正の相関
- X軸: モバイルマネー普及率 (Findex)
- Y軸: トッププロバイダーシェア (HHI的)
- 仮説: 普及率が高い国ほど、集中度も高い
- 期待: 右肩上がりの散布図

### H-Mobile-2: backbone別の脆弱性
- Platform型は脆弱、Central Bank型は中央リスクあるが構造的に分散
- 各タイプの障害頻度 vs 平均障害復旧時間

### H-Mobile-3: 銀行スキップ度
- (モバイル普及率 - 銀行口座保有率) を「リープフロッグ強度」と定義
- 高い国ほど legacy 不在 → 自由度高い → R層が薄い→脆い

### H-Mobile-4: ASEAN内回廊
- 越境決済 (Bakong + PromptPay 等) の連結が backbone タイプを跨ぐとき何が起きるか

## データソース (取得済 → `docs/data/A_findex.json`, `B_concentration.json`)

- World Bank Global Findex 2021
- GSMA Mobile Money report
- 各国中央銀行annual report
- BIS, IMF working papers

## 既存研究

- IMF 2021 e-money paper: M-Pesa集中=systemic risk と明記済
- Kenya CBK: 2016年から M-Pesa を systemic risk 分類
- BIS WP1129: retail payments concentration
- → 主張自体は既存、本プロジェクトの新規性は **圏論的構造 + 複数国比較 + 定量化** にある

## 何が見えてくる予測

- ASEAN10は backbone タイプで明確に3〜4クラスタに分かれる
- 「リープフロッグ強度」と「集中度」の正相関
- Central Bank型は構造的に強いが、政治変動で一気に弱体化リスク
- 先進国 (JP/US/EU) は legacy 銀行ネットワークで分散、ただし AI/プラットフォーム依存で同じ脆弱性に向かいつつある
