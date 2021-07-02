import urllib
import requests
import urllib.request
import json
import datetime
import pandas as pd
import tushare as ts
from urllib3.exceptions import InsecureRequestWarning
import json


class GP:
    def __init__(self):
        '''
        函数名                    功能                 参数
        ztg                      未知                20210308
        getklinetoday            未知                 0000001
        getklinehistory          未知               2021，0000001
        getdata             东方财富数据爬虫          rename(字典)
        generatecsv              未知                20210305
        get_data            华龙证券实时数据            无参数
        shh                    上证指数                无参数
        get                未知(其他模块调用)         datafram(字典)
        bkjx                  板块强度排序              整数
        bkcode             获取板块里面的个股          0000001, 20
        kpl                  获取开盘啦数据              无参数
        '''
        pass

    def return_result(self):
        return self.result

    @classmethod
    def ztg(cls, day):
        '''

        :param day:20210308
        :return:
        '''
        # http://stock.jrj.com.cn/tzzs/zdforce.shtml?to=pc
        url = 'http://home.flashdata2.jrj.com.cn/limitStatistic/ztForce/' + day + '.js'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

        response = requests.get(url, headers=headers)
        json_str = response.content.decode('gbk')
        json_str = json_str.replace('var yzb_ztForce=', '')
        index = json_str.find('Data')
        # print(index)
        data = json_str[index:]

        data = data.replace('Data:', '')
        data = data.replace('}', '')
        data = data[6:-1]

        data = json.loads(data)
        hi = pd.DataFrame(data)

        hi.columns = ['stockcode', 'stockname', 'nowPrice', 'priceLimit', 'fcb', 'flb', 'fdMoney', 'firstZtTime',
                      'lastZtTime', 'opentime', 'zhenfu', 'force']

        hi['day'] = day

        return hi

    @classmethod
    def getklinetoday(cls, code):
        '''

        :param code:股票代码
        :return:
        '''
        url = 'http://img1.money.126.net/data/hs/time/today/'
        url = url + code + '.json'
        r = requests.get(url)
        sh = pd.DataFrame(eval(r.text))
        sh = list(sh['data'])
        sh = pd.DataFrame(sh)
        #    print('sh')

        sh.columns = ['time', 'sh_price', 'sh_mean', 'sh_vol']

        sh['sh_p'] = sh['sh_price'].diff()

        for i in [5, 10, 20]:
            for j in ['sh_price', 'sh_p', 'sh_vol']:
                sh[str(j) + str(i)] = sh.rolling(i)[j].mean()
        return sh

    @classmethod
    def getklinehistory(cls, year, code):
        '''

        :param year:时间  2021
        :param code: 股票代码 0000001
        :return:
        '''
        url = 'http://img1.money.126.net/data/hs/kline/day/history/'

        url = url + year + '/' + code + '.json'

        r = requests.get(url)
        sh = pd.DataFrame(eval(r.text))

        sh = list(sh['data'])
        sh = pd.DataFrame(sh)

        sh.columns = ['date', 'open', 'close', 'high', 'low', 'vol', 'p']

        for j in [5, 10, 20]:
            for i in ['p', 'close', 'vol']:
                sh['sh_' + i + str(j)] = sh[i].rolling(j).mean()
        return sh

    @classmethod
    def getdata(cls, rename):
        '''
        东方财富数据爬虫
        :return: {
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
        '''
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

    @classmethod
    def generatecsv(cls, startdate):
        '''

        :param startdate:20210305
        :return:
        '''
        pro = ts.pro_api('7322d9b3de6e6f0a650c5f3a70ca121cb35006a52a1c8c46ee7f0c63')
        OpenList = pro.trade_cal(start_date=startdate)

        DatetimeNOW = datetime.datetime.now().strftime('%Y%m%d')
        kai = OpenList[(OpenList.cal_date < DatetimeNOW) & (OpenList.is_open == 1)]['cal_date']

        zt = pd.DataFrame()

        for i in kai:
            zt = zt.append(cls.ztg(i))
            print(i)
        return zt

    @classmethod
    def get_data(cls):
        '''
        华龙证券实时数据
        :return:
        '''
        url = '''https://trade.hlzq.com/market/json?funcno=21000&version=1&sort=24&order=1&type=0:2:9:18&curPage=1&rowOfPage=4030&field=1:2:9:12:14:22:24:7:8:15:29:30'''
        strhtml = requests.get(url)  # Get方式获取网页数据
        strhtml = strhtml.text
        data = eval(strhtml)['results']
        df = pd.DataFrame(data, columns=['涨幅', '现价', '今开', '昨收', '总金额', 'name', 'code', '涨速', '换手', '量比', '委差', '委比'])

        # 把 name 包括 st，退，重命名一列叫st，01
        #  df = df[ ~(df.name.str.contains("ST"))  &  ((df['总金额'] >  200000 ))]   #去掉st
        df["量比"][df.量比 >= 9999.00] = 9999.99  # 有时候，量比会非常大，替换一下，要不然插入会有问题

        return df

    @classmethod
    def shh(cls):
        '''
        获取 上证指数 ？？？？
        :return:
        '''
        url = '''http://api.money.126.net/data/feed/0000001,UD_SHAZ,UD_SHAD,UD_SHAP,money.api?callback=_ntes_quote_callback83569787'''
        strhtml = requests.get(url, stream=True)  # Get方式获取网页数据
        strhtml = strhtml.text
        data = (strhtml[28:-1])

        dat = eval(data)
        df1 = dat['0000001']

        df1['sh_up'] = dat['UD_SHAZ']['count']
        df1['sh_zero'] = dat['UD_SHAP']['count']
        df1['sh_down'] = dat['UD_SHAD']['count']

        print(df1)
        return df1

    def get(self, df):
        # 构造URL请求、user-agent头文件
        url = 'https://pchq.kaipanla.com/w1/api/index.php'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}
        session = requests.Session()
        # 禁用安全请求警告
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        html = session.post(url=url, data=df, headers=headers, verify=False).text
        ddf = eval(html)
        return ddf

    def bkjx(self, M):
        '''
        根据强度排序，获得板块, 获取强度前M行
        :param M:int
        :return:
        '''

        jx = {

            'c': 'PCArrangeData',
            'a': 'GetZSIndexPlate',
            'SelType': '2',
            'ZSType': '7',
            'PType': '1',
            'POrder': '1',

            'PStart': '',
            'PEnd': '',

            'PIndex': '0',
            'Pst': M,
            'UserID': '925781',
            'Token': '846a4fedd362a0fd18d7bf51e534e26b'}

        jx_df = self.get(jx)
        jxdata = pd.DataFrame(jx_df['plates']['list'])
        jxdata.rename(
            columns={0: 'PlateID', 1: 'Pname', 2: 'P强度', 3: 'P涨幅', 4: 'P涨速', 5: 'P成交额', 6: 'P主力净额', 7: 'P主力买入',
                     8: 'P主力卖出',
                     9: 'P量比', 10: 'P流通市值', 11: 'd2', 12: 'd3'}, inplace=True)

        jxdata['P强度rank'] = jxdata['P强度'].rank()
        jxdata['P涨幅rank'] = jxdata['P涨幅'].rank()
        jxdata['P量比rank'] = jxdata['P量比'].rank()
        jxdata['P涨速rank'] = jxdata['P涨速'].rank()
        jxdata['P主力净额rank'] = jxdata['P主力净额'].rank()

        return jxdata

    def bkcode(self, PlateID, N):
        # 获取板块里面的个股
        codes = {'c': 'PCArrangeData',
                 'a': 'GetZSIndexPlate',
                 'SelType': '3',
                 'LType': '6',
                 'LOrder': '1',
                 'LStart': '',
                 'LEnd': '',
                 'LIndex': '0',
                 'Lst': N,
                 'PlateID': PlateID,
                 'UserID': '925781',
                 'Token': '846a4fedd362a0fd18d7bf51e534e26b'}

        code_df = self.get(codes)
        codedata = pd.DataFrame(code_df['stocks']['list'])
        codedata.rename(
            columns={0: 'code', 1: 'name', 2: '价格', 3: '涨幅', 4: '成交额', 5: '换手率', 6: '涨速', 7: '实际流通', 8: '主力买入',
                     9: '主力卖出',
                     10: '主力净额', 11: '区间涨幅', 12: '概念'}, inplace=True)

        codedata['PlateID'] = PlateID
        codedata['涨幅rank'] = codedata['涨幅'].rank()
        codedata['涨速rank'] = codedata['涨速'].rank()

        return codedata

    @classmethod
    def kpl(cls):
        import requests
        import json
        data = {
            'c': 'StockRanking',
            'a': 'RealRankingInfo',
            'Ratio': '5',
            'Type': '6',
            'Order': '1',
            'index': '0',
            'st': '35',
            'UserID': '1068777',
            'Token': '5361442d34c60640a2b34727d80a67a0'}
        url = 'https://pchq.kaipanla.com/w1/api/index.php'
        headers = {
            'Host': 'pchq.kaipanla.com',
            'Origin': 'https://www.kaipanla.com',
            'Referer': 'https://www.kaipanla.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
        }
        r = requests.post(url=url, headers=headers, data=data)
        data = json.loads(r.text)
        return data


if __name__ == '__main__':
    # math列表传入函数名,params为函数所需要参数,无需传参则传入空字符串,多个参数则用列表
    math = ['kpl', 'ztg', 'getklinehistory', 'get_data']  # 函数名
    params = ['', '20210308', ['2021', '0000001'], '']  # 参数
    gupiao = eval('GP')()  # 类实例化
    for n in range(len(math[:1])):  # 循环执行函数
        try:
            if params[n] == '':
                r = getattr(gupiao, math[n])()
            elif type(params[n]) is str:
                r = getattr(gupiao, math[n])(params[n])
            else:
                r = getattr(gupiao, math[n])(*params[n])
            print(r)
        except Exception as e:
            print('错误函数:', math[n])
            print('错误原因:', e)
