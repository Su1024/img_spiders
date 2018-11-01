# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Spider, Request

from img_spiders.items import SheJiDiGuo


class ShejizhijiaSpider(Spider):
    name = 'shejizhijia'
    allowed_domains = ['www.sj33.cn']
    start_urls = ['http://www.sj33.cn/']
    base_url = 'http://www.sj33.cn{}'

    def parse(self, response):

        first_men_link_list = response.xpath(
            "//div[@id='mainnav']/ul/li[position()>2 and position()<11]/a/@href").extract()
        first_men_link_list.pop(5)
        for first_men_link in first_men_link_list:
            yield Request(self.base_url.format(first_men_link), callback=self.parse_send_men)

    def parse_send_men(self, response):
        send_men_link_list = []
        first_men_name = response.url.split("/")[-2]

        if first_men_name == "article":
            send_men_link_list = response.xpath(
                "//div[@class='type_map']/div[@class='right2']/a[position()<15]/@href").extract()

        elif first_men_name == "architecture":
            send_men_link_list = response.xpath("//div[@class='type_map']/div[@class='right2']/a/@href").extract()
            send_men_link_list.pop(4)
            send_men_link_list.pop(4)
        elif first_men_name == "digital":
            send_men_link_list = response.xpath(
                "//div[@class='type_map']/div[@class='right2']/a[position()<4]/@href").extract()
        elif first_men_name == "dphoto":
            send_men_link_list = response.xpath("//div[@class='type_map']/div[@class='right2']/a/@href").extract()
        elif first_men_name == "cg":
            send_men_link_list = response.xpath("//div[@class='type_map']/div[@class='right2']/a/@href").extract()
        elif first_men_name == "industry":
            send_men_link_list = response.xpath(
                "//div[@class='type_map']/div[@class='right2']/a[position()<6]/@href").extract()
        elif first_men_name == "ys":
            send_men_link_list = response.xpath("//div[@class='type_map']/div[@class='right2']/a/@href").extract()
            send_men_link_list.pop(3)
            send_men_link_list.pop(3)

        for send_men_link in send_men_link_list:
            url = self.base_url.format(send_men_link)
            yield Request(url, callback=self.parse_page_link,meta={"first_url":url})

    def parse_page_link(self, response):
        first_url = response.meta.get('first_url')
        print("--" * 30)
        print(response.url)
        page_links = response.xpath("//ul[@class='imglist2']/li/div[1]/a[1]/@href").extract()
        print(page_links)
        for page_link in page_links:
            item = SheJiDiGuo()
            item['link'] = self.base_url.format(page_link)
            print(item)

        next_url = response.xpath("//div[@class='showpage']/a[last()]/@href").extract_first()

        if next_url:
            print(first_url +"/"+ next_url)
            yield Request(first_url +"/"+ next_url, callback=self.parse_page_link,meta={"first_url":first_url})

if __name__ == '__main__':
    str="http://www.sj33.cn/article/visj/P2.html"
    print(str.rsplit('/'))



