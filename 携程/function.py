import json

from pymongo import MongoClient
from pymongo.collection import Collection
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from config import LOGIN_PARAMS


class ToolFunction:
    @classmethod
    def creat_driver(cls, wutou=False, shoudong=False, wutu=False, proxy=None):
        '''
        谷歌浏览器无头模式
        :return:
        '''
        options = webdriver.ChromeOptions()
        # options.add_argument("--proxy-server={}".format('http://121.204.194.160:28803'))
        # 无头模式
        if wutou:
            options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
            options.add_argument('--headless')
        # 手动启动谷歌浏览器，避免某些网站登入失败
        if shoudong:
            options.add_argument('--disable-extensions')
            options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # 非手动下，需要修改浏览器的特征值
        else:
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument("--disable-blink-features=AutomationControlled")
        # 无图模式
        if wutu:
            prefs = {'profile.managed_default_content_settings.images': 2}
            options.add_experimental_option('prefs', prefs)
        # 设置代理
        if proxy:
            options.add_argument("--proxy-server={}".format(proxy))
        driver = webdriver.Chrome(options=options)
        return driver

    @classmethod
    def login(cls):
        login_params = LOGIN_PARAMS
        result = {}
        while login_params:
            params = login_params.pop()
            proxy = params['proxy']
            cookie_path = params['cookie']
            with open(cookie_path, 'r', encoding='utf8') as f:
                cookies = json.loads(f.read())
            driver = cls.creat_driver(wutu=True, proxy=proxy)
            username, password = cookies.pop(-1).values()
            driver.get(
                'https://passport.ctrip.com/user/login?BackUrl=https%3A%2F%2Fwww.ctrip.com%2F#ctm_ref=c_ph_login_buttom')
            for cookie in cookies:
                driver.add_cookie(
                    {'name': cookie['name'], 'value': cookie['value'], 'path': cookie['path'],
                     'secure': cookie['secure']})
            driver.get(
                'https://hotels.ctrip.com/hotels/listPage?cityename=shanghai&city=2&checkin=2021/6/1&checkout=2021/06/02&optionId=2&optionType=City&crn=1&adult=1&children=0#ctm_ref=ctr_hp_sb_lst')
            if WebDriverWait(driver, 10).until(
                    lambda x: x.find_element_by_xpath('//*[@id="personpwd"]')):
                driver.find_element_by_xpath('//*[@id="personpwd"]').send_keys(password)
                driver.find_element_by_xpath('//*[@id="personSubmit"]').click()
                result['Thread-{}'.format(len(login_params))] = driver
        return result


if __name__ == '__main__':
    # pxs = ToolFunction.get_proxies('6h-12h')
    # print(pxs)
    r = ToolFunction.creat_driver()
