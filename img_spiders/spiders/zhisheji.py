# -*- coding: utf-8 -*-
import datetime
import json
import re
import uuid

import requests
import scrapy
from qiniu import Auth, BucketManager
from scrapy import Request

from img_spiders.items import ImgSpidersItem


class ZhishejiSpider(scrapy.Spider):
    name = 'zhisheji'
    allowed_domains = ['www.zhisheji.com']
    start_num = 0
    headers = {
        "Referer": "http://www.zhisheji.com/yuanchuang/dianpu/"
    }

    def __init__(self):
        self.access_key = 'fid6x1_ScoclezQaxV3Xq0oK1hXxvDTUGgCyJfaa'
        self.secret_key = 'K1fzpWGjVBOgxkfIQ4zzV_Ji1PqK8-8HWckaa6HT'
        self.bucket_name = 'imgs'
        q = Auth(self.access_key, self.secret_key)
        self.bucket = BucketManager(q)

    def start_requests(self):
        start_urls = ["http://www.zhisheji.com/yuanchuang/"]
        for url in start_urls:
            yield Request(url, headers=self.headers)

    def parse(self, response):
        self.start_num += 1
        print("页码", self.start_num, "*" * 50)
        base_url = "http://www.zhisheji.com"
        page_url_list = response.xpath("//ul[@class='list']/li/a[1]/@href").extract()
        for url in page_url_list:
            yield Request(base_url + url, callback=self.parse_detail)

        next_url = response.xpath(
            "//div[@class='page-list page-gray']//a[last()]/text()").extract_first()

        if next_url == '下一页':
            url = response.xpath("//div[@class='page-list page-gray']//a[last()]/@href").extract_first()
            yield Request(base_url + url, callback=self.parse, headers=self.headers)

    def parse_detail(self, response):
        title = response.xpath("//div[@class='content-tit']//h1/text()").extract_first()
        pics = response.xpath('//div[@class="cpimgbox"]/img/@data-path').extract()
        info = response.xpath("//div[@class='content-tit']//div[@class='times']/a[2]/text()").extract()
        view_num = response.xpath("//div[@class='content-tit']//div[@class='infos']/em[1]/text()").extract_first()
        tags = response.xpath("//div[@class='wrap ct-tip']//div[@class='tag']/a/text()").extract()

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

        if view_num:
            view_num = re.sub("[^0-9]", "", view_num[0])
        else:
            view_num = "0"

        ctime = ""

        if pics:
            pics = "||".join(pics).replace('?imageMogr2/quality/90', '').split('||')
            ctime = re.findall(r'^http://img.zhisheji.com/(.*?)$', pics[0])[0][0:8]

        if ctime:
            try:
                ctime = datetime.datetime.strptime(ctime, "%Y%m%d").strftime("%Y-%m-%d")
            except:
                ctime = '0000-00-00 00:00:00'
        else:
            ctime = '0000-00-00 00:00:00'

        img_dict = dict()
        img_dict['title'] = title
        img_dict['pics'] = pics
        img_dict['ctime'] = ctime
        img_dict['info1'] = info1
        img_dict['view_num'] = view_num
        img_dict['tags'] = tags
        img_dict['link'] = response.url

        for pic in pics:
            ext = pic.split('.')
            if ext:
                ext = '.' + ext[-1]
            else:
                ext = '.jpg'
            struuid = str(uuid.uuid1()) + ext
            key = 'pic/' + struuid
            print("开始上传图片:", pic)
            ret, info = self.bucket.fetch(pic, self.bucket_name, key)
            assert ret['key'] == key
            print("上传成功图片:", pic)
            hs = json.loads(info.text_body, encoding="utf-8")['hash']
            yield Request(url='https://www.baidu.com', callback=self.paser_img_info)

    def paser_img_info(self, response):
        print("1" * 1000)
        # result = response.json()
        # width = result['width']
        # height = result['height']
        # size = result['size']
        # formats = result['format']
        # if width > height:
        #     plate_type = 1
        # if width < height:
        #     plate_type = 2
        # if width == height:
        #     plate_type = 3
        # img_item = ImgSpidersItem()
        # img_dict = response.meta.get('img_dict')
        #
        # img_item['title'] = img_dict.get("title")
        # img_item['pics'] = img_dict.get("pics")
        # img_item['ctime'] = img_dict.get("ctime")
        # img_item['info1'] = img_dict.get("info1")
        # img_item['view_num'] = img_dict.get("view_num")
        # img_item['tags'] = img_dict.get("tags")
        # img_item['width'] = width
        # img_item['height'] = height
        # img_item['size'] = size
        # img_item['formats'] = formats
        # img_item['plate_type'] = plate_type
        # print(img_item)
