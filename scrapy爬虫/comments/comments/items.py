# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class CommentItem(Item):
    comment_time=Field()
    comment_text=Field()
    comment_user_id=Field()
    comment_user_name=Field()
    post_mid=Field()
    current_page=Field()
    #next_page=Field()
    max_id=Field()
    max_id_type=Field()
    source=Field()
    scrapy_time=Field()
