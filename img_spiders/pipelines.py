# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
class MysqlTwistedPipline(object):
    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool("pymysql", **spider.settings.get('MYSQLINFO'),cursorclass=pymysql.cursors.DictCursor)

    # 使用twisted将mysql插入变成异步执行
    def process_item(self, item, spider):
        # 指定操作方法和操作的数据
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 指定异常处理方法
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = self.get_insert_sql(item)
        cursor.execute(insert_sql, params)
        print("链接地址保存成功:", item['link'])

    def get_insert_sql(self,item):
        insert_sql = """
                     INSERT INTO shejizhijia_links (link) VALUES(%s);
                 """
        params = (
            item['link'])
        return insert_sql, params


