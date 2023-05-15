# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MafengwoItem(scrapy.Item):
    Title = scrapy.Field()      # 景点名字
    Reviews = scrapy.Field()    # 景点评论
    Percent = scrapy.Field()       # 推荐百分比

    pass
