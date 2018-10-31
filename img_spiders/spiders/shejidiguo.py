# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re

from img_spiders.items import SheJiDiGuo


class ShejidiguoSpider(scrapy.Spider):
    name = 'shejidiguo'
    allowed_domains = ['www.warting.com']
    headers = {
        "Referer": "http://www.warting.com/"
    }

    def start_requests(self):
        start_urls = ["http://www.warting.com/gallery/list_{}.html".format(i) for i in range(1, 856)]
        for url in start_urls:
            yield Request(url, headers=self.headers)

    def parse(self, response):
        base_url = "http://www.warting.com"
        page_list = response.xpath("//div[@class='pic_list']//a[@class='pic']/@href").extract()
        for page in page_list:
            yield Request(base_url + page, callback=self.parse_detail, meta={
                "link": base_url + page
            })

    def parse_detail(self, response):
        link = response.meta.get("link")

        page_num = response.xpath("//div[@class='page']//span[@class='pageinfo']/text()").extract_first()
        links_list = []
        if page_num:
            a = response.url.rsplit(".", 1)
            a.insert(1, "_{}.")
            base_url = "".join(a)
            page_num = re.findall(r'^共(.*?)页$', page_num)[0]
            links_list = [base_url.format(i) for i in range(2, int(page_num) + 1)]
        links_list.append(link)
        for  link in links_list:
            item = SheJiDiGuo()
            item['link'] = link
            yield item
