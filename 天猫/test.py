from tool_fun import ToolFunction
import time


def get_shop(driver, count):
    current_page = 0
    white_href = []
    black_href = []
    key = True

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
                    print(pay, shop_href, shop_href in black_href)
                    white_href.append(shop_href)
                else:
                    black_href.append(shop_href)
                    if shop_href in white_href and int(pay) < MAX_PAY * 2:
                        white_href.remove(shop_href)
            except Exception as e:
                print(e.__traceback__.tb_lineno, e)

    while key:
        if current_page == 0:
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            j_input = driver.find_element_by_xpath('//*[@class="input J_Input"]')
            max_page = j_input.get_attribute('max')
            driver.execute_script("arguments[0].value = {};".format(max_page), j_input)
            driver.find_element_by_xpath('//*[@class="btn J_Submit"]').click()
        else:
            driver.find_element_by_xpath('//*[@title="上一页"]').click()
        time.sleep(30)
        one_page()
        key = len(white_href) < count and current_page < MAX_PAGE
        current_page += 1
        print('当前页数:', int(max_page) - current_page, '店铺个数:', len(white_href))
    return white_href


if __name__ == '__main__':
    MAX_PAGE = 1
    MAX_PAY = 50
    key_word = '剃须刀'
    dr = ToolFunction.creat_driver(shoudong=True)
    url = 'https://s.taobao.com/search?q={}&tab=mall'.format(key_word)
    dr.get(url)
    sh_href = get_shop(driver=dr)
    for s in sh_href:
        print(s)