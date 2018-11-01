import json
import re

import requests
import uuid
from lxml import etree
from qiniu import Auth, BucketManager

access_key = 'Uon2lwH6FDLYBhVyGu5jN25PwVCQuNAIf-_PaQ8E'
secret_key = '1psRA7q7FUow3JdRl-Kii6TmWUEL2aez3t2wDr3K'
bucket_name = 'lingan-img'
q = Auth(access_key, secret_key)
bucket = BucketManager(q)

def save(title, ctime, info1, tags, pic, link, db):
    pic = 'http://img.warting.com/allimg/2011/0716/24-110G61TJ8.jpg'
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
            sql = "INSERT INTO shejidiguo (title,tags,cdn_path,width,height,size,format,plate_type,info1,link,ctime,hash) " \
                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (title, tags, key, width, height, size, formats, plate_type, info1, link, ctime, hs)
            cursor.execute(sql, args)
            sql = "DELETE FROM zhesheji_links WHERE link = '%s'" % (link)
            cursor.execute(sql)
        except Exception as e:
            print('Insert Error：', e, link, sql)
            db.rollback()
        else:
            db.commit()
    except:
        print("上传失败链接:" + link)
    return None

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    "Referer": "http://www.warting.com/gallery/"
}

response = requests.get(url='http://www.warting.com/gallery/201107/31744_2.html', headers=headers)
html = response.content
tree = etree.HTML(html)
title = tree.xpath("//div[@class='mainleft']//h1/text()")
pics = tree.xpath("//div[@class='mainleft']//ul[@class='picshow_first']//img/@src")
info = tree.xpath("//div[@class='auto location']//a[last()]/text()")
tags = tree.xpath("//div[@class='article_tags']//a/text()")
ctime = tree.xpath("//div[@class='article_info']//li[@class='time']/text()")

if info:
    infos = info[0].split("/")
    info1 = infos[0]
    tags.extend(infos)
else:
    info1 = ""

if title:
    title = title[0]
else:
    title = ''
if tags:
    tags = ','.join(tags)
else:
    tags = ''

if ctime:
    ctime = "".join(ctime).split()[1]
else:
    ctime = '0000-00-00 00:00:00'

if pics:
    for pic in pics:
        pic = pic.rsplit("?")[0]
        print(title, ctime, info1, tags, pic)

if __name__ == '__main__':
    pic = 'http://img.warting.com/allimg/2017/0724/56-1FH40T946-51.jpg'
    ext = pic.split('.')
    if ext:
        ext = '.' + ext[-1]
    else:
        ext = '.jpg'
    struuid = str(uuid.uuid1()) + ext
    key = 'pic/' + struuid
    print("开始保存图片：", pic)
    ret, info = bucket.fetch(pic, bucket_name, key)
    assert ret['key'] == key
    hs = json.loads(info.text_body, encoding="utf-8")['hash']
    url = "http://img.aiji66.com/{}?imageInfo".format(key)
    response = requests.get(url=url)
    result = response.json()
    width = result['width']
    height = result['height']
    size = result['size']
    formats = result['format']
    print(key, width, height, size, formats)
