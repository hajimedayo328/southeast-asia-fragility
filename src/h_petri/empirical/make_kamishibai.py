# -*- coding: utf-8 -*-
# 紙芝居(kamishibai.html)生成: 14枚・図解中心・自己完結
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import false_positive_panel as fp

ROOT = Path(__file__).resolve().parents[3]

meta = fp.load_real_countries(); real = set(meta)
fx = fp.load_series('fx_lcu_per_usd', real)
D_, A_ = fp.CRASH_RULES[fp.PRIMARY_RULE]
crash = fp.crash_years(fp.changes(fx, real, 1), fp.changes(fx, real, 2), D_, A_)
onset = fp.onsets(crash)
counts = {y: 0 for y in range(1977, 2023)}
for (c, y) in onset:
    if y in counts: counts[y] += 1
mx = max(counts.values())

# --- 実データ棒グラフ(嵐×歴史) ---
W, H, L, R, T, B = 880, 380, 50, 14, 80, 42
pw = (W - L - R) / len(counts)
storm = {1982: '中南米債務危機', 1990: '湾岸・ソ連末期', 1994: 'テキーラ/CFA',
         1998: 'アジア・ロシア', 2009: '世界金融危機', 2016: '資源安'}
bars = []; labels = []
for i, (y, c) in enumerate(sorted(counts.items())):
    x = L + i * pw; h = (H - T - B) * c / mx; yy = H - B - h
    col = '#d64545' if y in storm else '#b7c2cd'
    bars.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{pw*0.75:.1f}" height="{h:.1f}" fill="{col}" rx="2"/>')
    if y in storm:
        lx = x + pw * 0.4
        st = {1982: 0, 1990: 26, 1994: 0, 1998: 26, 2009: 0, 2016: 26}[y]
        labels.append(f'<line x1="{lx:.1f}" y1="{yy-4:.1f}" x2="{lx:.1f}" y2="{T-20+st}" stroke="#d64545" stroke-width="1.2" stroke-dasharray="3,3"/>')
        labels.append(f'<text x="{lx:.1f}" y="{T-25+st}" font-size="14" fill="#d64545" text-anchor="middle" font-weight="700">{y} {storm[y]}</text>')
xt = ''.join(f'<text x="{L+i*pw+pw*0.4:.1f}" y="{H-B+22}" font-size="13" fill="#66778a" text-anchor="middle">{y}</text>'
             for i, (y, c) in enumerate(sorted(counts.items())) if y % 10 == 0)
chart = f'<svg viewBox="0 0 {W} {H}">{"".join(bars)}{"".join(labels)}{xt}</svg>'


def slide(title, svg, caption, sub=''):
    s = f'<div class="slide"><h2>{title}</h2><div class="art">{svg}</div><p class="cap">{caption}</p>'
    if sub:
        s += f'<p class="sub">{sub}</p>'
    return s + '</div>'


S = []
S.append('''<div class="slide title"><h1>通貨危機は<br>どこから来るのか</h1>
<p class="cap">警報機を作りながら調べた、50年 × 113カ国</p><p class="sub">図でわかる版 — クリックか →キー でめくる</p>
<div class="art"><svg viewBox="0 0 600 160">
<circle cx="150" cy="80" r="34" fill="#d64545"/><text x="150" y="88" font-size="22" fill="#fff" text-anchor="middle">火事</text>
<line x1="188" y1="80" x2="272" y2="80" stroke="#d64545" stroke-width="6"/>
<circle cx="310" cy="80" r="34" fill="#f0a24a"/><text x="310" y="88" font-size="20" fill="#fff" text-anchor="middle">危険!</text>
<line x1="348" y1="80" x2="432" y2="80" stroke="#e3e8ee" stroke-width="3"/>
<circle cx="470" cy="80" r="34" fill="#b7c2cd"/><text x="470" y="88" font-size="20" fill="#fff" text-anchor="middle">平気</text>
</svg></div></div>''')

