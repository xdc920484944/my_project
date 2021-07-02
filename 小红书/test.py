import time
import json
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


# def response(flow):
#     '''
#     {'code': 0, 'success': True, 'data': {'items': [.....]}
#     :param flow:
#     :return:
#     '''
#     if 'api/sns/v10/search/notes' in flow.request.url:
#         print('===========================')
#         data = json.loads(flow.response.text)
#         # print(data)
#         for d in data['data']['items']:
#             print(d)
#             print('\n')

cap = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.xingin.xhs",
    "appActivity": "com.xingin.xhs.activity.SplashActivity",
    "noReset": True,
    "unicodekeyboard": True,  # 键盘输入 可输入中文
    "resetkeyboard": True  # 控制的时候使用的是appium的输入法,结束后需要还原
}

drivre = webdriver.Remote("http://localhost:4723/wd/hub", cap)
