#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import request
from urllib import error
import re
import pymysql
import uuid
import datetime
import requests
from qiniu import Auth, BucketManager
import json
import threading
from lxml import etree
import http.client

# db_host = 'sh-cdb-1vh4kpv4.sql.tencentcdb.com'
db_host = '172.16.0.32'
db_user = 's1326_aiji66'
db_password = 'Su_s1326@aiji'
db_port = 3306
db_name = 'bizhi'
db_charset = 'utf8'

threadNum = 1000  # 开启线程个数
lock = threading.Lock()

access_key = 'Uon2lwH6FDLYBhVyGu5jN25PwVCQuNAIf-_PaQ8E'
secret_key = '1psRA7q7FUow3JdRl-Kii6TmWUEL2aez3t2wDr3K'
bucket_name = 'lingan-img'
q = Auth(access_key, secret_key)
bucket = BucketManager(q)

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "H2A014240346U1KD"
proxyPass = "135EBB86283DE442"

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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    "Referer": "http://www.warting.com/gallery/"
}

def save(title, ctime, tags, info1, info2, info3, pic, link, db):
    cursor = db.cursor()
    ext = pic.split('.')
    if ext:
        ext = '.' + ext[-1]
    else:
        ext = '.jpg'
    struuid = str(uuid.uuid1()) + ext
    key = 'pic/' + struuid
    try:
        print("开始保存图片：", pic)
        ret, info = bucket.fetch(pic, bucket_name, key)
        assert ret['key'] == key
        print("保存成功",pic)
        hs = json.loads(info.text_body, encoding="utf-8")['hash']
        url = "http://img.aiji66.com/{}?imageInfo".format(key)
        response = requests.get(url=url)
        result = response.json()
        width = result['width']
        height = result['height']
        size = result['size']
        formats = result['format']
        if width > height:
            plate_type = 1
        if width < height:
            plate_type = 2
        if width == height:
            plate_type = 3
        try:
            sql = "INSERT INTO shejizhijia (title,tags,cdn_path,width,height,size,format,plate_type,info1,info2,info3,link,ctime,hash) " \
                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (title, tags, key, width, height, size, formats, plate_type, info1, info2,info3,link, ctime, hs)
            cursor.execute(sql, args)
            sql = "DELETE FROM shejizhijia_links WHERE link = '%s'" % (link)
            cursor.execute(sql)
        except Exception as e:
            print('Insert Error：', e, link, sql)
            db.rollback()
        else:
            db.commit()
    except Exception as e:
        print("上传失败链接:" ,link,e)
    return None


def open_link():
    db = pymysql.connect(db_host, db_user, db_password, db_name, charset=db_charset, port=db_port)
    global start
    while True:
        try:
            link = next(start)
            print("爬取：" + link)
            response = requests.get(url=link, headers=headers)
            try:
                html = response.content.decode()
                tree = etree.HTML(html)
                title = tree.xpath("//div[@class='articlebox']/h1/text()")
                pics = tree.xpath("//div[@class='articlebox']/div[@class='artcon']//img/@src")
                info = tree.xpath("//div[@id='loat6']/a[position()>1]/text()")
                tags = tree.xpath("//div[@class='zuozhe1']/a/text()")
                ctime = tree.xpath("//div[@class='zuozhe1']/text()")

                if info:
                    keys = ["info1", "info2", "info3"]
                    infos = dict(zip(keys, info))
                    info1 = infos.get('info1', '')
                    info2 = infos.get('info2', '')
                    info3 = infos.get('info3', '')
                    tags.extend(info)
                else:
                    info1 = ""
                    info2 = ""
                    info3 = ""

                if title:
                    title = title[0]
                else:
                    title = ''
                if tags:
                    tags = ','.join(tags)
                else:
                    tags = ''

                if ctime:
                    ctime = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})', ctime[0])[0]
                else:
                    ctime = '0000-00-00 00:00:00'

                if pics:
                    for pic in pics:
                        pic = pic.rsplit("?")[0]
                        save(title, ctime, tags, info1, info2, info3, pic,link, db)
            except Exception as e:
                print("Error：", e, threading.current_thread().name)
        except StopIteration as e:
            print('Generator return value:', e.value, threading.current_thread().name)
            break


def main():
    db = pymysql.connect(db_host, db_user, db_password, db_name, charset=db_charset, port=db_port)
    cursor = db.cursor()
    sql = "SELECT link FROM shejizhijia_links order by id asc "
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    global start
    start = (x[0] for x in result)
    for threads in range(threadNum):
        t = threading.Thread(target=open_link)
        t.start()


if __name__ == '__main__':
    main()
