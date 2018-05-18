from scrapy import cmdline
import os

os.chdir('lagou_distributed_crawl/spiders')
cmdline.execute('scrapy runspider lagou.py'.split())