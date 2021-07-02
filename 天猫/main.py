import os
from flask import Flask, request
import sys
import time

sys.path.append('..')
from get_data import get_tianmao_shop, get_taobao_shop, creat_driver, get_tianmao_detail, get_taobao_detail
import json
# https://luxianziwj.tmall.com/category.htm?user_number_id=3010306920
# nange1017 Zzhuhuichong1
# 112.124.1.107 administrator CUIhaonan1017
# chrome --remote-debugging-port=9222 --proxy-server="http://121.204.194.160:28803"
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    model = 'tianmao'
    result = {'list': []}
    keyword = request.args.get('keyword')
    count = int(request.args.get('count'))
    driver = creat_driver(shoudong=True)
    windows = driver.window_handles
    black_url = []
    if model == 'tianmao':
        u = 'https://list.tmall.com/search_product.htm?q={}&sort=new'.format(keyword)
        shop_url = get_tianmao_shop(driver=driver, count=count)
        driver.get(u)
        for url in shop_url:
            result['list'].append(get_tianmao_detail(driver=driver, url=url))

    elif model == 'tabao':
        u = 'https://s.taobao.com/search?q={}&tab=mall'.format(keyword)
        driver.get(u)
        while len(result['list']) < count:
            w_u, b_u = get_taobao_shop(driver=driver, windows=windows)
            black_url += b_u
            set(black_url)
            for url in w_u:
                if url not in black_url:
                    time.sleep(2)
                    result['list'].append(get_taobao_detail(driver=driver, list_url=url, windows=windows))

    result['errcode'] = 0
    result['errmsg'] = 'OK'
    driver.get('https://www.baidu.com/')
    driver.switch_to.window(windows[-1])
    return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
