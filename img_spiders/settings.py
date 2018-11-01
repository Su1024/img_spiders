# -*- coding: utf-8 -*-

# Scrapy settings for img_spiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

BOT_NAME = 'img_spiders'

SPIDER_MODULES = ['img_spiders.spiders']
NEWSPIDER_MODULE = 'img_spiders.spiders'

LOG_LEVEL = "WARNING"

# Crawl responsibly by identifying yourself (and your website) on the user-agent

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 500

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 500
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'accept':'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'www.sj33.cn',
    'Cookie': 'UM_distinctid=166ce35b4b4167-0861c8679518cc-b79193d-1fa400-166ce35b4bb321; Hm_lvt_32bdb1892164631690e25a7c7a5fd2f6=1541057918,1541059067; CNZZDATA30089843=cnzz_eid%3D537325359-1541056540-null%26ntime%3D1541056540; __51cke__=; __tins__16734211=%7B%22sid%22%3A%201541059111401%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201541061000015%7D; __51laig__=2; Hm_lpvt_32bdb1892164631690e25a7c7a5fd2f6=1541060493; CNZZDATA30058505=cnzz_eid%3D703386626-1541054805-%26ntime%3D1541060208',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'img_spiders.middlewares.ImgSpidersSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
#     'img_spiders.middlewares.ProxyMiddleware': 100
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'img_spiders.pipelines.MysqlTwistedPipline': 25,
}

# mysql 配置

MYSQLINFO = {
    'db': 'bizhi',
    'host': '172.16.0.32',
    'user': 's1326_aiji66',
    'passwd': 'Su_s1326@aiji',
    'charset': 'utf8'
}


# Ensure use this Scheduler
# SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# # Ensure all spiders share same duplicates filter through redis
# DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
#
# # Redis URL
# REDIS_URL = 'redis://127.0.0.1:6379'
#
# # Number of Hash Functions to use, defaults to 6
# BLOOMFILTER_HASH_NUMBER = 8
#
# # Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
# BLOOMFILTER_BIT = 30
#
# # Persist
# SCHEDULER_PERSIST = True

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
