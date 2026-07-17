# -*- coding: utf-8 -*-
# ATTACK-ALARM (事前固定): 警報の第二車線=攻撃リスク
# バックテスト: 毎年、準備の輸入月数の少ない順ランキング上位q%が、その年+翌年の
#   EMP攻撃onsetをどれだけ捕捉するか(q=10/20/30全報告・相対警報方式)
# ナウキャスト: 最新の準備月数ランキング + 現在の嵐(GSI, ドルはDTWEXBGSで延長)
import csv, math, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp
from attack_anatomy import load_fxm, build_emp_attacks


def main():
    fxm = load_fxm()
    attacks = build_emp_attacks(fxm)
    att_by_cy = defaultdict(set)
    for iso, y, m in attacks:
        att_by_cy[iso].add(y)

    res = defaultdict(dict)
    with open(ROOT / 'data_raw/il_reserves_monthly.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                y, m = row['period'].split('-M')
                res[row['iso3']][(int(y), int(m))] = float(row['reserves_usd'])
            except (ValueError, KeyError):
                continue
    imports = defaultdict(lambda: defaultdict(float))
    with open(ROOT / 'data_raw/imts_trade_xm.csv', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for rep, cp, yr, xv, mv in r:
            try:
                imports[rep][int(yr)] += float(mv)
            except ValueError:
                continue

    def rm_at(iso, y):
        # y年末(12月優先, 無ければ最終月)の準備 / (y年の輸入/12)
        cand = [res[iso].get((y, mm)) for mm in (12, 11, 10)]
        r1 = next((v for v in cand if v), None)
        imp = imports.get(iso, {}).get(y)
        if not r1 or not imp or imp <= 0:
            return None
        v = r1 / (imp / 12.0)
        return v if math.isfinite(v) and v <= 120 else None

    # バックテスト(2000年以降で採点; 判定=y年末ランキング→y+1〜y+2の攻撃)
    L = ['', 'ATTACK-ALARM 2026-07-17 (警報第二車線: 攻撃リスク=準備月数の相対ランキング。バックテスト+ナウキャスト)']
    for q in (0.10, 0.20, 0.30):
        tp = fn = fp_ = tn = 0
        for y in range(2000, 2023):
            pool = []
            for iso in res:
                v = rm_at(iso, y)
                if v is not None:
                    pool.append((v, iso))
            if len(pool) < 30:
                continue
            pool.sort()   # 少ない順
            kq = max(1, int(len(pool) * q))
            listed = {iso for _, iso in pool[:kq]}
            for v, iso in pool:
                hit = any((y + k) in att_by_cy.get(iso, set()) for k in (1, 2))
                if iso in listed and hit:
                    tp += 1
                elif iso in listed:
                    fp_ += 1
                elif hit:
                    fn += 1
                else:
                    tn += 1
        base = (tp + fn) / max(1, tp + fn + fp_ + tn)
        rec = tp / max(1, tp + fn)
        prec = tp / max(1, tp + fp_)
        lift = prec / base if base > 0 else 0
        L.append(f'  q={int(q*100)}%: 捕捉={rec:.3f} 的中={prec:.3f} lift={lift:.2f} (base={base:.3f}, n={tp+fn+fp_+tn})')

    # 現在の嵐ゲージ(GSI: ドル=DTWEXBGS 12m変化, 油, FF, VIX; 直近4四半期)
    def monthly(path):
        acc = defaultdict(list)
        with open(ROOT / path, encoding='utf-8') as f:
            r = csv.reader(f); next(r)
            for row in r:
                try:
                    acc[(int(row[0][:4]), int(row[0][5:7]))].append(float(row[1]))
                except (ValueError, IndexError):
                    continue
        return {k: statistics.mean(v) for k, v in acc.items()}
    ff = monthly('data_raw/fred_FEDFUNDS.csv'); dxb = monthly('data_raw/fred_DTWEXBGS.csv')
    oil = monthly('data_raw/fred_WTISPLC.csv'); vix = monthly('data_raw/fred_VIXCLS.csv')

    def qv(d, y, q, chg=False):
        vs = [d[m] for m in [(y, 3*q-2), (y, 3*q-1), (y, 3*q)] if m in d]
        if not vs:
            return None
        cur = statistics.mean(vs)
        if not chg:
            return cur
        vs0 = [d[m] for m in [(y-1, 3*q-2), (y-1, 3*q-1), (y-1, 3*q)] if m in d]
        if not vs0 or statistics.mean(vs0) == 0:
            return None
        return cur / statistics.mean(vs0) - 1
    QS = [(y, q) for y in range(2007, 2027) for q in (1, 2, 3, 4)]
    hist = {'dx': [], 'oil': [], 'ff': [], 'vix': []}
    vals = {}
    for (y, q) in QS:
        vals[(y, q)] = (qv(dxb, y, q, True), qv(oil, y, q, True), qv(ff, y, q), qv(vix, y, q))
        for k, v in zip(('dx', 'oil', 'ff', 'vix'), vals[(y, q)]):
            if v is not None:
                hist[k].append(v)
    mz = {k: (statistics.mean(v), statistics.pstdev(v)) for k, v in hist.items()}

    def gsi_of(y, q):
        v = vals.get((y, q))
        if not v:
            return None
        comps = []
        for k, x, sign in zip(('dx', 'oil', 'ff', 'vix'), v, (1, -1, 1, 1)):
            if x is None:
                continue
            m, s = mz[k]
            comps.append(sign * (x - m) / s)
        return statistics.mean(comps) if len(comps) >= 3 else None
    recent = [(y, q, gsi_of(y, q)) for (y, q) in QS if (y, q) >= (2024, 1) and gsi_of(y, q) is not None]
    L.append('  現在の嵐ゲージ(GSI, 2007年以降基準のz, ドル=広義指数):')
    for y, q, g in recent[-6:]:
        L.append(f'    {y}Q{q}: GSI={g:+.2f} ({"嵐" if g > 0.5 else "平穏" if g < -0.5 else "中立"})')

    # ナウキャスト: 最新年の攻撃警戒リスト
    meta = fp.load_real_countries()
    latest_y = 2025
    pool = []
    for iso in res:
        # 2025年の最新月準備 / 2024年輸入
        months = sorted((k for k in res[iso] if k[0] == latest_y), reverse=True)
        r1 = res[iso][months[0]] if months else None
        imp = imports.get(iso, {}).get(2024)
        if not r1 or not imp or imp <= 0:
            continue
        v = r1 / (imp / 12.0)
        if math.isfinite(v) and v <= 120:
            pool.append((v, iso, months[0]))
    pool.sort()
    L.append(f'  攻撃警戒リスト2026(準備月数の少ない順, {len(pool)}カ国中下位15):')
    for v, iso, mth in pool[:15]:
        nm = meta.get(iso, {}).get('name', iso)[:20]
        L.append(f'    {nm:20s} {v:5.1f}ヶ月分 (時点{mth[0]}-{mth[1]:02d})')
    with open(ROOT / 'docs/data/verified_results.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