S.append(slide('①「通貨危機」って何？',
'''<svg viewBox="0 0 600 220">
<rect x="60" y="50" width="200" height="100" rx="10" fill="#4a8f5c"/><text x="160" y="108" font-size="30" fill="#fff" text-anchor="middle" font-weight="700">100</text>
<text x="160" y="180" font-size="16" fill="#66778a" text-anchor="middle">去年のお金の価値</text>
<text x="300" y="108" font-size="34" fill="#1c2733" text-anchor="middle">→</text>
<rect x="360" y="80" width="130" height="70" rx="8" fill="#d64545"/><text x="425" y="125" font-size="26" fill="#fff" text-anchor="middle" font-weight="700">65</text>
<text x="425" y="180" font-size="16" fill="#66778a" text-anchor="middle">1年後(30%以上消えたら危機)</text>
</svg>''',
'その国のお金の価値が、対ドルで1年に30%以上吹き飛ぶ事件。',
'国民の貯金が目減りし、輸入品(ガソリン・食料・薬)が一斉に値上がる。50年で400回以上起きた。'))

S.append(slide('② 40年使われてきた警報',
'''<svg viewBox="0 0 600 230">
<line x1="300" y1="40" x2="300" y2="70" stroke="#1c2733" stroke-width="5"/>
<line x1="140" y1="70" x2="460" y2="70" stroke="#1c2733" stroke-width="5"/>
<line x1="140" y1="70" x2="140" y2="95" stroke="#1c2733" stroke-width="3"/>
<line x1="460" y1="70" x2="460" y2="95" stroke="#1c2733" stroke-width="3"/>
<rect x="85" y="95" width="110" height="55" rx="8" fill="#d64545"/><text x="140" y="128" font-size="17" fill="#fff" text-anchor="middle">借金</text>
<rect x="405" y="95" width="110" height="55" rx="8" fill="#4a8f5c"/><text x="460" y="128" font-size="17" fill="#fff" text-anchor="middle">貯金</text>
<text x="140" y="175" font-size="14" fill="#66778a" text-anchor="middle">1年以内に返す外貨</text>
<text x="460" y="175" font-size="14" fill="#66778a" text-anchor="middle">外貨準備</text>
<text x="300" y="215" font-size="19" fill="#1c2733" text-anchor="middle" font-weight="700">借金 ÷ 貯金 が 1 を超えたら警報</text>
</svg>''',
'「1年以内に返す借金が、貯金より多い国は危ない」——単純明快で、中央銀行の基準として現役。',
'ところが2025年に「この警報はもう死んだ」という論文が出た。誰も成績表を作らないまま。'))

S.append(slide('③ 成績表を作ってみた(世界初)',
'''<svg viewBox="0 0 600 250">
<rect x="90" y="30" width="200" height="90" rx="10" fill="#e7f0e9" stroke="#4a8f5c" stroke-width="2"/>
<text x="190" y="65" font-size="16" fill="#4a8f5c" text-anchor="middle" font-weight="700">的中 163</text><text x="190" y="95" font-size="13" fill="#66778a" text-anchor="middle">鳴って、危機が来た</text>
<rect x="310" y="30" width="200" height="90" rx="10" fill="#fdeeee" stroke="#d64545" stroke-width="2"/>
<text x="410" y="65" font-size="16" fill="#d64545" text-anchor="middle" font-weight="700">空振り 487</text><text x="410" y="95" font-size="13" fill="#66778a" text-anchor="middle">鳴ったのに、何もなし</text>
<rect x="90" y="135" width="200" height="90" rx="10" fill="#fdeeee" stroke="#d64545" stroke-width="2"/>
<text x="190" y="170" font-size="16" fill="#d64545" text-anchor="middle" font-weight="700">見逃し 298</text><text x="190" y="200" font-size="13" fill="#66778a" text-anchor="middle">黙ってたのに、危機</text>
<rect x="310" y="135" width="200" height="90" rx="10" fill="#eef2f6" stroke="#b7c2cd" stroke-width="2"/>
<text x="410" y="170" font-size="16" fill="#66778a" text-anchor="middle" font-weight="700">正しく沈黙 2,503</text><text x="410" y="200" font-size="13" fill="#66778a" text-anchor="middle">平和で、鳴らず</text>
</svg>''',
'鳴っても4回に3回は空振り。危機の3分の2は無警報で来る。',
'ただし当てずっぽうよりは1.88倍当たる——「本物だが、弱い」警報だった。'))

