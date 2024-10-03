# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RateItem(scrapy.Item):
    records = scrapy.Field()  # 歷史匯率紀錄
    # usd = scrapy.Field()    # 美元/人民幣 匯率
    # eur = scrapy.Field()    # 歐元/人民幣 匯率
    # jpy = scrapy.Field()    # 日幣/人民幣 匯率
    # hkd = scrapy.Field()    # 港幣/人民幣 匯率
    # gbp = scrapy.Field()    # 英鎊/人民幣 匯率
    # aud = scrapy.Field()    # 澳元/人民幣 匯率
    # sgd = scrapy.Field()    # 新加坡幣/人民幣 匯率
    # chf = scrapy.Field()    # 法郎/人民幣 匯率
    # cad = scrapy.Field()    # 加幣/人民幣 匯率
    
