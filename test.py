import re
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    "Host": "www.sj33.cn"
}

response = requests.get(url="http://www.sj33.cn/article/bssj/200801/13832.html", headers=headers)

html = response.content.decode('utf-8')
tree = etree.HTML(html)
title = tree.xpath("//div[@class='articlebox']/h1/text()")
pics = tree.xpath("//div[@class='articlebox']/div[@class='artcon']//img/@src")
info = tree.xpath("//div[@id='loat6']/a[position()>1]/text()")
tags = tree.xpath("//div[@class='zuozhe1']/a/text()")
ctime = tree.xpath("//div[@class='zuozhe1']/text()")

if info:
    keys = ["info1", "info2", "info3"]
    infos = dict(zip(keys, info))
    info1 = infos.get('info1','')
    info2 = infos.get('info2','')
    info3 = infos.get('info3','')
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
        print(title, ctime, tags,info1,info2,info3, pic)