S.append(slide('④「死んだ」は誤診だった',
'''<svg viewBox="0 0 640 240">
<text x="170" y="30" font-size="15" fill="#66778a" text-anchor="middle" font-weight="700">1990年代</text>
<rect x="80" y="45" width="180" height="150" rx="8" fill="none" stroke="#b7c2cd" stroke-width="2"/>
<rect x="80" y="85" width="180" height="110" fill="#cfe0f5"/>
<line x1="70" y1="120" x2="270" y2="120" stroke="#d64545" stroke-width="3" stroke-dasharray="6,4"/>
<text x="170" y="215" font-size="13" fill="#66778a" text-anchor="middle">借金の水位がラインを超える→鳴る</text>
<text x="470" y="30" font-size="15" fill="#66778a" text-anchor="middle" font-weight="700">2000年代〜(みんな貯金した)</text>
<rect x="380" y="45" width="180" height="150" rx="8" fill="none" stroke="#b7c2cd" stroke-width="2"/>
<rect x="380" y="160" width="180" height="35" fill="#cfe0f5"/>
<line x1="370" y1="120" x2="570" y2="120" stroke="#d64545" stroke-width="3" stroke-dasharray="6,4"/>
<text x="470" y="215" font-size="13" fill="#66778a" text-anchor="middle">水位が下がってラインに届かない→鳴らない</text>
</svg>''',
'アジア危機に懲りて各国が貯金を積み、警報が鳴る機会そのものが消えた。',
'鳴ったときの信頼度はむしろ上昇(1.4倍→1.9倍)。警報は死んでいない、静かになっただけ。'))

S.append(slide('⑤ 見逃しの正体：もらい事故',
'''<svg viewBox="0 0 640 240">
<circle cx="140" cy="110" r="42" fill="#d64545"/><text x="140" y="105" font-size="17" fill="#fff" text-anchor="middle">相手国</text><text x="140" y="126" font-size="15" fill="#fff" text-anchor="middle">火事!</text>
<line x1="186" y1="110" x2="354" y2="110" stroke="#d64545" stroke-width="8"/>
<text x="270" y="92" font-size="14" fill="#d64545" text-anchor="middle" font-weight="700">貿易の線(大口取引)</text>
<circle cx="400" cy="110" r="42" fill="#4a8f5c"/><text x="400" y="105" font-size="16" fill="#fff" text-anchor="middle">自分</text><text x="400" y="126" font-size="13" fill="#fff" text-anchor="middle">家計簿は健全</text>
<path d="M 455 95 q 30 15 0 30" stroke="#f0a24a" stroke-width="4" fill="none"/>
<text x="540" y="105" font-size="16" fill="#f0a24a" font-weight="700" text-anchor="middle">1〜2年後</text>
<text x="540" y="128" font-size="16" fill="#f0a24a" font-weight="700" text-anchor="middle">危険!</text>
<text x="320" y="205" font-size="15" fill="#66778a" text-anchor="middle">相手の通貨が暴落 → 激安品が流れ込む → 競り負けて自分の通貨にも売り圧力</text>
</svg>''',
'自分の家計簿が健全でも、大口の貿易相手が燃えていれば1〜2年後に自分も危ない。',
'これで、警報が原理的に見えなかった危機の一部(約14%)が見えるようになった。'))

