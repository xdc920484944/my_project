# -*- coding: utf-8 -*-
import scrapy
import random
from ..items import *
import json
import re
import time
from dateutil.parser import parse
from datetime import datetime


class TopicSpider(scrapy.Spider):
    name = 'topic'
    allowed_domains = ['m.weibo.cn']
    start_urls = 'https://m.weibo.cn/api/container/getIndex?containerid=1008080a161dbdc48b2a4e51643d9c24c2cf19_-_feed&luicode=10000011&lfid=100103type%3D1%26q%3D%E8%B4%BA%E5%B3%BB%E9%9C%96&since_id=4603833931534688'
    next_page_url = 'https://m.weibo.cn/api/container/getIndex?containerid=1008080a161dbdc48b2a4e51643d9c24c2cf19_-_feed&luicode=10000011&lfid=100103type%3D1%26q%3D%E8%B4%BA%E5%B3%BB%E9%9C%96&since_id={since_id}'
    use_cookies = list()
    raw_cookies = ([
        '_T_WM=68111315045; XSRF-TOKEN=4f03b1; WEIBOCN_FROM=1110006030; MLOGIN=1; SCF=Av0HmEkjMS5-2POcg1M0K0oELQks_QfZ74Cz4ERAXEgTo2AB_w7VJt13ATZ5LFTzaoiIIY5jZw4rZaIXYJNS34Q.; SUB=_2A25NWgkuDeRhGeFN7VAS9yzJzTyIHXVupJdmrDV6PUJbktAKLUrWkW1NQ--q_iHi2jvK0fm_AnRPV8iVtnlmQs-d; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFij34uDA_3l.OrQKZFMS105NHD95QNe0qEe0MESKq7Ws4Dqcjdi--Xi-z4iKy2i--ci-z0iKnXi--fi-20i-8F; SSOLoginState=1616804222',
        '_T_WM=55812186529; XSRF-TOKEN=eea693; WEIBOCN_FROM=1110006030; SCF=Ajb67KLHiO0qImsFIxRjQbd3nT_UmKemtUSu1f5jgN2VvV5ZVOOPOAdxlFat22cWSKlyzFRM2wGN7qXC_uj-sN0.; SUB=_2A25NWgsJDeRhGeFN7VAS9C_MzTqIHXVupJVBrDV6PUJbktANLWHWkW1NQ-_IRGFk90-J-zrCChKh3PSGHe97BxRA; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFIs4DKbvTc67dYuzkZqmMs5NHD95QNe0qEe0BpehqcWs4Dqcjdi--fi-82i-8hi--fi-8FiK.pi--ci-zci-2R; SSOLoginState=1616804697; MLOGIN=1'
    ])
    ####this is from cookie pool(my main acct)
    for cookie in raw_cookies:
        cookie_dict = {}
        items = cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            cookie_dict[key] = value
            use_cookies.append(cookie_dict)

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_weibo,
            cookies=random.choice(self.use_cookies),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
            }
        )

    def parse_weibo(self, response):
        current_page = response.url
        resp = json.loads(response.body)
        status_code = resp['ok']
        if status_code == 1:
            since_id = resp['data']['pageInfo']['since_id']
            cards = resp['data']['cards']
            for card in cards:
                if 'card_group' not in card:
                    continue
                else:
                    weibos = card['card_group']
                    for weibo in weibos:
                        if 'mblog' not in weibo:
                            continue
                        else:
                            try:
                                topic_item = TopicItem()
                                weibo_list = weibo
                                topic_item['scrapy_time'] = datetime.now()
                                topic_item['created_at'] = parse(weibo['mblog']['created_at']).date()
                                topic_item['post_mid'] = weibo['mblog']['mid']
                                weibo_content_raw = weibo['mblog']['text']
                                weibo_content_final = re.sub(r" ?\<[^)]+?\>", "", weibo_content_raw)
                                topic_item['post_content'] = weibo_content_final
                                topic_item['post_user_id'] = weibo['mblog']['user']['id']
                                topic_item['post_user_name'] = weibo['mblog']['user']['screen_name']
                                topic_item['comments_cnt'] = weibo['mblog']['comments_count']
                                topic_item['current_page'] = current_page
                                topic_item['since_id'] = since_id
                                topic_item['source'] = 'hjl_post'
                                mid = weibo['mblog']['mid']
                            except TypeError:
                                continue
                            if 'verified_reason' in weibo['mblog']['user']:
                                verified_reason = weibo['mblog']['user']['verified_reason']
                            else:
                                verified_reason = 'Null'
                            topic_item['verified_reason'] = verified_reason
                            yield topic_item

            if since_id:
                yield scrapy.Request(
                    url=self.next_page_url.format(since_id=since_id),
                    callback=self.parse_weibo,
                    meta={'since_id': since_id},
                    cookies=random.choice(self.use_cookies),
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
                    }
                )
