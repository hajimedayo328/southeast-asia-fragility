# -*- coding: utf-8 -*-
# EMP指数の材料取得: 月次準備(IL: RXF11_REVS, USD) と 月次金利(MFS_IR: MMRT/DISR)
# 再開可能(出力CSVに既にある国はスキップ)
import sys, csv, time, io
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import false_positive_panel as fp

HDR = {'Accept': 'application/vnd.sdmx.data+csv;version=1.0.0',
       'User-Agent': 'research-script (academic use)'}


def fetch_loop(out_path, url_fmt, parse_row, header):
    meta = fp.load_real_countries()
    countries = sorted(meta)
    done = set()
    out_path = Path(out_path)
    if out_path.exists():
        with open(out_path, encoding='utf-8') as f:
            r = csv.reader(f); next(r, None)
            for row in r:
                done.add(row[0])
    mode = 'a' if out_path.exists() else 'w'
    out = open(out_path, mode, encoding='utf-8', newline='')
    w = csv.writer(out)
    if mode == 'w':
        w.writerow(header)
    for i, c in enumerate(countries):
        if c in done:
            continue
        url = url_fmt.format(c=c)
        try:
            req = urllib.request.Request(url, headers=HDR)
            with urllib.request.urlopen(req, timeout=120) as resp:
                text = resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            print(f'{c}: FETCH FAIL {e}', flush=True)
            time.sleep(0.5)
            continue
        n = 0
        try:
            r = csv.reader(io.StringIO(text))
            hdr = next(r, None)
            if not hdr or 'OBS_VALUE' not in hdr:
                print(f'{c}: no data', flush=True)
                time.sleep(0.25)
                continue
            ci = {h: j for j, h in enumerate(hdr)}
            for row in r:
                rec = parse_row(c, row, ci)
                if rec:
                    w.writerow(rec); n += 1
        except Exception as e:
            print(f'{c}: PARSE FAIL {e}', flush=True)
            continue
        out.flush()
        print(f'[{i+1}/{len(countries)}] {c}: {n} rows', flush=True)
        time.sleep(0.25)
    out.close()


def parse_reserves(c, row, ci):
    try:
        per = row[ci['TIME_PERIOD']]; val = row[ci['OBS_VALUE']]
        if not per or not val:
            return None
        v = float(val)
        if v != v or v <= 0:
            return None
        return [c, per, f'{v:.6g}']
    except (ValueError, IndexError):
        return None


def parse_rate(c, row, ci):
    try:
        ind = row[ci['INDICATOR']]
        per = row[ci['TIME_PERIOD']]; val = row[ci['OBS_VALUE']]
        if not per or not val:
            return None
        v = float(val)
        if v != v:
            return None
        return [c, per, ind.split('_')[0], f'{v:.6g}']
    except (ValueError, IndexError, KeyError):
        return None


def main():
    print('=== reserves (IL RXF11_REVS USD monthly) ===', flush=True)
    fetch_loop(ROOT / 'data_raw/il_reserves_monthly.csv',
               'https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IL,+/{c}.RXF11_REVS.USD.M?startPeriod=1970&endPeriod=2026',
               parse_reserves, ['iso3', 'period', 'reserves_usd'])
    print('=== rates (MFS_IR MMRT+DISR monthly) ===', flush=True)
    fetch_loop(ROOT / 'data_raw/mfs_rates_monthly.csv',
               'https://api.imf.org/external/sdmx/2.1/data/IMF.STA,MFS_IR,+/{c}.MMRT_RT_PT_A_PT+DISR_RT_PT_A_PT.M?startPeriod=1970&endPeriod=2026',
               parse_rate, ['iso3', 'period', 'kind', 'rate'])
    print('DONE')


if __name__ == '__main__':
    main()
