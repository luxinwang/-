import requests
import time
from datetime import datetime
from lxml import etree
import hashlib
from connact_mysql import Mydb

# 请求网址
base_url = 'http://live.sina.com.cn/zt/f/v/finance/globalnews1'
# 定义请求头
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}
# 标识是否是第一次请求网页
is_first = True
# 定义向数据库插入数据函数
def insert_sql():
    sql = 'insert into xinlang(pub_time,time_id,news) values(%s,%s,%s) on duplicate key update time_id=values(time_id)'
    data = (pub_time_str, time_id, news)
    mydb.execute(sql, data)
while True:
    # 发起请求
    response = requests.get(base_url,headers=headers)
    # 定位包含信息的div
    html = response.text
    con = etree.HTML(html)
    msg_list = con.xpath('//div[@class="bd_list"]/div[contains(@class,"bd_i")]')
    for index,msg in enumerate(msg_list):
        # 发布时间
        pub_time_time = msg.xpath('.//div[@class="bd_i_time clearfix"]/p[@class="bd_i_time_c"]/text()')[0]
        pub_time_str = datetime.now().strftime('%Y-%m-%d') + ' ' + pub_time_time
        # 时间作为数据表唯一索引
        m = hashlib.md5()
        m.update(pub_time_str.encode(encoding='utf-8'))
        time_id = m.hexdigest()
        # 新闻内容
        news = msg.xpath('.//p[@class="bd_i_txt_c"]/text()')[0]

        # 数据存入数据库
        mydb = Mydb()
        # 是否是第一次请求
        if is_first:
            insert_sql()
        elif pub_time_time > max_time:
            insert_sql()
        else:
            pass
        if index == 0:
            temp_time = pub_time_time
        # print(pub_time_str,time_id,news)
    # 更新最新时间
    max_time = temp_time
    # 更改标识
    is_first = False
    time.sleep(60)

