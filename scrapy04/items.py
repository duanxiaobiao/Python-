# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy04Item(scrapy.Item):
    # 猎聘招聘的求职名称
    # 1. 求职名称
    name = scrapy.Field()
    # 2.职位所属公司
    company = scrapy.Field()
    # 3.工资
    salary = scrapy.Field()
    # 4.公司所在地
    address = scrapy.Field()
    # 5.工作经验
    experience = scrapy.Field()
    # 6.学历要求
    education = scrapy.Field()
    # 7.福利
    welfare = scrapy.Field()


