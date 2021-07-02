from bs4 import BeautifulSoup
from time import sleep
import requests
import datetime

try:
    from 我的工具 import xie_xls
except:
    import xie_xls

import sys
import re


def qing(url, xuan01, cookie01=''):
    while 1:
        try:
            if xuan01 == 0:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
                    # 'cookie':cookie01
                }
            else:
                headers = {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
                    # 'cookie': cookie01
                }

            if cookie01:
                headers['cookie'] = cookie01

            # 忽略不验证证书出现的警告,proxies=http
            requests.packages.urllib3.disable_warnings()

            r = requests.get(url, headers=headers, verify=False, timeout=10)
            r.encoding = 'utf-8'
            print(url)

            return r.text

        except Exception as e:
            print('请求错误：', e)
            sleep(1)


cookie01 = 'wpr=0; BAIDUID=1CA59ED3F4C108F48FBBA6C522D6ECD8:FG=1; __yjs_duid=1_09744cdcf68e117d1c86acb94f1eedff1612512566992; BIDUPSID=1CA59ED3F4C108F48FBBA6C522D6ECD8; PSTM=1612532388; delPer=0; BD_CK_SAM=1; shifen[217779364705_49566]=1613911157; shifen[21768983370_85079]=1613911742; BCLID=10160887919160527112; BDSFRCVID=TkAOJeC62myFKmTe-RU1UnZTye2-44TTH6aoMYXUSiw4ih3EpnkYEG0PJM8g0Ku-SoRAogKKQgOTHRPF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tb48VI0KfC83j-0z5KTs2J88Kl-X5-RLHD7XVbThBp7keq8CDxQ5hUAdhU_LQtJnQCoz-PTHbPJhbJO2y5jHhTtsQx6X5jF8Qb7H-fokbR6psIJMeh_WbT8U5f5HQ5j-aKviaMjjBMb1VxJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe6oyjNLHJjtsKKJ03bvb54o-ejrg-J5MKPL_Kxb3et6-bn3nBhjvWJ5TMCoz2fjvhq08qJ5PJlQXyHn80C_EJIbxShPC-tnYWqkA0UrftPc3t2TjWJvw3l02VhcEe-t2ynQD0UnN34RMW23I0h7mWUomsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKDGtjJT3P; BCLID_BFESS=10160887919160527112; BDSFRCVID_BFESS=TkAOJeC62myFKmTe-RU1UnZTye2-44TTH6aoMYXUSiw4ih3EpnkYEG0PJM8g0Ku-SoRAogKKQgOTHRPF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tb48VI0KfC83j-0z5KTs2J88Kl-X5-RLHD7XVbThBp7keq8CDxQ5hUAdhU_LQtJnQCoz-PTHbPJhbJO2y5jHhTtsQx6X5jF8Qb7H-fokbR6psIJMeh_WbT8U5f5HQ5j-aKviaMjjBMb1VxJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe6oyjNLHJjtsKKJ03bvb54o-ejrg-J5MKPL_Kxb3et6-bn3nBhjvWJ5TMCoz2fjvhq08qJ5PJlQXyHn80C_EJIbxShPC-tnYWqkA0UrftPc3t2TjWJvw3l02VhcEe-t2ynQD0UnN34RMW23I0h7mWUomsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKDGtjJT3P; BD_HOME=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; SE_LAUNCH=5%3A1614059714; MSA_PBT=150; MSA_ZOOM=1056; BD_UPN=14314654; G_PSCBD=105%3A1; G_LAUNCH=105%3A26901004; wpr=0; BDICON=10294984.98; MSA_WH=375_812; MSA_PHY_WH=1125_2436; BA_HECTOR=al2l4h2kkb8kak8hcb1g39aej0q; COOKIE_SESSION=536_22_3_9_2_w1_65_9_44_3_0_4_270_1614064614%7C9%230_0_0_0_0_0_0_0_1614059713%7C1; ab_sr=1.0.0_MWRiOGM1MWMxNGI5YTE2YTc5MTY5Y2RjYjRjY2YyM2RiNjczMjc4ODkwOWZiMzg0NDQ3NGUwMjE0NjQyY2RjMDNhYTFlYzQ2MjFkZGYzMWI1YjdlOGZiZjg1Nzc1NjA0; H_WISE_SIDS=107319_110085_127969_131423_131862_144966_154619_155930_156288_156928_160662_162372_162898_163568_164075_164215_164456_164954_165133_165136_165329_166147_166184_166334_166691_166830_167069_167112_167391_167536_167602_168310_168495_168501_168543_168570_168632_168703_168763_168797_168909_168914_169065_169165_169307_169660_169669_169697; BDSVRTM=70; FC_MODEL=0.28_20_36_0_0_0_2_0_0_0_0_0.28_7_65_7_62_0_1614066982_1614064614%7C9%230_0.28_0.28_7_7_1614066982_1614064614%7C9%230_nmghghghx_0_3_3_0_0_1614064614'

