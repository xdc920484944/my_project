import urllib.request
import pandas as pd
import urllib

# 获取数据=================================
rename = {
    'f12': 'code',
    'f14': 'name',
    'f26': '上市日期',

    'f3': '涨幅',
    'f7': '振幅',
    'f8': '换手',
    'f10': '量比',

    'f33': '委比',
    'f34': '外盘',
    'f35': '内盘',

    'f211': '买一量',
    'f212': '卖一量',

    'f17': '今开',
    'f18': '昨收',
    'f15': '最高',
    'f16': '最低',

    'f2': '现价',
    'f30': '现手',

    'f20': '总市值',
    'f21': '流通市值',
    'f46': '净利润同比',
    'f67': '总收入同比',

    'f9': '动态市盈率',
    'f23': '市净率',
    'f57': '负债率',

    'f5': '成交量',
    'f6': '成交额',

    'f184': 'net',
    'f69': 'net1',
    'f75': 'net2',
    'f81': 'net3',
    'f87': 'net4',

    'f22': 'up2M',
    'f11': 'up5M',
    'f127': 'up3D',
    'f160': 'up10D',
    'f24': 'up60D'

}

col = str(list(rename.keys()))
s = col[1:-1].replace("'", '').replace(" ", '')
url = 'http://56.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields='
url = url + s

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Referer': 'http://quote.eastmoney.com/center'}
opener = urllib.request.build_opener()
opener.addheaders = [headers]
data = opener.open(url, timeout=5).read().decode('utf-8')  # 超时时间 20s

d = eval(data)['data']['diff']
data = pd.DataFrame(d)
record = data.replace('-', '', inplace=False, )
col = eval(col)
record[col] = record[col].apply(pd.to_numeric, errors='ignore')

record['f12'] = record['f12'].astype('str').str.zfill(6)
record["f10"][record.f10 >= 9999.00] = 9999.99
result = record.rename(columns=rename, inplace=True)
print(result)