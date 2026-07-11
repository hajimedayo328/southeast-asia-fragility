# IMF IMTS(旧DOTS)から二国間貿易(輸出FOB+輸入CIF, 年次, USD)を取得
# 対象: GGパネルに現れる国のみ(報告国)。相手国は実在国(meta ISO3)のみ保持
# 再開可能: 出力CSVに既にある報告国はスキップ
import sys, csv, time, io
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp

OUT = ROOT / 'data_raw/imts_trade.csv'
BASE = 'https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IMTS,1.0.0'
HDR = {'Accept': 'application/vnd.sdmx.data+csv;version=1.0.0',
       'User-Agent': 'research-script (academic use)'}


def main():
    meta = fp.load_real_countries()
    real3 = set(meta)
    gg = fp.load_series('st_debt_reserves', set(meta))
    reporters = sorted({c for (c, t) in gg})
    print(f'reporters to fetch: {len(reporters)}')

    done = set()
    if OUT.exists():
        with open(OUT, encoding='utf-8') as f:
            r = csv.reader(f); next(r, None)
            for row in r:
                done.add(row[0])
    mode = 'a' if OUT.exists() else 'w'
    out = open(OUT, mode, encoding='utf-8', newline='')
    w = csv.writer(out)
    if mode == 'w':
        w.writerow(['reporter', 'partner', 'year', 'trade_usd'])

    for i, rep in enumerate(reporters):
        if rep in done:
            continue
        url = f'{BASE}/{rep}.XG_FOB_USD+MG_CIF_USD..A?startPeriod=1965&endPeriod=2025'
        try:
            req = urllib.request.Request(url, headers=HDR)
            with urllib.request.urlopen(req, timeout=120) as resp:
                text = resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            print(f'{rep}: FETCH FAIL {e}', flush=True)
            time.sleep(1.0)
            continue
        pair = {}
        try:
            r = csv.reader(io.StringIO(text))
            hdr = next(r, None)
            if not hdr or 'OBS_VALUE' not in hdr:
                print(f'{rep}: no data', flush=True)
                time.sleep(0.4)
                continue
            ci = {h: j for j, h in enumerate(hdr)}
            for row in r:
                try:
                    cp = row[ci['COUNTERPART_COUNTRY']]
                    yr = row[ci['TIME_PERIOD']]
                    val = row[ci['OBS_VALUE']]
                    if cp not in real3 or cp == rep or not val or not yr:
                        continue
                    v = float(val)
                    if v != v or v < 0:
                        continue
                    key = (cp, int(yr))
                    pair[key] = pair.get(key, 0.0) + v
                except (ValueError, IndexError):
                    continue
        except Exception as e:
            print(f'{rep}: PARSE FAIL {e}', flush=True)
            continue
        for (cp, yr), v in sorted(pair.items()):
            w.writerow([rep, cp, yr, f'{v:.0f}'])
        out.flush()
        print(f'[{i+1}/{len(reporters)}] {rep}: {len(pair)} pair-years', flush=True)
        time.sleep(0.4)
    out.close()
    print('DONE')


if __name__ == '__main__':
    main()