S.append(slide('⑥「効いて当然」の説明を全部つぶした',
'''<svg viewBox="0 0 620 250">
<g font-size="16">
<text x="40" y="45" fill="#1c2733">「世界中が燃えてる時代だから」</text><text x="520" y="45" fill="#4a8f5c" font-weight="700">→ 違う</text>
<text x="40" y="85" fill="#1c2733">「近所の国だから」(地理)</text><text x="520" y="85" fill="#4a8f5c" font-weight="700">→ 違う</text>
<text x="40" y="125" fill="#1c2733">「同じ通貨を使う国の道連れ」</text><text x="520" y="125" fill="#4a8f5c" font-weight="700">→ 違う</text>
<text x="40" y="165" fill="#1c2733">「人手で作った別の危機リストなら消える？」</text><text x="520" y="165" fill="#4a8f5c" font-weight="700">→ 残る</text>
<text x="40" y="205" fill="#1c2733">「銀行の貸し借りの線でも効く？」</text><text x="520" y="205" fill="#d64545" font-weight="700">→ 効かない</text>
</g>
<text x="310" y="240" font-size="14" fill="#66778a" text-anchor="middle">最後の1行が大事：何でも通るザル検定ではない。商売の線だけが効く。</text>
</svg>''',
'「貿易の火事」は7種類の疑いを全部生き残った。',
'しかも銀行危機・債務危機には効かない＝通貨危機専用。「暴落→安売り競争→通貨圧力」という理屈と一致。'))

S.append(slide('⑦ 警報は「順位」で出す',
'''<svg viewBox="0 0 640 250">
<text x="165" y="35" font-size="15" fill="#d64545" text-anchor="middle" font-weight="700">✗ 固定ライン方式</text>
<rect x="60" y="50" width="210" height="130" rx="8" fill="none" stroke="#b7c2cd" stroke-width="2"/>
<line x1="60" y1="90" x2="270" y2="90" stroke="#d64545" stroke-width="3" stroke-dasharray="6,4"/>
<rect x="60" y="150" width="210" height="30" fill="#cfe0f5"/>
<text x="165" y="205" font-size="13" fill="#66778a" text-anchor="middle">時代が変わると誰も届かず永久に沈黙</text>
<text x="470" y="35" font-size="15" fill="#4a8f5c" text-anchor="middle" font-weight="700">○ 毎年ランキング方式</text>
<rect x="380" y="60" width="180" height="24" rx="5" fill="#d64545"/><text x="392" y="77" font-size="13" fill="#fff">1位 いちばん危ない国</text>
<rect x="380" y="90" width="180" height="24" rx="5" fill="#f0a24a"/><text x="392" y="107" font-size="13" fill="#fff">2位</text>
<rect x="380" y="120" width="180" height="24" rx="5" fill="#f0c98a"/><text x="392" y="137" font-size="13" fill="#fff">3位 …上位を見張る</text>
<rect x="380" y="150" width="180" height="24" rx="5" fill="#dfe6ec"/><text x="392" y="167" font-size="13" fill="#66778a">…113位まで</text>
<text x="470" y="205" font-size="13" fill="#66778a" text-anchor="middle">「今年一番危ない順」は絶対に風化しない</text>
</svg>''',
'固定の危険水域は必ず風化する(本家も自作警報も同じ死に方をした)。',
'順位方式なら、どの監視予算でも捕捉率・的中率の両方が上がった。'))

S.append(slide('⑧ 大波の解剖：主犯は「嵐」',
'''<svg viewBox="0 0 640 240">
<rect x="80" y="60" width="420" height="60" rx="8" fill="#8fa3b8"/>
<rect x="500" y="60" width="70" height="60" rx="8" fill="#d64545"/>
<text x="290" y="97" font-size="19" fill="#fff" text-anchor="middle" font-weight="700">嵐(世界共通ショック) 85%</text>
<text x="535" y="88" font-size="13" fill="#fff" text-anchor="middle">伝染</text><text x="535" y="106" font-size="13" fill="#fff" text-anchor="middle">15%</text>
<text x="320" y="160" font-size="15" fill="#66778a" text-anchor="middle">1982年・1997年のような「同時多発の大波」の成分(火事シミュレーター500回で分解)</text>
<text x="320" y="195" font-size="15" fill="#1c2733" text-anchor="middle" font-weight="700">タイ1997を歴史から消しても、隣国の運命はほぼ変わらなかった</text>
<text x="320" y="220" font-size="14" fill="#66778a" text-anchor="middle">= タイは台風の最初の雨粒であって、台風の原因ではない</text>
</svg>''',
'嵐が波を作り(いつ・何件)、貿易の火事が犠牲者を選ぶ(誰が)。',
'国を1個ずつ見ても大波は説明できない——「気象」の情報が必要だった。'))