xx02 = ['办公室出租', '写字楼出租', '合肥办公室', '合肥写字楼', '瑶海区写字楼', '庐阳区写字楼', '包河区写字楼', '滨湖区写字楼', '蜀山区写字楼', '经开区写字楼', '政务区写字楼',
        '高新区写字楼']
xx01 = '''办公室出租
写字楼出租
合肥办公室
合肥写字楼
瑶海区写字楼
庐阳区写字楼
包河区写字楼
滨湖区写字楼
蜀山区写字楼
经开区写字楼
政务区写字楼
高新区写字楼
'''

yue01 = xie_xls.xie_xls('爬虫结果.xls')
yue01.chuangbiao([])

nowtime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
nowtime01 = datetime.datetime.now().strftime('%H:%M:%S')  # 现在

riqi01 = nowtime01.split(':')
riqi02 = int(riqi01[0])

riqi03 = ''
if 12 >= riqi02 >= 8:
    riqi03 = '上午'
elif 18 >= riqi02 >= 14:
    riqi03 = '下午'
else:
    riqi03 = nowtime01

sj01 = nowtime + ' ' + riqi03
print('时间：', sj01)

yue01.xiubiao02(['统计人：  日期：{}'.format(sj01), '合肥百度推广日常关键字搜索情况表'])
yue01.xiubiao02(['', '地点', ''] + xx02)

nr01 = []
nr02 = []

y02 = 0
for y02 in range(0, len(xx02)):
    print('*' * 120)
    print('第{}个。。。。。。'.format(y02))

    gjc01 = xx02[y02]
    url01 = 'https://www.baidu.com/s?ie=utf-8&wd={}'.format(gjc01)
    for y01 in range(2):
        a01 = 0
        while 1:
            a01 = a01 + 1
            if a01 > 6:
                input('超出重试次数*****************')
                sleep(10)

            data01 = qing(url01, y01)
            # print([data01])

            if data01.find('请稍后重试</div>') != -1:
                print('请求异常*************')
                sleep(1)
            else:
                break

        bs01 = BeautifulSoup(data01, 'lxml')

        n01 = bs01.select('article')
        print('个数：', len(n01))

        zhuan01 = []
        if y01 == 0:
            n02 = [bs01.find('div', id="300{}".format(n + 1)) for n in range(5)]
            n002 = []
            for n in n02:
                if n:
                    n002.append([m.text for m in n.find_all('span') if m.text is not None and '.' in m.text])
            if len(n002) < 5:
                n3 = bs01.select('a[class="c-showurl c-color-gray"]')
                n4 = [x.text for x in n3]
                n002 += n4[:5 - len(n002)]

            zhuan01 = n002

            nr01.append(n002)
        else:
            with open('22.html', 'w', encoding='utf-8') as f:
                f.write(data01)
            n03 = bs01.find_all(['div'], {'data-module': ['c-f', 'c-sm', 'c-sr']})
            n003 = [x.text.replace('\ue63c', '') for x in n03]
            zhuan01 = n003

            nr02.append(n003)

        print(zhuan01)
        print('结果个数：', len(zhuan01))
        # nr01.append(zhuan01)

v01 = []
for i01 in range(0, 5):
    zhuan02 = ['PC', '蓝海', '第{}名'.format(i01 + 1)]
    zhuan03 = []
    for i02 in range(0, len(nr01)):
        v02 = nr01[i02]
        zhuan03.append(v02[i01] if len(v02) > i01 else '-')

    print('内容：', zhuan02 + zhuan03)
    yue01.xiubiao02(zhuan02 + zhuan03)

yue01.xiubiao02(['', ''])
yue01.xiubiao02(['', '', ''] + xx02)

v01 = []
for i01 in range(0, 5):
    zhuan02 = ['手机', '蓝海', '第{}名'.format(i01 + 1)]
    zhuan03 = []
    for i02 in range(0, len(nr02)):
        v02 = nr02[i02]
        zhuan03.append(v02[i01] if len(v02) > i01 else '-')

    print('内容：', zhuan02 + zhuan03)
    yue01.xiubiao02(zhuan02 + zhuan03)

print('程序运行完成。。。。。。。。。。。。。。。。。。。。。。。。。。。。')

while 1:
    input('>>>')
