# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Request

from img_spiders.items import UplabsItem


class UplabsSpider(scrapy.Spider):
    name = 'uplabs'
    allowed_domains = ['www.uplabs.com']

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }

    def start_requests(self):
        start_urls = ['https://www.uplabs.com/posts/c/all/resources']
        for start_url in start_urls:
            yield Request(start_url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        base_url = "https://www.uplabs.com{}"
        Categories = response.xpath(
            "//div[@class='col-md-2']/div[1]/@data-react-props").extract_first()
        dict_categories = json.loads(Categories, encoding='utf-8')
        for dict_category in dict_categories['items']:
            url = dict_category.get('url', '')
            category = dict_category.get('title', '')
            count = dict_category.get('count', 0)
            yield Request(url=base_url.format(url), callback=self.parse_list,
                          meta={"category": category, "count": count})

    def parse_list(self, response):
        list_url = response.url + ".json?p={}"
        # 分类信息
        category = response.meta.get('category', '')
        count = response.meta.get('count', 0)
        if count != 0:
            page_num_count = (count // 4) + 1
            for page_num in range(1, page_num_count + 1):
                url = list_url.format(page_num)
                item = UplabsItem()
                item['link'] = url
                item['category'] = category
                yield item
                # print(url)
                # yield Request(url, callback=self.parse_detail, meta={"category": category})

    # def parse_detail(self, response):
    #     pages_list = json.loads(response.body_as_unicode())
    #     for page in pages_list:
    #         # 文章地址
    #         link = page.get('link_url', '')
    #         # 标题
    #         title = page.get('name', '')
    #         # 图片地址
    #         preview_url = [page['preview_url']]
    #         # 标签
    #         tag = page.get('label', '')
    #         subcategory_friendly_name = page.get('subcategory_friendly_name', '')
    #         tag = "{},{}".format(tag, subcategory_friendly_name)
    #
    #         # 附属图片地址
    #         imgs = list()
    #         for image in page.get('images', []):
    #             imgs.append(image['urls']['full'])
    #         preview_url.extend(imgs)
    #         # 来源
    #         source_name = page.get('source_name', '')
    #         # 时间
    #         showcased_at = page.get('showcased_at', '')
    #         ctime = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})', showcased_at)[0]
    # print(link, title, preview_url, tag, source_name, ctime)