S.append(slide('⑨ 機械が歴史の名場面を独力で言い当てた', chart,
'グレー＝毎年の危機発生数(実測)。赤＝機械が「説明できない嵐が強い」と逆算した年。',
'機械に与えたのは為替と貿易の数字だけ。事件名は一切教えていない。'))

S.append(slide('⑩ 嵐の指紋(月単位に拡大して有意に)',
'''<svg viewBox="0 0 640 230">
<g text-anchor="middle">
<rect x="60" y="50" width="120" height="90" rx="12" fill="#eef3fb" stroke="#3572d8"/><text x="120" y="92" font-size="24">💵⬆</text><text x="120" y="122" font-size="14" fill="#1c2733">ドル高</text>
<rect x="200" y="50" width="120" height="90" rx="12" fill="#eef3fb" stroke="#3572d8"/><text x="260" y="92" font-size="24">%⬆</text><text x="260" y="122" font-size="14" fill="#1c2733">米国の高金利</text>
<rect x="340" y="50" width="120" height="90" rx="12" fill="#eef3fb" stroke="#3572d8"/><text x="400" y="92" font-size="24">🛢⬇</text><text x="400" y="122" font-size="14" fill="#1c2733">資源安</text>
<rect x="480" y="50" width="120" height="90" rx="12" fill="#eef3fb" stroke="#3572d8"/><text x="540" y="92" font-size="24">😨⬆</text><text x="540" y="122" font-size="14" fill="#1c2733">恐怖指数</text>
</g>
<text x="330" y="180" font-size="16" fill="#1c2733" text-anchor="middle" font-weight="700">4つとも理論どおりの向きで統計的に有意(四半期190点)</text>
<text x="330" y="205" font-size="14" fill="#66778a" text-anchor="middle">この4つの平均=「世界ストレス指数」で、嵐の約8割が説明できた</text>
</svg>''',
'嵐の正体 ≒ ワシントンの金融環境と世界の投資家心理。',
'新興国の危機の波は、当事国ではなく「世界の気象」が作る。残り2割は未同定。'))

S.append(slide('⑪ 全部を1本の式に',
'''<svg viewBox="0 0 660 230">
<g text-anchor="middle">
<rect x="30" y="60" width="150" height="80" rx="12" fill="#e7f0e9" stroke="#4a8f5c"/><text x="105" y="95" font-size="15" fill="#1c2733" font-weight="700">家計簿</text><text x="105" y="118" font-size="12" fill="#66778a">借金÷貯金</text>
<text x="200" y="108" font-size="26" fill="#1c2733">+</text>
<rect x="220" y="60" width="150" height="80" rx="12" fill="#fdeeee" stroke="#d64545"/><text x="295" y="95" font-size="15" fill="#1c2733" font-weight="700">隣の火事</text><text x="295" y="118" font-size="12" fill="#66778a">貿易相手の危機</text>
<text x="390" y="108" font-size="26" fill="#1c2733">+</text>
<rect x="410" y="60" width="150" height="80" rx="12" fill="#eef2f6" stroke="#8fa3b8"/><text x="485" y="95" font-size="15" fill="#1c2733" font-weight="700">世界の嵐</text><text x="485" y="118" font-size="12" fill="#66778a">ドル・金利・資源・恐怖</text>
</g>
<text x="330" y="185" font-size="17" fill="#1c2733" text-anchor="middle" font-weight="700">→ 危険スコア → 毎年、世界ランキング上位を見張る</text>
<text x="330" y="210" font-size="13" fill="#66778a" text-anchor="middle">全部が公開データで計算できる。この式だけで50年の危機史の「質感」が再現できることを検証済み</text>
</svg>''',
'家計簿 + 隣の火事 + 世界の嵐 → 順位で見張る。',
'見えない自由変数はもう無い(嵐の残り2割を除く)。'))

