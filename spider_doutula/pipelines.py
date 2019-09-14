# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi


class SpiderDoutulaPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **params)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self,item,spider):
        # if spider.name not in self.dbpool.table_names(): #create table for this spider
        #     self.Picture.metadata.create_all(self.dbpool)
        query = self.dbpool.runInteraction(self.insert_into, item)

    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = 'INSERT INTO picture_tag (pic_url,tags) VALUES ("%s","%s");' % (item['pic_url'], item['tags'])
        print('[sql]:%s' % sql)
        # 执行sql语句
        cursor.execute(sql)

    def handle_error(self, failure, item, spider):
        # 错误信息
        print(failure)




