# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MafengwoItem(scrapy.Item):
    Title = scrapy.Field()      # ��������
    Reviews = scrapy.Field()    # ��������
    Percent = scrapy.Field()       # �Ƽ��ٷֱ�

    pass