S.append(slide('⑫ 実は「危機」は2種類あった',
'''<svg viewBox="0 0 640 240">
<text x="170" y="35" font-size="15" fill="#66778a" text-anchor="middle" font-weight="700">ゆっくり崩壊(通貨が沈む)</text>
<polyline points="60,70 120,85 180,105 240,140 280,170" stroke="#d64545" stroke-width="4" fill="none"/>
<text x="170" y="200" font-size="13" fill="#66778a" text-anchor="middle">貿易の火事が予告できるのはこっち</text>
<text x="470" y="35" font-size="15" fill="#66778a" text-anchor="middle" font-weight="700">鋭い攻撃(防衛成功も含む)</text>
<polyline points="380,120 430,118 450,60 470,118 560,120" stroke="#3572d8" stroke-width="4" fill="none"/>
<path d="M 445 75 L 465 75 L 465 98 Q 455 108 445 98 Z" fill="#4a8f5c"/>
<text x="470" y="200" font-size="13" fill="#66778a" text-anchor="middle">香港1998: 為替は1ミリも動かず防衛成功</text>
<text x="320" y="228" font-size="14" fill="#1c2733" text-anchor="middle" font-weight="700">2つの重なりは17%だけ。しかも固定相場の国の危機は攻撃型に+14ポイント偏る(制度が型を決める)</text>
</svg>''',
'為替に加えて「準備の急減」「金利の急騰」も見る物差しに変えたら、防衛に成功した攻撃が見えるようになった。',
'旧しくみでは香港1998(ペッグ防衛戦)は原理的に不可視だった。攻撃のタイミングは嵐と同期する(r=+0.39)。'))

S.append(slide('⑬ 貯金の真実：防ぐが、救わない',
'''<svg viewBox="0 0 660 240">
<g text-anchor="middle">
<path d="M 90 60 L 130 60 L 130 105 Q 110 125 90 105 Z" fill="#4a8f5c"/>
<text x="110" y="150" font-size="15" fill="#1c2733" font-weight="700">抑止力 ○</text>
<text x="110" y="172" font-size="12" fill="#66778a">貯金が薄い国ほど</text><text x="110" y="188" font-size="12" fill="#66778a">攻撃される(0.63)</text>
<path d="M 300 60 L 340 60 L 340 105 Q 320 125 300 105 Z" fill="#b7c2cd"/>
<line x1="295" y1="55" x2="345" y2="120" stroke="#d64545" stroke-width="5"/>
<text x="320" y="150" font-size="15" fill="#1c2733" font-weight="700">防衛力 ✗</text>
<text x="320" y="172" font-size="12" fill="#66778a">攻撃されたら貯金の</text><text x="320" y="188" font-size="12" fill="#66778a">多寡は生死を分けない(0.47)</text>
<circle cx="510" cy="75" r="24" fill="#d64545"/><line x1="537" y1="75" x2="580" y2="75" stroke="#d64545" stroke-width="6"/><circle cx="598" cy="75" r="18" fill="#f0a24a"/>
<text x="545" y="150" font-size="15" fill="#1c2733" font-weight="700">生死の分水嶺</text>
<text x="545" y="172" font-size="12" fill="#66778a">貿易近傍の火事(0.61)が</text><text x="545" y="188" font-size="12" fill="#66778a">倒れるかを決める</text>
</g>
<text x="330" y="225" font-size="13" fill="#66778a" text-anchor="middle">理由: 攻撃者は貯金を見て標的を選ぶ→攻撃された時点で貯金の情報は使い尽くされている</text>
</svg>''',
'貯金は攻撃の頻度を減らすが、攻撃されたときの生存率は買えない。',
'1997年後の世界的な貯金ブームは「攻撃されにくさ」を買った。生存を買うのは貿易構造——一朝一夕に積めない。'))

