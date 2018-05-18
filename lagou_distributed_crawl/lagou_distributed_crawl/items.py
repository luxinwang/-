# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouDistributedCrawlItem(scrapy.Item):
    url = scrapy.Field()
    url_id = scrapy.Field()  # md5 加密以后的字符串
    pname = scrapy.Field()  # 工作职位名称
    smoney = scrapy.Field()  # 最低工资
    emoney = scrapy.Field()  # 最高工资
    location = scrapy.Field()  # 城市
    syear = scrapy.Field()  # 要求经验
    eyear = scrapy.Field()
    degree = scrapy.Field()  # 学历
    ptype = scrapy.Field()  # 职位类型
    tags = scrapy.Field()  # 标签
    date_pub = scrapy.Field()  # 发布日期
    advantage = scrapy.Field()  # 职位诱惑
    jobdesc = scrapy.Field()  # 职位简介
    jobaddr = scrapy.Field()  # 详细地址
    company = scrapy.Field()  # 公司名称
    crawl_time = scrapy.Field()  # 抓取时间
    spider_name = scrapy.Field()

    def get_sql(self):
        sql = 'insert into lagou(url,url_id,pname,smoney,emoney,location,syear,eyear,degree,ptype,tags,date_pub,advantage,jobdesc,jobaddr,company,crawl_time,spider_name) ' \
              'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update url_id=values(url_id)'

        data = (self["url"], self["url_id"], self["pname"], self["smoney"], self["emoney"], self["location"], self["syear"],
                self["eyear"], self["degree"], self['ptype'], self['tags'], self['date_pub'], self['advantage'],
                self['jobdesc'], self['jobaddr'], self['company'], self["crawl_time"], self["spider_name"])
        return sql, data
