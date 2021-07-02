import json
import os
from datetime import datetime
import pandas as pd
import tushare as ts
import datetime
import numpy as np

class GG_RXHQ:
    def __init__(self, ts_code='', start_date='', end_date=''):
        self.pro = ts.pro_api(token='a51a57028c1ab1aa459a2fad7ebb6696e527443e75ec6f7e35a038bd')
        self.root_path = os.path.abspath('.')
        self.accuracy = 3  # 计算结果保留位数
        self.end_date = end_date
        self.start_date = start_date
        self.ts_code = ts_code
        df = self.pro.hk_daily(ts_code=self.ts_code, start_date=self.start_date, end_date=self.end_date)
        self.data = self.deal_data(df.to_dict())
        # self.data = self.deal_data(pd.read_excel('test_data.xlsx').to_dict())

    # =================== 工具函数 ===================
    def filter_accuracy(self, i):
        '''
        将计算结果保留self.accuracy位小数
        :param i: float 计算结果
        :return: float
        '''
        i = str(i).split('.')
        i[-1] = i[-1][:self.accuracy]
        i = float('.'.join(i))
        return i

    @staticmethod
    def deal_data(origin_data):
        '''
        处理源数据，按不同的字段分出列表
        :param origin_data: 源数据
        :return: dict
        '''
        key_list = ['trade_date', 'ts_code', 'open', 'high', 'low', 'close', 'pre_close', 'pct_chg',
                    'change', 'vol', 'amount']
        data = {}
        for key in key_list:
            d = list(origin_data[key].values())
            if not d:
                raise Exception('数据获取错误{}对应数据长度:{}'.format(key, len(d)))
            d.reverse()
            data[key] = d
        return data

    def get_satisfy_list(self, key, date, days):
        '''
        获取self.data中的数据
        :param key: 关键词
        :param date: 日期
        :param days: 前推天数
        :return: list []
        '''

        if date not in self.data['trade_date']:
            raise Exception('{}为非交易日，请重新输入'.format(date))
        if not days or int(days) > len(self.data['trade_date']):
            result = self.data[key]
        else:
            index1 = self.data['trade_date'].index(date) + 1
            # if index1 < days:
            #     raise Exception('交易数据{}小于交易天数{}'.format(index1, days))
            result = self.data[key][index1 - days:index1]
        return result

    def show_all_code(self):
        '''
        获取所有港股股票代码
        :return:
        '''
        df = self.pro.hk_basic()
        df = df.to_dict()
        return df

    def get_data(self, all_result):
        '''
        获取港股日线行情数据
        输入:
            ts_code	str	N	股票代码
            trade_date	str	N	交易日期
            start_date	str	N	开始日期
            end_date	str	N	结束日期
        输出:
            ts_code	str	Y	股票代码
            trade_date	str	Y	交易日期
            open	float	Y	开盘价
            high	float	Y	最高价
            low	float	Y	最低价
            close	float	Y	收盘价
            pre_close	float	Y	昨收价
            change	float	Y	涨跌额
            pct_chg	float	Y	涨跌幅(%)
            vol	float	Y	成交量(股)
            amount	float	Y	成交额(元)
        :param all_result:
        :return:
        '''

        def save_df():
            if not os.path.isdir(path):
                os.makedirs(path)
            df.to_csv(os.path.join(path, file_name))

        if self.ts_code:
            # 多日单股
            # df = self.pro.hk_daily(ts_code=self.ts_code, start_date=self.start_date, end_date=self.end_date)
            df = pd.DataFrame(all_result)
            path = os.path.join(self.root_path, 'all_share')
            file_name = self.start_date + '.csv'
        else:
            # 单日全股
            df = self.pro.hk_daily(trade_date=self.start_date)
            path = os.path.join(self.root_path, 'one_share')
            file_name = str(int(datetime.datetime.now().timestamp())) + '.csv'

        # 数据保存csv
        save_df()
        result = df.to_dict()
        return result, path, file_name

        # =================ave_line=================

    # 1 2 3 4 5
    def ave_line_calc(self, date, days):
        '''
        求日线 10 20 50 250
        :param date:日期
        :param days:开盘天数
        :return: int ave_line 平均值
        '''
        close_list = self.get_satisfy_list(key='close', date=date, days=days)
        if len(close_list) >= days:
            ave_line = sum(close_list) / len(close_list)
        else:
            ave_line = None
        return ave_line

    # 6
    def ave_line_compare(self, date=None, ave_line_list=None):
        '''
        10 20 50日线比较
        :param ave_line_list: [(ave_line_10, ave_line_20, ave_line_50), (), ...]
        :param date:list [('20200102', 10), ('20200102', 20), ('20200102', 50)]
        :return: list 比较结果 ['Y'or'N', 'Y'or'N']
        '''

        if date:
            a10 = self.ave_line_calc(date, 10)
            a20 = self.ave_line_calc(date, 20)
            a50 = self.ave_line_calc(date, 50)
            key = 'Y' if a10 > a20 > a50 else 'N'

        elif ave_line_list and None not in ave_line_list:
            a1, a2, a3 = ave_line_list
            key = 'Y' if a1 > a2 > a3 else 'N'
        else:
            key = None
        # print('功能:日线比较\t时间:{}\t结果:{}:'.format(date, key))
        return key

    # =================== RSI ===================

    @staticmethod
    def avg_Gain_Loss(Gain=None, pre=None, _list=None):
        '''

        :param Gain:
        :param pre:
        :param _list:
        :return:
        '''
        if Gain is not None:
            avg = (pre * 13 + Gain) / 14
        else:
            avg = sum(_list) / 14
        return avg

    # ================= EMA =================
    # 13 14
    def EMA(self, index, days, pre_EMA):
        '''
        求EMA 公式：EMA(n)=(前一日EMA(n) × (n-1)+今日收盤價 × 2) ÷ (n+1)
        (close*(2/(12+1)))+(pre_EMA*(1-(2/(12+1))))
        :param days: 12/26
        :param pre_EMA: 前一天的12/26EMA
        :param index:
        :return: list/int
        '''
        if pre_EMA:
            close = self.data['close'][index]
            EMA = (close * (2 / (days + 1))) + (pre_EMA * (1 - (2 / (days + 1))))
        else:
            EMA = sum(self.data['close'][:days]) / days
        return EMA

    # 16
    def EMA_9_of_MACD(self, MACD=None, pre_9_EMA_of_MACD=None, MACD_list=None):
        '''
        (MACD*(2/(9+1)))+(pre_9_EMA_of_MACD*(1-(2/(9+1))))
        :param MACD_list:
        :param MACD:
        :param pre_9_EMA_of_MACD:
        :return:
        '''
        if MACD_list:
            EMA_9_of_MACD = sum(MACD_list) / 9
        else:
            EMA_9_of_MACD = (MACD * (2 / (9 + 1))) + (pre_9_EMA_of_MACD * (1 - (2 / (9 + 1))))
        return EMA_9_of_MACD

    # =================== 基础运算 ===================
    # 18
    def MOM(self, index):
        '''
        動力指標 (預設值:10) MTM=当日收盘价-10日前收盘价
        :param index: str 时间
        :return:
        '''
        if index > 9:
            MOM = self.data['close'][index] - self.data['close'][index - 10]
        else:
            MOM = self.data['close'][index]
        return MOM

    # 19
    @staticmethod
    def ave_pct_chg(pct_chg_list):
        '''
        過去4天平均漲跌幅(%) 過去4天平均漲跌幅 ÷ 4
        AVERAGE(J3001:J3004)/100
        :param pct_chg_list:
        :return:
        '''
        ave_pre_close_value = sum(pct_chg_list) / len(pct_chg_list)
        return ave_pre_close_value

    # 20
    def ROC(self, index):
        '''
        变动速度指标 当日收市价与 N 日前的收市价的差，除以 N 日前的收市价，再乘以 100 。 N 的缺省值为 12
        1、AX=今日收盘价-N日前收盘价
        2、BX=N日前收盘价
        3、ROC=AX/BX
        (G2991-G3001)/G3001*100
        :param index: str 时间
        :return:
        '''
        now = self.data['close'][index]
        ago = self.data['close'][index - 10]
        ROC = (now - ago) / ago * 100
        return ROC

    @staticmethod
    def ATR(TR=None, pre_ATR=None, TR_list=None):
        if TR:
            ATR = (pre_ATR * 13 / 14) + (TR / 14)
        else:
            ATR = sum(TR_list) / 14
        return ATR

    @staticmethod
    def DM_14_EMA(DM=None, pre_DM_14=None, DM_list=None):
        '''

        :param DM:
        :param pre_DM_14:
        :param DM_list:
        :return:
        '''
        if DM is not None:
            DM_14_EMA = (1 - 1 / 14) * pre_DM_14 + (1 / 14 * DM)
        else:
            DM_14_EMA = sum(DM_list) / 14
        return DM_14_EMA

    @staticmethod
    def ADX(DX=None, pre_ADX=None, DX_list=None):
        '''

        :param DX:
        :param pre_ADX:
        :param DX_list:
        :return:
        '''
        if DX is not None:
            ADX = (pre_ADX * 13 + DX) / 14
        else:
            ADX = sum(DX_list) / 14
        return ADX

    def main(self):

        all_result = []
        trade_date_list = self.data['trade_date']

        for date in trade_date_list:
            result = {}
            index = self.data['trade_date'].index(date)
            # =======================base_data=======================
            key_list = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'pct_chg', 'change',
                        'vol', 'amount']
            for key in key_list:
                result[key] = self.data[key][index]
            # =======================ave_line=======================
            if index > 8:
                result['10SMA'] = sum(self.data['close'][index-9:index+1]) / 10
            if index > 18:
                result['20SMA'] = self.ave_line_calc(date=date, days=20)
            if index > 48:
                result['50SMA'] = self.ave_line_calc(date=date, days=50)
            if index > 248:
                result['250SMA'] = self.ave_line_calc(date=date, days=250)
            if index > 48:
                result['10SMA>20SMA>50SMA'] = self.ave_line_compare(
                    ave_line_list=[result['10SMA'], result['20SMA'], result['50SMA']])
            if index > 18:
                result['10SMA-20SMA'] = result['10SMA'] - result['20SMA']
            if index > 48:
                result['20SMA-50SMA'] = result['20SMA'] - result['50SMA']
            if index > 48:
                if index == 49:
                    result['No. of days of 10SMA>20SMA>50SMA'] = 1 if result['10SMA>20SMA>50SMA'] == 'Y' else 0
                else:
                    result['No. of days of 10SMA>20SMA>50SMA'] = all_result[-1]['No. of days of 10SMA>20SMA>50SMA']\
                                                                 + 1 if result['10SMA>20SMA>50SMA'] == 'Y' else 0
            # =======================RSI=======================
            change = self.data['change'][index]
            result['Gain'] = change if change > 0 else 0
            result['Loss'] = abs(change) if change < 0 else 0
            if index > 12:
                if index == 13:
                    Gain_list = [r['Gain'] for r in all_result[:index]] + [result['Gain']]
                    result['avg_Gain'] = self.avg_Gain_Loss(_list=Gain_list)
                    Loss_list = [r['Loss'] for r in all_result[:index]] + [result['Loss']]
                    result['avg_Loss'] = self.avg_Gain_Loss(_list=Loss_list)
                else:
                    pre_avg_Gain = all_result[-1]['avg_Gain']
                    result['avg_Gain'] = self.avg_Gain_Loss(Gain=result['Gain'], pre=pre_avg_Gain)

                    pre_avg_Gain = all_result[-1]['avg_Loss']
                    result['avg_Loss'] = self.avg_Gain_Loss(Gain=result['Loss'], pre=pre_avg_Gain)
            if index > 12:
                result['RS'] = result['avg_Gain'] / result['avg_Loss']
            if index > 12:
                result['14RSI'] = 100 - (100 / (result['RS'] + 1))
            if index > 20:
                RSI_list = [r['14RSI'] for r in all_result[index - 8:]] + [result['14RSI']]
                result['9SMA (14RSI)'] = sum(RSI_list) / 9
            if index > 20:
                result['14RSI÷9SMA-1 (%)'] = (result['14RSI'] / result['9SMA (14RSI)'] - 1) * 100
            # =======================EMA=======================
            if index > 10:
                pre_12_EMA = all_result[-1].get('12 EMA', None)
                result['12 EMA'] = self.EMA(index=index, days=12, pre_EMA=pre_12_EMA)
            if index > 24:
                pre_26_EMA = all_result[-1].get('26 EMA', None)
                result['26 EMA'] = self.EMA(index=index, days=26, pre_EMA=pre_26_EMA)
            if index > 24:
                result['MACD (12, 26)'] = result['12 EMA'] - result['26 EMA']
            if index > 32:
                if index == 33:
                    MACD_list = [r['MACD (12, 26)'] for r in all_result[-8:]] + [result['MACD (12, 26)']]
                    result['9EMA of MACD'] = self.EMA_9_of_MACD(MACD_list=MACD_list)  # MACD与EMA错误导致diff错误
                else:
                    MACD = result['MACD (12, 26)']
                    pre_EMA_9_of_MACD = all_result[-1]['9EMA of MACD']
                    result['9EMA of MACD'] = self.EMA_9_of_MACD(MACD=MACD, pre_9_EMA_of_MACD=pre_EMA_9_of_MACD)
            if index > 32:
                result['Diff'] = result['MACD (12, 26)'] - result['9EMA of MACD']
            # =======================other=======================
            result['MOM or MTM(interval 10)'] = self.MOM(index=index)
            if index > 3:
                pct_chg_list = self.data['pct_chg'][index - 3:index] + [self.data['pct_chg'][index]]
                result['Avg changing percentage of last 4 days'] = self.ave_pct_chg(pct_chg_list=pct_chg_list)
            if index > 9:
                result['ROC (interval 10)'] = self.ROC(index=index)
            result['H-L'] = self.data['high'][index] - self.data['low'][index]
            result['H-PC'] = self.data['high'][index] - self.data['pre_close'][index]
            result['L-PC'] = self.data['low'][index] - self.data['pre_close'][index]
            result['TR'] = max(result['H-L'], result['H-PC'], result['L-PC'])
            if index > 12:
                if index == 13:
                    TR_list = [r['TR'] for r in all_result[:index]] + [result['TR']]
                    result['ATR (14EMA) B'] = self.ATR(TR_list=TR_list)
                else:
                    pre_ATR = all_result[-1]['ATR (14EMA) B']
                    result['ATR (14EMA) B'] = self.ATR(TR=result['TR'], pre_ATR=pre_ATR)
            if index > 0:
                result['H-pH'] = self.data['high'][index] - self.data['high'][index - 1]
            if index > 0:
                result['pL-L'] = self.data['low'][index - 1] - self.data['low'][index]
            if index > 0:
                result['_+DM'] = result['H-pH'] if result['H-pH'] > result['pL-L'] and result['H-pH'] > 0 else 0
                result['_-DM'] = result['pL-L'] if result['pL-L'] > result['H-pH'] and result['pL-L'] > 0 else 0
            if index > 13:
                if index == 14:
                    DM_list_1 = [r['_+DM'] for r in all_result[index - 13:]] + [result['_+DM']]
                    result['+DM (14EMA)'] = self.DM_14_EMA(DM_list=DM_list_1)
                    DM_list_2 = [r['_-DM'] for r in all_result[1:index]] + [result['_-DM']]
                    result['-DM (14EMA)'] = self.DM_14_EMA(DM_list=DM_list_2)
                else:
                    pre_DM_14_1 = all_result[-1]['+DM (14EMA)']
                    pre_DM_14_2 = all_result[-1]['-DM (14EMA)']
                    result['+DM (14EMA)'] = self.DM_14_EMA(DM=result['_+DM'], pre_DM_14=pre_DM_14_1)
                    result['-DM (14EMA)'] = self.DM_14_EMA(DM=result['_-DM'], pre_DM_14=pre_DM_14_2)
            if index > 13:
                result['DMI (interval 14) : +DI'] = result['+DM (14EMA)'] / result['ATR (14EMA) B'] * 100
                result['DMI (interval 14) : -DI'] = result['-DM (14EMA)'] / result['ATR (14EMA) B'] * 100
                result['DX'] = (abs(result['DMI (interval 14) : +DI'] - result['DMI (interval 14) : -DI'])
                                / (result['DMI (interval 14) : +DI'] + result['DMI (interval 14) : -DI'])) * 100
            if index > 26:
                if index == 27:
                    DX_list = [r['DX'] for r in all_result[index - 13:]] + [result['DX']]
                    result['ADX'] = self.ADX(DX_list=DX_list)
                else:
                    pre_ADX = all_result[-1]['ADX']
                    result['ADX'] = self.ADX(DX=result['DX'], pre_ADX=pre_ADX)
            if index > 13:
                result['_+DI - (-DI)'] = result['DMI (interval 14) : +DI'] - result['DMI (interval 14) : -DI']
            if index > 13:
                result['_+DI - (-DI)" - ADX'] = result['DMI (interval 14) : +DI'] - result['DMI (interval 14) : -DI'] \
                                                - result.get('ADX', 0)
            # =======================BB=======================
            if index > 18:
                #
                BB_list_1 = self.data['close'][index - 19:index + 1]
                result['BB middle (Interval 20, no. of Std Dev 2)'] = sum(BB_list_1) / 20
                result['BB upper limit (Interval 20, no. of Std Dev 2)'] = \
                    result['BB middle (Interval 20, no. of Std Dev 2)'] + np.std(BB_list_1) * 2
                result['BB bottom limit (Interval 20, no. of Std Dev 2)'] = \
                    result['BB middle (Interval 20, no. of Std Dev 2)'] - np.std(BB_list_1) * 2

                result['Close > BB upper (+-%)'] = \
                    (result['BB upper limit (Interval 20, no. of Std Dev 2)'] / self.data['close'][index] - 1) * 100
                result['Close > BB middle (+-%)'] = (
                    result['BB middle (Interval 20, no. of Std Dev 2)'] / self.data['close'][index] - 1) * 100
                result['Close > BB lower (+-%)'] = \
                    (result['BB bottom limit (Interval 20, no. of Std Dev 2)'] / self.data['close'][index] - 1) * 100
            all_result.append(result)
        all_result.reverse()
        return self.get_data(all_result=all_result)


if __name__ == '__main__':
    DEBUG = False  # 影响数据获取方式 True读取本地文件 False 发送请求
    with open('all_ts_code', 'r', encoding='utf8') as f:
        all_ts_code = json.loads(f.read())
    t_c = '00002.HK'
    s_d = '20190101'
    e_d = '20210525'
    gp = GG_RXHQ(ts_code=t_c, start_date=s_d, end_date=e_d)
    r = gp.main()

