import xlwt  # 写excel
import xlrd  # 导入模块
from xlutils.copy import copy  # 导入copy模块
import time


class xie_xls():

    def __init__(self, name, biandan='sheet1'):
        self.name = name
        self.biandan = biandan

    # 创建表
    def chuangbiao(self, tou):
        book = xlwt.Workbook()  # 创建一个工作簿
        sheet = book.add_sheet(self.biandan)  # 创建一个表名
        # 第一个参数是行，第二个参数是列，都从0开始计算
        # tou = ['总积压', '通过', '拒绝', '今日积压']

        for i in range(0, len(tou)):
            sheet.write(0, i, tou[i])

        book.save('{}'.format(self.name))  # 保存一个excel文件
        print('表格创建成功。。。。。。。')

    # 修改表02
    def xiubiao02(self, data, biao01=1):
        rb = xlrd.open_workbook('{}'.format(self.name),
                                formatting_info=True)  # 打开weng.xls文件   保留表格格式 formatting_info=True
        wb = copy(rb)  # 利用xlutils.copy下的copy函数复制
        ws = wb.get_sheet(0)  # 获取表单0

        sh = rb.sheet_by_name(self.biandan)
        hang = sh.nrows  # 读取有几行，从1开始记

        # 设置背景为 red
        # style = xlwt.easyxf('pattern:pattern solid,fore_colour red')
        # ws.write(0,0,'',style)

        # 合并第0行的第0列到第3列。
        # ws.write_merge(6, 7, 0, 3, 'First Merge',style)

        for i01 in range(0, len(data)):
            ws.write(hang, i01, data[i01])  # 改变（0,0）的值
        wb.save('{}'.format(self.name))  # 保存文件

        if biao01 == 1:
            print('数据存入表格成功。。。。。。。。。。')

    # 修改表03
    def xiubiao03(self, data, biao01=1):
        rb = xlrd.open_workbook('{}'.format(self.name), formatting_info=True)  # 打开weng.xls文件
        wb = copy(rb)  # 利用xlutils.copy下的copy函数复制
        ws = wb.get_sheet(0)  # 获取表单0

        sh = rb.sheet_by_name(self.biandan)
        hang = sh.nrows  # 读取有几行，从1开始记

        for i01 in range(0, len(data)):
            for i02 in range(0, len(data[i01])):
                ws.write(hang + i01, i02, data[i01][i02])  # 改变（0,0）的值

        wb.save('{}'.format(self.name))  # 保存文件

        if biao01 == 1:
            print('数据集存入表格成功。。。。。。。。。。。。。')

    # 读取表
    def dubiao(self, xuan=-1):
        fname = "{}".format(self.name)
        bk = xlrd.open_workbook(fname)
        # shxrange = range(bk.nsheets)
        name01 = bk.sheet_names()
        print('表单名：', name01)
        print('读取表单名：', name01[xuan])
        sh = bk.sheet_by_name(name01[xuan])
        # sh = bk.sheet_by_name(self.biandan)

        nrows = sh.nrows  # 读取有几行，从1开始记
        ncols = sh.ncols  # 读取最后列的位置，从1开始记
        print("nrows %d, ncols %d" % (nrows, ncols))

        # cell_value = sh.cell_value(0, 0)  # 读取（0,0）位置的内容
        # print(cell_value)

        row_list = []
        for i in range(0, nrows):
            row_data = sh.row_values(i)  # 读取一行的内容，返回一个列表
            # print(row_data)
            row_list.append(row_data)
        # print(row_list)

        print('读取表格成功。。。。。。。。。。。。。')
        return row_list


if __name__ == '__main__':
    yue = xie_xls('爬虫结果(2).xls')
    # yue.chuangbiao([])
    tou = ['全部主题', '作者', '回复/查看', '最后发表']
    # yue.chuangbiao(tou)
    # yue.xiubiao02(tou)
    print(yue.dubiao())

# 设置超链接
# ws.write(row, colmn, xlwt.Formula('HYPERLINK("{}"; "{}")'.format(link, text)))

#     nr=[' 6年老店【NAIL ME】美甲美睫 脱毛 半永久纹眉 线雕水光 皮肤管理 祛痘点痣 可上门服务',  'attach_img NailMeBeauty,2014-05-02','0,217831',
# NailMeBeauty
# 5分钟前']
#     yue.xiubiao02(nr)
