# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request


class Design68Spider(Spider):
    name = 'design68'
    allowed_domains = ['www.68design.net']
    heders = {
        "Host": "www.68design.net",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
        "Connection": "keep-alive",
        "Referer": "http://www.68design.net/"
    }

    def start_requests(self):
        start_urls = ["http://www.warting.com/gallery/list_{}.html".format(i) for i in range(1, 856)]
        for url in start_urls:
            yield Request(url, headers=self.headers)

    def parse(self, response):
        pass
