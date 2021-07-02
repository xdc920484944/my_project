from selenium import webdriver
import time
from lxml import etree
from tqdm import tqdm
import datetime
import os
from tool_fun import ToolFunction
from concurrent.futures import ThreadPoolExecutor

thread = ThreadPoolExecutor(10)


def change_time(t):
    '''
    将xx:xx格式的时间转换成秒
    :param t: 时间 eg: 0:45
    :return: int
    '''
    t = t.split(':')
    if len(t) == 2:
        d = int(t[0]) * 60 + int(t[1])
        return d


def get_video_id(words, page):
    '''
    获取视频id
    :param words:搜索关键词
    :param page: 爬取页数
    :return: 视频id列表
    '''
    driver = ToolFunction.creat_driver(wutu=True)
    driver.maximize_window()
    video_id_list = []

    def execute_times():
        '''

        :return:
        '''
        for i in range(page):
            ########### 解析html ############
            html = etree.HTML(driver.page_source)
            labels = html.xpath('//*[@id="contents"]/ytd-video-renderer')

            ########### 获取视频id，过滤超过90S的视频 ############
            for l in labels:
                _id = l.xpath('div//a[@id="thumbnail"]/@href')[0]
                long = l.xpath('div//span[@class="style-scope ytd-thumbnail-overlay-time-status-renderer"]/text()')
                video_time = change_time(''.join(''.join(long).split()))
                video_id = _id.replace('/watch?v=', '')
                if video_time and video_time < 90:
                    video_id_list.append(video_id)

            ########### 模拟鼠标向下滑动 ############
            js = "var q=document.documentElement.scrollTop=100000000000"
            driver.execute_script(js)
            time.sleep(3)  # 等待页面刷新

    for query in words:
        url = 'https://www.youtube.com/results?search_query=' + query + '&sp=CAISAhgB'
        driver.get(url)
        print('搜索关键词:', query, '页数:', page, 'url:', url)
        ########### 模拟鼠标向下滑动 ############
        execute_times()
        time.sleep(1)

    ########### 退出Chrome ############
    driver.quit()
    return video_id_list


def download_video(video_id, save_path):
    '''
    下载视频
    :param save_path: 视频保存路径
    :param video_id:视频id
    :return:
    '''
    from pytube import YouTube
    YouTube('http://youtube.com/watch?v={}'.format(video_id)).streams.first().download(output_path=save_path)


if __name__ == '__main__':
    search_word = ['项链']  # 搜索关键词
    max_page = 2  # 页数，每页20个视频
    now = datetime.datetime.now().strftime('%Y%m%d')
    path = os.path.join('videos', now)  # 视频保存路径
    video_list = get_video_id(words=search_word, page=max_page)
    print('视频数量:', len(video_list))
    for _id in tqdm(video_list):
        download_video(video_id=_id, save_path=path)
