# -*- coding: utf-8 -*-
# 審判機 (notes/50 C): nowcast_monthly_2026_07.json を最新のer_monthlyで機械判定する
# 使い方: python judge_nowcast.py          -> ドライラン(現時点の途中経過)
#         python judge_nowcast.py --final  -> 本判定(2027-08以降に実行し正本へ追記)
# 判定ルール(JSONに固定済み): 各リスト国のasof月から12ヶ月以内に月次crashルール
# (LV_30_10)のonsetが出たらHIT。12ヶ月経過しonsetなしならMISS。未経過はPENDING。
import json, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
from attack_anatomy import load_fxm, fx_crash_months


def main():
    final = '--final' in sys.argv
    spec = json.load(open(ROOT / 'docs/data/nowcast_monthly_2026_07.json', encoding='utf-8'))
    fxm = load_fxm()
    crash_m = {iso: fx_crash_months(fxm[iso]) for iso in fxm}
    onset_idx = defaultdict(set)
    for iso, cr in crash_m.items():
        idxs = {y * 12 + m - 1 for (y, m) in cr}
        for (y, m) in sorted(cr):
            i = y * 12 + m - 1
            if not any((i - k) in idxs for k in range(1, 13)):
                onset_idx[iso].add(i)
    # データの最新月(判定可能範囲)
    latest_by_c = {c: max(y * 12 + m - 1 for (y, m) in d) for c, d in fxm.items() if d}

    def judge_list(lst):
        out = []
        for e in lst:
            iso = e['iso']
            y, m = e['asof'].split('-')
            a = int(y) * 12 + int(m) - 1
            horizon_end = a + 12
            hits = [i for i in onset_idx.get(iso, set()) if a < i <= horizon_end]
            data_end = latest_by_c.get(iso, a)
            if hits:
                first = min(hits)
                out.append((e['name'], 'HIT', f'onset {first//12}-{first%12+1:02d}'))
            elif data_end >= horizon_end:
                out.append((e['name'], 'MISS', f'12ヶ月経過(データ{data_end//12}-{data_end%12+1:02d})'))
            else:
                left = horizon_end - data_end
                out.append((e['name'], 'PENDING', f'残り{left}ヶ月分のデータ待ち'))
        return out

    L = ['', f'JUDGE-{"FINAL" if final else "DRYRUN"} {__import__("datetime").date.today()} (審判機: nowcast_monthly_2026_07.json, ルールはJSON固定のもの)']
    for key, nm in (('collapse_red', '崩壊赤'), ('attack_red', '攻撃赤'), ('dual_red', '二重赤')):
        res = judge_list(spec.get(key, []))
        hits = sum(1 for _, v, _ in res if v == 'HIT')
        miss = sum(1 for _, v, _ in res if v == 'MISS')
        pend = sum(1 for _, v, _ in res if v == 'PENDING')
        L.append(f'  {nm}: HIT={hits} MISS={miss} PENDING={pend}')
        for name, v, note in res:
            L.append(f'    {name[:16]:16s} {v:7s} {note}')
    txt = '\n'.join(L)
    print(txt)
    if final:
        with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
            f.write(txt + '\n')
        print('\n(正本に追記した)')
    else:
        print('\n(ドライラン: 正本には追記しない。本判定は2027-08以降に --final で)')


if __name__ == '__main__':
    main()
