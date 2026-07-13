# IMF ER データセットから月次為替レート(XDC_USD=自国通貨/米ドル, 月末値)を全世界分取得
# 再開可能: 出力CSVに既にある国はスキップ。用途: 危機の月次日付け(嵐の解剖・月次版)
import sys, csv, time, io
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp

OUT = ROOT / 'data_raw/er_monthly.csv'
BASE = 'https://api.imf.org/external/sdmx/2.1/data/IMF.STA,ER,+'
HDR = {'Accept': 'application/vnd.sdmx.data+csv;version=1.0.0',
       'User-Agent': 'research-script (academic use)'}


def main():
    meta = fp.load_real_countries()
    countries = sorted(meta)
    print(f'countries: {len(countries)}')

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
        w.writerow(['iso3', 'period', 'lcu_per_usd'])

    for i, c in enumerate(countries):
        if c in done:
            continue
        url = f'{BASE}/{c}.XDC_USD.EOP_RT.M?startPeriod=1970&endPeriod=2026'
        try:
            req = urllib.request.Request(url, headers=HDR)
            with urllib.request.urlopen(req, timeout=120) as resp:
                text = resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            print(f'{c}: FETCH FAIL {e}', flush=True)
            time.sleep(0.6)
            continue
        n = 0
        try:
            r = csv.reader(io.StringIO(text))
            hdr = next(r, None)
            if not hdr or 'OBS_VALUE' not in hdr:
                print(f'{c}: no data', flush=True)
                time.sleep(0.3)
                continue
            ci = {h: j for j, h in enumerate(hdr)}
            for row in r:
                try:
                    per = row[ci['TIME_PERIOD']]
                    val = row[ci['OBS_VALUE']]
                    if not per or not val:
                        continue
                    v = float(val)
                    if v != v or v <= 0:
                        continue
                    w.writerow([c, per, f'{v:.8g}'])
                    n += 1
                except (ValueError, IndexError):
                    continue
        except Exception as e:
            print(f'{c}: PARSE FAIL {e}', flush=True)
            continue
        out.flush()
        print(f'[{i+1}/{len(countries)}] {c}: {n} months', flush=True)
        time.sleep(0.3)
    out.close()
    print('DONE')


if __name__ == '__main__':
    main()
