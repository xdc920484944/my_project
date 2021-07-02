import queue
import threading
import time
from flask import Flask, request
from auto_script import XieCheng
from mongo import MonGo
from function import ToolFunction
from config import THREAD_NUM, DEBUG

app = Flask(__name__)
exitFlag = 0
queueLock = threading.Lock()
workQueue = queue.Queue(THREAD_NUM)
driver_dict = ToolFunction.login()
mongo = MonGo()


@app.route('/')
def index():
    return '携程爬虫接口调试成功'


class myThread(threading.Thread):
    def __init__(self, threadID, name, driver, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = name
        self.driver = driver
        self.q = q

    def run(self):
        print("开启线程：" + self.threadName)
        data = self.process_data(self.q)
        for hotel_id in data['task']:
            url = 'https://hotels.ctrip.com/hotels/detail/?hotelId={}&checkIn=&checkOut=' \
                .format(hotel_id, data['checkIn'], data['checkOut'])
            self.driver.get(url=url)
            bed_info = self.get_hotel_info()
            print(self.threadName, bed_info)
            mongo.insert_data(collection='bed', data=bed_info)
        print("退出线程：" + self.threadName)

    @staticmethod
    def process_data(q):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                data = q.get()
                queueLock.release()
                return data
            else:
                queueLock.release()

    def get_hotel_info(self):
        def get_bed_info():
            beds_info = {}
            divs = self.driver.find_elements_by_xpath('//div[@class="roomlist-baseroom"]/div')
            for div in divs:
                rooms_type = div.find_element_by_xpath('./div//div[@class="roomname"]').text
                beds = div.find_elements_by_xpath('./div//div[@class="salecardlist-rooms"]/div')
                for bed in beds:
                    ded_type = bed.find_element_by_xpath('./div//div[@class="bed-content"]').text
                    # breakfast = bed.find_element_by_xpath('./div//div[@class="bm-item"]').text
                    # smoke = bed.find_element_by_xpath('./div//div[@class="facility"]').text
                    # window = bed.find_element_by_xpath('./div//div[@class="facility"][2]').text
                    try:
                        price_delete = bed.find_element_by_xpath('./div//div[@class="price"]/span').text
                    except:
                        price_delete = None
                    price = bed.find_element_by_xpath('./div//div[@class="price"]/div').text
                    beds_info[rooms_type] = {'ded_type': ded_type, 'price_delete': price_delete, 'price': price}
            return beds_info

        hotel_info = {}
        hotel_info['hotelName'] = self.driver.find_element_by_xpath('//h1[@class="detail-headline_name  "]').text
        hotel_info['star'] = len(self.driver.find_elements_by_xpath('//div[@class="detail-headline_title "]/i'))
        hotel_info['badgeHover'] = True if len(
            self.driver.find_elements_by_xpath('//div[@class="detail-headline_title "]//span')) > 0 else False
        hotel_info['address'] = self.driver.find_element_by_xpath('//span[@class="detail-headline_position_text"]').text
        hotel_info['number'] = self.driver.find_element_by_xpath('//b[@class="detail-headreview_score_value"]').text
        hotel_info['checkIn'] = self.driver.find_element_by_xpath(
            '//div[@class="time-tab"]/input[@class="focus-input show-hightlight out-time"]') \
            .get_attribute('data-key').replace('/', '-')
        hotel_info['checkOut'] = self.driver.find_element_by_xpath(
            '//div[@class="time-tab"][2]/input[@class="focus-input show-hightlight out-time"]') \
            .get_attribute('data-key').replace('/', '-')
        hotel_info['bedList'] = get_bed_info()
        return hotel_info


def start_thread(hotelIds):
    threads = []
    threadID = 1

    # 创建新线程
    for tName, d in driver_dict.items():
        thread = myThread(threadID, tName, d, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    queueLock.acquire()
    for word in hotelIds:
        print(word)
        workQueue.put(word)
    queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("退出主线程")
    return exitFlag


@app.route('/hotel_detail', methods=['POST'])
def hotel_detail():
    if request.method == 'POST':
        params_dict = request.get_json()
        task = params_dict['hotelIds']

        print(task)
        exitFlag = start_thread(hotelIds=task)
    return '爬虫调用成功'


@app.route('/hotel_list', methods=['POST'])
def hotel_list():
    if request.method == 'POST':
        params_dict = request.get_json()
        hand_driver.switch_to.window(all_handle[0])
        xie_cheng = XieCheng(driver=hand_driver, params=params_dict)
    return '爬虫调用成功'


if __name__ == '__main__':
    # mitmdump -p 8889 --mode upstream:http://43.240.192.159:28803 -s C:\Users\xdc\Desktop\demo\spider\携程\dump_script.py
    # mitmdump -p 8889 --mode upstream:http://43.240.192.159:28803 -s C:\Users\Administrator\Desktop\携程\dump_script.py
    # chrome --remote-debugging-port=9222

    hand_driver = ToolFunction.creat_driver(shoudong=True)
    all_handle = hand_driver.window_handles
    app.run(port='9566', host='0.0.0.0', debug=False)
