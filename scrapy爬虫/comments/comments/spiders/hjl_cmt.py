# -*- coding: utf-8 -*-
import scrapy
import random
from ..items import *
import json
import re
import time
from dateutil.parser import parse
from datetime import datetime




class LywHjlCmtSpider(scrapy.Spider):
    name = 'hjl_cmt'
    allowed_domains = ['m.weibo.cn']
    
    with open(r'C:\Users\xdc\Desktop\demo\spider\新建文件夹 (2)\comments\comments\spiders\hjl_0301_cmt.csv', encoding='utf8') as f:
        start_urls = [url.strip() for url in f.readlines()[1:]]
    
    use_cookies=list()
    raw_cookies=([
        '_T_WM=29755345158; XSRF-TOKEN=bee93e; WEIBOCN_FROM=1110006030; MLOGIN=1; SCF=Av0HmEkjMS5-2POcg1M0K0oELQks_QfZ74Cz4ERAXEgTVeRNus_pj3vg0Gw38sPc0OqNN4yEG7TIfMseAkJIBVo.; SUB=_2A25NWXkGDeRhGeFL7lIY8irNzTqIHXVuogdOrDV6PUJbktAfLRnekW1NfeivJCHkvitYdqYGwNI-NlP7wACA36gf; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWzfVf5DHIROpVRMYMv3vq25NHD95QNSK-71KzXeKqcWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-feh.ESh2cSntt; SSOLoginState=1616709974' ,
        'SCF=Av0HmEkjMS5-2POcg1M0K0oELQks_QfZ74Cz4ERAXEgTzsNX1iKZOmbyz6IbAAXiNnX7KVghNhbJZwRXzsFlUmE.; ALF=1619057842; _T_WM=80236779953; XSRF-TOKEN=2b625f; WEIBOCN_FROM=1110006030; SUB=_2A25NXT_iDeRhGedJ41AR8yjNyDmIHXVuvkGqrDV6PUJbktANLWHakW1NUaMCTT629SampoxzoYjziNLsDx4jy5a-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhQSOhEcL0Zx97O_XgcuY8Y5JpX5K-hUgL.Fo2N1hz7e0qpe0-2dJLoIfQLxKBLB.2L12eLxKqLBoeLBK2LxK.L1-eL1h5LxKnLBKqL1h2LxK-LB.eLB.2LxK-LBKBLBKMLxKML1-2L1hBLxKnL1hMLB-2LxK-L1hnLBoqLxK-L122L1-zt; SSOLoginState=1616465842; MLOGIN=1',
        'SCF=Ajb67KLHiO0qImsFIxRjQbd3nT_UmKemtUSu1f5jgN2Vxr_imseP0Mp_u7YHRITZ4sIr0UjlieJlsbw75YeXlfI.; SUB=_2A25NUXAGDeRhGeBJ41oS8izNyjWIHXVuuhBOrDV6PUJbktANLRinkW1NRieR5iVNMK-HWsnIQ36rGfJo133VfND1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWY8LoD_yQ7L1NOo1.hBwvF5NHD95QcS0nRe0zEeK24Ws4Dqcj6i--Xi-iFi-2Xi--Xi-iWi-iWi--RiKn7i-z0i--4i-zRi-20i--NiKLWiKnXi--fi-isi-8Fi--Xi-z4iK.7; MLOGIN=1; _T_WM=79252814790; WEIBOCN_FROM=1110006030; XSRF-TOKEN=1122cd',
        '_T_WM=55812186529; WEIBOCN_FROM=1110006030; SCF=Ajb67KLHiO0qImsFIxRjQbd3nT_UmKemtUSu1f5jgN2VyWONHjXAVpNdtZiL6tUNM4y-0OYzqKnhUH_6Erljik8.; SUB=_2A25NWgeADeRhGeFN7VAR-CzNyz2IHXVupKnIrDV6PUJbktAfLXPCkW1NQ-_BXAKLRlVNYsHPuY9QqBWOMaTjyI6e; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhMMMyi7ujQVME6lFsN34Hv5NHD95QNe0qEehnEeK5pWs4Dqcj_i--fiKnNi-27i--fiK.pi-z0i--fi-z7iK.pi--fi-2fi-z0i--4i-20iKLs; SSOLoginState=1616803792; MLOGIN=1; XSRF-TOKEN=443303',
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
        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_comment,
                cookies=random.choice(self.use_cookies),
                headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'        
                }
            )
    
    def parse_comment(self,response):
        current_page=response.url
        #post_mid=re.split("&",str(re.split("&mid=",current_page)[1]))[0]
        resp=json.loads(response.body)
        status_code=resp['ok'] 
        if status_code==1:
            max_id=resp['data']['max_id']
            max_id_type=resp['data']['max_id_type']
            
            comments=resp['data']['data']
            for comment in comments:
                comment_item=CommentItem()
                comment_item['scrapy_time']=datetime.now()
                comment_item['comment_time']=parse(comment['created_at']).date()
                content_raw=comment['text']
                content_final=re.sub(r" ?\<[^)]+?\>", "",content_raw)
                comment_item['comment_text']=content_final
                comment_item['comment_user_id']=comment['user']['id']
                comment_item['comment_user_name']=comment['user']['screen_name']
                comment_item['post_mid']=re.split("&",str(re.split("&mid=",current_page)[1]))[0]
                comment_item['current_page']=current_page
                comment_item['max_id']=max_id
                comment_item['max_id_type']=max_id_type
                comment_item['source']='hjl_cmt'
                yield comment_item
            
            if max_id!=0:
                next_page=re.split("&max_id=",current_page)[0]
                next_page_url=next_page+'&max_id='+str(max_id)+'&max_id_type='+str(max_id_type)
                yield scrapy.Request (
                    url=next_page_url,
                    callback=self.parse_comment,
                    cookies=random.choice(self.use_cookies),
                    headers={
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'        
                    }
                )
