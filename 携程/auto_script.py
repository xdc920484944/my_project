import json
import random
from selenium.webdriver.support.wait import WebDriverWait
from function import ToolFunction
import time
import re


class XieCheng:
    def __init__(self, params, driver):
        self.driver = driver
        self.driver.get('https://hotels.ctrip.com/hotels/listPage')

        self.city = params.get('city')
        self.keyword = params.get('keyword')
        self.start_date = params.get('start_date')
        self.end_date = params.get('end_date')
        self.low_price = params.get('low_price')
        self.high_price = params.get('high_price')

        self.filter_params()
        self.max_page = self.get_max_page()
        self.turn_next_page()

    def filter_params(self):
        # 城市
        self.driver.find_element_by_xpath('//*[@id="hotels-destination"]').send_keys(self.city)
        time.sleep(1)
        divs = self.driver.find_elements_by_xpath('//div[@class="drop-result-list"]/div')
        divs[0].click()
        # 选择日期
        date_info = self.year_month_days()
        for date in (self.start_date, self.end_date):
            if date in date_info['days']:
                date_info['days'][date].click()
        # 关键词
        self.driver.find_element_by_xpath('//input[@id="keyword"]').send_keys(self.keyword)
        # 搜索
        self.driver.find_element_by_xpath('//*[@class="u-icon u-icon-search"]').click()
        # 价格过滤
        if WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_xpath('//input[@class="price-range-input-low"]')):
            self.driver.find_element_by_xpath('//input[@class="price-range-input-low"]').send_keys(self.low_price)
            self.driver.find_element_by_xpath('//input[@class="price-range-input-high"]').send_keys(self.high_price)
            self.driver.find_element_by_xpath('//input[@class="price-range-input-low"]').click()

    def get_max_page(self):
        if WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_xpath('//*[@class="filter-title clearfix"]')):
            time.sleep(2)
            hotel_num = self.driver.find_element_by_xpath('//h3').text
            max_page = int(''.join(re.findall('\d+', hotel_num))) // 10
            print('hotel_num:', hotel_num, 'max_page:', max_page)
        return max_page

    def turn_next_page(self):
        current_page = 1
        while self.max_page >= current_page:
            print('当前进度{}/{}'.format(current_page, self.max_page))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.find_element_by_xpath('//div[@class="list-btn-more"]/div').click()
            except:
                pass
            current_page += 1
            time.sleep(60 - random.randint(1, 10))

    def year_month_days(self):
        def parse_days():
            days = {}
            lis = now_month.find_elements_by_xpath('./div[@class="c-calendar-month__days"]//li')
            for li in lis:
                day = li.text
                if day:
                    day = '0' + day if len(day) == 1 else day
                    days[result['year'] + result['month'] + day] = li
            return days

        result = {}
        now_month, next_month = self.driver.find_elements_by_xpath('//div[@class="c-calendar-month"]')
        date = now_month.find_element_by_xpath('./h3')
        result['year'], result['month'] = re.findall('(\d+)+', date.text)
        result['month'] = result['month'] if len(result['month']) == 2 else '0' + result['month']
        result['days'] = parse_days()
        return result


if __name__ == '__main__':
    p = {'city': '福州', 'keyword': '鼓楼区', 'start_date': '20210624', 'end_date': '20210625', 'low_price': '400',
         'high_price': '500'}
    d = ToolFunction.creat_driver(shoudong=True)
    all_handle = d.window_handles
    d.switch_to.window(all_handle[0])
    xiecheng = XieCheng(params=p, driver=d)
