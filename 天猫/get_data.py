from selenium import webdriver
import time
import random
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime


def get_tianmao_shop(driver, count):
    def one_page():
        divs = driver.find_elements_by_xpath('//*[@id="J_ItemList"]/div')
        for div in divs:
            try:
                d = div.find_element_by_xpath('./div/*[@class="productStatus"]//em')
                sale_num = int(d.text.replace('笔', ''))
                shop_href = div.find_element_by_xpath('./div//*[@class="productShop-name"]').get_attribute('href')
                # 月销量大于0
                if sale_num > 0:
                    black_href.append(shop_href)
                    # 切在白名单中则删除白名单中的url
                    if shop_href in white_href and sale_num > 0:
                        white_href.remove(shop_href)
                # 销量等于0且不在黑白名中
                elif shop_href not in black_href and shop_href not in white_href:
                    white_href.append(shop_href)
            except Exception as e:
                pass
                # print(e.__traceback__.tb_lineno, e)

    def go_to_end():
        driver.execute_script("var q=document.documentElement.scrollTop=4000")
        max_page = driver.find_element_by_xpath('//*[@name="totalPage"]').get_attribute('value')
        j_input = driver.find_element_by_xpath('//*[@name="jumpto"]')
        driver.execute_script("arguments[0].value = {};".format(max_page), j_input)
        driver.find_element_by_xpath('//button[@class="ui-btn-s"]').click()
        return max_page

    white_href = []
    black_href = []
    rea_url = 'https://list.tmall.com/search_product.htm'
    key = True
    current_page = 0
    # go_to_end()
    while key:
        if not driver.current_url.startswith(rea_url):
            print('当前页面url非商品url，请检查后运行')
            return white_href
        current_page += 1
        key = len(white_href) < int(count)
        one_page()
        if key:
            driver.find_element_by_xpath('//p[@class="ui-page-s"]/a[@title="下一页"]').click()
            print('当前{}页数'.format(current_page), '当前商店数量{}'.format(len(white_href)))
            # time.sleep(20 + random.randint(1, 10))
    return white_href


def get_taobao_shop(driver, windows):
    driver.switch_to.window(windows[0])
    MAX_PAY = 50
    current_page = 0
    white_href = []
    black_href = []

    def one_page():
        shops = driver.find_elements_by_xpath('//div[@class="item J_MouserOnverReq  "]')
        for sh in shops:
            try:
                pay = sh.find_element_by_xpath(
                    './div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]//*[@class="deal-cnt"]').text.replace(
                    '人付款', '')
                shop_href = sh.find_element_by_xpath(
                    './div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]//*[@class="shopname J_MouseEneterLeave J_ShopInfo"]') \
                    .get_attribute('href').replace('shop/view_shop.htm', 'category.htm')  # category.htm search.htm
                if shop_href not in black_href and shop_href not in white_href and int(pay) < MAX_PAY:
                    white_href.append(shop_href)
                else:
                    black_href.append(shop_href)
                    # if shop_href in white_href and int(pay) < MAX_PAY * 2:
                    #     white_href.remove(shop_href)
            except Exception as e:
                print(e.__traceback__.tb_lineno, e)

    if current_page == 0:
        js = "var q=document.documentElement.scrollTop=4400"
        driver.execute_script(js)
        j_input = driver.find_element_by_xpath('//*[@class="input J_Input"]')
        max_page = j_input.get_attribute('max')
        driver.execute_script("arguments[0].value = {};".format(max_page), j_input)
        driver.find_element_by_xpath('//*[@class="btn J_Submit"]').click()
    else:
        driver.find_element_by_xpath('//*[@title="上一页"]').click()
    time.sleep(20)
    one_page()
    current_page += 1
    print('当前页数:', int(max_page) - current_page, '店铺个数:', len(white_href))
    return white_href, black_href


