# -*- coding: utf-8 -*-
# BEA APIから業種別投資テーブルを特定して取得 (キーは.envから・ユーザーGO済み 2026-07-22)
import json, sys, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KEY = dict(l.split('=', 1) for l in open(ROOT / '.env', encoding='utf-8').read().splitlines() if '=' in l)['BEA_API_KEY'].strip()
BASE = 'https://apps.bea.gov/api/data/'


def q(**params):
    p = {'UserID': KEY, 'ResultFormat': 'JSON', **params}
    with urllib.request.urlopen(BASE + '?' + urllib.parse.urlencode(p), timeout=120) as r:
        return json.load(r)


def main():
    if sys.argv[1:] and sys.argv[1] == 'list':
        d = q(method='GetParameterValues', datasetname='FixedAssets', ParameterName='TableName')
        vals = d['BEAAPI']['Results']['ParamValue']
        for v in vals:
            desc = v.get('Description', '')
            if '3.7' in desc or 'by Industry' in desc[:60]:
                print(v['TableName'], '|', desc[:100])
        print('total:', len(vals))
    else:
        tbl = sys.argv[1]
        d = q(method='GetData', datasetname='FixedAssets', TableName=tbl, Year='ALL')
        data = d['BEAAPI']['Results']['Data']
        out = ROOT / f'data_raw/bea_{tbl}.json'
        json.dump(data, open(out, 'w', encoding='utf-8'))
        lines = {x['LineDescription'] for x in data}
        yrs = sorted({x['Year'] for x in data})
        print(f'{out}: {len(data)} rows, {len(lines)} lines, years {yrs[0]}-{yrs[-1]}')
        for l in sorted(lines)[:25]:
            print(' ', l[:70])


if __name__ == '__main__':
    main()