S.append(slide('⑭ 警報は二車線に',
'''<svg viewBox="0 0 660 230">
<rect x="50" y="45" width="270" height="130" rx="12" fill="#fdeeee" stroke="#d64545"/>
<text x="185" y="75" font-size="15" fill="#d64545" text-anchor="middle" font-weight="700">遅い車線：崩壊を予知</text>
<text x="185" y="102" font-size="13" fill="#1c2733" text-anchor="middle">家計簿 + 貿易の火事</text>
<text x="185" y="124" font-size="13" fill="#1c2733" text-anchor="middle">1〜2年先/的中2.17倍</text>
<text x="185" y="152" font-size="12" fill="#66778a" text-anchor="middle">上位: ジブチ・ベラルーシ・アルメニア…</text>
<rect x="340" y="45" width="270" height="130" rx="12" fill="#eef3fb" stroke="#3572d8"/>
<text x="475" y="75" font-size="15" fill="#3572d8" text-anchor="middle" font-weight="700">速い車線：攻撃を予知</text>
<text x="475" y="102" font-size="13" fill="#1c2733" text-anchor="middle">準備の輸入月数の薄さ×嵐</text>
<text x="475" y="124" font-size="13" fill="#1c2733" text-anchor="middle">数ヶ月先/的中1.86倍</text>
<text x="475" y="152" font-size="12" fill="#66778a" text-anchor="middle">最薄: ボリビア0.7ヶ月・ジンバブエ0.7…</text>
<text x="330" y="205" font-size="14" fill="#1c2733" text-anchor="middle" font-weight="700">二車線とも赤: ベラルーシ・ジブチ・トルコ(最強警戒クラス) ／ 嵐ゲージは現在「中立」</text>
</svg>''',
'発見が全部そのまま警報の設計図になった。',
'顔検査: 準備最下位だったボリビア(2025年12月時点0.7ヶ月分)は、2026年2月に実際に危機入りした。'))

S.append(slide('⑮ で、いまどこが危ない？(2024年末データ)',
'''<svg viewBox="0 0 640 250">
<g font-size="15">
<rect x="60" y="35" width="440" height="28" rx="6" fill="#d64545"/><text x="72" y="55" fill="#fff" font-weight="700">1位 ジブチ — 借金過多 × エチオピアの火事42%</text>
<rect x="60" y="72" width="400" height="28" rx="6" fill="#e06c6c"/><text x="72" y="92" fill="#fff" font-weight="700">2位 ベラルーシ — 貿易の69%がロシア</text>
<rect x="60" y="109" width="360" height="28" rx="6" fill="#ea8f8f"/><text x="72" y="129" fill="#fff" font-weight="700">3位 アルメニア — ロシア38%</text>
<rect x="60" y="146" width="330" height="28" rx="6" fill="#f2b3b3"/><text x="72" y="166" fill="#1c2733" font-weight="700">4位 トルコ — 借金1.15 × 火事12%</text>
<rect x="60" y="183" width="300" height="28" rx="6" fill="#f7d2d2"/><text x="72" y="203" fill="#1c2733" font-weight="700">5位 ジョージア — ロシア11%</text>
</g>
<text x="320" y="240" font-size="14" fill="#66778a" text-anchor="middle">地図を与えていないのに、貿易の線がロシア圏とエチオピア回廊を再発見した</text>
</svg>''',
'2024年の火元：エジプト・ナイジェリア・アルゼンチン・エチオピア・ロシア等12カ国。',
'このリストは日付つきで公開保存済み——2027-28年に答え合わせができる(過去実績: 当てずっぽうの1.5〜2倍)。'))

