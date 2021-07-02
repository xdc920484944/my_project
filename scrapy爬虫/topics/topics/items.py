# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class TopicItem(Item):
    created_at=Field()
    post_mid=Field()
    post_content=Field()
    post_user_id=Field()
    post_user_name=Field()
    verified_reason=Field()
    comments_cnt=Field()
    current_page=Field()
    since_id=Field()
    #next_page_1=Field()
    source=Field()
    scrapy_time=Field()
