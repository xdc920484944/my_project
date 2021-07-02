import os
import sys

sys.path.append(os.getcwd())
import function
from flask import Flask, request, render_template, send_from_directory, jsonify
import datetime

app = Flask(__name__)


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         # 'Vol' '10SMA>20SMA>50SMA' '10SMA-20SMA' '20SMA-50SMA' 'days of 10SMA>20SMA>50SMA' '14RSI' '9SMA (14 RSI)' '14RSI÷9SMA-1 (%)' 'MACD (12, 26)' '9-EMA of MACD' 'Diff' 'MOM or MTM (interval 10)' 'Avg changing percentage of last 4 days' 'ROC (interval 10)' '+DI - (-DI)' '+DI - (-DI) - ADX' 'Close > BB upper (+-%)' 'Close > BB middle (+-%)' 'Close > BB lower (+-%)': ''}
#         params = dict(request.form)
#         print(params)
#         calc = params.get('calculated')
#         ts_code = params.pop('ts_code', None)
#         start_date = params.pop('start_date', None)
#         end_date = params.pop('end_date', None)
#         date = params.pop('date', None)
#         days = int(params.pop('days', 0))
#
#         gp = function.GG_RXHQ(ts_code=ts_code, start_date=start_date, end_date=end_date)
#
#         if calc == 'ave_line_calc':
#             result = gp.ave_line_calc(date=date, days=days)
#         elif calc == 'ave_line_compare':
#             result = gp.ave_line_compare(date=date)
#         elif calc == 'ave_line_diff':
#             result = gp.ave_line_diff(date=date)
#         elif calc == 'ave_line_go_up':
#             result = gp.ave_line_go_up(date=date, days=days)
#         elif calc == 'RSI':
#             result = gp.RSI(date=date, days=days)
#         elif calc == 'ave_RSI':
#             result = gp.ave_RSI(date=date, days=days)
#         elif calc == 'compare_RSI':
#             result = gp.compare_RSI(date=date)
#         elif calc == 'MTM':
#             result = gp.MTM(date=date, days=days)
#         elif calc == 'ave_pre_close':
#             result = gp.ave_pre_close(date=date, days=days)
#         elif calc == 'ROC':
#             result = gp.ROC(date=date, days=days)
#         elif calc == 'DMI':
#             result = gp.DMI(date=date, days=days)
#         elif calc == 'BOLL':
#             result = gp.BOLL(date=date, days=days)
#         else:
#             result = None
#         return jsonify({'calculate': calc, 'date': date, 'days': days, 'result': result})
#     return render_template('home.html')


@app.route("/download", methods=['POST', 'GET'])
def download_file():
    """
    下载excel表主服务
    :param directory: 文件夹
    :param filename: 文件名字
    :return:
    """
    if request.method == 'POST':
        ts_code = request.form.get('ts_code')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        gp = function.GG_RXHQ(ts_code=ts_code, start_date=start_date, end_date=end_date)
        result, path, filename = gp.main()
        return send_from_directory(path, filename, as_attachment=True)
    return render_template('download.html')


if __name__ == '__main__':
    app.run(port=9566, host='0.0.0.0', debug=False)
