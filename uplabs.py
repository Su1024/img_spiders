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

threadNum = 1  # 开启线程个数
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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
}


def save(title, ctime, tags, pic, source, link, db, page_url):
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
        print("保存成功", pic)
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
            sql = "select * from uplabs_links where link = %s "
            args = (page_url,)
            cursor.execute(sql, args)
            info1 = cursor.fetchall()[0][2]
            sql = "INSERT INTO uplabs (title,tags,cdn_path,width,height,size,format,plate_type,info1,source,link,ctime,hash) " \
                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (title, tags, key, width, height, size, formats, plate_type, info1, source, link, ctime, hs)
            cursor.execute(sql, args)
        except Exception as e:
            print('Insert Error：', e, link, sql)
            db.rollback()
        else:
            db.commit()
    except Exception as e:
        print("上传失败链接:", link, e)
    return None


def open_link():
    db = pymysql.connect(db_host, db_user, db_password, db_name, charset=db_charset, port=db_port)
    global start
    while True:
        try:
            link = next(start)
            print("爬取：" + link)
            response = requests.get(url=link, headers=headers)
            page_url = link
            try:
                pages_list = response.json()
                for page in pages_list:
                    # 文章地址
                    link = page.get('link_url', '')
                    # 标题
                    title = page.get('name', '')
                    # 图片地址
                    pic_list = [page['preview_url']]
                    # 标签
                    tag = page.get('label', '')
                    subcategory_friendly_name = page.get('subcategory_friendly_name', '')
                    tag_list = list()
                    tag_list.append(subcategory_friendly_name)
                    tag_list.append(tag)
                    tag = ",".join(tag_list)
                    # 附属图片地址
                    imgs = list()
                    for image in page.get('images', []):
                        imgs.append(image['urls']['full'])
                    pic_list.extend(imgs)
                    # 来源
                    source_name = page.get('source_name', '')
                    # 时间
                    showcased_at = page.get('showcased_at', '')
                    ctime = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})', showcased_at)[0]

                    if not ctime:
                        ctime = "0000-00-00 00:00:00"
                    for pic in pic_list:
                        save(title, ctime, tag, pic, source_name, link, db, page_url)
                else:
                    try:
                        cursor = db.cursor()
                        sql = "DELETE FROM uplabs_links WHERE link = '%s'" % (page_url)
                        cursor.execute(sql)
                    except Exception as e:
                        db.rollback()
                    else:
                        db.commit()
            except Exception as e:
                print("Error：", e, threading.current_thread().name)
        except StopIteration as e:
            print('Generator return value:', e.value, threading.current_thread().name)
            break


def main():
    db = pymysql.connect(db_host, db_user, db_password, db_name, charset=db_charset, port=db_port)
    cursor = db.cursor()
    sql = "SELECT link FROM uplabs_links order by id asc "
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
