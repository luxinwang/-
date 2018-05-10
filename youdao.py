import requests
import time
import random
import hashlib
import json

# md5加密函数
def md5(value):
    m = hashlib.md5()
    m.update(bytes(value,encoding='utf-8'))
    return m.hexdigest()
# 请求地址
base_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

keyword = input('请输入内容：')
# 构建参数salt与sign
salt = int(time.time() * 1000) + random.randint(0,9)
sign = "fanyideskweb" + keyword + str(salt) + "aNPG!!u6sesA>hBAW1@(-"
sign = md5(sign)

# 构建form表单
form = {
    "action": "FY_BY_REALTIME",
    "client": "fanyideskweb",
    "doctype": "json",
    "from": "AUTO",
    "i": keyword,
    "keyfrom": "fanyi.web",
    "salt": salt,
    "sign": sign,
    "smartresult": "dict",
    "to": "AUTO",
    "typoResult": "false",
    "version": "2.1",
}
# 构建请求头
headers = {
    "Host": "fanyi.youdao.com",
    "Connection": "keep-alive",
    # "Content-Length": len(data),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "http://fanyi.youdao.com",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "http://fanyi.youdao.com/",
    # "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "OUTFOX_SEARCH_USER_ID=-1654536531@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=1741530350.544148; JSESSIONID=aaae--o9SyvjE6azr5jnw; fanyi-ad-id=44055; fanyi-ad-closed=1; ___rl__test__cookies=1525957160280",
}
# 构建请求
response = requests.post(base_url,headers=headers,data=form)
html = response.text
data = json.loads(html)
res = '|'.join(data['smartResult']['entries'])
# print(data)
print(res)