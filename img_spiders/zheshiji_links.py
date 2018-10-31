import json
import threading
import time
from multiprocessing.dummy import Pool

import pymysql
import requests
from lxml import etree
from queue import Queue

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "HC08B1JNL576QO8D"
proxyPass = "4C27A88C03D1E661"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


class zhisheji(object):
    # 初始化
    def __init__(self, db_host='172.16.0.32', db_user='s1326_aiji66', db_password='Su_s1326@aiji', db_name='bizhi',
                 db_charset='utf8', db_port=3306):
        self.db_host = '172.16.0.32'
        self.db_user = 's1326_aiji66'
        self.db_password = 'Su_s1326@aiji'
        self.db_name = 'bizhi'
        self.db_charset = 'utf8'
        self.db_port = 3306
        self.url = "http://www.zhisheji.com/yuanchuang/{}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
            "Referer": "http://www.zhisheji.com/yuanchuang/dianpu/"
        }
        self.base_url = "http://www.zhisheji.com"
        # url 线程队列
        self.url_que = Queue()
        # 线程池
        self.pool = Pool()
        # 请求数
        self.requests_url = 0
        # 保存数
        self.response_url = 0
        # 判断条件
        self.is_runing = True

    def get_url(self):
        for i in range(3650, 5660):
            self.url_que.put(self.url.format(i))
            self.requests_url += 1

    # 发送求情 接受相应
    def pare_url(self, url):
        response = requests.get(url, headers=self.headers,proxies=proxies)
        return response.content

    # 提取数据
    def qu_url(self, html):
        html = etree.HTML(html)
        page_link = html.xpath("//ul[@class='list']/li/a[1]/@href")
        return page_link

    # 保存入裤
    def save_url(self, list):
        db = pymysql.connect(self.db_host, self.db_user, self.db_password, self.db_name, charset=self.db_charset,
                             port=self.db_port)
        cursor = db.cursor()
        for link in list:
            print(link)
            try:
                sql = "INSERT INTO zhesheji_links (link) VALUES('%s')" % (self.base_url + link)
                cursor.execute(sql)
            except Exception as e:
                print("失败的链接:", link)
                db.rollback()
            else:
                db.commit()
        cursor.close()
        db.close()

    def send_xpath_save(self):
        url = self.url_que.get()
        # 发送请求 接受相应
        html = self.pare_url(url)
        # 提取数据
        list = self.qu_url(html)
        # 保存入库
        self.save_url(list)

    # 循环函数
    def _callback(self, temp):
        if self.is_runing == True:
            self.pool.apply_async(self.send_xpath_save, callback=self._callback)

    # 主逻辑
    def run(self):
        # 获取url
        self.get_url()
        for i in range(1000):
            # 调用新函数
            self.pool.apply_async(self.send_xpath_save, callback=self._callback)
        # 判断执行结束
        while True:
            time.sleep(0.0001)
            if self.response_url == self.requests_url:
                self.is_runing = False
                break


if __name__ == '__main__':
    start_time = time.time()
    duan = zhisheji()
    duan.run()
    end_time = time.time()
    print('耗时：{}'.format(end_time - start_time))
