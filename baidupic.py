from selenium import webdriver
import time
from lxml import etree
from urllib import request

# 构建请求网址
base_url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1526044008897_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%BE%AE%E4%BF%A1%E5%A4%B4%E5%83%8F&f=3&oq=weixin&rsp=0'
# 初始化浏览器
dc = {
    'phantomjs.page.customHeaders.User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
browser = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe',desired_capabilities=dc)
# 定义获取图片的函数
def getPic(html):
    con = etree.HTML(html)
    # 只取每次刷新后的最后一个包含图片地址的div，其余已经抓取过了
    img_div = con.xpath('//div[@class="imgpage"]')[-1]
    # 定位图片地址
    pic_urls = img_div.xpath('.//ul/li//img/@data-imgurl')
    for pic in pic_urls:
        # 存储时的图片名称
        fname = pic.split('/')[-1]
        request.urlretrieve(pic,'images/'+fname)

# 实现网页自动滚轮
def getPage():
    browser.get(base_url)
    # 等待页面加载完毕
    time.sleep(2)
    # 获取加载完JS的网页源码
    html = browser.page_source
    # 执行获取图片的函数
    getPic(html)

    i = 0
    while True:
        try:
            print('滚动%d次'% i)
            browser.execute_script('scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
            # 重新获取网页源码
            html = browser.page_source
            # 执行获取图片函数
            getPic(html)
            i += 1
        except Exception as e:
            print(e)
            break
    # 浏览器退出
    browser.quit()

if __name__ == '__main__':
    getPage()