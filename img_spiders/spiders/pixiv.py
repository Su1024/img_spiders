# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest


class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    allowed_domains = ['accounts.pixiv.net', 'www.pixiv.net']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Referer': 'https://www.pixiv.net/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'
    }

    def start_requests(self):
        yield Request("https://www.pixiv.net/", headers=self.headers, meta={'cookiejar': 1}, callback=self.post_login)

    def post_login(self, response):
        print(1)
        post_key = response.xpath("//div[@id='old-login']//input[@name='post_key']/@value").extract_first()
        print(post_key)
        post_data = {
            "pixiv_id": "1059692428@163.com",
            "captcha": "",
            "g_recaptcha_response": "",
            "password": "SUU2429317",
            "post_key": post_key,
            "source": "pc",
            "ref": "wwwtop_accounts_index",
            "return_to": "https://www.pixiv.net/"
        }
        yield FormRequest.from_response(response, formdata=post_data, headers=self.headers, callback=self.after_login)

    def after_login(self, response):
        usename = response.xpath("//div[@class='user-name-container']/a/text()").extract_first()
        print(usename)