S.append('''<div class="slide title"><h1>まとめ</h1>
<div class="art"><svg viewBox="0 0 660 190">
<g font-size="17" fill="#1c2733">
<text x="40" y="45">1. 有名な警報は死んでいない——<tspan font-weight="700">鳴らなくなっただけ</tspan></text>
<text x="40" y="85">2. 見逃しの一部は<tspan font-weight="700">取引相手からのもらい事故</tspan>——順位で見張れば拾える</text>
<text x="40" y="125">3. 大波の主犯は<tspan font-weight="700">世界の嵐</tspan>(ドル・金利・資源・恐怖)——伝染は犠牲者を選ぶ役</text>
<text x="40" y="160">4. <tspan font-weight="700">貯金は攻撃を防ぐが救わない</tspan>——生死は貿易近傍、型は為替制度が決める</text>
</g>
<text x="40" y="185" font-size="13" fill="#66778a">まだ分からないこと: 見逃しの86%・嵐の残り2割・「皆が逃げたら成立する」原理的に予測不能な危機</text>
</svg></div>
<p class="cap">数字は全部、生の計算出力つきで公開してある——疑ってかかれる形で。</p>
<p class="sub">詳細版: advisor_brief.html ／ 正本: docs/data/verified_results.txt (GitHub)</p></div>''')

slides_html = ''.join(S)
html = '''<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>紙芝居 — 通貨危機はどこから来るのか</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,"Hiragino Kaku Gothic ProN","Noto Sans JP",Meiryo,sans-serif;background:#f2f5f8;color:#1c2733;overflow:hidden}
.slide{display:none;position:fixed;inset:0;padding:5vh 6vw;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:#fff}
.slide.on{display:flex}
.slide h1{font-size:clamp(1.8rem,5vw,3.2rem);line-height:1.25;margin-bottom:2vh}
.slide h2{font-size:clamp(1.2rem,3.2vw,1.9rem);margin-bottom:2.5vh}
.art{width:min(92vw,860px);margin:1vh 0}
.art svg{width:100%;height:auto}
.cap{font-size:clamp(1rem,2.4vw,1.25rem);font-weight:600;max-width:46em;margin-top:1.5vh}
.sub{font-size:clamp(.85rem,1.9vw,1rem);color:#66778a;max-width:46em;margin-top:1vh}
.nav{position:fixed;bottom:14px;right:18px;font-size:.9rem;color:#66778a;z-index:10}
.btn{position:fixed;top:50%;transform:translateY(-50%);font-size:2rem;color:#b7c2cd;cursor:pointer;user-select:none;z-index:10;padding:20px}
.btn:hover{color:#3572d8}
#prev{left:4px} #next{right:4px}
.hint{position:fixed;bottom:14px;left:18px;font-size:.85rem;color:#9aa8b5}
</style></head><body>
''' + slides_html + '''
<div id="prev" class="btn">&#8249;</div><div id="next" class="btn">&#8250;</div>
<div class="nav"><span id="pg"></span></div>
<div class="hint">クリック / ← → キーでめくる</div>
<script>
const sl=[...document.querySelectorAll('.slide')];let i=0;
function show(k){i=Math.max(0,Math.min(sl.length-1,k));sl.forEach((s,j)=>s.classList.toggle('on',j===i));document.getElementById('pg').textContent=(i+1)+' / '+sl.length;}
document.getElementById('next').onclick=e=>{e.stopPropagation();show(i+1)};
document.getElementById('prev').onclick=e=>{e.stopPropagation();show(i-1)};
document.body.onclick=()=>show(i+1);
document.onkeydown=e=>{if(e.key==='ArrowRight'||e.key===' ')show(i+1);if(e.key==='ArrowLeft')show(i-1)};
show(0);
</script></body></html>'''

out = ROOT / 'kamishibai.html'
out.write_text(html, encoding='utf-8')
print(f'kamishibai.html written, {len(S)} slides, {len(html)//1024} KB')
