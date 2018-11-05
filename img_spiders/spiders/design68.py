# -*- coding: utf-8 -*-
import json
import re

import uuid
from qiniu import Auth, BucketManager
from scrapy import Spider, Request

from img_spiders.items import ImgSpidersItem, SheJiDiGuo


class Design68Spider(Spider):
    name = 'design68'
    allowed_domains = ['www.68design.net', 'img.aiji66.com']
    headers = {
        "Host": "www.68design.net",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
        "Connection": "keep-alive",
        "Referer": "http://www.68design.net/"
    }

    def start_requests(self):
        start_urls = ["http://www.68design.net/work/?p={}".format(i) for i in range(1, 101)]
        for url in start_urls:
            yield Request(url, headers=self.headers)

    def parse(self, response):
        base_url = 'http://www.68design.net{}'
        link_list = response.xpath("//div[@class='works-info']//li/a/@href").extract()
        for link in link_list:
            item  = SheJiDiGuo()
            item['link'] = base_url.format(link)
            yield item