def creat_driver(wutou=False, shoudong=False, wutu=False, daili=None):
    '''
    谷歌浏览器无头模式
    :return:
    '''
    options = webdriver.ChromeOptions()
    # 无头模式
    if wutou:
        # 无图浏览
        options.add_argument('--headless')
    # 手动启动谷歌浏览器，避免某些网站登入失败
    if shoudong:
        options.add_argument('--disable-extensions')
        options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    # 无图模式
    if wutu:
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    return driver


def get_tianmao_detail(driver, url):
    driver.get(url)

    result = {'tmallStoreOnline': '1', 'tmallStoreProductCount': 0}
    result['tmallStoreAddress'] = driver.current_url
    result['tmallStoreName'] = driver.find_element_by_xpath('//*[@class="slogo-shopname"]').text
    items = driver.find_elements_by_xpath('//*[@class="item5line1"]//dl[@class="item "]')
    for i in items:
        sale_num = i.find_element_by_xpath('./dd[@class="detail"]//*[@class="sale-num"]').text
        result['tmallStoreProductCount'] += int(sale_num)

    if len(items) < 80:
        result['tmallStoreSalesCount'] = len(items)
    else:
        total_page = driver.find_element_by_xpath('//*[@class="ui-page-s-len"]').text.split('/')[-1]
        result['tmallStoreSalesCount'] = 80 * int(total_page)
    return result


def get_taobao_detail(driver, list_url, windows):
    driver.switch_to.window(windows[0])
    driver.get(list_url)
    story_name = driver.find_element_by_xpath('//*[@class="slogo-shopname"]').text
    result = {'tmallStoreOnline': '1', 'tmallStoreProductCount': 0,
              'tmallStoreAddress': driver.current_url, 'tmallStoreName': story_name,
              'tmallStoreSalesCount': 0}

    if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@class="ui-page-s-next"]')):
        next_page = driver.find_element_by_xpath('//*[@class="ui-page-s-next"]')
    while next_page.get_attribute('href') is not None:
        href_list = []
        items = driver.find_elements_by_xpath('//*[@class="item4line1"]/dl')
        for i in items:
            try:
                href_list.append(i.find_element_by_xpath('./dd[@class="detail"]//*[@class="item-name J_TGoldData"]') \
                    .get_attribute('href'))
                sale_num = i.find_element_by_xpath('./dd[@class="detail"]//*[@class="sale-num"]').text
                result['tmallStoreProductCount'] += int(sale_num)
            except Exception as e:
                pass
        # 存在商品月销量>0 或者 3个月内有评论
        # driver.switch_to.window(windows[1])
        # if not filter_goods(driver=driver, goods_url_list=href_list):
        #     return None
        # driver.switch_to.window(windows[0])
        next_page.click()
        if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@class="ui-page-s-next"]')):
            next_page = driver.find_element_by_xpath('//*[@class="ui-page-s-next"]')
        result['tmallStoreSalesCount'] += len(items)
    return result


def filter_goods(driver, goods_url_list):
    def date_calc(s_date):
        e_date = datetime.now().strftime('%Y%m%d')
        input_s_date = datetime.strptime(s_date, '%Y%m%d')
        input_e_date = datetime.strptime(e_date, '%Y%m%d')
        diff = input_e_date - input_s_date
        return diff.days

    key = True
    for goods_url in goods_url_list:
        driver.get(goods_url)
        count_num = driver.find_element_by_xpath('//*[@class="tm-count"]').text
        if count_num == 0:  #
            driver.find_element_by_xpath('//*[@class="J_ReviewsCount"]').click()
            if WebDriverWait(driver, 10).until(
                    lambda x: x.find_element_by_xpath('//*[@id="J_Reviews"]/div/div[6]/table/tbody/tr[1]/td[1]/div[2]')):
                date = driver.find_element_by_xpath(
                    '//*[@id="J_Reviews"]/div/div[6]/table/tbody/tr[1]/td[1]/div[2]').text.replace('.', '')
                date = '2021' + date if len(date) == 5 else date
                key = True if date_calc(date) <= 90 else False
                if not key:
                    return key
        else:
            key = False
            break
    return key
