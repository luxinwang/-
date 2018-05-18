# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
import re,datetime
import hashlib
from datetime import timedelta
from lagou_distributed_crawl.items import LagouDistributedCrawlItem


class LagouSpider(RedisCrawlSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    redis_key = 'lagou:start_url'

    rules = (
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'),callback='parse_item' ,follow=False,process_request='process_request'),

    )

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Host": "www.lagou.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Content-type": "application/json;charset=utf-8",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "_ga=GA1.2.239489779.1523859285; _gid=GA1.2.543080763.1523859285; user_trace_token=20180416141444-74b12d07-413d-11e8-873f-525400f775ce; LGUID=20180416141444-74b13137-413d-11e8-873f-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; SEARCH_ID=e5909b67bacd4003914aa4d7b2c5a5cc; JSESSIONID=ABAAABAAADEAAFICDE8731C9271F98BEAB179B060B7B728; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523859325,1523859329,1523859335,1523935071; LGSID=20180417111749-e870d84f-41ed-11e8-8903-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; X_HTTP_TOKEN=b40aebdc7fd75fb261ed33746dd05fa0; ab_test_random_num=0; _putrc=39C71B30C469D630123F89F2B170EADC; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B71691; _gat=1; hasDeliver=0; gate_login_token=1914467170b54e779d5ff62cc775c7d1e41b9479ee7bfc960b309276e8eee62d; LGRID=20180417111928-23765bd6-41ee-11e8-8903-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523935170",
        },
        'ROBOTSTXT_OBEY' : False,
        'RETRY_TIMES' : 2,
        'CONCURRENT_REQUESTS': 10,
        'COOKIES_ENABLED' : False,
        'DOWNLOAD_DELAY' : 1
    }
    num_pattern = re.compile(r'\d+')
    def process_request(self,request):
        request.priority = 1
        return request


    def parse_item(self, response):
        item = LagouDistributedCrawlItem()

        # 职位详情连接
        url = response.url
        # url MD5加密
        m = hashlib.md5()
        m.update(url.encode(encoding='utf-8'))
        url_id = m.hexdigest()
        # 工作名称
        pname = response.css('.job-name::attr(title)').extract()[0]  # 获取职位名称

        money = response.css('.job_request .salary::text').extract()[0]  #
        # 工资下限
        smoney = money.lower().replace('k', '').split('-')[0]
        # 工资上限
        emoney = money.lower().replace('k', '').split('-')[1]
        # 工作地点
        location = response.xpath('//*[@class="job_request"]/p/span[2]/text()').extract()[0]
        location = self.remove_splash(location)
        # 经验年限要求
        year = response.xpath('//*[@class="job_request"]/p/span[3]/text()').extract()[0]
        syear, eyear = self.process_year(year)
        # 学历
        degree = response.xpath('//*[@class="job_request"]/p/span[4]/text()').extract()[0]
        degree = self.remove_splash(degree)
        # 工作类型
        ptype = response.xpath('//*[@class="job_request"]/p/span[5]/text()').extract()[0]
        ptype = self.remove_splash(ptype)
        # 职位标签
        tags = response.css('.position-label li::text').extract()  # 获取职位所有标签
        tags = ','.join(tags)  # 把所有标签连接成字符串
        #发布日期
        date_pub = response.css('.publish_time::text').extract()[0]
        date_pub = self.process_date(date_pub)
        # 职位诱惑
        advantage = response.css('.job-advantage p::text').extract()[0]
        # 职位描述
        jobdesc = response.css('.job_bt div p::text').extract()
        jobdesc = ''.join(jobdesc)
        # 工作地址
        jobaddr1 = response.css('.work_addr a::text').extract()[:-1]
        jobaddr2 = response.css('.work_addr::text').extract()[-2].strip()
        jobaddr = ''.join(jobaddr1) + jobaddr2
        # 公司名称
        company = response.css('#job_company dt a img::attr(alt)').extract()[0]
        # 爬去时间
        crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')
        # 爬虫名称
        spider_name = self.name

        item['url'] = url
        item['url_id'] = url_id
        item['pname'] = pname
        item['smoney'] = smoney
        item['emoney'] = emoney
        item['location'] = location
        item['syear'] = syear
        item['eyear'] = eyear
        item['degree'] = degree
        item['ptype'] = ptype
        item['tags'] = tags
        item['date_pub'] = date_pub
        item['advantage'] = advantage
        item['jobdesc'] = jobdesc
        item['jobaddr'] = jobaddr
        item['company'] = company
        item['crawl_time'] = crawl_time
        item['spider_name'] = spider_name

        yield item

    def process_date(self, value):
        if '天前' in value:
            res = self.num_pattern.search(value).group()
            date_pub = (datetime.datetime.now() - timedelta(days=int(res))).strftime('%Y-%m-%d')
        else:
            date_pub = datetime.datetime.now().strftime('%Y-%m-%d')
        return date_pub

    def process_year(self, year):
        if '-' in year:
            res = self.num_pattern.findall(year)
            syear = res[0]
            eyear = res[1]
        elif '以上' in year:
            res = self.num_pattern.search(year)
            syear = res.group()
            eyear = res.group()
        else:
            syear = 0
            eyear = 0
        return syear, eyear

    def remove_splash(self, value):
        return value.replace('/', '').strip()