import requests
from lxml import etree
import re
import json

if __name__ == '__main__':
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }

    response = requests.get('https://www.uplabs.com/posts/c/all/resources/animation.json?p=3340', headers=headers)
    pages_list = response.json()

    for page in pages_list:
        # 文章地址
        link = page.get('link_url', '')
        # 标题
        title = page.get('name', '')
        # 图片地址
        preview_url = [page['preview_url']]
        # 标签
        tag = page.get('label', '')
        subcategory_friendly_name = page.get('subcategory_friendly_name', '')
        tag = "{},{}".format(tag, subcategory_friendly_name)

        # 附属图片地址
        imgs = list()
        for image in page.get('images', []):
            imgs.append(image['urls']['full'])
        preview_url.extend(imgs)
        # 来源
        source_name = page.get('source_name', '')
        # 时间
        showcased_at = page.get('showcased_at', '')
        ctime = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})', showcased_at)[0]
        print(link, title, preview_url, tag, source_name, ctime)
